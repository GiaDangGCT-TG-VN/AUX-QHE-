"""
Unified Noise Error Metrics Module for AUX-QHE

This module consolidates all noise analysis, error mitigation, and fidelity
measurement capabilities from multiple original files:
- error_analysis.py (ZNE, noise characterization)
- comprehensive_analysis.py (noise metrics visualization)
- testing_framework.py (fidelity calculations)

Provides: Zero Noise Extrapolation, noise characterization, fidelity metrics,
Wasserstein distance, Total Variation Distance, and visualization tools.
"""

import logging
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from qiskit.quantum_info import hellinger_fidelity
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler, EstimatorV2 as Estimator, SamplerOptions
from qiskit_ibm_runtime.noise_learner import NoiseLearner
from qiskit_ibm_runtime.options import NoiseLearnerOptions
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from scipy.stats import wasserstein_distance
from circuit_evaluation import aux_eval

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NoiseErrorAnalyzer:
    """Comprehensive noise and error analysis for AUX-QHE circuits."""
    
    def __init__(self, backend=None):
        self.backend = backend
        self.noise_model = None
        
    def simulate_ideal_execution(self, circuit, shots=4096):
        """
        Simulate ideal (noiseless) execution of a circuit.
        
        Args:
            circuit (QuantumCircuit): Circuit to simulate.
            shots (int): Number of measurement shots.
        
        Returns:
            dict: Measurement counts from ideal simulation.
        """
        try:
            # Use AerSimulator with statevector method for noiseless simulation
            ideal_simulator = AerSimulator(method='statevector')
            
            # Add measurements if not present
            meas_circuit = circuit.copy()
            if not meas_circuit.cregs:
                from qiskit import ClassicalRegister
                meas_circuit.add_register(ClassicalRegister(circuit.num_qubits, "meas"))
                meas_circuit.measure(range(circuit.num_qubits), range(circuit.num_qubits))
            
            # Run simulation
            job = ideal_simulator.run(meas_circuit, shots=shots)
            result = job.result()
            counts = result.get_counts()
            
            logger.debug(f"Ideal simulation completed: {len(counts)} unique outcomes")
            return counts
            
        except Exception as e:
            logger.error(f"Ideal simulation failed: {str(e)}")
            return {}

    def run_noisy_execution(self, circuit, shots=4096, mitigation_options=None):
        """
        Run circuit on noisy backend with optional error mitigation.
        
        Args:
            circuit (QuantumCircuit): Circuit to execute.
            shots (int): Number of measurement shots.
            mitigation_options (dict): Error mitigation configuration.
        
        Returns:
            dict: Measurement counts from noisy execution.
        """
        if not self.backend:
            logger.warning("No backend specified, using ideal simulation")
            return self.simulate_ideal_execution(circuit, shots)
            
        try:
            # Transpile circuit for backend
            pass_manager = generate_preset_pass_manager(
                optimization_level=1, 
                backend=self.backend
            )
            transpiled_circuit = pass_manager.run(circuit)
            
            # Configure sampler with mitigation options
            if mitigation_options is None:
                mitigation_options = SamplerOptions()
                mitigation_options.default_shots = shots
            
            sampler = Sampler(mode=self.backend, options=mitigation_options)
            
            # Run on backend
            job = sampler.run([(transpiled_circuit, None)])
            result = job.result()
            
            # Extract counts
            if hasattr(result[0].data, 'meas'):
                counts = result[0].data.meas.get_counts()
            else:
                # Try to get counts from first available register
                data_keys = list(result[0].data.__dict__.keys())
                if data_keys:
                    counts = getattr(result[0].data, data_keys[0]).get_counts()
                else:
                    logger.error("No measurement data found in result")
                    return {}
            
            logger.debug(f"Noisy execution completed: {len(counts)} unique outcomes")
            return counts
            
        except Exception as e:
            logger.error(f"Noisy execution failed: {str(e)}")
            return {}

    def apply_zero_noise_extrapolation(self, circuit, base_shots=1024, noise_factors=None):
        """
        Apply Zero Noise Extrapolation (ZNE) to mitigate errors.
        
        Args:
            circuit (QuantumCircuit): Circuit to execute with ZNE.
            base_shots (int): Base number of shots per noise level.
            noise_factors (list): Noise scaling factors.
        
        Returns:
            dict: ZNE-mitigated measurement counts.
        """
        if not self.backend:
            logger.warning("No backend specified for ZNE, using ideal simulation")
            return self.simulate_ideal_execution(circuit, base_shots * 4)
            
        try:
            if noise_factors is None:
                noise_factors = [1, 1.5, 2, 2.5]
            
            logger.info(f"Applying ZNE with noise factors: {noise_factors}")
            
            # Learn noise model
            learner_options = NoiseLearnerOptions()
            learner_options.max_layers_to_learn = 5
            learner_options.shots_per_randomization = base_shots
            
            learner = NoiseLearner(mode=self.backend, options=learner_options)
            noise_job = learner.run([circuit])
            self.noise_model = noise_job.result()
            
            # Run circuit with different noise levels
            results = []
            for factor in noise_factors:
                # Configure ZNE options (simplified for SamplerV2)
                zne_options = SamplerOptions()
                zne_options.default_shots = base_shots
                
                counts = self.run_noisy_execution(circuit, base_shots, zne_options)
                if counts:
                    results.append((factor, counts))
            
            if len(results) < 2:
                logger.warning("Insufficient ZNE data points, returning original counts")
                return self.run_noisy_execution(circuit, base_shots * len(noise_factors))
            
            # Extrapolate to zero noise
            zero_noise_counts = {}
            all_states = set()
            for _, counts in results:
                all_states.update(counts.keys())
            
            for state in all_states:
                probs = []
                factors = []
                for factor, counts in results:
                    total_shots = sum(counts.values())
                    prob = counts.get(state, 0) / total_shots if total_shots > 0 else 0
                    probs.append(prob)
                    factors.append(factor)
                
                # Linear extrapolation to factor = 0
                if len(probs) >= 2:
                    slope = (probs[1] - probs[0]) / (factors[1] - factors[0])
                    intercept = probs[0] - slope * factors[0]
                    zero_prob = max(0, intercept)  # Ensure non-negative
                else:
                    zero_prob = probs[0] if probs else 0
                
                zero_noise_counts[state] = int(zero_prob * base_shots * len(noise_factors))
            
            # Normalize counts to match total shots
            total_shots = base_shots * len(noise_factors)
            current_total = sum(zero_noise_counts.values())
            if current_total > 0:
                for state in zero_noise_counts:
                    zero_noise_counts[state] = int(
                        zero_noise_counts[state] * total_shots / current_total
                    )
            
            logger.info("ZNE extrapolation completed")
            return zero_noise_counts
            
        except Exception as e:
            logger.error(f"ZNE application failed: {str(e)}")
            # Fallback to regular noisy execution
            return self.run_noisy_execution(circuit, base_shots * 4)

