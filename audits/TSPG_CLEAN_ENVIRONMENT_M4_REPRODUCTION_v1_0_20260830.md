# TSPG clean-environment M4 reproduction audit v1.0

**Date:** 2026-08-30  
**Execution boundary:** same fresh FMLE clean-reproduction workspace used for portable materialization and M1--M3; public repository detached at `53c7ff9dc8afcc7ff782a6d2f340d8e183acbcf4`  
**Status:** `PASS_M4`  
**End-to-end M1--M5 status:** `IN_PROGRESS_M5_PENDING`

## Sequential-input gate

Before M4 execution, the clean-generated M2 AG2 task-gradient object

`TSPG_H1_0016_LEARNED_SEED42_AG2_320_FP64_TASK_GRADIENTS_v1_2.npy`

was copied into the portable runtime and rehashed. Its SHA-256 was

`2850c66d13dc45f48baa114f540e29c3ca75903db412ac8f93c048fdb8b930eb`,

exactly matching the locked identity. Thus the clean M4 run consumed the byte-identical AG2 gradients produced earlier in the same sequential clean-execution chain.

## Execution contract

The H1-0018 runner used existing gradients only and reported:

- model scientific compute: `0`
- GPU scientific compute: `0`
- new task gradients: `0`
- new G_A actions: `0`
- AG1 unique classes: `98`
- AG2 unique classes: `98`
- H1-0016 class histograms reproduced: `true`
- technical status: `PASS`

The full-n H1-0016 reproduction errors were all below `1e-13`; the maximum observed absolute error was `9.736655925962623e-14`.

## Result JSON comparison

Clean result JSON:

- size: `60648` bytes
- SHA-256: `b9d0bb9e01e4e8962b28e3a82fdf1136918a3d426c285f4352c7d3e7bf4eb82a`

Authoritative result JSON:

- size: `60751` bytes
- SHA-256: `c6828d72e918a8f88be8fd9b254f4c2695163e7a84e9db18dac0225bc6f876b8`

A complete decoded-tree comparison finds exactly `2` differing scalar leaves:

1. `sources.AG1_gradients.path`;
2. `sources.AG2_gradients.path`.

Both differences are expected host-local path changes introduced by the portable runtime. Every other decoded field is exactly equal, including the class-provenance state, full-n validation values, all deterministic resampling summaries, all planning-only n=640 forecasts, interpretation locks, conditional H1-0019 guardrails, and all output SHA identities.

Therefore M4 reproduces the authoritative scientific/numerical result exactly.

## Generated outputs

### Dual-Gram/resampling NPZ

`TSPG_H1_0018_DUAL_GRAMS_RESAMPLES_AND_CURVES_v1_0.npz`

- size: `2894583` bytes
- expected SHA-256: `228705665d79f4d917c7706059413dbb78a35795ed629a23bab69ac82c3b3855`
- clean generated SHA-256: `228705665d79f4d917c7706059413dbb78a35795ed629a23bab69ac82c3b3855`
- status: `EXACT_BYTE_MATCH`

### Replicate CSV

`TSPG_H1_0018_REPLICATE_CURVES_v1_0_20260829.csv`

- size: `289084` bytes
- expected SHA-256: `f2c54e193d496c128ee14eb3335ba25b8e609a249dee56667a9d3c584c492760`
- clean generated SHA-256: `f2c54e193d496c128ee14eb3335ba25b8e609a249dee56667a9d3c584c492760`
- status: `EXACT_BYTE_MATCH`

### Runtime summary CSV

`TSPG_H1_0018_SUMMARY_CURVES_v1_0_20260829.csv`

- size: `27628` bytes
- expected SHA-256: `92c1247bdb61d09c21aab696a00a6ddb0f560f209369ef98b9e5dbe3a774fa3e`
- clean generated SHA-256: `92c1247bdb61d09c21aab696a00a6ddb0f560f209369ef98b9e5dbe3a774fa3e`
- status: `EXACT_BYTE_MATCH`

This last equality is a reproduction statement about the historical runtime output, not a publication endorsement. The original H1-0018 summary CSV has a documented sample-size-label collision and remains superseded for public reporting by the corrected primary orientation-decomposition CSV. The clean test intentionally verifies the historical runtime byte identity without reversing that correction.

## Gate decision

**M4 decision:** `PASS_EXACT_SCIENTIFIC_NUMERICAL_REPRODUCTION_AND_GENERATED_BYTES_3_OF_3`.

The sequential clean-environment execution chain is now:

- portable materialization: `PASS`
- M1: `PASS`
- M2 gate/full: `PASS`
- M3: `PASS`
- M4: `PASS`
- M5 fit gate/full: pending

The end-to-end M1--M5 release gate remains open only for M5 execution/comparison and the subsequent environment/package freeze steps.
