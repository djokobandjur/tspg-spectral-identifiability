# Archival release checklist

The first GitHub/Zenodo release should not be tagged until all items below are complete.

- [ ] Public code set promoted from SHA-verified evidence artifacts — M1--M5 analysis code is complete; exact checkpoint model source `full_scale_experiment.py` (SHA-256 `83fc337128dec7f896c9816842806789a634154dea8372bb0a43bae19188d3bf`) remains to be promoted byte-for-byte
- [x] Locked configurations promoted
- [x] Dataset split/index manifest promoted
- [x] Compact H1-0015--H1-0019 result artifacts promoted
- [x] Public numerical/reproducibility audits promoted
- [x] Large/restricted artifacts documented by exact SHA-256 and acquisition/reconstruction policy (`docs/ARTIFACT_ACQUISITION.md`); actual release/Zenodo uploads remain separate release steps below
- [x] Manuscript-to-artifact map completed with no `pending promotion` entries for reported M1--M5 numerical findings
- [x] Sanitized reference numerical environment captured and provenance-bound
- [x] Portable runtime dependency manifest and fail-closed path-overlay/staging helper implemented; static/plan QA passed (`audits/TSPG_PORTABLE_RUNTIME_HELPER_STATIC_QA_v1_0_20260829.md`)
- [ ] Clean-environment portable materialization and M1--M5 reproduction path tested end-to-end
- [ ] Exact non-PyTorch dependency lock finalized from the clean-environment test
- [ ] Public release SHA-256 manifest generated after the tree is frozen
- [x] Code/repository licensing selected and documented: MIT
- [x] Verify that no manuscript PDF/TEX/source, submission package, cover letter, reviewer/editor material, or internal manuscript-governance artifact is present in the GitHub working tree
- [ ] `CITATION.cff` updated with release version and Zenodo DOI for the reproducibility package
- [ ] GitHub release tagged
- [ ] Verified Learned seed-42 checkpoint attached to the versioned GitHub Release
- [ ] Remaining archival evidence/large numerical assets uploaded to the immutable release/Zenodo record as specified by the acquisition policy
- [ ] Zenodo archive minted from the same immutable GitHub release
- [ ] Data Availability and Code Availability statements updated with the persistent reproducibility-package DOI

## Current verification notes

As of 2026-08-29, the exact non-superseded M1--M5 **analysis** code is SHA-bound by `manifests/CODE_SHA256.txt`; exact primary result identities are recorded in `manifests/RUN_RESULTS_SHA256.txt`; runtime evidence archives are recorded in `manifests/EVIDENCE_ARCHIVES_SHA256.txt`; and the M1--M5 public numerical mapping is complete in `docs/ARTIFACT_MAP.md`.

The release-preparation audit found one additional reproducibility dependency that had not yet been promoted: the exact model-definition source used to instantiate/load the checkpoint. A retained copy has been recovered and independently SHA-verified as `83fc337128dec7f896c9816842806789a634154dea8372bb0a43bae19188d3bf`. An approximate/reconstructed substitute was explicitly rejected; the authoritative byte sequence must be promoted before the code checkbox can close.

The sanitized reference environment is published as `environment/TSPG_PUBLIC_NUMERICAL_ENVIRONMENT_v1_0_20260829.json`, derived from SHA-locked P0-0001 and P0-0003 runtime evidence. Host/login/UID/absolute-path fields are omitted, while Python/PyTorch/CUDA/cuDNN/GPU and numerical-backend settings are preserved.

The portable runtime layer is now explicit rather than implicit. `manifests/TSPG_PORTABLE_RUNTIME_DEPENDENCIES_v1_0_20260829.json` enumerates the external M1--M5 input contract, including the previously omitted H1-0011 complement artifact. `tools/prepare_runtime_root.py` preserves the committed locked configs and creates only derived path/cache compatibility copies. Its syntax and five-target plan path passed static QA; materialization against the complete checkpoint/data/archive set remains deliberately open and is the next execution gate.

The repository is licensed under MIT via the root `LICENSE` file, and `CITATION.cff` records `license: MIT`.

The sole model checkpoint used by M1--M5 is the verified ViT-B/16 Learned seed-42 `best_model.pth` (343,559,209 bytes; SHA-256 `7fcca75916c2d6f0f64aa5c381812ad3a305ba1a04672e9288f4251ab683c536`). It is deliberately excluded from ordinary Git history and will be attached directly to the first versioned GitHub Release; no Google Drive/shared-folder dependency is part of the public checkpoint route.

Large-artifact identities and their archival/regeneration roles are documented in `manifests/LARGE_ARTIFACTS_SHA256.csv`, `manifests/TSPG_PORTABLE_RUNTIME_DEPENDENCIES_v1_0_20260829.json`, and `docs/ARTIFACT_ACQUISITION.md`. Final storage URLs remain unset until the immutable release/Zenodo record is created.

A recursive `main`-tree check after public promotion found no `.tex` or `.pdf` paths and no cover-letter path, consistent with the locked manuscript-exclusion policy. This check must be repeated on the final frozen release tree before tagging.
