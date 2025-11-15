# Content-Based File Organization - AUX-QHE

## Analysis Summary

After reviewing the **actual content** of all 119 files, here's the proper categorization:

---

## 1. CORE ALGORITHM (Keep in `core/`) ✅ Already Organized
**6 Python files - THE HEART OF AUX-QHE**

These are the main algorithm implementation files:

```
core/
├── bfv_core.py              (7.4KB)  - BFV homomorphic encryption
├── circuit_evaluation.py    (14KB)   - Circuit evaluation with aux keys
├── key_generation.py        (16KB)   - AUX-QHE key generation
├── openqasm3_integration.py (14KB)   - OpenQASM 3.0 export
├── qotp_crypto.py          (10KB)   - QOTP encryption/decryption
└── t_gate_gadgets.py       (22KB)   - T-gate gadget construction
```

**Action:** ✅ NO CHANGE - Already properly organized

---

## 2. MAIN EXECUTION SCRIPTS (Keep in ROOT)
**2 Python files - PRIMARY USER INTERFACE**

```
ROOT/
├── ibm_hardware_noise_experiment.py  - MAIN: Hardware execution with 4 error mitigation methods
└── test_hardware_script_local.py     - MAIN: Local validation before hardware run
```

**Purpose:**
- `ibm_hardware_noise_experiment.py` - The primary script users run for hardware experiments
- `test_hardware_script_local.py` - Validates everything works before spending IBM credits

**Action:** ✅ KEEP IN ROOT - These are the main entry points

---

## 3. RESULT DATA FILES (42 JSON files)
**Structured as: Final Results (6) + Interim Saves (36)**

### 3.1 Final Results - Most Recent (KEEP THESE)
```
results/final_latest/
├── 5q-2t_2025_10_30.json    (537KB) - ibm_noise_measurement_results_20251030_231319.json
├── 4q-3t_2025_10_30.json    (521KB) - ibm_noise_measurement_results_20251030_230642.json
└── 5q-3t_2025_10_30.json    (532KB) - ibm_noise_measurement_results_20251030_224547.json
```
**These 3 files are used in your current results table!**

### 3.2 Final Results - Older Runs (ARCHIVE)
```
results/archive_runs/
├── 5q-3t_run1_20251030_221640.json  (534KB)
├── 5q-3t_run2_20251030_222406.json  (523KB)
└── 5q-3t_run3_20251030_230404.json  (526KB)
```
**Older experimental runs - keep for reference**

### 3.3 Interim Results (CAN DELETE OR ARCHIVE)
```
results/interim_autosave/
└── (36 files) - Auto-saved during execution, superseded by final results
```
**These are intermediate saves made during runs - safe to delete or deep archive**

**Action:**
```bash
mkdir -p results/{final_latest,archive_runs,interim_autosave}

# Keep most recent finals
mv ibm_noise_measurement_results_20251030_231319.json results/final_latest/5q-2t_2025_10_30.json
mv ibm_noise_measurement_results_20251030_230642.json results/final_latest/4q-3t_2025_10_30.json
mv ibm_noise_measurement_results_20251030_224547.json results/final_latest/5q-3t_2025_10_30.json

# Archive older runs
mv ibm_noise_measurement_results_*.json results/archive_runs/

# Archive interim saves
mv ibm_noise_results_interim_*.json results/interim_autosave/
```

---

## 4. TESTING & VALIDATION SCRIPTS (15 files)
**Scripts that verify algorithm correctness**

### 4.1 Core Algorithm Tests (Move to `tests/core/`)
```
tests/core/
├── verify_qotp_theory.py           - Tests QOTP encryption/decryption theory
├── verify_shared_keys_fix.py       - Validates shared QOTP keys across methods
├── VERIFY_CIRCUIT_FIX.py          - Verifies circuit creation matches local sim
└── verify_circuit_description.py   - Validates circuits match paper description
```

### 4.2 Hardware Preparation Tests (Move to `tests/hardware/`)
```
tests/hardware/
├── test_ibm_connection.py          - Tests IBM Quantum connection
├── validate_fixes.py               - Validates depth & shot preservation fixes
├── validate_zne_fix.py             - Pre-flight ZNE validation
├── test_zne_fix_sxdg.py           - Tests ZNE gate decomposition
```

