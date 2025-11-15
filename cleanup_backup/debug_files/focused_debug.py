#!/usr/bin/env python3
"""
Focused debug to find why 4q-2t works but others fail.
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
    """Create the same test circuit as performance comparison."""
    original_circuit = QuantumCircuit(num_qubits)
    original_circuit.h(0)  # Hadamard
    if num_qubits > 1:
        original_circuit.cx(0, 1)  # CNOT
    original_circuit.t(0)  # T-gate
    if max_t_depth > 1:
        # Add more T-gates based on depth
        for layer in range(max_t_depth - 1):
            qubit_idx = min(layer + 1, num_qubits - 1) if num_qubits > 1 else 0
            original_circuit.t(qubit_idx)
    return original_circuit

def test_configuration(config_name, num_qubits, max_t_depth):
    """Test a specific configuration and return detailed info."""
    print(f"\n{'='*50}")
    print(f"TESTING: {config_name}")
    print(f"{'='*50}")

    try:
        # Use EXACT same workflow as performance comparison
        from openqasm_performance_comparison import OpenQASMPerformanceComparator

        # Initialize the performance comparison class
        perf_comp = OpenQASMPerformanceComparator()

        # Initialize BFV
        params, encoder, encryptor, decryptor, evaluator = initialize_bfv_params()
        poly_degree = params.poly_degree

        # Keys (same as performance comparison)
        base_a = [1, 0, 1, 1, 0, 1, 0, 1, 1, 0]
        base_b = [0, 1, 0, 1, 1, 0, 1, 0, 0, 1]
        a_init = base_a[:num_qubits]
        b_init = base_b[:num_qubits]

        print(f"Initial keys: a={a_init}, b={b_init}")

        # Generate AUX-QHE keys
        secret_key, eval_key, aux_prep_time, layer_sizes, total_aux_states = aux_keygen(
            num_qubits, max_t_depth, a_init, b_init
        )
        print(f"Auxiliary states: {total_aux_states}, Layer sizes: {layer_sizes}")

        # Use the EXACT workflow from performance comparison
        original_circuit, decrypted_circuit = perf_comp.run_complete_aux_qhe_workflow(
            num_qubits, max_t_depth, encryptor, decryptor, encoder, evaluator, poly_degree,
            eval_key, a_init, b_init
        )

        print(f"Original circuit: {[instr.operation.name for instr in original_circuit.data]}")
        print(f"Decrypted circuit: {len(decrypted_circuit.data)} operations")

        # Use the EXACT fidelity calculation from performance comparison
        fidelity, tvd = perf_comp.calculate_fidelity_and_tvd(original_circuit, decrypted_circuit)

        print(f"🎯 FIDELITY from perf_comp: {fidelity:.6f}")
        print(f"🎯 TVD from perf_comp: {tvd:.6f}")

        # Get state information for debugging
        original_clean = original_circuit.copy()
        original_clean.remove_final_measurements(inplace=True)
        ideal_statevector = Statevector.from_instruction(original_clean)
        ideal_probs = ideal_statevector.probabilities()

        decrypted_clean = decrypted_circuit.copy()
        decrypted_clean.remove_final_measurements(inplace=True)
        decrypted_statevector = Statevector.from_instruction(decrypted_clean)
        decrypted_probs = decrypted_statevector.probabilities()

        print(f"Ideal probabilities (first 4): {ideal_probs[:4]}")
        print(f"Decrypted probabilities (first 4): {decrypted_probs[:4]}")

        if fidelity < 0.8:
            print("❌ LOW FIDELITY - ANALYZING...")

            # We need the final encrypted keys for this analysis, but they're not available in this scope
            # Skip key evolution analysis for now
            print("Key evolution analysis skipped - would need final_enc_a/final_enc_b")

            # Compare circuits
            orig_gates = [instr.operation.name for instr in original_circuit.data]
            decr_gates = [instr.operation.name for instr in decrypted_clean.data
                         if instr.operation.name not in ['x', 'z', 'measure']]

            print(f"Original gates: {orig_gates}")
            print(f"Core decrypted gates: {decr_gates}")
            print(f"Gate preservation: {orig_gates == decr_gates[:len(orig_gates)]}")
        else:
            print("✅ HIGH FIDELITY - SUCCESS!")

        return fidelity

    except Exception as e:
        print(f"❌ Configuration failed: {e}")
        import traceback
        traceback.print_exc()
        return 0.0

def main():
    """Test different configurations to find the pattern."""
    print("🔍 FOCUSED DEBUG: Finding why 4q-2t works but others fail")

    # Test configurations
    configs = [
        ("3q-2t", 3, 2),  # FAILS
        ("4q-2t", 4, 2),  # WORKS
        ("5q-2t", 5, 2),  # FAILS
        ("3q-3t", 3, 3),  # FAILS
        ("4q-3t", 4, 3),  # FAILS
    ]

    results = {}

    for config_name, num_qubits, max_t_depth in configs:
        fidelity = test_configuration(config_name, num_qubits, max_t_depth)
        results[config_name] = fidelity

    print(f"\n{'='*70}")
    print("SUMMARY OF RESULTS")
    print(f"{'='*70}")

    for config_name, fidelity in results.items():
        status = "✅ WORKS" if fidelity > 0.8 else "❌ FAILS"
        print(f"{config_name}: {fidelity:.6f} {status}")

    # Analyze pattern
    working = [k for k, v in results.items() if v > 0.8]
    failing = [k for k, v in results.items() if v <= 0.8]

    print(f"\n🎯 PATTERN ANALYSIS:")
    print(f"Working: {working}")
    print(f"Failing: {failing}")

if __name__ == "__main__":
    main()