# TSPG Zenodo v1.1.0 upload-staging verification

Date: 2026-09-04

Status: **PASS_12_OF_12_SOURCE_TO_COPY_VERIFIED**

Scientific compute: **NONE**

The prepared Zenodo v1.1.0 staging directory contains exactly 12 archival objects: eight supplemental evidence objects and four A52 checkpoint binaries. The staging workflow re-verified each source object's expected byte count and SHA-256, copied the object into the upload directory, and re-verified the copied bytes.

- object count: `12`
- supplemental evidence objects: `8`
- checkpoint binaries: `4`
- aggregate payload bytes: `871,089,498`
- source/copy verification status: `12/12 PASS`
- staging manifest SHA-256: `ca942f8bf369c377ac5067b8e72f886a3cc1aa08f443880b6c0813c116b9c52b`
- SHA list SHA-256: `472095d86616fc59b0aa4748cae8839dbeca1b281f38f11154f20f738573cfa5`

The 12 filename/SHA pairs in `SHA256SUMS_ZENODO_V1_1_0_UPLOAD.txt` match the 12 records in `TSPG_ZENODO_V1_1_0_UPLOAD_STAGING_MANIFEST_v1_0_20260904.json` exactly; there are no missing, extra, or mismatched entries. The sum of the per-record byte counts equals the manifest aggregate (`871,089,498`).

This verification closes the local byte-staging gate only. Zenodo publication remains open until the new version DOI is reserved, the exact payload is uploaded/published, and every published object is independently downloaded and SHA-verified.
