#!/usr/bin/env python3
"""
Diagnose why fidelity is 0% for 5q-2t.
Check if the ideal state computation and decoding are correct.
"""

import sys
import os
sys.path.insert(0, '/Users/giadang/my_qiskitenv/AUX-QHE/core')
os.chdir('/Users/giadang/my_qiskitenv/AUX-QHE')

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
import numpy as np

# Configuration
num_qubits = 5
t_depth = 2

# Create ORIGINAL circuit (what should be compared against)
qc_original = QuantumCircuit(num_qubits)
qc_original.h(0)
if num_qubits > 1:
    qc_original.cx(0, 1)
for layer in range(t_depth):
    qc_original.t(0)

print("="*80)
print("ORIGINAL CIRCUIT (Unencrypted)")
print("="*80)
print(qc_original)

# Get ideal output distribution
ideal_state = Statevector(qc_original)
ideal_probs = np.abs(ideal_state.data)**2

print(f"\n📊 Ideal Output Distribution:")
print(f"   Total probability mass: {np.sum(ideal_probs):.6f}")
print(f"   Non-zero states: {np.sum(ideal_probs > 1e-10)}")

# Show top 10 most probable states
sorted_indices = np.argsort(ideal_probs)[::-1]
print(f"\n   Top 10 Most Probable States:")
for i in range(min(10, len(sorted_indices))):
    idx = sorted_indices[i]
    if ideal_probs[idx] > 1e-10:
        bitstring = format(idx, f'0{num_qubits}b')
        print(f"      |{bitstring}⟩: {ideal_probs[idx]:.6f}")

# Simulate with Aer to get counts
simulator = AerSimulator()
qc_with_meas = qc_original.copy()
qc_with_meas.measure_all()
job = simulator.run(qc_with_meas, shots=1024)
result = job.result()
counts = result.get_counts()

print(f"\n📊 Simulated Counts (1024 shots):")
print(f"   Unique outcomes: {len(counts)}")
sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
print(f"   Top 10:")
for bitstring, count in sorted_counts[:10]:
    print(f"      {bitstring}: {count} ({count/1024*100:.1f}%)")

print(f"\n" + "="*80)
print("ANALYSIS")
print("="*80)

# Expected behavior for H-CNOT-T-T circuit
print(f"\nFor circuit H(0) - CNOT(0,1) - T(0) - T(0):")
print(f"  - H(0) creates |0⟩+|1⟩ superposition on qubit 0")
print(f"  - CNOT(0,1) entangles: |00⟩+|11⟩")
print(f"  - T(0) twice: Adds phase e^(iπ/2) = i to |1⟩ component")
print(f"  - Expected: |00⟩ + i²|11⟩ = |00⟩ - |11⟩")
print(f"  - So dominant states should be |00000⟩ and |11000⟩")

# Check if this matches
state_00000 = ideal_probs[0b00000]  # |00000⟩
state_11000 = ideal_probs[0b11000]  # |11000⟩
state_00011 = ideal_probs[0b00011]  # |00011⟩ (reversed endianness?)

print(f"\n📊 Check Key States:")
print(f"   P(|00000⟩) = {state_00000:.6f}")
print(f"   P(|11000⟩) = {state_11000:.6f}")
print(f"   P(|00011⟩) = {state_00011:.6f} (if endianness reversed)")

# Note: Qiskit uses little-endian (rightmost qubit is q0)
# So |00011⟩ in qiskit notation = q4 q3 q2 q1 q0 = |11000⟩ in our notation
print(f"\n⚠️  IMPORTANT: Qiskit uses little-endian bit ordering!")
print(f"   Qiskit |00011⟩ = q4=0, q3=0, q2=0, q1=1, q0=1")
print(f"   Our circuit has CNOT from q0→q1, so we expect q0=q1")

# The correct states should be:
# |00000⟩ (all qubits 0) and |11000⟩ in our notation
# But in Qiskit's little-endian: |00011⟩
print(f"\n✅ Expected dominant states (Qiskit ordering):")
print(f"   |00000⟩ (all zero)")
print(f"   |00011⟩ (q0=1, q1=1, others=0)")

if state_00000 > 0.4 and state_00011 > 0.4:
    print(f"\n✅ VERIFIED: Circuit produces expected superposition!")
else:
    print(f"\n⚠️  WARNING: Unexpected distribution!")

print(f"\n" + "="*80)
print("CONCLUSION")
print("="*80)
print(f"\n💡 If hardware decoded counts DON'T match this distribution,")
print(f"   then the issue is with QOTP decoding, not the ideal state.")
print(f"\n💡 From your hardware results:")
print(f"   - 943 encrypted outcomes collapsed to only 10 decoded outcomes")
print(f"   - This 99% collapse suggests decoding is WRONG")
print(f"\n💡 Possible causes:")
print(f"   1. Final QOTP keys are incorrect")
print(f"   2. Decoding function has bugs")
print(f"   3. Hardware circuit differs from qc_encrypted")
