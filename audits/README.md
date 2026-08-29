# Audits

This directory contains the public numerical-certification, ingest, interpretation, and formal-closeout records supporting the reported M1--M5 results.

The audit layer deliberately preserves the distinction between a scientific result and a numerical, implementation, or governance artifact. A reported finding is therefore accompanied by the checks needed to establish what was computed, which gates passed or failed, what interpretation was authorized, and whether any follow-up computation was permitted.

Current public coverage includes:

- H1-0015 formal closeout for the matched-rank boundary/complement diagnostic (M1);
- H1-0016 ingest/interpretation plus the review-resolution/design-rationale record that closes the development trigger before H1-0017 (M2);
- H1-0017 ingest/interpretation and formal closeout for the B-normalized cross-fit audit (M3);
- H1-0018 ingest/interpretation and formal closeout for the finite-sample support/orientation audit (M4);
- H1-0019 ingest/interpretation and formal closeout for the final matched-sample consensus estimator (M5);
- `TSPG_STANDALONE_LARGE_ARTIFACT_SOURCE_BYTE_VERIFICATION_v1_0_20260829.md`, which records the pre-release size/SHA-256 verification of all eight standalone Zenodo numerical assets (`8/8 PASS`);
- `TSPG_ZENODO_STANDALONE_STAGING_SHA_VERIFICATION_v1_0_20260829.md`, which records the completed standalone release-staging gate: all eight staged copies match their locked SHA-256 identities and the generated staging metadata reports `PASS_8_OF_8`;
- `TSPG_CONVENIENCE_ASSETS_STAGING_VERIFICATION_v1_0_20260829.md`, which records the completed convenience-assets staging gate: the checkpoint plus five compact H1-0015--H1-0019 evidence ZIPs are `6/6` exact staged-copy SHA-256 matches.

Machine-readable static-QA and gate outputs are promoted under `../results/`. Authoritative compact runtime evidence archives are identified by SHA-256 under `../manifests/`; large raw arrays remain outside Git and are referenced by exact hashes rather than duplicated here.
