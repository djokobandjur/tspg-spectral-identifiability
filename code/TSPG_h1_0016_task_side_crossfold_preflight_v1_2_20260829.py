#!/usr/bin/env python3
import numpy as np

def sym(A):
    A=np.asarray(A,dtype=np.float64)
    return 0.5*(A+A.T)

def effective_rank_psd(A):
    A=sym(A)
    tr=float(np.trace(A))
    tr2=float(np.sum(A*A))
    return float((tr*tr)/tr2) if tr2>0 else 0.0

def eigh_desc(A):
    w,V=np.linalg.eigh(sym(A))
    order=np.argsort(w)[::-1]
    return w[order],V[:,order]

def class_composition_gate(targets, idx1, idx2, n_classes, min_fraction=0.95):
    targets=np.asarray(targets,dtype=np.int64)
    idx1=np.asarray(idx1,dtype=np.int64)
    idx2=np.asarray(idx2,dtype=np.int64)
    c1=np.bincount(targets[idx1],minlength=n_classes)
    c2=np.bincount(targets[idx2],minlength=n_classes)
    s1=set(np.flatnonzero(c1>0).tolist())
    s2=set(np.flatnonzero(c2>0).tolist())
    need=int(np.ceil(min_fraction*n_classes))
    result={
        "n_classes":int(n_classes),
        "minimum_required_classes":need,
        "AG1_unique_classes":len(s1),
        "AG2_unique_classes":len(s2),
        "class_intersection_count":len(s1&s2),
        "class_union_count":len(s1|s2),
        "AG1_class_histogram":[int(x) for x in c1],
        "AG2_class_histogram":[int(x) for x in c2],
        "pass":bool(len(s1)>=need and len(s2)>=need and len(s1&s2)>=need),
    }
    return result

def task_crossfold_metrics(C1,C2,M,report_ks=(1,2,4,8,16,32,64,128,320)):
    C1=sym(C1); C2=sym(C2); M=np.asarray(M,dtype=np.float64)
    r=C1.shape[0]
    if C1.shape!=(r,r) or C2.shape!=(r,r) or M.shape!=(r,r):
        raise ValueError("expected equal square reduced matrices")

    H21=sym(M@C2@M.T)
    H12=sym(M.T@C1@M)

    tr1=float(np.trace(C1)); tr2=float(np.trace(C2))
    phi12=float(np.trace(H21)/tr2)
    phi21=float(np.trace(H12)/tr1)

    Ospan=float(np.sum(M*M)/r)
    sM=np.linalg.svd(M,compute_uv=False)

    ew1,U1=eigh_desc(C1)
    ew2,U2=eigh_desc(C2)
    nu21,V21=eigh_desc(H21)
    nu12,V12=eigh_desc(H12)

    # train-fitted cumulative held-out energy
    diag12=np.diag(U1.T@H21@U1)
    diag21=np.diag(U2.T@H12@U2)
    T12=np.cumsum(diag12)/tr2
    T21=np.cumsum(diag21)/tr1

    U12=np.cumsum(nu21)/tr2
    U21=np.cumsum(nu12)/tr1

    eta12=np.divide(T12,U12,out=np.full_like(T12,np.nan),where=U12>0)
    eta21=np.divide(T21,U21,out=np.full_like(T21,np.nan),where=U21>0)

    leading={}
    for k in report_ks:
        if k<=r:
            s=np.linalg.svd(U1[:,:k].T@M@U2[:,:k],compute_uv=False)
            leading[str(k)]={
                "singular_values":[float(x) for x in s],
                "min":float(np.min(s)),
                "mean":float(np.mean(s)),
                "rms":float(np.sqrt(np.mean(s*s))),
            }

    return {
        "M":M,"H21":H21,"H12":H12,
        "canonical_correlations":sM,
        "O_span":Ospan,
        "phi_1_to_2":phi12,
        "phi_2_to_1":phi21,
        "A_phi":float(2*abs(phi12-phi21)/(phi12+phi21)) if (phi12+phi21)>0 else np.nan,
        "r_eff_C1":effective_rank_psd(C1),
        "r_eff_C2":effective_rank_psd(C2),
        "r_eff_H21_conditional_transferred":effective_rank_psd(H21),
        "r_eff_H12_conditional_transferred":effective_rank_psd(H12),
        "eig_C1":ew1,"eig_C2":ew2,"eig_H21":nu21,"eig_H12":nu12,
        "T_1_to_2":T12,"T_2_to_1":T21,
        "U_task_1_to_2":U12,"U_task_2_to_1":U21,
        "eta_task_1_to_2":eta12,"eta_task_2_to_1":eta21,
        "leading_oracle_vs_oracle":leading,
    }

def validate_identities(metrics, tol=1e-9):
    r=len(metrics["T_1_to_2"])
    checks={
        "Tfull_equals_phi_1_to_2":bool(abs(metrics["T_1_to_2"][-1]-metrics["phi_1_to_2"])<=tol),
        "Tfull_equals_phi_2_to_1":bool(abs(metrics["T_2_to_1"][-1]-metrics["phi_2_to_1"])<=tol),
        "Ufull_equals_phi_1_to_2":bool(abs(metrics["U_task_1_to_2"][-1]-metrics["phi_1_to_2"])<=tol),
        "Ufull_equals_phi_2_to_1":bool(abs(metrics["U_task_2_to_1"][-1]-metrics["phi_2_to_1"])<=tol),
        "etafull_equals_one_1_to_2":bool(abs(metrics["eta_task_1_to_2"][-1]-1.0)<=tol),
        "etafull_equals_one_2_to_1":bool(abs(metrics["eta_task_2_to_1"][-1]-1.0)<=tol),
        "T_le_U_all_k_1_to_2":bool(np.all(metrics["T_1_to_2"]<=metrics["U_task_1_to_2"]+tol)),
        "T_le_U_all_k_2_to_1":bool(np.all(metrics["T_2_to_1"]<=metrics["U_task_2_to_1"]+tol)),
        "canonical_corr_le_one":bool(np.max(metrics["canonical_correlations"])<=1.0+tol),
    }
    return checks
