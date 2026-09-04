# TSPG Spectral Identifiability

Public reproducibility repository supporting the study:

**Auditing Identifiability in Normalized Spectral Sensitivity: Separating Task Alignment from Denominator-Driven Selection**

## Scope

This repository contains public code, locked configurations, compact results, diagnostics, manifests, numerical-certification records, and archival provenance for the reported TSPG analyses.

The public evidence boundary now has four layers:

1. the exact H1-0012 direction-level numerator/denominator decomposition used as the motivating example;
2. the closed M1--M5 Learned-PE diagnostic sequence;
3. the pre-existing H1-0007 exact 12-dimensional ALiBi structural control and its deterministic zero-compute reanalysis;
4. the prespecified A52 diagnostic-portability panel, including the retrospective R0 anchor and four new case-wise arms.

The manuscript itself is intentionally **not** published in this repository. No manuscript PDF/TEX, submission package, cover letter, non-scientific publication correspondence, or internal manuscript-development/governance file is part of the public reproducibility release.

## Release status

The original public package remains frozen as GitHub release `v1.0.0` and Zenodo version DOI `10.5281/zenodo.22180107` (all-versions DOI `10.5281/zenodo.22180106`).

Branch `release/v1.1.0-alibi-a52` prepares the next archival version. It extends, rather than rewrites, the v1.0.0 provenance boundary. The v1.1.0 version DOI is reserved as `10.5281/zenodo.22308245`; it will become registered/public when the Zenodo draft is published. The stable all-versions DOI remains `10.5281/zenodo.22180106`.

Current pre-publication blockers are limited to final Git-tree freeze/manifest/tagging, Zenodo v1.1.0 publication, post-publication remote byte verification, and persistent-link insertion. The public A52 compatibility overlay and the local 12-object Zenodo byte-staging gate are closed. No new scientific experiment is part of this release update.

## Structure

- `code/` — analysis/operator implementations, including A52 runtime code and the ALiBi zero-compute reanalysis;
- `configs/` — locked analysis configurations;
- `manifests/` — split/checkpoint/protocol/release and SHA-256 manifests;
- `results/` — compact machine-readable result artifacts;
- `audits/` — numerical-certification, formal-closeout, provenance, and release-integrity records;
- `environment/` — sanitized reference software/numerical environment;
- `docs/` — reproduction, acquisition, release, and artifact-mapping documentation.

## Reproduction entry points

Start with:

- `docs/REPRODUCTION.md` — public reproduction boundary and workflows;
- `docs/ARTIFACT_MAP.md` — bidirectional map from reported evidence families to public artifacts;
- `docs/TSPG_RELEASE_V1_1_0_PREPARATION_20260904.md` — v1.1.0 release-staging state;
- `manifests/TSPG_RELEASE_ASSET_PLAN_v1_1_0_20260904.json` — exact new non-Git evidence-asset identities;
- `manifests/TSPG_A52_CHECKPOINT_MANIFEST_PUBLIC_v1_0_20260904.json` — exact A52 checkpoint identities;
- `manifests/TSPG_PROTOCOL_AMENDMENT_A52_DIAGNOSTIC_PORTABILITY_PANEL_PUBLIC_SCIENTIFIC_v1_0_20260904.md` — SHA-locked A52 protocol that fixes reported and primary rank ladders before arm execution.

## Data and checkpoints

Source ImageNet images are not redistributed. The existing public split/index manifest reconstructs the analyzed ImageNet-100 subsets from a legally obtained ImageNet copy.

The v1.0.0 package distributes the Learned ViT-B/16 seed-42 checkpoint used by M1--M5. A52 uses four additional exact checkpoints. Their SHA-256 identities, architectures, seeds, positional dimensions, and model-source hashes are recorded in `manifests/TSPG_A52_CHECKPOINT_MANIFEST_PUBLIC_v1_0_20260904.json`.

Reporting-level and reduced-matrix A52 verification is supported by the compact evidence archives. Full model-level A52 re-execution additionally requires those four exact checkpoint binaries. Their source-to-staging byte identities are verified 4/4, and the exact ViT-B/ViT-S model-construction sources are hash-locked in the public tree; remaining work is archival publication and remote verification, not scientific rerunning.

## License

The repository is released under the **MIT License**; see `LICENSE`. Third-party datasets and external materials remain subject to their original terms and are not relicensed by this repository.

## Authors

- **Đoko Banđur** — Faculty of Technical Sciences, University of Pristina, Kosovska Mitrovica — ORCID: 0000-0001-9034-6854
- **Miloš Banđur** — Faculty of Technical Sciences, University of Pristina, Kosovska Mitrovica — ORCID: 0009-0007-0124-3943

Corresponding author: Đoko Banđur (`djoko.bandjur@pr.ac.rs`).

## Citation

Until v1.1.0 is published, the released v1.0.0 package remains identified by version DOI `10.5281/zenodo.22180107`, while the stable all-versions DOI `10.5281/zenodo.22180106` identifies the evolving reproducibility record. The reserved v1.1.0 version DOI is `10.5281/zenodo.22308245`; `CITATION.cff` records that exact release DOI and it becomes citable when v1.1.0 is published.
