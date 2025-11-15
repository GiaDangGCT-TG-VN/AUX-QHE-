# File Organization Plan (No Execution)

This document shows the complete organization plan for all 119 files.

---

## PROPOSED FOLDER STRUCTURE

```
AUX-QHE/
│
├── README.md                              ← KEEP
├── QUICK_START.md                         ← KEEP
├── hardware_noise_results_table.md        ← KEEP
├── ibm_hardware_noise_experiment.py       ← KEEP (MAIN SCRIPT)
├── test_hardware_script_local.py          ← KEEP (MAIN VALIDATION)
│
├── core/                                  ← Already organized ✅
│   ├── bfv_core.py
│   ├── circuit_evaluation.py
│   ├── key_generation.py
│   ├── openqasm3_integration.py
│   ├── qotp_crypto.py
│   └── t_gate_gadgets.py
│
├── results/
│   ├── final_latest/
│   │   ├── 5q-2t_2025_10_30.json
│   │   ├── 4q-3t_2025_10_30.json
│   │   └── 5q-3t_2025_10_30.json
│   ├── archive_runs/
│   │   ├── [3 older final result files]
│   └── interim_autosave/
│       └── [36 interim files]
│
├── tests/
│   ├── core/
│   │   ├── verify_qotp_theory.py
│   │   ├── verify_shared_keys_fix.py
│   │   ├── VERIFY_CIRCUIT_FIX.py
│   │   └── verify_circuit_description.py
│   ├── hardware/
│   │   ├── test_ibm_connection.py
│   │   ├── validate_fixes.py
│   │   ├── validate_zne_fix.py
│   │   └── test_zne_fix_sxdg.py
│   ├── pipeline/
│   │   ├── test_local_full_pipeline.py
│   │   ├── test_noise_experiment_local.py
│   │   └── quick_test.py
│   └── tdepth/
│       ├── test_tdepth.py
│       ├── test_tdepth_fix.py
│       └── test_tdepth_fix_quick.py
│
├── debug_scripts/                         ← Already organized ✅
│   ├── CRITICAL_DEBUG_5q2t.py
│   ├── diagnose_fidelity_issue.py
│   ├── diagnose_metrics.py
│   ├── compare_local_vs_hardware.py
│   └── [9 more debug files]
│
├── analysis/
│   ├── analyze_ibm_noise_results.py
│   ├── analyze_circuit_complexity_vs_noise.py
│   └── compare_local_vs_hardware.py
│
├── tables/
│   ├── generate_hardware_table.py
│   ├── generate_latex_tables.py
│   ├── generate_results_table.py
│   ├── generate_compact_table.py
│   ├── generate_auxiliary_analysis_table.py
│   ├── add_5q2t_to_hardware_table.py
│   └── update_5q2t_hardware_table.py
│
├── visualization/
│   ├── visualize_aux_qhe_circuits.py
│   ├── visualize_aux_qhe_protocol.py
│   └── display_hardware_results.py
│
├── utilities/
│   ├── check_backend_queue.py
│   ├── monitor_queue.py
│   ├── schedule_experiment.py
│   ├── edit_ibm_account.py
│   ├── fix_instance_crn.py
│   ├── check_actual_tdepth.py
│   └── run_threshold_experiment.py
│
├── config/
│   ├── che_bfv.py
│   └── quick_update_aux_states.py
│
├── scripts/
│   ├── EXECUTE_5Q_2T.sh
│   ├── EXECUTE_4Q_3T.sh
│   ├── EXECUTE_5Q_3T.sh
│   ├── EXECUTE_ALL_CONFIGS.sh
│   └── HARDWARE_EXECUTION_COMMANDS.sh
│
├── docs/
│   ├── guides/
│   │   ├── README_EXECUTION.md
│   │   ├── README_IBM_EXPERIMENT.md
│   │   ├── ALL_CONFIGS_GUIDE.md
│   │   ├── PRE_EXECUTION_CHECKLIST.md
│   │   ├── PRE_EXECUTION_VALIDATION_REPORT.md
│   │   └── FINAL_PRE_EXECUTION_REPORT.md
│   ├── ibm_setup/
│   │   ├── IBM_DEPLOYMENT_GUIDE_INDEX.md
│   │   ├── QUICK_FIX_ACCOUNT.md
│   │   ├── TEST_NEW_ACCOUNT.md
│   │   ├── UPDATE_IBM_ACCOUNT_GUIDE.md
│   │   └── CORRECT_CRN_FORMAT.md
│   ├── results/
│   │   ├── AUX_QHE_5Q_2T_EXPERIMENTAL_RESULTS.md
│   │   ├── EXPERIMENTAL_RESULTS_ANALYSIS_20251027.md
│   │   ├── HARDWARE_RESULTS_SUMMARY.md
│   │   ├── EXECUTION_SUMMARY.md
│   │   └── CORRECTED_METRICS_TABLE.md
│   ├── fixes/
│   │   ├── DEBUG_SUMMARY_2025_10_27.md
│   │   ├── FINAL_FIX_5q2t.md
│   │   └── METRICS_BUG_FIX_EXPLANATION.md
│   └── archive/
│       ├── COMPLETE_ORGANIZATION_PLAN.md
│       ├── FINAL_ORGANIZATION_SUMMARY.md
│       ├── ORGANIZATION_COMPLETE.md
│       ├── DOCUMENTATION_INDEX.md
│       ├── FILES_CREATED.txt
│       ├── FILES_SUMMARY.txt
│       └── trace_corrected.txt
│
├── notebooks/
│   ├── Active_QEC-QHE.ipynb
│   └── FHE-AUX-QHE.ipynb
│
├── papers/
│   ├── LATEX_TABLES_FOR_PAPER.tex
│   ├── Quantum Feature.docx
│   └── Sequence Pair.docx
│
└── [Existing organized folders - keep as is]
    ├── 01_Hardware_Debug/
    ├── 02_Implementation_Fixes/
    ├── 03_Cleanup_Archive/
    ├── 04_Theory_Architecture/
    ├── 05_Results_Analysis/
    ├── 06_Testing_Scripts/
    ├── 07_Quick_Guides/
    ├── algorithm/
    ├── performance/
    ├── qasm3_exports/
    ├── circuit_diagrams/
    ├── debug_output/
    └── OLD_RESULTS_ARCHIVE/
```

