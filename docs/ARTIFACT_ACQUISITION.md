# Large-artifact acquisition and reconstruction

This document defines how non-Git artifacts enter the public TSPG reproducibility boundary. Exact identities are authoritative; filenames and storage locations are secondary.

Machine-readable sources:

- `../manifests/LARGE_ARTIFACTS_SHA256.csv` — binary identities and current public-location state;
- `../manifests/TSPG_RELEASE_ASSET_PLAN_v1_0_20260829.json` — first-release distribution plan;
- `../manifests/TSPG_PORTABLE_RUNTIME_DEPENDENCIES_v1_0_20260829.json` — external inputs needed by the portable M1--M5 runtime path.

## Distribution boundary

The first immutable release uses two coordinated surfaces:

1. **GitHub Release** — convenient download surface for the single Learned seed-42 checkpoint plus the five compact H1-0015--H1-0019 runtime-evidence ZIPs.
2. **Zenodo** — DOI-bearing self-contained archival record containing those same six convenience assets **plus** the standalone large numerical binaries that are not already contained in the compact evidence ZIPs.

This deliberately removes mutable Google Drive/shared-folder links from the permanent checkpoint/evidence chain. Ordinary Git history remains limited to source/config/result/audit/provenance files.

## Checkpoint

| Artifact | Supports | Public route | Required verification |
|---|---|---|---|
| `TSPG_LEARNED_SEED42_best_model.pth` | M1--M5 | GitHub Release asset **and** duplicate Zenodo archival asset | size `343559209` bytes; SHA-256 `7fcca75916c2d6f0f64aa5c381812ad3a305ba1a04672e9288f4251ab683c536` |

The checkpoint is intentionally excluded from ordinary Git history because of its size. A user may download it directly from the versioned GitHub Release; the Zenodo copy makes the DOI-bearing reproducibility record self-contained.

## Compact runtime evidence

The following authoritative archives will be attached to the versioned GitHub Release and duplicated in the Zenodo record:

| Archive | Size (bytes) | SHA-256 |
|---|---:|---|
| `TSPG_H1_0015_RUNTIME_EVIDENCE_v1_1_20260828.zip` | 24,682 | `8125067b17eee2abe61bf9a3519366d371b2c751e7a481a87b3de0c32ce11c71` |
| `TSPG_H1_0016_RUNTIME_EVIDENCE_v1_2_20260829.zip` | 144,501 | `0d7c6acfe8e38826fbb36322f30f187f9442d4ea42253e9463328d004062e022` |
| `TSPG_H1_0017_RUNTIME_EVIDENCE_v1_1_20260829.zip` | 2,522,591 | `5fff014e258c2bac92cc61f13ea559ba6cae67b41487d35141f4e00306ee1ae4` |
| `TSPG_H1_0018_RUNTIME_EVIDENCE_v1_0_20260829.zip` | 2,936,547 | `2ab57eeb8c27f229f37ceec1233033cf6c3061dce8943d526cf597f2ede7e567` |
| `TSPG_H1_0019_RUNTIME_EVIDENCE_v1_0_20260829.zip` | 4,072,637 | `f9eaadb43d0054a7d90714f2305b3e34fe3d47eaa34513659e4aed5ab09e62da` |

The archives are the authoritative run-evidence layer. Their internal result/control files remain bound by their own SHA manifests; extracting an archive is sufficient to obtain several late-stage NPZ/control inputs used by the portable runtime helper.

## Standalone Zenodo numerical assets

These binaries are not duplicated inside the compact evidence archives and therefore require explicit archival upload:

