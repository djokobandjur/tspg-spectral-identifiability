#!/usr/bin/env python3
import numpy as np

def sym(A):
    A=np.asarray(A,dtype=np.float64)
    return 0.5*(A+A.T)

def eigh_desc(A):
    w,V=np.linalg.eigh(sym(A))
    o=np.argsort(w)[::-1]
    return w[o],V[:,o]

def invsqrt_spd(B):
    ew,U=np.linalg.eigh(sym(B))
    if np.min(ew)<=0:
        raise ValueError("B not SPD")
    Bmhalf=(U*(ew**-0.5))@U.T
    Bhalf=(U*(ew**0.5))@U.T
    return ew,U,Bmhalf,Bhalf

def euclidean_orth_basis(X):
    Q,_=np.linalg.qr(np.asarray(X,dtype=np.float64),mode="reduced")
    return Q

def b_orthonormalize_span(Qe,B):
    Qe=euclidean_orth_basis(Qe)
    G=sym(Qe.T@B@Qe)
    ew,U=np.linalg.eigh(G)
    if np.min(ew)<=0:
        raise ValueError("span B Gram not SPD")
    Gmhalf=(U*(ew**-0.5))@U.T
    W=Qe@Gmhalf
    return W,Qe,G

def b_inf_error(W,B):
    I=np.eye(W.shape[1])
    return float(np.linalg.norm(W.T@B@W-I,ord=np.inf))

def self_scaled_generalized_residuals(A,B,W,lam):
    out=[]
    for j in range(W.shape[1]):
        w=W[:,j]
        r=A@w-lam[j]*(B@w)
        den=np.linalg.norm(A@w)+abs(lam[j])*np.linalg.norm(B@w)
        out.append(float(np.linalg.norm(r)/den if den>0 else np.linalg.norm(r)))
    return np.asarray(out)

def normwise_generalized_backward_errors(A,B,W,lam):
    nA=float(np.linalg.norm(A,2))
    nB=float(np.linalg.norm(B,2))
    out=[]
    for j in range(W.shape[1]):
        w=W[:,j]
        rr=A@w-lam[j]*(B@w)
        den=(nA+abs(lam[j])*nB)*np.linalg.norm(w)
        out.append(float(np.linalg.norm(rr)/den if den>0 else np.linalg.norm(rr)))
    return np.asarray(out)

def symmetric_backward_errors(K,Z,lam):
    nK=float(np.linalg.norm(K,2))
    out=[]
    for j in range(Z.shape[1]):
        z=Z[:,j]
        rr=K@z-lam[j]*z
        den=(nK+abs(lam[j]))*np.linalg.norm(z)
        out.append(float(np.linalg.norm(rr)/den if den>0 else np.linalg.norm(rr)))
    return np.asarray(out)

def projector_distance_from_cosines(cosines,k):
    c=np.clip(np.asarray(cosines,dtype=np.float64),0.0,1.0)
    return float(np.sqrt(max(0.0,1.0-float(np.mean(c*c)))))