---

## DETAILED FILE MAPPING

### ROOT DIRECTORY (Keep 5 files)
```
Current Location → New Location
----------------------------------------
README.md                              → ROOT (keep)
QUICK_START.md                         → ROOT (keep)
hardware_noise_results_table.md        → ROOT (keep)
ibm_hardware_noise_experiment.py       → ROOT (keep)
test_hardware_script_local.py          → ROOT (keep)
```

---

### RESULTS DATA (42 JSON files)

#### Final Latest Results (3 files - MOST IMPORTANT)
```
Current Location → New Location
----------------------------------------
ibm_noise_measurement_results_20251030_231319.json → results/final_latest/5q-2t_2025_10_30.json
ibm_noise_measurement_results_20251030_230642.json → results/final_latest/4q-3t_2025_10_30.json
ibm_noise_measurement_results_20251030_224547.json → results/final_latest/5q-3t_2025_10_30.json
```

#### Archived Final Results (3 files)
```
Current Location → New Location
----------------------------------------
ibm_noise_measurement_results_20251030_221640.json → results/archive_runs/5q-3t_run1.json
ibm_noise_measurement_results_20251030_222406.json → results/archive_runs/5q-3t_run2.json
ibm_noise_measurement_results_20251030_230404.json → results/archive_runs/5q-3t_run3.json
```

