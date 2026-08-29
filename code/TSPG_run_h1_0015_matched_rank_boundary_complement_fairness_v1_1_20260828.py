#!/usr/bin/env python3
from pathlib import Path
import argparse,json,importlib,sys,os
import numpy as np
import torch
from torchvision import datasets,transforms

from TSPG_h1_0015_matched_rank_boundary_complement_fairness_v1_1_20260828 import (
    sha256_file,locate_locked_raw,deterministic_qr,project_complement,
    coupling_diagnostics,residual_map,build_augmented,
    orthonormalize_union_with_actions,euclidean_top4_overlap,
    B_top4_overlap_same_metric
)
from TSPG_h1_0007_dual_blocksolve_ridge_fraction_alibi_control_v1_1_20260828 import (
    ga_matmat_vmap_streaming
)

MODEL_KWARGS=dict(embed_dim=768,depth=12,num_heads=12,mlp_ratio=4.0,dropout=0.0)

def save(p,o):
    p.write_text(json.dumps(o,indent=2),encoding="utf-8")

def build_dataset(val_dir):
    tfm=transforms.Compose([
        transforms.Resize(256),transforms.CenterCrop(224),transforms.ToTensor(),
        transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
    ])
    ds=datasets.ImageFolder(val_dir,transform=tfm)
    if len(ds)!=5000: raise RuntimeError(f"unexpected dataset size {len(ds)}")
    return ds

def load_model(source,checkpoint,device):
    sdir=str(Path(source).parent.resolve())
    if sdir not in sys.path: sys.path.insert(0,sdir)
    mod=importlib.import_module("full_scale_experiment")
    m=mod.VisionTransformer(
        **MODEL_KWARGS,img_size=224,patch_size=16,
        num_classes=100,pe_type="learned"
    ).to(device)
    state=torch.load(checkpoint,map_location=device,weights_only=False)
    if isinstance(state,dict) and "model_state_dict" in state:
        state=state["model_state_dict"]
    state={k.replace("_orig_mod.",""):v for k,v in state.items()}
    res=m.load_state_dict(state,strict=True)
    if res.missing_keys or res.unexpected_keys: raise RuntimeError(res)
    m.eval()
    for p in m.parameters(): p.requires_grad_(False)
    return m.double()

