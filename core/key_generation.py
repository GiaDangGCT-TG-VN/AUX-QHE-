"""
AUX-QHE Key Generation Module

This module implements the key generation phase of the AUX-QHE scheme,
corrected according to the theoretical pseudocode specification.
"""

import logging
import time
import random
import numpy as np
from qiskit import QuantumCircuit
from qiskit.qasm3 import dumps
from bfv_core import initialize_bfv_params

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class KeyPolynomial:
    """Structure for key polynomials with variables and terms."""
    def __init__(self):
        self.variables = set()
        self.terms = []  # Linear combination of monomials

class AuxiliaryState:
    """Structure for auxiliary states |+_{s,k}⟩ = Z^k P^s |+⟩."""
    def __init__(self, circuit, s_value, k_value, index):
        self.circuit = circuit
        self.s_value = s_value  # s parameter from theory
        self.k_value = k_value  # k parameter from theory
        self.index = index      # (layer, wire, term)

def build_term_sets(num_qubits, max_T_depth):
    """
    Build term sets T[ℓ] for each T-layer according to theory.
    
    Theory:
    T[1] ← {a₁, ..., aₙ, b₁, ..., bₙ}
    For ℓ = 2 to L:
        For each pair (t, t') in T[ℓ-1] where t ≠ t':
            T[ℓ] ← T[ℓ] ∪ {t·t'}
    
    Args:
        num_qubits (int): Number of qubits n.
        max_T_depth (int): Maximum T-depth L.
    
    Returns:
        dict: T[ℓ] term sets for each layer.
    """
    T = {}
    V = {}  # Variable sets for each layer
    
    # Layer 1: Base variables {a₁, ..., aₙ, b₁, ..., bₙ}
    T[1] = []
    V[1] = set()
    
    for i in range(num_qubits):
        a_var = f"a{i}"
        b_var = f"b{i}"
        T[1].extend([a_var, b_var])
        V[1].update([a_var, b_var])
    
    logger.info(f"T[1] = {T[1]} (size: {len(T[1])})")
    
    # Layers 2 to L: Add cross-products of all previous terms
    for ell in range(2, max_T_depth + 1):
        T[ell] = T[ell-1].copy()  # Inherit previous layer
        V[ell] = V[ell-1].copy()

        # Add products t·t' for all pairs (t, t') in T[ℓ-1] where t ≠ t'
        prev_terms = T[ell-1]
        new_cross_terms = []

        for i in range(len(prev_terms)):
            for j in range(i+1, len(prev_terms)):
                t1, t2 = prev_terms[i], prev_terms[j]
                if t1 != t2:  # Ensure t ≠ t'
                    cross_term = f"({t1})*({t2})"
                    new_cross_terms.append(cross_term)

        T[ell].extend(new_cross_terms)

        # Add new key variables for this layer (from previous layer evaluation)
        for i in range(num_qubits):
            for j in range(len(T[ell-1])):
                new_var = f"k{i}_{j}_L{ell-1}"
                T[ell].append(new_var)
                V[ell].add(new_var)

        logger.info(f"T[{ell}] size: {len(T[ell])} (added {len(new_cross_terms)} cross-terms, {num_qubits * len(T[ell-1])} new k-vars)")
        if ell <= 3:  # Log first few layers for debugging
            logger.debug(f"T[{ell}] = {T[ell][:10]}{'...' if len(T[ell]) > 10 else ''}")
    
    return T, V

