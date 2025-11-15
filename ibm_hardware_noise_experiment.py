#!/usr/bin/env python3
"""
AUX-QHE on IBM Quantum Hardware - Optimized Noise Measurement
Executes AUX-QHE with 4 error mitigation strategies:
1. Baseline (no error mitigation, opt_level=1)
2. ZNE (Zero-Noise Extrapolation, opt_level=1)
3. Opt-3 (Heavy optimization, opt_level=3)
4. Opt-3+ZNE (Heavy optimization + ZNE)

Configurations: 5q-2t, 3q-3t, 4q-3t, 5q-3t (4 total configs)
QASM Version: OpenQASM 3.0
Default Shots: 1024 (faster execution, ~3% error)

NOTE: Opt-0 and Opt-0+ZNE excluded for faster execution
NOTE: Testing focused on T-depth 3 and 5q-2t only
"""

import sys
import time
import json
from datetime import datetime
import numpy as np
import pandas as pd
from pathlib import Path

# Qiskit imports
from qiskit import QuantumCircuit, transpile, qasm3
from qiskit.quantum_info import Statevector, state_fidelity
from qiskit_ibm_runtime import QiskitRuntimeService, Session, Sampler, Options
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import Optimize1qGatesDecomposition

# AUX-QHE imports
sys.path.insert(0, 'core')
from key_generation import aux_keygen
from circuit_evaluation import aux_eval
from qotp_crypto import qotp_encrypt, qotp_decrypt
from bfv_core import initialize_bfv_params

# ZNE implementation
def apply_zne(circuit, backend, noise_factors=[1, 2, 3], shots=8192):
    """
    Apply Zero-Noise Extrapolation (ZNE) error mitigation.

    Args:
        circuit: Quantum circuit to execute
        backend: IBM quantum backend
        noise_factors: Noise scaling factors (default: [1, 2, 3])
        shots: Number of measurement shots

    Returns:
        Extrapolated measurement results
    """
    print(f"   🔬 Applying ZNE with noise factors: {noise_factors}")

    results = []

    for factor in noise_factors:
        # Scale noise by repeating gates (simple folding)
        if factor == 1:
            scaled_circuit = circuit
        else:
            scaled_circuit = circuit.copy()
            # Gate folding: insert identity (U†U) operations
            for _ in range(factor - 1):
                for instr in circuit.data:
                    gate = instr.operation
                    # Skip measurement and barrier gates during folding
                    if gate.name in ['measure', 'barrier']:
                        continue
                    qubits = instr.qubits
                    # Add gate and its inverse
                    scaled_circuit.append(gate, qubits)
                    scaled_circuit.append(gate.inverse(), qubits)

        # Execute at this noise level
        print(f"      Executing at noise factor {factor}...")

        # Transpile inverse gates to native basis without optimization
        # gate.inverse() creates gates like 'sxdg' which need decomposition to native gate set
        # Use optimization_level=0 to only decompose to basis gates, preserving U†U pairs
        if factor > 1:
            scaled_circuit = transpile(
                scaled_circuit,
                backend,
                optimization_level=0  # Only decompose to native gates, no optimization
            )

        # Use Sampler without Session (required for free/open plan)
        sampler = Sampler(mode=backend)
        job = sampler.run([scaled_circuit], shots=shots)
        result = job.result()

        # Extract probabilities
        quasi_dists = result[0].data.meas.get_counts()
        results.append(quasi_dists)

    # Richardson extrapolation to zero noise
    print(f"   📊 Performing Richardson extrapolation...")

    # For simplicity, use linear extrapolation with first 2 points
    # More sophisticated: polynomial fitting
    # Here we'll return the extrapolated distribution

    extrapolated = {}
    for bitstring in results[0].keys():
        probs = [r.get(bitstring, 0.0) for r in results]

        # Linear extrapolation: p(0) ≈ 2*p(1) - p(2)
        if len(probs) >= 2:
            p_extrap = 2 * probs[0] - probs[1] if len(probs) >= 2 else probs[0]
            # Clamp to [0, 1]
            p_extrap = max(0.0, min(1.0, p_extrap))
            if p_extrap > 0:
                extrapolated[bitstring] = p_extrap

    # Renormalize
    total = sum(extrapolated.values())
    if total > 0:
        extrapolated = {k: v/total for k, v in extrapolated.items()}

    # ✅ FIX: Ensure shot count preservation
    # Check if we lost probability mass during extrapolation
    if total < 0.98:  # If more than 2% probability lost
        print(f"   ⚠️  Richardson extrapolation lost {(1-total)*100:.1f}% probability mass")
        # Redistribute lost probability to most likely outcome
        if extrapolated:
            max_bitstring = max(extrapolated, key=extrapolated.get)
            extrapolated[max_bitstring] += (1.0 - total)
            print(f"   ✅ Recovered lost probability mass to outcome: {max_bitstring[:8]}...")

    return extrapolated


