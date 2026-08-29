# Results

This directory contains the compact machine-readable public result layer for the reported M1--M5 findings.

`core_findings_v0_1.json` is the manuscript-level numerical index across all five findings. Exact primary-run result identities are bound to their authoritative runtime bytes by `../manifests/RUN_RESULTS_SHA256.txt`, and the corresponding compact evidence archives are bound by `../manifests/EVIDENCE_ARCHIVES_SHA256.txt`.

Currently promoted exact/diagnostic artifacts include the H1-0015 and H1-0017 primary result JSONs, the H1-0016 pre-compute gate and final static QA, H1-0017--H1-0019 static-QA outputs, the corrected H1-0018 primary T/U/eta decomposition, and the H1-0019 pre-AP fit-lock gate. Together with the compact M1--M5 index and the public audit records, these expose the numerical checks needed to interpret the reported findings without placing large raw arrays in Git.

The original `TSPG_H1_0018_SUMMARY_CURVES_v1_0_20260829.csv` is intentionally **not** promoted: its sample-size column was a derived labeling error and the artifact is superseded. The corrected public H1-0018 T/U/eta decomposition is used instead; the authoritative H1-0018 result JSON remains SHA-bound inside its evidence archive.

Large `.npy`/`.npz` artifacts and the source ImageNet images are not stored in Git. Their SHA-256 identities and roles are recorded under `../manifests/`, and the immutable archival release will provide the versioned evidence package and reconstruction/acquisition instructions where appropriate.
