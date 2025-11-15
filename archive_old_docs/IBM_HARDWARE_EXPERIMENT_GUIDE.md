# 🚀 AUX-QHE on IBM Quantum Hardware - Experiment Guide

Complete guide for running AUX-QHE noise measurement experiments on IBM Quantum hardware.

---

## 📋 Overview

This experiment measures AUX-QHE performance on real IBM quantum hardware using **5 different error mitigation strategies**:

1. **Baseline** - No error mitigation (raw hardware results)
2. **ZNE** - Zero-Noise Extrapolation error mitigation
3. **Opt-0** - Optimization level 0 (minimal transpilation)
4. **Opt-3** - Optimization level 3 (heavy optimization)
5. **Opt-0+ZNE** - Minimal optimization + ZNE
6. **Opt-3+ZNE** - Heavy optimization + ZNE (best fidelity)

**Configurations tested:** 3q, 4q, 5q for T-depth 2 and 3 (6 total configurations)
**QASM Version:** OpenQASM 3.0 (all circuits exported to QASM 3 format)

---

## 🔧 Setup

### 1. IBM Quantum Account

First, ensure your IBM Quantum account is saved:

```python
from qiskit_ibm_runtime import QiskitRuntimeService

# Save account (only need to do once)
QiskitRuntimeService.save_account(
    channel='ibm_quantum',
    token='YOUR_IBM_QUANTUM_TOKEN'
)
```

**Your account is already saved in:** `~/.qiskit/qiskit-ibm.json`

### 2. Required Packages

```bash
pip install qiskit qiskit-ibm-runtime pandas numpy matplotlib seaborn
```

---

## 🎯 Running Experiments

### Basic Usage

Run full experiment (all 6 configs, all 5 methods):

```bash
python ibm_hardware_noise_experiment.py
```

### Custom Backend

Specify IBM backend (default: `ibm_brisbane`):

```bash
python ibm_hardware_noise_experiment.py --backend ibm_kyoto
```

### Single Configuration

Test a single configuration:

```bash
python ibm_hardware_noise_experiment.py --config 3q-2t
```

### Custom Shots

Set number of measurement shots (default: 8192):

```bash
python ibm_hardware_noise_experiment.py --shots 4096
```

### Combined Example

```bash
python ibm_hardware_noise_experiment.py --backend ibm_brisbane --config 5q-3t --shots 8192
```

---

## 📊 Analyzing Results

After experiments complete, analyze results:

```bash
python analyze_ibm_noise_results.py
```

This generates:
- **Fidelity comparison** across all methods
- **TVD (Total Variation Distance)** analysis
- **Runtime analysis** and overhead breakdown
- **Efficiency metrics** (fidelity/time)
- **Method rankings** and recommendations
- **Visualization plots** (`ibm_noise_measurement_analysis.png`)

---

## 📈 Output Files

The experiment generates:

1. **Results CSV**: `ibm_noise_measurement_results_YYYYMMDD_HHMMSS.csv`
   - All experimental data in tabular format
   - Columns: config, method, qasm_version, fidelity, tvd, runtime, etc.

2. **Results JSON**: `ibm_noise_measurement_results_YYYYMMDD_HHMMSS.json`
   - Complete results including measurement counts
   - Detailed metadata for each run

3. **Interim Results**: `ibm_noise_results_interim_YYYYMMDD_HHMMSS.json`
   - Saved after each experiment (in case of interruption)

4. **Analysis Plots**: `ibm_noise_measurement_analysis.png`
   - 6-panel visualization with all comparisons

5. **QASM 3.0 Exports**: `qasm3_exports/*.qasm`
   - Transpiled circuits in OpenQASM 3.0 format
   - One file per configuration + method combination
   - Example: `3q-2t_Baseline.qasm`, `5q-3t_Opt-3_ZNE.qasm`

---

## 🔬 What Gets Measured

### For Each Configuration + Method Combination:

| Metric | Description |
|--------|-------------|
| **Fidelity** | Quantum state similarity to ideal (1.0 = perfect) |
| **TVD** | Total Variation Distance (0.0 = perfect) |
| **Keygen Time** | AUX-QHE key generation time |
| **Encrypt Time** | QOTP encryption time |
| **Transpile Time** | Circuit compilation time |
| **Exec Time** | IBM hardware execution time (includes queue) |
| **Eval Time** | Homomorphic evaluation time |
| **Decrypt Time** | QOTP decryption time |
| **Total Time** | End-to-end runtime |
| **Circuit Depth** | Transpiled circuit depth |
| **Circuit Gates** | Total gate count |

---

## 🧪 Error Mitigation Methods Explained

### 1. Baseline
- **What it does**: No error mitigation
- **Optimization**: Level 1 (default)
- **When to use**: Quick testing, baseline comparison
- **Pros**: Fastest execution
- **Cons**: Lowest fidelity (hardware noise not mitigated)

### 2. ZNE (Zero-Noise Extrapolation)
- **What it does**: Executes circuit at multiple noise levels, extrapolates to zero noise
- **How it works**:
  1. Run circuit at noise factors [1, 2, 3]
  2. Scale noise using gate folding (insert U†U operations)
  3. Perform Richardson extrapolation to estimate zero-noise result
