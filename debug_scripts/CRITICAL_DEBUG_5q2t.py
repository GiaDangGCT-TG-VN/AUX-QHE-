#!/usr/bin/env python3
"""
CRITICAL DEBUG: Find why 5q-2t produces 0% fidelity.
This runs LOCAL SIMULATION to test the entire pipeline without hardware credits.
"""

import sys
import os
sys.path.insert(0, '/Users/giadang/my_qiskitenv/AUX-QHE/core')
os.chdir('/Users/giadang/my_qiskitenv/AUX-QHE')

from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from key_generation import aux_keygen
from bfv_core import initialize_bfv_params
from qotp_crypto import qotp_encrypt
from circuit_evaluation import aux_eval
import numpy as np
import random

print("="*100)
print("🔍 CRITICAL DEBUG: 5q-2t Full Pipeline Test (LOCAL SIMULATION)")
print("="*100)

# Configuration
num_qubits = 5
t_depth = 2
shots = 1024

# Use SAME keys as hardware execution
random.seed(42)  # Fixed for reproducibility
a_init = [1, 1, 1, 0, 1]
b_init = [1, 0, 0, 1, 0]

print(f"\n📌 Configuration:")
print(f"   Qubits: {num_qubits}")
print(f"   T-depth: {t_depth}")
print(f"   Shots: {shots}")
print(f"   a_init: {a_init}")
print(f"   b_init: {b_init}")

# Initialize BFV
print(f"\n{'='*100}")
print(f"STEP 1: Initialize BFV and Generate Keys")
print(f"{'='*100}")

bfv_params, bfv_encoder, bfv_encryptor, bfv_decryptor, bfv_evaluator = initialize_bfv_params()
poly_degree = bfv_params.poly_degree

secret_key, eval_key, prep_time, layer_sizes, total_aux = aux_keygen(
    num_qubits, t_depth, a_init, b_init
)

a_keys, b_keys, k_dict = secret_key
T_sets, V_sets, auxiliary_states = eval_key

print(f"✅ Keys generated:")
print(f"   a_keys: {a_keys}")
print(f"   b_keys: {b_keys}")
print(f"   Aux states: {total_aux}")
print(f"   Layer sizes: {layer_sizes}")

# Create ORIGINAL circuit
print(f"\n{'='*100}")
print(f"STEP 2: Create Original Circuit")
print(f"{'='*100}")

qc_original = QuantumCircuit(num_qubits)
qc_original.h(0)
if num_qubits > 1:
    qc_original.cx(0, 1)
qc_original.barrier()

for layer in range(t_depth):
    qc_original.t(0)
    qc_original.barrier()

print(f"✅ Original circuit:")
print(qc_original)

# Get ideal output
ideal_state = Statevector(qc_original)
ideal_probs = np.abs(ideal_state.data)**2

print(f"\n✅ Ideal output (expected result):")
print(f"   State |00000⟩: {ideal_probs[0b00000]:.6f}")
print(f"   State |00011⟩: {ideal_probs[0b00011]:.6f}")
print(f"   (These should be ~0.5 each)")

# QOTP Encrypt
print(f"\n{'='*100}")
print(f"STEP 3: QOTP Encryption")
print(f"{'='*100}")

qc_to_encrypt = qc_original.copy()
qc_encrypted, _, enc_a, enc_b = qotp_encrypt(
    qc_to_encrypt, a_keys, b_keys,
    counter_d=0,
    max_qubits=num_qubits * 2,
    encryptor=bfv_encryptor,
    encoder=bfv_encoder,
    decryptor=bfv_decryptor,
    poly_degree=poly_degree
)

print(f"✅ Encrypted circuit: {qc_encrypted.num_qubits} qubits, depth={qc_encrypted.depth()}")
print(f"✅ Encrypted circuit gates: {qc_encrypted.size()}")

# Compute final QOTP keys (what they SHOULD be after circuit execution)
print(f"\n{'='*100}")
print(f"STEP 4: Compute Final QOTP Keys (Using aux_eval)")
print(f"{'='*100}")

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

print(f"✅ Final QOTP keys (for decoding):")
print(f"   Initial: a={a_keys}, b={b_keys}")
print(f"   Final:   a={final_a}, b={final_b}")

# Execute encrypted circuit with Aer simulator
print(f"\n{'='*100}")
print(f"STEP 5: Execute Encrypted Circuit (Aer Simulator)")
print(f"{'='*100}")

simulator = AerSimulator()
qc_to_execute = qc_encrypted.copy()
qc_to_execute.measure_all()

job = simulator.run(qc_to_execute, shots=shots)
result = job.result()
encrypted_counts = result.get_counts()

print(f"✅ Encrypted execution completed:")
print(f"   Unique outcomes: {len(encrypted_counts)}")
print(f"   Total shots: {sum(encrypted_counts.values())}")

# Show top 10 encrypted outcomes
sorted_encrypted = sorted(encrypted_counts.items(), key=lambda x: x[1], reverse=True)
print(f"\n   Top 10 encrypted outcomes:")
for i, (bitstring, count) in enumerate(sorted_encrypted[:10]):
    print(f"      {i+1}. {bitstring}: {count}")

