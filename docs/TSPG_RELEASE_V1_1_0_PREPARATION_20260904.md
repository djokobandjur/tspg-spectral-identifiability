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
- local Zenodo source -> copy verification: `12/12 PASS`;
- exact public-tree promotion: PASS at commit `a84740dabd4eb50f13e413624f8f586082ecee6a`, Git tree `1b98538c4f7c3cb93fe20dc58d4cd7c30d8f87a2`;
- Zenodo v1.1.0 DOI reservation: `10.5281/zenodo.22308245`;
- DOI-bearing v1.1.0 metadata update: PASS;
- canonical tracked-file SHA-256 freeze: PASS via `manifests/TSPG_GIT_TRACKED_FILES_SHA256_v1_1_0_20260904.txt` (manifest self-excluded by construction; final Git commit/tree binds the manifest itself).

The exact local Zenodo staging manifest SHA-256 is `ca942f8bf369c377ac5067b8e72f886a3cc1aa08f443880b6c0813c116b9c52b`; the corresponding SHA list SHA-256 is `472095d86616fc59b0aa4748cae8839dbeca1b281f38f11154f20f738573cfa5`.

## Remaining release gates

1. create/tag GitHub release `v1.1.0` at the frozen release-manifest commit;
2. publish the exact 12-object Zenodo payload;
3. independently download and SHA-verify all new archival objects;
4. insert verified release links into manuscript v0.34 and run final freeze QA.

The v1.0.0 public version DOI is `10.5281/zenodo.22180107`; the reserved v1.1.0 version DOI is `10.5281/zenodo.22308245`; the stable all-versions DOI is `10.5281/zenodo.22180106`.
