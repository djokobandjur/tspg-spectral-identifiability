#!/usr/bin/env python3
from pathlib import Path
import argparse, json, hashlib, importlib, os, sys, time
import numpy as np

def sha256_file(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""):
            h.update(c)
    return h.hexdigest()

def save_json(p,o):
    p.write_text(json.dumps(o,indent=2),encoding="utf-8")

def locate_locked(spec,root):
    candidates=[Path(spec["known_path"]),root/spec["filename"],root.parent/spec["filename"]]
    seen=set()
    for p in candidates:
        p=p.expanduser()
        if str(p) in seen: continue
        seen.add(str(p))
        if p.is_file() and sha256_file(p)==spec["sha256"]:
            return p.resolve()
    base=Path("/home/djoko.bandjur.ftnkm/Notebooks/TSPG")
    if base.is_dir():
        for p in base.glob(f"**/{spec['filename']}"):
            if p.is_file() and sha256_file(p)==spec["sha256"]:
                return p.resolve()
    raise RuntimeError(f"SHA-locked source not found: {spec['filename']}")

def apply_env(cfg):
    for k,v in cfg["environment_required"].items():
        os.environ[k]=v
    for k in ["TORCHINDUCTOR_CACHE_DIR","TRITON_CACHE_DIR","XDG_CACHE_HOME"]:
        Path(os.environ[k]).mkdir(parents=True,exist_ok=True)

def enumerate_imagefolder_labels(root):
    root=Path(root)
    classes=sorted([p.name for p in root.iterdir() if p.is_dir()])
    class_to_idx={c:i for i,c in enumerate(classes)}
    exts={".jpg",".jpeg",".png",".ppm",".bmp",".pgm",".tif",".tiff",".webp"}
    labels=[]
    for c in classes:
        target=class_to_idx[c]
        for walk_root,_,fnames in sorted(os.walk(root/c,followlinks=True),key=lambda x:x[0]):
            for fname in sorted(fnames):
                p=Path(walk_root)/fname
                if p.suffix.lower() in exts:
                    labels.append(target)
    return classes,np.asarray(labels,dtype=np.int64)

def build_dataset(val_dir,datasets,transforms):
    tfm=transforms.Compose([
        transforms.Resize(256),transforms.CenterCrop(224),transforms.ToTensor(),
        transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
    ])
    ds=datasets.ImageFolder(val_dir,transform=tfm)
    if len(ds)!=5000:
        raise RuntimeError(f"unexpected dataset size {len(ds)}")
    return ds

def load_model(cfg,root,torch):
    mp=root/cfg["checkpoint_manifest"]["filename"]
    if sha256_file(mp)!=cfg["checkpoint_manifest"]["sha256"]:
        raise RuntimeError("checkpoint manifest SHA mismatch")
    man=json.loads(mp.read_text())
    dev=man["seed42_development_checkpoints"]["learned"]
    cp=Path(dev["path"])
    if sha256_file(cp)!=dev["sha256"]:
        raise RuntimeError("checkpoint SHA mismatch")
    source=Path(cfg["model_source"]["path"])
    if sha256_file(source)!=cfg["model_source"]["sha256"]:
        raise RuntimeError("model source SHA mismatch")
    sdir=str(source.parent.resolve())
    if sdir not in sys.path: sys.path.insert(0,sdir)
    mod=importlib.import_module("full_scale_experiment")
    m=mod.VisionTransformer(
        embed_dim=768,depth=12,num_heads=12,mlp_ratio=4.0,dropout=0.0,
        img_size=224,patch_size=16,num_classes=100,pe_type="learned"
    ).to(torch.device(cfg["runtime"]["device"]))
    state=torch.load(cp,map_location=cfg["runtime"]["device"],weights_only=False)
    if isinstance(state,dict) and "model_state_dict" in state:
        state=state["model_state_dict"]
    state={k.replace("_orig_mod.",""):v for k,v in state.items()}
    res=m.load_state_dict(state,strict=True)
    if res.missing_keys or res.unexpected_keys:
        raise RuntimeError(res)
    m.eval()
    for p in m.parameters(): p.requires_grad_(False)
    return m.double(),cp

def construct_basis_from_dual(G1,G2,A,block=8):
    # Q = G_F^T A, built without materializing pooled G_F.
    d=G1.shape[1]; k=A.shape[1]
    Q=np.empty((d,k),dtype=np.float64)
    for j in range(0,k,block):
        e=min(j+block,k)
        Q[:,j:e]=(
            np.asarray(G1,dtype=np.float64).T@A[:320,j:e]
            +np.asarray(G2,dtype=np.float64).T@A[320:,j:e]
        )
        print(f"[basis] cols {e}/{k}",flush=True)
    return Q

