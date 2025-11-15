#!/usr/bin/env python3
"""
Check actual T-depth after transpilation for different optimization levels
"""
import sys
sys.path.insert(0, 'core')

from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService
from circuit_evaluation import compute_t_depth
import random

print("Checking T-depth after transpilation...")

# Load IBM account
service = QiskitRuntimeService()
backend = service.backend('ibm_brisbane')

# Create 5q-3t circuit
num_qubits = 5
t_depth = 3

qc = QuantumCircuit(num_qubits)
for q in range(num_qubits):
    qc.h(q)

for layer in range(t_depth):
    for q in range(num_qubits - 1):
        qc.cx(q, q + 1)
    for q in range(num_qubits):
        qc.t(q)
    qc.barrier()

qc.measure_all()

print(f"\nOriginal circuit:")
print(f"  Depth: {qc.depth()}")
print(f"  Gates: {qc.size()}")
print(f"  T-depth: {t_depth}")

# Test different optimization levels
for opt_level in [1, 3]:
    print(f"\n{'='*60}")
    print(f"Optimization Level {opt_level}:")
    print(f"{'='*60}")
    
    qc_trans = transpile(qc, backend=backend, optimization_level=opt_level)
    
    # Count T gates after transpilation
    gate_counts = qc_trans.count_ops()
    print(f"  Depth: {qc_trans.depth()}")
    print(f"  Gates: {qc_trans.size()}")
    print(f"  Gate counts: {gate_counts}")
    
    # Calculate actual T-depth by analyzing circuit structure
    actual_t_depth = compute_t_depth(qc_trans)
    print(f"  ⚠️  Actual T-depth after transpilation: {actual_t_depth}")
    print(f"  📊 T-depth increase: {t_depth} -> {actual_t_depth} ({actual_t_depth/t_depth:.1f}x)")

