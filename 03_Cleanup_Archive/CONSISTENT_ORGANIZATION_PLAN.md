# Consistent AUX-QHE Organization Plan

## Current Structure Analysis

Your AUX-QHE already has an organized structure with numbered folders (01-07). Let me integrate the unorganized files into this EXISTING structure instead of creating new folders.

---

## EXISTING ORGANIZED STRUCTURE (Keep & Use)

```
AUX-QHE/
├── 01_Hardware_Debug/          ✅ Hardware debugging documentation
├── 02_Implementation_Fixes/    ✅ Bug fixes & implementation changes
├── 03_Cleanup_Archive/         ✅ Old/archived files
├── 04_Theory_Architecture/     ✅ Theoretical documentation
├── 05_Results_Analysis/        ✅ Results analysis & visualization
├── 06_Testing_Scripts/         ✅ Testing documentation (but missing actual scripts!)
├── 07_Quick_Guides/            ✅ Quick reference guides
│
├── core/                       ✅ Core algorithm implementation
├── algorithm/                  ✅ Algorithm performance comparison
├── performance/                ✅ Performance analysis scripts
├── results/                    ✅ Results data (has analysis/ and final/ subdirs)
├── debug_scripts/              ✅ Debug scripts (we just created)
│
├── qasm3_exports/              ✅ QASM 3.0 exported circuits
├── circuit_diagrams/           ✅ Circuit diagram outputs
├── debug_output/               ✅ Debug output files
├── OLD_RESULTS_ARCHIVE/        ✅ Old archived results
└── Papers/                     ✅ Paper materials
```

---

## REVISED ORGANIZATION PLAN (Consistent with Existing Structure)

### ROOT DIRECTORY (Keep Essential Files Only)
```
ROOT/
├── README.md                              ← KEEP
├── QUICK_START.md                         ← KEEP
├── ibm_hardware_noise_experiment.py       ← KEEP (MAIN EXECUTION)
├── test_hardware_script_local.py          ← KEEP (MAIN VALIDATION)
└── hardware_noise_results_table.md        ← KEEP (LATEST RESULTS)
```

---

## 1. CORE ALGORITHM (Already Organized ✅)

```
core/                                   ← NO CHANGE
├── bfv_core.py                         (7.6KB) - BFV encryption
├── circuit_evaluation.py               (14KB)  - Circuit evaluation
├── key_generation.py                   (16KB)  - Key generation
├── openqasm3_integration.py            (14KB)  - QASM integration
├── qotp_crypto.py                      (10KB)  - QOTP crypto
└── t_gate_gadgets.py                   (22KB)  - T-gate gadgets
```

**Action:** ✅ NO CHANGE

---

## 2. ALGORITHM PERFORMANCE (Already Organized ✅)

```
algorithm/                              ← NO CHANGE
└── openqasm_performance_comparison.py  (23KB) - Performance comparison

performance/                            ← NO CHANGE
├── algorithm_performance_hardware.py   (24KB) - Hardware performance
├── algorithm_performance_mock.py       (23KB) - Mock performance
├── error_analysis.py                   (14KB) - Error analysis
└── noise_error_metrics.py              (21KB) - Noise metrics
```

**Action:** ✅ NO CHANGE

---

## 3. RESULTS DATA (Expand Existing results/ folder)

**Current:**
```
results/
├── README.md
├── analysis/
├── final/
└── corrected_openqasm_performance_comparison.csv
```

**Revised:**
```
results/
├── README.md
├── corrected_openqasm_performance_comparison.csv
│
├── hardware_2025_10_30/               ← NEW: Latest hardware results
│   ├── 5q-2t_final.json              (537KB)
│   ├── 4q-3t_final.json              (521KB)
│   └── 5q-3t_final.json              (532KB)
│
├── archive_hardware/                  ← NEW: Older hardware runs
│   ├── 5q-3t_run1.json
│   ├── 5q-3t_run2.json
│   └── 5q-3t_run3.json
│
├── interim_autosave/                  ← NEW: Interim saves (can delete)
│   └── [36 interim JSON files]
│
├── analysis/                          ← EXISTING
└── final/                             ← EXISTING
```