### 4.3 Pipeline Tests (Move to `tests/pipeline/`)
```
tests/pipeline/
├── test_local_full_pipeline.py     - Full pipeline test with local simulator
├── test_noise_experiment_local.py  - Noise experiment local test
├── quick_test.py                   - Quick installation/fix verification
```

### 4.4 T-depth Tests (Move to `tests/tdepth/`)
```
tests/tdepth/
├── test_tdepth.py                  - T-depth measurement tests
├── test_tdepth_fix.py             - T-depth fix validation
└── test_tdepth_fix_quick.py       - Quick T-depth fix test
```

**Action:**
```bash
mkdir -p tests/{core,hardware,pipeline,tdepth}

# Core tests
mv verify_qotp_theory.py verify_shared_keys_fix.py VERIFY_CIRCUIT_FIX.py verify_circuit_description.py tests/core/

# Hardware tests
mv test_ibm_connection.py validate_fixes.py validate_zne_fix.py test_zne_fix_sxdg.py tests/hardware/

# Pipeline tests
mv test_local_full_pipeline.py test_noise_experiment_local.py quick_test.py tests/pipeline/

# T-depth tests
mv test_tdepth*.py tests/tdepth/
```

---

## 5. DEBUG & DIAGNOSTIC SCRIPTS (3 files)
**One-time debugging scripts - already moved to debug_scripts/ ✅**

```
debug_scripts/
├── CRITICAL_DEBUG_5q2t.py         - Debug 5q-2t 0% fidelity issue
├── diagnose_fidelity_issue.py     - Diagnose fidelity calculations
└── diagnose_metrics.py            - Diagnose metric computation
```

**Action:** ✅ ALREADY DONE - These are in debug_scripts/

---

## 6. ANALYSIS & METRICS SCRIPTS (3 files)
**Scripts that analyze experimental results**

```
analysis/
├── analyze_ibm_noise_results.py           - Generate comprehensive analysis & plots
├── analyze_circuit_complexity_vs_noise.py - Analyze complexity vs noise correlation
└── compare_local_vs_hardware.py          - Compare ideal vs real hardware results
```

**Action:**
```bash
mkdir -p analysis
mv analyze_ibm_noise_results.py analyze_circuit_complexity_vs_noise.py compare_local_vs_hardware.py analysis/
```

---

## 7. TABLE GENERATION SCRIPTS (7 files)
**Scripts that generate LaTeX tables for papers**

```
tables/
├── generate_hardware_table.py             - Generate main hardware results table
├── generate_latex_tables.py              - Generate all LaTeX tables
├── generate_results_table.py             - Generate results summary table
├── generate_compact_table.py             - Generate compact format table
├── generate_auxiliary_analysis_table.py  - Generate auxiliary state analysis
├── add_5q2t_to_hardware_table.py        - Add 5q-2t to existing table
└── update_5q2t_hardware_table.py        - Update 5q-2t hardware table
```

**Action:**
```bash
mkdir -p tables
mv generate_*.py add_5q2t_to_hardware_table.py update_5q2t_hardware_table.py tables/
```

---

## 8. VISUALIZATION SCRIPTS (3 files)
**Scripts that create circuit diagrams and plots**

```
visualization/
├── visualize_aux_qhe_circuits.py   - Generate circuit diagrams (input, encrypted, transpiled)
├── visualize_aux_qhe_protocol.py   - Visualize full AUX-QHE protocol flow
└── display_hardware_results.py     - Display hardware results with plots
```

**Action:**
```bash
mkdir -p visualization
mv visualize_*.py display_hardware_results.py visualization/
```

---

## 9. UTILITY SCRIPTS (7 files)
**Helper scripts for IBM backend and experiments**

```
utilities/
├── check_backend_queue.py     - Check IBM backend queue length
├── monitor_queue.py          - Monitor queue continuously
├── schedule_experiment.py    - Schedule experiment for off-peak hours
├── edit_ibm_account.py       - Edit IBM account credentials
├── fix_instance_crn.py       - Fix IBM instance CRN format
├── check_actual_tdepth.py    - Check actual T-depth after transpilation
└── run_threshold_experiment.py - Run T-depth threshold experiments
```

