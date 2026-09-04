# Public scientific semantic copy

This file is the public scientific semantic copy of the pre-execution A52 v1.5 lock. The exact locked source byte identity is:

`SHA-256 2fc2c8dbeca0ce0affe17055e7ba6e7a7ffd8c7b9ba7488c15bfcf7e32a89aeb`

Non-scientific publication-process governance clauses are omitted from this public copy. Scientific arms, checkpoint identities, rank ladders, estimands, contrasts, numerical gates, stopping rules, case-wise interpretation rules, singleton caveats, and drift prohibitions are unchanged. The exact locked digest above is independently recorded in the runtime provenance of all four prospective arms.

---

# TSPG PROTOCOL AMENDMENT A52 — DIAGNOSTIC PORTABILITY PANEL v1.5

**Date:** 2026-09-03  
**Status:** `LOCKED — AUTHORIZED ONLY THROUGH THE SHA-LOCKED A52 EXECUTION STARTER`  
**Authorized run:** `TSPG-RUN-PV-0001`  
**Archived implementation anchor:** `R0-REPRO`  
**New empirical arms:** `PV-A`, `PV-B1`, `PV-B2`, `PV-C`  
**Parent scientific lock:** A51 (exact parent byte identity retained in the private governance provenance)  
**Supersedes:** `A52 v1.4` design draft (not executed); incorporates the passed zero-compute pre-lock evidence and the final trace/accounting refinement below

---

## 1. Governance purpose and relation to A51

A51 closed the original estimator-development program after H1-0019. A52 does **not** reopen M1–M5, does not reuse the consumed AP fold for estimator repair, and does not authorize a new identifiability estimator.

A52 creates one narrowly scoped study with a different estimand:

> **How does the locked numerator–denominator diagnostic behave under prespecified implementation calibrations and under the H1-0017 actual-B cross-scoring audit on independent Learned-PE checkpoints?**

The portability panel tests the **diagnostic procedure and its empirical pattern**, not whether the original seed-42 ViT failure is universal.

### 1.1 A51 scientific locks retained

The following remain permanently closed and unchanged:

- M1 unrestricted generalized-optimization diagnosis;
- M2 AG1/AG2 support and orientation diagnosis;
- M3 seed-42 H1-0017 result;
- M4 finite-n result;
- M5 H1-0019 third-fold result;
- the AP fold and its anti-adaptation interpretation;
- `AP_gradients_before_arm_lock = 0`;
- `no_alternate_consensus_after_AP = true`.

A51 drift prohibitions 1–3 apply to **all A52 outputs**:

1. no causal attribution to high dimensionality;
2. no prevalence/generalization claim across checkpoints, PE families, architectures, or datasets;
3. no inevitability language implying that every estimator or sample configuration fails.

No portability outcome may redesign an M1–M5 estimator, replace/reinterpret H1-0019, or trigger another AP-based estimator attempt.

### 1.2 Scientific continuity with the parent lock

A52 does not supersede A51's scientific claim hierarchy, stopping rule, evidence, or drift prohibitions. It adds only the prespecified diagnostic-portability study defined below.

---

## 2. Three evidence layers

A52 separates three logically different questions.

### Layer 0 — archived implementation equivalence (`R0-REPRO`)

Before any new scientific compute, the new A52 reduced-analysis implementation must reproduce the archived H1-0017 seed-42 result from the locked reduced sources. This is a **technical equivalence test**, not a new scientific analysis and not an M1–M5 reopening.

`R0-REPRO` uses **zero new task gradients, zero model/GPU execution, and zero new G_A actions**.

### Layer A — algebraic / reduced-pipeline calibration (`P1`, `P1b`, `P3`)

Constructive controls verify that the implementation can identify a deliberately injected denominator-driven reversal and can avoid a denominator-driven flag under an equal-mean-denominator control. These controls are calibration tests only.

**They are not empirical evidence that a checkpoint naturally exhibits denominator-driven selection.**

### Layer B — empirical portability (`P2`)

The real attention geometry `B` is used without synthetic modification. P2 reports the numerator/denominator pattern separately in each prespecified case.

Because the same `B11` enters normalized selection and normalized held-out scoring, a small `R_B` can structurally amplify normalized scoring. Therefore P2's empirical content is not summarized as multiple independent confirmations. The primary empirical observables are:

- task-only selection contrast;
- actual denominator-response magnitude and anisotropy;
- normalized-score contrast;
- selector separation and held-out spectral identifiability diagnostics.

No P2 pattern is required for A52 to be a valid experiment.

---

## 3. Anchor and prespecified checkpoint panel

### 3.1 Closed anchor

| ID | Architecture/configuration | Dataset | PE | Seed | Training regime | Native Learned shape / d_p | SHA-256 |
|---|---|---|---|---:|---|---|---|
| `R0` | ViT-B, ImageNet configuration | ImageNet-100 | Learned | 42 | AMP-trained | `197 x 768 = 151,296` | `7fcca75916c2d6f0f64aa5c381812ad3a305ba1a04672e9288f4251ab683c536` |

`R0` is **retrospective and discovery-conditioned**: it is the checkpoint on which the denominator-selective pattern was identified during the closed M1--M5 program and which motivated the present portability study. It is retained as an archived anchor and implementation reference, not as a prospectively sampled cell. No contrast containing `R0` may be described as a fully prospective contrast.

### 3.2 New empirical arms

