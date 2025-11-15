#!/usr/bin/env python3
"""
Compare Local Simulation (Ideal) vs Hardware Execution Results

This script creates a comparison table showing:
- Local simulation: Ideal algorithm correctness (high fidelity, ~0.99+)
- Hardware results: Real machine behavior with noise (lower fidelity)
"""

import pandas as pd
import sys
import glob
import os

def load_local_results(csv_file="results/corrected_openqasm_performance_comparison.csv"):
    """Load local simulation results (ideal behavior)"""
    try:
        df = pd.read_csv(csv_file)

        # Extract relevant columns and rename for clarity
        local_df = df[['Config', 'QASM_Version', 'Fidelity', 'TVD', 'Aux_States']].copy()
        local_df.columns = ['Config', 'QASM', 'Local_Fidelity', 'Local_TVD', 'Aux_States']

        # Remove "OpenQASM " prefix from QASM version
        local_df['QASM'] = local_df['QASM'].str.replace('OpenQASM ', '')

        # Group by Config (average QASM 2 and 3 results since they're similar)
        local_grouped = local_df.groupby('Config').agg({
            'Local_Fidelity': 'mean',
            'Local_TVD': 'mean',
            'Aux_States': 'first'
        }).reset_index()

        return local_grouped

    except FileNotFoundError:
        print(f"❌ Error: Could not find {csv_file}")
        print("   This file contains ideal local simulation results.")
        return None
    except Exception as e:
        print(f"❌ Error loading local results: {str(e)}")
        return None

