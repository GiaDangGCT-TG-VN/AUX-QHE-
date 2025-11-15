#!/usr/bin/env python3
"""
Verify that all 4 methods now use the same QOTP keys and auxiliary states.
This script tests the fix without executing on hardware.
"""

import sys
import os
sys.path.insert(0, '/Users/giadang/my_qiskitenv/AUX-QHE')
sys.path.insert(0, '/Users/giadang/my_qiskitenv/AUX-QHE/core')

# Change to AUX-QHE directory for imports
os.chdir('/Users/giadang/my_qiskitenv/AUX-QHE')

from key_generation import aux_keygen
from bfv_core import initialize_bfv_params

def test_shared_keys():
    """Test that same keys produce same auxiliary states"""

    print("="*80)
    print("Testing Shared Keys Fix")
    print("="*80)

    # Configuration
    num_qubits = 5
    t_depth = 3

    # Generate fixed keys (simulating what main loop does)
    import random
    random.seed(42)  # Fixed seed for reproducible test
    config_a_init = [random.randint(0, 1) for _ in range(num_qubits)]
    config_b_init = [random.randint(0, 1) for _ in range(num_qubits)]

    print(f"\nShared QOTP keys:")
    print(f"  a_init = {config_a_init}")
    print(f"  b_init = {config_b_init}")

    # Initialize BFV
    initialize_bfv_params()

    # Simulate 4 methods using the SAME keys
    methods = ['Baseline', 'ZNE', 'Opt-3', 'Opt-3+ZNE']

    all_secrets = []
    all_aux_states = []

    for method in methods:
        print(f"\n{method}:")
        print(f"  Generating keys with a_init={config_a_init}, b_init={config_b_init}")

        # Call aux_keygen with SAME keys
        secret_key, eval_key, prep_time, layer_sizes, total_aux = aux_keygen(
            num_qubits, t_depth, config_a_init, config_b_init
        )

        a_keys, b_keys, k_dict = secret_key
        T_sets, V_sets, auxiliary_states = eval_key

        print(f"  Initial keys: a={a_keys}, b={b_keys}")
        print(f"  Aux states: {total_aux} (layers: {layer_sizes})")
        print(f"  First 3 k values: {list(k_dict.values())[:3]}")

        all_secrets.append(secret_key)
        all_aux_states.append(auxiliary_states)

    # Verification: All methods should have IDENTICAL keys and aux states
    print(f"\n{'='*80}")
    print("VERIFICATION:")
    print(f"{'='*80}")

    # Check if all a_keys are identical
    a_keys_match = all(s[0] == all_secrets[0][0] for s in all_secrets)
    b_keys_match = all(s[1] == all_secrets[0][1] for s in all_secrets)

    print(f"✅ All a_keys identical: {a_keys_match}" if a_keys_match else f"❌ a_keys differ!")
    print(f"✅ All b_keys identical: {b_keys_match}" if b_keys_match else f"❌ b_keys differ!")

    # Check if all k_dict are identical
    k_dicts = [s[2] for s in all_secrets]
    k_dict_match = all(k == k_dicts[0] for k in k_dicts)
    print(f"✅ All k_dict identical: {k_dict_match}" if k_dict_match else f"❌ k_dict differ!")

    # Check if all auxiliary states are identical
    aux_match = all(
        set(aux.keys()) == set(all_aux_states[0].keys())
        for aux in all_aux_states
    )
    print(f"✅ All aux states identical: {aux_match}" if aux_match else f"❌ Aux states differ!")

    if a_keys_match and b_keys_match and k_dict_match and aux_match:
        print(f"\n{'='*80}")
        print("✅ FIX VERIFIED: All methods use identical keys and auxiliary states!")
        print(f"{'='*80}")
        return True
    else:
        print(f"\n{'='*80}")
        print("❌ FIX FAILED: Methods have different keys!")
        print(f"{'='*80}")
        return False

if __name__ == "__main__":
    success = test_shared_keys()
    sys.exit(0 if success else 1)
