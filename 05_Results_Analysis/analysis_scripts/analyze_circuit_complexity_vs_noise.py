#!/usr/bin/env python3
"""
Analyze how circuit complexity affects hardware noise in AUX-QHE algorithm.

This script extracts all circuit depth and gate counts from hardware simulations
and correlates them with fidelity degradation.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Read hardware results
df = pd.read_csv('local_vs_hardware_comparison.csv')

# Filter only hardware results (exclude local-only rows)
hw_df = df[df['HW_Method'].notna()].copy()

print("=" * 80)
print("AUX-QHE CIRCUIT COMPLEXITY vs HARDWARE NOISE ANALYSIS")
print("=" * 80)

# ============================================================================
# SECTION 1: CIRCUIT COMPLEXITY SUMMARY BY CONFIGURATION
# ============================================================================
print("\n" + "=" * 80)
print("SECTION 1: CIRCUIT COMPLEXITY BY CONFIGURATION")
print("=" * 80)

# Group by config and get average metrics
complexity_summary = hw_df.groupby('Config').agg({
    'Aux_States': 'first',
    'Circuit_Depth': 'mean',
    'Circuit_Gates': 'mean',
    'HW_Fidelity': 'mean',
    'Fidelity_Drop': lambda x: x.str.rstrip('%').astype(float).mean()
}).round(2)

print("\n📊 Average Metrics per Configuration:")
print(complexity_summary.to_string())

# ============================================================================
# SECTION 2: DETAILED BREAKDOWN BY METHOD
# ============================================================================
print("\n" + "=" * 80)
print("SECTION 2: DETAILED BREAKDOWN BY ERROR MITIGATION METHOD")
print("=" * 80)

for config in sorted(hw_df['Config'].unique()):
    config_data = hw_df[hw_df['Config'] == config]
    print(f"\n{'─' * 80}")
    print(f"Configuration: {config}")
    print(f"{'─' * 80}")
    print(f"Auxiliary States: {config_data['Aux_States'].iloc[0]:,}")
    print()

    # Sort by fidelity descending
    config_data_sorted = config_data.sort_values('HW_Fidelity', ascending=False)

    for _, row in config_data_sorted.iterrows():
        method = row['HW_Method']
        depth = int(row['Circuit_Depth'])
        gates = int(row['Circuit_Gates'])
        fidelity = row['HW_Fidelity']
        fid_drop = row['Fidelity_Drop']

        print(f"  {method:12s} | Depth: {depth:3d} | Gates: {gates:3d} | "
              f"Fidelity: {fidelity:.6f} | Drop: {fid_drop}")

# ============================================================================
# SECTION 3: CORRELATION ANALYSIS
# ============================================================================
print("\n" + "=" * 80)
print("SECTION 3: CORRELATION: CIRCUIT COMPLEXITY vs HARDWARE FIDELITY")
print("=" * 80)

# Calculate correlations
corr_depth_fidelity = hw_df['Circuit_Depth'].corr(hw_df['HW_Fidelity'])
corr_gates_fidelity = hw_df['Circuit_Gates'].corr(hw_df['HW_Fidelity'])
corr_aux_fidelity = hw_df['Aux_States'].corr(hw_df['HW_Fidelity'])

print(f"\n📈 Pearson Correlation Coefficients:")
print(f"  Circuit Depth  ↔ Hardware Fidelity: {corr_depth_fidelity:+.4f}")
print(f"  Circuit Gates  ↔ Hardware Fidelity: {corr_gates_fidelity:+.4f}")
print(f"  Aux States     ↔ Hardware Fidelity: {corr_aux_fidelity:+.4f}")

print("\n💡 Interpretation:")
if corr_depth_fidelity < -0.3:
    print(f"  ⚠️  STRONG NEGATIVE: Higher circuit depth → Lower fidelity")
elif corr_depth_fidelity < -0.1:
    print(f"  ⚠️  MODERATE NEGATIVE: Higher circuit depth → Slightly lower fidelity")
else:
    print(f"  ✓  WEAK/NO CORRELATION: Circuit depth has minimal impact on fidelity")

if corr_aux_fidelity < -0.5:
    print(f"  ⚠️  VERY STRONG NEGATIVE: More auxiliary states → Much lower fidelity")
elif corr_aux_fidelity < -0.3:
    print(f"  ⚠️  STRONG NEGATIVE: More auxiliary states → Lower fidelity")
else:
    print(f"  ✓  WEAK/NO CORRELATION: Auxiliary states count has minimal direct impact")

# ============================================================================
# SECTION 4: COMPLEXITY RANGES
# ============================================================================
print("\n" + "=" * 80)
print("SECTION 4: CIRCUIT COMPLEXITY RANGES ACROSS ALL TESTS")
print("=" * 80)

print(f"\n📏 Circuit Depth Range:")
print(f"  Minimum: {hw_df['Circuit_Depth'].min():.0f} (Config: {hw_df.loc[hw_df['Circuit_Depth'].idxmin(), 'Config']}, Method: {hw_df.loc[hw_df['Circuit_Depth'].idxmin(), 'HW_Method']})")
print(f"  Maximum: {hw_df['Circuit_Depth'].max():.0f} (Config: {hw_df.loc[hw_df['Circuit_Depth'].idxmax(), 'Config']}, Method: {hw_df.loc[hw_df['Circuit_Depth'].idxmax(), 'HW_Method']})")
print(f"  Average: {hw_df['Circuit_Depth'].mean():.1f}")
print(f"  Std Dev: {hw_df['Circuit_Depth'].std():.1f}")

print(f"\n🔧 Circuit Gates Range:")
print(f"  Minimum: {hw_df['Circuit_Gates'].min():.0f} (Config: {hw_df.loc[hw_df['Circuit_Gates'].idxmin(), 'Config']}, Method: {hw_df.loc[hw_df['Circuit_Gates'].idxmin(), 'HW_Method']})")
print(f"  Maximum: {hw_df['Circuit_Gates'].max():.0f} (Config: {hw_df.loc[hw_df['Circuit_Gates'].idxmax(), 'Config']}, Method: {hw_df.loc[hw_df['Circuit_Gates'].idxmax(), 'HW_Method']})")
print(f"  Average: {hw_df['Circuit_Gates'].mean():.1f}")
print(f"  Std Dev: {hw_df['Circuit_Gates'].std():.1f}")

print(f"\n🔑 Auxiliary States Range:")
print(f"  Minimum: {hw_df['Aux_States'].min():,.0f} (Config: {hw_df.loc[hw_df['Aux_States'].idxmin(), 'Config']})")
print(f"  Maximum: {hw_df['Aux_States'].max():,.0f} (Config: {hw_df.loc[hw_df['Aux_States'].idxmax(), 'Config']})")
print(f"  Average: {hw_df['Aux_States'].mean():,.1f}")

# ============================================================================
# SECTION 5: KEY INSIGHTS
# ============================================================================
print("\n" + "=" * 80)
print("SECTION 5: KEY INSIGHTS - COMPLEXITY vs NOISE")
print("=" * 80)

# Find best and worst performers
best_config = hw_df.loc[hw_df['HW_Fidelity'].idxmax()]
worst_config = hw_df.loc[hw_df['HW_Fidelity'].idxmin()]

print("\n🏆 BEST PERFORMANCE:")
print(f"  Config: {best_config['Config']}, Method: {best_config['HW_Method']}")
print(f"  Fidelity: {best_config['HW_Fidelity']:.6f}")
print(f"  Circuit Depth: {best_config['Circuit_Depth']:.0f}")
print(f"  Circuit Gates: {best_config['Circuit_Gates']:.0f}")
print(f"  Aux States: {best_config['Aux_States']:,.0f}")

print("\n❌ WORST PERFORMANCE:")
print(f"  Config: {worst_config['Config']}, Method: {worst_config['HW_Method']}")
print(f"  Fidelity: {worst_config['HW_Fidelity']:.6f}")
print(f"  Circuit Depth: {worst_config['Circuit_Depth']:.0f}")
print(f"  Circuit Gates: {worst_config['Circuit_Gates']:.0f}")
print(f"  Aux States: {worst_config['Aux_States']:,.0f}")

# Calculate fidelity ratio
fidelity_ratio = best_config['HW_Fidelity'] / worst_config['HW_Fidelity']
print(f"\n📊 Fidelity Ratio (Best/Worst): {fidelity_ratio:.2f}x")

# Analyze by auxiliary states
print("\n" + "─" * 80)
print("💡 INSIGHT: Impact of Auxiliary States on Fidelity")
print("─" * 80)

aux_fidelity = hw_df.groupby('Aux_States')['HW_Fidelity'].agg(['mean', 'std', 'min', 'max'])
for aux_states, row in aux_fidelity.iterrows():
    config_name = hw_df[hw_df['Aux_States'] == aux_states]['Config'].iloc[0]
    print(f"\n{config_name} ({aux_states:,} aux states):")
    print(f"  Avg Fidelity: {row['mean']:.6f} ± {row['std']:.6f}")
    print(f"  Range: [{row['min']:.6f}, {row['max']:.6f}]")
    print(f"  Variance: {row['max'] - row['min']:.6f}")

# ============================================================================
# SECTION 6: METHOD COMPARISON
# ============================================================================
print("\n" + "=" * 80)
print("SECTION 6: ERROR MITIGATION METHOD EFFECTIVENESS")
print("=" * 80)

method_stats = hw_df.groupby('HW_Method').agg({
    'HW_Fidelity': ['mean', 'std'],
    'Circuit_Depth': 'mean',
    'Circuit_Gates': 'mean'
}).round(6)

print("\n📊 Average Performance by Method:")
print(method_stats.to_string())

# Rank methods by average fidelity
method_ranking = hw_df.groupby('HW_Method')['HW_Fidelity'].mean().sort_values(ascending=False)
print("\n🏆 Method Ranking (by average fidelity):")
for rank, (method, fidelity) in enumerate(method_ranking.items(), 1):
    print(f"  {rank}. {method:12s}: {fidelity:.6f}")

# ============================================================================
# SECTION 7: EXPORT DATA FOR VISUALIZATION
# ============================================================================
print("\n" + "=" * 80)
print("SECTION 7: EXPORTING DATA FOR VISUALIZATION")
print("=" * 80)

# Create summary table for paper/presentation
summary_table = hw_df[['Config', 'Aux_States', 'HW_Method', 'Circuit_Depth',
                        'Circuit_Gates', 'HW_Fidelity', 'Fidelity_Drop']].copy()
summary_table = summary_table.sort_values(['Config', 'HW_Fidelity'], ascending=[True, False])

# Save to CSV
output_file = 'circuit_complexity_vs_noise_summary.csv'
summary_table.to_csv(output_file, index=False)
print(f"\n✅ Summary table saved to: {output_file}")

# Generate LaTeX table
print("\n" + "=" * 80)
print("SECTION 8: LATEX TABLE FOR PAPER")
print("=" * 80)

print("\n% LaTeX table code:")
print("\\begin{table}[h]")
print("\\centering")
print("\\caption{Circuit Complexity and Hardware Fidelity in AUX-QHE}")
print("\\label{tab:circuit-complexity}")
print("\\begin{tabular}{lrcccc}")
print("\\hline")
print("Config & Aux States & Method & Depth & Gates & Fidelity \\\\")
print("\\hline")

for config in sorted(hw_df['Config'].unique()):
    config_data = hw_df[hw_df['Config'] == config].sort_values('HW_Fidelity', ascending=False)
    for i, (_, row) in enumerate(config_data.iterrows()):
        aux_str = f"{row['Aux_States']:,}" if i == 0 else ""
        config_str = config if i == 0 else ""
        print(f"{config_str} & {aux_str} & {row['HW_Method']} & "
              f"{int(row['Circuit_Depth'])} & {int(row['Circuit_Gates'])} & "
              f"{row['HW_Fidelity']:.4f} \\\\")
    print("\\hline")

print("\\end{tabular}")
print("\\end{table}")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
