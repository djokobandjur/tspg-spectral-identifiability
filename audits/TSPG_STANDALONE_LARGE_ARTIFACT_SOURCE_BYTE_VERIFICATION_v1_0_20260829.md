# TSPG standalone large-artifact source-byte verification v1.0

**Date:** 2026-08-29  
**Status:** `PASS_8_OF_8`  
**Scope:** standalone large numerical assets planned for the first Zenodo reproducibility release  
**Purpose:** verify exact byte identity before release staging; this audit does not itself upload or stage the binaries

## Verification rule

Each artifact is accepted only when the byte count and SHA-256 of the actual retained object match the locked public identity. A matching filename alone is insufficient.

Seven retained source objects were rehashed directly on the FMLE source host with streaming SHA-256. The eighth object, `TSPG_H1_0019_FIT_ARM_BASES_TOP32_v1_0.npz`, was transferred separately and independently rehashed after transfer. Host-specific absolute paths and login/container identifiers are intentionally omitted from this public audit.

## Results

| Artifact | Size (bytes) | SHA-256 | Verification |
|---|---:|---|---|
| `TSPG_H1_0007_LEARNED_SEED42_AG1_320_FP64_TASK_GRADIENTS_v1_0.npy` | 387,317,888 | `d02d8a31465912e7239164e965428162fa5f64f09082d5d0a158f6585b439009` | `PASS_SOURCE_REHASH` |
| `TSPG_H1_0010_LEARNED_SEED42_QR_TASK320_EXACT_GEOMETRY_v1_1.npz` | 776,283,320 | `08f23a6c0d87a58ed49c9f4bda841105f7d45eb848d18f30aa498eb42fb31074` | `PASS_SOURCE_REHASH` |
| `TSPG_H1_0011_LEARNED_SEED42_COMPLEMENT_KRYLOV_BASIS_v1_0.npz` | 79,126,618 | `4f948e96ec8c8ae911259f923b876864b6ffd83b1cf54669d7fdd00b90b88237` | `PASS_SOURCE_REHASH` |
| `TSPG_H1_0015_LEARNED_SEED42_TAIL_RANK5_8_COMPLEMENT_KRYLOV_L4_v1_0.npz` | 232,412,532 | `7d78e8584d265ff3a041ce84055720106a1fa49a09e7acc31be38482208e2279` | `PASS_SOURCE_REHASH` |
| `TSPG_H1_0016_LEARNED_SEED42_AG2_320_FP64_TASK_GRADIENTS_v1_2.npy` | 387,317,888 | `2850c66d13dc45f48baa114f540e29c3ca75903db412ac8f93c048fdb8b930eb` | `PASS_SOURCE_REHASH` |
| `TSPG_H1_0016_LEARNED_SEED42_AG1_AG2_TASK_CROSSFOLD_DERIVED_v1_2.npz` | 390,626,716 | `afe9a94d1c5c7f7f3d8986348b15c7513013c77969781d54d03c0f8154b4baea` | `PASS_SOURCE_REHASH` |
| `TSPG_H1_0019_LEARNED_SEED42_AP640_FP64_TASK_GRADIENTS_v1_0.npy` | 774,635,648 | `0398ec1949f7d5ad326902f438c554848b86325d352d73a67078473f7fba3145` | `PASS_SOURCE_REHASH` |
| `TSPG_H1_0019_FIT_ARM_BASES_TOP32_v1_0.npz` | 154,928,108 | `8bfc5c8e4bc7c677a882974a61b4e66d540f230dbb75b690ffbfe42ea47fa4e3` | `PASS_TRANSFERRED_COPY_REHASH` |

**Result:** `8/8 PASS`; no size or SHA-256 mismatch was observed.

The transferred H1-0019 fit-arm NPZ also opens without pickle and contains exactly four FP64 `(151296, 32)` matrices: `U320_AG1`, `U320_AG2`, `U640`, and `CONS640`.

## Release implication

The identity-discovery and source-byte-verification gate for the standalone Zenodo numerical set is closed. All eight filenames now have verified byte counts and locked SHA-256 identities.

This does **not** close the release-staging gate. Before Zenodo publication, the exact verified objects must still be copied into the release-upload staging area and the staged copies must be rehashed against these same SHA-256 values. The GitHub Release/Zenodo upload and DOI steps remain pending.
