# AUX-QHE Documentation Index

**Last Updated:** October 26, 2025
**Total Documents:** 41 files organized into 7 folders

---

## 📚 Quick Navigation

### Start Here
- **[README.md](README.md)** - Main project overview
- **[README_IBM_EXPERIMENT.md](README_IBM_EXPERIMENT.md)** - IBM hardware experiments guide
- **[IBM_DEPLOYMENT_GUIDE_INDEX.md](IBM_DEPLOYMENT_GUIDE_INDEX.md)** - IBM deployment guides

---

## 📁 Organized Documentation Folders

### 01. 🔍 Hardware Debug (11 files)
**Purpose:** Debug analysis, workflow verification, and hardware findings

**Start with:**
- **[HARDWARE_WORKFLOW_DEBUG_SUMMARY.md](01_Hardware_Debug/HARDWARE_WORKFLOW_DEBUG_SUMMARY.md)** ⭐ Main debug report
  - Complete workflow analysis
  - 9 issues identified (2 critical, 3 high, 4 medium)
  - Verdict: Workflow is correct, findings are real

**Key findings:**
- **[WHY_ERROR_MITIGATION_FAILED_5Q2T.md](01_Hardware_Debug/WHY_ERROR_MITIGATION_FAILED_5Q2T.md)** - Why Baseline > ZNE
- **[CIRCUIT_COMPLEXITY_VS_HARDWARE_NOISE.md](01_Hardware_Debug/CIRCUIT_COMPLEXITY_VS_HARDWARE_NOISE.md)** - Aux states dominate (r=-0.90)
- **[TABLE_ANOMALY_ANALYSIS.md](01_Hardware_Debug/TABLE_ANOMALY_ANALYSIS.md)** - Depth measurement timing issue

**Other files:**
- DEBUG_VERIFICATION_REPORT.md
- DEBUG_FIXES_SUMMARY.md
- VERIFICATION_5Q2T_FINDINGS.md
- 5Q2T_HARDWARE_TABLE_UPDATE_COMPLETE.md
- RERUN_5Q2T_HARDWARE_GUIDE.md
- IBM_HARDWARE_EXPERIMENTS_REVIEW.md
- HARDWARE_IMPACT_PREDICTION.md

---

### 02. 🔧 Implementation Fixes (8 files)
**Purpose:** Code fixes, implementation changes, and verification

**Start with:**
- **[RECOMMENDATION_CHECKLIST.md](02_Implementation_Fixes/RECOMMENDATION_CHECKLIST.md)** ⭐ Complete checklist
  - All recommendations tracked
  - Implementation status
  - What's done vs pending

**Key files:**
- **[CODE_FIXES_APPLIED_OCT26.md](02_Implementation_Fixes/CODE_FIXES_APPLIED_OCT26.md)** - What was fixed
- **[IMPLEMENTATION_COMPLETE.md](02_Implementation_Fixes/IMPLEMENTATION_COMPLETE.md)** - Implementation summary
- **[VERIFICATION_COMPLETE.md](02_Implementation_Fixes/VERIFICATION_COMPLETE.md)** - All verified ✅

**Other files:**
- FIXES_APPLIED_OLD.md (previous fixes)
- FIXES_APPLIED_THEORETICAL_COMPLIANCE.md
- SIMPLE_EXPLANATION_WHAT_CHANGED.md
- WHY_ONLY_T_DEPTH_2_AFFECTED.md

---

### 03. 🗑️ Cleanup Archive (2 files)
**Purpose:** File organization and cleanup

- **[CLEANUP_PLAN.md](03_Cleanup_Archive/CLEANUP_PLAN.md)** - Detailed cleanup plan
- **[CLEANUP_SUMMARY.md](03_Cleanup_Archive/CLEANUP_SUMMARY.md)** - What was archived and why

**Summary:** 63 old files (52 MB) archived to OLD_RESULTS_ARCHIVE/

---

### 04. 📖 Theory & Architecture (3 files)
**Purpose:** Theoretical background and system architecture

