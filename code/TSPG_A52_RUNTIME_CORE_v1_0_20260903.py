from __future__ import annotations
import os,sys,json,hashlib,time,importlib.util,pickle,csv
from pathlib import Path
import numpy as np
import torch
import torch.nn.functional as F
from torch.utils.data import Dataset,DataLoader,Subset
from torchvision import datasets,transforms
from PIL import Image
from TSPG_A52_REDUCED_METRICS_v1_0_20260903 import analyze_reduced,p1_p3_calibrations

def sha256_file(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''): h.update(b)
 return h.hexdigest()
def load_json(p): return json.loads(Path(p).read_text())
def save_json(p,o): Path(p).write_text(json.dumps(o,indent=2)+"\n")
def import_module(path,name):
 spec=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def state_dict_from_checkpoint(p):
 obj=torch.load(p,map_location='cpu',weights_only=True)

 if isinstance(obj,dict):
  for wk in ('state_dict','model','model_state_dict','net'):
   if wk in obj and isinstance(obj[wk],dict):
    sd=obj[wk]; wrapper=wk
    break
  else:
   sd=obj; wrapper='raw_state_dict'
 else:
  raise RuntimeError('checkpoint is not a state dict')

 # Normalize known training/wrapper namespaces only.
 prefixes=('module.','model.','net.','_orig_mod.')
 cleaned={}
 stripped=set()

 for k,v in sd.items():
  kk=str(k)
  changed=True
  while changed:
   changed=False
   for pref in prefixes:
    if kk.startswith(pref):
     kk=kk[len(pref):]
     stripped.add(pref)
     changed=True
  cleaned[kk]=v

 sd=cleaned

 if stripped:
  wrapper += '+strip_' + '_'.join(
   p.rstrip('.') for p in prefixes if p in stripped
  )

 return sd,wrapper

def hard_gate_checkpoint(arm,base):
 p=Path(arm['checkpoint']);
 if not p.is_file(): raise RuntimeError(f"missing checkpoint: {p}")
 got=sha256_file(p)
 if got!=arm['sha256']: raise RuntimeError(f"checkpoint SHA mismatch: {got}")
 sd,wrapper=state_dict_from_checkpoint(p)
 need={'pos_encoding.pos_embed':(1,arm['seq_len'],arm['embed_dim']),'patch_embed.proj.weight':(arm['embed_dim'],3,arm['patch_size'],arm['patch_size']),'head.weight':(arm['num_classes'],arm['embed_dim']),'blocks.0.attn.qkv.weight':(3*arm['embed_dim'],arm['embed_dim'])}
 shapes={}
 for k,exp in need.items():
  if k not in sd: raise RuntimeError(f"state key missing: {k}")
  sh=tuple(sd[k].shape); shapes[k]=list(sh)
  if sh!=tuple(exp): raise RuntimeError(f"shape mismatch {k}: {sh} != {exp}")
 block_ids=sorted({int(k.split('.')[1]) for k in sd if k.startswith('blocks.') and len(k.split('.'))>2 and k.split('.')[1].isdigit()})
 if block_ids!=list(range(arm['depth'])): raise RuntimeError(f"depth keys mismatch: {block_ids[:3]}...{block_ids[-3:] if block_ids else []}")
 src=base/arm['model_source'];
 if not src.is_file(): raise RuntimeError(f"bundled model source missing: {src}")
 return {'checkpoint':str(p),'sha256':got,'wrapper':wrapper,'state_shapes':shapes,'depth_from_state':len(block_ids),'model_source':str(src),'model_source_sha256':sha256_file(src),'status':'PASS'}

class RawCIFAR100Test(Dataset):
 def __init__(self,root):
  p=Path(root)/'test'
  with open(p,'rb') as f: d=pickle.load(f,encoding='latin1')
  data=d['data'] if 'data' in d else d[b'data']; labels=d.get('fine_labels',d.get(b'fine_labels'))
  self.data=np.asarray(data,dtype=np.uint8).reshape(-1,3,32,32).transpose(0,2,3,1); self.targets=list(map(int,labels))
  self.tf=transforms.Compose([transforms.ToTensor(),transforms.Normalize([0.5071,0.4867,0.4408],[0.2675,0.2565,0.2761])])
 def __len__(self): return len(self.targets)
 def __getitem__(self,i): return self.tf(Image.fromarray(self.data[i])),self.targets[i]

