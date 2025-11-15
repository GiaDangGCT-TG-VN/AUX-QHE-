#!/bin/bash
# Execute All 3 Configurations in Sequence
# Pre-validated - All tests passed
# Date: 2025-10-27

echo "================================================================================"
echo "🚀 AUX-QHE HARDWARE EXECUTION - ALL 3 CONFIGURATIONS"
echo "================================================================================"
echo ""
echo "This script will execute all 3 configurations in sequence:"
echo ""
echo "   1. 5q-2t (5 qubits, T-depth 2) - 575 aux states"
echo "   2. 4q-3t (4 qubits, T-depth 3) - 10,776 aux states"
echo "   3. 5q-3t (5 qubits, T-depth 3) - 31,025 aux states"
echo ""
echo "Backend: ibm_torino"
echo "Account: Gia_AUX_QHE"
echo "Shots per method: 1024"
echo "Methods per config: 4 (Baseline, ZNE, Opt-3, Opt-3+ZNE)"
echo ""
echo "Total expected runtime: ~80-115 minutes (plus queue waits)"
echo "Total expected credits: ~24 credits"
echo ""
echo "⚠️  This will execute on real quantum hardware and consume credits!"
echo "⚠️  Estimated queue wait: ~20-40 minutes per config (421 jobs ahead)"
echo ""
read -p "Press ENTER to start all 3 configs, or Ctrl+C to cancel..."

START_TIME=$(date +%s)

echo ""
echo "================================================================================"
echo "🔧 Activating virtual environment..."
echo "================================================================================"
cd /Users/giadang/my_qiskitenv
source bin/activate
cd AUX-QHE

# Track success/failure
declare -a RESULTS
TOTAL_CONFIGS=3
SUCCESS_COUNT=0
FAIL_COUNT=0

echo ""
echo "================================================================================"
echo "📋 CONFIGURATION 1/3: 5q-2t"
echo "================================================================================"
echo ""

./EXECUTE_5Q_2T.sh <<< ""

if [ $? -eq 0 ]; then
    RESULTS[0]="✅ 5q-2t: SUCCESS"
    ((SUCCESS_COUNT++))
else
    RESULTS[0]="❌ 5q-2t: FAILED"
    ((FAIL_COUNT++))
fi

echo ""
echo "================================================================================"
echo "⏸️  Pause between configs (30 seconds)..."
echo "================================================================================"
sleep 30

echo ""
echo "================================================================================"
echo "📋 CONFIGURATION 2/3: 4q-3t"
echo "================================================================================"
echo ""

./EXECUTE_4Q_3T.sh <<< ""

if [ $? -eq 0 ]; then
    RESULTS[1]="✅ 4q-3t: SUCCESS"
    ((SUCCESS_COUNT++))
else
    RESULTS[1]="❌ 4q-3t: FAILED"
    ((FAIL_COUNT++))
fi

echo ""
echo "================================================================================"
echo "⏸️  Pause between configs (30 seconds)..."
echo "================================================================================"
sleep 30

echo ""
echo "================================================================================"
echo "📋 CONFIGURATION 3/3: 5q-3t"
echo "================================================================================"
echo ""

./EXECUTE_5Q_3T.sh <<< ""

if [ $? -eq 0 ]; then
    RESULTS[2]="✅ 5q-3t: SUCCESS"
    ((SUCCESS_COUNT++))
else
    RESULTS[2]="❌ 5q-3t: FAILED"
    ((FAIL_COUNT++))
fi

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))
DURATION_MIN=$((DURATION / 60))
DURATION_SEC=$((DURATION % 60))

echo ""
echo "================================================================================"
echo "📊 ALL CONFIGURATIONS COMPLETE"
echo "================================================================================"
echo ""
echo "Total runtime: ${DURATION_MIN}m ${DURATION_SEC}s"
echo ""
echo "Results Summary:"
echo "   ${RESULTS[0]}"
echo "   ${RESULTS[1]}"
echo "   ${RESULTS[2]}"
echo ""
echo "Success: $SUCCESS_COUNT / $TOTAL_CONFIGS"
echo "Failed:  $FAIL_COUNT / $TOTAL_CONFIGS"
echo ""

if [ $SUCCESS_COUNT -eq $TOTAL_CONFIGS ]; then
    echo "🎉 ALL CONFIGURATIONS SUCCEEDED!"
    echo ""
    echo "📁 Result files generated:"
    echo ""
    ls -lt ibm_noise_measurement_results_*.csv 2>/dev/null | head -3
    echo ""
    echo "💡 Next steps:"
    echo "   1. Compare results: python compare_local_vs_hardware.py"
    echo "   2. Analyze ZNE improvements across all configs"
    echo "   3. Review final documentation"
elif [ $SUCCESS_COUNT -gt 0 ]; then
    echo "⚠️  PARTIAL SUCCESS ($SUCCESS_COUNT/$TOTAL_CONFIGS)"
    echo ""
    echo "💡 Review failed configurations and retry individually"
else
    echo "❌ ALL CONFIGURATIONS FAILED"
    echo ""
    echo "💡 Troubleshooting:"
    echo "   1. Check backend status"
    echo "   2. Verify account credentials"
    echo "   3. Review error messages above"
fi

echo ""
echo "================================================================================"
