import pathlib,json,hashlib,importlib.util,copy,datetime,os,sys,shutil,subprocess
R=pathlib.Path(__file__).resolve().parent
sys.dont_write_bytecode=True
s=importlib.util.spec_from_file_location('research_store',R/'package/scripts/research_store.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
cut='2024-08-02T23:59:59+00:00'
def dump(p,o):
 p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
def hashes(root):
 return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob('*')) if p.is_file()}
def leaves(root):
 reviews=[(p,json.loads(p.read_text())) for p in (root/'investing/assets/equities/aapl/cycles/2024Q3').glob('*/review.json')]
 eligible=[(p,x) for p,x in reviews if x['cutoff']<=cut]
 parents={x.get('predecessor') for p,x in eligible}
 result=[(p,x) for p,x in eligible if x['id'] not in parents]
 assert len(result)==1
 return result[0]
if len(sys.argv)>1:
 case=sys.argv[1];root=R/'cases'/case
 expected=m.publication_snapshot(root);dump(R/f'run-05-{case}-baseline.json',expected)
 discovery=m.discover(root,'latest',cut);dump(R/f'run-05-{case}-discovery-before.json',discovery)
 p,old=leaves(root)
 assert all({'record':'aapl/2024Q3/'+old['id'],'work':q} in discovery['reusable'] for q in ['growth','identity'])
 q=json.loads((root/'investing/assets/equities/aapl/data/sources/2024Q3.json').read_text());raw=json.loads((root/q['raw_ref']).read_text());assert raw==q['projection'];assert hashlib.sha256((root/q['raw_ref']).read_bytes()).hexdigest()==q['raw_digest']
 method=json.loads((root/'investing/assets/equities/aapl/data/analysis/growth-method.json').read_text());assert hashlib.sha256((root/method['content_ref']).read_bytes()).hexdigest()==method['content_digest']
 for u in old['units'].values():
  assert hashlib.sha256((root/u['output']['path']).read_bytes()).hexdigest()==u['output']['digest']
 rid='run-05-'+case+'-q3';run='run-05-'+case+'-interrupt';target='investing/assets/equities/aapl/cycles/2024Q3/2024-08-02-'+rid
 note=f'''# AAPL Q3 unfinished investment-case progress

Status: bounded unfinished progress; investment-case is NOT a completed unit. Assessment cutoff {cut}; fiscal Q3 ending 2024-06-29, original accession {q['identity']}, retained official publication {q['available_at']}. This is a 2026 reconstruction with no new external request, not a contemporaneous forecast.

Question tested: does the observed revenue recovery support a broad-based, durable demand thesis? Retained selected original MD&A net-sales table rows (iPhone, Mac, iPad, Wearables/Home/Accessories, Services, Greater China) support a narrower conclusion. In USD millions, Services 24,213 versus 21,213 contributes +3,000 and iPad 7,162 versus 5,791 contributes +1,371. Against that, iPhone 39,296 versus 39,669 contributes -373 and Wearables 8,097 versus 8,284 contributes -187. Mac 7,009 versus 6,840 contributes +169. The bridge is 3,000+1,371-373-187+169=3,980, matching consolidated revenue 85,777-81,797. Services accounts for 75.38% of the net increment (3,000/3,980), a contribution ratio rather than a segment growth rate or forecast. Greater China 14,728 versus 15,758 falls 1,030; geography overlaps the product totals and is not added to this bridge.

Working implication: consolidated recovery is compatible with concentrated offsets, rather than evidence that every major device category or geography has recovered. Strong Services and iPad are positive operating evidence; iPhone, Wearables and China are counterevidence. Launch timing, comparison base, currency, pricing and mix remain alternative explanations, not established causal estimates. Revenue does not establish unit demand, share gains, recurring-customer retention or durable competitive advantage. Higher consolidated margin in the preserved growth unit cannot isolate any of those drivers. No forecast or security-return conclusion follows from the bridge.

Next bounded research need: obtain cutoff-eligible original narrative on the product/geographic drivers and reconcile it with volumes/pricing/mix where available; inspect accounting/segment notes, liquidity and commitments, risks, governance/capital allocation and competition before synthesis. Obtain a dated eligible price and suitable valuation/scenario inputs before investment judgment. No probabilities, target price or investment rating are assigned. Full investment-case remains pending, with no verification record declaring it complete.

Coverage actually read: retained transformed quarter pack metadata, metrics and six selected MD&A table rows, plus predecessor growth reasoning. Original reference: {raw['source_url']}. Local evidence: {q['raw_ref']}, SHA256 {q['raw_digest']}. This is retained extraction, not retained HTML or a new original-page reading. Complete original narrative, notes, risk factors and proxy/governance have not been read here; raw inline context, amendment inventory and independent official-date validation remain unverified. Later-authored forecast/valuation supplements are not used as historical economic evidence.

Growth and identity units, including exact output/check references, frozen economic dependencies and growth's local v3 dependency, remain unchanged from {old['id']}. Local v3 revision {method['authored_at']} is separate from economic publication; its content digest is {method['content_digest']}. Earlier erroneous author-time records remain historical and are not recertified. Generic method: source-invoked finance-research references/research-method.md, with unchanged applied v3 manifest.

Short (0,3], medium (3,12], long (12,60] months anchored at {cut}: investment-return judgment remains insufficient_evidence for every window. Short-term operating recovery is uneven; medium-term persistence and long-term durability lack evidence and valuation linkage. These pilot windows are not the user's holding preference and differ from later one-quarter/1–3-year/5+-year conventions. Corrections to source identity, weakening Services, continued product/geographic weakness, or eligible evidence quantifying temporary effects would change this working thesis. Dated price/valuation and horizon-specific drivers are required before investment advice.
'''
 a=raw['metrics'];assert sum(a[k]-a[k+'_prior_year'] for k in ['services','ipad','iphone','wearables_home_and_accessories','mac'])==3980000000
 review=copy.deepcopy(old)
 for k in ['publication','provenance','requirements']:review.pop(k,None)
 review.update(id=rid,predecessor=old['id'])
 review['research']['changes']='Bounded unfinished MD&A concentration/counterevidence progress added; completed growth and identity reused verbatim. Full investment-case remains pending.'
 review['research']['progress_note']=target+'/investment-case-progress.md'
 files={'investment-case-progress.md':note,'progress-coverage.json':json.dumps({'status':'unfinished','completed_question':False,'source':q,'reading':'retained selected MD&A table rows only; no new original HTML reading','arithmetic':'3980 million bridge and 75.38% Services net contribution checked','predecessor':old['id'],'units_preserved':old['units'],'horizons':'all investment returns insufficient_evidence'})}
 dump(R/f'run-05-{case}-proposal.json',{'review':review,'files':files,'run':run,'target':target,'complete':False})
 original=m._write_new
 def fault(root_arg,reference,data):
  if reference==target+'/review.json':
   assert (root/'investing/.research-runs'/run/'journal.json').is_file()
   assert (root/'investing/.research-runs'/run/'draft/investment-case-progress.md').is_file()
   assert (root/target/'pending.json').is_file()
   assert (root/target/'investment-case-progress.md').is_file()
   print(json.dumps({'event':'controlled_save_process_interruption','target':reference,'run':run,'exit':75,'durable_journal_drafts_outputs':True}),flush=True)
   os._exit(75)
  return original(root_arg,reference,data)
 m._write_new=fault
 m.publish(root,'aapl',review,files,expected,run,complete=False)
 raise AssertionError('fault boundary not reached')
