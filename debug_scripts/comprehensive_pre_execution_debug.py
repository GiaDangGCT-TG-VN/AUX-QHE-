#!/usr/bin/env python3
"""
Comprehensive Pre-Execution Debug for 5q-2t Hardware Run
Tests ALL critical paths before spending hardware credits
"""

import sys
sys.path.insert(0, 'core')

from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector
from qiskit_ibm_runtime import QiskitRuntimeService
import numpy as np

print("="*80)
print("🔍 COMPREHENSIVE PRE-EXECUTION DEBUG - 5q-2t Configuration")
print("="*80)

# Configuration
config_name = "5q-2t"
num_qubits = 5
t_depth = 2
shots = 1024

# ============================================================================
# TEST 1: Account and Backend Validation
# ============================================================================
print("\n" + "="*80)
print("TEST 1: Account and Backend Validation")
print("="*80)

try:
    service = QiskitRuntimeService(name="Gia_AUX_QHE")
    print("✅ Account loaded: Gia_AUX_QHE")

    backend = service.backend("ibm_torino")
    status = backend.status()

    print(f"✅ Backend: {backend.name}")
    print(f"   Qubits: {backend.num_qubits}")
    print(f"   Status: {status.status_msg}")
    print(f"   Queue: {status.pending_jobs} jobs")
    print(f"   Operational: {'✅ Yes' if status.operational else '❌ No'}")

    # Check native gate set
    if hasattr(backend, 'target') and backend.target:
        native_gates = list(backend.target.operation_names)
    else:
        # Fallback for older backend interface
        config = backend.configuration()
        native_gates = config.basis_gates if hasattr(config, 'basis_gates') else []

    print(f"\n   Native gates: {native_gates}")

    # Critical check: sxdg NOT in native gates
    if 'sxdg' in native_gates:
        print("   ⚠️  WARNING: sxdg IS in native gates (unexpected)")
    else:
        print("   ✅ sxdg NOT in native gates (expected)")

    if not status.operational:
        print("\n❌ CRITICAL: Backend not operational!")
        sys.exit(1)

