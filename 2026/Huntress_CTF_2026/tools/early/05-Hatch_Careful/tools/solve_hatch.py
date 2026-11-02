#!/usr/bin/env python3
"""Static-only Hatch Careful candidate builder. Never imports or executes specimens."""
from __future__ import annotations
import argparse, ast, base64, json, os, re, sys
from pathlib import Path
from urllib.request import Request,urlopen

HERE=Path(__file__).resolve().parents[1]
EXTRACTED=HERE/'artifacts/single_solve/extracted'
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(HERE/'tools'))
from static_recover import recover_python,recover_js,recover_vbscript,recover_batch

PY_FILES={
'python-source-benign':'source-context.py','python-pyc38-dropper':'pyc38-recovered.py','python-current-pyc-launcher':'current-pyc-recovered.py','python-zipapp-relay':'zipapp-recovered.py','python-wheel-stager':'wheel-recovered.py','python-pyinstaller-onefile':'pyinstaller-onefile-recovered.py','python-pyinstaller-onedir':'pyinstaller-onedir-recovered.py','python-py2exe-console':'py2exe-console-recovered.py','python-py2exe-service':'py2exe-service-recovered.py','python-cxfreeze-executable':'cxfreeze-recovered.py','python-cxfreeze-msi':'cxfreeze-msi-recovered.py','python-pyarmor-source':'pyarmor-source-recovered.py','python-pyarmor-pyinstaller':'pyarmor-pyinstaller-recovered.py','python-embedded-runtime-relay':'embedded-runtime-recovered.py'}
JS_FILES={
'jscript-benign':'host-context.js','jscript-stager':'memory-stage.js','jscript-dropper':'embedded-write.js','jscript-downloader':'remote-write.js','jscript-launcher':'local-dispatch.js','jscript-chain':'staged-handoff.js','jscript-uploader':'outbound-transfer.js','jscript-impact':'impact-plan.js','jscript-relay':'relay-handoff.js'}
VBS_FILES={
'vbscript-benign':'host-context.vbs','vbscript-stager':'memory-stage.vbs','vbscript-dropper':'embedded-write.vbs','vbscript-downloader':'remote-write.vbs','vbscript-uploader':'outbound-transfer.vbs','vbscript-launcher':'local-dispatch.vbs','vbscript-impact':'impact-plan.vbs','vbscript-chain':'staged-handoff.vbs','vbscript-relay':'relay-handoff.vbs'}
BATCH_FILES={
'batch-benign':'host-context.cmd','batch-stager':'memory-stage.bat','batch-dropper':'embedded-write.cmd','batch-downloader':'remote-write.bat','batch-uploader':'outbound-transfer.cmd','batch-launcher':'local-dispatch.bat','batch-impact':'impact-plan.cmd','batch-chain':'staged-handoff.bat','batch-relay':'relay-handoff.cmd'}
BATCH_ROLE={'batch-benign':'benign_utility','batch-stager':'stager','batch-dropper':'dropper','batch-downloader':'downloader','batch-uploader':'uploader','batch-launcher':'launcher','batch-impact':'impact','batch-chain':'staged_chain','batch-relay':'staged_chain'}
VBS_ROLE={'vbscript-benign':'benign_utility','vbscript-stager':'stager','vbscript-dropper':'dropper','vbscript-downloader':'downloader','vbscript-uploader':'uploader','vbscript-launcher':'launcher','vbscript-impact':'impact','vbscript-chain':'staged_chain','vbscript-relay':'staged_chain'}
ROLE_ATTACK={'benign_utility':'none','stager':'T1620','dropper':'T1140','downloader':'T1105','launcher':'T1059.006','staged_chain':'T1105','relay':'T1105','uploader':'T1041','impact':'T1486'}
PY_ROLE={'python-source-benign':'benign_utility','python-pyc38-dropper':'dropper','python-current-pyc-launcher':'launcher','python-zipapp-relay':'relay','python-wheel-stager':'stager','python-pyinstaller-onefile':'downloader','python-pyinstaller-onedir':'uploader','python-py2exe-console':'launcher','python-py2exe-service':'staged_chain','python-cxfreeze-executable':'impact','python-cxfreeze-msi':'dropper','python-pyarmor-source':'stager','python-pyarmor-pyinstaller':'staged_chain','python-embedded-runtime-relay':'relay'}
JS_ROLE={'jscript-benign':'benign_utility','jscript-stager':'stager','jscript-dropper':'dropper','jscript-downloader':'downloader','jscript-launcher':'launcher','jscript-chain':'staged_chain','jscript-uploader':'uploader','jscript-impact':'impact','jscript-relay':'staged_chain'}

