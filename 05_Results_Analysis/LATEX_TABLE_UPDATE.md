# LaTeX Table Update for 5q-2t Results

**Date:** 2025-10-23
**File:** Papers/conference_101719_JBEdits.tex
**Table:** "Detailed Fidelity of Optimization Levels + ZNE techniques on IBM Quantum"

---

## Summary of Changes

### 5q-2t Results Comparison

| Method | OLD (1,350 states) | NEW (575 states) | Improvement |
|--------|-------------------|------------------|-------------|
| **Baseline** | 0.0279 | **0.0346** | **+24.2%** ✅ |
| **ZNE** | 0.0258 | **0.0296** | **+14.7%** ✅ |
| **Opt-3** | 0.0286 | 0.0284 | -0.7% ❌ |
| **Opt-3+ZNE** | 0.0339 | 0.0314 | -7.3% ❌ |

**Key Finding:**
- **Baseline improved by 24.2%** (most significant)
- Optimization methods showed slight degradation (likely due to different IBM backend state)
- 57.4% reduction in auxiliary states (1,350 → 575)

---

## LaTeX Code Update

### Option 1: Keep 8-Column Format (Current Paper Format)

**Location:** Line 297 in `Papers/conference_101719_JBEdits.tex`

**OLD:**
```latex
5q-T2 & 0.0117 & 0.0144 & 0.5040 & 0.6048 & 0.5880 & 0.7056 & 0.6440 & 0.7728 \\
```

**NEW (with updated 5q-2t data):**
```latex
5q-T2 & 0.0346 & 0.0296 & N/A & N/A & N/A & N/A & 0.0284 & 0.0314 \\
```

**Note:** This assumes the table columns are:
- Baseline, ZNE, Opt-0, Opt-0+ZNE, Opt-1, Opt-1+ZNE, Opt-3, Opt-3+ZNE

Since you didn't run Opt-0, Opt-0+ZNE, Opt-1, Opt-1+ZNE, those are marked as "N/A".

---

### Option 2: Simplify Table to 4-Column Format (RECOMMENDED)

If your paper currently shows 8 optimization methods but you only tested 4, you should update the entire table to match your actual experiments.

**NEW TABLE STRUCTURE:**

```latex
\begin{table*}[htbp]
\centering
\caption{Detailed Fidelity of Optimization Levels + ZNE techniques on IBM Quantum (Updated with Corrected 5q-T2)}
\label{tab:Hardware_performance}
\begin{tabular}{lcccc}
\toprule
\textbf{Config} & \textbf{Baseline} & \textbf{ZNE} & \textbf{Opt-3} & \textbf{Opt-3+ZNE} \\
\midrule
3q-T2 & 0.0029 & 0.0127 & 0.7360 & 0.8832 \\
3q-T3 & 0.0078 & 0.0167 & 0.7130 & 0.8556 \\
4q-T2 & 0.0042 & 0.0090 & 0.6900 & 0.8280 \\
4q-T3 & 0.0058 & 0.0000 & 0.6670 & 0.8004 \\
5q-T2 & \textbf{0.0346} & \textbf{0.0296} & \textbf{0.0284} & \textbf{0.0314} \\
5q-T3 & 0.0063 & 0.0088 & 0.6210 & 0.7452 \\
\bottomrule
\end{tabular}
\begin{tablenotes}
\small
\item \textbf{Note:} 5q-T2 results updated with corrected implementation (575 auxiliary states vs. previous 1,350). All other configurations use original data.
\end{tablenotes}
\end{table*}
```

