# Reproduction guide

## Status

GitHub/Zenodo release `v1.0.0` is public and independently verified. This branch prepares `v1.1.0`, which adds already-closed H1-0012, H1-0007 ALiBi, and A52 evidence. No new scientific computation is authorized or required by this release update.

The v1.0.0 version DOI is `10.5281/zenodo.22180107`; all versions are grouped under `10.5281/zenodo.22180106`.

## 1. Reference environment

The v1.0.0 M1--M5 environment remains authoritative for the original chain. See `../environment/` and the clean-execution dependency-capture/audit records. Exact historical configs are provenance artifacts and must not be edited in place.

## 2. Data boundary

Source ImageNet images are not redistributed. Reproduction of image-dependent stages requires a legally obtained ImageNet copy plus the published sample/split manifests. CIFAR-100 acquisition follows its standard public distribution; A52 split provenance is carried in the A52 evidence/closeout archives.

## 3. M1--M5

The existing `v1.0.0` workflow remains unchanged. Use `tools/prepare_runtime_root.py` with the existing public model source, seed-42 checkpoint, split manifest, compact evidence archives, and SHA-locked Tier-B numerical artifacts. The clean-environment end-to-end audit documents successful sequential reproduction of M1--M5.

## 4. H1-0012 motivating decomposition

The reporting-level endpoint is fully contained in the public compact result layer:

- `../results/TSPG_H1_0012_RESULT_v1_0_20260828.json`;
- `../results/TSPG_H1_0012_RESULT_POSTRUN_UPGRADE_v1_2_FROM_V1_1_20260828.json`;
- `../results/TSPG_H1_0012_TOP1_JOINT_TRAJECTORY_POSTRUN_UPGRADE_v1_2_FROM_V1_1_20260828.csv`.

The authoritative source and formal closeout are versioned as release/Zenodo assets. The reporting upgrade is zero-compute and preserves the original scientific result.

## 5. H1-0007 ALiBi structural control

Download/verify `TSPG_H1_0007_ALIBI_SEED42_DENSE_GA_GT_AND_TOP4_v1_1.npz` against SHA-256

`dd8e670f222824fd78eb833bc4cd23f31ac5119ba3ed5eb6921b318c6149329d`.

Then run:

```bash
python code/TSPG_h1_0007_alibi_structural_reanalysis_v1_1_20260904.py \
  /path/to/TSPG_H1_0007_ALIBI_SEED42_DENSE_GA_GT_AND_TOP4_v1_1.npz \
  --output-json /tmp/TSPG_H1_0007_ALIBI_STRUCTURAL_REANALYSIS_reproduced.json
```

The script is deterministic CPU algebra: no model load, GPU, dataset, new gradient, or new scientific experiment is involved. It reproduces the public `R_B`, selector-overlap, spectrum/conditioning, and Ky Fan bound readouts from the archived 12x12 matrices.

## 6. A52 reporting/reduced reproduction

The public branch includes:

- locked protocol `../manifests/TSPG_PROTOCOL_AMENDMENT_A52_DIAGNOSTIC_PORTABILITY_PANEL_PUBLIC_SCIENTIFIC_v1_0_20260904.md`;
- exact run config `../configs/TSPG_A52_RUN_CONFIG_v1_0_20260903.json`;
- runtime code under `../code/TSPG_A52_*`;
- four exact arm result JSONs and panel summaries under `../results/`;
- byte/provenance verification under `../audits/`.

The same locked protocol SHA-256 (`2fc2c8dbeca0ce0affe17055e7ba6e7a7ffd8c7b9ba7488c15bfcf7e32a89aeb`) is recorded in the runtime provenance of all four arms. The exact private lock text is not distributed; `TSPG_PROTOCOL_AMENDMENT_A52_DIAGNOSTIC_PORTABILITY_PANEL_PUBLIC_SCIENTIFIC_v1_0_20260904.md` is the public scientific semantic copy and preserves all scientific design fields. The protocol fixes reported ranks `k={1,2,4,8,16,32}` and primary portability ranks `k={4,8,16,32}` before outcome inspection.

The A52 runtime-byte provenance addendum contains the exact reduced matrices and executed runtime source needed for reporting-level/reduced verification.

## 7. A52 full model re-execution

Full model-level re-execution additionally requires the four exact checkpoints in `../manifests/TSPG_A52_CHECKPOINT_MANIFEST_PUBLIC_v1_0_20260904.json`:

- PV-A: ViT-B/16 ImageNet-100 Learned seed 123;
- PV-B1: ViT-S/16 ImageNet-100 Learned seed 42;
- PV-B2: ViT-S/16 ImageNet-100 Learned seed 123;
- PV-C: ViT-B CIFAR configuration Learned seed 42.

The SHA-256 checkpoint identities are authoritative. Until the v1.1.0 binary staging gate is closed, reporting/reduced reproduction is public while full model re-execution remains dependent on archival distribution of these exact checkpoint bytes.

## 8. Verification principle

Never identify a scientific binary by filename alone. Verify the relevant SHA-256 identities before use. For v1.1.0 additions consult:

- `../manifests/TSPG_RELEASE_ADDITIONS_SHA256_v1_1_0_20260904.txt`;
- `../manifests/TSPG_RELEASE_ASSET_PLAN_v1_1_0_20260904.json`;
- `../manifests/TSPG_A52_CHECKPOINT_MANIFEST_PUBLIC_v1_0_20260904.json`.

A final v1.1.0 tree manifest and post-publication remote verification record will be generated only after the Git tree, release assets, and Zenodo version are frozen.


## A52 model-source identity

For full model-level re-execution, verify both the checkpoint SHA and the corresponding model-source SHA from `manifests/TSPG_A52_MODEL_SOURCE_MANIFEST_PUBLIC_v1_0_20260904.json` before loading the checkpoint. Reporting/reduced-matrix checks do not require model loading.