def build_dataset(arm):
 if arm['split']=='ImageNet':
  tf=transforms.Compose([transforms.Resize(256),transforms.CenterCrop(224),transforms.ToTensor(),transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])]); return datasets.ImageFolder(arm['dataset_root'],transform=tf)
 return RawCIFAR100Test(arm['dataset_root'])
def split_indices(base,arm):
 if arm['split']=='ImageNet':
  d=load_json(base/'manifests/TSPG_SPLIT_MANIFEST_IN100_PILOT_v1_0_20260819.json')['indices']; return list(d['calibration_C']),list(d['geometry_A_G_1']),list(d['geometry_A_G_2'])
 d=load_json(base/'manifests/TSPG_A52_CIFAR_SPLIT_MANIFEST_v1_1_RECONSTRUCTED_20260903.json')['indices']; return list(d['C']),list(d['AG1']),list(d['AG2'])

def build_model(arm,base,device):
 src=base/arm['model_source']; mod=import_module(src,'a52_model_'+str(os.getpid())+'_'+str(arm['seed']))
 model=mod.VisionTransformer(img_size=arm['img_size'],patch_size=arm['patch_size'],num_classes=arm['num_classes'],embed_dim=arm['embed_dim'],depth=arm['depth'],num_heads=arm['num_heads'],mlp_ratio=4.0,dropout=0.1,pe_type='learned')
 sd,_=state_dict_from_checkpoint(arm['checkpoint']); model.load_state_dict(sd,strict=True); model.eval().to(device); return model

def math_ctx():
 try:
  from torch.nn.attention import sdpa_kernel,SDPBackend
  return sdpa_kernel(backends=[SDPBackend.MATH])
 except Exception:
  class C:
   def __enter__(self):
    self.x=torch.backends.cuda.sdp_kernel(enable_flash=False,enable_math=True,enable_mem_efficient=False,enable_cudnn=False); return self.x.__enter__()
   def __exit__(self,*a): return self.x.__exit__(*a)
  return C()
def native_d(model): return int(model.pos_encoding.pos_embed.numel())
def forward_delta(model,images,delta,return_centered=False):
 B=images.shape[0]; dsh=delta.reshape(model.pos_encoding.pos_embed.shape); x=model.patch_embed(images); cls=model.cls_token.expand(B,-1,-1); x=torch.cat([cls,x],dim=1); x=x+model.pos_encoding.pos_embed+dsh; centered=[]
 with math_ctx():
  for block in model.blocks:
   y=block.norm1(x); attn=block.attn; bs,n,ch=y.shape; qkv=attn.qkv(y).reshape(bs,n,3,attn.num_heads,attn.head_dim).permute(2,0,3,1,4); q,k,v=qkv[0],qkv[1],qkv[2]; z=(q@k.transpose(-2,-1))*attn.scale
   if return_centered: centered.append(z-z.mean(dim=-1,keepdim=True))
   out=F.scaled_dot_product_attention(q,k,v,dropout_p=0.0); out=out.transpose(1,2).reshape(bs,n,ch); x=x+attn.proj(out); x=x+block.mlp(block.norm2(x))
 x=model.norm(x); logits=model.head(x[:,0]); return (logits,tuple(centered)) if return_centered else logits
def zero(model,device): return torch.zeros(native_d(model),device=device,dtype=torch.float64)
def centered_map(model,images):
 def fn(delta): return forward_delta(model,images,delta,True)[1]
 return fn
def tenergy(xs): return sum(x.double().square().sum() for x in xs)

def clean_C_accuracy(model,dataset,idx,device,batch=32):
 loader=DataLoader(Subset(dataset,idx),batch_size=batch,shuffle=False,num_workers=0); n=cor=0
 with torch.no_grad():
  for x,y in loader:
   x=x.to(device); y=y.to(device); z=model(x); cor += int((z.argmax(1)==y).sum()); n += len(y)
 return {'n':n,'accuracy_percent':100*cor/n}

