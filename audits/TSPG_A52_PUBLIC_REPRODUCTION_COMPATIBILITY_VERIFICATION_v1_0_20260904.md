# A52 public reproduction compatibility verification

Date: 2026-09-04

Status: **PASS_PUBLIC_SCIENTIFIC_SEMANTICS_UNCHANGED**

Scientific compute: **NONE**

## Byte anchors

- exact private pre-execution A52 v1.5 lock SHA-256: `2fc2c8dbeca0ce0affe17055e7ba6e7a7ffd8c7b9ba7488c15bfcf7e32a89aeb`
- public scientific semantic copy SHA-256: `17772715e87052ed8d39c8837dbed98a1ff65f0b4a09f1cb8c1a700f4521f36e`

## Verification

A line-level unified diff was performed between the exact private v1.5 lock and the public scientific semantic copy.

The diff contains only:
1. a public provenance preamble recording the exact private-lock SHA;
2. removal/replacement of publication-process-only wording (manuscript title/submission/editor/reviewer references);
3. genericization of the parent-lock filename while retaining the parent scientific-lock relation;
4. terminology changes from manuscript-specific to reporting/number-level language.

No scientific arm definition, checkpoint identity, seed, architecture, dataset, rank ladder, estimand, contrast, numerical gate, stopping rule, sign rule, singleton caveat, drift prohibition, or execution authorization changed.

Changed-line accounting from the exact unified diff: `16` removed lines and `21` added lines, including blank/separator lines and the public preamble.

The public compatibility overlay is therefore suitable for release and does not alter any scientific field of the locked A52 protocol.
