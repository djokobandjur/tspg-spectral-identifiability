#!/usr/bin/env python3
"""Prepare a portable TSPG M1--M5 runtime root without editing locked configs.

This utility creates *derived runtime copies* of the public locked configs.  It
changes only host-local routing fields (paths, cache roots, and the compatibility
manifest identities that necessarily change when paths are made portable).
Scientific parameters are intentionally left untouched.

The tool is fail-closed in materialization mode: every external artifact that it
stages is SHA-256 verified against the public dependency manifest.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any, Iterable

MODEL_SOURCE_SHA256 = "83fc337128dec7f896c9816842806789a634154dea8372bb0a43bae19188d3bf"
CHECKPOINT_SHA256 = "7fcca75916c2d6f0f64aa5c381812ad3a305ba1a04672e9288f4251ab683c536"
CHECKPOINT_SIZE = 343_559_209
PUBLIC_SPLIT = "TSPG_USED_ANALYSIS_SPLIT_INDICES_PUBLIC_v1_0_20260829.json"
RUNTIME_SPLIT = "TSPG_RUNTIME_SPLIT_INDICES_PUBLIC_v1_0_20260829.json"
RUNTIME_CHECKPOINT_MANIFEST = "TSPG_RUNTIME_LEARNED_SEED42_CHECKPOINT_COMPAT_v1_0_20260829.json"
DEPENDENCY_MANIFEST = "TSPG_PORTABLE_RUNTIME_DEPENDENCIES_v1_0_20260829.json"

RUNS = {
    "M1": {
        "config": "TSPG_H1_0015_CONFIG_v1_1_20260828.json",
        "runner": "TSPG_run_h1_0015_matched_rank_boundary_complement_fairness_v1_1_20260828.py",
    },
    "M2": {
        "config": "TSPG_H1_0016_CONFIG_v1_2_20260829.json",
        "runner": "TSPG_run_h1_0016_task_side_crossfold_preflight_v1_2_20260829.py",
    },
    "M3": {
        "config": "TSPG_H1_0017_CONFIG_v1_1_20260829.json",
        "runner": "TSPG_run_h1_0017_offline_b_normalized_crossfit_v1_1_20260829.py",
    },
    "M4": {
        "config": "TSPG_H1_0018_CONFIG_v1_0_20260829.json",
        "runner": "TSPG_run_h1_0018_finite_sample_stability_v1_0_20260829.py",
    },
    "M5": {
        "config": "TSPG_H1_0019_CONFIG_v1_0_20260829.json",
        "runner": "TSPG_run_h1_0019_last_estimator_v1_0_20260829.py",
    },
}


def sha256_file(path: Path, block_size: int = 8 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b = f.read(block_size)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def json_bytes(obj: Any) -> bytes:
    return (json.dumps(obj, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(json_bytes(obj))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def verify(path: Path, expected_sha: str, *, expected_size: int | None = None) -> None:
    if not path.is_file():
        raise FileNotFoundError(path)
    if expected_size is not None and path.stat().st_size != expected_size:
        raise RuntimeError(
            f"size mismatch for {path}: {path.stat().st_size} != {expected_size}"
        )
    got = sha256_file(path)
    if got != expected_sha:
        raise RuntimeError(f"SHA-256 mismatch for {path}: {got} != {expected_sha}")


def relative_or_absolute(path: Path) -> str:
    return str(path.resolve())


def enumerate_imagefolder(val_dir: Path) -> tuple[int, int]:
    if not val_dir.is_dir():
        raise FileNotFoundError(val_dir)
    classes = sorted(p for p in val_dir.iterdir() if p.is_dir())
    images = 0
    allowed = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".JPEG", ".JPG"}
    for c in classes:
        images += sum(1 for p in c.rglob("*") if p.is_file() and p.suffix in allowed)
    return len(classes), images


def unique_candidate(filename: str, roots: Iterable[Path], expected_sha: str) -> Path | None:
    matches: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        for p in root.rglob(filename):
            if p.is_file() and sha256_file(p) == expected_sha:
                matches.append(p.resolve())
    unique = sorted(set(matches))
    if not unique:
        return None
    # Multiple byte-identical copies are harmless; select deterministically.
    return unique[0]


def stage_file(src: Path, dst: Path, mode: str) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() or dst.is_symlink():
        dst.unlink()
    if mode == "copy":
        shutil.copy2(src, dst)
    else:
        dst.symlink_to(src.resolve())


def set_change(changes: list[dict[str, Any]], cfg: dict[str, Any], path: list[str], value: Any) -> None:
    cur: Any = cfg
    for key in path[:-1]:
        cur = cur[key]
    leaf = path[-1]
    old = cur.get(leaf) if isinstance(cur, dict) else None
    if old != value:
        cur[leaf] = value
        changes.append({"json_path": ".".join(path), "old": old, "new": value})


def patch_environment(cfg: dict[str, Any], cache_root: Path, changes: list[dict[str, Any]]) -> None:
    env = cfg.get("environment_required")
    if not isinstance(env, dict):
        return
    current_user = os.environ.get("USER") or os.environ.get("LOGNAME") or "tspg"
    current_home = str(Path.home())
    replacements = {
        "USER": current_user,
        "LOGNAME": current_user,
        "HOME": current_home,
        "TORCHINDUCTOR_CACHE_DIR": str((cache_root / "torchinductor").resolve()),
        "TRITON_CACHE_DIR": str((cache_root / "triton").resolve()),
        "XDG_CACHE_HOME": str((cache_root / "xdg").resolve()),
        "MPLCONFIGDIR": str((cache_root / "matplotlib").resolve()),
    }
    for key, new in replacements.items():
        if key in env and env[key] != new:
            old = env[key]
            env[key] = new
            changes.append({"json_path": f"environment_required.{key}", "old": old, "new": new})
    for p in cache_root.glob("*"):
        p.mkdir(parents=True, exist_ok=True)
    cache_root.mkdir(parents=True, exist_ok=True)
    for name in ["torchinductor", "triton", "xdg", "matplotlib"]:
        (cache_root / name).mkdir(parents=True, exist_ok=True)


def patch_known_paths(obj: Any, staged: dict[str, Path], changes: list[dict[str, Any]], prefix: str = "") -> None:
    if isinstance(obj, dict):
        filename = obj.get("filename")
        if filename in staged and "known_path" in obj:
            old = obj["known_path"]
            new = str(staged[filename].resolve())
            if old != new:
                obj["known_path"] = new
                changes.append({"json_path": f"{prefix}.known_path".strip("."), "old": old, "new": new})
        for k, v in obj.items():
            patch_known_paths(v, staged, changes, f"{prefix}.{k}".strip("."))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            patch_known_paths(v, staged, changes, f"{prefix}[{i}]")


def patch_config(
    run: str,
    cfg: dict[str, Any],
    *,
    model_source: Path,
    val_dir: Path,
    split_sha: str,
    checkpoint_manifest_sha: str,
    runtime_root: Path,
    cache_root: Path,
    staged: dict[str, Path],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    out = copy.deepcopy(cfg)
    changes: list[dict[str, Any]] = []

    if "model_source" in out:
        set_change(changes, out, ["model_source", "path"], relative_or_absolute(model_source))
        # SHA is scientific provenance and must already be the exact locked value.
        if out["model_source"].get("sha256") != MODEL_SOURCE_SHA256:
            raise RuntimeError(f"{run}: unexpected locked model-source SHA")
    if "val_dir" in out:
        set_change(changes, out, ["val_dir"], relative_or_absolute(val_dir))

    if run == "M1":
        set_change(changes, out, ["split_manifest"], RUNTIME_SPLIT)
        set_change(changes, out, ["checkpoint_manifest"], RUNTIME_CHECKPOINT_MANIFEST)
    elif run == "M2":
        set_change(changes, out, ["split_manifest", "filename"], RUNTIME_SPLIT)
        set_change(changes, out, ["split_manifest", "sha256"], split_sha)
        set_change(changes, out, ["checkpoint_manifest", "filename"], RUNTIME_CHECKPOINT_MANIFEST)
        set_change(changes, out, ["checkpoint_manifest", "sha256"], checkpoint_manifest_sha)
    elif run == "M4":
        set_change(changes, out, ["sources", "split_manifest", "filename"], RUNTIME_SPLIT)
        set_change(changes, out, ["sources", "split_manifest", "sha256"], split_sha)
    elif run == "M5":
        set_change(changes, out, ["split_manifest", "filename"], RUNTIME_SPLIT)
        set_change(changes, out, ["split_manifest", "sha256"], split_sha)
        set_change(changes, out, ["checkpoint_manifest", "filename"], RUNTIME_CHECKPOINT_MANIFEST)
        set_change(changes, out, ["checkpoint_manifest", "sha256"], checkpoint_manifest_sha)

    patch_environment(out, cache_root, changes)
    patch_known_paths(out, staged, changes)
    return out, changes


def dependencies_for_targets(dep_manifest: dict[str, Any], targets: list[str]) -> dict[str, str]:
    key_map = {
        "M1": "M1_H1_0015",
        "M2": "M2_H1_0016",
        "M3": "M3_H1_0017",
        "M4": "M4_H1_0018",
        "M5": "M5_H1_0019",
    }
    needed: dict[str, str] = {}
    for t in targets:
        for item in dep_manifest["run_dependencies"][key_map[t]]:
            old = needed.get(item["filename"])
            if old is not None and old != item["sha256"]:
                raise RuntimeError(f"conflicting SHA identities for {item['filename']}")
            needed[item["filename"]] = item["sha256"]
    return needed


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo-root", type=Path, default=Path.cwd())
    p.add_argument("--output-root", type=Path, required=True)
    p.add_argument("--model-source", type=Path)
    p.add_argument("--checkpoint", type=Path)
    p.add_argument("--imagenet-val", type=Path)
    p.add_argument("--artifact-dir", type=Path, action="append", default=[])
    p.add_argument("--target", choices=sorted(RUNS), action="append", help="repeat; default M1--M5")
    p.add_argument("--stage-mode", choices=["symlink", "copy"], default="symlink")
    p.add_argument(
        "--plan-only",
        action="store_true",
        help="validate public metadata and emit a missing-input plan without requiring external checkpoint/data/artifacts",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    repo = args.repo_root.resolve()
    out = args.output_root.resolve()
    targets = args.target or list(RUNS)

    manifests = repo / "manifests"
    configs = repo / "configs"
    code = repo / "code"
    dep_path = manifests / DEPENDENCY_MANIFEST
    split_path = manifests / PUBLIC_SPLIT
    if not dep_path.is_file() or not split_path.is_file():
        raise FileNotFoundError("public dependency/split manifest missing from repository")
    deps = load_json(dep_path)
    split = load_json(split_path)
    if split.get("authoritative_locked_source", {}).get("sha256") != deps["shared"]["split"]["locked_source_sha256"]:
        raise RuntimeError("public split does not bind to the expected locked source SHA")
    for key, count in [("calibration_C", 256), ("geometry_A_G_1", 320), ("geometry_A_G_2", 320), ("independent_attack_A_P", 640)]:
        if len(split["indices"][key]) != count:
            raise RuntimeError(f"unexpected public split count for {key}")

    model_source = args.model_source.resolve() if args.model_source else Path("/REPLACE/WITH/full_scale_experiment.py")
    checkpoint = args.checkpoint.resolve() if args.checkpoint else Path("/REPLACE/WITH/TSPG_LEARNED_SEED42_best_model.pth")
    val_dir = args.imagenet_val.resolve() if args.imagenet_val else Path("/REPLACE/WITH/imagenet100/val")

    if not args.plan_only:
        if args.model_source is None or args.checkpoint is None or args.imagenet_val is None:
            raise SystemExit("materialization requires --model-source, --checkpoint, and --imagenet-val")
        verify(model_source, MODEL_SOURCE_SHA256)
        verify(checkpoint, CHECKPOINT_SHA256, expected_size=CHECKPOINT_SIZE)
        nclasses, nimages = enumerate_imagefolder(val_dir)
        if (nclasses, nimages) != (100, 5000):
            raise RuntimeError(f"unexpected ImageNet-100 ImageFolder: classes={nclasses}, images={nimages}")

    runtime_root = out / "runtime_root"
    runtime_cfg_dir = out / "runtime_configs"
    cache_root = out / "cache"
    runtime_root.mkdir(parents=True, exist_ok=True)
    runtime_cfg_dir.mkdir(parents=True, exist_ok=True)
    cache_root.mkdir(parents=True, exist_ok=True)

    # Public semantic split: copy bytes exactly, then bind the derived configs to its runtime SHA.
    runtime_split = runtime_root / RUNTIME_SPLIT
    shutil.copy2(split_path, runtime_split)
    split_sha = sha256_file(runtime_split)

    checkpoint_compat = {
        "schema": "TSPG_RUNTIME_SINGLE_CHECKPOINT_COMPAT_v1",
        "created_from": "manifests/TSPG_LEARNED_SEED42_CHECKPOINT_MANIFEST_v1_0_20260829.json",
        "seed42_development_checkpoints": {
            "learned": {
                "path": relative_or_absolute(checkpoint),
                "sha256": CHECKPOINT_SHA256,
            }
        },
        "note": "Portable compatibility manifest for unchanged locked runners; it changes only the host-local checkpoint path.",
    }
    checkpoint_compat_path = runtime_root / RUNTIME_CHECKPOINT_MANIFEST
    write_json(checkpoint_compat_path, checkpoint_compat)
    checkpoint_manifest_sha = sha256_file(checkpoint_compat_path)

    # Stage public analysis modules in the flat root expected by the locked runners.
    staged_code: list[dict[str, str]] = []
    for p in sorted(code.glob("*.py")):
        dst = runtime_root / p.name
        shutil.copy2(p, dst)
        staged_code.append({"filename": p.name, "sha256": sha256_file(dst)})

    needed = dependencies_for_targets(deps, targets)
    search_roots = [p.resolve() for p in args.artifact_dir] + [repo / "results", repo / "manifests"]
    staged: dict[str, Path] = {}
    missing: list[dict[str, str]] = []
    for filename, expected_sha in sorted(needed.items()):
        src = unique_candidate(filename, search_roots, expected_sha)
        if src is None:
            missing.append({"filename": filename, "sha256": expected_sha})
            continue
        dst = runtime_root / filename
        stage_file(src, dst, args.stage_mode)
        verify(dst, expected_sha)
        staged[filename] = dst

    config_audits = []
    for target in targets:
        meta = RUNS[target]
        src_cfg = configs / meta["config"]
        src_runner = code / meta["runner"]
        if not src_cfg.is_file() or not src_runner.is_file():
            raise FileNotFoundError(f"missing public config/runner for {target}")
        cfg = load_json(src_cfg)
        runtime_cfg, changes = patch_config(
            target,
            cfg,
            model_source=model_source,
            val_dir=val_dir,
            split_sha=split_sha,
            checkpoint_manifest_sha=checkpoint_manifest_sha,
            runtime_root=runtime_root,
            cache_root=cache_root,
            staged=staged,
        )
        dst_cfg = runtime_cfg_dir / f"{src_cfg.stem}.runtime.json"
        write_json(dst_cfg, runtime_cfg)
        config_audits.append(
            {
                "target": target,
                "locked_config": str(src_cfg.relative_to(repo)),
                "locked_config_sha256": sha256_file(src_cfg),
                "runtime_config": str(dst_cfg),
                "runtime_config_sha256": sha256_file(dst_cfg),
                "runner": str(src_runner.relative_to(repo)),
                "runner_sha256": sha256_file(src_runner),
                "changes": changes,
            }
        )

    report = {
        "schema": "TSPG_PORTABLE_RUNTIME_PREPARATION_REPORT_v1",
        "mode": "PLAN_ONLY" if args.plan_only else "MATERIALIZED",
        "targets": targets,
        "runtime_root": str(runtime_root),
        "public_split": {
            "source": str(split_path.relative_to(repo)),
            "runtime_filename": RUNTIME_SPLIT,
            "runtime_sha256": split_sha,
            "locked_source_sha256": deps["shared"]["split"]["locked_source_sha256"],
        },
        "checkpoint_compat_manifest": {
            "filename": RUNTIME_CHECKPOINT_MANIFEST,
            "sha256": checkpoint_manifest_sha,
        },
        "model_source": {"path": str(model_source), "required_sha256": MODEL_SOURCE_SHA256},
        "checkpoint": {"path": str(checkpoint), "required_sha256": CHECKPOINT_SHA256, "required_size": CHECKPOINT_SIZE},
        "imagenet_val": str(val_dir),
        "staged_code": staged_code,
        "staged_external_artifacts": [
            {"filename": name, "path": str(path), "sha256": needed[name]} for name, path in sorted(staged.items())
        ],
        "missing_external_artifacts": missing,
        "runtime_config_audit": config_audits,
        "scientific_parameter_edit_policy": "Only host-local routing/cache fields and compatibility-manifest filename/SHA fields are changed; all scientific parameters remain inherited from the exact locked configs.",
    }
    report_path = out / "TSPG_PORTABLE_RUNTIME_PREPARATION_REPORT_v1.json"
    write_json(report_path, report)

    print(f"Runtime preparation report: {report_path}")
    print(f"Targets: {', '.join(targets)}")
    print(f"Staged external artifacts: {len(staged)}")
    print(f"Missing external artifacts: {len(missing)}")
    for item in missing:
        print(f"  MISSING {item['filename']}  {item['sha256']}")
    if args.plan_only:
        print("PLAN_ONLY: external checkpoint/model/data hashes were not executed.")
        return 0
    if missing:
        print("Runtime root is incomplete; supply the missing SHA-locked archival artifacts and rerun.", file=sys.stderr)
        return 2
    print("Portable runtime root prepared with all requested external inputs SHA-verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
