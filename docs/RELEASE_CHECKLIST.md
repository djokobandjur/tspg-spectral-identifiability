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
- [x] `CITATION.cff` updated with release version `1.0.0` and version DOI
- [x] Complete 14-file non-Git evidence set uploaded to the saved Zenodo draft
- [x] Public release SHA-256 manifest generated and verified after the final metadata tree was frozen: content commit `535eb0e7efc6e983b042d63fa420859a3391e618`, 92 tracked files, manifest SHA-256 `d39ed8cf39c419a7e26ac676a091a8457705de6a833f72fa6a1908a3a34d53fe`
- [x] GitHub release `v1.0.0` tagged at release-manifest commit `2292cb17afb105572a9ac86de5ff33419033b073`
- [x] Verified Learned seed-42 checkpoint attached to the versioned GitHub Release
- [x] Five compact H1-0015--H1-0019 evidence ZIPs attached to the versioned GitHub Release; public GitHub API verification is 6/6 exact size + SHA-256 PASS after correction of the initially mis-selected H1-0016 ZIP
- [x] Zenodo record published, registering version DOI `10.5281/zenodo.22180107` (all-versions DOI `10.5281/zenodo.22180106`)
- [ ] Published GitHub/Zenodo assets reverified against the locked identities — GitHub 6/6 PASS; independent post-publication Zenodo retrieval/checksum verification still pending
- [ ] Data Availability and Code Availability statements updated with the persistent reproducibility-package DOI

## Current verification notes

The final public content tree is bound by `manifests/TSPG_PUBLIC_RELEASE_TREE_SHA256_v1_0_20260830.txt` and the associated freeze audits. GitHub release `v1.0.0` targets `2292cb17afb105572a9ac86de5ff33419033b073` and its six planned convenience assets have been independently checked against the locked public SHA-256 identities.

Before Zenodo publication, an H1-0016 ZIP with the correct filename but wrong bytes (`169389` bytes; SHA-256 `4622a6dcc17f212b95959744b248c47b0e49ea4c28cddc49959397785f7931e4`) was detected on the GitHub release. It was replaced by the authoritative archive (`144501` bytes; SHA-256 `0d7c6acfe8e38826fbb36322f30f187f9442d4ea42253e9463328d004062e022`). The unpublished Zenodo draft was corrected before publication; the corrected entry displayed MD5 `324b13e35f384c851657b4e583668d92`. See `audits/TSPG_PUBLICATION_AND_GITHUB_RELEASE_VERIFICATION_v1_0_20260831.md`.

The Zenodo record is now public as version `1.0.0`. For exact release pinning, use version DOI `10.5281/zenodo.22180107`; Zenodo's all-versions DOI is `10.5281/zenodo.22180106`. Independent post-publication retrieval and checksum verification of all 14 Zenodo files remains the final archive-integrity gate before the release verification checklist can be fully closed.
