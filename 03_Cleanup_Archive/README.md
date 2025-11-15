# 03. Cleanup Archive Documentation

**Purpose:** File organization and cleanup records

## 🗑️ What Was Cleaned

**Total archived:** 63 files (52 MB)
- Oct 12 results: 36 files (wrong aux states)
- Oct 13 results: 17 files (wrong aux states)  
- Oct 23 intermediate: 4 files (superseded)
- Old CSV files: 7 files (superseded)

**Archived to:** OLD_RESULTS_ARCHIVE/

## 📄 Files

- **CLEANUP_PLAN.md** - Detailed cleanup plan
  - What files to archive
  - Why they're wrong
  - Execution commands

- **CLEANUP_SUMMARY.md** - Cleanup summary
  - What was cleaned
  - Final results remaining
  - Verification checklist

## ✅ Final Results (Kept)

1. ibm_noise_results_interim_20251023_232611.json (555K)
2. local_vs_hardware_comparison.csv (1.0K)
3. circuit_complexity_vs_noise_summary.csv (667B)
4. hardware_workflow_debug_report.json (3.5K)

## ⚠️ What NOT to Use

Files in OLD_RESULTS_ARCHIVE/:
- Have wrong aux states (1,350 vs 575)
- Contain synthetic cross-terms bug
- Superseded by Oct 23 corrected run

---

**Total Files:** 2
**Archive Size:** 52 MB
