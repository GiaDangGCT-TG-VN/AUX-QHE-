#!/usr/bin/env python3
"""
Display IBM Hardware Results using the workflow pattern from generate_results_table.py

Reads hardware execution CSV and formats with:
- Formatted table display (string)
- Markdown format
- LaTeX format
- Summary statistics
"""
import pandas as pd
import sys
import os

# Get the latest hardware results file
csv_files = sorted([f for f in os.listdir('.') if f.startswith('ibm_noise_measurement_results_') and f.endswith('.csv')])
if not csv_files:
    print("❌ Error: No IBM hardware results found")
    print("   Run: python ibm_hardware_noise_experiment.py first")
    sys.exit(1)

csv_file = csv_files[-1]  # Latest file

try:
    df = pd.read_csv(csv_file)

    print("\n" + "="*120)
    print(f"IBM QUANTUM HARDWARE RESULTS - {csv_file}")
    print("="*120 + "\n")

    # Create formatted table with key columns for display
    table_data = []

    for _, row in df.iterrows():
        config = row['config']
        method = row['method']
        backend = row['backend']
        fidelity = row['fidelity']
        tvd = row['tvd']
        aux_states = row['aux_states']
        shots = row['shots']
        exec_time = row['exec_time']
        decrypt_time = row['decrypt_time']
        total_time = row['total_time']
        circuit_depth = row['circuit_depth']
        circuit_gates = row['circuit_gates']

        table_data.append({
            'Config': config,
            'Method': method,
            'Backend': backend,
            'Fidelity': f"{fidelity:.6f}",
            'TVD': f"{tvd:.6f}",
            'Aux States': aux_states,
            'Shots': shots,
            'Exec Time(s)': f"{exec_time:.3f}",
            'Decrypt Time(s)': f"{decrypt_time:.6f}",
            'Total Time(s)': f"{total_time:.3f}",
            'Depth': circuit_depth,
            'Gates': circuit_gates
        })

    # Create DataFrame
    results_df = pd.DataFrame(table_data)

    # Print formatted table
    print(results_df.to_string(index=False))
    print("\n" + "="*120)

    # Save to CSV
    output_file = "formatted_hardware_results.csv"
    results_df.to_csv(output_file, index=False)
    print(f"\n✅ Formatted table saved to: {output_file}")

    # Print markdown format
    print("\n" + "="*120)
    print("MARKDOWN FORMAT (for documentation)")
    print("="*120 + "\n")

    print(results_df.to_markdown(index=False))

    print("\n" + "="*120)

    # Print LaTeX format
    print("\nLATEX FORMAT (for papers)")
    print("="*120 + "\n")

    print(results_df.to_latex(index=False))

    print("\n" + "="*120)

    # Summary statistics
    print("\n📊 SUMMARY STATISTICS")
    print("="*120 + "\n")

    # Group by method
    methods = results_df['Method'].unique()
    configs = results_df['Config'].unique()
    backends = results_df['Backend'].unique()

    print(f"Total Experiments: {len(results_df)}")
    print(f"Configurations: {len(configs)} - {list(configs)}")
    print(f"Methods: {len(methods)} - {list(methods)}")
    print(f"Backends: {list(backends)}")
    print(f"\nAverage Fidelity: {df['fidelity'].mean():.6f}")
    print(f"Average TVD: {df['tvd'].mean():.6f}")
    print(f"Average Aux States: {df['aux_states'].mean():.1f}")
    print(f"Average Execution Time: {df['exec_time'].mean():.3f}s")
    print(f"Average Total Time: {df['total_time'].mean():.3f}s")

    # Fidelity by method
    print("\n📈 FIDELITY BY METHOD:")
    print("-" * 50)
    for method in methods:
        method_df = df[df['method'] == method]
        avg_fid = method_df['fidelity'].mean()
        print(f"  {method:15s}: {avg_fid:.6f}")

    # Fidelity by config
    print("\n📈 FIDELITY BY CONFIG:")
    print("-" * 50)
    for config in configs:
        config_df = df[df['config'] == config]
        avg_fid = config_df['fidelity'].mean()
        print(f"  {config:15s}: {avg_fid:.6f}")

    # Comparison matrix (like the weird metrics table)
    print("\n📊 FIDELITY COMPARISON MATRIX:")
    print("-" * 50)
    pivot_table = df.pivot_table(values='fidelity', index='config', columns='method', aggfunc='mean')
    print(pivot_table.to_string())

    print("\n" + "="*120)

    # Check for issues
    print("\n⚠️  QUALITY CHECKS:")
    print("-" * 50)
    low_fidelity = df[df['fidelity'] < 0.10]
    if len(low_fidelity) > 0:
        print(f"  ⚠️  {len(low_fidelity)} experiments with fidelity < 0.10")
        print(f"      Configs: {list(low_fidelity['config'].unique())}")

    # Check if ZNE is worse than baseline
    for config in configs:
        config_df = df[df['config'] == config]
        if 'Baseline' in config_df['method'].values and 'ZNE' in config_df['method'].values:
            baseline_fid = config_df[config_df['method'] == 'Baseline']['fidelity'].values[0]
            zne_fid = config_df[config_df['method'] == 'ZNE']['fidelity'].values[0]
            if zne_fid < baseline_fid:
                print(f"  ⚠️  {config}: ZNE ({zne_fid:.6f}) < Baseline ({baseline_fid:.6f})")

    print("\n" + "="*120)

except FileNotFoundError:
    print(f"❌ Error: Could not find {csv_file}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
