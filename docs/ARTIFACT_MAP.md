# Manuscript-to-artifact map

This file is the public bidirectional map between the main evidence families and reproducibility artifacts promoted to GitHub/archival release.

The v1.0.0 M1--M5 boundary remains immutable. v1.1.0 adds H1-0012, the pre-existing H1-0007 ALiBi control, and A52 without changing the original M1--M5 scientific results.

| Evidence component | Public numerical evidence | Public code / lock | Public audit / QA | Authoritative non-Git evidence |
|---|---|---|---|---|
| **H1-0012 — exact direction-level decomposition** | `results/TSPG_H1_0012_RESULT_v1_0_20260828.json`; `results/TSPG_H1_0012_RESULT_POSTRUN_UPGRADE_v1_2_FROM_V1_1_20260828.json`; trajectory CSV | `configs/TSPG_H1_0012_CONFIG_v1_1_20260828.json` | `audits/TSPG_H1_0012_FORMAL_CLOSEOUT_REPORT_v1_0_20260828.md` | `TSPG_H1_0012_POSTRUN_UPGRADE_EVIDENCE_v1_1_20260828.zip`; `TSPG_H1_0012_CLOSEOUT_EVIDENCE_v1_0_20260828.zip` |
| **M1 — unrestricted quotient pathology / search-conditioned boundary** | `results/core_findings_v0_1.json` → `M1_search_conditioned_boundary`; exact H1-0015 result | existing H1-0015 code/config | H1-0015 formal closeout | v1.0.0 H1-0015 runtime evidence |
| **M2 — task-support restriction and cross-fold orientation** | `results/core_findings_v0_1.json` → `M2_crossfold_orientation`; H1-0016 gate/static QA | existing H1-0016 code/config | H1-0016 ingest/interpretation | v1.0.0 H1-0016 runtime evidence + Tier-B arrays |
| **M3 — denominator-selective B-normalized selection / R0** | exact `results/TSPG_H1_0017_RESULT_v1_1_20260829.json` | existing H1-0017 code/config | H1-0017 ingest + formal closeout | v1.0.0 H1-0017 runtime evidence |
| **M4 — finite-sample support/orientation audit** | corrected T/U/eta decomposition + H1-0018 static QA | existing H1-0018 code/config | H1-0018 ingest + formal closeout | v1.0.0 H1-0018 runtime evidence |
| **M5 — matched-sample third-fold consensus test** | H1-0019 fit gate/static QA/core findings | existing H1-0019 code/config | H1-0019 ingest + formal closeout | v1.0.0 H1-0019 runtime evidence |
| **H1-0007 — exact ALiBi structural control** | `results/TSPG_H1_0007_ALIBI_DENSE_CONTROL_RESULT_v1_1_20260828.json`; `results/TSPG_H1_0007_ALIBI_STRUCTURAL_REANALYSIS_v1_1_20260904.json` | `code/TSPG_h1_0007_alibi_structural_reanalysis_v1_1_20260904.py`; locked A29 amendment | `audits/TSPG_H1_0007_FORMAL_CLOSEOUT_REPORT_v1_0_20260828.md` | H1-0007 runtime/closeout ZIPs + exact raw 12x12 NPZ |
| **A52 — diagnostic-portability panel** | four exact arm JSONs; panel summary/primary rows; conditioning context | A52 runtime/aggregate code; run config; locked v1.5 protocol; expected invariants | `audits/TSPG_A52_RAW_PROVENANCE_VERIFICATION_v1_0_20260904.md`; A52 reconstruction/closeout records | A52 runtime evidence, final closeout patch, runtime-byte provenance addendum |

## A52 evidential boundary

`R0` is retrospective discovery-conditioned context. The fully prospective ImageNet contrasts are `PV-A` vs `PV-B2` (architecture at seed 123) and `PV-B1` vs `PV-B2` (seed within ViT-S). `PV-C` is a singleton multi-regime stress case. The public locked protocol fixes the full rank ladder `k={1,2,4,8,16,32}` and the primary portability ranks `k={4,8,16,32}` before arm execution.

## Large/non-Git artifacts

Large raw task-gradient arrays, derived matrices, checkpoints, and source ImageNet images are not duplicated in ordinary Git history. Exact identities are carried by public SHA manifests and versioned release/Zenodo assets. The v1.1.0 asset plan is `manifests/TSPG_RELEASE_ASSET_PLAN_v1_1_0_20260904.json`; A52 checkpoint identities are in `manifests/TSPG_A52_CHECKPOINT_MANIFEST_PUBLIC_v1_0_20260904.json`.


### A52 exact model sources

The checkpoint manifest is paired with `manifests/TSPG_A52_MODEL_SOURCE_MANIFEST_PUBLIC_v1_0_20260904.json`, which binds PV-A/PV-C to the exact ViT-B model source and PV-B1/PV-B2 to the exact ViT-S model source by SHA-256.