**Files to Move:**
```bash
# Latest hardware results
ibm_noise_measurement_results_20251030_231319.json → results/hardware_2025_10_30/5q-2t_final.json
ibm_noise_measurement_results_20251030_230642.json → results/hardware_2025_10_30/4q-3t_final.json
ibm_noise_measurement_results_20251030_224547.json → results/hardware_2025_10_30/5q-3t_final.json

# Archive older runs
ibm_noise_measurement_results_20251030_221640.json → results/archive_hardware/
ibm_noise_measurement_results_20251030_222406.json → results/archive_hardware/
ibm_noise_measurement_results_20251030_230404.json → results/archive_hardware/

# Interim saves
ibm_noise_results_interim_*.json → results/interim_autosave/
```

---

## 4. TESTING SCRIPTS (Add to 06_Testing_Scripts/)

**Current:** Only has documentation, missing actual test scripts!

**Revised:**
```
06_Testing_Scripts/
├── README.md
├── ALL_SCRIPTS_DEBUGGED_SUMMARY.md
├── SCRIPT_STATUS_AND_USAGE.md
├── TABLE_GENERATION_SCRIPTS_GUIDE.md
├── TESTING_SUMMARY.md
│
├── core_tests/                        ← NEW: Algorithm validation
│   ├── verify_qotp_theory.py
│   ├── verify_shared_keys_fix.py
│   ├── VERIFY_CIRCUIT_FIX.py
│   └── verify_circuit_description.py
│
├── hardware_tests/                    ← NEW: Hardware validation
│   ├── test_ibm_connection.py
│   ├── validate_fixes.py
│   ├── validate_zne_fix.py
│   └── test_zne_fix_sxdg.py
│
├── pipeline_tests/                    ← NEW: Full pipeline tests
│   ├── test_local_full_pipeline.py
│   ├── test_noise_experiment_local.py
│   └── quick_test.py
│
└── tdepth_tests/                      ← NEW: T-depth tests
    ├── test_tdepth.py
    ├── test_tdepth_fix.py
    └── test_tdepth_fix_quick.py
```

**Files to Move:**
```bash
# Core tests
verify_qotp_theory.py           → 06_Testing_Scripts/core_tests/
verify_shared_keys_fix.py       → 06_Testing_Scripts/core_tests/
VERIFY_CIRCUIT_FIX.py          → 06_Testing_Scripts/core_tests/
verify_circuit_description.py   → 06_Testing_Scripts/core_tests/

# Hardware tests
test_ibm_connection.py  → 06_Testing_Scripts/hardware_tests/
validate_fixes.py       → 06_Testing_Scripts/hardware_tests/
validate_zne_fix.py     → 06_Testing_Scripts/hardware_tests/
test_zne_fix_sxdg.py   → 06_Testing_Scripts/hardware_tests/

# Pipeline tests
test_local_full_pipeline.py     → 06_Testing_Scripts/pipeline_tests/
test_noise_experiment_local.py  → 06_Testing_Scripts/pipeline_tests/
quick_test.py                   → 06_Testing_Scripts/pipeline_tests/

# T-depth tests
test_tdepth.py           → 06_Testing_Scripts/tdepth_tests/
test_tdepth_fix.py       → 06_Testing_Scripts/tdepth_tests/
test_tdepth_fix_quick.py → 06_Testing_Scripts/tdepth_tests/
```

---

## 5. DEBUG SCRIPTS (Already Organized ✅)

```
debug_scripts/                         ← Already done
├── README.md
├── CRITICAL_DEBUG_5q2t.py
├── diagnose_fidelity_issue.py
├── diagnose_metrics.py
├── compare_local_vs_hardware.py
└── [9 more debug files]
```

**Action:** ✅ ALREADY DONE

---

## 6. ANALYSIS SCRIPTS (Add to 05_Results_Analysis/)

**Current:**
```
05_Results_Analysis/
├── README.md
├── AUXILIARY_ANALYSIS_TABLE.md
├── CIRCUIT_VISUALIZATION_GUIDE.md
├── LATEX_TABLE_UPDATE.md
├── METRICS_ISSUE_ANALYSIS.md
└── aux_qhe_comprehensive_report.md
```