- **[AUX_QHE_PSEUDOCODE.md](04_Theory_Architecture/AUX_QHE_PSEUDOCODE.md)** - Algorithm pseudocode
- **[CORRECTED_ARCHITECTURE.md](04_Theory_Architecture/CORRECTED_ARCHITECTURE.md)** - System architecture
- **[THEORY_AUXILIARY_STATES.md](04_Theory_Architecture/THEORY_AUXILIARY_STATES.md)** - Auxiliary states theory

---

### 05. 📊 Results & Analysis (5 files)
**Purpose:** Results tables, LaTeX generation, and analysis

- **[AUXILIARY_ANALYSIS_TABLE.md](05_Results_Analysis/AUXILIARY_ANALYSIS_TABLE.md)** - Auxiliary states analysis
- **[LATEX_TABLE_UPDATE.md](05_Results_Analysis/LATEX_TABLE_UPDATE.md)** - LaTeX table generation
- **[METRICS_ISSUE_ANALYSIS.md](05_Results_Analysis/METRICS_ISSUE_ANALYSIS.md)** - Metrics analysis
- **[CIRCUIT_VISUALIZATION_GUIDE.md](05_Results_Analysis/CIRCUIT_VISUALIZATION_GUIDE.md)** - Visualization guide
- **[aux_qhe_comprehensive_report.md](05_Results_Analysis/aux_qhe_comprehensive_report.md)** - Comprehensive report

---

### 06. 🧪 Testing & Scripts (4 files)
**Purpose:** Testing guides and script documentation

- **[TESTING_SUMMARY.md](06_Testing_Scripts/TESTING_SUMMARY.md)** - Testing summary
- **[ALL_SCRIPTS_DEBUGGED_SUMMARY.md](06_Testing_Scripts/ALL_SCRIPTS_DEBUGGED_SUMMARY.md)** - Script debug status
- **[SCRIPT_STATUS_AND_USAGE.md](06_Testing_Scripts/SCRIPT_STATUS_AND_USAGE.md)** - Script usage guide
- **[TABLE_GENERATION_SCRIPTS_GUIDE.md](06_Testing_Scripts/TABLE_GENERATION_SCRIPTS_GUIDE.md)** - Table scripts

---

### 07. 🚀 Quick Start Guides (5 files)
**Purpose:** Quick reference and troubleshooting

- **[QUICK_START_GUIDE.md](07_Quick_Guides/QUICK_START_GUIDE.md)** - Quick start
- **[QUICK_START_TESTING.md](07_Quick_Guides/QUICK_START_TESTING.md)** - Quick testing
- **[TROUBLESHOOTING_IBM_EXPERIMENT.md](07_Quick_Guides/TROUBLESHOOTING_IBM_EXPERIMENT.md)** - Troubleshooting
- **[QUEUE_MANAGEMENT_GUIDE.md](07_Quick_Guides/QUEUE_MANAGEMENT_GUIDE.md)** - Queue management
- **[QASM_VERSION_EXPLAINED.md](07_Quick_Guides/QASM_VERSION_EXPLAINED.md)** - QASM versions

---

## 🎯 Common Tasks

### I want to understand the workflow debugging
→ Read [01_Hardware_Debug/HARDWARE_WORKFLOW_DEBUG_SUMMARY.md](01_Hardware_Debug/HARDWARE_WORKFLOW_DEBUG_SUMMARY.md)

### I want to see what code was fixed
→ Read [02_Implementation_Fixes/CODE_FIXES_APPLIED_OCT26.md](02_Implementation_Fixes/CODE_FIXES_APPLIED_OCT26.md)

### I want to verify all fixes are complete
→ Read [02_Implementation_Fixes/RECOMMENDATION_CHECKLIST.md](02_Implementation_Fixes/RECOMMENDATION_CHECKLIST.md)

### I want to understand why error mitigation failed
→ Read [01_Hardware_Debug/WHY_ERROR_MITIGATION_FAILED_5Q2T.md](01_Hardware_Debug/WHY_ERROR_MITIGATION_FAILED_5Q2T.md)

### I want to clean up old files
→ Read [03_Cleanup_Archive/CLEANUP_PLAN.md](03_Cleanup_Archive/CLEANUP_PLAN.md)

