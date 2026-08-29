# TSPG portable runtime helper — static/plan QA

**Date:** 2026-08-29  
**Artifact:** `tools/prepare_runtime_root.py`  
**QA scope:** portable staging/config-overlay logic only  
**Status:** `PASS_STATIC_PLAN_ONLY`  
**Scientific execution performed:** `NO`  
**Clean-environment end-to-end reproduction performed:** `NO`

## Purpose

The promoted H1-0015--H1-0019 configs are exact historical provenance artifacts and contain host-local absolute paths. The portable helper must therefore create derived runtime configs without editing the locked public configs and without changing scientific parameters.

## Checks performed

1. Python syntax compilation (`python -m py_compile`) passed.
2. A plan-mode interface fixture was constructed from the exact final H1-0015--H1-0019 runner/config files retained in the locked starter packages, together with a split object exposing the same public `indices` interface and locked-source binding expected by the helper.
3. `--plan-only` completed successfully for all five targets: `M1`, `M2`, `M3`, `M4`, and `M5`.
4. Five derived runtime configs were emitted.
5. The helper detected eleven distinct SHA-locked external dependencies required across the complete M1--M5 runtime chain:
   - H1-0007 AG1 gradient metadata;
   - H1-0007 AG1 raw gradients;
   - H1-0010 exact task-span geometry;
   - H1-0010 result contract;
   - H1-0011 complement Krylov basis;
   - H1-0016 gate result;
   - H1-0016 cross-fold derived binary;
   - H1-0016 AG2 raw gradients;
   - H1-0016 result contract;
   - H1-0018 dual Gram/resample binary;
   - H1-0018 result contract.
6. Host-local edits were confined to the intended routing layer: model-source path, validation-data path, compatibility split/checkpoint-manifest filename/SHA fields where applicable, cache/user environment fields where present, and known artifact paths when a SHA-verified artifact is staged.
7. M3 correctly required no model/data path overlay because the H1-0017 analysis is an offline reduced-artifact computation; its source paths are changed only when the corresponding SHA-verified artifacts are staged.

## Fail-closed materialization behavior

Materialization mode is designed to reject:

- a model source whose SHA-256 differs from `83fc337128dec7f896c9816842806789a634154dea8372bb0a43bae19188d3bf`;
- a checkpoint whose size/SHA differs from `343559209` bytes / `7fcca75916c2d6f0f64aa5c381812ad3a305ba1a04672e9288f4251ab683c536`;
- an ImageNet-100 validation ImageFolder that does not expose 100 class directories and 5000 recognized image files;
- any external artifact whose SHA-256 differs from `manifests/TSPG_PORTABLE_RUNTIME_DEPENDENCIES_v1_0_20260829.json`.

These fail-closed branches have not yet been exercised against the complete release asset set because the archival assets and release checkpoint have not yet been assembled in one clean environment.

## Decision

The helper passes the static/plan QA required to keep developing the release surface. This audit **does not close** the clean-environment reproduction gate. Before tagging the first immutable release, the exact model source, checkpoint, ImageNet-100 validation tree, and archival dependencies must be supplied to materialization mode and the resulting M1--M5 execution path must be tested and recorded separately.
