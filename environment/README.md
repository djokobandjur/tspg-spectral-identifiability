# Environment

This directory records the public execution-environment contract for the TSPG reproducibility package.

`TSPG_PUBLIC_NUMERICAL_ENVIRONMENT_v1_0_20260829.json` is a sanitized derivative of SHA-locked runtime evidence from the numerical preflight/conditioning path. It preserves the scientific and numerical backend settings while intentionally removing host/container identifiers, login names, UID values, HOME/working-directory paths, and host-specific cache paths.

The captured reference stack is:

- Linux `4.18.0-477.27.1.el8_8.x86_64` with glibc 2.39;
- Python 3.12.3 (GCC 13.3.0);
- PyTorch `2.8.0a0+5228986c39.nv25.06`;
- CUDA 12.9;
- cuDNN 9.10.2 (`91002`);
- one NVIDIA H200 (compute capability 9.0, 150,393,585,664 bytes visible memory);
- PyTorch default dtype `float32`, matmul precision `high`;
- cuDNN benchmark disabled, cuDNN deterministic mode disabled;
- TF32 matmul and cuDNN enabled;
- flash, memory-efficient, and math SDPA backends enabled at environment-capture time.

The fresh clean-environment reproduction test has now completed end-to-end. Portable materialization passed, M1--M5 reproduced all compared scientific/numerical fields exactly, and all checked generated numerical/runtime artifacts reproduced their authoritative SHA-256 identities.

The same successful clean environment was then captured at the Python-package and numerical-backend level:

- `TSPG_CLEAN_EXECUTION_DIRECT_DEPENDENCY_LOCK_v1_0_20260830.json` records the source-level external import set and exact installed distribution versions;
- `TSPG_CLEAN_EXECUTION_INSTALLED_DISTRIBUTIONS_v1_0_20260830.json` records the complete sanitized 302-distribution environment snapshot;
- `TSPG_CLEAN_EXECUTION_NUMERIC_BACKEND_CONFIG_v1_0_20260830.txt` records NumPy/SciPy BLAS/LAPACK/compiler/SIMD configuration;
- `../manifests/TSPG_CLEAN_EXECUTION_DEPENDENCY_CAPTURE_SHA256_v1_0_20260830.txt` binds those three captured files by SHA-256;
- `../audits/TSPG_CLEAN_EXECUTION_DEPENDENCY_LOCK_VERIFICATION_v1_0_20260830.md` records the independent checksum, privacy, and promotion verification.

The direct non-PyTorch distribution versions used by the public source are matplotlib `3.10.3`, NumPy `1.26.4`, scikit-learn `1.6.1`, SciPy `1.15.3`, torchvision `0.22.0a0+95f10a4e`, and tqdm `4.67.1`. PyTorch remains a separately recorded reference identity because the successful environment uses a custom NVIDIA build rather than a generic PyPI release.

The installed-distribution metadata normalizes the PyTorch local version suffix from runtime `...nv25.06` to `...nv25.6`; these are PEP-440-equivalent representations, not different builds.

These values describe the authoritative reference execution environment; they are not a claim that every compatible GPU/software stack is numerically identical. The remaining pre-release work begins with freezing the public Git tree and generating the final release-level SHA-256 manifest.

Host-local absolute paths embedded in the locked historical configs are provenance fields, not portable installation requirements. Public reproduction instructions map those fields to user-selected dataset, checkpoint, artifact, and cache locations.
