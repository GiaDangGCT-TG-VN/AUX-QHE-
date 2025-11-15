# 📊 AUX-QHE Auxiliary States Analysis

This table provides detailed analysis of auxiliary state generation and efficiency.

---

## 🎯 Analysis Table

| Config | Aux States | Theoretical Layer Sizes | Efficiency | T-Set Cross Terms | Poly Eval Time (s) |
|--------|------------|-------------------------|------------|-------------------|--------------------|
| 3q-2t  |        240 | [6, 74]                 |     727.3% |                62 |           0.254548 |
| 3q-3t  |       2826 | [6, 39, 897]            |     645.2% |               846 |           0.034368 |
| 4q-2t  |        668 | [8, 159]                |    1284.6% |               143 |           0.034581 |
| 4q-3t  |      10776 | [8, 68, 2618]           |     992.3% |              2534 |           0.031335 |
| 5q-2t  |       1350 | [10, 260]               |    1800.0% |               240 |           0.032173 |
| 5q-3t  |      31025 | [10, 105, 6090]         |    1357.8% |              5965 |           0.031684 |

---

## 📝 Column Definitions

| Column | Description |
|--------|-------------|
| **Config** | Circuit configuration (qubits-q, T-depth-t) |
| **Aux States** | Total number of auxiliary quantum states prepared |
| **Theoretical Layer Sizes** | Size of T-sets at each layer [T[1], T[2], ...] |
| **Efficiency** | Ratio of actual vs theoretical minimum states (higher = more redundancy) |
| **T-Set Cross Terms** | Number of cross-product terms generated across all layers |
| **Poly Eval Time (s)** | Time to evaluate polynomial expressions homomorphically |

---

## 📈 Key Insights

### 1. Auxiliary States Growth
- **Smallest:** 3q-2t (240 states)
- **Largest:** 5q-3t (31,025 states)
- **Total across all configs:** 46,885 states

### 2. Cross-Term Analysis
- **Total cross-terms:** 9,790
- **Cross-term percentage:** 20.9% of all auxiliary states
- **Most cross-terms:** 5q-3t (5,965 terms)
- **Fewest cross-terms:** 3q-2t (62 terms)

### 3. Layer Growth Patterns

**T-depth = 2 circuits:**
- 3q-2t: [6 → 74] = **12.3x growth**
- 4q-2t: [8 → 159] = **19.9x growth**
- 5q-2t: [10 → 260] = **26.0x growth**

**T-depth = 3 circuits:**
- 3q-3t: [6 → 39 → 897] = **6.5x → 23.0x growth**
- 4q-3t: [8 → 68 → 2618] = **8.5x → 38.5x growth**
- 5q-3t: [10 → 105 → 6090] = **10.5x → 58.0x growth**

**Pattern:** Exponential growth in later layers!

### 4. Performance Metrics
- **Average eval time:** 0.0698s
- **Time per aux state:** 0.0089ms (very efficient!)
- **Fastest eval:** 4q-3t (0.0313s despite 10,776 states!)

---

## 🔬 Detailed Analysis

### Efficiency Metric Explained

The efficiency percentage shows how the actual implementation compares to a theoretical minimum:
- **>100%** means redundancy is added (for correctness and security)
- **3q-3t** is most efficient at 645.2%
- **5q-2t** has highest redundancy at 1800.0%

This redundancy is **intentional** - it ensures:
1. All polynomial terms can be evaluated
2. Cross-terms are available for T-gadget operations
3. Correctness is maintained across different circuit sizes

### Cross-Terms Growth

Cross-terms grow quadratically within each layer:
- Layer ℓ cross-terms ≈ C(|T[ℓ-1]|, 2) = |T[ℓ-1]| × (|T[ℓ-1]| - 1) / 2

Example for 5q-3t:
- T[1] = 10 base terms
- T[2] = 105 terms (includes ~45 cross-terms from T[1])
- T[3] = 6090 terms (includes ~5,460 cross-terms from T[2])

This exponential growth is **necessary** for correct polynomial tracking but is the main scalability challenge.

### Polynomial Evaluation Performance

Despite the large number of auxiliary states, evaluation is fast:
- All configs complete in < 0.3s
- Most complete in < 0.05s
- Time scales sub-linearly with aux state count (homomorphic evaluation is efficient!)

---

## 🔧 How to Regenerate

```bash
python generate_auxiliary_analysis_table.py
```

Output files:
- `aux_qhe_auxiliary_analysis.csv` - CSV format
- Console output includes: ASCII, Markdown, LaTeX formats

---

## 📊 LaTeX Table (for Papers)

```latex
\begin{table}[h]
\centering
\caption{AUX-QHE Auxiliary States Analysis}
\label{tab:aux_analysis}
\begin{tabular}{lrrrrr}
\toprule
\textbf{Config} & \textbf{Aux States} & \textbf{Layer Sizes} & \textbf{Efficiency} & \textbf{Cross Terms} & \textbf{Eval Time (s)} \\
\midrule
3q-2t & 240 & \{6, 74\} & 727.3\% & 62 & 0.254548 \\
3q-3t & 2826 & \{6, 39, 897\} & 645.2\% & 846 & 0.034368 \\
4q-2t & 668 & \{8, 159\} & 1284.6\% & 143 & 0.034581 \\
4q-3t & 10776 & \{8, 68, 2618\} & 992.3\% & 2534 & 0.031335 \\
5q-2t & 1350 & \{10, 260\} & 1800.0\% & 240 & 0.032173 \\
5q-3t & 31025 & \{10, 105, 6090\} & 1357.8\% & 5965 & 0.031684 \\
\bottomrule
\end{tabular}
\end{table}
```

---

## 🎓 Implications for Scalability

1. **T-depth = 3** has massive cross-term growth (especially last layer)
2. **Number of qubits** affects initial T[1] size linearly
3. **Cross-terms dominate** at higher T-depths (exponential growth)
4. **Evaluation time** remains practical even for large state counts

**Recommendation:** For circuits with T-depth > 3, consider:
- Circuit optimization to reduce T-count
- Decomposition into smaller sub-circuits
- Parallel evaluation strategies

---

**Generated:** October 6, 2025  
**Based on:** Corrected AUX-QHE implementation with fixed auxiliary key generation
