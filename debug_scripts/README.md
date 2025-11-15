# Debug Scripts

This folder contains debugging and diagnostic scripts used during AUX-QHE development.

## Files

### Hardware Debugging
- **debug_before_hardware.py** - Pre-flight validation before hardware execution
- **debug_5q2t_before_hardware.py** - Specific debugging for 5q-2t configuration
- **debug_hardware_workflow.py** - Hardware execution workflow debugging
- **comprehensive_pre_execution_debug.py** - Comprehensive pre-execution validation

### QOTP Decryption Debugging (Oct 30, 2024)
These scripts were created to fix the critical QOTP decryption bit-ordering bug:

- **debug_key_evolution.py** - Verified aux_eval() returns correct final QOTP keys
- **debug_bit_ordering.py** - Identified Qiskit's qubit 0 = rightmost convention
- **debug_extraction.py** - Traced bit extraction logic step-by-step

### Other
- **debug_bfv_eval.py** - BFV homomorphic encryption debugging
- **test_debug_logging.py** - Debug logging system tests

## Bug Fix History

### QOTP Decryption Bit Ordering (Oct 30, 2024)
**Problem:** Local simulation showed 0% fidelity due to incorrect bit ordering in decryption.

**Root Cause:** Qiskit bitstrings have qubit 0 at the RIGHTMOST position, but decryption was XORing bits without accounting for this.

**Solution:** Modified decryption to:
1. Extract values: `extracted_values[i] = bitstring[-(physical_qubits[i] + 1)]`
2. XOR directly: `decoded_values[i] = extracted_values[i] ^ final_a[i]`
3. Reverse for output: `decoded_bits = ''.join(str(decoded_values[num_qubits-1-i])...)`

**Verification:** Local simulation achieved TVD=0.000000 (perfect).

## Usage

These scripts are for development/debugging only and are not part of the main execution pipeline.

To use:
```bash
python debug_scripts/<script_name>.py
```