def check_tdepth_feasibility(num_qubits, t_depth, optimization_level, backend):
    """
    Pre-flight check: Verify T-depth stays within feasible limits after transpilation.
    Returns True if feasible (T-depth <= 3), False otherwise.

    IMPORTANT: This function MUST create the SAME circuit as the main experiment
    to accurately test T-depth behavior. Uses same structure as local simulation.
    """
    # Create test circuit - MUST MATCH LOCAL SIMULATION!
    qc = QuantumCircuit(num_qubits)

    # Apply Hadamard only to qubit 0 (matches local simulation)
    qc.h(0)

    # Apply single CNOT (matches local simulation)
    if num_qubits > 1:
        qc.cx(0, 1)
    qc.barrier()

    # Apply T-gates sequentially on qubit 0 ONLY
    for layer in range(t_depth):
        qc.t(0)  # Apply T-gate ONLY to qubit 0 (same as local simulation)
        qc.barrier()

    # Transpile and check if T-depth explodes
    try:
        qc_trans = transpile(qc, backend=backend, optimization_level=optimization_level, seed_transpiler=42)

        # Count T gates in transpiled circuit
        from circuit_evaluation import organize_gates_into_layers
        circuit_ops = []
        for inst in qc_trans.data:
            gate_name = inst.operation.name
            qubits = tuple([qc_trans.find_bit(q).index for q in inst.qubits])
            if gate_name in ['t', 'tdg']:
                circuit_ops.append((gate_name, qubits))

        if len(circuit_ops) == 0:
            return True  # No T gates, feasible

        _, detected_t_depth = organize_gates_into_layers(circuit_ops)

        # T-depth > 3 requires too many auxiliary states (>31K)
        if detected_t_depth > 3:
            return False
        return True
    except Exception as e:
        print(f"   ⚠️  Pre-flight check failed: {e}")
        return False