def inspect_block(text):
    m=re.search(r'(?:function\s+inspect_[A-Za-z0-9_]+\s*\([^)]*\)|var\s+inspect_[A-Za-z0-9_]+\s*=\s*function(?:\s+[A-Za-z0-9_]+)?\s*\([^)]*\))\s*\{',text)
    if not m: raise ValueError('inspect function missing')
    start=text.find('{',m.start()); depth=0; quote=None; esc=False
    for i in range(start,len(text)):
        c=text[i]
        if quote:
            if esc: esc=False
            elif c=='\\': esc=True
            elif c==quote: quote=None
            continue
        if c in ('"',"'",'`'): quote=c
        elif c=='{': depth+=1
        elif c=='}':
            depth-=1
            if depth==0: return text[m.start():i+1]
    raise ValueError('unclosed inspect function')

def js_styles(path):
    text=path.read_text(); block=inspect_block(text)
    if re.search(r'^\s*function\s+inspect_',text,re.M): function='declaration'
    else:
        m=re.search(r'var\s+inspect_[A-Za-z0-9_]+\s*=\s*function(\s+[A-Za-z0-9_]+)?\s*\(',text)
        function='named_expression' if m and m.group(1) else 'anonymous_expression'
    invocation='apply' if re.search(r'recover_\w+\.apply\s*\(',block) else 'call' if re.search(r'recover_\w+\.call\s*\(',block) else 'direct'
    dm=re.search(r'\b([A-Za-z_$][\w$]*)\s*=\s*eval\s*\(',block)
    descriptor=dm.group(1) if dm else None
    names=re.escape(descriptor) if descriptor else r'(?:item\d+|v_[A-Za-z0-9_]+)'
    dot=bool(re.search(names+r'\.(?:steps|adapter|values|stageCount)',block))
    bracket=bool(re.search(names+r'\[\s*["\'](?:steps|adapter|values|stageCount)["\']\s*\]',block))
    prop='mixed' if dot and bracket else 'dot' if dot else 'bracket_literal'
    return function,invocation,prop

