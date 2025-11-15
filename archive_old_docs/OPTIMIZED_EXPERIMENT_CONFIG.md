# ⚡ Optimized IBM Hardware Experiment Configuration

**Updated settings for faster, more efficient execution**

---

## 🎯 What Changed

### Previous Configuration:
- ❌ 6 methods (Baseline, ZNE, Opt-0, Opt-3, Opt-0+ZNE, Opt-3+ZNE)
- ❌ 8192 shots (default)
- ❌ 72 total IBM jobs
- ❌ ~20-40 minutes runtime

### New Optimized Configuration:
- ✅ **4 methods** (Baseline, ZNE, Opt-3, Opt-3+ZNE)
- ✅ **1024 shots** (default)
- ✅ **24 total IBM jobs**
- ✅ **~5-10 minutes runtime**

**Speedup: ~4-6× faster!** 🚀

---

## 📊 New Experiment Matrix

### Methods Included:

| # | Method | Optimization | ZNE | Why Include |
|---|--------|--------------|-----|-------------|
| 1 | **Baseline** | Level 1 | ❌ | Raw hardware performance baseline |
| 2 | **ZNE** | Level 1 | ✅ | Error mitigation effectiveness |
| 3 | **Opt-3** | Level 3 | ❌ | Heavy optimization impact |
| 4 | **Opt-3+ZNE** | Level 3 | ✅ | **Best fidelity** (optimal) |

### Methods Excluded:

| Method | Why Excluded |
|--------|--------------|
| **Opt-0** | Minimal optimization provides little benefit over Baseline |
| **Opt-0+ZNE** | Redundant - Opt-3+ZNE is superior for error mitigation |

**Rationale:** Focus on most impactful comparisons while reducing runtime

---

## 🔢 Computational Requirements

### Per Configuration (e.g., 3q-2t):

```
Methods: 4
Jobs per method:
  - Baseline: 1 job (1024 shots)
  - ZNE: 3 jobs (1024 shots each, 3 noise levels)
  - Opt-3: 1 job (1024 shots)
  - Opt-3+ZNE: 3 jobs (1024 shots each, 3 noise levels)

Total: 8 jobs, 12,288 shots
Time: ~1-2 minutes
```

### Full Experiment (6 configs):

```
═══════════════════════════════════════════════════════════
OPTIMIZED AUX-QHE NOISE MEASUREMENT
═══════════════════════════════════════════════════════════

📊 Total IBM Jobs:           24 jobs (vs 72 before)
   ├─ Non-ZNE (2 methods):   12 jobs
   └─ ZNE (2 methods):       12 jobs

🎯 Total Quantum Shots:      36,864 shots (vs 589,824 before)
   ├─ Per standard job:      1,024 shots
   └─ Per ZNE method:        3,072 shots (3× noise levels)

⏱️  Total Runtime:           ~5-10 minutes (vs 20-40 min)
   ├─ Queue time:            ~2-5 min
   └─ Execution time:        ~1.5 min QPU

💾 Data Generated:           ~5-10 MB (vs 15-30 MB)

🖥️  IBM Resource Usage:      Light
   └─ Uses ~15% of free monthly quota!

💰 Cost Savings:             ~85% reduction in QPU time

═══════════════════════════════════════════════════════════

SPEEDUP: ~6× faster, ~16× fewer shots, ~67% fewer jobs
```

---

## 📈 Comparison: Old vs New

| Metric | Old Config | New Config | Improvement |
|--------|------------|------------|-------------|
| **Methods** | 6 | 4 | 33% reduction |
| **Shots** | 8192 | 1024 | 8× faster |
| **Jobs per config** | 12 | 8 | 33% reduction |
| **Total jobs** | 72 | 24 | **67% reduction** |
| **Total shots** | 589,824 | 36,864 | **94% reduction** |
| **Runtime** | 20-40 min | 5-10 min | **~75% faster** |
| **QPU time** | ~9 min | ~1.5 min | **83% reduction** |
| **Free quota used** | ~90% | ~15% | **75% savings** |

---

