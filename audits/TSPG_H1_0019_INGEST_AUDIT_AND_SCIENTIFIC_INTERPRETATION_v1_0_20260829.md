# TSPG H1-0019 INGEST AUDIT AND SCIENTIFIC INTERPRETATION v1.0

**Date:** 2026-08-29  
**Run:** `TSPG-RUN-H1-0019`  
**Role:** prospectively final estimator attempt  
**Evidence ZIP:** `TSPG_H1_0019_RUNTIME_EVIDENCE_v1_0_20260829.zip`  
**Evidence ZIP SHA-256:** `f9eaadb43d0054a7d90714f2305b3e34fe3d47eaa34513659e4aed5ab09e62da`  
**ZIP integrity:** `PASS`  
**Internal compact-evidence SHA checks:** `32/32 PASS`  
**Technical status:** `PASS`  
**Scientific status:** `CONSENSUS_NOT_ESTABLISHED_STOP_ESTIMATOR_SEARCH`  
**Confirmatory H1:** `BLOCKED`

## Fit-lock and AP-use integrity

The fit-only stage passed before AP task gradients existed:

- AP task gradients before fit lock: `0`
- pooled fit rank: `640`
- fit-lock SHA-256:
  `9d8d7fa7649f21a24d980172791c350dfae73c768ba7ab48a0d98b85180a8390`
- maximum arm orthonormality error:
  `2.887e-15`
- consensus fold-swap relative Frobenius error:
  `0.000e+00`

AP semantic gate:

- unique AP classes: `99/100`
- AP∩AG1 class count: `97/100`
- AP∩AG2 class count: `97/100`
- gate: `PASS`

The full stage then computed exactly 640 new AP FP64 task gradients.
AP is therefore consumed as a C1-development held-out set.

## Actual sample-size control

The actual pooled unilateral-640 estimator outperformed the arithmetic mean of
the two unilateral-320 estimators at every primary rank:

| k | U320 mean | U640 | Delta_sample |
|---:|---:|---:|---:|
| 4 | 0.044021 | 0.060132 | +0.016112 |
| 8 | 0.070005 | 0.091775 | +0.021770 |
| 16 | 0.105374 | 0.138207 | +0.032833 |
| 32 | 0.146351 | 0.184331 | +0.037980 |

Thus additional fit data have a real positive effect on third-fold task
capture. The H19 same-sample-size U640 control was necessary and informative.

## Consensus-versus-U640 result

The locked denominator-free consensus arm did **not** satisfy the prospective
success rule:

| k | U640 | CONS640 | Delta_cons | paired 95% CI |
|---:|---:|---:|---:|---:|
| 4 | 0.060132 | 0.065636 | +0.005504 | [+0.002737, +0.008215] |
| 8 | 0.091775 | 0.092719 | +0.000944 | [-0.003222, +0.004695] |
| 16 | 0.138207 | 0.129224 | -0.008983 | [-0.013834, -0.004297] |
| 32 | 0.184331 | 0.186578 | +0.002247 | [-0.001102, +0.005815] |

The decisive failures are:

1. pointwise positivity fails at `k=16`:
   `Delta_cons(16)=-0.008983`;
2. the k=16 paired 95% CI is entirely negative:
   `[-0.013834,
     -0.004297]`;
3. the prespecified curve-mean contrast is essentially zero:
   `Delta_curve=-0.00007214`;
4. its paired-bootstrap 95% CI crosses zero:
   `[-0.002306,
     +0.002166]`.

Therefore the locked result status
`CONSENSUS_NOT_ESTABLISHED_STOP_ESTIMATOR_SEARCH`
is the correct application of the prospective stopping rule.

The pattern is not a near-miss hidden by the curve average. The consensus arm
has one clearly positive rank (`k=4`), one clearly negative rank (`k=16`), and
two ranks whose paired intervals include zero (`k=8,32`). It therefore does
not define a rank-robust third-fold advantage over actual unilateral-640.

## Denominator-preference safety diagnostic

Unlike H1-0017, H1-0019 does **not** show a large B-response imbalance between
CONS640 and U640:

| k | bbar(CONS640) / bbar(U640) |
|---:|---:|
| 4 | 1.0320 |
| 8 | 0.9979 |
| 16 | 0.9578 |
| 32 | 1.0195 |

The ratios stay within approximately ±4.3% of one. The quadratic-consistency
checks for every B-response block are at approximately 1e-15.

Therefore H1-0019 failure cannot be attributed to the H1-0017 small-denominator
artifact. The consensus estimator is genuinely not superior under the
denominator-independent AP task criterion.

## Fit-side interpretation

At top-32, the pooled unilateral estimator captures more energy in both fit
folds than the consensus estimator:

- U640: AG1 `0.6454`,
  AG2 `0.5489`;
- CONS640: AG1 `0.5755`,
  AG2 `0.4709`.

The consensus construction therefore trades fold-wise task energy for
commonness, as intended, but that trade does not produce a robust AP transfer
advantage.

## Closed scientific interpretation

H1-0019 answers the final estimator question negatively:

> Explicitly weighting common AG1/AG2 task structure with the prospectively
> locked denominator-free consensus operator does not produce a rank-robust
> third-fold advantage over an ordinary unilateral estimator trained on the
> same 640 examples.

Together with H1-0011--H1-0018, the development sequence now supports the
negative-mechanistic conclusion:

- unrestricted generalized optimization is distorted by complement /
  denominator cancellation;
- task-supported restriction removes that full-space pathology but does not
  yield a stable unilateral low-dimensional orientation;
- B-normalized unilateral selection preferentially exploits low B response
  rather than improving held-out task transfer;
- increasing train n improves support coverage and actual pooled task capture,
  but does not repair the cross-fold orientation estimator;
- a final denominator-free common-structure estimator still fails its
  prospectively locked same-sample-size third-fold test.

Per the locked H1-0019 rule, estimator search stops here.

No next scientific package, confirmatory H1 run, C2, C3, or C4 execution is
authorized by this ingest report.