| Artifact | Role | Supports | Verified size | SHA-256 |
|---|---|---|---:|---|
| `TSPG_H1_0007_LEARNED_SEED42_AG1_320_FP64_TASK_GRADIENTS_v1_0.npy` | raw AG1 task gradients | M2--M5 | 387,317,888 | `d02d8a31465912e7239164e965428162fa5f64f09082d5d0a158f6585b439009` |
| `TSPG_H1_0010_LEARNED_SEED42_QR_TASK320_EXACT_GEOMETRY_v1_1.npz` | exact task-span geometry | M1--M3 | 776,283,320 | `08f23a6c0d87a58ed49c9f4bda841105f7d45eb848d18f30aa498eb42fb31074` |
| `TSPG_H1_0011_LEARNED_SEED42_COMPLEMENT_KRYLOV_BASIS_v1_0.npz` | upstream complement basis | M1 | pending transfer verification | `4f948e96ec8c8ae911259f923b876864b6ffd83b1cf54669d7fdd00b90b88237` |
| `TSPG_H1_0015_LEARNED_SEED42_TAIL_RANK5_8_COMPLEMENT_KRYLOV_L4_v1_0.npz` | matched-rank tail geometry | M1 | 232,412,532 | `7d78e8584d265ff3a041ce84055720106a1fa49a09e7acc31be38482208e2279` |
| `TSPG_H1_0016_LEARNED_SEED42_AG2_320_FP64_TASK_GRADIENTS_v1_2.npy` | raw AG2 task gradients | M2--M5 | 387,317,888 | `2850c66d13dc45f48baa114f540e29c3ca75903db412ac8f93c048fdb8b930eb` |
| `TSPG_H1_0016_LEARNED_SEED42_AG1_AG2_TASK_CROSSFOLD_DERIVED_v1_2.npz` | cross-fold derived binary | M2--M3 | 390,626,716 | `afe9a94d1c5c7f7f3d8986348b15c7513013c77969781d54d03c0f8154b4baea` |
| `TSPG_H1_0019_LEARNED_SEED42_AP640_FP64_TASK_GRADIENTS_v1_0.npy` | raw AP gradients | M5 | 774,635,648 | `0398ec1949f7d5ad326902f438c554848b86325d352d73a67078473f7fba3145` |
| `TSPG_H1_0019_FIT_ARM_BASES_TOP32_v1_0.npz` | pre-AP fit-arm bases | M5 | pending transfer verification | `8bfc5c8e4bc7c677a882974a61b4e66d540f230dbb75b690ffbfe42ea47fa4e3` |

The two unknown exact sizes are intentionally left blank in the machine-readable manifest until the corresponding bytes are materialized and independently rehashed. SHA-256, not an inferred size, remains the locked identity.

## Already contained — do not upload twice

The following binaries are already included inside the authoritative evidence ZIP listed below, so a second standalone copy is unnecessary:

- `TSPG_H1_0017_LEARNED_SEED42_AG1_TO_AG2_B_NORMALIZED_CROSSFIT_DERIVED_v1_1.npz` → H1-0017 evidence ZIP;
- `TSPG_H1_0018_DUAL_GRAMS_RESAMPLES_AND_CURVES_v1_0.npz` → H1-0018 evidence ZIP;
- `TSPG_H1_0019_FIT_LOCK_DUAL_COEFFICIENTS_v1_0_20260829.npz` → H1-0019 evidence ZIP;
- `TSPG_H1_0019_AP_PER_EXAMPLE_CAPTURE_v1_0.npz` → H1-0019 evidence ZIP.

This avoids redundant archival payloads while preserving exact bytes inside a SHA-locked container.

## Reconstruction versus byte-level audit

Several late-stage artifacts can be regenerated by the promoted H1-0015--H1-0019 runners once their upstream inputs are present. Regeneration is useful for scientific reproduction, but the immutable archive also retains expensive/raw outputs where byte-level provenance matters or regeneration would be unnecessarily costly.

A regenerated artifact that is numerically equivalent but not byte-identical because of environment/library differences must **not** silently replace the authoritative object. Record it separately with its environment and numerical comparison.

## Integrity rule

For every downloaded or regenerated binary, calculate SHA-256 and compare it with the public manifests. A matching filename with a non-matching SHA-256 is **not** the study artifact.

## Release state

All URLs/DOI fields remain pending until the Git tree is frozen, assets are independently rehashed at transfer, the versioned GitHub Release is created, and the matching Zenodo deposit is minted. Only then should the manifests and `CITATION.cff` be updated with permanent release locations.
