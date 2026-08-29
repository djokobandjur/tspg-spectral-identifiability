# TSPG RUN CARD — H1-0015 v1.1

**Run ID:** `TSPG-RUN-H1-0015`
**Status:** `AUTHORIZED_DEVELOPMENT_ONLY`

Unchanged compute budget:
maximum 32 new G_A TAIL directions.

Mandatory endpoint spectra:
1. BASELINE_L0 — Q only, uncontaminated reference;
2. HEAD — original top4-targeted L=4;
3. TAIL — matched ranks5--8 L=4;
4. COMBINED — HEAD+TAIL union.

Retain lambda1...lambda12 and k=4 boundary for all four.

Primary fairness question:
does the COMBINED k=4 boundary survive after ranks5--8 receive equal targeted
complement budget?

Claim lock:
- original HEAD L>=1 gap is target-conditioned;
- spectral gap is not the primary C1/H1 concentration statistic;
- k=4 is not reselected from seed42.

No random-range(R) branch is authorized in this run.
