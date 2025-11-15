"""
Unified AUX-QHE Analysis Master Controller

This is the main execution file that combines all 3 unified modules:
1. noise_error_metrics.py - Noise analysis, ZNE, fidelity metrics
2. algorithm_performance_mock.py - Mock BFV performance testing  
3. algorithm_performance_hardware.py - Real IBM hardware testing

Provides a single entry point for all AUX-QHE analysis with options for:
- Mock algorithm performance analysis
- Real hardware performance analysis  
- Comprehensive noise error metrics
- All 4 tables generation in one place
- Memory-safe progressive testing
- Visualization generation

Usage Examples:
    python unified_aux_qhe_analysis.py --mode mock --qubits 3,4 --tdepth 2,3
    python unified_aux_qhe_analysis.py --mode hardware --progressive --max-memory 30
    python unified_aux_qhe_analysis.py --mode both --visualizations
"""

import argparse
import logging
import time
import sys
from pathlib import Path

# Import unified modules
from noise_error_metrics import generate_noise_metrics_visualization
from algorithm_performance_mock import (
    generate_comprehensive_performance_tables as mock_tables,
    print_performance_table_only as print_mock_table,
    generate_performance_visualizations as mock_viz
)
from algorithm_performance_hardware import (
    run_progressive_hardware_analysis,
    print_hardware_table_only
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class UnifiedAUXQHEAnalyzer:
    """Master controller for all AUX-QHE analysis modes."""
    
    def __init__(self):
        self.mock_results = None
        self.hardware_results = None
        self.analysis_start_time = time.perf_counter()
        
    def run_mock_analysis(self, qubit_range, t_depth_range, visualizations=True):
        """
        Run comprehensive mock algorithm performance analysis.
        
        Args:
            qubit_range (list): Range of qubit counts to test.
            t_depth_range (list): Range of T-depths to test.
            visualizations (bool): Generate visualization diagrams.
        
        Returns:
            dict: Mock analysis results and tables.
        """
        logger.info("🧮 Starting Mock Algorithm Performance Analysis")
        print("=" * 70)
        print("🧮 MOCK BFV ALGORITHM PERFORMANCE ANALYSIS")
        print("=" * 70)
        
        # Generate comprehensive mock tables
        mock_start = time.perf_counter()
        tables = mock_tables(qubit_range, t_depth_range)
        mock_time = time.perf_counter() - mock_start
        
        if not tables:
            logger.error("Failed to generate mock performance tables")
            return None
        
        print(f"\\n✅ Mock analysis completed in {mock_time:.2f}s")
        print(f"   Generated {len(tables)} performance tables")
        print(f"   Test configurations: {len(qubit_range)} qubits × {len(t_depth_range)} T-depths")
        
        # Print main performance table
        print_mock_table(tables, 'table1_performance')
        
        # Generate visualizations if requested
        if visualizations:
            logger.info("Generating mock performance visualizations...")
            mock_viz(tables, save_dir="./")
            print("✅ Mock performance visualizations saved")
        
        self.mock_results = {
            'tables': tables,
            'analysis_time': mock_time,
            'config_count': len(qubit_range) * len(t_depth_range)
        }
        
        return self.mock_results
    
    def run_hardware_analysis(self, progressive=True, max_memory_gb=30, 
                             qubit_range=None, t_depth_range=None, visualizations=True):
        """
        Run comprehensive hardware performance analysis.
        
        Args:
            progressive (bool): Use progressive memory-safe testing.
            max_memory_gb (float): Maximum memory limit for progressive testing.
            qubit_range (list): Specific qubit range (if not progressive).
            t_depth_range (list): Specific T-depth range (if not progressive).
            visualizations (bool): Generate visualization diagrams.
        
        Returns:
            dict: Hardware analysis results and tables.
        """
        logger.info("🔧 Starting Hardware Algorithm Performance Analysis")
        print("=" * 70)
        print("🔧 REAL IBM HARDWARE PERFORMANCE ANALYSIS")
        print("=" * 70)
        
        hardware_start = time.perf_counter()
        
        if progressive:
            # Use progressive testing with memory safety
            results = run_progressive_hardware_analysis(
                max_memory_gb=max_memory_gb, 
                enable_htop=True
            )
        else:
            # Run specific configurations (would need implementation)
            logger.warning("Non-progressive hardware testing not yet implemented")
            logger.info("Falling back to progressive testing...")
            results = run_progressive_hardware_analysis(
                max_memory_gb=max_memory_gb, 
                enable_htop=False
            )
        
        hardware_time = time.perf_counter() - hardware_start
        
        if not results or not results.get('tables'):
            logger.error("Failed to generate hardware performance tables")
            return None
        
        print(f"\\n✅ Hardware analysis completed in {hardware_time:.2f}s")
        print(f"   Completed {results['completed_tests']}/{results['total_planned']} tests")
        print(f"   Generated {len(results['tables'])} hardware tables")
        
        # Print main hardware table
        if 'table1_hardware_noise' in results['tables']:
            print_hardware_table_only(results['tables'], 'table1_hardware_noise')
        
        # Generate hardware visualizations if requested
        if visualizations and results.get('results'):
            logger.info("Generating hardware performance visualizations...")
            self._generate_hardware_visualizations(results['results'])
            print("✅ Hardware performance visualizations saved")
        
        self.hardware_results = {
            'tables': results['tables'],
            'raw_results': results['results'],
            'analysis_time': hardware_time,
            'completed_tests': results['completed_tests'],
            'total_planned': results['total_planned'],
            'backend': results['analyzer'].backend.name if results['analyzer'].backend else 'Simulator'
        }
        
        return self.hardware_results
    
    def run_noise_analysis(self, results_data, save_visualizations=True):
        """
        Run comprehensive noise error metrics analysis.
        
        Args:
            results_data (list): List of analysis results for noise metrics.
            save_visualizations (bool): Save noise metrics visualizations.
        
        Returns:
            dict: Noise analysis results.
        """
        logger.info("📊 Starting Noise Error Metrics Analysis")
        print("=" * 70)
        print("📊 NOISE ERROR METRICS ANALYSIS")
        print("=" * 70)
        
        if not results_data:
            logger.warning("No results data provided for noise analysis")
            return None
        
        noise_start = time.perf_counter()
        
        # Generate noise metrics visualization
        if save_visualizations:
            generate_noise_metrics_visualization(
                results_data, 
                save_path="noise_metrics_comprehensive.png"
            )
        
        noise_time = time.perf_counter() - noise_start
        
        # Calculate noise statistics
        fidelities = [r.get('fidelity', 0) for r in results_data if 'fidelity' in r]
        tvds = [r.get('tvd', 1) for r in results_data if 'tvd' in r]
        
        noise_stats = {
            'avg_fidelity': sum(fidelities) / len(fidelities) if fidelities else 0,
            'min_fidelity': min(fidelities) if fidelities else 0,
            'max_fidelity': max(fidelities) if fidelities else 0,
            'avg_tvd': sum(tvds) / len(tvds) if tvds else 1,
            'min_tvd': min(tvds) if tvds else 1,
            'max_tvd': max(tvds) if tvds else 1,
            'analysis_time': noise_time,
            'sample_count': len(results_data)
        }
        
        print(f"\\n✅ Noise analysis completed in {noise_time:.2f}s")
        print(f"   Average fidelity: {noise_stats['avg_fidelity']:.4f}")
        print(f"   Average TVD: {noise_stats['avg_tvd']:.4f}")
        print(f"   Analyzed {noise_stats['sample_count']} configurations")
        
        return noise_stats
    
    def _generate_hardware_visualizations(self, hardware_results):
        """Generate hardware-specific visualizations."""
        try:
            import matplotlib.pyplot as plt
            import pandas as pd
            
            df = pd.DataFrame(hardware_results)
            
            # Hardware vs ZNE comparison
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
            fig.suptitle('Hardware Performance Analysis', fontsize=14, fontweight='bold')
            
            configs = [f"{row['num_qubits']}q,T{row['t_depth']}" for _, row in df.iterrows()]
            
            # Fidelity comparison
            x = range(len(configs))
            ax1.bar([i-0.2 for i in x], df['fidelity'], 0.4, label='Noisy Hardware', alpha=0.7, color='red')
            ax1.bar([i+0.2 for i in x], df['zne_fidelity'], 0.4, label='ZNE Corrected', alpha=0.7, color='green')
            ax1.set_xlabel('Configuration')
            ax1.set_ylabel('Fidelity')
            ax1.set_title('Hardware Fidelity: Noisy vs ZNE')
            ax1.set_xticks(x)
            ax1.set_xticklabels(configs, rotation=45)
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # Memory usage
            ax2.plot(x, df['memory_before_percent'], 'o-', label='Before Test', color='blue')
            ax2.plot(x, df['memory_after_percent'], 's-', label='After Test', color='orange')
            ax2.set_xlabel('Configuration')
            ax2.set_ylabel('Memory Usage (%)')
            ax2.set_title('Memory Usage During Hardware Tests')
            ax2.set_xticks(x)
            ax2.set_xticklabels(configs, rotation=45)
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig('hardware_performance_analysis.png', dpi=300, bbox_inches='tight')
            plt.close()
            
        except Exception as e:
            logger.warning(f"Hardware visualization generation failed: {e}")
    
    def generate_comprehensive_report(self, save_file="aux_qhe_comprehensive_report.md"):
        """
        Generate a comprehensive analysis report.
        
        Args:
            save_file (str): Path to save the report.
        """
        total_time = time.perf_counter() - self.analysis_start_time
        
        report = f"""# AUX-QHE Comprehensive Analysis Report

Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}
Total Analysis Time: {total_time:.2f}s

## Summary

"""
        
        if self.mock_results:
            report += f"""### Mock Algorithm Performance
- Analysis Time: {self.mock_results['analysis_time']:.2f}s
- Configurations Tested: {self.mock_results['config_count']}
- Tables Generated: {len(self.mock_results['tables'])}

"""
        
        if self.hardware_results:
            report += f"""### Hardware Performance Analysis
- Analysis Time: {self.hardware_results['analysis_time']:.2f}s
- Backend Used: {self.hardware_results['backend']}
- Tests Completed: {self.hardware_results['completed_tests']}/{self.hardware_results['total_planned']}
- Tables Generated: {len(self.hardware_results['tables'])}

"""
        
        report += f"""## Files Generated
- noise_error_metrics.py - Unified noise analysis module
- algorithm_performance_mock.py - Mock BFV performance module
- algorithm_performance_hardware.py - Hardware performance module
- unified_aux_qhe_analysis.py - Master controller (this file)

## Visualizations Generated
"""
        
        viz_files = [
            "optimization_levels_analysis_mock.png",
            "auxiliary_states_growth_mock.png", 
            "performance_breakdown_mock.png",
            "hardware_performance_analysis.png",
            "noise_metrics_comprehensive.png"
        ]
        
        for viz_file in viz_files:
            if Path(viz_file).exists():
                report += f"- {viz_file}\\n"
        
        report += f"""
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
"""
        
        with open(save_file, 'w') as f:
            f.write(report)
        
        logger.info(f"Comprehensive report saved to {save_file}")
        print(f"📄 Comprehensive report saved to {save_file}")

def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="Unified AUX-QHE Analysis System")
    
    parser.add_argument('--mode', choices=['mock', 'hardware', 'both'], default='both',
                       help='Analysis mode to run')
    parser.add_argument('--qubits', type=str, default='3,4,5', 
                       help='Comma-separated qubit counts (e.g., 3,4,5)')
    parser.add_argument('--tdepth', type=str, default='2,3',
                       help='Comma-separated T-depths (e.g., 2,3)')
    parser.add_argument('--progressive', action='store_true', default=True,
                       help='Use progressive memory-safe testing for hardware')
    parser.add_argument('--max-memory', type=float, default=30,
                       help='Maximum memory (GB) for progressive testing')
    parser.add_argument('--no-visualizations', action='store_true',
                       help='Skip visualization generation')
    parser.add_argument('--report', action='store_true', default=True,
                       help='Generate comprehensive report')
    
    args = parser.parse_args()
    
    # Parse qubit and T-depth ranges
    qubit_range = [int(x.strip()) for x in args.qubits.split(',')]
    t_depth_range = [int(x.strip()) for x in args.tdepth.split(',')]
    visualizations = not args.no_visualizations
    
    print("🚀 AUX-QHE Unified Analysis System")
    print("=" * 50)
    print(f"Mode: {args.mode.upper()}")
    print(f"Qubits: {qubit_range}")
    print(f"T-depths: {t_depth_range}")
    print(f"Visualizations: {'Enabled' if visualizations else 'Disabled'}")
    print("=" * 50)
    
    # Initialize analyzer
    analyzer = UnifiedAUXQHEAnalyzer()
    
    # Run analysis based on mode
    if args.mode in ['mock', 'both']:
        mock_results = analyzer.run_mock_analysis(
            qubit_range, t_depth_range, visualizations
        )
    
    if args.mode in ['hardware', 'both']:
        hardware_results = analyzer.run_hardware_analysis(
            progressive=args.progressive,
            max_memory_gb=args.max_memory,
            qubit_range=qubit_range,
            t_depth_range=t_depth_range,
            visualizations=visualizations
        )
    
    # Run noise analysis if we have results
    noise_results = None
    if analyzer.hardware_results and analyzer.hardware_results.get('raw_results'):
        noise_results = analyzer.run_noise_analysis(
            analyzer.hardware_results['raw_results'],
            save_visualizations=visualizations
        )
    elif analyzer.mock_results and analyzer.mock_results.get('tables'):
        # Use mock results for noise analysis demo
        mock_data = analyzer.mock_results['tables']['raw_results'].to_dict('records')
        noise_results = analyzer.run_noise_analysis(mock_data, save_visualizations=visualizations)
    
    # Generate comprehensive report
    if args.report:
        analyzer.generate_comprehensive_report()
    
    # Final summary
    total_time = time.perf_counter() - analyzer.analysis_start_time
    print("\\n" + "=" * 70)
    print("🎉 AUX-QHE UNIFIED ANALYSIS COMPLETED")
    print("=" * 70)
    print(f"Total execution time: {total_time:.2f}s")
    
    if analyzer.mock_results:
        print(f"✅ Mock analysis: {analyzer.mock_results['config_count']} configurations")
    
    if analyzer.hardware_results:
        print(f"✅ Hardware analysis: {analyzer.hardware_results['completed_tests']} tests")
    
    if noise_results:
        print(f"✅ Noise analysis: {noise_results['sample_count']} samples")
    
    print("\\n📁 Generated Files:")
    print("   - 3 unified modules (noise_error_metrics.py, algorithm_performance_*.py)")
    print("   - Performance tables (in memory/displayed)")
    if visualizations:
        print("   - Visualization diagrams (*.png)")
    if args.report:
        print("   - Comprehensive report (aux_qhe_comprehensive_report.md)")
    
    print("\\n🧹 Ready for cleanup - original duplicate files can be removed")
    print("   See comprehensive report for cleanup recommendations")

if __name__ == "__main__":
    main()