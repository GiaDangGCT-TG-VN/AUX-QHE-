#!/usr/bin/env python3
"""
Visualize AUX-QHE Circuit Diagrams

This script generates circuit diagrams for the complete AUX-QHE process:
1. Original circuit (input)
2. QOTP encrypted circuit
3. Transpiled circuit (for IBM hardware)
4. Full pipeline visualization

Uses Qiskit's circuit drawer with IBM-style formatting.
"""

import sys
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from pathlib import Path

from qiskit import QuantumCircuit, transpile
from qiskit.visualization import circuit_drawer
from qiskit_ibm_runtime import QiskitRuntimeService

# Import AUX-QHE modules
sys.path.insert(0, 'core')
from key_generation import aux_keygen
from qotp_crypto import qotp_encrypt
from bfv_core import initialize_bfv_params

def create_original_circuit(num_qubits, t_depth):
    """Create the original circuit (before encryption)"""
    qc = QuantumCircuit(num_qubits, name='Original')

    # Apply Hadamard gates for initialization
    for q in range(num_qubits):
        qc.h(q)

    # Apply T-gates and CX gates in layers
    for layer in range(t_depth):
        # Apply T-gates in parallel
        for q in range(num_qubits):
            qc.t(q)
        qc.barrier()

        # Add entanglement with CX gates
        if num_qubits >= 2:
            for q in range(0, num_qubits - 1, 2):
                qc.cx(q, q + 1)
        qc.barrier()

    return qc

def create_encrypted_circuit(qc, num_qubits, t_depth):
    """Create QOTP encrypted circuit"""
    # Initialize BFV
    bfv_params, bfv_encoder, bfv_encryptor, bfv_decryptor, bfv_evaluator = initialize_bfv_params()
    poly_degree = bfv_params.poly_degree

    # Key generation
    a_init = [0] * num_qubits
    b_init = [0] * num_qubits
    secret_key, eval_key, prep_time, layer_sizes, total_aux = aux_keygen(
        num_qubits, t_depth, a_init, b_init
    )
    a_keys, b_keys, k_dict = secret_key

    # QOTP encryption
    qc_encrypted, _, enc_a, enc_b = qotp_encrypt(
        qc, a_keys, b_keys,
        counter_d=0,
        max_qubits=num_qubits * 2,
        encryptor=bfv_encryptor,
        encoder=bfv_encoder,
        decryptor=bfv_decryptor,
        poly_degree=poly_degree
    )

    if qc_encrypted is None:
        raise ValueError("QOTP encryption failed")

    qc_encrypted.name = 'QOTP_Encrypted'
    return qc_encrypted

def create_transpiled_circuit(qc_encrypted, backend_name='ibm_brisbane'):
    """Create transpiled circuit for IBM hardware"""
    try:
        # Try to load IBM backend
        service = QiskitRuntimeService()
        backend = service.backend(backend_name)
        print(f"✅ Using real IBM backend: {backend_name}")
    except:
        print(f"⚠️  Could not load IBM backend, using fake backend for visualization")
        from qiskit_ibm_runtime.fake_provider import FakeBrisbane
        backend = FakeBrisbane()

    # Transpile
    qc_transpiled = transpile(qc_encrypted, backend, optimization_level=1)
    qc_transpiled.name = 'Transpiled'

    # Add measurements
    qc_transpiled.measure_all()

    return qc_transpiled

def draw_circuit(circuit, filename, title, style='iqx'):
    """Draw circuit and save to file using IBM style"""
    print(f"   📊 Drawing: {title}")
    print(f"      Gates: {circuit.size()}, Depth: {circuit.depth()}, Qubits: {circuit.num_qubits}")

    try:
        # Draw with IBM style ('iqx' = IBM Quantum Experience style)
        fig = circuit_drawer(
            circuit,
            output='mpl',  # matplotlib output
            style=style,
            plot_barriers=True,
            fold=-1,  # No folding - show full circuit
            scale=0.7
        )

        # Save figure
        if fig:
            plt.figure(fig.number)
            plt.title(title, fontsize=14, fontweight='bold')
            plt.tight_layout()
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()
            print(f"      ✅ Saved to: {filename}")
        else:
            print(f"      ⚠️  Warning: Could not generate figure")

    except Exception as e:
        print(f"      ❌ Error drawing circuit: {e}")

def draw_circuit_text(circuit, filename, title):
    """Draw circuit as text diagram"""
    print(f"   📝 Drawing text: {title}")

    try:
        text_diagram = circuit.draw(output='text', fold=-1)

        with open(filename, 'w') as f:
            f.write(f"{title}\n")
            f.write("="*80 + "\n\n")
            f.write(str(text_diagram))
            f.write("\n\n")
            f.write(f"Circuit Statistics:\n")
            f.write(f"  Qubits: {circuit.num_qubits}\n")
            f.write(f"  Gates: {circuit.size()}\n")
            f.write(f"  Depth: {circuit.depth()}\n")
            f.write(f"  Operations: {circuit.count_ops()}\n")

        print(f"      ✅ Saved to: {filename}")

    except Exception as e:
        print(f"      ❌ Error drawing text circuit: {e}")