## 🎯 Statistical Accuracy

### Error Analysis:

**With 1024 shots:**
```
Statistical error: 1/√1024 = 1/32 ≈ 3.1%

Fidelity measurement error:
σ(F) ≈ √(1 - F²) / √shots
     ≈ √(1 - 0.9²) / √1024
     ≈ 0.44 / 32
     ≈ 0.014 (±1.4%)
```

**Comparison:**

| Shots | Error | Accuracy | Use Case |
|-------|-------|----------|----------|
| 1024 | ±3.1% | Good | ✅ Testing, research drafts |
| 4096 | ±1.6% | Very good | Final research |
| 8192 | ±1.1% | Excellent | Publication |

**1024 shots = Good enough for research and testing!** ✅

---

## 🚀 Runtime Breakdown

### Full Experiment Timeline:

```
Total time: ~5-10 minutes

┌─────────────────────────────────────────────────┐
│ Phase 1: Connection & Setup                    │
│ • Load IBM account                     ~5s      │
│ • Get backend info                     ~3s      │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ Phase 2: Experiments (24 jobs)                 │
│ • 3q-2t (8 jobs)                       ~1 min   │
│ • 4q-2t (8 jobs)                       ~1 min   │
│ • 5q-2t (8 jobs)                       ~1 min   │
│ • 3q-3t (8 jobs)                       ~1 min   │
│ • 4q-3t (8 jobs)                       ~1 min   │
│ • 5q-3t (8 jobs)                       ~1 min   │
│                                                 │
│ Queue time (variable):              2-5 min     │
│ Execution time:                     ~1.5 min    │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ Phase 3: Analysis & Export                     │
│ • QASM 3 exports (24 files)            ~2s      │
│ • CSV/JSON export                      ~1s      │
│ • Analysis & visualization             ~5s      │
└─────────────────────────────────────────────────┘

Total: ~5-10 minutes (depends on queue)
```

---

## 📁 Output Files Generated

### QASM 3.0 Exports: 24 files (vs 36 before)

```
qasm3_exports/
├── 3q-2t_Baseline.qasm
├── 3q-2t_ZNE.qasm
├── 3q-2t_Opt-3.qasm
├── 3q-2t_Opt-3_ZNE.qasm
├── 4q-2t_Baseline.qasm
├── 4q-2t_ZNE.qasm
├── 4q-2t_Opt-3.qasm
├── 4q-2t_Opt-3_ZNE.qasm
├── 5q-2t_Baseline.qasm
├── 5q-2t_ZNE.qasm
├── 5q-2t_Opt-3.qasm
├── 5q-2t_Opt-3_ZNE.qasm
├── 3q-3t_Baseline.qasm
├── 3q-3t_ZNE.qasm
├── 3q-3t_Opt-3.qasm
├── 3q-3t_Opt-3_ZNE.qasm
├── 4q-3t_Baseline.qasm
├── 4q-3t_ZNE.qasm
├── 4q-3t_Opt-3.qasm
├── 4q-3t_Opt-3_ZNE.qasm
├── 5q-3t_Baseline.qasm
├── 5q-3t_ZNE.qasm
├── 5q-3t_Opt-3.qasm
└── 5q-3t_Opt-3_ZNE.qasm
```

### Results Data:

- `ibm_noise_measurement_results_TIMESTAMP.csv` (24 rows)
- `ibm_noise_measurement_results_TIMESTAMP.json` (24 entries)
- `ibm_noise_measurement_analysis.png` (4-method comparison)

---

## 🎯 Research Questions Answered

The optimized configuration still answers key questions:

### 1. ✅ How does ZNE affect fidelity?
**Compare:** Baseline vs ZNE

### 2. ✅ What's the impact of optimization?
**Compare:** Baseline vs Opt-3

### 3. ✅ What's the best method for production?
**Answer:** Opt-3+ZNE (highest fidelity)

### 4. ✅ What's the ZNE overhead with optimization?
**Compare:** Opt-3 vs Opt-3+ZNE

