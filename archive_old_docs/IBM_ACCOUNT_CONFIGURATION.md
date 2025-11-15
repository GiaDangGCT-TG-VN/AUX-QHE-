# 🔐 IBM Quantum Account Configuration Guide

**Your AUX-QHE Implementation - IBM Account Details**

---

## 📍 Account Location

**File:** `~/.qiskit/qiskit-ibm.json`

**Full Path:** `/Users/giadang/.qiskit/qiskit-ibm.json`

---

## 🔑 Your Configured Accounts

You have **7 IBM Quantum accounts** configured:

### 1. **default-ibm-quantum** (Recommended for AUX-QHE)
```json
{
  "channel": "ibm_quantum",
  "token": "7ab345d5b6de1328b915c2bbed0e422f...",
  "url": "https://auth.quantum.ibm.com/api"
}
```
**Use case:** IBM Quantum Platform (Open Plan)
**Access:** Free tier quantum computers

---

### 2. **DNA-Alignment**
```json
{
  "channel": "ibm_quantum_platform",
  "instance": "crn:v1:bluemix:public:quantum-computing:us-east:...",
  "token": "_E9_63Zvy4O9kGPlYGzAzKl4I7yhlzDi_JEYVuP80hkw",
  "url": "https://cloud.ibm.com"
}
```
**Use case:** IBM Cloud instance (Premium)
**Access:** Cloud-based quantum computing service

---

### 3. **GiaDang**
```json
{
  "channel": "ibm_cloud",
  "instance": "crn:v1:bluemix:public:quantum-computing:us-east:...",
  "token": "eHc1OpTrwz8rYRBQVTArP_6BxOlVBDN43G-RF9l8bkXz",
  "url": "https://cloud.ibm.com"
}
```
**Use case:** IBM Cloud instance
**Access:** Personal cloud service

---

### 4. **Gia_Dang**
```json
{
  "channel": "ibm_cloud",
  "instance": "crn:v1:bluemix:public:quantum-computing:us-east:...",
  "token": "ivT3H3kmsl7JhhpGtg0b73K-urCzXxDS0EW7zjRXK0Rg",
  "url": "https://cloud.ibm.com"
}
```
**Use case:** IBM Cloud instance (alternative)
**Access:** Cloud service

---

### 5. **default-ibm-cloud**
```json
{
  "channel": "ibm_cloud",
  "instance": "crn:v1:bluemix:public:quantum-computing:us-east:...",
  "token": "ivT3H3kmsl7JhhpGtg0b73K-urCzXxDS0EW7zjRXK0Rg",
  "url": "https://cloud.ibm.com"
}
```
**Use case:** Default IBM Cloud account
**Access:** Cloud-based quantum service

---

### 6. **open**
```json
{
  "channel": "ibm_quantum",
  "instance": "h2/g2/p2",
  "token": "<7b606bed6c7ae3ba3662f93c5555c9fd...>",
  "url": "https://auth.quantum-computing.ibm.com/api"
}
```
**Use case:** IBM Quantum Open Plan
**Access:** Public quantum computers

---

### 7. **qgss-2025**
```json
{
  "channel": "ibm_quantum_platform",
  "instance": "crn:v1:bluemix:public:quantum-computing:us-east:...",
  "token": "_E9_63Zvy4O9kGPlYGzAzKl4I7yhlzDi_JEYVuP80hkw",
  "url": "https://cloud.ibm.com"
}
```
**Use case:** Quantum Global Summer School 2025
**Access:** Special program access

---

## 🚀 How AUX-QHE Uses These Accounts

### Default Behavior

When you run the experiment:

```python
service = QiskitRuntimeService()
```

**What happens:**
1. Qiskit looks for `~/.qiskit/qiskit-ibm.json`
2. Loads the **first available account** (or default if specified)
3. Connects to IBM Quantum services
4. Provides access to backends

### Current Implementation

**File:** `ibm_hardware_noise_experiment.py` (line 343)

```python
# Load IBM Quantum account
print("\n🔐 Loading IBM Quantum account...")
try:
    service = QiskitRuntimeService()
    print(f"   ✅ Account loaded successfully")
except Exception as e:
    print(f"   ❌ Error loading account: {e}")
```