def create_pipeline_visualization(num_qubits, t_depth, backend_name='ibm_brisbane'):
    """Create complete pipeline visualization"""

    config_name = f"{num_qubits}q-{t_depth}t"
    output_dir = Path("circuit_diagrams") / config_name
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*80}")
    print(f"🎨 Generating Circuit Diagrams: {config_name}")
    print(f"{'='*80}\n")

    # 1. Original Circuit
    print("1️⃣  Creating original circuit...")
    qc_original = create_original_circuit(num_qubits, t_depth)

    draw_circuit(
        qc_original,
        output_dir / "01_original_circuit.png",
        f"AUX-QHE: Original Circuit ({config_name})"
    )
    draw_circuit_text(
        qc_original,
        output_dir / "01_original_circuit.txt",
        f"AUX-QHE: Original Circuit ({config_name})"
    )

    # 2. QOTP Encrypted Circuit
    print("\n2️⃣  Creating QOTP encrypted circuit...")
    try:
        qc_encrypted = create_encrypted_circuit(qc_original, num_qubits, t_depth)

        draw_circuit(
            qc_encrypted,
            output_dir / "02_qotp_encrypted_circuit.png",
            f"AUX-QHE: QOTP Encrypted Circuit ({config_name})"
        )
        draw_circuit_text(
            qc_encrypted,
            output_dir / "02_qotp_encrypted_circuit.txt",
            f"AUX-QHE: QOTP Encrypted Circuit ({config_name})"
        )
    except Exception as e:
        print(f"   ❌ Error creating encrypted circuit: {e}")
        qc_encrypted = None

    # 3. Transpiled Circuit
    if qc_encrypted:
        print("\n3️⃣  Creating transpiled circuit...")
        try:
            qc_transpiled = create_transpiled_circuit(qc_encrypted, backend_name)

            draw_circuit(
                qc_transpiled,
                output_dir / "03_transpiled_circuit.png",
                f"AUX-QHE: Transpiled Circuit ({config_name}, {backend_name})"
            )
            draw_circuit_text(
                qc_transpiled,
                output_dir / "03_transpiled_circuit.txt",
                f"AUX-QHE: Transpiled Circuit ({config_name}, {backend_name})"
            )
        except Exception as e:
            print(f"   ❌ Error creating transpiled circuit: {e}")

    # 4. Create summary document
    print("\n4️⃣  Creating summary document...")
    create_summary_document(output_dir, config_name, num_qubits, t_depth)

    print(f"\n{'='*80}")
    print(f"✅ All circuit diagrams saved to: {output_dir}")
    print(f"{'='*80}\n")

    return output_dir

def create_summary_document(output_dir, config_name, num_qubits, t_depth):
    """Create a summary document explaining the circuits"""

    summary_file = output_dir / "README.md"

    content = f"""# AUX-QHE Circuit Diagrams: {config_name}

## Configuration
- **Qubits**: {num_qubits}
- **T-depth**: {t_depth}
- **Algorithm**: Auxiliary Quantum Homomorphic Encryption (AUX-QHE)

## Circuit Pipeline

### 1. Original Circuit (`01_original_circuit.png`)

The input quantum circuit before any encryption or processing.

**Structure**:
- Hadamard gates (H) for initialization on all qubits
- {t_depth} layers of T-gates (non-Clifford gates)
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
Encrypted circuit = X^{{a[i]}} Z^{{b[i]}} U |ψ⟩
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
python ../visualize_aux_qhe_circuits.py --config {config_name}
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

Generated on: {Path.cwd()}
"""

    with open(summary_file, 'w') as f:
        f.write(content)

    print(f"   ✅ Summary saved to: {summary_file}")

def main():
    """Main function to generate all circuit diagrams"""

    import argparse

    parser = argparse.ArgumentParser(
        description="Generate AUX-QHE circuit diagrams in IBM Qiskit format"
    )
    parser.add_argument(
        '--config',
        type=str,
        default='3q-3t',
        help='Configuration to visualize (e.g., 3q-3t, 4q-3t, 5q-2t, 5q-3t)'
    )
    parser.add_argument(
        '--backend',
        type=str,
        default='ibm_brisbane',
        help='IBM backend for transpilation (default: ibm_brisbane)'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Generate diagrams for all configurations'
    )

    args = parser.parse_args()

    print("="*80)
    print("🎨 AUX-QHE CIRCUIT DIAGRAM GENERATOR")
    print("="*80)

    # Define configurations
    configs = {
        '3q-2t': (3, 2),
        '3q-3t': (3, 3),
        '4q-2t': (4, 2),
        '4q-3t': (4, 3),
        '5q-2t': (5, 2),
        '5q-3t': (5, 3)
    }

    if args.all:
        # Generate all configurations
        for config_name, (num_qubits, t_depth) in configs.items():
            try:
                create_pipeline_visualization(num_qubits, t_depth, args.backend)
            except Exception as e:
                print(f"❌ Error generating {config_name}: {e}\n")
    else:
        # Generate single configuration
        if args.config not in configs:
            print(f"❌ Error: Unknown configuration '{args.config}'")
            print(f"   Available: {', '.join(configs.keys())}")
            sys.exit(1)

        num_qubits, t_depth = configs[args.config]
        create_pipeline_visualization(num_qubits, t_depth, args.backend)

    print("\n✅ Circuit diagram generation complete!")

if __name__ == "__main__":
    main()
