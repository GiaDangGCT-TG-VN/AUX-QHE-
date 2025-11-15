#!/usr/bin/env python3
"""
Update 5q-2t Hardware Results in Paper Table
Compares OLD (1,350 aux states) vs NEW (575 aux states) results
"""

import json

# Load new results
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

# Old results (from local_vs_hardware_comparison.csv)
old_results_5q2t = {
    'Baseline': {'aux_states': 1350, 'fidelity': 0.027871, 'tvd': 0.900391},
    'ZNE': {'aux_states': 1350, 'fidelity': 0.025815, 'tvd': 0.910392},
    'Opt-3': {'aux_states': 1350, 'fidelity': 0.028631, 'tvd': 0.916016},
    'Opt-3+ZNE': {'aux_states': 1350, 'fidelity': 0.033934, 'tvd': 0.898592}
}

print("="*80)
print("5q-2t HARDWARE RESULTS COMPARISON")
print("="*80)

print("\n📊 OLD RESULTS (1,350 auxiliary states):")
print("-"*80)
print(f"{'Method':<15} {'Aux States':>12} {'Fidelity':>12} {'TVD':>12}")
print("-"*80)
for method in ['Baseline', 'ZNE', 'Opt-3', 'Opt-3+ZNE']:
    old = old_results_5q2t[method]
    print(f"{method:<15} {old['aux_states']:>12} {old['fidelity']:>12.6f} {old['tvd']:>12.6f}")

print("\n📊 NEW RESULTS (575 auxiliary states):")
print("-"*80)
print(f"{'Method':<15} {'Aux States':>12} {'Fidelity':>12} {'TVD':>12} {'Depth':>8} {'Gates':>8}")
print("-"*80)
for method in ['Baseline', 'ZNE', 'Opt-3', 'Opt-3+ZNE']:
    new = results_5q2t[method]
    print(f"{method:<15} {new['aux_states']:>12} {new['fidelity']:>12.6f} {new['tvd']:>12.6f} {new['circuit_depth']:>8} {new['circuit_gates']:>8}")

print("\n📈 IMPROVEMENT ANALYSIS:")
print("-"*80)
print(f"{'Method':<15} {'Old Fidelity':>14} {'New Fidelity':>14} {'Improvement':>14} {'Status':>10}")
print("-"*80)
for method in ['Baseline', 'ZNE', 'Opt-3', 'Opt-3+ZNE']:
    old_fid = old_results_5q2t[method]['fidelity']
    new_fid = results_5q2t[method]['fidelity']
    improvement = ((new_fid - old_fid) / old_fid) * 100
    status = "✅ Better" if improvement > 0 else "❌ Worse"
    print(f"{method:<15} {old_fid:>14.6f} {new_fid:>14.6f} {improvement:>13.1f}% {status:>10}")

print("\n📝 LATEX TABLE UPDATE:")
print("="*80)
print("Replace the 5q-T2 row in Table 'Detailed Fidelity of Optimization Levels + ZNE'")
print("\nOLD (in paper):")
print("5q-T2 & 0.0117 & 0.0144 & 0.5040 & 0.6048 & 0.5880 & 0.7056 & 0.6440 & 0.7728 \\\\")

print("\nNEW (based on your actual data):")
print("If table has 8 columns (Baseline, ZNE, Opt-0, Opt-0+ZNE, Opt-1, Opt-1+ZNE, Opt-3, Opt-3+ZNE):")
print(f"5q-T2 & {results_5q2t['Baseline']['fidelity']:.4f} & {results_5q2t['ZNE']['fidelity']:.4f} & N/A & N/A & N/A & N/A & {results_5q2t['Opt-3']['fidelity']:.4f} & {results_5q2t['Opt-3+ZNE']['fidelity']:.4f} \\\\")

print("\nOR if you want to update table to show only 4 methods (Baseline, ZNE, Opt-3, Opt-3+ZNE):")
print(f"5q-T2 & {results_5q2t['Baseline']['fidelity']:.4f} & {results_5q2t['ZNE']['fidelity']:.4f} & {results_5q2t['Opt-3']['fidelity']:.4f} & {results_5q2t['Opt-3+ZNE']['fidelity']:.4f} \\\\")

print("\n⚠️  IMPORTANT OBSERVATIONS:")
print("="*80)

best_old = max(old_results_5q2t.items(), key=lambda x: x[1]['fidelity'])
best_new = max(results_5q2t.items(), key=lambda x: x[1]['fidelity'])

print(f"1. Best OLD method: {best_old[0]} = {best_old[1]['fidelity']:.6f}")
print(f"2. Best NEW method: {best_new[0]} = {best_new[1]['fidelity']:.6f}")
print(f"3. Auxiliary states: 1,350 → 575 (57.4% reduction)")
print(f"4. Overall improvement: {((best_new[1]['fidelity'] - best_old[1]['fidelity']) / best_old[1]['fidelity']) * 100:.1f}%")

print("\n⚠️  UNEXPECTED FINDING:")
print("="*80)
print(f"Baseline OLD: {old_results_5q2t['Baseline']['fidelity']:.6f}")
print(f"Baseline NEW: {results_5q2t['Baseline']['fidelity']:.6f}")
improvement_baseline = ((results_5q2t['Baseline']['fidelity'] - old_results_5q2t['Baseline']['fidelity']) / old_results_5q2t['Baseline']['fidelity']) * 100
print(f"Baseline improvement: {improvement_baseline:+.1f}%")

if improvement_baseline > 0:
    print(f"✅ As expected: Fewer aux states (575 vs 1,350) improved fidelity")
else:
    print(f"❌ Unexpected: Fewer aux states but lower fidelity - possible causes:")
    print(f"   - Different IBM backend state (noise levels changed)")
    print(f"   - Different qubit allocation")
    print(f"   - Queue congestion (you had 3,674 jobs ahead)")
    print(f"   - Different QOTP keys (randomness)")

print("\n" + "="*80)
