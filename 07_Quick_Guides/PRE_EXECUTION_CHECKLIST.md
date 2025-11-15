# 🚀 Pre-Execution Checklist - Save Your Hardware Time!

**CRITICAL:** Hardware time is limited and expensive. Follow this checklist to avoid wasting resources.

---

## ✅ STEP 1: Update IBM Account (REQUIRED)

Your current account uses deprecated `ibm_quantum` channel. **You MUST update first!**

```bash
python edit_ibm_account.py
```

1. **Delete old account** (option 4): Delete `GiaDang_AUX`
2. **Add new account** (option 2):
   - Channel: **1** (IBM Cloud)
   - Name: `GiaDang_AUX`
   - Token: Get from https://cloud.ibm.com/quantum
   - Instance CRN: Get from IBM Cloud dashboard

**Verification:**
```bash
python check_backend_queue.py --account GiaDang_AUX
```

Should show available backends. If error, see [UPDATE_IBM_ACCOUNT_GUIDE.md](UPDATE_IBM_ACCOUNT_GUIDE.md)

---

## ✅ STEP 2: Test Local Simulation

Verify your algorithm works locally **before** using hardware:

```bash
python quick_test.py
```

**Expected:** Fidelity = 1.0 (perfect)

If this fails, **DO NOT run on hardware** - fix local issues first!

---

## ✅ STEP 3: Dry Run Validation (CRITICAL)

Test hardware connection WITHOUT executing:

```bash
python ibm_hardware_noise_experiment.py \
    --config 5q-2t \
    --backend ibm_brisbane \
    --account GiaDang_AUX \
    --dry-run
```

**Expected Output:**
```
✅ DRY RUN COMPLETE - All validations passed!

📋 Validated:
   ✅ Account connection
   ✅ Backend access: ibm_brisbane
   ✅ Backend operational
   ✅ Queue status: 2 jobs

🚀 Ready to run! Remove --dry-run to execute on hardware.
```

**If dry-run fails, DO NOT proceed!** Fix issues first.

---

## ✅ STEP 4: Check Backend Queue

Find backend with shortest queue to minimize wait time:

```bash
python check_backend_queue.py --account GiaDang_AUX
```

**Look for:**
- ✅ Operational status
- Low queue (< 10 jobs is ideal)
- Enough qubits (need ≥5 qubits)

**Best backends for AUX-QHE:**
- `ibm_brisbane` (127 qubits)
- `ibm_kyoto` (127 qubits)
- `ibm_sherbrooke` (127 qubits)

---

## ✅ STEP 5: Verify Configurations

### What Gets Executed:

**Default (all configs):**
```bash
python ibm_hardware_noise_experiment.py --account GiaDang_AUX
```
Runs: 4q-3t, 5q-1t, 5q-2t, 5q-3t (16 jobs total = ~2-4 hours)

**Single config:**
```bash
python ibm_hardware_noise_experiment.py --config 5q-2t --account GiaDang_AUX
```
Runs: 5q-2t only (4 jobs = ~20-40 minutes)

### Each Config Tests 4 Methods:
1. Baseline (opt_level=1, no ZNE)
2. ZNE (opt_level=1, with ZNE)
3. Opt-3 (opt_level=3, no ZNE)
4. Opt-3+ZNE (opt_level=3, with ZNE)

### Resource Usage:
- **5q-2t**: 575 aux states, ~5-10 min/job
- **4q-3t**: 10,776 aux states, ~10-15 min/job
- **5q-3t**: 31,025 aux states, ~20-30 min/job

---

## ✅ STEP 6: Pre-Flight Checklist

Before running, verify:

- [ ] ✅ Account updated to `ibm_cloud` channel
- [ ] ✅ Account test passed: `python check_backend_queue.py --account GiaDang_AUX`
- [ ] ✅ Local simulation works: `python quick_test.py` → Fidelity = 1.0
- [ ] ✅ Dry-run validation passed
- [ ] ✅ Backend queue checked (queue < 10 jobs ideal)
- [ ] ✅ Backend is operational
- [ ] ✅ You know which config to run (5q-2t recommended for first test)
- [ ] ✅ Estimated time calculated: 
  - Single config = 4 jobs × ~10 min = 40 minutes
  - All configs = 16 jobs × ~15 min = 4 hours

---

## 🚀 STEP 7: Execute on Hardware

### Start with Single Config (Recommended):

```bash
python ibm_hardware_noise_experiment.py \
    --config 5q-2t \
    --backend ibm_brisbane \
    --shots 1024 \
    --account GiaDang_AUX
```

**Why 5q-2t first?**
- Fewest aux states (575) → Fastest execution
- T-depth=2 → Good balance of complexity vs speed
- If this works, scale to 4q-3t and 5q-3t

### Monitor Execution:

The script will show:
- Real-time progress for each method
- Queue position
- Estimated completion time
- Fidelity results as they complete

**Save the output:**
```bash
python ibm_hardware_noise_experiment.py \
    --config 5q-2t \
    --backend ibm_brisbane \
    --account GiaDang_AUX \
    2>&1 | tee hardware_run_$(date +%Y%m%d_%H%M%S).log
```

---

## ⚠️ Common Issues & Fixes

### Issue: "Failed to resolve 'auth.quantum.ibm.com'"
**Cause:** Using old deprecated account  
**Fix:** Delete old account, create new one with `ibm_cloud` channel

### Issue: "Backend not operational"
**Cause:** Backend under maintenance  
**Fix:** Choose different backend from queue check

### Issue: "T-depth exceeds limit"
**Cause:** Circuit too deep for hardware after transpilation  
**Fix:** Script auto-skips these. Check output for which configs ran.

### Issue: Jobs stuck in queue
**Cause:** High traffic period  
**Fix:** Run during off-peak hours (US nighttime, 3-8am EST)

---

## 📊 Expected Results

After successful execution, you'll get:

1. **CSV file:** `ibm_noise_measurement_results_YYYYMMDD_HHMMSS.csv`
2. **JSON file:** `ibm_noise_results_interim_YYYYMMDD_HHMMSS.json`
3. **Summary statistics** printed to console

**Typical fidelities (for reference):**
- 5q-2t Baseline: ~0.03-0.05 (3-5%)
- 4q-3t Baseline: ~0.02-0.04 (2-4%)
- 5q-3t Baseline: ~0.01-0.02 (1-2%)

**Lower fidelity = More hardware noise (expected!)**

---

## 🎯 Recommended Execution Strategy

### First Time:
1. Run **5q-2t only** with dry-run
2. If dry-run passes, run **5q-2t live**
3. Verify results look reasonable
4. Then scale to other configs

### Full Experiment:
```bash
# Run all 4 configs (will take ~4 hours)
python ibm_hardware_noise_experiment.py \
    --backend ibm_brisbane \
    --account GiaDang_AUX
```

---

## ✅ Final Checklist Before Execution

**I confirm:**
- [ ] Account is updated to `ibm_cloud` channel
- [ ] Dry-run validation passed
- [ ] Local simulation works (Fidelity = 1.0)
- [ ] Backend queue is reasonable (< 20 jobs)
- [ ] I have 40 minutes (single config) or 4 hours (all configs) available
- [ ] I've saved important files (results will be overwritten)
- [ ] I know how to monitor the job progress

**If all checked, you're ready to run!** 🚀

**Command to execute:**
```bash
python ibm_hardware_noise_experiment.py \
    --config 5q-2t \
    --backend ibm_brisbane \
    --shots 1024 \
    --account GiaDang_AUX \
    2>&1 | tee hardware_run_$(date +%Y%m%d_%H%M%S).log
```