**This automatically uses your saved credentials!**

---

## 🔧 Selecting a Specific Account

### Method 1: Specify Account Name

```python
# Use specific account
service = QiskitRuntimeService(name='default-ibm-quantum')

# Or use instance
service = QiskitRuntimeService(name='DNA-Alignment')
```

### Method 2: Specify Channel

```python
# Use IBM Quantum channel
service = QiskitRuntimeService(channel='ibm_quantum')

# Use IBM Cloud channel
service = QiskitRuntimeService(channel='ibm_cloud')
```

### Method 3: Environment Variable

```bash
export QISKIT_IBM_ACCOUNT='default-ibm-quantum'
python ibm_hardware_noise_experiment.py
```

---

## 🛠️ Modifying the Experiment Script

If you want to use a **specific account**, update the script:

### Option A: Use Specific Account Name

```python
# In ibm_hardware_noise_experiment.py, line 343
# Replace:
service = QiskitRuntimeService()

# With:
service = QiskitRuntimeService(name='default-ibm-quantum')
```

### Option B: Add Account Selection Parameter

Add to the argument parser:

```python
parser.add_argument('--account', type=str, default=None,
                   help='IBM account name to use')
```

Then modify the service initialization:

```python
if args.account:
    service = QiskitRuntimeService(name=args.account)
else:
    service = QiskitRuntimeService()
```

**Usage:**
```bash
python ibm_hardware_noise_experiment.py --account default-ibm-quantum
```

---

## 📊 Account Comparison

| Account Name | Channel | Access Level | Best For |
|--------------|---------|--------------|----------|
| **default-ibm-quantum** | ibm_quantum | Open Plan | **Recommended for AUX-QHE** |
| DNA-Alignment | ibm_quantum_platform | Premium | Large-scale experiments |
| GiaDang | ibm_cloud | Cloud | Cloud integration |
| Gia_Dang | ibm_cloud | Cloud | Alternative cloud |
| default-ibm-cloud | ibm_cloud | Cloud | Default cloud |
| open | ibm_quantum | Open Plan | Public access |
| qgss-2025 | ibm_quantum_platform | Special | Summer school |

---

## 🎯 Recommended Setup for AUX-QHE

### For Best Results:

**Use:** `default-ibm-quantum` or `open`

**Why:**
- ✅ Direct access to IBM Quantum Platform
- ✅ No cloud overhead
- ✅ Access to latest quantum systems
- ✅ Better for research/experiments

### Backends Available:

Run this to see available backends:

```python
from qiskit_ibm_runtime import QiskitRuntimeService

service = QiskitRuntimeService(name='default-ibm-quantum')
backends = service.backends()

for backend in backends:
    print(f"- {backend.name}: {backend.num_qubits} qubits, {backend.status().status_msg}")
```

**Expected backends:**
- `ibm_brisbane` (127 qubits)
- `ibm_kyoto` (127 qubits)
- `ibm_osaka` (127 qubits)
- `ibm_sherbrooke` (127 qubits)
- `ibm_torino` (133 qubits)
- And more...

---

## 🔐 Security Notes

### Your Tokens are Stored Securely

**Location:** `~/.qiskit/qiskit-ibm.json`

**Permissions:**
```bash
chmod 600 ~/.qiskit/qiskit-ibm.json  # Read/write for owner only
```

### Never Share Tokens

- ❌ Don't commit to Git
- ❌ Don't share in code
- ❌ Don't include in logs
- ✅ Keep in `~/.qiskit/` directory

### Rotating Tokens

If you need to update a token:

```python
from qiskit_ibm_runtime import QiskitRuntimeService

# Delete old account
QiskitRuntimeService.delete_account(name='default-ibm-quantum')

# Save new account
QiskitRuntimeService.save_account(
    channel='ibm_quantum',
    token='YOUR_NEW_TOKEN',
    name='default-ibm-quantum',
    overwrite=True
)
```

---

## 📝 Checking Current Configuration

### View All Accounts

