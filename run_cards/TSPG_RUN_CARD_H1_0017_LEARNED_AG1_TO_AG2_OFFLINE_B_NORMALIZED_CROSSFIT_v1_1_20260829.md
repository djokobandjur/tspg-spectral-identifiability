# TSPG RUN CARD — H1-0017 v1.1

**Run ID:** `TSPG-RUN-H1-0017`  
**Status:** `AUTHORIZED_DEVELOPMENT_ONLY_V1_1`  
**Protocol:** `TSPG_PROTOCOL_LOCK_v0_47_20260829.md`

Scientific design is unchanged from A46.

A47/IC05 changes only numerical certification of generalized eigenpairs in
the pre-existing near-null tail.

The run remains pure offline FP64 320x320 algebra:
- no GPU;
- no model;
- no gradients;
- no new G_A action.

The original full-spectrum self-scaled generalized residual is reported for
transparency but is not a gate. See IC05.
