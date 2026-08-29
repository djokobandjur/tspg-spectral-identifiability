# TSPG clean-environment M3 reproduction audit v1.0

**Date:** 2026-08-30  
**Execution boundary:** same fresh FMLE clean-reproduction workspace used for the portable materialization and M1--M2 tests; public repository detached at `53c7ff9dc8afcc7ff782a6d2f340d8e183acbcf4`  
**Status:** `PASS_M3`  
**End-to-end M1--M5 status:** `IN_PROGRESS_M4_M5_PENDING`

## Sequential-input gate

Before M3 execution, the clean-generated M2 derived object

`TSPG_H1_0016_LEARNED_SEED42_AG1_AG2_TASK_CROSSFOLD_DERIVED_v1_2.npz`

was promoted into the portable runtime root and rehashed. Its SHA-256 was

`afe9a94d1c5c7f7f3d8986348b15c7513013c77969781d54d03c0f8154b4baea`,

exactly matching the locked M2 identity. Thus M3 consumed the byte-identical clean-generated M2 numerical dependency rather than an altered derivative.

## Execution contract

The H1-0017 runner executed in offline-only mode:

- GPU use: `false`
- model loaded: `false`
- new task gradients: `0`
- new G_A actions: `0`
- technical status: `PASS`

The observed B condition number was `1432.6002979879731`.

## Generated artifact

`TSPG_H1_0017_LEARNED_SEED42_AG1_TO_AG2_B_NORMALIZED_CROSSFIT_DERIVED_v1_1.npz`

- size: `2489394` bytes
- expected SHA-256: `6cdc0f467d7ed974be2fae4be2e973f97a403a2dc6a3e61bf32d6ba5adcc2415`
- clean generated SHA-256: `6cdc0f467d7ed974be2fae4be2e973f97a403a2dc6a3e61bf32d6ba5adcc2415`
- status: `EXACT_BYTE_MATCH`

## Result JSON comparison

Clean result JSON SHA-256:

`ffbf9bb5e9180f0c8fb424c685649da5bdd02d26280425ba85eeba58d5c47000`

Authoritative result JSON SHA-256:

`eb64cd67969a73dc47ddee861493f367b32a4f952429a14506c3c022abd26b90`

A complete semantic comparison shows that the decoded trees differ only at three scalar leaves:

1. the host-local `sources.h1_0010_raw.path`;
2. the host-local `sources.h1_0016_derived.path`;
3. `elapsed_sec`.

As an independent byte-level check of that classification, replacing only those three clean-run values with the authoritative values and serializing with the runner's `json.dumps(..., indent=2)` contract reproduces the authoritative JSON exactly: 12,625 bytes and SHA-256 `eb64cd67969a73dc47ddee861493f367b32a4f952429a14506c3c022abd26b90`.

Therefore every scientific/numerical field is exactly reproduced, including the matrix summary, all six k rows, task-baseline reproduction errors, numerical gates, interpretation locks, and derived-output identity.

Selected clean reproduced values:

| k | eta_task_SE | eta_task_SB | eta_B_SE | eta_B_SB | Delta_sel_task | Delta_sel_B |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.3042763701297588 | 0.042843747270655895 | 0.0067952419491500386 | 0.3881771377780471 | -0.2614326228591029 | 0.38138189582889703 |
| 2 | 0.3549209715500522 | 0.04191987603258509 | 0.00793356866859491 | 0.334907418200801 | -0.31300109551746713 | 0.3269738495322061 |
| 4 | 0.3448614933871695 | 0.05394057207649597 | 0.008420171627679236 | 0.3689314073918754 | -0.2909209213106735 | 0.3605112357641962 |
| 8 | 0.37270766908286573 | 0.060537385459386604 | 0.010385177542663142 | 0.3583965234484816 | -0.31217028362347915 | 0.34801134590581845 |
| 16 | 0.37824815658491223 | 0.07288629355739658 | 0.016303961628349187 | 0.36815880665499956 | -0.30536186302751567 | 0.3518548450266504 |
| 32 | 0.4058868482048357 | 0.09443349067222336 | 0.042700801797915695 | 0.4012407380949581 | -0.3114533575326124 | 0.3585399362970424 |

All numerical checks in the result JSON are `true`.

## Gate decision

**M3 decision:** `PASS_EXACT_SCIENTIFIC_NUMERICAL_REPRODUCTION_AND_DERIVED_RAW_BYTE_MATCH`.

The sequential clean-environment execution chain is now:

- portable materialization: `PASS`
- M1: `PASS`
- M2 gate/full: `PASS`
- M3: `PASS`
- M4: pending
- M5 fit gate/full: pending

The end-to-end M1--M5 release gate remains open until M4 and M5 also pass and are compared with their locked authoritative results.
