#!/usr/bin/env python3
"""
Add 5q-2t Hardware Results to local_vs_hardware_comparison.csv
Updates the table with new results from corrected implementation (575 aux states)
"""

import json
import pandas as pd
from datetime import datetime

# Load new results
print("Loading new 5q-2t results...")
with open('ibm_noise_results_interim_20251023_232611.json', 'r') as f:
    data = json.load(f)

# Extract 5q-2t results
results_5q2t = {}
for exp in data:
    if exp['config'] == '5q-2t':
        method = exp['method']
        results_5q2t[method] = {
            'aux_states': exp['aux_states'],
            'fidelity': exp['fidelity'],
            'tvd': exp['tvd'],
            'circuit_depth': exp.get('circuit_depth', 'N/A'),
            'circuit_gates': exp.get('circuit_gates', 'N/A')
        }

print(f"Found {len(results_5q2t)} methods for 5q-2t")

# Load existing CSV
print("\nLoading local_vs_hardware_comparison.csv...")
df = pd.read_csv('local_vs_hardware_comparison.csv')

print(f"Current CSV has {len(df)} rows")
print("\nCurrent 5q-2t entries:")
print(df[df['Config'] == '5q-2t'][['Config', 'HW_Method', 'Aux_States', 'HW_Fidelity']])

# Backup original
backup_file = f"local_vs_hardware_comparison_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
df.to_csv(backup_file, index=False)
print(f"\n✅ Backup created: {backup_file}")

# Update 5q-2t rows with new auxiliary states and hardware results
print("\nUpdating 5q-2t rows...")

for idx, row in df.iterrows():
    if row['Config'] == '5q-2t' and row['HW_Method'] in results_5q2t:
        method = row['HW_Method']
        new_data = results_5q2t[method]

        # Calculate fidelity drop
        local_fidelity = row['Local_Fidelity']
        hw_fidelity = new_data['fidelity']
        fidelity_drop = ((local_fidelity - hw_fidelity) / local_fidelity) * 100

        # Update row
        df.at[idx, 'Aux_States'] = new_data['aux_states']
        df.at[idx, 'HW_Fidelity'] = new_data['fidelity']
        df.at[idx, 'HW_TVD'] = new_data['tvd']
        df.at[idx, 'Fidelity_Drop'] = f"{fidelity_drop:.2f}%"
        df.at[idx, 'Circuit_Depth'] = new_data['circuit_depth']
        df.at[idx, 'Circuit_Gates'] = new_data['circuit_gates']

        print(f"  Updated {method}: Aux {1350}→{new_data['aux_states']}, "
              f"Fidelity {row['HW_Fidelity']:.6f}→{hw_fidelity:.6f}")

# Save updated CSV
df.to_csv('local_vs_hardware_comparison.csv', index=False)
print(f"\n✅ Updated CSV saved: local_vs_hardware_comparison.csv")

# Display updated 5q-2t rows
print("\n📊 Updated 5q-2t entries:")
print(df[df['Config'] == '5q-2t'][['Config', 'Aux_States', 'HW_Method', 'HW_Fidelity',
                                     'HW_TVD', 'Fidelity_Drop', 'Circuit_Depth', 'Circuit_Gates']])

# Generate LaTeX table rows
print("\n" + "="*80)
print("📝 LATEX TABLE ROWS (for paper)")
print("="*80)
print("\nCopy these rows into your LaTeX table:\n")

print("% Updated 5q-2t results (575 auxiliary states)")
for idx, row in df[df['Config'] == '5q-2t'].iterrows():
    if row['HW_Method'] != 'N/A':
        config = row['Config']
        aux_states = int(row['Aux_States'])
        hw_method = row['HW_Method']
        hw_fidelity = row['HW_Fidelity']
        hw_tvd = row['HW_TVD']
        fidelity_drop = row['Fidelity_Drop']
        circuit_depth = int(row['Circuit_Depth']) if row['Circuit_Depth'] != 'N/A' else 'N/A'
        circuit_gates = int(row['Circuit_Gates']) if row['Circuit_Gates'] != 'N/A' else 'N/A'

        latex_row = (f"{config} & {aux_states} & {hw_method} & {hw_fidelity:.6f} & "
                    f"{hw_tvd:.6f} & {fidelity_drop} & {circuit_depth} & {circuit_gates} \\\\")
        print(latex_row)

print("\n" + "="*80)
print("Summary Statistics")
print("="*80)

df_5q2t = df[df['Config'] == '5q-2t']
df_5q2t_hw = df_5q2t[df_5q2t['HW_Method'] != 'N/A']

print(f"\nConfiguration: 5q-2t")
print(f"Auxiliary States: {int(df_5q2t_hw['Aux_States'].iloc[0])}")
print(f"Methods tested: {len(df_5q2t_hw)}")
print(f"\nHardware Fidelity Range:")
print(f"  Best:  {df_5q2t_hw['HW_Fidelity'].max():.6f} ({df_5q2t_hw.loc[df_5q2t_hw['HW_Fidelity'].idxmax(), 'HW_Method']})")
print(f"  Worst: {df_5q2t_hw['HW_Fidelity'].min():.6f} ({df_5q2t_hw.loc[df_5q2t_hw['HW_Fidelity'].idxmin(), 'HW_Method']})")
print(f"  Mean:  {df_5q2t_hw['HW_Fidelity'].mean():.6f}")

print(f"\nFidelity Degradation Range:")
fidelity_drops = df_5q2t_hw['Fidelity_Drop'].str.replace('%', '').astype(float)
print(f"  Best:  {fidelity_drops.min():.2f}%")
print(f"  Worst: {fidelity_drops.max():.2f}%")
print(f"  Mean:  {fidelity_drops.mean():.2f}%")

print("\n" + "="*80)
print("✅ Update complete!")
print("="*80)