```python
from qiskit_ibm_runtime import QiskitRuntimeService

# List all saved accounts
accounts = QiskitRuntimeService.saved_accounts()
for name, account in accounts.items():
    print(f"{name}: {account['channel']}")
```

### Test Account Connection

```python
from qiskit_ibm_runtime import QiskitRuntimeService

try:
    service = QiskitRuntimeService(name='default-ibm-quantum')
    print(f"✅ Connected to IBM Quantum")
    print(f"   Available backends: {len(service.backends())}")
except Exception as e:
    print(f"❌ Connection failed: {e}")
```

---

## 🚀 Quick Setup for AUX-QHE

### 1. Verify Account

```bash
python -c "from qiskit_ibm_runtime import QiskitRuntimeService; service = QiskitRuntimeService(); print('✅ Account loaded:', service.active_account())"
```

### 2. List Backends

```bash
python -c "from qiskit_ibm_runtime import QiskitRuntimeService; service = QiskitRuntimeService(); [print(f'- {b.name}') for b in service.backends()[:10]]"
```

### 3. Run Experiment

```bash
python ibm_hardware_noise_experiment.py
```

**The script will automatically:**
- ✅ Load your saved account
- ✅ Connect to IBM Quantum
- ✅ Select specified backend (default: `ibm_brisbane`)
- ✅ Run all 36 experiments

---

## 🔧 Advanced Configuration

### Use Multiple Accounts

Run different configs with different accounts:

```python
# 3q configs with free account
service_free = QiskitRuntimeService(name='default-ibm-quantum')
backend_free = service_free.backend('ibm_brisbane')

# 5q configs with premium account
service_premium = QiskitRuntimeService(name='DNA-Alignment')
backend_premium = service_premium.backend('ibm_kyoto')
```

### Set Default Account

```python
from qiskit_ibm_runtime import QiskitRuntimeService

# This becomes the default
QiskitRuntimeService.save_account(
    channel='ibm_quantum',
    token='YOUR_TOKEN',
    name='default-ibm-quantum',
    set_as_default=True
)
```

---

## 📊 Account Selection Strategy

### For AUX-QHE Experiment:

| Use Case | Recommended Account | Backend |
|----------|-------------------|---------|
| **Quick test** | default-ibm-quantum | ibm_brisbane |
| **Full experiment** | default-ibm-quantum | ibm_kyoto |
| **Production** | DNA-Alignment (premium) | ibm_sherbrooke |
| **Research** | qgss-2025 | Any available |

### Backend Selection:

```python
# In ibm_hardware_noise_experiment.py
# Default backend (line 311):
backend_name = 'ibm_brisbane'

# Override with command line:
python ibm_hardware_noise_experiment.py --backend ibm_kyoto
```

---

## 🎯 Summary

### Your Current Setup:

✅ **7 accounts configured** in `~/.qiskit/qiskit-ibm.json`
✅ **Automatic loading** via `QiskitRuntimeService()`
✅ **No manual configuration needed** for basic usage

### For AUX-QHE:

✅ Default behavior uses your saved accounts
✅ Specify `--backend` to choose quantum computer
✅ No API key needed in code (already saved)
✅ Ready to run immediately

### To Run:

```bash
# Uses default account automatically
python ibm_hardware_noise_experiment.py

# Or specify backend
python ibm_hardware_noise_experiment.py --backend ibm_osaka
```

**Your accounts are already configured and ready to use!** 🚀

---

## 🆘 Troubleshooting

### Error: "No account found"

```python
# Re-save account
from qiskit_ibm_runtime import QiskitRuntimeService
QiskitRuntimeService.save_account(
    channel='ibm_quantum',
    token='YOUR_TOKEN',
    name='default-ibm-quantum'
)
```

### Error: "Invalid token"

- Check token hasn't expired
- Get new token from https://quantum.ibm.com
- Re-save with new token

### Error: "Backend not available"

```python
# List available backends
service = QiskitRuntimeService()
print([b.name for b in service.backends()])
```

---

**Your IBM Quantum accounts are configured and ready for AUX-QHE experiments!** ✅
