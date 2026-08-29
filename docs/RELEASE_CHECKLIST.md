# Archival release checklist

The first GitHub/Zenodo release should not be tagged until all items below are complete.

- [x] Public code set promoted from SHA-verified evidence artifacts — exact checkpoint model source plus final M1--M5 analysis code are public and SHA-bound
- [x] Locked configurations promoted
- [x] Dataset split/index manifest promoted
- [x] Compact H1-0015--H1-0019 result artifacts promoted
- [x] Public numerical/reproducibility audits promoted
- [x] Large/restricted artifacts documented by exact SHA-256 and acquisition/reconstruction policy (`docs/ARTIFACT_ACQUISITION.md`)
- [x] GitHub Release / Zenodo asset plan locked (`manifests/TSPG_RELEASE_ASSET_PLAN_v1_0_20260829.json`), including de-duplication of binaries already contained in compact evidence ZIPs
- [x] Manuscript-to-artifact map completed with no `pending promotion` entries for reported M1--M5 numerical findings
- [x] Sanitized reference numerical environment captured and provenance-bound
- [x] Portable runtime dependency manifest and fail-closed path-overlay/staging helper implemented; static/plan QA passed (`audits/TSPG_PORTABLE_RUNTIME_HELPER_STATIC_QA_v1_0_20260829.md`)
- [ ] Transfer/materialize and independently rehash the standalone archival numerical binaries; all exact sizes are now known and H1-0019 fit-arm-bases verification is PASS, while transfer-time rehash is still required for the remaining standalone assets
- [ ] Clean-environment portable materialization and M1--M5 reproduction path tested end-to-end
- [ ] Exact non-PyTorch dependency lock finalized from the clean-environment test
- [ ] Public release SHA-256 manifest generated after the tree is frozen
- [x] Code/repository licensing selected and documented: MIT
- [x] Verify that no manuscript PDF/TEX/source, submission package, cover letter, reviewer/editor material, or internal manuscript-governance artifact is present in the GitHub working tree
- [ ] `CITATION.cff` updated with release version and Zenodo DOI for the reproducibility package
- [ ] GitHub release tagged
- [ ] Verified Learned seed-42 checkpoint attached to the versioned GitHub Release
- [ ] Five compact H1-0015--H1-0019 evidence ZIPs attached to the versioned GitHub Release
- [ ] Complete non-Git evidence set uploaded to the matching Zenodo record, including the checkpoint, compact evidence ZIPs, and standalone large numerical binaries
- [ ] Zenodo DOI minted from the immutable release package
- [ ] Data Availability and Code Availability statements updated with the persistent reproducibility-package DOI

## Current verification notes

As of 2026-08-29, the exact checkpoint model source and the exact non-superseded M1--M5 analysis code are SHA-bound by `manifests/CODE_SHA256.txt`; exact primary result identities are recorded in `manifests/RUN_RESULTS_SHA256.txt`; runtime evidence archives are recorded in `manifests/EVIDENCE_ARCHIVES_SHA256.txt`; and the M1--M5 public numerical mapping is complete in `docs/ARTIFACT_MAP.md`.

The release-preparation audit identified the exact model-definition source used to instantiate/load the checkpoint. The retained authoritative file has now been promoted at `code/model/full_scale_experiment.py`: 66,351 bytes, SHA-256 `83fc337128dec7f896c9816842806789a634154dea8372bb0a43bae19188d3bf`. Promotion was gated on exact size and SHA-256, and the resulting Git blob (`46a6f2343e5d064244a0180b992af1fcdf6ecc2e`) is byte-identical to the retained TSPG source. The earlier approximate/reconstructed substitute was not accepted.

The sanitized reference environment is published as `environment/TSPG_PUBLIC_NUMERICAL_ENVIRONMENT_v1_0_20260829.json`, derived from SHA-locked P0-0001 and P0-0003 runtime evidence. Host/login/UID/absolute-path fields are omitted, while Python/PyTorch/CUDA/cuDNN/GPU and numerical-backend settings are preserved.

The portable runtime layer is explicit rather than implicit. `manifests/TSPG_PORTABLE_RUNTIME_DEPENDENCIES_v1_0_20260829.json` enumerates the external M1--M5 input contract, including the previously omitted H1-0011 complement artifact. `tools/prepare_runtime_root.py` preserves the committed locked configs and creates only derived path/cache compatibility copies. Its syntax and five-target plan path passed static QA; materialization against the complete checkpoint/data/archive set remains deliberately open and is the next execution gate.

The repository is licensed under MIT via the root `LICENSE` file, and `CITATION.cff` records `license: MIT`.

The sole model checkpoint used by M1--M5 is the verified ViT-B/16 Learned seed-42 `best_model.pth` (343,559,209 bytes; SHA-256 `7fcca75916c2d6f0f64aa5c381812ad3a305ba1a04672e9288f4251ab683c536`). It is deliberately excluded from ordinary Git history and will be attached directly to the first versioned GitHub Release; no Google Drive/shared-folder dependency is part of the public checkpoint route.

The non-Git distribution boundary is fixed in `manifests/TSPG_RELEASE_ASSET_PLAN_v1_0_20260829.json`: GitHub Release receives the checkpoint plus five compact evidence ZIPs; Zenodo receives the same six convenience assets plus only the standalone large numerical binaries not already present inside those ZIPs. Recorded sizes are AG1 gradients (387,317,888 bytes), H1-0010 geometry (776,283,320), H1-0011 complement basis (79,126,618), H1-0015 tail geometry (232,412,532), AG2 gradients (387,317,888), H1-0016 derived cross-fold binary (390,626,716), AP gradients (774,635,648), and H1-0019 fit-arm bases (154,928,108). The fit-arm-bases object was directly materialized, opened successfully without pickle, and independently rehashed to the locked SHA-256 `8bfc5c8e4bc7c677a882974a61b4e66d540f230dbb75b690ffbfe42ea47fa4e3`; it contains four FP64 `(151296, 32)` arm matrices (`U320_AG1`, `U320_AG2`, `U640`, `CONS640`). The H1-0011 size was recovered from authoritative runtime metadata and still requires transfer-time byte verification. There are now no unknown asset sizes.

A recursive `main`-tree check after public promotion found no `.tex` or `.pdf` paths and no cover-letter path, consistent with the locked manuscript-exclusion policy. This check must be repeated on the final frozen release tree before tagging.
