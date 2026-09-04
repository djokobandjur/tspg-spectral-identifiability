# A52 checkpoint release-staging verification — v1.0

Date: 2026-09-04  
Release target: `v1.1.0`  
Scientific computation: **NONE**

## Gate

The four checkpoint binaries required for full model-level A52 re-execution were verified at their retained source locations, copied into a dedicated release-staging directory, and independently re-hashed after copying. The gate is **PASS 4/4**.

| Arm | Architecture / dataset | Size (bytes) | SHA-256 | Status |
|---|---|---:|---|---|
| PV-A | ViT-B/16 / ImageNet-100 | 343,559,209 | `fbb8d70f72fb6ee1bb93b1d00cca663ffb222f489d16d8149f2e01efd65c351e` | `PASS_STAGED_EXACT` |
| PV-B1 | ViT-S/16 / ImageNet-100 | 86,873,641 | `a518ec4ba5478539e85b8a3841e847cd014e7f1eddc7e48752bfe105b68ace26` | `PASS_STAGED_EXACT` |
| PV-B2 | ViT-S/16 / ImageNet-100 | 86,873,641 | `c04bd01615a897d713e5e0deb94afea0cdc0e0367d09a14846ab46b93bf82524` | `PASS_STAGED_EXACT` |
| PV-C | ViT-B/CIFAR config / CIFAR-100 | 340,938,857 | `a65418972b2f3c9c68b5031d79159fa5141cfccab3d12454947321500d545cdd` | `PASS_STAGED_EXACT` |

Aggregate staged checkpoint payload: **858,245,348 bytes**.

The source SHA-256, expected SHA-256, and staged-copy SHA-256 agree for every arm. Host-local paths are deliberately excluded from the public manifest. The private path-bearing staging manifest remains outside the public Git tree and is bound here by SHA-256 `c98c3a689a776b8e863d4c0827f2887d1f63402f7e3090055a8a3c4996325415`.

## Distribution decision

The four A52 checkpoint binaries are required for **full model-level re-execution**, but not for verification of the already archived reduced matrices, arm-result JSONs, panel summaries, or zero-compute reporting analyses. For v1.1.0 they are designated as **Zenodo archival payloads**. They are not required to be duplicated as GitHub Release assets; the GitHub release will expose their exact identities and point to the DOI-bearing archive.

## Closeout

Checkpoint binary staging gate: `PASS_STAGED_EXACT_4_OF_4`.

No model execution, gradient computation, dataset access, or scientific endpoint recomputation occurred in this gate.
