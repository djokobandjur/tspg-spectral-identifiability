# TSPG H1-0016 INGEST AUDIT AND SCIENTIFIC INTERPRETATION v1.0

**Date:** 2026-08-29  
**Run:** `TSPG-RUN-H1-0016`  
**Evidence ZIP:** `TSPG_H1_0016_RUNTIME_EVIDENCE_v1_2_20260829.zip`  
**Evidence ZIP SHA-256:** `0d7c6acfe8e38826fbb36322f30f187f9442d4ea42253e9463328d004062e022`  
**Ingest status:** `PASS`  
**Technical status:** `PASS`  
**Scientific decision status:** `REVIEW_TRIGGER_FIRED — DISCUSSION REQUIRED`  
**Confirmatory H1:** `BLOCKED_PENDING_REVIEW`  
**Protocol:** `v0.45` unchanged

## Integrity

- ZIP integrity: PASS.
- Compact evidence internal SHA checks: 22/22 PASS.
- Gate/result provenance hashes are internally consistent.
- New AG2 task gradients: 320.
- New G_A actions: 0.
- All numerical identity gates in the H1-0016 result: PASS.

Large remote artifacts retained on FMLE:

- `TSPG_H1_0016_LEARNED_SEED42_AG2_320_FP64_TASK_GRADIENTS_v1_2.npy`
  - SHA-256 `2850c66d13dc45f48baa114f540e29c3ca75903db412ac8f93c048fdb8b930eb`
  - 387,317,888 bytes
- `TSPG_H1_0016_LEARNED_SEED42_AG1_AG2_TASK_CROSSFOLD_DERIVED_v1_2.npz`
  - SHA-256 `afe9a94d1c5c7f7f3d8986348b15c7513013c77969781d54d03c0f8154b4baea`
  - 390,626,716 bytes

## Semantic-composition hard gate

PASS:

- AG1 unique classes: 98/100
- AG2 unique classes: 98/100
- class-set intersection: 96/100

The catastrophic class-ordered-fold confound targeted by A45 is therefore not
present.

## Raw span reproducibility

`O_span = 0.203690266` versus random-subspace reference
`O_random = 0.002115059`.

Thus the observed full-span overlap is
`96.30x` the random reference.

The canonical-correlation spectrum is strongly non-random: the leading
correlations are near one and a large fraction of the 320-dimensional span
remains above the random singular-value scale.

This rules out the simple failure mode in which AG1 and AG2 are essentially
generic unrelated 320-dimensional subspaces.

## Energy-weighted coverage

- phi_1->2 = `0.407363954`
- phi_2->1 = `0.427679913`
- two-way mean phi = `0.417521934`
- A_phi = `0.048658`

Relative to raw span overlap:

- phi_1->2 / O_span = `1.999918610`
- phi_2->1 / O_span = `2.099658079`

Relative to random subspaces:

- phi_1->2 / O_random = `192.60x`
- phi_2->1 / O_random = `202.21x`

The prospective `ENERGY_ENRICHMENT_REVIEW_TRIGGER` fired because the
1->2 ratio is <=2. Numerically it is only `0.000081390`
below 2, i.e. `0.00407%` below the
threshold. This is a prespecified review trigger, not a claim failure.

Coverage is lower than the prospectively recorded development expectation
0.5--0.9, but it is highly symmetric and enormously above the random-space
reference.

## Conditional dimensionality of transferred energy

Always interpreted jointly with phi:

- in-sample r_eff(C1), planning only: `32.5965`
- in-sample r_eff(C2), planning only: `41.3595`
- r_eff(H_2|1), conditional on transferred energy: `23.7640`
- r_eff(H_1|2), conditional on transferred energy: `18.5723`

The transferred component is therefore concentrated on a scale of roughly
19--24 effective dimensions, but only after accounting for the fact that phi
is approximately 0.41--0.43.

## Task-only oracle versus fair cross-fit

Within the transferred component, the held-out oracle is strongly front-loaded:

- at k=16 it captures about 67--76% of transferred energy;
- at k=32 it captures about 86--91%;
- at k=64 it captures about 98--99%.

By contrast, train-fold top-k task eigenvectors transfer inefficiently at
small k. At k=32:

- eta_1->2 = `0.4059`
- eta_2->1 = `0.4372`

The low-k eta profile rises rather than showing the prospectively expected
high-small-k pattern. This means the held-out transferred energy is
low-dimensional, but the specific leading Euclidean task eigenspaces fit on
one fold are not themselves stably reproduced on the other fold.

This distinction is the principal scientific result of H1-0016.

## Development interpretation

H1-0016 does **not** support the simple conclusion "n=320 is too small and the
two task spans do not transfer." The raw spans overlap strongly and directional
coverage is symmetric.

It does show that:
1. only about 42% of total held-out task energy lies in the opposite fold's
   empirical task span;
2. the transferred energy itself is concentrated;
3. the low-dimensional in-sample Euclidean task modes are not reliable
   train-to-held representatives of that concentrated component.

Therefore the task-only preflight is informative but not sufficient to
authorize the 20-checkpoint confirmatory H1 run. The prespecified review
trigger is honored.

No new protocol or next scientific package is authorized by this ingest
report. The next design decision must be discussed before implementation.
