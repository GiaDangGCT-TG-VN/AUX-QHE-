# AUX-QHE: Auxiliary Quantum Homomorphic Encryption

**Experimental Validation of AUX scheme for Quantum Homomorphic Encryption on IBM Quantum Platforms**

[![Paper](https://img.shields.io/badge/Paper-QCNC%202026-blue)](QCNC_2026)
[![IBM Quantum](https://img.shields.io/badge/IBM%20Quantum-Tested-green)](https://quantum.ibm.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Qiskit](https://img.shields.io/badge/Qiskit-Latest-purple.svg)](https://qiskit.org/)

## 📄 About

This repository contains the complete implementation and experimental validation of the **AUX-QHE (Auxiliary Quantum Homomorphic Encryption)** scheme on IBM Quantum hardware platforms.

**Paper Submitted to:** QCNC 2026 Conference
**Research Focus:** Blind quantum computation using auxiliary states for T-gate evaluation

## 🎯 Key Features

- ✅ **Complete AUX-QHE Implementation** - Full protocol with QOTP encryption
- ✅ **IBM Quantum Hardware Validation** - Tested on ibm_torino (133 qubits)
- ✅ **Multiple Test Configurations** - 4-5 qubits, T-depths L=2,3
- ✅ **4 Error Mitigation Strategies** - Baseline, ZNE, Opt-3, Opt-3+ZNE
- ✅ **Comprehensive Testing Suite** - Local validation before hardware execution
- ✅ **Results Analysis Tools** - LaTeX table generation, visualization

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/AUX-QHE.git
cd AUX-QHE

# Install dependencies
pip install qiskit qiskit-ibm-runtime numpy pandas matplotlib seaborn

# Configure IBM Quantum account
# Edit your IBM credentials in the script or use environment variables
```

### Run Local Validation

```bash
# Test locally before using IBM credits
python test_hardware_script_local.py
```

### Run Hardware Experiment

```bash
# Execute on IBM Quantum hardware
python ibm_hardware_noise_experiment.py \
    --config 5q-2t \
    --backend ibm_torino \
    --account YOUR_ACCOUNT_NAME
```

### View Latest Results

```bash
# Check results table
cat hardware_noise_results_table.md

# View detailed results
ls results/hardware_2025_10_30/
```

## 📊 Experimental Results

### Hardware Performance (ibm_torino, Oct 2025)

| Config | Aux States | Best Method | Fidelity | TVD |
|--------|-----------|-------------|----------|-----|
| 5q-2t  | 575       | Opt-3+ZNE   | 37.82%   | 0.244 |
| 4q-3t  | 10,776    | Baseline    | 12.22%   | 0.169 |
| 5q-3t  | 31,025    | Opt-3+ZNE   | 13.05%   | 0.111 |

**Key Findings:**
- ✅ QOTP decryption verified correct (79% shots in expected outcomes)
- ✅ T-depth=2 achieves 3x better fidelity than T-depth=3
- ✅ Error mitigation effectiveness varies by configuration
- ✅ Demonstrates NISQ hardware limits for T-depth ≥ 3

## 📁 Repository Structure

```
AUX-QHE/
├── README.md                              # Main documentation
├── QUICK_START.md                         # Quick start guide
├── ibm_hardware_noise_experiment.py       # Main execution script
├── test_hardware_script_local.py          # Local validation
├── hardware_noise_results_table.md        # Latest results
│
├── core/                                  # Core algorithm
│   ├── bfv_core.py                       # BFV encryption
│   ├── circuit_evaluation.py             # Circuit evaluation
│   ├── key_generation.py                 # Key generation
│   ├── openqasm3_integration.py          # QASM integration
│   ├── qotp_crypto.py                    # QOTP encryption/decryption
│   └── t_gate_gadgets.py                 # T-gate gadgets
│
├── results/                               # Experimental results
│   └── hardware_2025_10_30/              # Latest hardware results
│
├── 05_Results_Analysis/                   # Analysis tools
│   ├── analysis_scripts/                 # Analysis scripts
│   ├── table_scripts/                    # Table generation
│   └── visualization_scripts/            # Visualization
│
├── 06_Testing_Scripts/                    # Testing suite
│   ├── core_tests/                       # Core algorithm tests
│   ├── hardware_tests/                   # Hardware tests
│   ├── pipeline_tests/                   # Pipeline tests
│   └── tdepth_tests/                     # T-depth tests
│
└── 07_Quick_Guides/                       # Guides & utilities
    ├── utility_scripts/                  # Utilities
    ├── execution_scripts/                # Execution scripts
    └── ibm_setup/                        # IBM setup guides
```

## 🔬 Research Highlights

### Algorithm Implementation

**AUX-QHE Protocol:**
1. **Key Generation** - Generate QOTP keys and auxiliary states for T-gates
2. **Encryption** - QOTP encrypt circuit with X^a Z^b gates
3. **Evaluation** - Execute encrypted circuit on IBM Quantum hardware
4. **Decryption** - Homomorphically decrypt using final QOTP keys

**Test Circuits:**
- Single-qubit Clifford gates (H, S)
- CNOT gates for entanglement
- T gates (non-Clifford, requiring auxiliary states)

### Critical Bug Fix (Oct 2025)

**Issue:** QOTP decryption had bit-ordering mismatch
- Qiskit bitstrings: qubit 0 at RIGHTMOST position
- Decryption was XORing bits without accounting for ordering

**Fix:**
```python
# Extract values with correct bit ordering
extracted_values[i] = bitstring[-(physical_qubits[i] + 1)]
decoded_values[i] = extracted_values[i] ^ final_a[i]
```

**Verification:** Local simulation achieved TVD=0.000000 (perfect)

## 📈 Error Mitigation Strategies

1. **Baseline** (opt_level=1) - No error mitigation
2. **ZNE** (Zero-Noise Extrapolation) - Richardson extrapolation
3. **Opt-3** (opt_level=3) - Heavy circuit optimization
4. **Opt-3+ZNE** - Combined optimization + ZNE

## 🛠️ Tools & Technologies

- **Qiskit** - Quantum circuit framework
- **IBM Quantum Runtime** - Hardware execution
- **BFV Scheme** - Classical homomorphic encryption component
- **OpenQASM 3.0** - Circuit representation
- **Python 3.9+** - Implementation language

## 📚 Citation

If you use this code in your research, please cite:

```bibtex
@inproceedings{auxqhe2026,
  title={Experimental Validation of AUX scheme for Quantum Homomorphic Encryption on IBM Quantum Platforms},
  author={[Your Name]},
  booktitle={QCNC 2026},
  year={2026}
}
```

## 📝 License

[Your License Here - e.g., MIT, Apache 2.0]

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

[Your Contact Information]

## 🙏 Acknowledgments

- IBM Quantum for providing access to quantum hardware
- QCNC 2026 conference organizers
- [Your institution/collaborators]

---

**Status:** ✅ Code verified on IBM Quantum hardware (October 2025)
**Paper:** Submitted to QCNC 2026