- **Optimization**: Level 1
- **When to use**: Error mitigation critical, moderate runtime acceptable
- **Pros**: Significant fidelity improvement
- **Cons**: ~15-25s overhead (requires multiple executions)

### 3. Opt-0 (Optimization Level 0)
- **What it does**: Minimal transpilation
- **Optimization**: Level 0
- **When to use**: Preserve circuit structure, minimal changes
- **Pros**: Fast transpilation, preserves original gates
- **Cons**: Longer circuit depth, more gates

### 4. Opt-3 (Optimization Level 3)
- **What it does**: Heavy optimization (gate reduction, depth optimization)
- **Optimization**: Level 3
- **When to use**: Reduce circuit complexity, improve gate fidelity
- **Pros**: Shorter depth, fewer gates, better hardware fidelity
- **Cons**: ~5s transpilation overhead

### 5. Opt-0+ZNE
- **What it does**: Minimal optimization + ZNE error mitigation
- **When to use**: Preserve structure + error mitigation
- **Pros**: Error mitigation with minimal changes
- **Cons**: Longer circuits + ZNE overhead

### 6. Opt-3+ZNE
- **What it does**: Heavy optimization + ZNE error mitigation
- **When to use**: **Production, best fidelity**
- **Pros**: **Best overall fidelity** (optimized circuit + error mitigation)
- **Cons**: Longest runtime (~35-55s total)

---

## 📊 Expected Results

### Fidelity Ranking (Best → Worst)
1. **Opt-3+ZNE** - Best fidelity (~90-98%)
2. **Opt-0+ZNE** - Good fidelity (~85-95%)
3. **ZNE** - Moderate-good fidelity (~80-92%)
4. **Opt-3** - Moderate fidelity (~75-88%)
5. **Opt-0** - Low-moderate fidelity (~70-85%)
6. **Baseline** - Lowest fidelity (~65-80%)

### Runtime Ranking (Fastest → Slowest)
1. **Opt-0** - Fastest (~10-15s)
2. **Baseline** - Very fast (~12-18s)
3. **Opt-3** - Fast (~15-23s)
4. **ZNE** - Moderate (~25-35s)
5. **Opt-0+ZNE** - Slow (~28-40s)
6. **Opt-3+ZNE** - Slowest (~35-55s)

### Efficiency (Fidelity/Time)
1. **Opt-3** or **Baseline** - Best efficiency
2. **ZNE** - Good efficiency
3. **Opt-3+ZNE** - Moderate efficiency (but best absolute fidelity)

---

## 💡 Recommendations

### For Different Use Cases:

| Use Case | Recommended Method | Why |
|----------|-------------------|-----|
| **Production** | Opt-3+ZNE | Best fidelity, both optimization and error mitigation |
| **Research** | Run all methods | Compare tradeoffs, understand noise characteristics |
| **Quick Testing** | Baseline or Opt-0 | Fast results for validation |
| **Balanced** | ZNE or Opt-3 | Good fidelity/time ratio |
| **Maximum Accuracy** | Opt-3+ZNE | Best possible fidelity |
| **Minimum Time** | Opt-0 or Baseline | Fastest execution |

### General Strategy:

1. **Start with Baseline/Opt-0** - Quick validation, sanity check
2. **Run ZNE** - Understand error mitigation impact
3. **Compare Opt-0 vs Opt-3** - Understand optimization impact
4. **Use Opt-3+ZNE for final results** - Best fidelity for publication/production

---

## 🔍 Understanding the Results

### Fidelity Interpretation:
- **Fidelity ≥ 0.95**: Excellent (very close to ideal)
- **Fidelity 0.85-0.95**: Good (acceptable for many applications)
- **Fidelity 0.75-0.85**: Moderate (significant noise)
- **Fidelity < 0.75**: Poor (high noise, may need error correction)

### TVD Interpretation:
- **TVD ≤ 0.05**: Excellent (very close to ideal)
- **TVD 0.05-0.15**: Good
- **TVD 0.15-0.25**: Moderate
- **TVD > 0.25**: Poor

### Runtime Components:
- **Keygen Time**: Scales with aux states (larger for 5q-3t)
- **IBM Queue Wait**: Dominates total time (varies by system load)
- **Exec Time**: Hardware execution (includes multiple shots)
- **ZNE Overhead**: ~15-25s for multiple noise level runs
- **Opt-3 Overhead**: ~5s for heavy transpilation

---

## 🛠️ Troubleshooting

### Error: "No IBM account found"
```bash
# Save account first:
python -c "from qiskit_ibm_runtime import QiskitRuntimeService; QiskitRuntimeService.save_account(channel='ibm_quantum', token='YOUR_TOKEN')"
```

### Error: "Backend not available"
```bash
# List available backends:
python -c "from qiskit_ibm_runtime import QiskitRuntimeService; service = QiskitRuntimeService(); print([b.name for b in service.backends()])"
```

### Long Queue Times
- IBM queue times vary by system load (5-15 minutes typical)
- Try different backends (`ibm_brisbane`, `ibm_kyoto`, `ibm_osaka`)
- Run during off-peak hours (weekends, late night UTC)

