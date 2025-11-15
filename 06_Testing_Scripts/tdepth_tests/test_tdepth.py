#!/usr/bin/env python3
"""Test T-depth calculation for circuit construction"""

from qiskit import QuantumCircuit

def organize_gates_into_layers_simple(circuit_operations):
    """Simplified version of organize_gates_into_layers"""
    layers = []
    current_layer = []
    used_qubits = set()
    t_depth = 0

    for gate_name, qubits in circuit_operations:
        # Convert to list if single qubit
        qubit_list = [qubits] if isinstance(qubits, int) else list(qubits)

        # Check if qubits are available (no conflicts)
        if any(q in used_qubits for q in qubit_list):
            # Start new layer
            if any(g == 't' for g, _ in current_layer):
                t_depth += 1
            layers.append(current_layer)
            current_layer = []
            used_qubits.clear()

        # Add operation to current layer
        current_layer.append((gate_name, qubits))
        used_qubits.update(qubit_list)

    # Add final layer
    if current_layer:
        if any(g == 't' for g, _ in current_layer):
            t_depth += 1
        layers.append(current_layer)

    return layers, t_depth

# Test circuit with 3 qubits, 3 T-layers
num_qubits = 3
t_depth = 3
qc = QuantumCircuit(num_qubits)

for q in range(num_qubits):
    qc.h(q)

for layer in range(t_depth):
    for q in range(num_qubits):
        qc.t(q)
    qc.barrier()
    if num_qubits >= 2:
        for q in range(0, num_qubits - 1, 2):
            qc.cx(q, q + 1)
    qc.barrier()

# Extract operations
circuit_operations = []
for instr in qc.data:
    gate_name = instr.operation.name.lower()
    qubits = tuple(qc.qubits.index(q) for q in instr.qubits)
    if gate_name == 'cx' and len(qubits) == 2:
        circuit_operations.append((gate_name, qubits))
    elif gate_name in ['h', 't', 'x', 'z', 'p'] and len(qubits) == 1:
        circuit_operations.append((gate_name, qubits[0]))

# Organize into layers
layers, actual_t_depth = organize_gates_into_layers_simple(circuit_operations)

print(f'Expected T-depth: {t_depth}')
print(f'Actual T-depth: {actual_t_depth}')
print(f'Total operations: {len(circuit_operations)}')
print(f'Total layers: {len(layers)}')
print(f'\nLayer breakdown:')
for i, layer in enumerate(layers):
    has_t = any(g == 't' for g, _ in layer)
    print(f'  Layer {i}: {len(layer)} gates, has T-gate: {has_t}')
    print(f'    Gates: {layer}')
