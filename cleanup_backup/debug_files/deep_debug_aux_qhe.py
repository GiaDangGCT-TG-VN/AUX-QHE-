"""
Deep Debug Analysis for AUX-QHE Implementation
Systematic investigation of why fidelity is consistently low (~0.25 instead of >0.95)
"""

import numpy as np
from qiskit import QuantumCircuit, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector, state_fidelity
import logging

# Import AUX-QHE modules
from bfv_core import initialize_bfv_params
from key_generation import aux_keygen
from qotp_crypto import qotp_encrypt, qotp_decrypt
from circuit_evaluation import aux_eval

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AUXQHEDeepDebugger:
    """Deep debugging of AUX-QHE fidelity issues."""

    def __init__(self):
        self.simulator = AerSimulator(method='statevector')

    def debug_qotp_encryption_decryption(self):
        """Test QOTP encryption/decryption in isolation."""
        print("🔍 TESTING QOTP ENCRYPTION/DECRYPTION IN ISOLATION")
        print("=" * 60)

        try:
            # Initialize BFV
            params, encoder, encryptor, decryptor, evaluator = initialize_bfv_params()
            poly_degree = params.poly_degree

            # Simple test circuit
            original_circuit = QuantumCircuit(2)
            original_circuit.h(0)
            original_circuit.cx(0, 1)

            print(f"Original circuit: {[instr.operation.name for instr in original_circuit.data]}")

            # Get ideal statevector
            ideal_statevector = Statevector.from_instruction(original_circuit)
            print(f"Ideal state probabilities: {ideal_statevector.probabilities()}")

            # QOTP keys
            a_init = [1, 0]
            b_init = [0, 1]

            # Test QOTP encryption alone
            encrypted_circuit, d, enc_a, enc_b = qotp_encrypt(
                original_circuit, a_init, b_init, 0, 4,
                encryptor, encoder, decryptor, poly_degree
            )

            print(f"Encrypted circuit: {[instr.operation.name for instr in encrypted_circuit.data]}")

            # Test QOTP decryption without homomorphic evaluation
            decrypted_circuit = qotp_decrypt(
                encrypted_circuit, enc_a, enc_b, decryptor, encoder, poly_degree
            )

            print(f"Decrypted circuit: {[instr.operation.name for instr in decrypted_circuit.data]}")

            # Check if QOTP alone preserves fidelity
            decrypted_clean = decrypted_circuit.copy()
            decrypted_clean.remove_final_measurements(inplace=True)

            decrypted_statevector = Statevector.from_instruction(decrypted_clean)
            qotp_fidelity = state_fidelity(ideal_statevector, decrypted_statevector)

            print(f"QOTP-only fidelity: {qotp_fidelity:.6f}")
            print(f"Decrypted state probabilities: {decrypted_statevector.probabilities()}")

            if qotp_fidelity < 0.95:
                print("❌ QOTP encryption/decryption itself is broken!")
                return False
            else:
                print("✅ QOTP encryption/decryption works correctly")
                return True

        except Exception as e:
            print(f"❌ QOTP test failed: {e}")
            import traceback
            traceback.print_exc()
            return False

    def debug_simple_t_gate_case(self):
        """Test the simplest possible T-gate case."""
        print("\n🔍 TESTING SIMPLEST T-GATE CASE")
        print("=" * 60)

        try:
            # Initialize BFV
            params, encoder, encryptor, decryptor, evaluator = initialize_bfv_params()
            poly_degree = params.poly_degree

            # Simplest possible circuit: just one T-gate
            original_circuit = QuantumCircuit(1)
            original_circuit.t(0)

            print(f"Original circuit: {[instr.operation.name for instr in original_circuit.data]}")

            # Get ideal statevector
            ideal_statevector = Statevector.from_instruction(original_circuit)
            print(f"Ideal state probabilities: {ideal_statevector.probabilities()}")

            # Generate AUX-QHE keys
            a_init = [1]
            b_init = [0]

            secret_key, eval_key, aux_prep_time, layer_sizes, total_aux_states = aux_keygen(
                1, 1, a_init, b_init
            )

            print(f"Auxiliary states generated: {total_aux_states}")

            # QOTP encrypt
            encrypted_circuit, d, enc_a, enc_b = qotp_encrypt(
                original_circuit, a_init, b_init, 0, 3,
                encryptor, encoder, decryptor, poly_degree
            )

            # Homomorphic evaluation
            T_sets, V_sets, auxiliary_states = eval_key
            eval_circuit, final_enc_a, final_enc_b = aux_eval(
                encrypted_circuit, enc_a, enc_b, auxiliary_states, 1,
                encryptor, decryptor, encoder, evaluator, poly_degree, debug=True
            )

            # QOTP decrypt
            decrypted_circuit = qotp_decrypt(
                eval_circuit, final_enc_a, final_enc_b, decryptor, encoder, poly_degree
            )

            # Check fidelity
            decrypted_clean = decrypted_circuit.copy()
            decrypted_clean.remove_final_measurements(inplace=True)

            decrypted_statevector = Statevector.from_instruction(decrypted_clean)
            simple_fidelity = state_fidelity(ideal_statevector, decrypted_statevector)

            print(f"Simple T-gate fidelity: {simple_fidelity:.6f}")
            print(f"Decrypted state probabilities: {decrypted_statevector.probabilities()}")

            # Debug key evolution
            print("\n🔑 Key Evolution Debug:")
            initial_a = int(encoder.decode(decryptor.decrypt(enc_a[0]))[0]) % 2
            initial_b = int(encoder.decode(decryptor.decrypt(enc_b[0]))[0]) % 2
            final_a = int(encoder.decode(decryptor.decrypt(final_enc_a[0]))[0]) % 2
            final_b = int(encoder.decode(decryptor.decrypt(final_enc_b[0]))[0]) % 2

            print(f"Initial keys: a=[{initial_a}], b=[{initial_b}]")
            print(f"Final keys: a=[{final_a}], b=[{final_b}]")

            return simple_fidelity > 0.95

        except Exception as e:
            print(f"❌ Simple T-gate test failed: {e}")
            import traceback
            traceback.print_exc()
            return False

    def debug_circuit_construction_step_by_step(self):
        """Debug circuit construction at each step."""
        print("\n🔍 STEP-BY-STEP CIRCUIT CONSTRUCTION DEBUG")
        print("=" * 60)

        try:
            # Initialize
            params, encoder, encryptor, decryptor, evaluator = initialize_bfv_params()
            poly_degree = params.poly_degree

            # Original circuit
            original = QuantumCircuit(2)
            original.h(0)
            original.cx(0, 1)

            print("Step 1: Original Circuit")
            original_sv = Statevector.from_instruction(original)
            print(f"  Statevector: {original_sv.data}")
            print(f"  Probabilities: {original_sv.probabilities()}")

            # After QOTP encryption
            a_init = [1, 0]
            b_init = [0, 1]

            encrypted, d, enc_a, enc_b = qotp_encrypt(
                original, a_init, b_init, 0, 4,
                encryptor, encoder, decryptor, poly_degree
            )

            print("\nStep 2: After QOTP Encryption")
            encrypted_clean = encrypted.copy()
            # Remove any measurement operations
            encrypted_clean.data = [instr for instr in encrypted_clean.data
                                  if instr.operation.name != 'measure']

            try:
                encrypted_sv = Statevector.from_instruction(encrypted_clean)
                print(f"  Statevector: {encrypted_sv.data}")
                print(f"  Probabilities: {encrypted_sv.probabilities()}")

                # Check if encryption preserves structure
                if np.allclose(np.abs(original_sv.data)**2, np.abs(encrypted_sv.data)**2):
                    print("  ✅ Encryption preserves probability structure")
                else:
                    print("  ❌ Encryption changes probability structure")
                    print(f"  Difference: {np.abs(original_sv.data)**2 - np.abs(encrypted_sv.data)**2}")
            except Exception as e:
                print(f"  ⚠️ Cannot compute encrypted statevector: {e}")

            # After decryption (no homomorphic eval)
            decrypted = qotp_decrypt(encrypted, enc_a, enc_b, decryptor, encoder, poly_degree)

            print("\nStep 3: After QOTP Decryption (no homomorphic eval)")
            decrypted_clean = decrypted.copy()
            decrypted_clean.remove_final_measurements(inplace=True)

            decrypted_sv = Statevector.from_instruction(decrypted_clean)
            fidelity_no_eval = state_fidelity(original_sv, decrypted_sv)

            print(f"  Statevector: {decrypted_sv.data}")
            print(f"  Probabilities: {decrypted_sv.probabilities()}")
            print(f"  Fidelity vs original: {fidelity_no_eval:.6f}")

            if fidelity_no_eval < 0.95:
                print("  ❌ QOTP encryption/decryption is the problem!")

                # Debug QOTP key application
                print("\n🔍 QOTP Key Application Debug:")
                print(f"  Original gates: {[op.operation.name for op in original.data]}")
                print(f"  Encrypted gates: {[op.operation.name for op in encrypted.data]}")
                print(f"  Decrypted gates: {[op.operation.name for op in decrypted.data]}")

                return False
            else:
                print("  ✅ QOTP works correctly without homomorphic evaluation")
                return True

        except Exception as e:
            print(f"❌ Step-by-step debug failed: {e}")
            import traceback
            traceback.print_exc()
            return False

    def debug_measurement_vs_statevector(self):
        """Compare measurement-based vs statevector-based fidelity."""
        print("\n🔍 MEASUREMENT vs STATEVECTOR FIDELITY COMPARISON")
        print("=" * 60)

        try:
            # Simple test case
            original = QuantumCircuit(2)
            original.h(0)
            original.cx(0, 1)

            # Get ideal measurement distribution
            original_with_meas = original.copy()
            original_with_meas.measure_all()

            ideal_job = self.simulator.run(transpile(original_with_meas, self.simulator), shots=4096)
            ideal_counts = ideal_job.result().get_counts()
            ideal_probs = {state: count/4096 for state, count in ideal_counts.items()}

            print(f"Ideal measurement distribution: {ideal_probs}")

            # Create a deliberately wrong circuit for comparison
            wrong_circuit = QuantumCircuit(2)
            wrong_circuit.x(0)  # Different circuit
            wrong_circuit.measure_all()

            wrong_job = self.simulator.run(transpile(wrong_circuit, self.simulator), shots=4096)
            wrong_counts = wrong_job.result().get_counts()
            wrong_probs = {state: count/4096 for state, count in wrong_counts.items()}

            # Calculate measurement-based fidelity
            all_states = set(ideal_probs.keys()) | set(wrong_probs.keys())
            meas_fidelity = sum(
                np.sqrt(ideal_probs.get(state, 0) * wrong_probs.get(state, 0))
                for state in all_states
            ) ** 2

            print(f"Wrong circuit measurement distribution: {wrong_probs}")
            print(f"Measurement-based fidelity (should be low): {meas_fidelity:.6f}")

            # Now test if our fidelity calculation method is working
            return meas_fidelity < 0.5  # Should be very low for different circuits

        except Exception as e:
            print(f"❌ Measurement vs statevector test failed: {e}")
            return False

    def run_comprehensive_debug(self):
        """Run all debug tests."""
        print("🚨 COMPREHENSIVE AUX-QHE DEBUG ANALYSIS")
        print("🎯 Target: Find why fidelity is ~0.25 instead of >0.95")
        print("=" * 70)

        # Test 1: QOTP in isolation
        print("\n" + "="*70)
        qotp_works = self.debug_qotp_encryption_decryption()

        # Test 2: Simplest T-gate case
        print("\n" + "="*70)
        t_gate_works = self.debug_simple_t_gate_case()

        # Test 3: Step-by-step circuit construction
        print("\n" + "="*70)
        step_by_step_works = self.debug_circuit_construction_step_by_step()

        # Test 4: Measurement vs statevector
        print("\n" + "="*70)
        measurement_method_works = self.debug_measurement_vs_statevector()

        # Summary
        print("\n" + "="*70)
        print("🏁 DEBUG SUMMARY")
        print("=" * 70)
        print(f"✅ QOTP encryption/decryption works: {qotp_works}")
        print(f"✅ Simple T-gate case works: {t_gate_works}")
        print(f"✅ Step-by-step construction works: {step_by_step_works}")
        print(f"✅ Measurement method works: {measurement_method_works}")

        if not qotp_works:
            print("\n🚨 ROOT CAUSE: QOTP encryption/decryption is broken")
            print("   🔧 Fix: Check QOTP key application in qotp_crypto.py")
        elif not step_by_step_works:
            print("\n🚨 ROOT CAUSE: QOTP key management issue")
            print("   🔧 Fix: Check key polynomial evaluation")
        elif not t_gate_works:
            print("\n🚨 ROOT CAUSE: T-gate auxiliary state handling")
            print("   🔧 Fix: Check aux_eval in circuit_evaluation.py")
        else:
            print("\n🤔 All individual components work - complex interaction issue")

        return {
            'qotp_works': qotp_works,
            't_gate_works': t_gate_works,
            'step_by_step_works': step_by_step_works,
            'measurement_method_works': measurement_method_works
        }

def main():
    """Main debug function."""
    debugger = AUXQHEDeepDebugger()
    results = debugger.run_comprehensive_debug()

    if not any(results.values()):
        print("\n💡 RECOMMENDATION: Start with fixing the most basic component first")
    else:
        print("\n💡 RECOMMENDATION: Focus on the failing component identified above")

if __name__ == "__main__":
    main()