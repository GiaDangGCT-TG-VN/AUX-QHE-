# AUX-QHE Protocol Visualization (5q-3t)

## Overview

This directory contains detailed circuit diagrams showing the three main phases of the Auxiliary Quantum Homomorphic Encryption (AUX-QHE) protocol for the 5q-3t configuration.

## Protocol Phases

### Phase 1: QOTP Encryption (`01_qotp_encryption.png`)

**Purpose**: Encrypt the input quantum state using Quantum One-Time Pad

**Steps**:
1. Generate random binary keys: a_init = [a₀, a₁, ..., a₄], b_init = [b₀, b₁, ..., b₄]
2. Apply encryption operators: X^{a[i]} Z^{b[i]} to each qubit i
3. Circuit is now encrypted - server cannot learn input without keys

**Key Formula**:
```
|ψ_encrypted⟩ = (⊗ᵢ X^{aᵢ} Z^{bᵢ}) |ψ⟩
```

**Security**: Information-theoretically secure (one-time pad property)

---

### Phase 2: T-Gadget Evaluation (`02_t_gadget_evaluation.png`)

**Purpose**: Apply T-gates homomorphically without decryption

**T-Gadget Protocol** (per T-gate):
1. **Auxiliary Preparation**: Prepare |A⟩ = (|0⟩ + e^{iπ/4}|1⟩)/√2 = H·T|0⟩
2. **Entanglement**: Apply CNOT from target qubit to auxiliary
3. **Measurement**: Measure auxiliary in X-basis → outcome c ∈ {0, 1}
4. **Correction**: If c=1, apply S gate to target qubit

**Why it works**:
- T-gate is applied via teleportation through auxiliary state
- Measurement outcome c is encrypted using BFV homomorphic encryption
- Client evaluates correction homomorphically: f_b ← f_a ⊕ f_b ⊕ k ⊕ (c·f_a)

**Key Properties**:
- Consumes 1 auxiliary state per T-gate
- For 5q-3t: 15 T-gates → 31,025 auxiliary states needed (with higher-order terms)
- Measurement is non-destructive to target computation

---

### Phase 3: QOTP Decryption (`03_qotp_decryption.png`)

**Purpose**: Remove encryption to recover original output

**Steps**:
1. Circuit execution completed on server
2. Client computes final keys: a_final, b_final (from polynomial evaluation)
3. Apply decryption operators: X^{a_final[i]} Z^{b_final[i]}
4. Measure in computational basis

**Key Formula**:
```
|ψ_output⟩ = (⊗ᵢ X^{a_final[i]} Z^{b_final[i]}) |ψ_encrypted_result⟩
```

**Polynomial Evaluation**:
- Keys evolve through T-gates: f_a, f_b become polynomials
- Client evaluates polynomials using BFV-encrypted measurement outcomes
- Example: f_b = b₀ + k₁ + b₀·k₂ + (b₀·b₁)·k₃ (with cross-terms!)

---

## Complete Protocol (`04_complete_protocol.png`)

Shows all three phases in sequence with barriers marking phase transitions.

**Timeline**:
```
Encryption → T-Layer 1 (Gadgets) → T-Layer 2 → T-Layer 3 → Decryption → Measure
```

**Circuit Statistics for 5q-3t**:
- 5 qubits (target computation)
- 3 T-depth layers (15 T-gates total)
- 1 auxiliary qubit per T-gate (shown simplified)
- 31,025 total auxiliary states (including higher-order cross-terms)

---

## Key Insights

### Why Auxiliary States Explode

**Layer 1**: 10 states (5 qubits × 2 keys)
**Layer 2**: 105 states (layer 1 + 45 cross-terms + 50 new keys)
**Layer 3**: 6,090 states (layer 2 + 5,460 cross-terms + 525 new keys)

**Total**: 6,205 unique states → 31,025 total including multiplicities

### Why Cross-Terms Matter

After each T-gadget:
- Measurement outcome c interacts with existing key f_a
- Creates cross-term: c·f_a
- Cross-terms must be encrypted homomorphically → BFV overhead
- 5q-3t has **5,505 cross-terms** to encrypt!

### Homomorphic Evaluation Location

**Critical**: The IBM hardware execution IS the homomorphic evaluation!
- Server runs encrypted circuit without learning anything
- Measurement outcomes encrypted with BFV
- Client decrypts outcomes and evaluates key polynomials locally

---

## Files

### Images (PNG)
- `01_qotp_encryption.png` - QOTP encryption phase
- `02_t_gadget_evaluation.png` - Single T-gadget circuit
- `03_qotp_decryption.png` - QOTP decryption phase  
- `04_complete_protocol.png` - Full protocol pipeline

### Text (TXT)
- `01_qotp_encryption.txt` - ASCII circuit diagram
- `02_t_gadget_evaluation.txt` - ASCII T-gadget
- `03_qotp_decryption.txt` - ASCII decryption
- `04_complete_protocol.txt` - ASCII full protocol

---

## How to View

```bash
# View images
open 01_qotp_encryption.png
open 02_t_gadget_evaluation.png
open 03_qotp_decryption.png
open 04_complete_protocol.png

# View text diagrams
cat 01_qotp_encryption.txt
cat 02_t_gadget_evaluation.txt
cat 03_qotp_decryption.txt
cat 04_complete_protocol.txt

# Regenerate
python ../visualize_aux_qhe_protocol.py
```

---

## References

**Key Equations**:

1. **QOTP Encryption**: |ψ'⟩ = ⊗ᵢ X^{aᵢ}Z^{bᵢ} |ψ⟩
2. **T-Gadget**: T|ψ⟩ ≈ S^c (CNOT_{target→aux} · |A⟩⊗|ψ⟩)
3. **Key Evolution**: f_b ← f_a ⊕ f_b ⊕ k ⊕ (c·f_a)
4. **Decryption**: |ψ_final⟩ = ⊗ᵢ X^{a_final[i]}Z^{b_final[i]} |ψ_result⟩

**Cross-Term Formula**: Σ C(layer_i, 2) for i = 1 to t_depth-1

**For 5q-3t**: C(10,2) + C(105,2) = 45 + 5,460 = 5,505 cross-terms

---

Generated for AUX-QHE research project
