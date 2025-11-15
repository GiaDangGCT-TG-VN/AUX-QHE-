"""
Auxiliary States and Cross-Terms Analysis Table
Separated table showing: Config | Aux States | Prep Time | Total Overhead | Efficiency | Cross-Terms
"""

import numpy as np
import pandas as pd

def create_aux_states_cross_terms_table(export_csv=False):
    """
    Create the specific table: Config | Aux States | Prep Time | Total Overhead | Efficiency | Cross-Terms

    Args:
        export_csv (bool): If True, export to CSV file
    """

    print("📊 AUXILIARY STATES & CROSS-TERMS ANALYSIS")
    print("=" * 84)
    print("Relationship between auxiliary states, preparation time, and cross-term complexity")
    print()

    # Get CORRECT auxiliary states from actual aux_keygen function
    from key_generation import aux_keygen, build_term_sets

    config_specs = [
        ("3q-2t", 3, 2), ("3q-3t", 3, 3), ("4q-2t", 4, 2),
        ("4q-3t", 4, 3), ("5q-2t", 5, 2), ("5q-3t", 5, 3)
    ]

    # Table header
    print(f"{'Config':<8} {'Aux States':<11} {'Prep Time':<10} {'Total Overhead':<15} {'Efficiency':<12} {'Cross-Terms':<12}")
    print("-" * 84)

    table_data = []

    for config_name, qubits, t_depth in config_specs:
        try:
            # Get real auxiliary states and prep time from aux_keygen
            _, _, real_prep_time, layer_sizes, real_aux_states = aux_keygen(qubits, t_depth)

            # Calculate overhead based on real aux states
            t_gadget_time = 0.1 + (t_depth * 0.05) + (qubits * 0.02)

            if real_aux_states > 10000:
                aux_management = 0.3 + (real_aux_states / 100000) * 4
            elif real_aux_states > 1000:
                aux_management = 0.1 + (real_aux_states / 10000) * 1.5
            else:
                aux_management = 0.05 + (real_aux_states / 1000) * 0.3

            poly_eval_time = 0.02 + (qubits * 0.01) + (t_depth * 0.01)
            total_overhead = t_gadget_time + aux_management + poly_eval_time

            # Calculate efficiency
            efficiency = real_aux_states / (real_prep_time + total_overhead)

            # Get T-set cross-terms (the real cross-terms from aux_keygen logs)
            T_sets, _ = build_term_sets(qubits, t_depth)
            final_layer_terms = T_sets[t_depth]
            t_set_cross_terms = len([term for term in final_layer_terms if '*' in term])

            # Print table row
            print(f"{config_name:<8} {real_aux_states:<11} {real_prep_time:<10.4f} {total_overhead:<15.3f} {efficiency:<12.1f} {t_set_cross_terms}")

            # Store data for CSV export
            table_data.append({
                'Config': config_name,
                'Qubits': qubits,
                'T_Depth': t_depth,
                'Aux_States': real_aux_states,
                'Layer_Sizes': str(layer_sizes),
                'Prep_Time_s': real_prep_time,
                'Total_Overhead_s': total_overhead,
                'Efficiency': efficiency,
                'T_Set_Cross_Terms': t_set_cross_terms,
                'T_Gadget_Time_s': t_gadget_time,
                'Aux_Management_s': aux_management,
                'Poly_Eval_Time_s': poly_eval_time
            })

        except Exception as e:
            print(f"❌ Error processing {config_name}: {e}")

    print("-" * 84)
    print("Key Insights:")
    print("• CORRECTED auxiliary states using real aux_keygen() results")
    print("• Efficiency = aux_states / (prep_time + overhead)")
    print("• Cross-Terms = cross-product terms in T-sets (for auxiliary state generation)")
    print("• Higher efficiency indicates better auxiliary state utilization")
    print("• T-set cross-terms drive auxiliary preparation complexity")

    # Export to CSV if requested
    if export_csv and table_data:
        df = pd.DataFrame(table_data)
        csv_filename = "aux_states_cross_terms_table.csv"
        df.to_csv(csv_filename, index=False)
        print(f"\n💾 Table exported to CSV: {csv_filename}")
        print(f"📊 {len(table_data)} rows × {len(df.columns)} columns")
        return csv_filename

    return table_data

def create_detailed_breakdown_table():
    """Create a more detailed breakdown of the auxiliary states and cross-terms."""

    print("\n🔬 DETAILED AUXILIARY STATES BREAKDOWN")
    print("=" * 100)
    print("Layer-by-layer analysis of auxiliary states and cross-term growth")
    print()

    # Get data from aux_keygen
    from key_generation import aux_keygen, build_term_sets

    config_specs = [
        ("3q-2t", 3, 2), ("3q-3t", 3, 3), ("4q-2t", 4, 2),
        ("4q-3t", 4, 3), ("5q-2t", 5, 2), ("5q-3t", 5, 3)
    ]

    print(f"{'Config':<8} {'Layer':<7} {'Total Terms':<12} {'Cross-Terms':<12} {'Aux States':<12} {'Cross %':<10}")
    print("-" * 100)

    for config_name, qubits, t_depth in config_specs:
        try:
            # Get layer information
            T_sets, _ = build_term_sets(qubits, t_depth)
            _, _, _, layer_sizes, total_aux_states = aux_keygen(qubits, t_depth)

            for layer in range(1, t_depth + 1):
                layer_terms = T_sets[layer]
                total_terms = len(layer_terms)
                cross_terms = len([term for term in layer_terms if '*' in term])
                layer_aux_states = qubits * total_terms  # aux states for this layer
                cross_percentage = (cross_terms / total_terms * 100) if total_terms > 0 else 0

                config_label = config_name if layer == 1 else ""
                print(f"{config_label:<8} L{layer:<6} {total_terms:<12} {cross_terms:<12} {layer_aux_states:<12} {cross_percentage:<10.1f}%")

            # Add total row
            print(f"{'TOTAL':<8} {'ALL':<6} {'-':<12} {'-':<12} {total_aux_states:<12} {'-':<10}")
            if config_name != config_specs[-1][0]:  # Not last config
                print("-" * 100)

        except Exception as e:
            print(f"❌ Error processing {config_name}: {e}")

    print("-" * 100)
    print("Legend:")
    print("• Layer: T-depth layer (L1, L2, L3)")
    print("• Total Terms: |T[ℓ]| - total terms in T-set for this layer")
    print("• Cross-Terms: Number of cross-product terms like (a₀)*(b₁)")
    print("• Aux States: Number of auxiliary states for this layer")
    print("• Cross %: Percentage of terms that are cross-products")

if __name__ == "__main__":
    # Create the main table
    create_aux_states_cross_terms_table(export_csv=True)

    # Create the detailed breakdown
    create_detailed_breakdown_table()

    print("\n✅ Auxiliary states and cross-terms analysis completed!")
    print("📋 For CSV export: python aux_states_cross_terms_table.py")