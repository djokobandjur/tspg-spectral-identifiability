# Archival release checklist

The first GitHub/Zenodo release should not be tagged or published until all applicable items below are complete.

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
- [x] Standalone Zenodo release staging complete: 8/8 staged copies match locked SHA-256 identities (`manifests/TSPG_ZENODO_STANDALONE_STAGING_SHA256_v1_0_20260829.txt`; `manifests/TSPG_ZENODO_STANDALONE_STAGING_MANIFEST_PUBLIC_v1_0_20260829.json`; `audits/TSPG_ZENODO_STANDALONE_STAGING_SHA_VERIFICATION_v1_0_20260829.md`)
- [x] Convenience-asset release staging complete: checkpoint + five compact H1-0015--H1-0019 evidence ZIPs are 6/6 exact staged-copy SHA-256 matches (`manifests/TSPG_CONVENIENCE_ASSETS_STAGING_SHA256_v1_0_20260829.txt`; `manifests/TSPG_CONVENIENCE_ASSETS_STAGING_MANIFEST_PUBLIC_v1_0_20260829.json`; `audits/TSPG_CONVENIENCE_ASSETS_STAGING_VERIFICATION_v1_0_20260829.md`)
- [x] Clean-environment portable materialization completed from a fresh FMLE session: public clone pinned to `53c7ff9dc8afcc7ff782a6d2f340d8e183acbcf4`, five evidence archives extracted, 11 external artifacts staged, 0 missing, all helper checks PASS (`audits/TSPG_CLEAN_ENVIRONMENT_PORTABLE_MATERIALIZATION_v1_0_20260829.md`)
- [x] Sequential clean-environment M1--M5 execution and numerical reproduction audit completed end-to-end (`audits/TSPG_CLEAN_ENVIRONMENT_M1_M5_END_TO_END_REPRODUCTION_v1_0_20260830.md`)
- [x] Exact non-PyTorch dependency lock finalized from the successful clean-environment execution test (`audits/TSPG_CLEAN_EXECUTION_DEPENDENCY_LOCK_VERIFICATION_v1_0_20260830.md`)
- [x] Code/repository licensing selected and documented: MIT
- [x] Verify that no manuscript PDF/TEX/source, submission package, cover letter, reviewer/editor material, or internal manuscript-governance artifact is present in the GitHub working tree
- [x] Zenodo DOI reserved for release `1.0.0`: `10.5281/zenodo.22180107`
- [x] `CITATION.cff` updated with release version `1.0.0` and reserved Zenodo DOI
- [x] Complete 14-file non-Git evidence set uploaded to the saved Zenodo draft; all 14 entries reached 100% with concrete size/checksum display (`audits/TSPG_ZENODO_DRAFT_UPLOAD_AND_RESERVED_DOI_v1_0_20260830.md`)
- [ ] Public release SHA-256 manifest generated and verified after the final metadata tree is frozen
- [ ] GitHub release `v1.0.0` tagged
- [ ] Verified Learned seed-42 checkpoint attached to the versioned GitHub Release
- [ ] Five compact H1-0015--H1-0019 evidence ZIPs attached to the versioned GitHub Release
- [ ] Saved Zenodo draft published, registering DOI `10.5281/zenodo.22180107`
- [ ] Published GitHub/Zenodo assets reverified against the locked identities
- [ ] Data Availability and Code Availability statements updated with the persistent reproducibility-package DOI

## Current verification notes

The exact checkpoint model source and the exact non-superseded M1--M5 analysis code are SHA-bound by `manifests/CODE_SHA256.txt`; exact primary result identities are recorded in `manifests/RUN_RESULTS_SHA256.txt`; runtime evidence archives are recorded in `manifests/EVIDENCE_ARCHIVES_SHA256.txt`; and the M1--M5 public numerical mapping is complete in `docs/ARTIFACT_MAP.md`.

The exact model-definition source is public at `code/model/full_scale_experiment.py`: 66,351 bytes, SHA-256 `83fc337128dec7f896c9816842806789a634154dea8372bb0a43bae19188d3bf`. The sanitized reference numerical environment and the exact clean-execution dependency capture are public under `environment/` and `manifests/`.

The fresh clean environment completed portable materialization followed by M1, M2 gate/full, M3, M4, and M5 fit gate/full. Every scientific/numerical field compared against authoritative evidence reproduced exactly; eleven checked generated numerical/runtime artifacts reproduced their authoritative SHA-256 identities. The end-to-end gate is closed by `audits/TSPG_CLEAN_ENVIRONMENT_M1_M5_END_TO_END_REPRODUCTION_v1_0_20260830.md`.

The non-Git release payload is exactly 14 files totaling 3,535,908,885 bytes: the checkpoint, five compact evidence ZIPs, and eight standalone numerical objects. Source/staging copies were SHA-verified before upload; the consolidated payload was again SHA-verified 14/14 after FMLE-to-removable-storage transfer. The saved Zenodo draft now contains all 14 files at 100% completion. This closes the draft-upload/file-presence gate but not post-publication remote SHA verification.

`CITATION.cff` now records release version `1.0.0`, date `2026-08-30`, and reserved DOI `10.5281/zenodo.22180107`. The DOI remains reserved until the Zenodo draft is published.

A previous 90-file pre-freeze candidate at commit `43f1a67578ec658220f73df4eb84569a25fb9430` passed the manuscript-exclusion/tree check, with candidate manifest SHA-256 `6af4f12371926a0f4d92182407f8b242c8ab3052e19078c681993c4e23f757f3`. That candidate predates the DOI/release-metadata updates and must **not** be used as the final release manifest.

The next release blocker is the final fresh-clone freeze check and release-level SHA-256 manifest. No further ordinary metadata edits should be made after that final content boundary except the explicitly scoped release-manifest commit itself.
