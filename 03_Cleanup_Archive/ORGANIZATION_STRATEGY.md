# File Organization Strategy - AUX-QHE

## Current State
- **119 unorganized files** in root directory
- **22 existing subdirectories** (some organized, some not)
- Mix of active files, archived files, and one-time debug scripts

## Strategic Approach: 3-Phase Organization

---

## Phase 1: Safety First - Archive Old Results (42 files)
**Goal:** Clear out result files that are already archived or superseded

### 1.1 Keep Only Most Recent Final Results (3 files)
```bash
mkdir -p results/final_2025_10_30
mv ibm_noise_measurement_results_20251030_224547.json results/final_2025_10_30/5q-3t_final.json
mv ibm_noise_measurement_results_20251030_230642.json results/final_2025_10_30/4q-3t_final.json
mv ibm_noise_measurement_results_20251030_231319.json results/final_2025_10_30/5q-2t_final.json
```

### 1.2 Archive Older Final Results (3 files)
```bash
mkdir -p results/archive_final
mv ibm_noise_measurement_results_*.json results/archive_final/
```

### 1.3 Archive All Interim Results (36 files)
```bash
mkdir -p results/interim
mv ibm_noise_results_interim_*.json results/interim/
```

**Result:** Root reduced by 42 files → **77 files remaining**

---

## Phase 2: Categorize by Function (Create New Structure)

### 2.1 Create New Folder Structure
```bash
# Create organized structure
mkdir -p scripts/{analysis,tables,utilities,execution,visualization,experimental}
mkdir -p docs/{guides,results,fixes,archive}
mkdir -p notebooks
mkdir -p paper_materials
```

### 2.2 Move Python Scripts by Category (39 files → organized)

#### Analysis Scripts (3 files → scripts/analysis/)
```bash
mv analyze_circuit_complexity_vs_noise.py scripts/analysis/
mv analyze_ibm_noise_results.py scripts/analysis/
mv display_hardware_results.py scripts/analysis/
```

#### Table Generation (8 files → scripts/tables/)
```bash
mv generate_hardware_table.py scripts/tables/
mv generate_latex_tables.py scripts/tables/
mv generate_results_table.py scripts/tables/
mv generate_compact_table.py scripts/tables/
mv generate_auxiliary_analysis_table.py scripts/tables/
mv add_5q2t_to_hardware_table.py scripts/tables/
mv update_5q2t_hardware_table.py scripts/tables/
mv quick_update_aux_states.py scripts/tables/
```

#### Utilities (6 files → scripts/utilities/)
```bash
mv edit_ibm_account.py scripts/utilities/
mv fix_instance_crn.py scripts/utilities/
mv check_backend_queue.py scripts/utilities/
mv monitor_queue.py scripts/utilities/
mv schedule_experiment.py scripts/utilities/
mv che_bfv.py scripts/utilities/
```

#### Visualization (2 files → scripts/visualization/)
```bash
mv visualize_aux_qhe_circuits.py scripts/visualization/
mv visualize_aux_qhe_protocol.py scripts/visualization/
```

#### Testing/Validation (14 files → 06_Testing_Scripts/)
```bash
mv test_ibm_connection.py 06_Testing_Scripts/
mv test_local_full_pipeline.py 06_Testing_Scripts/
mv test_noise_experiment_local.py 06_Testing_Scripts/
mv test_tdepth.py 06_Testing_Scripts/
mv test_tdepth_fix.py 06_Testing_Scripts/
mv test_tdepth_fix_quick.py 06_Testing_Scripts/
mv test_zne_fix_sxdg.py 06_Testing_Scripts/
mv validate_fixes.py 06_Testing_Scripts/
mv validate_zne_fix.py 06_Testing_Scripts/
mv verify_circuit_description.py 06_Testing_Scripts/
mv verify_qotp_theory.py 06_Testing_Scripts/
mv verify_shared_keys_fix.py 06_Testing_Scripts/
mv VERIFY_CIRCUIT_FIX.py 06_Testing_Scripts/
mv quick_test.py 06_Testing_Scripts/
```

