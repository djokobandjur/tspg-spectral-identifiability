#!/usr/bin/env python3
from pathlib import Path
import argparse, json, hashlib, sys, time
import numpy as np

def sha256_file(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""):
            h.update(c)
    return h.hexdigest()

def locate_locked(spec,root):
    candidates=[Path(spec["known_path"]),root/spec["filename"],root.parent/spec["filename"]]
    seen=set()
    for p in candidates:
        p=p.expanduser()
        if str(p) in seen: continue
        seen.add(str(p))
        if p.is_file():
            got=sha256_file(p)
            if got==spec["sha256"]:
                return p.resolve()
    search_root=Path("/home/djoko.bandjur.ftnkm/Notebooks/TSPG")
    if search_root.is_dir():
        for p in search_root.glob(f"**/{spec['filename']}"):
            if p.is_file() and sha256_file(p)==spec["sha256"]:
                return p.resolve()
    raise RuntimeError(f"SHA-locked source not found: {spec['filename']}")

def save_json(p,o):
    p.write_text(json.dumps(o,indent=2),encoding="utf-8")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--config",type=Path,required=True)
    ap.add_argument("--root",type=Path,required=True)
    ap.add_argument("--output-dir",type=Path,required=True)
    a=ap.parse_args()

    cfg=json.loads(a.config.read_text())
    root=a.root.resolve()
    out=a.output_dir.resolve()
    out.mkdir(parents=True,exist_ok=False)

    sys.path.insert(0,str(root))
    from TSPG_h1_0017_offline_b_normalized_crossfit_v1_1_20260829 import analyze

    print("H1-0017 OFFLINE ONLY",flush=True)
    print("GPU/model/gradients/G_A actions: 0",flush=True)

    h10=locate_locked(cfg["sources"]["h1_0010_raw"],root)
    h16=locate_locked(cfg["sources"]["h1_0016_derived"],root)
    print("H1-0010 source:",h10,flush=True)
    print("H1-0016 source:",h16,flush=True)

    t0=time.time()
    with np.load(h10) as z:
        C1=np.asarray(z["C320"],dtype=np.float64)
        A=np.asarray(z["A320"],dtype=np.float64)
    with np.load(h16) as z:
        C2=np.asarray(z["C2"],dtype=np.float64)
        H=np.asarray(z["H21"],dtype=np.float64)
        eta_existing=np.asarray(z["eta_task_1_to_2"],dtype=np.float64)

    alpha=float(cfg["alpha"])
    B=0.5*(A+A.T)+alpha*np.eye(A.shape[0],dtype=np.float64)
    C1=0.5*(C1+C1.T)
    C2=0.5*(C2+C2.T)
    H=0.5*(H+H.T)

    print("Matrices loaded; solving dense 320x320 problems...",flush=True)
    res=analyze(C1,H,B,cfg["k_ladder"])

    gates=cfg["numerical_gates"]
    checks={}
    checks["B_min_eigenvalue_positive"]=bool(np.min(res["B_eigenvalues"])>0)
    checks["B_invsqrt_reconstruction"]=bool(res["B_invsqrt_reconstruction_relative_fro"]<=gates["B_invsqrt_reconstruction_relative_fro"])
    checks["B_orth_train_full"]=bool(res["B_orth_error_train_full"]<=gates["B_orthonormality_inf"])
    checks["B_orth_oracle_full"]=bool(res["B_orth_error_oracle_full"]<=gates["B_orthonormality_inf"])
    checks["self_scaled_train_top32"]=bool(np.max(res["self_scaled_residual_train"][:32])<=gates["self_scaled_generalized_residual_top32"])
    checks["self_scaled_oracle_top32"]=bool(np.max(res["self_scaled_residual_oracle"][:32])<=gates["self_scaled_generalized_residual_top32"])
    checks["normwise_backward_train_all320"]=bool(np.max(res["normwise_backward_train"])<=gates["normwise_generalized_backward_error_all320"])
    checks["normwise_backward_oracle_all320"]=bool(np.max(res["normwise_backward_oracle"])<=gates["normwise_generalized_backward_error_all320"])
    checks["symmetric_backward_train_all320"]=bool(np.max(res["symmetric_backward_train"])<=gates["symmetric_backward_error_all320"])
    checks["symmetric_backward_oracle_all320"]=bool(np.max(res["symmetric_backward_oracle"])<=gates["symmetric_backward_error_all320"])

    baseline_errors={}
    for row in res["rows"]:
        k=row["k"]
        err=abs(row["eta_task_SE"]-float(eta_existing[k-1]))
        baseline_errors[str(k)]=float(err)
    checks["task_baseline_reproduced"]=bool(max(baseline_errors.values())<=gates["task_baseline_reproduction_abs"])

    all_eff=[]
    all_cos=[]
    for row in res["rows"]:
        all_eff += [row["eta_task_SE"],row["eta_task_SB"],row["eta_B_SE"],row["eta_B_SB"]]
        all_cos += row["B_principal_cosines"]
        checks[f"B_orth_train_k{row['k']}"]=bool(row["B_orth_error_train_k"]<=gates["B_orthonormality_inf"])
        checks[f"B_orth_oracle_k{row['k']}"]=bool(row["B_orth_error_oracle_k"]<=gates["B_orthonormality_inf"])
    checks["efficiencies_le_one"]=bool(max(all_eff)<=gates["efficiency_upper"])
    checks["principal_cosines_le_one"]=bool(max(all_cos)<=gates["principal_cosine_upper"])

    if not all(checks.values()):
        raise RuntimeError(f"numerical gate failed: {checks}")

    derived=out/cfg["output_names"]["derived_npz"]
    np.savez(
        derived,
        B11=B,
        B_eigenvalues=res["B_eigenvalues"],
        theta=res["theta"],nu=res["nu"],glam=res["glam"],mu=res["mu"],
        WB=res["WB"],WO=res["WO"],
        self_scaled_residual_train=res["self_scaled_residual_train"],
        self_scaled_residual_oracle=res["self_scaled_residual_oracle"],
        normwise_backward_train=res["normwise_backward_train"],
        normwise_backward_oracle=res["normwise_backward_oracle"],
        symmetric_backward_train=res["symmetric_backward_train"],
        symmetric_backward_oracle=res["symmetric_backward_oracle"],
    )

    result={
        "schema":"TSPG_H1_0017_RESULT_v1_1",
        "run_id":cfg["run_id"],
        "technical_status":"PASS",
        "scientific_status":"DEVELOPMENT_RESULT_PENDING_DISCUSSION",
        "confirmatory_H1_status":"BLOCKED",
        "offline_only":{"gpu":False,"model_loaded":False,"new_task_gradients":0,"new_GA_actions":0},
        "sources":{
            "h1_0010_raw":{"path":str(h10),"sha256":cfg["sources"]["h1_0010_raw"]["sha256"]},
            "h1_0016_derived":{"path":str(h16),"sha256":cfg["sources"]["h1_0016_derived"]["sha256"]},
        },
        "alpha":alpha,
        "matrix_summary":{
            "rank":int(B.shape[0]),
            "B_min_eigenvalue":float(np.min(res["B_eigenvalues"])),
            "B_max_eigenvalue":float(np.max(res["B_eigenvalues"])),
            "B_condition":res["B_condition"],
            "B_invsqrt_reconstruction_relative_fro":res["B_invsqrt_reconstruction_relative_fro"],
            "B_orth_error_train_full":res["B_orth_error_train_full"],
            "B_orth_error_oracle_full":res["B_orth_error_oracle_full"],
            "self_scaled_residual_train_max_all320":float(np.max(res["self_scaled_residual_train"])),
            "self_scaled_residual_oracle_max_all320":float(np.max(res["self_scaled_residual_oracle"])),
            "self_scaled_residual_train_max_top32":float(np.max(res["self_scaled_residual_train"][:32])),
            "self_scaled_residual_oracle_max_top32":float(np.max(res["self_scaled_residual_oracle"][:32])),
            "normwise_backward_train_max_all320":float(np.max(res["normwise_backward_train"])),
            "normwise_backward_oracle_max_all320":float(np.max(res["normwise_backward_oracle"])),
            "symmetric_backward_train_max_all320":float(np.max(res["symmetric_backward_train"])),
            "symmetric_backward_oracle_max_all320":float(np.max(res["symmetric_backward_oracle"])),
        },
        "k_rows":res["rows"],
        "task_baseline_reproduction_abs_error":baseline_errors,
        "predictions_not_gates":cfg["predictions_not_gates"],
        "interpretation_locks":cfg["interpretation_locks"],
        "numerical_checks":checks,
        "derived_output":{"filename":derived.name,"sha256":sha256_file(derived),"size_bytes":derived.stat().st_size},
        "elapsed_sec":float(time.time()-t0)
    }
    rp=out/cfg["output_names"]["result_json"]
    save_json(rp,result)

    print("\nTECHNICAL STATUS: PASS",flush=True)
    print("B condition:",res["B_condition"],flush=True)
    print("\nk  etaTask(SE) etaTask(SB) etaB(SE) etaB(SB) dSelTask dSelB  bRatio  minBcos gamma",flush=True)
    for x in res["rows"]:
        print(
            f"{x['k']:2d} "
            f"{x['eta_task_SE']:.4f} {x['eta_task_SB']:.4f} "
            f"{x['eta_B_SE']:.4f} {x['eta_B_SB']:.4f} "
            f"{x['Delta_sel_task']:+.4f} {x['Delta_sel_B']:+.4f} "
            f"{x['bbar_ratio_SB_over_SE']:.4f} "
            f"{x['B_min_principal_cosine']:.4f} "
            f"{x['heldout_gamma_k']:.4f}"
        ,flush=True)
    print("\nConfirmatory H1 remains BLOCKED pending scientific discussion.",flush=True)

if __name__=="__main__":
    main()