def ga_serial(model,dataset,idx,v,device,batch=1):
 loader=DataLoader(Subset(dataset,idx),batch_size=batch,shuffle=False,num_workers=0); v=v.reshape(-1).to(device=device,dtype=torch.float64); z0=zero(model,device); gsum=torch.zeros_like(z0); ce=torch.zeros((),device=device,dtype=torch.float64); te=torch.zeros_like(ce); t=time.time()
 for x,_ in loader:
  x=x.to(device=device,dtype=torch.float64); fn=centered_map(model,x); clean,vjp=torch.func.vjp(fn,z0); _,jv=torch.func.jvp(fn,(z0,),(v,)); g=vjp(jv)[0]; gsum+=g.detach(); ce+=tenergy(clean).detach(); te+=tenergy(jv).detach()
 gav=gsum/ce; return {'ga_v':gav.detach(),'q_dot':float(torch.dot(v,gav)),'q_direct':float(te/ce),'clean_energy':float(ce),'elapsed_sec':time.time()-t}
def ga_block_vmap(model,dataset,idx,V,device,batch=1):
 loader=DataLoader(Subset(dataset,idx),batch_size=batch,shuffle=False,num_workers=0); V=V.to(device=device,dtype=torch.float64); V=V[:,None] if V.ndim==1 else V; d,m=V.shape; z0=zero(model,device); gs=torch.zeros((d,m),device=device,dtype=torch.float64); ce=torch.zeros((),device=device,dtype=torch.float64); te=torch.zeros((m,),device=device,dtype=torch.float64); t=time.time()
 for x,_ in loader:
  x=x.to(device=device,dtype=torch.float64); fn=centered_map(model,x); clean,vjp=torch.func.vjp(fn,z0); ce+=tenergy(clean).detach()
  def jone(v): return torch.func.jvp(fn,(z0,),(v,))[1]
  jvs=torch.vmap(jone,in_dims=1,out_dims=0)(V)
  def pb(*cts): return vjp(tuple(cts))[0]
  grads=torch.vmap(pb,in_dims=tuple(0 for _ in jvs),out_dims=0)(*jvs); gs += grads.T.detach()
  for j in range(m): te[j]+=tenergy(tuple(q[j] for q in jvs)).detach()
 gav=gs/ce; qdot=(V*gav).sum(0); return {'ga_V':gav.detach(),'q_dot':qdot.detach().cpu().numpy(),'q_direct':(te/ce).detach().cpu().numpy(),'elapsed_sec':time.time()-t,'mode':'vmap'}
def ga_block_shared(model,dataset,idx,V,device,batch=1):
 loader=DataLoader(Subset(dataset,idx),batch_size=batch,shuffle=False,num_workers=0); V=V.to(device=device,dtype=torch.float64); V=V[:,None] if V.ndim==1 else V; d,m=V.shape; z0=zero(model,device); gs=torch.zeros((d,m),device=device,dtype=torch.float64); ce=torch.zeros((),device=device,dtype=torch.float64); te=torch.zeros((m,),device=device,dtype=torch.float64); t=time.time()
 for x,_ in loader:
  x=x.to(device=device,dtype=torch.float64); fn=centered_map(model,x); clean,vjp=torch.func.vjp(fn,z0); ce+=tenergy(clean).detach(); cols=[]
  for j in range(m):
   _,jv=torch.func.jvp(fn,(z0,),(V[:,j],)); cols.append(vjp(jv)[0].detach()); te[j]+=tenergy(jv).detach()
  gs += torch.stack(cols,1)
 gav=gs/ce; return {'ga_V':gav.detach(),'q_dot':((V*gav).sum(0)).detach().cpu().numpy(),'q_direct':(te/ce).detach().cpu().numpy(),'elapsed_sec':time.time()-t,'mode':'shared_vjp_loop'}
def ga_block(mode,*a,**k): return ga_block_vmap(*a,**k) if mode=='vmap' else ga_block_shared(*a,**k)