**Revised:**
```
05_Results_Analysis/
├── README.md
├── [existing .md files]
│
├── analysis_scripts/                  ← NEW: Analysis Python scripts
│   ├── analyze_ibm_noise_results.py
│   ├── analyze_circuit_complexity_vs_noise.py
│   └── compare_local_vs_hardware.py
│
├── table_scripts/                     ← NEW: Table generation
│   ├── generate_hardware_table.py
│   ├── generate_latex_tables.py
│   ├── generate_results_table.py
│   ├── generate_compact_table.py
│   ├── generate_auxiliary_analysis_table.py
│   ├── add_5q2t_to_hardware_table.py
│   └── update_5q2t_hardware_table.py
│
└── visualization_scripts/             ← NEW: Visualization
    ├── visualize_aux_qhe_circuits.py
    ├── visualize_aux_qhe_protocol.py
    └── display_hardware_results.py
```

**Files to Move:**
```bash
# Analysis scripts
analyze_ibm_noise_results.py           → 05_Results_Analysis/analysis_scripts/
analyze_circuit_complexity_vs_noise.py → 05_Results_Analysis/analysis_scripts/
compare_local_vs_hardware.py          → 05_Results_Analysis/analysis_scripts/

# Table generation
generate_*.py                    → 05_Results_Analysis/table_scripts/
add_5q2t_to_hardware_table.py   → 05_Results_Analysis/table_scripts/
update_5q2t_hardware_table.py   → 05_Results_Analysis/table_scripts/

# Visualization
visualize_*.py           → 05_Results_Analysis/visualization_scripts/
display_hardware_results.py → 05_Results_Analysis/visualization_scripts/
```

---

## 7. UTILITIES & CONFIG (Add to 07_Quick_Guides/)

**Current:**
```
07_Quick_Guides/
├── README.md
├── QASM_VERSION_EXPLAINED.md
├── QUEUE_MANAGEMENT_GUIDE.md
├── QUICK_START_GUIDE.md
├── QUICK_START_TESTING.md
└── TROUBLESHOOTING_IBM_EXPERIMENT.md
```

**Revised:**
```
07_Quick_Guides/
├── README.md
├── [existing .md files]
│
├── utility_scripts/                   ← NEW: Utility scripts
│   ├── check_backend_queue.py
│   ├── monitor_queue.py
│   ├── schedule_experiment.py
│   ├── edit_ibm_account.py
│   ├── fix_instance_crn.py
│   ├── check_actual_tdepth.py
│   └── run_threshold_experiment.py
│
├── config_scripts/                    ← NEW: Config/setup
│   ├── che_bfv.py
│   └── quick_update_aux_states.py
│
└── execution_scripts/                 ← NEW: Execution shell scripts
    ├── EXECUTE_5Q_2T.sh
    ├── EXECUTE_4Q_3T.sh
    ├── EXECUTE_5Q_3T.sh
    ├── EXECUTE_ALL_CONFIGS.sh
    └── HARDWARE_EXECUTION_COMMANDS.sh
```

**Files to Move:**
```bash
# Utilities
check_backend_queue.py     → 07_Quick_Guides/utility_scripts/
monitor_queue.py          → 07_Quick_Guides/utility_scripts/
schedule_experiment.py    → 07_Quick_Guides/utility_scripts/
edit_ibm_account.py       → 07_Quick_Guides/utility_scripts/
fix_instance_crn.py       → 07_Quick_Guides/utility_scripts/
check_actual_tdepth.py    → 07_Quick_Guides/utility_scripts/
run_threshold_experiment.py → 07_Quick_Guides/utility_scripts/

# Config
che_bfv.py                → 07_Quick_Guides/config_scripts/
quick_update_aux_states.py → 07_Quick_Guides/config_scripts/

# Execution scripts
EXECUTE_*.sh                       → 07_Quick_Guides/execution_scripts/
HARDWARE_EXECUTION_COMMANDS.sh     → 07_Quick_Guides/execution_scripts/
```

