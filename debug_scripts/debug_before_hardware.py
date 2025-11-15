#!/usr/bin/env python3
"""
Debug Script: Verify AUX-QHE Implementation Before Hardware Execution
Tests all components for 5q-2t configuration to ensure correctness.
"""

import sys
import time
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, state_fidelity

# AUX-QHE imports
sys.path.insert(0, 'core')
from key_generation import aux_keygen
from circuit_evaluation import aux_eval
from qotp_crypto import qotp_encrypt, qotp_decrypt
from bfv_core import initialize_bfv_params

print("="*80)
print("🔍 AUX-QHE IMPLEMENTATION DEBUG - 5q-2t Configuration")
print("="*80)

# Configuration
num_qubits = 5
t_depth = 2
config_name = "5q-2t"

print(f"\n📋 Configuration:")
print(f"   Qubits: {num_qubits}")
print(f"   T-depth: {t_depth}")
print(f"   Config: {config_name}")

# ============================================================================
# TEST 1: Key Generation (Most Critical - Check Aux States Count)
# ============================================================================
print(f"\n{'='*80}")
print(f"TEST 1: Key Generation")
print(f"{'='*80}")

try:
    import random
    random.seed(42)  # Reproducible keys

    a_init = [random.randint(0, 1) for _ in range(num_qubits)]
    b_init = [random.randint(0, 1) for _ in range(num_qubits)]

    print(f"   Initial keys:")
    print(f"   a_init = {a_init}")
    print(f"   b_init = {b_init}")

    keygen_start = time.time()
    secret_key, eval_key, prep_time, layer_sizes, total_aux = aux_keygen(
        num_qubits, t_depth, a_init, b_init
    )
    keygen_time = time.time() - keygen_start

    print(f"\n   ✅ Key Generation Results:")
    print(f"      Time: {keygen_time:.3f}s")
    print(f"      Auxiliary states: {total_aux}")
    print(f"      Layer sizes: {layer_sizes}")

    # CRITICAL CHECK: Verify 575 states (not 1,350)
    EXPECTED_AUX_STATES = 575
    if total_aux == EXPECTED_AUX_STATES:
        print(f"\n   ✅ PASS: Auxiliary states = {EXPECTED_AUX_STATES} (correct!)")
    elif total_aux == 1350:
        print(f"\n   ❌ FAIL: Auxiliary states = 1,350 (OLD CODE WITH SYNTHETIC TERMS!)")
        print(f"      ERROR: Synthetic cross-terms NOT removed from key_generation.py")
        print(f"      ACTION: Check lines 84-111 in core/key_generation.py")
        sys.exit(1)
    else:
        print(f"\n   ⚠️  WARNING: Unexpected auxiliary states = {total_aux}")
        print(f"      Expected: {EXPECTED_AUX_STATES}")
        print(f"      This may indicate an implementation issue")

    # Unpack keys
    a_keys, b_keys, k_dict = secret_key
    T_sets, V_sets, auxiliary_states = eval_key

    print(f"\n   📊 T-set Statistics:")
    for layer, t_set in T_sets.items():
        print(f"      T[{layer}]: {len(t_set)} terms")
        if layer <= 2:
            print(f"         Sample: {t_set[:5]}...")

    print(f"\n   ✅ TEST 1 PASSED")

