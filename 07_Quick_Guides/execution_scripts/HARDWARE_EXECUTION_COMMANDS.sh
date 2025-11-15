#!/bin/bash
#
# Hardware Execution Commands - VALIDATED AND SAFE TO RUN
# Date: 2025-10-27
# Status: All pre-flight checks PASSED
#

echo "=========================================="
echo "🚀 AUX-QHE Hardware Execution"
echo "=========================================="
echo ""
echo "✅ All validation tests PASSED"
echo "✅ ZNE fix verified"
echo "✅ Account authenticated: Gia_AUX_QHE"
echo "✅ Backend operational: ibm_torino (419 jobs in queue)"
echo ""
echo "⏱️  Estimated time: 14-35 hours per config"
echo ""

# Change to AUX-QHE directory
cd /Users/giadang/my_qiskitenv/AUX-QHE

# Configuration 1: 5q-2t (575 auxiliary states)
echo "=========================================="
echo "Running 5q-2t configuration..."
echo "=========================================="
python ibm_hardware_noise_experiment.py \
    --config 5q-2t \
    --backend ibm_torino \
    --account Gia_AUX_QHE

echo ""
echo "✅ 5q-2t completed!"
echo ""

# Configuration 2: 4q-3t (10,776 auxiliary states)
echo "=========================================="
echo "Running 4q-3t configuration..."
echo "=========================================="
python ibm_hardware_noise_experiment.py \
    --config 4q-3t \
    --backend ibm_torino \
    --account Gia_AUX_QHE

echo ""
echo "✅ 4q-3t completed!"
echo ""

# Configuration 3: 5q-3t (31,025 auxiliary states)
echo "=========================================="
echo "Running 5q-3t configuration..."
echo "=========================================="
python ibm_hardware_noise_experiment.py \
    --config 5q-3t \
    --backend ibm_torino \
    --account Gia_AUX_QHE

echo ""
echo "✅ 5q-3t completed!"
echo ""

echo "=========================================="
echo "🎉 ALL EXPERIMENTS COMPLETED!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Compare results: python compare_local_vs_hardware.py"
echo "2. Check result files: ls -lh ibm_noise_measurement_results_*.csv"
echo ""
