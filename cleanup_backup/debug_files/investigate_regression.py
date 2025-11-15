#!/usr/bin/env python3
"""
Investigate why the fix caused a regression in some configurations.
"""

from qiskit import QuantumCircuit

def analyze_circuit_differences():
    """Compare circuit structures before and after the fix."""
    print("🔍 INVESTIGATING CIRCUIT REGRESSION")
    print("="*50)

    # Test different configurations
    configs = [
        (3, 2, "3q-2t"),  # Now failing
        (3, 3, "3q-3t"),  # Now working
        (4, 2, "4q-2t"),  # Still working
        (5, 2, "5q-2t"),  # Now failing
    ]

    for num_qubits, max_t_depth, config_name in configs:
        print(f"\n{config_name} - Expected T-depth: {max_t_depth}")
        print("-" * 30)

        # Current (fixed) circuit generation
        circuit = QuantumCircuit(num_qubits)
        circuit.h(0)  # Hadamard
        if num_qubits > 1:
            circuit.cx(0, 1)  # CNOT

        # Fixed approach: All T-gates on qubit 0
        for t_layer in range(max_t_depth):
            circuit.t(0)  # All T-gates on qubit 0

        gates = [instr.operation.name for instr in circuit.data]

        # Count T-gates on each qubit
        t_count_per_qubit = {}
        for instr in circuit.data:
            if instr.operation.name == 't':
                qubit = instr.qubits[0]._index
                t_count_per_qubit[qubit] = t_count_per_qubit.get(qubit, 0) + 1

        print(f"Circuit: {gates}")
        print(f"T-gates per qubit: {t_count_per_qubit}")
        print(f"Max T-depth on any qubit: {max(t_count_per_qubit.values()) if t_count_per_qubit else 0}")

        # Analyze if this makes sense
        expected_t_depth = max(t_count_per_qubit.values()) if t_count_per_qubit else 0
        if expected_t_depth == max_t_depth:
            print("✅ T-depth matches expectation")
        else:
            print(f"❌ T-depth mismatch: expected {max_t_depth}, got {expected_t_depth}")

def check_auxiliary_state_mismatch():
    """Check if there's a mismatch between auxiliary states and circuit structure."""
    print(f"\n{'='*50}")
    print("AUXILIARY STATE ANALYSIS")
    print(f"{'='*50}")

    # The issue might be that we're generating auxiliary states for the REQUESTED T-depth
    # but the actual circuit might have different T-depth structure

    print("🤔 Hypothesis: Auxiliary state generation vs circuit structure mismatch")
    print("\nFor 3q-2t:")
    print("  - Auxiliary states generated for: T-depth 2")
    print("  - Circuit has: H, CX, T, T (on same qubit)")
    print("  - Actual T-depth: 2 on qubit 0")
    print("  - This should work... investigating further")

    print("\nFor 3q-3t:")
    print("  - Auxiliary states generated for: T-depth 3")
    print("  - Circuit has: H, CX, T, T, T (on same qubit)")
    print("  - Actual T-depth: 3 on qubit 0")
    print("  - This works!")

def main():
    """Main investigation function."""
    analyze_circuit_differences()
    check_auxiliary_state_mismatch()

    print(f"\n{'='*50}")
    print("CONCLUSIONS & NEXT STEPS")
    print(f"{'='*50}")
    print("1. 🔍 Need to check why same-qubit T-gates cause issues for T-depth 2")
    print("2. 🔍 Need to compare working vs failing T-depth patterns")
    print("3. 🔍 May need to debug specific T-gate key update logic")
    print("4. 💡 Consider that multiple T-gates on same qubit might require special handling")

if __name__ == "__main__":
    main()