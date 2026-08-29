#!/usr/bin/env python3
import hashlib
import numpy as np

def sym(A):
    A=np.asarray(A,dtype=np.float64)
    return 0.5*(A+A.T)

def eigh_desc(A):
    w,U=np.linalg.eigh(sym(A))
    o=np.argsort(w)[::-1]
    return w[o],U[:,o]

def psd_sqrt(A):
    w,U=eigh_desc(A)
    scale=max(float(np.max(np.abs(w))),1.0)
    if float(np.min(w)) < -1e-11*scale:
        raise ValueError(f"materially non-PSD matrix: min={float(np.min(w))}")
    wc=np.clip(w,0.0,None)
    return (U*np.sqrt(wc))@U.T,w

def seed_from_text(s):
    return int.from_bytes(hashlib.sha256(str(s).encode()).digest()[:8],"little")

def fit_arms_from_dual(K11,K22,K12,max_k=32):
    K11=sym(K11); K22=sym(K22); K12=np.asarray(K12,dtype=np.float64)
    n1=K11.shape[0]; n2=K22.shape[0]
    if K11.shape!=(n1,n1) or K22.shape!=(n2,n2) or K12.shape!=(n1,n2):
        raise ValueError("dual block shape mismatch")
    Kff=np.block([[K11,K12],[K12.T,K22]])
    Kff=sym(Kff)

    lamf,Uf=eigh_desc(Kff)
    tol=Kff.shape[0]*np.finfo(np.float64).eps*max(float(lamf[0]),1.0)
    keep=lamf>tol
    rank=int(np.sum(keep))
    if rank<max_k:
        raise ValueError(f"pooled rank {rank}<max_k {max_k}")
    Uf=Uf[:,keep]; lam=lamf[keep]
    R=Uf*(lam**-0.5)  # Q_F = G_F^T R

    K1F=np.concatenate([K11,K12],axis=1)
    K2F=np.concatenate([K12.T,K22],axis=1)
    B1=K1F@R
    B2=K2F@R
    A1=sym((B1.T@B1)/float(n1))
    A2=sym((B2.T@B2)/float(n2))

    N1=A1/np.trace(A1)
    N2=A2/np.trace(A2)
    S1,_=psd_sqrt(N1)
    S2,_=psd_sqrt(N2)
    Ccons=sym(0.5*(S1@N2@S1 + S2@N1@S2))
    cew,Zc=eigh_desc(Ccons)

    # Swap invariance.
    Cswap=sym(0.5*(S2@N1@S2 + S1@N2@S1))
    swap_rel=float(np.linalg.norm(Ccons-Cswap,"fro")/max(np.linalg.norm(Ccons,"fro"),1e-30))

    # U640 dual coefficients.
    A_u640=R[:,:max_k]

    # Consensus dual coefficients.
    A_cons=R@Zc[:,:max_k]

    # U320 constituents.
    e1,U1=eigh_desc(K11)
    e2,U2=eigh_desc(K22)
    if np.min(e1[:max_k])<=0 or np.min(e2[:max_k])<=0:
        raise ValueError("non-positive top fit eigenvalue")
    A_u1=np.zeros((n1+n2,max_k),dtype=np.float64)
    A_u2=np.zeros((n1+n2,max_k),dtype=np.float64)
    A_u1[:n1,:]=U1[:,:max_k]*(e1[:max_k]**-0.5)
    A_u2[n1:,:]=U2[:,:max_k]*(e2[:max_k]**-0.5)

    arms={
        "U320_AG1":A_u1,
        "U320_AG2":A_u2,
        "U640":A_u640,
        "CONS640":A_cons,
    }

    orth={}
    fit_energy={}
    tr1=float(np.trace(K11)); tr2=float(np.trace(K22))
    for name,A in arms.items():
        G=A.T@Kff@A
        orth[name]=float(np.max(np.abs(G-np.eye(max_k))))
        p1=K1F@A
        p2=K2F@A
        fit_energy[name]={
            "AG1_fraction_top32":float(np.sum(p1*p1)/tr1),
            "AG2_fraction_top32":float(np.sum(p2*p2)/tr2),
        }

    return {
        "Kff":Kff,"pooled_eigenvalues":lamf,"pooled_rank":rank,"pooled_tol":float(tol),
        "R":R,"A1":A1,"A2":A2,"N1":N1,"N2":N2,
        "Ccons":Ccons,"consensus_eigenvalues":cew,
        "swap_relative_fro":swap_rel,
        "arms":arms,"orthonormality":orth,"fit_energy":fit_energy,
    }

def score_from_projections(proj_by_arm,total_norm2,secondary_k,primary_k):
    total=float(np.sum(total_norm2))
    if total<=0:
        raise ValueError("non-positive AP task energy")
    ks=list(secondary_k)+list(primary_k)
    out={}
    per_example={}
    for arm,P in proj_by_arm.items():
        sq=np.asarray(P,dtype=np.float64)**2
        c=np.cumsum(sq,axis=1)
        out[arm]={}
        per_example[arm]={}
        for k in ks:
            e=c[:,k-1].copy()
            per_example[arm][int(k)]=e
            out[arm][int(k)]=float(np.sum(e)/total)
    return out,per_example

def paired_bootstrap_curve(per_example,total_norm2,primary_k,reps,seed):
    rng=np.random.default_rng(int(seed))
    n=len(total_norm2)
    point={}
    total=float(np.sum(total_norm2))
    for k in primary_k:
        point[int(k)]=float(
            (np.sum(per_example["CONS640"][k])-np.sum(per_example["U640"][k]))/total
        )
    curve=float(np.mean([point[k] for k in primary_k]))

    vals=np.empty(int(reps),dtype=np.float64)
    byk={int(k):np.empty(int(reps),dtype=np.float64) for k in primary_k}
    for b in range(int(reps)):
        idx=rng.integers(0,n,size=n)
        den=float(np.sum(total_norm2[idx]))
        ds=[]
        for k in primary_k:
            d=float(
                (np.sum(per_example["CONS640"][k][idx])-
                 np.sum(per_example["U640"][k][idx]))/den
            )
            byk[int(k)][b]=d
            ds.append(d)
        vals[b]=float(np.mean(ds))
    qlo,qhi=np.quantile(vals,[0.025,0.975])
    return {
        "point_by_k":point,
        "curve_point":curve,
        "curve_bootstrap_ci95":[float(qlo),float(qhi)],
        "curve_bootstrap_median":float(np.median(vals)),
        "pointwise_ci95_by_k":{
            str(k):[float(x) for x in np.quantile(byk[k],[0.025,0.975])]
            for k in primary_k
        }
    }
