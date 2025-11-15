# Quick Start - IBM Noise Experiment Testing

## 🚀 Ready to Run!

All bugs fixed. Architecture corrected. Let's test!

---

## Prerequisites

```bash
# 1. Activate environment
cd /Users/giadang/my_qiskitenv
source bin/activate
cd AUX-QHE

# 2. Verify IBM account (one-time setup)
python test_ibm_connection.py

# If not configured:
# python -c "from qiskit_ibm_runtime import QiskitRuntimeService; \
# QiskitRuntimeService.save_account(channel='ibm_quantum', token='YOUR_TOKEN')"
```

---

## Option 1: Local Test First (Recommended)

Test the full pipeline without using IBM credits:

```bash
# Test single configuration
python test_noise_experiment_local.py --qubits 3 --t-depth 2

# Test all configurations
python test_noise_experiment_local.py --all
```

**Expected:** All tests pass, confirms pipeline working correctly.

---

## Option 2: Single IBM Test

Test one configuration on real hardware:

```bash
python ibm_hardware_noise_experiment.py \
  --config 3q-2t \
  --shots 512 \
  --backend ibm_brisbane
```

**Time:** ~5 minutes
**Cost:** Minimal (512 shots × 4 methods = 2048 shots total)

---

## Option 3: Full Experiment

Run all configurations with all error mitigation methods:

```bash
python ibm_hardware_noise_experiment.py \
  --shots 1024 \
  --backend ibm_brisbane
```

**Runs:** 4 configs × 4 methods = 16 experiments
**Time:** ~1-2 hours (queue-dependent)
**Cost:** 1024 shots × 16 = 16,384 shots total

---

## What to Expect

### Console Output:
```
🎯 AUX-QHE IBM QUANTUM HARDWARE - NOISE MEASUREMENT EXPERIMENT
   QASM Version: OpenQASM 3.0
   Configurations: 5q-2t, 3q-3t, 4q-3t, 5q-3t (4 configs)

🔐 Loading IBM Quantum account...
   ✅ Account loaded successfully

🖥️  Getting backend: ibm_brisbane
   ✅ Backend: ibm_brisbane
      Status: active
      Queue: 5 jobs

================================================================================
🔹 Running 3q-3t with Baseline
================================================================================

   🔑 Key generation...
   ✅ Key generation: 0.037s, Aux states: 2826

   🔐 QOTP encryption...
   🔑 Keys: a_keys length=3, b_keys length=3
   🔑 Keys: a_keys=[0, 0, 0], b_keys=[0, 0, 0]
   🔐 Calling qotp_encrypt: circuit.num_qubits=3, counter_d=0, max_qubits=6
   ✅ Encryption: 0.001s

   ⚙️  Transpiling (opt_level=1)...
   ✅ Transpilation: 1.234s
      Circuit depth: 45
      Circuit gates: 120

   📝 Exporting to QASM 3.0...
      Saved to: qasm3_exports/3q-3t_Baseline.qasm

   🚀 Executing on IBM hardware...
   ✅ Execution: 12.456s
      (Note: IBM execution = Server-side homomorphic evaluation)

   🔍 Computing final QOTP keys...
   ✅ Final keys computed: 0.042s
      Final QOTP keys: a=[1, 0, 1], b=[0, 1, 0]

   🔓 Decoding measurement results...
   ✅ Decoding: 0.001s

   📊 Computing fidelity...

   ✅ RESULTS:
      Fidelity: 0.876543
      TVD: 0.123456
      Total time: 13.771s
```

### Files Generated:
```
qasm3_exports/
  3q-3t_Baseline.qasm
  3q-3t_ZNE.qasm
  3q-3t_Opt-3.qasm
  3q-3t_Opt-3_ZNE.qasm
  ... (more files)

ibm_noise_measurement_results_20251009_214500.csv
ibm_noise_measurement_results_20251009_214500.json
```

---

## Troubleshooting

### ❌ Error: "QOTP encryption failed"
**Cause:** Keys or BFV issue
**Fix:** Already fixed in latest version, re-pull code

### ❌ Error: "Circuit T-depth X exceeds maximum Y"
**Cause:** Circuit structure mismatch
**Fix:** Already fixed - test circuit now generates correct T-depth

### ❌ Error: "IBM account not found"
**Fix:**
```bash
python -c "from qiskit_ibm_runtime import QiskitRuntimeService; \
QiskitRuntimeService.save_account(channel='ibm_quantum', token='YOUR_TOKEN')"
```

### ❌ Error: "Backend not available"
**Fix:** Try different backend:
```bash
python ibm_hardware_noise_experiment.py --backend ibm_kyoto
```

### ⏳ Queue too long
**Fix:** Reduce shots or run later:
```bash
python ibm_hardware_noise_experiment.py --shots 512
```

---

## Interpreting Results

### CSV Columns:
| Column | Meaning |
|--------|---------|
| `fidelity` | How close results are to ideal (0-1, higher = better) |
| `tvd` | Total variation distance (0-1, lower = better) |
| `encrypted_counts` | Raw measurements from IBM (still encrypted) |
| `decoded_counts` | Decoded measurements (actual results) |
| `final_qotp_keys` | Keys used for decoding |

### Expected Fidelity:
- **Simulator:** ~0.99-1.00
- **IBM Hardware (no mitigation):** ~0.70-0.85
- **IBM Hardware (with ZNE):** ~0.75-0.90
- **IBM Hardware (with Opt-3+ZNE):** ~0.80-0.92

*(Actual values depend on hardware noise, queue time, etc.)*

---

## Analysis

After completion, run:

```bash
python analyze_ibm_noise_results.py ibm_noise_measurement_results_*.csv
```

This will generate:
- Fidelity comparison table
- TVD comparison table
- Best method per configuration
- Improvement analysis vs baseline

---

## Success Checklist

- [x] All bugs fixed
- [x] Architecture corrected
- [x] Local tests pass
- [ ] IBM account configured
- [ ] Single test successful
- [ ] Full experiment complete
- [ ] Results analyzed

---

## Quick Commands

```bash
# Local test
python test_noise_experiment_local.py --qubits 3 --t-depth 2

# IBM quick test
python ibm_hardware_noise_experiment.py --config 3q-2t --shots 512

# IBM full run
python ibm_hardware_noise_experiment.py --shots 1024

# Analyze results
python analyze_ibm_noise_results.py results.csv
```

---

## Documentation

- **[CORRECTED_ARCHITECTURE.md](CORRECTED_ARCHITECTURE.md)** - Full architecture explanation
- **[TESTING_SUMMARY.md](TESTING_SUMMARY.md)** - Detailed testing info
- **[IBM_NOISE_EXPERIMENT_ISSUES.md](IBM_NOISE_EXPERIMENT_ISSUES.md)** - Issues found & fixed

---

**Status:** ✅ READY TO RUN

**Questions?** Review [CORRECTED_ARCHITECTURE.md](CORRECTED_ARCHITECTURE.md) for detailed explanations.

**Let's go!** 🚀
