# 🔧 Troubleshooting IBM Hardware Experiment

**Fix for KeyError: 'fidelity' and other common issues**

---

## ❌ Error You Encountered

```python
KeyError: 'fidelity'
```

**What happened:**
- The experiment failed before collecting any results
- An empty DataFrame was returned
- The analysis function tried to access the 'fidelity' column that didn't exist

**Status:** ✅ **FIXED** - Added error handling to prevent this

---

## ✅ What Was Fixed

### 1. Added Safety Checks in Analysis Function

**Before:** Would crash if DataFrame was empty
**After:** Gracefully handles empty results with helpful error messages

```python
# Now checks if DataFrame has data
if df is None or len(df) == 0:
    print("❌ No results to analyze!")
    return
```

### 2. Added Better Error Messages

The script now tells you WHY it failed:
- Network connection issues
- IBM Quantum authentication failed
- Backend not available
- All experiments failed

---

## 🔍 Why the Original Experiment Failed

**Most likely reasons:**

1. **Network Connection**
   - IBM Quantum servers unreachable
   - Internet connection dropped

2. **Authentication Issue**
   - Token expired
   - Wrong channel type
   - Account configuration problem

3. **Backend Not Available**
   - `ibm_brisbane` was down/busy
   - Account doesn't have access to that backend

---

## 🚀 How to Fix & Test

### Step 1: Test Your IBM Connection First

**Run this BEFORE the full experiment:**

```bash
cd /Users/giadang/my_qiskitenv/AUX-QHE
python test_ibm_connection.py
```

**This will:**
- ✅ Verify your IBM account loads
- ✅ Check network connectivity
- ✅ List available backends
- ✅ Test specific backend access

**Expected output if working:**
```
🔌 TESTING IBM QUANTUM CONNECTION
=====================================

1️⃣  Loading IBM Quantum account...
   ✅ Account loaded successfully!

2️⃣  Getting account information...
   Account channel: ibm_quantum_platform
   URL: https://cloud.ibm.com
   ✅ Account info retrieved!

3️⃣  Fetching available backends...
   ✅ Found 15 quantum backends!

   📡 Available Quantum Computers:
   • ibm_brisbane (127 qubits)
   • ibm_kyoto (127 qubits)
   ...

✅ ALL TESTS PASSED!
```

---

### Step 2: If Connection Test Passes, Run Experiment

```bash
python ibm_hardware_noise_experiment.py
```

Now it will handle errors gracefully without crashing!

---

### Step 3: If Connection Test Fails

**Check these:**

#### A. Network Connection
```bash
ping quantum.ibm.com
```

If this fails, check your internet connection.

#### B. Account Status
```bash
python edit_ibm_account.py
# Choose: 1. View all accounts
# Choose: 5. Test account connection
```

#### C. Token Valid
Get new token from:
- https://quantum.ibm.com (for ibm_quantum)
- https://cloud.ibm.com/quantum (for ibm_cloud)

Update token:
```bash
python edit_ibm_account.py
# Choose: 3. Update account token
```

---

## 📊 Common Errors & Solutions

### Error 1: "No account found"

**Cause:** No IBM account configured

**Fix:**
```bash
python edit_ibm_account.py
# Choose: 2. Add new account
```

---

### Error 2: "Connection timeout"

**Cause:** Network/firewall issue

**Fix:**
- Check internet connection
- Check firewall settings
- Try different network
- Check if IBM Quantum is operational: https://quantum.ibm.com/status

---

### Error 3: "Backend not available"

**Cause:** Specified backend doesn't exist or you don't have access

**Fix:**
```bash
# List available backends first
python test_ibm_connection.py

# Then use one of the available backends
python ibm_hardware_noise_experiment.py --backend ibm_kyoto
```

---

### Error 4: "Invalid token" / "Authentication failed"

**Cause:** Token expired or incorrect

**Fix:**
1. Get new token from https://quantum.ibm.com
2. Update account:
```bash
python edit_ibm_account.py
# Choose: 3. Update account token
```

---

### Error 5: "KeyError: 'fidelity'" (Your original error)

**Cause:** Experiment failed, no results collected

**Fix:** ✅ Already fixed! Script now handles this gracefully

**Now shows:**
```
⚠️  Experiment finished but no results were collected

💡 Possible reasons:
   - Network connection issues
   - IBM Quantum authentication failed
   - Backend not available
   - All experiments failed
```

---

## 🎯 Recommended Workflow

### Before Running Full Experiment:

```bash
# 1. Test connection
python test_ibm_connection.py

# 2. If test passes, run small test first
python ibm_hardware_noise_experiment.py --config 3q-2t --shots 1024

# 3. If small test works, run full experiment
python ibm_hardware_noise_experiment.py
```

---

## 🔧 Quick Fixes

### Reset Everything

```bash
# Remove bad result files
rm ibm_noise_measurement_results_*.csv
rm ibm_noise_measurement_results_*.json

# Test connection
python test_ibm_connection.py

# Run experiment
python ibm_hardware_noise_experiment.py --config 3q-2t
```

---

### Check IBM Quantum Status

```bash
# Visit IBM Quantum status page
open https://quantum.ibm.com/status

# Or check from command line
python -c "from qiskit_ibm_runtime import QiskitRuntimeService; s = QiskitRuntimeService(); print(f'✅ Connected! Backends: {len(s.backends())}')"
```

---

## 📝 Diagnostic Commands

### Check Account Configuration
```bash
python -c "from qiskit_ibm_runtime import QiskitRuntimeService; print(QiskitRuntimeService.saved_accounts())"
```

### List All Backends
```bash
python -c "from qiskit_ibm_runtime import QiskitRuntimeService; s = QiskitRuntimeService(); [print(f'{b.name}: {b.num_qubits} qubits') for b in s.backends()]"
```

### Test Specific Backend
```bash
python test_ibm_connection.py --backend ibm_kyoto
```

---

## 🆘 Still Not Working?

### 1. Try Simulator First

```bash
# Use local simulator (doesn't need IBM connection)
python quick_test.py
```

This tests AUX-QHE locally without IBM hardware.

---

### 2. Check Required Packages

```bash
pip list | grep qiskit
```

Should show:
- `qiskit`
- `qiskit-ibm-runtime`

If missing:
```bash
pip install qiskit qiskit-ibm-runtime
```

---

### 3. Verify Python Version

```bash
python --version
```

Should be Python 3.8 or higher.

---

### 4. Clean Install

```bash
pip uninstall qiskit qiskit-ibm-runtime -y
pip install qiskit qiskit-ibm-runtime
```

---

## ✅ Summary of Fixes

| Issue | Status | Solution |
|-------|--------|----------|
| KeyError: 'fidelity' | ✅ Fixed | Added error handling in analysis |
| No error messages | ✅ Fixed | Added helpful diagnostics |
| Can't test connection | ✅ Fixed | Created test_ibm_connection.py |
| Can't manage accounts | ✅ Fixed | Created edit_ibm_account.py |

---

## 🚀 Next Steps

1. **Run connection test:**
   ```bash
   python test_ibm_connection.py
   ```

2. **If test passes, run small experiment:**
   ```bash
   python ibm_hardware_noise_experiment.py --config 3q-2t --shots 1024
   ```

3. **If successful, run full experiment:**
   ```bash
   python ibm_hardware_noise_experiment.py
   ```

---

**Your experiment script is now fixed and ready to use!** ✅
