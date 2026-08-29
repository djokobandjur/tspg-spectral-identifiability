#!/usr/bin/env python3
from pathlib import Path
import argparse, csv, hashlib, json, os, sys, time
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
        if p.is_file() and sha256_file(p)==spec["sha256"]:
            return p.resolve()
    search_root=Path("/home/djoko.bandjur.ftnkm/Notebooks/TSPG")
    if search_root.is_dir():
        for p in search_root.glob(f"**/{spec['filename']}"):
            if p.is_file() and sha256_file(p)==spec["sha256"]:
                return p.resolve()
    raise RuntimeError(f"SHA-locked source not found: {spec['filename']}")

def enumerate_imagefolder_labels(root):
    root=Path(root)
    classes=sorted([p.name for p in root.iterdir() if p.is_dir()])
    class_to_idx={c:i for i,c in enumerate(classes)}
    exts={".jpg",".jpeg",".png",".ppm",".bmp",".pgm",".tif",".tiff",".webp"}
    labels=[]
    paths=[]
    for c in classes:
        target=class_to_idx[c]
        croot=root/c
        walks=sorted(os.walk(croot,followlinks=True),key=lambda x:x[0])
        for walk_root,_,fnames in walks:
            for fname in sorted(fnames):
                p=Path(walk_root)/fname
                if p.suffix.lower() in exts:
                    paths.append(str(p))
                    labels.append(target)
    return classes,np.asarray(labels,dtype=np.int64),paths

def gram_block(A,B,block=16,label="K"):
    n=A.shape[0]
    m=B.shape[0]
    out=np.empty((n,m),dtype=np.float64)
    BT=B.T
    t0=time.time()
    for i in range(0,n,block):
        j=min(i+block,n)
        out[i:j,:]=np.asarray(A[i:j],dtype=np.float64)@BT
        print(f"[{label}] rows {j}/{n} elapsed={time.time()-t0:.1f}s",flush=True)
    return out

