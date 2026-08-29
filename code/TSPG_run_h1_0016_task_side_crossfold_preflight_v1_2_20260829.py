#!/usr/bin/env python3
from pathlib import Path
import argparse, json, hashlib, os, sys, time
import numpy as np

def sha256_file(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""):
            h.update(c)
    return h.hexdigest()

def save_json(p,o):
    p.write_text(json.dumps(o,indent=2),encoding="utf-8")

def locate_locked(filename, expected_sha, root, known_path=None):
    candidates=[]
    if known_path:
        candidates.append(Path(known_path))
    candidates += [root/filename, root.parent/filename]
    seen=set()
    for p in candidates:
        p=p.expanduser()
        if str(p) in seen: continue
        seen.add(str(p))
        if p.is_file():
            got=sha256_file(p)
            if got==expected_sha:
                return p.resolve(), [{"path":str(p.resolve()),"sha256":got}]
    base=Path("/home/djoko.bandjur.ftnkm/Notebooks/TSPG")
    checked=[]
    if base.is_dir():
        for p in base.glob(f"**/{filename}"):
            if not p.is_file(): continue
            got=sha256_file(p)
            checked.append({"path":str(p.resolve()),"sha256":got})
            if got==expected_sha:
                return p.resolve(),checked
    raise RuntimeError(f"SHA-locked source not found: {filename}; checked={checked[:8]}")

def apply_env(cfg):
    for k,v in cfg["environment_required"].items():
        os.environ[k]=v
    for k in ["TORCHINDUCTOR_CACHE_DIR","TRITON_CACHE_DIR","XDG_CACHE_HOME"]:
        Path(os.environ[k]).mkdir(parents=True,exist_ok=True)

def load_runtime_modules(root):
    import torch
    import torch.nn.functional as F
    from torch.utils.data import DataLoader,Subset
    from torchvision import datasets,transforms
    sys.path.insert(0,str(root))
    from TSPG_cross_family_pe_operator_v1_0_20260828 import (
        zeros_native,forward_with_native_delta
    )
    from TSPG_h1_0016_task_side_crossfold_preflight_v1_2_20260829 import (
        class_composition_gate,task_crossfold_metrics,validate_identities
    )
    return torch,F,DataLoader,Subset,datasets,transforms,zeros_native,forward_with_native_delta,class_composition_gate,task_crossfold_metrics,validate_identities

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
    import importlib
    man=json.loads((root/cfg["checkpoint_manifest"]["filename"]).read_text())
    dev=man["seed42_development_checkpoints"]["learned"]
    cp=Path(dev["path"])
    if sha256_file(cp)!=dev["sha256"]:
        raise RuntimeError("Learned seed42 checkpoint SHA mismatch")
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
    for p in m.parameters():
        p.requires_grad_(False)
    return m.double(),cp

def scalar_task_gradients(model,ds,indices,device,torch,F,DataLoader,Subset,zeros_native,forward_with_native_delta,progress_every):
    loader=DataLoader(Subset(ds,list(indices)),batch_size=1,shuffle=False,num_workers=0,pin_memory=False)
    rows=[]; losses=[]; t0=time.time()
    if torch.cuda.is_available():
        torch.cuda.empty_cache(); torch.cuda.reset_peak_memory_stats()
    for j,(images,labels) in enumerate(loader,1):
        images=images.to(device=device,dtype=torch.float64)
        labels=labels.to(device)
        delta=zeros_native(model,"learned",device).to(dtype=torch.float64).requires_grad_(True)
        logits=forward_with_native_delta(model,images,delta,"learned",backend="math")
        loss=F.cross_entropy(logits,labels,reduction="sum")
        g=torch.autograd.grad(loss,delta)[0]
        rows.append(g.detach().cpu().reshape(-1))
        losses.append(float(loss.detach().item()))
        if j%progress_every==0 or j==len(indices):
            print(f"[AG2 task gradients] {j}/{len(indices)} elapsed={time.time()-t0:.1f}s",flush=True)
        del images,labels,delta,logits,loss,g
    G=torch.stack(rows,dim=0).double().numpy()
    return G,losses,float(time.time()-t0),(
        int(torch.cuda.max_memory_allocated()) if torch.cuda.is_available() else None
    )

