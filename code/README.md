# Code

This directory contains the exact final, non-superseded **analysis** code promoted for the reported TSPG M1--M5 results. The listed analysis files are copied byte-for-byte from the SHA-locked execution starter packages used for the corresponding analyses; public SHA-256 values are recorded in `../manifests/CODE_SHA256.txt`.

Development-only and superseded implementations are intentionally not promoted. The public repository is a reproducibility surface, not a dump of the internal project workspace.

## Model-definition dependency

The Learned seed-42 checkpoint was instantiated from `full_scale_experiment.py` with authoritative SHA-256:

`83fc337128dec7f896c9816842806789a634154dea8372bb0a43bae19188d3bf`

An exact retained copy has been recovered and SHA-verified during release preparation. Its exact-byte public promotion is **still pending**. No reconstructed or approximate implementation is accepted as a substitute. This dependency therefore remains an explicit blocker for the first immutable release and is also recorded in the public checkpoint manifest and `../docs/REPRODUCTION.md`.

## Shared operators

- `TSPG_cross_family_pe_operator_v1_0_20260828.py` — common positional-parameter forward/gradient operator used across the reported analyses.
- `TSPG_h1_0003_matrixfree_geometry_operator_v1_1_20260828.py` — matrix-free attention-geometry operator used by M1 and M5 dependencies.
- `TSPG_h1_0007_dual_blocksolve_ridge_fraction_alibi_control_v1_1_20260828.py` — shared block/matvec and generalized-spectral utilities used by the final analysis path.

## M1 — unrestricted quotient pathology / search-conditioned boundary

- `TSPG_h1_0015_matched_rank_boundary_complement_fairness_v1_1_20260828.py`
- `TSPG_run_h1_0015_matched_rank_boundary_complement_fairness_v1_1_20260828.py`
- locked configuration: `../configs/TSPG_H1_0015_CONFIG_v1_1_20260828.json`
- run card: `../run_cards/TSPG_RUN_CARD_H1_0015_LEARNED_MATCHED_RANK_BOUNDARY_COMPLEMENT_FAIRNESS_v1_1_20260828.md`

## M2 — task-support restriction and cross-fold orientation

- `TSPG_h1_0016_task_side_crossfold_preflight_v1_2_20260829.py`
- `TSPG_run_h1_0016_task_side_crossfold_preflight_v1_2_20260829.py`
- locked configuration: `../configs/TSPG_H1_0016_CONFIG_v1_2_20260829.json`
- run card: `../run_cards/TSPG_RUN_CARD_H1_0016_LEARNED_AG1_AG2_TASK_SIDE_CROSSFOLD_PREFLIGHT_v1_2_20260829.md`

## M3 — denominator-selective B-normalized cross-fit selection

- `TSPG_h1_0017_offline_b_normalized_crossfit_v1_1_20260829.py`
- `TSPG_run_h1_0017_offline_b_normalized_crossfit_v1_1_20260829.py`
- `TSPG_H1_0017_STATIC_QA_v1_1_20260829.py`
- locked configuration: `../configs/TSPG_H1_0017_CONFIG_v1_1_20260829.json`
- run card: `../run_cards/TSPG_RUN_CARD_H1_0017_LEARNED_AG1_TO_AG2_OFFLINE_B_NORMALIZED_CROSSFIT_v1_1_20260829.md`

## M4 — finite-sample support/orientation stability

- `TSPG_h1_0018_dual_finite_sample_stability_v1_0_20260829.py`
- `TSPG_run_h1_0018_finite_sample_stability_v1_0_20260829.py`
- `TSPG_H1_0018_STATIC_QA_v1_0_20260829.py`
- locked configuration: `../configs/TSPG_H1_0018_CONFIG_v1_0_20260829.json`
- run card: `../run_cards/TSPG_RUN_CARD_H1_0018_LEARNED_SEED42_FINITE_SAMPLE_STABILITY_v1_0_20260829.md`

## M5 — matched-sample third-fold consensus test

- `TSPG_h1_0019_consensus_thirdfold_v1_0_20260829.py`
- `TSPG_run_h1_0019_last_estimator_v1_0_20260829.py`
- `TSPG_H1_0019_STATIC_QA_v1_0_20260829.py`
- locked configuration: `../configs/TSPG_H1_0019_CONFIG_v1_0_20260829.json`
- run card: `../run_cards/TSPG_RUN_CARD_H1_0019_LAST_ESTIMATOR_CONSENSUS_THIRDFOLD_v1_0_20260829.md`

The manuscript-level M1--M5 mapping is maintained in `../docs/ARTIFACT_MAP.md`. Portable path mapping and release-blocker status are documented in `../docs/REPRODUCTION.md`. Large raw arrays are not stored in Git; their identities and acquisition/reconstruction routes are preserved in `../manifests/` and `../docs/ARTIFACT_ACQUISITION.md`.
