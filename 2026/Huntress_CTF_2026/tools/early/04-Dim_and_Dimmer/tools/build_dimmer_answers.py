import contextlib,io,json,pathlib,re,os
src=open(pathlib.Path(__file__).resolve().with_name('decode_dimmer.py')).read()
ns={}
with contextlib.redirect_stdout(io.StringIO()): exec(src[:src.index('for p in sorted(root.iterdir()):')],ns)
root=pathlib.Path(os.environ.get('DIMMER_ARTIFACT_DIR','/tmp/huntress-d4-dim-tt'))
configs={}
code={}
for p in root.iterdir():
 if p.suffix not in ('.js','.vbs','.cmd','.bat'): continue
 s=p.read_text(errors='replace'); code[p.name]=s
 raw=(ns['decode_cmd'](p,s) if p.suffix in ('.cmd','.bat') else ns['decode_vbs'](p,s) if p.suffix=='.vbs' else ns['decode_js'](p,s))
 if raw.lstrip().startswith('{'):
  obj=json.loads(raw); c={**obj.get('values',{}),'adapter':obj.get('adapter'),'campaign_id':obj.get('values',{}).get('campaign_id'),'stage_count':obj.get('stageCount')}
  c['steps']=','.join(obj.get('steps',[]))
 else:
  c={}
  for item in raw.split('|'):
   if '=' in item:
    k,v=item.split('=',1); c[k.strip()]=v.strip()
 configs[p.name]=c

role_stem={'benign':'host-context','stager':'memory-stage','dropper':'embedded-write','downloader':'remote-write','launcher':'local-dispatch','chain':'staged-handoff','uploader':'outbound-transfer','impact':'impact-plan','relay':'relay-handoff'}
roles={'benign':'benign_utility','stager':'stager','dropper':'dropper','downloader':'downloader','launcher':'launcher','chain':'staged_chain','uploader':'uploader','impact':'impact','relay':'staged_chain'}
attacks={'benign':'none','stager':'T1105','dropper':'T1140','downloader':'T1105','launcher':'T1059.007','chain':'T1059.007','uploader':'T1041','impact':'T1486','relay':'T1059.007'}
answers={}
# PowerShell composite samples
import base64
for stem in ('resource-sample','collection-sample','impact-sample'):
 s=(root/(stem+'.ps1')).read_text(); enc=re.search(r"FromBase64String\('([^']+)'\)",s).group(1); d=json.loads(base64.b64decode(enc))
 if stem=='resource-sample': answers.update({'resource-scenario':'resource_hijacking','resource-attack':'T1496','resource-url':d['b'],'resource-wallet':d['c'],'resource-mutex':d['h']})
 elif stem=='collection-sample': answers.update({'collection-scenario':'synthetic_collection','collection-attack':'T1555.003','collection-url':d['b'],'collection-file':d['c'][0],'collection-user-agent':d['f']})
 else: answers.update({'impact-scenario':'synthetic_impact','impact-attack':'T1486','impact-extension':d['b'],'impact-note':d['c'],'impact-url':d['d']})