main_before=hashes(R/'investing');package_before=hashes(R/'package')
dump(R/'run-05-main-before.json',main_before);dump(R/'run-05-package-before.json',package_before)
dump(R/'run-05-main-discovery.json',m.discover(R,'latest',cut))
results=[]
for case in ['clean','useredit']:
 root=R/'cases'/case;root.mkdir(parents=True,exist_ok=False);shutil.copytree(R/'investing',root/'investing')
 before=hashes(root/'investing');assert before==main_before
 command=[sys.executable,str(R/'run-05-interrupt.py'),case]
 proc=subprocess.run(command,cwd=R,capture_output=True,text=True)
 (R/f'run-05-{case}-stdout.txt').write_text(proc.stdout);(R/f'run-05-{case}-stderr.txt').write_text(proc.stderr)
 dump(R/f'run-05-{case}-execution.json',{'argv':command,'cwd':str(R),'exit_code':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr})
 assert proc.returncode==75,(proc.returncode,proc.stdout,proc.stderr)
 after=hashes(root/'investing');assert all(after[k]==v for k,v in before.items())
 dump(R/f'run-05-{case}-hashes.json',{'before':before,'after':after,'all_original_bytes_preserved':True})
 discovery=m.discover(root,'latest',cut);dump(R/f'run-05-{case}-discovery-after.json',discovery)
 prop=json.loads((R/f'run-05-{case}-proposal.json').read_text());target=prop['target'];assert not (root/target/'review.json').exists()
 p,old=leaves(root);assert old['id']==prop['review']['predecessor'];assert old['units']==prop['review']['units']
 results.append({'case':case,'root':str(root),'run_id':prop['run'],'review_id':prop['review']['id'],'predecessor':old['id'],'original_view':str(p),'target':str(root/target),'progress_note':str(root/target/'investment-case-progress.md'),'journal':str(root/'investing/.research-runs'/prop['run']/'journal.json'),'drafts':str(root/'investing/.research-runs'/prop['run']/'draft'),'execution':str(R/f'run-05-{case}-execution.json'),'hashes':str(R/f'run-05-{case}-hashes.json'),'exit_code':proc.returncode,'status':'unfinished; final review.json absent; not resumed or rolled back','user_edits_this_invocation':False,'complete':False})
assert hashes(R/'investing')==main_before;assert hashes(R/'package')==package_before
dump(R/'run-05-main-after.json',hashes(R/'investing'))
dump(R/'run-05-cases.json',{'version':1,'interruption':'controlled save-process interruption in real host subprocess, not unexpected host crash','cutoff':cut,'main_investing_unchanged':True,'package_unchanged':True,'cases':results,'recovery_performed':False,'external_attempts':0,'external_freshness':'unverified'})
print(json.dumps(results,indent=2))
