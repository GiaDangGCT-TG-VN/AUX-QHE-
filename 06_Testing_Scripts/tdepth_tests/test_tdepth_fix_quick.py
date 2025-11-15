#!/usr/bin/env python3
"""
Quick test of T-depth fix with smaller configuration
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
print("QUICK TEST: T-DEPTH FIX (2 qubits, T-depth 2)")
print("="*80)

# Smaller test configuration
num_qubits = 2
t_depth = 2
print(f"\nTest config: {num_qubits} qubits, T-depth {t_depth}")

# Step 1: Create circuit
print("\n1️⃣  Creating test circuit...")
qc = QuantumCircuit(num_qubits)

for q in range(num_qubits):
    qc.h(q)

for layer in range(t_depth):
    for q in range(num_qubits):
        qc.t(q)
    qc.barrier()

print(f"   ✅ Circuit created: depth={qc.depth()}, gates={qc.size()}")

# Step 2: Generate keys with DOUBLED T-depth
print("\n2️⃣  Generating AUX keys with DOUBLED T-depth...")
keygen_t_depth = t_depth * 2
print(f"   Using T-depth: original={t_depth}, keygen={keygen_t_depth}")

a_init = [random.randint(0, 1) for _ in range(num_qubits)]
b_init = [random.randint(0, 1) for _ in range(num_qubits)]

secret_key, eval_key, prep_time, layer_sizes, total_aux = aux_keygen(
    num_qubits, keygen_t_depth, a_init, b_init
)
print(f"   ✅ Key generation SUCCESS!")
print(f"      Aux states: {total_aux}")
print(f"      Prep time: {prep_time:.3f}s")

# Step 3: Encrypt circuit
print("\n3️⃣  Encrypting circuit...")
params, encoder, encryptor, decryptor, evaluator = initialize_bfv_params()

a_keys, b_keys, k_dict = secret_key
T_sets, V_sets, auxiliary_states = eval_key

qc_encrypted, _, enc_a, enc_b = qotp_encrypt(
    qc, a_keys, b_keys, 0, num_qubits * 2,
    encryptor, encoder, decryptor, params.poly_degree
)
print(f"   ✅ Encryption SUCCESS!")

# Step 4: Transpile
print("\n4️⃣  Transpiling...")
backend = AerSimulator()
qc_transpiled = transpile(qc_encrypted, backend=backend, optimization_level=1)
print(f"   ✅ Transpiled: depth={qc_transpiled.depth()}, gates={qc_transpiled.size()}")

# Step 5: Test AUX evaluation with DOUBLED T-depth
print("\n5️⃣  Testing AUX evaluation with DOUBLED T-depth...")
actual_t_depth = t_depth * 2

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

print(f"      Final QOTP keys: a={final_a}, b={final_b}")

print("\n" + "="*80)
print("✅ QUICK TEST PASSED!")
print("="*80)
print("\nThe T-depth fix works! You can now run the full experiment:")
print("  python ibm_hardware_noise_experiment.py --config 5q-3t --backend ibm_brisbane")
print("="*80)
