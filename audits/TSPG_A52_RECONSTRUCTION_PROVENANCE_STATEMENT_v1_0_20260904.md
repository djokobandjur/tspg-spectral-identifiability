# TSPG A52 reconstruction provenance statement

**Date:** 2026-09-04  
**Purpose:** explain `_RECONSTRUCTED_` pre-lock artifact names without renaming or
breaking the existing SHA/provenance chain.

## What was reconstructed

The zero-compute pre-lock starter was reconstructed after the original starter
from a previous chat/session was no longer physically available as a downloadable
file. The reconstruction produced artifacts carrying `_RECONSTRUCTED_` in their
filenames, including the CIFAR split manifest, expected invariants, static QA,
P1b synthetic calibration, pre-lock config/run card, and reduced diagnostic code.

## Authoritative inputs

The reconstruction was tied to pre-existing authoritative artifacts, including:
- A52 diagnostic portability design (`v1.4`);
- the archived H1-0017 result and its SHA-locked H1-0010/H1-0016 reduced sources;
- the original ImageNet split manifest;
- deterministic static-QA and P1b specifications.

The reconstructed starter archive is preserved here with SHA-256:

`d5e2d1fd3b9b14590b1199695d9f385605976d26f3d874b8d896b31902d0f68d`

The executed pre-lock evidence archive is preserved here with SHA-256:

`de475c3bab394b11101ed8da191cdaeb192066df43d80e41a16e5702595497b3`

## Temporal / anti-adaptation chain

The reconstructed pre-lock files are timestamped before the A52 execution lock
and before the first PV-A scientific result files. The pre-lock runtime produced
the successful `R0_REPRO_PASS`, split provenance, static QA and P1b calibration
before the locked execution starter and before scientific arm execution.

The stronger protection is the byte-level chain: the execution starter embeds
the reconstructed pre-lock artifacts and their SHA-locked evidence before
`TSPG-RUN-PV-0001` outcomes are produced.

## IC01

IC01 corrected only the numerical implementation path used to reproduce the
archived H1-0017 result: it restored the archived explicit whitening /
`numpy.linalg.eigh` path instead of a mathematically equivalent direct generalized
solve. The successful reproduction had no matrix mismatch above `1e-12`, no
non-boundary row mismatch above `1e-12`, and no boundary-sensitive primary rank.

IC01 therefore changes neither the scientific estimand nor any new-arm outcome;
it is retained explicitly rather than hidden.

## Policy

Do not rename reconstructed files post hoc. Keep names and hashes unchanged and
cite this statement whenever the `_RECONSTRUCTED_` naming could otherwise be
misread as post-outcome scientific redesign.
