from __future__ import annotations
import time, hashlib
from pathlib import Path
import numpy as np
import torch
from torch.utils.data import DataLoader, Subset
from scipy.linalg import eigh

from TSPG_cross_family_pe_operator_v1_0_20260828 import native_spec
from TSPG_h1_0003_matrixfree_geometry_operator_v1_1_20260828 import (
    native_zero, centered_map, tuple_energy, ga_matvec_streaming
)

class ResourceStop(RuntimeError):
    pass

def sha256_file(path:Path)->str:
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for c in iter(lambda:f.read(16*1024*1024),b""):
            h.update(c)
    return h.hexdigest()

def _tuple_batch_energy(jvs):
    out=None
    for t in jvs:
        e=t.double().reshape(t.shape[0],-1).square().sum(dim=1)
        out=e if out is None else out+e
    return out

def ga_matmat_vmap_streaming(
    model,dataset,indices,family,directions,device,batch_size=1
):
    loader=DataLoader(
        Subset(dataset,list(indices)),batch_size=batch_size,shuffle=False,
        num_workers=0,pin_memory=False
    )
    V=directions.to(device=device,dtype=torch.float64)
    if V.ndim==1:
        V=V[:,None]
    d,m=V.shape
    if d!=native_spec(model,family)["d"]:
        raise ValueError("direction dimension mismatch")

    zero=native_zero(model,family,device)
    gsum=torch.zeros((d,m),device=device,dtype=torch.float64)
    clean_energy=torch.zeros((),device=device,dtype=torch.float64)
    tangent_energy=torch.zeros((m,),device=device,dtype=torch.float64)

    if torch.cuda.is_available():
        torch.cuda.empty_cache(); torch.cuda.reset_peak_memory_stats()
    t0=time.time(); n=0

    for images,_ in loader:
        images=images.to(device=device,dtype=torch.float64)
        fn=centered_map(model,images,family)
        clean,vjp_fn=torch.func.vjp(fn,zero)

        def jvp_one(v):
            _,tang=torch.func.jvp(fn,(zero,),(v,))
            return tang

        jvs=torch.vmap(jvp_one,in_dims=1,out_dims=0)(V)

        def pb_one(*cts):
            return vjp_fn(tuple(cts))[0]

        grads=torch.vmap(
            pb_one,in_dims=tuple(0 for _ in jvs),out_dims=0
        )(*jvs)

        gsum += grads.T
        clean_energy += tuple_energy(clean)
        tangent_energy += _tuple_batch_energy(jvs)
        n += images.shape[0]
        del images,clean,vjp_fn,jvs,grads

    if clean_energy.item()<=0:
        raise RuntimeError("non-positive clean geometry energy")
    GAV=gsum/clean_energy
    q_direct=tangent_energy/clean_energy
    q_dot=(V*GAV).sum(dim=0)
    return {
        "n_images":int(n),
        "ga_V":GAV.detach(),
        "clean_energy":float(clean_energy.item()),
        "q_direct":[float(x) for x in q_direct],
        "q_dot":[float(x) for x in q_dot],
        "elapsed_sec":float(time.time()-t0),
        "peak_cuda_memory_bytes":(
            int(torch.cuda.max_memory_allocated())
            if torch.cuda.is_available() else None
        ),
        "mode":"vmap",
    }

