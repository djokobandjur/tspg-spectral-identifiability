# TSPG RUN CARD — H1-0019 v1.0

**Run ID:** `TSPG-RUN-H1-0019`  
**Status:** `AUTHORIZED_DEVELOPMENT_ONLY_LAST_ESTIMATOR`  
**Protocol:** `TSPG_PROTOCOL_LOCK_v0_50_20260829.md`

H1-0019 is the prospectively final estimator attempt.

Execution is split deliberately:

1. `fit_gate`: uses only AG1/AG2 and H18 dual Gram evidence, freezes all arm
   definitions, writes a SHA-locked fit artifact, and checks AP class
   composition. **AP task gradients computed: 0.**
2. `full`: verifies the fit-lock SHA, constructs the frozen arm bases, computes
   exactly 640 AP FP64 task gradients, applies the locked task-only success
   rule, and then computes at most 128 G_A directions solely for post-fit
   `bbar` diagnostics.

No AP-dependent reranking, rank dropping, alternate consensus definition, or
replacement of actual U640 by the H18 forecast is permitted.
