# Audits

This directory contains the public numerical-certification, ingest, interpretation, formal-closeout, environment, and release-integrity records supporting the reported M1--M5 results and the archival package.

The audit layer deliberately preserves the distinction between a scientific result and a numerical, implementation, release, or governance artifact. A reported finding is therefore accompanied by the checks needed to establish what was computed, which gates passed or failed, what interpretation was authorized, and whether any follow-up computation or release action was permitted.

Current public coverage includes:

- H1-0015 formal closeout for the matched-rank boundary/complement diagnostic (M1);
- H1-0016 ingest/interpretation plus the review-resolution/design-rationale record that closes the development trigger before H1-0017 (M2);
- H1-0017 ingest/interpretation and formal closeout for the B-normalized cross-fit audit (M3);
- H1-0018 ingest/interpretation and formal closeout for the finite-sample support/orientation audit (M4);
- H1-0019 ingest/interpretation and formal closeout for the final matched-sample consensus estimator (M5);
- `TSPG_STANDALONE_LARGE_ARTIFACT_SOURCE_BYTE_VERIFICATION_v1_0_20260829.md`, which records pre-release size/SHA-256 verification of all eight standalone Zenodo numerical assets (`8/8 PASS`);
- `TSPG_ZENODO_STANDALONE_STAGING_SHA_VERIFICATION_v1_0_20260829.md`, which records the completed standalone release-staging gate: all eight staged copies match their locked SHA-256 identities;
- `TSPG_CONVENIENCE_ASSETS_STAGING_VERIFICATION_v1_0_20260829.md`, which records the completed convenience-assets staging gate: the checkpoint plus five compact H1-0015--H1-0019 evidence ZIPs are `6/6` exact staged-copy SHA-256 matches;
- `TSPG_CLEAN_ENVIRONMENT_PORTABLE_MATERIALIZATION_v1_0_20260829.md`, which records the fresh-session portable materialization PASS: public commit pinned, five evidence archives extracted, all M1--M5 targets prepared, 11 external artifacts SHA-verified and zero missing inputs;
- `TSPG_CLEAN_ENVIRONMENT_M1_M2_REPRODUCTION_PROGRESS_v1_0_20260830.md`, which records sequential clean-execution progress through M2;
- `TSPG_CLEAN_ENVIRONMENT_M3_REPRODUCTION_v1_0_20260830.md`, which records the sequential clean M3 PASS and exact generated derived-object byte match;
- `TSPG_CLEAN_ENVIRONMENT_M4_REPRODUCTION_v1_0_20260830.md`, which records the sequential clean M4 PASS, exact scientific/numerical reproduction, and exact generated-artifact matches while retaining the corrected public H1-0018 reporting source;
- `TSPG_CLEAN_ENVIRONMENT_M1_M5_END_TO_END_REPRODUCTION_v1_0_20260830.md`, which closes the clean execution gate: the complete M1--M5 chain is `PASS_END_TO_END_M1_M5` with eleven checked generated numerical/runtime artifacts matching their authoritative SHA-256 identities;
- `TSPG_CLEAN_EXECUTION_DEPENDENCY_LOCK_VERIFICATION_v1_0_20260830.md`, which closes the clean-environment dependency-lock gate: the direct source-level dependency lock, complete 302-distribution inventory, and NumPy/SciPy backend capture are checksum-verified and promoted byte-for-byte;
- `TSPG_ZENODO_DRAFT_UPLOAD_AND_RESERVED_DOI_v1_0_20260830.md`, which records reserved DOI `10.5281/zenodo.22180107`, the pre-upload 14-file SHA-verified boundary, and completion of all 14 files in the saved Zenodo draft while explicitly leaving post-publication remote checksum verification pending.

Machine-readable static-QA and gate outputs are promoted under `../results/`. Authoritative compact runtime evidence archives, clean-execution dependency-capture identities, and current release state are recorded under `../manifests/`; large raw arrays remain outside Git and are referenced by exact hashes rather than duplicated here.
