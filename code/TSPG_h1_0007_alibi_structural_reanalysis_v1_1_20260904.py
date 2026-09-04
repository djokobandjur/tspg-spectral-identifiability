#!/usr/bin/env python3
"""Deterministic reporting-only extension of the archived H1-0007 ALiBi control.

Consumes only the SHA-locked 12x12/320x12 FP64 NPZ. It evaluates the already
frozen Euclidean and generalized selectors, their Euclidean principal-angle
overlap, and sharp fixed-rank trace bounds implied by the complete B spectrum.
No model, GPU, dataset, new gradient, or new G_A action is used.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import numpy as np
from scipy.linalg import eigh

EXPECTED_SHA = "dd8e670f222824fd78eb833bc4cd23f31ac5119ba3ed5eb6921b318c6149329d"
C = 1e-4

def sha256_file(p: Path) -> str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20), b''):
            h.update(b)
    return h.hexdigest()

def canonical_qr(A: np.ndarray) -> np.ndarray:
    Q,R=np.linalg.qr(A, mode='reduced')
    s=np.sign(np.diag(R)); s[s==0]=1.0
    return Q*s

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('npz', type=Path)
    ap.add_argument('--output-json', type=Path, required=True)
    a=ap.parse_args()
    got=sha256_file(a.npz)
    if got!=EXPECTED_SHA: raise SystemExit(f'SHA mismatch {got}')
    with np.load(a.npz, allow_pickle=False) as z:
        GA=np.asarray(z['GA'],np.float64); GT=np.asarray(z['GT'],np.float64); G=np.asarray(z['task_gradients'],np.float64)
    if GA.shape!=(12,12) or GT.shape!=(12,12) or G.shape!=(320,12): raise SystemExit('shape mismatch')
    GT_recon=G.T@G/320.0
    gt_err=float(np.max(np.abs(GT-GT_recon)))
    GA=(GA+GA.T)/2; GT=(GT+GT.T)/2
    tau=C*float(np.trace(GA)); alpha=tau/12.0; B=GA+alpha*np.eye(12)
    be=np.linalg.eigvalsh(B) # ascending
    te,U=np.linalg.eigh(GT); U=U[:,np.argsort(te)[::-1]]
    ge,V=eigh(GT,B); order=np.argsort(ge)[::-1]; ge=ge[order]; V=V[:,order]
    rows=[]
    for k in range(1,13):
        QE=U[:,:k]
        QB=canonical_qr(V[:,:k])
        bE=float(np.trace(QE.T@B@QE)/k); bB=float(np.trace(QB.T@B@QB)/k)
        cos=np.clip(np.linalg.svd(QE.T@QB,compute_uv=False),0,1)
        max_angle=float(np.degrees(np.arccos(float(np.min(cos)))))
        overlap=float(np.mean(cos*cos))
        L=float(np.mean(be[:k])); Ubar=float(np.mean(be[-k:]))
        rows.append({
          'k':k,'k_over_dp':k/12.0,'bbar_SE':bE,'bbar_SB':bB,'R_B_SB_over_SE':bB/bE,
          'selector_principal_cosines':[float(x) for x in cos],
          'selector_max_principal_angle_deg':max_angle,
          'selector_overlap_mean_cos2':overlap,
          'sharp_bbar_lower':L,'sharp_bbar_upper':Ubar,
          'sharp_equal_dimensional_ratio_lower':L/Ubar,
          'sharp_equal_dimensional_ratio_upper':Ubar/L,
        })
    out={
      'schema':'TSPG_H1_0007_ALIBI_STRUCTURAL_REANALYSIS_v1_1',
      'date':'2026-09-04','status':'PASS_REPORTING_ONLY_DETERMINISTIC_ZERO_COMPUTE',
      'evidential_role':'postrun_archived_matrix_structural_readout_not_A52_arm_not_heldout_PE_family_test',
      'source_npz':a.npz.name,'source_npz_sha256':got,'GT_reconstruction_max_abs_error':gt_err,
      'locked_regularization':{'c':C,'trace_GA':float(np.trace(GA)),'tau':tau,'alpha':alpha,'B_definition':'GA + alpha I'},
      'B_spectrum_ascending':[float(x) for x in be],
      'B_lambda_min':float(be[0]),'B_lambda_max':float(be[-1]),'B_condition':float(be[-1]/be[0]),
      'crude_equal_dimensional_ratio_bound':[float(be[0]/be[-1]),float(be[-1]/be[0])],
      'generalized_eigenvalues_top4':[float(x) for x in ge[:4]],'rows':rows,
      'compute_boundary':{'model_loads':0,'gpu_actions':0,'new_task_gradients':0,'new_GA_actions':0,'dataset_access':0,'operation':'12x12 FP64 algebra over archived matrices only'},
      'claim_boundary':{
        'allowed':['The ALiBi B geometry is well conditioned in this archived control.','The normalized and Euclidean selectors remain closely aligned while R_B is mildly below one.','The complete B spectrum gives deterministic fixed-rank bounds on attainable mean-denominator ratios.'],
        'not_allowed':['PE-family portability','causal effect of d_p=12','population inference','a p-value or null-hypothesis test for selector preference','claim that G_A captures every downstream task pathway']
      }
    }
    a.output_json.write_text(json.dumps(out,indent=2)+'\n')
    print('PASS', a.output_json)
    for k in (1,2,4,8,12):
        r=rows[k-1]; print(k, r['R_B_SB_over_SE'], r['selector_overlap_mean_cos2'], r['selector_max_principal_angle_deg'], r['sharp_equal_dimensional_ratio_lower'], r['sharp_equal_dimensional_ratio_upper'])
if __name__=='__main__': main()
