# Zenodo draft upload and reserved DOI verification

**Date:** 2026-08-30  
**Release:** `v1.0.0`  
**Reserved DOI:** `10.5281/zenodo.22180107`  
**Status:** `PASS_DRAFT_UPLOAD_COMPLETE_REMOTE_SHA256_PENDING_PUBLICATION`

## Scope

This record documents the transition from the already SHA-verified non-Git release staging area to the saved Zenodo draft for the first TSPG reproducibility release. It does **not** declare the Zenodo record published and it does **not** substitute Zenodo's displayed MD5 values for the locked SHA-256 identities.

## Pre-upload integrity boundary

The release payload is exactly 14 files totaling `3,535,908,885` bytes:

- six convenience assets: the Learned seed-42 checkpoint plus five compact H1-0015--H1-0019 runtime-evidence ZIPs;
- eight standalone numerical assets.

The six convenience assets were previously verified as exact staged-copy SHA-256 matches by `TSPG_CONVENIENCE_ASSETS_STAGING_VERIFICATION_v1_0_20260829.md` and `../manifests/TSPG_CONVENIENCE_ASSETS_STAGING_SHA256_v1_0_20260829.txt`.

The eight standalone numerical assets were previously verified as exact staged-copy SHA-256 matches by `TSPG_ZENODO_STANDALONE_STAGING_SHA_VERIFICATION_v1_0_20260829.md` and `../manifests/TSPG_ZENODO_STANDALONE_STAGING_SHA256_v1_0_20260829.txt`.

Before browser upload, the consolidated 14-file payload was rechecked after transfer from FMLE to removable storage; all 14 local copies matched the locked SHA-256 identities (`14/14 PASS`).

## Zenodo draft state

The Zenodo draft reserved DOI `10.5281/zenodo.22180107` for software release `1.0.0`.

After upload recovery was performed one file at a time for entries that initially stalled, the saved draft UI reported:

- `14 out of 100 files`;
- aggregate displayed size `3.54 GB`;
- all 14 entries at `100%`;
- a concrete size and Zenodo MD5 checksum displayed for every entry;
- no remaining `Pending`, `N/A`, or partial-progress entry.

The draft was then saved. It has **not** been published.

## Interpretation

The upload-completion gate is closed at the UI/file-presence level. The authoritative scientific identity of every payload remains its locked SHA-256 value from the public manifests. Post-publication retrieval/checksum verification remains a separate pending gate because the unpublished Zenodo draft is not yet the immutable public archival object.

## Remaining release gates

1. Freeze the final public Git tree after all DOI/release metadata edits.
2. Generate and verify the final release-level SHA-256 tree manifest.
3. Create/tag GitHub release `v1.0.0` and attach the six planned convenience assets.
4. Publish the saved Zenodo draft, thereby registering the reserved DOI.
5. Verify the published Zenodo/GitHub assets against the locked identities and close availability statements.