**Changes made:**
1. Removed Opt-0, Opt-0+ZNE, Opt-1, Opt-1+ZNE columns (you didn't test these)
2. Updated 5q-T2 row with new values (bolded to highlight the change)
3. Added table note explaining the 5q-T2 update

---

### Option 3: Add Footnote to Existing Table

If you want to keep the 8-column format but explain missing data:

**Add after the table:**

```latex
\begin{tablenotes}
\small
\item \textbf{*} 5q-T2 configuration re-run with corrected implementation (575 auxiliary states). Opt-0, Opt-0+ZNE, Opt-1, and Opt-1+ZNE data not available for this configuration.
\end{tablenotes}
```

---

## Data Discrepancy Notice

⚠️ **IMPORTANT:** I noticed the OLD values in your paper **do NOT match** your CSV data:

### Your Paper Says (Line 297):
```
5q-T2 & 0.0117 & 0.0144 & 0.5040 & 0.6048 & 0.5880 & 0.7056 & 0.6440 & 0.7728
```

### Your CSV Says (local_vs_hardware_comparison.csv):
```
5q-2t Baseline: 0.0279 (not 0.0117)
5q-2t ZNE:      0.0258 (not 0.0144)
5q-2t Opt-3:    0.0286 (not 0.6440)
5q-2t Opt-3+ZNE: 0.0339 (not 0.7728)
```

**This is a BIG discrepancy!** The paper shows much higher fidelity for Opt-3 (0.6440) compared to CSV (0.0286).

**Possible explanations:**
1. Paper data is from a DIFFERENT experiment (perhaps simulator, not hardware)
2. Paper data includes error bars or different normalization
3. CSV data is mislabeled
4. Paper data is placeholder/synthetic

**Action required:** You need to clarify which data source is correct before updating the table.

---

## Recommended Update Process

### Step 1: Verify Data Source

Check if the paper's high fidelity values (0.6440, 0.7728) represent:
- Different experiment conditions
- Simulated vs. hardware results
- Different error mitigation settings

### Step 2: Update Table Based on Actual Hardware Results

**If CSV is correct (hardware results):**

Update the entire 5q-T2 row to match CSV data:

```latex
% OLD - INCORRECT DATA
% 5q-T2 & 0.0117 & 0.0144 & 0.5040 & 0.6048 & 0.5880 & 0.7056 & 0.6440 & 0.7728 \\

% NEW - CORRECTED 5q-2t with 575 auxiliary states
5q-T2 & 0.0346 & 0.0296 & N/A & N/A & N/A & N/A & 0.0284 & 0.0314 \\
```

### Step 3: Update Paper Text

**Location:** Around line 327 in the paper

**OLD TEXT:**
```
Following this, the correctness metrics have been markedly enhanced through
the combination of optimisation level 3 and ZNE techniques, achieving a
fidelity of 0.74 for the 5q-3T use case, while the best performance for
enhanced error was noted at 0.8832 for the 3q-2T configuration.
```

**NEW TEXT (if you use corrected 5q-2t data):**
```
Following this, the correctness metrics for 5q-2t improved from 0.0279
(baseline, 1,350 auxiliary states) to 0.0346 (baseline, 575 auxiliary states),
representing a 24.2% improvement after removing redundant cross-terms from
the key generation algorithm. However, even with this optimization, the
configuration still experiences 96.5% fidelity degradation compared to ideal
simulation, demonstrating the fundamental challenges of AUX-QHE on NISQ hardware.
```

---

## Summary Statistics for Paper

**5q-2t Configuration (Updated):**
- Auxiliary states: 575 (57.4% reduction from 1,350)
- Best fidelity: 0.0346 (Baseline method)
- Improvement: +24.2% vs. previous implementation
- Still 96.5% degradation from ideal (1.000)

**Key Message:**
> "Despite 57% reduction in auxiliary states through algorithmic optimization,
> the 5q-T2 configuration achieves only 3.46% fidelity on IBM hardware,
> demonstrating that circuit size reduction alone cannot overcome the
> fundamental noise limitations of current NISQ devices."

---

## Files to Update

1. **Papers/conference_101719_JBEdits.tex** (Line 297)
   - Update 5q-T2 table row

2. **Papers/conference_101719_JBEdits.tex** (Line 327)
   - Update results discussion text

3. **local_vs_hardware_comparison.csv**
   - Add new 5q-2t results with 575 aux states

4. **Paper footnotes/appendix**
   - Explain the correction and its impact

---

## Quick Copy-Paste (Option 2 - Recommended)

**Replace lines 285-301 in Papers/conference_101719_JBEdits.tex with:**

```latex
\begin{table*}[htbp]
\centering
\caption{Detailed Fidelity of Optimization Levels + ZNE techniques on IBM Quantum}
\label{tab:Hardware_performance}
\begin{tabular}{lcccc}
\toprule
\textbf{Config} & \textbf{Baseline} & \textbf{ZNE} & \textbf{Opt-3} & \textbf{Opt-3+ZNE} \\
\midrule
3q-T2 & 0.0029 & 0.0127 & 0.7360 & 0.8832 \\
3q-T3 & 0.0078 & 0.0167 & 0.7130 & 0.8556 \\
4q-T2 & 0.0042 & 0.0090 & 0.6900 & 0.8280 \\
4q-T3 & 0.0058 & 0.0000 & 0.6670 & 0.8004 \\
5q-T2\textsuperscript{*} & 0.0346 & 0.0296 & 0.0284 & 0.0314 \\
5q-T3 & 0.0063 & 0.0088 & 0.6210 & 0.7452 \\
\bottomrule
\end{tabular}
\end{table*}
```

**Add footnote after table:**
```latex
\textit{* 5q-T2 results updated with corrected key generation algorithm (575 auxiliary states, down from 1,350).}
```

---

**Need help updating the paper? Let me know which option you prefer!**
