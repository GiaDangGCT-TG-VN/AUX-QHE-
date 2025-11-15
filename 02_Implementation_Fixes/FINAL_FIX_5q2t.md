# CRITICAL BUG IDENTIFIED: 5q-2t Hardware Execution

## Problem Summary

**LOCAL SIMULATION:** 99.9999% fidelity ✅
**HARDWARE:** 0% fidelity ❌

## Root Cause

From your hardware logs:
```
🔍 DEBUG: First 3 keys: ['0000000000000010000000000010000000...000000110', ...]
```

These bitstrings are **~140 characters long**, but we only have **5 qubits**!

**The hardware is measuring 140+ qubits instead of 5!**

## Why This Happens

Looking at the transpilation output:
- Pre-folding gates: 148
- Original circuit: 10 gates (H, CNOT, 2×T, QOTP gates)

Transpilation is adding **ancilla qubits** or decomposing gates in a way that creates extra qubits.

## The Fix

**Option 1: Measure only first 5 qubits (RECOMMENDED)**

Change line 334 in `ibm_hardware_noise_experiment.py`:

```python
# BEFORE:
qc_transpiled.measure_all()

# AFTER:
from qiskit import ClassicalRegister
if qc_transpiled.num_qubits > num_qubits:
    # Transpilation added ancilla qubits - only measure original qubits
    qc_transpiled.add_register(ClassicalRegister(num_qubits, 'meas'))
    for i in range(num_qubits):
        qc_transpiled.measure(i, i)
else:
    qc_transpiled.measure_all()
```

**Option 2: Use initial_layout to prevent ancilla allocation**

Add to transpilation (line 318):

```python
qc_transpiled = transpile(
    qc_encrypted,
    backend=backend,
    optimization_level=optimization_level,
    seed_transpiler=42,
    initial_layout=list(range(num_qubits))  # ← ADD THIS
)
```

## Why Hardware Shows 140 Qubits

The bitstring length from your log:
`'000000000000001000000000000100000000000000000001000000...00110'`

Count: ~140 characters = ~140 qubits!

IBM's backend has 133 qubits. Transpilation is likely:
1. Adding ancilla qubits for decomposing complex gates
2. Using swap gates to route connections
3. Measuring all 133 physical qubits instead of just the 5 logical ones

## Expected Fix Results

After applying Option 1 or 2:
- Measurement bitstrings should be **5 characters** long (e.g., "00011", "00000")
- Decoded counts should collapse to **2 outcomes** (|00000⟩ and |00011⟩)
- Fidelity should be **>40%** (accounting for hardware noise)

##Implementation

I'll implement Option 2 (safer and cleaner).
