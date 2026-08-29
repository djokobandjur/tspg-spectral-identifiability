#!/usr/bin/env python3
import hashlib
import numpy as np

def sym(A):
    A=np.asarray(A,dtype=np.float64)
    return 0.5*(A+A.T)

def psd_eigh_desc(A):
    A=sym(A)
    w,U=np.linalg.eigh(A)
    o=np.argsort(w)[::-1]
    return w[o],U[:,o]

def psd_pinv_sqrt(A):
    w,U=psd_eigh_desc(A)
    tol=max(A.shape)*np.finfo(np.float64).eps*max(float(np.max(np.abs(w))),1.0)
    keep=w>tol
    if not np.any(keep):
        raise ValueError("PSD matrix has zero numerical rank")
    invsqrt=(U[:,keep]*(w[keep]**-0.5))@U[:,keep].T
    return invsqrt,w,U,int(np.sum(keep)),float(tol)

def seed_from_parts(*parts):
    s="|".join(str(x) for x in parts).encode()
    return int.from_bytes(hashlib.sha256(s).digest()[:8],"little",signed=False)

def coverage_first_subset(labels,n,seed):
    labels=np.asarray(labels,dtype=np.int64)
    N=len(labels)
    if n>N:
        raise ValueError("n>N")
    classes=np.unique(labels)
    if n<len(classes):
        raise ValueError("n smaller than represented class count")
    if n==N:
        return np.arange(N,dtype=np.int64)

    rng=np.random.default_rng(seed)
    selected=[]
    residual=[]
    for c in classes:
        loc=np.flatnonzero(labels==c)
        perm=rng.permutation(loc)
        selected.append(int(perm[0]))
        residual.extend(int(x) for x in perm[1:])
    residual=np.asarray(residual,dtype=np.int64)
    residual=rng.permutation(residual)
    need=n-len(selected)
    selected=np.asarray(selected+residual[:need].tolist(),dtype=np.int64)
    selected.sort()
    return selected

def dual_metrics(Kss_full,Khh_full,Ksh_full,s_idx,h_idx,k_ladder):
    s_idx=np.asarray(s_idx,dtype=np.int64)
    h_idx=np.asarray(h_idx,dtype=np.int64)
    Kss=sym(Kss_full[np.ix_(s_idx,s_idx)])
    Khh=sym(Khh_full[np.ix_(h_idx,h_idx)])
    Ksh=np.asarray(Ksh_full[np.ix_(s_idx,h_idx)],dtype=np.float64)

    invsqrt,eig_s,U_s,rank_s,tol=psd_pinv_sqrt(Kss)
    J=sym(invsqrt@Ksh@Ksh.T@invsqrt)
    nu,Uj=psd_eigh_desc(J)

    held_trace=float(np.trace(Khh))
    if held_trace<=0:
        raise ValueError("held trace <=0")

    phi=float(np.trace(J)/held_trace)

    # Train top-k parameter-space eigenvectors represented in dual form.
    out={}
    for k in k_ladder:
        if k>rank_s:
            raise ValueError(f"k={k} exceeds train numerical rank={rank_s}")
        lam=eig_s[:k]
        Us=U_s[:,:k]
        # G_H V_k = K_HS U_k Lambda^{-1/2}
        X=Ksh.T@Us
        X=X*(lam**-0.5)
        task_num=float(np.sum(X*X))
        oracle_num=float(np.sum(nu[:k]))
        T=task_num/held_trace
        U=oracle_num/held_trace
        eta=task_num/oracle_num if oracle_num>0 else np.nan
        out[int(k)]={"T":T,"U_oracle":U,"eta":eta}

    return {
        "phi":phi,
        "train_rank":rank_s,
        "train_rank_tol":tol,
        "held_trace":held_trace,
        "metrics_by_k":out,
    }

def summarize(values,qlo=0.05,qhi=0.95):
    x=np.asarray(values,dtype=np.float64)
    return {
        "n":int(x.size),
        "median":float(np.median(x)),
        "q05":float(np.quantile(x,qlo)),
        "q95":float(np.quantile(x,qhi)),
        "mean":float(np.mean(x)),
        "sd":float(np.std(x,ddof=1)) if x.size>1 else 0.0,
        "min":float(np.min(x)),
        "max":float(np.max(x)),
    }

def fit_inverse_n(n,y,target_n=640):
    n=np.asarray(n,dtype=np.float64)
    y=np.asarray(y,dtype=np.float64)
    X=np.column_stack([np.ones_like(n),1.0/n])
    coef,_,_,_=np.linalg.lstsq(X,y,rcond=None)
    pred=X@coef
    resid=y-pred
    ss_res=float(np.sum(resid*resid))
    ss_tot=float(np.sum((y-np.mean(y))**2))
    r2=float(1.0-ss_res/ss_tot) if ss_tot>0 else 1.0
    target=float(coef[0]+coef[1]/float(target_n))
    return {
        "a":float(coef[0]),
        "b":float(coef[1]),
        "rmse":float(np.sqrt(np.mean(resid*resid))),
        "r2":r2,
        "target_n":int(target_n),
        "prediction_raw":target,
        "prediction_bounded_0_1":float(np.clip(target,0.0,1.0)),
        "gain_from_last_observed_raw":float(target-y[-1]),
    }
