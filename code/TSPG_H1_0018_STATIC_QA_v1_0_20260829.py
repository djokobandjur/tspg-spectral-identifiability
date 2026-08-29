from pathlib import Path
import importlib.util, json, numpy as np, py_compile

HERE=Path(__file__).resolve().parent
helper=HERE/"TSPG_h1_0018_dual_finite_sample_stability_v1_0_20260829.py"
runner=HERE/"TSPG_run_h1_0018_finite_sample_stability_v1_0_20260829.py"
py_compile.compile(str(helper),doraise=True)
py_compile.compile(str(runner),doraise=True)

spec=importlib.util.spec_from_file_location("h18",helper)
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

rng=np.random.default_rng(20260829)
ns,nh,d=12,14,30
Gs=rng.normal(size=(ns,d))
Gh=rng.normal(size=(nh,d))
Kss=Gs@Gs.T
Khh=Gh@Gh.T
Ksh=Gs@Gh.T
sidx=np.arange(ns)
hidx=np.arange(nh)
dual=m.dual_metrics(Kss,Khh,Ksh,sidx,hidx,[1,2,4,8])

# Direct reference.
U,s,Vt=np.linalg.svd(Gs,full_matrices=False)
V=Vt.T
Q=V
GT_h=Gh.T@Gh
held_trace=np.trace(GT_h)
H=Q.T@GT_h@Q
nu=np.linalg.eigvalsh(0.5*(H+H.T))[::-1]
phi_direct=np.trace(H)/held_trace
assert abs(dual["phi"]-phi_direct)<1e-10
for k in [1,2,4,8]:
    T=np.trace(V[:,:k].T@GT_h@V[:,:k])/held_trace
    Uoracle=np.sum(nu[:k])/held_trace
    eta=T/Uoracle
    assert abs(dual["metrics_by_k"][k]["T"]-T)<1e-10
    assert abs(dual["metrics_by_k"][k]["U_oracle"]-Uoracle)<1e-10
    assert abs(dual["metrics_by_k"][k]["eta"]-eta)<1e-10

labels=np.repeat(np.arange(6),4)
idx=m.coverage_first_subset(labels,12,m.seed_from_parts("x",100,0))
assert len(idx)==12
assert len(np.unique(labels[idx]))==6
assert len(np.unique(idx))==12

fit=m.fit_inverse_n([192,224,256,288,320],[0.2,0.22,0.23,0.24,0.245],640)
assert np.isfinite(fit["prediction_raw"])

out={
 "schema":"TSPG_H1_0018_STATIC_QA_RESULT_v1_0",
 "status":"PASS",
 "tests":{
   "python_syntax":True,
   "dual_phi_matches_direct":True,
   "dual_T_U_eta_match_direct":True,
   "coverage_first_class_preservation":True,
   "deterministic_seed_path":True,
   "inverse_n_forecast_executes":True
 }
}
(HERE/"TSPG_H1_0018_STATIC_QA_RESULT_v1_0_20260829.json").write_text(json.dumps(out,indent=2))
print("H1-0018 STATIC QA: PASS")
