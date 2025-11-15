# 📊 IBM Quantum Hardware Noise Experiment - Configuration Summary

**Updated:** October 6, 2025

---

## 🎯 Experiment Overview

### QASM Version
- **OpenQASM 3.0** - All circuits exported in QASM 3 format

### Configurations Tested
**6 total configurations:**

| Config | Qubits | T-depth | Description |
|--------|--------|---------|-------------|
| **3q-2t** | 3 | 2 | Small circuit, T-depth 2 |
| **4q-2t** | 4 | 2 | Medium circuit, T-depth 2 |
| **5q-2t** | 5 | 2 | Large circuit, T-depth 2 |
| **3q-3t** | 3 | 3 | Small circuit, T-depth 3 |
| **4q-3t** | 4 | 3 | Medium circuit, T-depth 3 |
| **5q-3t** | 5 | 3 | Large circuit, T-depth 3 |

**Total circuits:** 3q, 4q, 5q for both T-depth=2 and T-depth=3

---

## 🔬 Error Mitigation Methods

**6 methods per configuration:**

| # | Method | Optimization Level | ZNE Applied | Purpose |
|---|--------|-------------------|-------------|---------|
| 1 | **Baseline** | 1 (default) | ❌ No | Raw hardware performance |
| 2 | **ZNE** | 1 (default) | ✅ Yes | Error mitigation via noise extrapolation |
| 3 | **Opt-0** | 0 (minimal) | ❌ No | Minimal transpilation |
| 4 | **Opt-3** | 3 (heavy) | ❌ No | Circuit depth/gate optimization |
| 5 | **Opt-0+ZNE** | 0 (minimal) | ✅ Yes | Minimal optimization + error mitigation |
| 6 | **Opt-3+ZNE** | 3 (heavy) | ✅ Yes | **Best fidelity** (full optimization + mitigation) |

**Total experiment runs:** 6 configs × 6 methods = **36 runs**

---

## 📁 Output Files Generated

### 1. Results Data
- **CSV**: `ibm_noise_measurement_results_TIMESTAMP.csv`
- **JSON**: `ibm_noise_measurement_results_TIMESTAMP.json`
- **Interim**: `ibm_noise_results_interim_TIMESTAMP.json` (auto-saved)

### 2. QASM 3.0 Exports
**36 QASM files** in `qasm3_exports/` directory:

```
qasm3_exports/
├── 3q-2t_Baseline.qasm
├── 3q-2t_ZNE.qasm
├── 3q-2t_Opt-0.qasm
├── 3q-2t_Opt-3.qasm
├── 3q-2t_Opt-0_ZNE.qasm
├── 3q-2t_Opt-3_ZNE.qasm
├── 4q-2t_Baseline.qasm
├── 4q-2t_ZNE.qasm
... (30 more files)
├── 5q-3t_Opt-3_ZNE.qasm
```

### 3. Analysis Outputs
- **Visualization**: `ibm_noise_measurement_analysis.png`
- **Console output**: Detailed analysis tables and statistics

---

## 📊 Data Collected Per Run

| Metric | Description |
|--------|-------------|
| **Config** | Configuration name (e.g., 3q-2t) |
| **Method** | Error mitigation method |
| **QASM Version** | OpenQASM 3.0 |
| **Backend** | IBM backend name |
| **Num Qubits** | Number of qubits |
| **T-depth** | T-gate depth |
| **Aux States** | Number of auxiliary states prepared |
| **Optimization Level** | Transpiler optimization level (0, 1, 3) |
| **ZNE Applied** | Whether ZNE was used |
| **Shots** | Measurement shots (default: 8192) |
| **QASM3 File** | Path to exported QASM 3 file |
| **Fidelity** | Quantum state fidelity (1.0 = perfect) |
| **TVD** | Total Variation Distance (0.0 = perfect) |
| **Keygen Time** | AUX-QHE key generation time |
| **Encrypt Time** | QOTP encryption time |
| **Transpile Time** | Circuit compilation time |
| **Exec Time** | IBM hardware execution time |
| **Eval Time** | Homomorphic evaluation time |
| **Decrypt Time** | QOTP decryption time |
| **Total Time** | End-to-end runtime |
| **Circuit Depth** | Transpiled circuit depth |
| **Circuit Gates** | Total gate count |

---

## 🎯 Experiment Matrix

### Full Experiment Matrix (6 configs × 6 methods = 36 runs)

| Config | Baseline | ZNE | Opt-0 | Opt-3 | Opt-0+ZNE | Opt-3+ZNE |
|--------|----------|-----|-------|-------|-----------|-----------|
| **3q-2t** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **4q-2t** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **5q-2t** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **3q-3t** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **4q-3t** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **5q-3t** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## ⏱️ Expected Timeline

### Per-Run Estimates:
- **Baseline**: ~12-18s
- **ZNE**: ~27-35s (requires multiple noise levels)
- **Opt-0**: ~11-16s
- **Opt-3**: ~17-23s
- **Opt-0+ZNE**: ~28-40s
- **Opt-3+ZNE**: ~35-50s

### Total Experiment:
- **Minimum**: ~18 minutes (ideal conditions)
- **Average**: ~25 minutes (typical queue)
- **Maximum**: ~45 minutes (busy queue)

**Note:** Highly variable due to IBM queue times!

---

## 🔬 ZNE (Zero-Noise Extrapolation) Details

