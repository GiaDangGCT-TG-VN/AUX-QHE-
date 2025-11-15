#!/usr/bin/env python3
"""
Quick Test Script for AUX-QHE Implementation
Run this to verify your installation and the recent fix
"""
import sys
sys.path.insert(0, 'core')

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, state_fidelity
from key_generation import aux_keygen
from circuit_evaluation import aux_eval
from qotp_crypto import qotp_encrypt, qotp_decrypt
from bfv_core import initialize_bfv_params

print("=" * 70)
print("AUX-QHE QUICK TEST")
print("=" * 70)

# Initialize BFV
print("\n1️⃣  Initializing BFV...")
params, encoder, encryptor, decryptor, evaluator = initialize_bfv_params()
poly_degree = params.poly_degree
print(f"   ✅ BFV initialized (degree={poly_degree})")

# Create test circuit
print("\n2️⃣  Creating quantum circuit...")
num_qubits = 3
t_depth = 2
qc = QuantumCircuit(num_qubits)
qc.h(0)
qc.cx(0, 1)
qc.t(0)
qc.t(0)
print(f"   ✅ Circuit created: {num_qubits} qubits, T-depth={t_depth}")
print(f"      Gates: H(0), CNOT(0,1), T(0), T(0)")

# Generate keys
print("\n3️⃣  Generating QOTP keys and auxiliary states...")
a_init = [1, 0, 1]
b_init = [0, 1, 0]
prep_key, eval_key, dec_key, prep_time, total_aux = aux_keygen(
    num_qubits, t_depth, a_init, b_init
)
print(f"   ✅ Keys generated: a={a_init}, b={b_init}")
print(f"   ✅ Auxiliary states: {total_aux} prepared")

# Encrypt circuit
print("\n4️⃣  Encrypting circuit with QOTP...")
enc_circuit, _, enc_a, enc_b = qotp_encrypt(
    qc, a_init, b_init, 0, num_qubits + 5,
    encryptor, encoder, decryptor, poly_degree
)
print(f"   ✅ Circuit encrypted ({len(enc_circuit.data)} operations)")

# Evaluate with T-gadgets
print("\n5️⃣  Evaluating circuit with T-gadgets...")
T_sets, V_sets, auxiliary_states = eval_key
eval_circuit, final_enc_a, final_enc_b = aux_eval(
    enc_circuit, enc_a, enc_b, auxiliary_states, t_depth,
    encryptor, decryptor, encoder, evaluator, poly_degree, debug=False
)
print(f"   ✅ Circuit evaluated ({len(eval_circuit.data)} operations)")

# Decrypt
print("\n6️⃣  Decrypting result...")
dec_circuit = qotp_decrypt(
    eval_circuit, final_enc_a, final_enc_b,
    decryptor, encoder, poly_degree
)
print(f"   ✅ Circuit decrypted ({len(dec_circuit.data)} operations)")

# Verify correctness
print("\n7️⃣  Verifying correctness...")
sv_original = Statevector(qc)
sv_decrypted = Statevector(dec_circuit)
fidelity = state_fidelity(sv_original, sv_decrypted)

print(f"   Original state:   {sv_original.data[:4]}")
print(f"   Decrypted state:  {sv_decrypted.data[:4]}")
print(f"   Fidelity:         {fidelity:.10f}")

print("\n" + "=" * 70)
if fidelity > 0.99:
    print("✅ TEST PASSED - AUX-QHE implementation is working correctly!")
    print("   The recent fix for auxiliary key generation is working!")
else:
    print("❌ TEST FAILED - Fidelity is too low")
    print(f"   Expected: >0.99, Got: {fidelity}")
print("=" * 70)

# Summary
print(f"\n📊 Summary:")
print(f"   Circuit: {num_qubits}q-{t_depth}t")
print(f"   Auxiliary states: {total_aux}")
print(f"   Fidelity: {fidelity:.6f}")
print(f"   Status: {'PASS ✅' if fidelity > 0.99 else 'FAIL ❌'}")
