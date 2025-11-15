# Unorganized Files Analysis - AUX-QHE

**Total files in root directory:** 119 files (not including subdirectories)

## File Categories

### 1. Python Scripts (39 files)

#### Main Execution Scripts (KEEP IN ROOT)
- `ibm_hardware_noise_experiment.py` - **PRIMARY** hardware execution script
- `test_hardware_script_local.py` - Local validation script

#### Testing/Validation Scripts (→ 06_Testing_Scripts)
- `test_ibm_connection.py`
- `test_local_full_pipeline.py`
- `test_noise_experiment_local.py`
- `test_tdepth.py`
- `test_tdepth_fix.py`
- `test_tdepth_fix_quick.py`
- `test_zne_fix_sxdg.py`
- `validate_fixes.py`
- `validate_zne_fix.py`
- `verify_circuit_description.py`
- `verify_qotp_theory.py`
- `verify_shared_keys_fix.py`
- `VERIFY_CIRCUIT_FIX.py`
- `quick_test.py`

#### Debug/Diagnostic Scripts (→ debug_scripts)
- `CRITICAL_DEBUG_5q2t.py`
- `diagnose_fidelity_issue.py`
- `diagnose_metrics.py`
- `compare_local_vs_hardware.py`

#### Analysis/Results Scripts (→ 05_Results_Analysis)
- `analyze_circuit_complexity_vs_noise.py`
- `analyze_ibm_noise_results.py`
- `display_hardware_results.py`

#### Table Generation Scripts (→ 05_Results_Analysis)
- `generate_hardware_table.py`
- `generate_latex_tables.py`
- `generate_results_table.py`
- `generate_compact_table.py`
- `generate_auxiliary_analysis_table.py`
- `add_5q2t_to_hardware_table.py`
- `update_5q2t_hardware_table.py`
- `quick_update_aux_states.py`

#### Visualization Scripts (→ 05_Results_Analysis or new viz folder)
- `visualize_aux_qhe_circuits.py`
- `visualize_aux_qhe_protocol.py`

#### Utility/Setup Scripts (KEEP IN ROOT or → utilities)
- `edit_ibm_account.py`
- `fix_instance_crn.py`
- `check_backend_queue.py`
- `monitor_queue.py`
- `schedule_experiment.py`

#### Experimental Scripts (→ 06_Testing_Scripts)
- `run_threshold_experiment.py`
- `check_actual_tdepth.py`
- `che_bfv.py`

---

### 2. Markdown Documentation (26 files)

#### Main Documentation (KEEP IN ROOT)
- `README.md` - Main project readme
- `QUICK_START.md` - Quick start guide
- `hardware_noise_results_table.md` - **RECENT** results table

#### Execution Guides (→ 07_Quick_Guides)
- `README_EXECUTION.md`
- `README_IBM_EXPERIMENT.md`
- `ALL_CONFIGS_GUIDE.md`
- `HARDWARE_EXECUTION_COMMANDS.sh` (shell script, see below)

#### Results/Analysis Documentation (→ 05_Results_Analysis)
- `AUX_QHE_5Q_2T_EXPERIMENTAL_RESULTS.md`
- `EXPERIMENTAL_RESULTS_ANALYSIS_20251027.md`
- `HARDWARE_RESULTS_SUMMARY.md`
- `EXECUTION_SUMMARY.md`
- `CORRECTED_METRICS_TABLE.md`

#### Debug/Fix Documentation (→ 02_Implementation_Fixes)
- `DEBUG_SUMMARY_2025_10_27.md`
- `FINAL_FIX_5q2t.md`
- `METRICS_BUG_FIX_EXPLANATION.md`

#### IBM Account Setup (→ 07_Quick_Guides)
- `IBM_DEPLOYMENT_GUIDE_INDEX.md`
- `QUICK_FIX_ACCOUNT.md`
- `TEST_NEW_ACCOUNT.md`
- `UPDATE_IBM_ACCOUNT_GUIDE.md`
- `CORRECT_CRN_FORMAT.md`

#### Pre-Execution Validation (→ 07_Quick_Guides)
- `PRE_EXECUTION_CHECKLIST.md`
- `PRE_EXECUTION_VALIDATION_REPORT.md`
- `FINAL_PRE_EXECUTION_REPORT.md`

#### Organization Documentation (→ 03_Cleanup_Archive)
- `COMPLETE_ORGANIZATION_PLAN.md`
- `FINAL_ORGANIZATION_SUMMARY.md`
- `ORGANIZATION_COMPLETE.md`
- `DOCUMENTATION_INDEX.md`

---

### 3. Shell Scripts (5 files)

#### Execution Scripts (KEEP IN ROOT or → scripts/)
- `EXECUTE_4Q_3T.sh`
- `EXECUTE_5Q_2T.sh`
- `EXECUTE_5Q_3T.sh`
- `EXECUTE_ALL_CONFIGS.sh`
- `HARDWARE_EXECUTION_COMMANDS.sh`

---

### 4. Result Data Files (42 JSON files)

#### Final Results (→ results/final/)
- `ibm_noise_measurement_results_20251030_221640.json` (5q-3t)
- `ibm_noise_measurement_results_20251030_222406.json` (5q-3t)
- `ibm_noise_measurement_results_20251030_224547.json` (5q-3t) **USED IN TABLE**
- `ibm_noise_measurement_results_20251030_230404.json` (5q-3t)
- `ibm_noise_measurement_results_20251030_230642.json` (4q-3t) **USED IN TABLE**
- `ibm_noise_measurement_results_20251030_231319.json` (5q-2t) **USED IN TABLE**

