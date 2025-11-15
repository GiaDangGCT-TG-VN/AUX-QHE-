# 🔄 IBM Account Flow in AUX-QHE Hardware Execution

**How your IBM Quantum accounts integrate with the AUX-QHE algorithm**

---

## 🎯 Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                     AUX-QHE Hardware Execution Flow                  │
└─────────────────────────────────────────────────────────────────────┘

Step 1: Account Loading
┌──────────────────────────────────────────────────────────────────┐
│  ibm_hardware_noise_experiment.py (line 343)                     │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ service = QiskitRuntimeService()                         │   │
│  └──────────────────────────────────────────────────────────┘   │
│                            │                                      │
│                            ▼                                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Reads: ~/.qiskit/qiskit-ibm.json                         │   │
│  │                                                           │   │
│  │ Available accounts:                                       │   │
│  │   • default-ibm-quantum (ibm_quantum) ✅ RECOMMENDED     │   │
│  │   • DNA-Alignment (ibm_quantum_platform)                 │   │
│  │   • GiaDang (ibm_cloud)                                  │   │
│  │   • Gia_Dang (ibm_cloud)                                 │   │
│  │   • default-ibm-cloud (ibm_cloud)                        │   │
│  │   • open (ibm_quantum)                                   │   │
│  │   • qgss-2025 (ibm_quantum_platform)                     │   │
│  └──────────────────────────────────────────────────────────┘   │
│                            │                                      │
│                            ▼                                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Loads default or first available account                 │   │
│  │ Token: Retrieved from JSON                               │   │
│  │ Channel: Retrieved from JSON                             │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
                             │
                             ▼

Step 2: Backend Selection
┌──────────────────────────────────────────────────────────────────┐
│  ibm_hardware_noise_experiment.py (line 354)                     │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ backend = service.backend(backend_name)                  │   │
│  │ Default: 'ibm_brisbane'                                  │   │
│  └──────────────────────────────────────────────────────────┘   │
│                            │                                      │
│                            ▼                                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Connects to IBM Quantum Backend:                         │   │
│  │   • ibm_brisbane (127 qubits)                            │   │
│  │   • ibm_kyoto (127 qubits)                               │   │
│  │   • ibm_osaka (127 qubits)                               │   │
│  │   • ibm_sherbrooke (127 qubits)                          │   │
│  │   • ibm_torino (133 qubits)                              │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
                             │
                             ▼

