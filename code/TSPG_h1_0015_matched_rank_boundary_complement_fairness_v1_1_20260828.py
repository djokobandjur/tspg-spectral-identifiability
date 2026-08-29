from __future__ import annotations
import hashlib
from pathlib import Path
import numpy as np
from scipy.linalg import eigh

def sha256_file(path:Path)->str:
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for c in iter(lambda:f.read(16*1024*1024),b""):
            h.update(c)
    return h.hexdigest()

def locate_locked_raw(filename,expected_sha,roots):
    candidates=[]
    for root in roots:
        root=Path(root)
        if root.exists():
            candidates.extend([p.resolve() for p in root.rglob(filename) if p.is_file()])
    uniq=[]; seen=set()
    for p in candidates:
        if str(p) not in seen:
            seen.add(str(p)); uniq.append(p)
    checked=[]; matches=[]
    for p in uniq:
        got=sha256_file(p)
        checked.append({"path":str(p),"sha256":got})
        if got==expected_sha: matches.append(p)
    if len(matches)!=1:
        raise RuntimeError(
            f"Expected exactly one SHA-matching {filename}; found {len(matches)}. Checked={checked}"
        )
    return matches[0],checked

def deterministic_qr(X,rel_tol=1e-12):
    X=np.asarray(X,dtype=np.float64)
    if X.size==0:
        return np.zeros((X.shape[0],0),dtype=np.float64),{
            "input_cols":0,"retained_rank":0,"diag_abs":[]
        },None
    Q,R=np.linalg.qr(X,mode="reduced")
    diag=np.abs(np.diag(R))
    scale=float(diag.max()) if diag.size else 0.0
    keep=diag >= rel_tol*scale if scale>0 else np.zeros(diag.shape,dtype=bool)
    rank=int(np.sum(keep))
    if rank:
        bad=np.where(~keep)[0]
        if len(bad): rank=min(rank,int(bad[0]))
    Q=Q[:,:rank]; R=R[:rank,:]
    if rank:
        signs=np.where(np.diag(R[:,:rank])<0.0,-1.0,1.0)
        Q=Q*signs.reshape(1,-1)
        R=R*signs.reshape(-1,1)
    return Q,{
        "input_cols":int(X.shape[1]),
        "retained_rank":rank,
        "diag_abs":[float(x) for x in diag],
        "relative_tolerance":float(rel_tol)
    },R

def project_complement(Q,X,Z=None):
    Y=np.asarray(X,dtype=np.float64)-Q@(Q.T@X)
    if Z is not None and Z.shape[1]:
        Y=Y-Z@(Z.T@Y)
        Y=Y-Q@(Q.T@Y)
        Y=Y-Z@(Z.T@Y)
    return Y

def coupling_diagnostics(Q,GAQ,A,C,alpha):
    M=GAQ.T@GAQ-A.T@A
    M=0.5*(M+M.T)
    ew,V=np.linalg.eigh(M)
    ix=np.argsort(ew)[::-1]
    ew=ew[ix]; V=V[:,ix]
    sing=np.sqrt(np.maximum(ew,0.0))

    B=A+float(alpha)*np.eye(A.shape[0])
    lam,W=eigh(C,B,check_finite=True)
    ix=np.argsort(lam)[::-1]
    return {
        "coupling_gram":M,
        "coupling_singular_values_desc":sing,
        "coupling_right_vectors":V,
        "restricted_generalized_eigenvalues":lam[ix],
        "restricted_generalized_vectors":W[:,ix]
    }

def residual_map(Q,GAQ,A,V):
    return GAQ@V-Q@(A@V)

def build_augmented(Q,C,A,GAQ,Z,GAZ,alpha,nvals=12,k=4):
    r=C.shape[0]; z=Z.shape[1]
    if z:
        E=np.column_stack([Q,Z])
        GAE=np.column_stack([GAQ,GAZ])
        QGZ=Q.T@GAZ
        ZGZ=Z.T@GAZ
        Gaug=np.block([[A,QGZ],[QGZ.T,0.5*(ZGZ+ZGZ.T)]])
        Caug=np.zeros((r+z,r+z),dtype=np.float64); Caug[:r,:r]=C
    else:
        E=Q; GAE=GAQ; Gaug=A.copy(); Caug=C.copy()

    Gaug=0.5*(Gaug+Gaug.T)
    Caug=0.5*(Caug+Caug.T)
    Baug=Gaug+float(alpha)*np.eye(r+z)

    ev,W=eigh(Caug,Baug,check_finite=True)
    ix=np.argsort(ev)[::-1]; ev=ev[ix]; W=W[:,ix]
    if len(ev)<nvals: raise RuntimeError("insufficient eigenvalues")

    V4=E@W[:,:k]
    GAV4=GAE@W[:,:k]
    BV4=GAV4+float(alpha)*V4

    Borth=float(np.max(np.abs(V4.T@BV4-np.eye(k))))
    R=Caug@W[:,:k]-Baug@W[:,:k]*ev[:k].reshape(1,-1)
    den=np.maximum(
        np.linalg.norm(Caug@W[:,:k],axis=0)+
        np.abs(ev[:k])*np.linalg.norm(Baug@W[:,:k],axis=0),1e-30
    )
    gres=np.linalg.norm(R,axis=0)/den

    vals=[float(x) for x in ev[:nvals]]
    l4,l5=vals[3],vals[4]
    return {
        "dimension":int(r+z),
        "complement_dimension":int(z),
        "lambda_1_to_12":vals,
        "gap_4_5_abs":l4-l5,
        "gap_4_5_rel":(l4-l5)/l4,
        "lambda4_over_lambda5":l4/l5 if l5>0 else None,
        "top4_full_vectors":V4,
        "top4_B_vectors":BV4,
        "B_orthonormality_max_abs":Borth,
        "projected_generalized_residuals":[float(x) for x in gres],
        "projected_generalized_residual_max":float(np.max(gres))
    }

def orthonormalize_union_with_actions(Q,Zs,GAZs,rel_tol=1e-12):
    # Each input branch is already Q-orthogonal. QR the union.
    ZU=np.column_stack(Zs)
    GZU=np.column_stack(GAZs)
    ZU=ZU-Q@(Q.T@ZU)
    Qc,meta,R=deterministic_qr(ZU,rel_tol)
    rank=meta["retained_rank"]
    if rank==0: raise RuntimeError("combined complement rank zero")
    # deterministic_qr returns Qc = ZU[:, :]*T only if full-column rank.
    # Use least-squares coefficient map for retained Qc; this is exact to
    # numerical precision and allows GA(Qc)=GA(ZU)T without new GA calls.
    T,_,_,_=np.linalg.lstsq(ZU,Qc,rcond=None)
    recon=float(np.max(np.abs(ZU@T-Qc)))
    GQc=GZU@T
    return Qc,GQc,meta,recon

def euclidean_top4_overlap(V1,V2):
    Q1,_=np.linalg.qr(V1,mode="reduced")
    Q2,_=np.linalg.qr(V2,mode="reduced")
    s=np.linalg.svd(Q1.T@Q2,compute_uv=False)
    s=np.clip(s,0.0,1.0)
    return [float(x) for x in s]

def B_top4_overlap_same_metric(V1,BV2):
    s=np.linalg.svd(V1.T@BV2,compute_uv=False)
    s=np.clip(s,0.0,1.0)
    return [float(x) for x in s]
