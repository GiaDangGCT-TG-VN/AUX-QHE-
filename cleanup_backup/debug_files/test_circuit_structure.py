#!/usr/bin/env python3
"""
Test circuit structure to understand T-depth issue.
"""

from qiskit import QuantumCircuit

def analyze_circuit_structure(num_qubits, max_t_depth):
    """Analyze how circuits are structured."""
    circuit = QuantumCircuit(num_qubits)
    circuit.h(0)  # Hadamard
    if num_qubits > 1:
        circuit.cx(0, 1)  # CNOT
    circuit.t(0)  # First T-gate
    if max_t_depth > 1:
        for layer in range(max_t_depth - 1):
            qubit_idx = min(layer + 1, num_qubits - 1) if num_qubits > 1 else 0
            circuit.t(qubit_idx)

    print(f"\n{num_qubits}q-{max_t_depth}t Circuit:")
    print(f"Gates: {[instr.operation.name for instr in circuit.data]}")
    print("Detailed structure:")
    for i, instr in enumerate(circuit.data):
        qubits = [q._index for q in instr.qubits]
        print(f"  {i}: {instr.operation.name} on qubits {qubits}")

    # Analyze T-gate dependencies
    t_gates = []
    for i, instr in enumerate(circuit.data):
        if instr.operation.name == 't':
            qubits = [q._index for q in instr.qubits]
            t_gates.append((i, qubits[0]))

    print(f"T-gates: {t_gates}")

    # Check if T-gates can be parallel
    if len(t_gates) > 1:
        parallel_possible = all(t_gates[i][1] != t_gates[i+1][1] for i in range(len(t_gates)-1))
        print(f"T-gates can be parallel: {parallel_possible}")
        if parallel_possible:
            print("⚠️  All T-gates are on different qubits → Can be executed in parallel → T-depth = 1")
        else:
            print("✅ T-gates have dependencies → Sequential execution required")

def main():
    """Test different circuit configurations."""
    print("🔍 CIRCUIT STRUCTURE ANALYSIS")
    print("="*50)

    configs = [
        (3, 2),  # Working in latest results
        (3, 3),  # Working in latest results
        (4, 2),  # Working
        (4, 3),  # Failing
        (5, 2),  # Working
        (5, 3),  # Failing
    ]

    for num_qubits, max_t_depth in configs:
        analyze_circuit_structure(num_qubits, max_t_depth)

    print(f"\n{'='*70}")
    print("CONCLUSION")
    print(f"{'='*70}")
    print("🎯 ISSUE IDENTIFIED:")
    print("  - Test circuits place T-gates on DIFFERENT qubits")
    print("  - T-gates on different qubits can execute in PARALLEL")
    print("  - Therefore, actual T-depth = 1 for all configurations")
    print("  - But auxiliary key generation expects SEQUENTIAL T-layers")
    print("\n💡 SOLUTION:")
    print("  - Either fix circuit generation to create sequential T-gates")
    print("  - Or fix T-depth counting to match actual circuit structure")

if __name__ == "__main__":
    main()