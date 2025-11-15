#!/usr/bin/env python3
"""
Local validation test for ibm_hardware_noise_experiment.py
Tests the full pipeline with local simulation before hardware execution
"""
import sys
sys.path.insert(0, 'core')

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from qiskit import transpile
import numpy as np
from key_generation import aux_keygen
from qotp_crypto import qotp_encrypt
from bfv_core import initialize_bfv_params
from circuit_evaluation import aux_eval

print('='*80)
print('LOCAL VALIDATION TEST - FULL PIPELINE')
print('Testing configuration: 5q-3t')
print('='*80)
print()

# Configuration
num_qubits = 5
t_depth = 3
a_init = [1, 1, 0, 0, 0]
b_init = [0, 0, 0, 0, 1]
shots = 1024

# Step 1: Create original circuit
qc = QuantumCircuit(num_qubits)
qc.h(0)
qc.cx(0, 1)
for layer in range(t_depth):
    qc.t(0)

print('Step 1: Original circuit')
print('  H(0), CX(0,1), T(0)×3')
print()

# Step 2: Compute ideal distribution
ideal_state = Statevector(qc)
ideal_probs = np.abs(ideal_state.data)**2

print('Step 2: Ideal distribution')
for i, prob in enumerate(ideal_probs):
    if prob > 0.01:
        bitstring = format(i, '05b')
        print(f'  |{bitstring}⟩: {prob:.6f} ({prob*100:.2f}%)')
print()

# Step 3: Initialize BFV and generate keys
print('Step 3: Key generation')
initialize_bfv_params()
bfv_params, bfv_encoder, bfv_encryptor, bfv_decryptor, bfv_evaluator = initialize_bfv_params()
poly_degree = bfv_params.poly_degree

secret_key, eval_key, prep_time, layer_sizes, total_aux = aux_keygen(
    num_qubits, t_depth, a_init, b_init
)

a_keys, b_keys, k_dict = secret_key
print(f'  Initial QOTP keys: a={a_keys}, b={b_keys}')
print(f'  Aux states: {total_aux}')
print()

# Step 4: Encrypt circuit
print('Step 4: QOTP encryption')
qc_encrypted, _, enc_a, enc_b = qotp_encrypt(
    qc, a_keys, b_keys,
    counter_d=0,
    max_qubits=num_qubits * 2,
    encryptor=bfv_encryptor,
    encoder=bfv_encoder,
    decryptor=bfv_decryptor,
    poly_degree=poly_degree
)
print(f'  Encrypted circuit: {qc_encrypted.num_qubits} qubits, {qc_encrypted.size()} gates')
print()

# Step 5: Simulate encrypted circuit
print('Step 5: Execute encrypted circuit (local simulation)')
qc_encrypted.measure_all()
simulator = AerSimulator()
qc_sim = transpile(qc_encrypted, simulator)

job = simulator.run(qc_sim, shots=shots)
result = job.result()
counts = result.get_counts()

print(f'  Encrypted measurements: {len(counts)} unique outcomes')
print(f'  Sample outcomes:')
for i, (bitstring, count) in enumerate(list(counts.items())[:3]):
    print(f'    {bitstring}: {count}')
print()

# Step 6: Compute final QOTP keys
print('Step 6: Compute final QOTP keys using aux_eval()')
T_sets, V_sets, auxiliary_states = eval_key

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

print(f'  Final QOTP keys: a={final_a}, b={final_b}')
print()

# Step 7: Decode measurements (USING CORRECTED BIT ORDERING)
print('Step 7: Decode measurements')
decoded_counts = {}

# For local simulation, physical_qubits = [0,1,2,3,4]
physical_qubits = list(range(num_qubits))

for bitstring, count in counts.items():
    # Extract values for each logical qubit
    extracted_values = [
        int(bitstring[-(physical_qubits[i] + 1)]) for i in range(num_qubits)
    ]

    # Decode: XOR with final_a
    decoded_values = [extracted_values[i] ^ final_a[i] for i in range(num_qubits)]

    # Convert back to Qiskit bitstring format (qubit 0 at rightmost)
    decoded_bits = ''.join(str(decoded_values[num_qubits-1-i]) for i in range(num_qubits))

    if decoded_bits in decoded_counts:
        decoded_counts[decoded_bits] += count
    else:
        decoded_counts[decoded_bits] = count

print(f'  Decoded measurements: {len(decoded_counts)} unique outcomes')
for bitstring, count in sorted(decoded_counts.items(), key=lambda x: -x[1])[:5]:
    print(f'    |{bitstring}⟩: {count} ({count/shots*100:.2f}%)')
print()

# Step 8: Compute fidelity and TVD
print('Step 8: Compute fidelity metrics')
noisy_probs = np.zeros(2**num_qubits)
for bitstring, count in decoded_counts.items():
    idx = int(bitstring, 2)
    noisy_probs[idx] = count / shots

noisy_probs = noisy_probs / np.sum(noisy_probs)
noisy_amplitudes = np.sqrt(noisy_probs)
noisy_state = Statevector(noisy_amplitudes)

from qiskit.quantum_info import state_fidelity
fidelity = state_fidelity(ideal_state, noisy_state)
tvd = 0.5 * np.sum(np.abs(ideal_probs - noisy_probs))

print(f'  Fidelity: {fidelity:.6f} ({fidelity*100:.2f}%)')
print(f'  TVD: {tvd:.6f}')
print()

# Validation
print('='*80)
print('VALIDATION RESULT:')
print('='*80)

# Check decoded outcomes
expected_outcomes = {'00000', '00011'}
decoded_outcomes = set(decoded_counts.keys())

if decoded_outcomes == expected_outcomes:
    print('✅ Decoded outcomes are CORRECT!')
    print(f'   Got: {decoded_outcomes}')
    print(f'   Expected: {expected_outcomes}')
else:
    print('❌ Decoded outcomes are WRONG!')
    print(f'   Got: {decoded_outcomes}')
    print(f'   Expected: {expected_outcomes}')

print()

# Check TVD
if tvd < 0.02:  # Allow 2% error for 1024 shots
    print(f'✅ TVD is excellent: {tvd:.6f} (<2%)')
    print('   Local simulation works perfectly!')
else:
    print(f'❌ TVD is too high: {tvd:.6f}')
    print('   Something is wrong with decryption')

print()
print('='*80)
if decoded_outcomes == expected_outcomes and tvd < 0.02:
    print('✅✅✅ ALL TESTS PASSED - READY FOR HARDWARE EXECUTION! ✅✅✅')
else:
    print('❌❌❌ TESTS FAILED - DO NOT RUN ON HARDWARE YET! ❌❌❌')
print('='*80)
