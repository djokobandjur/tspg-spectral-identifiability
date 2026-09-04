# Archival release checklist

## v1.0.0 — CLOSED

GitHub release `v1.0.0` and Zenodo version DOI `10.5281/zenodo.22180107` are public. The complete Zenodo payload and GitHub release assets were independently retrieved and SHA-verified. The all-versions DOI is `10.5281/zenodo.22180106`.

## v1.1.0 — evidence expansion

- [x] Preserve v1.0.0 as immutable historical release.
- [x] Create dedicated branch `release/v1.1.0-alibi-a52` from current `main`.
- [x] Assemble and SHA-verify a local public-safe candidate set for H1-0012, H1-0007 ALiBi, and A52.
- [x] Assemble and SHA-verify the eight supplemental evidence objects for the new release boundary.
- [x] Exclude manuscript PDF/TEX, submission files, editor/reviewer material, and internal manuscript-governance artifacts from the public candidate.
- [ ] Promote the remaining candidate public-safe code/config/result/audit/manifest files into the release branch and verify the branch tree.
- [x] Obtain/stage the four exact A52 checkpoint binaries and verify source -> staged-copy SHA-256 identity (`4/4 PASS`; aggregate `858,245,348` bytes).
- [x] Lock A52 checkpoint distribution policy: the four checkpoint binaries are Zenodo v1.1.0 archival payloads; GitHub Release duplication is not required because the public tree exposes their exact SHA identities and the DOI acquisition route.
- [ ] Lock distribution of the eight small supplemental evidence objects (GitHub Release convenience assets, Zenodo, or both); preserve exact identities from `manifests/TSPG_RELEASE_ASSET_PLAN_v1_1_0_20260904.json`.
- [ ] Reserve the Zenodo new-version DOI for `1.1.0`; update `CITATION.cff` only after the DOI exists.
- [ ] Freeze the v1.1.0 Git content tree; generate and verify the full tracked-file SHA-256 manifest.
- [ ] Create/tag GitHub release `v1.1.0` at the frozen release-manifest commit.
- [ ] Upload/publish the v1.1.0 Zenodo payload under the all-versions DOI lineage.
- [ ] Independently download every new GitHub/Zenodo asset and verify byte count + SHA-256.
- [ ] Replace manuscript release placeholders with the final v1.1.0 DOI/public URL, then run manuscript v0.34 final-freeze QA.