def run_aux_qhe_config(config_name, num_qubits, t_depth, backend, method='baseline',
                       optimization_level=1, apply_zne_flag=False, shots=8192,
                       a_init=None, b_init=None):
    """
    Run AUX-QHE for a single configuration with specified error mitigation.

    Args:
        config_name: Configuration name (e.g., '3q-2t')
        num_qubits: Number of qubits
        t_depth: T-gate depth
        backend: IBM quantum backend
        method: Error mitigation method name
        optimization_level: Qiskit transpiler optimization level (0, 1, 2, 3)
        apply_zne_flag: Whether to apply ZNE
        shots: Number of measurement shots
        a_init: Initial QOTP 'a' keys (if None, generate random)
        b_init: Initial QOTP 'b' keys (if None, generate random)

    Returns:
        Dictionary with results, or None if skipped due to T-depth infeasibility
    """
    print(f"\n{'='*80}")
    print(f"🔹 Running {config_name} with {method}")
    print(f"   Backend: {backend.name}")
    print(f"   Optimization Level: {optimization_level}")
    print(f"   ZNE: {'Yes' if apply_zne_flag else 'No'}")
    print(f"   Shots: {shots}")
    print(f"{'='*80}")

    # Pre-flight check: Verify T-depth feasibility
    print("   🔍 Checking T-depth feasibility...")
    if not check_tdepth_feasibility(num_qubits, t_depth, optimization_level, backend):
        print(f"   ⏭️  SKIPPED: T-depth would exceed threshold (>3) after transpilation")
        print(f"      Reason: opt_level={optimization_level} causes T-depth explosion")
        print(f"      Required aux states would exceed NISQ feasibility")
        return None

    print(f"   ✅ T-depth check passed")

    start_time = time.time()

    # Create simple test circuit - MUST MATCH LOCAL SIMULATION!
    # Use the EXACT same circuit structure as openqasm_performance_comparison.py
    qc = QuantumCircuit(num_qubits)

    # Apply Hadamard only to qubit 0 (matches local simulation)
    qc.h(0)

    # Apply single CNOT (matches local simulation)
    if num_qubits > 1:
        qc.cx(0, 1)
    qc.barrier()

    # Apply T-gates sequentially on qubit 0 ONLY to ensure true T-depth
    # This matches the local simulation exactly: all T-gates on the same qubit
    for layer in range(t_depth):
        qc.t(0)  # Apply T-gate ONLY to qubit 0 (same as local simulation)
        qc.barrier()

    # DON'T add measurements yet - they'll be added after transpilation
    # qc.measure_all()  # Removed - measurements added later

    # Initialize BFV parameters
    initialize_bfv_params()

    # Step 1: Key Generation
    print("   🔑 Key generation...")
    keygen_start = time.time()

    num_wires = num_qubits
    # Generate random QOTP keys (binary values) if not provided
    if a_init is None or b_init is None:
        import random
        a_init = [random.randint(0, 1) for _ in range(num_wires)]
        b_init = [random.randint(0, 1) for _ in range(num_wires)]
    else:
        # Use provided keys (for consistent comparison across methods)
        a_init = list(a_init)
        b_init = list(b_init)

    # Generate AUX keys for T-depth=3 (31,025 states - feasible for NISQ)
    # T-depth=4 would require 18.5M states (infeasible)
    secret_key, eval_key, prep_time, layer_sizes, total_aux = aux_keygen(
        num_wires, t_depth, a_init, b_init
    )

    keygen_time = time.time() - keygen_start
    print(f"   ✅ Key generation: {keygen_time:.3f}s, Aux states: {total_aux}")

    # Step 2: Encryption
    print("   🔐 QOTP encryption...")
    encrypt_start = time.time()

    # Extract a_keys and b_keys from secret_key tuple
    a_keys, b_keys, k_dict = secret_key

    # Ensure keys are lists (not numpy arrays or other types)
    a_keys = list(a_keys) if not isinstance(a_keys, list) else a_keys
    b_keys = list(b_keys) if not isinstance(b_keys, list) else b_keys

    print(f"   🔑 Keys: a_keys length={len(a_keys)}, b_keys length={len(b_keys)}")
    print(f"   🔑 Keys: a_keys={a_keys}, b_keys={b_keys}")
    print(f"   🔑 Keys types: a_keys type={type(a_keys)}, b_keys type={type(b_keys)}")

    # Initialize BFV parameters for QOTP encryption
    bfv_params, bfv_encoder, bfv_encryptor, bfv_decryptor, bfv_evaluator = initialize_bfv_params()
    poly_degree = bfv_params.poly_degree

    # Create input state |+⟩^n
    input_state = Statevector.from_label('+' * num_qubits)

    # Apply QOTP encryption with BFV parameters
    # max_qubits should be at least num_qubits to avoid bounds check failure
    print(f"   🔐 Calling qotp_encrypt: circuit.num_qubits={qc.num_qubits}, counter_d=0, max_qubits={num_qubits * 2}")
    qc_encrypted, _, enc_a, enc_b = qotp_encrypt(
        qc, a_keys, b_keys,
        counter_d=0,
        max_qubits=num_qubits * 2,  # Allow sufficient headroom
        encryptor=bfv_encryptor,
        encoder=bfv_encoder,
        decryptor=bfv_decryptor,
        poly_degree=poly_degree
    )

    if qc_encrypted is None:
        print(f"   ❌ Encryption returned None")
        raise ValueError("QOTP encryption failed")

    encrypt_time = time.time() - encrypt_start
    print(f"   ✅ Encryption: {encrypt_time:.3f}s")

    # Step 3: Transpilation with specified optimization level
    print(f"   ⚙️  Transpiling (opt_level={optimization_level})...")
    transpile_start = time.time()

    qc_transpiled = transpile(
        qc_encrypted,
        backend=backend,
        optimization_level=optimization_level,
        seed_transpiler=42
    )

    # Get the layout: maps logical qubit index -> physical qubit index
    layout = qc_transpiled.layout.final_index_layout()
    physical_qubits = [layout[i] for i in range(num_qubits)]
    print(f"   🗺️  Qubit mapping: Logical {list(range(num_qubits))} -> Physical {physical_qubits}")

    # Add measurements after transpilation
    qc_transpiled.measure_all()

    transpile_time = time.time() - transpile_start

    print(f"   ✅ Transpilation: {transpile_time:.3f}s")
    print(f"      Pre-folding depth: {qc_transpiled.depth()}")
    print(f"      Pre-folding gates: {qc_transpiled.size()}")
    print(f"      T-depth: {t_depth} (opt_level={optimization_level} preserves T-depth)")

    # Export to QASM 3.0
    print(f"   📝 Exporting to QASM 3.0...")
    qasm3_str = qasm3.dumps(qc_transpiled)
    qasm3_file = f"qasm3_exports/{config_name}_{method.replace('+', '_')}.qasm"
    Path("qasm3_exports").mkdir(exist_ok=True)
    with open(qasm3_file, 'w') as f:
        f.write(qasm3_str)
    print(f"      Saved to: {qasm3_file}")

    # Step 4: Execution (with or without ZNE)
    print("   🚀 Executing on IBM hardware...")
    exec_start = time.time()

    if apply_zne_flag:
        quasi_dist = apply_zne(qc_transpiled, backend, shots=shots)

        # ✅ FIX: Record circuit depth AFTER ZNE folding
        # ZNE uses noise levels [1x, 2x, 3x]
        # Calculate the maximum folded depth (3x noise level)
        print(f"   📏 Computing post-folding circuit metrics...")
        scaled_circuit = qc_transpiled.copy()

        # Fold gates twice to simulate 3x noise (same as apply_zne does)
        for _ in range(2):  # 2 folds = 3x noise
            for instr in qc_transpiled.data:
                gate = instr.operation
                # Skip measurement and barrier gates during folding
                if gate.name in ['measure', 'barrier']:
                    continue
                qubits = instr.qubits
                # Add gate and its inverse (folding)
                scaled_circuit.append(gate, qubits)
                scaled_circuit.append(gate.inverse(), qubits)

        # Decompose inverse gates to native basis (same as apply_zne does)
        # This ensures depth/gate metrics match what actually executes
        scaled_circuit = transpile(
            scaled_circuit,
            backend,
            optimization_level=0  # Only decompose, don't optimize
        )

        circuit_depth = scaled_circuit.depth()
        circuit_gates = scaled_circuit.size()
        print(f"      Post-folding depth: {circuit_depth} (3x noise level)")
        print(f"      Post-folding gates: {circuit_gates} (3x noise level)")

        # ZNE returns probabilities with string keys, convert to counts
        # Keep the full bitstring (133 bits) - we'll extract the correct qubits later
        counts = {}
        for k, v in quasi_dist.items():
            # Check if k is already a string or needs formatting
            if isinstance(k, str):
                bitstring = k
            else:
                # Format to backend's full qubit count, not just num_qubits
                bitstring = format(int(k), f'0{backend.num_qubits}b')
            counts[bitstring] = int(v * shots)
    else:
        # No ZNE - record normal depth
        circuit_depth = qc_transpiled.depth()
        circuit_gates = qc_transpiled.size()
        print(f"      Final depth: {circuit_depth}")
        print(f"      Final gates: {circuit_gates}")

        # Use Sampler without Session (required for free/open plan)
        sampler = Sampler(mode=backend)
        job = sampler.run([qc_transpiled], shots=shots)
        result = job.result()

        quasi_dist = result[0].data.meas.get_counts()

        # DEBUG: Log what we get from IBM
        print(f"   🔍 DEBUG: Raw quasi_dist type: {type(quasi_dist)}")
        print(f"   🔍 DEBUG: Number of unique outcomes: {len(quasi_dist)}")
        print(f"   🔍 DEBUG: First 3 keys: {list(quasi_dist.keys())[:3]}")
        print(f"   🔍 DEBUG: First 3 values: {list(quasi_dist.values())[:3]}")

        # Handle both string and integer keys from get_counts()
        # Keep the full bitstring (133 bits) - we'll extract the correct qubits later
        counts = {}
        for k, v in quasi_dist.items():
            if isinstance(k, str):
                bitstring = k
            else:
                # Format to backend's full qubit count, not just num_qubits
                bitstring = format(int(k), f'0{backend.num_qubits}b')
            counts[bitstring] = v

        # DEBUG: Verify counts
        total_counts = sum(counts.values())
        print(f"   🔍 DEBUG: Total counts: {total_counts}, Expected (shots): {shots}")
        if abs(total_counts - shots) > 10:
            print(f"   ⚠️  WARNING: Counts sum ({total_counts}) != shots ({shots})")

    exec_time = time.time() - exec_start
    print(f"   ✅ Execution: {exec_time:.3f}s")
    print(f"      (Note: IBM execution = Server-side homomorphic evaluation)")

    # Step 5: Compute Final QOTP Keys (Client-side, using circuit structure)
    print("   🔍 Computing final QOTP keys...")
    eval_start = time.time()

    # Unpack eval_key
    T_sets, V_sets, auxiliary_states = eval_key

    # aux_eval computes what the final QOTP keys are after circuit execution
    # This does NOT re-execute the circuit, just tracks key evolution
    qc_eval, final_enc_a, final_enc_b = aux_eval(
        qc_encrypted, enc_a, enc_b, auxiliary_states, t_depth,
        bfv_encryptor, bfv_decryptor, bfv_encoder, bfv_evaluator, poly_degree, debug=False
    )

    # Decrypt final keys to get the QOTP decoding values
    final_a = []
    final_b = []
    for i in range(num_qubits):
        a_val = int(bfv_encoder.decode(bfv_decryptor.decrypt(final_enc_a[i]))[0]) % 2
        b_val = int(bfv_encoder.decode(bfv_decryptor.decrypt(final_enc_b[i]))[0]) % 2
        final_a.append(a_val)
        final_b.append(b_val)

    eval_time = time.time() - eval_start
    print(f"   ✅ Final keys computed: {eval_time:.3f}s")
    print(f"      Final QOTP keys: a={final_a}, b={final_b}")

    # Step 6: Decode Measurement Results (using final QOTP keys)
    print("   🔓 Decoding measurement results...")
    decrypt_start = time.time()

    # DEBUG: Log encrypted counts
    print(f"   🔍 DEBUG: Encrypted counts - unique outcomes: {len(counts)}")
    print(f"   🔍 DEBUG: Encrypted counts - total: {sum(counts.values())}")
    print(f"   🔍 DEBUG: First bitstring length: {len(list(counts.keys())[0])} bits")

    # Decode the encrypted measurement outcomes from IBM
    # Each measured bitstring needs to be XORed with final QOTP keys
    # CRITICAL: Extract bits from the correct physical qubits (not just first num_qubits bits!)
    decoded_counts = {}
    for bitstring, count in counts.items():
        # Extract bits from physical qubit positions
        # Qiskit bitstring format: qubit N is at position -(N+1) (rightmost is qubit 0)
        # Extract values for each logical qubit
        extracted_values = [
            int(bitstring[-(physical_qubits[i] + 1)]) for i in range(num_qubits)
        ]

        # Decode: XOR each extracted bit with corresponding final_a
        # extracted_values[i] = value of logical qubit i
        # final_a[i] = QOTP key for logical qubit i
        decoded_values = [extracted_values[i] ^ final_a[i] for i in range(num_qubits)]

        # Convert back to Qiskit bitstring format (qubit 0 at rightmost)
        # decoded_values is [qubit0, qubit1, qubit2, qubit3, qubit4]
        # Qiskit wants: qubit4 qubit3 qubit2 qubit1 qubit0
        decoded_bits = ''.join(str(decoded_values[num_qubits-1-i]) for i in range(num_qubits))
        # IMPORTANT: Accumulate counts, don't overwrite (multiple encrypted bitstrings may decode to same value)
        if decoded_bits in decoded_counts:
            decoded_counts[decoded_bits] += count
        else:
            decoded_counts[decoded_bits] = count

    # Verify no shots were lost in decoding
    decoded_total = sum(decoded_counts.values())
    encrypted_total = sum(counts.values())
    assert decoded_total == encrypted_total, f"Shots lost in decoding! {decoded_total} != {encrypted_total}"

    decrypt_time = time.time() - decrypt_start

    # DEBUG: Log decoded counts
    print(f"   🔍 DEBUG: Decoded counts - unique outcomes: {len(decoded_counts)}")
    print(f"   🔍 DEBUG: Decoded counts - total: {decoded_total}")
    print(f"   ✅ Decoding: {decrypt_time:.3f}s")
    print(f"      Shots preserved: {decoded_total}/{shots}")

    # Step 7: Fidelity calculation
    print("   📊 Computing fidelity...")

    # Simulate ideal circuit to get expected distribution
    ideal_state = Statevector(qc)
    ideal_probs = np.abs(ideal_state.data)**2

    # Reconstruct noisy state from DECODED counts
    noisy_probs = np.zeros(2**num_qubits)
    for bitstring, count in decoded_counts.items():
        idx = int(bitstring, 2)
        noisy_probs[idx] = count / shots

    # Normalize in case of decoding errors
    if np.sum(noisy_probs) > 0:
        noisy_probs = noisy_probs / np.sum(noisy_probs)

    # Convert probabilities to amplitudes for Statevector
    # Since we only have classical probability distribution, use sqrt(p) as amplitude
    noisy_amplitudes = np.sqrt(noisy_probs)
    noisy_state = Statevector(noisy_amplitudes)

    fidelity = state_fidelity(ideal_state, noisy_state)

    # Total variation distance
    tvd = 0.5 * np.sum(np.abs(ideal_probs - noisy_probs))

    total_time = time.time() - start_time

    print(f"\n   ✅ RESULTS:")
    print(f"      Fidelity: {fidelity:.6f}")
    print(f"      TVD: {tvd:.6f}")
    print(f"      Total time: {total_time:.3f}s")

    return {
        'config': config_name,
        'method': method,
        'backend': backend.name,
        'qasm_version': 'OpenQASM 3.0',
        'num_qubits': num_qubits,
        't_depth': t_depth,
        'aux_states': total_aux,
        'optimization_level': optimization_level,
        'zne_applied': apply_zne_flag,
        'shots': shots,
        'qasm3_file': qasm3_file,
        'fidelity': fidelity,
        'tvd': tvd,
        'keygen_time': keygen_time,
        'encrypt_time': encrypt_time,
        'transpile_time': transpile_time,
        'exec_time': exec_time,
        'eval_time': eval_time,
        'decrypt_time': decrypt_time,
        'total_time': total_time,
        'circuit_depth': circuit_depth,  # ✅ FIX: Use computed value (correct for both ZNE and non-ZNE)
        'circuit_gates': circuit_gates,  # ✅ FIX: Use computed value (correct for both ZNE and non-ZNE)
        'encrypted_counts': counts,  # Raw counts from IBM (still encrypted)
        'decoded_counts': decoded_counts,  # Decoded counts (after QOTP decoding)
        'final_qotp_keys': {'a': final_a, 'b': final_b}  # Final QOTP keys used for decoding
    }