def certify_ga(model,dataset,C,device,cfg):
 d=native_d(model); dirs=[]
 for seed in cfg['ga_certification']['seeds']:
  rng=np.random.default_rng(seed); v=(2*rng.integers(0,2,size=d,dtype=np.int8)-1).astype(np.float64); v/=np.linalg.norm(v); dirs.append(v)
 V=np.stack(dirs,1); short=C[:8]; refs=[ga_serial(model,dataset,short,torch.from_numpy(V[:,j]),device) for j in range(4)]; A=np.stack([r['ga_v'].cpu().numpy() for r in refs],1); qref=np.array([r['q_dot'] for r in refs]); candidates=[]; selected=None
 for mode in ['vmap','shared_vjp_loop']:
  try:
   rr=ga_block(mode,model,dataset,short,torch.from_numpy(V),device); B=rr['ga_V'].cpu().numpy(); rel=np.linalg.norm(B-A,axis=0)/np.maximum(np.linalg.norm(A,axis=0),1e-30); qrel=np.abs(np.asarray(rr['q_dot'])-qref)/np.maximum(np.abs(qref),1e-30); passed=bool(rel.max()<=cfg['ga_certification']['relative_l2_gate'] and qrel.max()<=cfg['ga_certification']['quadratic_relative_gate']); candidates.append({'mode':mode,'supported':True,'pass':passed,'relative_l2_per_column':rel.tolist(),'relative_l2_max':float(rel.max()),'quadratic_relative_per_column':qrel.tolist(),'quadratic_relative_max':float(qrel.max()),'elapsed_sec':rr['elapsed_sec']});
   if passed and selected is None: selected=mode
  except Exception as e: candidates.append({'mode':mode,'supported':False,'pass':False,'exception':repr(e)})
 if selected is None: raise RuntimeError(f"G_A block certification failed: {candidates}")
 return {'status':'PASS','selected_mode':selected,'candidates':candidates,'actions':8}

def trace_probe(model,dataset,C,v,device):
 # JVP-only exact quadratic on fixed C. One direction-action.
 loader=DataLoader(Subset(dataset,C),batch_size=1,shuffle=False,num_workers=0); v=v.to(device=device,dtype=torch.float64); z0=zero(model,device); ce=torch.zeros((),device=device,dtype=torch.float64); te=torch.zeros_like(ce)
 for x,_ in loader:
  x=x.to(device=device,dtype=torch.float64); fn=centered_map(model,x); clean,jv=torch.func.jvp(fn,(z0,),(v,)); ce+=tenergy(clean).detach(); te+=tenergy(jv).detach()
 return float(te/ce)
def adaptive_trace(model,dataset,C,device,cfg):
 vals=[]; base=cfg['trace']['seed_base_learned']; gate=cfg['trace']['rse_gate']; selected=None
 for target in cfg['trace']['probe_counts']:
  while len(vals)<target:
   j=len(vals); rng=np.random.default_rng(base+j); z=(2*rng.integers(0,2,size=native_d(model),dtype=np.int8)-1).astype(np.float64); q=trace_probe(model,dataset,C,torch.from_numpy(z),device); vals.append(q); print(f"TRACE {j+1}/{target} q={q:.8g}",flush=True)
  a=np.asarray(vals); mean=float(a.mean()); sd=float(a.std(ddof=1)); se=sd/np.sqrt(len(a)); rse=se/abs(mean) if mean!=0 else float('inf'); print(f"TRACE checkpoint n={len(a)} mean={mean:.8g} RSE={rse:.6g}",flush=True)
  if rse<=gate: selected=len(a); break
 if selected is None: raise RuntimeError('TRACE_ESTIMATION_GATE_FAIL')
 mean=float(np.mean(vals)); sd=float(np.std(vals,ddof=1)); se=sd/np.sqrt(len(vals)); return {'status':'PASS','values':vals,'n':len(vals),'trace_hat':mean,'sd':sd,'se':se,'rse':se/abs(mean),'tau':cfg['trace']['c']*mean,'actions':len(vals)}