| Arm | Role | Architecture/configuration | Dataset | PE | Seed | Training regime | Native Learned shape / d_p | SHA-256 |
|---|---|---|---|---|---:|---|---|---|
| `PV-A` | ViT-B seed portability | ViT-B, ImageNet configuration | ImageNet-100 | Learned | 123 | AMP-trained | `197 x 768 = 151,296` | `fbb8d70f72fb6ee1bb93b1d00cca663ffb222f489d16d8149f2e01efd65c351e` |
| `PV-B1` | backbone portability, seed 42 | ViT-S, ImageNet configuration | ImageNet-100 | Learned | 42 | AMP-trained auxiliary cohort | `197 x 384 = 75,648` | `a518ec4ba5478539e85b8a3841e847cd014e7f1eddc7e48752bfe105b68ace26` |
| `PV-B2` | backbone portability, seed 123 / within-axis replicate | ViT-S, ImageNet configuration | ImageNet-100 | Learned | 123 | AMP-trained auxiliary cohort | `197 x 384 = 75,648` | `c04bd01615a897d713e5e0deb94afea0cdc0e0367d09a14846ab46b93bf82524` |
| `PV-C` | dataset / input-tokenization stress case | ViT-B backbone, CIFAR configuration (4x4 patches) | CIFAR-100 | Learned | 42 | AMP-trained | `65 x 768 = 49,920` | `a65418972b2f3c9c68b5031d79159fa5141cfccab3d12454947321500d545cdd` |

### 3.3 Prespecified ImageNet 2x2 architecture × seed grid

The ImageNet evidence is displayed as a small crossed design for context:

| | seed 42 | seed 123 |
|---|---|---|
| ViT-B | `R0` retrospective/discovery-conditioned anchor | `PV-A` prospective |
| ViT-S | `PV-B1` prospective | `PV-B2` prospective |

The four geometrically obvious cell contrasts are **not evidentially equivalent**. They are partitioned prospectively before outcome access.

**Fully prospective contrasts (primary portability contrasts):**

- architecture at seed 123: `PV-A` vs `PV-B2`;
- seed within ViT-S: `PV-B1` vs `PV-B2`.

These two contrasts contain no discovery-conditioned cell. They are the primary cross-cell evidence in the prespecified crossed design.

**R0-containing retrospective-context contrasts (secondary/descriptive only):**

- seed inside ViT-B: `R0` vs `PV-A`;
- architecture at seed 42: `R0` vs `PV-B1`.

These remain useful for showing the full 2x2 pattern and for asking whether a direction seen at the discovery anchor is reproduced in a newly prespecified cell, but they may not be counted as fully prospective replication evidence.

With one checkpoint per cell, the design supports **case-wise contrast replication/directional comparison**, not estimation of an architecture or seed effect distribution. In particular, no `X ± Y`, random-effects, or within-cell variance claim is authorized.

`PV-C` sits outside this grid. It is a single prespecified stress case with no same-regime replicate and simultaneously changes dataset, input/tokenization regime, sequence length, and native positional dimension. Therefore a `PV-C` deviation cannot be separated from singleton checkpoint variation and may not be interpreted as a dataset effect or as replicated cross-dataset evidence.

### 3.4 PE-family scope

All arms use Learned PE because the estimand is a native **learned positional-parameter** geometry. In the available Sinusoidal, RoPE, and ALiBi checkpoints, the corresponding positional state is fixed rather than an analogous learned positional table. A52 therefore does **not** test PE-family portability and may not be presented as doing so.

No additional checkpoint may be added after outcome inspection.

### 3.5 Checkpoint hard gate

Before model execution, per new arm:

1. resolve exact local checkpoint path;
2. recompute SHA-256 and require exact match;
3. record model config, head count, embedding dimension, patch size, sequence length, Learned positional tensor shape, clean metadata, and training-regime label;
4. abort the arm on mismatch; no substitution without a new amendment.

---

## 4. Numerical path

All arms retain the authoritative closed-program numerical path:

- FP64 derivatives;
- Math SDPA;
- ordinary scalar reverse-mode per-example gradients;
- dense native `d_p x d_p` task/attention matrices prohibited;
- exact reduced/low-rank task-side representations;
- matrix-free/reduced attention-geometry actions;
- row-centered pre-softmax attention displacement;
- all non-positional model parameters frozen;
- native Learned positional table only;
- `B = G_A + tau M_p`, `M_p=I/d_p`, `tau=1e-4 tr(G_A)`;
- `alpha=tau/d_p` in the reduced task-support generalized problem.

Numerical tolerances are not loosened after observing an arm.

### 4.1 Ridge-relative geometry sentinel

Because `d_p` and `tr(G_A)` differ across architectures/input regimes, `alpha=tau/d_p` is not numerically identical across cells even though the ridge construction is scale-normalized. For every empirical arm report

`rho_ridge = alpha / lambda_min(B11)`.

Also store `alpha`, `lambda_min(B11)`, and `lambda_max(B11)`. `rho_ridge` is an **interpretability sentinel**, not a post-hoc tuning parameter. A value approaching one means that the smallest reduced B mode is increasingly ridge-determined; cross-architecture differences in `bbar`/normalized scoring must then be qualified as potentially ridge-influenced rather than attributed solely to attention geometry. No outcome-dependent threshold change is permitted.

The archived R0 target is

`alpha = 1.6493039157931138e-09`,
`lambda_min(B11) = 3.33269921485444e-05`,
`rho_ridge = 4.948853195157456e-05`.

---

## 5. Samples and split provenance

### 5.1 ImageNet cells `R0`, `PV-A`, `PV-B1`, `PV-B2`

Use the exact original TSPG ImageNet-100 **5,000-image validation-set** arrays:

- `C`: 256 attention-geometry calibration images;
- `AG1`: 320 fit task-gradient images;
- `AG2`: 320 independent scoring task-gradient images.

The pre-run split-provenance record must identify the authoritative source files, dataset root contract, index-array SHA-256 values, label semantics, and class histograms. At minimum it must reproduce the archived H1-0016 index hashes:

- `AG1_indices_sha256 = bca79e4000650685a2c9d4de5c5842cea7bce5880f4c659f08c3756d0fb11246`;
- `AG2_indices_sha256 = 9c16aba3c4596716f43a67e5405ab75aa1216baf68bd3dc6e26319180c61aea1`.

The authoritative archived TSPG split manifest is now frozen to