def run_fit_gate(cfg,root,out):
    out.mkdir(parents=True,exist_ok=False)
    sys.path.insert(0,str(root))
    from TSPG_h1_0019_consensus_thirdfold_v1_0_20260829 import fit_arms_from_dual

    print("H1-0019 FIT-ONLY LOCK — AP task gradients not accessed",flush=True)

    dual=root/cfg["fit_sources"]["H18_dual"]["filename"]
    if sha256_file(dual)!=cfg["fit_sources"]["H18_dual"]["sha256"]:
        raise RuntimeError("H18 dual SHA mismatch")
    with np.load(dual) as z:
        K11=np.asarray(z["K11"],dtype=np.float64)
        K22=np.asarray(z["K22"],dtype=np.float64)
        K12=np.asarray(z["K12"],dtype=np.float64)
        lab1=np.asarray(z["AG1_labels"],dtype=np.int64)
        lab2=np.asarray(z["AG2_labels"],dtype=np.int64)

    fit=fit_arms_from_dual(K11,K22,K12,cfg["consensus"]["fit_max_k"])
    if fit["swap_relative_fro"]>1e-14:
        raise RuntimeError("consensus fold-swap invariance failed")
    if max(fit["orthonormality"].values())>1e-10:
        raise RuntimeError(f"arm orthonormality failed: {fit['orthonormality']}")

    # AP semantic composition only; no AP gradients.
    sp=root/cfg["split_manifest"]["filename"]
    if sha256_file(sp)!=cfg["split_manifest"]["sha256"]:
        raise RuntimeError("split manifest SHA mismatch")
    split=json.loads(sp.read_text())
    I1=split["indices"][cfg["split_manifest"]["AG1_key"]]
    I2=split["indices"][cfg["split_manifest"]["AG2_key"]]
    IAP=split["indices"][cfg["split_manifest"]["AP_key"]]
    classes,labels=enumerate_imagefolder_labels(Path(cfg["val_dir"]))
    if len(classes)!=100 or len(labels)!=5000:
        raise RuntimeError("unexpected ImageFolder enumeration")
    l1=labels[np.asarray(I1,dtype=np.int64)]
    l2=labels[np.asarray(I2,dtype=np.int64)]
    lap=labels[np.asarray(IAP,dtype=np.int64)]
    if not np.array_equal(l1,lab1) or not np.array_equal(l2,lab2):
        raise RuntimeError("H18 dual labels do not reproduce current split/ImageFolder labels")
    s1=set(map(int,np.unique(l1))); s2=set(map(int,np.unique(l2))); sap=set(map(int,np.unique(lap)))
    gate={
        "AP_unique_classes":len(sap),
        "AP_intersection_AG1":len(sap&s1),
        "AP_intersection_AG2":len(sap&s2),
    }
    gate["pass"]=bool(
        gate["AP_unique_classes"]>=cfg["AP_gate"]["minimum_unique_classes"]
        and gate["AP_intersection_AG1"]>=cfg["AP_gate"]["minimum_intersection_with_AG1"]
        and gate["AP_intersection_AG2"]>=cfg["AP_gate"]["minimum_intersection_with_AG2"]
    )
    if not gate["pass"]:
        save_json(out/cfg["output_names"]["fit_gate_json"],{
            "technical_status":"STOP_AP_CLASS_CONFOUND","class_gate":gate
        })
        raise SystemExit(12)

    lock=out/cfg["output_names"]["fit_lock_npz"]
    np.savez(
        lock,
        pooled_eigenvalues=fit["pooled_eigenvalues"],
        consensus_eigenvalues=fit["consensus_eigenvalues"],
        A_U320_AG1=fit["arms"]["U320_AG1"],
        A_U320_AG2=fit["arms"]["U320_AG2"],
        A_U640=fit["arms"]["U640"],
        A_CONS640=fit["arms"]["CONS640"],
    )
    payload={
        "schema":"TSPG_H1_0019_FIT_GATE_RESULT_v1_0",
        "run_id":cfg["run_id"],
        "technical_status":"PASS",
        "AP_task_gradients_computed":0,
        "pooled_rank":fit["pooled_rank"],
        "pooled_rank_tol":fit["pooled_tol"],
        "arm_orthonormality":fit["orthonormality"],
        "fit_energy_top32":fit["fit_energy"],
        "consensus_fold_swap_relative_fro":fit["swap_relative_fro"],
        "AP_class_gate":gate,
        "fit_lock":{"filename":lock.name,"sha256":sha256_file(lock),"size_bytes":lock.stat().st_size},
        "consensus_definition":cfg["consensus"],
    }
    save_json(out/cfg["output_names"]["fit_gate_json"],payload)
    print("FIT LOCK PASS:",lock.name,sha256_file(lock),flush=True)
    print("AP class gate:",gate,flush=True)

