#!/usr/bin/env python3
from pathlib import Path
import argparse,json,csv,hashlib,zipfile,shutil
ap=argparse.ArgumentParser(); ap.add_argument('--runtime-root',required=True); ap.add_argument('--package-root',required=True); a=ap.parse_args(); R=Path(a.runtime_root); P=Path(a.package_root); arms=['PV-A','PV-B1','PV-B2','PV-C']
def load(p): return json.loads(p.read_text())
def sha(p):
 h=hashlib.sha256();
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''): h.update(b)
 return h.hexdigest()
res={x:load(R/x/f'TSPG_A52_{x}_RESULT_v1_0_20260903.json') for x in arms}
h1=load(P/'provenance/TSPG_H1_0017_RESULT_v1_1_20260829.json'); r0={int(x['k']):x for x in h1['k_rows']}
rows=[]
for arm in arms:
 for x in res[arm]['P2']['rows']:
  if x['k'] in (4,8,16,32): rows.append({'arm':arm,**{k:x[k] for k in ['k','Delta_sel_task','Delta_sel_B','R_B','M_mean','F_ratio','R_norm','ordering_sentinel','label']}})
# prospective contrast differences are descriptive only
def p2row(arm,k): return next(x for x in res[arm]['P2']['rows'] if x['k']==k)
contr=[]
for name,A,B,layer in [('PV-A__vs__PV-B2','PV-A','PV-B2','FULLY_PROSPECTIVE_ARCHITECTURE_SEED123'),('PV-B1__vs__PV-B2','PV-B1','PV-B2','FULLY_PROSPECTIVE_VITS_SEED'),('R0__vs__PV-A','R0','PV-A','RETROSPECTIVE_ANCHOR_CONTEXT'),('R0__vs__PV-B1','R0','PV-B1','RETROSPECTIVE_ANCHOR_CONTEXT')]:
 for k in (4,8,16,32):
  aa=r0[k] if A=='R0' else p2row(A,k); bb=p2row(B,k); contr.append({'contrast':name,'evidence_layer':layer,'k':k,'Delta_sel_task_difference_A_minus_B':aa['Delta_sel_task']-bb['Delta_sel_task'],'Delta_sel_B_difference_A_minus_B':aa['Delta_sel_B']-bb['Delta_sel_B'],'log10_RB_difference_A_minus_B':__import__('math').log10(aa.get('R_B',aa.get('bbar_ratio_SB_over_SE')))-__import__('math').log10(bb['R_B'])})
all_tech=all(x['technical_status']=='PASS' for x in res.values()); any_noneval=any(x.get('empirical_status')!='EVALUABLE' for x in res.values()); completion=('TECHNICAL_FAIL' if not all_tech else ('PORTABILITY_PARTIAL_NON_EVALUABLE' if any_noneval else 'PORTABILITY_COMPLETE'))
out={'schema':'TSPG_A52_PANEL_SUMMARY_v1_0','run_id':'TSPG-RUN-PV-0001','completion_status':completion,'case_rows':rows,'prespecified_contrasts':contr,'PV-C_caveat':'single checkpoint; no same-regime replicate; dataset, tokenization/input regime, sequence length, and positional dimension change together; deviation cannot be separated from singleton checkpoint variation.'}; (R/'TSPG_A52_PANEL_SUMMARY_v1_0_20260903.json').write_text(json.dumps(out,indent=2)+"\n")
with open(R/'TSPG_A52_PANEL_PRIMARY_ROWS_v1_0_20260903.csv','w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
with open(R/'TSPG_A52_IMAGENET_CROSSED_DESIGN_SUMMARY_v1_0_20260903.csv','w',newline='') as f:
 fields=list(contr[0]); w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(contr)
pvc={'schema':'TSPG_A52_PV_C_STRESS_CASE_SUMMARY_v1_0','arm':'PV-C','empirical_status':res['PV-C']['empirical_status'],'checkpoint_gate':res['PV-C']['checkpoint_gate'],'primary_rows':[x for x in res['PV-C']['P2']['rows'] if x['k'] in (4,8,16,32)],'mandatory_caveat':'single checkpoint; no same-regime replicate; dataset, tokenization/input regime, sequence length, and positional dimension change together; deviation cannot be separated from singleton checkpoint variation.'}; (R/'TSPG_A52_PV_C_STRESS_CASE_SUMMARY_v1_0_20260903.json').write_text(json.dumps(pvc,indent=2)+"\n")
# compact evidence: result json/meta only, raw big artifacts referenced by hashes already in results
E=R.parent/'TSPG_A52_RUNTIME_EVIDENCE_v1_0_20260903'; Z=R.parent/'TSPG_A52_RUNTIME_EVIDENCE_v1_0_20260903.zip'
if E.exists() or Z.exists(): raise RuntimeError('evidence destination exists')
E.mkdir(); shutil.copy2(R/'TSPG_A52_PANEL_SUMMARY_v1_0_20260903.json',E); shutil.copy2(R/'TSPG_A52_PANEL_PRIMARY_ROWS_v1_0_20260903.csv',E)
for arm in arms:
 for pattern in ('*.json','*.csv'):
  for p in (R/arm).glob(pattern): shutil.copy2(p,E/f'{arm}__{p.name}')
for p in [R/'TSPG_A52_IMAGENET_CROSSED_DESIGN_SUMMARY_v1_0_20260903.csv',R/'TSPG_A52_PV_C_STRESS_CASE_SUMMARY_v1_0_20260903.json',P/'TSPG_PROTOCOL_LOCK_v0_52_20260903.md',P/'TSPG_PROTOCOL_AMENDMENT_A52_DIAGNOSTIC_PORTABILITY_PANEL_PUBLIC_SCIENTIFIC_v1_0_20260904.md',P/'TSPG_A52_RUN_CONFIG_v1_0_20260903.json',P/'TSPG_A52_EXPECTED_INVARIANTS_FINAL_v1_0_20260903.json',P/'TSPG_A52_PREDICTIONS_NOT_GATES_v1_0_20260903.json',P/'SHA256SUMS.txt']:
 shutil.copy2(p,E/p.name)
lines=[]
for p in sorted(E.iterdir()):
 if p.is_file(): lines.append(f'{sha(p)}  {p.name}')
(E/'EVIDENCE_SHA256SUMS.txt').write_text('\n'.join(lines)+'\n')
with zipfile.ZipFile(Z,'w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(E.iterdir()): z.write(p,p.name)
with zipfile.ZipFile(Z) as z: assert z.testzip() is None
print('PANEL:',R/'TSPG_A52_PANEL_SUMMARY_v1_0_20260903.json'); print('EVIDENCE ZIP:',Z); print('SHA256:',sha(Z)); print('A52 AGGREGATION/PACKAGING: PASS')