`TSPG_SPLIT_MANIFEST_IN100_PILOT_v1_0_20260819.json`,
SHA-256 `9488e109f43f23a1bdd1ebda771a707e2b4b1e6f535ce6227bf0705d1834d1af`.

Using the same byte convention as the archived AG hashes,
`sha256(np.asarray(indices,dtype=np.int64).tobytes())`, the calibration set is locked to

- `C_indices_sha256 = 44007d048ec59a2329da221ab9cad1f20259a48719225f0467065fa33dcbb968`.

The pre-lock host preflight must additionally read the actual ImageFolder targets and reproduce the archived AG semantic coverage (AG1/AG2 unique classes `98/98`, intersection `96`). No resampling. `AP` is never accessed.

### 5.2 CIFAR arm `PV-C`

Create one portability-only deterministic manifest **before any model gradient or G_A action**:

1. canonical CIFAR-100 test-set indices/labels;
2. initialize **one** NumPy `Generator(PCG64(seed=20260903))` exactly once, then for class IDs `0..99` in ascending order call `rng.permutation(indices_of_that_class)`;
3. concatenate by a continuing round-robin stream over class IDs `0..99`;
4. first 256 -> `C`;
5. next 320 -> `AG1`;
6. next 320 -> `AG2`;
7. require pairwise zero overlap;
8. require all 100 classes in `AG1` and `AG2`; record exact class counts for all sets;
9. SHA-lock JSON/CSV manifest before scientific compute.

No split modification after outcomes.

---

## 6. Rank ladder and evaluability

To preserve H1-0017 comparability:

- reported ladder: `k={1,2,4,8,16,32}`;
- primary portability ranks: `k={4,8,16,32}`;
- `k={1,2}` secondary/sentinel.

P1/P3 require 64 AG1 task eigenvectors so that paired top-k/next-k blocks exist through `k=32`.

### 6.1 Locked numerical-rank and constructive-stability rules

Let the symmetrized reduced AG1 task matrix have descending eigenvalues

`lambda_1 >= ... >= lambda_m >= 0`, with `m<=320`.

Define

`tol_rank = m * eps64 * lambda_1`,

where `eps64 = 2.220446049250313e-16`, and

`r_num = count(lambda_i > tol_rank)`.

The machine-epsilon rank rule is retained as a bookkeeping rank diagnostic, but **it is not sufficient to certify the constructive P1/P3 layer**, because a formally nonzero near-null tail may still have numerically unstable eigenvectors.

Therefore P1/P3 additionally require the prespecified constructive spectral-floor gate

`lambda_64/lambda_1 > 1e-8`.

Both conditions must hold:

1. `r_num >= 64`;
2. `lambda_64/lambda_1 > 1e-8`.

If either fails, mark `NON_EVALUABLE_CONSTRUCTIVE_STABILITY_GATE`; do not run P1/P3 at `k=32`, do not lower the maximum rank post hoc, and do not relabel the condition as a calibration failure. P2 may still be technically computable, but the asymmetry must be reported explicitly.

For transparency, also record task-spectrum relative boundary gaps

`g_task(j)=(lambda_j-lambda_(j+1))/lambda_1`

for every available `j` in the union of `{k,2k}` over `k={1,2,4,8,16,32}`. These gaps are diagnostics of cut sensitivity; the hard constructive gate remains the locked `lambda_64/lambda_1` floor above.

The pre-run code must record `lambda_1`, `lambda_64`, `lambda_64/lambda_1`, `tol_rank`, `r_num`, and all requested `g_task(j)` values. No threshold change is permitted after any P1/P2/P3 outcome is inspected.

---

## 7. `R0-REPRO` archived implementation-equivalence gate

Before any new model/GPU execution, the A52 reduced-analysis code must run on the archived H1-0017 locked sources and reproduce `TSPG_H1_0017_RESULT_v1_1_20260829.json`.

Required sources include the archived reduced train geometry and cross-fold source used by H1-0017. Their SHA-256 values must be checked before use.

For `k={1,2,4,8,16,32}` reproduce, to absolute tolerance `1e-12` unless a stored quantity has a stricter original gate:

- all four 2x2 efficiencies;
- both matched contrasts;
- `bbar(S_E)`, `bbar(S_B)`, `R_B`;
- raw task and B numerators;
- oracle sums/fractions;
- held-out generalized gap;
- B-principal-angle quantities;
- numerical certification quantities that are deterministically recomputable.

The expected descriptive pattern is `DENOMINATOR_SELECTIVE_REVERSAL` at all six ranks, including stored `R_B` values approximately

`0.00246, 0.00273, 0.00341, 0.00475, 0.00736, 0.01342`.

#### Train-boundary sensitivity safeguard

Before applying the `1e-12` exact-k equivalence tolerance, recompute and store the train generalized relative boundary gap

`g_train_B(k)=(lambda_train,k-lambda_train,k+1)/lambda_train,k`

for every reported `k<rank`, with prespecified numerical near-tie sentinel

`eps_gap_repro = 1e-8`.

- If `g_train_B(k) >= eps_gap_repro`, the exact-k reproduction quantities above remain hard equivalence gates.
- If `g_train_B(k) < eps_gap_repro`, mark that cut `R0_REPRO_BOUNDARY_SENSITIVE`. A mismatch confined to selector-dependent exact-k trace/angle quantities at that cut is **not** automatically `TECHNICAL_EQUIVALENCE_FAIL`; the cut is documented as numerically non-identifying at the requested boundary. Source hashes, reduced matrices, eigenvalues, B reconstruction/orthogonality/backward-error checks, and all non-boundary-sensitive ranks must still pass.
- If boundary sensitivity prevents equivalence assessment at more than two of the four primary ranks `{4,8,16,32}`, return `R0_REPRO_INCONCLUSIVE_BOUNDARY_SENSITIVITY` and keep new scientific compute blocked pending an explicit amendment.

This safeguard is fixed before execution and prevents a near-degenerate cut from being misclassified as an implementation failure.

