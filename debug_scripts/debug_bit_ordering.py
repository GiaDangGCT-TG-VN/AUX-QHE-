#!/usr/bin/env python3
"""
Debug bit ordering in Qiskit measurements vs key indices
"""

print('='*80)
print('BIT ORDERING DEBUG')
print('='*80)
print()

# Qiskit measurement strings
encrypted1 = '00010'  # First measurement
encrypted2 = '00001'  # Second measurement

print('Encrypted measurements from Qiskit:')
print(f'  {encrypted1}')
print(f'  {encrypted2}')
print()

print('Qiskit bit ordering: qubit 0 is RIGHTMOST')
print('  Position: 43210')
print(f'  String:   {encrypted1}')
print(f'  Qubit 0 = {encrypted1[4]} (rightmost)')
print(f'  Qubit 1 = {encrypted1[3]}')
print(f'  Qubit 2 = {encrypted1[2]}')
print(f'  Qubit 3 = {encrypted1[1]}')
print(f'  Qubit 4 = {encrypted1[0]} (leftmost)')
print()

# Expected decrypted outcomes
expected1 = '00000'
expected2 = '00011'

print('Expected decrypted outcomes:')
print(f'  {expected1}')
print(f'  {expected2}')
print()

# Compute required final_a
print('Computing required final_a to decrypt correctly:')
print('  encrypted ⊕ final_a = expected')
print('  final_a = encrypted ⊕ expected')
print()

final_a_bits1 = ''.join(str(int(encrypted1[i]) ^ int(expected1[i])) for i in range(5))
final_a_bits2 = ''.join(str(int(encrypted2[i]) ^ int(expected2[i])) for i in range(5))

print(f'  From measurement 1: {encrypted1} ⊕ {expected1} = {final_a_bits1}')
print(f'  From measurement 2: {encrypted2} ⊕ {expected2} = {final_a_bits2}')
print()

if final_a_bits1 == final_a_bits2:
    print(f'✅ Both give same final_a: {final_a_bits1}')
    print()
    print('Converting to list (qubit 0 is RIGHTMOST):')
    # Reverse to get [qubit0, qubit1, qubit2, qubit3, qubit4]
    final_a_list = [int(final_a_bits1[4-i]) for i in range(5)]
    print(f'  final_a = {final_a_list}')
    print(f'  (qubit 0={final_a_list[0]}, qubit 1={final_a_list[1]}, etc.)')
else:
    print('❌ Measurements give different final_a - something is wrong!')
print()

print('='*80)
print('What aux_eval() returns:')
print('  final_a = [0, 1, 0, 0, 0]')
print(f'What we NEED:')
print(f'  final_a = {final_a_list}')
print()

if final_a_list == [0, 1, 0, 0, 0]:
    print('✅ Match! aux_eval() is correct.')
else:
    print('❌ Mismatch! aux_eval() is computing wrong keys.')
    print()
    print('Checking if its a bit ordering issue...')
    final_a_reversed = final_a_list[::-1]
    print(f'  final_a reversed = {final_a_reversed}')
    if final_a_reversed == [0, 1, 0, 0, 0]:
        print('  ✅ It IS a bit ordering issue!')
        print('  aux_eval() returns keys in reversed order!')
    else:
        print('  ❌ Not just bit ordering - keys are actually wrong')
