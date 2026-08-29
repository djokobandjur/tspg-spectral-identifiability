from __future__ import annotations
import time
from typing import Dict, Sequence
import numpy as np
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader, Subset

from TSPG_cross_family_pe_operator_v1_0_20260828 import (
    native_spec, forward_with_native_delta, deterministic_native_direction,
)

def native_zero(model, family, device):
    return torch.zeros(
        native_spec(model,family)["d"], device=device, dtype=torch.float64
    )

def centered_map(model, images, family):
    def fn(delta):
        _, zs = forward_with_native_delta(
            model, images, delta, family,
            backend="math", return_centered_logits=True
        )
        return zs
    return fn

def tuple_energy(xs):
    return sum(x.double().square().sum() for x in xs)

def tuple_dot(xs, ys):
    return sum((x.double()*y.double()).sum() for x,y in zip(xs,ys))

def ga_matvec_streaming(model, dataset, indices:Sequence[int], family:str,
                        direction:torch.Tensor, device, batch_size:int=1) -> Dict:
    """Exact matrix-free GA*v on the supplied calibration indices in FP64.

    GA = J^T J / ||F||^2, where F is concatenated row-centered attention logits.
    """
    loader=DataLoader(
        Subset(dataset,list(indices)), batch_size=batch_size, shuffle=False,
        num_workers=0, pin_memory=False
    )
    d=native_spec(model,family)["d"]
    v=direction.reshape(d).to(device=device,dtype=torch.float64)
    zero=native_zero(model,family,device)
    gsum=torch.zeros_like(zero)
    clean_energy=torch.zeros((),device=device,dtype=torch.float64)
    tangent_energy=torch.zeros((),device=device,dtype=torch.float64)

    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats()
    t0=time.time()
    n=0

    for images,_ in loader:
        images=images.to(device=device,dtype=torch.float64)
        fn=centered_map(model,images,family)

        clean, vjp_fn = torch.func.vjp(fn, zero)
        _, jv = torch.func.jvp(fn, (zero,), (v,))

        g = vjp_fn(jv)[0]
        gsum += g
        clean_energy += tuple_energy(clean)
        tangent_energy += tuple_energy(jv)
        n += images.shape[0]

        del clean, vjp_fn, jv, g, images

    if clean_energy.item() <= 0:
        raise RuntimeError("non-positive clean geometry energy")

    ga_v=gsum/clean_energy
    q_direct=tangent_energy/clean_energy
    q_dot=torch.dot(v,ga_v)

    return {
        "n_images":int(n),
        "ga_v":ga_v.detach(),
        "clean_energy":float(clean_energy.item()),
        "tangent_energy":float(tangent_energy.item()),
        "q_direct":float(q_direct.item()),
        "q_dot":float(q_dot.item()),
        "elapsed_sec":float(time.time()-t0),
        "peak_cuda_memory_bytes":(
            int(torch.cuda.max_memory_allocated()) if torch.cuda.is_available() else None
        ),
    }

def scalar_task_gradients(model,dataset,indices,family,device):
    loader=DataLoader(
        Subset(dataset,list(indices)),batch_size=1,shuffle=False,num_workers=0
    )
    rows=[]
    losses=[]
    if torch.cuda.is_available():
        torch.cuda.empty_cache(); torch.cuda.reset_peak_memory_stats()
    t0=time.time()
    for images,labels in loader:
        images=images.to(device=device,dtype=torch.float64)
        labels=labels.to(device)
        delta=native_zero(model,family,device).requires_grad_(True)
        logits=forward_with_native_delta(model,images,delta,family,backend="math")
        loss=F.cross_entropy(logits,labels,reduction="sum")
        g=torch.autograd.grad(loss,delta,create_graph=False)[0]
        rows.append(g.detach().cpu())
        losses.append(float(loss.detach().item()))
        del images,labels,delta,logits,loss,g
    G=torch.stack(rows,dim=0).double()
    return {
        "G":G,
        "losses":losses,
        "elapsed_sec":float(time.time()-t0),
        "peak_cuda_memory_bytes":(
            int(torch.cuda.max_memory_allocated()) if torch.cuda.is_available() else None
        ),
    }