def analyze(C,H,B,k_ladder):
    C=sym(C); H=sym(H); B=sym(B)
    r=C.shape[0]
    if C.shape!=(r,r) or H.shape!=(r,r) or B.shape!=(r,r):
        raise ValueError("shape mismatch")

    b_ew,b_U,Bmhalf,Bhalf=invsqrt_spd(B)

    theta,E=eigh_desc(C)
    nu,OE=eigh_desc(H)

    Ktrain=sym(Bmhalf@C@Bmhalf)
    glam,Ztrain=eigh_desc(Ktrain)
    WB=Bmhalf@Ztrain

    Kheld=sym(Bmhalf@H@Bmhalf)
    mu,Zoracle=eigh_desc(Kheld)
    WO=Bmhalf@Zoracle

    self_train=self_scaled_generalized_residuals(C,B,WB,glam)
    self_oracle=self_scaled_generalized_residuals(H,B,WO,mu)
    back_train=normwise_generalized_backward_errors(C,B,WB,glam)
    back_oracle=normwise_generalized_backward_errors(H,B,WO,mu)
    sym_train=symmetric_backward_errors(Ktrain,Ztrain,glam)
    sym_oracle=symmetric_backward_errors(Kheld,Zoracle,mu)

    total_B_oracle=float(np.sum(mu))
    rows=[]

    for k in k_ladder:
        QE=E[:,:k]
        QB=euclidean_orth_basis(WB[:,:k])

        WE_B,_,_=b_orthonormalize_span(QE,B)
        WB_B,_,_=b_orthonormalize_span(QB,B)

        task_oracle=float(np.sum(nu[:k]))
        b_oracle=float(np.sum(mu[:k]))

        task_num_E=float(np.trace(QE.T@H@QE))
        task_num_B=float(np.trace(QB.T@H@QB))
        b_num_E=float(np.trace(WE_B.T@H@WE_B))
        b_num_B=float(np.trace(WB_B.T@H@WB_B))

        eta_task_E=task_num_E/task_oracle
        eta_task_B=task_num_B/task_oracle
        eta_B_E=b_num_E/b_oracle
        eta_B_B=b_num_B/b_oracle

        bbar_E=float(np.trace(QE.T@B@QE)/k)
        bbar_B=float(np.trace(QB.T@B@QB)/k)

        X=WB[:,:k].T@B@WO[:,:k]
        cos=np.linalg.svd(X,compute_uv=False)
        cos=np.clip(cos,0.0,1.0)
        min_cos=float(np.min(cos))
        max_angle_deg=float(np.degrees(np.arccos(min_cos)))
        proj_dist=projector_distance_from_cosines(cos,k)

        gamma=None
        if k<r:
            gamma=float((mu[k-1]-mu[k])/mu[k-1]) if mu[k-1]!=0 else None

        rows.append({
            "k":int(k),
            "eta_task_SE":eta_task_E,
            "eta_task_SB":eta_task_B,
            "eta_B_SE":eta_B_E,
            "eta_B_SB":eta_B_B,
            "Delta_sel_task":eta_task_B-eta_task_E,
            "Delta_sel_B":eta_B_B-eta_B_E,
            "bbar_SE":bbar_E,
            "bbar_SB":bbar_B,
            "bbar_ratio_SB_over_SE":bbar_B/bbar_E,
            "task_num_SE":task_num_E,
            "task_num_SB":task_num_B,
            "B_num_SE":b_num_E,
            "B_num_SB":b_num_B,
            "U_task_oracle_sum":task_oracle,
            "U_B_oracle_sum":b_oracle,
            "C_cross_B_SE":b_num_E/total_B_oracle,
            "C_cross_B_SB":b_num_B/total_B_oracle,
            "U_B_fraction":b_oracle/total_B_oracle,
            "B_principal_cosines":[float(x) for x in cos],
            "B_min_principal_cosine":min_cos,
            "B_max_principal_angle_deg":max_angle_deg,
            "B_projector_distance_normalized":proj_dist,
            "heldout_gamma_k":gamma,
            "B_orth_error_train_k":b_inf_error(WB[:,:k],B),
            "B_orth_error_oracle_k":b_inf_error(WO[:,:k],B),
        })

    recon=np.linalg.norm(Bmhalf@B@Bmhalf-np.eye(r),"fro")/np.sqrt(r)
    return {
        "B_eigenvalues":b_ew,
        "B_condition":float(np.max(b_ew)/np.min(b_ew)),
        "B_invsqrt_reconstruction_relative_fro":float(recon),
        "theta":theta,"nu":nu,"glam":glam,"mu":mu,
        "WB":WB,"WO":WO,"Ztrain":Ztrain,"Zoracle":Zoracle,
        "self_scaled_residual_train":self_train,
        "self_scaled_residual_oracle":self_oracle,
        "normwise_backward_train":back_train,
        "normwise_backward_oracle":back_oracle,
        "symmetric_backward_train":sym_train,
        "symmetric_backward_oracle":sym_oracle,
        "B_orth_error_train_full":b_inf_error(WB,B),
        "B_orth_error_oracle_full":b_inf_error(WO,B),
        "rows":rows,
    }