def write_json(p,o):
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
    from TSPG_h1_0018_dual_finite_sample_stability_v1_0_20260829 import (
        coverage_first_subset, dual_metrics, fit_inverse_n, seed_from_parts, summarize
    )

    print("H1-0018 — existing gradients only",flush=True)
    print("New model/GPU/gradient/G_A scientific compute: 0",flush=True)

    # Small provenance.
    split=json.loads((root/cfg["sources"]["split_manifest"]["filename"]).read_text())
    ag1meta=json.loads((root/cfg["sources"]["AG1_metadata"]["filename"]).read_text())
    h16=json.loads((root/cfg["sources"]["H1_0016_result"]["filename"]).read_text())
    gate=json.loads((root/cfg["sources"]["H1_0016_gate"]["filename"]).read_text())

    I1=split["indices"]["geometry_A_G_1"]
    I2=split["indices"]["geometry_A_G_2"]
    if I1!=ag1meta["sample_indices"]:
        raise RuntimeError("AG1 sample-order provenance mismatch")
    if I2!=h16["AG2_gradients"]["sample_indices"]:
        raise RuntimeError("AG2 sample-order provenance mismatch")

    # Exact raw gradient identities.
    g1p=locate_locked(cfg["sources"]["AG1_gradients"],root)
    g2p=locate_locked(cfg["sources"]["AG2_gradients"],root)
    print("AG1 raw:",g1p,flush=True)
    print("AG2 raw:",g2p,flush=True)

    G1=np.load(g1p,mmap_mode="r")
    G2=np.load(g2p,mmap_mode="r")
    if list(G1.shape)!=cfg["sources"]["AG1_gradients"]["shape"] or str(G1.dtype)!="float64":
        raise RuntimeError("AG1 raw shape/dtype mismatch")
    if list(G2.shape)!=cfg["sources"]["AG2_gradients"]["shape"] or str(G2.dtype)!="float64":
        raise RuntimeError("AG2 raw shape/dtype mismatch")

    # Pure-Python ImageFolder enumeration, verified against H1-0016 gate.
    classes,all_labels,_=enumerate_imagefolder_labels(Path(cfg["val_dir"]))
    if len(classes)!=100 or len(all_labels)!=5000:
        raise RuntimeError(f"unexpected ImageFolder enumeration: classes={len(classes)} n={len(all_labels)}")
    lab1=all_labels[np.asarray(I1,dtype=np.int64)]
    lab2=all_labels[np.asarray(I2,dtype=np.int64)]
    hist1=np.bincount(lab1,minlength=100)
    hist2=np.bincount(lab2,minlength=100)
    cg=gate["class_composition"]
    if hist1.tolist()!=cg["AG1_class_histogram"] or hist2.tolist()!=cg["AG2_class_histogram"]:
        raise RuntimeError("pure-Python ImageFolder class enumeration does not reproduce H1-0016 gate histograms")
    print("Class provenance PASS: AG1",np.count_nonzero(hist1),"AG2",np.count_nonzero(hist2),flush=True)

    # One-time dual Grams.
    print("\nSTAGE A — dual Gram matrices",flush=True)
    K11=gram_block(G1,G1,16,"K11")
    K22=gram_block(G2,G2,16,"K22")
    K12=gram_block(G1,G2,16,"K12")
    K11=0.5*(K11+K11.T)
    K22=0.5*(K22+K22.T)

    n_ladder=cfg["n_ladder"]
    k_ladder=cfg["k_ladder"]
    reps=cfg["replicates_per_n"]
    all_idx=np.arange(320,dtype=np.int64)

    records=[]
    subset_store={}
    run_id=cfg["run_id"]

    def run_direction(direction,train_labels,held_labels,Ktt,Khh,Kth):
        # Primary: train-n / held-320
        for role in [cfg["primary_role"],cfg["secondary_role"]]:
            for n in n_ladder:
                R=1 if n==320 else reps
                for rep in range(R):
                    if role==cfg["primary_role"]:
                        seed=seed_from_parts(run_id,direction,role,n,rep)
                        s_idx=coverage_first_subset(train_labels,n,seed)
                        h_idx=all_idx
                        subset_store[f"{direction}_{role}_n{n}_r{rep}_train"]=s_idx
                        m=dual_metrics(Ktt,Khh,Kth,s_idx,h_idx,k_ladder)
                        train_classes=len(np.unique(train_labels[s_idx]))
                        held_classes=len(np.unique(held_labels))
                    else:
                        seed=seed_from_parts(run_id,direction,role,n,rep)
                        s_idx=all_idx
                        h_idx=coverage_first_subset(held_labels,n,seed)
                        subset_store[f"{direction}_{role}_n{n}_r{rep}_held"]=h_idx
                        m=dual_metrics(Ktt,Khh,Kth,s_idx,h_idx,k_ladder)
                        train_classes=len(np.unique(train_labels))
                        held_classes=len(np.unique(held_labels[h_idx]))
                    row={
                        "direction":direction,"role":role,"n":int(n),"replicate":int(rep),
                        "seed":int(seed if n<320 else 0),
                        "phi":m["phi"],"train_rank":m["train_rank"],
                        "train_classes":int(train_classes),"held_classes":int(held_classes)
                    }
                    for k in k_ladder:
                        row[f"T{k}"]=m["metrics_by_k"][k]["T"]
                        row[f"U{k}"]=m["metrics_by_k"][k]["U_oracle"]
                        row[f"eta{k}"]=m["metrics_by_k"][k]["eta"]
                    records.append(row)
                print(f"[{direction} {role}] n={n} reps={R} PASS",flush=True)

    print("\nSTAGE B — deterministic resampling curves",flush=True)
    run_direction("AG1_TO_AG2",lab1,lab2,K11,K22,K12)
    run_direction("AG2_TO_AG1",lab2,lab1,K22,K11,K12.T)

    # Hard full-n reproduction of H1-0016.
    print("\nSTAGE C — full-n reproduction gates",flush=True)
    full={}
    for d in ["AG1_TO_AG2","AG2_TO_AG1"]:
        rr=[x for x in records if x["direction"]==d and x["role"]==cfg["primary_role"] and x["n"]==320][0]
        full[d]=rr
    phi_ref={
        "AG1_TO_AG2":h16["coverage"]["phi_1_to_2"],
        "AG2_TO_AG1":h16["coverage"]["phi_2_to_1"]
    }
    eta_ref={
        "AG1_TO_AG2":h16["task_only_curves"]["full_eta_task_1_to_2"],
        "AG2_TO_AG1":h16["task_only_curves"]["full_eta_task_2_to_1"]
    }
    validation={}
    for d in full:
        validation[f"{d}_phi_abs_error"]=abs(full[d]["phi"]-phi_ref[d])
        for k in k_ladder:
            validation[f"{d}_eta{k}_abs_error"]=abs(full[d][f"eta{k}"]-eta_ref[d][k-1])
    if max(validation.values())>cfg["hard_validation"]["full_n_phi_abs_error"]:
        raise RuntimeError(f"full-n H1-0016 reproduction failed: {validation}")
    if full["AG1_TO_AG2"]["train_rank"]<320 or full["AG2_TO_AG1"]["train_rank"]<320:
        raise RuntimeError("full-fold empirical rank < 320")
    if min(x["train_rank"] for x in records)<32:
        raise RuntimeError("subset train rank <32")

    # Class coverage must remain full-fold class count on all resamples.
    if min(x["train_classes"] for x in records if x["role"]==cfg["primary_role"])<98:
        raise RuntimeError("primary train resample lost class coverage")
    if min(x["held_classes"] for x in records if x["role"]==cfg["secondary_role"])<98:
        raise RuntimeError("secondary held resample lost class coverage")

    # Replicate CSV.
    rep_csv=out/cfg["output_names"]["replicate_csv"]
    fieldnames=["direction","role","n","replicate","seed","phi","train_rank","train_classes","held_classes"]
    for k in k_ladder:
        fieldnames += [f"T{k}",f"U{k}",f"eta{k}"]
    with rep_csv.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fieldnames); w.writeheader(); w.writerows(records)

    # Summaries.
    summary_rows=[]
    summary_nested={}
    for d in ["AG1_TO_AG2","AG2_TO_AG1"]:
        summary_nested[d]={}
        for role in [cfg["primary_role"],cfg["secondary_role"]]:
            summary_nested[d][role]={}
            for n in n_ladder:
                rr=[x for x in records if x["direction"]==d and x["role"]==role and x["n"]==n]
                metrics=["phi"]+[f"eta{k}" for k in k_ladder]
                ss={}
                for metric in metrics:
                    s=summarize([x[metric] for x in rr],cfg["quantiles"][0],cfg["quantiles"][1])
                    ss[metric]=s
                    summary_rows.append({
                        "direction":d,"role":role,"n":n,"metric":metric,**s
                    })
                summary_nested[d][role][str(n)]=ss

    sum_csv=out/cfg["output_names"]["summary_csv"]
    sf=["direction","role","n","metric","median","q05","q95","mean","sd","min","max"]
    with sum_csv.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=sf); w.writeheader(); w.writerows(summary_rows)

    # Planning-only 1/n forecasts from PRIMARY curve.
    forecasts={}
    fit_n=cfg["forecast_640"]["fit_n"]
    for d in ["AG1_TO_AG2","AG2_TO_AG1"]:
        forecasts[d]={}
        for metric in ["phi"]+[f"eta{k}" for k in k_ladder]:
            y=[summary_nested[d][cfg["primary_role"]][str(n)][metric]["median"] for n in fit_n]
            forecasts[d][metric]=fit_inverse_n(fit_n,y,cfg["forecast_640"]["target_n"])

    derived=out/cfg["output_names"]["derived_npz"]
    np.savez_compressed(
        derived,
        K11=K11,K22=K22,K12=K12,
        AG1_labels=lab1,AG2_labels=lab2,
        **subset_store
    )

    result={
        "schema":"TSPG_H1_0018_RESULT_v1_0",
        "run_id":cfg["run_id"],
        "technical_status":"PASS",
        "scientific_status":"FINITE_SAMPLE_CURVES_PENDING_DISCUSSION",
        "confirmatory_H1_status":"BLOCKED",
        "scientific_new_compute":{"model":0,"gpu":0,"task_gradients":0,"GA_actions":0},
        "sources":{
            "AG1_gradients":{"path":str(g1p),"sha256":cfg["sources"]["AG1_gradients"]["sha256"]},
            "AG2_gradients":{"path":str(g2p),"sha256":cfg["sources"]["AG2_gradients"]["sha256"]}
        },
        "class_provenance":{
            "AG1_unique_classes":int(np.count_nonzero(hist1)),
            "AG2_unique_classes":int(np.count_nonzero(hist2)),
            "histograms_reproduce_H1_0016_gate":True
        },
        "full_n_validation":validation,
        "summary":summary_nested,
        "forecast_640_planning_only":forecasts,
        "interpretation_locks":cfg["interpretation_locks"],
        "conditional_H19_guardrails":cfg["conditional_H19_guardrails"],
        "outputs":{
            "replicate_csv":{"filename":rep_csv.name,"sha256":sha256_file(rep_csv)},
            "summary_csv":{"filename":sum_csv.name,"sha256":sha256_file(sum_csv)},
            "derived_npz":{"filename":derived.name,"sha256":sha256_file(derived),"size_bytes":derived.stat().st_size}
        }
    }
    rp=out/cfg["output_names"]["result_json"]
    write_json(rp,result)

    print("\nH1-0018 TECHNICAL STATUS: PASS",flush=True)
    for d in ["AG1_TO_AG2","AG2_TO_AG1"]:
        print("\nPRIMARY",d,flush=True)
        for n in n_ladder:
            s=summary_nested[d][cfg["primary_role"]][str(n)]
            print(
                f"n={n:3d} phi={s['phi']['median']:.4f} "
                + " ".join(f"eta{k}={s[f'eta{k}']['median']:.4f}" for k in k_ladder),
                flush=True
            )
        print("planning forecast n=640:",flush=True)
        for metric,v in forecasts[d].items():
            print(f"  {metric}: {v['prediction_bounded_0_1']:.4f} "
                  f"(gain raw {v['gain_from_last_observed_raw']:+.4f}, R2={v['r2']:.3f})",flush=True)

    print("\nConfirmatory H1 remains BLOCKED. H19 is NOT authorized.",flush=True)

if __name__=="__main__":
    main()
