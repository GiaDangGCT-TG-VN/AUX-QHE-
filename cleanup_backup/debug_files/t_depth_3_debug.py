#!/usr/bin/env python3
"""
Debug T-depth 3 issue in AUX-QHE algorithm.
Compare working T-depth 2 vs failing T-depth 3.
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, state_fidelity

# Import AUX-QHE modules
from bfv_core import initialize_bfv_params
from key_generation import aux_keygen
from qotp_crypto import qotp_encrypt, qotp_decrypt
from circuit_evaluation import aux_eval

def create_test_circuit(num_qubits, max_t_depth):
    """Create test circuit with specified T-depth."""
    circuit = QuantumCircuit(num_qubits)
    circuit.h(0)  # Hadamard
    if num_qubits > 1:
        circuit.cx(0, 1)  # CNOT
    circuit.t(0)  # First T-gate
    if max_t_depth > 1:
        for layer in range(max_t_depth - 1):
            qubit_idx = min(layer + 1, num_qubits - 1) if num_qubits > 1 else 0
            circuit.t(qubit_idx)
    return circuit

def debug_t_depth_issue(num_qubits, working_depth, failing_depth):
    """Compare working vs failing T-depth configurations."""
    print(f"\n{'='*70}")
    print(f"DEBUGGING T-DEPTH ISSUE: {num_qubits}q")
    print(f"Working: T-depth {working_depth}, Failing: T-depth {failing_depth}")
    print(f"{'='*70}")

    # Common setup
    params, encoder, encryptor, decryptor, evaluator = initialize_bfv_params()
    poly_degree = params.poly_degree

    base_a = [1, 0, 1, 1, 0, 1, 0, 1, 1, 0]
    base_b = [0, 1, 0, 1, 1, 0, 1, 0, 0, 1]
    a_init = base_a[:num_qubits]
    b_init = base_b[:num_qubits]

    results = {}

    for depth_name, t_depth in [("WORKING", working_depth), ("FAILING", failing_depth)]:
        print(f"\n🔍 Testing {depth_name} (T-depth {t_depth}):")
        print("-" * 50)

        try:
            # Generate keys
            secret_key, eval_key, aux_prep_time, layer_sizes, total_aux_states = aux_keygen(
                num_qubits, t_depth, a_init, b_init
            )
            T_sets, V_sets, auxiliary_states = eval_key

            print(f"Auxiliary states: {total_aux_states}")
            print(f"Layer sizes: {layer_sizes}")
            print(f"T_sets keys: {list(T_sets.keys())}")

            # Show detailed T_sets for analysis
            for layer in T_sets:
                print(f"  T[{layer}] size: {len(T_sets[layer])}")
                if len(T_sets[layer]) <= 10:  # Show content for small sets
                    print(f"    Content: {T_sets[layer]}")
                else:
                    print(f"    Sample: {T_sets[layer][:5]}...")

            # Create circuit
            original_circuit = create_test_circuit(num_qubits, t_depth)
            print(f"Circuit gates: {[instr.operation.name for instr in original_circuit.data]}")

            # Get ideal state
            ideal_statevector = Statevector.from_instruction(original_circuit)
            ideal_probs = ideal_statevector.probabilities()

            # QOTP encrypt
            encrypted_circuit, d, enc_a, enc_b = qotp_encrypt(
                original_circuit, a_init, b_init, 0, num_qubits + 2,
                encryptor, encoder, decryptor, poly_degree
            )

            # Homomorphic evaluation with detailed logging
            print(f"Starting homomorphic evaluation...")
            eval_circuit, final_enc_a, final_enc_b = aux_eval(
                encrypted_circuit, enc_a, enc_b, auxiliary_states, t_depth,
                encryptor, decryptor, encoder, evaluator, poly_degree, debug=True
            )

            # QOTP decrypt
            decrypted_circuit = qotp_decrypt(
                eval_circuit, final_enc_a, final_enc_b, decryptor, encoder, poly_degree
            )

            # Calculate fidelity
            decrypted_clean = decrypted_circuit.copy()
            decrypted_clean.remove_final_measurements(inplace=True)
            decrypted_statevector = Statevector.from_instruction(decrypted_clean)
            decrypted_probs = decrypted_statevector.probabilities()
            fidelity = state_fidelity(ideal_statevector, decrypted_statevector)

            print(f"Ideal probabilities (first 4): {ideal_probs[:4]}")
            print(f"Decrypted probabilities (first 4): {decrypted_probs[:4]}")
            print(f"🎯 FIDELITY: {fidelity:.6f}")

            results[depth_name] = {
                'fidelity': fidelity,
                'layer_sizes': layer_sizes,
                'total_aux_states': total_aux_states,
                'T_sets': T_sets,
                'ideal_probs': ideal_probs,
                'decrypted_probs': decrypted_probs,
                'circuit_gates': [instr.operation.name for instr in original_circuit.data],
                'success': fidelity > 0.8
            }

        except Exception as e:
            print(f"❌ Error in {depth_name}: {e}")
            import traceback
            traceback.print_exc()
            results[depth_name] = {'success': False, 'error': str(e)}

    return results

def analyze_t_sets_difference(working_t_sets, failing_t_sets):
    """Analyze differences in T_sets between working and failing cases."""
    print(f"\n🔍 T_SETS ANALYSIS")
    print("=" * 50)

    print("Working T_sets layers:", list(working_t_sets.keys()))
    print("Failing T_sets layers:", list(failing_t_sets.keys()))

    # Check layer 1 and 2 (should be the same)
    for layer in [1, 2]:
        if layer in working_t_sets and layer in failing_t_sets:
            working_set = set(working_t_sets[layer])
            failing_set = set(failing_t_sets[layer])
            if working_set == failing_set:
                print(f"✅ Layer {layer}: IDENTICAL ({len(working_set)} terms)")
            else:
                print(f"❌ Layer {layer}: DIFFERENT")
                print(f"   Working only: {working_set - failing_set}")
                print(f"   Failing only: {failing_set - working_set}")

    # Check layer 3 (only in failing case)
    if 3 in failing_t_sets:
        layer_3_terms = failing_t_sets[3]
        print(f"\n🔍 Layer 3 Analysis ({len(layer_3_terms)} terms):")

        # Categorize terms
        simple_terms = [t for t in layer_3_terms if '*' not in t]
        cross_terms = [t for t in layer_3_terms if '*' in t]

        print(f"   Simple terms: {len(simple_terms)}")
        if simple_terms[:5]:
            print(f"   Sample: {simple_terms[:5]}")

        print(f"   Cross terms: {len(cross_terms)}")
        if cross_terms[:5]:
            print(f"   Sample: {cross_terms[:5]}")

def main():
    """Debug T-depth 3 issue for different qubit configurations."""
    print("🚨 T-DEPTH 3 DEBUG ANALYSIS")
    print("🎯 Goal: Find why T-depth 3 fails while T-depth 2 works")

    # Test 4-qubit case (T-depth 2 works, T-depth 3 fails)
    print("\n" + "="*70)
    print("TESTING 4-QUBIT CONFIGURATION")
    print("="*70)

    results_4q = debug_t_depth_issue(4, 2, 3)

    if results_4q.get('WORKING', {}).get('success') and results_4q.get('FAILING', {}).get('T_sets'):
        working_t_sets = results_4q['WORKING']['T_sets']
        failing_t_sets = results_4q['FAILING']['T_sets']
        analyze_t_sets_difference(working_t_sets, failing_t_sets)

    # Test 5-qubit case as well
    print("\n" + "="*70)
    print("TESTING 5-QUBIT CONFIGURATION")
    print("="*70)

    results_5q = debug_t_depth_issue(5, 2, 3)

    # Summary
    print(f"\n{'='*70}")
    print("SUMMARY OF T-DEPTH 3 DEBUG")
    print(f"{'='*70}")

    for qubits, results in [("4q", results_4q), ("5q", results_5q)]:
        print(f"\n{qubits} Results:")
        for case, data in results.items():
            if data.get('success'):
                print(f"  {case}: ✅ Fidelity = {data['fidelity']:.6f}")
            else:
                print(f"  {case}: ❌ Failed - {data.get('error', 'Low fidelity')}")

    print(f"\n🎯 FOCUS AREAS FOR T-DEPTH 3 FIX:")
    print("1. Layer 3 auxiliary state generation")
    print("2. Cross-term evaluation in deep circuits")
    print("3. Multi-layer T-gate interaction")
    print("4. Polynomial evaluation complexity")

if __name__ == "__main__":
    main()