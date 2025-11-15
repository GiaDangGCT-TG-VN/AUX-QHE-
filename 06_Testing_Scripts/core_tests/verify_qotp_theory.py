#!/usr/bin/env python3
"""
Verify QOTP encryption/decryption theory
"""
import sys
sys.path.insert(0, 'core')
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from qiskit import transpile
import numpy as np

print('='*80)
print('QOTP THEORY VERIFICATION')
print('='*80)
print()

# Original circuit
qc_orig = QuantumCircuit(5)
qc_orig.h(0)
qc_orig.cx(0, 1)
qc_orig.t(0)
qc_orig.t(0)
qc_orig.t(0)

print('Original circuit (UNENCRYPTED):')
print('  H(0), CX(0,1), T(0)×3')
print()

# Simulate original (unencrypted)
sv_orig = Statevector(qc_orig)
probs_orig = np.abs(sv_orig.data)**2

print('Expected outcomes (unencrypted):')
for i, p in enumerate(probs_orig):
    if p > 0.01:
        print(f'  |{format(i, "05b")}⟩: {p:.6f}')
print()

# Now manually encrypt: Add X^a Z^b BEFORE the gates
a_init = [1, 1, 0, 0, 0]
b_init = [0, 0, 0, 0, 1]

qc_enc = QuantumCircuit(5)

# Apply encryption: X^a Z^b
for i in range(5):
    if a_init[i] == 1:
        qc_enc.x(i)
    if b_init[i] == 1:
        qc_enc.z(i)

# Then apply original gates
qc_enc.h(0)
qc_enc.cx(0, 1)
qc_enc.t(0)
qc_enc.t(0)
qc_enc.t(0)

print('Encrypted circuit:')
print(f'  X^{a_init} Z^{b_init}, then H(0), CX(0,1), T(0)×3')
print()

# Simulate encrypted circuit
qc_enc.measure_all()
simulator = AerSimulator()
qc_sim = transpile(qc_enc, simulator)
job = simulator.run(qc_sim, shots=10000)
result = job.result()
counts_enc = result.get_counts()

print(f'Encrypted measurements: {len(counts_enc)} unique outcomes')
for bitstring, count in sorted(counts_enc.items(), key=lambda x: -x[1])[:5]:
    print(f'  {bitstring}: {count} ({count/10000*100:.2f}%)')
print()

# Now compute final keys using the gate transformations
print('Computing final keys:')
print('  Initial: a=[1,1,0,0,0], b=[0,0,0,0,1]')
print('  After H(0): a[0]↔b[0] → a=[0,1,0,0,0], b=[1,0,0,0,1]')
print('  After CX(0,1): a[1]←a[1]⊕a[0], b[0]←b[0]⊕b[1]')
print(f'    a[1] = 1⊕0 = 1')
print(f'    b[0] = 1⊕0 = 1')
print('  Final (before T-gates): a=[0,1,0,0,0], b=[1,0,0,0,1]')
print('  T-gates dont change a, so final_a=[0,1,0,0,0]')
print()

final_a = [0, 1, 0, 0, 0]

# Decrypt with CORRECT bit ordering
# Qiskit bitstrings have qubit 0 at RIGHTMOST, but final_a is [qubit0, qubit1, ...]
# So we need to reverse final_a when XORing
counts_dec = {}
for bitstring, count in counts_enc.items():
    decoded = ''.join(str(int(bitstring[i]) ^ final_a[4-i]) for i in range(5))
    if decoded in counts_dec:
        counts_dec[decoded] += count
    else:
        counts_dec[decoded] = count

print(f'Decrypted measurements: {len(counts_dec)} unique outcomes')
for bitstring, count in sorted(counts_dec.items(), key=lambda x: -x[1])[:5]:
    print(f'  |{bitstring}⟩: {count} ({count/10000*100:.2f}%)')
print()

# Check fidelity
noisy_probs = np.zeros(32)
for bitstring, count in counts_dec.items():
    idx = int(bitstring, 2)
    noisy_probs[idx] = count / 10000

noisy_probs = noisy_probs / np.sum(noisy_probs)
noisy_amplitudes = np.sqrt(noisy_probs)
noisy_state = Statevector(noisy_amplitudes)

from qiskit.quantum_info import state_fidelity
fidelity = state_fidelity(sv_orig, noisy_state)

# Also compute TVD (Total Variation Distance)
tvd = 0.5 * np.sum(np.abs(probs_orig - noisy_probs))

print(f'Fidelity: {fidelity:.6f} ({fidelity*100:.2f}%)')
print(f'TVD: {tvd:.6f}')
print()

# For computational basis, TVD is the better metric
if tvd < 0.01:
    print('✅ QOTP encryption/decryption works perfectly!')
    print(f'   TVD = {tvd:.6f} (< 1% error)')
    print('   (Low fidelity is expected when using sqrt(probs) as amplitudes)')
else:
    print(f'❌ QOTP has issues - TVD = {tvd:.6f}')
    print('   Expected TVD < 0.01 for noise-free simulation')