Step 3: AUX-QHE Algorithm Execution
┌──────────────────────────────────────────────────────────────────┐
│  For each configuration (3q-2t, 4q-2t, 5q-2t, 3q-3t, 4q-3t,     │
│                         5q-3t):                                   │
│                                                                   │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ 1. Key Generation (local - no IBM)                     │     │
│  │    ├─ aux_keygen(num_wires, t_depth, a_init, b_init)  │     │
│  │    └─ Generates: prep_key, eval_key, dec_key          │     │
│  └────────────────────────────────────────────────────────┘     │
│                            │                                      │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ 2. Circuit Creation (local - no IBM)                   │     │
│  │    ├─ Create QuantumCircuit                            │     │
│  │    ├─ Apply H, T, CX gates                             │     │
│  │    └─ qotp_encrypt(circuit, a_keys, b_keys)           │     │
│  └────────────────────────────────────────────────────────┘     │
│                            │                                      │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ 3. Transpilation (local - no IBM)                      │     │
│  │    └─ transpile(circuit, backend, opt_level)           │     │
│  └────────────────────────────────────────────────────────┘     │
│                            │                                      │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ 4. Export to QASM 3.0 (local - no IBM)                │     │
│  │    └─ qasm3.dumps(circuit) → qasm3_exports/*.qasm      │     │
│  └────────────────────────────────────────────────────────┘     │
│                            │                                      │
│                            ▼                                      │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ 5. IBM Hardware Execution ⚡ (USES IBM API)            │     │
│  │                                                         │     │
│  │    For each error mitigation method:                   │     │
│  │    ┌──────────────────────────────────────────────┐   │     │
│  │    │ Method: Baseline / ZNE / Opt-0 / Opt-3 ...   │   │     │
│  │    │                                               │   │     │
│  │    │ Session(backend=backend):                    │   │     │
│  │    │   ├─ Sampler(session)                        │   │     │
│  │    │   ├─ job = sampler.run(circuit, shots=8192)  │   │     │
│  │    │   │                                           │   │     │
│  │    │   │   ┌───────────────────────────────────┐ │   │     │
│  │    │   │   │ IBM Quantum Backend Execution:    │ │   │     │
│  │    │   │   │                                   │ │   │     │
│  │    │   └───┤ 1. Circuit queued                │ │   │     │
│  │    │       │ 2. Executed on real quantum HW   │ │   │     │
│  │    │       │ 3. Measurements collected        │ │   │     │
│  │    │       │ 4. Results returned              │ │   │     │
│  │    │       └───────────────────────────────────┘ │   │     │
│  │    │                                               │   │     │
│  │    │   └─ result = job.result()                  │   │     │
│  │    │       ├─ quasi_dists (probability dist)     │   │     │
│  │    │       └─ counts (measurement outcomes)      │   │     │
│  │    └──────────────────────────────────────────────┘   │     │
│  └────────────────────────────────────────────────────────┘     │
│                            │                                      │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ 6. Post-Processing (local - no IBM)                    │     │
│  │    ├─ aux_eval(circuit, eval_key)                      │     │
│  │    ├─ qotp_decrypt(circuit, final_enc_a, final_enc_b) │     │
│  │    ├─ Fidelity calculation                             │     │
│  │    └─ TVD calculation                                  │     │
│  └────────────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────────┘
                             │
                             ▼

Step 4: Results Aggregation
┌──────────────────────────────────────────────────────────────────┐
│  Save Results:                                                    │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ • ibm_noise_measurement_results_TIMESTAMP.csv          │     │
│  │ • ibm_noise_measurement_results_TIMESTAMP.json         │     │
│  │ • qasm3_exports/*.qasm (36 files)                      │     │
│  │ • ibm_noise_measurement_analysis.png                   │     │
│  └────────────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🔐 Account Authentication Details

### Where Tokens Are Used:

```python
# Step 1: Load account (uses token from JSON)
service = QiskitRuntimeService()
    ↓
Reads: ~/.qiskit/qiskit-ibm.json
    ↓
{
  "default-ibm-quantum": {
    "channel": "ibm_quantum",
    "token": "7ab345d5b6de1328b915c2bbed0e422f...",  ← Used here
    "url": "https://auth.quantum.ibm.com/api"
  }
}
    ↓
# Authenticates with IBM Quantum API
HTTP Header: Authorization: Bearer 7ab345d5b6de1328b915c2bbed0e422f...
```

### API Endpoints Called:

1. **Authentication:**
   - `https://auth.quantum.ibm.com/api/users/loginWithToken`
   - Headers: `{"X-Qx-Access-Token": "YOUR_TOKEN"}`

2. **Backend List:**
   - `https://api.quantum.ibm.com/runtime/backends`

3. **Backend Info:**
   - `https://api.quantum.ibm.com/runtime/backends/{backend_name}`

4. **Job Submission:**
   - `https://api.quantum.ibm.com/runtime/jobs`
   - POST with circuit data, transpiled QASM

5. **Job Status:**
   - `https://api.quantum.ibm.com/runtime/jobs/{job_id}`

6. **Job Results:**
   - `https://api.quantum.ibm.com/runtime/jobs/{job_id}/results`

---

## 🎯 Code Location Reference

### Where IBM Account is Used:

| File | Line | Purpose |
|------|------|---------|
| `ibm_hardware_noise_experiment.py` | 343 | Load IBM account |
| `ibm_hardware_noise_experiment.py` | 354 | Get backend |
| `ibm_hardware_noise_experiment.py` | 215-222 | Execute circuit (Session) |
| `ibm_hardware_noise_experiment.py` | 72-79 | ZNE execution (Session) |

### Detailed Code:

**Account Loading (Line 340-349):**
```python
# Load IBM Quantum account
print("\n🔐 Loading IBM Quantum account...")
try:
    service = QiskitRuntimeService()  # ← Loads from ~/.qiskit/qiskit-ibm.json
    print(f"   ✅ Account loaded successfully")
except Exception as e:
    print(f"   ❌ Error loading account: {e}")
    return None
```

**Backend Selection (Line 350-364):**
```python
# Get backend
print(f"\n🖥️  Getting backend: {backend_name}")
try:
    backend = service.backend(backend_name)  # ← Uses loaded account
    print(f"   ✅ Backend: {backend.name}")
    print(f"      Status: {backend.status().status_msg}")
    print(f"      Queue: {backend.status().pending_jobs} jobs")
except Exception as e:
    print(f"   ❌ Error accessing backend: {e}")
```

**Circuit Execution (Line 215-222):**
```python
with Session(backend=backend) as session:  # ← Uses authenticated backend
    sampler = Sampler(session=session)
    job = sampler.run(qc_transpiled, shots=shots)  # ← Submits to IBM
    result = job.result()  # ← Retrieves from IBM

    quasi_dist = result.quasi_dists[0]
    counts = {format(k, f'0{num_qubits}b'): int(v * shots)
             for k, v in quasi_dist.items()}
```

---

## 📊 Data Flow: Local vs IBM Cloud

### Local Operations (No IBM API calls):
- ✅ Key generation (`aux_keygen`)
- ✅ Circuit construction (`QuantumCircuit`)
- ✅ QOTP encryption (`qotp_encrypt`)
- ✅ Transpilation (`transpile`)
- ✅ QASM export (`qasm3.dumps`)
- ✅ Homomorphic evaluation (`aux_eval`)
- ✅ QOTP decryption (`qotp_decrypt`)
- ✅ Fidelity calculation
- ✅ Results saving

### IBM Cloud Operations (Requires IBM account):
- 🌐 Account authentication
- 🌐 Backend listing
- 🌐 Backend status check
- 🌐 **Circuit execution** (main IBM usage)
- 🌐 Job status polling
- 🌐 Results retrieval

---

## ⚡ IBM Hardware Execution Details

### What Gets Sent to IBM:

1. **Transpiled Circuit:**
   - QASM representation
   - Gate-level instructions
   - Qubit mappings

2. **Execution Parameters:**
   - `shots=8192` (measurement repetitions)
   - Optimization level metadata
   - Backend selection

3. **Authentication:**
   - API token from `~/.qiskit/qiskit-ibm.json`
   - Account credentials

### What IBM Returns:

1. **Measurement Counts:**
   ```python
   {
     '000': 1024,
     '001': 512,
     '010': 256,
     ...
   }
   ```

2. **Quasi-Distributions:**
   ```python
   {
     0: 0.125,  # |000⟩
     1: 0.0625, # |001⟩
     2: 0.03125, # |010⟩
     ...
   }
   ```

3. **Metadata:**
   - Execution time
   - Queue time
   - Backend info
   - Job ID

---

## 🔧 Account Selection Options

### Default (Current Implementation):

```python
# Uses first available or default account
service = QiskitRuntimeService()
```

### Specify Account Name:

```python
# Use specific account
service = QiskitRuntimeService(name='default-ibm-quantum')
```

### Specify Channel:

```python
# Use IBM Quantum channel
service = QiskitRuntimeService(channel='ibm_quantum')

# Use IBM Cloud channel
service = QiskitRuntimeService(channel='ibm_cloud')
```

---

## 📈 Full Experiment Flow

```
User runs: python ibm_hardware_noise_experiment.py
                        │
                        ▼
          ┌─────────────────────────────┐
          │ Load IBM Account            │ ← ~/.qiskit/qiskit-ibm.json
          │ QiskitRuntimeService()      │
          └─────────────────────────────┘
                        │
                        ▼
          ┌─────────────────────────────┐
          │ Connect to Backend          │ ← IBM API call
          │ service.backend('ibm_...')  │
          └─────────────────────────────┘
                        │
                        ▼
     ┌──────────────────────────────────────────┐
     │ For each config (3q-2t, 4q-2t, 5q-2t,   │
     │                  3q-3t, 4q-3t, 5q-3t):   │
     │                                           │
     │  For each method (Baseline, ZNE, ...):   │
     │                                           │
     │    ┌─────────────────────────────────┐  │
     │    │ 1. Local: Key generation        │  │
     │    │ 2. Local: Circuit creation      │  │
     │    │ 3. Local: QOTP encryption       │  │
     │    │ 4. Local: Transpilation         │  │
     │    │ 5. Local: QASM 3 export         │  │
     │    │ 6. IBM:   Circuit execution ⚡   │  │ ← IBM API call
     │    │ 7. Local: Post-processing       │  │
     │    │ 8. Local: Fidelity/TVD calc     │  │
     │    └─────────────────────────────────┘  │
     │                                           │
     └──────────────────────────────────────────┘
                        │
                        ▼
          ┌─────────────────────────────┐
          │ Save Results                 │
          │ - CSV (36 rows)              │
          │ - JSON (36 entries)          │
          │ - QASM files (36 files)      │
          └─────────────────────────────┘
```

---

## 🎯 Summary

### IBM Account is Used For:

1. ✅ **Authentication** - Validates access to IBM Quantum
2. ✅ **Backend Access** - Lists and selects quantum computers
3. ✅ **Circuit Execution** - Runs circuits on real quantum hardware
4. ✅ **Results Retrieval** - Gets measurement outcomes

### IBM Account is NOT Used For:

1. ❌ Key generation (local)
2. ❌ Circuit construction (local)
3. ❌ QOTP encryption/decryption (local)
4. ❌ Homomorphic evaluation (local)
5. ❌ QASM export (local)
6. ❌ Analysis/visualization (local)

### Your Setup:

✅ **7 accounts configured** and ready
✅ **Automatic loading** - no code changes needed
✅ **Secure storage** - tokens in `~/.qiskit/qiskit-ibm.json`
✅ **Ready to execute** - just run the script!

---

**Your IBM Quantum accounts are integrated and ready for AUX-QHE hardware execution!** 🚀
