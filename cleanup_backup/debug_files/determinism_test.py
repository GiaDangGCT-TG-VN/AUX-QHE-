#!/usr/bin/env python3
"""
Test determinism of AUX-QHE algorithm to find why results are inconsistent.
"""

from openqasm_performance_comparison import OpenQASMPerformanceComparator
import numpy as np

def test_determinism():
    """Test if the same configuration gives consistent results."""
    print("🔍 TESTING DETERMINISM OF AUX-QHE ALGORITHM")
    print("="*60)

    comparator = OpenQASMPerformanceComparator()

    # Test the same configuration multiple times
    config = ("3q-2t", 3, 2)
    config_name, num_qubits, max_t_depth = config

    print(f"Testing {config_name} configuration 5 times:")
    print("-" * 40)

    results = []

    for run in range(5):
        print(f"\nRun {run + 1}:")
        try:
            result = comparator.run_aux_qhe_benchmark(
                config_name, num_qubits, max_t_depth
            )

            qasm2_fidelity = result.get('qasm2_fidelity', 'N/A')
            qasm3_fidelity = result.get('qasm3_fidelity', 'N/A')

            print(f"  QASM2 Fidelity: {qasm2_fidelity}")
            print(f"  QASM3 Fidelity: {qasm3_fidelity}")

            results.append({
                'run': run + 1,
                'qasm2_fidelity': qasm2_fidelity,
                'qasm3_fidelity': qasm3_fidelity
            })

        except Exception as e:
            print(f"  ❌ Error: {e}")
            results.append({
                'run': run + 1,
                'qasm2_fidelity': 'ERROR',
                'qasm3_fidelity': 'ERROR'
            })

    # Analyze results
    print(f"\n{'='*60}")
    print("DETERMINISM ANALYSIS")
    print(f"{'='*60}")

    qasm2_fidelities = [r['qasm2_fidelity'] for r in results if r['qasm2_fidelity'] != 'ERROR']
    qasm3_fidelities = [r['qasm3_fidelity'] for r in results if r['qasm3_fidelity'] != 'ERROR']

    if qasm2_fidelities:
        qasm2_unique = len(set(qasm2_fidelities))
        print(f"QASM2 Results: {qasm2_fidelities}")
        print(f"QASM2 Unique values: {qasm2_unique}")
        if qasm2_unique == 1:
            print("✅ QASM2 is deterministic")
        else:
            print("❌ QASM2 is NON-deterministic")

    if qasm3_fidelities:
        qasm3_unique = len(set(qasm3_fidelities))
        print(f"QASM3 Results: {qasm3_fidelities}")
        print(f"QASM3 Unique values: {qasm3_unique}")
        if qasm3_unique == 1:
            print("✅ QASM3 is deterministic")
        else:
            print("❌ QASM3 is NON-deterministic")

def test_multiple_configs():
    """Test multiple configurations once each to see the pattern."""
    print(f"\n{'='*60}")
    print("TESTING MULTIPLE CONFIGURATIONS")
    print(f"{'='*60}")

    comparator = OpenQASMPerformanceComparator()

    configs = [
        ("3q-2t", 3, 2),
        ("3q-3t", 3, 3),
        ("4q-2t", 4, 2),
        ("5q-2t", 5, 2)
    ]

    for config_name, num_qubits, max_t_depth in configs:
        print(f"\nTesting {config_name}:")
        try:
            result = comparator.run_aux_qhe_benchmark(
                config_name, num_qubits, max_t_depth
            )

            qasm2_fidelity = result.get('qasm2_fidelity', 'N/A')
            qasm3_fidelity = result.get('qasm3_fidelity', 'N/A')

            print(f"  QASM2: {qasm2_fidelity}")
            print(f"  QASM3: {qasm3_fidelity}")

        except Exception as e:
            print(f"  ❌ Error: {e}")

def main():
    """Main test function."""
    test_determinism()
    test_multiple_configs()

if __name__ == "__main__":
    main()