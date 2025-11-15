# Auxiliary States for Polynomial Sums - Theory vs Implementation

## The Problem

After the first T-gate on qubit 0, we have:
- `f_a[0] = 'b0 + c0_1'` (a polynomial sum)

When we apply the second T-gate, we need an auxiliary state for this polynomial.

## Current Implementation (WRONG)

The code tries to look up `auxiliary_states[(2, 0, 'b0 + c0_1')]`, but:
- T[2] contains **products** like `'b0*c0_1'`, not sums like `'b0 + c0_1'`
- The auxiliary lookup fails or returns incorrect state

## Theoretical Solution

According to AUX-QHE theory, the auxiliary state for a polynomial f should be:

```
|+_{s,k}⟩ where s = f AND k = f
```

For f_a = 'b0 + c0_1' with b0=1, c0_1=1:
- Evaluated value: f = 1 ⊕ 1 = 0
- Auxiliary state: |+_{s=0, k=0}⟩ = H|0⟩ = |+⟩
- Measurement outcome: c = k = 0

## Implementation Fix

Instead of looking up auxiliary by polynomial string, we should:

1. **Evaluate the polynomial** using current variable values
2. **Use the evaluated value** to determine s and k
3. **Construct auxiliary** as |+_{s=f, k=f}⟩

This matches the theory: the auxiliary state encodes the **current value** of the polynomial, not its symbolic form.

## Code Changes Needed

In `update_keys_for_t_gate`:

```python
# OLD (WRONG):
aux_state = auxiliary_states.get((layer, wire, f_a_polynomial))

# NEW (CORRECT):
f_a_value = evaluate_term(f_a_polynomial, variable_values)
aux_k = f_a_value  # k equals the polynomial value
aux_s = f_a_value  # s equals the polynomial value
# Construct auxiliary |+_{s,k}⟩ on-the-fly
```

This way, we don't need to pre-generate auxiliary states for all possible polynomial sums - we just evaluate and construct on-demand.