def exact_ga_block(model,ds,Cidx,X,device,batch_size,chunk):
    outs=[]; qrels=[]; records=[]
    for start in range(0,X.shape[1],chunk):
        stop=min(start+chunk,X.shape[1])
        print(f"    [GA TAIL] cols {start+1:02d}-{stop:02d}/{X.shape[1]}",flush=True)
        Dt=torch.from_numpy(np.asarray(X[:,start:stop],dtype=np.float64)).to(
            device=device,dtype=torch.float64
        )
        br=ga_matmat_vmap_streaming(
            model,ds,Cidx,"learned",Dt,device,batch_size
        )
        Gv=br["ga_V"].detach().cpu().numpy()
        q=np.asarray(br["q_dot"]); qd=np.asarray(br["q_direct"])
        qr=np.abs(q-qd)/np.maximum(np.abs(qd),1e-30)
        outs.append(Gv); qrels.extend([float(x) for x in qr])
        records.append({
            "start_col_1based":start+1,"stop_col_1based":stop,
            "elapsed_sec":br["elapsed_sec"],
            "peak_cuda_memory_bytes":br["peak_cuda_memory_bytes"],
            "quadratic_consistency_relative_max":float(qr.max())
        })
    return np.column_stack(outs),records,max(qrels) if qrels else 0.0

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--config",type=Path,required=True)
    ap.add_argument("--root",type=Path,required=True)
    ap.add_argument("--output-dir",type=Path,required=True)
    a=ap.parse_args()

    cfg=json.loads(a.config.read_text())
    for k,v in cfg["environment_required"].items():
        if os.environ.get(k)!=v:
            raise RuntimeError(f"environment {k}: {os.environ.get(k)} != {v}")

    root=a.root.resolve(); out=a.output_dir.resolve()
    out.mkdir(parents=True,exist_ok=False)

    print("STAGE A — SHA-LOCKED RAW SOURCES",flush=True)
    s10=cfg["source_raw_artifacts"]["task_span"]
    s11=cfg["source_raw_artifacts"]["head_complement"]
    p10,c10=locate_locked_raw(s10["filename"],s10["sha256"],[root,root.parent,root.parent.parent])
    p11,c11=locate_locked_raw(s11["filename"],s11["sha256"],[root,root.parent,root.parent.parent])
    print("H1-0010:",p10,flush=True)
    print("H1-0011 HEAD:",p11,flush=True)

    d10=np.load(p10,mmap_mode="r")
    d11=np.load(p11,mmap_mode="r")
    for n in s10["required_arrays"]:
        if n not in d10.files: raise RuntimeError(f"missing {n}")
    for n in s11["required_arrays"]:
        if n not in d11.files: raise RuntimeError(f"missing {n}")

    Q=np.asarray(d10["Q320"],dtype=np.float64)
    C=np.asarray(d10["C320"],dtype=np.float64)
    GAQ=np.asarray(d10["GA_Q320"],dtype=np.float64)
    A=np.asarray(d10["A320"],dtype=np.float64)
    Zhead=np.asarray(d11["Z_complement"],dtype=np.float64)
    GAZhead=np.asarray(d11["GA_Z_complement"],dtype=np.float64)
    if Zhead.shape[1]!=s11["expected_dimension"]:
        raise RuntimeError(f"HEAD dimension {Zhead.shape}")

    alpha=float(cfg["locked_metric"]["alpha_tau_over_d"])

    print("\nSTAGE B — OFFLINE TAIL SEED RANKS 5-8",flush=True)
    cd=coupling_diagnostics(Q,GAQ,A,C,alpha)
    Vc=cd["coupling_right_vectors"][:,4:8]
    Vt=cd["restricted_generalized_vectors"][:,4:8]
    Vinit=np.column_stack([Vc,Vt])
    Zraw=residual_map(Q,GAQ,A,Vinit)
    Zraw=project_complement(Q,Zraw,None)
    Z0,qr0,_=deterministic_qr(
        Zraw,cfg["tail_seed"]["qr_relative_diagonal_rank_tolerance"]
    )
    print("TAIL initial rank:",qr0["retained_rank"],flush=True)
    if Z0.shape[1]==0:
        raise RuntimeError("TAIL initial rank zero")

    print("coupling singular values ranks1-8:",
          [float(x) for x in cd["coupling_singular_values_desc"][:8]],flush=True)
    print("restricted generalized lambda ranks1-8:",
          [float(x) for x in cd["restricted_generalized_eigenvalues"][:8]],flush=True)

    print("\nSTAGE C — MODEL / CALIBRATION LOAD",flush=True)
    man=json.loads((root/cfg["checkpoint_manifest"]).read_text())
    split=json.loads((root/cfg["split_manifest"]).read_text())
    dev=man["seed42_development_checkpoints"]["learned"]
    cp=Path(dev["path"])
    if sha256_file(cp)!=dev["sha256"]: raise RuntimeError("checkpoint hash mismatch")
    source=Path(cfg["model_source"]["path"])
    if sha256_file(source)!=cfg["model_source"]["sha256"]:
        raise RuntimeError("model source hash mismatch")
    device=torch.device(cfg["runtime"]["device"])
    ds=build_dataset(Path(cfg["val_dir"]))
    model=load_model(source,cp,device)
    Cidx=split["indices"]["calibration_C"][:cfg["tail_krylov"]["calibration_images"]]

    print("\nSTAGE D — MATCHED FOUR-BLOCK TAIL KRYLOV",flush=True)
    Zblocks=[]; GAZblocks=[]; block_meta=[]
    current=Z0
    tail_intermediate=[]

    for level in range(cfg["tail_krylov"]["max_blocks"]):
        print(f"[TAIL KRYLOV] block {level+1}/4 rank={current.shape[1]}",flush=True)
        GAZ,records,qrel=exact_ga_block(
            model,ds,Cidx,current,device,
            cfg["runtime"]["calibration_batch_size"],
            cfg["tail_krylov"]["ga_direction_chunk_size"]
        )
        if qrel>cfg["tail_krylov"]["block_quadratic_consistency_gate"]:
            raise RuntimeError("TAIL quadratic consistency failed")

        Zprev=np.column_stack(Zblocks) if Zblocks else np.zeros((Q.shape[0],0))
        qorth=float(np.max(np.abs(Q.T@current))) if current.shape[1] else 0.0
        zorth=float(np.max(np.abs(Zprev.T@current))) if Zprev.shape[1] else 0.0
        if qorth>cfg["tail_krylov"]["Q_orthogonality_gate"]:
            raise RuntimeError(f"Q/TAIL orthogonality failed {qorth}")
        if zorth>cfg["tail_krylov"]["Z_orthogonality_gate"]:
            raise RuntimeError(f"TAIL block orthogonality failed {zorth}")

        Zblocks.append(current); GAZblocks.append(GAZ)
        Ztail=np.column_stack(Zblocks); GAZtail=np.column_stack(GAZblocks)
        L=level+1
        aug=build_augmented(
            Q,C,A,GAQ,Ztail,GAZtail,alpha,
            cfg["endpoint"]["top_eigenvalues_report"],
            cfg["endpoint"]["top_subspace_k"]
        )
        tail_intermediate.append({
            "L":L,
            "complement_dimension":int(Ztail.shape[1]),
            "lambda_1_to_12":aug["lambda_1_to_12"],
            "gap_4_5_rel":aug["gap_4_5_rel"],
            "lambda4_over_lambda5":aug["lambda4_over_lambda5"]
        })
        print(
            f"  L={L} dim={aug['dimension']} "
            f"lambda4={aug['lambda_1_to_12'][3]:.6g} "
            f"lambda5={aug['lambda_1_to_12'][4]:.6g} "
            f"gap4_rel={aug['gap_4_5_rel']:.6g}",
            flush=True
        )

        block_meta.append({
            "L":L,"rank":int(current.shape[1]),
            "q_orthogonality_max_abs":qorth,
            "previous_tail_orthogonality_max_abs":zorth,
            "ga_records":records
        })

        if L>=cfg["tail_krylov"]["max_blocks"]:
            break
        W=project_complement(Q,GAZ,Ztail)
        nxt,qrmeta,_=deterministic_qr(
            W,cfg["tail_seed"]["qr_relative_diagonal_rank_tolerance"]
        )
        block_meta[-1]["next_block_qr"]=qrmeta
        if nxt.shape[1]==0:
            raise RuntimeError("TAIL block-Krylov exhausted before matched L=4 endpoint")
        current=nxt

    Ztail=np.column_stack(Zblocks)
    GAZtail=np.column_stack(GAZblocks)
    if len(Zblocks)!=4:
        raise RuntimeError("Matched four-block endpoint not reached")

    print("\nSTAGE E — BASELINE / HEAD / TAIL / COMBINED ENDPOINTS",flush=True)
    Zempty=np.zeros((Q.shape[0],0),dtype=np.float64)
    baseline=build_augmented(
        Q,C,A,GAQ,Zempty,Zempty,alpha,
        cfg["endpoint"]["top_eigenvalues_report"],
        cfg["endpoint"]["top_subspace_k"]
    )
    head=build_augmented(
        Q,C,A,GAQ,Zhead,GAZhead,alpha,
        cfg["endpoint"]["top_eigenvalues_report"],
        cfg["endpoint"]["top_subspace_k"]
    )
    tail=build_augmented(
        Q,C,A,GAQ,Ztail,GAZtail,alpha,
        cfg["endpoint"]["top_eigenvalues_report"],
        cfg["endpoint"]["top_subspace_k"]
    )

    Zcomb,GAZcomb,comb_qr,comb_recon=orthonormalize_union_with_actions(
        Q,[Zhead,Ztail],[GAZhead,GAZtail],
        cfg["endpoint"]["combined_qr_relative_diagonal_rank_tolerance"]
    )
    if comb_recon>1e-10:
        raise RuntimeError(f"combined QR reconstruction error {comb_recon}")

    combined=build_augmented(
        Q,C,A,GAQ,Zcomb,GAZcomb,alpha,
        cfg["endpoint"]["top_eigenvalues_report"],
        cfg["endpoint"]["top_subspace_k"]
    )

    for name,obj in [("BASELINE_L0",baseline),("HEAD",head),("TAIL",tail),("COMBINED",combined)]:
        if obj["B_orthonormality_max_abs"]>cfg["endpoint"]["B_orthonormality_gate"]:
            raise RuntimeError(f"{name} B-orth gate")
        if obj["projected_generalized_residual_max"]>cfg["endpoint"]["generalized_residual_gate"]:
            raise RuntimeError(f"{name} projected residual gate")

    head_tail_overlap=euclidean_top4_overlap(Zhead,Ztail[:,:min(4,Ztail.shape[1])]) if False else None

    e_overlap=euclidean_top4_overlap(
        head["top4_full_vectors"],combined["top4_full_vectors"]
    )
    b_overlap=B_top4_overlap_same_metric(
        head["top4_full_vectors"],combined["top4_B_vectors"]
    )

    # Complement-space overlap itself, Euclidean principal cosines.
    Qh,_=np.linalg.qr(Zhead,mode="reduced")
    Qt,_=np.linalg.qr(Ztail,mode="reduced")
    cs=np.linalg.svd(Qh.T@Qt,compute_uv=False)
    cs=np.clip(cs,0.0,1.0)

    raw=out/"TSPG_H1_0015_LEARNED_SEED42_TAIL_RANK5_8_COMPLEMENT_KRYLOV_L4_v1_0.npz"
    np.savez(
        raw,
        tail_initial_task_vectors=Vinit,
        Z_tail_complement=Ztail,
        GA_Z_tail_complement=GAZtail,
        Z_combined_complement=Zcomb,
        GA_Z_combined_complement=GAZcomb
    )

    hvals=np.asarray(head["lambda_1_to_12"])
    tvals=np.asarray(tail["lambda_1_to_12"])
    cvals=np.asarray(combined["lambda_1_to_12"])

    result={
        "schema":"TSPG_H1_0015_RESULT_v1",
        "run_id":cfg["run_id"],
        "technical_status":"PASS",
        "scientific_H1_status":cfg["scientific_H1_status"],
        "source_raw_artifacts":{
            "task_span":{"path":str(p10),"sha256":s10["sha256"],"checked":c10},
            "head_complement":{"path":str(p11),"sha256":s11["sha256"],"checked":c11}
        },
        "tail_seed":{
            "coupling_singular_values_ranks1_8":
                [float(x) for x in cd["coupling_singular_values_desc"][:8]],
            "restricted_generalized_lambda_ranks1_8":
                [float(x) for x in cd["restricted_generalized_eigenvalues"][:8]],
            "initial_QR":qr0
        },
        "tail_krylov_blocks":block_meta,
        "tail_intermediate":tail_intermediate,
        "matched_endpoint":{
            "BASELINE_L0":{
                **{k:v for k,v in baseline.items()
                   if k not in {"top4_full_vectors","top4_B_vectors"}},
                "interpretation_role":"UNCONTAMINATED_SPECTRAL_REFERENCE"
            },
            "HEAD":{
                **{k:v for k,v in head.items()
                   if k not in {"top4_full_vectors","top4_B_vectors"}},
                "interpretation_role":"TOP4_TARGET_CONDITIONED_MATCHED_L4"
            },
            "TAIL":{
                k:v for k,v in tail.items()
                if k not in {"top4_full_vectors","top4_B_vectors"}
            },
            "COMBINED":{
                k:v for k,v in combined.items()
                if k not in {"top4_full_vectors","top4_B_vectors"}
            },
            "combined_QR":comb_qr,
            "combined_QR_reconstruction_max_abs":comb_recon,
            "combined_over_HEAD_lambda_ratios_ranks1_8":
                [float(x) for x in (cvals[:8]/hvals[:8])],
            "TAIL_over_HEAD_lambda_ratios_ranks1_8":
                [float(x) for x in (tvals[:8]/hvals[:8])],
            "HEAD_vs_COMBINED_top4_euclidean_principal_cosines":
                e_overlap,
            "HEAD_vs_COMBINED_top4_B_principal_cosines":
                b_overlap,
            "HEAD_vs_TAIL_complement_principal_cosines":
                [float(x) for x in cs]
        },
        "raw_output":{
            "filename":raw.name,
            "sha256":sha256_file(raw),
            "size_bytes":raw.stat().st_size,
            "included_in_compact_evidence_zip":False
        },
        "new_GA_direction_budget_max":32,
        "c_changed":False,
        "k_changed":False,
        "confirmatory_execution_performed":False,
        "claim_restrictions":cfg["claim_restrictions"],
        "random_range_R_branch_performed":False
    }
    save(out/"TSPG_H1_0015_RESULT_v1_1_20260828.json",result)
    print("\nH1-0015 TECHNICAL STATUS: PASS",flush=True)
    print("BASELINE_L0 gap4_rel:",baseline["gap_4_5_rel"],flush=True)
    print("HEAD gap4_rel:",head["gap_4_5_rel"],flush=True)
    print("TAIL gap4_rel:",tail["gap_4_5_rel"],flush=True)
    print("COMBINED gap4_rel:",combined["gap_4_5_rel"],flush=True)
    print("raw:",raw,flush=True)

if __name__=="__main__":
    main()
