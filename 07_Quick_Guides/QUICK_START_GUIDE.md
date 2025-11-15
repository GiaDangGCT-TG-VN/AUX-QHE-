# Quick Start Guide - IBM Hardware Execution

## All Bugs Fixed ✅

The code is now fully debugged and ready for hardware execution. All 4 configurations (3q-3t, 4q-3t, 5q-2t, 5q-3t) pass local testing.

## Before Running on IBM Hardware

### 1. Check Queue Status
```bash
python check_backend_queue.py
```

**Current Status** (as of last check):
- `ibm_torino`: 638 jobs (shortest queue)
- `ibm_brisbane`: 3916 jobs
- `ibm_kyoto`: 1000+ jobs

**Recommendation**: Use `ibm_torino` for fastest execution

### 2. Verify Local Test (Optional)
```bash
python test_local_full_pipeline.py
```

Expected output: All tests should show `✅ PASS`

---

## Running on IBM Hardware

### Single Configuration (Recommended for First Run)

**Test with 3q-3t configuration** (smallest, fastest):
```bash
python ibm_hardware_noise_experiment.py --config 3q-3t --backend ibm_torino
```

**Run specific configuration**:
```bash
# 3 qubits, 3 T-layers
python ibm_hardware_noise_experiment.py --config 3q-3t --backend ibm_torino

# 4 qubits, 3 T-layers
python ibm_hardware_noise_experiment.py --config 4q-3t --backend ibm_torino

# 5 qubits, 2 T-layers
python ibm_hardware_noise_experiment.py --config 5q-2t --backend ibm_torino

# 5 qubits, 3 T-layers (most complex)
python ibm_hardware_noise_experiment.py --config 5q-3t --backend ibm_torino
```

### All Configurations (Full Experiment)

**Run all 4 configurations** (will take several hours due to queue):
```bash
python ibm_hardware_noise_experiment.py --backend ibm_torino
```

With custom shots:
```bash
python ibm_hardware_noise_experiment.py --backend ibm_torino --shots 2048
```

---

## What Gets Tested

For each configuration, the experiment runs **4 tests**:

1. **Baseline** - Optimization level 1, no ZNE
2. **ZNE** - Optimization level 1 with Zero-Noise Extrapolation
3. **Opt-3** - Optimization level 3, no ZNE
4. **Opt-3+ZNE** - Optimization level 3 with ZNE

### Expected Execution Flow

```
🔑 Key generation (0.05-0.63s depending on config)
🔐 QOTP encryption (<0.001s)
⚙️  Transpilation (0.03-0.24s)
🚀 Execution on IBM hardware (WAIT TIME: queue dependent)
🔍 Computing final QOTP keys (0.001-0.002s)
🔓 Decoding measurements (<0.001s)
📊 Computing fidelity
```

**Total time per configuration**:
- Local processing: ~1s
- IBM queue wait: Variable (depends on queue length)
- IBM execution: ~5 minutes for 1024 shots

---

## Monitoring Queue

### Real-time Queue Monitor
```bash
python monitor_queue.py --backend ibm_torino --threshold 100
```

This will:
- Check queue every 5 minutes
- Alert when queue drops below 100 jobs
- Auto-exit when threshold is met

### Schedule for Off-Peak Hours
```bash
python schedule_experiment.py --config 5q-3t --backend ibm_torino --off-peak
```

This will wait until 3am-8am EST (off-peak hours) to run the experiment.

---

## Output Files

### Results
- **CSV**: `ibm_noise_measurement_results_YYYYMMDD_HHMMSS.csv`
- **JSON**: `ibm_noise_measurement_results_YYYYMMDD_HHMMSS.json`

### QASM Exports
All transpiled circuits are saved to `qasm3_exports/`:
- `{config}_Baseline.qasm`
- `{config}_ZNE.qasm`
- `{config}_Opt_3.qasm`
- `{config}_Opt_3_ZNE.qasm`

---

## Results Interpretation

### Metrics Collected

For each test:
- **Fidelity**: State fidelity between ideal and noisy output (0-1, higher is better)
- **TVD**: Total Variation Distance (0-1, lower is better)
- **Execution Time**: Total time for the test
- **Circuit Depth**: Transpiled circuit depth
- **Circuit Gates**: Number of gates after transpilation

### Expected Fidelity Range

Based on local simulations:
- **3q-3t**: ~0.02 (2% fidelity)
- **4q-3t**: ~0.01 (1% fidelity)
- **5q-2t**: ~0.07 (7% fidelity)
- **5q-3t**: ~0.002 (0.2% fidelity)

**Note**: Hardware fidelity will likely be lower due to real noise.

### Comparing Methods

**Baseline vs ZNE**: ZNE should show improved fidelity
**Opt-1 vs Opt-3**: Opt-3 may reduce circuit depth but could introduce more errors
**Best method**: Look for highest fidelity + lowest TVD

---

## Troubleshooting

### Issue: "QOTP encryption failed"
**Fix**: This was a bug that's now fixed. Re-pull the latest code.

### Issue: "Circuit T-depth exceeds maximum"
**Fix**: This was a bug that's now fixed. Re-pull the latest code.

### Issue: "Unknown format code 'b' for object of type 'str'"
**Fix**: This was a bug that's now fixed. Re-pull the latest code.

### Issue: Queue is too long
**Options**:
1. Use `monitor_queue.py` to wait for shorter queue
2. Use `schedule_experiment.py` to run during off-peak hours
3. Try different backend (check with `check_backend_queue.py`)

### Issue: Job takes too long
**Explanation**: IBM hardware jobs can take hours due to:
- Queue wait time (638-3916 jobs ahead)
- Transpilation on IBM servers
- Circuit execution (5+ minutes per circuit)

**Solution**: Be patient or use monitoring tools

---

## All Fixed Bugs

✅ ZNE string format error - Fixed line 268-276, 284-291
✅ ZNE measurement gate error - Fixed line 69-70
✅ Circuit T-depth mismatch - Fixed line 143-168
✅ State fidelity calculation - Fixed line 345-348
✅ QOTP encryption validation - Enhanced core/qotp_crypto.py:37-54

See [DEBUG_FIXES_SUMMARY.md](DEBUG_FIXES_SUMMARY.md) for complete details.

---

## Summary

**You're ready to run on IBM hardware!** 🚀

**Recommended first command**:
```bash
python ibm_hardware_noise_experiment.py --config 3q-3t --backend ibm_torino
```

Good luck with your experiments!
