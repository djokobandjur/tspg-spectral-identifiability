# TSPG H1-0017 FORMAL CLOSEOUT REPORT v1.0

**Date:** 2026-08-29  
**Run:** `TSPG-RUN-H1-0017`  
**Formal status:** `CLOSED_PASS_DIAGNOSTIC_NEGATIVE`  
**Confirmatory H1:** `BLOCKED`

## Integrity

The authoritative H1-0017 v1.1 evidence package passed all compact-evidence
SHA checks and all corrected A47/IC05 numerical certification gates.

The run was fully offline:
- model load: 0;
- GPU scientific compute: 0;
- new task gradients: 0;
- new `G_A` actions: 0.

## Scientific result

The motivating question was whether the locked `B11` metric selects a more
cross-image reproducible task-sensitive orientation inside AG1 task support.

The answer is **no**.

Across every locked k in `{1,2,4,8,16,32}`:

- `Delta_sel|task = eta_task(S_B) - eta_task(S_E)` is negative;
- `Delta_sel|B = eta_B(S_B) - eta_B(S_E)` is positive.

The positive B-scoring gain is accompanied by an extreme reduction in
Euclidean-unit B response. The selected `S_B` spans have roughly 75x--406x
lower mean B response than the corresponding Euclidean task spans.

Therefore the B-scoring gain is classified as primarily
`DENOMINATOR_SELECTIVE`, not as improved cross-image task transfer.

The B-principal-angle diagnostics also do not support a reproducible
generalized top-k subspace. The minimum B-principal cosine decreases from about
0.494 at k=1 to about 0.008 at k=32.

## Prospective prediction audit

The `predictions_not_gates` field in the runtime result is retained unchanged
because it records the predictions made before execution. Their observed
outcomes are:

1. `eta_B(S_B)` exceeds the pre-existing task-only `eta_task(S_E)` at small k:
   **NOT SUPPORTED** as a general low-k pattern; it is mixed and holds clearly
   only at k=1.
2. `Delta_sel|B > 0` over much of the low-k ladder:
   **SUPPORTED**; positive at all six locked k.
3. `Delta_sel|task > 0` as denominator-independent corroboration:
   **NOT SUPPORTED**; negative at all six locked k.
4. held-out `gamma_k` small at the smallest cuts and larger by k=32:
   **NOT SUPPORTED**.
5. B-principal angles largest at k=1--2 and then improve:
   **NOT SUPPORTED**.

## Closed interpretation

H1-0017 closes the proposed B-normalized remedy:

> The shared attention metric does not solve the cross-fold orientation
> problem; its apparent gain under B-normalized scoring is driven primarily by
> selection of directions with very small B response.

This does not invalidate the shared task support or held-out oracle ceilings
observed in H1-0016. It invalidates the narrower estimator
`top-k(C1,B11)` as the reproducible C1 subspace estimator.

The next authorized step is H1-0018, a zero-new-gradient finite-sample support
and orientation stability audit.
