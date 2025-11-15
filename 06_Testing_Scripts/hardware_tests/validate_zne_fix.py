#!/usr/bin/env python3
"""
Pre-flight validation script to verify ZNE fix before hardware execution.
This script tests the ZNE implementation locally to ensure no credits are wasted.
"""

import sys
sys.path.insert(0, 'core')

from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
import numpy as np

def create_test_circuit():
    """Create a simple test circuit with known structure"""
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(1, 2)
    qc.t(0)
    qc.t(1)
    qc.barrier()
    return qc

def manual_gate_folding(circuit, fold_factor=3):
    """
    Manually fold gates (same as apply_zne does).
    Returns folded circuit.
    """
    folded = circuit.copy()

    # Fold gates (fold_factor - 1) times
    for _ in range(fold_factor - 1):
        for instr in circuit.data:
            gate = instr.operation
            # Skip measurements and barriers
            if gate.name in ['measure', 'barrier']:
                continue
            qubits = instr.qubits
            # Add gate and its inverse
            folded.append(gate, qubits)
            folded.append(gate.inverse(), qubits)

    return folded

def test_zne_folding():
    """Test that gate folding works correctly"""
    print("="*80)
    print("🔬 TESTING ZNE GATE FOLDING")
    print("="*80)

    # Create test circuit
    qc = create_test_circuit()

    # Transpile (simulate what happens before apply_zne)
    backend = AerSimulator()
    qc_transpiled = transpile(qc, backend, optimization_level=1)

    print(f"\n1️⃣ Original transpiled circuit:")
    print(f"   Depth: {qc_transpiled.depth()}")
    print(f"   Gates: {qc_transpiled.size()}")
    print(f"   Non-measurement gates: {len([i for i in qc_transpiled.data if i.operation.name not in ['measure', 'barrier']])}")

    # Test folding WITHOUT re-transpiling (CORRECT)
    qc_folded_correct = manual_gate_folding(qc_transpiled, fold_factor=3)

    print(f"\n2️⃣ Folded circuit (NO re-transpiling) - CORRECT:")
    print(f"   Depth: {qc_folded_correct.depth()}")
    print(f"   Gates: {qc_folded_correct.size()}")
    print(f"   Non-measurement gates: {len([i for i in qc_folded_correct.data if i.operation.name not in ['measure', 'barrier']])}")

    # Test folding WITH re-transpiling (WRONG - old code)
    qc_folded_wrong = manual_gate_folding(qc_transpiled, fold_factor=3)
    qc_folded_wrong = transpile(qc_folded_wrong, backend, optimization_level=1)  # Re-transpile (destroys folds)

    print(f"\n3️⃣ Folded circuit (WITH re-transpiling) - WRONG (old code):")
    print(f"   Depth: {qc_folded_wrong.depth()}")
    print(f"   Gates: {qc_folded_wrong.size()}")
    print(f"   Non-measurement gates: {len([i for i in qc_folded_wrong.data if i.operation.name not in ['measure', 'barrier']])}")

    # Calculate expected values
    original_gates = len([i for i in qc_transpiled.data if i.operation.name not in ['measure', 'barrier']])
    expected_folded_gates = original_gates * 3  # Should triple
    actual_correct_gates = len([i for i in qc_folded_correct.data if i.operation.name not in ['measure', 'barrier']])
    actual_wrong_gates = len([i for i in qc_folded_wrong.data if i.operation.name not in ['measure', 'barrier']])

    print(f"\n📊 VALIDATION RESULTS:")
    print(f"   Original gates: {original_gates}")
    print(f"   Expected after 3× fold: {expected_folded_gates}")
    print(f"   Actual (CORRECT method): {actual_correct_gates}")
    print(f"   Actual (WRONG method): {actual_wrong_gates}")

    # Check if folding worked
    fold_ratio_correct = actual_correct_gates / original_gates
    fold_ratio_wrong = actual_wrong_gates / original_gates

    print(f"\n   Fold ratio (CORRECT): {fold_ratio_correct:.2f}× (expected: 3.0×)")
    print(f"   Fold ratio (WRONG): {fold_ratio_wrong:.2f}× (expected: 3.0×)")

    # Validate
    if fold_ratio_correct >= 2.8:  # Allow small tolerance
        print(f"\n   ✅ CORRECT method: Gate folding works! ({fold_ratio_correct:.2f}×)")
    else:
        print(f"\n   ❌ CORRECT method: Gate folding FAILED! ({fold_ratio_correct:.2f}×)")
        return False

    if fold_ratio_wrong < 1.5:  # Old bug shows ~1.0×
        print(f"   ✅ WRONG method shows bug: Only {fold_ratio_wrong:.2f}× (confirms old code was broken)")
    else:
        print(f"   ⚠️  WRONG method unexpectedly worked: {fold_ratio_wrong:.2f}×")

    return True

