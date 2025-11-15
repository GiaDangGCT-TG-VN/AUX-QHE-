#!/usr/bin/env python3
"""
Fix T-depth circuit generation to create truly sequential T-gates.
"""

from qiskit import QuantumCircuit

def create_sequential_t_depth_circuit(num_qubits, max_t_depth):
    """
    Create a circuit with truly sequential T-gates for proper T-depth testing.

    Strategy:
    - Use a single qubit for all T-gates to force sequential execution
    - This ensures T-depth = number of T-gates on that qubit
    """
    circuit = QuantumCircuit(num_qubits)

    # Initial setup
    circuit.h(0)  # Hadamard
    if num_qubits > 1:
        circuit.cx(0, 1)  # CNOT

    # Sequential T-gates on the SAME qubit to force T-depth
    target_qubit = 0  # Use qubit 0 for all T-gates
    for t_layer in range(max_t_depth):
        circuit.t(target_qubit)

    return circuit

def create_distributed_t_depth_circuit(num_qubits, max_t_depth):
    """
    Create circuit with T-gates distributed but with dependencies.

    Strategy:
    - Use CNOT gates to create dependencies between T-gates
    - This forces sequential execution even on different qubits
    """
    circuit = QuantumCircuit(num_qubits)

    # Initial setup
    circuit.h(0)
    if num_qubits > 1:
        circuit.cx(0, 1)

    # Create T-depth with dependencies
    for t_layer in range(max_t_depth):
        qubit_idx = t_layer % num_qubits
        circuit.t(qubit_idx)

        # Add dependency to next qubit if available
        if t_layer + 1 < max_t_depth and num_qubits > 1:
            next_qubit = (t_layer + 1) % num_qubits
            if next_qubit != qubit_idx:
                circuit.cx(qubit_idx, next_qubit)

    return circuit

def test_circuit_strategies():
    """Test different circuit generation strategies."""
    print("🔧 TESTING T-DEPTH CIRCUIT GENERATION STRATEGIES")
    print("="*60)

    configs = [(4, 2), (4, 3), (5, 3)]

    for num_qubits, max_t_depth in configs:
        print(f"\n📊 Testing {num_qubits}q-{max_t_depth}t:")
        print("-" * 40)

        # Strategy 1: Sequential T-gates on same qubit
        seq_circuit = create_sequential_t_depth_circuit(num_qubits, max_t_depth)
        seq_gates = [instr.operation.name for instr in seq_circuit.data]

        # Count T-gates on each qubit
        t_gate_count_per_qubit = {}
        for instr in seq_circuit.data:
            if instr.operation.name == 't':
                qubit = instr.qubits[0]._index
                t_gate_count_per_qubit[qubit] = t_gate_count_per_qubit.get(qubit, 0) + 1

        print(f"Sequential strategy:")
        print(f"  Gates: {seq_gates}")
        print(f"  T-gates per qubit: {t_gate_count_per_qubit}")
        print(f"  Expected T-depth: {max(t_gate_count_per_qubit.values()) if t_gate_count_per_qubit else 0}")

        # Strategy 2: Distributed with dependencies
        dist_circuit = create_distributed_t_depth_circuit(num_qubits, max_t_depth)
        dist_gates = [instr.operation.name for instr in dist_circuit.data]

        print(f"Distributed strategy:")
        print(f"  Gates: {dist_gates}")
        print(f"  Gate count: {len(dist_gates)}")

def main():
    """Test and recommend circuit generation strategy."""
    test_circuit_strategies()

    print(f"\n{'='*60}")
    print("RECOMMENDATION")
    print(f"{'='*60}")
    print("💡 Use SEQUENTIAL strategy for T-depth testing:")
    print("   - All T-gates on the same qubit")
    print("   - Forces true sequential execution")
    print("   - T-depth = number of T-gates on that qubit")
    print("   - Matches auxiliary key generation expectations")

if __name__ == "__main__":
    main()