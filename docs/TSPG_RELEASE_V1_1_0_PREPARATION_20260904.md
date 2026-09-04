# TSPG public release v1.1.0 preparation

This branch prepares the next public reproducibility-package version. The existing `v1.0.0` GitHub/Zenodo release remains immutable and continues to identify the original M1--M5 package.

The v1.1.0 candidate extends the public evidence boundary with three already-closed components: the H1-0012 direction-level numerator/denominator decomposition, the pre-existing H1-0007 ALiBi exact dense structural control, and the A52 diagnostic-portability panel.

No manuscript PDF/TEX, submission material, editor/reviewer correspondence, or internal manuscript-governance documents are part of this public branch.

## Current staging state

A SHA-verified local candidate tree has been assembled for H1-0012, H1-0007, and A52 public-safe code/config/result/audit/manifest additions, together with eight supplemental non-Git evidence objects. Promotion of the remaining candidate files into this branch is the next Git-tree gate.

The four A52 checkpoints required for full model-level re-execution are staged and re-hashed: `PASS_STAGED_EXACT_4_OF_4`, aggregate `858,245,348` bytes. Public path-sanitized evidence is recorded in `manifests/TSPG_A52_CHECKPOINT_RELEASE_STAGING_MANIFEST_PUBLIC_v1_0_20260904.json`, `manifests/TSPG_A52_CHECKPOINT_RELEASE_STAGING_SHA256_v1_0_20260904.txt`, and `audits/TSPG_A52_CHECKPOINT_RELEASE_STAGING_VERIFICATION_v1_0_20260904.md`. These four checkpoint binaries are designated for the DOI-bearing Zenodo v1.1.0 payload; GitHub Release duplication is not required.

The complete new Zenodo v1.1.0 payload has now also been staged locally and verified source -> copy for all 12 objects: eight supplemental evidence objects plus the four A52 checkpoints, aggregate `871,089,498` bytes (`12/12 PASS`). The formal gate record is `audits/TSPG_ZENODO_V1_1_0_UPLOAD_STAGING_VERIFICATION_v1_0_20260904.md`.

The current public version DOI is `10.5281/zenodo.22180107`; the stable all-versions DOI is `10.5281/zenodo.22180106`. The v1.1.0 version DOI will be recorded only after the new Zenodo version is reserved/published.

Reporting-level/reduced-matrix A52 verification is already supported by the compact evidence archives. The checkpoint-binary and local Zenodo byte-staging gates for full model-level public reproduction are closed. Remaining blockers are exact public-tree promotion/verification, the public A52 compatibility-overlay verification, Zenodo DOI reservation/publication, and post-publication remote SHA verification.
