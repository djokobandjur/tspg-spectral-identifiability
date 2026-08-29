# TSPG Zenodo standalone staging SHA verification v1.0

**Date:** 2026-08-29  
**Scope:** eight standalone numerical artifacts planned for the Zenodo archival record  
**Status:** `PASS_SHA_8_OF_8_METADATA_MANIFEST_PENDING`

## Evidence

A generated staged-copy checksum manifest was supplied after running the release-staging workflow:

`STAGING_SHA256.txt`

The exact promoted public copy is:

`../manifests/TSPG_ZENODO_STANDALONE_STAGING_SHA256_v1_0_20260829.txt`

The supplied checksum file is 1,026 bytes and has SHA-256:

`c809c81e2f8be8a1d93bb473fdb837900cc15ef9592c4a6014ad3dae2fff2f3a`

## Verification result

All eight staged-copy SHA-256 entries exactly match the already locked standalone artifact identities in `../manifests/LARGE_ARTIFACTS_SHA256.csv` and `../manifests/TSPG_RELEASE_ASSET_PLAN_v1_0_20260829.json`:

| Artifact | Staged SHA-256 status |
|---|---|
| `TSPG_H1_0007_LEARNED_SEED42_AG1_320_FP64_TASK_GRADIENTS_v1_0.npy` | PASS |
| `TSPG_H1_0010_LEARNED_SEED42_QR_TASK320_EXACT_GEOMETRY_v1_1.npz` | PASS |
| `TSPG_H1_0011_LEARNED_SEED42_COMPLEMENT_KRYLOV_BASIS_v1_0.npz` | PASS |
| `TSPG_H1_0015_LEARNED_SEED42_TAIL_RANK5_8_COMPLEMENT_KRYLOV_L4_v1_0.npz` | PASS |
| `TSPG_H1_0016_LEARNED_SEED42_AG2_320_FP64_TASK_GRADIENTS_v1_2.npy` | PASS |
| `TSPG_H1_0016_LEARNED_SEED42_AG1_AG2_TASK_CROSSFOLD_DERIVED_v1_2.npz` | PASS |
| `TSPG_H1_0019_LEARNED_SEED42_AP640_FP64_TASK_GRADIENTS_v1_0.npy` | PASS |
| `TSPG_H1_0019_FIT_ARM_BASES_TOP32_v1_0.npz` | PASS |

**Result:** `8/8 exact SHA-256 matches`.

The aggregate payload size, from the independently locked per-artifact sizes, is `3,182,648,718` bytes (about 2.964 GiB).

## Remaining staging metadata gate

This checksum manifest proves that the eight hashes recorded for the staged copies are the expected hashes. It does not itself contain the staging directory, per-file size/status fields, or the explicit `PASS_8_OF_8` metadata emitted by the staging script.

The staging workflow also generates:

`TSPG_ZENODO_STANDALONE_STAGING_MANIFEST_v1_0_20260829.json`

That small JSON metadata manifest should be retained/promoted before the standalone staging gate is marked fully closed. Until then, SHA verification is closed `8/8 PASS`, while staging-metadata capture remains pending.

No scientific result is changed by this audit. It is a release-integrity/provenance check only.
