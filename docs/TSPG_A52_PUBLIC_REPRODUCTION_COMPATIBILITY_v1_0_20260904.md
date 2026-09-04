# A52 public reproduction compatibility note

The public v1.1.0 release preserves the exact historical A52 runtime code/config bytes and the exact pre-execution protocol digest. The exact protocol text also contained non-scientific publication-process governance and is therefore not distributed verbatim. Its SHA-256 identity is public in `manifests/TSPG_A52_PRIVATE_LOCK_IDENTITY_PUBLIC_v1_0_20260904.json`; a scientific semantic copy is included in the public A52 evidence archives.

This creates one expected host-compatibility difference for full model-level re-execution: historical runtime provenance originally hashed the exact protocol file by local filename. A public reproducer should use a derived local overlay that records the published exact locked digest from the identity manifest instead of requiring the omitted non-scientific text. This overlay may change only host-local routing/provenance plumbing. Checkpoints, samples, rank ladders, trace seeds/probes, numerical tolerances, estimands, selectors, calibration controls, and all scientific operations remain unchanged.

The committed historical A52 code/config files are provenance artifacts and must not be edited in place. Reporting-level and reduced-matrix verification requires no compatibility overlay and is fully supported by the public evidence archives.

A release-integrity gate must verify the derived overlay before v1.1.0 is described as supporting full model-level public re-execution.
