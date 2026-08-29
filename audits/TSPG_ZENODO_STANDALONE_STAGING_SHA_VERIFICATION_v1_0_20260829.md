# TSPG Zenodo standalone staging SHA verification v1.0

**Date:** 2026-08-29  
**Scope:** eight standalone numerical artifacts planned for the Zenodo archival record  
**Status:** `PASS_COMPLETE_8_OF_8`

## Evidence

The release-staging workflow produced both a staged-copy checksum manifest and a staging metadata JSON:

- `STAGING_SHA256.txt`
- `TSPG_ZENODO_STANDALONE_STAGING_MANIFEST_v1_0_20260829.json`

The exact checksum manifest is promoted publicly as:

`../manifests/TSPG_ZENODO_STANDALONE_STAGING_SHA256_v1_0_20260829.txt`

The supplied checksum file is 1,026 bytes and has SHA-256:

`c809c81e2f8be8a1d93bb473fdb837900cc15ef9592c4a6014ad3dae2fff2f3a`

The supplied staging JSON is 2,303 bytes and has SHA-256:

`6483ea07f6deefa4db3a08b2af9d22358bc930ad1038842deaeb3135cf9e61c5`

Because the raw staging JSON contains a host-local absolute path and username, it is not promoted byte-for-byte. A sanitized semantic public copy preserving the release-relevant metadata and binding back to the exact private JSON by size/SHA-256 is promoted as:

`../manifests/TSPG_ZENODO_STANDALONE_STAGING_MANIFEST_PUBLIC_v1_0_20260829.json`

## Verification result

The raw staging metadata reports `PASS_8_OF_8`, aggregate payload size `3,182,648,718` bytes, and `PASS_STAGED_COPY_MATCH` for all eight artifacts. Every staged-copy SHA-256 exactly matches the already locked standalone artifact identity in `../manifests/LARGE_ARTIFACTS_SHA256.csv` and `../manifests/TSPG_RELEASE_ASSET_PLAN_v1_0_20260829.json`:

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

**Result:** standalone Zenodo staging gate `PASS_COMPLETE_8_OF_8`.

The exact local stage directory is retained in the private JSON but intentionally redacted from the public semantic copy. This sanitization changes no scientific or integrity-relevant metadata: filenames, byte counts, SHA-256 identities, per-artifact staged-copy status, aggregate payload size, source-manifest identity, and overall pass status are preserved.

## Next non-Git staging gate

The standalone numerical payload is fully staged and verified. The remaining release-upload workspace step is to stage and independently rehash the six convenience assets: the Learned seed-42 checkpoint plus the five compact H1-0015--H1-0019 runtime-evidence ZIPs.

No scientific result is changed by this audit. It is a release-integrity/provenance check only.
