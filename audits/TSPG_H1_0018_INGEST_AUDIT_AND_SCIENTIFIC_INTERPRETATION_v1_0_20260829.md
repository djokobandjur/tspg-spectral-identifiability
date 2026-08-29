# TSPG H1-0018 INGEST AUDIT AND SCIENTIFIC INTERPRETATION v1.0

**Date:** 2026-08-29  
**Run:** `TSPG-RUN-H1-0018`  
**Evidence ZIP SHA-256:** `2ab57eeb8c27f229f37ceec1233033cf6c3061dce8943d526cf597f2ede7e567`  
**Integrity:** `27/27 internal SHA checks PASS`  
**Technical status:** `PASS`  
**Scientific classification:** `HYBRID_SAMPLE_SIZE_DECOUPLING`  
**Confirmatory H1:** `BLOCKED`

## Core finite-sample result

H1-0018 separates two effects that do not move together.

### Support coverage

Primary train-n / held-320 coverage rises strongly throughout n=100--320 in
both directions and shows no observed saturation by n=320.

This must **not** be described as complete support estimation. Full-fold
phi remains below one, so a 320-example empirical train span does not cover
all task-gradient support observed in the opposite fold.

No post-hoc linear extrapolation to phi=1 or to a population rank is allowed.
The prospectively locked `a+b/n` n=640 forecast remains planning-only.

### Orientation efficiency

The task-only orientation efficiencies show **no coherent improvement** with
increasing train n.

There are modest gains at some small-k cuts, especially eta4 in the reverse
direction, but the pattern is not dimensionally coherent. Most importantly,
eta32 decreases strongly over the same train-size range:

- AG1->AG2: 0.529716 -> 0.405887
  (Delta=-0.123829)
- AG2->AG1: 0.563551 -> 0.437230
  (Delta=-0.126321)

This is positive evidence against the simple explanation that poor orientation
transfer is caused only by insufficient train sample size in the observed
100--320 range.

## Direct T32 / U32 decomposition

The eta32 decline is not produced by a collapse of the train-fitted numerator.
Both T32 and the held-out oracle ceiling U32 rise with n, but U32 rises much
faster.

AG1->AG2:
- T32: 0.111585 -> 0.142266
  (Delta=+0.030680)
- U32: 0.213154 -> 0.350506
  (Delta=+0.137352)
- U32 absolute gain is 4.48x the T32 absolute gain.

AG2->AG1:
- T32: 0.134591 -> 0.169530
  (Delta=+0.034938)
- U32: 0.239341 -> 0.387736
  (Delta=+0.148395)
- U32 absolute gain is 4.25x the T32 absolute gain.

Thus larger train samples expose substantially more held-out transferable
32-dimensional oracle structure than the unilateral train-fitted top-32
estimator succeeds in capturing.

The AG1->AG2 eta32 sequence is not mathematically strictly monotone because
224->256 increases by less than 0.001, but the net decline is large and the
upper-range planning forecast continues downward. AG2->AG1 declines throughout
the locked ladder.

## Secondary held-out-size diagnostic

When train is fixed at 320 and the held-out operator is subsampled, eta changes
substantially. Therefore eta is not intrinsically insensitive to sample size.

The correct interpretation is `held-out finite-sample sensitivity`, not pure
scoring variance: changing the held-out sample changes both the estimated
held-out oracle and the score.

This provides an internal control for the primary result: support coverage
responds strongly to train n, and held-out eta responds to held-out n, but
orientation efficiency does not show a corresponding coherent improvement
with train n.

## Planning-only n=640 expectations

The prospectively locked inverse-n forecasts remain planning-only.

They predict only modest further small-k unilateral gains and a slight further
decline at k=32. These forecasts are useful as expectations before a possible
H19 run but are never substitutes for the actual unilateral-640 arm.

## Scientific conclusion

> Across a more than three-fold train-sample range, held-out support coverage
> increases strongly without observed saturation, while low-dimensional
> orientation transfer shows no coherent improvement and top-32 orientation
> efficiency decreases by approximately 0.12 in both directions. The observed
> orientation failure is therefore not explained by train sample size within
> the measured range.

This result supports proceeding, if separately authorized, to the final H19
question: whether an explicitly common-structure estimator can recover a
third-fold-transferable orientation that unilateral estimators do not.

H19 is not authorized by this audit.
