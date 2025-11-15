"""
Enhanced Zero Noise Extrapolation (ZNE) for AUX-QHE
Optimized for maximum noise mitigation based on algorithm performance attributes

This module provides advanced ZNE techniques specifically tuned for:
- AUX-QHE algorithm characteristics (T-depth, qubit count)
- IBM quantum hardware noise patterns
- Performance table metrics (Fidelity, TVD, Error Reduction)
"""

import logging
import numpy as np
import time
from typing import Dict, List, Tuple, Optional
from qiskit import QuantumCircuit
from qiskit_ibm_runtime import SamplerV2 as Sampler, SamplerOptions
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.quantum_info import hellinger_fidelity
from scipy.optimize import curve_fit
from circuit_evaluation import aux_eval

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnhancedZNEOptimizer:
    """
    Advanced ZNE implementation optimized for AUX-QHE algorithm performance.
    
    Features:
    - Adaptive noise scaling based on circuit characteristics
    - Multiple extrapolation models (linear, polynomial, exponential)
    - Circuit-aware noise amplification
    - Performance metrics tracking
    """
    
    def __init__(self, backend):
        self.backend = backend
        self.performance_history = []
        
    def adaptive_noise_factors(self, num_qubits: int, t_depth: int, aux_states: int) -> List[float]:
        """
        Generate adaptive noise scaling factors based on AUX-QHE circuit characteristics.
        
        Args:
            num_qubits: Number of qubits in circuit
            t_depth: T-gate depth
            aux_states: Number of auxiliary states
            
        Returns:
            List of optimized noise scaling factors
        """
        # Base factors for different circuit complexities
        if t_depth <= 2 and num_qubits <= 3:
            # Simple circuits - fine-grained sampling
            base_factors = [1.0, 1.3, 1.6, 2.0, 2.5]
        elif t_depth <= 3 and num_qubits <= 4:
            # Medium circuits - balanced sampling
            base_factors = [1.0, 1.5, 2.0, 2.8, 3.5]
        else:
            # Complex circuits - aggressive scaling needed
            base_factors = [1.0, 1.8, 2.5, 3.5, 4.5, 6.0]
        
        # Adjust based on auxiliary states (higher aux_states = more noise sensitivity)
        aux_factor = 1.0 + (aux_states / 10000)  # Scale based on aux complexity
        adjusted_factors = [f * aux_factor for f in base_factors]
        
        logger.info(f"Adaptive noise factors for {num_qubits}q, T{t_depth}, {aux_states} aux: {adjusted_factors}")
        return adjusted_factors
    
    def circuit_folding_amplification(self, circuit: QuantumCircuit, noise_factor: float) -> QuantumCircuit:
        """
        Apply circuit folding to amplify noise by specified factor.
        Uses unitary folding: U → U·U†·U (measurement gates excluded)
        """
        if noise_factor == 1.0:
            return circuit
        
        # Separate measurement gates from unitary operations  
        # Copy the original circuit structure (registers and all)
        unitary_circuit = QuantumCircuit(*circuit.qregs, *circuit.cregs)
        measurement_ops = []
        
        for instr, qargs, cargs in circuit.data:
            if instr.name == 'measure':
                measurement_ops.append((instr, qargs, cargs))
            else:
                unitary_circuit.append(instr, qargs, cargs)
        
        # Apply folding only to unitary part
        folded_circuit = unitary_circuit.copy()
        
        # Calculate number of folding rounds needed
        fold_rounds = max(1, int((noise_factor - 1.0) / 2.0))
        
        for _ in range(fold_rounds):
            # Add inverse operations (U†) - only for unitary gates
            try:
                inverse_circuit = unitary_circuit.inverse()
                folded_circuit = folded_circuit.compose(inverse_circuit)
                # Add original operations again (U)
                folded_circuit = folded_circuit.compose(unitary_circuit)
            except Exception as e:
                logger.warning(f"Circuit folding failed: {e}, skipping fold round")
                break
        
        # Re-add measurement gates at the end
        for instr, qargs, cargs in measurement_ops:
            folded_circuit.append(instr, qargs, cargs)
        
        logger.debug(f"Circuit folding: {noise_factor}x noise, {fold_rounds} rounds, "
                    f"{circuit.size()} → {folded_circuit.size()} gates")
        
        return folded_circuit
    
    def multi_model_extrapolation(self, noise_factors: List[float], 
                                  fidelities: List[float]) -> Tuple[float, str, float]:
        """
        Apply multiple extrapolation models and choose the best fit.
        
        Returns:
            Tuple of (extrapolated_fidelity, best_model_name, confidence_score)
        """
        models = {}
        
        # Linear extrapolation
        try:
            z = np.polyfit(noise_factors, fidelities, 1)
            linear_extrap = np.poly1d(z)(0.0)
            # R² calculation for linear fit
            y_pred = np.poly1d(z)(noise_factors)
            ss_res = np.sum((np.array(fidelities) - y_pred) ** 2)
            ss_tot = np.sum((np.array(fidelities) - np.mean(fidelities)) ** 2)
            r2_linear = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
            models['linear'] = (max(0.0, min(1.0, linear_extrap)), r2_linear)
        except:
            models['linear'] = (0.0, 0.0)
        
        # Exponential extrapolation: f(λ) = A * exp(-B * λ)
        try:
            def exp_model(x, A, B):
                return A * np.exp(-B * x)
            
            popt, _ = curve_fit(exp_model, noise_factors, fidelities, 
                               bounds=([0.5, 0], [1.5, 10]), maxfev=1000)
            exp_extrap = exp_model(0.0, *popt)
            
            # Calculate R² for exponential fit
            y_pred = exp_model(np.array(noise_factors), *popt)
            ss_res = np.sum((np.array(fidelities) - y_pred) ** 2)
            ss_tot = np.sum((np.array(fidelities) - np.mean(fidelities)) ** 2)
            r2_exp = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
            models['exponential'] = (max(0.0, min(1.0, exp_extrap)), r2_exp)
        except:
            models['exponential'] = (0.0, 0.0)
        
        # Polynomial extrapolation (degree 2)
        if len(noise_factors) >= 3:
            try:
                z = np.polyfit(noise_factors, fidelities, 2)
                poly_extrap = np.poly1d(z)(0.0)
                
                # R² calculation for polynomial fit
                y_pred = np.poly1d(z)(noise_factors)
                ss_res = np.sum((np.array(fidelities) - y_pred) ** 2)
                ss_tot = np.sum((np.array(fidelities) - np.mean(fidelities)) ** 2)
                r2_poly = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
                models['polynomial'] = (max(0.0, min(1.0, poly_extrap)), r2_poly)
            except:
                models['polynomial'] = (0.0, 0.0)
        
        # Choose best model based on R² score
        best_model = max(models.items(), key=lambda x: x[1][1])
        best_fidelity, confidence = best_model[1]
        best_name = best_model[0]
        
        logger.debug(f"ZNE extrapolation models: {models}")
        logger.info(f"Best ZNE model: {best_name} (R²={confidence:.3f}) → fidelity={best_fidelity:.4f}")
        
        return best_fidelity, best_name, confidence
    
    def enhanced_zne_execution(self, circuit: QuantumCircuit, enc_a: List, enc_b: List, 
                              auxiliary_states: Dict, max_t_depth: int,
                              encryptor, decryptor, encoder, evaluator, poly_degree: int,
                              shots: int = 1024) -> Dict:
        """
        Execute enhanced ZNE with comprehensive performance tracking.
        
        Returns:
            Dictionary with enhanced performance metrics matching algorithm_performance table
        """
        start_time = time.perf_counter()
        
        # Determine circuit characteristics
        num_qubits = circuit.num_qubits
        t_depth = max_t_depth
        aux_states = len(auxiliary_states)
        
        logger.info(f"Enhanced ZNE for {num_qubits}q, T{t_depth}, {aux_states} aux states")
        
        # Step 1: Apply AUX-QHE homomorphic evaluation
        eval_start = time.perf_counter()
        eval_circuit, final_enc_a, final_enc_b = aux_eval(
            circuit, enc_a, enc_b, auxiliary_states, max_t_depth,
            encryptor, decryptor, encoder, evaluator, poly_degree, debug=False
        )
        eval_time = time.perf_counter() - eval_start
        
        # Add measurements for hardware execution
        if eval_circuit is not None:
            from qiskit import ClassicalRegister
            eval_circuit_with_measurements = eval_circuit.copy()
            if len(eval_circuit_with_measurements.clbits) == 0:
                cr = ClassicalRegister(eval_circuit_with_measurements.num_qubits, 'c')
                eval_circuit_with_measurements.add_register(cr)
            eval_circuit_with_measurements.measure_all()
            eval_circuit = eval_circuit_with_measurements
        
        # Step 2: Get adaptive noise factors
        noise_factors = self.adaptive_noise_factors(num_qubits, t_depth, aux_states)
        
        # Step 3: Execute at different noise levels
        zne_start = time.perf_counter()
        fidelity_data = []
        execution_times = []
        
        for factor in noise_factors:
            factor_start = time.perf_counter()
            
            # Apply noise amplification
            if factor > 1.0:
                amplified_circuit = self.circuit_folding_amplification(eval_circuit, factor)
            else:
                amplified_circuit = eval_circuit
            
            # Transpile for hardware
            pass_manager = generate_preset_pass_manager(optimization_level=1, backend=self.backend)
            transpiled_circuit = pass_manager.run(amplified_circuit)
            
            # Execute on hardware (fixed for SamplerV2)
            options = SamplerOptions()
            options.default_shots = shots
            sampler = Sampler(mode=self.backend, options=options)
            
            try:
                job = sampler.run([(transpiled_circuit, None)])
                result = job.result()
                
                # Extract counts
                if hasattr(result[0].data, 'meas'):
                    counts = result[0].data.meas.get_counts()
                elif hasattr(result[0].data, 'c'):
                    counts = result[0].data.c.get_counts()
                else:
                    data_keys = list(result[0].data.__dict__.keys())
                    counts = getattr(result[0].data, data_keys[0]).get_counts() if data_keys else {}
                
                # Calculate fidelity (simplified - use distribution entropy as proxy)
                if counts:
                    total_shots = sum(counts.values())
                    probs = [count/total_shots for count in counts.values()]
                    entropy = -sum(p * np.log2(p + 1e-10) for p in probs)
                    max_entropy = np.log2(len(counts))
                    # Normalized entropy as fidelity proxy (higher entropy = more noise)
                    fidelity = 1.0 - (entropy / max_entropy if max_entropy > 0 else 0)
                else:
                    fidelity = 0.0
                
                fidelity_data.append(fidelity)
                factor_time = time.perf_counter() - factor_start
                execution_times.append(factor_time)
                
                logger.debug(f"Noise factor {factor:.1f}: fidelity={fidelity:.4f}, time={factor_time:.2f}s")
                
            except Exception as e:
                logger.error(f"Execution failed at noise factor {factor}: {e}")
                fidelity_data.append(0.0)
                execution_times.append(0.0)
        
        zne_time = time.perf_counter() - zne_start
        
        # Step 4: Multi-model extrapolation
        if len(fidelity_data) >= 2:
            zne_fidelity, best_model, confidence = self.multi_model_extrapolation(
                noise_factors, fidelity_data
            )
        else:
            zne_fidelity, best_model, confidence = 0.0, "none", 0.0
        
        # Step 5: Compile performance metrics (matching algorithm_performance table format)
        total_time = time.perf_counter() - start_time
        
        # Calculate improvement metrics
        baseline_fidelity = fidelity_data[0] if fidelity_data else 0.0  # No noise amplification
        if baseline_fidelity < 1.0:
            fidelity_improvement = ((zne_fidelity - baseline_fidelity) / (1 - baseline_fidelity)) * 100
        else:
            fidelity_improvement = 0.0
        
        # Calculate TVD (simplified)
        noisy_tvd = 1.0 - baseline_fidelity
        zne_tvd = 1.0 - zne_fidelity
        tvd_reduction = ((noisy_tvd - zne_tvd) / noisy_tvd * 100) if noisy_tvd > 0 else 0.0
        
        results = {
            # Circuit characteristics
            'num_qubits': num_qubits,
            't_depth': t_depth,
            'aux_states': aux_states,
            
            # Performance metrics (matching algorithm_performance format)
            'fidelity_baseline': baseline_fidelity,
            'fidelity_zne': zne_fidelity,
            'fidelity_improvement_percent': fidelity_improvement,
            'tvd_baseline': noisy_tvd,
            'tvd_zne': zne_tvd, 
            'tvd_reduction_percent': tvd_reduction,
            
            # Timing metrics
            'aux_eval_time': eval_time,
            'zne_execution_time': zne_time,
            'total_time': total_time,
            'avg_shot_time': np.mean(execution_times) if execution_times else 0.0,
            
            # ZNE specific metrics
            'noise_factors_used': noise_factors,
            'fidelity_progression': fidelity_data,
            'extrapolation_model': best_model,
            'extrapolation_confidence': confidence,
            
            # Hardware efficiency
            'total_shots': len(noise_factors) * shots,
            'successful_executions': len([f for f in fidelity_data if f > 0]),
            'hardware_efficiency': len([f for f in fidelity_data if f > 0]) / len(noise_factors)
        }
        
        # Store in performance history
        self.performance_history.append(results)
        
        logger.info(f"Enhanced ZNE completed: baseline={baseline_fidelity:.4f} → ZNE={zne_fidelity:.4f} "
                   f"({fidelity_improvement:.1f}% improvement)")
        
        return results
    
    def generate_zne_performance_table(self, results_list: List[Dict]) -> str:
        """
        Generate performance table matching algorithm_performance format with ZNE enhancements.
        """
        if not results_list:
            return "No ZNE results available"
        
        header = ("Test Config\t| Qubits\t| T-Depth\t| Aux States\t| Baseline Fidelity\t| ZNE Fidelity\t| "
                 "Improvement (%)\t| TVD Reduction (%)\t| ZNE Model\t| Confidence\t| Total Time (s)")
        
        separator = "-" * len(header)
        rows = [header, separator]
        
        for i, result in enumerate(results_list):
            config = f"zne_test_{i+1}"
            row = (f"{config}\t| {result['num_qubits']}\t| {result['t_depth']}\t| "
                  f"{result['aux_states']}\t| {result['fidelity_baseline']:.4f}\t\t| "
                  f"{result['fidelity_zne']:.4f}\t\t| {result['fidelity_improvement_percent']:.2f}\t\t| "
                  f"{result['tvd_reduction_percent']:.2f}\t\t\t| {result['extrapolation_model']}\t| "
                  f"{result['extrapolation_confidence']:.3f}\t\t| {result['total_time']:.2f}")
            rows.append(row)
        
        return "\n".join(rows)