### Out of Memory
- Reduce shots: `--shots 4096`
- Run single config: `--config 3q-2t`
- 5q-3t has 31,025 aux states (high memory)

---

## 📊 Example Analysis Output

```
🎯 FIDELITY COMPARISON ACROSS ALL METHODS
================================================================
              Baseline    ZNE    Opt-0   Opt-3  Opt-0+ZNE  Opt-3+ZNE
3q-2t         0.7845   0.8912  0.7623  0.8456   0.8845    0.9234
3q-3t         0.7623   0.8734  0.7412  0.8234   0.8656    0.9123
...

🏆 BEST METHOD PER CONFIGURATION
----------------------------------
3q-2t: Opt-3+ZNE (Fidelity: 0.923400)
3q-3t: Opt-3+ZNE (Fidelity: 0.912300)
...

💡 RECOMMENDATIONS
----------------------------------
Best Fidelity: Opt-3+ZNE (Avg: 0.9178)
Fastest: Opt-0 (Avg: 12.3s)
Best Efficiency: Opt-3 (Fidelity/Time: 0.0534)
```

---

## 🎓 Understanding ZNE

### Zero-Noise Extrapolation Explained:

1. **Noise Scaling**: Execute circuit at increasing noise levels
   - Factor 1: Original circuit (baseline noise)
   - Factor 2: Double noise (gate folding: G → G·G†·G)
   - Factor 3: Triple noise

2. **Measurement**: Get results at each noise level

3. **Extrapolation**: Fit polynomial and extrapolate to zero noise
   - Linear: `p(0) ≈ 2·p(1) - p(2)`
   - Quadratic: Fit parabola through points

4. **Result**: Estimated zero-noise result

**Why it works**: Assumes noise scales linearly/polynomially with circuit repetition

---

## 🔬 Circuit Optimization Levels

| Level | Transpilation | Gate Reduction | Depth Optimization | Runtime Overhead |
|-------|--------------|----------------|-------------------|------------------|
| **0** | Minimal | None | None | ~1s |
| **1** | Light | Some | Some | ~2s (default) |
| **2** | Moderate | Good | Good | ~3s |
| **3** | Heavy | Aggressive | Aggressive | ~5s |

**Level 3 benefits**:
- Fewer gates → less gate error
- Shorter depth → less decoherence
- Better routing → fewer SWAP gates

---

## 📁 Project Structure

```
AUX-QHE/
├── ibm_hardware_noise_experiment.py   # Main experiment script
├── analyze_ibm_noise_results.py       # Results analysis
├── IBM_HARDWARE_EXPERIMENT_GUIDE.md   # This guide
├── core/                              # AUX-QHE implementation
│   ├── key_generation.py
│   ├── qotp_crypto.py
│   ├── circuit_evaluation.py
│   └── ...
├── qasm3_exports/                     # QASM 3.0 circuit exports
│   ├── 3q-2t_Baseline.qasm
│   ├── 3q-2t_ZNE.qasm
│   ├── 3q-2t_Opt-0.qasm
│   ├── 3q-2t_Opt-3.qasm
│   ├── 3q-2t_Opt-0_ZNE.qasm
│   ├── 3q-2t_Opt-3_ZNE.qasm
│   └── ... (36 total QASM files)
└── results/                           # Output directory
    ├── ibm_noise_measurement_results_*.csv
    ├── ibm_noise_measurement_results_*.json
    └── ibm_noise_measurement_analysis.png
```

---

## ⚡ Quick Start Commands

```bash
# 1. Run full experiment (all configs, all methods)
python ibm_hardware_noise_experiment.py

# 2. Analyze results
python analyze_ibm_noise_results.py

# 3. View plots
open ibm_noise_measurement_analysis.png
```

---

## 🎯 Expected Completion Time

| Configs | Methods | Total Runs | Est. Time |
|---------|---------|------------|-----------|
| 1 config | All 6 | 6 runs | ~3-5 minutes |
| 3 configs | All 6 | 18 runs | ~9-15 minutes |
| All 6 configs | All 6 | 36 runs | ~18-30 minutes |

**Note**: Highly variable due to IBM queue times!

**Configurations tested:**
- T-depth 2: 3q-2t, 4q-2t, 5q-2t
- T-depth 3: 3q-3t, 4q-3t, 5q-3t

---

## 📝 Citation

If you use this AUX-QHE implementation in your research, please cite:

```bibtex
@software{aux_qhe_2025,
  title={AUX-QHE: Auxiliary Quantum Homomorphic Encryption},
  author={Your Name},
  year={2025},
  note={IBM Quantum Hardware Implementation with Error Mitigation}
}
```

---

## 🆘 Support

For issues or questions:
1. Check this guide first
2. Review error messages carefully
3. Verify IBM account and backend access
4. Check IBM Quantum status: https://quantum.ibm.com/

---

**Generated:** October 6, 2025
**Based on:** AUX-QHE implementation with corrected auxiliary key generation
**IBM Quantum Runtime:** Qiskit Runtime Service API

🚀 **Ready to run your noise measurement experiments!**
