# AUX-QHE Circuit Visualization Guide

## Overview

This guide explains how to generate and view circuit diagrams for the complete AUX-QHE algorithm process.

## Generated Files

For each configuration (e.g., 3q-3t, 5q-3t), the following files are generated:

### 1. **Original Circuit** (`01_original_circuit.*`)
- Shows the input quantum circuit before encryption
- Contains Hadamard initialization, T-gates, and CX gates
- This is what you want to compute homomorphically

### 2. **QOTP Encrypted Circuit** (`02_qotp_encrypted_circuit.*`)
- Shows the circuit after QOTP encryption
- Has X^a Z^b gates at the beginning (encryption layer)
- Original gates are preserved after encryption

### 3. **Transpiled Circuit** (`03_transpiled_circuit.*`)
- Shows the circuit after transpilation for IBM hardware
- Decomposed into native gate set (sx, rz, cx)
- Includes qubit mapping and measurements
- **This is what actually runs on IBM Quantum**

## File Formats

### PNG Images (`.png`)
- High-resolution diagrams (300 DPI)
- IBM Qiskit style formatting
- Suitable for papers, presentations, documentation

### Text Diagrams (`.txt`)
- ASCII art representation
- Can be viewed in terminal
- Includes circuit statistics

### README (`README.md`)
- Detailed explanation of each circuit
- Protocol overview with diagrams
- References and usage instructions

## Quick Start

### Generate Circuit Diagrams

#### Single Configuration
```bash
# 3 qubits, 3 T-layers
python visualize_aux_qhe_circuits.py --config 3q-3t

# 5 qubits, 3 T-layers (most complex)
python visualize_aux_qhe_circuits.py --config 5q-3t
```

#### All Configurations
```bash
python visualize_aux_qhe_circuits.py --all
```

#### With Specific Backend
```bash
python visualize_aux_qhe_circuits.py --config 5q-3t --backend ibm_torino
```

### View Diagrams

#### View PNG Images
```bash
# macOS
open circuit_diagrams/3q-3t/01_original_circuit.png
open circuit_diagrams/3q-3t/02_qotp_encrypted_circuit.png
open circuit_diagrams/3q-3t/03_transpiled_circuit.png

# Linux
xdg-open circuit_diagrams/3q-3t/01_original_circuit.png

# Windows
start circuit_diagrams/3q-3t/01_original_circuit.png
```

#### View Text Diagrams
```bash
cat circuit_diagrams/3q-3t/01_original_circuit.txt
cat circuit_diagrams/3q-3t/02_qotp_encrypted_circuit.txt
```

#### View All Files in Directory
```bash
ls -lh circuit_diagrams/3q-3t/
```

## Directory Structure

```
circuit_diagrams/
├── 3q-2t/
│   ├── 01_original_circuit.png
│   ├── 01_original_circuit.txt
│   ├── 02_qotp_encrypted_circuit.png
│   ├── 02_qotp_encrypted_circuit.txt
│   ├── 03_transpiled_circuit.png
│   ├── 03_transpiled_circuit.txt
│   └── README.md
├── 3q-3t/
│   └── ... (same structure)
├── 4q-2t/
├── 4q-3t/
├── 5q-2t/
└── 5q-3t/
    └── ... (same structure)
```

## Example: 3q-3t Original Circuit

```
AUX-QHE: Original Circuit (3q-3t)
================================================================================

     ┌───┐┌───┐ ░       ░ ┌───┐ ░       ░ ┌───┐ ░       ░
q_0: ┤ H ├┤ T ├─░───■───░─┤ T ├─░───■───░─┤ T ├─░───■───░─
     ├───┤├───┤ ░ ┌─┴─┐ ░ ├───┤ ░ ┌─┴─┐ ░ ├───┤ ░ ┌─┴─┐ ░
q_1: ┤ H ├┤ T ├─░─┤ X ├─░─┤ T ├─░─┤ X ├─░─┤ T ├─░─┤ X ├─░─
     ├───┤├───┤ ░ └───┘ ░ ├───┤ ░ └───┘ ░ ├───┤ ░ └───┘ ░
q_2: ┤ H ├┤ T ├─░───────░─┤ T ├─░───────░─┤ T ├─░───────░─
     └───┘└───┘ ░       ░ └───┘ ░       ░ └───┘ ░       ░

Circuit Statistics:
  Qubits: 3
  Gates: 15
  Depth: 7
  Operations: {'t': 9, 'barrier': 6, 'h': 3, 'cx': 3}
```

**Interpretation**:
- **H gates**: Initialize qubits in superposition
- **T gates**: Non-Clifford gates (3 layers)
- **CX gates**: Create entanglement between adjacent qubits
- **Barriers**: Separate layers for clarity

## Circuit Statistics Comparison

