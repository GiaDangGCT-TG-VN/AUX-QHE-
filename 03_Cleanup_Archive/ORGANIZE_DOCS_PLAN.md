# Documentation Organization Plan

**Date:** October 26, 2025
**Purpose:** Organize 41 markdown files into logical folders

---

## 📁 Proposed Folder Structure

### 1. **01_Hardware_Debug/** (11 files)
Debug analysis and workflow verification

- HARDWARE_WORKFLOW_DEBUG_SUMMARY.md
- DEBUG_VERIFICATION_REPORT.md
- DEBUG_FIXES_SUMMARY.md
- WHY_ERROR_MITIGATION_FAILED_5Q2T.md
- VERIFICATION_5Q2T_FINDINGS.md
- TABLE_ANOMALY_ANALYSIS.md
- 5Q2T_HARDWARE_TABLE_UPDATE_COMPLETE.md
- RERUN_5Q2T_HARDWARE_GUIDE.md
- IBM_HARDWARE_EXPERIMENTS_REVIEW.md
- HARDWARE_IMPACT_PREDICTION.md
- CIRCUIT_COMPLEXITY_VS_HARDWARE_NOISE.md

### 2. **02_Implementation_Fixes/** (8 files)
Code fixes and implementation changes

- CODE_FIXES_APPLIED_OCT26.md
- IMPLEMENTATION_COMPLETE.md
- RECOMMENDATION_CHECKLIST.md
- VERIFICATION_COMPLETE.md
- FIXES_APPLIED_OLD.md
- FIXES_APPLIED_THEORETICAL_COMPLIANCE.md
- SIMPLE_EXPLANATION_WHAT_CHANGED.md
- WHY_ONLY_T_DEPTH_2_AFFECTED.md

### 3. **03_Cleanup_Archive/** (2 files)
File cleanup and organization

- CLEANUP_PLAN.md
- CLEANUP_SUMMARY.md

### 4. **04_Theory_Architecture/** (3 files)
Theoretical background and architecture

- AUX_QHE_PSEUDOCODE.md
- CORRECTED_ARCHITECTURE.md
- THEORY_AUXILIARY_STATES.md

### 5. **05_Results_Analysis/** (5 files)
Results tables and analysis

- AUXILIARY_ANALYSIS_TABLE.md
- LATEX_TABLE_UPDATE.md
- aux_qhe_comprehensive_report.md
- METRICS_ISSUE_ANALYSIS.md
- CIRCUIT_VISUALIZATION_GUIDE.md

### 6. **06_Testing_Scripts/** (4 files)
Testing guides and summaries

- TESTING_SUMMARY.md
- ALL_SCRIPTS_DEBUGGED_SUMMARY.md
- SCRIPT_STATUS_AND_USAGE.md
- TABLE_GENERATION_SCRIPTS_GUIDE.md

### 7. **07_Quick_Guides/** (5 files)
Quick start and troubleshooting

- QUICK_START_GUIDE.md
- QUICK_START_TESTING.md
- QUEUE_MANAGEMENT_GUIDE.md
- TROUBLESHOOTING_IBM_EXPERIMENT.md
- QASM_VERSION_EXPLAINED.md

### 8. **00_Main/** (3 files - keep in root)
Main documentation to keep visible

- README.md
- README_IBM_EXPERIMENT.md
- IBM_DEPLOYMENT_GUIDE_INDEX.md (points to existing IBM guides)

---

## 🎯 Organization Strategy

**Numbering:** Folders numbered for logical flow
- 00 = Main (root level)
- 01 = Hardware (most important for debugging)
- 02 = Implementation fixes
- 03 = Cleanup
- 04 = Theory
- 05 = Results
- 06 = Testing
- 07 = Quick guides

**Benefits:**
- ✅ Easy to navigate
- ✅ Logical grouping
- ✅ Numbered for ordering
- ✅ Main docs still in root

---

## 📋 Execution Commands

