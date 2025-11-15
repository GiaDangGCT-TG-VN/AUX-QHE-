"""
Simple OpenQASM 3 Executor for AUX-QHE Circuits
Execute and visualize OpenQASM 3 circuits with results
"""

import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit import transpile
import re

def create_aux_qhe_equivalent_circuit():
    """
    Create equivalent circuit based on our OpenQASM 3 AUX-QHE design.
    This simulates the same operations as the OpenQASM 3 version.
    """
    print("🔧 Creating AUX-QHE Equivalent Circuit")
    print("=" * 50)

    # Create 3-qubit circuit (matching our OpenQASM 3 example)
    circuit = QuantumCircuit(3, 3)  # 3 qubits, 3 classical bits

    print("⚙️  Applying AUX-QHE Operations:")

    # Step 1: Hadamard on qubit 0 (initialization)
    circuit.h(0)
    print("   1. H(0) - Hadamard initialization")

    # Step 2: T-gate on qubit 0 with auxiliary correction
    circuit.t(0)
    print("   2. T(0) - T-gate with auxiliary states")

    # Simulate auxiliary correction based on cross-terms
    # (In real OpenQASM 3, this would be conditional)
    circuit.z(0)  # Auxiliary correction simulation
    print("   3. Z(0) - Auxiliary correction")

    # Step 3: CNOT(0,1)
    circuit.cx(0, 1)
    print("   4. CNOT(0,1) - Entanglement")

    # Step 4: T-gate on qubit 1 with auxiliary correction
    circuit.t(1)
    print("   5. T(1) - T-gate with auxiliary states")

    # Simulate auxiliary correction
    circuit.z(1)  # Auxiliary correction simulation
    print("   6. Z(1) - Auxiliary correction")

    # Step 5: Hadamard on qubit 2
    circuit.h(2)
    print("   7. H(2) - Final Hadamard")

    # Add QOTP decryption simulation (XOR with final keys)
    # Based on our analysis: final keys a=[0,0,1], b=[0,1,0]
    # Apply X gates where keys are 1
    circuit.x(1)  # b[1] = 1
    circuit.x(2)  # a[2] = 1
    print("   8. QOTP Decryption - X(1), X(2)")

    # Add measurements
    circuit.measure_all()
    print("   9. Measure all qubits")

    print(f"\n✅ Circuit created: {circuit.num_qubits} qubits, {len(circuit.data)} operations")
    return circuit

def execute_and_visualize(circuit, shots=2048):
    """Execute circuit and visualize results."""
    print(f"\n⚙️  Executing Circuit with {shots} shots")
    print("=" * 50)

    # Use AerSimulator
    simulator = AerSimulator(method='statevector')

    # Transpile for simulator
    transpiled_circuit = transpile(circuit, simulator)

    # Execute
    job = simulator.run(transpiled_circuit, shots=shots)
    result = job.result()
    counts = result.get_counts()

    print("✅ Execution completed!")
    print(f"📊 Unique measurement outcomes: {len(counts)}")

    # Display results
    display_results(counts, shots)

    return counts

def display_results(counts, shots):
    """Display and visualize measurement results."""
    print("\n📊 MEASUREMENT RESULTS")
    print("=" * 40)

    # Sort by count (most frequent first)
    sorted_counts = dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))

    # Show top results
    print("Most frequent outcomes:")
    for i, (state, count) in enumerate(sorted_counts.items()):
        probability = count / shots * 100
        bar = "█" * int(probability / 2)  # Visual bar
        print(f"  |{state}⟩: {count:4d}/{shots} ({probability:5.1f}%) {bar}")
        if i >= 7:  # Show top 8
            break

    # Calculate statistics
    entropy = calculate_entropy(counts, shots)
    uniformity = len(counts) / 8  # How close to uniform (max 8 states for 3 qubits)

    print(f"\n📈 Statistics:")
    print(f"   Total states measured: {len(counts)}")
    print(f"   Shannon entropy: {entropy:.3f} bits")
    print(f"   Distribution uniformity: {uniformity:.3f}")
    print(f"   Most probable state: |{max(counts, key=counts.get)}⟩")

    # Create visualization
    create_results_plot(sorted_counts, shots)

def calculate_entropy(counts, shots):
    """Calculate Shannon entropy of the distribution."""
    probabilities = [count/shots for count in counts.values()]
    entropy = -sum(p * np.log2(p) for p in probabilities if p > 0)
    return entropy

