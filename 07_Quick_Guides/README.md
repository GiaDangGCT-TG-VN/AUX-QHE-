# 07. Quick Start Guides

**Purpose:** Quick reference and troubleshooting

## 🚀 Files

- **QUICK_START_GUIDE.md** - Quick start
  - Installation
  - First run
  - Basic usage

- **QUICK_START_TESTING.md** - Quick testing
  - Run tests
  - Verify results
  - Common issues

- **TROUBLESHOOTING_IBM_EXPERIMENT.md** - Troubleshooting
  - Common errors
  - Solutions
  - Debug steps

- **QUEUE_MANAGEMENT_GUIDE.md** - Queue management
  - Check queue status
  - Estimate wait time
  - Priority tips

- **QASM_VERSION_EXPLAINED.md** - QASM versions
  - OpenQASM 2.0 vs 3.0
  - Compatibility
  - Migration guide

## 🎯 Quick Commands

**Run test:**
```bash
python test_local_full_pipeline.py
```

**Run on IBM:**
```bash
python ibm_hardware_noise_experiment.py --config 5q-2t --shots 1024
```

**Check queue:**
```bash
python -c "from qiskit_ibm_runtime import QiskitRuntimeService; print(QiskitRuntimeService().backend('ibm_brisbane').status())"
```

---

**Total Files:** 5
**Total Size:** ~30 KB
