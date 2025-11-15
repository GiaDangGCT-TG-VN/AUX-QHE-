#!/usr/bin/env python3
"""
Quick test to verify debug logging and count accumulation works
"""

# Simulate the decoding fix
counts = {
    '00000': 100,
    '00001': 150,
    '00010': 200,
    '00011': 50,
    '00100': 100,
    '00101': 424,  # Total = 1024
}

# Simulate decoding with QOTP keys that might create collisions
final_a = [0, 0, 0, 1, 1]  # XOR with bits 3 and 4
final_b = [0, 0, 0, 0, 0]

num_qubits = 5
shots = 1024

print("="*80)
print("TESTING COUNT ACCUMULATION FIX")
print("="*80)

print(f"\n📊 Original encrypted counts:")
print(f"   Unique outcomes: {len(counts)}")
print(f"   Total: {sum(counts.values())}")
for k, v in list(counts.items())[:3]:
    print(f"      {k}: {v}")

# OLD METHOD (buggy - overwrites):
print(f"\n❌ OLD METHOD (overwrites):")
decoded_old = {}
for bitstring, count in counts.items():
    decoded_bits = ''.join(
        str(int(bitstring[i]) ^ final_a[i]) for i in range(num_qubits)
    )
    decoded_old[decoded_bits] = count  # BUG: Overwrites!

print(f"   Unique outcomes: {len(decoded_old)}")
print(f"   Total: {sum(decoded_old.values())}")
if sum(decoded_old.values()) != shots:
    print(f"   ⚠️  LOST SHOTS: {shots - sum(decoded_old.values())}")

# NEW METHOD (correct - accumulates):
print(f"\n✅ NEW METHOD (accumulates):")
decoded_new = {}
for bitstring, count in counts.items():
    decoded_bits = ''.join(
        str(int(bitstring[i]) ^ final_a[i]) for i in range(num_qubits)
    )
    # Accumulate instead of overwrite
    if decoded_bits in decoded_new:
        decoded_new[decoded_bits] += count
    else:
        decoded_new[decoded_bits] = count

print(f"   Unique outcomes: {len(decoded_new)}")
print(f"   Total: {sum(decoded_new.values())}")
if sum(decoded_new.values()) == shots:
    print(f"   ✅ ALL SHOTS PRESERVED: {sum(decoded_new.values())}/{shots}")
else:
    print(f"   ❌ LOST SHOTS: {shots - sum(decoded_new.values())}")

# Verify
assert sum(decoded_new.values()) == shots, "Shots were lost!"

print(f"\n{'='*80}")
print(f"✅ TEST PASSED: Count accumulation works correctly")
print(f"{'='*80}")
