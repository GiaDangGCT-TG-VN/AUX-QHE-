# ⚠️ Table Anomaly Analysis: Circuit Depth Inconsistencies

**Date:** 2025-10-24
**Issue:** Several metrics in hardware comparison table are contradictory/unexpected

---

## 🔍 Identified Anomalies

### ANOMALY 1: ZNE Should INCREASE Depth, But Sometimes Stays Same ⚠️

**What ZNE Does:**
- Applies gate folding (adds gate + inverse pairs)
- Should ALWAYS increase circuit depth/gates
- Example: Circuit with depth 18 → depth ~36-54 after folding

**Problem in Your Table:**

#### 4q-3t:
```
Baseline:    Depth=16, Gates=164
ZNE:         Depth=16, Gates=164  ← SAME as Baseline! ❌
Opt-3+ZNE:   Depth=18, Gates=164  ← Only +2 depth ⚠️
```

**Expected:**
```
Baseline:    Depth=16, Gates=164
ZNE:         Depth=32-48, Gates=328-492  ← Should DOUBLE or TRIPLE
Opt-3+ZNE:   Depth=36-54, Gates=328-492
```

**Conclusion:** ZNE data for 4q-3t is **WRONG** or ZNE was **NOT applied**

---

#### 5q-3t:
```
Baseline:    Depth=19, Gates=175
ZNE:         Depth=19, Gates=176  ← Only +1 gate! ❌
Opt-3+ZNE:   Depth=14, Gates=165  ← DECREASED depth! ❌❌❌
```

**Expected:**
```
Baseline:    Depth=19, Gates=175
ZNE:         Depth=38-57, Gates=350-525  ← Should DOUBLE or TRIPLE
Opt-3+ZNE:   Depth=28-42, Gates=330-495
```

**Conclusion:** ZNE data for 5q-3t is **COMPLETELY WRONG**

---

#### 5q-2t (Your NEW data):
```
Baseline:    Depth=18, Gates=170
ZNE:         Depth=19, Gates=172  ← Only +1 depth, +2 gates ❌
Opt-3+ZNE:   Depth=27, Gates=173  ← Only +9 depth ⚠️
```

**Expected:**
```
Baseline:    Depth=18, Gates=170
ZNE:         Depth=36-54, Gates=340-510  ← Should DOUBLE or TRIPLE
Opt-3+ZNE:   Depth=26-39, Gates=320-480
```

**Conclusion:** ZNE data for 5q-2t shows **MINIMAL** increase (suspicious)

---

### ANOMALY 2: Opt-3+ZNE Has LOWER Depth Than Opt-3 Alone ❌

#### 5q-3t (CRITICAL ERROR):
```
Opt-3:       Depth=15, Gates=167
Opt-3+ZNE:   Depth=14, Gates=165  ← LOWER than Opt-3! ❌❌❌
```

**This is IMPOSSIBLE!**
- ZNE adds gates (folding)
- Opt-3+ZNE must have depth ≥ Opt-3
- Getting LOWER depth means ZNE was NOT applied

**Conclusion:** 5q-3t Opt-3+ZNE data is **WRONG**

---

#### 4q-3t:
```
Opt-3:       Depth=21, Gates=166
Opt-3+ZNE:   Depth=18, Gates=164  ← LOWER than Opt-3! ❌❌❌
```

**This is IMPOSSIBLE!**

**Conclusion:** 4q-3t Opt-3+ZNE data is also **WRONG**

---

### ANOMALY 3: Opt-3 Sometimes INCREASES Depth ⚠️

#### 4q-3t:
```
Baseline:    Depth=16, Gates=164
Opt-3:       Depth=21, Gates=166  ← INCREASED by +5! ⚠️
```