def run_enhanced_zne_analysis(backend, test_configs: List[Tuple[int, int]], 
                             encryptor, decryptor, encoder, evaluator, poly_degree: int) -> List[Dict]:
    """
    Run comprehensive enhanced ZNE analysis for multiple AUX-QHE configurations.
    
    Args:
        backend: IBM quantum backend
        test_configs: List of (num_qubits, t_depth) tuples
        BFV components: encryptor, decryptor, encoder, evaluator, poly_degree
    
    Returns:
        List of detailed ZNE performance results
    """
    optimizer = EnhancedZNEOptimizer(backend)
    results = []
    
    logger.info(f"Starting enhanced ZNE analysis for {len(test_configs)} configurations")
    
    for num_qubits, t_depth in test_configs:
        logger.info(f"\\n=== Enhanced ZNE Test: {num_qubits} qubits, T-depth {t_depth} ===")
        
        # Generate test circuit
        from qiskit import QuantumCircuit
        circuit = QuantumCircuit(num_qubits)
        
        # Add typical AUX-QHE circuit structure
        for i in range(num_qubits):
            circuit.h(i)
        
        for i in range(min(t_depth, num_qubits)):
            circuit.t(i)
        
        if num_qubits > 1:
            for i in range(num_qubits - 1):
                circuit.cx(i, i + 1)
        
        # Generate mock auxiliary states (for testing)
        auxiliary_states = {f"aux_{i}": i for i in range(100)}  # Simplified
        
        # Generate mock encrypted keys
        enc_a = [encryptor.encrypt(encoder.encode([1] + [0] * (poly_degree - 1))) 
                for _ in range(num_qubits)]
        enc_b = [encryptor.encrypt(encoder.encode([0] + [0] * (poly_degree - 1))) 
                for _ in range(num_qubits)]
        
        # Run enhanced ZNE
        try:
            result = optimizer.enhanced_zne_execution(
                circuit, enc_a, enc_b, auxiliary_states, t_depth,
                encryptor, decryptor, encoder, evaluator, poly_degree
            )
            results.append(result)
            
        except Exception as e:
            logger.error(f"Enhanced ZNE failed for {num_qubits}q, T{t_depth}: {e}")
            print(f"DEBUG: Enhanced ZNE error for {num_qubits}q, T{t_depth}: {e}")
            import traceback
            traceback.print_exc()
    
    # Generate summary table
    if results:
        table = optimizer.generate_zne_performance_table(results)
        print(f"\\n=== Enhanced ZNE Performance Analysis ===\\n{table}")
        
        # Summary statistics
        avg_improvement = np.mean([r['fidelity_improvement_percent'] for r in results])
        avg_tvd_reduction = np.mean([r['tvd_reduction_percent'] for r in results])
        
        print(f"\\n=== ZNE Enhancement Summary ===")
        print(f"Average fidelity improvement: {avg_improvement:.2f}%")
        print(f"Average TVD reduction: {avg_tvd_reduction:.2f}%")
        print(f"Total configurations tested: {len(results)}")
        
    return results

if __name__ == "__main__":
    # Example usage
    logger.info("Enhanced ZNE Optimization Module loaded successfully")
    print("🎯 Enhanced ZNE ready for AUX-QHE optimization!")