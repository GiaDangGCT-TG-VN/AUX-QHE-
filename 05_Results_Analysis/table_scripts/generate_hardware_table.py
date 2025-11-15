#!/usr/bin/env python3
"""
Generate LaTeX table for hardware noise experiment results
Configs: 5q-2t, 4q-3t, 5q-3t (most recent executions)
"""

import json
import sys

# Most recent result files for each config
result_files = {
    '5q-2t': 'ibm_noise_measurement_results_20251030_231319.json',
    '4q-3t': 'ibm_noise_measurement_results_20251030_230642.json',
    '5q-3t': 'ibm_noise_measurement_results_20251030_224547.json',  # From previous session
}

# Aux states for each config (from actual key generation in results)
aux_states = {
    '5q-2t': 575,     # 5 qubits, T-depth=2
    '4q-3t': 10776,   # 4 qubits, T-depth=3
    '5q-3t': 31025,   # 5 qubits, T-depth=3
}

def load_results(filename):
    """Load results from JSON file"""
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def calculate_fidelity_drop(hw_fidelity):
    """Calculate fidelity drop from ideal (100%)"""
    ideal_fidelity = 100.0
    return ideal_fidelity - hw_fidelity

def generate_table():
    """Generate LaTeX table in user's preferred format"""

    print("\\begin{table*}[htbp]")
    print("\\centering")
    print("\\caption{Detailed Fidelity of Optimisation Levels + ZNE techniques on IBM Quantum}")
    print("\\label{tab:Hardware_performance}")
    print("\\begin{tabular}{lrllllllll}")
    print("\\toprule")
    print("Config & Aux States & HW Method & HW Fidelity & HW TVD & Fidelity Drop \\\\")
    print("\\midrule")

    # Process each config
    for config_name in ['5q-2t', '4q-3t', '5q-3t']:
        filename = result_files[config_name]
        aux_count = aux_states[config_name]

        try:
            results = load_results(filename)

            # Filter for this config
            config_results = [r for r in results if r['config'] == config_name]

            # Sort by method order: Baseline, ZNE, Opt-3, Opt-3+ZNE
            method_order = ['Baseline', 'ZNE', 'Opt-3', 'Opt-3+ZNE']
            config_results_sorted = []
            for method_name in method_order:
                for r in config_results:
                    if r['method'] == method_name:
                        config_results_sorted.append(r)
                        break

            # Print rows - each row shows config, aux states, method
            for result in config_results_sorted:
                method = result['method']
                fidelity = result['fidelity']  # Keep as decimal (not percentage)
                tvd = result['tvd']
                fidelity_drop = calculate_fidelity_drop(fidelity * 100)  # Calculate from percentage

                # Print row with config and aux states repeated for each method
                print(f"{config_name} & {aux_count} & {method} & {fidelity:.4f} & {tvd:.4f} & {fidelity_drop:.2f}\\% \\\\")

        except Exception as e:
            print(f"% ERROR: Could not process {config_name}: {e}", file=sys.stderr)

    print("\\bottomrule")
    print("\\end{tabular}")
    print("\\end{table*}")

if __name__ == "__main__":
    print("% Hardware Noise Experiment Results Table")
    print("% Generated from most recent executions (2025-10-30)")
    print("% Backend: ibm_torino (133 qubits)")
    print("% Shots: 1024 per method")
    print()
    generate_table()
    print()
    print("% Summary statistics:")

    # Calculate averages
    for config_name in ['5q-2t', '4q-3t', '5q-3t']:
        filename = result_files[config_name]
        results = load_results(filename)
        config_results = [r for r in results if r['config'] == config_name]

        avg_fidelity = sum(r['fidelity'] for r in config_results) / len(config_results) * 100
        avg_tvd = sum(r['tvd'] for r in config_results) / len(config_results)

        print(f"% {config_name}: Avg Fidelity = {avg_fidelity:.2f}%, Avg TVD = {avg_tvd:.3f}")
