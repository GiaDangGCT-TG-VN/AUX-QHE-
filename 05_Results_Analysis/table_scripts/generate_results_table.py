#!/usr/bin/env python3
"""
Generate formatted results table from AUX-QHE benchmark

This script creates a detailed results table with separate rows for OpenQASM 2 and 3
(showing both versions even though they have identical metrics).

Extracts: Config, Fidelity, TVD, QASM, Aux Qubits, Aux Prep Time,
          T-Gadget Time, Decrypt Eval Time, Total Run Time

Reads from: corrected_openqasm_performance_comparison.csv
Outputs:
  - Console table (formatted)
  - CSV: aux_qhe_results_table.csv
  - Markdown format
  - LaTeX format
  - Summary statistics

Note: To update with latest auxiliary state counts after fixes, run:
  python quick_update_aux_states.py
  python generate_results_table.py
"""
import pandas as pd
import sys

# Read the CSV file
csv_file = "results/corrected_openqasm_performance_comparison.csv"

try:
    df = pd.read_csv(csv_file)

    # Create formatted table with requested columns
    table_data = []

    for _, row in df.iterrows():
        config = row['Config']
        qasm_version = row['QASM_Version']
        fidelity = row['Fidelity']
        tvd = row['TVD']
        aux_qubits = row['Aux_States']  # Number of auxiliary qubits/states
        aux_prep_time = row['Aux_Prep_Time_s']
        t_gadget_time = row['T_Gadget_Time_s']
        decrypt_time = row['Decrypt_Time_s']
        eval_time = row['Eval_Time_s']

        # Total run time = Aux Prep + T-Gadget + Decrypt + Eval
        total_time = aux_prep_time + t_gadget_time + decrypt_time + eval_time

        table_data.append({
            'Config': config,
            'Fidelity': f"{fidelity:.4f}",
            'TVD': f"{tvd:.4f}",
            'QASM': qasm_version.replace('OpenQASM ', ''),
            'Aux Qubits': aux_qubits,
            'Aux Prep Time(s)': f"{aux_prep_time:.6f}",
            'T-Gadget Time(s)': f"{t_gadget_time:.6f}",
            'Decrypt Eval Time(s)': f"{decrypt_time + eval_time:.6f}",
            'Total Run Time(s)': f"{total_time:.6f}"
        })

    # Create DataFrame
    results_df = pd.DataFrame(table_data)

    # Print formatted table
    print("\n" + "="*120)
    print("AUX-QHE PERFORMANCE RESULTS TABLE")
    print("="*120 + "\n")

    # Print as formatted table
    print(results_df.to_string(index=False))

    print("\n" + "="*120)

    # Save to CSV
    output_file = "aux_qhe_results_table.csv"
    results_df.to_csv(output_file, index=False)
    print(f"\n✅ Table saved to: {output_file}")

    # Print markdown format
    print("\n" + "="*120)
    print("MARKDOWN FORMAT (for documentation)")
    print("="*120 + "\n")

    print(results_df.to_markdown(index=False))

    print("\n" + "="*120)

    # Print LaTeX format
    print("\nLATEX FORMAT (for papers)")
    print("="*120 + "\n")

    print(results_df.to_latex(index=False))

    print("\n" + "="*120)

    # Summary statistics
    print("\n📊 SUMMARY STATISTICS")
    print("="*120 + "\n")

    # Group by config (combine QASM versions)
    configs = results_df['Config'].unique()

    print(f"Total Configurations: {len(configs)}")
    print(f"Total Tests: {len(results_df)}")
    print(f"\nAverage Fidelity: {df['Fidelity'].mean():.6f}")
    print(f"Average TVD: {df['TVD'].mean():.6f}")
    print(f"Average Aux Qubits: {df['Aux_States'].mean():.0f}")
    print(f"Average Total Time: {df['Total_Aux_Overhead_s'].mean():.6f}s")

    # Fidelity check
    print(f"\n✅ All tests passed: {(df['Fidelity'] > 0.99).all()}")

    print("\n" + "="*120)

except FileNotFoundError:
    print(f"❌ Error: Could not find {csv_file}")
    print("   Please run the benchmark first:")
    print("   $ python algorithm/openqasm_performance_comparison.py")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {str(e)}")
    sys.exit(1)
