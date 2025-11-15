# 🚀 IBM Quantum Hardware Deployment Guide

**Purpose:** Step-by-step guide for deploying quantum algorithms on IBM Quantum hardware
**Based on:** AUX-QHE hardware execution experience (Oct 2024)
**Target Audience:** Researchers deploying quantum cryptography/algorithms on NISQ devices

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Account Setup](#account-setup)
3. [Code Structure Template](#code-structure-template)
4. [Error Mitigation Strategies](#error-mitigation-strategies)
5. [Common Pitfalls & Solutions](#common-pitfalls--solutions)
6. [Performance Optimization](#performance-optimization)
7. [Data Collection & Analysis](#data-collection--analysis)
8. [Troubleshooting](#troubleshooting)

---

## 1. Prerequisites

### Required Python Packages

```bash
# Create virtual environment
python3 -m venv my_qiskitenv
source my_qiskitenv/bin/activate

# Install Qiskit and IBM Runtime
pip install qiskit>=1.0.0
pip install qiskit-ibm-runtime>=0.15.0
pip install numpy pandas matplotlib

# Optional: For error mitigation
pip install qiskit-aer  # Local simulation
```

### IBM Quantum Account

1. Create account at: https://quantum.ibm.com/
2. Get API token from: Account Settings → API Token
3. Note your plan type (Free/Open/Premium)

---

## 2. Account Setup

### One-Time Authentication Setup

```python
from qiskit_ibm_runtime import QiskitRuntimeService

# Save credentials (only needed once)
QiskitRuntimeService.save_account(
    channel='ibm_quantum',
    token='YOUR_IBM_QUANTUM_TOKEN_HERE',
    overwrite=True  # Use if updating token
)

print("✅ Account saved successfully!")
```

### Verify Account Access

```python
from qiskit_ibm_runtime import QiskitRuntimeService

# Load saved account
service = QiskitRuntimeService()

# List available backends
print("Available backends:")
for backend in service.backends():
    print(f"  - {backend.name}: {backend.num_qubits} qubits")
```

---

## 3. Code Structure Template

### Basic Template for Hardware Execution

```python
#!/usr/bin/env python3
"""
Template: IBM Quantum Hardware Execution
Modify this template for your specific algorithm
"""

import sys
import time
import json
from datetime import datetime
import numpy as np
from pathlib import Path

# Qiskit imports
from qiskit import QuantumCircuit, transpile, qasm3
from qiskit.quantum_info import Statevector, state_fidelity
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler

def run_on_ibm_hardware(circuit, backend_name='ibm_brisbane',
                        optimization_level=1, shots=1024):
    """
    Execute quantum circuit on IBM hardware.

    Args:
        circuit: QuantumCircuit to execute
        backend_name: IBM backend name
        optimization_level: 0, 1, 2, or 3
        shots: Number of measurement shots

    Returns:
        dict with results
    """
    print(f"\n{'='*80}")
    print(f"🚀 Executing on IBM Hardware: {backend_name}")
    print(f"{'='*80}")

    start_time = time.time()

    # Step 1: Load IBM account
    print("🔐 Loading IBM Quantum account...")
    service = QiskitRuntimeService()
    backend = service.backend(backend_name)

    print(f"✅ Backend: {backend.name}")
    print(f"   Status: {backend.status().status_msg}")
    print(f"   Queue: {backend.status().pending_jobs} jobs")

    # Step 2: Transpile circuit
    print(f"\n⚙️  Transpiling circuit (opt_level={optimization_level})...")
    transpile_start = time.time()

    qc_transpiled = transpile(
        circuit,
        backend=backend,
        optimization_level=optimization_level,
        seed_transpiler=42  # For reproducibility
    )

    # Add measurements if not present
    if not any(inst.operation.name == 'measure' for inst in qc_transpiled.data):
        qc_transpiled.measure_all()

    transpile_time = time.time() - transpile_start

    print(f"✅ Transpilation complete: {transpile_time:.3f}s")
    print(f"   Circuit depth: {qc_transpiled.depth()}")
    print(f"   Circuit gates: {qc_transpiled.size()}")
    print(f"   Qubits used: {qc_transpiled.num_qubits}")

    # Step 3: Export to QASM (optional, for debugging)
    qasm_dir = Path("qasm_exports")
    qasm_dir.mkdir(exist_ok=True)
    qasm_file = qasm_dir / f"circuit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.qasm"

    try:
        qasm_str = qasm3.dumps(qc_transpiled)
        with open(qasm_file, 'w') as f:
            f.write(qasm_str)
        print(f"📝 QASM exported to: {qasm_file}")
    except Exception as e:
        print(f"⚠️  QASM export failed: {e}")

    # Step 4: Execute on hardware
    print(f"\n🚀 Submitting job to IBM hardware...")
    exec_start = time.time()

    sampler = Sampler(mode=backend)
    job = sampler.run([qc_transpiled], shots=shots)

    print(f"   Job ID: {job.job_id()}")
    print(f"   Waiting for results...")

    result = job.result()
    exec_time = time.time() - exec_start

    print(f"✅ Execution complete: {exec_time:.3f}s")

    # Step 5: Extract results
    counts = result[0].data.meas.get_counts()

    print(f"\n📊 Results:")
    print(f"   Total counts: {sum(counts.values())}")
    print(f"   Unique outcomes: {len(counts)}")
    print(f"   Top 5 outcomes:")
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    for bitstring, count in sorted_counts[:5]:
        prob = count / shots
        print(f"      {bitstring}: {count} ({prob*100:.1f}%)")

    total_time = time.time() - start_time

    return {
        'backend': backend_name,
        'optimization_level': optimization_level,
        'shots': shots,
        'circuit_depth': qc_transpiled.depth(),
        'circuit_gates': qc_transpiled.size(),
        'transpile_time': transpile_time,
        'exec_time': exec_time,
        'total_time': total_time,
        'counts': counts,
        'job_id': job.job_id()
    }


# Example usage
if __name__ == "__main__":
    # Create simple test circuit
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(1, 2)
    qc.t(0)
    qc.t(1)

    # Run on IBM hardware
    results = run_on_ibm_hardware(
        circuit=qc,
        backend_name='ibm_brisbane',
        optimization_level=1,
        shots=1024
    )

    # Save results
    with open('hardware_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("\n✅ Execution complete!")
```

---

## 4. Error Mitigation Strategies

### Strategy 1: Baseline (No Mitigation)

**When to use:** Small circuits (<100 gates), understanding raw hardware performance

```python
results = run_on_ibm_hardware(
    circuit=qc,
    optimization_level=1,  # Minimal optimization
    shots=1024
)
```

**Pros:**
- Fastest execution
- Most predictable
- Best for small circuits

**Cons:**
- No error correction
- Worst fidelity for large circuits

---

### Strategy 2: Circuit Optimization (Opt-3)

**When to use:** Large circuits (>500 gates), CNOT-heavy algorithms

```python
results = run_on_ibm_hardware(
    circuit=qc,
    optimization_level=3,  # Aggressive optimization
    shots=1024
)
```

**Pros:**
- Reduces gate count
- Shorter circuit depth
- Better for routing-constrained circuits

**Cons:**
- May use worse qubits
- Longer transpilation time
- Can introduce more per-gate errors

**⚠️ Warning:** For circuits <200 gates, Opt-3 may DEGRADE fidelity (see AUX-QHE findings)

---

### Strategy 3: Zero-Noise Extrapolation (ZNE)

**When to use:** Circuits <50 gates, linear noise assumptions valid

```python
def apply_zne(circuit, backend, noise_factors=[1, 2, 3], shots=1024):
    """
    Apply ZNE error mitigation.

    WARNING: Only effective for small circuits (<50 gates)!
    For larger circuits, noise becomes non-linear and ZNE FAILS.
    """
    print(f"🔬 Applying ZNE with noise factors: {noise_factors}")

    results = []
    service = QiskitRuntimeService()
    backend_obj = service.backend(backend)

    for factor in noise_factors:
        if factor == 1:
            scaled_circuit = circuit
        else:
            # Gate folding
            scaled_circuit = circuit.copy()
            for _ in range(factor - 1):
                for inst in circuit.data:
                    if inst.operation.name not in ['measure', 'barrier']:
                        gate = inst.operation
                        qubits = inst.qubits
                        scaled_circuit.append(gate, qubits)
                        scaled_circuit.append(gate.inverse(), qubits)

        # Transpile and execute
        transpiled = transpile(scaled_circuit, backend_obj, optimization_level=1)
        transpiled.measure_all()

        sampler = Sampler(mode=backend_obj)
        job = sampler.run([transpiled], shots=shots)
        result = job.result()

        counts = result[0].data.meas.get_counts()
        results.append(counts)

    # Richardson extrapolation
    extrapolated = {}
    for bitstring in results[0].keys():
        probs = [r.get(bitstring, 0.0) / shots for r in results]

        # Linear extrapolation: p(0) ≈ 2*p(1) - p(2)
        p_extrap = max(0, min(1, 2*probs[0] - probs[1]))
        extrapolated[bitstring] = p_extrap

    # Renormalize
    total = sum(extrapolated.values())
    if total > 0:
        extrapolated = {k: v/total for k, v in extrapolated.items()}

    return extrapolated
```

**Pros:**
- Can improve fidelity for small circuits
- Well-studied technique

**Cons:**
- **FAILS for circuits >50 gates** (non-linear noise)
- Requires 3x more shots (higher cost)
- Assumes linear noise (often violated)

**⚠️ Critical:** AUX-QHE showed ZNE DEGRADES fidelity for 170-gate circuits!

---

### Strategy 4: Combined (Opt-3 + ZNE)

**When to use:** Medium circuits (100-200 gates), have extra credits for ZNE

```python
# First optimize
qc_opt = transpile(circuit, backend, optimization_level=3)

# Then apply ZNE
results = apply_zne(qc_opt, backend, shots=1024)
```

**⚠️ Warning:** This can make things WORSE if:
- Circuit already small (<200 gates)
- Queue is congested (gets bad qubits)
- Noise is non-linear

---

## 5. Common Pitfalls & Solutions

### Pitfall 1: Recording Circuit Metrics for ZNE ❌

**WRONG:**
```python
qc_transpiled = transpile(circuit, backend, opt_level=1)
circuit_depth = qc_transpiled.depth()  # ← Recorded BEFORE ZNE

if use_zne:
    results = apply_zne(qc_transpiled, backend)  # ← But ZNE changes depth!
```

**Correct:**
```python
qc_transpiled = transpile(circuit, backend, opt_level=1)

if use_zne:
    # ZNE runs 3 circuits with different depths - don't record single depth
    results = apply_zne(qc_transpiled, backend)
    circuit_depth = "Variable (ZNE 1x-3x)"
else:
    circuit_depth = qc_transpiled.depth()
    results = execute_normal(qc_transpiled)
```

---

### Pitfall 2: Not Adding Measurements ❌

**WRONG:**
```python
qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
# Missing: qc.measure_all()

sampler.run([qc])  # ← ERROR: No measurements!
```

**Correct:**
```python
qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()  # ← Add measurements

sampler.run([qc])
```

---

### Pitfall 3: Using Sessions on Free Plan ❌

**WRONG:**
```python
# Sessions NOT supported on free plan!
with Session(service=service, backend=backend) as session:
    sampler = Sampler(session=session)  # ← ERROR
```

**Correct:**
```python
# Use Sampler without Session for free/open plan
sampler = Sampler(mode=backend)
job = sampler.run([circuit], shots=1024)
```

---

### Pitfall 4: Ignoring Queue Congestion ⚠️

**Problem:**
- Queue with 3,000+ jobs → wait times >30 minutes
- May get allocated to worse qubits

**Solution:**
```python
backend = service.backend('ibm_brisbane')
status = backend.status()

print(f"Queue: {status.pending_jobs} jobs")

if status.pending_jobs > 2000:
    print("⚠️  Warning: High queue congestion!")
    print("   Consider using different backend or waiting")

    # Try alternative backend
    alternatives = ['ibm_kyoto', 'ibm_osaka', 'ibm_sherbrooke']
    for alt in alternatives:
        try:
            alt_backend = service.backend(alt)
            alt_queue = alt_backend.status().pending_jobs
            print(f"   {alt}: {alt_queue} jobs")
            if alt_queue < status.pending_jobs / 2:
                print(f"   ✅ Recommend switching to {alt}")
                break
        except:
            continue
```

---

### Pitfall 5: Not Handling Different Key Types from get_counts() ❌

**Problem:** IBM returns counts as dict with either string or int keys

**WRONG:**
```python
counts = result[0].data.meas.get_counts()
for bitstring, count in counts.items():
    # Assumes bitstring is string
    idx = int(bitstring, 2)  # ← ERROR if bitstring is int!
```

**Correct:**
```python
counts = result[0].data.meas.get_counts()

# Convert to consistent format
formatted_counts = {}
for k, v in counts.items():
    if isinstance(k, str):
        bitstring = k
    else:
        bitstring = format(int(k), f'0{num_qubits}b')
    formatted_counts[bitstring] = v
```

---

## 6. Performance Optimization

### Optimization 1: Reduce Shots for Testing

```python
# Development/testing: 100-500 shots
results_dev = run_on_ibm_hardware(circuit, shots=100)

# Production: 1024-8192 shots
results_prod = run_on_ibm_hardware(circuit, shots=1024)
```

**Tradeoff:**
- 100 shots: ~±10% statistical error, 10x faster
- 1024 shots: ~±3% error
- 8192 shots: ~±1% error, 8x slower

---

### Optimization 2: Batch Multiple Circuits

```python
# Instead of running circuits one-by-one
sampler = Sampler(mode=backend)

# Run multiple circuits in one job
circuits = [qc1, qc2, qc3]
job = sampler.run(circuits, shots=1024)

results = job.result()
for i, circuit_result in enumerate(results):
    print(f"Circuit {i}: {circuit_result.data.meas.get_counts()}")
```

**Benefit:** Reduces queue wait time (one wait instead of N)

---

### Optimization 3: Save Intermediate Results

```python
import json
from datetime import datetime

def save_interim_results(results, filename=None):
    """Save results after each experiment to avoid data loss."""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"interim_results_{timestamp}.json"

    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"💾 Interim results saved: {filename}")

# Use in your experiment loop
all_results = []
for config in configurations:
    result = run_on_ibm_hardware(circuit, ...)
    all_results.append(result)

    # Save after each iteration
    save_interim_results(all_results)
```

**Benefit:** If job fails mid-experiment, you don't lose all data

---

## 7. Data Collection & Analysis

### Template: Comprehensive Results Collection

```python
def run_comprehensive_experiment(circuit, backend_name='ibm_brisbane'):
    """
    Run experiment with all error mitigation strategies.
    Returns complete dataset for analysis.
    """

    methods = [
        {'name': 'Baseline', 'opt_level': 1, 'use_zne': False},
        {'name': 'Opt-3', 'opt_level': 3, 'use_zne': False},
        {'name': 'ZNE', 'opt_level': 1, 'use_zne': True},
        {'name': 'Opt-3+ZNE', 'opt_level': 3, 'use_zne': True},
    ]

    results = []

    for method in methods:
        print(f"\n{'='*80}")
        print(f"Running: {method['name']}")
        print(f"{'='*80}")

        try:
            if method['use_zne']:
                # ZNE path
                service = QiskitRuntimeService()
                backend = service.backend(backend_name)
                qc_trans = transpile(circuit, backend,
                                    optimization_level=method['opt_level'])
                counts = apply_zne(qc_trans, backend_name)

                result = {
                    'method': method['name'],
                    'optimization_level': method['opt_level'],
                    'zne_applied': True,
                    'counts': counts,
                    'circuit_depth': 'Variable (ZNE)',
                    'circuit_gates': 'Variable (ZNE)'
                }
            else:
                # Regular path
                result = run_on_ibm_hardware(
                    circuit,
                    backend_name=backend_name,
                    optimization_level=method['opt_level'],
                    shots=1024
                )
                result['method'] = method['name']
                result['zne_applied'] = False

            results.append(result)

            # Save interim
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            with open(f'interim_{timestamp}.json', 'w') as f:
                json.dump(results, f, indent=2)

        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            continue

    return results
```

---

### Template: Results Analysis

```python
import pandas as pd
import matplotlib.pyplot as plt

def analyze_results(results_file):
    """Analyze hardware execution results."""

    with open(results_file, 'r') as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    print("📊 Results Summary:")
    print("="*80)
    print(df[['method', 'circuit_depth', 'circuit_gates', 'exec_time']])

    # Compare execution times
    print("\n⏱️  Execution Time Comparison:")
    for _, row in df.iterrows():
        print(f"  {row['method']:<15}: {row['exec_time']:.1f}s")

    # Plot fidelity comparison (if you computed fidelity)
    if 'fidelity' in df.columns:
        plt.figure(figsize=(10, 6))
        plt.bar(df['method'], df['fidelity'])
        plt.xlabel('Method')
        plt.ylabel('Fidelity')
        plt.title('Hardware Fidelity Comparison')
        plt.ylim([0, 1])
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('fidelity_comparison.png')
        print("\n📈 Plot saved: fidelity_comparison.png")

    return df
```

---

## 8. Troubleshooting

### Issue 1: "Account not found"

**Error:**
```
AccountNotFoundError: No IBM Quantum account found
```

**Solution:**
```python
from qiskit_ibm_runtime import QiskitRuntimeService

QiskitRuntimeService.save_account(
    channel='ibm_quantum',
    token='YOUR_TOKEN',
    overwrite=True
)
```

---

### Issue 2: Job stuck in queue for >1 hour

**Symptoms:** Job shows "QUEUED" status indefinitely

**Solutions:**

```python
# Check job status
job = service.job('JOB_ID_HERE')
print(f"Status: {job.status()}")
print(f"Queue position: {job.queue_position()}")

# If stuck, cancel and retry with different backend
job.cancel()

# Try less-congested backend
backends = service.backends()
for b in sorted(backends, key=lambda x: x.status().pending_jobs):
    print(f"{b.name}: {b.status().pending_jobs} jobs")
```

---

### Issue 3: Circuit too large for transpilation

**Error:**
```
TranspilerError: Circuit requires more qubits than backend has
```

**Solutions:**

1. **Reduce circuit size:**
```python
# Check circuit requirements
print(f"Circuit needs: {qc.num_qubits} qubits")
print(f"Backend has: {backend.num_qubits} qubits")
```

2. **Use larger backend:**
```python
# Switch to larger backend
large_backends = [b for b in service.backends() if b.num_qubits >= qc.num_qubits]
print(f"Compatible backends: {[b.name for b in large_backends]}")
```

---

### Issue 4: Low fidelity results

**Symptoms:** Fidelity <0.1 on hardware

**Diagnostic checklist:**

```python
# 1. Check circuit size
print(f"Circuit depth: {qc.depth()}")
print(f"Circuit gates: {qc.size()}")
print(f"T-gates: {sum(1 for inst in qc.data if inst.operation.name == 't')}")

# Rule of thumb for NISQ:
# - Depth >20: Expect fidelity <0.5
# - Depth >50: Expect fidelity <0.1
# - Depth >100: Expect fidelity <0.05

# 2. Check backend quality
props = backend.properties()
avg_t1 = np.mean([props.qubit_property(i).t1 for i in range(backend.num_qubits)])
avg_t2 = np.mean([props.qubit_property(i).t2 for i in range(backend.num_qubits)])

print(f"Backend coherence: T1={avg_t1*1e6:.0f}µs, T2={avg_t2*1e6:.0f}µs")

# 3. Check if circuit exceeds coherence time
gate_time = 100e-9  # 100ns typical
circuit_time = qc.size() * gate_time

print(f"Estimated circuit time: {circuit_time*1e6:.1f}µs")
print(f"Coherence time: {avg_t2*1e6:.0f}µs")
print(f"Ratio: {circuit_time/avg_t2*100:.1f}%")

if circuit_time / avg_t2 > 0.2:
    print("⚠️  Circuit time >20% of coherence time - expect low fidelity!")
```

---

## 📚 Additional Resources

### Official Documentation

- **Qiskit Documentation:** https://docs.quantum.ibm.com/
- **IBM Quantum Platform:** https://quantum.ibm.com/
- **Qiskit Runtime API:** https://docs.quantum.ibm.com/api/qiskit-ibm-runtime

### Best Practices

1. **Always test locally first:**
```python
from qiskit_aer import Aer

# Simulate locally before hardware
simulator = Aer.get_backend('qasm_simulator')
qc_sim = transpile(circuit, simulator)
result = simulator.run(qc_sim).result()
```

2. **Start small, scale up:**
- Test with 2-3 qubits first
- Gradually increase to target size
- Monitor fidelity degradation

3. **Track costs:**
```python
# Check plan limits
service = QiskitRuntimeService()
print(f"Plan: {service.active_account()['plan']}")

# Track job runtime
total_runtime = sum([r['exec_time'] for r in results])
print(f"Total runtime used: {total_runtime:.0f}s")
```

---

## 🎯 Quick Start Checklist

Before running on IBM hardware:

- [ ] IBM account setup with API token saved
- [ ] Virtual environment activated
- [ ] Circuit tested locally (qasm_simulator)
- [ ] Circuit has measurements (measure_all())
- [ ] Choose appropriate optimization level
- [ ] Decide on shot count (100 dev, 1024 prod)
- [ ] Check backend queue status
- [ ] Set up interim result saving
- [ ] Have error handling for job failures

---

## 📊 Expected Performance (Based on AUX-QHE Experience)

| Circuit Size | Depth | Gates | Expected Fidelity | Recommended Method |
|-------------|-------|-------|-------------------|-------------------|
| Small | <20 | <100 | 0.3-0.8 | Baseline or ZNE |
| Medium | 20-50 | 100-300 | 0.1-0.3 | Opt-3 (maybe) |
| Large | >50 | >300 | <0.1 | ⚠️ May not work on NISQ |

**Critical Findings from AUX-QHE:**
- 170-gate circuit: 0.03 fidelity (96.5% degradation)
- Baseline often better than Opt-3 for <200 gates
- ZNE fails for >50 gates (non-linear noise)
- Queue congestion significantly impacts results

---

**Generated:** 2025-10-24
**Based on:** AUX-QHE IBM hardware deployment experience
**Status:** ✅ Production-ready guide
