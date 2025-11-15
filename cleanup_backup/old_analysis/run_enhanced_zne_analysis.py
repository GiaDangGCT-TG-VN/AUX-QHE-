#!/usr/bin/env python3
"""
Run Enhanced ZNE Analysis for AUX-QHE Algorithm
Maximizes noise mitigation using performance table attributes

This script runs comprehensive ZNE optimization specifically tuned for your
AUX-QHE algorithm characteristics and performance requirements.
"""

import logging
import time
from qiskit_ibm_runtime import QiskitRuntimeService
from bfv_core import initialize_bfv_params
from key_generation import aux_keygen
from enhanced_zne_optimization import run_enhanced_zne_analysis
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Run comprehensive enhanced ZNE analysis for AUX-QHE."""
    
    print("🚀 Enhanced ZNE Optimization for AUX-QHE Algorithm")
    print("=" * 70)
    
    # Step 1: Initialize BFV parameters
    print("\\n📋 Step 1: Initializing BFV Parameters")
    params, encoder, encryptor, decryptor, evaluator = initialize_bfv_params()
    poly_degree = params.poly_degree
    print(f"✅ BFV initialized: polynomial degree={poly_degree}")
    
    # Step 2: Connect to IBM Quantum Backend
    print("\\n🔗 Step 2: Connecting to IBM Quantum Backend")
    try:
        service = QiskitRuntimeService()
        backend = service.least_busy(operational=True, simulator=False)
        print(f"✅ Using backend: {backend.name} ({backend.configuration().n_qubits} qubits)")
    except Exception as e:
        print(f"❌ Backend connection failed: {e}")
        return
    
    # Step 3: Define test configurations based on your algorithm performance
    print("\\n🧪 Step 3: Defining Test Configurations")
    
    # Based on your performance table, focus on configurations with heavy noise impact
    test_configs = [
        # (qubits, t_depth) - Start with configurations showing significant noise
        (3, 2),  # Baseline configuration
        (3, 3),  # Higher T-depth = more noise
        (4, 2),  # More qubits = more noise
        (4, 3),  # Complex configuration
        (5, 2),  # Maximum complexity from your tests
    ]
    
    print(f"Test configurations: {test_configs}")
    print(f"Total tests: {len(test_configs)} configurations")
    
    # Step 4: Run Enhanced ZNE Analysis
    print("\\n🎯 Step 4: Running Enhanced ZNE Analysis")
    print("This will execute multiple noise levels per configuration...")
    
    start_time = time.perf_counter()
    
    try:
        results = run_enhanced_zne_analysis(
            backend=backend,
            test_configs=test_configs,
            encryptor=encryptor,
            decryptor=decryptor,
            encoder=encoder,
            evaluator=evaluator,
            poly_degree=poly_degree
        )
        
        analysis_time = time.perf_counter() - start_time
        
        # Step 5: Detailed Results Analysis
        print(f"\\n📊 Step 5: Enhanced ZNE Results Analysis")
        print(f"Analysis completed in {analysis_time:.2f} seconds")
        
        if results:
            # Calculate comprehensive statistics
            improvements = [r['fidelity_improvement_percent'] for r in results]
            tvd_reductions = [r['tvd_reduction_percent'] for r in results]
            confidences = [r['extrapolation_confidence'] for r in results]
            
            print(f"\\n=== ZNE Enhancement Statistics ===")
            print(f"📈 Fidelity Improvements:")
            print(f"   Average: {np.mean(improvements):.2f}%")
            print(f"   Best: {np.max(improvements):.2f}%")
            print(f"   Range: {np.min(improvements):.2f}% - {np.max(improvements):.2f}%")
            
            print(f"\\n📉 Noise Reduction (TVD):")
            print(f"   Average reduction: {np.mean(tvd_reductions):.2f}%")
            print(f"   Best reduction: {np.max(tvd_reductions):.2f}%")
            
            print(f"\\n🎯 ZNE Model Confidence:")
            print(f"   Average R²: {np.mean(confidences):.3f}")
            print(f"   Best fit: {np.max(confidences):.3f}")
            
            # Identify best performing configuration
            best_idx = np.argmax(improvements)
            best_config = results[best_idx]
            
            print(f"\\n🏆 Best ZNE Performance:")
            print(f"   Configuration: {best_config['num_qubits']} qubits, T-depth {best_config['t_depth']}")
            print(f"   Fidelity improvement: {best_config['fidelity_improvement_percent']:.2f}%")
            print(f"   Baseline: {best_config['fidelity_baseline']:.4f} → ZNE: {best_config['fidelity_zne']:.4f}")
            print(f"   Extrapolation model: {best_config['extrapolation_model']}")
            print(f"   Model confidence (R²): {best_config['extrapolation_confidence']:.3f}")
            
            # Configuration-specific analysis
            print(f"\\n📋 Configuration-Specific Analysis:")
            for i, result in enumerate(results):
                config = test_configs[i]
                print(f"   {config[0]}q, T{config[1]}: {result['fidelity_improvement_percent']:.1f}% improvement, "
                      f"{result['extrapolation_model']} model")
            
            # Hardware efficiency metrics
            efficiencies = [r['hardware_efficiency'] for r in results]
            print(f"\\n⚡ Hardware Execution Efficiency:")
            print(f"   Average success rate: {np.mean(efficiencies):.1%}")
            print(f"   Total quantum shots used: {sum(r['total_shots'] for r in results)}")
            
            # Recommendations
            print(f"\\n💡 ZNE Optimization Recommendations:")
            
            if np.mean(improvements) > 10:
                print("   ✅ ZNE is highly effective for your AUX-QHE algorithm")
                print("   ✅ Consider using ZNE for all hardware executions")
            elif np.mean(improvements) > 5:
                print("   ⚠️  ZNE provides moderate improvement")
                print("   ⚠️  Consider ZNE for critical computations only")
            else:
                print("   ❌ ZNE shows limited effectiveness")
                print("   ❌ May need different error mitigation strategies")
            
            # Best model type recommendation
            model_counts = {}
            for r in results:
                model = r['extrapolation_model']
                model_counts[model] = model_counts.get(model, 0) + 1
            
            best_model = max(model_counts.items(), key=lambda x: x[1])[0]
            print(f"   🎯 Recommended extrapolation model: {best_model}")
            
            print(f"\\n🎉 Enhanced ZNE Analysis Complete!")
            print(f"Your AUX-QHE algorithm can achieve up to {np.max(improvements):.1f}% fidelity improvement with ZNE!")
            
        else:
            print("❌ No successful ZNE results obtained")
            print("Check backend connectivity and circuit configuration")
    
    except Exception as e:
        logger.error(f"Enhanced ZNE analysis failed: {e}")
        print(f"❌ Analysis failed: {e}")

if __name__ == "__main__":
    main()