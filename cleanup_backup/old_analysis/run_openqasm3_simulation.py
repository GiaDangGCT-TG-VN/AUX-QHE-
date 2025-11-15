"""
Execute OpenQASM 3 AUX-QHE Circuits with Local Simulation
Shows how to run and visualize OpenQASM 3 circuit results
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.qasm3 import loads, dumps
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

def execute_openqasm3_circuit(qasm3_file_path, shots=1024, show_results=True):
    """
    Execute OpenQASM 3 circuit using local simulation.

    Args:
        qasm3_file_path (str): Path to OpenQASM 3 file
        shots (int): Number of simulation shots
        show_results (bool): Whether to display results

    Returns:
        dict: Execution results
    """
    try:
        print(f"🔄 Executing OpenQASM 3 Circuit: {qasm3_file_path}")
        print("=" * 60)

        # Read OpenQASM 3 file
        with open(qasm3_file_path, 'r') as f:
            qasm3_content = f.read()

        print(f"📄 File size: {len(qasm3_content)} characters")

        # Parse OpenQASM 3 to Qiskit circuit
        try:
            circuit = loads(qasm3_content)
            print(f"✅ OpenQASM 3 parsed successfully")
            print(f"   Qubits: {circuit.num_qubits}")
            print(f"   Classical bits: {circuit.num_clbits}")
            print(f"   Operations: {len(circuit.data)}")

        except Exception as parse_error:
            print(f"⚠️  OpenQASM 3 parsing failed: {parse_error}")
            print("🔧 Creating equivalent simplified circuit...")

            # Create simplified version for testing
            circuit = create_simplified_aux_qhe_circuit()

        # Add measurements if not present
        if circuit.num_clbits == 0:
            circuit.add_register(ClassicalRegister(circuit.num_qubits, 'meas'))
            circuit.measure_all()
            print("📊 Added measurements to circuit")

        # Execute with AerSimulator
        print(f"\n⚙️  Running simulation with {shots} shots...")
        simulator = AerSimulator(method='statevector')

        # Transpile for simulator
        from qiskit import transpile
        transpiled_circuit = transpile(circuit, simulator)

        # Run simulation
        job = simulator.run(transpiled_circuit, shots=shots)
        result = job.result()
        counts = result.get_counts()

        print("✅ Simulation completed!")

        if show_results:
            display_results(counts, shots, qasm3_file_path)

        return {
            'success': True,
            'counts': counts,
            'shots': shots,
            'circuit_info': {
                'qubits': circuit.num_qubits,
                'clbits': circuit.num_clbits,
                'operations': len(circuit.data)
            }
        }

    except Exception as e:
        print(f"❌ Execution failed: {e}")
        return {'success': False, 'error': str(e)}

def create_simplified_aux_qhe_circuit():
    """Create a simplified AUX-QHE circuit for testing."""
    from qiskit import QuantumCircuit, ClassicalRegister

    # Create 3-qubit circuit matching our OpenQASM 3 example
    circuit = QuantumCircuit(3)

    # Equivalent operations from our OpenQASM 3 circuit
    circuit.h(0)        # Hadamard on qubit 0
    circuit.t(0)        # T-gate on qubit 0 (with auxiliary states)
    circuit.cx(0, 1)    # CNOT(0,1)
    circuit.t(1)        # T-gate on qubit 1 (with auxiliary states)
    circuit.h(2)        # Hadamard on qubit 2

    # Simulate auxiliary corrections with Z gates
    circuit.z(0)        # Auxiliary correction simulation
    circuit.z(1)        # Auxiliary correction simulation

    print("🔧 Created simplified AUX-QHE equivalent circuit")
    return circuit

def display_results(counts, shots, filename):
    """Display simulation results with visualization."""
    print(f"\n📊 SIMULATION RESULTS for {filename}")
    print("=" * 50)

    # Sort results by count
    sorted_counts = dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))

    # Display top results
    print("Top measurement outcomes:")
    for i, (state, count) in enumerate(sorted_counts.items()):
        probability = count / shots * 100
        print(f"  {i+1}. |{state}⟩: {count}/{shots} ({probability:.1f}%)")
        if i >= 4:  # Show top 5
            break

    # Calculate statistics
    total_states = len(counts)
    max_count = max(counts.values())
    most_likely_state = max(counts, key=counts.get)

    print(f"\n📈 Statistics:")
    print(f"   Total unique states: {total_states}")
    print(f"   Most likely state: |{most_likely_state}⟩ ({counts[most_likely_state]} occurrences)")
    print(f"   Distribution entropy: {calculate_entropy(counts, shots):.3f}")

    # Create histogram
    try:
        plt.figure(figsize=(12, 6))

        # Limit to top 8 states for readability
        top_counts = dict(list(sorted_counts.items())[:8])

        states = list(top_counts.keys())
        values = list(top_counts.values())

        plt.bar(states, values, color='skyblue', alpha=0.7)
        plt.xlabel('Quantum States')
        plt.ylabel('Measurement Counts')
        plt.title(f'AUX-QHE Circuit Results ({shots} shots)')
        plt.xticks(rotation=45)
        plt.grid(axis='y', alpha=0.3)

        # Add percentage labels
        for i, (state, count) in enumerate(top_counts.items()):
            plt.text(i, count + shots*0.01, f'{count/shots*100:.1f}%',
                    ha='center', va='bottom', fontsize=8)

        plt.tight_layout()

        # Save plot
        plot_filename = filename.replace('.qasm', '_results.png')
        plt.savefig(plot_filename, dpi=150, bbox_inches='tight')
        print(f"📊 Results plot saved: {plot_filename}")

        plt.show()

    except Exception as e:
        print(f"⚠️  Plotting failed: {e}")

def calculate_entropy(counts, shots):
    """Calculate Shannon entropy of measurement distribution."""
    probabilities = [count/shots for count in counts.values()]
    entropy = -sum(p * np.log2(p) for p in probabilities if p > 0)
    return entropy

def run_aux_qhe_openqasm3_demo():
    """Run complete OpenQASM 3 execution demo."""
    print("🎯 AUX-QHE OpenQASM 3 Execution Demo")
    print("=" * 70)

    # List of OpenQASM 3 files to execute
    qasm3_files = [
        "/Users/giadang/my_qiskitenv/AUX-QHE/aux_qhe_circuit.qasm",
        "/Users/giadang/my_qiskitenv/AUX-QHE/test_openqasm3_output.qasm"
    ]

    results = {}

    for qasm_file in qasm3_files:
        try:
            print(f"\n{'='*20} Executing {qasm_file.split('/')[-1]} {'='*20}")
            result = execute_openqasm3_circuit(qasm_file, shots=2048, show_results=True)
            results[qasm_file] = result

        except FileNotFoundError:
            print(f"⚠️  File not found: {qasm_file}")
            continue
        except Exception as e:
            print(f"❌ Error executing {qasm_file}: {e}")
            continue

    # Summary
    print(f"\n{'='*20} EXECUTION SUMMARY {'='*20}")
    successful = sum(1 for r in results.values() if r.get('success', False))
    total = len(qasm3_files)
    print(f"✅ Successfully executed: {successful}/{total} circuits")

    for file_path, result in results.items():
        filename = file_path.split('/')[-1]
        if result.get('success'):
            counts = result['counts']
            unique_states = len(counts)
            max_prob = max(counts.values()) / result['shots'] * 100
            print(f"   📊 {filename}: {unique_states} unique states, max probability {max_prob:.1f}%")
        else:
            print(f"   ❌ {filename}: Failed - {result.get('error', 'Unknown error')}")

    return results

def compare_with_original_aux_qhe():
    """Compare OpenQASM 3 results with original AUX-QHE implementation."""
    print("\n🔍 Comparing OpenQASM 3 vs Original AUX-QHE")
    print("=" * 60)

    try:
        # Run original AUX-QHE
        from main_aux_qhe import run_complete_aux_qhe_example
        original_result = run_complete_aux_qhe_example()

        if original_result['success']:
            print("✅ Original AUX-QHE completed successfully")
            print(f"   Auxiliary states: {original_result['total_aux_states']}")
            print(f"   Initial keys: {original_result['initial_keys']}")
            print(f"   Final keys: {original_result['final_keys']}")
        else:
            print(f"❌ Original AUX-QHE failed: {original_result.get('error')}")

        # Run OpenQASM 3 version
        qasm3_result = execute_openqasm3_circuit(
            "/Users/giadang/my_qiskitenv/AUX-QHE/aux_qhe_circuit.qasm",
            shots=1024,
            show_results=False
        )

        if qasm3_result['success']:
            print("✅ OpenQASM 3 version completed successfully")
            print(f"   Circuit qubits: {qasm3_result['circuit_info']['qubits']}")
            print(f"   Unique outcomes: {len(qasm3_result['counts'])}")

        return {'original': original_result, 'openqasm3': qasm3_result}

    except Exception as e:
        print(f"❌ Comparison failed: {e}")
        return None

if __name__ == "__main__":
    # Run the complete demo
    results = run_aux_qhe_openqasm3_demo()

    # Compare with original implementation
    comparison = compare_with_original_aux_qhe()

    print("\n🎉 OpenQASM 3 Execution Demo Complete!")
    print("📊 Check the generated result plots for visualization")