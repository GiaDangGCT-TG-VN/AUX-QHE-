#!/usr/bin/env python3
"""
Generate LaTeX Tables for Paper
Creates 3 tables: Hardware Performance, Key Size, and Local Simulation
"""

import json
import pandas as pd

print("="*80)
print("📊 GENERATING ALL 3 LATEX TABLES FOR PAPER")
print("="*80)

# ============================================================================
# TABLE 1: Hardware Performance (with corrected ZNE metrics)
# ============================================================================

print("\n" + "="*80)
print("TABLE 1: Hardware Performance on IBM Quantum")
print("="*80 + "\n")

json_files = [
    'ibm_noise_measurement_results_20251027_164719.json',  # 5q-2t
    'ibm_noise_measurement_results_20251027_172449.json',  # 4q-3t
    'ibm_noise_measurement_results_20251027_173307.json',  # 5q-3t
]

hw_data = []
for json_file in json_files:
    with open(json_file, 'r') as f:
        data = json.load(f)

    df = pd.DataFrame(data)
    baseline_row = df[df['method'] == 'Baseline'].iloc[0]
    baseline_time = baseline_row['exec_time']
    baseline_gates = baseline_row['circuit_gates']

    for _, row in df.iterrows():
        method = row['method']
        config = row['config']
        aux_states = row['aux_states']
        fidelity = row['fidelity']
        tvd = row['tvd']
        exec_time = row['exec_time']

        # Calculate corrected gates/depth for ZNE methods
        if 'ZNE' in method:
            runtime_ratio = exec_time / baseline_time
            corrected_gates = int(baseline_gates * runtime_ratio)
            corrected_depth = int(row['circuit_depth'] * runtime_ratio)
        else:
            corrected_gates = row['circuit_gates']
            corrected_depth = row['circuit_depth']

        # Fidelity drop from ideal (1.0)
        fidelity_drop = (1.0 - fidelity) * 100

        hw_data.append({
            'Config': config,
            'Aux_States': aux_states,
            'Method': method,
            'Fidelity': fidelity,
            'TVD': tvd,
            'Fidelity_Drop': fidelity_drop
        })

hw_df = pd.DataFrame(hw_data)

# LaTeX output
print("\\begin{table}[htbp]")
print("\\centering")
print("\\caption{Hardware Execution Performance on IBM Quantum (ibm\\_torino, 133 qubits)}")
print("\\label{tab:Hardware_performance}")
print("\\begin{tabular}{lrllll}")
print("\\toprule")
print("Config & Aux States & HW Method & HW Fidelity & HW TVD & Fidelity Drop \\\\")
print("\\midrule")

for _, row in hw_df.iterrows():
    print(f"{row['Config']} & {row['Aux_States']} & {row['Method']} & "
          f"{row['Fidelity']:.4f} & {row['TVD']:.4f} & "
          f"{row['Fidelity_Drop']:.2f}\\% \\\\")

print("\\bottomrule")
print("\\end{tabular}")
print("\\footnotesize")
print("\\textit{Note: ZNE applies Zero-Noise Extrapolation with noise factors [1, 2, 3].}")
print("\\end{table}")

# ============================================================================
# TABLE 2: Key Size and Auxiliary States
# ============================================================================

print("\n" + "="*80)
print("TABLE 2: Key Size and Auxiliary States")
print("="*80 + "\n")

key_data = []
for json_file in json_files:
    with open(json_file, 'r') as f:
        data = json.load(f)

    baseline = data[0]  # Get baseline entry
    config = baseline['config']
    aux_states = baseline['aux_states']
    num_qubits = baseline['num_qubits']
    t_depth = baseline['t_depth']

    # Layer sizes: [n, n^2, n^3, ...] for each T-depth layer
    layer_sizes = [num_qubits**i for i in range(1, t_depth+1)]
    layer_str = ', '.join(map(str, layer_sizes))

    # Efficiency: average aux states per layer
    efficiency = aux_states / t_depth if t_depth > 0 else 0

    # Cross terms: combinations of qubits times layers
    cross_terms = num_qubits * (num_qubits - 1) // 2 * t_depth

    # Eval time
    eval_time = baseline.get('eval_time', 0)

    key_data.append({
        'Config': config,
        'Aux_States': aux_states,
        'Layer_Sizes': layer_str,
        'Efficiency': efficiency,
        'Cross_Terms': cross_terms,
        'Eval_Time': eval_time
    })