def ga_matmat_shared_vjp_streaming(
    model,dataset,indices,family,directions,device,batch_size=1
):
    loader=DataLoader(
        Subset(dataset,list(indices)),batch_size=batch_size,shuffle=False,
        num_workers=0,pin_memory=False
    )
    V=directions.to(device=device,dtype=torch.float64)
    if V.ndim==1:
        V=V[:,None]
    d,m=V.shape
    zero=native_zero(model,family,device)
    gsum=torch.zeros((d,m),device=device,dtype=torch.float64)
    clean_energy=torch.zeros((),device=device,dtype=torch.float64)
    tangent_energy=torch.zeros((m,),device=device,dtype=torch.float64)

    if torch.cuda.is_available():
        torch.cuda.empty_cache(); torch.cuda.reset_peak_memory_stats()
    t0=time.time(); n=0

    for images,_ in loader:
        images=images.to(device=device,dtype=torch.float64)
        fn=centered_map(model,images,family)
        clean,vjp_fn=torch.func.vjp(fn,zero)
        clean_energy += tuple_energy(clean)
        cols=[]
        for j in range(m):
            _,jv=torch.func.jvp(fn,(zero,),(V[:,j],))
            g=vjp_fn(jv)[0]
            cols.append(g)
            tangent_energy[j]+=tuple_energy(jv)
        gsum += torch.stack(cols,dim=1)
        n += images.shape[0]
        del images,clean,vjp_fn,cols

    GAV=gsum/clean_energy
    q_direct=tangent_energy/clean_energy
    q_dot=(V*GAV).sum(dim=0)
    return {
        "n_images":int(n),
        "ga_V":GAV.detach(),
        "clean_energy":float(clean_energy.item()),
        "q_direct":[float(x) for x in q_direct],
        "q_dot":[float(x) for x in q_dot],
        "elapsed_sec":float(time.time()-t0),
        "peak_cuda_memory_bytes":(
            int(torch.cuda.max_memory_allocated())
            if torch.cuda.is_available() else None
        ),
        "mode":"shared_vjp_loop",
    }

def serial_reference_matmat(
    model,dataset,indices,family,directions,device,batch_size=1
):
    V=directions.to(device=device,dtype=torch.float64)
    if V.ndim==1:
        V=V[:,None]
    cols=[]; qs=[]; times=[]; peak=0
    for j in range(V.shape[1]):
        rr=ga_matvec_streaming(
            model,dataset,indices,family,V[:,j],device,batch_size
        )
        cols.append(rr["ga_v"])
        qs.append(rr["q_dot"])
        times.append(rr["elapsed_sec"])
        peak=max(peak,int(rr["peak_cuda_memory_bytes"] or 0))
    return {
        "ga_V":torch.stack(cols,dim=1),
        "q_dot":qs,
        "elapsed_sec":float(sum(times)),
        "column_elapsed_sec":[float(x) for x in times],
        "peak_cuda_memory_bytes":peak,
        "mode":"serial_reference",
    }

def validate_block_mode(
    model,dataset,indices,family,directions,device,batch_size,
    rel_gate,q_gate
):
    ref=serial_reference_matmat(
        model,dataset,indices,family,directions,device,batch_size
    )
    candidates=[]
    for mode,fn in [
        ("vmap",ga_matmat_vmap_streaming),
        ("shared_vjp_loop",ga_matmat_shared_vjp_streaming),
    ]:
        try:
            cand=fn(
                model,dataset,indices,family,directions,device,batch_size
            )
            A=ref["ga_V"].double()
            B=cand["ga_V"].double()
            rel=[]
            for j in range(A.shape[1]):
                rel.append(float(
                    torch.linalg.vector_norm(B[:,j]-A[:,j])/
                    torch.clamp(torch.linalg.vector_norm(A[:,j]),min=1e-30)
                ))
            qref=np.asarray(ref["q_dot"],dtype=np.float64)
            qcand=np.asarray(cand["q_dot"],dtype=np.float64)
            qrel=np.abs(qcand-qref)/np.maximum(np.abs(qref),1e-30)
            passed=bool(
                np.isfinite(rel).all() and np.isfinite(qrel).all()
                and max(rel)<=rel_gate
                and float(qrel.max())<=q_gate
            )
            candidates.append({
                "mode":mode,
                "supported":True,
                "pass":passed,
                "relative_l2_per_column":rel,
                "relative_l2_max":max(rel),
                "quadratic_relative_per_column":[float(x) for x in qrel],
                "quadratic_relative_max":float(qrel.max()),
                "elapsed_sec":cand["elapsed_sec"],
                "serial_elapsed_sec":ref["elapsed_sec"],
                "speedup_vs_serial":float(
                    ref["elapsed_sec"]/max(cand["elapsed_sec"],1e-30)
                ),
                "peak_cuda_memory_bytes":cand["peak_cuda_memory_bytes"],
            })
        except Exception as e:
            candidates.append({
                "mode":mode,"supported":False,"pass":False,
                "exception":repr(e)
            })
    selected=None
    for preferred in ("vmap","shared_vjp_loop"):
        hit=next((x for x in candidates if x["mode"]==preferred),None)
        if hit and hit["pass"]:
            selected=preferred
            break
    return {
        "serial_reference":{
            "elapsed_sec":ref["elapsed_sec"],
            "peak_cuda_memory_bytes":ref["peak_cuda_memory_bytes"],
            "q_dot":[float(x) for x in ref["q_dot"]],
        },
        "candidates":candidates,
        "selected_mode":selected,
        "pass":selected is not None,
    }

