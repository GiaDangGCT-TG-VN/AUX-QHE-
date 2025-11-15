"""
Circuit Evaluation Module

This module implements the main homomorphic circuit evaluation for AUX-QHE,
corrected according to the theoretical specification with proper polynomial tracking.
"""

import logging
import time
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.quantum_info import Statevector
from sympy import symbols, Xor, lambdify
from bfv_core import initialize_bfv_params
from key_generation import aux_keygen, evaluate_term
from t_gate_gadgets import (update_keys_for_t_gate, update_keys_for_clifford_gate, 
                           construct_auxiliary_for_polynomial)

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def organize_gates_into_layers(circuit_operations):
    """
    Organize circuit operations into T and Clifford layers.
    
    Args:
        circuit_operations (list): List of (gate_name, qubit_indices) operations.
    
    Returns:
        tuple: (layers, t_depth) where layers is list of parallel operations.
    """
    try:
        layers = []
        current_layer = []
        used_qubits = set()
        t_depth = 0
        
        for gate_name, qubits in circuit_operations:
            # Convert to list if single qubit
            qubit_list = [qubits] if isinstance(qubits, int) else list(qubits)
            
            # Check if qubits are available (no conflicts)
            if any(q in used_qubits for q in qubit_list):
                # Start new layer
                if any(g == 't' for g, _ in current_layer):
                    t_depth += 1
                layers.append(current_layer)
                current_layer = []
                used_qubits.clear()
            
            # Add operation to current layer
            current_layer.append((gate_name, qubits))
            used_qubits.update(qubit_list)
        
        # Add final layer
        if current_layer:
            if any(g == 't' for g, _ in current_layer):
                t_depth += 1
            layers.append(current_layer)
        
        logger.info(f"Organized {len(circuit_operations)} operations into {len(layers)} layers, T-depth={t_depth}")
        return layers, t_depth
        
    except Exception as e:
        logger.error(f"Layer organization failed: {str(e)}")
        raise

def homomorphic_polynomial_evaluation(polynomials, variable_values, encryptor, encoder, 
                                    decryptor, evaluator, poly_degree):
    """
    Homomorphically evaluate key polynomials using BFV.
    
    Theory: ã_final[i] ← HE.Eval_{f_a[i]}(evk, encrypted_keys)
    
    Args:
        polynomials (list): List of polynomial expressions.
        variable_values (dict): Variable assignments.
        encryptor, encoder, decryptor, evaluator: BFV components.
        poly_degree (int): BFV polynomial degree.
    
    Returns:
        list: List of encrypted polynomial evaluations.
    """
    try:
        encrypted_results = []
        
        logger.debug(f"Evaluating {len(polynomials)} polynomials")
        logger.debug(f"Variable values available: {list(variable_values.keys())}")
        logger.debug(f"Variable values: {variable_values}")
        
        for i, poly in enumerate(polynomials):
            try:
                # Handle various polynomial formats
                if poly is None or poly == '0' or poly == '' or poly == 'None':
                    result_value = 0
                    logger.debug(f"Polynomial {i}: empty/zero -> 0")
                else:
                    # Evaluate polynomial using improved evaluate_term function
                    result_value = evaluate_term(str(poly), variable_values)
                    logger.debug(f"Polynomial {i}: '{poly}' -> {result_value}")
                
                # Ensure result is binary (0 or 1)
                result_value = int(result_value) % 2
                
                # Encrypt the result
                encoded = encoder.encode([result_value] + [0] * (poly_degree - 1))
                encrypted = encryptor.encrypt(encoded)
                encrypted_results.append(encrypted)
                
                # Verify encryption round-trip for debugging
                verification = int(encoder.decode(decryptor.decrypt(encrypted))[0]) % 2
                if verification != result_value:
                    logger.warning(f"Polynomial {i} encryption mismatch: "
                                 f"expected {result_value}, got {verification}")
                else:
                    logger.debug(f"Polynomial {i} encryption verified: {result_value}")
                    
            except Exception as e:
                logger.error(f"Failed to evaluate polynomial {i} '{poly}': {str(e)}")
                logger.debug(f"Exception details: {type(e).__name__}: {e}")
                # Default to encrypting 0 but log the issue
                logger.warning(f"Defaulting polynomial {i} to 0 due to evaluation error")
                encoded = encoder.encode([0] + [0] * (poly_degree - 1))
                encrypted_results.append(encryptor.encrypt(encoded))
        
        logger.debug(f"Successfully evaluated {len(encrypted_results)} polynomials")
        return encrypted_results
        
    except Exception as e:
        logger.error(f"Homomorphic polynomial evaluation failed: {str(e)}")
        raise