def load_hardware_results(files_list=None):
    """Load hardware execution results (real machine behavior)"""
    try:
        # Use specific files if provided, otherwise search for all
        if files_list is None:
            files_list = [
                'ibm_noise_measurement_results_20251027_164719.csv',  # 5q-2t (NEW)
                'ibm_noise_measurement_results_20251027_172449.csv',  # 4q-3t (NEW)
                'ibm_noise_measurement_results_20251027_173307.csv',  # 5q-3t (NEW)
            ]

        all_hw_data = []
        loaded_files = []

        for file in files_list:
            if os.path.exists(file):
                print(f"📂 Loading: {file}")
                df = pd.read_csv(file)

                # Extract relevant columns
                hw_df = df[['config', 'method', 'fidelity', 'tvd', 'aux_states',
                            'circuit_depth', 'circuit_gates', 'total_time']].copy()
                hw_df.columns = ['Config', 'Method', 'HW_Fidelity', 'HW_TVD', 'Aux_States',
                                'Circuit_Depth', 'Circuit_Gates', 'Runtime_s']

                all_hw_data.append(hw_df)
                loaded_files.append(file)
            else:
                print(f"⚠️  File not found: {file}")

        if not all_hw_data:
            print(f"❌ Error: No hardware results files found")
            print("   Please run: python ibm_hardware_noise_experiment.py")
            return None, None

        # Combine all hardware data
        combined_hw_df = pd.concat(all_hw_data, ignore_index=True)

        print(f"✅ Loaded {len(loaded_files)} hardware result files")
        print(f"   Total experiments: {len(combined_hw_df)}")

        return combined_hw_df, loaded_files

    except Exception as e:
        print(f"❌ Error loading hardware results: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, None

def create_comparison_table(local_df, hw_df):
    """Create comparison table between local and hardware results"""

    # Merge dataframes on Config
    comparison_data = []

    for config in local_df['Config'].unique():
        local_row = local_df[local_df['Config'] == config].iloc[0]

        # Get hardware results for this config (all methods)
        hw_rows = hw_df[hw_df['Config'] == config]

        if len(hw_rows) == 0:
            # No hardware data for this config
            comparison_data.append({
                'Config': config,
                'Aux_States': int(local_row['Aux_States']),
                'Local_Fidelity': f"{local_row['Local_Fidelity']:.6f}",
                'Local_TVD': f"{local_row['Local_TVD']:.6f}",
                'HW_Method': 'N/A',
                'HW_Fidelity': 'N/A',
                'HW_TVD': 'N/A',
                'Fidelity_Drop': 'N/A',
                'Circuit_Depth': 'N/A',
                'Circuit_Gates': 'N/A'
            })
        else:
            # Add row for each hardware method
            for _, hw_row in hw_rows.iterrows():
                local_fid = local_row['Local_Fidelity']
                hw_fid = hw_row['HW_Fidelity']

                # Calculate fidelity drop
                if pd.notna(hw_fid) and hw_fid > 0:
                    fidelity_drop = ((local_fid - hw_fid) / local_fid) * 100
                    fid_drop_str = f"{fidelity_drop:.2f}%"
                else:
                    fid_drop_str = 'N/A'

                comparison_data.append({
                    'Config': config,
                    'Aux_States': int(local_row['Aux_States']),
                    'Local_Fidelity': f"{local_fid:.6f}",
                    'Local_TVD': f"{local_row['Local_TVD']:.6f}",
                    'HW_Method': hw_row['Method'],
                    'HW_Fidelity': f"{hw_fid:.6f}" if pd.notna(hw_fid) else 'N/A',
                    'HW_TVD': f"{hw_row['HW_TVD']:.6f}" if pd.notna(hw_row['HW_TVD']) else 'N/A',
                    'Fidelity_Drop': fid_drop_str,
                    'Circuit_Depth': int(hw_row['Circuit_Depth']) if pd.notna(hw_row['Circuit_Depth']) else 'N/A',
                    'Circuit_Gates': int(hw_row['Circuit_Gates']) if pd.notna(hw_row['Circuit_Gates']) else 'N/A',
                    'Runtime_s': f"{hw_row['Runtime_s']:.1f}" if pd.notna(hw_row['Runtime_s']) else 'N/A'
                })

    return pd.DataFrame(comparison_data)

def display_hardware_results_by_config(hw_df):
    """Display hardware results organized by configuration"""
    print("\n" + "="*120)
    print("🔬 HARDWARE EXPERIMENTAL RESULTS BY CONFIGURATION")
    print("="*120 + "\n")

    configs = hw_df['Config'].unique()

    for config in sorted(configs):
        config_data = hw_df[hw_df['Config'] == config]

        print(f"📊 {config.upper()}:")
        print(f"   Auxiliary States: {config_data['Aux_States'].iloc[0]}")
        print(f"   {'Method':<15} {'Fidelity':<12} {'TVD':<12} {'Depth':<8} {'Gates':<8} {'Runtime (s)':<12}")
        print(f"   {'-'*90}")

        # Sort by fidelity descending
        config_data_sorted = config_data.sort_values('HW_Fidelity', ascending=False)

        for _, row in config_data_sorted.iterrows():
            print(f"   {row['Method']:<15} {row['HW_Fidelity']:<12.6f} {row['HW_TVD']:<12.6f} {row['Circuit_Depth']:<8} {row['Circuit_Gates']:<8} {row['Runtime_s']:<12.1f}")

        # Best method for this config
        best = config_data_sorted.iloc[0]
        baseline = config_data[config_data['Method'] == 'Baseline'].iloc[0] if 'Baseline' in config_data['Method'].values else None

        if baseline is not None and best['Method'] != 'Baseline':
            improvement = ((best['HW_Fidelity'] - baseline['HW_Fidelity']) / baseline['HW_Fidelity']) * 100
            print(f"\n   🏆 Best: {best['Method']} with {best['HW_Fidelity']:.6f} fidelity ({improvement:+.1f}% vs Baseline)")
        else:
            print(f"\n   🏆 Best: {best['Method']} with {best['HW_Fidelity']:.6f} fidelity")

        print()

def print_summary_stats(comparison_df):
    """Print summary statistics"""
    print("\n" + "="*120)
    print("📊 LOCAL vs HARDWARE SUMMARY STATISTICS")
    print("="*120 + "\n")

    # Filter out N/A values
    valid_rows = comparison_df[comparison_df['HW_Fidelity'] != 'N/A'].copy()

    if len(valid_rows) == 0:
        print("⚠️  No valid hardware results to compare")
        return

    # Convert strings back to floats for statistics
    valid_rows['Local_Fidelity_Float'] = valid_rows['Local_Fidelity'].astype(float)
    valid_rows['HW_Fidelity_Float'] = valid_rows['HW_Fidelity'].astype(float)

    print(f"Configurations tested: {comparison_df['Config'].nunique()}")
    print(f"Hardware methods tested: {valid_rows['HW_Method'].nunique()}")
    print(f"Total test runs: {len(valid_rows)}")

    print(f"\n📈 Fidelity Comparison:")
    print(f"   Local (Ideal) Average: {valid_rows['Local_Fidelity_Float'].mean():.6f}")
    print(f"   Hardware Average: {valid_rows['HW_Fidelity_Float'].mean():.6f}")
    print(f"   Average Fidelity Drop: {((valid_rows['Local_Fidelity_Float'] - valid_rows['HW_Fidelity_Float']) / valid_rows['Local_Fidelity_Float'] * 100).mean():.2f}%")

    # Best and worst hardware methods
    method_avg = valid_rows.groupby('HW_Method')['HW_Fidelity_Float'].mean().sort_values(ascending=False)
    print(f"\n🏆 Best Hardware Method: {method_avg.index[0]} (Fidelity: {method_avg.iloc[0]:.6f})")
    if len(method_avg) > 1:
        print(f"⚠️  Worst Hardware Method: {method_avg.index[-1]} (Fidelity: {method_avg.iloc[-1]:.6f})")

    print("\n" + "="*120)

def main():
    print("="*120)
    print("🔬 AUX-QHE: LOCAL SIMULATION vs HARDWARE EXECUTION COMPARISON")
    print("="*120 + "\n")

    # Load local simulation results (ideal)
    print("📂 Loading local simulation results (ideal behavior)...")
    local_df = load_local_results()

    if local_df is None:
        sys.exit(1)

    print(f"✅ Loaded {len(local_df)} local configurations\n")

    # Load hardware results (real machine)
    print("📂 Loading hardware execution results (real machine)...")
    result = load_hardware_results()

    if result is None or result[0] is None:
        sys.exit(1)

    hw_df, hw_files = result
    print(f"   Files loaded: {', '.join([os.path.basename(f) for f in hw_files])}\n")

    # Display hardware results by configuration first
    display_hardware_results_by_config(hw_df)

    # Create comparison table
    print("🔄 Creating comparison table...\n")
    comparison_df = create_comparison_table(local_df, hw_df)

    # Print formatted table
    print("\n" + "="*120)
    print("📊 LOCAL vs HARDWARE COMPARISON TABLE")
    print("="*120 + "\n")

    print(comparison_df.to_string(index=False))

    # Print summary statistics
    print_summary_stats(comparison_df)

    # Save to CSV
    output_file = "local_vs_hardware_comparison.csv"
    comparison_df.to_csv(output_file, index=False)
    print(f"\n✅ Comparison table saved to: {output_file}")

    # Print markdown format
    print("\n" + "="*120)
    print("📝 MARKDOWN FORMAT (for documentation)")
    print("="*120 + "\n")

    print(comparison_df.to_markdown(index=False))

    print("\n" + "="*120)

    # Print LaTeX format
    print("\n📄 LATEX FORMAT (for papers)")
    print("="*120 + "\n")

    print(comparison_df.to_latex(index=False))

    print("\n" + "="*120)

    # Interpretation guide
    print("\n" + "="*120)
    print("💡 INTERPRETATION GUIDE")
    print("="*120 + "\n")

    print("Local Simulation (Ideal):")
    print("  - Fidelity ≈ 1.0 (0.99+): Algorithm is correct, no noise")
    print("  - TVD ≈ 0.0: Perfect match with expected output")
    print("")
    print("Hardware Execution (Real Machine):")
    print("  - Fidelity << 1.0: Real quantum noise affects results")
    print("  - TVD > 0: Deviation from ideal behavior due to hardware errors")
    print("")
    print("Fidelity Drop:")
    print("  - Shows percentage decrease from ideal to real hardware")
    print("  - Lower drop = better noise resilience")
    print("")
    print("Methods:")
    print("  - Baseline: Optimization level 1, no error mitigation")
    print("  - ZNE: Zero-Noise Extrapolation applied")
    print("  - Opt-3: Higher optimization level")
    print("  - Opt-3+ZNE: Combined optimization and error mitigation")

    print("\n" + "="*120)

if __name__ == "__main__":
    main()