Absent the prespecified boundary-sensitive exception above, `R0-REPRO` failure is `TECHNICAL_EQUIVALENCE_FAIL` and blocks all new scientific compute. It is not a new scientific negative result.

---

## 8. Actual-B empirical portability diagnostic (`P2`)

P2 reproduces the H1-0017 definitions for each new empirical arm.

Let `Q1` be an Euclidean-orthonormal basis for empirical AG1 task support. In Q1 coordinates define:

- `C1 = Q1^T G_T^(1) Q1`;
- `A11 = Q1^T G_A Q1`;
- `B11 = A11 + alpha I`, where `alpha=tau/d_p`;
- `H21 = Q1^T G_T^(2) Q1`.

### 8.1 Train selectors and mandatory Euclidean QR conversion

For each locked `k`:

- `S_E(k)`: leading `k` eigenspace of `C1`;
- solve `C1 w = lambda B11 w` for the generalized directions;
- `S_B(k)`: span of the leading `k` generalized directions.

The generalized solver basis is `B11`-orthonormal, **not** Euclidean-orthonormal. Therefore all Euclidean-span quantities must use

`Q_B = qr(W_B[:, :k])`

(or an algebraically equivalent deterministic Euclidean orthonormalization of the same span), never the raw generalized eigenvectors.

Mandatory gates:

- `||Q_B^T Q_B-I||_inf <= 1e-10`;
- projector/span equivalence between `Q_B` and raw leading generalized span <=`1e-10`;
- raw generalized basis retains its separate `B11`-orthonormality certification.

`eta_task(S_B)` and `bbar(S_B)` **must** use `Q_B`.

### 8.2 Held-out task-only efficiency

Let `nu_j` be descending eigenvalues of `H21`. For Euclidean-orthonormal `Q_S`:

`task_num(S)=tr(Q_S^T H21 Q_S)`

`U_task(k)=sum_(j<=k) nu_j`

`eta_task(S,k)=task_num(S)/U_task(k)`.

### 8.3 Held-out B-normalized efficiency

Define

`K_held = B11^(-1/2) H21 B11^(-1/2)`

with descending eigenvalues `mu_j`. For candidate Euclidean span `Q_S`, define

`W_S = Q_S (Q_S^T B11 Q_S)^(-1/2)`.

Then

`B_num(S)=tr(W_S^T H21 W_S)`

`U_B(k)=sum_(j<=k) mu_j`

`eta_B(S,k)=B_num(S)/U_B(k)`.

Also retain

`C_cross_B(S)=B_num(S)/tr(B11^(-1)H21)`

`U_B_fraction(k)=U_B(k)/tr(B11^(-1)H21)`.

### 8.4 Locked 2x2 table

At every `k` report:

| train-selected span | held-out task-only | held-out B-normalized |
|---|---:|---:|
| `S_E(k)` | `eta_task(S_E)` | `eta_B(S_E)` |
| `S_B(k)` | `eta_task(S_B)` | `eta_B(S_B)` |

Primary matched contrasts:

`Delta_sel_task = eta_task(S_B)-eta_task(S_E)`

`Delta_sel_B = eta_B(S_B)-eta_B(S_E)`.

### 8.5 Euclidean-unit denominator response and anisotropy

For Euclidean-orthonormal `Q_S`:

`G_B(S)=Q_S^T B11 Q_S`

`bbar(S,k)=tr(G_B(S))/k`

`R_B(k)=bbar(S_B,k)/bbar(S_E,k)`.

Because `bbar` is a mean response and can hide within-span anisotropy, also report for each `S_E` and `S_B`:

- `bgram_min = lambda_min(G_B(S))`;
- `bgram_max = lambda_max(G_B(S))`;
- `bgram_condition = bgram_max/bgram_min`.

No universal `R_B` pathology threshold is authorized.

### 8.6 Diagnostic-dependence / amplification audit

The three quantities `Delta_sel_task`, `Delta_sel_B`, and `R_B` are not treated as statistically independent confirmations.

Report

`tau_task = eta_task(S_B)/eta_task(S_E)`

and the observed normalized selector ratio

`R_norm = eta_B(S_B)/eta_B(S_E)`.

Define

`A_norm = R_norm/tau_task`,

`M_mean = tau_task/R_B`,

where `M_mean` is the normalized selector ratio predicted by a scalar/mean-denominator approximation. Also report `1/R_B`.

For each span define the exact span correction factor

`F(S) = bbar(S) * B_num(S) / task_num(S)`.

Then the following identity is exact for the reported trace quantities:

`R_norm = M_mean * F(S_B)/F(S_E)`,

so

`A_over_mean_den = A_norm/(1/R_B) = F(S_B)/F(S_E)`.

For `k=1`, `F(S_E)=F(S_B)=1` up to numerical tolerance and the scalar mean-denominator relation is exact. For `k>1`, `F` measures the correction induced by within-span denominator anisotropy and its alignment with held-out task energy. `bbar` alone is therefore not claimed to determine normalized amplification.

Also emit the ordering diagnostic:

- `MEAN_DENOMINATOR_ORDERING_SUFFICIENT_FOR_SIGN` if `M_mean` and `R_norm` lie on the same side of one (or both are tied within tolerance);
- `ANISOTROPY_DECISIVE_FOR_NORMALIZED_ORDERING` if the `F(S_B)/F(S_E)` correction changes the normalized ordering relative to `M_mean`.

This is descriptive mechanism accounting, not an additional independent confirmation.

#### Prespecified R0 reference expectation

In the archived R0 result, the per-span correction factor relative to `1/bbar` is modest compared with the mean-denominator margin: `F(S_B)` ranges from approximately `1.0000` to `1.1810`, `F(S_E)` from approximately `1.0000` to `2.1795`, while `M_mean=tau_task/R_B` ranges from approximately `17.34` to `57.12` across the locked ladder. Thus R0's normalized ordering is not close to being reversed by the observed anisotropy correction.