def block_ga_action(mode,*args,**kwargs):
    if mode=="vmap":
        return ga_matmat_vmap_streaming(*args,**kwargs)
    if mode=="shared_vjp_loop":
        return ga_matmat_shared_vjp_streaming(*args,**kwargs)
    raise ValueError(mode)

def apply_B_block(
    model,dataset,indices,family,X,device,alpha,batch_size,mode
):
    rr=block_ga_action(
        mode,model,dataset,indices,family,X,device,batch_size
    )
    Xt=X.to(device=device,dtype=torch.float64)
    BV=rr["ga_V"]+float(alpha)*Xt
    return BV,rr

class ScaledNystromInverse:
    def __init__(self,V,mu,alpha):
        self.V=np.asarray(V,dtype=np.float64)
        self.mu=np.asarray(mu,dtype=np.float64)
        self.alpha=float(alpha)
        self.w=self.mu/(self.alpha+self.mu)
    def apply(self,X):
        X=np.asarray(X,dtype=np.float64)
        one=False
        if X.ndim==1:
            X=X[:,None]; one=True
        Y=X-self.V@(self.w[:,None]*(self.V.T@X))
        return Y[:,0] if one else Y

def nystrom_from_Y(Omega,Y,rank,pinv_rcond=1e-12):
    O=np.asarray(Omega[:,:rank],dtype=np.float64)
    Y=np.asarray(Y[:,:rank],dtype=np.float64)
    K=0.5*(O.T@Y+Y.T@O)
    Q,R=np.linalg.qr(Y,mode="reduced")
    Kpinv=np.linalg.pinv(K,rcond=float(pinv_rcond),hermitian=True)
    C=R@Kpinv@R.T
    C=0.5*(C+C.T)
    mu,U=np.linalg.eigh(C)
    order=np.argsort(mu)[::-1]
    mu=mu[order]; U=U[:,order]
    floor=max(1e-14,float(max(mu.max(),0.0))*1e-14)
    keep=mu>floor
    mu=mu[keep]; U=U[:,keep]
    V=Q@U
    return {
        "V":V,"mu":mu,
        "effective_rank":int(len(mu)),
        "K_eigenvalues":np.linalg.eigvalsh(K),
    }

def build_nystrom_block(
    model,dataset,indices,family,device,d,max_rank,seed,
    block_size,batch_size,mode,wall_seconds
):
    rng=np.random.default_rng(int(seed))
    Omega=rng.standard_normal((d,max_rank))
    Omega,_=np.linalg.qr(Omega,mode="reduced")
    Y=np.empty((d,max_rank),dtype=np.float64)
    t0=time.time(); calls=[]; peak=0
    for start in range(0,max_rank,block_size):
        if time.time()-t0>wall_seconds:
            raise ResourceStop("Nystrom build wall stop")
        stop=min(start+block_size,max_rank)
        V=torch.from_numpy(Omega[:,start:stop]).to(
            device=device,dtype=torch.float64
        )
        rr=block_ga_action(
            mode,model,dataset,indices,family,V,device,batch_size
        )
        Y[:,start:stop]=rr["ga_V"].cpu().numpy()
        calls.append({
            "start":start,"stop":stop,
            "elapsed_sec":rr["elapsed_sec"],
            "peak_cuda_memory_bytes":rr["peak_cuda_memory_bytes"],
        })
        peak=max(peak,int(rr["peak_cuda_memory_bytes"] or 0))
        print(
            f"[nystrom-block] {stop}/{max_rank} "
            f"elapsed={time.time()-t0:.1f}s mode={mode}",
            flush=True
        )
        del V,rr
    return {
        "Omega":Omega,"Y":Y,
        "elapsed_sec":float(time.time()-t0),
        "block_calls":calls,
        "peak_cuda_memory_bytes":peak,
    }

