# 🧪 AUX-QHE Testing Guide

This guide shows you how to test your AUX-QHE implementation.

---

## ✅ Quick Start - Run All Tests

The fastest way to verify everything works:

```bash
# Quick integration test (3q-2t configuration)
python quick_test.py

# Full benchmark (all 6 configurations)
python algorithm/openqasm_performance_comparison.py
```

**Expected Results:**
- ✅ Quick test: Fidelity = 1.000000
- ✅ Full benchmark: All 6 configs with Fidelity = 1.0000

---

## 📊 Test Options

### 1️⃣ Quick Test (Recommended for verification)

**Purpose:** Fast smoke test to verify the implementation works

```bash
python quick_test.py
```

**What it tests:**
- BFV initialization
- Quantum circuit creation (3q-2t)
- QOTP key generation (including the fixed auxiliary key generation!)
- Circuit encryption with QOTP
- T-gadget evaluation
- Circuit decryption
- Fidelity verification

**Runtime:** ~1 second  
**Expected:** Fidelity = 1.000000 ✅

---

### 2️⃣ Full Benchmark (Comprehensive testing)

**Purpose:** Test all configurations and measure performance

```bash
python algorithm/openqasm_performance_comparison.py
```

**What it tests:**
- **6 configurations:**
  - 3q-2t (3 qubits, T-depth 2)
  - 3q-3t (3 qubits, T-depth 3)
  - 4q-2t (4 qubits, T-depth 2) ← Previously failing, now fixed!
  - 4q-3t (4 qubits, T-depth 3)
  - 5q-2t (5 qubits, T-depth 2)
  - 5q-3t (5 qubits, T-depth 3)
- OpenQASM 2 vs OpenQASM 3 comparison
- Performance metrics (timing, overhead)

**Runtime:** ~1-2 seconds  
**Expected:** All configs with Fidelity = 1.0000 ✅

**Output:** CSV file with detailed results
- Saved to: `corrected_openqasm_performance_comparison.csv`

---

### 3️⃣ Test Individual Modules

**Purpose:** Debug or verify specific components

#### Test BFV Core:
```bash
python core/bfv_core.py
```
Expected: Mock BFV encryption/decryption test passes

#### Test QOTP Crypto:
```bash
python core/qotp_crypto.py
```
Expected: "✅ QOTP encryption/decryption successful"

#### Test Key Generation:
```bash
python -c "
import sys
sys.path.insert(0, 'core')
from key_generation import aux_keygen
prep, eval_key, dec, time, total = aux_keygen(3, 2, [1,0,1], [0,1,0])
print(f'✅ Generated {total} auxiliary states')
"
```
Expected: "✅ Generated 240 auxiliary states"

---

## 🎯 Understanding Test Results

### Fidelity Metric

**Fidelity** measures how similar two quantum states are:
- **1.0** = Perfect match (what we want!)
- **0.0** = Completely different

**For AUX-QHE:** We expect fidelity ≈ 1.0 (typically 0.9999999999999993 due to floating point)

### What Good Results Look Like:

```
✅ TEST PASSED - AUX-QHE implementation is working correctly!
   Fidelity: 1.000000
```

```
3q-2t|  QASM2|  1.0000|  0.0000  ✅
3q-3t|  QASM2|  1.0000|  0.0000  ✅
4q-2t|  QASM2|  1.0000|  0.0000  ✅
...
```

---

## 🔍 Verifying the Recent Fix

The recent fix addressed a bug where auxiliary k-values were circuit-size dependent. 

**To verify the fix is working:**

Run the full benchmark and check that **4q-2t** and **3q-2t** both pass:

```bash
python algorithm/openqasm_performance_comparison.py 2>&1 | grep "Fidelity:"
```

You should see:
```
Fidelity: 1.000000  ← 3q-2t ✅
Fidelity: 1.000000  ← 3q-3t ✅
Fidelity: 1.000000  ← 4q-2t ✅ (was failing before fix!)
Fidelity: 1.000000  ← 4q-3t ✅
Fidelity: 1.000000  ← 5q-2t ✅
Fidelity: 1.000000  ← 5q-3t ✅
```

---

## 🐛 Troubleshooting

### Test Fails with Import Error

**Problem:** `ModuleNotFoundError: No module named 'core'`

**Solution:**
```bash
# Make sure you're in the AUX-QHE directory
cd /Users/giadang/my_qiskitenv/AUX-QHE

# Or add the path
export PYTHONPATH=/Users/giadang/my_qiskitenv/AUX-QHE:$PYTHONPATH
```

### Low Fidelity Results

**Problem:** Fidelity < 0.99

**Possible causes:**
1. Code was modified incorrectly
2. The fix in `core/key_generation.py` was reverted
3. Dependencies are outdated

**Solution:**
1. Check that `core/key_generation.py` line 324 has:
   ```python
   k_hash = f"aux_{ell}_{wire}_{term}"
   ```
   NOT:
   ```python
   k_hash = f"{config_hash}_aux_{ell}_{wire}_{term_idx}"
   ```

2. Verify all core files are present:
   ```bash
   ls core/*.py
   # Should show: bfv_core.py, circuit_evaluation.py, key_generation.py,
   #              openqasm3_integration.py, qotp_crypto.py, t_gate_gadgets.py
   ```

---

## 📚 What Each Test Validates

| Test | What It Checks | Key Components |
|------|----------------|----------------|
| **quick_test.py** | End-to-end pipeline | All modules integrated |
| **Full benchmark** | All configurations | Scalability, correctness |
| **BFV core** | Homomorphic encryption | BFV scheme |
| **QOTP crypto** | Quantum encryption | QOTP operations |
| **Key generation** | Auxiliary states | The recent fix! |

---

## 🎓 Next Steps

After all tests pass:

1. ✅ Your implementation is correct
2. ✅ The auxiliary key generation fix is working
3. ✅ Ready to use in your research/application

To use in your code:
```python
from core.key_generation import aux_keygen
from core.circuit_evaluation import aux_eval
from core.qotp_crypto import qotp_encrypt, qotp_decrypt
```

---

## 📊 Performance Metrics

Typical performance (from full benchmark):

| Config | Aux States | Time (s) | Fidelity |
|--------|------------|----------|----------|
| 3q-2t  | 240        | ~0.25    | 1.0000   |
| 3q-3t  | 2,826      | ~0.08    | 1.0000   |
| 4q-2t  | 668        | ~0.04    | 1.0000   |
| 4q-3t  | 10,776     | ~0.24    | 1.0000   |
| 5q-2t  | 1,350      | ~0.05    | 1.0000   |
| 5q-3t  | 31,025     | ~0.67    | 1.0000   |

---

**Last Updated:** October 5, 2025  
**Fix Applied:** Auxiliary k-value generation (circuit-size independence)