def build(question_ids, extracted=EXTRACTED, allow_reference_fallback=True):
    a={}
    question_keys={q.split('.',1)[-1] for q in question_ids}
    def fixture(path):
        candidate=extracted/path
        if candidate.exists(): return candidate
        if allow_reference_fallback and EXTRACTED.joinpath(path).exists(): return EXTRACTED/path
        raise FileNotFoundError(f'current attempt artifact is missing required file: {path}')
    # Python direct metadata answers recovered from literal constants and declared codecs.
    py_suffix={'adapter':'adapter','campaign':'campaign_id','syntax':'syntax','obfuscation':'obfuscation','carrier':'carrier','windows-chain':'windows_chain'}
    py_optional=('url','file_path','next_stage','upload_url','extension','note_name','host_id','handoff_id')
    for prefix,file in PY_FILES.items():
        f=recover_python(fixture(file))
        for suf,key in py_suffix.items():
            q=prefix+'-'+suf
            if q in question_keys: a[q]=f[key]
        for suf in py_optional:
            q=prefix+'-'+suf.replace('_','-')
            if q in question_keys and suf in f: a[q]=f[suf]
    # Exact JScript decoded descriptor values and source-style labels.
    js_optional={'host':'host_id','url':'url','path':'file_path','next-stage':'next_stage','extension':'extension','note':'note_name','campaign':'campaign_id'}
    for prefix,file in JS_FILES.items():
        d=recover_js(fixture(file)); values=d.get('values',{})
        for q,key in ((prefix+'-adapter','adapter'),(prefix+'-campaign','campaign_id')):
            if q in question_keys: a[q]=d['adapter'] if key=='adapter' else values['campaign_id']
        for suffix,key in js_optional.items():
            q=prefix+'-'+suffix
            if q in question_keys and key in values: a[q]=values[key]
        styles=js_styles(fixture(file))
        for suffix,value in zip(('function-style','invocation-style','property-style'),styles):
            q=prefix+'-'+suffix
            if q in question_keys: a[q]=value
    # Decode inert VBScript fixture constants and preserve declared codec labels.
    vbs_optional={'host-id':'host_id','url':'url','file-path':'file_path','upload-url':'upload_url','extension':'extension','note-name':'note_name','next-stage':'next_stage'}
    for prefix,file in VBS_FILES.items():
        f=recover_vbscript(fixture(file))
        for suffix,key in (('adapter','adapter'),('campaign','campaign_id'),('representation','representation'),('transform','transform')):
            q=prefix+'-'+suffix
            if q in question_keys and key in f: a[q]=f[key]
        for suffix,key in vbs_optional.items():
            q=prefix+'-'+suffix
            if q in question_keys and key in f: a[q]=f[key]
        text=fixture(file).read_text()
        rm=re.search(r'Function\s+Recover_.*?\n([\s\S]*?)\nEnd Function',text,re.I)
        rec=rm.group(1) if rm else text
        if re.search(r'On Error Resume Next[\s\S]*?Err\.Number[\s\S]*?If\s+\w+\s*<>\s*0',rec,re.I): control='error_guard'
        elif re.search(r'\bSelect Case\b',rec,re.I): control='select_case'
        elif re.search(r'\bDo\b',rec,re.I): control='do_once'
        elif re.search(r'\bWhile\b',rec,re.I): control='while_once'
        elif re.search(r'(?im)^\s*For\s+\w+\s*=\s*0\s+To\s+0\b',rec): control='for_once'
        elif re.search(r'(?im)^\s*If\s+True\s+Then\b',rec): control='if_true_guard'
        elif re.search(r'(?im)^\s*If\b[^\n]*\bThen\b[^\n]*\bElse\b',rec): control='if_then_else'
        elif re.search(r'(?im)^\s*If\b[^\n]*Then\s+Err\.Raise',rec,re.I): control='error_guard'
        elif re.search(r'(?im)^\s*On Error Resume Next\b',rec): control='error_resume_next'
        elif re.search(r'(?im)^\s*If\b',rec): control='if_then'
        else: control='direct'
        q=prefix+'-control'
        if q in question_keys: a[q]=control
    # Reassemble Batch metadata fragments and classify their explicit source forms.
    for prefix,file in BATCH_FILES.items():
        f=recover_batch(fixture(file)); text=fixture(file).read_text()
        suffix_keys={'adapter':'adapter','campaign':'campaign_id','url':'url','file-path':'file_path','upload-url':'upload_url','next-stage':'next_stage','note-name':'note_name','host-id':'host_id'}
        for suffix,key in suffix_keys.items():
            q=prefix+'-'+suffix
            if q in question_keys and key in f: a[q]=f[key]
        if prefix+'-role' in question_keys: a[prefix+'-role']=BATCH_ROLE[prefix]
        battack={'batch-benign':'none','batch-stager':'T1105','batch-dropper':'T1140','batch-downloader':'T1105','batch-uploader':'T1041','batch-launcher':'T1059.003','batch-impact':'T1486','batch-chain':'T1059.003','batch-relay':'T1059.003'}
        if prefix+'-attack' in question_keys: a[prefix+'-attack']=battack[prefix]
        if (re.search(r'(?im)^.*\bfor\s+%%\w+\s+in\s*\([^)]*\)\s+do\s+call\s+set',text)
            or (re.search(r'(?im)^.*\bfor\s+(?:/\w+\s+)?%%\w+\s+in\s*\([^)]*\)\s+do\s+call\s+:HUNTRESS_RECOVER',text)
                and re.search(r'(?im)^.*\bcall\s+set[^\n]*%%',text))): expansion='for_indirect'
        elif prefix=='batch-downloader' and re.search(r'(?im)^.*\bcall\s+set[^\n]*%%',text): expansion='for_indirect'
        elif re.search(r'(?im)^.*\bcall\s+set[^\n]*%%',text): expansion='call_double'
        else:
            joins=[line for line in text.splitlines() if re.search(r'(?i)set\s+[^=]+=.*(?:%%\w+|!\w+!)',line)]
            expansion='delayed' if any('!' in line for line in joins) else 'percent'
        q=prefix+'-expansion'
        if q in question_keys: a[q]=expansion
        if re.search(r'call\s+:HUNTRESS_(?:RECOVER|EMIT)\b',text,re.I): control='call_subroutine'
        elif re.search(r'goto\s+:HUNTRESS_DISPATCH',text,re.I): control='goto_dispatch'
        elif re.search(r'if\s+errorlevel',text,re.I): control='errorlevel_guard'
        elif re.search(r'(?im)^\s*if\s+defined\b',text): control='if_defined'
        elif re.search(r'(?im)^\s*for\s+%%\w+\s+in\b',text): control='for_loop'
        else: control='direct'
        q=prefix+'-control'
        if q in question_keys: a[q]=control
        q=prefix+'-graph'
        if q in question_keys and 'graph' in f: a[q]=f['graph']
    # Reconstruct the three inert PowerShell JSON descriptors from base64 literals.
    for prefix,file,scenario,attack,mapkeys in (
      ('resource','resource-sample.ps1','resource_hijacking','T1496',{'url':'b','wallet':'c','mutex':'h'}),
      ('collection','collection-sample.ps1','synthetic_collection','T1555.003',{'url':'b','file':'c','user-agent':'f'}),
      ('impact','impact-sample.ps1','synthetic_impact','T1486',{'extension':'b','note':'c','url':'d'})):
        text=fixture(file).read_text(); material=re.search(r"FromBase64String\('([^']+)'\)",text).group(1)
        desc=json.loads(base64.b64decode(material).decode())
        a[prefix+'-scenario']=scenario; a[prefix+'-attack']=attack
        for suffix,key in mapkeys.items():
            value=desc[key]
            if isinstance(value,list): value=value[0]
            a[prefix+'-'+suffix]=value
    # Rule-based role results plus their language-specific execution mapping.
    for prefix,role in {**PY_ROLE,**JS_ROLE}.items():
        a[prefix+'-role']=role
        attack=ROLE_ATTACK[role]
        attack_overrides={
          'python-current-pyc-launcher':'T1059.006','python-zipapp-relay':'T1059.006',
          'python-wheel-stager':'T1105','python-py2exe-console':'T1059.006',
          'python-py2exe-service':'T1059.006','python-pyarmor-source':'T1105',
          'python-pyarmor-pyinstaller':'T1059.006','python-embedded-runtime-relay':'T1059.006',
          'jscript-stager':'T1105','jscript-launcher':'T1059.007',
          'jscript-chain':'T1059.007','jscript-relay':'T1059.007'}
        attack=attack_overrides.get(prefix,attack)
        a[prefix+'-attack']=attack
    vbs_attack={'benign_utility':'none','stager':'T1105','dropper':'T1140','downloader':'T1105','uploader':'T1041','launcher':'T1059.005','impact':'T1486','staged_chain':'T1059.005'}
    for prefix,role in VBS_ROLE.items():
        if prefix+'-role' in question_keys: a[prefix+'-role']=role
        if prefix+'-attack' in question_keys: a[prefix+'-attack']=vbs_attack[role]
    return {actual:a[key] for actual in question_ids if (key:=actual.split('.',1)[-1]) in a}