def run_gate(cfg,root,out):
    # Runtime compatibility must succeed before any gate artifact exists.
    torch,F,DataLoader,Subset,datasets,transforms,zeros_native,forward_with_native_delta,class_gate,task_metrics,validate_ids = load_runtime_modules(root)
    out.mkdir(parents=True,exist_ok=False)

    split_path=root/cfg["split_manifest"]["filename"]
    if sha256_file(split_path)!=cfg["split_manifest"]["sha256"]:
        raise RuntimeError("split manifest SHA mismatch")
    split=json.loads(split_path.read_text())
    I1=split["indices"][cfg["folds"]["AG1_manifest_key"]]
    I2=split["indices"][cfg["folds"]["AG2_manifest_key"]]
    if len(I1)!=320 or len(I2)!=320 or set(I1)&set(I2):
        raise RuntimeError("AG1/AG2 index identity/disjointness gate failed")

    ds=build_dataset(Path(cfg["val_dir"]),datasets,transforms)
    if len(ds.classes)!=cfg["class_composition_hard_gate"]["dataset_classes"]:
        raise RuntimeError("dataset class-count gate failed")
    cg=class_gate(
        ds.targets,I1,I2,len(ds.classes),
        cfg["class_composition_hard_gate"]["minimum_fraction"]
    )

    meta=json.loads((root/cfg["AG1_source_gradients"]["metadata_filename"]).read_text())
    if sha256_file(root/cfg["AG1_source_gradients"]["metadata_filename"])!=cfg["AG1_source_gradients"]["metadata_sha256"]:
        raise RuntimeError("AG1 metadata SHA mismatch")
    if meta["sample_indices"]!=I1 or meta["sha256"]!=cfg["AG1_source_gradients"]["sha256"]:
        raise RuntimeError("AG1 metadata-to-split provenance gate failed")

    h10r=json.loads((root/cfg["H1_0010_task_basis_source"]["result_filename"]).read_text())
    if sha256_file(root/cfg["H1_0010_task_basis_source"]["result_filename"])!=cfg["H1_0010_task_basis_source"]["result_sha256"]:
        raise RuntimeError("H1-0010 result JSON SHA mismatch")
    if h10r["source_task_gradients"]["sha256"]!=cfg["AG1_source_gradients"]["sha256"]:
        raise RuntimeError("H1-0010 AG1 gradient provenance mismatch")
    if h10r["raw_output"]["sha256"]!=cfg["H1_0010_task_basis_source"]["sha256"]:
        raise RuntimeError("H1-0010 raw basis provenance mismatch")

    gp,gchecked=locate_locked(
        cfg["AG1_source_gradients"]["filename"],
        cfg["AG1_source_gradients"]["sha256"],root,
        cfg["AG1_source_gradients"].get("known_path")
    )
    bp,bchecked=locate_locked(
        cfg["H1_0010_task_basis_source"]["filename"],
        cfg["H1_0010_task_basis_source"]["sha256"],root,
        cfg["H1_0010_task_basis_source"].get("known_path")
    )

    payload={
        "schema":"TSPG_H1_0016_GATE_RESULT_v1_2",
        "run_id":cfg["run_id"],
        "technical_status":"PASS" if cg["pass"] else cfg["class_composition_hard_gate"]["failure_status"],
        "new_task_gradients_computed":0,
        "class_composition":cg,
        "AG1_indices_sha256":hashlib.sha256(np.asarray(I1,dtype=np.int64).tobytes()).hexdigest(),
        "AG2_indices_sha256":hashlib.sha256(np.asarray(I2,dtype=np.int64).tobytes()).hexdigest(),
        "AG1_source":{"path":str(gp),"sha256":cfg["AG1_source_gradients"]["sha256"],"checked":gchecked},
        "H1_0010_basis_source":{"path":str(bp),"sha256":cfg["H1_0010_task_basis_source"]["sha256"],"checked":bchecked},
    }
    save_json(out/"TSPG_H1_0016_GATE_RESULT_v1_2_20260829.json",payload)
    print("AG1 unique classes:",cg["AG1_unique_classes"],flush=True)
    print("AG2 unique classes:",cg["AG2_unique_classes"],flush=True)
    print("class intersection:",cg["class_intersection_count"],flush=True)
    print("gate status:",payload["technical_status"],flush=True)
    if not cg["pass"]:
        raise SystemExit(12)

