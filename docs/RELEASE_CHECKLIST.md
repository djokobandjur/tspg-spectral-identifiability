# Archival release checklist

The first GitHub/Zenodo release should not be tagged until all items below are complete.

- [x] Public code set promoted from SHA-verified evidence artifacts
- [x] Locked configurations promoted
- [x] Dataset split/index manifest promoted
- [x] Compact H1-0015--H1-0019 result artifacts promoted
- [x] Public numerical/reproducibility audits promoted
- [ ] Large/restricted artifacts documented by exact SHA-256 **and acquisition/reconstruction instructions**
- [x] Manuscript-to-artifact map completed with no `pending promotion` entries for reported M1--M5 results
- [ ] Clean-environment reproduction instructions tested
- [ ] Public release SHA-256 manifest generated after the tree is frozen
- [x] Code/repository licensing selected and documented: MIT
- [x] Verify that no manuscript PDF/TEX/source, submission package, cover letter, reviewer/editor material, or internal manuscript-governance artifact is present in the GitHub working tree
- [ ] `CITATION.cff` updated with release version and Zenodo DOI for the reproducibility package
- [ ] GitHub release tagged
- [ ] Verified Learned seed-42 checkpoint attached to the versioned GitHub Release
- [ ] Zenodo archive minted from the same immutable GitHub release
- [ ] Data Availability and Code Availability statements updated with the persistent reproducibility-package DOI

## Current verification notes

As of 2026-08-29, the final non-superseded M1--M5 code set is SHA-bound by `manifests/CODE_SHA256.txt`; exact primary result identities are recorded in `manifests/RUN_RESULTS_SHA256.txt`; runtime evidence archives are recorded in `manifests/EVIDENCE_ARCHIVES_SHA256.txt`; and the M1--M5 public mapping is complete in `docs/ARTIFACT_MAP.md`.

The repository is licensed under MIT via the root `LICENSE` file, and `CITATION.cff` records `license: MIT`.

The sole model checkpoint used by M1--M5 is the verified ViT-B/16 Learned seed-42 `best_model.pth` (343,559,209 bytes; SHA-256 `7fcca75916c2d6f0f64aa5c381812ad3a305ba1a04672e9288f4251ab683c536`). It is deliberately excluded from ordinary Git history and will be attached directly to the first versioned GitHub Release; no Google Drive/shared-folder dependency is planned.

A recursive `main`-tree check after public promotion found no `.tex` or `.pdf` paths and no cover-letter path, consistent with the locked manuscript-exclusion policy. This check must be repeated on the final frozen release tree before tagging.

The remaining technical blockers before an immutable release are environment/reconstruction verification, large-artifact acquisition/reconstruction documentation, and final release-manifest generation. DOI-dependent citation/submission updates remain pending until the immutable archive exists.
