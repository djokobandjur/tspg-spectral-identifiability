# Zenodo post-publication remote SHA-256 verification

**Audit date:** 2026-08-31  
**Release:** `v1.0.0`  
**Zenodo record ID:** `22180107`  
**Zenodo version DOI:** `10.5281/zenodo.22180107`  
**Release version:** `1.0.0`  
**Status:** `PASS_REMOTE_SHA256_14_OF_14`

## Scope and verification boundary

This audit closes the final public archive-integrity gate for the DOI-bearing Zenodo payload. The published Zenodo record was queried from an independent internet-connected Windows host, each of the 14 published objects was downloaded from its public Zenodo content endpoint, and the downloaded bytes were compared against the locked release identities.

The operator-supplied PowerShell verification transcript used for this closeout is 13,651 bytes with SHA-256 `43832d6ca402d8aa19988f3b21c8fb1581679e2860c3ffaa5db592043ccaf8d6`. The transcript records both the Zenodo-advertised MD5 values and independently computed MD5/SHA-256 values over the downloaded bytes. Temporary downloaded objects were removed after hashing.

## Metadata and file-set gate

The public Zenodo API returned:

- record ID `22180107`;
- DOI `10.5281/zenodo.22180107`;
- version `1.0.0`;
- exactly 14 files;
- exact expected filename set;
- exact expected per-file sizes;
- aggregate payload size `3,535,908,885` bytes.

All metadata and file-set checks passed before the byte-level download verification proceeded.

## Exact remote-byte verification

| Published object | Bytes | Expected / downloaded SHA-256 | Zenodo MD5 / downloaded MD5 | Result |
|---|---:|---|---|---|
| `TSPG_LEARNED_SEED42_best_model.pth` | 343559209 | `7fcca75916c2d6f0f64aa5c381812ad3a305ba1a04672e9288f4251ab683c536` | `9d3cdc4fbfcc3017687f0cc770331990` | PASS |
| `TSPG_H1_0015_RUNTIME_EVIDENCE_v1_1_20260828.zip` | 24682 | `8125067b17eee2abe61bf9a3519366d371b2c751e7a481a87b3de0c32ce11c71` | `24086717623e07fa7c228430bc967672` | PASS |
| `TSPG_H1_0016_RUNTIME_EVIDENCE_v1_2_20260829.zip` | 144501 | `0d7c6acfe8e38826fbb36322f30f187f9442d4ea42253e9463328d004062e022` | `324b13e35f384c851657b4e583668d92` | PASS |
| `TSPG_H1_0017_RUNTIME_EVIDENCE_v1_1_20260829.zip` | 2522591 | `5fff014e258c2bac92cc61f13ea559ba6cae67b41487d35141f4e00306ee1ae4` | `b8fc41bc3c60503ff6cbcf8f96feaf10` | PASS |
| `TSPG_H1_0018_RUNTIME_EVIDENCE_v1_0_20260829.zip` | 2936547 | `2ab57eeb8c27f229f37ceec1233033cf6c3061dce8943d526cf597f2ede7e567` | `5948a2d111bb5d704796012d6d1d8c06` | PASS |
| `TSPG_H1_0019_RUNTIME_EVIDENCE_v1_0_20260829.zip` | 4072637 | `f9eaadb43d0054a7d90714f2305b3e34fe3d47eaa34513659e4aed5ab09e62da` | `8d6ae565187d78e8eba5fd4756f2b0ea` | PASS |
| `TSPG_H1_0007_LEARNED_SEED42_AG1_320_FP64_TASK_GRADIENTS_v1_0.npy` | 387317888 | `d02d8a31465912e7239164e965428162fa5f64f09082d5d0a158f6585b439009` | `b844e0c3ceca5bb04cc664817b15584b` | PASS |
| `TSPG_H1_0010_LEARNED_SEED42_QR_TASK320_EXACT_GEOMETRY_v1_1.npz` | 776283320 | `08f23a6c0d87a58ed49c9f4bda841105f7d45eb848d18f30aa498eb42fb31074` | `f5e7ae3c8c193090c46bfce4d85513cc` | PASS |
| `TSPG_H1_0011_LEARNED_SEED42_COMPLEMENT_KRYLOV_BASIS_v1_0.npz` | 79126618 | `4f948e96ec8c8ae911259f923b876864b6ffd83b1cf54669d7fdd00b90b88237` | `2a821fabfeca91c7d43c33fdf2d93a38` | PASS |
| `TSPG_H1_0015_LEARNED_SEED42_TAIL_RANK5_8_COMPLEMENT_KRYLOV_L4_v1_0.npz` | 232412532 | `7d78e8584d265ff3a041ce84055720106a1fa49a09e7acc31be38482208e2279` | `487466552e1a3e7fc5fc23f231ff7f12` | PASS |
| `TSPG_H1_0016_LEARNED_SEED42_AG2_320_FP64_TASK_GRADIENTS_v1_2.npy` | 387317888 | `2850c66d13dc45f48baa114f540e29c3ca75903db412ac8f93c048fdb8b930eb` | `cc83075704c28e13d478e8cf648d8809` | PASS |
| `TSPG_H1_0016_LEARNED_SEED42_AG1_AG2_TASK_CROSSFOLD_DERIVED_v1_2.npz` | 390626716 | `afe9a94d1c5c7f7f3d8986348b15c7513013c77969781d54d03c0f8154b4baea` | `d7ce4fc806c81afe2cdfd370f617cdeb` | PASS |
| `TSPG_H1_0019_LEARNED_SEED42_AP640_FP64_TASK_GRADIENTS_v1_0.npy` | 774635648 | `0398ec1949f7d5ad326902f438c554848b86325d352d73a67078473f7fba3145` | `db3ab590f011792b1c81a7fdda072496` | PASS |
| `TSPG_H1_0019_FIT_ARM_BASES_TOP32_v1_0.npz` | 154928108 | `8bfc5c8e4bc7c677a882974a61b4e66d540f230dbb75b690ffbfe42ea47fa4e3` | `55089d795be5bb359e4ed0576eb2a6a7` | PASS |

For every row, the downloaded byte count equaled the locked expected size, the independently computed SHA-256 equaled the locked release SHA-256, and the independently computed MD5 equaled the checksum exposed by the public Zenodo record.

## Aggregate result

The final PowerShell summary reported:

- remote files: `14`;
- exact SHA-256 pass: `14/14`;
- expected total bytes: `3,535,908,885`;
- downloaded total bytes: `3,535,908,885`;
- final gate: `PASS_REMOTE_SHA256_14_OF_14`.

This closes the post-publication Zenodo integrity gate. Together with the independently verified GitHub release gate (`6/6` planned convenience assets exact size + SHA-256 PASS), the public `v1.0.0` release payload is byte-verified on both distribution surfaces.