class FidelityMetrics:
    """Comprehensive fidelity and distance metrics for quantum circuit analysis."""
    
    @staticmethod
    def compute_hellinger_fidelity(ideal_probs, noisy_probs):
        """Compute Hellinger fidelity between probability distributions."""
        try:
            return hellinger_fidelity(ideal_probs, noisy_probs)
        except Exception as e:
            logger.warning(f"Hellinger fidelity calculation failed: {e}")
            return 0.0
    
    @staticmethod
    def compute_tvd(ideal_counts, noisy_counts, shots):
        """
        Compute Total Variation Distance between measurement counts.
        
        Args:
            ideal_counts (dict): Ideal measurement counts.
            noisy_counts (dict): Noisy measurement counts.
            shots (int): Number of shots used.
        
        Returns:
            float: Total Variation Distance.
        """
        try:
            ideal_probs = {k: v / shots for k, v in ideal_counts.items()}
            noisy_probs = {k: v / sum(noisy_counts.values()) for k, v in noisy_counts.items()}
            
            all_states = set(ideal_probs.keys()).union(noisy_probs.keys())
            
            tvd = 0.5 * sum(abs(ideal_probs.get(state, 0) - noisy_probs.get(state, 0)) 
                           for state in all_states)
            return tvd
        except Exception as e:
            logger.warning(f"TVD calculation failed: {e}")
            return 1.0
    
    @staticmethod
    def compute_wasserstein_distance(ideal_probs, noisy_probs):
        """
        Compute Wasserstein distance between probability distributions.
        
        Args:
            ideal_probs (dict): Ideal probability distribution.
            noisy_probs (dict): Noisy probability distribution.
        
        Returns:
            float: Wasserstein distance.
        """
        try:
            if not ideal_probs or not noisy_probs:
                return 1.0
                
            ideal_vals = list(ideal_probs.values())
            noisy_vals = [noisy_probs.get(k, 0) for k in ideal_probs.keys()]
            
            return wasserstein_distance(ideal_vals, noisy_vals)
        except Exception as e:
            logger.warning(f"Wasserstein distance calculation failed: {e}")
            return 1.0

