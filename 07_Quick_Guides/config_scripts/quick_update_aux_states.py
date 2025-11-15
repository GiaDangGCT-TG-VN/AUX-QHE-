#!/usr/bin/env python3
"""
Quick update: Generate auxiliary states data with FIXED code (no synthetic terms)

This script updates the CSV with new auxiliary state counts without running
the full performance comparison (which takes 5-10 minutes).

It directly calls aux_keygen() to get the corrected values.
"""

import pandas as pd
import sys
sys.path.insert(0, 'core')

from key_generation import aux_keygen

print('🔄 Updating auxiliary states with FIXED values (no synthetic terms)')
print('='*70)

# Read existing CSV
csv_file = "corrected_openqasm_performance_comparison.csv"
try:
    df = pd.read_csv(csv_file)
    print(f'✅ Read existing CSV: {csv_file}')
except FileNotFoundError:
    print(f'❌ CSV file not found: {csv_file}')
    print('   Please run: python algorithm/openqasm_performance_comparison.py')
    sys.exit(1)

# Configuration mapping
configs = {
    '3q-2t': (3, 2, [1, 0, 1], [0, 1, 0]),
    '3q-3t': (3, 3, [1, 0, 1], [0, 1, 0]),
    '4q-2t': (4, 2, [1, 0, 1, 0], [0, 1, 0, 1]),
    '4q-3t': (4, 3, [1, 0, 1, 0], [0, 1, 0, 1]),
    '5q-2t': (5, 2, [1, 0, 1, 0, 1], [0, 1, 0, 1, 0]),
    '5q-3t': (5, 3, [1, 0, 1, 0, 1], [0, 1, 0, 1, 0])
}

print(f'\n📊 Generating new auxiliary state counts:')
print(f'{'Config':<8} {'OLD':<8} {'NEW':<8} {'Change':<12}')
print('-' * 40)

updated_count = 0

for config_name, (num_qubits, max_t_depth, a_init, b_init) in configs.items():
    # Get NEW auxiliary state count from FIXED code
    try:
        _, _, _, layer_sizes, new_total = aux_keygen(
            num_qubits, max_t_depth, a_init, b_init
        )

        # Find rows matching this config
        mask = df['Config'] == config_name
        old_total = df.loc[mask, 'Aux_States'].iloc[0] if mask.any() else 0

        if old_total != new_total:
            # Update the CSV
            df.loc[mask, 'Aux_States'] = new_total

            change = old_total - new_total
            pct = (change / old_total * 100) if old_total > 0 else 0
            print(f'{config_name:<8} {old_total:<8} {new_total:<8} -{pct:>5.1f}%')
            updated_count += 1
        else:
            print(f'{config_name:<8} {old_total:<8} {new_total:<8} (unchanged)')

    except Exception as e:
        print(f'{config_name:<8} ERROR: {e}')

print('-' * 40)
print(f'\n✅ Updated {updated_count} configurations')

# Save updated CSV
if updated_count > 0:
    # Backup old CSV
    backup_file = csv_file.replace('.csv', '_BACKUP_OLD.csv')
    df_backup = pd.read_csv(csv_file)
    df_backup.to_csv(backup_file, index=False)
    print(f'💾 Backed up old CSV to: {backup_file}')

    # Save new CSV
    df.to_csv(csv_file, index=False)
    print(f'✅ Updated CSV saved: {csv_file}')

    print(f'\n🎉 Success! Now run:')
    print(f'   python generate_auxiliary_analysis_table.py')
    print(f'   to see the updated values in the tables.')
else:
    print(f'\n⚠️  No updates needed - values already current')

print('\n' + '='*70)
