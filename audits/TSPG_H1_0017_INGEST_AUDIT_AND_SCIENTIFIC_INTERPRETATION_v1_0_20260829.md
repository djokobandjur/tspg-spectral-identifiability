# TSPG H1-0017 INGEST AUDIT AND SCIENTIFIC INTERPRETATION v1.0

**Date:** 2026-08-29  
**Run:** `TSPG-RUN-H1-0017`  
**Evidence ZIP:** `TSPG_H1_0017_RUNTIME_EVIDENCE_v1_1_20260829.zip`  
**Evidence ZIP SHA-256:** `5fff014e258c2bac92cc61f13ea559ba6cae67b41487d35141f4e00306ee1ae4`  
**Ingest status:** `PASS`  
**Technical status:** `PASS`  
**Scientific status:** `DEVELOPMENT_RESULT_PENDING_DISCUSSION`  
**Confirmatory H1:** `BLOCKED`

## Integrity

- ZIP integrity: PASS.
- Internal compact-evidence SHA checks: 23/23 PASS.
- All numerical checks in the H1-0017 result: PASS.
- Offline-only contract: PASS.
- New task gradients: 0.
- New G_A actions: 0.
- Model/GPU execution: none.

## Numerical certification after A47/IC05

B11:
- min eigenvalue = 3.332699214854e-05
- max eigenvalue = 4.774425888305e-02
- condition number = 1432.600298
- inverse-square-root reconstruction relative Frobenius error =
  2.149e-14
- full train B-orthonormality infinity error =
  9.353e-13
- full oracle B-orthonormality infinity error =
  7.450e-13

The original full-spectrum self-scaled residual is retained descriptively:
- train max all 320 = 6.123e-10
- oracle max all 320 = 1.857e-05

The corrected A47 certification passes:
- train self-scaled max top32 =
  1.474e-13
- oracle self-scaled max top32 =
  6.287e-14
- train all-spectrum normwise backward error =
  2.619e-15
- oracle all-spectrum normwise backward error =
  3.072e-16
- train whitened symmetric backward error =
  7.220e-16
- oracle whitened symmetric backward error =
  6.353e-16

## 2x2 cross-scoring result

| k | eta_task(SE) | eta_task(SB) | eta_B(SE) | eta_B(SB) | Delta_sel|task | Delta_sel|B | bbar(SB)/bbar(SE) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.3043 | 0.0428 | 0.0068 | 0.3882 | -0.2614 | +0.3814 | 0.00246 |
| 2 | 0.3549 | 0.0419 | 0.0079 | 0.3349 | -0.3130 | +0.3270 | 0.00273 |
| 4 | 0.3449 | 0.0539 | 0.0084 | 0.3689 | -0.2909 | +0.3605 | 0.00341 |
| 8 | 0.3727 | 0.0605 | 0.0104 | 0.3584 | -0.3122 | +0.3480 | 0.00475 |
| 16 | 0.3782 | 0.0729 | 0.0163 | 0.3682 | -0.3054 | +0.3519 | 0.00736 |
| 32 | 0.4059 | 0.0944 | 0.0427 | 0.4012 | -0.3115 | +0.3585 | 0.01342 |

The result is directionally uniform across the full locked ladder.

### Task-only held-out scoring

`S_B` is substantially worse than `S_E` at every k:

- Delta_sel|task ranges from
  -0.3130
  to -0.2614.
- At k=4:
  eta_task(SE)=0.3449,
  eta_task(SB)=0.0539.
- At k=32:
  eta_task(SE)=0.4059,
  eta_task(SB)=0.0944.

Thus B-based train selection does **not** improve held-out task transfer.
It reduces it markedly.

### B-normalized held-out scoring

Under B-normalized scoring the ordering reverses:

- Delta_sel|B is positive at every k, ranging from
  +0.3270
  to +0.3814.
- At k=4:
  eta_B(SE)=0.0084,
  eta_B(SB)=0.3689.
- At k=32:
  eta_B(SE)=0.0427,
  eta_B(SB)=0.4012.

However this B-scoring gain is accompanied by an extreme reduction in
Euclidean-unit B response. Across k=1...32, S_B has approximately
74.5x to 405.7x lower mean B
response than S_E.

This is the key decomposition:
- B-selection wins strongly when the held-out score rewards low B response;
- the same B-selected span loses strongly when the held-out score is pure task
  transfer.

Therefore the positive Delta_sel|B is primarily **denominator-selective** and
is not evidence that B found a more reproducible task-sensitive orientation.

## B-principal-angle geometry

| k | min B-principal cosine | max angle (deg) | normalized projector distance | held-out gamma_k |
|---:|---:|---:|---:|---:|
| 1 | 0.4939 | 60.40 | 0.8695 | 0.1730 |
| 2 | 0.1860 | 79.28 | 0.9252 | 0.0638 |
| 4 | 0.0435 | 87.50 | 0.8794 | 0.0646 |
| 8 | 0.0238 | 88.63 | 0.8819 | 0.0695 |
| 16 | 0.0468 | 87.32 | 0.8597 | 0.0803 |
| 32 | 0.0080 | 89.54 | 0.8256 | 0.0601 |

The train generalized subspace and held-out B-oracle subspace are not well
aligned. The minimum principal cosine falls to 0.0080
by k=32, and the normalized projector distance remains
0.8256. The prospective expectation that
B-principal angles would systematically improve with k is not supported.

The local held-out generalized gaps are modest:
- k=1: 0.1730
- k=2--32: approximately
  0.0601 to
  0.0803.

Thus hard low-k cuts are not strongly isolated, but weak boundary isolation
does not explain away the low eta: eta is a rotation-invariant subspace trace
metric.

## Prospective-prediction audit

1. `eta_B(S_B)` consistently above existing task-only `eta_task(S_E)`:
   **NOT SUPPORTED**. The comparison is mixed and uses different oracle
   normalizations in any case.
2. `Delta_sel|B > 0` over much of the low-k ladder:
   **SUPPORTED**, in fact positive at all six locked k.
3. `Delta_sel|task > 0` as denominator-independent corroboration:
   **NOT SUPPORTED**; it is negative at all six locked k.
4. held-out gamma small at the smallest cuts and larger by k=32:
   **NOT SUPPORTED**. k=1 has the largest local gap; k=2--32 remain modest.
5. B-principal angles largest at k=1--2 and then improve:
   **NOT SUPPORTED** by the boundary cosine or projector-distance profiles.

## Development interpretation

H1-0017 gives a clean negative answer to the motivating question:

> The locked B11 metric does not select a more cross-image reproducible
> task-sensitive subspace inside AG1 support.

The B-selected space has a strong structural preference for directions with
very small B response. Because the same B11 operator is used in train
selection and held-out B scoring, that denominator preference transfers
deterministically. The 2x2 cross-scoring matrix exposes the distinction:
the gain survives only under B-normalized scoring and reverses under pure
held-out task scoring.

Therefore attention normalization does not resolve the cross-fold orientation
problem identified by H1-0016.

This result does not invalidate the existence of a shared task support or the
low-dimensional held-out oracle ceilings established by H1-0016. It does
invalidate the narrower proposed remedy that generalized top-k directions of
(C1,B11) are themselves the reproducible C1 subspace estimator.

No confirmatory scaling, B22 build, or next scientific package is authorized
by this ingest. A design discussion is required first.