---

## 8. DOCUMENTATION (Organize into existing numbered folders)

### 8.1 Execution Guides → 07_Quick_Guides/
```bash
README_EXECUTION.md                    → 07_Quick_Guides/
README_IBM_EXPERIMENT.md              → 07_Quick_Guides/
ALL_CONFIGS_GUIDE.md                  → 07_Quick_Guides/
PRE_EXECUTION_CHECKLIST.md            → 07_Quick_Guides/
PRE_EXECUTION_VALIDATION_REPORT.md    → 07_Quick_Guides/
FINAL_PRE_EXECUTION_REPORT.md         → 07_Quick_Guides/
```

### 8.2 IBM Setup Guides → 07_Quick_Guides/ibm_setup/
```bash
IBM_DEPLOYMENT_GUIDE_INDEX.md  → 07_Quick_Guides/ibm_setup/
QUICK_FIX_ACCOUNT.md          → 07_Quick_Guides/ibm_setup/
TEST_NEW_ACCOUNT.md           → 07_Quick_Guides/ibm_setup/
UPDATE_IBM_ACCOUNT_GUIDE.md   → 07_Quick_Guides/ibm_setup/
CORRECT_CRN_FORMAT.md         → 07_Quick_Guides/ibm_setup/
```

### 8.3 Results Documentation → 05_Results_Analysis/
```bash
AUX_QHE_5Q_2T_EXPERIMENTAL_RESULTS.md    → 05_Results_Analysis/
EXPERIMENTAL_RESULTS_ANALYSIS_20251027.md → 05_Results_Analysis/
HARDWARE_RESULTS_SUMMARY.md              → 05_Results_Analysis/
EXECUTION_SUMMARY.md                     → 05_Results_Analysis/
CORRECTED_METRICS_TABLE.md               → 05_Results_Analysis/
```

### 8.4 Bug Fix Documentation → 02_Implementation_Fixes/
```bash
DEBUG_SUMMARY_2025_10_27.md      → 02_Implementation_Fixes/
FINAL_FIX_5q2t.md               → 02_Implementation_Fixes/
METRICS_BUG_FIX_EXPLANATION.md  → 02_Implementation_Fixes/
```

### 8.5 Organization Archive → 03_Cleanup_Archive/
```bash
COMPLETE_ORGANIZATION_PLAN.md   → 03_Cleanup_Archive/
FINAL_ORGANIZATION_SUMMARY.md  → 03_Cleanup_Archive/
ORGANIZATION_COMPLETE.md       → 03_Cleanup_Archive/
DOCUMENTATION_INDEX.md         → 03_Cleanup_Archive/
FILES_CREATED.txt              → 03_Cleanup_Archive/
FILES_SUMMARY.txt              → 03_Cleanup_Archive/
trace_corrected.txt            → 03_Cleanup_Archive/
```

---

## 9. NOTEBOOKS & PAPERS (Use existing Papers/ folder)

```
Papers/                                ← Already exists
├── LATEX_TABLES_FOR_PAPER.tex
├── Quantum Feature.docx
├── Sequence Pair.docx
│
└── notebooks/                         ← NEW subfolder
    ├── Active_QEC-QHE.ipynb
    └── FHE-AUX-QHE.ipynb
```

**Files to Move:**
```bash
*.ipynb                    → Papers/notebooks/
LATEX_TABLES_FOR_PAPER.tex → Papers/
"Quantum Feature.docx"     → Papers/
"Sequence Pair.docx"       → Papers/
```

---

## FINAL CONSISTENT STRUCTURE

