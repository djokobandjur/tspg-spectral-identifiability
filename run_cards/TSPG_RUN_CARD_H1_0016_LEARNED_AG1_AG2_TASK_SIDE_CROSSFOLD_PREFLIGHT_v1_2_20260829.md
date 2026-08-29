# TSPG RUN CARD — H1-0016 v1.2

**Run ID:** `TSPG-RUN-H1-0016`  
**Status:** `AUTHORIZED_DEVELOPMENT_ONLY_V1_2`  
**Protocol:** `TSPG_PROTOCOL_LOCK_v0_45_20260829.md`  
**Implementation corrections:** `IC02`, `IC03`

v1.2 supersedes v1.1 because the v1.1 runner/notebook disagreed on generated
gate/result filenames. No scientific H1-0016 computation occurred under the
failed v1.1 attempt.

Scientific design is unchanged from A45.

After the zero-gradient hard gate passes, the only new scientific compute
authorized is exactly 320 AG2 per-example true-label FP64 task gradients.

No new `G_A` action is permitted.