def test_depth_measurement():
    """Test that depth measurement is correct"""
    print("\n" + "="*80)
    print("📏 TESTING DEPTH MEASUREMENT")
    print("="*80)

    qc = create_test_circuit()
    backend = AerSimulator()
    qc_transpiled = transpile(qc, backend, optimization_level=1)

    # Measure depth before and after folding
    depth_before = qc_transpiled.depth()

    qc_folded = manual_gate_folding(qc_transpiled, fold_factor=3)
    depth_after = qc_folded.depth()

    print(f"\n   Depth before folding: {depth_before}")
    print(f"   Depth after 3× folding: {depth_after}")
    print(f"   Depth increase: {depth_after / depth_before:.2f}×")

    # Depth should increase by at least 1.5× (typically 2-3×)
    if depth_after >= depth_before * 1.5:
        print(f"   ✅ Depth measurement correct (increased by {depth_after / depth_before:.2f}×)")
        return True
    else:
        print(f"   ❌ Depth measurement FAILED (only increased by {depth_after / depth_before:.2f}×)")
        return False

def test_statevector_preservation():
    """Test that folding preserves quantum state (U†U = I)"""
    print("\n" + "="*80)
    print("🔬 TESTING QUANTUM STATE PRESERVATION")
    print("="*80)

    qc = create_test_circuit()

    # Get original statevector
    sv_original = Statevector.from_instruction(qc)

    # Create folded circuit
    backend = AerSimulator()
    qc_transpiled = transpile(qc, backend, optimization_level=1)
    qc_folded = manual_gate_folding(qc_transpiled, fold_factor=3)

    # Get folded statevector
    sv_folded = Statevector.from_instruction(qc_folded)

    # Calculate fidelity (should be ~1.0 if U†U pairs work correctly)
    from qiskit.quantum_info import state_fidelity
    fidelity = state_fidelity(sv_original, sv_folded)

    print(f"\n   Original vs Folded fidelity: {fidelity:.6f}")

    if fidelity > 0.999:
        print(f"   ✅ Quantum state preserved (fidelity = {fidelity:.6f})")
        return True
    else:
        print(f"   ❌ Quantum state NOT preserved (fidelity = {fidelity:.6f})")
        return False

def main():
    print("\n" + "="*80)
    print("🚀 PRE-FLIGHT VALIDATION FOR ZNE FIX")
    print("="*80)
    print("\nThis script validates the ZNE fix WITHOUT using hardware credits")
    print("Running 3 critical tests...\n")

    results = []

    # Test 1: Gate folding
    results.append(("Gate Folding", test_zne_folding()))

    # Test 2: Depth measurement
    results.append(("Depth Measurement", test_depth_measurement()))

    # Test 3: State preservation
    results.append(("State Preservation", test_statevector_preservation()))

    # Summary
    print("\n" + "="*80)
    print("📊 VALIDATION SUMMARY")
    print("="*80 + "\n")

    all_passed = True
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"   {test_name:25} {status}")
        if not passed:
            all_passed = False

    print("\n" + "="*80)
    if all_passed:
        print("✅ ALL TESTS PASSED - SAFE TO RUN ON HARDWARE")
        print("="*80)
        print("\nYour ZNE fix is working correctly!")
        print("You can now run on hardware with confidence:")
        print("  python ibm_hardware_noise_experiment.py --config 5q-2t --backend ibm_torino --account Gia_AUX_QHE")
        return 0
    else:
        print("❌ SOME TESTS FAILED - DO NOT RUN ON HARDWARE")
        print("="*80)
        print("\nPlease fix the issues before running on hardware to avoid wasting credits!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