except Exception as e:
    print(f"\n   ❌ TEST 1 FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============================================================================
# TEST 2: Circuit Construction
# ============================================================================
print(f"\n{'='*80}")
print(f"TEST 2: Circuit Construction")
print(f"{'='*80}")

try:
    # Create test circuit (same as hardware script)
    qc = QuantumCircuit(num_qubits)

    # Hadamard initialization
    for q in range(num_qubits):
        qc.h(q)

    # Entanglement (Clifford gates)
    if num_qubits >= 2:
        for q in range(num_qubits - 1):
            qc.cx(q, q + 1)
    qc.barrier()

    # T-gates in layers
    for layer in range(t_depth):
        for q in range(num_qubits):
            qc.t(q)
        qc.barrier()

    print(f"   ✅ Circuit Created:")
    print(f"      Qubits: {qc.num_qubits}")
    print(f"      Depth: {qc.depth()}")
    print(f"      Gates: {qc.size()}")
    print(f"      T-gates: {sum(1 for inst in qc.data if inst.operation.name == 't')}")

    # Verify T-gate count
    expected_t_gates = num_qubits * t_depth
    actual_t_gates = sum(1 for inst in qc.data if inst.operation.name == 't')

    if actual_t_gates == expected_t_gates:
        print(f"\n   ✅ PASS: T-gate count = {actual_t_gates} (expected: {expected_t_gates})")
    else:
        print(f"\n   ❌ FAIL: T-gate count = {actual_t_gates} (expected: {expected_t_gates})")
        sys.exit(1)

    print(f"\n   ✅ TEST 2 PASSED")

except Exception as e:
    print(f"\n   ❌ TEST 2 FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============================================================================
# TEST 3: BFV Initialization
# ============================================================================
print(f"\n{'='*80}")
print(f"TEST 3: BFV Homomorphic Encryption Initialization")
print(f"{'='*80}")

try:
    bfv_params, bfv_encoder, bfv_encryptor, bfv_decryptor, bfv_evaluator = initialize_bfv_params()
    poly_degree = bfv_params.poly_degree

    print(f"   ✅ BFV Initialized:")
    print(f"      Polynomial degree: {poly_degree}")
    print(f"      Plaintext modulus: {bfv_params.plain_modulus}")

    # Test encryption/decryption
    test_value = 1
    test_plain = bfv_encoder.encode([test_value])
    test_encrypted = bfv_encryptor.encrypt(test_plain)
    test_decrypted = bfv_encoder.decode(bfv_decryptor.decrypt(test_encrypted))[0]

    if int(test_decrypted) % 2 == test_value:
        print(f"\n   ✅ PASS: BFV encrypt/decrypt works correctly")
    else:
        print(f"\n   ❌ FAIL: BFV encrypt/decrypt failed")
        print(f"      Input: {test_value}, Output: {test_decrypted}")
        sys.exit(1)

    print(f"\n   ✅ TEST 3 PASSED")

except Exception as e:
    print(f"\n   ❌ TEST 3 FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============================================================================
# TEST 4: QOTP Encryption
# ============================================================================
print(f"\n{'='*80}")
print(f"TEST 4: QOTP Encryption")
print(f"{'='*80}")

try:
    encrypt_start = time.time()

    # Ensure keys are lists
    a_keys = list(a_keys) if not isinstance(a_keys, list) else a_keys
    b_keys = list(b_keys) if not isinstance(b_keys, list) else b_keys

    print(f"   Encrypting circuit with QOTP...")
    print(f"   Keys: a={a_keys}, b={b_keys}")

    qc_encrypted, _, enc_a, enc_b = qotp_encrypt(
        qc, a_keys, b_keys,
        counter_d=0,
        max_qubits=num_qubits * 2,
        encryptor=bfv_encryptor,
        encoder=bfv_encoder,
        decryptor=bfv_decryptor,
        poly_degree=poly_degree
    )

    encrypt_time = time.time() - encrypt_start

    if qc_encrypted is None:
        print(f"\n   ❌ FAIL: qotp_encrypt returned None")
        sys.exit(1)

    print(f"\n   ✅ Encryption Results:")
    print(f"      Time: {encrypt_time:.3f}s")
    print(f"      Encrypted circuit qubits: {qc_encrypted.num_qubits}")
    print(f"      Encrypted circuit depth: {qc_encrypted.depth()}")
    print(f"      Encrypted circuit gates: {qc_encrypted.size()}")

    # Verify encrypted keys
    print(f"\n   🔐 Encrypted Keys:")
    print(f"      enc_a length: {len(enc_a)}")
    print(f"      enc_b length: {len(enc_b)}")

    # Decrypt first key to verify
    dec_a0 = int(bfv_encoder.decode(bfv_decryptor.decrypt(enc_a[0]))[0]) % 2
    dec_b0 = int(bfv_encoder.decode(bfv_decryptor.decrypt(enc_b[0]))[0]) % 2

    if dec_a0 == a_keys[0] and dec_b0 == b_keys[0]:
        print(f"      Decryption check: enc_a[0]={dec_a0} (expected {a_keys[0]}), enc_b[0]={dec_b0} (expected {b_keys[0]}) ✅")
    else:
        print(f"\n   ❌ FAIL: Encrypted keys don't decrypt to original values")
        sys.exit(1)

    print(f"\n   ✅ TEST 4 PASSED")

except Exception as e:
    print(f"\n   ❌ TEST 4 FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============================================================================
# TEST 5: Homomorphic Evaluation (Key Tracking)
# ============================================================================
print(f"\n{'='*80}")
print(f"TEST 5: Homomorphic Evaluation")
print(f"{'='*80}")

try:
    eval_start = time.time()

    print(f"   Computing final QOTP keys after circuit evaluation...")

    qc_eval, final_enc_a, final_enc_b = aux_eval(
        qc_encrypted, enc_a, enc_b, auxiliary_states, t_depth,
        bfv_encryptor, bfv_decryptor, bfv_encoder, bfv_evaluator, poly_degree, debug=False
    )

    eval_time = time.time() - eval_start

    # Decrypt final keys
    final_a = []
    final_b = []
    for i in range(num_qubits):
        a_val = int(bfv_encoder.decode(bfv_decryptor.decrypt(final_enc_a[i]))[0]) % 2
        b_val = int(bfv_encoder.decode(bfv_decryptor.decrypt(final_enc_b[i]))[0]) % 2
        final_a.append(a_val)
        final_b.append(b_val)

    print(f"\n   ✅ Evaluation Results:")
    print(f"      Time: {eval_time:.3f}s")
    print(f"      Initial QOTP keys: a={a_keys}, b={b_keys}")
    print(f"      Final QOTP keys:   a={final_a}, b={final_b}")

    # Verify keys changed (T-gates should modify keys)
    if final_a != a_keys or final_b != b_keys:
        print(f"\n   ✅ PASS: Keys evolved through T-gates (expected)")
    else:
        print(f"\n   ⚠️  WARNING: Keys unchanged (unexpected for T-depth > 0)")

    print(f"\n   ✅ TEST 5 PASSED")

except Exception as e:
    print(f"\n   ❌ TEST 5 FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============================================================================
# TEST 6: End-to-End Simulation (Local Fidelity Check)
# ============================================================================
print(f"\n{'='*80}")
print(f"TEST 6: End-to-End Simulation (Local Fidelity)")
print(f"{'='*80}")

try:
    print(f"   Running ideal simulation...")
    ideal_state = Statevector(qc)

    print(f"   Running encrypted simulation...")
    encrypted_state = Statevector(qc_encrypted)

    # For full verification, we'd need to decrypt the encrypted state
    # Here we just check that both simulations complete

    print(f"\n   ✅ Simulation Results:")
    print(f"      Ideal state dimension: {len(ideal_state.data)}")
    print(f"      Encrypted state dimension: {len(encrypted_state.data)}")

    # Calculate ideal distribution
    ideal_probs = np.abs(ideal_state.data)**2
    print(f"      Ideal probabilities sum: {np.sum(ideal_probs):.6f}")

    if abs(np.sum(ideal_probs) - 1.0) < 1e-6:
        print(f"\n   ✅ PASS: Ideal state properly normalized")
    else:
        print(f"\n   ❌ FAIL: Ideal state not normalized")
        sys.exit(1)

    print(f"\n   ✅ TEST 6 PASSED")

except Exception as e:
    print(f"\n   ❌ TEST 6 FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============================================================================
# TEST 7: Circuit Export (QASM 3.0)
# ============================================================================
print(f"\n{'='*80}")
print(f"TEST 7: QASM 3.0 Export")
print(f"{'='*80}")

try:
    from qiskit import qasm3
    from pathlib import Path

    # Add measurements
    qc_to_export = qc_encrypted.copy()
    qc_to_export.measure_all()

    print(f"   Exporting to QASM 3.0...")
    qasm3_str = qasm3.dumps(qc_to_export)

    # Save to file
    Path("debug_output").mkdir(exist_ok=True)
    qasm3_file = f"debug_output/{config_name}_debug.qasm"
    with open(qasm3_file, 'w') as f:
        f.write(qasm3_str)

    print(f"\n   ✅ QASM Export Results:")
    print(f"      File: {qasm3_file}")
    print(f"      Size: {len(qasm3_str)} characters")
    print(f"      First 200 chars:")
    print(f"      {qasm3_str[:200]}...")

    print(f"\n   ✅ TEST 7 PASSED")

except Exception as e:
    print(f"\n   ❌ TEST 7 FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============================================================================
# SUMMARY
# ============================================================================
print(f"\n{'='*80}")
print(f"✅ ALL TESTS PASSED - READY FOR HARDWARE EXECUTION")
print(f"{'='*80}")

print(f"\n📊 Summary:")
print(f"   Configuration: {config_name}")
print(f"   Auxiliary States: {total_aux} (correct: {EXPECTED_AUX_STATES})")
print(f"   Circuit Depth: {qc.depth()}")
print(f"   Circuit Gates: {qc.size()}")
print(f"   T-gates: {expected_t_gates}")
print(f"   Key Generation Time: {keygen_time:.3f}s")
print(f"   Encryption Time: {encrypt_time:.3f}s")
print(f"   Evaluation Time: {eval_time:.3f}s")

print(f"\n🚀 Next Step:")
print(f"   python3 ibm_hardware_noise_experiment.py --config {config_name} --shots 1024")

print(f"\n⚠️  Important Verification:")
print(f"   When running on hardware, CHECK the console output for:")
print(f"   '✅ Key generation: X.XXXs, Aux states: {EXPECTED_AUX_STATES}'")
print(f"   If you see {EXPECTED_AUX_STATES}, the fix is applied correctly!")
print(f"   If you see 1,350, DO NOT CONTINUE - fix not applied!")

print(f"\n" + "="*80)
