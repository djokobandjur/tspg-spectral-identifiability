# TSPG public release v1.1.0 preparation

This branch prepares the next public reproducibility-package version. The existing `v1.0.0` GitHub/Zenodo release remains immutable and continues to identify the original M1--M5 package.

The v1.1.0 candidate extends the public evidence boundary with three already-closed components: H1-0012 direction-level numerator/denominator decomposition, the pre-existing H1-0007 ALiBi exact dense structural control, and the A52 diagnostic-portability panel.

No manuscript PDF/TEX, submission material, non-scientific publication correspondence, or internal manuscript-governance documents are part of this public branch.

## Closed staging gates

- recursive-clean public candidate: PASS;
- A52 public scientific semantic copy vs exact private v1.5 lock: PASS, scientific fields unchanged;
- four A52 checkpoints: `4/4 PASS`, aggregate `858,245,348` bytes;
- eight supplemental evidence objects: exact identities locked;
- complete new Zenodo payload: 12 objects, aggregate `871,089,498` bytes;
- local Zenodo source -> copy verification: `12/12 PASS`.

The exact local Zenodo staging manifest SHA-256 is `ca942f8bf369c377ac5067b8e72f886a3cc1aa08f443880b6c0813c116b9c52b`; the corresponding SHA list SHA-256 is `472095d86616fc59b0aa4748cae8839dbeca1b281f38f11154f20f738573cfa5`.

## Remaining release gates

1. promote and verify the exact public candidate Git tree;
2. reserve the Zenodo v1.1.0 DOI;
3. update DOI-bearing metadata (`CITATION.cff` and release docs only);
4. freeze/tag GitHub `v1.1.0`;
5. publish the exact 12-object Zenodo payload;
6. independently download and SHA-verify all new archival objects;
7. insert verified release links into manuscript v0.34 and run final freeze QA.

The current public version DOI is `10.5281/zenodo.22180107`; the stable all-versions DOI is `10.5281/zenodo.22180106`.
