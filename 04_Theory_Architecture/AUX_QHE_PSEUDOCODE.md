# AUX-QHE Algorithm Pseudocode

**Corrected Implementation with Fixed Auxiliary Key Generation**

---

## 📋 Table of Contents

1. [Main Algorithm](#main-algorithm)
2. [Key Generation Phase](#key-generation-phase)
3. [Encryption Phase](#encryption-phase)
4. [Evaluation Phase](#evaluation-phase)
5. [Decryption Phase](#decryption-phase)
6. [Auxiliary Functions](#auxiliary-functions)

---

## Main Algorithm

```
Algorithm: AUX-QHE (Auxiliary-based Quantum Homomorphic Encryption)
Input:
  - Quantum circuit C with n qubits and T-depth L
  - Initial QOTP keys a_init, b_init ∈ {0,1}^n
Output:
  - Decrypted quantum state equivalent to C|0⟩

1. // Key Generation Phase
   (prep_key, eval_key, dec_key, stats) ← AUX_KEYGEN(n, L, a_init, b_init)

2. // Encryption Phase
   C_enc ← QOTP_ENCRYPT(C, a_init, b_init)

3. // Evaluation Phase
   C_eval ← AUX_EVAL(C_enc, eval_key)

4. // Decryption Phase
   C_dec ← QOTP_DECRYPT(C_eval, dec_key)

5. Return C_dec
```

---

## Key Generation Phase

### Algorithm: AUX_KEYGEN

```
Algorithm: AUX_KEYGEN(n, L, a_init, b_init)
Input:
  - n: number of qubits
  - L: T-depth of circuit
  - a_init, b_init: initial QOTP keys
Output:
  - prep_key: preparation key (initial a, b)
  - eval_key: evaluation key (T_sets, V_sets, auxiliary_states)
  - dec_key: decryption key (final a, b encrypted with BFV)
  - stats: key generation statistics

1. Initialize BFV parameters (poly_degree, plain_modulus)

2. // Build T-sets for each layer
   T_sets ← BUILD_T_SETS(n, L)

3. // Initialize variable values
   For i = 0 to n-1:
       variable_values[a_i] ← a_init[i]
       variable_values[b_i] ← b_init[i]

4. // Generate auxiliary states for each layer
   auxiliary_states ← {}
   For ℓ = 1 to L:
       For wire = 0 to n-1:
           For each term ∈ T_sets[ℓ]:
               // CRITICAL FIX: k-value depends only on (layer, wire, term)
               // NOT on num_qubits or circuit configuration
               k_hash ← HASH("aux", ℓ, wire, term)
               k_value ← k_hash mod 2

               // Evaluate s-value from term
               s_value ← EVALUATE_TERM(term, variable_values)

               // Create auxiliary state |+_{s,k}⟩
               aux_circuit ← PREPARE_AUX_STATE(s_value, k_value)

               // Store with index (layer, wire, term)
               index ← (ℓ, wire, term)
               auxiliary_states[index] ← AuxiliaryState(aux_circuit, s_value, k_value, index)

5. // Create evaluation key
   eval_key ← (T_sets, variable_values, auxiliary_states)

6. // Create preparation and decryption keys
   prep_key ← (a_init, b_init)
   dec_key ← (a_init, b_init)  // Will be updated after evaluation

7. Return (prep_key, eval_key, dec_key, stats)
```

### Algorithm: BUILD_T_SETS

```
Algorithm: BUILD_T_SETS(n, L)
Input:
  - n: number of qubits
  - L: T-depth
Output:
  - T_sets: dictionary mapping layer → set of terms

1. T_sets ← {}

2. // Layer 1: base terms
   T_sets[1] ← {a_0, b_0, a_1, b_1, ..., a_{n-1}, b_{n-1}}

3. // Layers 2 to L: add cross-terms
   For ℓ = 2 to L:
       T_sets[ℓ] ← T_sets[ℓ-1]  // Start with previous layer

       // Add cross-product terms
       For each (t, t') ∈ T_sets[ℓ-1] × T_sets[ℓ-1] where t ≠ t':
           cross_term ← t * t'  // GF(2) multiplication
           T_sets[ℓ] ← T_sets[ℓ] ∪ {cross_term}

       // Add k-variables for previous layer T-gates
       For i = 0 to n-1:
           k_var ← k_{i,ℓ-1}
           T_sets[ℓ] ← T_sets[ℓ] ∪ {k_var}

4. Return T_sets
```

---

## Encryption Phase

### Algorithm: QOTP_ENCRYPT

```
Algorithm: QOTP_ENCRYPT(C, a_keys, b_keys)
Input:
  - C: quantum circuit
  - a_keys, b_keys: QOTP keys
Output:
  - C_enc: encrypted circuit

1. Create new circuit C_enc with same number of qubits as C

2. // Apply QOTP encryption: X^a Z^b before circuit
   For i = 0 to num_qubits-1:
       If a_keys[i] = 1:
           C_enc.X(i)
       If b_keys[i] = 1:
           C_enc.Z(i)

3. // Append original circuit gates
   For each gate G in C:
       C_enc.append(G)

4. // Encrypt keys with BFV for homomorphic operations
   enc_a ← []
   enc_b ← []
   For i = 0 to num_qubits-1:
       enc_a[i] ← BFV_ENCRYPT(a_keys[i])
       enc_b[i] ← BFV_ENCRYPT(b_keys[i])

5. Return (C_enc, enc_a, enc_b)
```

---

## Evaluation Phase

### Algorithm: AUX_EVAL

```
Algorithm: AUX_EVAL(C_enc, eval_key)
Input:
  - C_enc: encrypted circuit
  - eval_key: (T_sets, variable_values, auxiliary_states)
Output:
  - C_eval: evaluated circuit
  - final_enc_a, final_enc_b: encrypted final keys

1. Unpack eval_key
   (T_sets, V_sets, auxiliary_states) ← eval_key

2. // Organize circuit into layers by gate type
   layers ← ORGANIZE_INTO_LAYERS(C_enc)

3. // Initialize polynomial tracking for QOTP keys
   For i = 0 to n-1:
       f_a[i] ← "a_{i}"  // Polynomial for X-key
       f_b[i] ← "b_{i}"  // Polynomial for Z-key

4. C_eval ← new QuantumCircuit(n)
   t_layer ← 1  // Current T-layer counter

5. // Process each layer
   For each layer in layers:
       gate_type ← layer.gate_type

       If gate_type = "init":
           // Copy initialization gates (QOTP encryption)
           For each gate in layer.gates:
               C_eval.append(gate)

       Else If gate_type = "clifford":
           // Process Clifford gates
           For each gate in layer.gates:
               UPDATE_KEYS_CLIFFORD(gate, f_a, f_b)
               C_eval.append(gate)

       Else If gate_type = "t":
           // Process T-gates with auxiliary gadgets
           For each gate in layer.gates:
               qubit ← gate.qubit
               (f_a[qubit], f_b[qubit]) ← UPDATE_KEYS_T_GATE(
                   qubit, f_a[qubit], f_b[qubit],
                   variable_values, auxiliary_states,
                   t_layer, C_eval
               )
           t_layer ← t_layer + 1

6. // Homomorphically evaluate final key polynomials
   final_enc_a ← []
   final_enc_b ← []
   For i = 0 to n-1:
       final_enc_a[i] ← EVAL_POLYNOMIAL_FHE(f_a[i], variable_values)
       final_enc_b[i] ← EVAL_POLYNOMIAL_FHE(f_b[i], variable_values)

7. Return (C_eval, final_enc_a, final_enc_b)
```

### Algorithm: UPDATE_KEYS_CLIFFORD

```
Algorithm: UPDATE_KEYS_CLIFFORD(gate, f_a, f_b)
Input:
  - gate: Clifford gate (H, CNOT, S, etc.)
  - f_a, f_b: current key polynomials
Output:
  - Updated f_a, f_b

1. gate_name ← gate.name

2. If gate_name = "H":
       // Hadamard swaps a and b
       i ← gate.qubit
       SWAP(f_a[i], f_b[i])

3. Else If gate_name = "CNOT":
       // CNOT(control, target)
       ctrl ← gate.control
       tgt ← gate.target
       f_a[tgt] ← f_a[tgt] ⊕ f_a[ctrl]  // XOR in GF(2)
       f_b[ctrl] ← f_b[ctrl] ⊕ f_b[tgt]

4. Else If gate_name = "S":
       // Phase gate S
       i ← gate.qubit
       f_b[i] ← f_b[i] ⊕ f_a[i]

5. Else If gate_name = "X":
       // Pauli X
       i ← gate.qubit
       f_b[i] ← f_b[i] ⊕ 1

6. Else If gate_name = "Z":
       // Pauli Z
       i ← gate.qubit
       f_a[i] ← f_a[i] ⊕ 1
```

### Algorithm: UPDATE_KEYS_T_GATE

```
Algorithm: UPDATE_KEYS_T_GATE(qubit, f_a_poly, f_b_poly,
                              variable_values, auxiliary_states,
                              t_layer, C_eval)
Input:
  - qubit: target qubit index
  - f_a_poly, f_b_poly: current key polynomials for this qubit
  - variable_values: current variable assignments
  - auxiliary_states: prepared auxiliary states
  - t_layer: current T-layer
  - C_eval: circuit being constructed
Output:
  - (new_f_a, new_f_b): updated key polynomials

1. // Get auxiliary state for current f_a polynomial
   index ← (t_layer, qubit, f_a_poly)
   aux_state ← auxiliary_states[index]
   k_value ← aux_state.k_value

2. // Apply T-gate to data circuit
   C_eval.T(qubit)

3. // Apply T-gadget to get measurement outcome c
   c ← APPLY_T_GADGET(C_eval, aux_state.circuit, k_value, qubit, f_a_poly)

4. // Generate variable names for this T-gate
   k_var_name ← "k_{qubit}_{t_layer}"
   c_var_name ← "c_{qubit}_{t_layer}"

5. // NOTE: Z^c correction is NOT applied as a gate
   // It's implicitly handled in the QOTP key update

6. // Update f_a: f_a' ← f_a ⊕ c
   If f_a_poly ≠ "0" and f_a_poly ≠ "":
       new_f_a ← f_a_poly + " + " + c_var_name
   Else:
       new_f_a ← c_var_name if c = 1 else "0"

   variable_values[c_var_name] ← c

7. // Update f_b: f_b' ← f_a ⊕ f_b ⊕ k ⊕ (c · f_a)
   new_f_b_parts ← []

   If f_a_poly ≠ "0":
       new_f_b_parts.append(f_a_poly)

   If f_b_poly ≠ "0":
       new_f_b_parts.append(f_b_poly)

   // Always add k variable
   new_f_b_parts.append(k_var_name)
   variable_values[k_var_name] ← k_value

   // Add cross-term (c · f_a) only if c = 1
   // CRITICAL: Since c is known (0 or 1), not a variable:
   // - If c = 1: cross-term = f_a, so add f_a terms directly
   // - If c = 0: cross-term = 0, so don't add anything
   If c = 1 and f_a_poly ≠ "0":
       // Split f_a into individual terms and add each
       f_a_terms ← SPLIT(f_a_poly, '+')
       For each term in f_a_terms:
           term ← TRIM(term)
           If term ≠ "" and term ≠ "0":
               new_f_b_parts.append(term)

   new_f_b ← JOIN(new_f_b_parts, " + ")

8. Return (new_f_a, new_f_b)
```

---

## Decryption Phase

### Algorithm: QOTP_DECRYPT

```
Algorithm: QOTP_DECRYPT(C_eval, final_enc_a, final_enc_b)
Input:
  - C_eval: evaluated circuit
  - final_enc_a, final_enc_b: BFV-encrypted final keys
Output:
  - C_dec: decrypted circuit

1. C_dec ← COPY(C_eval)

2. // Decrypt BFV-encrypted keys
   For i = 0 to num_qubits-1:
       a_val ← BFV_DECRYPT(final_enc_a[i]) mod 2
       b_val ← BFV_DECRYPT(final_enc_b[i]) mod 2

       // Apply QOTP decryption: Z^b then X^a
       // This reverses the encryption applied at the start

       If b_val = 1:
           C_dec.Z(i)

       If a_val = 1:
           C_dec.X(i)

3. Return C_dec
```

---

## Auxiliary Functions

### Algorithm: PREPARE_AUX_STATE

```
Algorithm: PREPARE_AUX_STATE(s_value, k_value)
Input:
  - s_value: evaluation of polynomial term
  - k_value: auxiliary secret key bit
Output:
  - aux_circuit: quantum circuit for |+_{s,k}⟩

1. aux_circuit ← QuantumCircuit(1)

2. // Prepare |+⟩ = H|0⟩
   aux_circuit.H(0)

3. // Apply P^s = Z^s
   If s_value = 1:
       aux_circuit.Z(0)

4. // Apply Z^k
   If k_value = 1:
       aux_circuit.Z(0)

5. Return aux_circuit
```

### Algorithm: APPLY_T_GADGET

```
Algorithm: APPLY_T_GADGET(data_circuit, aux_circuit, k_value, data_qubit, poly_hash)
Input:
  - data_circuit: main quantum circuit
  - aux_circuit: auxiliary circuit for |+_{s,k}⟩
  - k_value: auxiliary secret
  - data_qubit: target qubit
  - poly_hash: hash of polynomial for determinism
Output:
  - c: measurement outcome

1. // Simulate T-gadget measurement
   // In practice: prepare aux state, apply controlled operations, measure

2. // Deterministic measurement based on polynomial
   measurement_hash ← HASH(poly_hash, k_value)
   c ← measurement_hash mod 2

3. Return c
```

### Algorithm: EVALUATE_TERM

```
Algorithm: EVALUATE_TERM(term, variable_values)
Input:
  - term: polynomial term (string)
  - variable_values: variable assignments
Output:
  - value: evaluated result in GF(2)

1. If term is empty or "0":
       Return 0

2. If term is a single variable:
       Return variable_values[term] mod 2

3. If term contains '+':
       // XOR of sub-terms
       sub_terms ← SPLIT(term, '+')
       result ← 0
       For each sub_term in sub_terms:
           result ← result ⊕ EVALUATE_TERM(sub_term, variable_values)
       Return result mod 2

4. If term contains '*':
       // Product of factors (AND in GF(2))
       factors ← SPLIT(term, '*')
       result ← 1
       For each factor in factors:
           result ← result * EVALUATE_TERM(factor, variable_values)
       Return result mod 2

5. Return 0  // Unknown term
```

### Algorithm: ORGANIZE_INTO_LAYERS

```
Algorithm: ORGANIZE_INTO_LAYERS(circuit)
Input:
  - circuit: quantum circuit
Output:
  - layers: list of gate layers grouped by type

1. layers ← []
   current_layer ← new Layer("init")

2. For each gate in circuit.gates:
       gate_type ← CLASSIFY_GATE(gate)

       If gate_type ≠ current_layer.type:
           // Start new layer
           layers.append(current_layer)
           current_layer ← new Layer(gate_type)

       current_layer.gates.append(gate)

3. layers.append(current_layer)

4. Return layers
```

---

## 🔑 Key Theoretical Properties

### QOTP Key Evolution

For gate G on qubit i with current keys (a_i, b_i):

1. **Hadamard (H):**
   ```
   a'_i ← b_i
   b'_i ← a_i
   ```

2. **CNOT(ctrl=i, tgt=j):**
   ```
   a'_j ← a_j ⊕ a_i
   b'_i ← b_i ⊕ b_j
   ```

3. **T-gate:**
   ```
   a'_i ← a_i ⊕ c
   b'_i ← a_i ⊕ b_i ⊕ k ⊕ (c · a_i)
   ```
   where c is T-gadget measurement, k is auxiliary key

### Critical Fix (October 2025)

**Issue:** Auxiliary k-values were circuit-size dependent
```python
# WRONG (old implementation):
k_hash = f"{num_qubits}_{max_t_depth}_{term_idx}"

# CORRECT (fixed implementation):
k_hash = f"aux_{layer}_{wire}_{term}"
```

**Impact:** Same polynomial term now gets same k-value regardless of circuit size, ensuring consistent behavior across different configurations.

---

## 📊 Complexity Analysis

| Phase | Time Complexity | Space Complexity |
|-------|----------------|------------------|
| Key Generation | O(n · 2^L) | O(n · 2^L) |
| Encryption | O(m) | O(m) |
| Evaluation | O(m + n · T) | O(n · 2^L) |
| Decryption | O(m + n) | O(m) |

Where:
- n = number of qubits
- L = T-depth
- m = number of gates
- T = number of T-gates

**Dominant factor:** Auxiliary state preparation (exponential in T-depth)

---

**Last Updated:** October 6, 2025
**Implementation:** Corrected with circuit-size independent auxiliary key generation