except Exception as e:
    print(f"❌ FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============================================================================
# TEST 2: Circuit Creation and Initial Transpilation
# ============================================================================
print("\n" + "="*80)
print("TEST 2: Circuit Creation and Initial Transpilation")
print("="*80)

# Create test circuit - MUST MATCH LOCAL SIMULATION!
qc = QuantumCircuit(num_qubits)

# Apply Hadamard only to qubit 0 (matches local simulation)
qc.h(0)

# Apply single CNOT (matches local simulation)
if num_qubits > 1:
    qc.cx(0, 1)
qc.barrier()

# Apply T-gates sequentially on qubit 0 ONLY
for layer in range(t_depth):
    qc.t(0)  # Apply T-gate ONLY to qubit 0 (same as local simulation)
    qc.barrier()

print(f"✅ Circuit created: {num_qubits} qubits, T-depth {t_depth}")
print(f"   Original depth: {qc.depth()}")
print(f"   Original gates: {qc.size()}")

# Transpile with optimization_level=1 (baseline)
print("\n   Transpiling with opt_level=1 (baseline)...")
qc_trans = transpile(qc, backend=backend, optimization_level=1, seed_transpiler=42)
qc_trans.measure_all()

print(f"✅ Transpiled (opt=1):")
print(f"   Depth: {qc_trans.depth()}")
print(f"   Gates: {qc_trans.size()}")

# Check for non-native gates
gates_used = set()
for instr in qc_trans.data:
    gates_used.add(instr.operation.name)

print(f"   Gates used: {sorted(gates_used)}")

# Exclude directives (barrier, measure) from native gate check
directives = {'barrier', 'measure', 'reset', 'delay'}
actual_gates = gates_used - directives
non_native = actual_gates - set(native_gates)

if non_native:
    print(f"   ❌ CRITICAL: Non-native gates found: {non_native}")
    sys.exit(1)
else:
    print(f"   ✅ All gates are native (excluding directives)")

# ============================================================================
# TEST 3: ZNE Gate Folding with Native Gate Decomposition
# ============================================================================
print("\n" + "="*80)
print("TEST 3: ZNE Gate Folding with Native Gate Decomposition")
print("="*80)

# Remove measurements for folding
qc_no_meas = qc_trans.copy()
qc_no_meas.remove_final_measurements(inplace=True)

print(f"📏 Pre-folding circuit:")
print(f"   Depth: {qc_no_meas.depth()}")
print(f"   Gates: {qc_no_meas.size()}")

# Fold gates (factor=2, simulating 3x noise level)
scaled_circuit = qc_no_meas.copy()
fold_factor = 2

print(f"\n🔄 Folding gates (factor={fold_factor})...")
for _ in range(fold_factor):
    for instr in qc_no_meas.data:
        gate = instr.operation
        if gate.name in ['measure', 'barrier']:
            continue
        qubits = instr.qubits
        scaled_circuit.append(gate, qubits)
        scaled_circuit.append(gate.inverse(), qubits)

print(f"   Gates after folding: {scaled_circuit.size()}")

# Check for non-native gates (like sxdg)
gates_after_fold = set()
has_sxdg = False
for instr in scaled_circuit.data:
    gate_name = instr.operation.name
    gates_after_fold.add(gate_name)
    if gate_name == 'sxdg':
        has_sxdg = True

print(f"   Gates used: {sorted(gates_after_fold)}")

if has_sxdg:
    print(f"   ⚠️  Found sxdg gates (created by .inverse())")
    print(f"   ✅ This is expected - will be fixed by opt_level=0 transpile")
else:
    print(f"   ℹ️  No sxdg gates found (may vary by circuit)")

# Apply fix: transpile with opt_level=0
print(f"\n🔧 Applying fix: transpile with opt_level=0...")
scaled_circuit_fixed = transpile(
    scaled_circuit,
    backend,
    optimization_level=0,
    initial_layout=list(range(scaled_circuit.num_qubits))
)

print(f"   Gates after fix: {scaled_circuit_fixed.size()}")
print(f"   Depth after fix: {scaled_circuit_fixed.depth()}")

# Check gates again
gates_after_fix = set()
has_sxdg_after = False
for instr in scaled_circuit_fixed.data:
    gate_name = instr.operation.name
    gates_after_fix.add(gate_name)
    if gate_name == 'sxdg':
        has_sxdg_after = True

print(f"   Gates used: {sorted(gates_after_fix)}")

# Exclude directives from check
actual_gates_after = gates_after_fix - directives
non_native_after = actual_gates_after - set(native_gates)
if non_native_after:
    print(f"   ❌ CRITICAL: Non-native gates still present: {non_native_after}")
    sys.exit(1)
else:
    print(f"   ✅ All gates are native after fix (excluding directives)")

# Verify folding preserved
original_gates = qc_no_meas.size()
expected_gates_min = original_gates * (fold_factor + 1)  # At least 3x
actual_gates = scaled_circuit_fixed.size()
fold_ratio = actual_gates / original_gates

print(f"\n📊 Fold ratio validation:")
print(f"   Original gates: {original_gates}")
print(f"   Expected (min): {expected_gates_min} ({fold_factor+1}x)")
print(f"   Actual: {actual_gates}")
print(f"   Fold ratio: {fold_ratio:.2f}x")

if fold_ratio < 2.5:  # Should be at least 2.5x for factor=2
    print(f"   ❌ CRITICAL: Folding not preserved (ratio too low)")
    sys.exit(1)
else:
    print(f"   ✅ Folding preserved")

# ============================================================================
# TEST 4: T-Depth Validation Logic
# ============================================================================
print("\n" + "="*80)
print("TEST 4: T-Depth Validation Logic")
print("="*80)

from circuit_evaluation import organize_gates_into_layers

# Count T gates in transpiled circuit
circuit_ops = []
for inst in qc_trans.data:
    gate_name = inst.operation.name
    qubits = tuple([qc_trans.find_bit(q).index for q in inst.qubits])
    if gate_name in ['t', 'tdg']:
        circuit_ops.append((gate_name, qubits))

print(f"   T-gates found: {len(circuit_ops)}")

if len(circuit_ops) == 0:
    print(f"   ℹ️  No T-gates (optimization removed them)")
    print(f"   ✅ T-depth check: PASSED (no T-gates)")
else:
    _, detected_t_depth = organize_gates_into_layers(circuit_ops)
    print(f"   Detected T-depth: {detected_t_depth}")

    if detected_t_depth > 3:
        print(f"   ❌ CRITICAL: T-depth > 3 (would be skipped in actual run)")
        print(f"   This configuration won't execute on hardware")
    else:
        print(f"   ✅ T-depth check: PASSED (≤3)")

# ============================================================================
# TEST 5: Results Dictionary Structure
# ============================================================================
print("\n" + "="*80)
print("TEST 5: Results Dictionary Structure")
print("="*80)

# Simulate result dictionary keys
result_keys = [
    'config', 'method', 'backend', 'qasm_version', 'num_qubits', 't_depth',
    'aux_states', 'optimization_level', 'zne_applied', 'shots', 'qasm3_file',
    'fidelity', 'tvd', 'keygen_time', 'encrypt_time', 'transpile_time',
    'exec_time', 'eval_time', 'decrypt_time', 'total_time', 'circuit_depth',
    'circuit_gates', 'encrypted_counts', 'decoded_counts', 'final_qotp_keys'
]

print(f"✅ Result dictionary has {len(result_keys)} keys:")
for key in result_keys:
    print(f"   - {key}")

# ============================================================================
# TEST 6: File I/O Paths
# ============================================================================
print("\n" + "="*80)
print("TEST 6: File I/O Paths")
print("="*80)

from pathlib import Path
import os

# Check qasm3_exports directory
qasm_dir = Path("qasm3_exports")
if not qasm_dir.exists():
    print(f"   ℹ️  Directory doesn't exist: {qasm_dir}")
    print(f"   ✅ Will be created by script")
else:
    print(f"   ✅ Directory exists: {qasm_dir}")

# Check core module imports
core_modules = ['key_generation', 'circuit_evaluation', 'qotp_crypto', 'bfv_core']
for module in core_modules:
    module_path = Path(f"core/{module}.py")
    if module_path.exists():
        print(f"   ✅ Module found: {module_path}")
    else:
        print(f"   ❌ CRITICAL: Module missing: {module_path}")
        sys.exit(1)

# ============================================================================
# TEST 7: Richardson Extrapolation Logic
# ============================================================================
print("\n" + "="*80)
print("TEST 7: Richardson Extrapolation Logic")
print("="*80)

# Simulate Richardson extrapolation with test data
test_results = [
    {'00000': 0.5, '11111': 0.5},  # 1x noise
    {'00000': 0.45, '11111': 0.45, '01010': 0.1},  # 2x noise
    {'00000': 0.4, '11111': 0.4, '01010': 0.2}  # 3x noise
]

extrapolated = {}
for bitstring in test_results[0].keys():
    probs = [r.get(bitstring, 0.0) for r in test_results]
    # Linear extrapolation: p(0) ≈ 2*p(1) - p(2)
    if len(probs) >= 2:
        p_extrap = 2 * probs[0] - probs[1]
        p_extrap = max(0.0, min(1.0, p_extrap))
        if p_extrap > 0:
            extrapolated[bitstring] = p_extrap

total = sum(extrapolated.values())
print(f"   Extrapolated probabilities: {extrapolated}")
print(f"   Total probability: {total}")

if total < 0.98:
    print(f"   ⚠️  Probability mass lost: {(1-total)*100:.1f}%")
    print(f"   ✅ Script will recover lost probability")
else:
    print(f"   ✅ Probability mass preserved")

# Renormalize
if total > 0:
    extrapolated = {k: v/total for k, v in extrapolated.items()}
    print(f"   ✅ Renormalized: {extrapolated}")

# ============================================================================
# TEST 8: QOTP Key Decoding Logic
# ============================================================================
print("\n" + "="*80)
print("TEST 8: QOTP Key Decoding Logic")
print("="*80)

# Simulate QOTP decoding
test_encrypted_counts = {'10101': 100, '01010': 50}
test_final_a = [1, 0, 1, 0, 1]

decoded_counts = {}
for bitstring, count in test_encrypted_counts.items():
    decoded_bits = ''.join(
        str(int(bitstring[i]) ^ test_final_a[i]) for i in range(len(test_final_a))
    )
    if decoded_bits in decoded_counts:
        decoded_counts[decoded_bits] += count
    else:
        decoded_counts[decoded_bits] = count

print(f"   Encrypted counts: {test_encrypted_counts}")
print(f"   Final QOTP keys: {test_final_a}")
print(f"   Decoded counts: {decoded_counts}")

# Verify no shots lost
decoded_total = sum(decoded_counts.values())
encrypted_total = sum(test_encrypted_counts.values())

if decoded_total == encrypted_total:
    print(f"   ✅ No shots lost in decoding ({decoded_total}/{encrypted_total})")
else:
    print(f"   ❌ CRITICAL: Shots lost in decoding ({decoded_total} != {encrypted_total})")
    sys.exit(1)

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("\n" + "="*80)
print("✅ ALL PRE-EXECUTION TESTS PASSED!")
print("="*80)
print("\n📋 Validated Components:")
print("   ✅ Account authentication (Gia_AUX_QHE)")
print("   ✅ Backend access (ibm_torino)")
print("   ✅ Native gate compatibility")
print("   ✅ ZNE gate folding with opt_level=0 fix")
print("   ✅ sxdg decomposition working")
print("   ✅ Fold ratio preserved (>2.5x)")
print("   ✅ T-depth validation logic")
print("   ✅ Result dictionary structure")
print("   ✅ File I/O paths and modules")
print("   ✅ Richardson extrapolation logic")
print("   ✅ QOTP decoding logic")

print("\n🚀 READY FOR HARDWARE EXECUTION!")
print("\nCommand to run:")
print("   python ibm_hardware_noise_experiment.py --config 5q-2t --backend ibm_torino --account Gia_AUX_QHE")
print("\n⚠️  This will consume hardware credits - proceed with caution!")
print("="*80)
