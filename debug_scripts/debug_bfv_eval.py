#!/usr/bin/env python3
"""Debug BFV evaluation to see if final_a is computed correctly"""
import sys
import numpy as np
sys.path.insert(0, 'core')

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, state_fidelity
from qiskit_aer import AerSimulator

from key_generation import aux_keygen
from qotp_crypto import qotp_encrypt
from circuit_evaluation import aux_eval
from bfv_core import initialize_bfv_params

# Simple test: 3q-2t
num_qubits = 3
t_depth = 2
shots = 512

print("Creating circuit...")
qc = QuantumCircuit(num_qubits)
for q in range(num_qubits):
    qc.h(q)
for layer in range(t_depth):
    for q in range(num_qubits):
        qc.t(q)

print("BFV init...")
bfv_params, bfv_encoder, bfv_encryptor, bfv_decryptor, bfv_evaluator = initialize_bfv_params()
poly_degree = bfv_params.poly_degree

print("Key generation...")
a_init = [0] * num_qubits
b_init = [0] * num_qubits
secret_key, eval_key, prep_time, layer_sizes, total_aux = aux_keygen(
    num_qubits, t_depth, a_init, b_init
)
a_keys, b_keys, k_dict = secret_key
T_sets, V_sets, auxiliary_states = eval_key

print(f"Initial keys: a={a_keys}, b={b_keys}")

print("Encryption...")
qc_encrypted, _, enc_a, enc_b = qotp_encrypt(
    qc, a_keys, b_keys, counter_d=0, max_qubits=num_qubits * 2,
    encryptor=bfv_encryptor, encoder=bfv_encoder, decryptor=bfv_decryptor, poly_degree=poly_degree
)

print("Evaluation (computing final keys)...")
qc_eval, final_enc_a, final_enc_b = aux_eval(
    qc_encrypted, enc_a, enc_b, auxiliary_states, t_depth,
    bfv_encryptor, bfv_decryptor, bfv_encoder, bfv_evaluator, poly_degree, debug=True
)

print("\nDecrypting final keys...")
final_a = []
for i in range(num_qubits):
    a_val = int(bfv_encoder.decode(bfv_decryptor.decrypt(final_enc_a[i]))[0]) % 2
    final_a.append(a_val)

print(f"Final a keys: {final_a}")
print(f"Expected (for a_init=[0,0,0]): Should depend on T-gates applied")

# Now check if decoding works
print("\nRunning simulation...")
from qiskit import transpile
backend = AerSimulator()
qc_t = transpile(qc_encrypted, backend, optimization_level=1)
qc_t.measure_all()
result = backend.run(qc_t, shots=shots).result()
counts = result.get_counts()

# Decode
decoded_counts = {}
for bitstring, count in counts.items():
    decoded_bits = ''.join(str(int(bitstring[i]) ^ final_a[i]) for i in range(num_qubits))
    decoded_counts[decoded_bits] = count

# Compare
ideal_state = Statevector(qc)
ideal_probs = np.abs(ideal_state.data)**2

noisy_probs = np.zeros(2**num_qubits)
for bitstring, count in decoded_counts.items():
    idx = int(bitstring, 2)
    noisy_probs[idx] = count / shots

fidelity = state_fidelity(ideal_state, Statevector(np.sqrt(noisy_probs)))

print(f"\n🎯 Fidelity: {fidelity:.6f}")
print(f"\nTop 3 ideal outcomes:")
top_ideal = sorted(enumerate(ideal_probs), key=lambda x: x[1], reverse=True)[:3]
for idx, prob in top_ideal:
    print(f"  |{bin(idx)[2:].zfill(num_qubits)}⟩: {prob:.4f}")

print(f"\nTop 3 measured outcomes:")
top_measured = sorted(decoded_counts.items(), key=lambda x: x[1], reverse=True)[:3]
for bitstring, count in top_measured:
    print(f"  |{bitstring}⟩: {count/shots:.4f}")