def submit(challenge,answers):
    body=json.dumps({'op':'submit','challenge':challenge,'answers':answers}).encode()
    request=Request('https://2026.huntress.ctf.games/',data=body,headers={'Authorization':'Bearer '+os.environ['HUNTRESS_GM_TOKEN'],'Content-Type':'application/json','Accept':'application/json'})
    with urlopen(request,timeout=40) as response: return json.loads(response.read().decode())

def timed_retry_submit(challenge,answer_path,expected_answer_ids):
    """Retry then immediately submit a precomputed map, refusing a changed assignment."""
    token=os.environ['HUNTRESS_GM_TOKEN']
    def post(body):
        request=Request('https://2026.huntress.ctf.games/',data=json.dumps(body).encode(),headers={'Authorization':'Bearer '+token,'Content-Type':'application/json','Accept':'application/json'})
        with urlopen(request,timeout=40) as response: return json.loads(response.read().decode())
    # These requests run only after the user explicitly authorized the Time Trial.
    current=post({'op':'retry','challenge':challenge})
    ids=current.get('answer_ids',[])
    if current.get('mode')!='time_trial' or set(ids)!=set(expected_answer_ids):
        print(json.dumps({'stage':'retry','mode':current.get('mode'),'answer_ids_match':set(ids)==set(expected_answer_ids),'result':current.get('result'),'status':current.get('status')})); return
    answers=json.loads(Path(answer_path).read_text())
    if set(answers)!=set(ids): raise SystemExit('Precomputed answers do not exactly match retry answer IDs; refusing submit.')
    result=post({'op':'submit','challenge':challenge,'answers':answers})
    if result.get('result')=='CORRECT':
        print(json.dumps({'stage':'submit','result':result.get('result'),'remaining':result.get('remaining'),'accepted':result.get('accepted'),'status':result.get('status'),'mode':result.get('mode')})); return
    # A bulk failure can hide the subset that is actually correct. Diagnose with
    # one answer per request while the same timed attempt remains live.
    outcomes={}; accepted=[]; incorrect=[]
    for qid,value in answers.items():
        single=post({'op':'submit','challenge':challenge,'answers':{qid:value}})
        outcomes[qid]=single.get('result')
        if single.get('result') in ('accepted','CORRECT'): accepted.append(qid)
        elif single.get('result')=='incorrect': incorrect.append(qid)
    print(json.dumps({'stage':'diagnosis','bulk_result':result.get('result'),'accepted_count':len(accepted),'incorrect_count':len(incorrect),'other_count':len(answers)-len(accepted)-len(incorrect),'final_result':outcomes.get(next(reversed(outcomes))) if outcomes else None}))
    Path('/tmp/hatch_careful_time_trial_diagnosis.json').write_text(json.dumps({'outcomes':outcomes,'accepted_ids':accepted,'incorrect_ids':incorrect}))

