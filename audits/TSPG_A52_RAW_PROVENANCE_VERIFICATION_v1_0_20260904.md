# TSPG A52 RAW PROVENANCE VERIFICATION v1.0

**Date:** 2026-09-04  
**Status:** `PASS_RAW_BYTE_AND_NUMBER_PROVENANCE`  
**Scientific execution status:** `PORTABILITY_COMPLETE`  
**New scientific experiments authorized:** `NO`

## Archive and manifest verification

- Runtime evidence ZIP SHA-256: `d9fbab1fe06bbb8d3b34e5e3370cbcddf2481836006e3b3e5488c000a7a68d57`.
- Zero-compute final closeout patch ZIP SHA-256: `1b894a28b1599e703ae2b7def2338aa655b1c1b8fd0349bd72076a84d13493b0`.
- Runtime byte-provenance addendum ZIP SHA-256: `9f3621629781553f6027dc0cb802261edcd1a3ff9a92e8bfed671dfcff3d4d73`.
- Internal archive verification: **113/113 PASS; 0 failures**.
- Primary A52 signed-display table versus raw arm JSON: **maximum numeric absolute error = 0**.

## Arm-level byte binding

| Arm | Result JSON SHA-256 | Reduced matrices SHA-256 | Technical / calibration | Primary signed task range | Primary R_B range |
|---|---|---|---|---:|---:|
| PV-A | `431d69e23a797cb637e478ec2fe79a39d42fa60ef4e4050152e4a64659e643fb` | `c6114406d19c79321dd81f3772b430bed019f3118d37dbc0e9d1d69a7efbc51c` | PASS / CALIBRATION_PASS | -81.152% to -69.641% | 0.008804--0.023976 |
| PV-B1 | `136730bdffdc0cfa2158d1538157eb05c383d1b46f8f508f3bbd3dc08bc3eafc` | `a97276763ffcee8b623a0a75487fd2f6b5aec5b847a99916ea9cdb99c8ae52e8` | PASS / CALIBRATION_PASS | +6.600% to +15.071% | 0.140591--0.217501 |
| PV-B2 | `20c61f11778d1ddf59774fd8459462cedf2c012c475dd4f25feb36d59f0015be` | `0474c9d00bcec42dfeea8aed8a96d846d65cf6d13b99e4d873a93df007f9b061` | PASS / CALIBRATION_PASS | +3.711% to +15.687% | 0.231541--0.352584 |
| PV-C | `304cef69320bd742670957f49ca5128d5414d2d2b61ec1f4edc954e52d8ddaa3` | `4012df1b6d18cb54f7c528d8ba106a4e2e9a834fd0082f4d1ecd53eeb2a97e8d` | PASS / CALIBRATION_PASS | -20.086% to -1.198% | 0.199462--0.257888 |

## Implementation-only correction provenance

- IC04 checkpoint-namespace normalization: SHA-256 `33646a6b25762f09d8e5c8f837849aeede6a3c57c0a7804b30a8ed74a0ba31de`; pre-scientific implementation correction; scientific design unchanged.
- IC05 CUDA graph-lifetime/resource correction: SHA-256 `dec47d28e9e15433f2a950797b52078b6b370ce4186530041422c08221200a33`; failed PV-A attempt did not yield a P2/P1-P3 scientific outcome and no partial trace was reused; scientific design unchanged.
- Executed post-IC05 runtime core SHA-256: `cc6ded7ff70f18b6cb36d0677e79ee361e13c41f55b58298800e775b5b542b41`.

## Scientific closeout consequence

The raw bytes support the manuscript A52 numbers without correction. The closeout remains `PORTABILITY_COMPLETE`; no additional arm, seed, threshold, rank, selector, or estimator is authorized. R0 remains retrospective context, and PV-C remains a singleton multi-regime stress case.