def run_full(cfg,root,out,gate_dir):
    gate_path=gate_dir/"TSPG_H1_0016_GATE_RESULT_v1_2_20260829.json"
    if not gate_path.is_file():
        raise RuntimeError("gate result missing")
    gate=json.loads(gate_path.read_text())
    if gate["technical_status"]!="PASS":
        raise RuntimeError("precompute hard gate not PASS")

    out.mkdir(parents=True,exist_ok=False)
    torch,F,DataLoader,Subset,datasets,transforms,zeros_native,forward_with_native_delta,class_gate,task_metrics,validate_ids = load_runtime_modules(root)

    split=json.loads((root/cfg["split_manifest"]["filename"]).read_text())
    I1=split["indices"][cfg["folds"]["AG1_manifest_key"]]
    I2=split["indices"][cfg["folds"]["AG2_manifest_key"]]

    gp,_=locate_locked(
        cfg["AG1_source_gradients"]["filename"],
        cfg["AG1_source_gradients"]["sha256"],root,
        cfg["AG1_source_gradients"].get("known_path")
    )
    bp,_=locate_locked(
        cfg["H1_0010_task_basis_source"]["filename"],
        cfg["H1_0010_task_basis_source"]["sha256"],root,
        cfg["H1_0010_task_basis_source"].get("known_path")
    )

    print("STAGE A — LOAD DATASET / MODEL",flush=True)
    ds=build_dataset(Path(cfg["val_dir"]),datasets,transforms)
    model,cp=load_model(cfg,root,torch)
    device=torch.device(cfg["runtime"]["device"])

    print("\nSTAGE B — EXACTLY 320 NEW AG2 FP64 TASK GRADIENTS",flush=True)
    G2,losses,grad_sec,peak=scalar_task_gradients(
        model,ds,I2,device,torch,F,DataLoader,Subset,zeros_native,forward_with_native_delta,
        cfg["task_gradient"]["progress_every"]
    )
    if list(G2.shape)!=[320,cfg["native_d"]] or str(G2.dtype)!="float64":
        raise RuntimeError(f"unexpected G2 {G2.shape} {G2.dtype}")
    G2raw=out/"TSPG_H1_0016_LEARNED_SEED42_AG2_320_FP64_TASK_GRADIENTS_v1_2.npy"
    np.save(G2raw,G2,allow_pickle=False)

    print("\nSTAGE C — DETERMINISTIC THIN QR FOR AG2",flush=True)
    t0=time.time()
    Q2,R2=np.linalg.qr(G2.T,mode="reduced")
    qr_elapsed=time.time()-t0
    RR=(R2@R2.T)/320.0
    C2=0.5*(RR+RR.T)
    q2orth=float(np.max(np.abs(Q2.T@Q2-np.eye(320))))
    print("Q2 orthonormality max abs:",q2orth,flush=True)

    print("\nSTAGE D — LOAD SHA-LOCKED H1-0010 Q1/C1",flush=True)
    with np.load(bp) as z:
        Q1=np.asarray(z["Q320"],dtype=np.float64)
        C1=np.asarray(z["C320"],dtype=np.float64)
    if Q1.shape!=(cfg["native_d"],320) or C1.shape!=(320,320):
        raise RuntimeError(f"unexpected H1-0010 Q/C shapes {Q1.shape} {C1.shape}")

    print("\nSTAGE E — OFFLINE CROSSFOLD ALGEBRA",flush=True)
    M=Q1.T@Q2
    metrics=task_metrics(C1,C2,M,tuple(cfg["reporting"]["primary_k"]))
    checks=validate_ids(metrics,1e-8)
    checks["Q2_orthonormality"] = bool(q2orth<=1e-10)
    if not all(checks.values()):
        raise RuntimeError(f"identity gate failed: {checks}")

    O_random=320.0/cfg["native_d"]
    phi12=metrics["phi_1_to_2"]; phi21=metrics["phi_2_to_1"]
    enrichment_span_12=phi12/metrics["O_span"] if metrics["O_span"]>0 else float("inf")
    enrichment_span_21=phi21/metrics["O_span"] if metrics["O_span"]>0 else float("inf")
    review_trigger=bool(enrichment_span_12<=2.0 or enrichment_span_21<=2.0)

    print("O_span:",metrics["O_span"],flush=True)
    print("O_random:",O_random,flush=True)
    print("phi 1->2:",phi12,"phi/O_span:",enrichment_span_12,flush=True)
    print("phi 2->1:",phi21,"phi/O_span:",enrichment_span_21,flush=True)
    print("A_phi:",metrics["A_phi"],flush=True)
    print("r_eff C1:",metrics["r_eff_C1"],flush=True)
    print("r_eff C2:",metrics["r_eff_C2"],flush=True)
    print("conditional transferred r_eff H21:",metrics["r_eff_H21_conditional_transferred"],flush=True)
    print("conditional transferred r_eff H12:",metrics["r_eff_H12_conditional_transferred"],flush=True)
    print("review trigger:",review_trigger,flush=True)

    raw=out/"TSPG_H1_0016_LEARNED_SEED42_AG1_AG2_TASK_CROSSFOLD_DERIVED_v1_2.npz"
    np.savez(
        raw,Q2=Q2,C2=C2,M=M,H21=metrics["H21"],H12=metrics["H12"],
        canonical_correlations=metrics["canonical_correlations"],
        eig_C1=metrics["eig_C1"],eig_C2=metrics["eig_C2"],
        eig_H21=metrics["eig_H21"],eig_H12=metrics["eig_H12"],
        T_1_to_2=metrics["T_1_to_2"],T_2_to_1=metrics["T_2_to_1"],
        U_task_1_to_2=metrics["U_task_1_to_2"],U_task_2_to_1=metrics["U_task_2_to_1"],
        eta_task_1_to_2=metrics["eta_task_1_to_2"],eta_task_2_to_1=metrics["eta_task_2_to_1"],
    )

    report_ks=cfg["reporting"]["primary_k"]+cfg["reporting"]["secondary_k"]
    def curve_rows(direction):
        if direction=="1_to_2":
            T=metrics["T_1_to_2"]; U=metrics["U_task_1_to_2"]; eta=metrics["eta_task_1_to_2"]; phi=phi12
        else:
            T=metrics["T_2_to_1"]; U=metrics["U_task_2_to_1"]; eta=metrics["eta_task_2_to_1"]; phi=phi21
        return [{
            "k":int(k),"T_cross":float(T[k-1]),"U_task_oracle":float(U[k-1]),
            "eta_task":float(eta[k-1]),"T_over_phi":float(T[k-1]/phi) if phi>0 else None
        } for k in report_ks]

    result={
        "schema":"TSPG_H1_0016_RESULT_v1_2",
        "run_id":cfg["run_id"],
        "technical_status":"PASS",
        "scientific_H1_status":cfg["scientific_H1_status"],
        "confirmatory_H1_status":cfg["confirmatory_H1_status"],
        "new_GA_actions":0,
        "new_AG2_task_gradients":320,
        "gate_result":{"path":str(gate_path),"sha256":sha256_file(gate_path),"class_composition":gate["class_composition"]},
        "sources":{
            "AG1_gradients":{"path":str(gp),"sha256":cfg["AG1_source_gradients"]["sha256"]},
            "H1_0010_Q1_C1":{"path":str(bp),"sha256":cfg["H1_0010_task_basis_source"]["sha256"]},
            "checkpoint":{"path":str(cp),"sha256":json.loads((root/cfg["checkpoint_manifest"]["filename"]).read_text())["seed42_development_checkpoints"]["learned"]["sha256"]},
        },
        "AG2_gradients":{
            "filename":G2raw.name,"sha256":sha256_file(G2raw),"size_bytes":G2raw.stat().st_size,
            "shape":[320,cfg["native_d"]],"dtype":"float64","sample_indices":[int(x) for x in I2],
            "elapsed_sec":grad_sec,"peak_cuda_memory_bytes":peak,"included_in_compact_evidence_zip":False
        },
        "AG2_QR":{"Q2_orthonormality_max_abs":q2orth,"elapsed_sec":float(qr_elapsed)},
        "full_span":{
            "canonical_correlations":[float(x) for x in metrics["canonical_correlations"]],
            "O_span":metrics["O_span"],"O_random":O_random,
            "sqrt_O_random":float(np.sqrt(O_random)),
            "role":"DESCRIPTIVE_NOT_GATE"
        },
        "coverage":{
            "phi_1_to_2":phi12,"phi_2_to_1":phi21,"A_phi":metrics["A_phi"],
            "phi_over_O_span_1_to_2":enrichment_span_12,
            "phi_over_O_span_2_to_1":enrichment_span_21,
            "phi_over_O_random_1_to_2":phi12/O_random,
            "phi_over_O_random_2_to_1":phi21/O_random,
            "review_trigger":review_trigger,
            "review_trigger_definition":cfg["review_trigger"]
        },
        "effective_rank":{
            "r_eff_C1_in_sample_planning_only":metrics["r_eff_C1"],
            "r_eff_C2_in_sample_planning_only":metrics["r_eff_C2"],
            "r_eff_H21_conditional_on_transferred_energy":metrics["r_eff_H21_conditional_transferred"],
            "r_eff_H12_conditional_on_transferred_energy":metrics["r_eff_H12_conditional_transferred"],
            "interpretation_lock":"report transferred r_eff only jointly with its phi"
        },
        "task_only_curves":{
            "reporting_1_to_2":curve_rows("1_to_2"),
            "reporting_2_to_1":curve_rows("2_to_1"),
            "full_T_1_to_2":[float(x) for x in metrics["T_1_to_2"]],
            "full_T_2_to_1":[float(x) for x in metrics["T_2_to_1"]],
            "full_U_task_1_to_2":[float(x) for x in metrics["U_task_1_to_2"]],
            "full_U_task_2_to_1":[float(x) for x in metrics["U_task_2_to_1"]],
            "full_eta_task_1_to_2":[float(x) for x in metrics["eta_task_1_to_2"]],
            "full_eta_task_2_to_1":[float(x) for x in metrics["eta_task_2_to_1"]],
            "identity_note":"T_320=phi and eta_320=1 by construction"
        },
        "leading_eigenspace_overlap":{
            "role":"ORACLE_VS_ORACLE_GEOMETRIC_DIAGNOSTIC",
            "by_k":metrics["leading_oracle_vs_oracle"]
        },
        "identity_gates":checks,
        "raw_derived":{
            "filename":raw.name,"sha256":sha256_file(raw),"size_bytes":raw.stat().st_size,
            "included_in_compact_evidence_zip":False
        },
        "expectations_not_gates":cfg["expectations_not_gates"],
        "prohibitions_respected":{
            "new_GA_action":True,"B_normalized_C1_not_run":True,"confirmatory_not_run":True,
            "folds_not_resampled":True,"c_not_changed":True
        }
    }
    save_json(out/"TSPG_H1_0016_RESULT_v1_2_20260829.json",result)
    print("\nH1-0016 TECHNICAL STATUS: PASS",flush=True)
    print("Confirmatory H1 remains BLOCKED pending ingest/discussion.",flush=True)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--config",type=Path,required=True)
    ap.add_argument("--root",type=Path,required=True)
    ap.add_argument("--output-dir",type=Path,required=True)
    ap.add_argument("--stage",choices=["gate","full"],required=True)
    ap.add_argument("--gate-dir",type=Path)
    a=ap.parse_args()
    cfg=json.loads(a.config.read_text())
    apply_env(cfg)
    root=a.root.resolve()
    if a.stage=="gate":
        run_gate(cfg,root,a.output_dir.resolve())
    else:
        if a.gate_dir is None: raise RuntimeError("--gate-dir required for full")
        run_full(cfg,root,a.output_dir.resolve(),a.gate_dir.resolve())

if __name__=="__main__":
    main()
