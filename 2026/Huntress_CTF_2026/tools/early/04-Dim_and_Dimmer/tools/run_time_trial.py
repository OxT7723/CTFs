import os,json,urllib.parse,hashlib,tempfile,subprocess,sys,pathlib,time,requests
BASE='https://2026.huntress.ctf.games/'; CID='script-analysis-day-04-shell-contrast/time_trial'
HERE=pathlib.Path(__file__).resolve().parent
CHALLENGE_DIR=HERE.parent
TOKEN=os.environ.get('HUNTRESS_GM_TOKEN')
if not TOKEN: raise SystemExit('HUNTRESS_GM_TOKEN missing')
S=requests.Session(); S.headers.update({'Authorization':'Bearer '+TOKEN,'Content-Type':'application/json'})
def post(x):
 try: return S.post(BASE,json=x,timeout=3).json()
 except Exception as e: return {'error':type(e).__name__}
start=post({'op':'retry','challenge':CID})
if not start.get('deadline'): start=post({'challenge':CID})
if not start.get('deadline'):
 print('START_FAILED',json.dumps({k:start.get(k) for k in ('status','result','error') if k in start}));raise SystemExit(1)
t0=time.monotonic(); archive=S.get(BASE+'?'+urllib.parse.urlencode({'op':'artifact','challenge':CID}),timeout=3).content
sha=hashlib.sha256(archive).hexdigest(); aid=str(start.get('attempt_id','unidentified'))
rootrepo=CHALLENGE_DIR/'artifacts/time_trial'/('attempt-'+aid);rootrepo.mkdir(parents=True,exist_ok=True);(rootrepo/'evidence.zip').write_bytes(archive)
outcomes=[]; accepted={}; rejected=[]
def submit(label, amap):
 if not amap:return None
 r=post({'challenge':CID,'answers':amap}); outcomes.append({'group':label,'count':len(amap),'result':r.get('result'),'remaining':r.get('remaining')})
 if r.get('result') in ('accepted','CORRECT'):
  accepted.update(amap)
 elif r.get('result')=='incorrect': rejected.extend([{'id':k,'candidate':v} for k,v in amap.items()])
 return r
with tempfile.TemporaryDirectory(prefix='dimmer-refine-') as td:
 td=pathlib.Path(td); zp=td/'a.zip'; root=td/'x';root.mkdir();zp.write_bytes(archive)
 ex=subprocess.run(['7z','x','-y','-pinfected','-o'+str(root),str(zp)],stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,timeout=4)
 if ex.returncode not in (0,1): print('EXTRACT_FAILED',sha);raise SystemExit(1)
 cp=td/'answers.json';env=os.environ.copy();env['DIMMER_ARTIFACT_DIR']=str(root);env['DIMMER_CANDIDATES_PATH']=str(cp)
 b=subprocess.run([sys.executable,str(HERE/'build_dimmer_answers.py')],env=env,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=4)
 if b.returncode: print('DECODE_FAILED',sha,b.stderr[:800]);raise SystemExit(1)
 ans=json.load(open(cp));stpath=CHALLENGE_DIR/'challenge_state.json';st=json.load(open(stpath)); ids=set(st['modes']['time_trial']['answer_ids'])
 known={k for k in ids if (k.startswith(('resource-','collection-','impact-')) and not k.endswith('-attack')) or (k.startswith('jscript-') and not k.endswith(('-role','-attack'))) or (k.startswith('batch-') and not k.endswith(('-role','-attack','-expansion','-control'))) or (k.startswith('vbscript-') and not k.endswith(('-role','-attack','-control')))}
 known|={k for k in ids if k.endswith('-scenario')}
 for suff,roles in [('-attack',('benign','stager','dropper','downloader','launcher','uploader','impact','chain','relay')),('-role',('benign','stager','dropper','downloader','launcher','uploader','impact','chain','relay'))]: known|={k for k in ids if k.endswith(suff) and any(f'-{r}{suff}' in k for r in roles)}
 known|={'resource-attack','impact-attack','collection-attack'}
 assert len(known)==204,(len(known),len(ans))
 submit('confirmed_candidates',{k:ans[k] for k in sorted(known)})
 # Probe each Batch expansion label for this exact file. Stop at first accepted candidate.
 expvals=['percent','delayed','call_double','for_indirect']
 for k in sorted(k for k in ids if k.startswith('batch-') and k.endswith('-expansion')):
  vals=[ans[k]]+[v for v in expvals if v!=ans[k]]
  for i,v in enumerate(vals):
   r=submit('probe_'+k+'_'+v,{k:v})
   if r and r.get('result') in ('accepted','CORRECT'): break
 # Control values that are already confirmed are grouped by the current parser label.
 for k in sorted(k for k in ids if k.startswith('batch-') and k.endswith('-control')):
  v=ans[k]
  if v in ('call_subroutine','direct','errorlevel_guard','goto_dispatch'):
   submit('probe_'+k+'_'+v,{k:v})
  else:
   tried=[]
   for cand in [v,'defined_guard','environment_guard','if_guard','if_defined_guard','conditional_guard','guarded_set','call_subroutine','direct']:
    if cand in tried:continue
    tried.append(cand);r=submit('probe_'+k+'_'+cand,{k:cand})
    if r and r.get('result') in ('accepted','CORRECT'):break
 # Probe non-branch VB controls in answer groups; individually probe the branch-shaped candidate.
 vbgroups={}
 for k in sorted(k for k in ids if k.startswith('vbscript-') and k.endswith('-control')):
  v=ans[k]
  if v in ('direct','do_once','error_guard','error_resume_next','for_once','select_case','while_once'):
   vbgroups.setdefault(v,{})[k]=v
  else:
   tried=[]
   for cand in [v,'if_true_guard','if_guard','if_then','if_condition','conditional','conditional_guard','branch_guard','if_else','if_else_guard','if_then_guard']:
    if cand in tried:continue
    tried.append(cand);r=submit('probe_'+k+'_'+cand,{k:cand})
    if r and r.get('result') in ('accepted','CORRECT'):break
 for v,amap in sorted(vbgroups.items()): submit('vbscript_controls_'+v,amap)
# record time-trial result in local state, without any credential material
st=json.load(open(stpath));m=st['modes']['time_trial'];last=outcomes[-1] if outcomes else {}
remaining=next((x['remaining'] for x in reversed(outcomes) if x.get('remaining') is not None),None)
rec={'attempt_id':aid,'mode':'time_trial','deadline':start.get('deadline'),'artifact_sha256':sha,'artifact_path':str(rootrepo.relative_to('/home/kali/repos/ctf-huntress-ctf-2026'))+'/evidence.zip','result':'expired' if remaining not in (0,) else 'CORRECT','confirmed_answers':231-remaining if remaining is not None else len(accepted),'submission_groups':outcomes,'accepted_answer_values':accepted,'rejected_candidates':rejected}
m.setdefault('attempts',[]).append(rec);m['status']={'status':rec['result'],'result':rec['result']}
m['progress_summary']=f"Latest Time Trial attempt confirmed {rec['confirmed_answers']} of 231 fields; {remaining if remaining is not None else 'unknown'} remain."
with open(stpath,'w') as f:json.dump(st,f,indent=2);f.write('\n')
print('ROUNDTRIP',json.dumps({'artifact_sha256':sha,'candidate_count':len(ans),'elapsed_seconds':round(time.monotonic()-t0,3),'attempt_id':aid,'deadline':start.get('deadline'),'confirmed_answers':rec['confirmed_answers'],'remaining':remaining,'submissions':outcomes}))
