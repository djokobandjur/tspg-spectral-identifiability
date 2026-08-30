# TSPG clean-execution dependency-lock verification v1.0

**Date:** 2026-08-30  
**Status:** `PASS_DEPENDENCY_LOCK`  
**Execution source:** the same fresh FMLE environment that completed `PASS_END_TO_END_M1_M5`

## Scope

This audit closes the exact non-PyTorch dependency-lock gate after the successful sequential clean-environment M1--M5 reproduction test. The capture was made from the clean workspace pinned to public execution commit `53c7ff9dc8afcc7ff782a6d2f340d8e183acbcf4`.

The capture package contained exactly four small text artifacts: a direct dependency lock, a complete sanitized installed-distribution inventory, NumPy/SciPy backend configuration, and a SHA-256 manifest over the first three files.

## Byte verification

The uploaded dependency-capture package was independently inspected. The checksum manifest reproduced all three referenced SHA-256 values exactly:

| artifact | bytes | SHA-256 | status |
|---|---:|---|---|
| `TSPG_CLEAN_EXECUTION_DIRECT_DEPENDENCY_LOCK_v1_0_20260830.json` | 2575 | `bdfaaf55743a5b6b7d956533fe6dada3f8db92642e485f8210efae34fa4c5c40` | PASS |
| `TSPG_CLEAN_EXECUTION_INSTALLED_DISTRIBUTIONS_v1_0_20260830.json` | 8652 | `06f6fbc7c3ec140f82c3ba8a7d5f784cecf71619806f60d68622f556d4b4fe32` | PASS |
| `TSPG_CLEAN_EXECUTION_NUMERIC_BACKEND_CONFIG_v1_0_20260830.txt` | 3388 | `cbaec3bc69e6624effcf066be88c8b001a3892ba581793ffdb4a999c27d17867` | PASS |

The checksum-manifest file itself is 387 bytes with SHA-256 `4adb114fa62b7c25ba45277e32f560edd5ca7c465a98a47435dbe63ccba5dc97`.

The three promoted `environment/` files were then checked at Git-blob level against the captured source bytes. Expected and promoted blob identities match exactly:

- direct lock: `6b6b0a91c1510ddd6a96b20ae24f3c0199ce421b`;
- installed-distribution inventory: `725610c960ea268d79b2a9ea01a638f5505b28ea`;
- numerical backend configuration: `94558aa1a2e21e9ef60bca560a9aca2193bcb288`.

Therefore the public files are byte-identical to the verified clean-execution capture.

## Direct import lock

The capture statically scanned 18 public Python files under `code/**/*.py` plus `tools/prepare_runtime_root.py`. The external import roots resolved to:

`matplotlib`, `numpy`, `scipy`, `sklearn`, `torch`, `torchvision`, and `tqdm`.

The exact direct installed-distribution versions are:

- matplotlib `3.10.3`;
- NumPy `1.26.4`;
- scikit-learn `1.6.1`;
- SciPy `1.15.3`;
- torchvision `0.22.0a0+95f10a4e`;
- tqdm `4.67.1`.

PyTorch is recorded separately as a reference identity rather than converted into a generic PyPI requirement because the successful environment uses the custom NVIDIA build `2.8.0a0+5228986c39.nv25.06`, CUDA `12.9`, and cuDNN `91002`.

The installed-distribution metadata spells the same PyTorch local version as `2.8.0a0+5228986c39.nv25.6`. This is the PEP-440-normalized representation of the runtime `torch.__version__` string ending in `.nv25.06`; the two version objects are equivalent. This is not a dependency mismatch.

## Full environment inventory

The sanitized reference inventory records `302` installed Python distributions by name and version, with no install paths. It is retained as a provenance snapshot of the environment that actually passed M1--M5, not as a claim that all 302 packages are minimal requirements.

For example, Pillow `11.2.1` appears in the complete inventory but is not a direct import root of the scanned public TSPG source. This distinction is intentional: the direct lock records source-level imports; the full inventory records the successful environment including transitive dependencies.

## Numerical backend capture

The backend record binds additional compiled numerical-library context:

- NumPy `1.26.4`: `openblas64`, reported OpenBLAS `0.3.23.dev`, 64-bit integers, OpenMP, Haswell dynamic architecture;
- SciPy `1.15.3`: `scipy-openblas` `0.3.28`, Haswell dynamic architecture;
- compiler/build metadata and visible SIMD capabilities are retained from `numpy.__config__.show()` / `scipy.__config__.show()`.

These build/configuration paths are generic container/build-system paths and contain no user, host, repository, or dataset locations.

## UID/passwd note

The bare interactive container shell reports that its current numeric UID has no `/etc/passwd` entry. The capture records only the sanitized status token `CURRENT_UID_NOT_PRESENT_IN_PASSWD`; the numeric UID itself is not published.

A direct `torchvision` import from that bare shell can therefore hit a `getpwuid()` identity-resolution error. The installed torchvision version was captured without importing the module, through `importlib.metadata`. This is not evidence of a failed scientific environment: the M1--M5 runners executed successfully under their derived runtime environment contract and completed the end-to-end clean reproduction gate before this dependency capture.

## Privacy / release-policy check

The promoted capture contains no user/login name, no home or repository path, no container identifier, and no numeric UID. The backend text contains only generic software-build/install paths such as `/usr/local/...` and `/opt/...`; no TSPG host-local dataset/checkpoint paths are present.

## Gate decision

**Dependency-lock decision:** `PASS_EXACT_NON_PYTORCH_DEPENDENCY_LOCK_CAPTURED_AND_PROMOTED`.

The clean-execution environment gate is now fully closed:

- portable materialization: `PASS`;
- sequential M1--M5 scientific/numerical reproduction: `PASS`;
- generated-artifact byte reproduction: `PASS`;
- exact direct dependency/version capture: `PASS`;
- complete installed-distribution snapshot: `PASS`;
- numerical backend capture: `PASS`.

The next release gate is to freeze the public Git tree and generate the final release-level SHA-256 manifest before tagging and archival upload.
