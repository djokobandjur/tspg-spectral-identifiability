# TSPG clean-environment portable materialization audit v1.0

**Date:** 2026-08-29  
**Scope:** public M1--M5 portable runtime preparation from a fresh FMLE GPU session  
**Status:** `PASS_MATERIALIZATION`

## Test boundary

A fresh FMLE GPU session was used to clone the public repository, detach at the release-preparation commit, extract the five SHA-locked compact runtime-evidence archives, and run `tools/prepare_runtime_root.py` in materialization mode using the staged release payload plus the local ImageNet-100 validation tree.

The test intentionally separates **portable materialization** from **scientific end-to-end execution**. This audit closes only the former. M1--M5 execution and numerical comparison with the locked results remain pending.

## Environment observed

The clean session reported:

- GPU: NVIDIA H200
- Python: 3.12.3
- PyTorch: `2.8.0a0+5228986c39.nv25.06`
- CUDA reported by PyTorch: 12.9
- CUDA available: yes

Host/container identifiers, usernames, and absolute host-local paths are intentionally omitted from this public audit.

## Repository identity

The clean clone was detached at:

`53c7ff9dc8afcc7ff782a6d2f340d8e183acbcf4`

The observed `HEAD` exactly matched the requested commit.

## Evidence extraction

The five compact runtime-evidence archives H1-0015 through H1-0019 were extracted successfully before materialization:

- H1-0015 evidence ZIP: PASS
- H1-0016 evidence ZIP: PASS
- H1-0017 evidence ZIP: PASS
- H1-0018 evidence ZIP: PASS
- H1-0019 evidence ZIP: PASS

Result: `5/5 PASS`.

## Portable runtime preparation

`tools/prepare_runtime_root.py` was executed with:

- the exact public model source from `code/model/full_scale_experiment.py`;
- the verified Learned seed-42 release-staged checkpoint;
- the ImageNet-100 validation tree;
- the staged standalone archival numerical payload;
- the extracted compact runtime-evidence archives;
- `--stage-mode copy`.

The fail-closed preparation report returned:

- mode: `MATERIALIZED`
- targets: `M1, M2, M3, M4, M5`
- staged external artifacts: `11`
- missing external artifacts: `0`

The helper therefore reported:

`Portable runtime root prepared with all requested external inputs SHA-verified.`

## Gate decision

**Portable materialization gate: PASS.**

This establishes that a fresh environment can reconstruct the public M1--M5 runtime boundary from the public repository plus the planned non-Git release payload and the separately obtained ImageNet-100 source data, with all required external artifact identities resolved and SHA-verified.

This does **not** yet establish numerical reproduction of M1--M5. The next gate is sequential execution of the promoted M1--M5 runners from the materialized runtime, respecting the prespecified H1-0016 gate/full and H1-0019 fit-gate/full ordering, followed by numerical comparison with the locked public results.

No scientific result is changed by this audit.
