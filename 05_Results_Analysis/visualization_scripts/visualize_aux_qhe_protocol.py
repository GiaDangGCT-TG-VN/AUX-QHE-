#!/usr/bin/env python3
"""
Visualize Complete AUX-QHE Protocol for 5q-3t
Shows: QOTP Encryption → T-Gadget Evaluation → QOTP Decryption
"""

import sys
sys.path.insert(0, 'core')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.visualization import circuit_drawer

def create_qotp_encryption_circuit(num_qubits=5):
    """Show QOTP encryption phase"""
    qr = QuantumRegister(num_qubits, 'q')
    qc = QuantumCircuit(qr, name='QOTP_Encryption')
    
    # Add encryption gates X^a Z^b
    for i in range(num_qubits):
        qc.x(i)  # X^a[i] (example: a[i]=1)
        qc.z(i)  # Z^b[i] (example: b[i]=1)
    
    qc.barrier(label='Encrypted')
    
    # Original computation starts
    for i in range(num_qubits):
        qc.h(i)
    qc.barrier(label='Layer 1')
    
    # First T-layer
    for i in range(num_qubits):
        qc.t(i)
    qc.barrier()
    
    # Entanglement
    for i in range(0, num_qubits-1, 2):
        qc.cx(i, i+1)
    
    return qc

def create_t_gadget_circuit():
    """Show T-gadget homomorphic evaluation"""
    # Target qubit + auxiliary qubit
    target = QuantumRegister(1, 'target')
    aux = QuantumRegister(1, 'aux')
    c = ClassicalRegister(1, 'c')
    
    qc = QuantumCircuit(target, aux, c, name='T_Gadget')
    
    # Step 1: Prepare auxiliary state |A⟩
    qc.h(aux[0])
    qc.t(aux[0])
    qc.barrier(label='Aux Prep')
    
    # Step 2: CNOT from target to auxiliary
    qc.cx(target[0], aux[0])
    qc.barrier(label='Entangle')
    
    # Step 3: Measure auxiliary in X-basis
    qc.h(aux[0])
    qc.measure(aux[0], c[0])
    qc.barrier(label='Measure')
    
    # Step 4: Correction on target (c-dependent)
    qc.s(target[0]).c_if(c, 1)
    qc.barrier(label='Correct')
    
    return qc

def create_decryption_circuit(num_qubits=5):
    """Show QOTP decryption phase"""
    qr = QuantumRegister(num_qubits, 'q')
    cr = ClassicalRegister(num_qubits, 'c')
    qc = QuantumCircuit(qr, cr, name='QOTP_Decryption')
    
    # After circuit execution, apply final QOTP keys
    qc.barrier(label='Final Keys')
    
    for i in range(num_qubits):
        qc.x(i)  # X^{a_final[i]}
        qc.z(i)  # Z^{b_final[i]}
    
    qc.barrier(label='Decrypted')
    
    # Measure in computational basis
    qc.measure(qr, cr)
    
    return qc

def create_full_protocol_circuit(num_qubits=5, t_depth=3):
    """Create complete AUX-QHE protocol circuit"""
    qr = QuantumRegister(num_qubits, 'q')
    aux_qr = QuantumRegister(1, 'aux')  # One auxiliary for demonstration
    c_aux = ClassicalRegister(1, 'c_aux')
    c_final = ClassicalRegister(num_qubits, 'c')
    
    qc = QuantumCircuit(qr, aux_qr, c_aux, c_final, name='AUX_QHE_Protocol')
    
    # ========================================
    # PHASE 1: QOTP ENCRYPTION
    # ========================================
    qc.barrier(label='═══ ENCRYPTION ═══')
    
    # Apply initial QOTP keys X^a Z^b
    for i in range(num_qubits):
        qc.x(i)  # X^{a_init[i]}
        qc.z(i)  # Z^{b_init[i]}
    
    qc.barrier(label='Keys Applied')
    
    # Initialize with Hadamards
    for i in range(num_qubits):
        qc.h(i)
    
    qc.barrier(label='Initialized')
    
    # ========================================
    # PHASE 2: HOMOMORPHIC EVALUATION (T-GADGETS)
    # ========================================
    
    for layer in range(t_depth):
        qc.barrier(label=f'═══ T-LAYER {layer+1} ═══')
        
        # Apply T-gates homomorphically using gadgets
        # For demonstration, show first qubit's T-gadget
        if layer == 0:
            # Prepare auxiliary state |A⟩ = (|0⟩ + e^{iπ/4}|1⟩)/√2
            qc.h(aux_qr[0])
            qc.t(aux_qr[0])
            qc.barrier(label='Aux Prep')
            
            # Entangle target with auxiliary
            qc.cx(qr[0], aux_qr[0])
            qc.barrier(label='Entangle')
            
            # Measure auxiliary in X-basis
            qc.h(aux_qr[0])
            qc.measure(aux_qr[0], c_aux[0])
            qc.barrier(label='Measure')
            
            # Correction based on measurement
            qc.s(qr[0]).c_if(c_aux, 1)
            qc.barrier(label='Correct')
        
        # Apply T-gates to remaining qubits (simplified)
        for i in range(1, num_qubits):
            qc.t(i)
        
        qc.barrier()
        
        # Add entanglement
        for i in range(0, num_qubits-1, 2):
            qc.cx(i, i+1)
        
        qc.barrier(label=f'Layer {layer+1} Done')
    
    # ========================================
    # PHASE 3: QOTP DECRYPTION
    # ========================================
    qc.barrier(label='═══ DECRYPTION ═══')
    
    # Apply final QOTP keys (after polynomial evaluation)
    for i in range(num_qubits):
        qc.x(i)  # X^{a_final[i]}
        qc.z(i)  # Z^{b_final[i]}
    
    qc.barrier(label='Keys Applied')
    
    # Final measurement
    qc.measure(qr, c_final)
    
    return qc

