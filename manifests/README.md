# Manifests

This directory contains the public manifests needed to reconstruct and verify the analyzed model/data state without redistributing restricted source material.

Current public provenance layers include:

- `TSPG_USED_ANALYSIS_SPLIT_INDICES_PUBLIC_v1_0_20260829.json` — exact semantic copy of all sample indices used by the reported M1--M5 analyses, tied to the locked canonical split hashes.
- `TSPG_LEARNED_SEED42_CHECKPOINT_MANIFEST_v1_0_20260829.json` — checkpoint identity, size, SHA-256, model-source identity, and GitHub-Release acquisition route for the instrumented Learned seed-42 model.
- `TSPG_PORTABLE_RUNTIME_DEPENDENCIES_v1_0_20260829.json` — machine-readable M1--M5 external-input contract, including each required upstream control/binary SHA and whether it is an archival dependency or a reproducible late-stage output.
- `TSPG_RELEASE_ASSET_PLAN_v1_0_20260829.json` — locked coordinated GitHub Release / Zenodo asset plan, including exact compact-evidence ZIP identities, standalone archival binaries, staged-verification state, and de-duplication rules for binaries already contained inside evidence ZIPs.
- `TSPG_RELEASE_STATUS_v1_0_20260830.json` — current `v1.0.0` release state: reserved Zenodo DOI, saved-draft upload completion, final content-tree freeze PASS, and pending GitHub/Zenodo publication gates.
- `TSPG_PUBLIC_RELEASE_TREE_SHA256_v1_0_20260830.txt` — final 92-entry SHA-256 manifest for every Git-tracked regular file in frozen content commit `535eb0e7efc6e983b042d63fa420859a3391e618`; manifest SHA-256 `d39ed8cf39c419a7e26ac676a091a8457705de6a833f72fa6a1908a3a34d53fe`.
- `TSPG_ZENODO_STANDALONE_STAGING_SHA256_v1_0_20260829.txt` — exact eight-entry SHA-256 manifest emitted for the staged standalone Zenodo numerical payload; all eight entries match their locked identities.
- `TSPG_ZENODO_STANDALONE_STAGING_MANIFEST_PUBLIC_v1_0_20260829.json` — sanitized public semantic copy of the generated standalone staging metadata: `PASS_8_OF_8`, total payload size, per-artifact filename/size/SHA/status, plus the exact private staging-manifest size/SHA binding. Host-local absolute path and username are intentionally omitted.
- `TSPG_CONVENIENCE_ASSETS_STAGING_SHA256_v1_0_20260829.txt` — exact six-entry SHA-256 manifest for the staged checkpoint plus five compact runtime-evidence ZIPs; all six entries match their locked identities.
- `TSPG_CONVENIENCE_ASSETS_STAGING_MANIFEST_PUBLIC_v1_0_20260829.json` — sanitized public semantic copy of the convenience-assets staging metadata: `PASS_6_OF_6`, aggregate payload size, per-artifact filename/size/SHA/status, and exact bindings to the supplied private JSON/checksum manifests.
- `TSPG_CLEAN_EXECUTION_DEPENDENCY_CAPTURE_SHA256_v1_0_20260830.txt` — exact SHA-256 identities for the clean-execution dependency-capture files.
- `CODE_SHA256.txt` — SHA-256 identities of the exact final non-superseded public analysis code and the exact promoted checkpoint model-definition source.
- `RUN_RESULTS_SHA256.txt` — SHA-256 identities of the exact primary H1-0015--H1-0019 result JSON bytes in the authoritative runtime evidence archives.
- `EVIDENCE_ARCHIVES_SHA256.txt` — SHA-256 identities of the authoritative compact H1-0015--H1-0019 runtime evidence ZIP archives.
- `EVIDENCE_ARCHIVES_PUBLIC_INDEX.csv` — public mapping for those evidence archives.
- `LARGE_ARTIFACTS_SHA256.csv` — identities, verified sizes, and distribution status of large artifacts that are not stored in ordinary Git history, including the H1-0011 M1 complement dependency.

`tools/prepare_runtime_root.py` uses the provenance manifests to construct a fail-closed portable runtime overlay without altering committed locked configs. The scientific/reproducibility content tree is frozen at commit `535eb0e7efc6e983b042d63fa420859a3391e618`; its complete tracked-file SHA-256 manifest is promoted in the successor release-manifest envelope. The intended `v1.0.0` tag target is that release-manifest commit, while the manifest's `content_commit` remains the authoritative pre-envelope content boundary.