#### Debug Scripts (4 files → debug_scripts/)
```bash
mv CRITICAL_DEBUG_5q2t.py debug_scripts/
mv diagnose_fidelity_issue.py debug_scripts/
mv diagnose_metrics.py debug_scripts/
mv compare_local_vs_hardware.py debug_scripts/
```

#### Experimental (2 files → scripts/experimental/)
```bash
mv run_threshold_experiment.py scripts/experimental/
mv check_actual_tdepth.py scripts/experimental/
```

**Result:** 39 Python scripts organized → **38 files remaining**

### 2.3 Move Shell Scripts (5 files → scripts/execution/)
```bash
mv EXECUTE_4Q_3T.sh scripts/execution/
mv EXECUTE_5Q_2T.sh scripts/execution/
mv EXECUTE_5Q_3T.sh scripts/execution/
mv EXECUTE_ALL_CONFIGS.sh scripts/execution/
mv HARDWARE_EXECUTION_COMMANDS.sh scripts/execution/
```

**Result:** 5 shell scripts organized → **33 files remaining**

### 2.4 Move Documentation (26 files)

#### Execution Guides (3 files → docs/guides/)
```bash
mv README_EXECUTION.md docs/guides/
mv README_IBM_EXPERIMENT.md docs/guides/
mv ALL_CONFIGS_GUIDE.md docs/guides/
```

#### Results Documentation (5 files → docs/results/)
```bash
mv AUX_QHE_5Q_2T_EXPERIMENTAL_RESULTS.md docs/results/
mv EXPERIMENTAL_RESULTS_ANALYSIS_20251027.md docs/results/
mv HARDWARE_RESULTS_SUMMARY.md docs/results/
mv EXECUTION_SUMMARY.md docs/results/
mv CORRECTED_METRICS_TABLE.md docs/results/
```

#### Debug/Fix Documentation (3 files → docs/fixes/)
```bash
mv DEBUG_SUMMARY_2025_10_27.md docs/fixes/
mv FINAL_FIX_5q2t.md docs/fixes/
mv METRICS_BUG_FIX_EXPLANATION.md docs/fixes/
```

#### IBM Setup Guides (5 files → docs/guides/)
```bash
mv QUICK_FIX_ACCOUNT.md docs/guides/
mv TEST_NEW_ACCOUNT.md docs/guides/
mv UPDATE_IBM_ACCOUNT_GUIDE.md docs/guides/
mv CORRECT_CRN_FORMAT.md docs/guides/
mv IBM_DEPLOYMENT_GUIDE_INDEX.md docs/guides/
```

#### Pre-Execution Docs (3 files → docs/guides/)
```bash
mv PRE_EXECUTION_CHECKLIST.md docs/guides/
mv PRE_EXECUTION_VALIDATION_REPORT.md docs/guides/
mv FINAL_PRE_EXECUTION_REPORT.md docs/guides/
```

#### Organization Docs (4 files → docs/archive/)
```bash
mv COMPLETE_ORGANIZATION_PLAN.md docs/archive/
mv FINAL_ORGANIZATION_SUMMARY.md docs/archive/
mv ORGANIZATION_COMPLETE.md docs/archive/
mv DOCUMENTATION_INDEX.md docs/archive/
```

#### Metadata (3 files → docs/archive/)
```bash
mv FILES_CREATED.txt docs/archive/
mv FILES_SUMMARY.txt docs/archive/
mv trace_corrected.txt docs/archive/
```

**Result:** 26 markdown docs + 3 metadata organized → **4 files remaining**

### 2.5 Move Notebooks & Papers (5 files)
```bash
mv Active_QEC-QHE.ipynb notebooks/
mv FHE-AUX-QHE.ipynb notebooks/

mv LATEX_TABLES_FOR_PAPER.tex paper_materials/
mv "Quantum Feature.docx" paper_materials/
mv "Sequence Pair.docx" paper_materials/
```