```
AUX-QHE/
│
├── README.md                              # Main README
├── QUICK_START.md                         # Quick start
├── hardware_noise_results_table.md        # Latest results
├── ibm_hardware_noise_experiment.py       # MAIN: Hardware execution
├── test_hardware_script_local.py          # MAIN: Local validation
│
├── core/                                  # Core algorithm (6 files)
├── algorithm/                             # Algorithm comparison (1 file)
├── performance/                           # Performance analysis (4 files)
│
├── results/                               # All experimental data
│   ├── hardware_2025_10_30/              # Latest finals (3 JSON)
│   ├── archive_hardware/                  # Older runs (3 JSON)
│   ├── interim_autosave/                  # Interim saves (36 JSON)
│   ├── analysis/                          # Analysis results
│   └── final/                             # Other final results
│
├── 01_Hardware_Debug/                     # Hardware debug docs
├── 02_Implementation_Fixes/               # Bug fixes + new fix docs
├── 03_Cleanup_Archive/                    # Archive + organization docs
├── 04_Theory_Architecture/                # Theory docs
│
├── 05_Results_Analysis/                   # Results analysis
│   ├── analysis_scripts/                  # Analysis scripts (3)
│   ├── table_scripts/                     # Table generation (7)
│   ├── visualization_scripts/             # Visualization (3)
│   └── [existing .md files]
│
├── 06_Testing_Scripts/                    # Testing
│   ├── core_tests/                        # Core tests (4)
│   ├── hardware_tests/                    # Hardware tests (4)
│   ├── pipeline_tests/                    # Pipeline tests (3)
│   ├── tdepth_tests/                      # T-depth tests (3)
│   └── [existing .md files]
│
├── 07_Quick_Guides/                       # Quick guides
│   ├── utility_scripts/                   # Utilities (7)
│   ├── config_scripts/                    # Config (2)
│   ├── execution_scripts/                 # Shell scripts (5)
│   ├── ibm_setup/                         # IBM setup guides (5)
│   └── [existing .md files + new guides]
│
├── debug_scripts/                         # Debug scripts (13)
│
├── Papers/                                # Paper materials
│   ├── notebooks/                         # Jupyter notebooks (2)
│   └── [paper docs]
│
└── [Other existing folders]
    ├── qasm3_exports/
    ├── circuit_diagrams/
    ├── debug_output/
    └── OLD_RESULTS_ARCHIVE/
```

---

## EXECUTION COMMANDS (Consistent with Existing Structure)

### Step 1: Create New Subdirectories
```bash
cd /Users/giadang/my_qiskitenv/AUX-QHE

# Results
mkdir -p results/{hardware_2025_10_30,archive_hardware,interim_autosave}

# Testing Scripts
mkdir -p 06_Testing_Scripts/{core_tests,hardware_tests,pipeline_tests,tdepth_tests}

# Results Analysis
mkdir -p 05_Results_Analysis/{analysis_scripts,table_scripts,visualization_scripts}

# Quick Guides
mkdir -p 07_Quick_Guides/{utility_scripts,config_scripts,execution_scripts,ibm_setup}

# Papers
mkdir -p Papers/notebooks
```

### Step 2: Move Result Files (42 JSON files)
```bash
# Latest hardware results (IMPORTANT!)
mv ibm_noise_measurement_results_20251030_231319.json results/hardware_2025_10_30/5q-2t_final.json
mv ibm_noise_measurement_results_20251030_230642.json results/hardware_2025_10_30/4q-3t_final.json
mv ibm_noise_measurement_results_20251030_224547.json results/hardware_2025_10_30/5q-3t_final.json

# Archive older runs
mv ibm_noise_measurement_results_20251030_221640.json results/archive_hardware/
mv ibm_noise_measurement_results_20251030_222406.json results/archive_hardware/
mv ibm_noise_measurement_results_20251030_230404.json results/archive_hardware/

# Interim saves
mv ibm_noise_results_interim_*.json results/interim_autosave/
```

### Step 3: Move Testing Scripts (15 files)
```bash
# Core tests
mv verify_qotp_theory.py verify_shared_keys_fix.py VERIFY_CIRCUIT_FIX.py verify_circuit_description.py 06_Testing_Scripts/core_tests/

# Hardware tests
mv test_ibm_connection.py validate_fixes.py validate_zne_fix.py test_zne_fix_sxdg.py 06_Testing_Scripts/hardware_tests/

# Pipeline tests
mv test_local_full_pipeline.py test_noise_experiment_local.py quick_test.py 06_Testing_Scripts/pipeline_tests/

# T-depth tests
mv test_tdepth.py test_tdepth_fix.py test_tdepth_fix_quick.py 06_Testing_Scripts/tdepth_tests/
```

