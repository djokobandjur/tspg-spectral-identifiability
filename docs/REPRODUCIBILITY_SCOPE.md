# Public reproducibility scope

This repository is the public reproducibility surface for the TSPG spectral-identifiability study.

## Included

The first archival release is intended to contain only the artifacts needed to reproduce or audit the reported manuscript results:

- analysis/operator code used by the reported runs;
- locked configurations and protocol-facing manifests;
- dataset split/index manifests that do not redistribute restricted source images;
- compact machine-readable result files;
- numerical-certification and reproducibility audits;
- software/environment information;
- a release manifest with SHA-256 hashes and file-to-result mapping.

## Not included by default

The public repository is not a mirror of the internal development workspace. It will not publish, unless scientifically required:

- superseded intermediate artifacts;
- failed implementation-only attempts that produced no scientific evidence;
- private/internal manuscript-governance records;
- unrelated project files;
- restricted ImageNet source images;
- large model/data artifacts whose redistribution rights are not established.

Where a large or restricted artifact cannot be hosted directly, the release documentation will provide its exact identifier/hash and reconstruction or acquisition instructions.

## Provenance principle

Public artifacts are promoted from the internal evidence chain only after consistency checks. The intended trace is:

`manuscript result -> compact result artifact -> run/config -> code -> split/checkpoint manifest -> SHA-256 provenance`.

The GitHub release and corresponding Zenodo archive will be versioned together so that a manuscript citation points to an immutable reproducibility snapshot.
