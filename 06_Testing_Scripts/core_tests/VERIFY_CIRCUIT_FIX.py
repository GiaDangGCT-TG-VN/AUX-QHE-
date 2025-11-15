#!/usr/bin/env python3
"""
Verification Script: Ensure ALL circuit creation matches local simulation
"""

import sys
sys.path.insert(0, 'core')

from qiskit import QuantumCircuit

print("="*80)
print("🔍 CIRCUIT CONSISTENCY VERIFICATION")
print("="*80)

def create_local_simulation_circuit(num_qubits, t_depth):
    """Reference: Local simulation circuit structure"""
    qc = QuantumCircuit(num_qubits)
    qc.h(0)
    if num_qubits > 1:
        qc.cx(0, 1)
    for t_layer in range(t_depth):
        qc.t(0)
    return qc

def create_hardware_experiment_circuit(num_qubits, t_depth):
    """Current: Hardware experiment circuit (from ibm_hardware_noise_experiment.py)"""
    qc = QuantumCircuit(num_qubits)
    qc.h(0)
    if num_qubits > 1:
        qc.cx(0, 1)
    qc.barrier()
    for layer in range(t_depth):
        qc.t(0)
        qc.barrier()
    return qc

def verify_circuit_match(qc1, qc2, name1, name2):
    """Verify two circuits have same gate structure (ignoring barriers)"""
    
    # Get operations (excluding barriers)
    ops1 = [(inst.operation.name, tuple([qc1.find_bit(q).index for q in inst.qubits])) 
            for inst in qc1.data if inst.operation.name != 'barrier']
    ops2 = [(inst.operation.name, tuple([qc2.find_bit(q).index for q in inst.qubits])) 
            for inst in qc2.data if inst.operation.name != 'barrier']
    
    # Count gate types
    from collections import Counter
    counts1 = Counter(op[0] for op in ops1)
    counts2 = Counter(op[0] for op in ops2)
    
    match = ops1 == ops2
    
    print(f"\n{'='*80}")
    print(f"Comparing: {name1} vs {name2}")
    print(f"{'='*80}")
    
    print(f"\n{name1}:")
    print(f"  Gate counts: {dict(counts1)}")
    print(f"  Operations: {ops1}")
    
    print(f"\n{name2}:")
    print(f"  Gate counts: {dict(counts2)}")
    print(f"  Operations: {ops2}")
    
    if match:
        print(f"\n✅ MATCH: Circuits are identical!")
    else:
        print(f"\n❌ MISMATCH: Circuits differ!")
        
    return match

# Test all configurations
configs = [
    ("3q-2t", 3, 2),
    ("4q-2t", 4, 2),
    ("5q-2t", 5, 2),
    ("3q-3t", 3, 3),
    ("4q-3t", 4, 3),
    ("5q-3t", 5, 3)
]

all_match = True

for config_name, num_qubits, t_depth in configs:
    print(f"\n{'#'*80}")
    print(f"Testing Configuration: {config_name}")
    print(f"{'#'*80}")
    
    qc_local = create_local_simulation_circuit(num_qubits, t_depth)
    qc_hardware = create_hardware_experiment_circuit(num_qubits, t_depth)
    
    match = verify_circuit_match(
        qc_local, qc_hardware,
        f"Local Simulation ({config_name})",
        f"Hardware Experiment ({config_name})"
    )
    
    if not match:
        all_match = False
    
    # Display circuit
    print(f"\n{config_name} Circuit:")
    print(qc_hardware.draw(output='text', fold=-1))
    
    # Verify T-gate count
    expected_t_gates = t_depth
    actual_t_gates = qc_hardware.count_ops().get('t', 0)
    
    print(f"\nT-gate verification:")
    print(f"  Expected: {expected_t_gates} T-gates")
    print(f"  Actual: {actual_t_gates} T-gates")
    
    if expected_t_gates == actual_t_gates:
        print(f"  ✅ Correct!")
    else:
        print(f"  ❌ WRONG! Should be {expected_t_gates}, not {actual_t_gates}")
        all_match = False

print("\n" + "="*80)
print("FINAL RESULT")
print("="*80)

if all_match:
    print("\n✅ SUCCESS: All circuits match local simulation!")
    print("   Hardware experiments will test the SAME circuit structure.")
    print("   Your description 'three T-gates' (for t_depth=3) is CORRECT!")
else:
    print("\n❌ FAILURE: Some circuits don't match!")
    print("   Need to fix remaining inconsistencies.")

sys.exit(0 if all_match else 1)

