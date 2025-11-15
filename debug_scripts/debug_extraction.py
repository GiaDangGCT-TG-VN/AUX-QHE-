#!/usr/bin/env python3
"""
Debug the bit extraction and decryption logic
"""

print('='*80)
print('BIT EXTRACTION AND DECRYPTION DEBUG')
print('='*80)
print()

# Scenario 1: Local simulation (5 qubits)
print('SCENARIO 1: Local simulation (5 qubits)')
print('-'*80)

bitstring = '00010'  # Qiskit measurement
physical_qubits = [0, 1, 2, 3, 4]  # Identity mapping
final_a = [0, 1, 0, 0, 0]  # From aux_eval

print(f'Bitstring from Qiskit: {bitstring}')
print(f'Physical qubits: {physical_qubits}')
print(f'final_a (logical order): {final_a}')
print()

print('Qiskit convention: qubit 0 is RIGHTMOST')
print(f'  {bitstring} means:')
print(f'    qubit 0 = {bitstring[4]} (rightmost)')
print(f'    qubit 1 = {bitstring[3]}')
print(f'    qubit 2 = {bitstring[2]}')
print(f'    qubit 3 = {bitstring[1]}')
print(f'    qubit 4 = {bitstring[0]} (leftmost)')
print()

# Current extraction
extracted = ''.join(bitstring[-(physical_qubits[i] + 1)] for i in range(5))
print(f'Current extraction: {extracted}')
print('  Breakdown:')
for i in range(5):
    idx = -(physical_qubits[i] + 1)
    print(f'    i={i}: bitstring[{idx}] = {bitstring[idx]}')
print()

# What we need for decryption
print('For correct decryption:')
print('  We need: bitstring_value XOR final_a_value = original_value')
print('  Bitstring values: qubit 0=0, qubit 1=1, qubit 2=0, qubit 3=0, qubit 4=0')
print(f'  final_a values: {final_a}')
print('  XOR result should give us the original unencrypted state')
print()

# The correct way
print('CORRECT METHOD:')
print('  For each logical qubit i:')
print('    1. Get physical qubit number: physical_qubits[i]')
print('    2. Extract bit from bitstring at that physical position')
print('    3. XOR with final_a[i]')
print()

result_bits = []
for i in range(5):
    phys_qubit = physical_qubits[i]
    # Qiskit: qubit N is at position -(N+1)
    bit_value = int(bitstring[-(phys_qubit + 1)])
    decoded_bit = bit_value ^ final_a[i]
    result_bits.append(str(decoded_bit))
    print(f'  Logical qubit {i}: physical={phys_qubit}, bit={bit_value}, final_a={final_a[i]}, decoded={decoded_bit}')

decoded_result = ''.join(result_bits)
print()
print(f'Decoded result: {decoded_result}')
print(f'Expected: 00000 or 00011')
print()

# Check if this matches our expectation
if decoded_result in ['00000', '00011']:
    print('✅ Decryption works!')
else:
    print('❌ Decryption failed!')
    print()
    print('The extracted_bits string is in REVERSED order!')
    print('We need to reverse final_a when XORing, OR reverse extracted_bits first')
