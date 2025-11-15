# AUX-QHE Comprehensive Analysis Report

Generated: 2025-09-10 15:25:37
Total Analysis Time: 0.34s

## Summary

### Mock Algorithm Performance
- Analysis Time: 0.34s
- Configurations Tested: 4
- Tables Generated: 5

## Files Generated
- noise_error_metrics.py - Unified noise analysis module
- algorithm_performance_mock.py - Mock BFV performance module
- algorithm_performance_hardware.py - Hardware performance module
- unified_aux_qhe_analysis.py - Master controller (this file)

## Visualizations Generated
- optimization_levels_analysis_mock.png\n- auxiliary_states_growth_mock.png\n- performance_breakdown_mock.png\n- hardware_performance_analysis.png\n- noise_metrics_comprehensive.png\n
## Cleanup Recommendations
The following original files can be removed as they are now consolidated:
- comprehensive_analysis.py (functionality moved to unified modules)
- progressive_tester.py (integrated into algorithm_performance_hardware.py)
- safe_limits_config.py (integrated into algorithm_performance_hardware.py)
- jupyter_safe_run.py (functionality distributed across modules)

## Usage
Use this unified system with:
```bash
python unified_aux_qhe_analysis.py --mode [mock|hardware|both] [options]
```
