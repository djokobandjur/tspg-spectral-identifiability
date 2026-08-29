# Manuscript-to-artifact map

This file is the public bidirectional map between the manuscript-level M1--M5 findings and the reproducibility artifacts currently promoted to GitHub.

The compact numerical index is `results/core_findings_v0_1.json`. Authoritative runtime evidence is identified by SHA-256 in `manifests/EVIDENCE_ARCHIVES_SHA256.txt` and will be deposited in the versioned archival release.

| Manuscript component | Public evidence | Authoritative run evidence | Notes |
|---|---|---|---|
| M1 — unrestricted quotient pathology | `results/core_findings_v0_1.json` → `M1_search_conditioned_boundary` | `TSPG_H1_0015_RUNTIME_EVIDENCE_v1_1_20260828.zip` | Matched BASELINE/HEAD/TAIL/COMBINED support designs show the spectral boundary follows the targeted search support. |
| M2 — task-support restriction and cross-fold orientation | `results/core_findings_v0_1.json` → `M2_crossfold_orientation` | `TSPG_H1_0016_RUNTIME_EVIDENCE_v1_2_20260829.zip` | Strongly non-random support overlap coexists with inefficient transfer of the leading unilateral orientation. |
| M3 — denominator-selective normalized selection | `results/core_findings_v0_1.json` → `M3_denominator_selective_normalization` | `TSPG_H1_0017_RUNTIME_EVIDENCE_v1_1_20260829.zip` | 2×2 cross-scoring plus Euclidean-unit mean denominator response distinguishes task transfer from denominator preference. |
| M4 — finite-sample support/orientation audit | `results/core_findings_v0_1.json` → `M4_finite_sample_decoupling` | `TSPG_H1_0018_RUNTIME_EVIDENCE_v1_0_20260829.zip` | Train-size curves separate increasing support coverage from non-coherent low-dimensional orientation transfer. |
| M5 — matched-sample third-fold consensus test | `results/core_findings_v0_1.json` → `M5_matched_sample_consensus` | `TSPG_H1_0019_RUNTIME_EVIDENCE_v1_0_20260829.zip` | Actual U640 controls fit sample size; the final consensus effect is rank dependent and fails the prespecified curve-level success rule. |

## Next promotion step

The first archival release will add the exact public code/config/result files underlying these rows, plus large-artifact hashes and reconstruction/acquisition instructions. GitHub will remain the human-readable/code surface; the immutable GitHub release and Zenodo archive will share one release version.