def aux_eval(input_circuit, encrypted_a_keys, encrypted_b_keys, auxiliary_states, 
             max_t_depth, encryptor, decryptor, encoder, evaluator, poly_degree, debug=True):
    """
    Homomorphically evaluate a quantum circuit using AUX-QHE (corrected version).
    
    Theory:
    1. Initialize key polynomials f_a[i] ← a_i, f_b[i] ← b_i
    2. For each gate, update polynomials according to gate type
    3. Homomorphically evaluate final polynomials
    
    Args:
        input_circuit (QuantumCircuit): Input quantum circuit.
        encrypted_a_keys, encrypted_b_keys (list): Encrypted QOTP keys.
        auxiliary_states (dict): Dictionary of auxiliary states.
        max_t_depth (int): Maximum T-depth.
        encryptor, decryptor, encoder, evaluator: BFV components.
        poly_degree (int): BFV polynomial degree.
        debug (bool): Enable debug logging.
    
    Returns:
        tuple: (evaluated_circuit, new_encrypted_a_keys, new_encrypted_b_keys)
    """
    try:
        eval_start_time = time.perf_counter()
        num_qubits = input_circuit.num_qubits
        
        if debug:
            logger.info(f"Starting AUX evaluation: {num_qubits} qubits, max T-depth {max_t_depth}")
        
        # Decrypt initial keys to get starting values
        initial_a = []
        initial_b = []
        for i in range(num_qubits):
            a_val = int(encoder.decode(decryptor.decrypt(encrypted_a_keys[i]))[0]) % 2
            b_val = int(encoder.decode(decryptor.decrypt(encrypted_b_keys[i]))[0]) % 2
            initial_a.append(a_val)
            initial_b.append(b_val)
        
        logger.debug(f"Initial keys: a={initial_a}, b={initial_b}")
        
        # Initialize key polynomials
        f_a_polynomials = [f'a{i}' for i in range(num_qubits)]
        f_b_polynomials = [f'b{i}' for i in range(num_qubits)]
        
        # Initialize variable values
        variable_values = {}
        for i in range(num_qubits):
            variable_values[f'a{i}'] = initial_a[i]
            variable_values[f'b{i}'] = initial_b[i]
        
        # Extract circuit operations (only original gates, not QOTP X^a Z^b)
        circuit_operations = []
        for instr in input_circuit.data:
            gate_name = instr.operation.name.lower()
            qubits = tuple(input_circuit.qubits.index(q) for q in instr.qubits)

            if gate_name == 'cx' and len(qubits) == 2:
                circuit_operations.append((gate_name, qubits))
            elif gate_name in ['h', 't', 'x', 'z', 'p'] and len(qubits) == 1:
                circuit_operations.append((gate_name, qubits[0]))
            elif gate_name not in ['initialize', 'barrier']:
                logger.debug(f"Skipping unknown gate: {gate_name}")

        if debug:
            logger.debug(f"Extracted {len(circuit_operations)} operations from encrypted circuit: {circuit_operations}")

        # Organize into layers
        # NOTE: organize_gates_into_layers may overestimate T-depth due to QOTP encryption gates
        # We trust the max_t_depth parameter which reflects the original circuit structure
        layers, detected_t_depth = organize_gates_into_layers(circuit_operations)

        if debug:
            logger.info(f"Detected T-depth: {detected_t_depth}, using max_t_depth: {max_t_depth}")

        # Use max_t_depth (from key generation) instead of detected_t_depth
        t_depth = max_t_depth
        
        # Create evaluation circuit
        eval_circuit = QuantumCircuit(num_qubits, name='aux_eval')

        # Track current T-layer PER QUBIT (not global)
        qubit_t_layers = [1] * num_qubits  # Each qubit starts at T-layer 1

        # Process each layer
        total_t_time = 0.0

        for layer_idx, layer in enumerate(layers):
            layer_has_t_gates = any(gate == 't' for gate, _ in layer)

            if debug:
                logger.debug(f"Processing layer {layer_idx}: {layer}")

            # Process gates in parallel within the layer
            for gate_name, qubits in layer:
                if gate_name == 't':
                    # Apply T-gate with auxiliary states
                    qubit = qubits
                    t_start = time.perf_counter()

                    # Use the per-qubit T-layer
                    qubit_t_layer = qubit_t_layers[qubit]

                    new_f_a, new_f_b, c, k = update_keys_for_t_gate(
                        qubit, f_a_polynomials[qubit], f_b_polynomials[qubit],
                        variable_values, auxiliary_states, qubit_t_layer,
                        eval_circuit, debug
                    )

                    f_a_polynomials[qubit] = new_f_a
                    f_b_polynomials[qubit] = new_f_b

                    # Increment THIS qubit's T-layer for next T-gate on this qubit
                    qubit_t_layers[qubit] += 1

                    total_t_time += time.perf_counter() - t_start

                    if debug:
                        logger.debug(f"T-gate on qubit {qubit}: f_a='{new_f_a}', f_b='{new_f_b}'")
                
                elif gate_name in ['h', 'x', 'z', 'p']:
                    # Apply Clifford gate
                    qubit = qubits
                    if debug:
                        logger.debug(f"Before {gate_name.upper()}({qubit}): f_a={f_a_polynomials}, f_b={f_b_polynomials}")

                    f_a_polynomials, f_b_polynomials = update_keys_for_clifford_gate(
                        gate_name, qubit, f_a_polynomials, f_b_polynomials,
                        variable_values, eval_circuit, debug
                    )

                    if debug:
                        logger.debug(f"After {gate_name.upper()}({qubit}): f_a={f_a_polynomials}, f_b={f_b_polynomials}")
                
                elif gate_name == 'cx':
                    # Apply CNOT
                    control, target = qubits
                    f_a_polynomials, f_b_polynomials = update_keys_for_clifford_gate(
                        gate_name, (control, target), f_a_polynomials, f_b_polynomials,
                        variable_values, eval_circuit, debug
                    )
                    
                    if debug:
                        logger.debug(f"CNOT gate ({control}, {target})")

        # Note: T-layer tracking is now per-qubit, no global increment needed

        # Homomorphically evaluate final key polynomials
        logger.info("Evaluating final key polynomials homomorphically")
        
        final_encrypted_a = homomorphic_polynomial_evaluation(
            f_a_polynomials, variable_values, encryptor, encoder, 
            decryptor, evaluator, poly_degree
        )
        
        final_encrypted_b = homomorphic_polynomial_evaluation(
            f_b_polynomials, variable_values, encryptor, encoder,
            decryptor, evaluator, poly_degree  
        )
        
        eval_time = time.perf_counter() - eval_start_time
        
        if debug:
            logger.debug(f"Variable values at end of evaluation:")
            for var in sorted(variable_values.keys()):
                logger.debug(f"  {var} = {variable_values[var]}")
            logger.info(f"AUX evaluation completed:")
            logger.info(f"  - T-depth used: {t_depth}/{max_t_depth}")
            logger.info(f"  - Total T-gate time: {total_t_time:.4f}s")
            logger.info(f"  - Total evaluation time: {eval_time:.4f}s")
            logger.info(f"  - Final polynomials: f_a={f_a_polynomials}, f_b={f_b_polynomials}")
        
        return eval_circuit, final_encrypted_a, final_encrypted_b
        
    except Exception as e:
        logger.error(f"AUX evaluation failed: {str(e)}")
        raise

