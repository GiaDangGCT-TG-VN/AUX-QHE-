# 🔑 Update IBM Account - Migration Guide

**Date:** October 26, 2025  
**Issue:** Old `ibm_quantum` channel is deprecated (sunset July 1, 2025)  
**Solution:** Migrate to new `ibm_cloud` channel

---

## ⚠️ Important Notice

The old IBM Quantum channel (`auth.quantum.ibm.com`) is **deprecated**. You must update to:
- **IBM Cloud** (`ibm_cloud`) - Recommended for all users
- **IBM Quantum Platform** (`ibm_quantum_platform`) - Premium only

---

## 🚀 Step-by-Step Update Process

### Step 1: Delete Old Account

```bash
cd /Users/giadang/my_qiskitenv/AUX-QHE
python edit_ibm_account.py
```

Select **option 4** (Delete account), then delete `GiaDang_AUX`

### Step 2: Get Your New Credentials

Go to: **https://cloud.ibm.com/quantum**

1. **Login** with your IBM account
2. Click on your **Quantum instance**
3. Copy these 2 things:
   - **API Token** (44 characters)
   - **Instance CRN** (starts with `crn:v1:bluemix:public:quantum-computing:...`)

### Step 3: Add New Account

```bash
python edit_ibm_account.py
```

Select **option 2** (Add new account)

**Input the following:**
- Channel: **1** (IBM Cloud)
- Account name: `GiaDang_AUX` (or any name you prefer)
- API Token: **[Paste your 44-character token]**
- Instance CRN: **[Paste your full CRN]**

### Step 4: Test Connection

In the same script, select **option 5** (Test account connection)

You should see:
```
✅ Connected successfully!
📡 Available backends: X
   • ibm_brisbane (127 qubits) - active
   • ibm_kyoto (127 qubits) - active
   ...
```

---

## 🔧 Alternative: Direct Python Command

```python
from qiskit_ibm_runtime import QiskitRuntimeService

QiskitRuntimeService.save_account(
    channel='ibm_cloud',
    token='YOUR_44_CHARACTER_TOKEN_HERE',
    instance='crn:v1:bluemix:public:quantum-computing:us-south:...',
    name='GiaDang_AUX',
    overwrite=True
)

# Test it
service = QiskitRuntimeService(name='GiaDang_AUX')
print(f"✅ Connected! Backends: {len(service.backends())}")
```

---

## 📍 Where to Find Instance CRN

**Method 1: IBM Cloud Dashboard**
1. Go to: https://cloud.ibm.com/quantum
2. Click your instance name
3. Look for **Instance CRN** in the details section
4. Format: `crn:v1:bluemix:public:quantum-computing:us-south:a/...:...::`

**Method 2: From Service**
```python
from qiskit_ibm_runtime import QiskitRuntimeService
service = QiskitRuntimeService()
instances = service.instances()
print(instances)  # Shows all your instance CRNs
```

---

## ✅ Verification

After updating, verify your hardware script works:

```bash
python test_ibm_connection.py
```

Expected output:
```
✅ Successfully connected to IBM Quantum
📡 Available backends: X
   • ibm_brisbane (127 qubits)
   • ibm_kyoto (127 qubits)
   ...
```

---

## 🎯 Ready to Run Hardware Experiments

Once your account is updated, you can run hardware experiments:

```bash
python ibm_hardware_noise_experiment.py --config 5q-2t --backend ibm_brisbane --shots 1024
```

---

## ❓ Troubleshooting

**Error: "Failed to resolve 'auth.quantum.ibm.com'"**
- **Cause**: Using old deprecated channel
- **Fix**: Delete old account, create new one with `ibm_cloud` channel

**Error: "No instance specified"**
- **Cause**: Missing Instance CRN
- **Fix**: Add your Instance CRN when creating account

**Error: "401 Unauthorized"**
- **Cause**: Invalid or expired token
- **Fix**: Generate new token from https://cloud.ibm.com/quantum

---

## 📚 Official Migration Guide

IBM's official guide: https://quantum.cloud.ibm.com/docs/migration-guides/classic-iqp-to-cloud-iqp
