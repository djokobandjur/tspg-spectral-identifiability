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

These values describe the authoritative reference execution environment; they are not a claim that every compatible GPU/software stack is numerically identical. The first immutable release remains blocked until a clean-environment reproduction check is executed and documented.

Host-local absolute paths embedded in the locked historical configs are provenance fields, not portable installation requirements. Public reproduction instructions map those fields to user-selected dataset, checkpoint, artifact, and cache locations.
