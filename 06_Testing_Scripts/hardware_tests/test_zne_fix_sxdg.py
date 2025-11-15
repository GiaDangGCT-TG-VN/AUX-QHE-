#!/usr/bin/env python3
"""
Test that ZNE fix handles inverse gates correctly for IBM backends.
This addresses the sxdg gate error.
"""

from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService

print("="*80)
print("Testing ZNE Fix for sxdg Gate Issue")
print("="*80)

# Load IBM backend
service = QiskitRuntimeService(name='Gia_AUX_QHE')
backend = service.backend('ibm_torino')

print(f"\n✅ Backend: {backend.name}")
print(f"   Native gates: {backend.operation_names}")
print()

# Create test circuit
qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)
qc.t(0)
qc.t(1)

print("📋 Test Circuit:")
print(f"   Gates: {[inst.operation.name for inst in qc.data]}")
print()

# Transpile to ibm_torino (simulates what happens before ZNE)
print("🔄 Transpiling to ibm_torino with opt_level=3...")
qc_transpiled = transpile(qc, backend, optimization_level=3)

print(f"   Transpiled gates: {set([inst.operation.name for inst in qc_transpiled.data])}")
print(f"   Total gates: {len([i for i in qc_transpiled.data if i.operation.name not in ['measure', 'barrier']])}")
print()

# Manual folding (simulates ZNE noise factor=2)
print("🔬 Folding gates (factor=2)...")
qc_folded = qc_transpiled.copy()

for inst in qc_transpiled.data:
    gate = inst.operation
    if gate.name in ['measure', 'barrier']:
        continue
    qubits = inst.qubits
    qc_folded.append(gate, qubits)
    qc_folded.append(gate.inverse(), qubits)

folded_gates = [inst.operation.name for inst in qc_folded.data if inst.operation.name not in ['measure', 'barrier']]
print(f"   Folded gates: {set(folded_gates)}")
print(f"   Total gates: {len(folded_gates)}")
print(f"   Contains sxdg? {('sxdg' in folded_gates)}")
print(f"   Contains sx? {('sx' in folded_gates)}")
print()

# Check if sxdg is in backend's native gates
if 'sxdg' in folded_gates:
    if 'sxdg' not in backend.operation_names:
        print(f"   ⚠️  sxdg NOT in backend's native gates!")
        print(f"   ❌ This would cause: 'instruction sxdg not supported' error")
        print()

        # Apply fix: transpile with opt=0
        print("🔧 Applying fix: transpile with opt_level=0...")
        qc_folded_fixed = transpile(
            qc_folded,
            backend,
            optimization_level=0,
            initial_layout=list(range(qc_folded.num_qubits))
        )

        fixed_gates = [inst.operation.name for inst in qc_folded_fixed.data if inst.operation.name not in ['measure', 'barrier']]
        print(f"   Fixed gates: {set(fixed_gates)}")
        print(f"   Total gates: {len(fixed_gates)}")
        print(f"   Contains sxdg? {('sxdg' in fixed_gates)}")
        print()

        # Verify all gates are supported
        unsupported = [g for g in set(fixed_gates) if g not in backend.operation_names]
        if unsupported:
            print(f"   ❌ Still has unsupported gates: {unsupported}")
        else:
            print(f"   ✅ All gates now supported by backend!")

        # Verify fold ratio
        original_count = len([i for i in qc_transpiled.data if i.operation.name not in ['measure', 'barrier']])
        fixed_count = len(fixed_gates)
        fold_ratio = fixed_count / original_count

        print(f"\n📊 Fold Ratio:")
        print(f"   Original: {original_count} gates")
        print(f"   After folding + fix: {fixed_count} gates")
        print(f"   Ratio: {fold_ratio:.2f}× (expected ~3.0× for factor=2)")

        if fold_ratio >= 2.5:
            print(f"   ✅ Folding preserved!")
        else:
            print(f"   ❌ WARNING: Folding may have been optimized away!")
    else:
        print(f"   ✅ sxdg IS in backend's native gates (no issue)")
else:
    print(f"   ✅ No sxdg gates created (no issue)")

print("\n" + "="*80)
print("Test Complete")
print("="*80)
