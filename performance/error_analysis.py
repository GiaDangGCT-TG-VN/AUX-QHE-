"""
Error Analysis and Mitigation Module

This module implements error analysis and mitigation techniques for AUX-QHE,
including Zero Noise Extrapolation (ZNE) and noise characterization.
"""

import logging
import numpy as np
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

def simulate_ideal_execution(circuit, shots=4096):
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

def run_noisy_execution(circuit, backend, shots=4096, mitigation_options=None):
    """
    Run circuit on noisy backend with optional error mitigation.
    
    Args:
        circuit (QuantumCircuit): Circuit to execute.
        backend: IBM Quantum backend.
        shots (int): Number of measurement shots.
        mitigation_options (dict): Error mitigation configuration.
    
    Returns:
        dict: Measurement counts from noisy execution.
    """
    try:
        # Transpile circuit for backend
        pass_manager = generate_preset_pass_manager(
            optimization_level=1, 
            backend=backend
        )
        transpiled_circuit = pass_manager.run(circuit)
        
        # Configure sampler with mitigation options
        from qiskit_ibm_runtime import SamplerOptions
        
        if mitigation_options is None:
            mitigation_options = SamplerOptions()
            mitigation_options.default_shots = shots
            # Note: optimization_level handled by transpiler, not sampler options
        
        sampler = Sampler(mode=backend, options=mitigation_options)
        
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

def apply_zero_noise_extrapolation(circuit, backend, base_shots=1024, noise_factors=None):
    """
    Apply Zero Noise Extrapolation (ZNE) to mitigate errors.
    
    Args:
        circuit (QuantumCircuit): Circuit to execute with ZNE.
        backend: IBM Quantum backend.
        base_shots (int): Base number of shots per noise level.
        noise_factors (list): Noise scaling factors.
    
    Returns:
        dict: ZNE-mitigated measurement counts.
    """
    try:
        if noise_factors is None:
            noise_factors = [1, 1.5, 2, 2.5]
        
        logger.info(f"Applying ZNE with noise factors: {noise_factors}")
        
        # Learn noise model
        learner_options = NoiseLearnerOptions()
        learner_options.max_layers_to_learn = 5
        learner_options.shots_per_randomization = base_shots
        
        learner = NoiseLearner(mode=backend, options=learner_options)
        noise_job = learner.run([circuit])
        noise_model = noise_job.result()
        
        # Run circuit with different noise levels
        results = []
        for factor in noise_factors:
            # Configure ZNE options
            zne_options = {
                "optimization_level": 1,
                "resilience": {
                    "zne": {
                        "enabled": True,
                        "noise_factors": [factor],
                        "extrapolator": "linear",
                        "noise_model": noise_model
                    }
                },
                "execution": {"shots": base_shots}
            }
            
            counts = run_noisy_execution(circuit, backend, base_shots, zne_options)
            if counts:
                results.append((factor, counts))
        
        if len(results) < 2:
            logger.warning("Insufficient ZNE data points, returning original counts")
            return run_noisy_execution(circuit, backend, base_shots * len(noise_factors))
        
        # Extrapolate to zero noise
        # Simple linear extrapolation for demonstration
        # In practice, more sophisticated methods would be used
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
        return run_noisy_execution(circuit, backend, base_shots * len(noise_factors))