def generalized_eigh_dense(A,B):
    A=np.asarray(A,dtype=np.float64); B=np.asarray(B,dtype=np.float64)
    A=0.5*(A+A.T); B=0.5*(B+B.T)
    eb,Ub=np.linalg.eigh(B)
    if eb.min() <= 0:
        raise RuntimeError(f"projected B not positive definite: {eb.min()}")
    Binvsqrt=(Ub*(1.0/np.sqrt(eb)))@Ub.T
    M=Binvsqrt@A@Binvsqrt
    ew,U=np.linalg.eigh(0.5*(M+M.T))
    order=np.argsort(ew)[::-1]
    ew=ew[order]; U=U[:,order]
    V=Binvsqrt@U
    return ew,V

def projected_solver_preflight(model,dataset,task_indices,cal_indices,family,
                               device,c,trace_probes,trace_seed_base,batch_size=1):
    tg=scalar_task_gradients(model,dataset,task_indices,family,device)
    G=tg["G"].numpy()  # n x d, FP64 CPU
    n,d=G.shape

    # Euclidean orthonormal basis of the task-gradient span.
    Q,_=np.linalg.qr(G.T,mode="reduced")  # d x r
    r=Q.shape[1]

    # Micro trace estimate: E[z^T GA z], Rademacher z.
    trace_vals=[]
    for j in range(trace_probes):
        rng=np.random.default_rng(int(trace_seed_base+j))
        z=(2*rng.integers(0,2,size=d,dtype=np.int8)-1).astype(np.float64)
        zt=torch.from_numpy(z).to(device)
        rr=ga_matvec_streaming(
            model,dataset,cal_indices,family,zt,device,batch_size
        )
        trace_vals.append(rr["q_dot"])
        del zt, rr
    trace_hat=float(np.mean(trace_vals))
    tau=float(c*trace_hat)
    alpha=float(tau/d)
    if not np.isfinite(alpha) or alpha <= 0:
        raise RuntimeError("invalid projected-preflight ridge")

    # Project GA by exact matrix-free products on Q columns.
    GAQ=[]
    ga_times=[]
    for j in range(r):
        q=torch.from_numpy(Q[:,j]).to(device=device,dtype=torch.float64)
        rr=ga_matvec_streaming(
            model,dataset,cal_indices,family,q,device,batch_size
        )
        GAQ.append(rr["ga_v"].cpu().numpy())
        ga_times.append(rr["elapsed_sec"])
        del q,rr
    GAQ=np.stack(GAQ,axis=1)  # d x r

    GAproj=Q.T@GAQ

    # EXACT low-rank empirical task-operator projection:
    # Q.T @ (G.T @ G / n) @ Q == (G @ Q).T @ (G @ Q) / n.
    # No d x d task operator is constructed.
    GQ=G@Q
    GTproj=(GQ.T@GQ)/float(n)
    Bproj=GAproj + alpha*np.eye(r,dtype=np.float64)

    ew,V=generalized_eigh_dense(GTproj,Bproj)
    Borth=float(np.max(np.abs(V.T@Bproj@V-np.eye(r))))
    denom=np.maximum(
        np.linalg.norm(GTproj@V,axis=0)+np.abs(ew)*np.linalg.norm(Bproj@V,axis=0),
        1e-30
    )
    residuals=np.linalg.norm(GTproj@V-(Bproj@V)*ew.reshape(1,-1),axis=0)/denom

    return {
        "task_gradient_shape":[int(n),int(d)],
        "task_gradient_elapsed_sec":tg["elapsed_sec"],
        "task_gradient_peak_cuda_memory_bytes":tg["peak_cuda_memory_bytes"],
        "task_gradient_losses":tg["losses"],
        "projected_rank":int(r),
        "trace_probe_values":[float(x) for x in trace_vals],
        "trace_hat":trace_hat,
        "tau":tau,
        "alpha_tau_over_d":alpha,
        "ga_projected_matvec_elapsed_sec":[float(x) for x in ga_times],
        "projected_eigenvalues":[float(x) for x in ew],
        "projected_B_orth_error":Borth,
        "projected_generalized_residual_max":float(residuals.max()),
        "projected_B_min_eigenvalue":float(np.linalg.eigvalsh(0.5*(Bproj+Bproj.T)).min()),
        "task_operator_projection_method":"EXACT_LOW_RANK_GQ",
        "dense_GT_constructed":False,
        "forbidden_dense_GT_bytes":int(d*d*8),
        "forbidden_dense_GT_gib":float(d*d*8/(1024**3)),
        "GQ_shape":[int(x) for x in GQ.shape],
        "GTproj_shape":[int(x) for x in GTproj.shape],
    }
