# 📊 AUX-QHE Results Tables

This document shows the generated tables from your AUX-QHE performance benchmarks.

---

## 🎯 Compact Results Table

**File:** `aux_qhe_compact_results.csv`

| Config | Fidelity | TVD | QASM | Aux Qubits | Aux Prep Time(s) | T-Gadget Time(s) | Decrypt Eval Time(s) | Total Run Time(s) |
|--------|----------|-----|---------|------------|------------------|------------------|----------------------|-------------------|
| 3q-2t  |   1.0000 | 0.0000 | Both 2&3 |        240 |         0.003271 |         0.000308 |             0.254548 |          0.258128 |
| 3q-3t  |   1.0000 | 0.0000 | Both 2&3 |       2826 |         0.038700 |         0.003553 |             0.034368 |          0.076621 |
| 4q-2t  |   1.0000 | 0.0000 | Both 2&3 |        668 |         0.009254 |         0.000847 |             0.034581 |          0.044682 |
| 4q-3t  |   1.0000 | 0.0000 | Both 2&3 |      10776 |         0.203022 |         0.012408 |             0.031335 |          0.246766 |
| 5q-2t  |   1.0000 | 0.0000 | Both 2&3 |       1350 |         0.018683 |         0.001700 |             0.032173 |          0.052556 |
| 5q-3t  |   1.0000 | 0.0000 | Both 2&3 |      31025 |         0.679310 |         0.036046 |             0.031684 |          0.747041 |

---

## 📈 Key Insights

- ✅ **Total Configurations:** 6
- ✅ **All Tests Passed:** 100% success rate
- ✅ **Average Fidelity:** 1.000000 (perfect!)
- ✅ **Perfect Fidelity Count:** 6/6

### Performance Insights:
- ⚡ **Fastest config:** 4q-2t (0.044682s)
- 🐌 **Slowest config:** 5q-3t (0.747041s)
- 📊 **Most aux qubits:** 5q-3t (31,025 qubits)

---

## 📝 Column Definitions

| Column | Description |
|--------|-------------|
| **Config** | Circuit configuration (qubits-q, T-depth-t) |
| **Fidelity** | State fidelity (1.0 = perfect match) |
| **TVD** | Total Variation Distance (0.0 = perfect) |
| **QASM** | OpenQASM version tested (Both 2&3 means identical results) |
| **Aux Qubits** | Number of auxiliary qubits/states prepared |
| **Aux Prep Time(s)** | Time to prepare auxiliary states |
| **T-Gadget Time(s)** | Time for T-gadget operations |
| **Decrypt Eval Time(s)** | Combined decryption and evaluation time |
| **Total Run Time(s)** | Total execution time (sum of all times) |

---

## 🔧 How to Generate Tables

### 1. Run the benchmark first:
```bash
python algorithm/openqasm_performance_comparison.py
```

### 2. Generate compact table:
```bash
python generate_compact_table.py
```

### 3. Generate full table (with QASM 2 & 3 separate):
```bash
python generate_results_table.py
```

---

## 📄 Available Output Formats

The scripts generate tables in multiple formats:

### CSV Files:
- `aux_qhe_compact_results.csv` - One row per config
- `aux_qhe_results_table.csv` - Separate rows for QASM 2 & 3
- `corrected_openqasm_performance_comparison.csv` - Raw benchmark data

### Formatted Outputs:
- **ASCII Table** - For terminal/documentation
- **Markdown Table** - For README files
- **LaTeX Table** - For academic papers

---

## 📊 LaTeX Table (for Papers)

```latex
\begin{table}[h]
\centering
\caption{AUX-QHE Performance Results}
\label{tab:aux_qhe_results}
\begin{tabular}{lcccrrrr}
\toprule
\textbf{Config} & \textbf{Fidelity} & \textbf{TVD} & \textbf{QASM} & \textbf{Aux Qubits} & \textbf{Prep (s)} & \textbf{T-Gadget (s)} & \textbf{Total (s)} \\
\midrule
3q-2t & 1.0000 & 0.0000 & Both 2\&3 & 240 & 0.003271 & 0.000308 & 0.258128 \\
3q-3t & 1.0000 & 0.0000 & Both 2\&3 & 2826 & 0.038700 & 0.003553 & 0.076621 \\
4q-2t & 1.0000 & 0.0000 & Both 2\&3 & 668 & 0.009254 & 0.000847 & 0.044682 \\
4q-3t & 1.0000 & 0.0000 & Both 2\&3 & 10776 & 0.203022 & 0.012408 & 0.246766 \\
5q-2t & 1.0000 & 0.0000 & Both 2\&3 & 1350 & 0.018683 & 0.001700 & 0.052556 \\
5q-3t & 1.0000 & 0.0000 & Both 2\&3 & 31025 & 0.679310 & 0.036046 & 0.747041 \\
\bottomrule
\end{tabular}
\end{table}
```

---

## 🎓 Notes

1. **Fidelity = 1.0000** means perfect correctness ✅
2. **TVD = 0.0000** confirms perfect state preservation ✅
3. **QASM 2 & 3** produce identical results (as expected)
4. **Auxiliary qubits** grow exponentially with T-depth
5. **Total time** dominated by auxiliary preparation for high T-depth circuits

---

**Generated:** October 5, 2025  
**Fix Applied:** Auxiliary k-value generation (circuit-size independence)