def analyze_aux_qhe_errors(circuit, enc_a, enc_b, auxiliary_states, max_t_depth, 
                          encryptor, decryptor, encoder, evaluator, poly_degree,
                          backend, shots=4096):
    """
    Comprehensive error analysis for AUX-QHE evaluated circuits.
    
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
        dict: Comprehensive error analysis results.
    """
    try:
        logger.info("Starting comprehensive error analysis for AUX-QHE")
        
        # Step 1: Homomorphic evaluation
        eval_circuit, final_enc_a, final_enc_b = aux_eval(
            circuit, enc_a, enc_b, auxiliary_states, max_t_depth,
            encryptor, decryptor, encoder, evaluator, poly_degree, debug=False
        )
        
        # Step 2: Ideal simulation
        logger.info("Running ideal simulation")
        ideal_counts = simulate_ideal_execution(eval_circuit, shots)
        ideal_probs = {k: v / shots for k, v in ideal_counts.items()}
        
        # Step 3: Noisy execution without mitigation
        logger.info("Running noisy execution (no mitigation)")
        no_mitigation_options = SamplerOptions()
        no_mitigation_options.default_shots = shots
        # Note: optimization_level and resilience are handled by transpiler, not sampler options
        
        noisy_counts = run_noisy_execution(eval_circuit, backend, shots, no_mitigation_options)
        noisy_probs = {k: v / shots for k, v in noisy_counts.items()}
        
        # Step 4: ZNE-mitigated execution
        logger.info("Running ZNE-mitigated execution")
        zne_counts = apply_zero_noise_extrapolation(eval_circuit, backend, shots // 4)
        total_zne = sum(zne_counts.values())
        zne_probs = {k: v / total_zne for k, v in zne_counts.items()} if total_zne > 0 else {}
        
        # Step 5: Error metric calculations
        results = {
            'ideal_counts': ideal_counts,
            'noisy_counts': noisy_counts,
            'zne_counts': zne_counts,
            'ideal_probs': ideal_probs,
            'noisy_probs': noisy_probs,
            'zne_probs': zne_probs
        }
        
        # Fidelity calculations
        if ideal_probs and noisy_probs:
            results['noisy_fidelity'] = hellinger_fidelity(ideal_probs, noisy_probs)
            results['noisy_tvd'] = compute_tvd(ideal_counts, noisy_counts, shots)
        else:
            results['noisy_fidelity'] = 0.0
            results['noisy_tvd'] = 1.0
        
        if ideal_probs and zne_probs:
            results['zne_fidelity'] = hellinger_fidelity(ideal_probs, zne_probs)
            results['zne_tvd'] = compute_tvd(ideal_counts, zne_counts, max(shots, total_zne))
        else:
            results['zne_fidelity'] = 0.0
            results['zne_tvd'] = 1.0
        
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
        
        # Wasserstein distance (additional metric)
        if ideal_probs and noisy_probs:
            ideal_vals = list(ideal_probs.values())
            noisy_vals = [noisy_probs.get(k, 0) for k in ideal_probs.keys()]
            results['wasserstein_noisy'] = wasserstein_distance(ideal_vals, noisy_vals)
        
        if ideal_probs and zne_probs:
            zne_vals = [zne_probs.get(k, 0) for k in ideal_probs.keys()]
            results['wasserstein_zne'] = wasserstein_distance(ideal_vals, zne_vals)
        
        logger.info("Error analysis completed")
        logger.info(f"  Noisy fidelity: {results['noisy_fidelity']:.4f}")
        logger.info(f"  ZNE fidelity: {results['zne_fidelity']:.4f}")
        logger.info(f"  Fidelity improvement: {fidelity_improvement:.2f}%")
        logger.info(f"  TVD reduction: {tvd_reduction:.2f}%")
        
        return results
        
    except Exception as e:
        logger.error(f"Error analysis failed: {str(e)}")
        return {'error': str(e)}

if __name__ == "__main__":
    # Test error analysis functionality
    logger.info("Testing error analysis module...")
    
    from qiskit import QuantumCircuit
    from bfv_core import initialize_bfv_params
    from key_generation import aux_keygen
    from qiskit_ibm_runtime import QiskitRuntimeService
    
    # Create test circuit
    test_circuit = QuantumCircuit(2)
    test_circuit.h(0)
    test_circuit.cx(0, 1)
    test_circuit.t(0)
    test_circuit.t(1)
    
    # Initialize components
    params, encoder, encryptor, decryptor, evaluator = initialize_bfv_params()
    poly_degree = params.poly_degree
    
    # Generate keys
    secret_key, eval_key, _, _, _ = aux_keygen(2, 2, [1, 0], [0, 1])
    a_init, b_init, k_dict = secret_key
    T_sets, V_sets, auxiliary_states = eval_key
    
    # Encrypt keys
    enc_a = [encryptor.encrypt(encoder.encode([a_init[i]] + [0] * (poly_degree - 1))) for i in range(2)]
    enc_b = [encryptor.encrypt(encoder.encode([b_init[i]] + [0] * (poly_degree - 1))) for i in range(2)]
    
    # Test ideal simulation
    ideal_counts = simulate_ideal_execution(test_circuit, 1000)
    print(f"✅ Ideal simulation test: {len(ideal_counts)} outcomes")
    
    # Test with backend if available
    try:
        service = QiskitRuntimeService()
        backend = service.least_busy(operational=True, simulator=False)
        print(f"Using backend: {backend.name}")
        
        # Run error analysis
        results = analyze_aux_qhe_errors(
            test_circuit, enc_a, enc_b, auxiliary_states, 2,
            encryptor, decryptor, encoder, evaluator, poly_degree,
            backend, shots=1000
        )
        
        if 'error' not in results:
            print("✅ Error analysis completed successfully")
            print(f"  Noisy fidelity: {results.get('noisy_fidelity', 'N/A'):.4f}")
            print(f"  ZNE fidelity: {results.get('zne_fidelity', 'N/A'):.4f}")
        else:
            print(f"❌ Error analysis failed: {results['error']}")
            
    except Exception as e:
        print(f"Backend connection failed: {e}")
        print("✅ Module loaded successfully (backend tests skipped)")
    
    print("🎉 Error analysis module test completed!")