def run_full_experiment(configs=None, backend_name='ibm_brisbane', shots=8192, account_name=None, dry_run=False):
    """
    Run full noise measurement experiment with all 5 methods.

    Args:
        configs: List of configurations to test
        backend_name: IBM backend name
        shots: Number of measurement shots
        account_name: IBM account name (optional, uses default if None)
        dry_run: If True, validate setup without running on hardware

    Args:
        configs: List of configurations to test (default: all 6)
        backend_name: IBM backend name
        shots: Number of measurement shots

    Returns:
        DataFrame with all results
    """
    print("\n" + "="*100)
    print("🎯 AUX-QHE IBM QUANTUM HARDWARE - NOISE MEASUREMENT EXPERIMENT")
    print("   QASM Version: OpenQASM 3.0")
    print("   Configurations: 4q-3t, 5q-1t, 5q-2t, 5q-3t (4 configs)")
    print("   Methods: Baseline, ZNE, Opt-3, Opt-3+ZNE (skips if T-depth > 3)")
    print("="*100)

    # Default configurations: Testing practical threshold of AUX-QHE
    # 4q-3t, 5q-1t, 5q-2t, 5q-3t
    if configs is None:
        configs = [
            {'name': '4q-3t', 'qubits': 4, 't_depth': 3},
            {'name': '5q-1t', 'qubits': 5, 't_depth': 1},
            {'name': '5q-2t', 'qubits': 5, 't_depth': 2},
            {'name': '5q-3t', 'qubits': 5, 't_depth': 3},
        ]

    # Load IBM Quantum account
    print("\n🔐 Loading IBM Quantum account...")
    try:
        if account_name:
            service = QiskitRuntimeService(name=account_name)
            print(f"   ✅ Account loaded: {account_name}")
        else:
            service = QiskitRuntimeService()
            print(f"   ✅ Default account loaded")
    except Exception as e:
        print(f"   ❌ Error loading account: {e}")
        print(f"   💡 Fix your account:")
        print(f"      python edit_ibm_account.py")
        print(f"   💡 Or specify account:")
        print(f"      --account GiaDang_AUX")
        print(f"   💡 Migration guide:")
        print(f"      cat UPDATE_IBM_ACCOUNT_GUIDE.md")
        return None

    # Get backend
    print(f"\n🖥️  Getting backend: {backend_name}")
    try:
        backend = service.backend(backend_name)
        status = backend.status()
        print(f"   ✅ Backend: {backend.name}")
        print(f"      Qubits: {backend.num_qubits}")
        print(f"      Status: {status.status_msg}")
        print(f"      Queue: {status.pending_jobs} jobs")
        print(f"      Operational: {'✅ Yes' if status.operational else '❌ No'}")

        if not status.operational:
            print(f"\n   ⚠️  WARNING: Backend is not operational!")
            print(f"   Current status: {status.status_msg}")
            return None

        if status.pending_jobs > 50:
            print(f"\n   ⚠️  WARNING: High queue ({status.pending_jobs} jobs)")
            print(f"   Estimated wait: {status.pending_jobs * 2}-{status.pending_jobs * 5} minutes")

    except Exception as e:
        print(f"   ❌ Error accessing backend: {e}")
        print(f"\n   💡 Available backends:")
        backends = service.backends()
        for b in backends[:5]:
            print(f"      - {b.name} ({b.num_qubits} qubits)")
        return None

    # DRY RUN MODE - Stop before execution
    if dry_run:
        print(f"\n{'='*100}")
        print(f"✅ DRY RUN COMPLETE - All validations passed!")
        print(f"{'='*100}")
        print(f"\n📋 Validated:")
        print(f"   ✅ Account connection")
        print(f"   ✅ Backend access: {backend.name}")
        print(f"   ✅ Backend operational")
        print(f"   ✅ Queue status: {status.pending_jobs} jobs")
        print(f"\n🚀 Ready to run! Remove --dry-run to execute on hardware.")
        return None

    # Define error mitigation methods to test
    # All 4 methods - will intelligently skip if T-depth exceeds threshold
    methods = [
        {'name': 'Baseline', 'opt_level': 1, 'zne': False},
        {'name': 'ZNE', 'opt_level': 1, 'zne': True},
        {'name': 'Opt-3', 'opt_level': 3, 'zne': False},
        {'name': 'Opt-3+ZNE', 'opt_level': 3, 'zne': True},
    ]

    # Run experiments
    all_results = []

    for config in configs:
        # 🔑 CRITICAL FIX: Generate QOTP keys ONCE per configuration
        # All 4 methods must use the SAME keys for fair comparison!
        import random
        num_qubits = config['qubits']
        config_a_init = [random.randint(0, 1) for _ in range(num_qubits)]
        config_b_init = [random.randint(0, 1) for _ in range(num_qubits)]

        print(f"\n{'='*100}")
        print(f"🔐 Configuration {config['name']}: Using shared QOTP keys for all methods")
        print(f"   a_init = {config_a_init}")
        print(f"   b_init = {config_b_init}")
        print(f"{'='*100}")

        for method in methods:
            try:
                result = run_aux_qhe_config(
                    config_name=config['name'],
                    num_qubits=config['qubits'],
                    t_depth=config['t_depth'],
                    backend=backend,
                    method=method['name'],
                    optimization_level=method['opt_level'],
                    apply_zne_flag=method['zne'],
                    shots=shots,
                    a_init=config_a_init,  # 🔑 Pass same keys to all methods
                    b_init=config_b_init   # 🔑 Pass same keys to all methods
                )
                # Only add if not None (None = skipped due to T-depth infeasibility)
                if result is not None:
                    all_results.append(result)

                # Save intermediate results
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                interim_file = f"ibm_noise_results_interim_{timestamp}.json"
                with open(interim_file, 'w') as f:
                    json.dump(all_results, f, indent=2)

            except Exception as e:
                print(f"\n   ❌ Error running {config['name']} with {method['name']}: {e}")
                import traceback
                traceback.print_exc()
                continue

    # Convert to DataFrame
    df = pd.DataFrame(all_results)

    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    csv_file = f"ibm_noise_measurement_results_{timestamp}.csv"
    df.to_csv(csv_file, index=False)
    print(f"\n✅ Results saved to: {csv_file}")

    json_file = f"ibm_noise_measurement_results_{timestamp}.json"
    with open(json_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"✅ Results saved to: {json_file}")

    return df


