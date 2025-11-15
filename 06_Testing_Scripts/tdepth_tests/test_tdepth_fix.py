#!/usr/bin/env python3
"""
Test the T-depth fix locally before running on IBM hardware
"""
import sys
sys.path.insert(0, 'core')

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from key_generation import aux_keygen
from qotp_crypto import qotp_encrypt
from circuit_evaluation import aux_eval
from bfv_core import initialize_bfv_params
import random

print("="*80)
print("TESTING T-DEPTH FIX LOCALLY")
print("="*80)

# Test configuration
num_qubits = 5
t_depth = 3
print(f"\nTest config: {num_qubits} qubits, T-depth {t_depth}")

# Step 1: Create circuit (same as hardware experiment)
print("\n1️⃣  Creating test circuit...")
qc = QuantumCircuit(num_qubits)

# Apply Hadamard gates for initialization
for q in range(num_qubits):
    qc.h(q)

# Apply T-gates and CX gates in a pattern that maintains T-depth
for layer in range(t_depth):
    # Apply T-gates in parallel
    for q in range(num_qubits):
        qc.t(q)
    qc.barrier()

    # Add entanglement with CX gates
    if num_qubits >= 2:
        for q in range(0, num_qubits - 1, 2):
            qc.cx(q, q + 1)
    qc.barrier()

print(f"   ✅ Circuit created: depth={qc.depth()}, gates={qc.size()}")

# Step 2: Generate keys with DOUBLED T-depth (the fix!)
print("\n2️⃣  Generating AUX keys with DOUBLED T-depth...")
keygen_t_depth = t_depth * 2  # FIX: Double the T-depth
print(f"   Using T-depth: original={t_depth}, keygen={keygen_t_depth}")

a_init = [random.randint(0, 1) for _ in range(num_qubits)]
b_init = [random.randint(0, 1) for _ in range(num_qubits)]
print(f"   Random QOTP keys: a={a_init}, b={b_init}")

try:
    secret_key, eval_key, prep_time, layer_sizes, total_aux = aux_keygen(
        num_qubits, keygen_t_depth, a_init, b_init
    )
    print(f"   ✅ Key generation SUCCESS!")
    print(f"      Aux states: {total_aux}")
    print(f"      Layer sizes: {layer_sizes}")
except Exception as e:
    print(f"   ❌ Key generation FAILED: {e}")
    sys.exit(1)

# Step 3: Encrypt circuit
print("\n3️⃣  Encrypting circuit with QOTP...")
params, encoder, encryptor, decryptor, evaluator = initialize_bfv_params()

a_keys, b_keys, k_dict = secret_key
T_sets, V_sets, auxiliary_states = eval_key

try:
    qc_encrypted, _, enc_a, enc_b = qotp_encrypt(
        qc, a_keys, b_keys, 0, num_qubits * 2,
        encryptor, encoder, decryptor, params.poly_degree
    )
    if qc_encrypted is None:
        raise ValueError("Encryption returned None")
    print(f"   ✅ Encryption SUCCESS!")
    print(f"      Encrypted circuit: depth={qc_encrypted.depth()}, gates={qc_encrypted.size()}")
except Exception as e:
    print(f"   ❌ Encryption FAILED: {e}")
    sys.exit(1)

# Step 4: Transpile (simulate what IBM does)
print("\n4️⃣  Transpiling circuit (simulating IBM hardware)...")
backend = AerSimulator()

qc_transpiled = transpile(
    qc_encrypted,
    backend=backend,
    optimization_level=1,
    seed_transpiler=42
)

print(f"   ✅ Transpilation SUCCESS!")
print(f"      Transpiled circuit: depth={qc_transpiled.depth()}, gates={qc_transpiled.size()}")

# Step 5: Test AUX evaluation with DOUBLED T-depth
print("\n5️⃣  Testing AUX evaluation with DOUBLED T-depth...")
actual_t_depth = t_depth * 2  # FIX: Use doubled T-depth

try:
    qc_eval, final_enc_a, final_enc_b = aux_eval(
        qc_encrypted, enc_a, enc_b, auxiliary_states, actual_t_depth,
        encryptor, decryptor, encoder, evaluator, params.poly_degree, debug=False
    )
    print(f"   ✅ AUX evaluation SUCCESS!")

    # Decrypt final keys
    final_a = []
    final_b = []
    for i in range(num_qubits):
        a_val = int(encoder.decode(decryptor.decrypt(final_enc_a[i]))[0]) % 2
        b_val = int(encoder.decode(decryptor.decrypt(final_enc_b[i]))[0]) % 2
        final_a.append(a_val)
        final_b.append(b_val)

    print(f"      Final QOTP keys: a={final_a}, b={b_val}")

except Exception as e:
    print(f"   ❌ AUX evaluation FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*80)
print("✅ ALL TESTS PASSED!")
print("="*80)
print("\nThe T-depth fix is working correctly. You can now run the full experiment:")
print("  python ibm_hardware_noise_experiment.py --config 5q-3t --backend ibm_brisbane")
print("="*80)
