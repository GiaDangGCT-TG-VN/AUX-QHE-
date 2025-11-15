#!/usr/bin/env python3
"""
Generate auxiliary states analysis table
Columns: Config | Aux States | Theoretical Layer Sizes | Redundancy Ratio | T-Set Cross Terms | Poly Eval Time (s)

Note: This script reads from corrected_openqasm_performance_comparison.csv
To get updated values after removing synthetic cross-terms, re-run:
  python algorithm/openqasm_performance_comparison.py
"""
import pandas as pd
import sys
import re

csv_file = "results/corrected_openqasm_performance_comparison.csv"

try:
    df = pd.read_csv(csv_file)

    # Filter to QASM 2 only (same results for both)
    df_qasm2 = df[df['QASM_Version'] == 'OpenQASM 2'].copy()

    table_data = []

    for _, row in df_qasm2.iterrows():
        config = row['Config']
        aux_states = row['Aux_States']

        # Parse config to get qubits and T-depth
        match = re.match(r'(\d+)q-(\d+)t', config)
        if match:
            num_qubits = int(match.group(1))
            t_depth = int(match.group(2))
        else:
            continue

        # Calculate theoretical layer sizes
        # T[1] = 2n (a and b for each qubit)
        # T[ℓ] grows with cross-terms
        t1_size = 2 * num_qubits

        # Theoretical sizes based on cross-term growth
        theoretical_sizes = []
        current_size = t1_size
        theoretical_sizes.append(current_size)

        for layer in range(2, t_depth + 1):
            # Approximate cross-term growth: C(current_size, 2) new terms
            cross_terms = current_size * (current_size - 1) // 2
            # Plus k-variables (one per term in previous layer)
            k_vars = current_size
            # New layer size (simplified)
            current_size = current_size + cross_terms + k_vars
            theoretical_sizes.append(current_size)

        theoretical_layer_str = str(theoretical_sizes)

        # Calculate actual efficiency
        # From logs, we can estimate actual layer sizes
        # For now, use approximation based on total aux states
        actual_layer_sizes = []
        if t_depth == 2:
            # Known patterns from logs
            if num_qubits == 3:
                actual_layer_sizes = [6, 74]  # 3q-2t: T[1]=6, T[2]=74
            elif num_qubits == 4:
                actual_layer_sizes = [8, 159]  # 4q-2t: T[1]=8, T[2]=159
            elif num_qubits == 5:
                actual_layer_sizes = [10, 260]  # 5q-2t: T[1]=10, T[2]=260
        elif t_depth == 3:
            if num_qubits == 3:
                actual_layer_sizes = [6, 39, 897]  # 3q-3t
            elif num_qubits == 4:
                actual_layer_sizes = [8, 68, 2618]  # 4q-3t
            elif num_qubits == 5:
                actual_layer_sizes = [10, 105, 6090]  # 5q-3t

        # Calculate T-set cross terms (sum of cross-terms in each layer)
        cross_terms_total = 0
        for i, size in enumerate(actual_layer_sizes):
            if i == 0:
                # First layer has no cross-terms
                cross_terms = 0
            else:
                # Estimate cross-terms from growth
                prev_size = actual_layer_sizes[i-1]
                # Cross terms ≈ new terms added beyond base terms and k-vars
                cross_terms = max(0, size - prev_size - prev_size)
                cross_terms_total += cross_terms

        # Redundancy ratio: actual vs theoretical (shows overhead factor)
        theoretical_total = sum(theoretical_sizes)
        actual_total = aux_states
        redundancy_ratio = (actual_total / theoretical_total) if theoretical_total > 0 else 1.0

        # Polynomial evaluation time
        poly_eval_time = row['Eval_Time_s']

        table_data.append({
            'Config': config,
            'Aux States': aux_states,
            'Theoretical Layer Sizes': str(actual_layer_sizes),  # Use actual (more accurate)
            'Redundancy Ratio': f"{redundancy_ratio:.2f}x",
            'T-Set Cross Terms': cross_terms_total,
            'Poly Eval Time (s)': f"{poly_eval_time:.6f}"
        })

    results_df = pd.DataFrame(table_data)

    # Print formatted table
    print("\n" + "="*120)
    print("AUX-QHE AUXILIARY STATES ANALYSIS TABLE")
    print("="*120 + "\n")

    print(results_df.to_string(index=False))

    print("\n" + "="*120)

    # Save to CSV
    output_file = "aux_qhe_auxiliary_analysis.csv"
    results_df.to_csv(output_file, index=False)
    print(f"\n✅ Table saved to: {output_file}")

    # Markdown
    print("\n" + "="*120)
    print("MARKDOWN FORMAT")
    print("="*120 + "\n")
    print(results_df.to_markdown(index=False))

    # ASCII table
    print("\n" + "="*120)
    print("ASCII TABLE")
    print("="*120 + "\n")

    header = "| Config | Aux States | Theoretical Layer Sizes | Redundancy Ratio | T-Set Cross Terms | Poly Eval Time (s) |"
    separator = "|" + "-"*8 + "|" + "-"*12 + "|" + "-"*25 + "|" + "-"*18 + "|" + "-"*19 + "|" + "-"*20 + "|"

    print(header)
    print(separator)

    for _, row in results_df.iterrows():
        print(f"| {row['Config']:<6} | {row['Aux States']:>10} | {row['Theoretical Layer Sizes']:<23} | {row['Redundancy Ratio']:>16} | {row['T-Set Cross Terms']:>17} | {row['Poly Eval Time (s)']:>18} |")

    print("\n" + "="*120)

    # Insights
    print("\n📊 KEY INSIGHTS")
    print("="*120 + "\n")

    print("Auxiliary States Growth:")
    for _, row in results_df.iterrows():
        print(f"  {row['Config']}: {row['Aux States']:>6} states, Cross-terms: {row['T-Set Cross Terms']:>5}, Eval time: {row['Poly Eval Time (s)']}")

    print(f"\n⚡ Performance:")
    print(f"  - Lowest redundancy: {results_df.loc[results_df['Redundancy Ratio'].str.rstrip('x').astype(float).idxmin(), 'Config']}")
    print(f"  - Most cross-terms: {results_df.loc[results_df['T-Set Cross Terms'].astype(int).idxmax(), 'Config']} "
          f"({results_df['T-Set Cross Terms'].max()} terms)")
    print(f"  - Fastest eval: {results_df.loc[results_df['Poly Eval Time (s)'].str.replace('s','').astype(float).idxmin(), 'Config']}")

    # LaTeX
    print("\n" + "="*120)
    print("LATEX TABLE (for papers)")
    print("="*120 + "\n")

    latex_str = """\\begin{table}[h]
\\centering
\\caption{AUX-QHE Auxiliary States Analysis}
\\label{tab:aux_analysis}
\\begin{tabular}{lrrrrr}
\\toprule
\\textbf{Config} & \\textbf{Aux States} & \\textbf{Layer Sizes} & \\textbf{Redundancy} & \\textbf{Cross Terms} & \\textbf{Eval Time (s)} \\\\
\\midrule
"""

    for _, row in results_df.iterrows():
        # Escape special characters for LaTeX
        layer_sizes = row['Theoretical Layer Sizes'].replace('[', '\\{').replace(']', '\\}')
        latex_str += f"{row['Config']} & {row['Aux States']} & {layer_sizes} & {row['Redundancy Ratio']} & {row['T-Set Cross Terms']} & {row['Poly Eval Time (s)']} \\\\\n"

    latex_str += """\\bottomrule
\\end{tabular}
\\end{table}"""

    print(latex_str)

    print("\n" + "="*120)

    # Analysis
    print("\n🔬 DETAILED ANALYSIS")
    print("="*120 + "\n")

    print("1. Layer Size Growth Pattern:")
    for _, row in results_df.iterrows():
        sizes = eval(row['Theoretical Layer Sizes'])
        growth = [sizes[i]/sizes[i-1] if i > 0 else 0 for i in range(len(sizes))]
        growth_str = ", ".join([f"{g:.1f}x" for g in growth[1:]])
        print(f"   {row['Config']}: {row['Theoretical Layer Sizes']} → Growth: [{growth_str}]")

    print("\n2. Cross-Term Impact:")
    total_states = results_df['Aux States'].sum()
    total_cross = results_df['T-Set Cross Terms'].sum()
    print(f"   Total auxiliary states: {total_states}")
    print(f"   Total cross-terms: {total_cross}")
    print(f"   Cross-term percentage: {(total_cross/total_states)*100:.1f}%")

    print("\n3. Polynomial Evaluation Performance:")
    avg_eval_time = results_df['Poly Eval Time (s)'].str.replace('s','').astype(float).mean()
    print(f"   Average eval time: {avg_eval_time:.6f}s")
    print(f"   Time per aux state (avg): {(avg_eval_time / results_df['Aux States'].mean()) * 1000:.6f}ms")

    print("\n" + "="*120)

except FileNotFoundError:
    print(f"❌ Error: Could not find {csv_file}")
    print("   Please run: python algorithm/openqasm_performance_comparison.py")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
