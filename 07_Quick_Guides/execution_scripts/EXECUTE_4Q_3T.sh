#!/bin/bash
# Hardware Execution Script for 4q-3t Configuration
# Pre-validated - All tests passed
# Date: 2025-10-27

echo "================================================================================"
echo "🚀 AUX-QHE HARDWARE EXECUTION - 4q-3t Configuration"
echo "================================================================================"
echo ""
echo "Backend: ibm_torino"
echo "Account: Gia_AUX_QHE"
echo "Shots: 1024"
echo "Methods: Baseline, ZNE, Opt-3, Opt-3+ZNE (4 total)"
echo ""
echo "Configuration Details:"
echo "   Qubits: 4"
echo "   T-depth: 3"
echo "   Aux states: 10,776 (more complex than 5q-2t)"
echo ""
echo "Expected runtime: ~25-35 minutes (plus queue wait)"
echo "Expected credits: ~8 credits"
echo ""
echo "⚠️  This will execute on real quantum hardware and consume credits!"
echo ""
read -p "Press ENTER to continue, or Ctrl+C to cancel..."

echo ""
echo "================================================================================"
echo "🔧 Activating virtual environment..."
echo "================================================================================"
cd /Users/giadang/my_qiskitenv
source bin/activate

echo ""
echo "================================================================================"
echo "📂 Navigating to AUX-QHE directory..."
echo "================================================================================"
cd AUX-QHE

echo ""
echo "================================================================================"
echo "🔍 Pre-flight check: Listing recent result files..."
echo "================================================================================"
echo ""
echo "Recent IBM result files:"
ls -lt ibm_noise_measurement_results_*.csv 2>/dev/null | head -5 || echo "   (No previous results found)"
echo ""

echo "================================================================================"
echo "🚀 EXECUTING HARDWARE RUN..."
echo "================================================================================"
echo ""
echo "Command:"
echo "   python ibm_hardware_noise_experiment.py --config 4q-3t --backend ibm_torino --account Gia_AUX_QHE"
echo ""

python ibm_hardware_noise_experiment.py --config 4q-3t --backend ibm_torino --account Gia_AUX_QHE

EXIT_CODE=$?

echo ""
echo "================================================================================"
echo "📊 EXECUTION COMPLETE"
echo "================================================================================"
echo ""
echo "Exit code: $EXIT_CODE"

if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ SUCCESS"
    echo ""
    echo "📁 Result files:"
    echo ""
    echo "Latest CSV:"
    ls -t ibm_noise_measurement_results_*.csv 2>/dev/null | head -1 || echo "   (Not found)"
    echo ""
    echo "Latest JSON:"
    ls -t ibm_noise_measurement_results_*.json 2>/dev/null | head -1 || echo "   (Not found)"
    echo ""
    echo "💡 Next steps:"
    echo "   1. Review results: cat ibm_noise_measurement_results_*.csv | tail -4"
    echo "   2. Run next config: ./EXECUTE_5Q_3T.sh"
    echo "   3. Compare all results: python compare_local_vs_hardware.py"
else
    echo "❌ FAILED"
    echo ""
    echo "💡 Troubleshooting:"
    echo "   1. Check error messages above"
    echo "   2. Verify backend status: python -c 'from qiskit_ibm_runtime import QiskitRuntimeService; s=QiskitRuntimeService(name=\"Gia_AUX_QHE\"); b=s.backend(\"ibm_torino\"); print(b.status())'"
    echo "   3. Check interim files for partial results: ls -lt ibm_noise_results_interim_*.json | head -1"
fi

echo ""
echo "================================================================================"
