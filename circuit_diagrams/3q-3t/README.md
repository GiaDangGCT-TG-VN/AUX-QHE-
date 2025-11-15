# AUX-QHE Circuit Diagrams: 3q-3t

## Configuration
- **Qubits**: 3
- **T-depth**: 3
- **Algorithm**: Auxiliary Quantum Homomorphic Encryption (AUX-QHE)

## Circuit Pipeline

### 1. Original Circuit (`01_original_circuit.png`)

The input quantum circuit before any encryption or processing.

**Structure**:
- Hadamard gates (H) for initialization on all qubits
- 3 layers of T-gates (non-Clifford gates)
- CX gates for entanglement between qubits
- Barriers to separate layers

**Purpose**: This represents the computation we want to perform homomorphically.

---

### 2. QOTP Encrypted Circuit (`02_qotp_encrypted_circuit.png`)

The circuit after applying Quantum One-Time Pad (QOTP) encryption.

**Encryption Process**:
1. Generate random QOTP keys: `a_keys`, `b_keys` (binary)
2. Apply X^a Z^b gates at the beginning (encryption)
3. Append original circuit gates
4. Keys are encrypted using BFV homomorphic encryption

**Theory**:
```
Encrypted circuit = X^{a[i]} Z^{b[i]} U |ψ⟩
```

Where U is the original circuit and |ψ⟩ is the input state.

**Purpose**: Protects the computation from eavesdropping. The server (IBM Quantum) cannot learn the input or computation without the keys.

---

### 3. Transpiled Circuit (`03_transpiled_circuit.png`)

The circuit after transpilation for IBM quantum hardware.

**Transpilation Process**:
1. Decompose gates into IBM's native gate set (sx, rz, cx)
2. Route qubits to match hardware connectivity
3. Optimize circuit depth and gate count
4. Add measurements at the end

**Changes**:
- Higher gate count (decomposition)
- Potentially higher depth
- Hardware-specific optimizations applied

**Purpose**: Convert abstract circuit into executable form on real IBM quantum processor.

---

## File Formats

### Image Files (`.png`)
- High-resolution circuit diagrams (300 DPI)
- IBM Quantum Experience style (`iqx`)
- Suitable for papers, presentations, documentation

### Text Files (`.txt`)
- ASCII art representation of circuits
- Includes circuit statistics (gates, depth, operations)
- Easy to view in terminal or text editor

---

## How to Use

### View Images
Open the `.png` files with any image viewer:
```bash
open 01_original_circuit.png
open 02_qotp_encrypted_circuit.png
open 03_transpiled_circuit.png
```

### View Text Diagrams
```bash
cat 01_original_circuit.txt
cat 02_qotp_encrypted_circuit.txt
cat 03_transpiled_circuit.txt
```

### Regenerate Diagrams
```bash
python ../visualize_aux_qhe_circuits.py --config 3q-3t
```

---

## Circuit Statistics

Run statistics will be added here after generation:
- Original circuit: X gates, Y depth
- Encrypted circuit: X gates, Y depth
- Transpiled circuit: X gates, Y depth

---

## AUX-QHE Protocol Overview

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Client    │     │ IBM Quantum  │     │   Client    │
│             │     │   (Server)   │     │             │
└──────┬──────┘     └──────┬───────┘     └──────┬──────┘
       │                   │                    │
       │ 1. Key Gen        │                    │
       ├──────────────────>│                    │
       │                   │                    │
       │ 2. QOTP Encrypt   │                    │
       ├──────────────────>│                    │
       │                   │                    │
       │ 3. Send Encrypted │                    │
       │    Circuit        │                    │
       ├──────────────────>│                    │
       │                   │                    │
       │                   │ 4. Execute         │
       │                   │    (Homomorphic    │
       │                   │     Evaluation)    │
       │                   ├───────────────────>│
       │                   │                    │
       │ 5. Return Results │                    │
       │<──────────────────┤                    │
       │                   │                    │
       │ 6. Decode with    │                    │
       │    Final Keys     │                    │
       ├──────────────────────────────────────>│
       │                   │                    │
```

**Key Point**: The execution on IBM hardware IS the homomorphic evaluation phase. The server executes the encrypted circuit without learning the input or computation.

---

## References

- **Paper**: [AUX-QHE: Auxiliary-Based Quantum Homomorphic Encryption](https://arxiv.org/abs/xxxx.xxxxx)
- **Repository**: [AUX-QHE GitHub](https://github.com/yourusername/AUX-QHE)
- **Qiskit**: [IBM Quantum Documentation](https://qiskit.org/documentation/)

---

Generated on: /Users/giadang/my_qiskitenv/AUX-QHE
