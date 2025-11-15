# ✏️ How to Edit IBM Quantum Accounts

**3 Easy Ways to Edit Your IBM Account Details**

---

## 📍 **Your Accounts File Location:**

```
/Users/giadang/.qiskit/qiskit-ibm.json
```

---

## 🎯 **Method 1: Interactive Editor (EASIEST)**

### Use the Account Editor Tool:

```bash
cd /Users/giadang/my_qiskitenv/AUX-QHE
python edit_ibm_account.py
```

**Features:**
- ✅ View all accounts
- ✅ Add new account
- ✅ Update account token
- ✅ Delete account
- ✅ Test connection
- ✅ Direct JSON edit

**Menu:**
```
🔧 IBM QUANTUM ACCOUNT EDITOR
================================
1. View all accounts
2. Add new account
3. Update account token
4. Delete account
5. Test account connection
6. Edit JSON file directly
7. Exit
```

---

## 🎯 **Method 2: Edit JSON File Directly**

### Open in Text Editor:

```bash
# Option A: Default editor
open ~/.qiskit/qiskit-ibm.json

# Option B: Nano
nano ~/.qiskit/qiskit-ibm.json

# Option C: VS Code (if installed)
code ~/.qiskit/qiskit-ibm.json

# Option D: Vim
vim ~/.qiskit/qiskit-ibm.json
```

### JSON Structure:

```json
{
  "ACCOUNT_NAME_HERE": {
    "channel": "ibm_quantum",
    "token": "YOUR_TOKEN_HERE",
    "url": "https://auth.quantum.ibm.com/api"
  }
}
```

### Example Edit:

**Before:**
```json
{
  "default-ibm-quantum": {
    "channel": "ibm_quantum",
    "token": "OLD_TOKEN_12345",
    "url": "https://auth.quantum.ibm.com/api"
  }
}
```

**After (updated token):**
```json
{
  "default-ibm-quantum": {
    "channel": "ibm_quantum",
    "token": "NEW_TOKEN_67890",
    "url": "https://auth.quantum.ibm.com/api"
  }
}
```

**⚠️ Important:**
- Must be valid JSON syntax
- Check for missing commas
- No trailing commas on last item
- Quotes required around strings

---

## 🎯 **Method 3: Python Script**

### Quick Update Script:

```python
from qiskit_ibm_runtime import QiskitRuntimeService

# Update existing account
QiskitRuntimeService.save_account(
    channel='ibm_quantum',
    token='YOUR_NEW_TOKEN_HERE',
    name='default-ibm-quantum',
    overwrite=True  # Replace existing
)

print("✅ Account updated!")
```

### Command Line (One-liner):

```bash
python -c "from qiskit_ibm_runtime import QiskitRuntimeService; QiskitRuntimeService.save_account(channel='ibm_quantum', token='YOUR_TOKEN', name='default-ibm-quantum', overwrite=True); print('✅ Updated!')"
```

---

## 🔑 **Getting Your IBM Quantum Token**

### For IBM Quantum (Free/Open Plan):

1. Go to https://quantum.ibm.com
2. Login to your account
3. Click **your profile icon** (top right)
4. Select **Account settings**
5. Click **Copy** next to API Token
6. Token format: `7ab345d5b6de1328b915c2bbed0e422f...`

### For IBM Cloud (Premium):

1. Go to https://cloud.ibm.com/quantum
2. Login to your IBM Cloud account
3. Navigate to **Quantum services**
4. Click **API tokens**
5. Copy your token
6. Token format: `eHc1OpTrwz8rYRBQVTArP_6BxOlVBDN4...`

---

## 📝 **Common Edits**

### 1. Update Token (Token Expired)

**Option A: Using editor tool:**
```bash
python edit_ibm_account.py
# Choose: 3. Update account token
```

**Option B: Direct JSON edit:**
```bash
nano ~/.qiskit/qiskit-ibm.json
# Find your account
# Replace "token": "OLD_TOKEN" with "token": "NEW_TOKEN"
# Save (Ctrl+O, Enter, Ctrl+X)
```

**Option C: Python:**
```python
from qiskit_ibm_runtime import QiskitRuntimeService

QiskitRuntimeService.save_account(
    channel='ibm_quantum',
    token='NEW_TOKEN_HERE',
    name='default-ibm-quantum',
    overwrite=True
)
```

---

### 2. Add New Account

**Option A: Using editor tool:**
```bash
python edit_ibm_account.py
# Choose: 2. Add new account
```

**Option B: Direct JSON edit:**
```bash
nano ~/.qiskit/qiskit-ibm.json
```

Add to JSON:
```json
{
  "existing-account": { ... },
  "new-account-name": {
    "channel": "ibm_quantum",
    "token": "YOUR_TOKEN",
    "url": "https://auth.quantum.ibm.com/api"
  }
}
```

**Option C: Python:**
```python
from qiskit_ibm_runtime import QiskitRuntimeService

QiskitRuntimeService.save_account(
    channel='ibm_quantum',
    token='YOUR_TOKEN',
    name='new-account-name'
)
```

