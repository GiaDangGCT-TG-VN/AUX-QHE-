"""
Debug Analysis for AUX-QHE Fidelity Issues
Investigate why fidelity is low (~0.24) instead of expected >0.95
"""

import numpy as np
from qiskit import QuantumCircuit, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector, state_fidelity, partial_trace
import logging

# Import AUX-QHE modules
from bfv_core import initialize_bfv_params
from key_generation import aux_keygen
from qotp_crypto import qotp_encrypt, qotp_decrypt
from circuit_evaluation import aux_eval

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FidelityDebugger:
    """Debug fidelity calculation in AUX-QHE implementation."""

    def __init__(self):
        self.simulator = AerSimulator(method='statevector')

    def run_complete_aux_qhe_with_debug(self, num_qubits=3, max_t_depth=2):
        """Run complete AUX-QHE with detailed fidelity debugging."""

        print("🔍 AUX-QHE Fidelity Debug Analysis")
        print("=" * 60)
        print(f"Testing: {num_qubits} qubits, T-depth {max_t_depth}")
        print("Expected: Fidelity > 0.95 between original and decrypted states")
        print()

        try:
            # Step 1: Initialize BFV
            print("1️⃣ Initializing BFV Parameters...")
            params, encoder, encryptor, decryptor, evaluator = initialize_bfv_params()
            poly_degree = params.poly_degree
            print(f"   ✅ BFV initialized: degree={poly_degree}")

            # Step 2: Generate AUX-QHE keys
            print("\n2️⃣ Generating AUX-QHE Keys...")
            # Ensure a_init and b_init have enough elements for any number of qubits
            base_a = [1, 0, 1, 1, 0, 1, 0, 1]  # Extended pattern
            base_b = [0, 1, 0, 1, 1, 0, 1, 0]  # Extended pattern
            a_init = base_a[:num_qubits]
            b_init = base_b[:num_qubits]

            secret_key, eval_key, aux_prep_time, layer_sizes, total_aux_states = aux_keygen(
                num_qubits, max_t_depth, a_init, b_init
            )
            print(f"   ✅ Keys generated: {total_aux_states} auxiliary states")

            # Step 3: Create original test circuit
            print("\n3️⃣ Creating Original Test Circuit...")
            original_circuit = QuantumCircuit(num_qubits)
            original_circuit.h(0)  # Hadamard
            if num_qubits > 1:
                original_circuit.cx(0, 1)  # CNOT
            original_circuit.t(0)  # T-gate
            if max_t_depth > 1:
                original_circuit.t(1 if num_qubits > 1 else 0)  # Another T-gate

            print(f"   ✅ Original circuit: {len(original_circuit.data)} operations")
            print(f"   Operations: {[instr.operation.name for instr in original_circuit.data]}")

            # Step 4: Get ideal statevector (what we expect after decryption)
            print("\n4️⃣ Computing Ideal Statevector...")
            ideal_statevector = Statevector.from_instruction(original_circuit)
            ideal_probs = ideal_statevector.probabilities()
            print(f"   ✅ Ideal state computed: {len(ideal_probs)} amplitudes")
            print(f"   Top probabilities: {sorted(enumerate(ideal_probs), key=lambda x: x[1], reverse=True)[:3]}")

            # Step 5: QOTP Encryption
            print("\n5️⃣ QOTP Encryption...")
            encrypted_circuit, d, enc_a, enc_b = qotp_encrypt(
                original_circuit, a_init, b_init, 0, num_qubits + 2,
                encryptor, encoder, decryptor, poly_degree
            )

            if encrypted_circuit is None:
                raise Exception("QOTP encryption failed")

            print(f"   ✅ QOTP encryption successful")
            print(f"   Encrypted circuit: {len(encrypted_circuit.data)} operations")

            # Step 6: Homomorphic Evaluation
            print("\n6️⃣ Homomorphic Circuit Evaluation...")
            T_sets, V_sets, auxiliary_states = eval_key

            eval_circuit, final_enc_a, final_enc_b = aux_eval(
                encrypted_circuit, enc_a, enc_b, auxiliary_states, max_t_depth,
                encryptor, decryptor, encoder, evaluator, poly_degree, debug=True
            )

            print(f"   ✅ Homomorphic evaluation completed")
            print(f"   Evaluated circuit: {len(eval_circuit.data)} operations")

            # Step 7: QOTP Decryption
            print("\n7️⃣ QOTP Decryption...")
            decrypted_circuit = qotp_decrypt(
                eval_circuit, final_enc_a, final_enc_b, decryptor, encoder, poly_degree
            )

            print(f"   ✅ QOTP decryption completed")
            print(f"   Decrypted circuit: {len(decrypted_circuit.data)} operations")

            # Step 8: Compute decrypted statevector
            print("\n8️⃣ Computing Decrypted Statevector...")

            # Remove measurements for statevector computation
            decrypted_circuit_no_meas = decrypted_circuit.copy()
            decrypted_circuit_no_meas.remove_final_measurements(inplace=True)

            try:
                decrypted_statevector = Statevector.from_instruction(decrypted_circuit_no_meas)
                decrypted_probs = decrypted_statevector.probabilities()
                print(f"   ✅ Decrypted state computed: {len(decrypted_probs)} amplitudes")
                print(f"   Top probabilities: {sorted(enumerate(decrypted_probs), key=lambda x: x[1], reverse=True)[:3]}")
            except Exception as e:
                print(f"   ❌ Statevector computation failed: {e}")
                print("   🔧 Using measurement-based approach...")
                return self.measurement_based_fidelity_check(
                    original_circuit, decrypted_circuit, num_qubits
                )

            # Step 9: Calculate true fidelity
            print("\n9️⃣ Calculating Fidelity...")

            # Method 1: Direct statevector fidelity
            try:
                direct_fidelity = state_fidelity(ideal_statevector, decrypted_statevector)
                print(f"   📊 Direct Statevector Fidelity: {direct_fidelity:.6f}")
            except Exception as e:
                print(f"   ⚠️  Direct fidelity calculation failed: {e}")
                direct_fidelity = None

            # Method 2: Probability distribution fidelity (Hellinger)
            hellinger_fidelity = np.sum(np.sqrt(ideal_probs * decrypted_probs)) ** 2
            print(f"   📊 Hellinger Fidelity: {hellinger_fidelity:.6f}")

            # Method 3: Total Variation Distance
            tvd = 0.5 * np.sum(np.abs(ideal_probs - decrypted_probs))
            print(f"   📊 Total Variation Distance: {tvd:.6f}")

            # Step 10: Detailed Analysis
            print("\n🔍 DETAILED ANALYSIS")
            print("=" * 40)

            # Compare probability distributions
            print("Probability Distribution Comparison:")
            print("State | Ideal Prob | Decrypted Prob | Difference")
            print("-" * 50)

            for i in range(min(8, len(ideal_probs))):  # Show top 8 states
                diff = abs(ideal_probs[i] - decrypted_probs[i])
                print(f"|{i:03b}⟩ | {ideal_probs[i]:10.6f} | {decrypted_probs[i]:12.6f} | {diff:10.6f}")

            # Key analysis
            print(f"\n🔑 Key Analysis:")
            print(f"   Initial QOTP keys: a={a_init}, b={b_init}")

            # Decrypt final keys
            final_a = []
            final_b = []
            for i in range(num_qubits):
                a_val = int(encoder.decode(decryptor.decrypt(final_enc_a[i]))[0]) % 2
                b_val = int(encoder.decode(decryptor.decrypt(final_enc_b[i]))[0]) % 2
                final_a.append(a_val)
                final_b.append(b_val)

            print(f"   Final QOTP keys:   a={final_a}, b={final_b}")

            # Circuit analysis
            print(f"\n⚙️  Circuit Analysis:")
            original_gates = [instr.operation.name for instr in original_circuit.data]
            decrypted_gates = [instr.operation.name for instr in decrypted_circuit.data
                              if instr.operation.name not in ['x', 'z', 'measure']]

            print(f"   Original gates: {original_gates}")
            print(f"   Decrypted gates: {decrypted_gates}")
            print(f"   Gate preservation: {original_gates == decrypted_gates[:len(original_gates)]}")

            return {
                'direct_fidelity': direct_fidelity,
                'hellinger_fidelity': hellinger_fidelity,
                'tvd': tvd,
                'ideal_probs': ideal_probs,
                'decrypted_probs': decrypted_probs,
                'initial_keys': (a_init, b_init),
                'final_keys': (final_a, final_b),
                'gate_preservation': original_gates == decrypted_gates[:len(original_gates)]
            }

        except Exception as e:
            print(f"❌ Debug analysis failed: {e}")
            import traceback
            traceback.print_exc()
            return None

    def measurement_based_fidelity_check(self, original_circuit, decrypted_circuit, num_qubits):
        """Check fidelity using measurement statistics when statevector fails."""
        print("🔧 Measurement-Based Fidelity Check")
        print("-" * 40)

        shots = 4096

        # Add measurements
        original_with_meas = original_circuit.copy()
        original_with_meas.add_register(ClassicalRegister(num_qubits, 'c'))
        original_with_meas.measure_all()

        decrypted_with_meas = decrypted_circuit.copy()
        if decrypted_with_meas.num_clbits == 0:
            decrypted_with_meas.add_register(ClassicalRegister(num_qubits, 'c'))
            decrypted_with_meas.measure_all()

        # Execute both circuits
        original_job = self.simulator.run(transpile(original_with_meas, self.simulator), shots=shots)
        decrypted_job = self.simulator.run(transpile(decrypted_with_meas, self.simulator), shots=shots)

        original_counts = original_job.result().get_counts()
        decrypted_counts = decrypted_job.result().get_counts()

        # Convert to probabilities
        original_probs = {state: count/shots for state, count in original_counts.items()}
        decrypted_probs = {state: count/shots for state, count in decrypted_counts.items()}

        # Calculate fidelity
        all_states = set(original_probs.keys()) | set(decrypted_probs.keys())

        hellinger_fidelity = sum(
            np.sqrt(original_probs.get(state, 0) * decrypted_probs.get(state, 0))
            for state in all_states
        ) ** 2

        tvd = 0.5 * sum(
            abs(original_probs.get(state, 0) - decrypted_probs.get(state, 0))
            for state in all_states
        )

        print(f"   📊 Measurement-based Hellinger Fidelity: {hellinger_fidelity:.6f}")
        print(f"   📊 Measurement-based TVD: {tvd:.6f}")

        return {
            'measurement_fidelity': hellinger_fidelity,
            'measurement_tvd': tvd,
            'original_counts': original_counts,
            'decrypted_counts': decrypted_counts
        }

    def diagnose_low_fidelity_causes(self):
        """Diagnose potential causes of low fidelity."""
        print("\n🚨 POTENTIAL CAUSES OF LOW FIDELITY")
        print("=" * 50)

        print("1. ❌ QOTP Key Update Errors:")
        print("   - Incorrect polynomial evaluation")
        print("   - BFV encryption/decryption errors")
        print("   - Key synchronization issues")

        print("\n2. ❌ T-Gate Auxiliary State Errors:")
        print("   - Wrong auxiliary state selection")
        print("   - Incorrect cross-term evaluation")
        print("   - Phase correction mistakes")

        print("\n3. ❌ Circuit Construction Errors:")
        print("   - Extra gates added during encryption/decryption")
        print("   - Wrong gate order or placement")
        print("   - Measurement interference")

        print("\n4. ❌ Statevector Calculation Issues:")
        print("   - Wrong circuit used for ideal state")
        print("   - Measurement artifacts")
        print("   - Normalization problems")