def scalar_task_gradients(model,dataset,idx,device,out_path):
 rows=[]; losses=[]; t=time.time()
 for n,i in enumerate(idx,1):
  x,y=dataset[i]; x=x.unsqueeze(0).to(device=device,dtype=torch.float64); y=torch.tensor([y],device=device); d=zero(model,device).requires_grad_(True); logits=forward_delta(model,x,d,False); loss=F.cross_entropy(logits,y,reduction='sum'); g=torch.autograd.grad(loss,d)[0]; rows.append(g.detach().cpu().numpy()); losses.append(float(loss));
  if n==1 or n%20==0: print(f"TASK_GRAD {n}/{len(idx)} elapsed={time.time()-t:.1f}s",flush=True)
 G=np.stack(rows,0); np.save(out_path,G); return {'path':str(out_path),'shape':list(G.shape),'losses':losses,'elapsed_sec':time.time()-t,'G':G}
def compute_GAQ(model,dataset,C,Q,mode,device,out_path,block=4):
 d,r=Q.shape; Y=np.empty((d,r),dtype=np.float64); t=time.time()
 for s in range(0,r,block):
  e=min(s+block,r); rr=ga_block(mode,model,dataset,C,torch.from_numpy(Q[:,s:e]),device); Y[:,s:e]=rr['ga_V'].cpu().numpy(); print(f"GA_SUPPORT {e}/{r} elapsed={time.time()-t:.1f}s mode={mode}",flush=True)
 np.save(out_path,Y); return {'path':str(out_path),'shape':list(Y.shape),'actions':r,'elapsed_sec':time.time()-t,'Y':Y}

