# Hardware Noise Experiment Results

**Generated:** 2025-10-30
**Backend:** IBM Quantum (ibm_torino, 133 qubits)
**Shots:** 1024 per method
**Configurations:** 5q-2t, 4q-3t, 5q-3t (most recent executions)

## LaTeX Table

```latex
\begin{table*}[htbp]
\centering
\caption{Detailed Fidelity of Optimisation Levels + ZNE techniques on IBM Quantum}
\label{tab:Hardware_performance}
\begin{tabular}{lrllllllll}
\toprule
Config & Aux States & HW Method & HW Fidelity & HW TVD & Fidelity Drop \\
\midrule
5q-2t & 575 & Baseline & 0.3569 & 0.2861 & 64.31\% \\
5q-2t & 575 & ZNE & 0.3296 & 0.3409 & 67.04\% \\
5q-2t & 575 & Opt-3 & 0.3618 & 0.2764 & 63.82\% \\
5q-2t & 575 & Opt-3+ZNE & 0.3782 & 0.2435 & 62.18\% \\
4q-3t & 10776 & Baseline & 0.1222 & 0.1689 & 87.78\% \\
4q-3t & 10776 & ZNE & 0.1162 & 0.2086 & 88.38\% \\
4q-3t & 10776 & Opt-3 & 0.1165 & 0.2061 & 88.35\% \\
4q-3t & 10776 & Opt-3+ZNE & 0.1145 & 0.2257 & 88.55\% \\
5q-3t & 31025 & Baseline & 0.1199 & 0.2100 & 88.01\% \\
5q-3t & 31025 & ZNE & 0.1175 & 0.2155 & 88.25\% \\
5q-3t & 31025 & Opt-3 & 0.1293 & 0.1201 & 87.07\% \\
5q-3t & 31025 & Opt-3+ZNE & 0.1305 & 0.1114 & 86.95\% \\
\bottomrule
\end{tabular}
\end{table*}
```

**Table Format:**
- ✅ Uses `\begin{table*}[htbp]` (two-column table)
- ✅ Uses `\toprule`, `\midrule`, `\bottomrule` (booktabs style)
- ✅ Uses `lrllllllll` column alignment (no borders)
- ✅ Repeats config and aux states on each row (no multirow)
- ✅ Fidelity as decimals (0.3569 not 35.69%)
- ✅ Correct aux states: 575, 10776, 31025
- ✅ Caption matches your style

**Note:** Requires `\usepackage{booktabs}` in LaTeX preamble

---

## Key Findings

### 1. **5q-2t Configuration** (575 aux states)
- **Best Overall Performance**: 35.69% - 37.82% fidelity
- **Best Method**: Opt-3+ZNE (37.82% fidelity, 0.244 TVD)
- **Fidelity Drop**: 62.18% - 67.04%
- **Observation**: Lower T-depth (L=2) enables significantly better fidelity

### 2. **4q-3t Configuration** (10,776 aux states)
- **Moderate Performance**: 11.45% - 12.22% fidelity
- **Best Method**: Baseline (12.22% fidelity, 0.169 TVD)
- **Fidelity Drop**: 87.78% - 88.55%
- **Observation**: T-depth=3 increases auxiliary state overhead and noise accumulation

### 3. **5q-3t Configuration** (31,025 aux states)
- **Similar to 4q-3t**: 11.75% - 13.05% fidelity
- **Best Method**: Opt-3+ZNE (13.05% fidelity, 0.111 TVD - lowest TVD!)
- **Fidelity Drop**: 86.95% - 88.25%
- **Observation**: Higher qubit count + T-depth=3 challenges NISQ hardware limits

---

## Summary Statistics

| Config | Avg Fidelity | Avg TVD | Aux States |
|--------|--------------|---------|------------|
| 5q-2t  | 35.66%       | 0.287   | 575        |
| 4q-3t  | 11.74%       | 0.202   | 10,776     |
| 5q-3t  | 12.43%       | 0.164   | 31,025     |

---

## Analysis

### T-Depth Impact
- **T-depth=2 (5q-2t)**: ~36% average fidelity → **3x better** than T-depth=3
- **T-depth=3 (4q-3t, 5q-3t)**: ~12% average fidelity → Significant noise accumulation

### Error Mitigation Effectiveness
- **5q-2t**: Opt-3+ZNE provides best results (37.82%)
- **4q-3t**: Surprisingly, Baseline outperforms others (12.22%)
- **5q-3t**: Opt-3+ZNE achieves best fidelity (13.05%) and lowest TVD (0.111)

### Auxiliary State Overhead
- Exponential growth with T-depth: 575 → 10,776 → 31,025
- More auxiliary states correlate with higher noise and lower fidelity
- Demonstrates NISQ hardware limits for T-depth ≥ 3

---

## Hardware Conditions

**Backend:** ibm_torino (133 qubits)
**Execution Dates:**
- 5q-2t: 2025-10-30 23:13:19
- 4q-3t: 2025-10-30 23:06:42
- 5q-3t: 2025-10-30 22:45:47

**Note:** Hardware quality varies by execution time due to:
- Thermal drift
- Queue length (affects calibration freshness)
- Individual qubit error rates (e.g., qubit 0 had 13.23% readout error in previous runs)

---

## Verification Against Paper Description

✅ **Matches Paper Requirements:**
- Qubit count: 4-5 qubits (all three configs match)
- T-depth: L = 2, 3 (all configs match)
- Circuit structure: Includes H (Clifford), CNOT (entanglement), T gates
- T-depth definition: Sequential T-gate layers (correct interpretation)

✅ **Decryption Verified:** Local simulation achieved TVD=0.000000, confirming QOTP decryption correctness

---

## Source Files

**Result Files:**
- 5q-2t: `ibm_noise_measurement_results_20251030_231319.json`
- 4q-3t: `ibm_noise_measurement_results_20251030_230642.json`
- 5q-3t: `ibm_noise_measurement_results_20251030_224547.json`

**Generation Script:** `generate_hardware_table.py`
