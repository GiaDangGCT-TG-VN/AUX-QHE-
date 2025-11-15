# Quick Start - Hardware Execution

## ✅ STATUS: READY TO EXECUTE

All validations passed. No bugs detected.

---

## 🚀 EXECUTE NOW

```bash
cd /Users/giadang/my_qiskitenv/AUX-QHE
./EXECUTE_5Q_2T.sh
```

**OR**

```bash
cd /Users/giadang/my_qiskitenv && source bin/activate && cd AUX-QHE
python ibm_hardware_noise_experiment.py --config 5q-2t --backend ibm_torino --account Gia_AUX_QHE
```

---

## ⏱️ EXPECTED RUNTIME

- **Queue wait**: ~20-40 minutes (421 jobs ahead)
- **Execution**: ~15-20 minutes
- **Total**: ~35-60 minutes

---

## 💰 CREDITS

~8 credits per configuration

---

## 🎯 SUCCESS INDICATORS

**ZNE Method** (Critical test):
- ✅ No `sxdg` errors
- ✅ Gates ~500-600 (not ~160)
- ✅ Depth ~60-100 (not ~22)
- ✅ Fidelity >4.2% (not ~3%)

---

## ❌ FAILURE INDICATORS

Stop if:
- ❌ `sxdg` error appears
- ❌ ZNE gates = Baseline gates
- ❌ ZNE fidelity < Baseline fidelity

---

## 📊 EXPECTED RESULTS

| Method | Fidelity | Gates | Depth |
|--------|----------|-------|-------|
| Baseline | ~2.94% | ~162 | ~22 |
| **ZNE** | **~4.6%** | **~500** | **~100** |
| Opt-3 | ~3.12% | ~155 | ~20 |
| Opt-3+ZNE | ~4.8% | ~500 | ~95 |

---

## 📁 OUTPUT FILES

- `ibm_noise_measurement_results_{timestamp}.csv`
- `ibm_noise_measurement_results_{timestamp}.json`
- `qasm3_exports/5q-2t_*.qasm`

---

## 📖 FULL DOCS

- Detailed report: [FINAL_PRE_EXECUTION_REPORT.md](FINAL_PRE_EXECUTION_REPORT.md)
- Debug summary: [DEBUG_SUMMARY_2025_10_27.md](DEBUG_SUMMARY_2025_10_27.md)
- Test suite: `comprehensive_pre_execution_debug.py`

---

## 🆘 TROUBLESHOOTING

**Backend issues?**
```bash
python -c "from qiskit_ibm_runtime import QiskitRuntimeService; s=QiskitRuntimeService(name='Gia_AUX_QHE'); b=s.backend('ibm_torino'); print(b.status())"
```

**Partial results?**
```bash
ls -lt ibm_noise_results_interim_*.json | head -1
```

---

**Last Validated**: 2025-10-27
**Confidence**: 🟢 100%
**Status**: ✅ CLEARED FOR EXECUTION
