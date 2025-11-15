# 🧪 Test Your New IBM Account Setup

After updating to the new `ibm_cloud` channel, use these commands to verify everything works.

---

## ✅ Step 1: Test Basic Connection

```bash
python check_backend_queue.py --account GiaDang_AUX
```

**Expected Output:**
```
✅ Account loaded: GiaDang_AUX

Found X quantum backends:

Backend              Qubits   Queue    Status       Message
--------------------------------------------------------------------------------
ibm_brisbane         127      0        ✅           active
ibm_kyoto            127      2        ✅           active
...
```

**If you see errors:**
- Update account: `python edit_ibm_account.py`
- Follow: `cat UPDATE_IBM_ACCOUNT_GUIDE.md`

---

## ✅ Step 2: Check Specific Backend

```bash
python check_backend_queue.py ibm_brisbane --account GiaDang_AUX
```

**Expected Output:**
```
🔍 Checking ibm_brisbane...

Backend: ibm_brisbane
Qubits: 127
Queue: 0 jobs
Status: active
Operational: ✅ Yes
```

---

## ✅ Step 3: Test Connection Script

```bash
python test_ibm_connection.py
```

**Expected Output:**
```
✅ Successfully connected to IBM Quantum
📡 Available backends: X
   • ibm_brisbane (127 qubits)
   • ibm_kyoto (127 qubits)
   ...
```

---

## ✅ Step 4: Dry Run Hardware Experiment (Optional)

Test the main script without actually running (just checks setup):

```bash
python ibm_hardware_noise_experiment.py --help
```

---

## 🎯 Usage Examples After Setup

### Check All Backends
```bash
python check_backend_queue.py --account GiaDang_AUX
```

### Check Specific Backend
```bash
python check_backend_queue.py ibm_brisbane --account GiaDang_AUX
```

### Use Default Account (if set as default)
```bash
python check_backend_queue.py
```

---

## 🚀 Ready to Run Experiments

Once all tests pass, run your AUX-QHE experiment:

```bash
# Example: 5q-2t on ibm_brisbane with 1024 shots
python ibm_hardware_noise_experiment.py \
    --config 5q-2t \
    --backend ibm_brisbane \
    --shots 1024
```

---

## ❓ Common Issues

**Issue: "Failed to resolve 'auth.quantum.ibm.com'"**
- **Fix:** Old account still exists, delete it:
  ```bash
  python edit_ibm_account.py
  # Choose option 4 (Delete account)
  # Then add new account with option 2
  ```

**Issue: "No instance specified"**
- **Fix:** Add Instance CRN when creating account
- Get from: https://cloud.ibm.com/quantum → Your Instance

**Issue: "Account not found: GiaDang_AUX"**
- **Fix:** Create account first:
  ```bash
  python edit_ibm_account.py
  # Choose option 2 (Add new account)
  ```

---

## 📋 Checklist

- [ ] Old `ibm_quantum` account deleted
- [ ] New `ibm_cloud` account created with name `GiaDang_AUX`
- [ ] API Token added (44 characters)
- [ ] Instance CRN added (starts with `crn:v1:bluemix:...`)
- [ ] `check_backend_queue.py` shows available backends
- [ ] Test connection successful

**Once all checked, you're ready to run hardware experiments!** ✅
