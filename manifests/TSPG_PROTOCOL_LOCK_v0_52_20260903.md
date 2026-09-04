# TSPG PROTOCOL LOCK v0.52

**Date:** 2026-09-03  
**Status:** `ACTIVE`  
**Supersedes:** `TSPG_PROTOCOL_LOCK_v0_51_20260829.md`  
**Authorized run:** `TSPG-RUN-PV-0001`  

## State transition

Protocol v0.51 closed the original H1 estimator-development program and authorized manuscript reconstruction only. A52 v1.5 creates a **separate diagnostic-portability study**; it does not reopen H1-0019, AP, or any M1--M5 estimator. A51 scientific closeout and drift prohibitions remain binding.

The zero-compute A52 pre-lock evidence was ingested as `PASS_ZERO_COMPUTE_PRELOCK_EVIDENCE_INGESTED`. Its source evidence ZIP SHA-256 is `de475c3bab394b11101ed8da191cdaeb192066df43d80e41a16e5702595497b3`. `R0-REPRO` passed after the provenance-preserving IC01 correction, with no boundary-sensitive cut.

## Sole scientific authorization

Only `TSPG-RUN-PV-0001` is authorized, and only for the four prespecified new Learned-PE arms `PV-A`, `PV-B1`, `PV-B2`, `PV-C` under A52 v1.5. R0 remains retrospective/archive-only and consumes no new model/GPU compute. No extra checkpoint, seed, PE family, rank substitution, split change, alternate tau, or post-outcome redesign is authorized.

Before any scientific model execution, the locked starter must pass its checkpoint byte/config/state-dict hard gate. Failure leaves scientific execution blocked.

## Trace/tau lock

For each new arm, `tau=1e-4*trace_hat(G_A)` uses deterministic FP64 Rademacher Hutchinson probes on the locked C cohort with counts `16 -> 32 -> 64`, RSE gate `<=0.02`, and Learned seed stream beginning at `2026083200`. Failure at 64 is `TRACE_ESTIMATION_GATE_FAIL`. No extension is permitted.

## Compute ceiling per new arm

- task gradients: 320 AG1 + 320 AG2 = 640;
- support-basis G_A direction-actions: <=320;
- trace quadratic JVP direction-actions: <=64;
- implementation certification: exactly 8 direction-actions;
- maximum geometry direction-actions: 392.

Across four arms: 2560 task gradients and at most 1568 geometry direction-actions. The C sets contain 1024 unique arm-image memberships in total; repeated operator traversals are accounted by direction-actions, not misreported as one-time image evaluations.

## Evidence and inference boundary

Primary prospective cross-cell contrasts are only `PV-A vs PV-B2` (architecture at seed 123) and `PV-B1 vs PV-B2` (seed within ViT-S). R0-containing comparisons are `RETROSPECTIVE_ANCHOR_CONTEXT`. PV-C is a singleton stress case. No p-values, population architecture effect, seed variance estimate, prevalence claim, or universal-replication language is authorized.

Scientific outcomes do not define PASS/FAIL. Completion status is `PORTABILITY_COMPLETE`, `PORTABILITY_PARTIAL_NON_EVALUABLE`, or `TECHNICAL_FAIL`; P2 mechanism labels remain case-wise descriptive outputs.