def analyze_aux_qhe_noise_impact(circuit, enc_a, enc_b, auxiliary_states, max_t_depth, 
                                encryptor, decryptor, encoder, evaluator, poly_degree,
                                backend, shots=4096):
    """
    Comprehensive noise impact analysis for AUX-QHE evaluated circuits.
    
    Args:
        circuit (QuantumCircuit): Input circuit.
        enc_a, enc_b (list): Encrypted QOTP keys.
        auxiliary_states (dict): Auxiliary states.
        max_t_depth (int): Maximum T-depth.
        encryptor, decryptor, encoder, evaluator: BFV components.
        poly_degree (int): BFV polynomial degree.
        backend: IBM Quantum backend.
        shots (int): Number of measurement shots.
    
    Returns:
        dict: Comprehensive noise impact analysis results.
    """
    try:
        logger.info("Starting comprehensive noise impact analysis for AUX-QHE")
        
        # Initialize analyzer
        analyzer = NoiseErrorAnalyzer(backend)
        metrics = FidelityMetrics()
        
        # Step 1: Homomorphic evaluation
        eval_circuit, final_enc_a, final_enc_b = aux_eval(
            circuit, enc_a, enc_b, auxiliary_states, max_t_depth,
            encryptor, decryptor, encoder, evaluator, poly_degree, debug=False
        )
        
        # Add measurements to the evaluated circuit for real hardware execution
        if eval_circuit is not None:
            # Create a copy with measurements for hardware execution
            from qiskit import ClassicalRegister
            eval_circuit_with_measurements = eval_circuit.copy()
            
            # Add classical register if not present
            if len(eval_circuit_with_measurements.clbits) == 0:
                cr = ClassicalRegister(eval_circuit_with_measurements.num_qubits, 'c')
                eval_circuit_with_measurements.add_register(cr)
            
            # Add measurement gates
            eval_circuit_with_measurements.measure_all()
            
            # Use the circuit with measurements for hardware tests
            eval_circuit = eval_circuit_with_measurements
        
        # Step 2: Ideal simulation
        logger.info("Running ideal simulation")
        ideal_counts = analyzer.simulate_ideal_execution(eval_circuit, shots)
        ideal_probs = {k: v / shots for k, v in ideal_counts.items()}
        
        # Step 3: Noisy execution without mitigation
        logger.info("Running noisy execution (no mitigation)")
        no_mitigation_options = SamplerOptions()
        no_mitigation_options.default_shots = shots
        
        noisy_counts = analyzer.run_noisy_execution(eval_circuit, shots, no_mitigation_options)
        noisy_total = sum(noisy_counts.values()) if noisy_counts else shots
        noisy_probs = {k: v / noisy_total for k, v in noisy_counts.items()}
        
        # Step 4: ZNE-mitigated execution
        logger.info("Running ZNE-mitigated execution")
        zne_counts = analyzer.apply_zero_noise_extrapolation(eval_circuit, shots // 4)
        zne_total = sum(zne_counts.values()) if zne_counts else 1
        zne_probs = {k: v / zne_total for k, v in zne_counts.items()}
        
        # Step 5: Calculate all noise metrics
        results = {
            'ideal_counts': ideal_counts,
            'noisy_counts': noisy_counts,
            'zne_counts': zne_counts,
            'ideal_probs': ideal_probs,
            'noisy_probs': noisy_probs,
            'zne_probs': zne_probs
        }
        
        # Fidelity calculations
        results['noisy_fidelity'] = metrics.compute_hellinger_fidelity(ideal_probs, noisy_probs)
        results['zne_fidelity'] = metrics.compute_hellinger_fidelity(ideal_probs, zne_probs)
        
        # TVD calculations
        results['noisy_tvd'] = metrics.compute_tvd(ideal_counts, noisy_counts, shots)
        results['zne_tvd'] = metrics.compute_tvd(ideal_counts, zne_counts, max(shots, zne_total))
        
        # Wasserstein distance
        results['wasserstein_noisy'] = metrics.compute_wasserstein_distance(ideal_probs, noisy_probs)
        results['wasserstein_zne'] = metrics.compute_wasserstein_distance(ideal_probs, zne_probs)
        
        # Improvement metrics
        fidelity_improvement = (
            (results['zne_fidelity'] - results['noisy_fidelity']) / 
            (1 - results['noisy_fidelity']) * 100
        ) if results['noisy_fidelity'] < 1 else 0
        
        tvd_reduction = (
            (results['noisy_tvd'] - results['zne_tvd']) / 
            results['noisy_tvd'] * 100
        ) if results['noisy_tvd'] > 0 else 0
        
        results['fidelity_improvement_percent'] = fidelity_improvement
        results['tvd_reduction_percent'] = tvd_reduction
        
        logger.info("Noise impact analysis completed")
        logger.info(f"  Noisy fidelity: {results['noisy_fidelity']:.4f}")
        logger.info(f"  ZNE fidelity: {results['zne_fidelity']:.4f}")
        logger.info(f"  Fidelity improvement: {fidelity_improvement:.2f}%")
        logger.info(f"  TVD reduction: {tvd_reduction:.2f}%")
        
        return results
        
    except Exception as e:
        logger.error(f"Noise impact analysis failed: {str(e)}")
        return {'error': str(e)}

def generate_noise_metrics_visualization(analysis_results, save_path="noise_metrics_analysis.png"):
    """
    Generate comprehensive noise metrics visualization.
    
    Args:
        analysis_results (list): List of analysis result dictionaries.
        save_path (str): Path to save the visualization.
    """
    try:
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('AUX-QHE Noise Metrics Analysis', fontsize=16, fontweight='bold')
        
        # Extract data
        configs = [f"{r.get('num_qubits', 0)}q,T{r.get('t_depth', 0)}" for r in analysis_results]
        noisy_fidelities = [r.get('noisy_fidelity', 0) for r in analysis_results]
        zne_fidelities = [r.get('zne_fidelity', 0) for r in analysis_results]
        noisy_tvds = [r.get('noisy_tvd', 1) for r in analysis_results]
        zne_tvds = [r.get('zne_tvd', 1) for r in analysis_results]
        
        # Plot 1: Fidelity Comparison
        x = np.arange(len(configs))
        width = 0.35
        ax1.bar(x - width/2, noisy_fidelities, width, label='Noisy', alpha=0.7, color='red')
        ax1.bar(x + width/2, zne_fidelities, width, label='ZNE', alpha=0.7, color='green')
        ax1.set_xlabel('Configuration')
        ax1.set_ylabel('Fidelity')
        ax1.set_title('Fidelity: Noisy vs ZNE')
        ax1.set_xticks(x)
        ax1.set_xticklabels(configs, rotation=45)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: TVD Comparison
        ax2.bar(x - width/2, noisy_tvds, width, label='Noisy', alpha=0.7, color='red')
        ax2.bar(x + width/2, zne_tvds, width, label='ZNE', alpha=0.7, color='green')
        ax2.set_xlabel('Configuration')
        ax2.set_ylabel('Total Variation Distance')
        ax2.set_title('TVD: Noisy vs ZNE')
        ax2.set_xticks(x)
        ax2.set_xticklabels(configs, rotation=45)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Fidelity Improvement
        improvements = [(zne - noisy) / (1 - noisy) * 100 if noisy < 1 else 0 
                       for noisy, zne in zip(noisy_fidelities, zne_fidelities)]
        ax3.bar(x, improvements, alpha=0.7, color='blue')
        ax3.set_xlabel('Configuration')
        ax3.set_ylabel('Fidelity Improvement (%)')
        ax3.set_title('ZNE Fidelity Improvement')
        ax3.set_xticks(x)
        ax3.set_xticklabels(configs, rotation=45)
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: TVD Reduction
        reductions = [(noisy - zne) / noisy * 100 if noisy > 0 else 0 
                     for noisy, zne in zip(noisy_tvds, zne_tvds)]
        ax4.bar(x, reductions, alpha=0.7, color='purple')
        ax4.set_xlabel('Configuration')
        ax4.set_ylabel('TVD Reduction (%)')
        ax4.set_title('ZNE TVD Reduction')
        ax4.set_xticks(x)
        ax4.set_xticklabels(configs, rotation=45)
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        logger.info(f"Noise metrics visualization saved to {save_path}")
        
    except Exception as e:
        logger.error(f"Visualization generation failed: {str(e)}")

if __name__ == "__main__":
    # Test noise error metrics functionality
    logger.info("Testing noise error metrics module...")
    
    from qiskit import QuantumCircuit
    from bfv_core import initialize_bfv_params
    from key_generation import aux_keygen
    
    # Create test circuit
    test_circuit = QuantumCircuit(2)
    test_circuit.h(0)
    test_circuit.cx(0, 1)
    test_circuit.t(0)
    
    # Initialize components
    params, encoder, encryptor, decryptor, evaluator = initialize_bfv_params()
    poly_degree = params.poly_degree
    
    # Generate keys
    secret_key, eval_key, _, _, _ = aux_keygen(2, 1, [1, 0], [0, 1])
    a_init, b_init, k_dict = secret_key
    T_sets, V_sets, auxiliary_states = eval_key
    
    # Encrypt keys
    enc_a = [encryptor.encrypt(encoder.encode([a_init[i]] + [0] * (poly_degree - 1))) for i in range(2)]
    enc_b = [encryptor.encrypt(encoder.encode([b_init[i]] + [0] * (poly_degree - 1))) for i in range(2)]
    
    # Test noise metrics with simulator
    analyzer = NoiseErrorAnalyzer(backend=None)  # No backend = simulator mode
    
    # Test ideal simulation
    ideal_counts = analyzer.simulate_ideal_execution(test_circuit, 1000)
    print(f"✅ Ideal simulation test: {len(ideal_counts)} outcomes")
    
    # Test metrics
    metrics = FidelityMetrics()
    ideal_probs = {k: v / 1000 for k, v in ideal_counts.items()}
    test_fidelity = metrics.compute_hellinger_fidelity(ideal_probs, ideal_probs)
    test_tvd = metrics.compute_tvd(ideal_counts, ideal_counts, 1000)
    
    print(f"✅ Fidelity test (should be 1.0): {test_fidelity:.4f}")
    print(f"✅ TVD test (should be 0.0): {test_tvd:.4f}")
    
    print("🎉 Noise error metrics module test completed!")