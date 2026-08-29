from pathlib import Path
import importlib.util, json, numpy as np, py_compile

HERE=Path(__file__).resolve().parent
helper=HERE/"TSPG_h1_0017_offline_b_normalized_crossfit_v1_1_20260829.py"
runner=HERE/"TSPG_run_h1_0017_offline_b_normalized_crossfit_v1_1_20260829.py"
py_compile.compile(str(helper),doraise=True)
py_compile.compile(str(runner),doraise=True)

spec=importlib.util.spec_from_file_location("h17v11",helper)
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

rng=np.random.default_rng(20260829)
r=12
X=rng.normal(size=(r,r))
C=X@X.T+0.5*np.eye(r)
B=np.eye(r)
H=C.copy()
res=m.analyze(C,H,B,[1,2,4,8])

for row in res["rows"]:
    assert abs(row["eta_task_SE"]-1)<1e-10
    assert abs(row["eta_task_SB"]-1)<1e-10
    assert abs(row["eta_B_SE"]-1)<1e-10
    assert abs(row["eta_B_SB"]-1)<1e-10
    assert abs(row["Delta_sel_task"])<1e-10
    assert abs(row["Delta_sel_B"])<1e-10

assert np.max(res["self_scaled_residual_train"])<1e-10
assert np.max(res["normwise_backward_train"])<1e-10
assert np.max(res["symmetric_backward_train"])<1e-10

# Construct a near-null diagonal tail. Self-scaled residual is still computed,
# while normwise and symmetric backward errors remain the stable certification.
vals=np.geomspace(1.0,1e-14,r)
C2=np.diag(vals)
B2=np.eye(r)
res2=m.analyze(C2,C2,B2,[1,2,4,8])
assert np.max(res2["normwise_backward_train"])<1e-10
assert np.max(res2["symmetric_backward_train"])<1e-10

out={
 "schema":"TSPG_H1_0017_STATIC_QA_v1_1",
 "status":"PASS",
 "tests":{
   "python_syntax":True,
   "identity_case_cross_scoring":True,
   "all_three_residual_diagnostics_computed":True,
   "near_null_normwise_backward_stable":True,
   "near_null_symmetric_backward_stable":True
 }
}
(HERE/"TSPG_H1_0017_STATIC_QA_RESULT_v1_1_20260829.json").write_text(json.dumps(out,indent=2))
print("H1-0017 v1.1 STATIC QA: PASS")