def main():
    """Main function to run fidelity debugging."""
    debugger = FidelityDebugger()

    # Test different configurations
    configs = [
        (3, 2, "3q-2t"),
        (3, 3, "3q-3t"),
        (4, 2, "4q-2t")
    ]

    all_results = {}

    for num_qubits, max_t_depth, config_name in configs:
        print(f"\n{'='*70}")
        print(f"TESTING CONFIGURATION: {config_name}")
        print(f"{'='*70}")

        result = debugger.run_complete_aux_qhe_with_debug(num_qubits, max_t_depth)
        all_results[config_name] = result

        if result and result.get('hellinger_fidelity', 0) < 0.8:
            print(f"\n⚠️  LOW FIDELITY DETECTED: {result['hellinger_fidelity']:.4f}")
            debugger.diagnose_low_fidelity_causes()

    # Summary
    print(f"\n{'='*70}")
    print("SUMMARY OF FIDELITY RESULTS")
    print(f"{'='*70}")

    for config_name, result in all_results.items():
        if result:
            fidelity = result.get('hellinger_fidelity', 0)
            tvd = result.get('tvd', 0)
            status = "✅ GOOD" if fidelity > 0.8 else "❌ LOW"
            print(f"{config_name}: Fidelity = {fidelity:.4f}, TVD = {tvd:.4f} {status}")
        else:
            print(f"{config_name}: ❌ FAILED")

if __name__ == "__main__":
    main()