#### Interim Results (→ results/interim/)
All `ibm_noise_results_interim_*.json` files (36 files)

---

### 5. LaTeX/Documents (3 files)

#### Paper Materials (→ Papers/ or keep in root)
- `LATEX_TABLES_FOR_PAPER.tex`
- `Quantum Feature.docx`
- `Sequence Pair.docx`

---

### 6. Jupyter Notebooks (2 files)

#### Research Notebooks (→ algorithm/ or new notebooks/)
- `Active_QEC-QHE.ipynb`
- `FHE-AUX-QHE.ipynb`

---

### 7. Other Files (2 files)

#### Metadata/Logs (→ 03_Cleanup_Archive)
- `FILES_CREATED.txt`
- `FILES_SUMMARY.txt`
- `trace_corrected.txt`

---

## Recommended Organization Actions

### Priority 1: Move Debug/Test Scripts
```bash
# Move to debug_scripts/
mv CRITICAL_DEBUG_5q2t.py diagnose_*.py compare_local_vs_hardware.py debug_scripts/

# Move to 06_Testing_Scripts/
mv test_*.py verify_*.py VERIFY_*.py validate_*.py quick_test.py 06_Testing_Scripts/
```

### Priority 2: Organize Result Files
```bash
# Keep most recent final results
mkdir -p results/final
mv ibm_noise_measurement_results_20251030_224547.json results/final/  # 5q-3t
mv ibm_noise_measurement_results_20251030_230642.json results/final/  # 4q-3t
mv ibm_noise_measurement_results_20251030_231319.json results/final/  # 5q-2t

# Archive older final results
mkdir -p results/archive
mv ibm_noise_measurement_results_*.json results/archive/

# Move interim results
mkdir -p results/interim
mv ibm_noise_results_interim_*.json results/interim/
```

### Priority 3: Organize Scripts by Function
```bash
# Create scripts/ subdirectory
mkdir -p scripts/analysis scripts/tables scripts/utilities

# Move analysis scripts
mv analyze_*.py display_hardware_results.py scripts/analysis/

# Move table generation scripts
mv generate_*.py *_table.py scripts/tables/

# Move utilities
mv edit_ibm_account.py fix_instance_crn.py check_backend_queue.py monitor_queue.py schedule_experiment.py scripts/utilities/

# Move visualization
mkdir -p scripts/visualization
mv visualize_*.py scripts/visualization/
```

### Priority 4: Organize Documentation
```bash
# Move execution guides
mv README_EXECUTION.md README_IBM_EXPERIMENT.md ALL_CONFIGS_GUIDE.md 07_Quick_Guides/

# Move results documentation
mv AUX_QHE_5Q_2T_EXPERIMENTAL_RESULTS.md EXPERIMENTAL_RESULTS_ANALYSIS_*.md HARDWARE_RESULTS_SUMMARY.md EXECUTION_SUMMARY.md CORRECTED_METRICS_TABLE.md 05_Results_Analysis/

# Move debug/fix docs
mv DEBUG_SUMMARY_*.md FINAL_FIX_*.md METRICS_BUG_FIX_EXPLANATION.md 02_Implementation_Fixes/

# Move IBM setup guides
mv QUICK_FIX_ACCOUNT.md TEST_NEW_ACCOUNT.md UPDATE_IBM_ACCOUNT_GUIDE.md CORRECT_CRN_FORMAT.md IBM_DEPLOYMENT_GUIDE_INDEX.md 07_Quick_Guides/

# Move pre-execution docs
mv PRE_EXECUTION_*.md FINAL_PRE_EXECUTION_REPORT.md 07_Quick_Guides/

# Archive organization docs
mv COMPLETE_ORGANIZATION_PLAN.md FINAL_ORGANIZATION_SUMMARY.md ORGANIZATION_COMPLETE.md DOCUMENTATION_INDEX.md 03_Cleanup_Archive/
```

### Priority 5: Handle Execution Scripts
```bash
# Option A: Keep in root (they're used frequently)
# Option B: Create scripts/execution/
mkdir -p scripts/execution
mv EXECUTE_*.sh HARDWARE_EXECUTION_COMMANDS.sh scripts/execution/
```

### Priority 6: Other Files
```bash
# Move research notebooks
mkdir -p notebooks
mv *.ipynb notebooks/

# Archive metadata
mv FILES_*.txt trace_corrected.txt 03_Cleanup_Archive/
```

---

## Files to KEEP in Root Directory

1. **Essential Scripts:**
   - `ibm_hardware_noise_experiment.py` - Main execution script
   - `test_hardware_script_local.py` - Local validation

2. **Key Documentation:**
   - `README.md` - Main readme
   - `QUICK_START.md` - Quick start
   - `hardware_noise_results_table.md` - Recent results table

3. **Possibly Execution Scripts (if frequently used):**
   - `EXECUTE_*.sh` scripts
   - OR move to scripts/execution/

4. **Paper Materials (if actively editing):**
   - `LATEX_TABLES_FOR_PAPER.tex`

---

## Summary

**Total files to organize:** ~115 files

**Suggested new structure:**
- Root: 3-8 essential files only
- `debug_scripts/`: All debug scripts (already done ✅)
- `scripts/`: All utility/analysis/table generation scripts
- `results/`: All result JSON files organized by type
- `notebooks/`: Jupyter notebooks
- Existing organized folders: Move relevant docs/scripts

Would you like me to execute any of these organization actions?