**Action:**
```bash
mkdir -p utilities
mv check_backend_queue.py monitor_queue.py schedule_experiment.py edit_ibm_account.py fix_instance_crn.py check_actual_tdepth.py run_threshold_experiment.py utilities/
```

---

## 10. CONFIGURATION/SETUP (2 files)
**Special setup files**

```
config/
├── che_bfv.py                - BFV scheme module (converted from notebook)
└── quick_update_aux_states.py - Quick aux states table updater
```

**Action:**
```bash
mkdir -p config
mv che_bfv.py quick_update_aux_states.py config/
```

---

## 11. EXECUTION SCRIPTS (5 shell scripts)
**Scripts to run experiments**

```
scripts/
├── EXECUTE_5Q_2T.sh               - Run 5q-2t configuration
├── EXECUTE_4Q_3T.sh               - Run 4q-3t configuration
├── EXECUTE_5Q_3T.sh               - Run 5q-3t configuration
├── EXECUTE_ALL_CONFIGS.sh         - Run all configurations
└── HARDWARE_EXECUTION_COMMANDS.sh - Hardware execution command reference
```

**Action:**
```bash
mkdir -p scripts
mv EXECUTE_*.sh HARDWARE_EXECUTION_COMMANDS.sh scripts/
```

---

## 12. DOCUMENTATION FILES (26 MD + 3 other files)

### 12.1 Main Documentation (KEEP IN ROOT)
```
ROOT/
├── README.md                     - Main project README
├── QUICK_START.md               - Quick start guide
└── hardware_noise_results_table.md - Latest results table (ACTIVE)
```

### 12.2 Execution Guides
```
docs/guides/
├── README_EXECUTION.md           - Execution guide
├── README_IBM_EXPERIMENT.md     - IBM experiment guide
├── ALL_CONFIGS_GUIDE.md         - All configurations guide
├── PRE_EXECUTION_CHECKLIST.md   - Pre-execution checklist
├── PRE_EXECUTION_VALIDATION_REPORT.md - Validation report
├── FINAL_PRE_EXECUTION_REPORT.md - Final pre-execution report
```

### 12.3 IBM Account Setup
```
docs/ibm_setup/
├── IBM_DEPLOYMENT_GUIDE_INDEX.md - IBM deployment guide index
├── QUICK_FIX_ACCOUNT.md         - Quick account fix guide
├── TEST_NEW_ACCOUNT.md          - Test new account guide
├── UPDATE_IBM_ACCOUNT_GUIDE.md  - Update account guide
└── CORRECT_CRN_FORMAT.md        - CRN format correction guide
```

### 12.4 Results Documentation
```
docs/results/
├── AUX_QHE_5Q_2T_EXPERIMENTAL_RESULTS.md    - 5q-2t results
├── EXPERIMENTAL_RESULTS_ANALYSIS_20251027.md - Oct 27 analysis
├── HARDWARE_RESULTS_SUMMARY.md              - Hardware results summary
├── EXECUTION_SUMMARY.md                     - Execution summary
└── CORRECTED_METRICS_TABLE.md               - Corrected metrics
```

### 12.5 Bug Fixes Documentation
```
docs/fixes/
├── DEBUG_SUMMARY_2025_10_27.md      - Debug summary Oct 27
├── FINAL_FIX_5q2t.md               - Final 5q-2t fix
└── METRICS_BUG_FIX_EXPLANATION.md  - Metrics bug explanation
```

### 12.6 Organization Archive
```
docs/archive/
├── COMPLETE_ORGANIZATION_PLAN.md    - Organization plan
├── FINAL_ORGANIZATION_SUMMARY.md   - Organization summary
├── ORGANIZATION_COMPLETE.md        - Organization complete
├── DOCUMENTATION_INDEX.md          - Documentation index
├── FILES_CREATED.txt               - Files created log
├── FILES_SUMMARY.txt               - Files summary
└── trace_corrected.txt             - Trace log
```