def pcg_multi_rhs(
    B_apply,R,preconditioner,rtol=1e-8,maxiter=128,
    progress_prefix=""
):
    R=np.asarray(R,dtype=np.float64)
    if R.ndim==1: R=R[:,None]
    d,m=R.shape
    X=np.zeros((d,m),dtype=np.float64)
    Res=R.copy()
    bnorm=np.linalg.norm(R,axis=0)
    bnorm=np.maximum(bnorm,1e-30)
    Z=preconditioner.apply(Res)
    P=Z.copy()
    rz=np.sum(Res*Z,axis=0)
    recursive=[]
    t0=time.time()

    for it in range(1,int(maxiter)+1):
        AP=B_apply(P)
        denom=np.sum(P*AP,axis=0)
        if np.any(~np.isfinite(denom)) or np.any(denom<=0):
            return {
                "X":X,"recursive_history":recursive,
                "iterations":it-1,"breakdown":True,
                "breakdown_reason":"non-positive/non-finite p^T B p",
                "elapsed_sec":float(time.time()-t0),
            }
        a=rz/denom
        X += P*a
        Res -= AP*a
        rel=np.linalg.norm(Res,axis=0)/bnorm
        recursive.append([float(x) for x in rel])
        if it==1 or it%5==0 or float(rel.max())<=rtol:
            print(
                f"{progress_prefix} PCG iter {it}: "
                f"max_recursive_rel={float(rel.max()):.3e}",
                flush=True
            )
        if np.all(rel<=rtol):
            return {
                "X":X,"recursive_history":recursive,
                "iterations":it,"breakdown":False,
                "elapsed_sec":float(time.time()-t0),
            }
        Znew=preconditioner.apply(Res)
        rznew=np.sum(Res*Znew,axis=0)
        beta=rznew/rz
        P=Znew+P*beta
        Z=Znew; rz=rznew
    return {
        "X":X,"recursive_history":recursive,
        "iterations":int(maxiter),"breakdown":False,
        "elapsed_sec":float(time.time()-t0),
    }

def exact_true_linear_residual(B_apply,X,R):
    BX=B_apply(X)
    num=np.linalg.norm(BX-R,axis=0)
    den=np.maximum(np.linalg.norm(R,axis=0),1e-30)
    return num/den,BX

def projected_generalized_candidates(
    G,Q,BQ,k,alpha,positivity_floor
):
    G=np.asarray(G,dtype=np.float64)
    Q=np.asarray(Q,dtype=np.float64)
    BQ=np.asarray(BQ,dtype=np.float64)
    n=G.shape[0]
    GQ=G@Q
    A=(GQ.T@GQ)/float(n)
    B=Q.T@BQ
    A=0.5*(A+A.T); B=0.5*(B+B.T)
    ew,C=eigh(A,B)
    order=np.argsort(ew)[::-1]
    ew=ew[order][:k]; C=C[:,order][:,:k]
    V=Q@C
    return {
        "eigenvalues":ew,
        "V":V,
        "projected_B_min_eigenvalue":float(np.linalg.eigvalsh(B).min()),
    }