Prospectively, this is an **expectation, not a gate**: if a new arm has a large mean-denominator margin and order-one `F(S_B)/F(S_E)`, the denominator mechanism remains sufficient for the ordering; if `M_mean` is near one and the anisotropy correction changes the ordering, `Delta_sel_B` contains mechanism information not reducible to `bbar` alone. The arm-specific quantities decide which case applies; no R0-derived magnitude threshold is imposed on new arms.

### 8.7 Selector and held-out identifiability diagnostics

At every reported `k`, also report:

1. held-out normalized local gap
   `gamma_k=(mu_k-mu_(k+1))/mu_k` for `k<rank`;
2. B-principal cosines / maximum angle / normalized projector distance between train `S_B` and held-out B-oracle top-k space, using the H1-0017 definition;
3. Euclidean principal cosines / maximum angle / normalized projector distance between `S_E` and Euclidean-orthonormalized `S_B`.

The `S_E`–`S_B` comparison is required to distinguish “no mechanism observed” from the trivial case in which both selectors choose nearly the same span.

Large principal angles are interpreted only in conjunction with local spectral gaps.

### 8.8 Exhaustive descriptive label map

Define fixed numerical sign tolerance

`eps_label = 1e-10` (absolute in efficiency-difference units)

and denominator equality tolerance

`eps_R = 1e-10`.

For `Delta_sel_B > eps_label`:

- if `Delta_sel_task > eps_label`: `NORMALIZED_AND_TASK_GAIN_SAME_DIRECTION`;
- if `|Delta_sel_task| <= eps_label`: `NORMALIZED_GAIN_WITH_TASK_TIE`;
- if `Delta_sel_task < -eps_label` and `R_B < 1-eps_R`: `DENOMINATOR_SELECTIVE_REVERSAL`;
- if `Delta_sel_task < -eps_label` and `|R_B-1| <= eps_R`: `NORMALIZED_GAIN_TASK_LOSS_EQUAL_MEAN_DENOMINATOR`;
- if `Delta_sel_task < -eps_label` and `R_B > 1+eps_R`: `NORMALIZED_GAIN_TASK_LOSS_WITHOUT_LOW_DENOMINATOR`.

For `Delta_sel_B <= eps_label`, use `NO_POSITIVE_NORMALIZED_SELECTION_GAIN`, while still reporting the sign of `Delta_sel_task` and `R_B` numerically.

The implementation must additionally emit exactly one category for each of the three axes:

- `B_SIGN in {POS,TIE,NEG}` with the `eps_label` boundary applied explicitly;
- `TASK_SIGN in {POS,TIE,NEG}`;
- `DEN_REL in {LOW,TIE,HIGH}` relative to one using `eps_R`.

Static QA must enumerate the Cartesian product, including exact zero/tie boundaries and values exactly at `±eps_label` / `1±eps_R`, and assert that exactly one primary label plus exactly one category on each axis is returned for every test point. This is a programmatic test, not a manual inspection.

This hierarchy is mechanically exhaustive for all sign/equality combinations. Raw numerical values are primary; labels are descriptive summaries only.

### 8.9 No bootstrap

A52 uses no image-level bootstrap and makes no population-level inferential claim. Point estimates, exact decomposition observables, numerical certification, and the prespecified cross-cell comparisons are primary.

---

## 9. Constructive positive calibration (`P1`) and end-to-end reduced calibration (`P1b`)

### 9.1 P1 analytic trace-ratio calibration

For each primary `k`, let `H=[h_1,...,h_k]` be AG1 task eigenvectors ranks `1..k` and `L=[l_1,...,l_k]` ranks `k+1..2k`. Fix `theta=pi/6`, `c=sqrt(3)/2`, `s=1/2`, and define

`Q_plus = c H + s L`

`Q_minus = -s H + c L`.

Both are Euclidean orthonormal and mutually orthogonal.

Define mean AG1 task energies

`t_plus=tr(Q_plus^T G_T^(1)Q_plus)/k`

`t_minus=tr(Q_minus^T G_T^(1)Q_minus)/k`

and `r_k=t_minus/t_plus`. The rotation guarantees `1/3 <= r_k <=1` for the nonnegative ordered task spectrum.

Set `gamma_k=r_k/10`, hence `1/30 <= gamma_k <=0.1`, and define a positive-definite synthetic denominator with mean response 1 on `Q_plus`, `gamma_k` on `Q_minus`, and 1 on the orthogonal complement.

For the calibration trace-ratio score `synth_score=t/dbar_D`, the ratio `synth_score(Q_minus)/synth_score(Q_plus)=10` exactly by construction while task response does not improve.

P1 hard gate, relative tolerance `1e-10`:

- Euclidean orthonormality / mutual orthogonality;
- `r_k in [1/3,1]`;
- denominator ratio `gamma_k=r_k/10`;
- synthetic normalized ratio = 10;
- emitted attribution `DENOMINATOR_DRIVEN_BY_CONSTRUCTION`.

### 9.2 P1b end-to-end reduced-pipeline calibration

P1 alone does not exercise the P2 generalized selector/scoring implementation. Therefore the pre-run package must include a deterministic synthetic reduced problem that is passed through the **same functions used by P2** for:

- Euclidean eigenselection;
- generalized eigenselection;
- Euclidean QR conversion of `S_B`;
- `B^{-1/2}` whitening;
- held-out task and B-normalized scoring;
- `bbar` / B-Gram diagnostics;
- descriptive labeler.

Construct per primary rank a diagonal/reduced `C_syn`, positive-definite `B_syn`, and `H_syn` with:

- `S_E` fixed to a higher-task block;
- `S_B` forced to a lower-task block by a smaller denominator;
- `Delta_sel_task < 0`;
- `Delta_sel_B > 0`;
- `R_B < 1`;
- expected label `DENOMINATOR_SELECTIVE_REVERSAL`.

The pre-lock synthetic problem is now frozen at reduced dimension 64. For `j=0,...,31`, define

`h_j = 2.64 - 0.01 j`, `l_j = 0.5 h_j`,

and set

