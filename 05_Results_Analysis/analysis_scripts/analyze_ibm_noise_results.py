#!/usr/bin/env python3
"""
Analyze IBM Quantum Hardware Noise Measurement Results
Generate comprehensive analysis and visualizations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json
import sys

def load_latest_results():
    """Load the most recent results file."""
    csv_files = sorted(Path('.').glob('ibm_noise_measurement_results_*.csv'))

    if not csv_files:
        print("❌ No results files found!")
        print("   Please run: python ibm_hardware_noise_experiment.py first")
        return None

    latest_file = csv_files[-1]
    print(f"📂 Loading results from: {latest_file}")

    df = pd.read_csv(latest_file)
    print(f"   ✅ Loaded {len(df)} experimental results")

    return df


def create_fidelity_comparison_table(df):
    """Create detailed fidelity comparison table."""
    print("\n" + "="*120)
    print("🎯 FIDELITY COMPARISON ACROSS ALL METHODS")
    print("="*120)

    pivot = df.pivot_table(
        index='config',
        columns='method',
        values='fidelity',
        aggfunc='mean'
    )

    # Reorder columns in logical order
    method_order = ['Baseline', 'ZNE', 'Opt-0', 'Opt-3', 'Opt-0+ZNE', 'Opt-3+ZNE']
    pivot = pivot[[col for col in method_order if col in pivot.columns]]

    print("\n📊 FIDELITY VALUES")
    print(pivot.to_string(float_format=lambda x: f'{x:.6f}'))

    # Calculate improvements over baseline
    print("\n📈 IMPROVEMENT OVER BASELINE (%)")
    baseline = pivot['Baseline']
    improvement = pd.DataFrame()

    for col in pivot.columns:
        if col != 'Baseline':
            improvement[col] = ((pivot[col] - baseline) / baseline * 100)

    print(improvement.to_string(float_format=lambda x: f'{x:+.2f}%'))

    # Best method per config
    print("\n🏆 BEST METHOD PER CONFIGURATION")
    print("-" * 60)
    for config in pivot.index:
        best_method = pivot.loc[config].idxmax()
        best_fidelity = pivot.loc[config].max()
        worst_method = pivot.loc[config].idxmin()
        worst_fidelity = pivot.loc[config].min()

        improvement = ((best_fidelity - worst_fidelity) / worst_fidelity) * 100

        print(f"   {config}:")
        print(f"      Best:  {best_method:<12} (Fidelity: {best_fidelity:.6f})")
        print(f"      Worst: {worst_method:<12} (Fidelity: {worst_fidelity:.6f})")
        print(f"      Improvement: {improvement:.2f}%")

    return pivot


def create_tvd_comparison_table(df):
    """Create TVD (Total Variation Distance) comparison table."""
    print("\n" + "="*120)
    print("📉 TOTAL VARIATION DISTANCE (TVD) COMPARISON")
    print("="*120)
    print("Lower TVD = Better (closer to ideal state)")

    pivot = df.pivot_table(
        index='config',
        columns='method',
        values='tvd',
        aggfunc='mean'
    )

    method_order = ['Baseline', 'ZNE', 'Opt-0', 'Opt-3', 'Opt-0+ZNE', 'Opt-3+ZNE']
    pivot = pivot[[col for col in method_order if col in pivot.columns]]

    print("\n📊 TVD VALUES")
    print(pivot.to_string(float_format=lambda x: f'{x:.6f}'))

    # Calculate reduction from baseline
    print("\n📉 TVD REDUCTION FROM BASELINE (%)")
    baseline = pivot['Baseline']
    reduction = pd.DataFrame()

    for col in pivot.columns:
        if col != 'Baseline':
            reduction[col] = ((baseline - pivot[col]) / baseline * 100)

    print(reduction.to_string(float_format=lambda x: f'{x:+.2f}%'))

    return pivot


def create_runtime_analysis(df):
    """Analyze runtime across all methods."""
    print("\n" + "="*120)
    print("⏱️  RUNTIME ANALYSIS")
    print("="*120)

    pivot = df.pivot_table(
        index='config',
        columns='method',
        values='total_time',
        aggfunc='mean'
    )

    method_order = ['Baseline', 'ZNE', 'Opt-0', 'Opt-3', 'Opt-0+ZNE', 'Opt-3+ZNE']
    pivot = pivot[[col for col in method_order if col in pivot.columns]]

    print("\n📊 TOTAL RUNTIME (seconds)")
    print(pivot.to_string(float_format=lambda x: f'{x:.2f}'))

    # Calculate overhead
    print("\n⏲️  RUNTIME OVERHEAD VS BASELINE (seconds)")
    baseline = pivot['Baseline']
    overhead = pd.DataFrame()

    for col in pivot.columns:
        if col != 'Baseline':
            overhead[col] = pivot[col] - baseline

    print(overhead.to_string(float_format=lambda x: f'{x:+.2f}s'))

    # Runtime breakdown
    print("\n🔍 DETAILED RUNTIME BREAKDOWN (Average across all configs)")
    print("-" * 80)

    breakdown_cols = ['keygen_time', 'encrypt_time', 'transpile_time',
                     'exec_time', 'eval_time', 'decrypt_time']

    breakdown = df.groupby('method')[breakdown_cols].mean()

    print(breakdown.to_string(float_format=lambda x: f'{x:.3f}'))

    return pivot


def create_performance_efficiency_analysis(df):
    """Analyze performance/time efficiency."""
    print("\n" + "="*120)
    print("⚖️  PERFORMANCE vs EFFICIENCY ANALYSIS")
    print("="*120)

    # Calculate efficiency metric: Fidelity / Runtime
    df['efficiency'] = df['fidelity'] / df['total_time']

    pivot = df.pivot_table(
        index='config',
        columns='method',
        values='efficiency',
        aggfunc='mean'
    )

    method_order = ['Baseline', 'ZNE', 'Opt-0', 'Opt-3', 'Opt-0+ZNE', 'Opt-3+ZNE']
    pivot = pivot[[col for col in method_order if col in pivot.columns]]

    print("\n📊 EFFICIENCY METRIC (Fidelity/Second)")
    print("Higher = Better (more fidelity per unit time)")
    print(pivot.to_string(float_format=lambda x: f'{x:.6f}'))

    # Best efficiency per config
    print("\n🏆 MOST EFFICIENT METHOD PER CONFIGURATION")
    print("-" * 60)
    for config in pivot.index:
        best_method = pivot.loc[config].idxmax()
        best_eff = pivot.loc[config].max()

        print(f"   {config}: {best_method:<12} (Efficiency: {best_eff:.6f})")

    return pivot


def create_method_rankings(df):
    """Create overall rankings for each method."""
    print("\n" + "="*120)
    print("🏅 OVERALL METHOD RANKINGS")
    print("="*120)

    rankings = df.groupby('method').agg({
        'fidelity': ['mean', 'std'],
        'tvd': ['mean', 'std'],
        'total_time': ['mean', 'std']
    }).round(6)

    # Calculate composite scores
    fidelity_scores = df.groupby('method')['fidelity'].mean()
    tvd_scores = 1 - df.groupby('method')['tvd'].mean()  # Invert (lower TVD is better)
    time_scores = 1 / df.groupby('method')['total_time'].mean()  # Invert (lower time is better)

    # Normalize to 0-1
    fidelity_norm = (fidelity_scores - fidelity_scores.min()) / (fidelity_scores.max() - fidelity_scores.min())
    tvd_norm = (tvd_scores - tvd_scores.min()) / (tvd_scores.max() - tvd_scores.min())
    time_norm = (time_scores - time_scores.min()) / (time_scores.max() - time_scores.min())

    # Composite score (weighted: 50% fidelity, 30% TVD, 20% time)
    composite = 0.5 * fidelity_norm + 0.3 * tvd_norm + 0.2 * time_norm

    ranking_df = pd.DataFrame({
        'Avg Fidelity': fidelity_scores,
        'Avg TVD': df.groupby('method')['tvd'].mean(),
        'Avg Time (s)': df.groupby('method')['total_time'].mean(),
        'Composite Score': composite
    }).round(6)

    ranking_df = ranking_df.sort_values('Composite Score', ascending=False)

    print("\n📊 METHOD COMPARISON")
    print(ranking_df.to_string())

    print("\n🏆 OVERALL RANKING (by Composite Score)")
    print("-" * 60)
    for rank, (method, row) in enumerate(ranking_df.iterrows(), 1):
        medal = {1: '🥇', 2: '🥈', 3: '🥉'}.get(rank, f'{rank}.')
        print(f"   {medal} {method:<12} (Score: {row['Composite Score']:.4f})")

    return ranking_df


def create_recommendation_summary(df):
    """Generate recommendations based on results."""
    print("\n" + "="*120)
    print("💡 RECOMMENDATIONS")
    print("="*120)

    # Analyze which method is best for different use cases
    fidelity_best = df.groupby('method')['fidelity'].mean().idxmax()
    time_best = df.groupby('method')['total_time'].mean().idxmin()

    df['efficiency'] = df['fidelity'] / df['total_time']
    efficiency_best = df.groupby('method')['efficiency'].mean().idxmax()

    print("\n🎯 USE CASE RECOMMENDATIONS:")
    print("-" * 60)

    print(f"\n1. **Best Fidelity** (Maximum accuracy):")
    print(f"   → {fidelity_best}")
    fid_val = df[df['method'] == fidelity_best]['fidelity'].mean()
    time_val = df[df['method'] == fidelity_best]['total_time'].mean()
    print(f"      Avg Fidelity: {fid_val:.6f}")
    print(f"      Avg Runtime: {time_val:.2f}s")
    print(f"      Use when: Maximum accuracy is critical, time is not a constraint")

    print(f"\n2. **Fastest Execution** (Minimum time):")
    print(f"   → {time_best}")
    fid_val = df[df['method'] == time_best]['fidelity'].mean()
    time_val = df[df['method'] == time_best]['total_time'].mean()
    print(f"      Avg Fidelity: {fid_val:.6f}")
    print(f"      Avg Runtime: {time_val:.2f}s")
    print(f"      Use when: Quick results needed, some accuracy loss acceptable")

    print(f"\n3. **Best Efficiency** (Fidelity/Time ratio):")
    print(f"   → {efficiency_best}")
    fid_val = df[df['method'] == efficiency_best]['fidelity'].mean()
    time_val = df[df['method'] == efficiency_best]['total_time'].mean()
    eff_val = df[df['method'] == efficiency_best]['efficiency'].mean()
    print(f"      Avg Fidelity: {fid_val:.6f}")
    print(f"      Avg Runtime: {time_val:.2f}s")
    print(f"      Efficiency: {eff_val:.6f}")
    print(f"      Use when: Balanced performance needed")

    print("\n📋 GENERAL GUIDELINES:")
    print("-" * 60)
    print("• Baseline: Fast prototyping, quick tests")
    print("• ZNE: Error mitigation needed, moderate runtime acceptable")
    print("• Opt-0: Minimal transpilation, preserve circuit structure")
    print("• Opt-3: Heavy optimization, reduce circuit depth")
    print("• Opt-0+ZNE: Error mitigation with minimal optimization")
    print("• Opt-3+ZNE: Maximum accuracy, both optimization and error mitigation")

    print("\n⚠️  CONSIDERATIONS:")
    print("-" * 60)
    print("• ZNE adds ~15-25s overhead but can significantly improve fidelity")
    print("• Opt-3 adds ~5s transpilation but reduces circuit depth/gates")
    print("• For production: Use Opt-3+ZNE for best results")
    print("• For development: Use Baseline or Opt-0 for speed")
    print("• For research: Compare all methods to understand tradeoffs")


def generate_summary_statistics(df):
    """Generate comprehensive summary statistics."""
    print("\n" + "="*120)
    print("📈 SUMMARY STATISTICS")
    print("="*120)

    print("\n🔢 DATASET OVERVIEW:")
    print(f"   Total experiments: {len(df)}")
    print(f"   Configurations tested: {df['config'].nunique()}")
    print(f"   Methods tested: {df['method'].nunique()}")
    print(f"   Backends used: {df['backend'].nunique()}")

    print("\n📊 FIDELITY STATISTICS:")
    print(f"   Overall mean: {df['fidelity'].mean():.6f}")
    print(f"   Overall std: {df['fidelity'].std():.6f}")
    print(f"   Best result: {df['fidelity'].max():.6f} ({df.loc[df['fidelity'].idxmax(), 'config']} - {df.loc[df['fidelity'].idxmax(), 'method']})")
    print(f"   Worst result: {df['fidelity'].min():.6f} ({df.loc[df['fidelity'].idxmin(), 'config']} - {df.loc[df['fidelity'].idxmin(), 'method']})")

    print("\n⏱️  RUNTIME STATISTICS:")
    print(f"   Overall mean: {df['total_time'].mean():.2f}s")
    print(f"   Overall std: {df['total_time'].std():.2f}s")
    print(f"   Fastest: {df['total_time'].min():.2f}s ({df.loc[df['total_time'].idxmin(), 'config']} - {df.loc[df['total_time'].idxmin(), 'method']})")
    print(f"   Slowest: {df['total_time'].max():.2f}s ({df.loc[df['total_time'].idxmax(), 'config']} - {df.loc[df['total_time'].idxmax(), 'method']})")

    print("\n🔬 TVD STATISTICS:")
    print(f"   Overall mean: {df['tvd'].mean():.6f}")
    print(f"   Overall std: {df['tvd'].std():.6f}")
    print(f"   Best (lowest): {df['tvd'].min():.6f} ({df.loc[df['tvd'].idxmin(), 'config']} - {df.loc[df['tvd'].idxmin(), 'method']})")
    print(f"   Worst (highest): {df['tvd'].max():.6f} ({df.loc[df['tvd'].idxmax(), 'config']} - {df.loc[df['tvd'].idxmax(), 'method']})")


def create_visualization_plots(df):
    """Create comprehensive visualization plots."""
    print("\n📊 Generating visualization plots...")

    sns.set_style("whitegrid")
    fig = plt.figure(figsize=(20, 12))

    # 1. Fidelity comparison across methods
    ax1 = plt.subplot(2, 3, 1)
    pivot_fid = df.pivot_table(index='config', columns='method', values='fidelity')
    pivot_fid.plot(kind='bar', ax=ax1)
    ax1.set_title('Fidelity Comparison Across Methods', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Configuration')
    ax1.set_ylabel('Fidelity')
    ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax1.grid(True, alpha=0.3)

    # 2. TVD comparison
    ax2 = plt.subplot(2, 3, 2)
    pivot_tvd = df.pivot_table(index='config', columns='method', values='tvd')
    pivot_tvd.plot(kind='bar', ax=ax2)
    ax2.set_title('Total Variation Distance (Lower is Better)', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Configuration')
    ax2.set_ylabel('TVD')
    ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax2.grid(True, alpha=0.3)

    # 3. Runtime comparison
    ax3 = plt.subplot(2, 3, 3)
    pivot_time = df.pivot_table(index='config', columns='method', values='total_time')
    pivot_time.plot(kind='bar', ax=ax3)
    ax3.set_title('Total Runtime Comparison', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Configuration')
    ax3.set_ylabel('Runtime (s)')
    ax3.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax3.grid(True, alpha=0.3)

    # 4. Fidelity vs Runtime scatter
    ax4 = plt.subplot(2, 3, 4)
    for method in df['method'].unique():
        method_df = df[df['method'] == method]
        ax4.scatter(method_df['total_time'], method_df['fidelity'],
                   label=method, s=100, alpha=0.7)
    ax4.set_title('Fidelity vs Runtime Tradeoff', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Runtime (s)')
    ax4.set_ylabel('Fidelity')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # 5. Method performance heatmap
    ax5 = plt.subplot(2, 3, 5)
    heatmap_data = df.pivot_table(index='method', columns='config', values='fidelity')
    sns.heatmap(heatmap_data, annot=True, fmt='.4f', cmap='RdYlGn',
                ax=ax5, cbar_kws={'label': 'Fidelity'})
    ax5.set_title('Fidelity Heatmap (Method vs Config)', fontsize=14, fontweight='bold')
    ax5.set_xlabel('Configuration')
    ax5.set_ylabel('Method')

    # 6. Efficiency comparison
    ax6 = plt.subplot(2, 3, 6)
    df['efficiency'] = df['fidelity'] / df['total_time']
    efficiency_avg = df.groupby('method')['efficiency'].mean().sort_values(ascending=False)
    efficiency_avg.plot(kind='barh', ax=ax6, color='steelblue')
    ax6.set_title('Overall Efficiency (Fidelity/Time)', fontsize=14, fontweight='bold')
    ax6.set_xlabel('Efficiency (Fidelity/Second)')
    ax6.set_ylabel('Method')
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()

    # Save plot
    plot_file = 'ibm_noise_measurement_analysis.png'
    plt.savefig(plot_file, dpi=300, bbox_inches='tight')
    print(f"   ✅ Visualization saved to: {plot_file}")

    plt.close()


def main():
    """Main analysis function."""
    print("\n" + "="*120)
    print("🔬 IBM QUANTUM HARDWARE - NOISE MEASUREMENT ANALYSIS")
    print("="*120)

    # Load results
    df = load_latest_results()

    if df is None:
        return

    # Generate all analysis
    generate_summary_statistics(df)
    create_fidelity_comparison_table(df)
    create_tvd_comparison_table(df)
    create_runtime_analysis(df)
    create_performance_efficiency_analysis(df)
    create_method_rankings(df)
    create_recommendation_summary(df)

    # Create visualizations
    create_visualization_plots(df)

    print("\n" + "="*120)
    print("✅ Analysis completed successfully!")
    print("="*120)


if __name__ == "__main__":
    main()