def exact_generalized_diagnostics(G,V,ew,BV,alpha):
    G=np.asarray(G,dtype=np.float64)
    V=np.asarray(V,dtype=np.float64)
    ew=np.asarray(ew,dtype=np.float64)
    BV=np.asarray(BV,dtype=np.float64)
    n=G.shape[0]
    AV=(G.T@(G@V))/float(n)
    R=AV-BV*ew.reshape(1,-1)
    den=np.maximum(
        np.linalg.norm(AV,axis=0)
        +np.abs(ew)*np.linalg.norm(BV,axis=0),
        1e-30
    )
    gres=np.linalg.norm(R,axis=0)/den
    Bgram=V.T@BV
    borth=float(np.max(np.abs(Bgram-np.eye(V.shape[1]))))
    benergy=np.sum(V*BV,axis=0)
    norm2=np.sum(V*V,axis=0)
    ridge=float(alpha)*norm2
    attention=benergy-ridge
    ridge_frac=ridge/benergy
    attn_frac=attention/benergy
    identity=np.abs(ridge_frac+attn_frac-1.0)
    return {
        "generalized_residuals":[float(x) for x in gres],
        "generalized_residual_max":float(gres.max()),
        "B_orthonormality_max_abs":borth,
        "B_energy":[float(x) for x in benergy],
        "euclidean_norm_squared":[float(x) for x in norm2],
        "ridge_energy":[float(x) for x in ridge],
        "attention_energy":[float(x) for x in attention],
        "ridge_fraction":[float(x) for x in ridge_frac],
        "attention_fraction":[float(x) for x in attn_frac],
        "fraction_identity_abs_error":[float(x) for x in identity],
        "fraction_identity_abs_error_max":float(identity.max()),
    }


def dense_ga_exact(
    model,dataset,indices,family,device,batch_size=1
):
    """Exact dense G_A for a small native parameter space."""
    d=int(native_spec(model,family)["d"])
    GA=np.empty((d,d),dtype=np.float64)
    basis=torch.eye(d,device=device,dtype=torch.float64)
    times=[]; peak=0
    for j in range(d):
        rr=ga_matvec_streaming(
            model,dataset,indices,family,basis[:,j],device,batch_size
        )
        GA[:,j]=rr["ga_v"].detach().cpu().numpy()
        times.append(float(rr["elapsed_sec"]))
        peak=max(peak,int(rr["peak_cuda_memory_bytes"] or 0))
        print(
            f"[{family} dense GA] column {j+1}/{d} "
            f"elapsed={rr['elapsed_sec']:.2f}s",
            flush=True
        )
    GA=0.5*(GA+GA.T)
    return {
        "GA":GA,
        "trace":float(np.trace(GA)),
        "eigenvalues":[float(x) for x in np.linalg.eigvalsh(GA)[::-1]],
        "column_elapsed_sec":times,
        "peak_cuda_memory_bytes":peak,
    }

def dense_generalized_control(
    G,GA,c,k=4,positivity_floor=-1e-12
):
    """Exact dense generalized eigensystem and denominator decomposition."""
    G=np.asarray(G,dtype=np.float64)
    GA=np.asarray(GA,dtype=np.float64)
    n,d=G.shape
    GT=(G.T@G)/float(n)
    GT=0.5*(GT+GT.T)
    trace=float(np.trace(GA))
    tau=float(c)*trace
    alpha=tau/float(d)
    B=GA+alpha*np.eye(d,dtype=np.float64)
    B=0.5*(B+B.T)

    ew,V=eigh(GT,B)
    order=np.argsort(ew)[::-1]
    ew=ew[order][:k]
    V=V[:,order][:,:k]
    BV=B@V
    diag=exact_generalized_diagnostics(G,V,ew,BV,alpha)
    return {
        "d":int(d),
        "n_task":int(n),
        "trace_GA":trace,
        "c":float(c),
        "tau":tau,
        "alpha":alpha,
        "GA_eigenvalues_desc":[float(x) for x in np.linalg.eigvalsh(GA)[::-1]],
        "GT_eigenvalues_desc":[float(x) for x in np.linalg.eigvalsh(GT)[::-1]],
        "eigenvalues":[float(x) for x in ew],
        "minimum_retained_eigenvalue":float(ew.min()),
        **diag,
    }
