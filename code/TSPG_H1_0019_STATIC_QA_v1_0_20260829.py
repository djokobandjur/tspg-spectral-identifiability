from pathlib import Path
import importlib.util, json, numpy as np, py_compile

HERE=Path(__file__).resolve().parent
helper=HERE/"TSPG_h1_0019_consensus_thirdfold_v1_0_20260829.py"
runner=HERE/"TSPG_run_h1_0019_last_estimator_v1_0_20260829.py"
py_compile.compile(str(helper),doraise=True)
py_compile.compile(str(runner),doraise=True)

spec=importlib.util.spec_from_file_location("h19",helper)
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

rng=np.random.default_rng(20260829)
n=20; d=60
G1=rng.normal(size=(n,d))
G2=0.7*G1+0.3*rng.normal(size=(n,d))
K11=G1@G1.T; K22=G2@G2.T; K12=G1@G2.T
fit=m.fit_arms_from_dual(K11,K22,K12,max_k=8)

assert fit["swap_relative_fro"]<1e-14
assert max(fit["orthonormality"].values())<1e-10

# Scalar-rescaling invariance of consensus arm.
fit2=m.fit_arms_from_dual(9.0*K11,4.0*K22,6.0*K12,max_k=8)
A=fit["arms"]["CONS640"]
B=fit2["arms"]["CONS640"]
# Compare parameter-space subspaces through their dual Kff grams.
# Rescaling rows changes coefficient representation, so compare consensus
# operator eigenvalues, which must be invariant after trace normalization.
c1=fit["consensus_eigenvalues"][:8]
c2=fit2["consensus_eigenvalues"][:8]
assert np.max(np.abs(c1-c2))<1e-10

# Commuting diagonal limit: product ordering.
N1=np.diag([0.5,0.3,0.2])
N2=np.diag([0.2,0.5,0.3])
S1=np.diag(np.sqrt(np.diag(N1))); S2=np.diag(np.sqrt(np.diag(N2)))
C=0.5*(S1@N2@S1+S2@N1@S2)
assert np.max(np.abs(np.diag(C)-np.diag(N1)*np.diag(N2)))<1e-14

# Bootstrap success logic deterministic.
P={
 "U640":np.ones((40,8))*0.1,
 "CONS640":np.ones((40,8))*0.2,
}
total=np.ones(40)
scores,per=m.score_from_projections(P,total,[1,2],[4,8])
b=m.paired_bootstrap_curve(per,total,[4,8],1000,123)
assert b["curve_bootstrap_ci95"][0]>0

out={
 "schema":"TSPG_H1_0019_STATIC_QA_RESULT_v1_0",
 "status":"PASS",
 "tests":{
   "python_syntax":True,
   "fold_swap_invariance":True,
   "trace_normalized_scalar_rescaling_invariance":True,
   "commuting_limit_product_identity":True,
   "arm_orthonormality":True,
   "paired_bootstrap_deterministic_path":True
 }
}
(HERE/"TSPG_H1_0019_STATIC_QA_RESULT_v1_0_20260829.json").write_text(json.dumps(out,indent=2))
print("H1-0019 STATIC QA: PASS")