`C_syn = H_syn = diag(h_0,...,h_31,l_0,...,l_31)`,

`B_syn = diag(1,...,1,0.1,...,0.1)` with 32 entries per block.

At every locked rank `k<=32` this construction has exact targets

- `eta_task(S_E)=1`, `eta_task(S_B)=0.5`;
- `eta_B(S_E)=0.2`, `eta_B(S_B)=1`;
- `Delta_sel_task=-0.5`, `Delta_sel_B=+0.8`;
- `R_B=0.1`, `tau_task=0.5`, `R_norm=5`;
- `F(S_E)=F(S_B)=1`;
- label `DENOMINATOR_SELECTIVE_REVERSAL`.

These spectra and targets are duplicated in the SHA-locked expected-invariants JSON. P1b is CPU/reduced algebra only and consumes no model outputs beyond deterministic dimensions.

Any P1b failure is `CALIBRATION_CONTROL_FAIL` and blocks new scientific P2 execution.

---

## 10. Constructive negative calibration (`P3`)

Using the same `Q_plus`, `Q_minus`, define a positive-definite anisotropic denominator `D_k^(-)` whose **mean** response is exactly equal on both spans but whose within-span eigenvalues are nonconstant.

For each primary even `k`, use eigenvalue multiset `{0.5,1.5}` repeated equally within each span, with the ordering permuted between `Q_plus` and `Q_minus`; use response 1 on the orthogonal complement. Thus

`dbar_D(Q_plus)=dbar_D(Q_minus)=1`

while the denominator is not the identity and the span-level B-Gram condition number equals 3.

The trace-ratio normalized-score ratio must equal `t_minus/t_plus`, and the labeler must emit no denominator-driven attribution.

P3 hard gate, relative tolerance `1e-10`:

- equal mean denominator ratio = 1;
- nontrivial anisotropy confirmed (`bgram_condition=3` within tolerance);
- normalized trace-score ratio = task ratio;
- no denominator-driven flag.

P3 is an algebraic false-positive control. It does not replace the real-data M5 internal negative control (`CONS640/U640` bbar ratios `1.032, 0.998, 0.958, 1.020`).

---

## 11. Numerical certification gates

P2 must retain the corrected H1-0017/A47 three-layer certification explicitly:

1. **Scientifically used top-32 self-scaled generalized residual**
   - train and held-out/oracle problems;
   - maximum over top 32 <=`1e-10`.
2. **All-spectrum normwise generalized backward error**
   - train and held-out/oracle problems;
   - maximum over all reduced eigenpairs <=`1e-10`.
3. **All-spectrum whitened symmetric-eigenproblem backward error**
   - train and held-out/oracle problems;
   - maximum over all reduced eigenpairs <=`1e-10`.

The original all-spectrum self-scaled generalized residual is **reported but is not a gate**.

Additional mandatory gates:

- all reduced matrices FP64;
- symmetry max abs <=`1e-10` after explicit checks;
- `lambda_min(B11)>0`;
- `alpha`, `lambda_min(B11)`, and `rho_ridge=alpha/lambda_min(B11)` reported per empirical arm;
- B condition number reported;
- B inverse-square-root reconstruction relative Frobenius error <=`1e-10`;
- generalized train and oracle B-orthonormality infinity error <=`1e-10`;
- Euclidean QR orthonormality and span-equivalence gates from §8.1;
- principal cosines <=`1+1e-10`;
- all efficiencies <=`1+1e-10`;
- R0-reproduction gate passes before any new scientific compute;
- P1/P1b/P3 calibration identities pass before P2 interpretation.

No arm is scientifically interpreted until certification passes.

---

## 12. Reporting and status

### 12.1 Per-arm/rank required output

For every reported rank store:

- checkpoint identity/SHA/configuration;
- exact split hashes;
- `k`;
- all four P2 2x2 efficiencies;
- both P2 matched contrasts;
- `task_num` for `S_E` and `S_B`;
- `B_num` for `S_E` and `S_B`;
- `U_task`, `U_B`, `C_cross_B`, `U_B_fraction`;
- `bbar(S_E)`, `bbar(S_B)`, `R_B`;
- B-Gram min/max/condition for each span;
- `alpha`, `lambda_min(B11)`, `lambda_max(B11)`, `rho_ridge`;
- `tau_task`, `R_norm`, `A_norm`, `M_mean=tau_task/R_B`, `1/R_B`, `F(S_E)`, `F(S_B)`, `A_over_mean_den`, and the mean-denominator-vs-anisotropy ordering label;
- `S_E`–`S_B` Euclidean principal-angle diagnostics;
- `S_B`–held-out-B-oracle B-principal-angle diagnostics;
- held-out `gamma_k`;
- P2 raw pattern and descriptive label;
- P1/P1b/P3 calibration outputs;
- all numerical certificates;
- prespecified prediction outcomes in machine-readable JSON, even when predictions are not gates.

### 12.2 No heterogeneous panel medians

No median is computed across `PV-A`, `PV-B1`, `PV-B2`, and `PV-C`, because the cases are deliberately nonexchangeable in architecture/input regime.

Report individual values and the prespecified ImageNet crossed comparison only. `PV-C` is reported separately as a stress case and must carry the explicit caption/footnote: **single checkpoint; no same-regime replicate; dataset, tokenization/input regime, sequence length, and positional dimension change together; a deviation cannot be separated from singleton checkpoint variation.**

### 12.3 Descriptive ImageNet cross-cell summary

At each primary rank report the four ImageNet cells (`R0`, `PV-A`, `PV-B1`, `PV-B2`) for:

- `Delta_sel_task`;
- `Delta_sel_B`;
- `log10(R_B)`;
- `M_mean`, `F(S_B)/F(S_E)`, and `R_norm`;
- `rho_ridge`;
- selector angle / projector distance;
- B-Gram condition.

The summary must be shown in **two evidential layers**:

