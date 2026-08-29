# Reproduction guide

## Status

This is a **pre-release** reproduction guide. The public evidence/code/config promotion is substantially complete, but the first immutable release must not be tagged until the remaining items in `RELEASE_CHECKLIST.md` are closed. In particular, a clean-environment end-to-end verification is still pending.

## 1. Reference environment

The authoritative captured numerical environment is recorded in:

- `../environment/TSPG_PUBLIC_NUMERICAL_ENVIRONMENT_v1_0_20260829.json`

Reference values are Python 3.12.3, PyTorch `2.8.0a0+5228986c39.nv25.06`, CUDA 12.9, cuDNN 9.10.2, and one NVIDIA H200. The manifest also records the relevant PyTorch numerical-backend settings.

The original SHA-locked runtime records additionally contain host/login/absolute-path information. Those fields are intentionally omitted from the public environment manifest because they are not scientific requirements.

The exact versions of non-PyTorch Python dependencies have **not yet been frozen as a clean-environment lock file**. Do not interpret the current repository as claiming bitwise reproduction on an arbitrary compatible stack; the clean-environment test will produce the final portable dependency lock before release tagging.

## 2. ImageNet-100 data

ImageNet source images are not redistributed by this repository. A reproducer must obtain ImageNet under the applicable ImageNet terms and construct the same ImageNet-100 validation set used by the study.

The exact sample identities used by M1--M5 are published in:

- `../manifests/TSPG_USED_ANALYSIS_SPLIT_INDICES_PUBLIC_v1_0_20260829.json`

The public file is semantically tied to the locked canonical source manifest by SHA-256 and preserves the original sample ordering and the contiguous `A_G_1`, `A_G_2`, and `A_P` partition rule. No second RNG split is introduced.

## 3. Learned seed-42 checkpoint

All reported M1--M5 analyses use one checkpoint only: ViT-B/16, Learned positional encoding, seed 42.

Authoritative identity:

- original filename: `best_model.pth`
- planned GitHub Release asset: `TSPG_LEARNED_SEED42_best_model.pth`
- size: `343559209` bytes
- SHA-256: `7fcca75916c2d6f0f64aa5c381812ad3a305ba1a04672e9288f4251ab683c536`

The checkpoint is **not** committed to ordinary Git history because it exceeds GitHub's normal Git-object size limit. It will be attached directly to the first versioned GitHub Release. No Google Drive/shared-folder checkpoint dependency is part of the public design.

After downloading the release asset, verify it before any run, for example on Linux:

```bash
sha256sum TSPG_LEARNED_SEED42_best_model.pth
```

The value must match the SHA-256 above exactly.

## 4. Portable runtime staging

Files under `../configs/` are retained as exact historical analysis configurations. Several therefore contain execution-time absolute paths and cache/user fields. **Do not edit those committed files in place.** They are provenance artifacts.

The public helper `../tools/prepare_runtime_root.py` creates derived runtime copies and a flat staging root while preserving the locked configs unchanged. It changes only host-local routing/cache fields plus the filename/SHA of compatibility manifests whose bytes necessarily change when local paths are substituted.

The complete external-input contract is machine-readable in:

- `../manifests/TSPG_PORTABLE_RUNTIME_DEPENDENCIES_v1_0_20260829.json`.

Before downloading large artifacts, the helper can be run in plan mode:

```bash
python tools/prepare_runtime_root.py \
  --repo-root . \
  --output-root ./tspg_runtime \
  --plan-only
```

Plan mode validates the public split binding and M1--M5 config/runner interfaces, emits derived runtime-config copies, and reports every still-missing SHA-locked external input. It deliberately does **not** claim to verify the checkpoint, model source, or ImageNet directory.

Materialization mode is fail-closed:

```bash
python tools/prepare_runtime_root.py \
  --repo-root . \
  --output-root ./tspg_runtime \
  --model-source /path/to/full_scale_experiment.py \
  --checkpoint /path/to/TSPG_LEARNED_SEED42_best_model.pth \
  --imagenet-val /path/to/imagenet100/val \
  --artifact-dir /path/to/extracted_tspg_archival_assets
```

It verifies the exact model-source SHA, checkpoint size/SHA, the `100`-class / `5000`-image ImageFolder contract, and every staged external artifact SHA before declaring the runtime root complete. External artifacts are symlinked by default; use `--stage-mode copy` for a self-contained staging directory.

The helper writes `TSPG_PORTABLE_RUNTIME_PREPARATION_REPORT_v1.json`, recording:

- locked-config and runner SHA-256 identities;
- every derived runtime-config SHA-256;
- every host-local field changed, including old and new values;
- public-split and compatibility checkpoint-manifest identities;
- staged and missing external artifacts.

Scientific parameters, split sample identities, ranks, gates, tolerances, dtype choices, metric definitions, and locked result values are not changed by the helper.

The M1--M5 runners expose `--config`, `--root`, and `--output-dir` interfaces. H1-0016 and H1-0019 additionally separate the prespecified `gate`/`fit_gate` stages from their full stages. End-to-end execution of this portable path is still required before release tagging.

## 5. Exact model source

The checkpoint manifest binds the model implementation to SHA-256:

`83fc337128dec7f896c9816842806789a634154dea8372bb0a43bae19188d3bf`

An exact retained copy has been recovered and SHA-verified during release preparation. Its exact-byte promotion into the public reproduction surface is still a release blocker; no reconstructed or approximate substitute should be treated as authoritative.

## 6. Large/derived artifacts

See `ARTIFACT_ACQUISITION.md`, `../manifests/LARGE_ARTIFACTS_SHA256.csv`, and `../manifests/TSPG_PORTABLE_RUNTIME_DEPENDENCIES_v1_0_20260829.json`.

Large raw gradients and geometry arrays are never identified by filename alone: the SHA-256 value is the identity. Some late-stage artifacts can be regenerated from earlier locked inputs with the promoted M1--M5 code; earlier expensive dependencies will be supplied in the archival package when reconstruction would otherwise require re-running the pre-M1 development chain.

## 7. Verification principle

A reproduction is accepted only after verifying the relevant identities in:

- `../manifests/CODE_SHA256.txt`;
- `../manifests/RUN_RESULTS_SHA256.txt`;
- `../manifests/EVIDENCE_ARCHIVES_SHA256.txt`;
- `../manifests/LARGE_ARTIFACTS_SHA256.csv`;
- `../manifests/TSPG_PORTABLE_RUNTIME_DEPENDENCIES_v1_0_20260829.json`;
- `../manifests/TSPG_LEARNED_SEED42_CHECKPOINT_MANIFEST_v1_0_20260829.json`.

The final tagged release will add a release-level SHA-256 manifest over the frozen public tree and archival assets.