**Result:** 5 files organized → **-1 files remaining** (we kept some in root)

---

## Phase 3: Finalize Root Directory

### Keep in Root (Essential Files Only)
```
AUX-QHE/
├── README.md                              # Main project readme
├── QUICK_START.md                         # Quick start guide
├── ibm_hardware_noise_experiment.py       # PRIMARY execution script
├── test_hardware_script_local.py          # Local validation script
├── hardware_noise_results_table.md        # Most recent results table
└── UNORGANIZED_FILES_ANALYSIS.md          # This analysis (can archive later)
```

### Final Structure Overview
```
AUX-QHE/
├── README.md
├── QUICK_START.md
├── ibm_hardware_noise_experiment.py
├── test_hardware_script_local.py
├── hardware_noise_results_table.md
│
├── core/                          # Core library (already organized)
├── algorithm/                     # Algorithm implementations
│
├── scripts/                       # NEW: All utility scripts
│   ├── analysis/                  # Analysis scripts (3)
│   ├── tables/                    # Table generation (8)
│   ├── utilities/                 # Utilities (6)
│   ├── execution/                 # Execution scripts (5 .sh files)
│   ├── visualization/             # Visualization (2)
│   └── experimental/              # Experimental scripts (2)
│
├── debug_scripts/                 # Debug/diagnostic scripts (13)
├── 06_Testing_Scripts/            # Testing & validation (14)
│
├── docs/                          # NEW: All documentation
│   ├── guides/                    # Execution & setup guides (11)
│   ├── results/                   # Results documentation (5)
│   ├── fixes/                     # Bug fix documentation (3)
│   └── archive/                   # Old organization docs (7)
│
├── results/                       # NEW: All result files
│   ├── final_2025_10_30/          # Most recent final results (3)
│   ├── archive_final/             # Older final results (3)
│   └── interim/                   # Interim results (36)
│
├── notebooks/                     # Jupyter notebooks (2)
├── paper_materials/               # LaTeX & Word docs (3)
│
├── 01_Hardware_Debug/             # (existing, may merge with debug_scripts)
├── 02_Implementation_Fixes/       # (existing)
├── 03_Cleanup_Archive/            # (existing)
├── 04_Theory_Architecture/        # (existing)
├── 05_Results_Analysis/           # (existing)
├── 07_Quick_Guides/               # (existing)
│
├── qasm3_exports/                 # QASM exports
├── circuit_diagrams/              # Circuit diagrams
└── OLD_RESULTS_ARCHIVE/           # Old results archive
```

---

## Execution Plan: Safe Batch Commands

### Step 1: Create New Structure (safe, just creates directories)
```bash
cd /Users/giadang/my_qiskitenv/AUX-QHE

mkdir -p scripts/{analysis,tables,utilities,execution,visualization,experimental}
mkdir -p docs/{guides,results,fixes,archive}
mkdir -p notebooks
mkdir -p paper_materials
mkdir -p results/{final_2025_10_30,archive_final,interim}
```

### Step 2: Move Results (42 files, low risk)
```bash
# Most recent finals
mv ibm_noise_measurement_results_20251030_224547.json results/final_2025_10_30/5q-3t_final.json
mv ibm_noise_measurement_results_20251030_230642.json results/final_2025_10_30/4q-3t_final.json
mv ibm_noise_measurement_results_20251030_231319.json results/final_2025_10_30/5q-2t_final.json

# Archive older finals
mv ibm_noise_measurement_results_*.json results/archive_final/ 2>/dev/null || true

# Archive interims
mv ibm_noise_results_interim_*.json results/interim/
```