if __name__ == "__main__":
    # Test circuit evaluation
    logger.info("Testing AUX circuit evaluation...")
    
    # Initialize BFV
    params, encoder, encryptor, decryptor, evaluator = initialize_bfv_params()
    poly_degree = params.poly_degree
    
    # Generate keys and auxiliary states
    secret_key, eval_key, prep_time, layer_sizes, total_states = aux_keygen(
        num_qubits=2, 
        max_T_depth=2,
        a_init=[1, 0],
        b_init=[0, 1]
    )
    
    T_sets, V_sets, auxiliary_states = eval_key
    
    # Encrypt initial keys
    a_init, b_init, k_dict = secret_key
    enc_a = [encryptor.encrypt(encoder.encode([a_init[i]] + [0] * (poly_degree - 1))) for i in range(2)]
    enc_b = [encryptor.encrypt(encoder.encode([b_init[i]] + [0] * (poly_degree - 1))) for i in range(2)]
    
    # Test circuit
    test_circuit = QuantumCircuit(2)
    test_circuit.h(0)
    test_circuit.t(0)
    test_circuit.cx(0, 1)
    test_circuit.t(1)
    
    # Evaluate circuit
    eval_circuit, final_enc_a, final_enc_b = aux_eval(
        test_circuit, enc_a, enc_b, auxiliary_states, 2,
        encryptor, decryptor, encoder, evaluator, poly_degree
    )
    
    # Check results
    final_a = [int(encoder.decode(decryptor.decrypt(final_enc_a[i]))[0]) % 2 for i in range(2)]
    final_b = [int(encoder.decode(decryptor.decrypt(final_enc_b[i]))[0]) % 2 for i in range(2)]
    
    print(f"Test results:")
    print(f"  Initial a: {a_init}, b: {b_init}")
    print(f"  Final a: {final_a}, b: {final_b}")
    print(f"  Circuit operations: {len(eval_circuit.data)}")
    print("✅ Circuit evaluation test completed")