### I want to run tests
→ Read [06_Testing_Scripts/TESTING_SUMMARY.md](06_Testing_Scripts/TESTING_SUMMARY.md)

### I want quick start
→ Read [07_Quick_Guides/QUICK_START_GUIDE.md](07_Quick_Guides/QUICK_START_GUIDE.md)

### I want to understand the theory
→ Read [04_Theory_Architecture/AUX_QHE_PSEUDOCODE.md](04_Theory_Architecture/AUX_QHE_PSEUDOCODE.md)

---

## 📈 Key Findings Summary

### From Hardware Debug
1. **Workflow is correct** ✅ - Fidelity values are trustworthy
2. **Auxiliary states dominate noise** (r = -0.90) - Primary design target
3. **Baseline > Error mitigation for 5q-2t** - Circuit in "sweet spot"
4. **Depth paradox is real** - Lower depth ≠ better fidelity
5. **Only issue:** Depth measured before ZNE folding (fixed in code)

### From Implementation
1. **Fix #1:** Depth measurement timing - ✅ FIXED
2. **Fix #2:** Shot count preservation - ✅ FIXED
3. **All tests passed** - Validation complete ✅
4. **Documentation complete** - 41 files, 7 folders organized

### From Cleanup
1. **63 old files archived** (52 MB) - Moved to OLD_RESULTS_ARCHIVE/
2. **6 final result files** - Only correct data in main folder
3. **No confusion risk** - Clear which data to use for paper

---

## 📝 File Counts by Folder

| Folder | Files | Purpose |
|--------|-------|---------|
| 00_Root | 4 | Main documentation (README, index) |
| 01_Hardware_Debug | 11 | Debug analysis and findings |
| 02_Implementation_Fixes | 8 | Code fixes and verification |
| 03_Cleanup_Archive | 2 | File organization |
| 04_Theory_Architecture | 3 | Theoretical background |
| 05_Results_Analysis | 5 | Results tables and analysis |
| 06_Testing_Scripts | 4 | Testing and script guides |
| 07_Quick_Guides | 5 | Quick reference |
| **Total** | **42** | **Fully organized** |

---

## 🔄 Recent Changes

**October 26, 2025:**
- ✅ Debugged hardware workflow (9 issues identified)
- ✅ Applied 2 code fixes (depth measurement, shot preservation)
- ✅ Validated all fixes (all tests passed)
- ✅ Cleaned up 63 old result files (archived)
- ✅ Organized 41 documentation files into 7 folders

---

## 📚 Related Folders

- **IBM_Hardware_Deployment_Guides/** - IBM deployment documentation
- **OLD_RESULTS_ARCHIVE/** - Archived old result files (can delete)
- **qasm3_exports/** - QASM 3.0 circuit exports
- **core/** - AUX-QHE core implementation

---

## 🎓 For Paper Writing

### Final Data Files (Use These!)
- `ibm_noise_results_interim_20251023_232611.json` (555K)
- `local_vs_hardware_comparison.csv` (1.0K)
- `circuit_complexity_vs_noise_summary.csv` (667B)

### Key Findings to Include
1. Auxiliary states correlation (r = -0.90)
2. Error mitigation "sweet spot" phenomenon
3. Circuit complexity analysis
4. Depth-fidelity paradox explanation

### Text Snippets for Paper
- See [02_Implementation_Fixes/RECOMMENDATION_CHECKLIST.md](02_Implementation_Fixes/RECOMMENDATION_CHECKLIST.md)
- Footnote, Results, and Discussion text provided

---

## 💡 Tips

**Finding something specific?**
- Use folder numbers (01-07) for logical order
- Check this index for quick links
- Main findings in 01_Hardware_Debug/

**Need to add new documentation?**
- Put in appropriate numbered folder
- Update this index
- Use descriptive filename

**Sharing documentation?**
- Share entire folder (e.g., 01_Hardware_Debug/)
- Or share specific file with context
- This index provides navigation

---

**Index Created:** October 26, 2025
**Status:** ✅ Complete and organized
**Maintenance:** Update when adding new docs
