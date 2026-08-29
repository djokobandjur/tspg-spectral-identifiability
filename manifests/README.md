# Manifests

This directory contains the public manifests needed to reconstruct and verify the analyzed model/data state without redistributing restricted source material.

Current public provenance layers include:

- `TSPG_USED_ANALYSIS_SPLIT_INDICES_PUBLIC_v1_0_20260829.json` — exact semantic copy of all sample indices used by the reported M1--M5 analyses, tied to the locked canonical split hashes.
- `TSPG_LEARNED_SEED42_CHECKPOINT_MANIFEST_v1_0_20260829.json` — checkpoint identity and SHA-256 metadata for the instrumented Learned seed-42 model.
- `CODE_SHA256.txt` — SHA-256 identities of the exact final non-superseded public analysis code copied from the locked execution starters.
- `RUN_RESULTS_SHA256.txt` — SHA-256 identities of the exact primary H1-0015--H1-0019 result JSON bytes in the authoritative runtime evidence archives.
- `EVIDENCE_ARCHIVES_SHA256.txt` — SHA-256 identities of the authoritative compact H1-0015--H1-0019 runtime evidence ZIP archives.
- `EVIDENCE_ARCHIVES_PUBLIC_INDEX.csv` — public mapping for those evidence archives.
- `LARGE_ARTIFACTS_SHA256.csv` — identities and roles of large artifacts that are not stored in Git.

The working `main` branch is not the immutable archival object. The release-level manifest will be generated only after the public tree is frozen; the tagged GitHub release and Zenodo archive will then share one versioned provenance boundary.
