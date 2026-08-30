# GitHub release verification and Zenodo publication record

**Audit date:** 2026-08-31  
**Release:** `v1.0.0`  
**GitHub release-manifest commit:** `2292cb17afb105572a9ac86de5ff33419033b073`  
**Zenodo version DOI:** `10.5281/zenodo.22180107`  
**Zenodo all-versions DOI:** `10.5281/zenodo.22180106`  
**Status:** `PASS_GITHUB_RELEASE_6_OF_6_EXACT_AND_ZENODO_PUBLICATION_CONFIRMED_REMOTE_ZENODO_SHA_PENDING`

## Scope

This audit records publication of the coordinated `v1.0.0` GitHub/Zenodo reproducibility release after the final public-tree freeze. It distinguishes three separate gates: GitHub release/tag publication, byte-level verification of the six GitHub convenience assets, and publication of the Zenodo archival record. Independent post-publication byte retrieval of all 14 Zenodo files remains a separate pending gate.

## GitHub release

The public GitHub release `v1.0.0` was published with target commit:

`2292cb17afb105572a9ac86de5ff33419033b073`

GitHub's public release API reported the six planned user-uploaded assets as `uploaded` and exposed their SHA-256 digests. After correction of the H1-0016 archive described below, all six matched the locked public identities exactly:

| Asset | Size (bytes) | SHA-256 | Result |
|---|---:|---|---|
| `TSPG_LEARNED_SEED42_best_model.pth` | 343559209 | `7fcca75916c2d6f0f64aa5c381812ad3a305ba1a04672e9288f4251ab683c536` | PASS |
| `TSPG_H1_0015_RUNTIME_EVIDENCE_v1_1_20260828.zip` | 24682 | `8125067b17eee2abe61bf9a3519366d371b2c751e7a481a87b3de0c32ce11c71` | PASS |
| `TSPG_H1_0016_RUNTIME_EVIDENCE_v1_2_20260829.zip` | 144501 | `0d7c6acfe8e38826fbb36322f30f187f9442d4ea42253e9463328d004062e022` | PASS |
| `TSPG_H1_0017_RUNTIME_EVIDENCE_v1_1_20260829.zip` | 2522591 | `5fff014e258c2bac92cc61f13ea559ba6cae67b41487d35141f4e00306ee1ae4` | PASS |
| `TSPG_H1_0018_RUNTIME_EVIDENCE_v1_0_20260829.zip` | 2936547 | `2ab57eeb8c27f229f37ceec1233033cf6c3061dce8943d526cf597f2ede7e567` | PASS |
| `TSPG_H1_0019_RUNTIME_EVIDENCE_v1_0_20260829.zip` | 4072637 | `f9eaadb43d0054a7d90714f2305b3e34fe3d47eaa34513659e4aed5ab09e62da` | PASS |

The two additional `Source code (zip)` / `Source code (tar.gz)` entries displayed by GitHub are automatically generated tag archives and are not part of the six planned convenience assets.

## H1-0016 release-asset correction

The first H1-0016 ZIP selected from the removable-storage release folder had the correct filename but the wrong byte identity: `169389` bytes with SHA-256 `4622a6dcc17f212b95959744b248c47b0e49ea4c28cddc49959397785f7931e4`. This discrepancy was detected from the public GitHub release digest before Zenodo publication.

The authoritative H1-0016 archive was then independently identified and checked as `144501` bytes with SHA-256 `0d7c6acfe8e38826fbb36322f30f187f9442d4ea42253e9463328d004062e022`; its ZIP integrity check passed. The incorrect GitHub release asset was deleted and replaced. The public GitHub API subsequently reported the exact locked size and SHA-256 above.

The still-unpublished Zenodo draft was corrected in the same way before publication. The corrected H1-0016 entry displayed `144.50 KB`, 100% completion, and MD5 `324b13e35f384c851657b4e583668d92`, matching the independently checked authoritative archive. Therefore the incorrect H1-0016 byte object was not intentionally carried into the published Zenodo version.

## Zenodo publication

The saved Zenodo draft was published after the H1-0016 correction. The public record page showed:

- title `TSPG Spectral Identifiability: Reproducibility Package`;
- resource type `Software`;
- publication date August 30, 2026;
- version `1.0.0`;
- version DOI `10.5281/zenodo.22180107`;
- all-versions DOI `10.5281/zenodo.22180106`;
- public/open status.

The version-specific DOI remains the release-pinning DOI used by `CITATION.cff`. The all-versions DOI is Zenodo's concept DOI for resolving to the latest version and does not replace the version DOI in the exact `v1.0.0` provenance boundary.

## Remaining verification gate

The GitHub release asset gate is closed at `6/6 exact size + SHA-256 PASS`. Zenodo publication is confirmed. Independent post-publication retrieval and checksum verification of the complete 14-file Zenodo payload remains pending; the authoritative expected SHA-256 values remain those in the public release manifests and pre-upload staging audits.
