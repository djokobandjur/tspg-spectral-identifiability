# Final public release content-freeze verification

**Date:** 2026-08-30  
**Release:** `v1.0.0`  
**Reserved Zenodo DOI:** `10.5281/zenodo.22180107`  
**Status:** `PASS_FINAL_CONTENT_TREE_MANIFEST_VERIFIED_FOR_PROMOTION`

## Frozen content boundary

The final fresh-clone freeze run bound the complete Git-tracked public content tree at commit:

`535eb0e7efc6e983b042d63fa420859a3391e618`

The freeze report records a clean clone, `92` tracked regular files totaling `489,666` bytes, zero forbidden tracked paths, successful citation/DOI and Zenodo-draft metadata checks, and a `14`-file non-Git release payload totaling `3,535,908,885` bytes with the public non-Git SHA manifests cross-checked successfully.

The generated tree manifest is:

`manifests/TSPG_PUBLIC_RELEASE_TREE_SHA256_v1_0_20260830.txt`

with SHA-256:

`d39ed8cf39c419a7e26ac676a091a8457705de6a833f72fa6a1908a3a34d53fe`

and exactly `92` entries.

## Promotion-side independent verification

Before promotion, the supplied manifest and freeze report were independently inspected outside the fresh-clone workspace.

The following checks passed:

- the uploaded tree-manifest byte stream rehashes to exactly `d39ed8cf39c419a7e26ac676a091a8457705de6a833f72fa6a1908a3a34d53fe`;
- the uploaded freeze-report byte stream rehashes to `af1610edaa60559c468d19ad94b88e288059c67b053fb23e86de0d98d22b4ca8`;
- the report's embedded tree-manifest SHA exactly matches the independently rehashed manifest;
- the manifest contains exactly `92` syntactically valid `SHA-256  path` records;
- all manifest paths are unique and lexicographically sorted;
- the report records the same `92`-file count and frozen content commit;
- all release-boundary booleans are PASS and the forbidden tracked-path count is `0`;
- the report records `14` non-Git assets totaling `3,535,908,885` bytes and a successful non-Git SHA-manifest cross-check;
- immediately before promotion, the public `main` ref was re-read and still pointed to `535eb0e7efc6e983b042d63fa420859a3391e618`;
- selected critical manifest entries match their previously locked identities, including `CITATION.cff`, `code/model/full_scale_experiment.py`, `manifests/TSPG_RELEASE_ASSET_PLAN_v1_0_20260829.json`, and `manifests/TSPG_RELEASE_STATUS_v1_0_20260830.json`.

## Release-manifest envelope rule

The tree manifest intentionally does not hash itself. It binds every Git-tracked regular file in the frozen **content commit** above. This verification record, the machine-readable freeze report, the tree manifest itself, and the narrowly scoped release-state/index updates are promoted together in a successor **release-manifest commit**.

The `v1.0.0` tag must point to that successor release-manifest commit. The manifest's `content_commit` field remains the authoritative hash boundary for the pre-envelope public content tree, while the release-manifest commit is the archival envelope that carries the manifest and verification records.

No ordinary scientific, numerical, configuration, model-source, result, or manuscript-content file is changed by this promotion.

## Decision

`PASS_FINAL_CONTENT_TREE_MANIFEST_VERIFIED_FOR_PROMOTION`

The Git freeze / public release SHA-256 manifest gate is closed. The remaining coordinated-release gates are GitHub `v1.0.0` release creation plus six verified convenience assets, Zenodo publication, and post-publication asset verification.