def evaluate_term(term, variable_values):
    """
    Evaluate a polynomial term using variable values.

    Args:
        term (str): Term like "a0", "b1", "(a0)*(b1)", "a1 + b0", etc.
        variable_values (dict): Mapping from variable names to binary values.

    Returns:
        int: Evaluated result (0 or 1).
    """
    # Clean up malformed terms
    if isinstance(term, str):
        term = term.strip()
        # Fix malformed patterns like "1)" by removing trailing parentheses
        if term.endswith(')') and not term.startswith('(') and '(' not in term[:-1]:
            logger.debug(f"Fixing malformed term: {term} -> {term[:-1]}")
            term = term[:-1]

    # Handle simple variables
    if term in variable_values:
        return variable_values[term]
    
    # Handle addition operations like "a1 + b0" or "b0 + a0 + b1"
    if "+" in term:
        # Split by + and evaluate each term
        addends = [t.strip() for t in term.split("+")]
        result = 0
        for addend in addends:
            # Recursively evaluate each addend
            if addend in variable_values:
                result += variable_values[addend]
            elif addend.startswith("k") and "_" in addend:
                # Handle k-variables
                if addend in variable_values:
                    result += variable_values[addend]
                else:
                    logger.debug(f"Unknown k-variable in addition: {addend}, defaulting to 0")
                    # Don't add anything (equivalent to adding 0)
            elif addend.isdigit():
                # Handle numeric constants
                result += int(addend)
            else:
                # Try to recursively evaluate complex addends
                try:
                    result += evaluate_term(addend, variable_values)
                except:
                    logger.debug(f"Could not evaluate addend '{addend}' in term '{term}', defaulting to 0")
                    # Don't add anything (equivalent to adding 0)
        
        return result % 2  # Binary arithmetic (mod 2)
    
    # Handle cross-products like "(a0)*(b1)", "(a0)*(b1)*(a1)", etc.
    if "*" in term and "(" in term:
        # Parse cross-products (supports any number of factors)
        term = term.replace("(", "").replace(")", "")
        factors = [f.strip() for f in term.split("*")]
        result = 1
        for factor in factors:
            if not factor:  # Skip empty factors
                continue
            if factor in variable_values:
                result *= variable_values[factor]
            elif factor.isdigit():
                result *= int(factor)
            else:
                # Unknown variable, try to evaluate recursively or default to 0
                try:
                    factor_val = evaluate_term(factor, variable_values)
                    result *= factor_val
                except:
                    logger.debug(f"Unknown variable in term evaluation: {factor}, defaulting to 0")
                    return 0
        return result % 2
    
    # Handle k-variables (auxiliary key variables)
    if term.startswith("k") and "_" in term:
        # These are auxiliary keys, should be in variable_values
        if term in variable_values:
            return variable_values[term]
        else:
            logger.debug(f"Unknown k-variable: {term}, defaulting to 0")
            return 0  # Default to 0 for unknown k-variables
    
    # Handle numeric constants
    if term.isdigit():
        return int(term) % 2
    
    # Handle empty or None terms
    if not term or term.strip() == '' or term == 'None':
        return 0
    
    logger.warning(f"Could not evaluate term: {term}")
    return 0

def prepare_auxiliary_state(s_value, k_value):
    """
    Prepare auxiliary state |+_{s,k}⟩ = Z^k P^s |+⟩.
    
    Theory: |+_{s,k}⟩ = Z^k P^s |+⟩ where P is a phase gate.
    
    Args:
        s_value (int): s parameter (0 or 1).
        k_value (int): k parameter (0 or 1).
    
    Returns:
        QuantumCircuit: Circuit preparing the auxiliary state.
    """
    qc = QuantumCircuit(1, name=f'aux_s{s_value}_k{k_value}')
    
    # Start with |+⟩ state
    qc.h(0)
    
    # Apply P^s (phase gate s times)
    if s_value == 1:
        qc.p(np.pi/2, 0)  # P = e^{iπ/4} phase gate
    
    # Apply Z^k (Z gate k times)
    if k_value == 1:
        qc.z(0)
    
    return qc