def run_full(cfg,root,out,fit_gate_dir):
    gatep=fit_gate_dir/cfg["output_names"]["fit_gate_json"]
    if not gatep.is_file():
        raise RuntimeError("fit gate JSON missing")
    gate=json.loads(gatep.read_text())
    if gate["technical_status"]!="PASS":
        raise RuntimeError("fit gate not PASS")
    lockp=fit_gate_dir/cfg["output_names"]["fit_lock_npz"]
    if sha256_file(lockp)!=gate["fit_lock"]["sha256"]:
        raise RuntimeError("fit lock SHA mismatch")

    out.mkdir(parents=True,exist_ok=False)
    apply_env(cfg)

    import torch
    import torch.nn.functional as F
    from torch.utils.data import DataLoader,Subset
    from torchvision import datasets,transforms

    sys.path.insert(0,str(root))
    from TSPG_cross_family_pe_operator_v1_0_20260828 import zeros_native,forward_with_native_delta
    from TSPG_h1_0019_consensus_thirdfold_v1_0_20260829 import score_from_projections,paired_bootstrap_curve
    from TSPG_h1_0007_dual_blocksolve_ridge_fraction_alibi_control_v1_1_20260828 import ga_matmat_vmap_streaming

    sp=root/cfg["split_manifest"]["filename"]
    if sha256_file(sp)!=cfg["split_manifest"]["sha256"]:
        raise RuntimeError("split manifest SHA mismatch")
    split=json.loads(sp.read_text())
    IAP=split["indices"][cfg["split_manifest"]["AP_key"]]
    Cidx=split["indices"]["calibration_C"][:cfg["bbar"]["calibration_images"]]

    # Raw fit gradients and frozen arm bases are constructed BEFORE AP gradient compute.
    g1p=locate_locked(cfg["fit_sources"]["AG1_gradients"],root)
    g2p=locate_locked(cfg["fit_sources"]["AG2_gradients"],root)
    G1=np.load(g1p,mmap_mode="r")
    G2=np.load(g2p,mmap_mode="r")
    with np.load(lockp) as z:
        A={
            "U320_AG1":np.asarray(z["A_U320_AG1"],dtype=np.float64),
            "U320_AG2":np.asarray(z["A_U320_AG2"],dtype=np.float64),
            "U640":np.asarray(z["A_U640"],dtype=np.float64),
            "CONS640":np.asarray(z["A_CONS640"],dtype=np.float64),
        }

    print("STAGE A — CONSTRUCT FROZEN FIT ARM BASES BEFORE AP GRADIENTS",flush=True)
    Q={}
    for name in ["U320_AG1","U320_AG2","U640","CONS640"]:
        print("arm:",name,flush=True)
        Q[name]=construct_basis_from_dual(G1,G2,A[name],block=8)
        err=float(np.max(np.abs(Q[name].T@Q[name]-np.eye(32))))
        print("  orth err:",err,flush=True)
        if err>1e-9:
            raise RuntimeError(f"{name} basis orthonormality failed {err}")
    armraw=out/cfg["output_names"]["arm_basis_npz"]
    np.savez(armraw,**Q)
    arm_sha=sha256_file(armraw)
    print("Frozen arm basis SHA:",arm_sha,flush=True)

    print("\nSTAGE B — MODEL / DATASET",flush=True)
    ds=build_dataset(Path(cfg["val_dir"]),datasets,transforms)
    model,cp=load_model(cfg,root,torch)
    device=torch.device(cfg["runtime"]["device"])

    # Concatenate frozen bases for projection only.
    order=["U320_AG1","U320_AG2","U640","CONS640"]
    Dall=np.concatenate([Q[n] for n in order],axis=1)
    Dtorch=torch.from_numpy(Dall).to(device=device,dtype=torch.float64)

    print("\nSTAGE C — EXACTLY 640 NEW AP FP64 TASK GRADIENTS",flush=True)
    loader=DataLoader(Subset(ds,list(IAP)),batch_size=1,shuffle=False,num_workers=0,pin_memory=False)
    G=np.empty((640,cfg["native_d"]),dtype=np.float64)
    projections={n:np.empty((640,32),dtype=np.float64) for n in order}
    total_norm2=np.empty(640,dtype=np.float64)
    losses=np.empty(640,dtype=np.float64)
    t0=time.time()
    if torch.cuda.is_available():
        torch.cuda.empty_cache(); torch.cuda.reset_peak_memory_stats()
    for i,(images,labels) in enumerate(loader):
        images=images.to(device=device,dtype=torch.float64)
        labels=labels.to(device)
        delta=zeros_native(model,"learned",device).to(dtype=torch.float64).requires_grad_(True)
        logits=forward_with_native_delta(model,images,delta,"learned",backend="math")
        loss=F.cross_entropy(logits,labels,reduction="sum")
        g=torch.autograd.grad(loss,delta)[0].reshape(-1)
        gv=g.detach()
        G[i,:]=gv.cpu().numpy()
        total_norm2[i]=float(torch.dot(gv,gv).item())
        pv=(gv@Dtorch).detach().cpu().numpy()
        for ai,name in enumerate(order):
            projections[name][i,:]=pv[ai*32:(ai+1)*32]
        losses[i]=float(loss.detach().item())
        if (i+1)%cfg["AP_gradients"]["progress_every"]==0:
            print(f"[AP gradient] {i+1}/640 elapsed={time.time()-t0:.1f}s",flush=True)

    grad_elapsed=time.time()-t0
    gradraw=out/cfg["output_names"]["AP_gradients"]
    np.save(gradraw,G,allow_pickle=False)
    grad_sha=sha256_file(gradraw)
    peak=int(torch.cuda.max_memory_allocated()) if torch.cuda.is_available() else None

    print("\nSTAGE D — TASK-ONLY AP SCORING / BOOTSTRAP",flush=True)
    scores,per=score_from_projections(
        projections,total_norm2,cfg["reporting"]["secondary_k"],cfg["reporting"]["primary_k"]
    )
    boot=paired_bootstrap_curve(
        per,total_norm2,cfg["reporting"]["primary_k"],
        cfg["success_rule"]["bootstrap_replicates"],cfg["success_rule"]["bootstrap_seed"]
    )
    primary=cfg["reporting"]["primary_k"]
    allpos=all(boot["point_by_k"][int(k)]>0 for k in primary)
    cilow=float(boot["curve_bootstrap_ci95"][0])
    success=bool(allpos and cilow>0)
    status=cfg["success_rule"]["success_status"] if success else cfg["success_rule"]["failure_status"]

    # Sample-size decomposition.
    sample={}
    cons={}
    for k in cfg["reporting"]["secondary_k"]+primary:
        u320mean=0.5*(scores["U320_AG1"][k]+scores["U320_AG2"][k])
        sample[str(k)]={
            "U320_AG1":scores["U320_AG1"][k],
            "U320_AG2":scores["U320_AG2"][k],
            "U320_MEAN":u320mean,
            "U640":scores["U640"][k],
            "Delta_sample_U640_minus_U320mean":scores["U640"][k]-u320mean,
        }
        cons[str(k)]={
            "U640":scores["U640"][k],
            "CONS640":scores["CONS640"][k],
            "Delta_cons":scores["CONS640"][k]-scores["U640"][k],
        }

    print("Consensus status:",status,flush=True)
    for k in primary:
        print(f"k={k}: U640={scores['U640'][k]:.6f} CONS={scores['CONS640'][k]:.6f} "
              f"delta={scores['CONS640'][k]-scores['U640'][k]:+.6f}",flush=True)
    print("curve bootstrap CI95:",boot["curve_bootstrap_ci95"],flush=True)

    perraw=out/cfg["output_names"]["per_example_npz"]
    np.savez_compressed(
        perraw,total_norm2=total_norm2,losses=losses,
        **{f"proj_{name}":projections[name] for name in order},
        **{f"capture_{name}_k{k}":per[name][k] for name in order for k in cfg["reporting"]["secondary_k"]+primary}
    )

    print("\nSTAGE E — POST-FIT BBAR DIAGNOSTIC ONLY",flush=True)
    bbar={}
    qdiag={}
    chunk=cfg["bbar"]["direction_chunk_size"]
    for name in order:
        print("bbar arm:",name,flush=True)
        q=np.empty(32,dtype=np.float64)
        qdirect=np.empty(32,dtype=np.float64)
        blocks=[]
        for s in range(0,32,chunk):
            e=min(s+chunk,32)
            Dt=torch.from_numpy(Q[name][:,s:e]).to(device=device,dtype=torch.float64)
            rr=ga_matmat_vmap_streaming(
                model,ds,Cidx,"learned",Dt,device,cfg["runtime"]["calibration_batch_size"]
            )
            q[s:e]=np.asarray(rr["q_dot"],dtype=np.float64)
            qdirect[s:e]=np.asarray(rr["q_direct"],dtype=np.float64)
            rel=np.abs(q[s:e]-qdirect[s:e])/np.maximum(np.abs(qdirect[s:e]),1e-30)
            blocks.append({
                "start":s,"stop":e,"elapsed_sec":rr["elapsed_sec"],
                "quadratic_consistency_relative_max":float(np.max(rel))
            })
            print(f"  cols {e}/32 qrel={float(np.max(rel)):.3e}",flush=True)
            if float(np.max(rel))>cfg["bbar"]["quadratic_consistency_relative_gate"]:
                raise RuntimeError("bbar quadratic consistency failed")
        qb=q+float(cfg["bbar"]["alpha"])
        bbar[name]={str(k):float(np.mean(qb[:k])) for k in cfg["reporting"]["secondary_k"]+primary}
        qdiag[name]={"q_A":[float(x) for x in q],"q_direct":[float(x) for x in qdirect],"blocks":blocks}

    result={
        "schema":"TSPG_H1_0019_RESULT_v1_0",
        "run_id":cfg["run_id"],
        "technical_status":"PASS",
        "scientific_status":status,
        "confirmatory_H1_status":"BLOCKED",
        "fit_lock":{
            "path":str(lockp),"sha256":gate["fit_lock"]["sha256"],
            "arm_basis_path":str(armraw),"arm_basis_sha256":arm_sha,
            "AP_gradients_before_arm_lock":0
        },
        "AP":{
            "count":640,
            "class_gate":gate["AP_class_gate"],
            "gradients":{"filename":gradraw.name,"sha256":grad_sha,"size_bytes":gradraw.stat().st_size},
            "gradient_elapsed_sec":grad_elapsed,
            "peak_cuda_memory_bytes":peak,
            "consumed_as_C1_development_heldout":True
        },
        "task_capture":{
            "scores":{a:{str(k):v for k,v in d.items()} for a,d in scores.items()},
            "sample_size_decomposition":sample,
            "consensus_decomposition":cons,
            "paired_bootstrap":boot,
            "success_rule":cfg["success_rule"],
        },
        "bbar":{
            "role":"POST_FIT_DIAGNOSTIC_ONLY_NOT_USED_IN_SELECTION_OR_AP_SCORING",
            "new_GA_directions":128,
            "alpha":cfg["bbar"]["alpha"],
            "by_arm":bbar,
            "quadratic_diagnostics":qdiag,
        },
        "planning_forecast_H18":{
            "role":"PLANNING_ONLY_NOT_H19_CONTROL",
            "forecast_640":json.loads((root/cfg["fit_sources"]["H18_result"]["filename"]).read_text())["forecast_640_planning_only"]
        },
        "outputs":{
            "per_example":{"filename":perraw.name,"sha256":sha256_file(perraw)},
            "arm_basis":{"filename":armraw.name,"sha256":arm_sha}
        },
        "prohibitions_respected":{
            "no_alternate_consensus_after_AP":True,
            "B_or_GA_not_used_in_fit":True,
            "B_or_GA_not_used_in_AP_task_score":True,
            "actual_U640_used":True,
            "no_primary_k_dropped":True
        }
    }
    rp=out/cfg["output_names"]["result_json"]
    save_json(rp,result)
    print("\nH1-0019 TECHNICAL STATUS: PASS",flush=True)
    print("SCIENTIFIC STATUS:",status,flush=True)
    print("Confirmatory H1 remains BLOCKED.",flush=True)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--config",type=Path,required=True)
    ap.add_argument("--root",type=Path,required=True)
    ap.add_argument("--output-dir",type=Path,required=True)
    ap.add_argument("--stage",choices=["fit_gate","full"],required=True)
    ap.add_argument("--fit-gate-dir",type=Path)
    a=ap.parse_args()
    cfg=json.loads(a.config.read_text())
    root=a.root.resolve()
    if a.stage=="fit_gate":
        run_fit_gate(cfg,root,a.output_dir.resolve())
    else:
        if a.fit_gate_dir is None:
            raise RuntimeError("--fit-gate-dir required")
        run_full(cfg,root,a.output_dir.resolve(),a.fit_gate_dir.resolve())

if __name__=="__main__":
    main()
