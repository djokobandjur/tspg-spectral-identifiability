# TSPG H1-0012 FORMAL CLOSEOUT REPORT

**Run:** `TSPG-RUN-H1-0012`  
**Formal status:** `CLOSED_PASS_DIAGNOSTIC`  
**Full-space eigenpair certification:** `NOT_ACHIEVED`

Runtime evidence SHA-256:

`ba01958be17df19947b90434714b2603de997a27ec40e7d8dc1505eab7c893c4`

ZIP integrity PASS; internal SHA manifest 10/10 PASS.

The scientific computation was the completed v1.1 runtime through L=16.
IC02/IC03 repaired only output naming/path discovery, and the post-run upgrade
added zero-cost A38 reporting fields. No new model or G_A computation occurred.

## Joint top-1 trajectory

| L | dim | lambda1 | ||v||^2 | q_T | q_A | q_A/mean(G_A) | leakage | rho_full |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 320 | 2483.120 | 14829.5 | 0.167445 | 6.743e-05 | 4.088 | 0.020959 | 0.600505 |
| 1 | 328 | 6481.867 | 41312.7 | 0.156898 | 2.420e-05 | 1.468 | 0.014709 | 0.637302 |
| 2 | 336 | 7050.795 | 50605.9 | 0.139328 | 1.976e-05 | 1.198 | 0.013793 | 0.639189 |
| 4 | 352 | 11421.533 | 85684.5 | 0.133298 | 1.167e-05 | 0.708 | 0.011442 | 0.650390 |
| 8 | 384 | 19303.956 | 166014.0 | 0.116279 | 6.022e-06 | 0.365 | 0.008724 | 0.656995 |
| 12 | 416 | 29098.222 | 281178.1 | 0.103487 | 3.555e-06 | 0.216 | 0.007093 | 0.656021 |
| 16 | 448 | 37385.558 | 401519.4 | 0.093110 | 2.489e-06 | 0.151 | 0.005887 | 0.639800 |

## Decisive observations

From L=0 to L=16:

- leading Ritz value increases **15.06x**
  (2483.1 -> 37385.6);
- B-normalized Euclidean norm squared increases
  **27.08x**;
- Euclidean task Rayleigh quotient falls by
  **44.4%**
  (0.1674 -> 0.0931);
- Euclidean attention Rayleigh quotient falls
  **27.1x**;
- geometry location moves from **4.09x** the mean G_A
  eigenvalue to only **0.151x**;
- raw G_A leakage norm falls **3.56x**, but
  `|lambda| * leakage` grows **4.23x**;
- normalized full-space residual remains in the narrow high band
  **[0.601, 0.657]**, ending at
  **0.640**;
- no top-1 or complete top-4 set satisfies the locked `1e-6`
  full-space certification gate.

The exact and leakage-based normalized residuals agree to floating-point
precision, validating the closed-form residual interpretation.

## Mechanistic conclusion

H1-0012 strengthens the H1-0011 Schur-coupling result.

The nested maximizer does not gain quotient by improving task alignment per
unit Euclidean norm. Its task Rayleigh quotient instead becomes weaker, while
its attention response per unit norm collapses much faster.

At L=16 the leading direction retains only
**13.3%** of the maximum empirical task Rayleigh
quotient, but sits at only **0.151x** the mean G_A
eigenvalue. The complement fraction has grown to
**35.2%**.

This is a denominator-side geometry-cancellation mechanism, not a search for
a stronger task direction.

The effect is still not ridge dominated at L=16:
`ridge_fraction = 6.622e-04`.

## Numerical conclusion

The L=16 augmented Ritz sequence is **not converged to a full-space
generalized eigenpair**. This is not a technical run failure: the diagnostic
completed exactly as designed. It means the locked unrestricted generalized
estimand is not yet numerically stable enough to scale to confirmatory H1.

A deeper blind Krylov continuation is not authorized here. The next
development step is a zero-G_A regularization-sensitivity analysis on the
already computed nested augmented spaces.