#### Interim Results (36 files - can be archived or deleted)
```
Current Location → New Location
----------------------------------------
ibm_noise_results_interim_20251030_221552.json → results/interim_autosave/
ibm_noise_results_interim_20251030_221613.json → results/interim_autosave/
ibm_noise_results_interim_20251030_221620.json → results/interim_autosave/
ibm_noise_results_interim_20251030_221640.json → results/interim_autosave/
ibm_noise_results_interim_20251030_222318.json → results/interim_autosave/
ibm_noise_results_interim_20251030_222339.json → results/interim_autosave/
ibm_noise_results_interim_20251030_222347.json → results/interim_autosave/
ibm_noise_results_interim_20251030_222405.json → results/interim_autosave/
ibm_noise_results_interim_20251030_224457.json → results/interim_autosave/
ibm_noise_results_interim_20251030_224518.json → results/interim_autosave/
ibm_noise_results_interim_20251030_224525.json → results/interim_autosave/
ibm_noise_results_interim_20251030_224547.json → results/interim_autosave/
ibm_noise_results_interim_20251030_230317.json → results/interim_autosave/
ibm_noise_results_interim_20251030_230337.json → results/interim_autosave/
ibm_noise_results_interim_20251030_230344.json → results/interim_autosave/
ibm_noise_results_interim_20251030_230404.json → results/interim_autosave/
ibm_noise_results_interim_20251030_230554.json → results/interim_autosave/
ibm_noise_results_interim_20251030_230613.json → results/interim_autosave/
ibm_noise_results_interim_20251030_230621.json → results/interim_autosave/
ibm_noise_results_interim_20251030_230642.json → results/interim_autosave/
ibm_noise_results_interim_20251030_231233.json → results/interim_autosave/
ibm_noise_results_interim_20251030_231254.json → results/interim_autosave/
ibm_noise_results_interim_20251030_231301.json → results/interim_autosave/
ibm_noise_results_interim_20251030_231319.json → results/interim_autosave/
[... 12 more interim files]
```

---

### TESTING SCRIPTS (15 files)

#### Core Algorithm Tests (4 files)
```
Current Location → New Location
----------------------------------------
verify_qotp_theory.py           → tests/core/verify_qotp_theory.py
verify_shared_keys_fix.py       → tests/core/verify_shared_keys_fix.py
VERIFY_CIRCUIT_FIX.py          → tests/core/VERIFY_CIRCUIT_FIX.py
verify_circuit_description.py   → tests/core/verify_circuit_description.py
```

#### Hardware Tests (4 files)
```
Current Location → New Location
----------------------------------------
test_ibm_connection.py  → tests/hardware/test_ibm_connection.py
validate_fixes.py       → tests/hardware/validate_fixes.py
validate_zne_fix.py     → tests/hardware/validate_zne_fix.py
test_zne_fix_sxdg.py   → tests/hardware/test_zne_fix_sxdg.py
```

#### Pipeline Tests (3 files)
```
Current Location → New Location
----------------------------------------
test_local_full_pipeline.py     → tests/pipeline/test_local_full_pipeline.py
test_noise_experiment_local.py  → tests/pipeline/test_noise_experiment_local.py
quick_test.py                   → tests/pipeline/quick_test.py
```

#### T-depth Tests (4 files)
```
Current Location → New Location
----------------------------------------
test_tdepth.py           → tests/tdepth/test_tdepth.py
test_tdepth_fix.py       → tests/tdepth/test_tdepth_fix.py
test_tdepth_fix_quick.py → tests/tdepth/test_tdepth_fix_quick.py
```

---

### ANALYSIS SCRIPTS (3 files)
```
Current Location → New Location
----------------------------------------
analyze_ibm_noise_results.py           → analysis/analyze_ibm_noise_results.py
analyze_circuit_complexity_vs_noise.py → analysis/analyze_circuit_complexity_vs_noise.py
compare_local_vs_hardware.py          → analysis/compare_local_vs_hardware.py
```

---