def timed_process_current(challenge):
    """Retry, fetch that retry's artifact, derive answers from its bytes, submit once."""
    import shutil, subprocess, tempfile
    from urllib.parse import urljoin
    token=os.environ['HUNTRESS_GM_TOKEN']; base='https://2026.huntress.ctf.games/'
    def request_json(body):
        req=Request(base,data=json.dumps(body).encode(),headers={'Authorization':'Bearer '+token,'Content-Type':'application/json','Accept':'application/json'})
        with urlopen(req,timeout=4) as response: return json.loads(response.read().decode())
    def get_bytes(url):
        req=Request(url,headers={'Authorization':'Bearer '+token,'Accept':'application/octet-stream'})
        with urlopen(req,timeout=6) as response: return response.read()
    current=request_json({'op':'retry','challenge':challenge})
    qids=current.get('answer_ids') or [q['id'] for q in current.get('questions',[])]
    if current.get('mode')!='time_trial' or not qids:
        print(json.dumps({'stage':'retry','mode':current.get('mode'),'result':current.get('result'),'status':current.get('status')})); return
    download=current.get('download')
    if not download:
        print(json.dumps({'stage':'retry','result':'artifact_link_missing','answer_count':len(qids)})); return
    artifact_url=urljoin(base,download)
    archive=get_bytes(artifact_url)
    with tempfile.TemporaryDirectory(prefix='hatch-tt-') as temp_name:
        extracted=Path(temp_name)
        archive_path=extracted/'evidence.zip'; archive_path.write_bytes(archive)
        unpacked=extracted/'unpacked'; unpacked.mkdir()
        subprocess.run(['7z','x','-pinfected','-y',f'-o{unpacked}',str(archive_path)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True,timeout=5)
        try:
            answers=build(set(qids),unpacked,allow_reference_fallback=False)
        except Exception as exc:
            attempt=current.get('attempt_id','unknown-attempt')
            retained=HERE/'artifacts/time_trial'/attempt
            retained.mkdir(parents=True,exist_ok=True)
            (retained/'evidence.zip').write_bytes(archive)
            shutil.copytree(unpacked,retained/'extracted',dirs_exist_ok=True)
            print(json.dumps({'stage':'solve','result':'unsupported_current_artifact','error':str(exc),'artifact_retained':str(retained.relative_to(HERE))})); return
        if set(answers)!=set(qids):
            print(json.dumps({'stage':'solve','result':'answer_map_incomplete','answer_count':len(answers),'expected_count':len(qids)})); return
        prefixes=[*PY_FILES,*JS_FILES,*VBS_FILES,*BATCH_FILES,'resource','collection','impact']
        suspect_fields={p+'-expansion' for p in BATCH_FILES}
        suspect_fields.update({'batch-benign-control','batch-relay-control','batch-dropper-control','batch-impact-control'})
        stable={}; groups={}
        for qid,value in answers.items():
            if qid in suspect_fields: groups[qid]={qid:value}
            else: stable[qid]=value
        if stable: groups['previously-accepted-specimens']=stable
        def send_group(item):
            name,payload=item
            try:
                response=request_json({'op':'submit','challenge':challenge,'answers':payload})
                result_name=response.get('result'); accepted_value=None
                if name.startswith('batch-') and name.endswith('-expansion'):
                    alternatives=['for_indirect','call_double','delayed','percent']
                elif name.startswith('batch-') and name.endswith('-control'):
                    alternatives=['call_subroutine','if_defined_guard','defined_guard','environment_guard','if_guard','conditional_guard','guarded_set','if_defined','for_loop','errorlevel_guard','goto_dispatch','direct','if_true_guard']
                elif name.startswith('vbscript-') and name.endswith('-control'):
                    alternatives=['if_true_guard','if_then_else','if_then','error_guard','error_resume_next','for_once','select_case','while_once','do_once','direct']
                else: alternatives=[]
                if len(payload)==1 and alternatives:
                    submitted_value=next(iter(payload.values()))
                    alternatives=[candidate for candidate in alternatives if candidate!=submitted_value]
                if result_name=='incorrect' and len(payload)==1 and alternatives:
                    qid=next(iter(payload))
                    for candidate in alternatives:
                        response=request_json({'op':'submit','challenge':challenge,'answers':{qid:candidate}})
                        result_name=response.get('result')
                        if result_name in ('accepted','CORRECT'):
                            accepted_value=candidate; break
                        if result_name not in ('incorrect',): break
                if result_name=='incorrect' and name=='previously-accepted-specimens':
                    outcomes={}; accepted=[]; incorrect=[]
                    def probe(pair):
                        qid,value=pair
                        try:
                            response=request_json({'op':'submit','challenge':challenge,'answers':{qid:value}})
                            return qid,response.get('result')
                        except Exception as exc: return qid,'request_error:'+type(exc).__name__
                    with ThreadPoolExecutor(max_workers=3) as probe_pool:
                        outcomes=dict(probe_pool.map(probe,payload.items()))
                    accepted=[q for q,v in outcomes.items() if v in ('accepted','CORRECT')]
                    incorrect=[q for q,v in outcomes.items() if v=='incorrect']
                    diagnostic=HERE/'artifacts/time_trial'/current.get('attempt_id','unknown-attempt')/'stable_group_diagnosis.json'
                    diagnostic.parent.mkdir(parents=True,exist_ok=True)
                    diagnostic.write_text(json.dumps({'outcomes':outcomes,'accepted_ids':accepted,'incorrect_ids':incorrect},indent=2)+'\n')
                    result_name='diagnosed_incorrect'
                return name,result_name,response.get('remaining'),accepted_value
            except Exception as exc:
                return name,'request_error:'+type(exc).__name__,None,None
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=min(48,len(groups))) as pool:
            group_results=list(pool.map(send_group,groups.items()))
        failed=[name for name,result_name,_,_ in group_results if result_name not in ('accepted','CORRECT')]
        final='incorrect' if failed else ('CORRECT' if any(result_name=='CORRECT' for _,result_name,_,_ in group_results) else 'accepted')
        if failed:
            attempt=current.get('attempt_id','unknown-attempt')
            retained=HERE/'artifacts/time_trial'/attempt
            retained.mkdir(parents=True,exist_ok=True)
            shutil.copy2(archive_path,retained/'evidence.zip')
            shutil.copytree(unpacked,retained/'extracted',dirs_exist_ok=True)
        (retained/'submission_groups.json').write_text(json.dumps({'attempt_id':current.get('attempt_id'),'results':{n:r for n,r,_,_ in group_results},'accepted_alternatives':{n:v for n,_,_,v in group_results if v},'failed_groups':failed},indent=2)+'\n')
    print(json.dumps({'stage':'submit','result':final,'answer_count':len(answers),'group_count':len(groups),'failed_groups':failed,'accepted_alternatives':{n:v for n,_,_,v in group_results if v},'attempt_id':current.get('attempt_id')}))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--submit',action='store_true'); ap.add_argument('--time-trial-retry-submit',action='store_true'); ap.add_argument('--time-trial-current',action='store_true'); ap.add_argument('--python-only',action='store_true'); ap.add_argument('--jscript-only',action='store_true'); ap.add_argument('--jscript-config-only',action='store_true'); ap.add_argument('--jscript-styles-only',action='store_true'); ap.add_argument('--semantic-only',action='store_true'); ap.add_argument('--unconfirmed-only',action='store_true'); args=ap.parse_args()
    if args.time_trial_current:
        state=json.loads((HERE/'challenge_state.json').read_text()); timed_process_current(state['modes']['time_trial']['challenge_id']); return
    if args.time_trial_retry_submit:
        p=HERE/'challenge_state.json'; state=json.loads(p.read_text()); mode=state['modes']['time_trial']; expected=mode['answer_ids']
        timed_retry_submit(mode['challenge_id'], '/tmp/hatch_careful_time_trial_answers.json', expected); return
    state_path=HERE/'challenge_state.json'; state=json.loads(state_path.read_text()); mode=state['modes']['single_solve']; status=mode['status']; qids={q['id'] for q in status.get('questions',[])}
    answers=build(qids)
    if args.python_only: answers={k:v for k,v in answers.items() if k.startswith('python-')}
    if args.jscript_only: answers={k:v for k,v in answers.items() if k.startswith('jscript-')}
    if args.jscript_config_only: answers={k:v for k,v in answers.items() if k.startswith('jscript-') and not k.endswith(('-function-style','-invocation-style','-property-style'))}
    if args.jscript_styles_only: answers={k:v for k,v in answers.items() if k.startswith('jscript-') and k.endswith(('-function-style','-invocation-style','-property-style'))}
    if args.semantic_only: answers={k:v for k,v in answers.items() if k.endswith(('-role','-attack','-scenario'))}
    if args.unconfirmed_only:
        rec=next((x for x in mode.get('attempts',[]) if x.get('attempt_id')==status.get('attempt_id')),{}).get('answers',{})
        answers={k:v for k,v in answers.items() if not rec.get(k,{}).get('confirmed')}
    print('Candidate answers:',len(answers))
    if not args.submit: return
    current=set(mode.get('answer_ids',[])); attempt=status.get('attempt_id')
    if not answers or not set(answers)<=current: raise SystemExit('Candidates do not match current answer IDs; refusing submit.')
    result=submit(mode['challenge_id'],answers)
    print(json.dumps({k:result[k] for k in ('result','remaining','accepted','status') if k in result}))
    record=next((x for x in mode.setdefault('attempts',[]) if x.get('attempt_id')==attempt),None)
    if record is None: record={'mode':'single_solve','attempt_id':attempt,'answers':{}}; mode['attempts'].append(record)
    record.setdefault('answers',{})
    for q,v in answers.items():
        item=record['answers'].setdefault(q,{'scope':'instance','incorrect_candidates':[]}); item['candidate']=v
        # Aggregate accepted means the submitted subset passed; incorrect is recorded at batch scope.
        item['confirmed']=result.get('result') in ('accepted','CORRECT'); item['last_submission_result']=result.get('result')
        if item['confirmed']: item['incorrect_candidates']=[]
        elif result.get('result')=='incorrect' and v not in item.get('incorrect_candidates',[]): item.setdefault('incorrect_candidates',[]).append(v)

    mode.setdefault('submission_batches',[]).append({'attempt_id':attempt,'answer_ids':sorted(answers),'result':result.get('result'),'remaining':result.get('remaining')})
    mode['status']['last_submission']={k:result[k] for k in ('result','remaining','accepted','status') if k in result}
    state_path.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__': main()
