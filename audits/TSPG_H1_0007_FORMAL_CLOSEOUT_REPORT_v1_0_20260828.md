# TSPG H1-0007 FORMAL CLOSEOUT REPORT

**Run:** `TSPG-RUN-H1-0007`  
**Formal status:** `CLOSED_TECHNICAL_NUMERICAL_NONCONVERGENCE`  
**Scientific H1:** `NOT_EVALUATED`

Runtime evidence SHA-256: `0fd3fc803b4cedb24f5cfeae2a5c624b56bf078ea0d7032b08594cb8c7f60f6c`. ZIP integrity PASS; internal SHA
manifest 14/14 PASS.

## Learned exact block geometry oracle

FP64 `vmap` block `G_A V` passed against the serial exact operator:
relative-L2 max `4.628e-16`, quadratic discrepancy
`1.719e-16`, observed speedup
`4.742x`.

## ALiBi exact dense diagnostic control

The 12D ALiBi control passed at machine precision. Top-4 attention fractions
are `[0.9999208849857297, 0.9998938818976985, 0.9999109312732071, 0.9999054156050659]` and ridge fractions are
`[7.911501427026964e-05, 0.00010611810230150748, 8.906872679289083e-05, 9.458439493411822e-05]`. This is a development
diagnostic, not cross-family inference.

## Learned exact B-solve pilot

Rank32 ended after 128 PCG iterations with independent true relative residual
`2.14340805409`. Rank64 ended after 128 iterations
with `1.38757508808`. Both fail the unchanged
`1e-8` gate. Rank64 improves the terminal true residual by
`35.3%`,
but remains `1.388e+08` times above the
gate.

The precommitted dual/range stage was therefore correctly not entered.

## Closeout interpretation

H1-0007 does not yield a converged Learned generalized eigenpair, so no
Learned ridge fraction or full-space generalized eigenvalue is interpreted.

Before any rank128 attempt, `c` change, or geometry-support restriction, the
next run will directly measure the existing Learned geometry sketch and the
location of dominant task directions within that geometry.