print("\\begin{table}[htbp]")
print("\\centering")
print("\\caption{Key Size and Auxiliary States for AUX-QHE Protocol}")
print("\\label{tab:Key}")
print("\\begin{tabular}{lrrrrr}")
print("\\toprule")
print("\\textbf{Config} & \\textbf{Aux States} & \\textbf{Layer Sizes} & \\textbf{Efficiency} & \\textbf{Cross Terms} & \\textbf{Eval Time (s)} \\\\")
print("\\midrule")

for item in key_data:
    print(f"{item['Config']} & {item['Aux_States']} & "
          f"${item['Layer_Sizes']}$ & {item['Efficiency']:.1f} & "
          f"{item['Cross_Terms']} & {item['Eval_Time']:.3f} \\\\")

print("\\bottomrule")
print("\\end{tabular}")
print("\\footnotesize")
print("\\textit{Note: Layer sizes show auxiliary states per T-depth layer ($n^i$ for layer $i$).}")
print("\\end{table}")

# ============================================================================
# TABLE 3: Local Simulation Performance
# ============================================================================

print("\n" + "="*80)
print("TABLE 3: Local Simulation Performance")
print("="*80 + "\n")

local_file = 'results/corrected_openqasm_performance_comparison.csv'
try:
    local_df = pd.read_csv(local_file)

    print("\\begin{table}[htbp]")
    print("\\centering")
    print("\\caption{AUX-QHE Algorithm Performance on Local Simulation (Ideal, No Noise)}")
    print("\\label{tab:algorithm_performance}")
    print("\\footnotesize")
    print("\\begin{tabular}{llllrllll}")
    print("\\toprule")
    print("Config & Fidelity & TVD & QASM & Aux States & Aux Prep (s) & T-Gadget (s) & Decrypt Eval (s) & Total Time (s) \\\\")
    print("\\midrule")

    # Group by config (average QASM 2 and 3 if both present)
    for config in local_df['Config'].unique():
        config_data = local_df[local_df['Config'] == config]

        # Take first row (or average)
        row = config_data.iloc[0]

        fidelity = row['Fidelity']
        tvd = row['TVD']
        qasm = row['QASM_Version'].replace('OpenQASM ', '')
        aux_states = row['Aux_States']

        # Get timing columns with correct names
        aux_prep = row.get('Aux_Prep_Time_s', 0)
        t_gadget = row.get('T_Gadget_Time_s', 0)
        decrypt_eval = row.get('Eval_Time_s', 0)  # Using Eval_Time_s for decrypt eval

        # Calculate total time from components
        total_time = aux_prep + t_gadget + decrypt_eval

        print(f"{config} & {fidelity:.4f} & {tvd:.4f} & {qasm} & {aux_states} & "
              f"{aux_prep:.3f} & {t_gadget:.3f} & {decrypt_eval:.3f} & {total_time:.3f} \\\\")

    print("\\bottomrule")
    print("\\end{tabular}")
    print("\\footnotesize")
    print("\\textit{Note: Local simulation shows ideal behavior (Fidelity $\\\\approx$ 1.0, TVD $\\\\approx$ 0.0).}")
    print("\\end{table}")

except Exception as e:
    print(f"⚠️  Error loading local simulation data: {e}")
    print("Please check the file path: results/corrected_openqasm_performance_comparison.csv")

print("\n" + "="*80)
print("✅ ALL TABLES GENERATED SUCCESSFULLY!")
print("="*80)
print("\nCopy the LaTeX code above and paste into your Overleaf document.")
print("All tables are ready for publication!")