def create_results_plot(counts, shots):
    """Create and save results visualization."""
    try:
        plt.figure(figsize=(12, 8))

        # Prepare data (top 8 states)
        top_counts = dict(list(counts.items())[:8])
        states = list(top_counts.keys())
        values = list(top_counts.values())
        probabilities = [v/shots for v in values]

        # Create subplot layout
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

        # Bar chart
        bars = ax1.bar(range(len(states)), values, color='skyblue', alpha=0.7, edgecolor='navy')
        ax1.set_xlabel('Quantum States')
        ax1.set_ylabel('Measurement Counts')
        ax1.set_title(f'AUX-QHE Circuit Results ({shots} shots)')
        ax1.set_xticks(range(len(states)))
        ax1.set_xticklabels([f'|{s}⟩' for s in states], rotation=45)
        ax1.grid(axis='y', alpha=0.3)

        # Add percentage labels on bars
        for i, (bar, prob) in enumerate(zip(bars, probabilities)):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + shots*0.01,
                    f'{prob*100:.1f}%', ha='center', va='bottom', fontsize=9)

        # Pie chart for top 4 states
        top_4_counts = dict(list(counts.items())[:4])
        others_count = sum(counts.values()) - sum(top_4_counts.values())

        pie_labels = [f'|{s}⟩' for s in top_4_counts.keys()]
        pie_values = list(top_4_counts.values())

        if others_count > 0:
            pie_labels.append('Others')
            pie_values.append(others_count)

        colors = plt.cm.Set3(np.linspace(0, 1, len(pie_values)))
        wedges, texts, autotexts = ax2.pie(pie_values, labels=pie_labels, autopct='%1.1f%%',
                                          colors=colors, startangle=90)
        ax2.set_title('Distribution of Top States')

        plt.tight_layout()

        # Save plot
        plot_filename = "/Users/giadang/my_qiskitenv/AUX-QHE/aux_qhe_results.png"
        plt.savefig(plot_filename, dpi=150, bbox_inches='tight')
        print(f"📊 Results plot saved: {plot_filename}")

        plt.show()

    except Exception as e:
        print(f"⚠️  Plotting failed: {e}")

def analyze_aux_qhe_behavior(counts):
    """Analyze the behavior specific to AUX-QHE."""
    print("\n🔍 AUX-QHE BEHAVIOR ANALYSIS")
    print("=" * 50)

    total_measurements = sum(counts.values())

    # Analyze qubit correlations
    qubit_marginals = {0: {0: 0, 1: 0}, 1: {0: 0, 1: 0}, 2: {0: 0, 1: 0}}

    for state, count in counts.items():
        # Extract just the 3-bit quantum state (ignore classical register part)
        quantum_state = state.split()[0] if ' ' in state else state
        for i, bit in enumerate(quantum_state[:3]):  # Only take first 3 bits
            qubit_marginals[i][int(bit)] += count

    print("📊 Individual Qubit Statistics:")
    for qubit in range(3):
        prob_0 = qubit_marginals[qubit][0] / total_measurements
        prob_1 = qubit_marginals[qubit][1] / total_measurements
        bias = abs(prob_0 - 0.5)
        print(f"   Qubit {qubit}: |0⟩={prob_0:.3f}, |1⟩={prob_1:.3f}, bias={bias:.3f}")

    # Analyze entanglement indicators
    print("\n🔗 Entanglement Analysis:")

    # Check for Bell-state-like correlations
    correlated_states = 0
    for state, count in counts.items():
        # Extract quantum state part
        quantum_state = state.split()[0] if ' ' in state else state
        # Check for patterns like 00x, 11x (CNOT correlation between qubits 0 and 1)
        if len(quantum_state) >= 2 and quantum_state[0] == quantum_state[1]:
            correlated_states += count

    correlation_strength = correlated_states / total_measurements
    print(f"   CNOT correlation (q0-q1): {correlation_strength:.3f}")

    # Analyze auxiliary correction effects
    print("\n🛠️  Auxiliary Correction Effects:")
    z_corrected_outcomes = 0
    for state, count in counts.items():
        # Extract quantum state part
        quantum_state = state.split()[0] if ' ' in state else state
        # States that show Z-gate effects (phase flips)
        if quantum_state[:3].count('1') % 2 == 1:  # Odd parity suggests phase effects
            z_corrected_outcomes += count

    correction_ratio = z_corrected_outcomes / total_measurements
    print(f"   Z-correction signature: {correction_ratio:.3f}")

    return {
        'qubit_biases': [abs(qubit_marginals[i][0]/total_measurements - 0.5) for i in range(3)],
        'correlation_strength': correlation_strength,
        'correction_ratio': correction_ratio
    }

def run_complete_openqasm3_demo():
    """Run complete OpenQASM 3 demonstration."""
    print("🎯 AUX-QHE OpenQASM 3 Execution Demo")
    print("=" * 70)
    print("Simulating OpenQASM 3 enhanced AUX-QHE circuit with local execution")
    print()

    # Create and execute circuit
    circuit = create_aux_qhe_equivalent_circuit()

    # Execute with different shot counts
    shot_counts = [1024, 2048, 4096]

    all_results = {}

    for shots in shot_counts:
        print(f"\n{'='*20} Execution with {shots} shots {'='*20}")
        counts = execute_and_visualize(circuit, shots)
        analysis = analyze_aux_qhe_behavior(counts)
        all_results[shots] = {'counts': counts, 'analysis': analysis}

    # Compare results across different shot counts
    print(f"\n{'='*20} COMPARISON ACROSS SHOT COUNTS {'='*20}")
    print("Shot Count | Unique States | Entropy | Correlation | Correction")
    print("-" * 65)

    for shots, data in all_results.items():
        counts = data['counts']
        analysis = data['analysis']
        entropy = calculate_entropy(counts, shots)
        print(f"{shots:>9} | {len(counts):>12} | {entropy:>7.3f} | {analysis['correlation_strength']:>10.3f} | {analysis['correction_ratio']:>9.3f}")

    print("\n🎉 OpenQASM 3 Execution Demo Complete!")
    print("✅ Successfully demonstrated AUX-QHE circuit execution")
    print("📊 Check aux_qhe_results.png for detailed visualization")

    return all_results

if __name__ == "__main__":
    run_complete_openqasm3_demo()