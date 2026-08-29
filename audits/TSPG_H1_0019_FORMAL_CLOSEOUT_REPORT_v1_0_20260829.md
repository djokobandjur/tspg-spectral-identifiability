# TSPG H1-0019 FORMAL CLOSEOUT REPORT v1.0

**Date:** 2026-08-29  
**Run:** `TSPG-RUN-H1-0019`  
**Formal status:** `CLOSED_PASS_DIAGNOSTIC_FINAL_ESTIMATOR_NOT_ESTABLISHED`  
**Estimator-development program:** `STOPPED_BY_PRESPECIFIED_RULE`  
**Scientific compute after closeout:** `NONE AUTHORIZED`

## Integrity and anti-adaptation evidence

The authoritative runtime evidence ZIP is:

`TSPG_H1_0019_RUNTIME_EVIDENCE_v1_0_20260829.zip`

SHA-256:

`f9eaadb43d0054a7d90714f2305b3e34fe3d47eaa34513659e4aed5ab09e62da`

Compact-evidence integrity: `32/32 PASS`.

The two key anti-adaptation facts are explicit:

- `AP_gradients_before_arm_lock = 0`;
- `no_alternate_consensus_after_AP = true`.

The remaining H1-0019 prohibitions were also respected:

- `B_or_GA_not_used_in_fit = true`;
- `B_or_GA_not_used_in_AP_task_score = true`;
- `actual_U640_used = true`;
- `no_primary_k_dropped = true`.

Fit-lock SHA-256:

`9d8d7fa7649f21a24d980172791c350dfae73c768ba7ab48a0d98b85180a8390`

AP semantic gate:

- unique classes: `99/100`;
- intersection with AG1 classes: `97/100`;
- intersection with AG2 classes: `97/100`;
- gate: `PASS`.

Exactly 640 AP FP64 per-example task gradients were computed only after the fit lock.

## Same-sample-size control

Pooling the two 320-example fit folds into the actual unilateral-640 estimator
improved third-fold task-energy capture at every primary rank:

| k | U320 mean | U640 | Delta_sample |
|---:|---:|---:|---:|
| 4 | 0.044021 | 0.060132 | +0.016112 |
| 8 | 0.070005 | 0.091775 | +0.021770 |
| 16 | 0.105374 | 0.138207 | +0.032833 |
| 32 | 0.146351 | 0.184331 | +0.037980 |

This establishes a real fit-sample-size benefit and makes U640 the necessary
baseline for evaluating the consensus principle.

## Consensus principle result

The locked consensus effect was rank dependent:

| k | U640 | CONS640 | Delta_cons | paired 95% CI |
|---:|---:|---:|---:|---:|
| 4 | 0.060132 | 0.065636 | +0.005504 | [+0.002737, +0.008215] |
| 8 | 0.091775 | 0.092719 | +0.000944 | [-0.003222, +0.004695] |
| 16 | 0.138207 | 0.129224 | -0.008983 | [-0.013834, -0.004297] |
| 32 | 0.184331 | 0.186578 | +0.002247 | [-0.001102, +0.005815] |

The prespecified four-rank mean contrast was:

`Delta_curve = -0.00007214`

with paired-bootstrap 95% CI:

`[-0.002306, +0.002166]`.

The locked success rule therefore fails. The consensus effect is clearly
positive at k=4, clearly negative at k=16, and not separated from zero at k=8
or k=32.

## Fit-side commonness trade

The consensus estimator made the intended fit-side trade.

At top-32:

- U640 fit capture:
  - AG1 = `0.645441`
  - AG2 = `0.548906`
- CONS640 fit capture:
  - AG1 = `0.575527`
  - AG2 = `0.470865`

Thus commonness cost approximately 0.07--0.08 fold-wise task-energy fraction,
yet this trade did not produce a rank-robust AP advantage.

## bbar internal negative control

The same denominator-preference diagnostic that exposed the H1-0017
small-denominator effect remained approximately neutral in H1-0019:

| k | bbar(CONS640) / bbar(U640) |
|---:|---:|
| 4 | 1.0320 |
| 8 | 0.9979 |
| 16 | 0.9578 |
| 32 | 1.0195 |

This is retained as an **internal negative control for the diagnostic itself**:
the diagnostic reports a large imbalance when the H1-0017 artifact is present
and remains near one when that artifact is absent.

## Data-use closeout

AP is consumed as a C1-development held-out set.

The original AG1/AG2/AP three-fold setup therefore has no unused third fold for
another independent estimator-development test. Opening a new held-out subset
from the untouched evaluation pool would constitute a new development cycle,
which is outside the prospectively closed estimator program.

## Final decision

The tested consensus construction did not establish a rank-robust third-fold
advantage over matched-sample unilateral-640.

Per the prespecified H1-0019 rule:

`STOP ESTIMATOR SEARCH`.

No H20 estimator run, 20-checkpoint scaling, or downstream subspace-dependent
claim experiment is authorized.
