# 🔧 Quick Fix - Invalid Instance CRN

## ❌ Problem Identified:

Your Instance CRN ends with `::` which is **INVALID**.

**Your current CRN:**
```
crn:v1:bluemix:public:quantum-computing:us-east:a/cb5d89200ff54ca69120ca844d3fd203:d318e406-a5ff-43da-9759-824b932cbdf3::
                                                                                                                     ^^
                                                                                                                  REMOVE THIS!
```

**Should be:**
```
crn:v1:bluemix:public:quantum-computing:us-east:a/cb5d89200ff54ca69120ca844d3fd203:d318e406-a5ff-43da-9759-824b932cbdf3:
                                                                                                                     ^
                                                                                                                   ONE COLON
```

---

## ✅ Solution: Update Account with Correct CRN

### Option 1: Manual Fix (Recommended)

```bash
python edit_ibm_account.py
```

1. **Delete ALL old accounts** (option 4)
   - Delete `GiaDang_AUX`
   - Delete any other old accounts

2. **Add NEW account** (option 2)
   - Channel: **1** (IBM Cloud)
   - Name: `GiaDang_AUX`
   - Token: **Get NEW token from https://cloud.ibm.com/quantum**
   - Instance CRN: **Copy from IBM Cloud, remove trailing `:` if double**

**Critical:** When copying CRN from IBM Cloud:
- If it ends with `::`, manually remove one `:`
- Should end with single `:` only

---

### Option 2: Quick Python Fix

```python
from qiskit_ibm_runtime import QiskitRuntimeService

# Delete old accounts
QiskitRuntimeService.delete_account(name='GiaDang_AUX')

# Add new account with CORRECT CRN (remove trailing :: if present)
QiskitRuntimeService.save_account(
    channel='ibm_cloud',
    token='YOUR_NEW_TOKEN_FROM_IBM_CLOUD',  # Get from https://cloud.ibm.com/quantum
    instance='crn:v1:bluemix:public:quantum-computing:us-east:a/cb5d89200ff54ca69120ca844d3fd203:d318e406-a5ff-43da-9759-824b932cbdf3:',
    # NOTE: Single : at end   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 
    name='GiaDang_AUX',
    overwrite=True
)

print("✅ Account updated!")
```

---

### Option 3: Try WITHOUT Instance CRN

Sometimes IBM Cloud accounts work better WITHOUT specifying instance:

```python
from qiskit_ibm_runtime import QiskitRuntimeService

QiskitRuntimeService.delete_account(name='GiaDang_AUX')

QiskitRuntimeService.save_account(
    channel='ibm_cloud',
    token='YOUR_NEW_TOKEN',
    name='GiaDang_AUX',
    # NO instance parameter!
    overwrite=True
)
```

---

## 🔍 How to Get Correct Credentials:

### Step 1: Go to IBM Cloud
https://cloud.ibm.com/quantum

### Step 2: Select Your Instance
Click on your instance name

### Step 3: Get API Token
- Click "API tokens" or "Generate token"
- Copy the **44-character token**

### Step 4: Get Instance CRN (Optional)
- In instance details, copy Instance CRN
- **IMPORTANT:** If it ends with `::`, remove one `:`
- Should end with SINGLE colon `:`

---

## ✅ Test Your Fixed Account:

```bash
python check_backend_queue.py --account GiaDang_AUX
```

**Expected:** Should show backends without warnings

---

## 🆘 If Still Not Working:

### Check 1: Verify Token is Valid
- Go to https://cloud.ibm.com/quantum
- Generate a **NEW** API token
- Tokens expire, so always use fresh one

### Check 2: Verify Instance Access
- Make sure your instance has "Quantum Computing" service
- Free tier has limited access
- Some instances don't have backend access

### Check 3: Try Different Instance
If you have multiple instances, try:
```python
from qiskit_ibm_runtime import QiskitRuntimeService
service = QiskitRuntimeService()
instances = service.instances()
print(instances)  # Try each one
```

---

## 📋 Quick Checklist:

- [ ] Delete ALL old accounts
- [ ] Get NEW API token from IBM Cloud
- [ ] Get Instance CRN (remove trailing `::` if present)
- [ ] Create new account with correct credentials
- [ ] Test with: `python check_backend_queue.py --account GiaDang_AUX`
- [ ] Should see backends without "Invalid instance" warnings

**Once fixed, you'll be able to access backends!** ✅
