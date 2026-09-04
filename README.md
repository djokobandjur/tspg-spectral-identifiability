# TSPG Spectral Identifiability

Public reproducibility repository supporting the study:

**Auditing Identifiability in Normalized Spectral Sensitivity: Separating Task Alignment from Denominator-Driven Selection**

## Scope

This repository contains public code, locked configurations, compact results, diagnostics, manifests, numerical-certification records, and archival provenance for the reported TSPG analyses.

The public evidence boundary being prepared for the next release has four layers: the exact H1-0012 direction-level numerator/denominator decomposition; the closed M1--M5 Learned-PE diagnostic sequence; the pre-existing H1-0007 exact 12-dimensional ALiBi structural control and deterministic zero-compute reanalysis; and the prespecified A52 diagnostic-portability panel.

The manuscript itself is intentionally **not** published in this repository. No manuscript PDF/TEX, submission package, cover letter, editor/reviewer material, or internal manuscript-development/governance file is part of the public reproducibility release.

## Release status

GitHub/Zenodo release `v1.0.0` is public and independently verified. Its version DOI is `10.5281/zenodo.22180107`; the all-versions DOI is `10.5281/zenodo.22180106`.

Branch `release/v1.1.0-alibi-a52` prepares the next archival version. It extends, rather than rewrites, the v1.0.0 provenance boundary. No new scientific experiment is part of this release update. The v1.1.0 version DOI will be recorded only after a new Zenodo version is reserved/published and independently verified.

The four exact A52 checkpoint binaries required for full model-level re-execution have now passed source -> staging -> re-hash verification (`4/4 PASS`, aggregate `858,245,348` bytes). Their path-sanitized public manifest and exact SHA list are under `manifests/`; the binaries are designated for the Zenodo v1.1.0 archival payload rather than mandatory duplication as GitHub Release assets.

Current preparation state is documented in `docs/TSPG_RELEASE_V1_1_0_PREPARATION_20260904.md` and `docs/RELEASE_CHECKLIST.md`.

## Structure

- `code/` — analysis and operator implementations
- `configs/` — locked analysis configurations
- `manifests/` — split, checkpoint, protocol, release, and provenance manifests
- `results/` — compact machine-readable result artifacts
- `audits/` — numerical-certification, closeout, provenance, and release-integrity records
- `environment/` — sanitized reference software/numerical environment
- `docs/` — reproduction, acquisition, release, and artifact-mapping documentation

## Data and checkpoints

Source ImageNet images are not redistributed. The v1.0.0 package distributes the Learned ViT-B/16 seed-42 checkpoint used by M1--M5. Full model-level A52 reproduction additionally requires four exact SHA-locked checkpoints; their source and staged copies have now been independently verified and their Zenodo v1.1.0 archival staging gate is closed.

## License

The repository is released under the **MIT License**; see `LICENSE`. Third-party datasets and external materials remain subject to their original terms and are not relicensed by this repository.

## Authors

- **Đoko Banđur** — Faculty of Technical Sciences, University of Pristina, Kosovska Mitrovica — ORCID: 0000-0001-9034-6854
- **Miloš Banđur** — Faculty of Technical Sciences, University of Pristina, Kosovska Mitrovica — ORCID: 0009-0007-0124-3943

Corresponding author: Đoko Banđur (`djoko.bandjur@pr.ac.rs`).

## Citation

Until v1.1.0 is published, use version DOI `10.5281/zenodo.22180107` for the released v1.0.0 package or all-versions DOI `10.5281/zenodo.22180106` when referring to the evolving reproducibility record. `CITATION.cff` will be advanced only after the new version DOI exists.
