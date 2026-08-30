# TSPG Spectral Identifiability

Reproducibility repository supporting the study:

**Diagnosing Spectral Identifiability Failures in Task-Sensitive Parameter Geometry: A Vision Transformer Case Study**

## Scope

This repository contains the code, configurations, manifests, derived results, diagnostics, and provenance records needed to reproduce the analyses reported in the study.

**The manuscript itself is intentionally not published in this repository.** No manuscript PDF, LaTeX source, submission package, cover letter, reviewer material, or internal manuscript-development file is part of the public reproducibility release.

The study examines finite-sample spectral identifiability of task-sensitive parameter geometry in one exhaustively instrumented Vision Transformer case. The public package is organized around the locked diagnostic sequence rather than the internal development history.

## Repository status

**Release candidate `v1.0.0` is in final archival preparation.** The exact checkpoint model source, M1--M5 analysis code/config/result/audit layer, portable-runtime materialization, sequential clean-environment M1--M5 reproduction, and exact dependency capture have all passed their public verification gates. The complete 14-file non-Git payload has been SHA-verified before upload and is present in the saved Zenodo draft at 100% completion for all files.

Zenodo DOI `10.5281/zenodo.22180107` is reserved for this release but is not registered/public until the draft is published. Remaining gates are the final frozen-tree SHA-256 manifest, the versioned GitHub Release with its six convenience assets, Zenodo publication, and post-publication asset verification.

Track the remaining blockers in `docs/RELEASE_CHECKLIST.md`; the current machine-readable release state is `manifests/TSPG_RELEASE_STATUS_v1_0_20260830.json`.

## Structure

- `code/` — analysis and operator implementations
- `configs/` — locked analysis configurations
- `manifests/` — split, checkpoint, and provenance manifests
- `results/` — compact machine-readable result artifacts
- `audits/` — reproducibility and numerical-certification reports
- `environment/` — sanitized reference software/numerical environment
- `docs/` — reproduction, acquisition, release, and artifact mapping documentation

## Reproduction

Start with:

- `docs/REPRODUCTION.md` — pre-release reproduction workflow and portable-path rules;
- `docs/ARTIFACT_ACQUISITION.md` — checkpoint and large numerical artifact acquisition/reconstruction policy;
- `docs/ARTIFACT_MAP.md` — bidirectional M1--M5 evidence map;
- `environment/TSPG_PUBLIC_NUMERICAL_ENVIRONMENT_v1_0_20260829.json` — reference numerical environment;
- `manifests/CODE_SHA256.txt`, `RUN_RESULTS_SHA256.txt`, `EVIDENCE_ARCHIVES_SHA256.txt`, and `LARGE_ARTIFACTS_SHA256.csv` — integrity identities.

The committed configs are exact historical provenance artifacts. Host-local absolute paths in those files are not portable requirements and must not be edited in place; the release workflow uses a runtime path-only overlay while preserving all scientific parameters.

## Data and checkpoint

Source ImageNet images are not redistributed. The public split/index manifest reconstructs the analyzed ImageNet-100 subsets from a legally obtained ImageNet copy.

All reported M1--M5 analyses use one instrumented checkpoint: ViT-B/16, Learned positional encoding, seed 42. Its authoritative identity is recorded in `manifests/TSPG_LEARNED_SEED42_CHECKPOINT_MANIFEST_v1_0_20260829.json`:

- original filename: `best_model.pth`
- planned GitHub Release asset: `TSPG_LEARNED_SEED42_best_model.pth`
- size: 343,559,209 bytes
- SHA-256: `7fcca75916c2d6f0f64aa5c381812ad3a305ba1a04672e9288f4251ab683c536`

Because the checkpoint exceeds ordinary GitHub Git-history file limits, it is not committed to the repository tree. The SHA-verified checkpoint is already present in the saved Zenodo draft and will also be attached directly to the versioned **GitHub Release**, eliminating any dependency on a separate Google Drive/shared-folder download.

## License

The repository is released under the **MIT License**; see `LICENSE`. Third-party datasets and other external materials remain subject to their original terms and are not relicensed by this repository.

## Authors

- **Đoko Banđur** — Faculty of Technical Sciences, University of Pristina, Kosovska Mitrovica — ORCID: 0000-0001-9034-6854
- **Miloš Banđur** — Faculty of Technical Sciences, University of Pristina, Kosovska Mitrovica — ORCID: 0009-0007-0124-3943

Corresponding author: Đoko Banđur (`djoko.bandjur@pr.ac.rs`)

## Citation

Release version: `1.0.0`  
Reserved Zenodo DOI: `10.5281/zenodo.22180107`

The DOI identifies the reproducibility package, not a copy of the manuscript. It becomes the registered public archival DOI when the saved Zenodo record is published. See `CITATION.cff` for the versioned citation metadata.
