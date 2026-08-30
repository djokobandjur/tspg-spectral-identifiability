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
- [x] Standalone Zenodo numerical set identified and independently source-byte verified: 8/8 exact size/SHA-256 PASS (`audits/TSPG_STANDALONE_LARGE_ARTIFACT_SOURCE_BYTE_VERIFICATION_v1_0_20260829.md`)
- [x] Standalone Zenodo release staging complete: 8/8 staged copies match locked SHA-256 identities; checksum and sanitized metadata manifests promoted (`manifests/TSPG_ZENODO_STANDALONE_STAGING_SHA256_v1_0_20260829.txt`; `manifests/TSPG_ZENODO_STANDALONE_STAGING_MANIFEST_PUBLIC_v1_0_20260829.json`; `audits/TSPG_ZENODO_STANDALONE_STAGING_SHA_VERIFICATION_v1_0_20260829.md`)
- [x] Convenience-asset release staging complete: checkpoint + five compact H1-0015--H1-0019 evidence ZIPs are 6/6 exact staged-copy SHA-256 matches (`manifests/TSPG_CONVENIENCE_ASSETS_STAGING_SHA256_v1_0_20260829.txt`; `manifests/TSPG_CONVENIENCE_ASSETS_STAGING_MANIFEST_PUBLIC_v1_0_20260829.json`; `audits/TSPG_CONVENIENCE_ASSETS_STAGING_VERIFICATION_v1_0_20260829.md`)
- [x] Clean-environment portable materialization completed from a fresh FMLE session: public clone pinned to `53c7ff9dc8afcc7ff782a6d2f340d8e183acbcf4`, five evidence archives extracted, 11 external artifacts staged, 0 missing, all helper checks PASS (`audits/TSPG_CLEAN_ENVIRONMENT_PORTABLE_MATERIALIZATION_v1_0_20260829.md`)
- [x] Sequential clean-environment M1--M5 execution and numerical reproduction audit completed end-to-end (`audits/TSPG_CLEAN_ENVIRONMENT_M1_M5_END_TO_END_REPRODUCTION_v1_0_20260830.md`)
- [x] Exact non-PyTorch dependency lock finalized from the successful clean-environment execution test; direct dependency lock, complete installed-distribution inventory, numerical backend capture, and checksum manifest promoted (`audits/TSPG_CLEAN_EXECUTION_DEPENDENCY_LOCK_VERIFICATION_v1_0_20260830.md`)
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

The portable runtime layer is explicit rather than implicit. `manifests/TSPG_PORTABLE_RUNTIME_DEPENDENCIES_v1_0_20260829.json` enumerates the external M1--M5 input contract, including the H1-0011 complement artifact. `tools/prepare_runtime_root.py` preserves the committed locked configs and creates only derived path/cache compatibility copies. Static/plan QA had already passed; the fresh-session materialization test also passed in `MATERIALIZED` mode with targets `M1`--`M5`, 11 staged external artifacts and zero missing inputs.

The same clean environment then completed the sequential M1--M5 execution chain. M1, M2 gate/full, M3, M4, and M5 fit gate/full all passed. Every scientific/numerical field compared against authoritative evidence reproduced exactly; runtime JSON differences were limited to host-local paths, timing, peak-memory metadata, or a gate-JSON SHA induced by local path differences. Eleven checked generated numerical/runtime artifacts reproduced their authoritative SHA-256 identities exactly, including the M5 fit lock, fit-arm bases, AP640 gradients, and AP per-example capture. The clean execution gate is therefore closed by `audits/TSPG_CLEAN_ENVIRONMENT_M1_M5_END_TO_END_REPRODUCTION_v1_0_20260830.md`.

The fresh materialization/execution session matched the captured core numerical stack: Python 3.12.3, PyTorch `2.8.0a0+5228986c39.nv25.06`, CUDA 12.9, and NVIDIA H200. The same successful environment was then dependency-captured. The source-level external import scan covered 18 public Python files plus the portable-runtime helper and resolved direct versions for matplotlib 3.10.3, NumPy 1.26.4, scikit-learn 1.6.1, SciPy 1.15.3, torchvision `0.22.0a0+95f10a4e`, and tqdm 4.67.1; PyTorch remains a separately recorded custom NVIDIA reference identity. A complete sanitized inventory of 302 installed distributions and the NumPy/SciPy backend configuration were also promoted byte-for-byte and bound by `manifests/TSPG_CLEAN_EXECUTION_DEPENDENCY_CAPTURE_SHA256_v1_0_20260830.txt`. The dependency-lock gate is closed by `audits/TSPG_CLEAN_EXECUTION_DEPENDENCY_LOCK_VERIFICATION_v1_0_20260830.md`.

The repository is licensed under MIT via the root `LICENSE` file, and `CITATION.cff` records `license: MIT`.

The sole model checkpoint used by M1--M5 is the verified ViT-B/16 Learned seed-42 `best_model.pth` (343,559,209 bytes; SHA-256 `7fcca75916c2d6f0f64aa5c381812ad3a305ba1a04672e9288f4251ab683c536`). It is deliberately excluded from ordinary Git history and will be attached directly to the first versioned GitHub Release; no Google Drive/shared-folder dependency is part of the public checkpoint route.

The non-Git release-upload workspace is fully staged and byte-verified. The standalone Zenodo payload contains eight objects totaling 3,182,648,718 bytes with 8/8 staged-copy SHA-256 matches. The convenience payload contains the checkpoint plus five compact evidence ZIPs totaling 353,260,167 bytes with 6/6 staged-copy SHA-256 matches. Upload to GitHub Release/Zenodo and post-upload verification remain separate pending gates.

The next release blocker is now to freeze the public Git tree, repeat the manuscript-exclusion scan on that frozen tree, and generate the final release-level SHA-256 manifest before tagging.
