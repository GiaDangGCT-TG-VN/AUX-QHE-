# 🚀 IBM Quantum Hardware - Quick Reference Card

**One-page cheat sheet for quick deployment**

---

## 🔧 Setup (One-Time)

```bash
# Install
pip install qiskit qiskit-ibm-runtime

# Save credentials
python3 -c "from qiskit_ibm_runtime import QiskitRuntimeService; \
QiskitRuntimeService.save_account(channel='ibm_quantum', token='YOUR_TOKEN')"
```

---

## ⚡ Quick Deploy

```python
from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler

# 1. Load account
service = QiskitRuntimeService()
backend = service.backend('ibm_brisbane')

# 2. Create circuit
qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

# 3. Transpile
qc_t = transpile(qc, backend, optimization_level=1)

# 4. Execute
sampler = Sampler(mode=backend)
job = sampler.run([qc_t], shots=1024)
result = job.result()

# 5. Get counts
counts = result[0].data.meas.get_counts()
print(counts)
```

---

## 📊 Decision Tree: Which Method?

```
Circuit Size?
├─ <50 gates
│  ├─ Use: Baseline (opt_level=1) ✅
│  └─ Maybe: ZNE (if <50 gates)
│
├─ 50-200 gates
│  ├─ Use: Baseline ✅
│  └─ Avoid: Opt-3 (may degrade) ❌
│
└─ >200 gates
   ├─ Try: Opt-3 ⚠️
   └─ Note: Expect <0.1 fidelity
```

---

## ⚙️ Optimization Levels

| Level | Gates | Depth | Use When |
|-------|-------|-------|----------|
| 0 | No change | No change | Debug only |
| 1 | Minimal | Minimal | **Default** ✅ |
| 2 | Medium | Medium | Rarely needed |
| 3 | Heavy | Reduced | >500 gates only |

---

## 🎯 Shot Count Guide

| Shots | Error | Use Case | Time |
|-------|-------|----------|------|
| 100 | ±10% | Testing | Fast |
| 512 | ±4% | Development | Medium |
| 1024 | ±3% | **Production** ✅ | Standard |
| 8192 | ±1% | High precision | 8x slower |

---

## ⚠️ Common Errors

### "No measurements"
```python
qc.measure_all()  # ← Add this!
```

### "Account not found"
```python
QiskitRuntimeService.save_account(channel='ibm_quantum', token='TOKEN')
```

### "Circuit too large"
```python
# Check: qc.num_qubits <= backend.num_qubits
# Use smaller circuit or larger backend
```

---

## 📈 Expected Fidelity (NISQ)

| Depth | Fidelity | Status |
|-------|----------|--------|
| <20 | 0.3-0.8 | ✅ Good |
| 20-50 | 0.1-0.3 | ⚠️ Okay |
| >50 | <0.1 | ❌ Poor |

---

## 🔍 Debug Checklist

```python
# Check circuit
print(f"Qubits: {qc.num_qubits}, Depth: {qc.depth()}, Gates: {qc.size()}")

# Check backend
print(f"Queue: {backend.status().pending_jobs}")

# Check results
print(f"Total counts: {sum(counts.values())}")
```

---

## 💾 Save Results

```python
import json
from datetime import datetime

# Save to file
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
with open(f'results_{timestamp}.json', 'w') as f:
    json.dump({'counts': counts, 'metadata': {...}}, f, indent=2)
```

---

## 🚨 Critical Learnings (AUX-QHE)

1. **Baseline often best for <200 gates** ✅
2. **ZNE fails for >50 gates** ❌
3. **Opt-3 can make things worse** ⚠️
4. **Queue congestion matters** (check pending jobs)
5. **170 gates = 0.03 fidelity** (96.5% degradation)

---

## 📞 Quick Help

```python
# List backends
for b in service.backends():
    print(f"{b.name}: {b.num_qubits}q, {b.status().pending_jobs} jobs")

# Check job status
job = service.job('JOB_ID')
print(job.status())

# Cancel job
job.cancel()
```

---

**Full Guide:** [IBM_HARDWARE_DEPLOYMENT_GUIDE.md](IBM_HARDWARE_DEPLOYMENT_GUIDE.md)