def run_arm(base,arm_id,outdir,device='cuda'):
 base=Path(base); cfg=load_json(base/'TSPG_A52_RUN_CONFIG_v1_0_20260903.json'); arm=cfg['arms'][arm_id]; outdir=Path(outdir)
 if outdir.exists(): raise RuntimeError(f"output exists: {outdir}")
 gate=hard_gate_checkpoint(arm,base); outdir.mkdir(parents=True); save_json(outdir/'checkpoint_gate.json',gate)
 dataset=build_dataset(arm); C,A1,A2=split_indices(base,arm); model=build_model(arm,base,device); clean=clean_C_accuracy(model,dataset,C,device); model=model.double();
 for p in model.parameters(): p.requires_grad_(False)
 print('C clean:',clean,flush=True)
 cert=certify_ga(model,dataset,C,device,cfg); save_json(outdir/'ga_certification.json',cert)
 tr=adaptive_trace(model,dataset,C,device,cfg); d=native_d(model); alpha=tr['tau']/d; tr['alpha']=alpha; save_json(outdir/'trace.json',tr)
 g1=scalar_task_gradients(model,dataset,A1,device,outdir/'AG1_gradients.npy'); G1=g1.pop('G'); save_json(outdir/'AG1_gradient_meta.json',g1)
 g2=scalar_task_gradients(model,dataset,A2,device,outdir/'AG2_gradients.npy'); G2=g2.pop('G'); save_json(outdir/'AG2_gradient_meta.json',g2)
 Q,R=np.linalg.qr(G1.T,mode='reduced'); np.save(outdir/'Q1.npy',Q); C1=(G1@Q).T@(G1@Q)/len(A1); H21=(G2@Q).T@(G2@Q)/len(A2); C1=.5*(C1+C1.T); H21=.5*(H21+H21.T)
 theta_pre=np.linalg.eigvalsh(C1)[::-1]; lam1_pre=float(theta_pre[0]); tol_pre=float(C1.shape[0]*np.finfo(np.float64).eps*lam1_pre); rnum_pre=int(np.sum(theta_pre>tol_pre)); ratio64_pre=(float(theta_pre[63]/lam1_pre) if len(theta_pre)>=64 and lam1_pre!=0 else None); constructive_evaluable=bool(rnum_pre>=cfg['rank_gate']['min_r_num'] and ratio64_pre is not None and ratio64_pre>cfg['rank_gate']['lambda64_over_lambda1_strict_gt'])
 cal=p1_p3_calibrations(C1,tuple(cfg['primary_ranks'])); cal['constructive_gate_precheck']={'lambda_1':lam1_pre,'lambda_64':(float(theta_pre[63]) if len(theta_pre)>=64 else None),'lambda64_over_lambda1':ratio64_pre,'tol_rank':tol_pre,'r_num':rnum_pre,'evaluable':constructive_evaluable}; cal['status']=('CALIBRATION_PASS' if constructive_evaluable and cal['pass'] else ('NON_EVALUABLE_CONSTRUCTIVE_STABILITY_GATE' if not constructive_evaluable else 'CALIBRATION_CONTROL_FAIL')); save_json(outdir/'P1_P3_calibration.json',cal)
 if constructive_evaluable and not cal['pass']: raise RuntimeError('CALIBRATION_CONTROL_FAIL P1/P3')
 gaq=compute_GAQ(model,dataset,C,Q,cert['selected_mode'],device,outdir/'GA_Q1.npy',block=4); Y=gaq.pop('Y'); save_json(outdir/'GA_support_meta.json',gaq)
 A11=.5*(Q.T@Y+(Q.T@Y).T); B11=A11+alpha*np.eye(A11.shape[0]); np.savez(outdir/'reduced_matrices.npz',C1=C1,H21=H21,A11=A11,B11=B11,alpha=np.array(alpha))
 p2=analyze_reduced(C1,H21,B11,tuple(cfg['rank_ladder']),alpha=alpha,eps_label=cfg['labels']['eps_label'],eps_R=cfg['labels']['eps_R'])
 gates=cfg['numerical_gates']; ms=p2['matrix_summary']; numer_pass=bool(ms['B_min_eigenvalue']>0 and ms['B_invsqrt_reconstruction_relative_fro']<=gates['B_invsqrt_reconstruction_relative_fro'] and ms['B_orth_error_train_full']<=gates['B_orthonormality_inf'] and ms['B_orth_error_oracle_full']<=gates['B_orthonormality_inf'] and ms['self_scaled_residual_train_max_top32']<=gates['self_scaled_generalized_residual_top32'] and ms['self_scaled_residual_oracle_max_top32']<=gates['self_scaled_generalized_residual_top32'] and ms['normwise_backward_train_max_all']<=gates['normwise_generalized_backward_error_all'] and ms['normwise_backward_oracle_max_all']<=gates['normwise_generalized_backward_error_all'] and ms['symmetric_backward_train_max_all']<=gates['symmetric_backward_error_all'] and ms['symmetric_backward_oracle_max_all']<=gates['symmetric_backward_error_all'])
 for row in p2['rows']: numer_pass &= row['Q_B_orth_error_inf']<=gates['qr_orthonormality_inf'] and row['Q_B_raw_span_equivalence_relative_fro']<=gates['qr_span_equivalence_relative_fro'] and max(row['eta_task_SE'],row['eta_task_SB'],row['eta_B_SE'],row['eta_B_SB'])<=gates['efficiency_upper'] and max(row['euclidean_selector_principal_cosines']+row['B_principal_cosines'])<=gates['principal_cosine_upper'] and row['exact_identity_relative_error']<=1e-10
 if not numer_pass: raise RuntimeError('P2_NUMERICAL_CERTIFICATION_FAIL')
 # Machine-readable/tabular post-run artifacts required by the lock.
 p2_fields=['k','eta_task_SE','eta_task_SB','eta_B_SE','eta_B_SB','Delta_sel_task','Delta_sel_B','bbar_SE','bbar_SB','R_B','task_num_SE','task_num_SB','B_num_SE','B_num_SB','U_task_oracle_sum','U_B_oracle_sum','tau_task','R_norm','M_mean','F_SE','F_SB','F_ratio','exact_identity_relative_error','ordering_sentinel','label','B_SIGN','TASK_SIGN','DEN_REL','heldout_gamma_k','Bgram_SE_condition','Bgram_SB_condition','euclidean_selector_max_angle_deg','euclidean_selector_projector_distance','B_max_principal_angle_deg','B_projector_distance_normalized']
 with open(outdir/'P2_2x2_v1_0_20260903.csv','w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=p2_fields); w.writeheader(); w.writerows([{k:r.get(k) for k in p2_fields} for r in p2['rows']])
 cal_rows=[]
 for kind in ['P1','P3']:
  for r in cal[kind]: cal_rows.append({'control':kind,**r})
 cal_fields=sorted(set().union(*(x.keys() for x in cal_rows))) if cal_rows else ['control']
 with open(outdir/'P1_P3_calibration_v1_0_20260903.csv','w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=cal_fields); w.writeheader(); w.writerows(cal_rows)
 cert_rows=[]
 for r in p2['rows']:
  cert_rows.append({'k':r['k'],'Q_B_orth_error_inf':r['Q_B_orth_error_inf'],'Q_B_raw_span_equivalence_relative_fro':r['Q_B_raw_span_equivalence_relative_fro'],'exact_identity_relative_error':r['exact_identity_relative_error'],'max_efficiency':max(r['eta_task_SE'],r['eta_task_SB'],r['eta_B_SE'],r['eta_B_SB']),'max_principal_cosine':max(r['euclidean_selector_principal_cosines']+r['B_principal_cosines'])})
 save_json(outdir/'numerical_certification_v1_0_20260903.json',{'status':'PASS','matrix_summary':p2['matrix_summary'],'task_rank_gate':p2['task_rank_gate'],'row_checks':cert_rows,'gates':gates})
 save_json(outdir/'runtime_provenance_v1_0_20260903.json',{'arm':arm_id,'checkpoint':gate,'dataset_root':arm['dataset_root'],'split_kind':arm['split'],'split_sizes':{'C':len(C),'AG1':len(A1),'AG2':len(A2)},'locked_run_config_sha256':sha256_file(base/'TSPG_A52_RUN_CONFIG_v1_0_20260903.json'),'locked_protocol_sha256':sha256_file(base/'TSPG_PROTOCOL_AMENDMENT_A52_DIAGNOSTIC_PORTABILITY_PANEL_PUBLIC_SCIENTIFIC_v1_0_20260904.md')})
 rank_pass=p2['task_rank_gate']['pass']; assert bool(rank_pass)==bool(constructive_evaluable), (p2['task_rank_gate'],cal['constructive_gate_precheck']); empirical_status='EVALUABLE' if rank_pass else 'P2_COMPUTED_P1_P3_NON_EVALUABLE_CONSTRUCTIVE_STABILITY_GATE'
 if len(A1)+len(A2)!=cfg['compute_ceiling']['task_gradients_per_arm']: raise RuntimeError('TASK_GRADIENT_ACCOUNTING_FAIL')
 if gaq['actions']>cfg['compute_ceiling']['support_ga_actions_per_arm_max']: raise RuntimeError('SUPPORT_GA_ACTION_CEILING_EXCEEDED')
 if tr['actions']>cfg['compute_ceiling']['trace_jvp_actions_per_arm_max']: raise RuntimeError('TRACE_ACTION_CEILING_EXCEEDED')
 result={'schema':'TSPG_A52_ARM_RESULT_v1_0','run_id':'TSPG-RUN-PV-0001','arm':arm_id,'technical_status':'PASS','empirical_status':empirical_status,'checkpoint_gate':gate,'clean_C_preflight':clean,'ga_certification':cert,'trace':tr,'compute_accounting':{'task_gradients':len(A1)+len(A2),'support_ga_actions':gaq['actions'],'trace_actions':tr['actions'],'cert_actions':8,'total_geometry_direction_actions':gaq['actions']+tr['actions']+8},'P1_P3':cal,'P2':p2,'raw_artifacts':{}}
 for fn in ['AG1_gradients.npy','AG2_gradients.npy','Q1.npy','GA_Q1.npy','reduced_matrices.npz']:
  p=outdir/fn; result['raw_artifacts'][fn]={'sha256':sha256_file(p),'size_bytes':p.stat().st_size}
 save_json(outdir/f'TSPG_A52_{arm_id}_RESULT_v1_0_20260903.json',result); print('ARM PASS',arm_id,empirical_status,flush=True); return result
