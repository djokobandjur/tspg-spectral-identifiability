# TSPG H1-0015 FORMAL CLOSEOUT REPORT v1.0

**Date:** 2026-08-29  
**Run:** `TSPG-RUN-H1-0015`  
**Formal status:** `CLOSED_PASS_DIAGNOSTIC`  
**Scientific H1:** `NOT_EVALUATED`  
**Confirmatory H1:** `BLOCKED`

## Provenance

Runtime evidence ZIP SHA-256:

`8125067b17eee2abe61bf9a3519366d371b2c751e7a481a87b3de0c32ce11c71`

Stored result JSON SHA-256:

`ca2b79172d36c14726999be8b64dbfa82ff210ca52bd5b41d2f88d1b1d574d3c`

Remote raw NPZ:

`TSPG_H1_0015_LEARNED_SEED42_TAIL_RANK5_8_COMPLEMENT_KRYLOV_L4_v1_0.npz`

SHA-256:

`7d78e8584d265ff3a041ce84055720106a1fa49a09e7acc31be38482208e2279`

The failed UID-1545 attempt created no runtime directory and consumed no
scientific compute. The successful execution used an implementation-only
environment propagation correction before `torchvision` import.

## Closed scientific diagnostic

The decisive HEAD-to-COMBINED eigenvalue gains were:

- ranks 1--4: 1.12x, 1.20x, 1.23x, 1.30x
- ranks 5--8: 5.25x, 5.57x, 5.42x, 5.04x

Boundary diagnostics:

| space | Delta4 | lambda4/lambda5 | Delta8 | lambda8/lambda9 |
|---|---:|---:|---:|---:|
| BASELINE_L0 | 0.025243 | 1.025896 | 0.069211 | 1.074357 |
| HEAD | 0.768178 | 4.313657 | 0.039928 | 1.041588 |
| TAIL | 0.596531 | 2.478504 | 0.300381 | 1.429349 |
| COMBINED | 0.065411 | 1.069989 | 0.790273 | 4.768108 |

`Delta8` was derived post-run from the unchanged stored `lambda1...lambda12`
values. No rerun, no new `G_A` call, no raw-artifact mutation, and no
scientific budget expansion occurred.

Interpretation is locked as follows:

1. In the unrestricted augmented problem, complement-supported quotient
   amplification follows the task modes that receive targeted complement
   support.
2. The augmented spectral elbow therefore tracks the supported-mode/search
   boundary rather than an established intrinsic task dimension.
3. The TAIL branch separates task-mode count from raw seed-column count:
   eight raw seed columns but four targeted task modes again produce a
   four-mode-dominant branch.
4. HEAD-versus-COMBINED principal cosines show that the leading interior is
   comparatively stable while the cut-boundary mode is unstable; the
   instability is localized to the hard rank cut.
5. This mechanism is not transferred to the task-supported restricted problem.
   The uncontaminated L0 spectrum has its own separate result: no pronounced
   boundary at either k=4 or k=8.

No H1-0015 rerun, v1.2 scientific package, monolithic top-8 branch, or
random-range(R) control is required for closeout.