### TABLE GENERATION SCRIPTS (7 files)
```
Current Location → New Location
----------------------------------------
generate_hardware_table.py             → tables/generate_hardware_table.py
generate_latex_tables.py              → tables/generate_latex_tables.py
generate_results_table.py             → tables/generate_results_table.py
generate_compact_table.py             → tables/generate_compact_table.py
generate_auxiliary_analysis_table.py  → tables/generate_auxiliary_analysis_table.py
add_5q2t_to_hardware_table.py        → tables/add_5q2t_to_hardware_table.py
update_5q2t_hardware_table.py        → tables/update_5q2t_hardware_table.py
```

---

### VISUALIZATION SCRIPTS (3 files)
```
Current Location → New Location
----------------------------------------
visualize_aux_qhe_circuits.py  → visualization/visualize_aux_qhe_circuits.py
visualize_aux_qhe_protocol.py  → visualization/visualize_aux_qhe_protocol.py
display_hardware_results.py    → visualization/display_hardware_results.py
```

---

### UTILITY SCRIPTS (7 files)
```
Current Location → New Location
----------------------------------------
check_backend_queue.py     → utilities/check_backend_queue.py
monitor_queue.py          → utilities/monitor_queue.py
schedule_experiment.py    → utilities/schedule_experiment.py
edit_ibm_account.py       → utilities/edit_ibm_account.py
fix_instance_crn.py       → utilities/fix_instance_crn.py
check_actual_tdepth.py    → utilities/check_actual_tdepth.py
run_threshold_experiment.py → utilities/run_threshold_experiment.py
```

---

### CONFIG/SETUP (2 files)
```
Current Location → New Location
----------------------------------------
che_bfv.py                → config/che_bfv.py
quick_update_aux_states.py → config/quick_update_aux_states.py
```

---

### EXECUTION SCRIPTS (5 shell files)
```
Current Location → New Location
----------------------------------------
EXECUTE_5Q_2T.sh               → scripts/EXECUTE_5Q_2T.sh
EXECUTE_4Q_3T.sh               → scripts/EXECUTE_4Q_3T.sh
EXECUTE_5Q_3T.sh               → scripts/EXECUTE_5Q_3T.sh
EXECUTE_ALL_CONFIGS.sh         → scripts/EXECUTE_ALL_CONFIGS.sh
HARDWARE_EXECUTION_COMMANDS.sh → scripts/HARDWARE_EXECUTION_COMMANDS.sh
```

---

### DOCUMENTATION (29 files)

#### Execution Guides (6 files)
```
Current Location → New Location
----------------------------------------
README_EXECUTION.md                    → docs/guides/README_EXECUTION.md
README_IBM_EXPERIMENT.md              → docs/guides/README_IBM_EXPERIMENT.md
ALL_CONFIGS_GUIDE.md                  → docs/guides/ALL_CONFIGS_GUIDE.md
PRE_EXECUTION_CHECKLIST.md            → docs/guides/PRE_EXECUTION_CHECKLIST.md
PRE_EXECUTION_VALIDATION_REPORT.md    → docs/guides/PRE_EXECUTION_VALIDATION_REPORT.md
FINAL_PRE_EXECUTION_REPORT.md         → docs/guides/FINAL_PRE_EXECUTION_REPORT.md
```

#### IBM Setup Guides (5 files)
```
Current Location → New Location
----------------------------------------
IBM_DEPLOYMENT_GUIDE_INDEX.md  → docs/ibm_setup/IBM_DEPLOYMENT_GUIDE_INDEX.md
QUICK_FIX_ACCOUNT.md          → docs/ibm_setup/QUICK_FIX_ACCOUNT.md
TEST_NEW_ACCOUNT.md           → docs/ibm_setup/TEST_NEW_ACCOUNT.md
UPDATE_IBM_ACCOUNT_GUIDE.md   → docs/ibm_setup/UPDATE_IBM_ACCOUNT_GUIDE.md
CORRECT_CRN_FORMAT.md         → docs/ibm_setup/CORRECT_CRN_FORMAT.md
```