| Config | Original | Encrypted | Transpiled |
|--------|----------|-----------|------------|
| 3q-3t  | 15 gates, depth 7 | 15 gates, depth 7 | ~178 gates, depth ~27 |
| 5q-3t  | 26 gates, depth 7 | 26 gates, depth 7 | ~300+ gates, depth ~40 |

**Note**: Transpiled circuits are much larger due to:
1. Gate decomposition into native gate set
2. Qubit mapping for hardware connectivity
3. Additional optimization passes

## Understanding the Pipeline

```
┌──────────────────┐
│ Original Circuit │  ← Input computation
└────────┬─────────┘
         │
         │ Apply QOTP Encryption (X^a Z^b)
         │
         ▼
┌──────────────────┐
│ Encrypted Circuit│  ← Protected computation
└────────┬─────────┘
         │
         │ Transpile for IBM hardware
         │
         ▼
┌──────────────────┐
│ Transpiled Circuit│ ← Executable on IBM Quantum
└──────────────────┘
         │
         │ Execute on IBM hardware
         │
         ▼
    Measurement
    Results
```

## AUX-QHE Protocol Visualization

```
Client Side          IBM Quantum Server          Client Side
══════════          ═══════════════════          ══════════

┌─────────┐
│ Original│
│ Circuit │
└────┬────┘
     │
     │ 1. Generate QOTP keys
     │    a = [0/1, 0/1, ...]
     │    b = [0/1, 0/1, ...]
     │
     ▼
┌─────────┐
│ Encrypt │
│ X^a Z^b │
└────┬────┘
     │
     │ 2. Send encrypted circuit
     │
     ├──────────────────────────►┌──────────┐
                                 │ Transpile│
                                 └─────┬────┘
                                       │
                                       │ 3. Execute
                                       │    (Homomorphic
                                       │     Evaluation)
                                       │
                                       ▼
                                 ┌──────────┐
                                 │ Measure  │
                                 └─────┬────┘
                                       │
     ┌─────────────────────────────────┤
     │ 4. Return encrypted results     │
     │                                 │
     ▼
┌─────────┐
│ Compute │
│ Final   │
│ Keys    │
└────┬────┘
     │
     │ 5. Decode measurements
     │    with final QOTP keys
     │
     ▼
┌─────────┐
│ Result  │
└─────────┘
```

## Tips

### For Papers/Presentations
1. Use PNG images (high resolution, 300 DPI)
2. Include circuit statistics in captions
3. Show progression: Original → Encrypted → Transpiled

### For Code Documentation
1. Use text diagrams in README files
2. Include circuit statistics
3. Explain gate operations

### For Understanding
1. Start with smallest config (3q-2t)
2. Compare original vs encrypted (notice X^a Z^b gates)
3. Compare encrypted vs transpiled (notice gate explosion)

## Available Configurations

| Config | Qubits | T-depth | Aux States | Complexity |
|--------|--------|---------|------------|------------|
| 3q-2t  | 3      | 2       | 240        | Smallest   |
| 3q-3t  | 3      | 3       | 2,826      | Small      |
| 4q-2t  | 4      | 2       | 668        | Small      |
| 4q-3t  | 4      | 3       | 10,776     | Medium     |
| 5q-2t  | 5      | 2       | 1,350      | Medium     |
| 5q-3t  | 5      | 3       | 31,025     | Largest    |

## Troubleshooting

### Issue: "Style JSON file 'iqx.json' not found"
**Solution**: This is a warning, not an error. The default style will be used instead.

### Issue: Images are too large
**Solution**: The transpiled circuits can be very large (4MB+) due to high gate count. This is normal for IBM hardware.

### Issue: Cannot load IBM backend
**Solution**: The script will automatically fall back to a fake backend for visualization purposes.

### Issue: Text diagrams are hard to read
**Solution**: Use PNG images instead. Text diagrams work best for small circuits (3-4 qubits).

## Command Reference

```bash
# Generate single configuration
python visualize_aux_qhe_circuits.py --config 3q-3t

# Generate all configurations
python visualize_aux_qhe_circuits.py --all

# Specify backend
python visualize_aux_qhe_circuits.py --config 5q-3t --backend ibm_torino

# View generated files
ls circuit_diagrams/*/

# View text diagram
cat circuit_diagrams/3q-3t/01_original_circuit.txt

# Open PNG image (macOS)
open circuit_diagrams/3q-3t/01_original_circuit.png
```

## Related Files

- **[visualize_aux_qhe_circuits.py](visualize_aux_qhe_circuits.py)** - Main script
- **[ibm_hardware_noise_experiment.py](ibm_hardware_noise_experiment.py)** - Hardware execution
- **[compare_local_vs_hardware.py](compare_local_vs_hardware.py)** - Results comparison

---

Generated: 2025-10-11
Status: Ready for use