def aux_keygen(num_qubits, max_T_depth, a_init=None, b_init=None):
    """
    Generate keys and auxiliary states for AUX-QHE scheme (corrected version).

    Args:
        num_qubits (int): Number of qubits n.
        max_T_depth (int): Maximum T-depth L.
        a_init (list, optional): Initial QOTP X-keys (if None, random).
        b_init (list, optional): Initial QOTP Z-keys (if None, random).

    Returns:
        tuple: (secret_key, eval_key, aux_prep_time, layer_sizes, total_aux_states)
            - secret_key: (a_init, b_init, k_dict)
            - eval_key: (T_sets, V_sets, auxiliary_states)
            - aux_prep_time: Time taken for preparation.
            - layer_sizes: List of |T_ell| for each layer.
            - total_aux_states: Total number of auxiliary states.
    """
    try:
        # Use current random state (set by caller) for deterministic auxiliary key generation
        # Don't override the seed here as it should be set by the caller

        aux_prep_start = time.perf_counter()

        # Generate QOTP keys if not provided
        if a_init is None:
            a_init = [random.randint(0, 1) for _ in range(num_qubits)]
        if b_init is None:
            b_init = [random.randint(0, 1) for _ in range(num_qubits)]

        logger.info(f"QOTP keys: a={a_init}, b={b_init}")

        # Build term sets T[ℓ] according to theory
        T_sets, V_sets = build_term_sets(num_qubits, max_T_depth)
        layer_sizes = [len(T_sets[ell]) for ell in range(1, max_T_depth + 1)]

        # Initialize variable values for term evaluation
        variable_values = {}
        for i in range(num_qubits):
            variable_values[f"a{i}"] = a_init[i]
            variable_values[f"b{i}"] = b_init[i]

        # Create deterministic pseudorandom generator for auxiliary states
        # Use configuration-specific hash to ensure deterministic but unique values
        import hashlib
        config_hash = f"{num_qubits}_{max_T_depth}_{tuple(a_init)}_{tuple(b_init)}"
        hash_bytes = hashlib.md5(config_hash.encode()).digest()

        # Pre-generate k-values for all layers deterministically
        k_values_dict = {}  # Maps k-variable names to their deterministic values
        for ell in range(1, max_T_depth + 1):
            for i in range(num_qubits):
                if ell > 1:  # k-variables only exist for layers > 1
                    prev_layer_size = len(T_sets[ell-1])
                    for j in range(prev_layer_size):
                        k_var_name = f"k{i}_{j}_L{ell-1}"
                        # Use hash-based deterministic value
                        var_hash = f"{config_hash}_{k_var_name}"
                        var_bytes = hashlib.md5(var_hash.encode()).digest()
                        k_values_dict[k_var_name] = var_bytes[0] % 2
                        variable_values[k_var_name] = k_values_dict[k_var_name]

        logger.debug(f"Pre-generated {len(k_values_dict)} k-variables deterministically")

        # Generate auxiliary states for each layer, wire, and term
        auxiliary_states = {}
        k_dict = {}  # Store k values for secret key
        total_aux_states = 0

        for ell in range(1, max_T_depth + 1):
            for wire in range(num_qubits):
                for term_idx, term in enumerate(T_sets[ell]):
                    # Generate deterministic k value for this auxiliary state
                    # CRITICAL: k should only depend on (layer, wire, term)
                    # NOT on num_qubits or initial keys - k is an independent auxiliary secret
                    k_hash = f"aux_{ell}_{wire}_{term}"
                    k_bytes = hashlib.md5(k_hash.encode()).digest()
                    k_value = k_bytes[0] % 2

                    # Evaluate s value using current variable assignments
                    s_value = evaluate_term(term, variable_values)

                    # Prepare auxiliary state |+_{s,k}⟩
                    aux_circuit = prepare_auxiliary_state(s_value, k_value)

                    # CRITICAL FIX: Index by (layer, wire, term_string) instead of term_idx
                    # This allows proper lookup by polynomial term
                    index = (ell, wire, term)  # Use term string, not index
                    aux_state = AuxiliaryState(aux_circuit, s_value, k_value, index)
                    auxiliary_states[index] = aux_state

                    # Store k value in secret key
                    k_dict[(ell, wire, term)] = k_value
                    total_aux_states += 1

                    logger.debug(f"Layer {ell}, wire {wire}, term '{term}': s={s_value}, k={k_value}")
        
        aux_prep_time = time.perf_counter() - aux_prep_start
        
        # Prepare secret and evaluation keys
        secret_key = (a_init, b_init, k_dict)
        eval_key = (T_sets, V_sets, auxiliary_states)
        
        logger.info(f"AUX key generation completed:")
        logger.info(f"  - Total auxiliary states: {total_aux_states}")
        logger.info(f"  - Layer sizes: {layer_sizes}")
        logger.info(f"  - Preparation time: {aux_prep_time:.4f}s")
        
        return secret_key, eval_key, aux_prep_time, layer_sizes, total_aux_states

    except Exception as e:
        logger.error(f"AUX key generation failed: {str(e)}")
        raise