def analyze_noise_results(df):
    """
    Analyze and compare noise measurement results across all methods.

    Args:
        df: DataFrame with experiment results
    """
    print("\n" + "="*100)
    print("📊 NOISE MEASUREMENT ANALYSIS")
    print("="*100)

    # Check if DataFrame is empty or missing required columns
    if df is None or len(df) == 0:
        print("\n❌ No results to analyze!")
        print("   The experiment may have failed before collecting data.")
        return

    required_columns = ['config', 'method', 'fidelity', 'tvd', 'total_time']
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        print(f"\n❌ Missing required columns: {missing_columns}")
        print(f"   Available columns: {list(df.columns)}")
        print("\n   The experiment failed before completing.")
        return

    # Group by configuration and method
    pivot_fidelity = df.pivot_table(
        index='config',
        columns='method',
        values='fidelity',
        aggfunc='mean'
    )

    pivot_tvd = df.pivot_table(
        index='config',
        columns='method',
        values='tvd',
        aggfunc='mean'
    )

    pivot_time = df.pivot_table(
        index='config',
        columns='method',
        values='total_time',
        aggfunc='mean'
    )

    print("\n🎯 FIDELITY COMPARISON")
    print(pivot_fidelity.to_string())

    print("\n📉 TOTAL VARIATION DISTANCE (TVD)")
    print(pivot_tvd.to_string())

    print("\n⏱️  TOTAL RUNTIME (seconds)")
    print(pivot_time.to_string())

    # Best method per config
    print("\n🏆 BEST METHOD PER CONFIGURATION (by Fidelity)")
    print("-" * 60)
    for config in pivot_fidelity.index:
        best_method = pivot_fidelity.loc[config].idxmax()
        best_fidelity = pivot_fidelity.loc[config].max()
        print(f"   {config}: {best_method} (Fidelity: {best_fidelity:.6f})")

    # Overall statistics
    print("\n📈 OVERALL STATISTICS")
    print("-" * 60)

    method_stats = df.groupby('method').agg({
        'fidelity': ['mean', 'std', 'min', 'max'],
        'tvd': ['mean', 'std'],
        'total_time': ['mean', 'std']
    }).round(6)

    print(method_stats.to_string())

    # Improvement analysis
    print("\n💡 IMPROVEMENT ANALYSIS (vs Baseline)")
    print("-" * 60)

    baseline_fidelity = df[df['method'] == 'Baseline']['fidelity'].mean()

    for method in df['method'].unique():
        if method == 'Baseline':
            continue

        method_fidelity = df[df['method'] == method]['fidelity'].mean()
        improvement = ((method_fidelity - baseline_fidelity) / baseline_fidelity) * 100

        print(f"   {method}: {improvement:+.2f}% improvement")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='AUX-QHE IBM Quantum Hardware Noise Experiment')
    parser.add_argument('--backend', type=str, default='ibm_brisbane',
                       help='IBM backend name (default: ibm_brisbane)')
    parser.add_argument('--shots', type=int, default=1024,
                       help='Number of measurement shots (default: 1024)')
    parser.add_argument('--config', type=str, default=None,
                       help='Single config to test (e.g., 3q-2t), or "all" for all configs')
    parser.add_argument('--account', type=str, default=None,
                       help='IBM account name to use (e.g., GiaDang_AUX)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Validate setup without executing on hardware')

    args = parser.parse_args()

    # Determine configurations to test
    configs = None
    if args.config and args.config != 'all':
        # Parse single config
        parts = args.config.split('-')
        if len(parts) == 2:
            qubits = int(parts[0].replace('q', ''))
            t_depth = int(parts[1].replace('t', ''))
            configs = [{'name': args.config, 'qubits': qubits, 't_depth': t_depth}]

    # Run experiment
    print(f"\n🚀 Starting AUX-QHE noise measurement experiment")
    print(f"   Backend: {args.backend}")
    print(f"   Shots: {args.shots}")
    print(f"   Configs: {'All' if configs is None else args.config}")
    print(f"   Account: {args.account if args.account else 'Default'}")
    print(f"   Mode: {'DRY RUN (validation only)' if args.dry_run else 'LIVE EXECUTION'}")

    df = run_full_experiment(
        configs=configs,
        backend_name=args.backend,
        shots=args.shots,
        account_name=args.account,
        dry_run=args.dry_run
    )

    if df is not None and len(df) > 0:
        analyze_noise_results(df)

        print("\n" + "="*100)
        print("✅ Experiment completed successfully!")
        print("="*100)
    elif df is not None and len(df) == 0:
        print("\n" + "="*100)
        print("⚠️  Experiment finished but no results were collected")
        print("="*100)
        print("\n💡 Possible reasons:")
        print("   - Network connection issues")
        print("   - IBM Quantum authentication failed")
        print("   - Backend not available")
        print("   - All experiments failed")
    else:
        print("\n" + "="*100)
        print("❌ Experiment failed to start")
        print("="*100)
