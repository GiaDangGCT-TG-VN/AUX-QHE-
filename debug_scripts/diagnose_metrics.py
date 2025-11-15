#!/usr/bin/env python3
"""
Diagnose Weird Fidelity Metrics

This script analyzes the IBM hardware results to identify issues with:
1. Measurement decoding
2. Fidelity calculation
3. QOTP key computation
"""

import pandas as pd
import json
import numpy as np
from collections import Counter

def analyze_measurement_distribution(decoded_counts, num_qubits):
    """Analyze if measurement distribution looks reasonable"""
    print(f"\n📊 Measurement Distribution Analysis")
    print(f"   Num qubits: {num_qubits}")
    print(f"   Num unique outcomes: {len(decoded_counts)}")
    print(f"   Expected max outcomes: {2**num_qubits}")

    # Calculate entropy
    total = sum(decoded_counts.values())
    probs = [count/total for count in decoded_counts.values()]
    entropy = -sum(p * np.log2(p) for p in probs if p > 0)
    max_entropy = num_qubits  # Maximum entropy for uniform distribution

    print(f"   Entropy: {entropy:.4f} / {max_entropy:.4f}")
    print(f"   Entropy ratio: {entropy/max_entropy:.4f}")

    # Show top outcomes
    print(f"\n   Top 5 outcomes:")
    for bitstring, count in sorted(decoded_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
        prob = count / total
        print(f"      {bitstring}: {count} ({prob*100:.2f}%)")

    # Check if distribution is too uniform (might indicate decoding issue)
    if len(decoded_counts) > 5:
        counts_list = list(decoded_counts.values())
        std_dev = np.std(counts_list)
        mean = np.mean(counts_list)
        cv = std_dev / mean if mean > 0 else 0
        print(f"\n   Coefficient of variation: {cv:.4f}")
        if cv < 0.3:
            print(f"   ⚠️  WARNING: Distribution is very uniform (CV < 0.3)")
            print(f"      This might indicate a decoding issue!")

def check_qotp_keys(final_a, final_b):
    """Check if QOTP keys look reasonable"""
    print(f"\n🔑 QOTP Key Analysis")
    print(f"   Final a keys: {final_a}")
    print(f"   Final b keys: {final_b}")

    # Check if all zeros (suspicious for non-trivial circuit)
    if all(k == 0 for k in final_a) and all(k == 0 for k in final_b):
        print(f"   ⚠️  WARNING: All keys are zero!")
        print(f"      This is suspicious for a non-trivial circuit.")
        print(f"      QOTP decoding might have no effect.")

def analyze_fidelity_calculation(fidelity, tvd, config):
    """Analyze if fidelity value makes sense"""
    print(f"\n📈 Fidelity Analysis for {config}")
    print(f"   Fidelity: {fidelity:.6f}")
    print(f"   TVD: {tvd:.6f}")

    # Check for suspicious patterns
    if fidelity < 0.001:
        print(f"   ⚠️  WARNING: Fidelity extremely low (< 0.1%)")
        print(f"      Possible causes:")
        print(f"      - Wrong ideal state comparison")
        print(f"      - Measurement decoding error")
        print(f"      - Severe hardware noise")

    if fidelity > 0.5:
        print(f"   ✅ GOOD: Fidelity > 50%")
    elif fidelity > 0.1:
        print(f"   ⚠️  OK: Fidelity 10-50% (high noise but plausible)")
    elif fidelity > 0.01:
        print(f"   ⚠️  LOW: Fidelity 1-10% (very high noise)")
    else:
        print(f"   ❌ SUSPICIOUS: Fidelity < 1%")

def diagnose_single_result(result_row):
    """Diagnose a single result row"""
    config = result_row['config']
    method = result_row['method']
    fidelity = result_row['fidelity']
    tvd = result_row['tvd']
    num_qubits = result_row['num_qubits']

    print(f"\n{'='*80}")
    print(f"🔍 Diagnosing: {config} - {method}")
    print(f"{'='*80}")

    # Parse decoded counts
    try:
        decoded_counts = eval(result_row['decoded_counts'])
        if isinstance(decoded_counts, dict):
            analyze_measurement_distribution(decoded_counts, num_qubits)
        else:
            print(f"⚠️  WARNING: decoded_counts is not a dict: {type(decoded_counts)}")
    except Exception as e:
        print(f"❌ Error parsing decoded_counts: {e}")

    # Parse final QOTP keys
    try:
        final_keys = eval(result_row['final_qotp_keys'])
        if isinstance(final_keys, dict) and 'a' in final_keys and 'b' in final_keys:
            check_qotp_keys(final_keys['a'], final_keys['b'])
        else:
            print(f"⚠️  WARNING: final_qotp_keys format unexpected: {final_keys}")
    except Exception as e:
        print(f"❌ Error parsing final_qotp_keys: {e}")

    # Analyze fidelity
    analyze_fidelity_calculation(fidelity, tvd, f"{config}-{method}")

def compare_methods(df):
    """Compare fidelity across methods to find patterns"""
    print(f"\n{'='*80}")
    print(f"📊 METHOD COMPARISON")
    print(f"{'='*80}\n")

    # Group by config and method
    pivot = df.pivot_table(values='fidelity', index='config', columns='method')

    print("Fidelity by Config and Method:")
    print(pivot.to_string())

    print(f"\n🎯 Suspicious Patterns:")

    # Check if ZNE is worse than baseline
    for config in pivot.index:
        if 'Baseline' in pivot.columns and 'ZNE' in pivot.columns:
            baseline = pivot.loc[config, 'Baseline']
            zne = pivot.loc[config, 'ZNE']
            if pd.notna(baseline) and pd.notna(zne):
                if zne < baseline * 0.9:  # ZNE is 10% worse
                    print(f"   ⚠️  {config}: ZNE ({zne:.6f}) worse than Baseline ({baseline:.6f})")

    # Check if Opt-3 is much worse than Opt-1
    for config in pivot.index:
        if 'Baseline' in pivot.columns and 'Opt-3' in pivot.columns:
            baseline = pivot.loc[config, 'Baseline']
            opt3 = pivot.loc[config, 'Opt-3']
            if pd.notna(baseline) and pd.notna(opt3):
                if opt3 < baseline * 0.5:  # Opt-3 is 50% worse
                    print(f"   ⚠️  {config}: Opt-3 ({opt3:.6f}) much worse than Baseline ({baseline:.6f})")

    # Check for same fidelity across different methods (suspicious)
    for config in pivot.index:
        values = pivot.loc[config].dropna()
        if len(values) > 1:
            if values.std() < 0.001:  # All values nearly identical
                print(f"   ⚠️  {config}: All methods have nearly identical fidelity: {values.tolist()}")

def main():
    import glob

    print("="*80)
    print("🔬 FIDELITY METRICS DIAGNOSTIC")
    print("="*80)

    # Find latest results file
    files = glob.glob("ibm_noise_measurement_results_*.csv")
    if not files:
        print("❌ No results files found!")
        return

    latest_file = max(files, key=lambda f: f.split('_')[-1].replace('.csv', ''))
    print(f"\n📂 Analyzing: {latest_file}\n")

    # Load results
    df = pd.read_csv(latest_file)

    print(f"Total results: {len(df)}")
    print(f"Configs: {df['config'].unique()}")
    print(f"Methods: {df['method'].unique()}")

    # Compare methods first
    compare_methods(df)

    # Diagnose each result
    print(f"\n{'='*80}")
    print(f"DETAILED DIAGNOSIS")
    print(f"{'='*80}")

    for idx, row in df.iterrows():
        diagnose_single_result(row)

        # Limit output for readability
        if idx >= 3:  # Only show first 4 results
            remaining = len(df) - idx - 1
            if remaining > 0:
                print(f"\n... ({remaining} more results not shown)")
            break

    print(f"\n{'='*80}")
    print(f"💡 RECOMMENDATIONS")
    print(f"{'='*80}\n")

    print("Based on the analysis:")
    print("1. Check if QOTP decoding is working correctly")
    print("2. Verify that ideal state matches the circuit being executed")
    print("3. Check if measurement bitstring interpretation is correct")
    print("4. Consider if hardware noise is actually this severe")
    print("5. Verify ZNE implementation (should improve, not worsen)")

    print(f"\n{'='*80}")

if __name__ == "__main__":
    main()