### How ZNE Works:
1. **Noise Scaling**: Execute circuit at noise factors [1, 2, 3]
   - Factor 1: Baseline (original circuit)
   - Factor 2: 2× noise (gate folding: G → G·G†·G)
   - Factor 3: 3× noise

2. **Measurement**: Get probability distributions at each noise level

3. **Extrapolation**: Richardson extrapolation to zero noise
   - Linear: `p(0) ≈ 2·p(1) - p(2)`
   - Estimates ideal zero-noise result

4. **Overhead**: ~15-25 seconds (requires 3 executions)

---

## 📈 Analysis Comparisons

The analysis script generates:

### 1. Fidelity Comparison
- Pivot table: Config × Method
- Improvement over baseline
- Best method per configuration

### 2. TVD Analysis
- Total Variation Distance comparison
- Reduction from baseline
- Lower = better

### 3. Runtime Analysis
- Total time per method
- Overhead vs baseline
- Detailed breakdown (keygen, transpile, exec, etc.)

### 4. Efficiency Metrics
- Fidelity/Time ratio
- Most efficient method per config

### 5. Overall Rankings
- Composite scores (50% fidelity, 30% TVD, 20% time)
- Method rankings
- Recommendations

### 6. Visualizations
- 6-panel comparison plot
- Fidelity heatmaps
- Runtime comparisons
- Efficiency scatter plots

---

## 🎯 Key Research Questions Answered

1. **How does ZNE affect fidelity on real hardware?**
   - Compare Baseline vs ZNE, Opt-3 vs Opt-3+ZNE

2. **What's the impact of optimization level?**
   - Compare Opt-0 vs Opt-3

3. **What's the best method for production?**
   - Likely Opt-3+ZNE (highest fidelity)

4. **What's the performance/time tradeoff?**
   - Efficiency metric: Fidelity/Time

5. **How does circuit size affect noise?**
   - Compare 3q, 4q, 5q results

6. **How does T-depth affect noise?**
   - Compare T-depth=2 vs T-depth=3

---

## 🚀 Quick Start Commands

### Run Full Experiment
```bash
python ibm_hardware_noise_experiment.py
```

### Run Specific Config
```bash
python ibm_hardware_noise_experiment.py --config 3q-2t
```

### Custom Backend and Shots
```bash
python ibm_hardware_noise_experiment.py --backend ibm_kyoto --shots 8192
```

### Analyze Results
```bash
python analyze_ibm_noise_results.py
```

---

## 📝 Example Output Structure

### CSV Format
```csv
config,method,qasm_version,backend,num_qubits,t_depth,aux_states,optimization_level,zne_applied,shots,qasm3_file,fidelity,tvd,keygen_time,encrypt_time,transpile_time,exec_time,eval_time,decrypt_time,total_time,circuit_depth,circuit_gates
3q-2t,Baseline,OpenQASM 3.0,ibm_brisbane,3,2,240,1,False,8192,qasm3_exports/3q-2t_Baseline.qasm,0.7845,0.1234,0.003,0.002,1.2,10.5,0.25,0.001,12.1,45,156
3q-2t,ZNE,OpenQASM 3.0,ibm_brisbane,3,2,240,1,True,8192,qasm3_exports/3q-2t_ZNE.qasm,0.8912,0.0856,0.003,0.002,1.2,28.3,0.25,0.001,29.8,45,156
...
```

### QASM 3.0 Export Example
```qasm
OPENQASM 3.0;
include "stdgates.inc";

qubit[3] q;
bit[3] c;

h q[0];
h q[1];
h q[2];
t q[0];
t q[1];
t q[2];
cx q[0], q[1];
cx q[1], q[2];
...
measure q -> c;
```

---

## 💡 Best Practices

1. **Start small**: Test with single config first (`--config 3q-2t`)
2. **Check queue**: Run during off-peak hours for faster results
3. **Monitor progress**: Watch interim JSON files
4. **Backup results**: Results auto-saved after each run
5. **Analyze incrementally**: Can analyze partial results while experiment continues

---

## 🏆 Expected Best Performers

### By Fidelity (Best → Worst):
1. **Opt-3+ZNE** (~90-98%)
2. **Opt-0+ZNE** (~85-95%)
3. **ZNE** (~80-92%)
4. **Opt-3** (~75-88%)
5. **Opt-0** (~70-85%)
6. **Baseline** (~65-80%)

### By Speed (Fastest → Slowest):
1. **Opt-0** (~11-16s)
2. **Baseline** (~12-18s)
3. **Opt-3** (~17-23s)
4. **ZNE** (~27-35s)
5. **Opt-0+ZNE** (~28-40s)
6. **Opt-3+ZNE** (~35-50s)

### By Efficiency (Fidelity/Time):
1. **Baseline** or **Opt-3** (depends on fidelity gain)
2. **ZNE**
3. **Opt-3+ZNE**

---

## 📚 References

- **AUX-QHE Algorithm**: See `AUX_QHE_PSEUDOCODE.md`
- **Testing Guide**: See `TESTING_GUIDE.md`
- **Experiment Guide**: See `IBM_HARDWARE_EXPERIMENT_GUIDE.md`
- **Performance Analysis**: See `AUXILIARY_ANALYSIS_TABLE.md`

---

**Ready to measure AUX-QHE noise characteristics on IBM Quantum hardware!** 🚀
