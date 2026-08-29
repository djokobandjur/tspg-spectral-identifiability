# TSPG H1-0018 FORMAL CLOSEOUT REPORT v1.0

**Date:** 2026-08-29  
**Run:** `TSPG-RUN-H1-0018`  
**Formal status:** `CLOSED_PASS_DIAGNOSTIC_HYBRID_SAMPLE_SIZE_DECOUPLING`  
**Confirmatory H1:** `BLOCKED`  
**H1-0019:** `NOT_AUTHORIZED — DESIGN DISCUSSION PENDING`

## Closed findings

1. Support coverage remains train-sample-limited over n=100--320:
   phi rises strongly and shows no observed saturation.
2. A phi plateau, if one had occurred, would not have implied complete support
   estimation; this interpretation remains prohibited.
3. Orientation efficiency is not coherently train-sample-limited over the
   observed range.
4. The strongest evidence is eta32, which falls by about 0.12 in both
   directions as train n increases from 100 to 320.
5. Direct decomposition shows that T32 rises modestly while the held-out oracle
   ceiling U32 rises about 4.48x and 4.25x
   faster in absolute gain in the two directions.
6. Secondary held-out subsampling demonstrates held-out finite-sample
   sensitivity, so the primary train-size result is not caused by eta being
   generally insensitive to sample size.
7. No post-hoc linear extrapolation of phi to one, and no population-rank
   estimate, is permitted.
8. The prespecified n=640 inverse-n forecast remains planning-only.

## IC07

The original summary CSV contains a derived column-label collision and is
superseded only as a derived view. The scientific evidence and runtime result
remain authoritative and unchanged.

Corrected summary:
`TSPG_H1_0018_SUMMARY_CURVES_v1_1_20260829.csv`

Mechanism decomposition:
`TSPG_H1_0018_PRIMARY_T_U_ORIENTATION_DECOMPOSITION_v1_0_20260829.csv`

## H19 implication

H18 does not justify a separate unilateral sample-size escalation as the next
scientific step.

If H19 is later authorized, its question is instead:

> Can a prospectively locked estimator of common AG1/AG2 structure recover a
> third-fold-transferable orientation that unilateral estimators fail to
> recover?

The existing H19 guardrails remain mandatory:
- unilateral-320;
- actual unilateral-640;
- consensus-640;
- same untouched AP held-out set;
- no candidate-orientation-dependent denominator advantage;
- mandatory bbar control;
- H19 is the last estimator attempt.

No H19 package is created by this closeout.
