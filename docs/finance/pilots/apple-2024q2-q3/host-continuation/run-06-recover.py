import sys,json,pathlib,hashlib,importlib.util,traceback
sys.dont_write_bytecode=True
R=pathlib.Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('research_store',R/'package/scripts/research_store.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(name,obj): (R/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def hashes(root):
 out={}
 for p in sorted(root.rglob('*')):
  assert not p.is_symlink(),str(p)
  if p.is_file():out[str(p.relative_to(root))]=sha(p.read_bytes())
 return out
cases=json.loads((R/'run-05-cases.json').read_text());edit=json.loads((R/'run-06-user-edit.json').read_text());cut=cases['cutoff']
protected={k:hashes(R/k) for k in ['investing','package','retained']};before={};checks={};calls=[]
for c in cases['cases']:
 key=c['case'];root=pathlib.Path(c['root']);run=root/'investing/.research-runs'/c['run_id'];raw=(run/'request.json').read_bytes();req=json.loads(raw);journal=json.loads((run/'journal.json').read_text());target=pathlib.Path(c['target']);rel=str(target.relative_to(root))
 before[key]=hashes(root);dump(f'run-06-{key}-discovery-before.json',m.discover(root,'latest',cut))
 assert sha(raw)==journal['request_digest']
 # Compare original immutable map without substituting a new baseline.
 current=m.publication_snapshot(root,_exclude=rel)
 assert current==req['expected']
 assert req['expected']==json.loads((R/f'run-05-{key}-baseline.json').read_text())
 for p,obj in req['review']['provenance'].items():
  assert json.loads((root/p).read_text())==obj
  for ref,digest in [('raw_ref','raw_digest'),('content_ref','content_digest')]:
   if ref in obj:assert sha((root/obj[ref]).read_bytes())==obj[digest]
 for name,text in req['files'].items(): assert (run/'draft'/name).read_bytes()==text.encode()
 for unit in req['review']['units'].values():assert sha((root/unit['output']['path']).read_bytes())==unit['output']['digest']
 assert req['review']['units']==req['previous']['units']
 checks[key]={'journal_request_digest':sha(raw),'original_preconditions_match':True,'provenance_and_raw_method_digests_match':True,'original_drafts_match_request':True,'reused_outputs_and_units_match':True,'scope':json.loads((root/'investing/research.json').read_text()),'questions':json.loads((root/'investing/assets/equities/aapl/asset.json').read_text()),'research':req['review']['research'],'last_attempt':req['review'].get('last_attempt'),'last_success':req['review'].get('last_success')}
 if key=='useredit':
  actual=pathlib.Path(edit['path']).read_bytes();draft=pathlib.Path(edit['original_draft']).read_bytes()
  assert sha(actual)==edit['after_sha256'] and sha(draft)==edit['original_draft_sha256']==edit['before_sha256']
  assert actual==draft+edit['appended_text'].encode()
  checks[key]['user_edit']={'path':edit['path'],'sha256':sha(actual),'original_draft_sha256':sha(draft),'exact_appended_bytes_match':True}
dump('run-06-revalidation.json',checks);dump('run-06-files-before.json',{'cases':before,'protected':protected})
for c in cases['cases']:
 key=c['case'];root=pathlib.Path(c['root'])
 for action in ['resume','rollback']:
  call={'call':f'research_store.recover({str(root)!r}, {c["run_id"]!r}, action={action!r})','case':key,'action':action}
  try:call['result']=m.recover(root,c['run_id'],action=action)
  except (ValueError,OSError) as e:call.update(error_type=type(e).__name__,error=str(e),traceback=traceback.format_exc())
  calls.append(call);dump('run-06-helper-calls.json',calls)
  dump(f'run-06-{key}-discovery-after-{action}.json',m.discover(root,'latest',cut))
  if key=='clean':assert call.get('result',{}).get('status')==('checkpoint' if action=='resume' else 'rolled_back')
  else:assert call.get('error_type')=='ValueError' and 'user edited' in call['error']
after={c['case']:hashes(pathlib.Path(c['root'])) for c in cases['cases']}
validation={'original_files_preserved':{k:all(after[k].get(p)==h for p,h in files.items()) for k,files in before.items()},'protected_unchanged':{k:hashes(R/k)==h for k,h in protected.items()},'useredit_all_files_unchanged':after['useredit']==before['useredit'],'external_attempts_this_run':0,'external_successes_this_run':0,'external_freshness':'unverified'}
assert all(validation['original_files_preserved'].values()) and all(validation['protected_unchanged'].values()) and validation['useredit_all_files_unchanged']
dump('run-06-preserved-file-hashes.json',{'before':before,'after':after});dump('run-06-validation.json',validation)
print(json.dumps({'calls':calls,'validation':validation},indent=2))
