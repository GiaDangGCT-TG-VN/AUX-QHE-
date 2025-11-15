# AUX-QHE Correct Architecture for IBM Quantum Hardware

## ✅ CORRECTED Understanding

### Three-Party Model

1. **Client** - Has secret keys, prepares encryption, decodes results
2. **Quantum Server (IBM Hardware)** - Executes encrypted circuit (this IS the homomorphic evaluation)
3. **Classical Server** (optional) - Could store auxiliary states, not used in this experiment

---

## Correct Execution Flow

### **CLIENT SIDE (Preparation)**

#### Step 1: Key Generation
```python
secret_key, eval_key, ... = aux_keygen(num_qubits, t_depth, a_init, b_init)
a_keys, b_keys, k_dict = secret_key
T_sets, V_sets, auxiliary_states = eval_key
```
- Generate initial QOTP keys (a, b)
- Generate auxiliary states for T-gate gadgets
- These stay on client side (secret!)

#### Step 2: Circuit Encryption (QOTP)
```python
qc_encrypted, _, enc_a, enc_b = qotp_encrypt(
    qc, a_keys, b_keys, ...
)
```
- Apply X^a Z^b gates at beginning of circuit
- Encrypt QOTP keys with BFV for homomorphic operations
- Creates encrypted circuit ready for server

#### Step 3: Transpilation
```python
qc_transpiled = transpile(qc_encrypted, backend, optimization_level=...)
```
- Optimize circuit for IBM hardware
- Still encrypted at this point

---

### **SERVER SIDE (IBM Quantum Hardware)**

#### Step 4: Homomorphic Evaluation
```python
# Send encrypted circuit to IBM
with Session(backend=backend) as session:
    sampler = Sampler(session=session)
    job = sampler.run(qc_transpiled, shots=shots)
    result = job.result()

    # Get encrypted measurement results
    counts = result.quasi_dists[0]
```
- **This execution IS the homomorphic evaluation phase!**
- IBM hardware runs the encrypted circuit
- Returns measurement outcomes (still encrypted under QOTP)
- Server never learns the original circuit or results

---

### **CLIENT SIDE (Decoding)**

#### Step 5: Compute Final QOTP Keys
```python
# Use circuit structure to compute final keys
qc_eval, final_enc_a, final_enc_b = aux_eval(
    qc_encrypted, enc_a, enc_b, auxiliary_states, t_depth, ...
)

# Decrypt final keys
final_a = [decrypt_bfv(final_enc_a[i]) for i in range(num_qubits)]
final_b = [decrypt_bfv(final_enc_b[i]) for i in range(num_qubits)]
```
- `aux_eval` does NOT re-execute the circuit
- It tracks how QOTP keys evolve through circuit gates
- Computes final keys homomorphically using BFV

#### Step 6: Decode Measurement Results
```python
decoded_counts = {}
for bitstring, count in counts.items():
    # XOR with final QOTP keys to decode
    decoded_bits = bitstring XOR final_a
    decoded_counts[decoded_bits] = count
```
- Apply final QOTP keys to decode encrypted measurements
- Reveals actual measurement outcomes

---

## Key Insights

### ✅ What `aux_eval` Actually Does

`aux_eval` is a **client-side simulation** that:
1. Takes the circuit structure (gate sequence)
2. Tracks how QOTP keys transform through each gate
3. Computes final key values using BFV homomorphic operations
4. **Does NOT** execute quantum gates - just tracks classical key evolution

### ✅ Why IBM Execution = Homomorphic Evaluation

- The encrypted circuit runs on real quantum hardware
- Hardware sees only X^a Z^b encrypted gates, not original circuit intent
- This IS the "blind" quantum computation
- Results come back encrypted, preserving privacy

### ✅ Two Types of "Evaluation"

1. **Quantum Evaluation (Server):** IBM hardware executes encrypted circuit
2. **Classical Key Evolution (Client):** `aux_eval` computes final QOTP keys

Both are needed for complete homomorphic execution!

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                       CLIENT SIDE                            │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ 1. Key Generation                                      │ │
│  │    aux_keygen() → (secret_key, eval_key)              │ │
│  └────────────────────────────────────────────────────────┘ │
│                           ↓                                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ 2. Circuit Encryption                                  │ │
│  │    qotp_encrypt(qc, a_keys, b_keys)                   │ │
│  │    → qc_encrypted                                      │ │
│  └────────────────────────────────────────────────────────┘ │
│                           ↓                                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ 3. Transpilation                                       │ │
│  │    transpile(qc_encrypted) → qc_transpiled            │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            ↓  (send encrypted circuit)
┌─────────────────────────────────────────────────────────────┐
│                    IBM QUANTUM SERVER                        │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ 4. Homomorphic Evaluation (Quantum Execution)         │ │
│  │    Execute qc_transpiled on quantum hardware          │ │
│  │    → encrypted_counts                                 │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            ↓  (receive encrypted results)
┌─────────────────────────────────────────────────────────────┐
│                       CLIENT SIDE                            │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ 5. Compute Final Keys (Classical Simulation)          │ │
│  │    aux_eval(qc_encrypted, enc_a, enc_b, ...)         │ │
│  │    → final_enc_a, final_enc_b                         │ │
│  └────────────────────────────────────────────────────────┘ │
│                           ↓                                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ 6. Decode Measurements                                 │ │
│  │    XOR encrypted_counts with final keys               │ │
│  │    → decoded_counts (actual results!)                 │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## IBM Experiment - Corrected Flow

### What Was Wrong
```python
# WRONG: aux_eval called AFTER IBM execution
IBM.execute() → counts
aux_eval(qc_encrypted) → qc_eval  # ❌ Re-executing circuit
qotp_decrypt(qc_eval) → qc_decrypted  # ❌ Trying to decrypt circuit
```

### What's Correct Now
```python
# CORRECT: aux_eval computes keys, then decode measurements
IBM.execute() → encrypted_counts  # ✅ Server-side homomorphic evaluation
aux_eval(qc_encrypted) → final_keys  # ✅ Client computes final keys
XOR encrypted_counts with final_keys → decoded_counts  # ✅ Decode results
```

---

## Privacy Properties

### What IBM Server Sees:
- Encrypted circuit with X^a Z^b gates
- Cannot determine original circuit structure
- Measurement results are encrypted

### What IBM Server DOESN'T See:
- Initial QOTP keys (a, b)
- Original circuit before encryption
- Actual measurement outcomes
- Auxiliary states or BFV keys

### Client Privacy Maintained:
✅ Circuit privacy (through QOTP encryption)
✅ Result privacy (measurements encrypted)
✅ Key privacy (BFV homomorphic encryption)

---

## Experiment Purpose

This IBM experiment measures:
1. **Noise effects** on AUX-QHE encrypted circuits
2. **Error mitigation** effectiveness (ZNE, optimization levels)
3. **Scalability** across different qubit/T-depth configurations
4. **Fidelity degradation** due to hardware noise

**NOT implementing full delegation** - just measuring performance on real hardware!

---

## Summary

✅ **Fixed:** IBM experiment now correctly implements AUX-QHE architecture
✅ **Clarified:** IBM execution IS the homomorphic evaluation (server-side)
✅ **Corrected:** `aux_eval` computes final keys (client-side), doesn't re-execute
✅ **Implemented:** Proper measurement decoding using final QOTP keys

**Status:** Ready for IBM hardware testing! 🚀

---

**Last Updated:** 2025-10-09
**Architecture:** Corrected based on proper understanding of QHE delegation model
