import pathlib,json,hashlib,importlib.util,copy,datetime
from decimal import Decimal as D
r=pathlib.Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('research_store',r/'package/scripts/research_store.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
load=lambda p:json.loads((r/p).read_text())
hashp=lambda p:hashlib.sha256((r/p).read_bytes()).hexdigest()
def put(p,o):
 assert not (r/p).exists(),p
 (r/p).write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
base='investing/assets/equities/aapl';cut='2024-08-02T23:59:59+00:00'
expected=load('run-03-baseline.json');assert m.publication_snapshot(r)==expected
before=load('run-03-files-before.json');method=load(base+'/data/analysis/growth-method.json');assert hashp(method['content_ref'])==method['content_digest'];assert method['identity']=='v3-authorship-corrected'
old=load(base+'/cycles/2024Q3/2024-08-02-run-02-q3/review.json')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
assert datetime.datetime.fromisoformat(method['authored_at'])<=datetime.datetime.fromisoformat(now)
initial=load('run-03-discovery-before.json');assert {'record':'aapl/2024Q3/run-02-q3','work':'identity'} in initial['reusable'];assert any('2024Q2/new' in x['record'] for x in initial['decisions']);assert not any(x['work']=='growth' for x in initial['reusable'])
put('run-03-runtime-check.json',{'runtime':load('runtime-source-v2.json'),'actual_helper_sha256':hashp('package/scripts/research_store.py'),'initial_discovery':'run-03-discovery-before.json','preserved_defective_discovery':{p:hashp(p) for p in ['run-01-discovery-before.json','run-01-discovery-after.json','run-02-discovery-before.json','run-02-discovery-after.json']},'current_utc_checked':now,'method_current_not_future':True,'earlier_exact_times':'preparer declarations, unverified; v2 was future; retained errors not rewritten','method_readme_resolution':'package README.md plus finance-research references/research-method.md; no separate method/README exists in designated root'})
# Web tool actually opened this exact original and inspected these sections. No HTML bytes were downloaded or hash claimed.
access={'version':1,'checked_at':now,'url':'https://www.sec.gov/Archives/edgar/data/320193/000032019324000069/aapl-20240330.htm','channel':'web.run open/find','external_attempted':True,'page_access_success':True,'scope':'bounded Q2 original page corroboration only','read_coverage':['cover lines 11-19, 90-94 and extracted declaration text line 0; fiscal Q2 footer line 161','statements of operations lines 120-158: units and three/six month headers, net sales, gross margin','MD&A fiscal-period lines 675-677; category rows and drivers lines 723-755; Greater China lines 688-711; gross margin lines 761-788'],'not_checked':['raw inline-XBRL contextRef semantics','filing index/official date independently','amendment inventory','complete notes, risk factors, governance/proxy','full SEC acquisition or current coverage'],'SEC_USER_AGENT_configured':False,'acquisition_attempts':0,'new_page_successes':1,'raw_html_retained':False,'raw_html_digest_this_run':None,'economic_cutoff':cut,'eligible_date_basis':'retained official date 2024-05-03; not retrieval time or May 2 signature','prior_source_manifests':'retained/data/source-manifests.json','freshness':'bounded page checked; inventory and full coverage unverified'}
put('run-03-source-access.json',access)
results=[];calcs={}
for quarter in ['2024Q3','2024Q2']:
 q=load(base+'/data/sources/'+quarter+'.json');raw=load(q['raw_ref']);assert raw==q['projection'];assert hashp(q['raw_ref'])==q['raw_digest'];assert q['available_at']<=cut[:10]
 assert raw['original_accession']==q['identity']==q['fiscal']['original_accession'];assert raw['end']==q['fiscal']['period_end'];assert raw['quarter']==quarter
 a=raw['metrics'];rev,pr,gp,pgp=[D(a[k]) for k in ['revenue','revenue_prior_year','gross_profit','gross_profit_prior_year']]
 growth=(rev/pr-1)*100;gm=gp/rev*100;pgm=pgp/pr*100;pp=gm-pgm
 cats=['iphone','mac','ipad','wearables_home_and_accessories','services'];deltas={k:a[k]-a[k+'_prior_year'] for k in cats};assert sum(a[k] for k in cats)==rev;assert sum(a[k+'_prior_year'] for k in cats)==pr;assert sum(deltas.values())==rev-pr
 # Alternative exact decimal route; percent-point margin change, not margin percent-growth.
 assert abs(growth-(rev-pr)/pr*100)<D('1e-24');assert abs(pp-(gp*pr-pgp*rev)/(rev*pr)*100)<D('1e-24')
 rid='run-03-'+quarter[-2:].lower();ref=base+'/cycles/'+quarter+'/2024-08-02-'+rid
 dep={'consumed':{q['id']:{'version':q['identity'],'projection':q['projection']}}}
 calc={'source':q,'raw_identity_verified':True,'period':{'start':raw['start'],'end':raw['end'],'type':'three-month quarter; comparative prior-year quarter; not cumulative'},'unit':'USD; divide by 1000000 for USD millions','inputs':{k:a[k] for k in ['revenue','revenue_prior_year','gross_profit','gross_profit_prior_year']},'formulas':{'revenue_yoy_pct':'100*(revenue/revenue_prior_year-1)','current_gross_margin_pct':'100*gross_profit/revenue','prior_gross_margin_pct':'100*gross_profit_prior_year/revenue_prior_year','gross_margin_change_pp':'current margin percent minus prior margin percent'},'values':dict(zip(['revenue_yoy_pct','current_gross_margin_pct','prior_gross_margin_pct','gross_margin_change_pp'],map(str,[growth,gm,pgm,pp]))),'product_revenue_deltas_usd':deltas,'product_sum_checks':True,'independent_arithmetic_route_checked':True,'method':method}
 calcs[quarter]=calc['values']
 if quarter=='2024Q2':
  interpretation='Revenue contraction coexists with higher margin. Product changes in USD millions are iPhone -5,371, Mac +283, iPad -1,111, Wearables/Home/Accessories -844 and Services +2,960: total -4,083. Greater China fell 1,440 million. Services offsets do not establish broad demand strength. Original MD&A attributes Services margin improvement to mix; currency and product volume oppose an inference of durable pricing power. These are management explanations, not independently isolated causes.'
 else:
  interpretation='Revenue expansion coexists with uneven demand: Services +3,000 and iPad +1,371 million offset iPhone -373 and Wearables/Home/Accessories -187; Mac +169 reconciles total +3,980. Greater China fell 1,030 million. Higher consolidated margin does not prove broad volume growth or durable pricing power; mix, pricing, currency, cost and launch timing cannot be separately quantified from this pack.'
 text=f'''# AAPL {quarter}: freshly recomputed growth under v3

Latest local assessment cutoff {cut}; reconstructed with a later-authored local method, not a contemporaneous forecast. Retained original accession {q['identity']}, period {raw['start']} through {raw['end']}; economic publication {q['available_at']} is eligible at cutoff. No retrieval or method date establishes historical economic availability.

Revenue {rev} versus {pr} USD gives {growth:.12f}% year-over-year growth. Gross profit {gp} versus {pgp} USD gives current margin {gm:.12f}%, prior margin {pgm:.12f}%, change {pp:.12f} percentage points. Calculations use dollar inputs afresh, never saved percentage outputs. See calculations.json for formulas, exact Decimal results, alternative arithmetic checks and product reconciliation. Quarter values are compared with prior-year quarter values; cumulative columns, EPS and average shares are not subtracted.

{interpretation}

Source binding: `{q['raw_ref']}`, SHA256 `{q['raw_digest']}`, metadata `data/sources/{quarter}.json`. [Original filing reference]({raw['source_url']}). The raw_ref is a retained transformed quarter pack, not HTML. Locally read period/identity metadata, four primary numeric inputs and MD&A product/geographic table_rows. Q2 original page was accessed for selected cover, fiscal labels, statement and MD&A passages documented in source-check.json; Q3 original was not newly opened and its identity was not re-researched. Original-page access does not retain raw HTML or verify the prior HTML hash. No full filing reading, raw-context validation, amendment inventory or fresh official filing-date check is claimed.

Method v3-authorship-corrected content and dependency were reverified; actual revision {method['authored_at']}, content SHA256 {method['content_digest']}. Earlier v1/v2 exact author times were incorrectly supplied preparer declarations, not verified actual times; v2 was future when discovered. Old reports and frozen erroneous records remain intact. This new calculation/check/output supersedes affected growth, rather than rebinding old prose to v3. Q3 independent identity remains the exact predecessor unit.

Competing interpretation tested: margin improvement alone might look healthy despite concentrated revenue offsets; the category reconciliation and geographic weakness reject an unqualified broad-growth thesis. Source corrections, revised period definitions or quantified temporary mix/currency/cost effects could overturn the bounded interpretation. This completes only the configured growth question at retained-evidence scope. Full investment-case remains required and pending: full narrative, notes, governance, competition, forecasts, dated price and valuation are not resolved. No later-authored economic observations or later comparative rows from forecast/valuation supplements were used. No price, target, rating or expected return is invented.
'''
 files={'growth.md':text,'calculations.json':json.dumps(calc,indent=2),'source-check.json':json.dumps(access if quarter=='2024Q2' else {'external_attempted':False,'external_success':False,'retained_prior_check':base+'/cycles/2024Q3/2024-08-02-run-01-q3/source-check.json','read_coverage':[q['raw_ref']+': four growth inputs and table_rows'],'limitations':['No new Q3 original reading or identity research; prior page success is not new success.']},indent=2),'method-check.json':json.dumps({'applied':method,'actual_content_digest':hashp(method['content_ref']),'authorship_correction':'AUTHORSHIP-CORRECTION.md','generic_method_hashes':{p:hashp(p) for p in ['package/README.md','package/skills/finance-research/SKILL.md','package/skills/finance-research/references/research-method.md']},'prior_growth_input':old['units']['growth']['analysis_inputs'],'new_analysis_not_relabel':True},indent=2)}
 def unit(name,content,inputs=False):
  digest=hashlib.sha256(content.encode()).hexdigest();files[name+'.md']=content;files[name+'-check.json']=json.dumps({'version':1,'output_digest':digest,'checks':dict.fromkeys(['sources','citations','calculations','counterevidence'],True),'unresolved':[],'scope':'author self-check, bounded retained original-quarter evidence; not independent review','evidence':['calculations.json','source-check.json']},indent=2)
  u={**copy.deepcopy(dep),'output':{'path':ref+'/'+name+'.md','digest':digest},'verification':ref+'/'+name+'-check.json'}
  if inputs:u['analysis_inputs']={'growth-method':{'kind':method['kind'],'version':method['identity'],**{k:method[k] for k in ['authored_at','projection','content_ref','content_digest']}}}
  return u
 units={'growth':unit('growth',text,True)}
 if quarter=='2024Q3':units['identity']=copy.deepcopy(old['units']['identity'])
 else:
  manifests=load('retained/data/source-manifests.json');res=next(x['resolution'] for x in manifests if x['quarter']==quarter);assert res['original_accession']==q['identity'];assert res['evidence']['declarations']=={'DocumentFiscalYearFocus':'2024','DocumentFiscalPeriodFocus':'Q2','DocumentPeriodEndDate':'2024-03-30','EntityCentralIndexKey':'0000320193'}
  identity=f'''# AAPL 2024Q2: bounded fiscal identity

Fiscal 2024 Q2, endpoint 2024-03-30, accession {q['identity']}. [Original 10-Q]({raw['source_url']}) cover and Q2 footer corroborate retained declarations (2024/Q2/0000320193). Three-month comparison ends April 1, 2023; six-month columns are separate. Calendar Q1 labeling and cumulative-period confusion are rejected by these source labels, not by filename or quote date.

Retained source-manifests.json Q2 resolution records c-1 declarations, official filing date 2024-05-03, original HTML digest {res['evidence']['sha256']} and retrieval {res['evidence']['retrieved_at']}. This is preserved provenance, not a newly recomputed HTML hash. Pack raw_ref {q['raw_ref']} SHA256 {q['raw_digest']} matches bytes and projection; source metadata fiscal/accession/end agree with retained declaration record and newly accessed original labels. Official-date metadata is accepted at retained-evidence scope; signature May 2 is not substituted for official publication May 3. Both precede assessment cutoff {cut}.

Raw inline tags/contextRef semantics, independent filing-index date, amendments and inventory completeness remain unverified. Thus bounded fiscal identity is verified, not a full acquisition resolution rerun. Contradictory original declarations or revised accession/date would invalidate it. No inference from local method date, filename, price or calendar month is used. Source-check.json records actual page access and exclusions. No Q3 identity was re-researched.
'''
  units['identity']=unit('identity',identity)
 research={'method':'revenue-yoy-and-gross-margin-v3-authorship-corrected; actual local revision '+method['authored_at'],'assumptions':['Retained official publication dates accepted; independent index/amendment check pending','Retained transformed packs accepted for bounded questions; no later economic supplements used','Pilot horizons retained, not a user-confirmed holding preference'],'changes':'Q3 growth recomputed from raw dollar inputs after real v3 content/authorship change; Q3 identity reused exactly. Q2 first managed bounded growth and identity analysis; original errors/history preserved.','gaps':['investment-case required and pending','Full narrative, notes, governance, competition, forecasts, dated price and valuation pending','Raw HTML/context validation and filing-index/amendment coverage unverified'],'horizons':{}}
 for h,window in [('short','(0,3]'),('medium','(3,12]'),('long','(12,60]')]:
  research['horizons'][h]={'judgment':f'insufficient_evidence for investment return; {window} months anchored at {cut}. '+('Revenue contraction and margin expansion are mixed operating evidence.' if quarter=='2024Q2' else 'Revenue and margin expansion are uneven across products and geography.')+' No price/valuation bridge; convention differs from later one-quarter/1–3-year/5+-year approach.','evidence':[ref+'/growth.md',units['identity']['output']['path']],'invalidation_triggers':['Correction of original inputs or period identity','Services weakness or persistent product/geographic weakness','Obtain dated price, appropriate valuation and horizon-specific driver evidence before investment judgment']}
 review={'version':1,'id':rid,'fiscal':q['fiscal'],'cutoff':cut,'units':units,'research':research}
 if quarter=='2024Q3':
  review['predecessor']=old['id']
  for k in ['last_attempt','last_success']:
   if k in old:review[k]=old[k]
 else:review['last_attempt']=now # actual successful original page access; never a full-case success
 try:saved=m.publish(r,'aapl',review,files,expected,rid,complete=False)
 except (ValueError,OSError) as e:
  put('run-03-error-'+quarter+'.json',{'run':rid,'error':str(e)});raise
 results.append(saved)
 current=m.publication_snapshot(r)
 assert all(current[p]==v for p,v in expected.items())
 if quarter=='2024Q3':
  put('run-03-between-publications.json',{'old_paths_unchanged':True,'known_new_paths':{p:v for p,v in current.items() if p not in expected},'reason':'Only reviewed Q3 partial checkpoint additions; baseline extended for subsequent Q2 publication'})
  expected=current;put('run-03-q2-baseline.json',expected)
put('run-03-publication.json',results);after=m.discover(r,'latest',cut);put('run-03-discovery-after.json',after)
assert len(after['reusable'])==4,after
assert {x['work'] for x in after['reusable']}=={'growth','identity'}
assert all(x['evidence']=='investment-case' or x['evidence']=='dependencies:investment-case' for x in after['gaps']),after
new=load(results[0]['review']);assert new['units']['identity']==old['units']['identity'];assert new.get('last_success')==old.get('last_success');assert ('last_success' in new)==('last_success' in old)
changes={p:{'before':v,'after':hashp(p)} for p,v in before.items() if hashp(p)!=v};managed={p:{'before':v,'after':hashp(p)} for p,v in load('before-run-03.json').items()};assert all(x['before']==x['after'] for x in managed.values())
put('run-03-preservation.json',{'preexisting_managed_hashes':managed,'all_preexisting_managed_unchanged':True,'preexisting_files_changed':changes,'identity_unit_exact_equal':True,'identity_output_hash':hashp(old['units']['identity']['output']['path']),'identity_check_hash':hashp(old['units']['identity']['verification']),'last_success_presence_preserved':True,'new_last_success':False,'prior_preservation_evidence':{p:hashp(p) for p in ['run-02-reuse-evidence.json','run-02-final-validation.json','independent-runs-01-02-check.json']},'calculations':calcs,'source_attempts':{'original_Q2_page_attempt':1,'original_Q2_page_success':1,'Q3_new_page_attempt':0,'SEC_acquisition_attempt':0,'full_inventory_success':0}})
print(json.dumps({'published':results,'values':calcs,'reusable':after['reusable'],'status':after['status'],'preexisting_changes':changes},indent=2))
