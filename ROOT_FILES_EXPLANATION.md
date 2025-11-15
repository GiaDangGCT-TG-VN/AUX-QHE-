# Root Directory Files - Why They Stay

These 6 files are **intentionally kept in the ROOT** directory. They are the essential files users need immediate access to.

---

## ✅ Files That SHOULD Stay in Root

### 1. **README.md** ✅ KEEP
**Why:** Main project documentation - first file people see
**Purpose:**
- Project overview
- Installation instructions
- Quick reference
- Entry point for new users

**Usage:** `cat README.md` or view on GitHub

---

### 2. **QUICK_START.md** ✅ KEEP
**Why:** Fast onboarding for users
**Purpose:**
- Quick setup guide
- Essential commands
- Common workflows
- Troubleshooting basics

**Usage:** For users who want to get started immediately

---

### 3. **ibm_hardware_noise_experiment.py** ✅ KEEP (MAIN SCRIPT)
**Why:** **PRIMARY EXECUTION SCRIPT** - The main entry point
**Purpose:**
- Main hardware experiment execution
- Run AUX-QHE on IBM Quantum
- 4 error mitigation strategies
- All configurations (5q-2t, 4q-3t, 5q-3t)

**Usage:**
```bash
python ibm_hardware_noise_experiment.py --config 5q-2t --backend ibm_torino --account Gia_AUX_QHE
```

**This is THE script users run for experiments!**

---

### 4. **test_hardware_script_local.py** ✅ KEEP (MAIN VALIDATION)
**Why:** **PRIMARY VALIDATION SCRIPT** - Essential pre-flight check
**Purpose:**
- Local validation before hardware execution
- Prevent wasting IBM credits on bugs
- Verify full pipeline works
- Debug locally without hardware

**Usage:**
```bash
python test_hardware_script_local.py
```

**This is THE script users run before spending credits!**

---

### 5. **hardware_noise_results_table.md** ✅ KEEP (LATEST RESULTS)
**Why:** Most recent experimental results - quick reference
**Purpose:**
- Latest hardware results table
- LaTeX table for paper (ready to copy)
- Quick performance reference
- Active research document

**Usage:** Quick access to latest results without navigating folders

**Note:** This is an ACTIVE file you just created/updated!

---

### 6. **my_qiskitenv.code-workspace** ✅ KEEP (IDE CONFIG)
**Why:** VSCode workspace configuration
**Purpose:**
- VSCode project settings
- Editor configuration
- Workspace layout
- Development environment

**Usage:** Open with VSCode - `code my_qiskitenv.code-workspace`

**This is your IDE configuration file!**

---

## Why These 6 Files Stay in Root

### ✅ **Principle 1: Accessibility**
Users should find main scripts and docs immediately without navigating folders.

### ✅ **Principle 2: Convention**
Standard practice in software projects:
```
project/
├── README.md              # Standard location
├── main_script.py         # Main executable
├── config_file           # Configuration
└── organized_folders/    # Everything else
```

### ✅ **Principle 3: Workflow**
Common user workflow:
1. Read `README.md` → Understand project
2. Read `QUICK_START.md` → Get started fast
3. Run `test_hardware_script_local.py` → Validate locally
4. Run `ibm_hardware_noise_experiment.py` → Execute on hardware
5. Check `hardware_noise_results_table.md` → View results

**All in root = Easy workflow!**

### ✅ **Principle 4: Active vs Archive**
- **Root:** Active, frequently used files
- **Organized folders:** Supporting files, archives, utilities

---

## Comparison: Before vs After Organization

### BEFORE (Messy - 120+ files in root)
```
AUX-QHE/
├── README.md
├── ibm_hardware_noise_experiment.py
├── test_hardware_script_local.py
├── analyze_ibm_noise_results.py          ← Should be organized
├── generate_hardware_table.py            ← Should be organized
├── test_tdepth.py                        ← Should be organized
├── verify_qotp_theory.py                 ← Should be organized
├── ibm_noise_results_interim_*.json      ← Should be organized (36 files!)
├── debug_fidelity_issue.py               ← Should be organized
├── ... (110+ more files!)                ← TOO MANY!
```

### AFTER (Clean - 6 essential files)
```
AUX-QHE/
├── README.md                              ✅ Essential doc
├── QUICK_START.md                         ✅ Essential doc
├── ibm_hardware_noise_experiment.py       ✅ Main script
├── test_hardware_script_local.py          ✅ Main validation
├── hardware_noise_results_table.md        ✅ Latest results
├── my_qiskitenv.code-workspace            ✅ IDE config
│
└── [Everything else properly organized]
    ├── 05_Results_Analysis/               ← Analysis scripts
    ├── 06_Testing_Scripts/                ← Test scripts
    ├── results/                           ← Result data
    ├── debug_scripts/                     ← Debug scripts
    └── ...
```

---

## What If You Want Even Cleaner Root?

If you want ONLY 4 files in root (absolute minimum):

### Option 1: Move results table to results/
```bash
mv hardware_noise_results_table.md results/
# Pro: Even cleaner root
# Con: Less visible, harder to find latest results
```

### Option 2: Move workspace file
```bash
mv my_qiskitenv.code-workspace .vscode/
# Pro: Cleaner root
# Con: Non-standard location, might break VSCode
```

### Option 3: Keep current (RECOMMENDED)
```
Keep all 6 files in root - this is the industry standard!
```

---

## Industry Standards - What Other Projects Do

### Example: TensorFlow
```
tensorflow/
├── README.md                    ← In root
├── setup.py                     ← In root
├── LICENSE                      ← In root
└── tensorflow/                  ← Code organized
```

### Example: PyTorch
```
pytorch/
├── README.md                    ← In root
├── setup.py                     ← In root
├── torch/                       ← Code organized
└── docs/                        ← Docs organized
```

### Example: Qiskit
```
qiskit/
├── README.md                    ← In root
├── setup.py                     ← In root
├── qiskit/                      ← Code organized
└── test/                        ← Tests organized
```

**Pattern:** Essential files in root, everything else organized!

---

## Final Recommendation

✅ **KEEP ALL 6 FILES IN ROOT**

These files are:
1. **README.md** - Project documentation (standard)
2. **QUICK_START.md** - Quick reference (standard)
3. **ibm_hardware_noise_experiment.py** - Main executable (standard)
4. **test_hardware_script_local.py** - Main validation (standard)
5. **hardware_noise_results_table.md** - Latest results (convenient)
6. **my_qiskitenv.code-workspace** - IDE config (standard)

**This is a clean, professional project structure!**

---

## Summary

| File | Keep in Root? | Reason |
|------|--------------|--------|
| README.md | ✅ YES | Main documentation |
| QUICK_START.md | ✅ YES | Quick reference |
| ibm_hardware_noise_experiment.py | ✅ YES | Main script |
| test_hardware_script_local.py | ✅ YES | Main validation |
| hardware_noise_results_table.md | ✅ YES | Latest results |
| my_qiskitenv.code-workspace | ✅ YES | IDE config |

**Total in root: 6 files (down from 120+)**

✅ **This is EXCELLENT organization!**
