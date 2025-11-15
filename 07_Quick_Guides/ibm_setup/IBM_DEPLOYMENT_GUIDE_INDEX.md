# 📍 IBM Hardware Deployment Guides - Quick Index

**Location:** `IBM_Hardware_Deployment_Guides/`
**Total Size:** ~50 KB (43+ pages)
**Status:** ✅ Complete & Production-Ready

---

## 📂 Folder Contents

```
IBM_Hardware_Deployment_Guides/
├── README.md (10 KB)
│   └── Master index with usage scenarios
│
├── IBM_HARDWARE_DEPLOYMENT_GUIDE.md (22 KB)
│   └── Main reference guide (27 pages)
│   └── Sections:
│       1. Prerequisites
│       2. Account Setup
│       3. Code Structure Template ⭐
│       4. Error Mitigation Strategies
│       5. Common Pitfalls & Solutions
│       6. Performance Optimization
│       7. Data Collection & Analysis
│       8. Troubleshooting
│
├── IBM_HARDWARE_QUICK_REFERENCE.md (3.4 KB)
│   └── One-page cheat sheet ⚡
│   └── Contains:
│       - 5-min quick deploy code
│       - Decision tree
│       - Shot count guide
│       - Common errors
│
└── LESSONS_LEARNED_IBM_DEPLOYMENT.md (14 KB)
    └── Experience report (15 pages)
    └── Sections:
        - 6 Key Findings 🎯
        - 4 Technical Insights
        - What NOT to Do 🚫
        - Best Practices ✅
        - Recommendations
```

---

## ⚡ Quick Navigation

### I need to...

**Deploy my first circuit on IBM hardware:**
→ Read: `IBM_HARDWARE_QUICK_REFERENCE.md` (5 min)
→ Then: `IBM_HARDWARE_DEPLOYMENT_GUIDE.md` Section 3

**Decide which error mitigation to use:**
→ Check: `IBM_HARDWARE_QUICK_REFERENCE.md` Decision Tree
→ Read: `LESSONS_LEARNED_IBM_DEPLOYMENT.md` Findings 1-4

**Debug a failed job:**
→ Check: `IBM_HARDWARE_QUICK_REFERENCE.md` Common Errors
→ Consult: `IBM_HARDWARE_DEPLOYMENT_GUIDE.md` Section 8

**Understand why error mitigation failed:**
→ Read: `LESSONS_LEARNED_IBM_DEPLOYMENT.md` Findings 2-3
→ Details: Parent directory `WHY_ERROR_MITIGATION_FAILED_5Q2T.md`

**Write paper about hardware results:**
→ Read: `LESSONS_LEARNED_IBM_DEPLOYMENT.md` all sections
→ Use data from: `local_vs_hardware_comparison.csv`

**Optimize performance/costs:**
→ Read: `IBM_HARDWARE_DEPLOYMENT_GUIDE.md` Section 6
→ Best practices: `LESSONS_LEARNED_IBM_DEPLOYMENT.md`

---

## 🎯 Key Findings at a Glance

### 1. Baseline > Error Mitigation (for circuits <200 gates)
- 5q-2t: Baseline 0.035 vs Opt-3 0.028 (-18%) ⚠️

### 2. ZNE Fails for >50 Gates
- 170-gate circuit: ZNE degraded fidelity by 14%

### 3. Shorter Circuit ≠ Better Fidelity
- Opt-3: depth 13, fidelity 0.028
- Baseline: depth 18, fidelity 0.035 ✅

### 4. NISQ Ceiling ~3-4% Fidelity
- All configurations: 96-99% degradation from ideal

### 5. Queue Congestion Matters
- 3,674 jobs → 133s wait vs 5.6s

### 6. Circuit Size Determines Strategy
- <200 gates: Use Baseline
- >500 gates: Maybe Opt-3

---

## 📊 Usage Statistics (From AUX-QHE)

- **Experiments:** 12 (4 methods × 3 configs)
- **Backend:** ibm_brisbane (127 qubits)
- **Total runtime:** ~190 seconds
- **Best fidelity:** 0.035 (5q-2t Baseline)
- **Worst fidelity:** 0.010 (5q-3t)

---

## 🔗 Related Documentation (Parent Directory)

### Analysis Files:
- `WHY_ERROR_MITIGATION_FAILED_5Q2T.md` - Deep dive on ZNE/Opt-3 failures
- `VERIFICATION_5Q2T_FINDINGS.md` - Data verification
- `TABLE_ANOMALY_ANALYSIS.md` - ZNE metric recording issues
- `5Q2T_HARDWARE_TABLE_UPDATE_COMPLETE.md` - Results summary

### Code Files:
- `ibm_hardware_noise_experiment.py` - Production execution script
- `add_5q2t_to_hardware_table.py` - Results processing
- `update_5q2t_hardware_table.py` - Table generation

### Data Files:
- `local_vs_hardware_comparison.csv` - Main results table
- `ibm_noise_measurement_results_*.json` - Raw hardware data

---

## 📞 Support

**For questions about:**
- Setup/Installation → `IBM_HARDWARE_DEPLOYMENT_GUIDE.md` Section 1-2
- Error messages → `IBM_HARDWARE_QUICK_REFERENCE.md` Common Errors
- Performance issues → `LESSONS_LEARNED_IBM_DEPLOYMENT.md` Best Practices
- Unexpected results → `LESSONS_LEARNED_IBM_DEPLOYMENT.md` Key Findings

---

## ✅ Checklist: Ready to Deploy?

Before running on IBM hardware:

- [ ] Read README.md in `IBM_Hardware_Deployment_Guides/`
- [ ] IBM account setup & token saved
- [ ] Circuit tested locally
- [ ] Chosen error mitigation method (usually Baseline)
- [ ] Decided shot count (1024 for production)
- [ ] Checked backend queue status
- [ ] Set up result saving

---

## 🚀 Get Started

```bash
# Navigate to guides folder
cd IBM_Hardware_Deployment_Guides/

# Quick start (5 min)
open IBM_HARDWARE_QUICK_REFERENCE.md

# Comprehensive guide (30 min)
open IBM_HARDWARE_DEPLOYMENT_GUIDE.md

# Learn from experience (15 min)
open LESSONS_LEARNED_IBM_DEPLOYMENT.md
```

---

**Created:** 2024-10-24
**Total Pages:** 43+
**Status:** ✅ Production-ready
**Access:** `cd IBM_Hardware_Deployment_Guides/`