```bash
cd /Users/giadang/my_qiskitenv/AUX-QHE

# Create folders
mkdir -p 01_Hardware_Debug
mkdir -p 02_Implementation_Fixes
mkdir -p 03_Cleanup_Archive
mkdir -p 04_Theory_Architecture
mkdir -p 05_Results_Analysis
mkdir -p 06_Testing_Scripts
mkdir -p 07_Quick_Guides

# Move files to 01_Hardware_Debug/
mv HARDWARE_WORKFLOW_DEBUG_SUMMARY.md 01_Hardware_Debug/
mv DEBUG_VERIFICATION_REPORT.md 01_Hardware_Debug/
mv DEBUG_FIXES_SUMMARY.md 01_Hardware_Debug/
mv WHY_ERROR_MITIGATION_FAILED_5Q2T.md 01_Hardware_Debug/
mv VERIFICATION_5Q2T_FINDINGS.md 01_Hardware_Debug/
mv TABLE_ANOMALY_ANALYSIS.md 01_Hardware_Debug/
mv 5Q2T_HARDWARE_TABLE_UPDATE_COMPLETE.md 01_Hardware_Debug/
mv RERUN_5Q2T_HARDWARE_GUIDE.md 01_Hardware_Debug/
mv IBM_HARDWARE_EXPERIMENTS_REVIEW.md 01_Hardware_Debug/
mv HARDWARE_IMPACT_PREDICTION.md 01_Hardware_Debug/
mv CIRCUIT_COMPLEXITY_VS_HARDWARE_NOISE.md 01_Hardware_Debug/

# Move files to 02_Implementation_Fixes/
mv CODE_FIXES_APPLIED_OCT26.md 02_Implementation_Fixes/
mv IMPLEMENTATION_COMPLETE.md 02_Implementation_Fixes/
mv RECOMMENDATION_CHECKLIST.md 02_Implementation_Fixes/
mv VERIFICATION_COMPLETE.md 02_Implementation_Fixes/
mv FIXES_APPLIED_OLD.md 02_Implementation_Fixes/
mv FIXES_APPLIED_THEORETICAL_COMPLIANCE.md 02_Implementation_Fixes/
mv SIMPLE_EXPLANATION_WHAT_CHANGED.md 02_Implementation_Fixes/
mv WHY_ONLY_T_DEPTH_2_AFFECTED.md 02_Implementation_Fixes/

# Move files to 03_Cleanup_Archive/
mv CLEANUP_PLAN.md 03_Cleanup_Archive/
mv CLEANUP_SUMMARY.md 03_Cleanup_Archive/

# Move files to 04_Theory_Architecture/
mv AUX_QHE_PSEUDOCODE.md 04_Theory_Architecture/
mv CORRECTED_ARCHITECTURE.md 04_Theory_Architecture/
mv THEORY_AUXILIARY_STATES.md 04_Theory_Architecture/

# Move files to 05_Results_Analysis/
mv AUXILIARY_ANALYSIS_TABLE.md 05_Results_Analysis/
mv LATEX_TABLE_UPDATE.md 05_Results_Analysis/
mv aux_qhe_comprehensive_report.md 05_Results_Analysis/
mv METRICS_ISSUE_ANALYSIS.md 05_Results_Analysis/
mv CIRCUIT_VISUALIZATION_GUIDE.md 05_Results_Analysis/

# Move files to 06_Testing_Scripts/
mv TESTING_SUMMARY.md 06_Testing_Scripts/
mv ALL_SCRIPTS_DEBUGGED_SUMMARY.md 06_Testing_Scripts/
mv SCRIPT_STATUS_AND_USAGE.md 06_Testing_Scripts/
mv TABLE_GENERATION_SCRIPTS_GUIDE.md 06_Testing_Scripts/

# Move files to 07_Quick_Guides/
mv QUICK_START_GUIDE.md 07_Quick_Guides/
mv QUICK_START_TESTING.md 07_Quick_Guides/
mv QUEUE_MANAGEMENT_GUIDE.md 07_Quick_Guides/
mv TROUBLESHOOTING_IBM_EXPERIMENT.md 07_Quick_Guides/
mv QASM_VERSION_EXPLAINED.md 07_Quick_Guides/

echo "✅ Documentation organized into 7 folders"
```

---

## 📝 Create Master INDEX.md

After organizing, create an index file in root.
