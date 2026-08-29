# TSPG H1-0016 REVIEW RESOLUTION AND H1-0017 DESIGN RATIONALE v1.0

**Date:** 2026-08-29  
**H1-0016 status after review:** `CLOSED_PASS_DIAGNOSTIC_REVIEW_RESOLVED`  
**Confirmatory H1:** `BLOCKED`  
**Next authorized diagnostic:** `TSPG-RUN-H1-0017`

## H1-0016 review resolution

The H1-0016 development review establishes:

1. AG1 and AG2 are not generic unrelated task spans. Raw span overlap is about
   96x the random-subspace reference and the class-composition hard gate passed.
2. Energy-weighted coverage is symmetric at approximately 0.41--0.43, while
   the transferred component itself is low-dimensional.
3. The low-k task-only transfer efficiencies are nevertheless low. Because
   `eta_k` is a trace over the selected k-dimensional subspace, it is invariant
   to rotations of the basis inside that subspace. Low eta therefore reflects
   a subspace mismatch, not merely arbitrary rotation of individual
   eigenvectors.
4. The top-1 cross-fold cosine near 0.052 is a direct empirical instability
   result. The broad L0 leading spectrum is treated as an analogous stability
   pattern, not as proof of top-1 degeneracy.
5. The prospective `phi/O_span` review trigger fired and was honored. It is
   retained in provenance as a development-only fired trigger and is not
   carried into confirmatory inference. Future support reporting uses `phi`,
   `phi/O_random`, `A_phi`, and conditional transferred effective rank.

No increase of n and no split redesign is justified at this point.

## Why H1-0017 is one-way and offline

H1-0010 already stores exact Learned-seed42 AG1 reduced geometry:
`C1`, `A320=Q1^T G_A Q1`, and therefore

`B11 = A320 + alpha I`

with locked alpha `1.6493039157931138e-09`.

H1-0016 stores

`H_2|1 = Q1^T G_T^(2) Q1`.

Therefore AG1->AG2 B-normalized cross-fit is exactly computable with dense
320x320 FP64 linear algebra and requires:

- no model load;
- no GPU;
- no new task gradient;
- no new G_A action.

## Important correction: no ad hoc fixed-rho third train space

A proposed third space
`S_B^(fixed-rho)` defined by matching `tr(W^T B W)/k` is not locked.

Reason:

- without a basis normalization, `tr(W^T B W)` is scale dependent and can be
  changed without changing the subspace;
- for a B-orthonormal basis it is identically k for every subspace;
- imposing Euclidean orthonormality plus an exact B-trace constraint would
  define a new constrained Grassmann optimization, not a matched version of
  the generalized top-k problem.

Instead H1-0017 separates denominator preference using two basis-invariant
quantities:

1. **Euclidean-unit B response**
   `bbar(S)=tr(Q_S^T B11 Q_S)/k`, where `Q_S` is any Euclidean-orthonormal
   basis of the subspace.
2. **Off-diagonal task scoring of the B-selected span**. If B-selection gains
   only under B-scoring but not under held-out task-only scoring, while also
   selecting substantially lower `bbar`, the gain is classified as
   denominator-selective rather than evidence of improved task transfer.

This decomposition answers the intended confound without introducing a new
optimization problem.