1. **Full contextual 2x2**, including the discovery-conditioned `R0` anchor. R0-containing contrasts are visually marked `RETROSPECTIVE_ANCHOR_CONTEXT`.
2. **Prospective-only contrast panel**, containing only:
   - architecture at seed 123: `PV-A` vs `PV-B2`;
   - seed within ViT-S: `PV-B1` vs `PV-B2`.

These two prospective-only contrasts are the primary cross-cell portability evidence. No p-value, prevalence estimate, population statement, `X ± Y` architecture/seed effect, or within-cell variance estimate is permitted.

The design can support statements such as “the architecture contrast at the prospectively evaluated seed 123 had the same/opposite direction as the discovery-anchor context at seed 42” or “the ViT-S seed contrast was stable/changed across the two prespecified checkpoints.” It does **not** estimate a population architecture effect or seed variance.

### 12.4 Permitted wording

- If a mechanism pattern recurs in a cell: “The same denominator-driven selection pattern was observed in this prespecified case.”
- If it does not: “The original denominator-driven selection pattern did not recur in this prespecified case; the diagnostic reports the numerator/denominator behavior without treating absence as a technical failure.”
- If patterns differ by cell: “The natural numerator/denominator pattern was checkpoint-dependent across the prespecified cases.”
- For the crossed ImageNet design: “The fully prospective architecture contrast at seed 123 [did/did not] match the direction seen in the discovery-anchor context at seed 42,” and/or “the fully prospective ViT-S seed contrast was [direction].”

Do not use “general across models”, “replicated universally”, prevalence language, or an architecture/seed effect reported as `X ± Y`.

---

## 13. Success/status definitions

A52 has three separate status axes.

### 13.1 Implementation-equivalence status

`R0_REPRO_PASS` only if the archived H1-0017 result is reproduced under §7.

### 13.2 Calibration status

`CALIBRATION_PASS` only if P1, P1b, and P3 identities, expected labels, and numerical gates pass.

This means the implemented diagnostic/calibration arithmetic behaves as prespecified. It is **not** a general empirical validation claim.

### 13.3 Empirical portability completion status

Use only:

- `PORTABILITY_COMPLETE`;
- `PORTABILITY_PARTIAL_NON_EVALUABLE`;
- `TECHNICAL_FAIL`.

Scientific P2 outcomes are recorded as a case-wise pattern vector, not collapsed into `UNIFORM/MIXED/NOT_REPLICATED` pass/fail categories.

Other technical statuses:

- `NON_EVALUABLE_CONSTRUCTIVE_STABILITY_GATE`;
- `R0_REPRO_BOUNDARY_SENSITIVE`;
- `R0_REPRO_INCONCLUSIVE_BOUNDARY_SENSITIVITY`;
- `TECHNICAL_EQUIVALENCE_FAIL`;
- `CALIBRATION_CONTROL_FAIL`.

P2 outcome is never a reason to add cases or redesign selectors.

---

## 14. Stopping rule

`TSPG-RUN-PV-0001` ends after `PV-A`, `PV-B1`, `PV-B2`, and `PV-C` complete or are formally non-evaluable under locked gates.

After outcome access:

- no extra seed;
- no alternate ViT-S precision regime;
- no second CIFAR seed;
- no new PE family;
- no denominator-strength retuning;
- no rank-ladder change;
- no new selector;
- no AP access;
- no M1–M5 reopening.

Technical rerun only after a documented implementation-only correction preserving checkpoints, samples, metrics, controls, gates, and run ID.

---

## 15. Compute authorization proposed upon final lock

`R0-REPRO`, P1, P1b, and P3 consume no new model/GPU/gradient/G_A scientific compute.

Per new empirical arm only:

- checkpoint integrity/clean preflight;
- 256-image `C` attention-geometry calibration, accounted separately from task gradients;
- exactly 320 AG1 per-example task gradients;
- exactly 320 AG2 per-example task gradients;
- reduced/matrix-free G_A actions needed for AG1 task-support B, hard ceiling 320 support-basis actions;
- **fixed implementation-certification bundle:** four deterministic FP64 Rademacher directions generated with independent `PCG64` seeds `{2026090301,2026090302,2026090303,2026090304}`, Euclidean unit-normalized, evaluated on the first 8 locked `C` images under both the serial exact `G_A` action and the candidate block `G_A` action. This is exactly `4 x 2 = 8` certification direction-actions per new arm. Require every column finite, per-column relative L2 disagreement `<=1e-8`, and quadratic-form relative discrepancy `<=1e-8`;
- CPU/FP64 reduced algebra;
- no AP gradients;
- no finite-perturbation attack;
- no downstream subspace-dependent model-damage experiment.

Total new task gradients if all four new arms execute: **2560**.

Total planned attention-geometry calibration exposure: **4 × 256 = 1024 C-image evaluations** (not task gradients).

Total support-basis G_A action ceiling: **4 × 320 = 1280 support-basis actions**. The fixed certification bundle is **8 direction-actions per arm = 32 total certification direction-actions**, each using only the first 8 locked `C` images. It may not be enlarged after any scientific outcome.

Any overage requires a new amendment before execution.

---


## 15A. Final-lock trace estimator and corrected direction-action accounting

This section is frozen **before any new A52 model/GPU scientific outcome is accessed** and closes the final execution-specification gap in v1.4. Section 5 already fixed `tau=1e-4*trace(G_A)` but v1.4 did not spell out the scalable trace estimator or count its direction-actions. The final lock restores the already validated TSPG trace convention from A23.

For every new A52 arm, estimate `trace(G_A)` on the locked `C` cohort with deterministic FP64 Rademacher Hutchinson probes using the direct centered-attention JVP quadratic identity. Probe counts are adaptive and prespecified: `16 -> 32 -> 64`. Stop at the first count with relative standard error `RSE <= 0.02`; if the gate is not met at 64 probes, the arm receives `TRACE_ESTIMATION_GATE_FAIL` and no post-hoc probe extension, tau change, or ridge change is permitted.