#### Results Documentation (5 files)
```
Current Location → New Location
----------------------------------------
AUX_QHE_5Q_2T_EXPERIMENTAL_RESULTS.md    → docs/results/AUX_QHE_5Q_2T_EXPERIMENTAL_RESULTS.md
EXPERIMENTAL_RESULTS_ANALYSIS_20251027.md → docs/results/EXPERIMENTAL_RESULTS_ANALYSIS_20251027.md
HARDWARE_RESULTS_SUMMARY.md              → docs/results/HARDWARE_RESULTS_SUMMARY.md
EXECUTION_SUMMARY.md                     → docs/results/EXECUTION_SUMMARY.md
CORRECTED_METRICS_TABLE.md               → docs/results/CORRECTED_METRICS_TABLE.md
```

#### Fix Documentation (3 files)
```
Current Location → New Location
----------------------------------------
DEBUG_SUMMARY_2025_10_27.md      → docs/fixes/DEBUG_SUMMARY_2025_10_27.md
FINAL_FIX_5q2t.md               → docs/fixes/FINAL_FIX_5q2t.md
METRICS_BUG_FIX_EXPLANATION.md  → docs/fixes/METRICS_BUG_FIX_EXPLANATION.md
```

#### Archive Documentation (7 files)
```
Current Location → New Location
----------------------------------------
COMPLETE_ORGANIZATION_PLAN.md   → docs/archive/COMPLETE_ORGANIZATION_PLAN.md
FINAL_ORGANIZATION_SUMMARY.md  → docs/archive/FINAL_ORGANIZATION_SUMMARY.md
ORGANIZATION_COMPLETE.md       → docs/archive/ORGANIZATION_COMPLETE.md
DOCUMENTATION_INDEX.md         → docs/archive/DOCUMENTATION_INDEX.md
FILES_CREATED.txt              → docs/archive/FILES_CREATED.txt
FILES_SUMMARY.txt              → docs/archive/FILES_SUMMARY.txt
trace_corrected.txt            → docs/archive/trace_corrected.txt
```

---

### NOTEBOOKS & PAPERS (5 files)
```
Current Location → New Location
----------------------------------------
Active_QEC-QHE.ipynb       → notebooks/Active_QEC-QHE.ipynb
FHE-AUX-QHE.ipynb         → notebooks/FHE-AUX-QHE.ipynb

LATEX_TABLES_FOR_PAPER.tex → papers/LATEX_TABLES_FOR_PAPER.tex
Quantum Feature.docx       → papers/Quantum Feature.docx
Sequence Pair.docx         → papers/Sequence Pair.docx
```

---

## SUMMARY

### Total Files: 119

**By Category:**
- Core Algorithm: 6 files (already organized ✅)
- Main Scripts (ROOT): 5 files (README + 2 main scripts + 2 guides)
- Results Data: 42 JSON files
- Testing Scripts: 15 Python files
- Debug Scripts: 13 Python files (already organized ✅)
- Analysis: 3 Python files
- Tables: 7 Python files
- Visualization: 3 Python files
- Utilities: 7 Python files
- Config: 2 Python files
- Execution: 5 shell scripts
- Documentation: 26 Markdown files + 3 text files
- Notebooks: 2 files
- Papers: 3 files

**Root Directory After Organization:**
- Only 5 essential files remain in root
- Everything else organized by function
- Clear, logical folder structure
- Easy to find and maintain files

---

## NOTES

1. **No files deleted** - Everything is preserved, just reorganized
2. **Core algorithm untouched** - The `core/` folder stays as-is
3. **Main scripts in root** - Easy access to primary execution scripts
4. **Results organized by recency** - Latest finals separate from archives
5. **Tests grouped by type** - Core, hardware, pipeline, T-depth
6. **Documentation categorized** - Guides, setup, results, fixes, archive

This plan is ready for execution when you approve.
