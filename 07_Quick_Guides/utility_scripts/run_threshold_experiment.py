#!/usr/bin/env python3
"""
Run AUX-QHE practical threshold experiment.

Tests 4 configurations: 4q-3t, 5q-1t, 5q-2t, 5q-3t
With 4 methods each: Baseline, ZNE, Opt-3, Opt-3+ZNE

Intelligently skips methods that cause T-depth explosion beyond threshold (>3).
"""

import sys
sys.path.insert(0, 'core')

from ibm_hardware_noise_experiment import run_full_experiment

if __name__ == '__main__':
    print("="*100)
    print("🎯 AUX-QHE PRACTICAL THRESHOLD EXPERIMENT")
    print("="*100)
    print("\n📋 Configurations to test:")
    print("   - 4q-3t: 4 qubits, T-depth 3")
    print("   - 5q-1t: 5 qubits, T-depth 1")
    print("   - 5q-2t: 5 qubits, T-depth 2")
    print("   - 5q-3t: 5 qubits, T-depth 3 (practical threshold)")
    print("\n🔬 Methods to test (where feasible):")
    print("   - Baseline (opt_level=1)")
    print("   - ZNE (opt_level=1 + error mitigation)")
    print("   - Opt-3 (opt_level=3)")
    print("   - Opt-3+ZNE (opt_level=3 + error mitigation)")
    print("\n⚠️  Note: Methods causing T-depth explosion (>3) will be skipped")
    print("="*100)

    # Run experiment with all 4 configurations
    configs = [
        {'name': '4q-3t', 'qubits': 4, 't_depth': 3},
        {'name': '5q-1t', 'qubits': 5, 't_depth': 1},
        {'name': '5q-2t', 'qubits': 5, 't_depth': 2},
        {'name': '5q-3t', 'qubits': 5, 't_depth': 3},
    ]

    results = run_full_experiment(
        configs=configs,
        backend_name='ibm_brisbane',
        shots=1024  # Use 1024 shots for faster testing
    )

    if results is not None:
        print("\n" + "="*100)
        print("✅ EXPERIMENT COMPLETED SUCCESSFULLY!")
        print("="*100)
        print(f"\nTotal successful experiments: {len(results)}")
        print("\nResults saved to:")
        print("   - ibm_noise_measurement_results_<timestamp>.csv")
        print("   - ibm_noise_measurement_results_<timestamp>.json")
    else:
        print("\n" + "="*100)
        print("❌ EXPERIMENT FAILED")
        print("="*100)