All A52 arms are Learned PE, so the locked A23 Learned seed stream is reused: probe `j` uses `PCG64` seed `2026083200+j`, starting at `j=0`. Probe vectors are unnormalised Rademacher `{-1,+1}` directions, as required for an unbiased trace estimator. Report every probe quadratic, running trace estimate, sample SD, SE, RSE, selected probe count, `tau`, `alpha=tau/d_p`, and `rho_ridge=alpha/lambda_min(B11)`.

This trace stage is separate from the four-direction implementation-certification bundle. Per arm the maximum geometry direction-action budget is therefore:

- support-basis `G_A` actions: `<=320`;
- trace quadratic JVP actions: `<=64`;
- implementation certification: `8` direction-actions (4 serial + the same 4 candidate-block);
- **maximum total: `392` direction-actions per arm, `1568` across four arms**.

The phrase `4 x 256 calibration image evaluations` from the draft accounting is retired as a pass-count claim. The correct invariant is `4 x 256 = 1024` **unique arm-image memberships** in the locked `C` cohorts; trace, support-basis and certification operators revisit those fixed images as required by their direction-actions. No additional calibration images are selected.

This refinement changes neither the scientific estimand, checkpoint panel, split, P1/P1b/P2/P3 definitions, label map, nor any scientific outcome gate. It only fixes the trace implementation and makes compute accounting complete before execution.

---
## 16. Required pre-run artifacts

A52 v1.4 introduced a **zero-compute host preflight** that could inspect files, dataset labels, and archived reduced matrices, and could run CPU reduced algebra, but could not instantiate/run a model, compute a task gradient, or perform any new scientific `G_A` action. That preflight is now complete and formally ingested as `PASS_ZERO_COMPUTE_PRELOCK_EVIDENCE_INGESTED`; `R0-REPRO`, P1b, label-partition QA, constructive-stability QA, ImageNet split provenance, and the deterministic CIFAR manifest have passed before this lock.

The following required artifacts are now created and SHA-locked in the execution starter:

1. checkpoint manifest JSON/CSV including `R0`, `PV-A`, `PV-B1`, `PV-B2`, `PV-C` and exact config fields/SHA-256;
2. ImageNet split-provenance record including source dataset and `C/AG1/AG2` hashes;
3. CIFAR split manifest JSON/CSV;
4. run config JSON including §6 numerical-rank/stability rules, `eps_label`, `eps_R`, `eps_gap_repro`, the frozen 8-action-per-arm G_A implementation-certification bundle, and no-bootstrap decision;
5. exact H1-0017 P2 metric schema plus P1/P1b/P3 definitions;
6. expected-invariants JSON including exact R0 reproduction targets, `rho_ridge` anchor, R0 amplification-accounting reference values, constructive spectral-floor rule, and synthetic-control spectra/labels;
7. run card and visible-progress notebook/runbook;
8. static QA including an executable exhaustive label-partition test over sign/tie boundaries and a constructive-stability gate test;
9. SHA-256 manifest covering code/config/manifests;
10. artifact-registry entries and number-level provenance mappings;
11. provenance chain recording `H1-0017 development result -> A51 M3 lock -> headline reporting use`;
12. machine-readable predictions-not-gates schema with outcome fields.

Scientific execution is authorized **only** through the SHA-locked execution starter and only after its first-execution checkpoint/host hard gate passes. A failed host gate leaves all scientific arm cells blocked.

---

## 17. Required post-run artifacts

At minimum:

- per-arm raw/reduced result JSON;
- P2 2x2 CSV;
- P1/P1b/P3 calibration CSV/JSON;
- R0 reproduction report;
- numerical-certification JSON;
- checkpoint/split/runtime provenance JSON;
- ImageNet crossed-design summary CSV;
- PV-C stress-case summary;
- claim/evidence audit;
- ingest audit;
- formal closeout;
- updated artifact registry + SHA manifest;
- bidirectional number-level provenance map.

---

## 18. Reporting-use lock

A52 may support only:

1. P1/P1b/P3 calibrate the attribution implementation under deliberately constructed controls;
2. P2 reports actual-B numerator/denominator behavior in the prespecified independent cases;
3. the ImageNet 2x2 display is contextually useful, but only `PV-A` vs `PV-B2` and `PV-B1` vs `PV-B2` are fully prospective cross-cell contrasts; R0-containing contrasts are discovery-anchor context;
4. the crossed design supports case-wise contrast replication/directional comparison, not architecture/seed effect variance estimation;
5. PV-C is a singleton dataset/input-regime stress case with no same-regime replicate;
6. original M1–M5 conclusions remain unchanged.

A52 may not support:

- prevalence across neural networks;
- universal denominator-driven selection;
- a claim that calibration controls prove empirical portability;
- universal spectral non-identifiability beyond Proposition 1's stated ratio-form setting;
- repair of H1-0019;
- a causal claim that PV-C isolates dataset alone;
- PE-family portability;
- a population theorem about ViTs;
- counting correlated P2 observables as independent convergent confirmations.

---

## 19. Activation closeout

Current state: `LOCKED — TSPG-RUN-PV-0001 AUTHORIZED SUBJECT TO FIRST-EXECUTION HOST HARD GATE`.

The activation conditions are closed as follows:

1. author-approved checkpoint/control/split design: **CLOSED**;
2. independent-review blockers B1–B4 and static-QA requirements: **CLOSED**;
3. A52 v1.5 marked `LOCKED`: **CLOSED**;
4. successor Protocol Lock v0.52 names `TSPG-RUN-PV-0001` as the sole authorized scientific run: **CLOSED**;
5. §16 pre-run artifacts generated, audited, and SHA-locked: **CLOSED**;
6. `R0-REPRO`, P1b, 125/125 label-partition QA, and 5/5 constructive-stability QA passed before new model/GPU scientific compute: **CLOSED**;
7. execution may begin only after the starter's checkpoint byte/config/state-dict host gate passes.

No scientific outcome has been used to modify this lock.