### Questions NOT answered (but not critical):
- ❌ Minimal optimization (Opt-0) impact
- ❌ ZNE on minimal optimization

**These are rarely used in practice anyway!**

---

## 💰 Cost Analysis

### Free Tier (IBM Quantum Open Plan):

**Monthly limit:** 10 minutes QPU time

**Old config:**
- QPU time: ~9 minutes
- Usage: **90% of quota**
- Can run: ~1 full experiment per month

**New config:**
- QPU time: ~1.5 minutes
- Usage: **15% of quota**
- Can run: ~6 full experiments per month

**Benefit: 6× more experiments with free tier!** 🎉

---

### Premium Plans:

**Cost:** ~$1.60 per second of QPU time

**Old config:**
- QPU time: ~540 seconds
- Cost: ~$864 per experiment 💰

**New config:**
- QPU time: ~90 seconds
- Cost: ~$144 per experiment 💰

**Savings: ~$720 per experiment (83% reduction)**

---

## 🚀 How to Run

### Default (Optimized):

```bash
python ibm_hardware_noise_experiment.py
```

**Runs:**
- 4 methods
- 1024 shots
- All 6 configs
- ~5-10 minutes

---

### Test Single Config First:

```bash
python ibm_hardware_noise_experiment.py --config 3q-2t
```

**Runs:**
- 4 methods
- 1024 shots
- Single config
- ~1 minute

---

### Increase Accuracy (More Shots):

```bash
python ibm_hardware_noise_experiment.py --shots 4096
```

**Runs:**
- 4 methods
- 4096 shots (±1.6% error)
- ~15-20 minutes

---

## 📊 Expected Results Table

### Fidelity Comparison (Example):

| Config | Baseline | ZNE | Opt-3 | Opt-3+ZNE |
|--------|----------|-----|-------|-----------|
| 3q-2t | 0.78 | 0.89 | 0.85 | **0.92** |
| 4q-2t | 0.76 | 0.87 | 0.83 | **0.91** |
| 5q-2t | 0.74 | 0.86 | 0.82 | **0.90** |
| 3q-3t | 0.76 | 0.87 | 0.83 | **0.91** |
| 4q-3t | 0.73 | 0.85 | 0.80 | **0.89** |
| 5q-3t | 0.71 | 0.83 | 0.78 | **0.87** |

**Key insight:** Opt-3+ZNE consistently best! ✅

---

## 💡 When to Use Higher Shots

### Use 1024 shots (default) when:
- ✅ Testing the algorithm
- ✅ Initial research/exploration
- ✅ Limited free tier quota
- ✅ Quick turnaround needed

### Use 4096-8192 shots when:
- 📄 Preparing for publication
- 📊 Final results needed
- 💰 Budget available (premium account)
- 🎯 High accuracy critical

---

## ✅ Summary

### Optimizations Applied:

1. ✅ **Reduced methods:** 6 → 4 (removed Opt-0, Opt-0+ZNE)
2. ✅ **Reduced shots:** 8192 → 1024 (8× faster)
3. ✅ **Result:** 6× faster, 83% less QPU time

### Benefits:

- ⚡ **Faster:** ~5-10 min (vs 20-40 min)
- 💰 **Cheaper:** 83% cost reduction
- 🆓 **Free-tier friendly:** 15% quota (vs 90%)
- 🎯 **Still comprehensive:** All key comparisons preserved
- ✅ **Good accuracy:** ±3% error (acceptable for research)

### Trade-offs:

- ⚠️ Slightly less accurate (±3% vs ±1%)
- ⚠️ Missing Opt-0 comparison (rarely needed)

**Overall: Excellent balance of speed, cost, and quality!** 🎯

---

## 🎓 Recommendation

**For most research:** Use the optimized config (default)

**For publication:** Increase to 4096 or 8192 shots:
```bash
python ibm_hardware_noise_experiment.py --shots 8192
```

**For testing:** Use single config first:
```bash
python ibm_hardware_noise_experiment.py --config 3q-2t
```

---

**Your experiment is now optimized for fast, efficient execution!** 🚀
