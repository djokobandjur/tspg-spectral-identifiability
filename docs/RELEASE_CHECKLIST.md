# Archival release checklist

## v1.0.0 — CLOSED

GitHub release `v1.0.0` and Zenodo version DOI `10.5281/zenodo.22180107` are public. The complete Zenodo payload and GitHub release assets were independently retrieved and SHA-verified. The all-versions DOI is `10.5281/zenodo.22180106`.

## v1.1.0 — evidence expansion

- [x] Preserve v1.0.0 as immutable historical release.
- [x] Create dedicated branch `release/v1.1.0-alibi-a52` from current `main`.
- [x] Assemble and SHA-verify the recursive-clean public-safe candidate for H1-0012, H1-0007 ALiBi, and A52.
- [x] Exclude manuscript/submission/non-scientific publication correspondence and internal manuscript-governance artifacts from the public candidate.
- [x] Verify the public A52 scientific semantic copy against the exact private v1.5 lock; scientific fields unchanged.
- [x] Obtain/stage the four exact A52 checkpoint binaries and verify source -> staged-copy SHA-256 identity (`4/4 PASS`; aggregate `858,245,348` bytes).
- [x] Lock A52 checkpoint distribution policy: four checkpoint binaries are Zenodo v1.1.0 archival payloads; GitHub Release duplication is not required.
- [x] Lock distribution of the eight small supplemental evidence objects to both GitHub Release and Zenodo.
- [x] Lock the exact 12-object new Zenodo v1.1.0 payload identity set: eight supplemental evidence objects + four A52 checkpoints, aggregate `871,089,498` bytes.
- [x] Build the local Zenodo v1.1.0 upload staging directory and verify source -> copy identity for all 12 objects (`12/12 PASS`).
- [ ] Promote the exact remaining public-safe candidate tree into the release branch and verify the branch tree.
- [ ] Reserve the Zenodo new-version DOI for `1.1.0`; update `CITATION.cff` only after the DOI exists.
- [ ] Freeze the v1.1.0 Git content tree; generate and verify the full tracked-file SHA-256 manifest.
- [ ] Create/tag GitHub release `v1.1.0` at the frozen release-manifest commit.
- [ ] Upload/publish the exact v1.1.0 Zenodo payload under the all-versions DOI lineage.
- [ ] Independently download every new GitHub/Zenodo asset and verify byte count + SHA-256.
- [ ] Replace manuscript release placeholders with the final v1.1.0 DOI/public URL, then run manuscript v0.34 final-freeze QA.