**Expected:** Opt-3 should DECREASE depth (that's the point of optimization!)

**Possible Explanation:**
- Opt-3 may increase depth on some backends if it prioritizes CNOT reduction over depth
- This CAN happen if circuit topology requires more swaps for qubit routing
- **Not necessarily wrong**, but unexpected

---

## 🔬 Root Cause Analysis

### Theory 1: Circuit Depth/Gates Are From DIFFERENT Stages ✅ (Most Likely)

**Hypothesis:** The depth/gates shown are NOT from the same circuit that ZNE ran

**Evidence:**

#### What Likely Happened:
```python
# Step 1: Transpile circuit (get depth/gates)
qc_transpiled = transpile(circuit, backend, optimization_level=1)
circuit_depth = qc_transpiled.depth()  # Record: 19
circuit_gates = qc_transpiled.size()   # Record: 175

# Step 2: Apply ZNE (adds folding)
qc_zne = apply_zne(qc_transpiled)  # NOW depth is ~38-57

# Step 3: Run on hardware
results = run(qc_zne)

# BUG: Recorded depth/gates from Step 1, not Step 2!
```

**Check your code:**
```python
# In ibm_hardware_noise_experiment.py around line 300-310
# Where do you record circuit_depth and circuit_gates?
```

**If you record BEFORE ZNE folding:** This explains the anomaly! ✅

---

### Theory 2: ZNE Implementation Only Runs 1x Noise Factor ⚠️

**Hypothesis:** Your ZNE implementation may not be doing full folding

**Check your ZNE code:**
```python
def apply_zne(circuit, backend, noise_factors=[1, 2, 3], shots=8192):
    ...
    for factor in noise_factors:
        if factor == 1:
            scaled_circuit = circuit  # ← No folding for 1x
        else:
            # Gate folding here
```

**If ZNE only uses factor=1:** No folding happens, depth stays same!

**But then extrapolation should fail...** Let me check if fidelity patterns match this.

---

### Theory 3: Transpiler Optimizes Away Folded Gates ⚠️

**Hypothesis:** IBM transpiler may recognize gate-inverse pairs and cancel them

**Example:**
```
Original:     H - T - H
ZNE adds:     H - T - T† - T - H  (folded T gate)
Transpiler:   H - T - H  (recognizes T-T† = I, cancels it)
```

**If this happens:** ZNE folding is UNDONE by transpilation!

---

## 🔍 How to Verify the Root Cause

### Check 1: Where Are Circuit Depth/Gates Recorded?

**Look at your code around line 300-310 in ibm_hardware_noise_experiment.py:**

```python
# If you have something like:
qc_transpiled = transpile(qc_encrypted, backend, optimization_level=opt_level)
circuit_depth = qc_transpiled.depth()  # ← Recorded HERE

if apply_zne_flag:
    quasi_dist = apply_zne(qc_transpiled, backend)  # ← But ZNE happens AFTER
```

**This would record depth BEFORE ZNE!** ❌

**Fix:**
```python
qc_transpiled = transpile(qc_encrypted, backend, optimization_level=opt_level)

if apply_zne_flag:
    # Apply ZNE (which adds folding)
    quasi_dist = apply_zne(qc_transpiled, backend)
    # Record depth AFTER ZNE (but this is hard since ZNE runs 3 circuits...)
    circuit_depth = qc_transpiled.depth()  # This is still PRE-ZNE depth
```

**Problem:** ZNE runs 3 different circuits (1x, 2x, 3x noise), each with different depths!

**Solution:** Record the 2x or 3x depth, or note that ZNE runs multiple depths

---

### Check 2: Print Actual Circuit Depths During Execution

**Add debugging to your ZNE function:**

```python
def apply_zne(circuit, backend, noise_factors=[1, 2, 3], shots=8192):
    print(f"   Original circuit depth: {circuit.depth()}")

    for factor in noise_factors:
        if factor == 1:
            scaled_circuit = circuit
        else:
            scaled_circuit = circuit.copy()
            # Gate folding
            ...

        print(f"   Noise factor {factor}x: depth={scaled_circuit.depth()}, gates={scaled_circuit.size()}")

        # Execute
        ...
```

**Run this and check console output from your execution.**

---

### Check 3: Verify ZNE Actually Runs Multiple Jobs

**Look at your console output from the run:**

You showed this earlier:
```
   🔬 Applying ZNE with noise factors: [1, 2, 3]
      Executing at noise factor 1...
      Executing at noise factor 2...
      Executing at noise factor 3...
```

**This suggests ZNE DID run 3 jobs!** ✅

**But why doesn't depth increase?** → Because you recorded depth BEFORE ZNE folding!

---

## 📊 What the Table SHOULD Look Like (Corrected)

### 4q-3t (Corrected):
```
Config & Method      & Depth & Gates & Fidelity
4q-3t  & Baseline    & 16    & 164   & 0.030
4q-3t  & ZNE (1x)    & 16    & 164   & \multirow{3}{*}{0.034}
4q-3t  & ZNE (2x)    & 32    & 328   &
4q-3t  & ZNE (3x)    & 48    & 492   &
4q-3t  & Opt-3       & 21    & 166   & 0.031
4q-3t  & Opt-3+ZNE   & 42-63 & 332-498 & 0.034
```

**Note:** ZNE runs 3 circuits, so you need to clarify which depth you report!

---

### 5q-2t (Corrected):
```
Config & Method      & Depth & Gates & Fidelity
5q-2t  & Baseline    & 18    & 170   & 0.035
5q-2t  & ZNE (1x)    & 18    & 170   & \multirow{3}{*}{0.030}
5q-2t  & ZNE (2x)    & 36    & 340   &
5q-2t  & ZNE (3x)    & 54    & 510   &
5q-2t  & Opt-3       & 13    & 160   & 0.028
5q-2t  & Opt-3+ZNE   & 26-39 & 320-480 & 0.031
```

---

### 5q-3t (Corrected):
```
Config & Method      & Depth & Gates & Fidelity
5q-3t  & Baseline    & 19    & 175   & 0.012
5q-3t  & ZNE (1x)    & 19    & 175   & \multirow{3}{*}{0.014}
5q-3t  & ZNE (2x)    & 38    & 350   &
5q-3t  & ZNE (3x)    & 57    & 525   &
5q-3t  & Opt-3       & 15    & 167   & 0.011
5q-3t  & Opt-3+ZNE   & 30-45 & 334-501 & 0.010
```

---

## 🎯 Recommended Fix for Table

### Option 1: Remove Circuit Depth/Gates Columns for ZNE Methods

**Rationale:** ZNE runs 3 different circuits, so single depth/gates is misleading

**Updated Table:**
```latex
\begin{tabular}{lrlllll}
\toprule
Config & Aux-States & HW Method & HW Fidelity & HW TVD & Fidelity Drop \\
\midrule
4q-3t & 10776 & Baseline & 0.030155 & 0.884766 & 96.98\% \\
4q-3t & 10776 & ZNE\textsuperscript{*} & 0.034009 & 0.871669 & 96.60\% \\
4q-3t & 10776 & Opt-3 & 0.031381 & 0.888672 & 96.86\% \\
4q-3t & 10776 & Opt-3+ZNE\textsuperscript{*} & 0.034317 & 0.886905 & 96.57\% \\
...
\bottomrule
\end{tabular}

\textsuperscript{*} ZNE methods execute multiple circuit variants (1x, 2x, 3x noise scaling);
depth/gates vary across executions.
```

---

### Option 2: Report Depth Range for ZNE

**Updated Table:**
```latex
5q-2t & 575 & Baseline & 0.034607 & ... & 18 & 170 \\
5q-2t & 575 & ZNE & 0.029611 & ... & 18-54 & 170-510 \\
5q-2t & 575 & Opt-3 & 0.028423 & ... & 13 & 160 \\
5q-2t & 575 & Opt-3+ZNE & 0.031442 & ... & 13-39 & 160-480 \\
```

---

### Option 3: Report Only Non-ZNE Methods with Depth/Gates

**Keep Baseline and Opt-3 rows with depth/gates, omit for ZNE methods:**

```latex
\begin{tabular}{lrlllllll}
\toprule
Config & Aux-States & HW Method & HW Fidelity & HW TVD & Fidelity Drop & Depth & Gates \\
\midrule
5q-2t & 575 & Baseline & 0.034607 & 0.872070 & 96.54\% & 18 & 170 \\
5q-2t & 575 & ZNE & 0.029611 & 0.877976 & 97.04\% & -- & -- \\
5q-2t & 575 & Opt-3 & 0.028423 & 0.872070 & 97.16\% & 13 & 160 \\
5q-2t & 575 & Opt-3+ZNE & 0.031442 & 0.874128 & 96.86\% & -- & -- \\
\bottomrule
\end{tabular}
```

---

## 📝 Code Fix Needed

### In `ibm_hardware_noise_experiment.py`:

**Current (WRONG):**
```python
qc_transpiled = transpile(qc_encrypted, backend, optimization_level=opt_level)
# ... record depth here ...

if apply_zne_flag:
    quasi_dist = apply_zne(qc_transpiled, backend, shots=shots)
```

**Fixed:**
```python
qc_transpiled = transpile(qc_encrypted, backend, optimization_level=opt_level)

if apply_zne_flag:
    # Don't record depth/gates for ZNE (runs 3 different circuits)
    circuit_depth = None  # or "Variable (ZNE)"
    circuit_gates = None
    quasi_dist = apply_zne(qc_transpiled, backend, shots=shots)
else:
    # Only record for non-ZNE methods
    circuit_depth = qc_transpiled.depth()
    circuit_gates = qc_transpiled.size()
    # Execute normally
    ...
```

---

## ⚠️ Summary of Anomalies

| Config | Method | Issue | Severity |
|--------|--------|-------|----------|
| 4q-3t | ZNE | Depth same as Baseline (should increase) | ❌ WRONG |
| 4q-3t | Opt-3+ZNE | Depth < Opt-3 (impossible) | ❌❌❌ CRITICAL |
| 5q-2t | ZNE | Depth +1 only (should +18-36) | ❌ WRONG |
| 5q-2t | Opt-3+ZNE | Depth +9 only (should +13-26) | ⚠️ SUSPICIOUS |
| 5q-3t | ZNE | Depth +0 (should +19-38) | ❌ WRONG |
| 5q-3t | Opt-3+ZNE | Depth < Opt-3 (impossible) | ❌❌❌ CRITICAL |
| 4q-3t | Opt-3 | Depth > Baseline (+5) | ⚠️ UNEXPECTED |

---

## ✅ Recommendation

**For your paper submission:**

1. **Remove Circuit Depth/Gates columns for ZNE methods** (Option 1)
   - Add footnote explaining ZNE runs multiple circuits

2. **OR** Fix the code to record correct depths
   - But this requires re-running experiments

3. **Add clarification in paper text:**
   ```
   Note: Circuit depth and gate counts reported for Baseline and Opt-3
   represent the transpiled circuit executed on hardware. ZNE methods
   execute multiple circuit variants (1x, 2x, 3x noise scaling) with
   varying depths; only the extrapolated fidelity is reported.
   ```

---

**Your observation was CORRECT! The table has inconsistencies that need to be addressed before publication.**

---

**Generated:** 2025-10-24
**Status:** ⚠️ Table anomalies identified and analyzed
