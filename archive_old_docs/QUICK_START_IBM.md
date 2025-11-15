# ⚡ Quick Start - IBM Quantum Hardware Experiment

**Updated for QASM 3.0 | Configs: 3q-5q for T-depth 2 & 3**

---

## 🚀 Run Experiment (One Command)

```bash
python ibm_hardware_noise_experiment.py
```

**This will:**
- Test 6 configurations: 3q, 4q, 5q for T-depth 2 and 3
- Apply 6 error mitigation methods per config
- Total: **36 experimental runs**
- Export all circuits to **QASM 3.0** format
- Save results to CSV and JSON
- Estimated time: **18-30 minutes**

---

## 📊 Analyze Results

```bash
python analyze_ibm_noise_results.py
```

**This generates:**
- Fidelity comparison tables
- TVD analysis
- Runtime breakdown
- Efficiency metrics
- Method rankings
- Visualization plots

---

## 🎯 Configurations Tested

| Config | Qubits | T-depth | Aux States |
|--------|--------|---------|------------|
| 3q-2t | 3 | 2 | 240 |
| 4q-2t | 4 | 2 | 668 |
| 5q-2t | 5 | 2 | 1,350 |
| 3q-3t | 3 | 3 | 2,826 |
| 4q-3t | 4 | 3 | 10,776 |
| 5q-3t | 5 | 3 | 31,025 |

---

## 🔬 Error Mitigation Methods

1. **Baseline** - No mitigation (opt_level=1)
2. **ZNE** - Zero-Noise Extrapolation (opt_level=1 + ZNE)
3. **Opt-0** - Minimal optimization (opt_level=0)
4. **Opt-3** - Heavy optimization (opt_level=3)
5. **Opt-0+ZNE** - Minimal opt + ZNE
6. **Opt-3+ZNE** - Heavy opt + ZNE (**best fidelity**)

---

## 📁 Output Files

### Results
- `ibm_noise_measurement_results_TIMESTAMP.csv` - All data
- `ibm_noise_measurement_results_TIMESTAMP.json` - Detailed results
- `ibm_noise_measurement_analysis.png` - Visualizations

### QASM 3.0 Exports
- `qasm3_exports/` - 36 transpiled circuits in QASM 3 format
  - Example: `3q-2t_Baseline.qasm`, `5q-3t_Opt-3_ZNE.qasm`

---

## ⚙️ Custom Options

### Single Configuration
```bash
python ibm_hardware_noise_experiment.py --config 3q-2t
```

### Different Backend
```bash
python ibm_hardware_noise_experiment.py --backend ibm_kyoto
```

### Custom Shots
```bash
python ibm_hardware_noise_experiment.py --shots 4096
```

### Combined
```bash
python ibm_hardware_noise_experiment.py --backend ibm_osaka --config 5q-3t --shots 8192
```

---

## 📊 Expected Results

### Fidelity (1.0 = perfect)
- **Opt-3+ZNE**: 0.90-0.98 (best)
- **Opt-0+ZNE**: 0.85-0.95
- **ZNE**: 0.80-0.92
- **Opt-3**: 0.75-0.88
- **Opt-0**: 0.70-0.85
- **Baseline**: 0.65-0.80 (worst)

### Runtime
- **Opt-0**: ~11-16s (fastest)
- **Baseline**: ~12-18s
- **Opt-3**: ~17-23s
- **ZNE**: ~27-35s
- **Opt-0+ZNE**: ~28-40s
- **Opt-3+ZNE**: ~35-50s (slowest, best quality)

---

## 🔍 What Gets Measured

Per experiment run:
- ✅ Fidelity
- ✅ Total Variation Distance (TVD)
- ✅ Key generation time
- ✅ Encryption time
- ✅ Transpilation time
- ✅ IBM hardware execution time
- ✅ Homomorphic evaluation time
- ✅ Decryption time
- ✅ Total end-to-end time
- ✅ Circuit depth
- ✅ Gate count
- ✅ QASM 3.0 export

---

## 💡 Recommendations

| Use Case | Method | Why |
|----------|--------|-----|
| **Production** | Opt-3+ZNE | Best fidelity |
| **Quick Test** | Baseline | Fastest |
| **Research** | All methods | Full comparison |
| **Balanced** | ZNE or Opt-3 | Good fidelity/time |

---

## 🆘 Troubleshooting

### No IBM account found
```bash
python -c "from qiskit_ibm_runtime import QiskitRuntimeService; QiskitRuntimeService.save_account(channel='ibm_quantum', token='YOUR_TOKEN')"
```

### Backend not available
```bash
# List available backends
python -c "from qiskit_ibm_runtime import QiskitRuntimeService; service = QiskitRuntimeService(); print([b.name for b in service.backends()])"
```

### Long queue times
- Try different backend: `--backend ibm_kyoto`
- Run during off-peak hours
- Test single config first: `--config 3q-2t`

---

## 📚 Full Documentation

- **Detailed Guide**: `IBM_HARDWARE_EXPERIMENT_GUIDE.md`
- **Experiment Summary**: `IBM_NOISE_EXPERIMENT_SUMMARY.md`
- **AUX-QHE Algorithm**: `AUX_QHE_PSEUDOCODE.md`

---

## ⏱️ Expected Timeline

- **1 config × 6 methods**: ~3-5 minutes
- **3 configs × 6 methods**: ~9-15 minutes
- **6 configs × 6 methods**: ~18-30 minutes

*Highly variable due to IBM queue times!*

---

**Ready to measure AUX-QHE noise on IBM Quantum hardware!** 🎯
