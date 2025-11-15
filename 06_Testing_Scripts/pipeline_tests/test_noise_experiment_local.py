#!/usr/bin/env python3
"""
Local Test Script for IBM Noise Experiment
Tests the AUX-QHE pipeline without IBM hardware using Aer simulator
"""

import sys
import time
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, state_fidelity
from qiskit_aer import AerSimulator

# AUX-QHE imports
sys.path.insert(0, 'core')
from key_generation import aux_keygen
from circuit_evaluation import aux_eval
from qotp_crypto import qotp_encrypt, qotp_decrypt
from bfv_core import initialize_bfv_params

def test_aux_qhe_pipeline(num_qubits=3, t_depth=2):
    """
    Test the complete AUX-QHE pipeline locally.

    Args:
        num_qubits: Number of qubits (default: 3)
        t_depth: T-gate depth (default: 2)

    Returns:
        bool: True if test passes, False otherwise
    """
    print(f"\n{'='*80}")
    print(f"🧪 Testing AUX-QHE Pipeline: {num_qubits}q-{t_depth}t")
    print(f"{'='*80}\n")

    try:
        # Step 1: Create test circuit (NO measurements for homomorphic evaluation)
        print("📝 Step 1: Creating test circuit...")
        qc = QuantumCircuit(num_qubits)

        # Apply some gates based on T-depth
        for q in range(num_qubits):
            qc.h(q)

        # Apply T-gates in separate layers
        for layer in range(t_depth):
            # T-gates for this layer
            for q in range(num_qubits):
                qc.t(q)

        # Add entanglement after all T-layers
        for q in range(num_qubits - 1):
            qc.cx(q, q + 1)

        print(f"   ✅ Circuit created: {qc.num_qubits} qubits, {qc.count_ops()}")

        # Step 2: Key Generation
        print("\n🔑 Step 2: Key generation...")
        keygen_start = time.time()

        num_wires = num_qubits
        a_init = [0] * num_wires
        b_init = [0] * num_wires

        secret_key, eval_key, prep_time, layer_sizes, total_aux = aux_keygen(
            num_wires, t_depth, a_init, b_init
        )

        keygen_time = time.time() - keygen_start
        print(f"   ✅ Key generation: {keygen_time:.3f}s")
        print(f"      Auxiliary states: {total_aux}")
        print(f"      Layer sizes: {layer_sizes}")

        # Step 3: Encryption
        print("\n🔐 Step 3: QOTP encryption...")
        encrypt_start = time.time()

        # Extract keys
        a_keys, b_keys, k_dict = secret_key

        # Ensure keys are lists
        a_keys = list(a_keys) if not isinstance(a_keys, list) else a_keys
        b_keys = list(b_keys) if not isinstance(b_keys, list) else b_keys

        print(f"   Keys: a={a_keys}, b={b_keys}")

        # Initialize BFV
        bfv_params, bfv_encoder, bfv_encryptor, bfv_decryptor, bfv_evaluator = initialize_bfv_params()
        poly_degree = bfv_params.poly_degree

        print(f"   BFV params: poly_degree={poly_degree}")

        # Encrypt circuit
        qc_encrypted, _, enc_a, enc_b = qotp_encrypt(
            qc, a_keys, b_keys,
            counter_d=0,
            max_qubits=num_qubits * 2,
            encryptor=bfv_encryptor,
            encoder=bfv_encoder,
            decryptor=bfv_decryptor,
            poly_degree=poly_degree
        )

        if qc_encrypted is None:
            print("   ❌ Encryption failed!")
            return False

        encrypt_time = time.time() - encrypt_start
        print(f"   ✅ Encryption: {encrypt_time:.3f}s")
        print(f"      Encrypted circuit depth: {qc_encrypted.depth()}")

        # Step 4: Homomorphic Evaluation
        print("\n🔍 Step 4: Homomorphic evaluation...")
        eval_start = time.time()

        # Unpack eval_key
        T_sets, V_sets, auxiliary_states = eval_key

        print(f"   T_sets layers: {len(T_sets)}")
        print(f"   Auxiliary states: {len(auxiliary_states)}")

        # Evaluate circuit
        qc_eval, final_enc_a, final_enc_b = aux_eval(
            qc_encrypted, enc_a, enc_b, auxiliary_states, t_depth,
            bfv_encryptor, bfv_decryptor, bfv_encoder, bfv_evaluator, poly_degree, debug=False
        )

        eval_time = time.time() - eval_start
        print(f"   ✅ Evaluation: {eval_time:.3f}s")
        print(f"      Evaluated circuit depth: {qc_eval.depth()}")

        # Step 5: Decryption
        print("\n🔓 Step 5: QOTP decryption...")
        decrypt_start = time.time()

        qc_decrypted = qotp_decrypt(
            qc_eval, final_enc_a, final_enc_b,
            bfv_decryptor, bfv_encoder, poly_degree
        )

        decrypt_time = time.time() - decrypt_start
        print(f"   ✅ Decryption: {decrypt_time:.3f}s")
        print(f"      Decrypted circuit depth: {qc_decrypted.depth()}")

        # Step 6: Simulation and Fidelity
        print("\n📊 Step 6: Simulation and fidelity check...")

        print(f"   Original circuit gates: {qc.count_ops()}")
        print(f"   Decrypted circuit gates: {qc_decrypted.count_ops()}")

        # Simulate original circuit
        ideal_state = Statevector(qc)
        print(f"   Ideal state norm: {np.linalg.norm(ideal_state.data):.6f}")

        # Simulate decrypted circuit
        decrypted_state = Statevector(qc_decrypted)
        print(f"   Decrypted state norm: {np.linalg.norm(decrypted_state.data):.6f}")

        # Compute fidelity
        fidelity = state_fidelity(ideal_state, decrypted_state)

        print(f"   Fidelity: {fidelity:.6f}")

        # Check success
        if fidelity > 0.99:
            print(f"   ✅ SUCCESS: High fidelity ({fidelity:.6f})")
            success = True
        elif fidelity > 0.90:
            print(f"   ⚠️  WARNING: Moderate fidelity ({fidelity:.6f})")
            success = True
        else:
            print(f"   ❌ FAILURE: Low fidelity ({fidelity:.6f})")
            success = False

        # Summary
        total_time = keygen_time + encrypt_time + eval_time + decrypt_time
        print(f"\n{'='*80}")
        print(f"📋 SUMMARY")
        print(f"{'='*80}")
        print(f"   Configuration: {num_qubits}q-{t_depth}t")
        print(f"   Fidelity: {fidelity:.6f}")
        print(f"   Total time: {total_time:.3f}s")
        print(f"      - Key generation: {keygen_time:.3f}s")
        print(f"      - Encryption: {encrypt_time:.3f}s")
        print(f"      - Evaluation: {eval_time:.3f}s")
        print(f"      - Decryption: {decrypt_time:.3f}s")
        print(f"   Status: {'✅ PASS' if success else '❌ FAIL'}")
        print(f"{'='*80}\n")

        return success

    except Exception as e:
        print(f"\n❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_all_configurations():
    """
    Test all planned configurations for the IBM experiment.
    """
    print("\n" + "="*80)
    print("🧪 TESTING ALL CONFIGURATIONS")
    print("="*80)

    configs = [
        {'qubits': 3, 't_depth': 2},
        {'qubits': 3, 't_depth': 3},
        {'qubits': 4, 't_depth': 2},
        {'qubits': 4, 't_depth': 3},
        {'qubits': 5, 't_depth': 2},
        {'qubits': 5, 't_depth': 3},
    ]

    results = []

    for config in configs:
        result = test_aux_qhe_pipeline(
            num_qubits=config['qubits'],
            t_depth=config['t_depth']
        )
        results.append({
            'config': f"{config['qubits']}q-{config['t_depth']}t",
            'passed': result
        })

    # Summary
    print("\n" + "="*80)
    print("📊 TEST SUMMARY")
    print("="*80)

    passed = sum(1 for r in results if r['passed'])
    total = len(results)

    for r in results:
        status = '✅ PASS' if r['passed'] else '❌ FAIL'
        print(f"   {r['config']}: {status}")

    print(f"\n   Total: {passed}/{total} tests passed")

    if passed == total:
        print(f"\n   🎉 All tests passed! Ready for IBM hardware.")
    else:
        print(f"\n   ⚠️  Some tests failed. Fix issues before running on IBM hardware.")

    print("="*80 + "\n")

    return passed == total


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Local test for IBM noise experiment')
    parser.add_argument('--qubits', type=int, default=None,
                       help='Number of qubits (default: test all)')
    parser.add_argument('--t-depth', type=int, default=None,
                       help='T-gate depth (default: test all)')
    parser.add_argument('--all', action='store_true',
                       help='Test all configurations')

    args = parser.parse_args()

    if args.all or (args.qubits is None and args.t_depth is None):
        # Test all configurations
        success = test_all_configurations()
        sys.exit(0 if success else 1)
    else:
        # Test single configuration
        if args.qubits is None or args.t_depth is None:
            print("❌ Error: Both --qubits and --t-depth required for single test")
            sys.exit(1)

        success = test_aux_qhe_pipeline(
            num_qubits=args.qubits,
            t_depth=args.t_depth
        )
        sys.exit(0 if success else 1)
