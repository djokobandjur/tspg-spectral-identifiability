# TSPG clean-environment M1--M2 reproduction progress audit v1.0

**Date:** 2026-08-30  
**Execution boundary:** fresh FMLE clean-reproduction workspace, public repository detached at `53c7ff9dc8afcc7ff782a6d2f340d8e183acbcf4`  
**Status:** `PASS_M1_M2`  
**End-to-end M1--M5 status:** `IN_PROGRESS_M3_M5_PENDING`

## Purpose

This audit records the first two stages of the sequential clean-environment M1--M5 execution test after portable materialization passed. The comparison is against the exact authoritative result JSON bytes contained in the SHA-locked H1-0015 and H1-0016 runtime-evidence archives. Runtime-local paths, wall-clock timing, and peak-memory metadata are classified separately from scientific/numerical fields.

No scientific claim or locked result is changed by this audit.

## M1 / H1-0015

### Execution

- runner return code: `0`
- technical status: `PASS`
- clean result JSON SHA-256: `becfe8441ab6ff8669b8aa2b49e184d89a8423a49a22f79eaddb04a532d2ab61`
- authoritative result JSON SHA-256: `ca2b79172d36c14726999be8b64dbfa82ff210ca52bd5b41d2f88d1b1d574d3c`

### Recursive JSON comparison

The complete decoded JSON trees differ at exactly `12` scalar leaves:

- `4` host-local source-path fields;
- `8` GA block `elapsed_sec` fields.

All other decoded fields are exactly equal, including all spectra, eigenvalues, gap statistics, QR diagnostics, orthogonality and residual metrics, principal-cosine quantities, gate/status fields, claim restrictions, and scientific metadata.

### Generated raw artifact

`TSPG_H1_0015_LEARNED_SEED42_TAIL_RANK5_8_COMPLEMENT_KRYLOV_L4_v1_0.npz`

- size: `232412532` bytes
- expected SHA-256: `7d78e8584d265ff3a041ce84055720106a1fa49a09e7acc31be38482208e2279`
- clean generated SHA-256: `7d78e8584d265ff3a041ce84055720106a1fa49a09e7acc31be38482208e2279`
- status: `EXACT_BYTE_MATCH`

**M1 decision:** `PASS_EXACT_SCIENTIFIC_NUMERICAL_REPRODUCTION_AND_RAW_BYTE_MATCH`.

## M2 / H1-0016

### Prespecified gate

The clean run executed the required `gate` stage before `full`.

Observed gate state:

- technical status: `PASS`
- new task gradients computed during gate: `0`
- AG1 unique classes: `98`
- AG2 unique classes: `98`
- class intersection: `96`
- class union: `100`
- class-composition gate: `PASS`

Clean gate JSON SHA-256: `6700d6c3832bc4005df120e4fd35cf15bad1047c50ed82f3cf591898a2c1e644`  
Authoritative gate JSON SHA-256: `97e6e20baa6aa3130385c6c91d5f5d4179925e2f54a48da7bc7eed3c4c656759`

A complete decoded-tree comparison finds exactly `4` differences, all host-local source-path fields. Every other gate field is exactly equal.

### Full execution

- technical status: `PASS`
- newly computed AG2 FP64 task gradients: `320`
- new GA actions: `0`
- confirmatory H1 status remains the locked development-state value
- clean result JSON SHA-256: `c31519c197dd2502cc53c5dd69ad2581192efa21cb00f766897ca89f91a1ce14`
- authoritative result JSON SHA-256: `6ea3ed7d85fddaff6e60a0d6c40974f84c13106f67c3508360c0ed37862e4428`

Selected reproduced values include:

- `O_span = 0.20369026626979364`
- `phi_1_to_2 = 0.4073639540946265`
- `phi_2_to_1 = 0.42767991322327903`
- `A_phi = 0.04865842364403148`
- `phi_1_to_2 / O_span = 1.9999186095375867`
- `phi_2_to_1 / O_span = 2.099658079177945`
- review trigger: `true`
- `r_eff_C1 = 32.59649705153393`
- `r_eff_C2 = 41.35948980632585`
- transferred `r_eff_H21 = 23.76395093487638`
- transferred `r_eff_H12 = 18.572277907313683`

### Recursive JSON comparison

The complete decoded M2 result trees differ at exactly `8` scalar leaves:

- `3` host-local source/checkpoint path fields;
- `1` host-local gate-result path field;
- `1` gate-result SHA field, induced solely by the gate JSON's host-local path differences;
- `2` elapsed-time fields;
- `1` peak-CUDA-memory field.

Every other decoded field is exactly equal. This includes the full canonical-correlation vector, all task-only curves, coverage and effective-rank values, identity-gate outputs, sample indices, provenance SHA identities, status fields, and all reported numerical quantities.

### Generated artifacts

1. `TSPG_H1_0016_LEARNED_SEED42_AG2_320_FP64_TASK_GRADIENTS_v1_2.npy`
   - size: `387317888` bytes
   - expected SHA-256: `2850c66d13dc45f48baa114f540e29c3ca75903db412ac8f93c048fdb8b930eb`
   - clean generated SHA-256: `2850c66d13dc45f48baa114f540e29c3ca75903db412ac8f93c048fdb8b930eb`
   - status: `EXACT_BYTE_MATCH`

2. `TSPG_H1_0016_LEARNED_SEED42_AG1_AG2_TASK_CROSSFOLD_DERIVED_v1_2.npz`
   - size: `390626716` bytes
   - expected SHA-256: `afe9a94d1c5c7f7f3d8986348b15c7513013c77969781d54d03c0f8154b4baea`
   - clean generated SHA-256: `afe9a94d1c5c7f7f3d8986348b15c7513013c77969781d54d03c0f8154b4baea`
   - status: `EXACT_BYTE_MATCH`

**M2 decision:** `PASS_EXACT_SCIENTIFIC_NUMERICAL_REPRODUCTION_AND_GENERATED_BYTES_2_OF_2`.

## Overall progress decision

The clean-environment execution chain is now:

- portable materialization: `PASS`
- M1: `PASS`
- M2 prespecified gate: `PASS`
- M2 full execution: `PASS`
- M3: pending
- M4: pending
- M5 fit gate/full: pending

The end-to-end M1--M5 release gate remains open until M3--M5 execute successfully and are compared against their locked authoritative results.