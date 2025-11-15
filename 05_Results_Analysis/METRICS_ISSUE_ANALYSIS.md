# Fidelity Metrics Issue Analysis

## Problem Summary

The fidelity metrics from IBM hardware execution appear incorrect:

```
method  Baseline     Opt-3  Opt-3+ZNE       ZNE
config
3q-3t   0.054289  0.054289   0.054289  0.018306
4q-3t   0.020833  0.044643   0.008929  0.012500
5q-2t   0.020833  0.017913   0.031250  0.022321
5q-3t   0.020238  0.017782   0.004464  0.008523
```

### Issues Identified:

1. **Fidelity too low** (< 5%, should be higher even with noise)
2. **ZNE worse than baseline** (should improve, not worsen)
3. **Identical fidelity across methods** (3q-3t: Baseline = Opt-3 = 0.054289)
4. **Counter-intuitive patterns** (Opt-3 sometimes much worse)

## Root Cause Analysis

### Diagnostic Results:

Running `diagnose_metrics.py` revealed:

```
📊 Measurement Distribution Analysis
   Num qubits: 5
   Num unique outcomes: 6
   Expected max outcomes: 32
   Entropy: 2.5850 / 5.0000

   Top 5 outcomes:
      01001: 1 (16.67%)
      01011: 1 (16.67%)
      11001: 1 (16.67%)
      00001: 1 (16.67%)
      01000: 1 (16.67%)

   Coefficient of variation: 0.0000
   ⚠️  WARNING: Distribution is very uniform (CV < 0.3)
      This might indicate a decoding issue!
```

### Critical Finding:

**Each outcome has exactly 1 count**, despite 1024 shots!

This means:
- Only 6-9 unique outcomes observed (out of 32 possible for 5 qubits)
- Each outcome has count = 1
- Total counts = 6-9 (should be 1024)

## Possible Causes

### 1. Measurement Retrieval Issue (MOST LIKELY)

**Problem**: The `counts` dictionary from IBM might contain the wrong data structure.

**Location**: `ibm_hardware_noise_experiment.py:283-291`

```python
quasi_dist = result[0].data.meas.get_counts()
# Handle both string and integer keys from get_counts()
counts = {}
for k, v in quasi_dist.items():
    if isinstance(k, str):
        bitstring = k
    else:
        bitstring = format(int(k), f'0{num_qubits}b')
    counts[bitstring] = v
```

**Hypothesis**: `quasi_dist` might be returning something other than shot counts.

### 2. QOTP Decoding Issue

**Problem**: Measurement decoding might be creating duplicate keys.

**Location**: `ibm_hardware_noise_experiment.py:330-337`

```python
decoded_counts = {}
for bitstring, count in counts.items():
    decoded_bits = ''.join(
        str(int(bitstring[i]) ^ final_a[i]) for i in range(num_qubits)
    )
    decoded_counts[decoded_bits] = count
```

**Issue**: If multiple encrypted bitstrings decode to the same plain bitstring, only the last count is kept (dictionary overwrite).

### 3. Ideal State Mismatch

**Problem**: Comparing against wrong ideal state.

**Location**: `ibm_hardware_noise_experiment.py:346`

```python
ideal_state = Statevector(qc)  # Using ORIGINAL circuit
```

**Issue**: Should we compare against the encrypted circuit or original? Currently using original `qc`, but we're executing the encrypted circuit.

## Recommended Fixes

### Fix 1: Debug Measurement Retrieval

Add logging to see what's actually in the counts:

```python
# After getting counts from IBM
print(f"   🔍 DEBUG: Raw quasi_dist type: {type(quasi_dist)}")
print(f"   🔍 DEBUG: Quasi_dist keys (first 3): {list(quasi_dist.keys())[:3]}")
print(f"   🔍 DEBUG: Quasi_dist values (first 3): {list(quasi_dist.values())[:3]}")
print(f"   🔍 DEBUG: Sum of counts: {sum(counts.values())}")
print(f"   🔍 DEBUG: Expected sum (shots): {shots}")

# Verify counts sum matches shots
if abs(sum(counts.values()) - shots) > 10:
    print(f"   ⚠️  WARNING: Counts sum ({sum(counts.values())}) != shots ({shots})")
```

### Fix 2: Handle Decoding Collisions

Accumulate counts when multiple bitstrings decode to same value:

```python
decoded_counts = {}
for bitstring, count in counts.items():
    decoded_bits = ''.join(
        str(int(bitstring[i]) ^ final_a[i]) for i in range(num_qubits)
    )
    # Accumulate instead of overwrite
    if decoded_bits in decoded_counts:
        decoded_counts[decoded_bits] += count
    else:
        decoded_counts[decoded_bits] = count

# Verify no shots lost
assert sum(decoded_counts.values()) == sum(counts.values()), "Shots lost in decoding!"
```

### Fix 3: Verify Ideal State

The ideal state should be the **original circuit** (what we want to compute), not the encrypted one:

```python
# Correct: Compare decoded measurements against original circuit
ideal_state = Statevector(qc)  # qc is the original circuit
```

This is actually correct as-is.

### Fix 4: Check IBM API Changes

The Sampler API might have changed. Verify the result format:

```python
result = job.result()
print(f"   🔍 DEBUG: Result type: {type(result)}")
print(f"   🔍 DEBUG: Result[0] type: {type(result[0])}")
print(f"   🔍 DEBUG: Result[0].data: {result[0].data}")
print(f"   🔍 DEBUG: Result[0].data.meas type: {type(result[0].data.meas)}")
```

## Testing Plan

1. **Add debug logging** to see actual counts from IBM
2. **Run single test** (3q-3t) and examine output
3. **Check if counts sum to shots**
4. **Verify decoding doesn't lose shots**
5. **Compare encrypted vs decoded distributions**

## Expected Behavior

With 1024 shots:
- Should see dozens to hundreds of unique outcomes
- Counts should sum to exactly 1024
- Most frequent outcomes should have counts > 1
- Distribution should NOT be uniform (real quantum noise creates bias)

## Next Steps

1. ✅ Run diagnostic script (`diagnose_metrics.py`) - DONE
2. ⏳ Add debug logging to measurement retrieval
3. ⏳ Test with single configuration
4. ⏳ Implement fixes based on findings
5. ⏳ Re-run experiments

---

Created: 2025-10-11
Status: Issue identified, fixes pending
