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
- [ ] Code/data licensing selected and documented
- [x] Verify that no manuscript PDF/TEX/source, submission package, cover letter, reviewer/editor material, or internal manuscript-governance artifact is present in the GitHub working tree
- [ ] `CITATION.cff` updated with release version and Zenodo DOI for the reproducibility package
- [ ] GitHub release tagged
- [ ] Zenodo archive minted from the same immutable GitHub release
- [ ] Data Availability and Code Availability statements updated with the persistent reproducibility-package DOI

## Current verification notes

As of 2026-08-29, the final non-superseded M1--M5 code set is SHA-bound by `manifests/CODE_SHA256.txt`; exact primary result identities are recorded in `manifests/RUN_RESULTS_SHA256.txt`; runtime evidence archives are recorded in `manifests/EVIDENCE_ARCHIVES_SHA256.txt`; and the M1--M5 public mapping is complete in `docs/ARTIFACT_MAP.md`.

A recursive `main`-tree check after public promotion found no `.tex` or `.pdf` paths and no cover-letter path, consistent with the locked manuscript-exclusion policy. This check must be repeated on the final frozen release tree before tagging.

The remaining technical blockers before an immutable release are therefore environment/reconstruction verification and final release-manifest generation. Licensing and the DOI-dependent citation/submission updates remain explicit release decisions rather than inferred defaults.