# Decode using final QOTP keys
print(f"\n{'='*100}")
print(f"STEP 6: Decode Encrypted Results")
print(f"{'='*100}")

# Manual decoding
decoded_counts = {}
for encrypted_bitstring, count in encrypted_counts.items():
    # Decode by XORing with final QOTP keys
    decoded_bits = []
    for i in range(num_qubits):
        encrypted_bit = int(encrypted_bitstring[-(i+1)])  # Qiskit little-endian
        decoded_bit = encrypted_bit ^ final_a[i]  # XOR with final a_key
        decoded_bits.append(str(decoded_bit))

    # Reverse back to Qiskit ordering
    decoded_bitstring = ''.join(decoded_bits[::-1])

    if decoded_bitstring not in decoded_counts:
        decoded_counts[decoded_bitstring] = 0
    decoded_counts[decoded_bitstring] += count

print(f"✅ Decoded results:")
print(f"   Unique outcomes: {len(decoded_counts)}")
print(f"   Total shots: {sum(decoded_counts.values())}")

sorted_decoded = sorted(decoded_counts.items(), key=lambda x: x[1], reverse=True)
print(f"\n   All decoded outcomes:")
for bitstring, count in sorted_decoded:
    prob = count / shots
    print(f"      |{bitstring}⟩: {count} ({prob*100:.1f}%)")

# Compare with ideal
print(f"\n{'='*100}")
print(f"STEP 7: Fidelity Computation")
print(f"{'='*100}")

# Convert to probability distributions
decoded_probs = np.zeros(2**num_qubits)
for bitstring, count in decoded_counts.items():
    idx = int(bitstring, 2)
    decoded_probs[idx] = count / shots

# Compute fidelity
fidelity_from_probs = np.sum(np.sqrt(ideal_probs * decoded_probs))**2
tvd = 0.5 * np.sum(np.abs(ideal_probs - decoded_probs))

print(f"✅ Fidelity: {fidelity_from_probs:.6f}")
print(f"✅ TVD: {tvd:.6f}")

# Diagnostic
print(f"\n{'='*100}")
print(f"DIAGNOSTIC ANALYSIS")
print(f"{'='*100}")

if len(decoded_counts) == 2:
    print(f"✅ GOOD: Decoded to 2 outcomes (expected)")
else:
    print(f"❌ BAD: Decoded to {len(decoded_counts)} outcomes (expected 2!)")
    print(f"   This indicates QOTP decoding is incorrect!")

if fidelity_from_probs > 0.8:
    print(f"✅ GOOD: High fidelity ({fidelity_from_probs:.6f})")
    print(f"   The pipeline works correctly in local simulation!")
    print(f"   Hardware issue is likely:")
    print(f"   1. Hardware circuit differs from qc_encrypted")
    print(f"   2. Hardware noise corrupts the state beyond recovery")
elif fidelity_from_probs > 0.3:
    print(f"⚠️  MEDIUM: Moderate fidelity ({fidelity_from_probs:.6f})")
    print(f"   Local simulation has some issues but works partially")
elif fidelity_from_probs < 0.01:
    print(f"❌ CRITICAL: Near-zero fidelity ({fidelity_from_probs:.6f})")
    print(f"   QOTP decoding is WRONG even in local simulation!")
    print(f"   Possible causes:")
    print(f"   1. aux_eval() computes wrong final keys")
    print(f"   2. qotp_decrypt logic is incorrect")
    print(f"   3. Circuit structure mismatch")

# Additional diagnostic: Check if decoded distribution matches ideal
print(f"\n📊 Distribution Comparison:")
print(f"   {'State':<10} {'Ideal':<10} {'Decoded':<10} {'Match?'}")
print(f"   {'-'*45}")
for idx in range(min(10, 2**num_qubits)):
    bitstring = format(idx, f'0{num_qubits}b')
    ideal_p = ideal_probs[idx]
    decoded_p = decoded_probs[idx]
    match = "✅" if abs(ideal_p - decoded_p) < 0.1 else "❌"
    if ideal_p > 0.01 or decoded_p > 0.01:
        print(f"   |{bitstring}⟩   {ideal_p:.4f}     {decoded_p:.4f}     {match}")

print(f"\n{'='*100}")
print(f"CONCLUSION")
print(f"{'='*100}")

if fidelity_from_probs > 0.8:
    print(f"✅ Local simulation works perfectly!")
    print(f"   The code logic is CORRECT.")
    print(f"   Hardware 0% fidelity is due to:")
    print(f"   - Measurement includes QOTP gates (extra qubits)")
    print(f"   - Need to measure only ORIGINAL {num_qubits} qubits, not encrypted qubits")
    print(f"\n💡 FIX NEEDED: Check if qc_encrypted has correct measurement")
    print(f"   Hardware should only measure the first {num_qubits} qubits!")
else:
    print(f"❌ Local simulation ALSO fails!")
    print(f"   The bug is in the code logic, not hardware execution.")
    print(f"   Need to debug:")
    print(f"   1. aux_eval() final key computation")
    print(f"   2. QOTP decoding logic")
    print(f"   3. Circuit encryption process")