### Step 3: Move Python Scripts (39 files)
```bash
# Analysis
mv analyze_circuit_complexity_vs_noise.py analyze_ibm_noise_results.py display_hardware_results.py scripts/analysis/

# Tables
mv generate_*.py add_5q2t_to_hardware_table.py update_5q2t_hardware_table.py quick_update_aux_states.py scripts/tables/

# Utilities
mv edit_ibm_account.py fix_instance_crn.py check_backend_queue.py monitor_queue.py schedule_experiment.py che_bfv.py scripts/utilities/

# Visualization
mv visualize_*.py scripts/visualization/

# Testing
mv test_*.py verify_*.py VERIFY_*.py validate_*.py quick_test.py 06_Testing_Scripts/

# Debug
mv CRITICAL_DEBUG_5q2t.py diagnose_*.py compare_local_vs_hardware.py debug_scripts/

# Experimental
mv run_threshold_experiment.py check_actual_tdepth.py scripts/experimental/
```

### Step 4: Move Shell Scripts (5 files)
```bash
mv EXECUTE_*.sh HARDWARE_EXECUTION_COMMANDS.sh scripts/execution/
```

### Step 5: Move Documentation (29 files)
```bash
# Guides
mv README_EXECUTION.md README_IBM_EXPERIMENT.md ALL_CONFIGS_GUIDE.md docs/guides/
mv QUICK_FIX_ACCOUNT.md TEST_NEW_ACCOUNT.md UPDATE_IBM_ACCOUNT_GUIDE.md CORRECT_CRN_FORMAT.md IBM_DEPLOYMENT_GUIDE_INDEX.md docs/guides/
mv PRE_EXECUTION_*.md FINAL_PRE_EXECUTION_REPORT.md docs/guides/

# Results
mv AUX_QHE_5Q_2T_EXPERIMENTAL_RESULTS.md EXPERIMENTAL_RESULTS_ANALYSIS_*.md HARDWARE_RESULTS_SUMMARY.md EXECUTION_SUMMARY.md CORRECTED_METRICS_TABLE.md docs/results/

# Fixes
mv DEBUG_SUMMARY_*.md FINAL_FIX_*.md METRICS_BUG_FIX_EXPLANATION.md docs/fixes/

# Archive
mv COMPLETE_ORGANIZATION_PLAN.md FINAL_ORGANIZATION_SUMMARY.md ORGANIZATION_COMPLETE.md DOCUMENTATION_INDEX.md docs/archive/
mv FILES_*.txt trace_corrected.txt docs/archive/
```

### Step 6: Move Notebooks & Papers (5 files)
```bash
mv *.ipynb notebooks/
mv LATEX_TABLES_FOR_PAPER.tex "Quantum Feature.docx" "Sequence Pair.docx" paper_materials/
```

### Step 7: Create Index Files
```bash
# Create README in each new folder
echo "# Analysis Scripts" > scripts/analysis/README.md
echo "# Table Generation Scripts" > scripts/tables/README.md
echo "# Utility Scripts" > scripts/utilities/README.md
echo "# Execution Scripts" > scripts/execution/README.md
echo "# Results Data" > results/README.md
echo "# Documentation" > docs/README.md
```

---

## Benefits of This Strategy

### 1. **Phased Approach** (Safest)
- Phase 1: Archive results (low risk, easy to undo)
- Phase 2: Organize by function (clear categories)
- Phase 3: Clean root (final step)

### 2. **Clear Categories**
- `scripts/` - All executable scripts by purpose
- `docs/` - All documentation by type
- `results/` - All data files by status
- Root - Only essentials

### 3. **Backward Compatibility**
- Keep main execution scripts in root
- Existing organized folders untouched
- Easy to find files by category

### 4. **Maintainable**
- Clear folder structure
- README in each folder
- Similar files grouped together

---

## Quick Execution (All-in-One)

Want me to execute this entire organization in one go? I can run all commands safely with:
1. Dry run first (show what would move)
2. Execute with confirmation
3. Verify results

Just say "execute organization" and I'll proceed!