for lang in ('jscript','batch','vbscript'):
 ext={'jscript':'.js','batch':None,'vbscript':'.vbs'}[lang]
 for role,stem in role_stem.items():
  if lang=='batch':
   fname=stem+('.bat' if stem in ('local-dispatch','memory-stage','remote-write','staged-handoff') else '.cmd')
  else: fname=stem+ext
  s=code[fname]; c=configs[fname]
  prefix=f'{lang}-{role}'
  answers[prefix+'-role']=roles[role]
  answers[prefix+'-attack']=('T1059.003' if lang=='batch' and role in ('launcher','chain','relay') else 'T1059.005' if lang=='vbscript' and role in ('launcher','chain','relay') else attacks[role])
  answers[prefix+'-adapter']=c.get('adapter','')
  if 'campaign_id' in c: answers[prefix+'-campaign']=c['campaign_id']
  if role=='uploader' and lang=='jscript' and 'upload_url' in c: answers[prefix+'-url']=c['upload_url']
  # primary artifact-specific outputs by prompt ID suffix
  for suffix,key in [('host','host_id'),('host-id','host_id'),('url','url'),('upload-url','upload_url'),('path','file_path'),('file-path','file_path'),('next-stage','next_stage'),('next-language','next_language'),('extension','extension'),('note','note_name'),('note-name','note_name'),('stage','stage_count')]:
   aid=prefix+'-'+suffix
   if key in c: answers[aid]=str(c[key])
  if lang=='jscript':
   # inspect function representation
   m=re.search(r'(?:function\s+(inspect_\w+)\s*\([^)]*\)|(?:var|let|const)\s+(inspect_\w+)\s*=\s*function\s*(\w*)\s*\([^)]*\))',s)
   if m:
    if m.group(1): fs='declaration'
    else: fs='named_expression' if m.group(3) else 'anonymous_expression'
   else: fs='declaration'
   answers[prefix+'-function-style']=fs
   # descriptor recovery invocation syntax in inspect body
   im=re.search(r'(?:function\s+inspect_\w+\s*\([^)]*\)|(?:var|let|const)\s+inspect_\w+\s*=\s*function[^\{]*\{)(.*?)(?:\n\};|\n\})',s,re.S)
   ib=im.group(1) if im else s
   call=re.search(r'recover_\w+\s*\.\s*(apply|call)\s*\(',ib)
   answers[prefix+'-invocation-style']=call.group(1) if call else 'direct'
   dot=bool(re.search(r'\b\w+\.(?:steps|adapter|values|stageCount)\b',ib))
   br=bool(re.search(r'\b\w+\[\s*"(?:steps|adapter|values|stageCount)"\s*\]',ib))
   answers[prefix+'-property-style']='mixed' if dot and br else 'bracket_literal' if br else 'dot'
  elif lang=='batch':
   # expansion syntax used in the actual config reconstruction
   if re.search(r'(?im)^.*\bfor\s+%%\w+\s+in\s*\([^)]*\)\s+do\s+call\s+set[^\n]*%%%%h%%\w+%%',s): expansion='call_double'
   elif re.search(r'(?im)^.*\bfor\s+%%\w+\s+in\s*\([^)]*\)\s+do\s+call\s+set',s): expansion='for_indirect'
   elif re.search(r'(?im)^\s*if\s+defined\b[^\n]*\bcall\s+set',s): expansion='delayed'
   elif re.search(r'(?im)^.*\bcall\s+set[^\n]*%%%%h\d+%%',s): expansion='call_double'
   elif re.search(r'(?im)^.*\bcall\s+set[^\n]*%%',s): expansion='delayed'
   else:
    joins=[line for line in s.splitlines() if re.search(r'(?i)set\s+[^=]+=.*(?:%%\w+|!\w+!)',line)]
    expansion='delayed' if any('!' in line for line in joins) or re.search(r'(?im)^\s*echo\(!\w+!',s) else 'percent'
   answers[prefix+'-expansion']=expansion
   answers[prefix+'-graph']=c.get('graph','')
   if re.search(r'(?im)^.*\bcall\s+:HUNTRESS_(?:RECOVER|EMIT)\b',s): control='call_subroutine'
   elif re.search(r'(?im)^\s*goto\s+:HUNTRESS_DISPATCH\b',s): control='goto_dispatch'
   elif re.search(r'(?im)^\s*if\s+errorlevel\b',s): control='errorlevel_guard'
   elif re.search(r'(?im)^\s*if\s+defined\b',s): control='if_guard'
   else: control='direct'
   answers[prefix+'-control']=control
  else:
   co=re.search(r'Const Codec_\w+ = "([^"]+)"',s).group(1).split('|')
   answers[prefix+'-representation']=co[0]
   answers[prefix+'-transform']=co[1]
   rec=re.search(r'Function Recover_.*?\n(.*?)\nEnd Function',s,re.S|re.I).group(1)
   rec=re.sub(r'(?im)^\s*If\s*\(\s*2\s*>\s*1\s*\)\s*Then[^\n]*\bElse\b[^\n]*$', '', rec)
   if re.search(r'\bSelect Case\b',rec,re.I): control='select_case'
   elif re.search(r'\bDo\b',rec,re.I): control='do_once'
   elif re.search(r'\bWhile\b',rec,re.I): control='while_once'
   elif re.search(r'(?im)^\s*For\s+\w+\s*=\s*0\s+To\s+0\b',rec): control='for_once'
   elif re.search(r'(?im)^\s*If\b[^\n]*\bThen\b[^\n]*\bElse\b',rec) and not re.search(r'(?im)^\s*If\b[^\n]*\bThen\s+harmlessValue\s*=',rec): control='if_then_else'
   elif re.search(r'(?im)^\s*If\b[^\n]*Then\s+Err\.Raise',rec): control='error_guard'
   elif re.search(r'(?im)^\s*On Error Resume Next\b',rec): control='error_resume_next'
   elif re.search(r'(?im)^\s*If\s+True\s+Then\b',rec): control='direct'
   elif re.search(r'(?im)^\s*If\b(?![^\n]*\bThen\s+harmlessValue\s*=)',rec): control='if_then'
   else: control='direct'
   answers[prefix+'-control']=control

challenge_dir=pathlib.Path(__file__).resolve().parents[1]
p=json.load(open(challenge_dir/'challenge_state.json'))
ids=p['modes']['time_trial'].get('answer_ids') or p['modes']['time_trial']['status'].get('answer_ids',[])
missing=[x for x in ids if x not in answers]
extra=[x for x in answers if x not in ids]
answers={k:v for k,v in answers.items() if k in ids}
if missing: raise SystemExit('Missing answer IDs: '+','.join(missing))
out=os.environ.get('DIMMER_CANDIDATES_PATH','/tmp/dimmer-tt-candidates.json')
json.dump(answers,open(out,'w'),indent=2)
print('CANDIDATES',len(answers),'REQUIRED',len(ids),'MISSING',len(missing))
