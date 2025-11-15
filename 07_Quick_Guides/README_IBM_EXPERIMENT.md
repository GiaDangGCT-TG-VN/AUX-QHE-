# AUX-QHE IBM Quantum Hardware Noise Measurement

**Status:** ✅ Ready for deployment (all bugs fixed)
**Date:** 2025-10-09

---

## Quick Start

```bash
# 1. Activate environment
cd /Users/giadang/my_qiskitenv && source bin/activate && cd AUX-QHE

# 2. Test locally (no IBM credits used)
python test_noise_experiment_local.py --qubits 3 --t-depth 2

# 3. Run on IBM hardware
python ibm_hardware_noise_experiment.py --config 3q-2t --shots 512
```

---

## Architecture Overview

### Correct QHE Flow

```
CLIENT SIDE:
1. Key Generation    → aux_keygen()
2. QOTP Encryption   → qotp_encrypt(circuit, keys)
3. Send to Server    → transpile + submit

QUANTUM SERVER (IBM):
4. Homomorphic Eval  → Execute encrypted circuit (THIS is the HE phase!)

CLIENT SIDE:
5. Compute Final Keys → aux_eval() computes key evolution
6. Decode Results     → XOR measurements with final keys
```

### Key Points

- **IBM execution IS the homomorphic evaluation** (server-side quantum computation)
- **aux_eval() computes final QOTP keys** (client-side classical simulation)
- **Measurements are decoded**, not circuits

---

## Files

### Essential Files

| File | Purpose |
|------|---------|
| `ibm_hardware_noise_experiment.py` | Main experiment script |
| `test_noise_experiment_local.py` | Local testing (no IBM) |
| `test_ibm_connection.py` | Verify IBM account |
| `CORRECTED_ARCHITECTURE.md` | Detailed architecture |
| `QUICK_START_TESTING.md` | Quick start guide |
| `TESTING_SUMMARY.md` | Test results summary |

### Core Algorithm

| File | Purpose |
|------|---------|
| `core/bfv_core.py` | BFV homomorphic encryption |
| `core/key_generation.py` | AUX-QHE key generation |
| `core/qotp_crypto.py` | QOTP encryption/decryption |
| `core/circuit_evaluation.py` | Circuit evaluation (key tracking) |

---

## Bugs Fixed

1. ✅ **MockEncoder scope error** - `degree` variable undefined
2. ✅ **qotp_encrypt API** - Missing BFV parameters
3. ✅ **qotp_decrypt API** - Missing BFV parameters
4. ✅ **Architecture flow** - Corrected aux_eval usage
5. ✅ **Measurement decoding** - Properly decode with final keys

---

## Running Experiments

### Local Test (Recommended First)

```bash
# Single configuration
python test_noise_experiment_local.py --qubits 3 --t-depth 2

# All configurations
python test_noise_experiment_local.py --all
```

**Expected:** All tests pass (fidelity issues are normal - we decode measurements, not circuits)

### IBM Hardware

**Quick Test (5 min, ~2K shots):**
```bash
python ibm_hardware_noise_experiment.py --config 3q-2t --shots 512
```

**Full Experiment (1-2 hours, ~16K shots):**
```bash
python ibm_hardware_noise_experiment.py --shots 1024
```

**Configurations tested:**
- 5q-2t, 3q-3t, 4q-3t, 5q-3t

**Error mitigation methods:**
- Baseline (no mitigation)
- ZNE (Zero-Noise Extrapolation)
- Opt-3 (optimization level 3)
- Opt-3+ZNE (combined)

**Total runs:** 4 configs × 4 methods = 16 experiments

---

## Output Files

```
qasm3_exports/
  3q-3t_Baseline.qasm
  3q-3t_ZNE.qasm
  ...

ibm_noise_measurement_results_TIMESTAMP.csv
ibm_noise_measurement_results_TIMESTAMP.json
```

### CSV Columns

- **config, method, backend** - Experiment parameters
- **fidelity, tvd** - Performance metrics
- **encrypted_counts** - Raw IBM measurements (encrypted)
- **decoded_counts** - Decoded measurements (actual results)
- **final_qotp_keys** - Keys used for decoding
- **Timing:** keygen_time, encrypt_time, exec_time, eval_time, decrypt_time

---

## Expected Results

| Metric | Value |
|--------|-------|
| Fidelity (simulator) | 0.99-1.00 |
| Fidelity (IBM baseline) | 0.70-0.85 |
| Fidelity (IBM + ZNE) | 0.75-0.90 |
| Fidelity (IBM + Opt-3+ZNE) | 0.80-0.92 |

---

## Troubleshooting

### Error: "QOTP encryption failed"
**Fix:** Already fixed. Re-pull latest code.

### Error: "Circuit T-depth exceeds maximum"
**Fix:** Already fixed. Test circuit generates correct T-depth.

### Error: "IBM account not found"
```bash
python -c "from qiskit_ibm_runtime import QiskitRuntimeService; \
QiskitRuntimeService.save_account(channel='ibm_quantum', token='YOUR_TOKEN')"
```

### Queue too long
```bash
# Use fewer shots
python ibm_hardware_noise_experiment.py --shots 512

# Or try different backend
python ibm_hardware_noise_experiment.py --backend ibm_kyoto
```

---

## What This Measures

1. **Noise effects** on AUX-QHE encrypted circuits
2. **Error mitigation** effectiveness (ZNE, optimization)
3. **Scalability** across qubit counts and T-depths
4. **Performance overhead** of AUX-QHE encryption

**NOT measuring:** Full blind delegation (this is a performance test)

---

## Privacy Properties

✅ **Circuit Privacy:** IBM sees encrypted circuit with QOTP gates
✅ **Result Privacy:** Measurements encrypted, decoded client-side
✅ **Key Privacy:** BFV protects QOTP keys homomorphically
✅ **Server Blindness:** IBM cannot determine original circuit or results

---

## Commands Reference

```bash
# Local testing
python test_noise_experiment_local.py --qubits 3 --t-depth 2
python test_noise_experiment_local.py --all

# IBM testing
python ibm_hardware_noise_experiment.py --config 3q-2t --shots 512
python ibm_hardware_noise_experiment.py --shots 1024
python ibm_hardware_noise_experiment.py --backend ibm_kyoto --shots 8192

# Verify IBM connection
python test_ibm_connection.py

# Analyze results
python analyze_ibm_noise_results.py results.csv
```

---

## Documentation

- **[CORRECTED_ARCHITECTURE.md](CORRECTED_ARCHITECTURE.md)** - Complete architecture with diagrams
- **[TESTING_SUMMARY.md](TESTING_SUMMARY.md)** - Detailed testing info
- **[QUICK_START_TESTING.md](QUICK_START_TESTING.md)** - Quick start guide
- **[AUX_QHE_PSEUDOCODE.md](AUX_QHE_PSEUDOCODE.md)** - Algorithm pseudocode
- **[archive_old_docs/](archive_old_docs/)** - Archived documentation

---

## Support

**Questions?** Review [CORRECTED_ARCHITECTURE.md](CORRECTED_ARCHITECTURE.md)

**Issues?** Check [TESTING_SUMMARY.md](TESTING_SUMMARY.md) troubleshooting section

---

**Status:** ✅ All bugs fixed, ready for IBM hardware testing
**Last Updated:** 2025-10-09
