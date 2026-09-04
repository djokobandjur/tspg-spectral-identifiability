# TSPG PROTOCOL AMENDMENT A29 — H1-0007 ALiBi DENSE CONTROL AND ESTIMAND BRANCHES

**Date:** 2026-08-28  
**Status:** `LOCKED_BEFORE_H1-0007_RUNTIME`  
**Amends:** `TSPG_PROTOCOL_AMENDMENT_A28_H1_0007_DUAL_BLOCKSOLVE_RIDGE_FRACTION_PREFLIGHT_v1_0_20260828.md`  
**Execution status:** `PREPARED; DO NOT EXECUTE UNTIL H1-0006 FORMAL CLOSEOUT`

## Purpose

A29 adds a second, exact diagnostic arm to H1-0007 without changing the
Learned arm, its numerical gates, `c`, `tau`, `alpha`, splits, or H1 claim
criteria.

The added arm tests whether ridge/attention denominator behavior differs
between:

- an additive positional parameterization, Learned PE, where a positional
  perturbation can affect the task through pathways not completely represented
  by attention-logit displacement; and
- ALiBi, where the native positional perturbation enters through attention
  logits by construction.

This is a diagnostic contrast, not a confirmatory family comparison.

## Arm A — Learned seed42

Arm A is unchanged from A28:

- full-C `G_A`, C=256;
- true-label AG1 task gradients, n=320;
- exact FP64 block `G_A V` validation;
- exact-residual multi-RHS B solves;
- randomized dual/range ladder `ell = 14 -> 28`;
- exact original generalized-residual gate `<=1e-6`;
- mandatory ridge/attention denominator decomposition;
- `c=1e-4` remains unchanged.

## Arm B — ALiBi seed42 dense exact control

Arm B uses the ALiBi seed42 development checkpoint only.

Native dimension:

`d_p = 12`.

Use the same canonical C=256 calibration set and AG1=320 task examples.

Construct:

`G_A` exactly as a dense 12x12 matrix by applying the already validated
FP64 exact matrix-free geometry operator to all 12 Euclidean basis vectors.

Construct:

`G_T = G^T G / 320`

from ordinary scalar FP64 per-example true-label gradients.

The regularization rule is unchanged:

`tau_ALiBi = c * tr(G_A_ALiBi)`

with:

`c = 1e-4`

and:

`alpha_ALiBi = tau_ALiBi / 12`.

Then solve the dense exact generalized problem:

`G_T v = lambda (G_A + alpha I) v`

with `scipy.linalg.eigh`.

No Nystrom approximation, randomized range, CG, LOBPCG, or preconditioner is
used in Arm B.

## ALiBi technical validation

The dense top-4 result must record:

- eigenvalues;
- B-orthonormality error;
- normalized generalized residuals;
- Euclidean squared norms;
- `B_energy`;
- `ridge_energy`;
- `attention_energy`;
- `ridge_fraction`;
- `attention_fraction`;
- fraction identity error.

Technical gates:

- B-orthonormality max absolute error `<=1e-10`;
- normalized generalized residual max `<=1e-10`;
- fraction identity absolute error max `<=1e-10`;
- finite eigenvalues;
- minimum retained eigenvalue `>= -1e-12`.

These are numerical-validity gates only.

## No ridge-fraction threshold

Neither Arm A nor Arm B uses a threshold such as

`attention_fraction >= 0.5`

or

`ridge_fraction <= 0.5`.

The fractions remain continuous diagnostics.

A strong Learned-versus-ALiBi contrast may motivate a later estimand amendment,
but it does not itself change H1-0007 or authorize confirmatory inference.

## Architectural interpretation boundary

H1-0007 may test the hypothesis that additive PE parameterizations permit
task-sensitive directions weakly represented by the attention-logit geometry.

It must not state before evidence that such directions must exist or that the
full-space quotient is structurally singular.

For ALiBi, the dense control tests the corresponding logit-mediated
parameterization under the same regularization rule.

## Two equal downstream branches

If H1-0007 produces a converged ridge-dominated Learned solution, two
scientifically legitimate next-step branches remain equally open:

1. **regularization sensitivity / revised `c` design**;
2. **explicit restriction to a geometry-supported `G_A` subspace**.

Neither branch is preferred or authorized by A29.

A future geometry-supported-subspace definition must use a geometry-only,
precommitted support criterion, such as a numerical-noise, spectral-stability,
or reproducibility criterion. The task outcome may not be used to choose the
support cutoff or rank.

A future `c` sweep likewise requires a separate amendment locked before that
sweep is inspected.

## Governance boundary

- H1-0006 must still be formally closed before H1-0007 execution.
- Protocol lock v0.27 remains active until H1-0006 closeout.
- seed42 remains development-only.
- confirmatory H1 remains blocked.
- cross-family expansion remains unauthorized.
- H2/H3 remain unauthorized.
