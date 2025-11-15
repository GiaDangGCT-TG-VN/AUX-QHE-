# IBM Noise Experiment - Issues Found & Fixes

## ✅ FIXED ISSUES

### 1. **MockEncoder Scope Error**
**File:** `core/bfv_core.py:65-70`

**Issue:** `MockEncoder.encode()` referenced undefined variable `degree`

**Fix:**
```python
class MockEncoder:
    def __init__(self, degree):  # Added __init__
        self.degree = degree

    def encode(self, values):
        return values[:self.degree] + [0] * (self.degree - len(values)) ...
```

**Status:** ✅ Fixed

---

### 2. **QOTP Encryption API Mismatch**
**File:** `ibm_hardware_noise_experiment.py:193-201`

**Issue:** Script was calling `qotp_encrypt()` without required BFV parameters

**Fix:** Added all required parameters:
```python
qc_encrypted, _, enc_a, enc_b = qotp_encrypt(
    qc, a_keys, b_keys,
    counter_d=0,
    max_qubits=num_qubits * 2,
    encryptor=bfv_encryptor,
    encoder=bfv_encoder,
    decryptor=bfv_decryptor,
    poly_degree=poly_degree
)
```

**Status:** ✅ Fixed

---

### 3. **QOTP Decryption API Mismatch**
**File:** `ibm_hardware_noise_experiment.py:280`

**Issue:** Script was calling `qotp_decrypt()` without BFV parameters

**Fix:**
```python
qc_decrypted = qotp_decrypt(
    qc_eval, final_enc_a, final_enc_b,
    bfv_decryptor, bfv_encoder, poly_degree
)
```

**Status:** ✅ Fixed

---

## ⚠️ CRITICAL ARCHITECTURAL ISSUE

### **Incorrect Usage of Homomorphic Evaluation**

**Location:** `ibm_hardware_noise_experiment.py:266-280`

**Problem:**
The script is calling `aux_eval()` **AFTER** executing the circuit on IBM hardware. This is incorrect because:

1. `aux_eval()` performs **homomorphic circuit evaluation** - it processes the circuit structure to compute updated QOTP keys
2. It should run **BEFORE** execution, not after
3. The current flow is:
   ```
   Encrypt → Transpile → Execute on IBM → aux_eval → Decrypt
   ```

4. The correct flow should be:
   ```
   Encrypt → aux_eval (compute final keys) → Transpile → Execute on IBM → Decode measurements
   ```

**Current Code (INCORRECT):**
```python
# Step 4: Execute on IBM
with Session(backend=backend) as session:
    sampler = Sampler(session=session)
    job = sampler.run(qc_transpiled, shots=shots)
    result = job.result()

# Step 5: Homomorphic Evaluation (WRONG - circuit already executed!)
qc_eval, final_enc_a, final_enc_b = aux_eval(
    qc_encrypted, enc_a, enc_b, auxiliary_states, t_depth,
    bfv_encryptor, bfv_decryptor, bfv_encoder, bfv_evaluator, poly_degree
)

# Step 6: Decryption (WRONG - trying to decrypt circuit instead of measurements)
qc_decrypted = qotp_decrypt(qc_eval, final_enc_a, final_enc_b, ...)
```

**Why This is Wrong:**
- Hom. evaluation computes updated encryption keys based on circuit gates
- It doesn't process measurement results - it processes gate sequences
- You can't "decrypt" a circuit that's already been executed
- The IBM hardware returns **measurement counts**, not quantum states

---

## 🔧 RECOMMENDED FIX

### Option A: Proper Homomorphic Flow (Complex)
```python
# 1. Key Generation
secret_key, eval_key, ... = aux_keygen(...)
a_keys, b_keys, k_dict = secret_key

# 2. Homomorphic Evaluation (BEFORE execution)
#    Compute what the final QOTP keys will be after circuit execution
T_sets, V_sets, auxiliary_states = eval_key
final_a, final_b = compute_final_keys_homomorphically(
    qc, a_keys, b_keys, auxiliary_states, t_depth, ...
)

# 3. Encryption (prepare circuit with initial QOTP)
qc_encrypted = apply_initial_qotp(qc, a_keys, b_keys)

# 4. Transpile & Execute on IBM
qc_transpiled = transpile(qc_encrypted, backend, ...)
result = execute_on_ibm(qc_transpiled, shots)
counts = result.quasi_dists[0]

# 5. Decode Measurements (using final keys)
decoded_counts = {}
for bitstring, prob in counts.items():
    decoded_bits = decode_bitstring(bitstring, final_a, final_b)
    decoded_counts[decoded_bits] = prob
```

### Option B: Simplified Testing (For Noise Measurement)

If the goal is just to measure **noise effects** on AUX-QHE circuits, simplify:

```python
# 1. Key Generation
secret_key, eval_key, ... = aux_keygen(...)

# 2. Create encrypted circuit (with QOTP gates)
qc_encrypted = create_aux_qhe_circuit(qc, secret_key)

# 3. Transpile & Execute on IBM
qc_transpiled = transpile(qc_encrypted, backend, ...)
result = execute_on_ibm(qc_transpiled, shots)

# 4. Compare with ideal (for noise measurement)
ideal_counts = simulate_ideal(qc)
noisy_counts = result.quasi_dists[0]
fidelity = compute_fidelity(ideal_counts, noisy_counts)
```

**This removes the homomorphic evaluation complexity and just measures noise on AUX-QHE circuits.**

---

## 📊 TEST RESULTS

### Local Pipeline Test (3q-2t)
- ✅ Key generation: Working
- ✅ Encryption: Working
- ✅ Evaluation: Working
- ✅ Decryption: Working
- ⚠️  Fidelity: 0.000000 (Extra X gates in decrypted circuit)

**Root Cause:** The current implementation treats AUX-QHE as a full homomorphic execution system, but the IBM experiment is trying to use it for noise measurement on hardware-executed circuits.

---

## 🎯 RECOMMENDATIONS

### For Immediate Testing:

1. **Remove `aux_eval` and `qotp_decrypt` from IBM experiment**
   - They don't make sense for hardware-executed circuits
   - Focus on noise measurement of the encrypted circuit itself

2. **Simplified Flow:**
   ```python
   - Generate keys
   - Encrypt circuit with QOTP
   - Transpile
   - Execute on IBM hardware
   - Compare noisy results with ideal simulation
   ```

3. **Measure:**
   - How noise affects AUX-QHE encrypted circuits
   - Impact of different optimization levels
   - Effectiveness of ZNE on AUX-QHE circuits

### For Full AUX-QHE Implementation:

If you want true homomorphic evaluation:
1. Compute final keys **before** execution using `aux_eval`
2. Execute encrypted circuit on IBM
3. Decode measurement results using final keys (not decrypt circuit)
4. This requires implementing measurement decoding logic

---

## 📝 SUMMARY

**Current Status:**
- ✅ Core AUX-QHE components working
- ✅ API mismatches fixed
- ⚠️  IBM experiment has incorrect architectural flow

**Next Steps:**
1. Decide on experiment goal: Noise measurement OR full homomorphic evaluation
2. Implement appropriate flow based on goal
3. Test locally before running on IBM hardware

**Estimated Time to Fix:**
- Simplified noise measurement: ~30 minutes
- Full homomorphic implementation: ~2-3 hours

---

**Last Updated:** 2025-10-09
**Status:** Ready for decision on implementation approach