---

### 3. Delete Account

**Option A: Using editor tool:**
```bash
python edit_ibm_account.py
# Choose: 4. Delete account
```

**Option B: Direct JSON edit:**
```bash
nano ~/.qiskit/qiskit-ibm.json
# Remove entire account block
```

**Option C: Python:**
```python
from qiskit_ibm_runtime import QiskitRuntimeService

QiskitRuntimeService.delete_account(name='account-to-delete')
```

---

### 4. Change Default Account

**Option A: Set specific account as default:**
```python
from qiskit_ibm_runtime import QiskitRuntimeService

QiskitRuntimeService.save_account(
    channel='ibm_quantum',
    token='YOUR_TOKEN',
    name='default-ibm-quantum',  # This becomes default
    set_as_default=True,
    overwrite=True
)
```

**Option B: Rename account to "default-ibm-quantum":**
```bash
nano ~/.qiskit/qiskit-ibm.json
# Change account name in JSON
```

---

## ✅ **Verify Your Changes**

### Test Account Connection:

```bash
python edit_ibm_account.py
# Choose: 5. Test account connection
```

**Or manually:**

```python
from qiskit_ibm_runtime import QiskitRuntimeService

# Test connection
service = QiskitRuntimeService(name='default-ibm-quantum')
print(f"✅ Connected!")
print(f"Backends: {len(service.backends())}")

# List backends
for backend in service.backends()[:5]:
    print(f"  - {backend.name}")
```

---

## 🔒 **Security Best Practices**

### 1. File Permissions

Ensure only you can read the file:

```bash
chmod 600 ~/.qiskit/qiskit-ibm.json
ls -la ~/.qiskit/qiskit-ibm.json
# Should show: -rw-------
```

### 2. Backup Before Editing

```bash
cp ~/.qiskit/qiskit-ibm.json ~/.qiskit/qiskit-ibm.json.backup
```

### 3. Validate JSON Syntax

After editing, test:

```bash
python -c "import json; json.load(open('/Users/giadang/.qiskit/qiskit-ibm.json')); print('✅ Valid JSON')"
```

---

## 🚨 **Troubleshooting**

### Error: "Invalid JSON"

```bash
# Check syntax
python -c "import json; json.load(open('/Users/giadang/.qiskit/qiskit-ibm.json'))"
```

**Common issues:**
- Missing comma between accounts
- Trailing comma on last item
- Missing quotes around strings
- Unbalanced braces `{}`

**Fix:** Restore from backup or use editor tool

---

### Error: "Account not found"

**Check available accounts:**
```python
from qiskit_ibm_runtime import QiskitRuntimeService
print(QiskitRuntimeService.saved_accounts())
```

---

### Error: "Invalid token"

**Reasons:**
- Token expired
- Token typo
- Wrong token format

**Fix:**
1. Get new token from IBM Quantum website
2. Update using one of the 3 methods above

---

## 📊 **Account Types**

### IBM Quantum (Free/Open Plan)
```json
{
  "channel": "ibm_quantum",
  "token": "TOKEN_HERE",
  "url": "https://auth.quantum.ibm.com/api"
}
```

### IBM Cloud
```json
{
  "channel": "ibm_cloud",
  "instance": "crn:v1:bluemix:public:...",
  "token": "TOKEN_HERE",
  "url": "https://cloud.ibm.com"
}
```

### IBM Quantum Platform (Premium)
```json
{
  "channel": "ibm_quantum_platform",
  "instance": "crn:v1:bluemix:public:...",
  "token": "TOKEN_HERE",
  "url": "https://cloud.ibm.com"
}
```

---

## 🎯 **Quick Reference**

| Task | Easiest Method | Command |
|------|----------------|---------|
| **Update token** | Editor tool | `python edit_ibm_account.py` → 3 |
| **Add account** | Editor tool | `python edit_ibm_account.py` → 2 |
| **Delete account** | Editor tool | `python edit_ibm_account.py` → 4 |
| **View accounts** | Editor tool | `python edit_ibm_account.py` → 1 |
| **Test connection** | Editor tool | `python edit_ibm_account.py` → 5 |
| **Direct edit** | Text editor | `open ~/.qiskit/qiskit-ibm.json` |

---

## ✅ **After Editing, Run AUX-QHE:**

```bash
# Your accounts are now updated
python ibm_hardware_noise_experiment.py
```

The experiment will use your updated account automatically! 🚀

---

## 📚 **Additional Resources**

- **IBM Quantum Dashboard:** https://quantum.ibm.com
- **IBM Cloud:** https://cloud.ibm.com/quantum
- **Qiskit Docs:** https://docs.quantum.ibm.com
- **Your Account Details:** `IBM_ACCOUNT_CONFIGURATION.md`
- **Account Flow Diagram:** `IBM_ACCOUNT_FLOW.md`

---

**Need help? Run the interactive editor:** `python edit_ibm_account.py` ✨
