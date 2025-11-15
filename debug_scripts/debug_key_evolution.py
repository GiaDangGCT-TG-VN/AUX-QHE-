#!/usr/bin/env python3
"""
Debug script to trace QOTP key evolution through the circuit
"""

print('='*80)
print('MANUAL KEY EVOLUTION TRACE')
print('='*80)
print()

# Initial keys
f_a = ['a0', 'a1', 'a2', 'a3', 'a4']
f_b = ['b0', 'b1', 'b2', 'b3', 'b4']
values = {'a0': 1, 'a1': 1, 'a2': 0, 'a3': 0, 'a4': 0,
          'b0': 0, 'b1': 0, 'b2': 0, 'b3': 0, 'b4': 1}

print('Initial state:')
print(f'  f_a = {f_a}')
print(f'  f_b = {f_b}')
print(f'  Initial a_values = [1, 1, 0, 0, 0]')
print(f'  Initial b_values = [0, 0, 0, 0, 1]')
print()

# Gate 1: H(0)
print('Gate 1: H(0) - Swap f_a[0] and f_b[0]')
f_a[0], f_b[0] = f_b[0], f_a[0]
print(f'  f_a = {f_a}')
print(f'  f_b = {f_b}')
print()

# Gate 2: CX(0,1)
print('Gate 2: CX(0,1)')
print('  Rule: f_b[control=0] <- f_b[0] XOR f_b[1]')
print('  Rule: f_a[target=1] <- f_a[1] XOR f_a[0]')

# f_b[0] = f_b[0] + f_b[1]
if f_b[1] and f_b[1] != '0':
    f_b[0] = f'{f_b[0]} + {f_b[1]}' if f_b[0] and f_b[0] != '0' else f_b[1]

# f_a[1] = f_a[1] + f_a[0]
if f_a[0] and f_a[0] != '0':
    f_a[1] = f'{f_a[1]} + {f_a[0]}' if f_a[1] and f_a[1] != '0' else f_a[0]

print(f'  f_a = {f_a}')
print(f'  f_b = {f_b}')
print()

# Evaluate the polynomials with the initial values
def evaluate_poly(poly_str, values):
    if not poly_str or poly_str == '0':
        return 0

    # Split by + and evaluate each term
    terms = [t.strip() for t in str(poly_str).split('+')]
    result = 0
    for term in terms:
        if term in values:
            result ^= values[term]  # XOR for mod 2
        elif term.isdigit():
            result ^= int(term)
    return result

print('='*80)
print('EVALUATION (before T-gates):')
print('='*80)
for i in range(5):
    val = evaluate_poly(f_a[i], values)
    print(f'  f_a[{i}] = {f_a[i]:20s} -> {val}')

final_a_before_t = [evaluate_poly(f_a[i], values) for i in range(5)]
print()
print(f'Keys after H and CX (before T-gates): {final_a_before_t}')
print()

print('='*80)
print('EXPECTED BEHAVIOR:')
print('='*80)
print('Our circuit: H(0), CX(0,1), T(0)x3')
print()
print('For QOTP, the circuit should behave like:')
print('  Input: |00000> encrypted as |11000> (with a=[1,1,0,0,0])')
print('  After gates: still produces |00000> or |00011>')
print('  Final keys should decrypt: |encrypted> XOR final_a = |original>')
print()
print('The T-gates should NOT change the f_a polynomial significantly')
print('because T only affects phases (f_b), not computational basis (f_a)')
print()
print(f'Expected final_a ≈ {final_a_before_t} (unchanged by T-gates)')
print()
print('But aux_eval() returns final_a = [0, 1, 0, 0, 0]')
print('This is WRONG! Should be [0, 1, 0, 0, 0] after H and CX')
print()
print('Wait... [0, 1, 0, 0, 0] IS correct after H and CX!')
print('So the problem must be in the ENCRYPTION step, not aux_eval()!')