def export_aux_keys_to_qasm3(secret_key, eval_key, num_qubits, max_t_depth):
    """
    Export AUX-QHE keys and auxiliary states to OpenQASM 3 format.

    Args:
        secret_key: Secret key tuple (a_init, b_init, k_dict)
        eval_key: Evaluation key tuple (T_sets, V_sets, auxiliary_states)
        num_qubits (int): Number of qubits
        max_t_depth (int): Maximum T-depth

    Returns:
        str: OpenQASM 3 representation of keys and auxiliary states
    """
    try:
        a_init, b_init, k_dict = secret_key
        T_sets, V_sets, auxiliary_states = eval_key

        qasm3_export = f"""
// OpenQASM 3 Export of AUX-QHE Keys and Auxiliary States
// Generated from AUX-QHE key generation module
// Qubits: {num_qubits}, Max T-depth: {max_t_depth}

OPENQASM 3.0;
include "stdgates.inc";

// Classical key data
const int num_qubits = {num_qubits};
const int max_t_depth = {max_t_depth};

// Initial QOTP keys
bit[{num_qubits}] a_init = "{''.join(map(str, a_init))}";
bit[{num_qubits}] b_init = "{''.join(map(str, b_init))}";

// Auxiliary state parameters
const int total_aux_states = {len(k_dict)};

// T-set cross-terms by layer
"""

        # Add T-sets data
        for layer, terms in T_sets.items():
            cross_terms = [term for term in terms if '*' in term]
            qasm3_export += f"""
// Layer {layer}: {len(terms)} total terms, {len(cross_terms)} cross-terms
const int layer_{layer}_size = {len(terms)};
const int layer_{layer}_cross_terms = {len(cross_terms)};
"""

        # Add auxiliary state definitions
        qasm3_export += f"""

// Auxiliary state definitions for each (layer, wire, term)
struct AuxiliaryState {{
    int layer;
    int wire;
    int s_value;
    int k_value;
}};

// Auxiliary state data
AuxiliaryState[{len(k_dict)}] aux_states = {{"""

        for i, ((layer, wire, term), k_value) in enumerate(k_dict.items()):
            s_value = 0  # Default s value
            qasm3_export += f"""
    {{.layer = {layer}, .wire = {wire}, .s_value = {s_value}, .k_value = {k_value}}}"""
            if i < len(k_dict) - 1:
                qasm3_export += ","

        qasm3_export += """
};

// Function to retrieve auxiliary state for given (layer, wire, term)
def get_aux_state(int layer, int wire) -> AuxiliaryState {
    for int i in [0:total_aux_states-1] {
        if (aux_states[i].layer == layer && aux_states[i].wire == wire) {
            return aux_states[i];
        }
    }
    // Default auxiliary state
    AuxiliaryState default_state = {.layer = 0, .wire = 0, .s_value = 0, .k_value = 0};
    return default_state;
}

// Function to apply auxiliary correction
def apply_aux_correction(qubit target, int layer, int wire) {
    AuxiliaryState aux = get_aux_state(layer, wire);

    // Apply P^s correction
    if (aux.s_value == 1) {
        z target;
    }

    // Apply Z^k correction
    if (aux.k_value == 1) {
        z target;
    }
}

// T-gate with auxiliary states
def aux_t_gate(qubit target, int layer, int wire) {
    // Apply T-gate
    t target;

    // Apply auxiliary correction
    apply_aux_correction(target, layer, wire);
}
"""

        logger.info(f"Exported AUX-QHE keys to OpenQASM 3 format")
        return qasm3_export

    except Exception as e:
        logger.error(f"Failed to export keys to OpenQASM 3: {e}")
        raise

if __name__ == "__main__":
    # Test key generation
    logger.info("Testing AUX key generation...")
    
    secret_key, eval_key, prep_time, layer_sizes, total_states = aux_keygen(
        num_qubits=3, 
        max_T_depth=2,
        a_init=[1, 0, 1],
        b_init=[0, 1, 0]
    )
    
    print(f"Secret key a: {secret_key[0]}")
    print(f"Secret key b: {secret_key[1]}")
    print(f"Number of k values: {len(secret_key[2])}")
    print(f"Layer sizes: {layer_sizes}")
    print(f"Total auxiliary states: {total_states}")
    print(f"Preparation time: {prep_time:.4f}s")