# Results

This directory is the compact machine-readable public result layer.

The original v1.0.0 M1--M5 results remain unchanged. v1.1.0 adds:

- H1-0012 original and zero-compute reporting-upgrade JSONs plus the exact top-1 trajectory CSV;
- the archived H1-0007 ALiBi dense-control result and deterministic structural-reanalysis JSON;
- four exact A52 arm result JSONs;
- A52 primary-row, crossed-ImageNet, PV-C, conditioning, and panel-summary views.

The result layer is intentionally compact. Authoritative runtime evidence archives and raw/reduced matrices are versioned as GitHub Release/Zenodo assets and identified by SHA-256 in `../manifests/`.

For M4, the corrected public T/U/orientation decomposition remains the reporting source; the superseded summary CSV with the sample-size labeling collision is not reintroduced.