def draw_circuit_with_phases(circuit, filename, title):
    """Draw circuit with clear phase separation"""
    print(f"📊 Drawing: {title}")
    print(f"   Gates: {circuit.size()}, Depth: {circuit.depth()}")
    
    try:
        fig = circuit_drawer(
            circuit,
            output='mpl',
            plot_barriers=True,
            fold=-1,
            scale=0.6,
            style={'backgroundcolor': '#EFEFEF'}
        )
        
        if fig:
            plt.figure(fig.number)
            plt.suptitle(title, fontsize=16, fontweight='bold', y=0.98)
            plt.tight_layout()
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()
            print(f"   ✅ Saved: {filename}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def draw_text_circuit(circuit, filename, title):
    """Draw text version"""
    print(f"📝 Text: {title}")
    
    try:
        text = circuit.draw(output='text', fold=-1)
        
        with open(filename, 'w') as f:
            f.write(f"{title}\n")
            f.write("="*100 + "\n\n")
            f.write(str(text))
            f.write("\n\n")
            f.write("Circuit Statistics:\n")
            f.write(f"  Total Qubits: {circuit.num_qubits}\n")
            f.write(f"  Total Gates: {circuit.size()}\n")
            f.write(f"  Circuit Depth: {circuit.depth()}\n")
            f.write(f"  Operations: {circuit.count_ops()}\n")
        
        print(f"   ✅ Saved: {filename}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def main():
    output_dir = Path("circuit_diagrams/5q-3t-protocol")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n" + "="*80)
    print("🎨 AUX-QHE PROTOCOL VISUALIZATION (5q-3t)")
    print("="*80 + "\n")
    
    # 1. QOTP Encryption Phase
    print("1️⃣  QOTP Encryption Phase")
    qc_encrypt = create_qotp_encryption_circuit(5)
    draw_circuit_with_phases(
        qc_encrypt,
        output_dir / "01_qotp_encryption.png",
        "Phase 1: QOTP Encryption (5q-3t)"
    )
    draw_text_circuit(
        qc_encrypt,
        output_dir / "01_qotp_encryption.txt",
        "Phase 1: QOTP Encryption"
    )
    
    # 2. T-Gadget Evaluation
    print("\n2️⃣  T-Gadget Homomorphic Evaluation")
    qc_gadget = create_t_gadget_circuit()
    draw_circuit_with_phases(
        qc_gadget,
        output_dir / "02_t_gadget_evaluation.png",
        "Phase 2: T-Gadget Homomorphic Evaluation"
    )
    draw_text_circuit(
        qc_gadget,
        output_dir / "02_t_gadget_evaluation.txt",
        "Phase 2: T-Gadget Evaluation"
    )
    
    # 3. QOTP Decryption Phase
    print("\n3️⃣  QOTP Decryption Phase")
    qc_decrypt = create_decryption_circuit(5)
    draw_circuit_with_phases(
        qc_decrypt,
        output_dir / "03_qotp_decryption.png",
        "Phase 3: QOTP Decryption (5q-3t)"
    )
    draw_text_circuit(
        qc_decrypt,
        output_dir / "03_qotp_decryption.txt",
        "Phase 3: QOTP Decryption"
    )
    
    # 4. Full Protocol
    print("\n4️⃣  Complete AUX-QHE Protocol")
    qc_full = create_full_protocol_circuit(5, 3)
    draw_circuit_with_phases(
        qc_full,
        output_dir / "04_complete_protocol.png",
        "Complete AUX-QHE Protocol: Encryption → Evaluation → Decryption (5q-3t)"
    )
    draw_text_circuit(
        qc_full,
        output_dir / "04_complete_protocol.txt",
        "Complete AUX-QHE Protocol"
    )
    
    # Create README
    print("\n5️⃣  Creating documentation")
    create_readme(output_dir)
    
    print("\n" + "="*80)
    print(f"✅ All protocol diagrams saved to: {output_dir}")
    print("="*80 + "\n")

def create_readme(output_dir):
    """Create comprehensive README"""
    content = """# AUX-QHE Protocol Visualization (5q-3t)

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
"""
    
    readme_path = output_dir / "README.md"
    with open(readme_path, 'w') as f:
        f.write(content)
    
    print(f"   ✅ README saved: {readme_path}")

if __name__ == "__main__":
    main()