**Action:**
```bash
mkdir -p docs/{guides,ibm_setup,results,fixes,archive}

# Guides
mv README_EXECUTION.md README_IBM_EXPERIMENT.md ALL_CONFIGS_GUIDE.md PRE_EXECUTION_*.md FINAL_PRE_EXECUTION_REPORT.md docs/guides/

# IBM setup
mv IBM_DEPLOYMENT_GUIDE_INDEX.md QUICK_FIX_ACCOUNT.md TEST_NEW_ACCOUNT.md UPDATE_IBM_ACCOUNT_GUIDE.md CORRECT_CRN_FORMAT.md docs/ibm_setup/

# Results
mv AUX_QHE_5Q_2T_EXPERIMENTAL_RESULTS.md EXPERIMENTAL_RESULTS_ANALYSIS_*.md HARDWARE_RESULTS_SUMMARY.md EXECUTION_SUMMARY.md CORRECTED_METRICS_TABLE.md docs/results/

# Fixes
mv DEBUG_SUMMARY_*.md FINAL_FIX_*.md METRICS_BUG_FIX_EXPLANATION.md docs/fixes/

# Archive
mv COMPLETE_ORGANIZATION_PLAN.md FINAL_ORGANIZATION_SUMMARY.md ORGANIZATION_COMPLETE.md DOCUMENTATION_INDEX.md FILES_*.txt trace_corrected.txt docs/archive/
```

---

## 13. NOTEBOOKS & PAPERS (5 files)

```
notebooks/
├── Active_QEC-QHE.ipynb  - Active research notebook on QEC-QHE
└── FHE-AUX-QHE.ipynb    - FHE-AUX-QHE research notebook

papers/
├── LATEX_TABLES_FOR_PAPER.tex - LaTeX tables for paper
├── Quantum Feature.docx       - Quantum feature document
└── Sequence Pair.docx         - Sequence pair document
```

**Action:**
```bash
mkdir -p notebooks papers
mv *.ipynb notebooks/
mv LATEX_TABLES_FOR_PAPER.tex "Quantum Feature.docx" "Sequence Pair.docx" papers/
```

---

## FINAL ORGANIZED STRUCTURE

```
AUX-QHE/
│
├── README.md                              # Main README
├── QUICK_START.md                         # Quick start
├── hardware_noise_results_table.md        # Latest results
│
├── ibm_hardware_noise_experiment.py       # MAIN: Hardware execution
├── test_hardware_script_local.py          # MAIN: Local validation
│
├── core/                                  # Core algorithm (6 files)
│   ├── bfv_core.py
│   ├── circuit_evaluation.py
│   ├── key_generation.py
│   ├── openqasm3_integration.py
│   ├── qotp_crypto.py
│   └── t_gate_gadgets.py
│
├── results/                               # All experimental data
│   ├── final_latest/                      # Most recent finals (3 JSON)
│   ├── archive_runs/                      # Older runs (3 JSON)
│   └── interim_autosave/                  # Auto-saves (36 JSON)
│
├── tests/                                 # Testing & validation (15 files)
│   ├── core/                              # Algorithm tests (4)
│   ├── hardware/                          # Hardware tests (4)
│   ├── pipeline/                          # Pipeline tests (3)
│   └── tdepth/                            # T-depth tests (4)
│
├── debug_scripts/                         # Debug scripts (13 files)
│
├── analysis/                              # Analysis scripts (3 files)
├── tables/                                # Table generation (7 files)
├── visualization/                         # Visualization (3 files)
├── utilities/                             # Utilities (7 files)
├── config/                                # Configuration (2 files)
├── scripts/                               # Shell scripts (5 files)
│
├── docs/                                  # All documentation
│   ├── guides/                            # Execution guides (6 MD)
│   ├── ibm_setup/                         # IBM setup (5 MD)
│   ├── results/                           # Results docs (5 MD)
│   ├── fixes/                             # Fix docs (3 MD)
│   └── archive/                           # Old docs (7 MD + 3 txt)
│
├── notebooks/                             # Jupyter notebooks (2)
├── papers/                                # Paper materials (3)
│
└── [existing organized folders]
    ├── algorithm/
    ├── qasm3_exports/
    ├── circuit_diagrams/
    ├── OLD_RESULTS_ARCHIVE/
    └── ...
```

---

## EXECUTION COMMANDS (Run in Order)