### Step 4: Move Analysis & Table Scripts (13 files)
```bash
# Analysis
mv analyze_ibm_noise_results.py analyze_circuit_complexity_vs_noise.py compare_local_vs_hardware.py 05_Results_Analysis/analysis_scripts/

# Tables
mv generate_hardware_table.py generate_latex_tables.py generate_results_table.py generate_compact_table.py generate_auxiliary_analysis_table.py add_5q2t_to_hardware_table.py update_5q2t_hardware_table.py 05_Results_Analysis/table_scripts/

# Visualization
mv visualize_aux_qhe_circuits.py visualize_aux_qhe_protocol.py display_hardware_results.py 05_Results_Analysis/visualization_scripts/
```

### Step 5: Move Utilities & Config (14 files)
```bash
# Utilities
mv check_backend_queue.py monitor_queue.py schedule_experiment.py edit_ibm_account.py fix_instance_crn.py check_actual_tdepth.py run_threshold_experiment.py 07_Quick_Guides/utility_scripts/

# Config
mv che_bfv.py quick_update_aux_states.py 07_Quick_Guides/config_scripts/

# Execution scripts
mv EXECUTE_5Q_2T.sh EXECUTE_4Q_3T.sh EXECUTE_5Q_3T.sh EXECUTE_ALL_CONFIGS.sh HARDWARE_EXECUTION_COMMANDS.sh 07_Quick_Guides/execution_scripts/
```

### Step 6: Move Documentation (26 MD + 3 txt files)
```bash
# Execution guides → 07_Quick_Guides/
mv README_EXECUTION.md README_IBM_EXPERIMENT.md ALL_CONFIGS_GUIDE.md PRE_EXECUTION_CHECKLIST.md PRE_EXECUTION_VALIDATION_REPORT.md FINAL_PRE_EXECUTION_REPORT.md 07_Quick_Guides/

# IBM setup → 07_Quick_Guides/ibm_setup/
mv IBM_DEPLOYMENT_GUIDE_INDEX.md QUICK_FIX_ACCOUNT.md TEST_NEW_ACCOUNT.md UPDATE_IBM_ACCOUNT_GUIDE.md CORRECT_CRN_FORMAT.md 07_Quick_Guides/ibm_setup/

# Results docs → 05_Results_Analysis/
mv AUX_QHE_5Q_2T_EXPERIMENTAL_RESULTS.md EXPERIMENTAL_RESULTS_ANALYSIS_20251027.md HARDWARE_RESULTS_SUMMARY.md EXECUTION_SUMMARY.md CORRECTED_METRICS_TABLE.md 05_Results_Analysis/

# Fix docs → 02_Implementation_Fixes/
mv DEBUG_SUMMARY_2025_10_27.md FINAL_FIX_5q2t.md METRICS_BUG_FIX_EXPLANATION.md 02_Implementation_Fixes/

# Archive docs → 03_Cleanup_Archive/
mv COMPLETE_ORGANIZATION_PLAN.md FINAL_ORGANIZATION_SUMMARY.md ORGANIZATION_COMPLETE.md DOCUMENTATION_INDEX.md FILES_CREATED.txt FILES_SUMMARY.txt trace_corrected.txt 03_Cleanup_Archive/
```

### Step 7: Move Notebooks & Papers (5 files)
```bash
mv Active_QEC-QHE.ipynb FHE-AUX-QHE.ipynb Papers/notebooks/
mv LATEX_TABLES_FOR_PAPER.tex "Quantum Feature.docx" "Sequence Pair.docx" Papers/
```

---

## BENEFITS OF THIS APPROACH

✅ **Consistent with Existing Structure** - Uses your numbered folders (01-07)
✅ **Logical Organization** - Each folder has a clear purpose
✅ **Minimal Disruption** - Builds on existing organization
✅ **Easy to Navigate** - Similar files grouped together
✅ **Maintainable** - Clear categories for future files

**Root directory:** Only 5 essential files
**Total organized:** 119 files into existing numbered structure
