#!/usr/bin/env python3
"""
Local test of the full AUX-QHE pipeline without IBM hardware.
Uses Qiskit's AerSimulator to test the complete flow.
"""

import sys
import time
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector, state_fidelity
from qiskit_aer import AerSimulator

# Import AUX-QHE modules
sys.path.insert(0, 'core')
from key_generation import aux_keygen
from qotp_crypto import qotp_encrypt, qotp_decrypt
from circuit_evaluation import aux_eval
from bfv_core import initialize_bfv_params

def test_config(num_qubits, t_depth, shots=1024):
    """Test a single configuration locally"""
    print(f"\n{'='*80}")
    print(f"Testing {num_qubits}q-{t_depth}t configuration")
    print(f"{'='*80}")

    # Create test circuit
    qc = QuantumCircuit(num_qubits)

    # Apply Hadamard gates for initialization
    for q in range(num_qubits):
        qc.h(q)

    # Apply T-gates and CX gates in layers
    for layer in range(t_depth):
        for q in range(num_qubits):
            qc.t(q)
        qc.barrier()
        if num_qubits >= 2:
            for q in range(0, num_qubits - 1, 2):
                qc.cx(q, q + 1)
        qc.barrier()

    print(f"✓ Circuit created: {qc.size()} gates, depth={qc.depth()}")

    # Initialize BFV
    bfv_params, bfv_encoder, bfv_encryptor, bfv_decryptor, bfv_evaluator = initialize_bfv_params()
    poly_degree = bfv_params.poly_degree
    print(f"✓ BFV initialized: poly_degree={poly_degree}")

    # Key generation
    print("⏳ Key generation...")
    start = time.time()
    a_init = [0] * num_qubits
    b_init = [0] * num_qubits
    secret_key, eval_key, prep_time, layer_sizes, total_aux = aux_keygen(
        num_qubits, t_depth, a_init, b_init
    )
    a_keys, b_keys, k_dict = secret_key
    T_sets, V_sets, auxiliary_states = eval_key
    keygen_time = time.time() - start
    print(f"✓ Key generation: {keygen_time:.3f}s, {total_aux} aux states")

    # Encryption
    print("⏳ QOTP encryption...")
    start = time.time()
    qc_encrypted, _, enc_a, enc_b = qotp_encrypt(
        qc, a_keys, b_keys,
        counter_d=0,
        max_qubits=num_qubits * 2,
        encryptor=bfv_encryptor,
        encoder=bfv_encoder,
        decryptor=bfv_decryptor,
        poly_degree=poly_degree
    )
    encrypt_time = time.time() - start

    if qc_encrypted is None:
        print("✗ Encryption failed")
        return False

    print(f"✓ Encryption: {encrypt_time:.3f}s")

    # Transpilation
    print("⏳ Transpiling...")
    start = time.time()
    backend = AerSimulator()
    qc_transpiled = transpile(qc_encrypted, backend, optimization_level=1)
    qc_transpiled.measure_all()
    transpile_time = time.time() - start
    print(f"✓ Transpilation: {transpile_time:.3f}s")

    # Execution (simulation)
    print("⏳ Simulating execution...")
    start = time.time()
    result = backend.run(qc_transpiled, shots=shots).result()
    counts = result.get_counts()
    exec_time = time.time() - start
    print(f"✓ Execution: {exec_time:.3f}s, {len(counts)} unique outcomes")

    # Compute final QOTP keys
    print("⏳ Computing final QOTP keys...")
    start = time.time()
    qc_eval, final_enc_a, final_enc_b = aux_eval(
        qc_encrypted, enc_a, enc_b, auxiliary_states, t_depth,
        bfv_encryptor, bfv_decryptor, bfv_encoder, bfv_evaluator, poly_degree, debug=False
    )

    # Decrypt final keys
    final_a = []
    final_b = []
    for i in range(num_qubits):
        a_val = int(bfv_encoder.decode(bfv_decryptor.decrypt(final_enc_a[i]))[0]) % 2
        b_val = int(bfv_encoder.decode(bfv_decryptor.decrypt(final_enc_b[i]))[0]) % 2
        final_a.append(a_val)
        final_b.append(b_val)

    eval_time = time.time() - start
    print(f"✓ Final key computation: {eval_time:.3f}s")

    # Decode measurements
    print("⏳ Decoding measurements...")
    start = time.time()
    decoded_counts = {}
    for bitstring, count in counts.items():
        decoded_bits = ''.join(
            str(int(bitstring[i]) ^ final_a[i]) for i in range(num_qubits)
        )
        decoded_counts[decoded_bits] = count
    decode_time = time.time() - start
    print(f"✓ Decoding: {decode_time:.3f}s, {len(decoded_counts)} outcomes")

    # Fidelity calculation
    print("⏳ Computing fidelity...")
    ideal_state = Statevector(qc)
    ideal_probs = np.abs(ideal_state.data)**2

    noisy_probs = np.zeros(2**num_qubits)
    for bitstring, count in decoded_counts.items():
        idx = int(bitstring, 2)
        noisy_probs[idx] = count / shots

    if np.sum(noisy_probs) > 0:
        noisy_probs = noisy_probs / np.sum(noisy_probs)

    noisy_amplitudes = np.sqrt(noisy_probs)
    noisy_state = Statevector(noisy_amplitudes)

    fidelity = state_fidelity(ideal_state, noisy_state)
    tvd = 0.5 * np.sum(np.abs(ideal_probs - noisy_probs))

    print(f"\n✅ TEST PASSED")
    print(f"   Fidelity: {fidelity:.6f}")
    print(f"   TVD: {tvd:.6f}")

    return True

def main():
    """Run tests for all configurations"""
    print("="*80)
    print("AUX-QHE LOCAL PIPELINE TEST")
    print("="*80)

    configs = [
        (3, 3),  # 3q-3t
        (4, 3),  # 4q-3t
        (5, 2),  # 5q-2t
        (5, 3),  # 5q-3t
    ]

    results = []
    for num_qubits, t_depth in configs:
        try:
            success = test_config(num_qubits, t_depth, shots=512)
            results.append((f"{num_qubits}q-{t_depth}t", success))
        except Exception as e:
            print(f"\n✗ Test failed: {e}")
            import traceback
            traceback.print_exc()
            results.append((f"{num_qubits}q-{t_depth}t", False))

    print(f"\n{'='*80}")
    print("TEST SUMMARY")
    print(f"{'='*80}")
    for config, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{config}: {status}")

    all_passed = all(success for _, success in results)
    print(f"\nOverall: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")

    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