### Step 1: Create Structure
```bash
cd /Users/giadang/my_qiskitenv/AUX-QHE

mkdir -p results/{final_latest,archive_runs,interim_autosave}
mkdir -p tests/{core,hardware,pipeline,tdepth}
mkdir -p analysis tables visualization utilities config scripts
mkdir -p docs/{guides,ibm_setup,results,fixes,archive}
mkdir -p notebooks papers
```

### Step 2: Organize Results (42 files)
```bash
# Final latest
mv ibm_noise_measurement_results_20251030_231319.json results/final_latest/5q-2t_2025_10_30.json
mv ibm_noise_measurement_results_20251030_230642.json results/final_latest/4q-3t_2025_10_30.json
mv ibm_noise_measurement_results_20251030_224547.json results/final_latest/5q-3t_2025_10_30.json

# Archive runs
mv ibm_noise_measurement_results_*.json results/archive_runs/ 2>/dev/null || true

# Interim
mv ibm_noise_results_interim_*.json results/interim_autosave/
```

### Step 3: Organize Python Scripts (39 files)
```bash
# Tests
mv verify_qotp_theory.py verify_shared_keys_fix.py VERIFY_CIRCUIT_FIX.py verify_circuit_description.py tests/core/
mv test_ibm_connection.py validate_fixes.py validate_zne_fix.py test_zne_fix_sxdg.py tests/hardware/
mv test_local_full_pipeline.py test_noise_experiment_local.py quick_test.py tests/pipeline/
mv test_tdepth*.py tests/tdepth/

# Analysis & Tables
mv analyze_ibm_noise_results.py analyze_circuit_complexity_vs_noise.py compare_local_vs_hardware.py analysis/
mv generate_*.py add_5q2t_to_hardware_table.py update_5q2t_hardware_table.py tables/

# Visualization & Utilities
mv visualize_*.py display_hardware_results.py visualization/
mv check_backend_queue.py monitor_queue.py schedule_experiment.py edit_ibm_account.py fix_instance_crn.py check_actual_tdepth.py run_threshold_experiment.py utilities/

# Config
mv che_bfv.py quick_update_aux_states.py config/
```

### Step 4: Organize Scripts (5 files)
```bash
mv EXECUTE_*.sh HARDWARE_EXECUTION_COMMANDS.sh scripts/
```

### Step 5: Organize Documentation (29 files)
```bash
# Guides
mv README_EXECUTION.md README_IBM_EXPERIMENT.md ALL_CONFIGS_GUIDE.md PRE_EXECUTION_*.md FINAL_PRE_EXECUTION_REPORT.md docs/guides/

# IBM setup
mv IBM_DEPLOYMENT_GUIDE_INDEX.md QUICK_FIX_ACCOUNT.md TEST_NEW_ACCOUNT.md UPDATE_IBM_ACCOUNT_GUIDE.md CORRECT_CRN_FORMAT.md docs/ibm_setup/

# Results & Fixes
mv AUX_QHE_5Q_2T_EXPERIMENTAL_RESULTS.md EXPERIMENTAL_RESULTS_ANALYSIS_*.md HARDWARE_RESULTS_SUMMARY.md EXECUTION_SUMMARY.md CORRECTED_METRICS_TABLE.md docs/results/
mv DEBUG_SUMMARY_*.md FINAL_FIX_*.md METRICS_BUG_FIX_EXPLANATION.md docs/fixes/

# Archive
mv COMPLETE_ORGANIZATION_PLAN.md FINAL_ORGANIZATION_SUMMARY.md ORGANIZATION_COMPLETE.md DOCUMENTATION_INDEX.md FILES_*.txt trace_corrected.txt docs/archive/
```

### Step 6: Organize Notebooks & Papers (5 files)
```bash
mv *.ipynb notebooks/
mv LATEX_TABLES_FOR_PAPER.tex "Quantum Feature.docx" "Sequence Pair.docx" papers/
```

---

## Summary

**Total organized:** 119 files
- Core algorithm: 6 files (already organized)
- Main scripts: 2 files (keep in root)
- Results data: 42 JSON files
- Python scripts: 39 files → 7 categories
- Shell scripts: 5 files
- Documentation: 29 files → 5 categories
- Notebooks/Papers: 5 files

**Root directory after:** 3-5 essential files only
