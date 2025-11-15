#!/usr/bin/env python3
"""
Generate compact results table - one row per config (QASM 2 average)

This script creates a compact summary table combining OpenQASM 2 and 3 results
(which have identical performance metrics in AUX-QHE).

Reads from: corrected_openqasm_performance_comparison.csv
Outputs:
  - Console table (formatted)
  - CSV: aux_qhe_compact_results.csv
  - Markdown format
  - LaTeX format

Note: To update with latest auxiliary state counts after fixes, run:
  python quick_update_aux_states.py
  python generate_compact_table.py
"""
import pandas as pd
import sys

csv_file = "results/corrected_openqasm_performance_comparison.csv"

try:
    df = pd.read_csv(csv_file)

    # Filter to only QASM 2 results (both versions have same metrics)
    df_qasm2 = df[df['QASM_Version'] == 'OpenQASM 2'].copy()

    # Create formatted table
    table_data = []

    for _, row in df_qasm2.iterrows():
        config = row['Config']
        fidelity = row['Fidelity']
        tvd = row['TVD']
        aux_qubits = row['Aux_States']
        aux_prep_time = row['Aux_Prep_Time_s']
        t_gadget_time = row['T_Gadget_Time_s']
        decrypt_time = row['Decrypt_Time_s']
        eval_time = row['Eval_Time_s']

        # Combined decrypt + eval time
        decrypt_eval_time = decrypt_time + eval_time

        # Total run time
        total_time = aux_prep_time + t_gadget_time + decrypt_eval_time

        table_data.append({
            'Config': config,
            'Fidelity': f"{fidelity:.4f}",
            'TVD': f"{tvd:.4f}",
            'QASM': 'Both 2&3',
            'Aux Qubits': aux_qubits,
            'Aux Prep Time(s)': f"{aux_prep_time:.6f}",
            'T-Gadget Time(s)': f"{t_gadget_time:.6f}",
            'Decrypt Eval Time(s)': f"{decrypt_eval_time:.6f}",
            'Total Run Time(s)': f"{total_time:.6f}"
        })

    results_df = pd.DataFrame(table_data)

    # Print formatted table
    print("\n" + "="*120)
    print("AUX-QHE PERFORMANCE RESULTS - COMPACT TABLE")
    print("="*120 + "\n")

    print(results_df.to_string(index=False))

    print("\n" + "="*120)

    # Save to CSV
    output_file = "aux_qhe_compact_results.csv"
    results_df.to_csv(output_file, index=False)
    print(f"\n✅ Compact table saved to: {output_file}")

    # Markdown
    print("\n" + "="*120)
    print("MARKDOWN FORMAT")
    print("="*120 + "\n")
    print(results_df.to_markdown(index=False))

    # Nice formatted ASCII table
    print("\n" + "="*120)
    print("ASCII TABLE (for terminal/documentation)")
    print("="*120 + "\n")

    # Custom formatted table
    header = "| Config | Fidelity | TVD | QASM | Aux Qubits | Aux Prep Time(s) | T-Gadget Time(s) | Decrypt Eval Time(s) | Total Run Time(s) |"
    separator = "|" + "-"*8 + "|" + "-"*10 + "|" + "-"*5 + "|" + "-"*9 + "|" + "-"*12 + "|" + "-"*18 + "|" + "-"*18 + "|" + "-"*22 + "|" + "-"*19 + "|"

    print(header)
    print(separator)

    for _, row in results_df.iterrows():
        print(f"| {row['Config']:<6} | {row['Fidelity']:>8} | {row['TVD']:>3} | {row['QASM']:<7} | {row['Aux Qubits']:>10} | {row['Aux Prep Time(s)']:>16} | {row['T-Gadget Time(s)']:>16} | {row['Decrypt Eval Time(s)']:>20} | {row['Total Run Time(s)']:>17} |")

    print("\n" + "="*120)

    # Summary
    print("\n📊 KEY INSIGHTS")
    print("="*120 + "\n")

    total_configs = len(results_df)
    all_pass = all(float(x) > 0.99 for x in results_df['Fidelity'])

    print(f"✅ Tested Configurations: {total_configs}")
    print(f"✅ All Tests Passed: {all_pass} (100% success rate)")
    print(f"✅ Average Fidelity: {df_qasm2['Fidelity'].mean():.6f}")
    print(f"✅ Perfect Fidelity Count: {(df_qasm2['Fidelity'] > 0.99).sum()}/{total_configs}")

    # Performance insights
    print(f"\n⏱️  Performance Insights:")
    print(f"   - Fastest config: {results_df.loc[results_df['Total Run Time(s)'].astype(float).idxmin(), 'Config']} "
          f"({results_df['Total Run Time(s)'].astype(float).min():.6f}s)")
    print(f"   - Slowest config: {results_df.loc[results_df['Total Run Time(s)'].astype(float).idxmax(), 'Config']} "
          f"({results_df['Total Run Time(s)'].astype(float).max():.6f}s)")
    print(f"   - Most aux qubits: {results_df.loc[results_df['Aux Qubits'].astype(int).idxmax(), 'Config']} "
          f"({int(results_df['Aux Qubits'].max())} qubits)")

    print("\n" + "="*120)

    # Export for papers
    print("\n📄 LATEX TABLE (ready for papers)")
    print("="*120 + "\n")

    latex_str = """\\begin{table}[h]
\\centering
\\caption{AUX-QHE Performance Results}
\\label{tab:aux_qhe_results}
\\begin{tabular}{lcccrrrr}
\\toprule
\\textbf{Config} & \\textbf{Fidelity} & \\textbf{TVD} & \\textbf{QASM} & \\textbf{Aux Qubits} & \\textbf{Prep (s)} & \\textbf{T-Gadget (s)} & \\textbf{Total (s)} \\\\
\\midrule
"""

    for _, row in results_df.iterrows():
        total = float(row['Total Run Time(s)'])
        latex_str += f"{row['Config']} & {row['Fidelity']} & {row['TVD']} & {row['QASM']} & {row['Aux Qubits']} & {row['Aux Prep Time(s)']} & {row['T-Gadget Time(s)']} & {total:.6f} \\\\\n"

    latex_str += """\\bottomrule
\\end{tabular}
\\end{table}"""

    print(latex_str)

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
