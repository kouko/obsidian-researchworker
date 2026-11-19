import pathlib,json,hashlib,importlib.util,copy
from decimal import Decimal
r=pathlib.Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('research_store',r/'package/scripts/research_store.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
load=lambda p:json.loads((r/p).read_text())
digest=lambda p:hashlib.sha256((r/p).read_bytes()).hexdigest()
put=lambda p,o:(r/p).write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
expected=load('run-02-baseline.json');assert m.publication_snapshot(r)==expected
# Preserve every preexisting regular file, including reports outside investing.
before={str(p.relative_to(r)):hashlib.sha256(p.read_bytes()).hexdigest() for p in r.rglob('*') if p.is_file() and not p.is_symlink()}
put('run-02-files-before.json',before)
base='investing/assets/equities/aapl';oldref=base+'/cycles/2024Q3/2024-08-02-run-01-q3';old=load(oldref+'/review.json')
method=load(base+'/data/analysis/growth-method.json');assert digest(method['content_ref'])==method['content_digest'];assert method['identity']=='v2'
q=load(base+'/data/sources/2024Q3.json');raw=load(q['raw_ref']);assert digest(q['raw_ref'])==q['raw_digest'];assert raw==q['projection']
a=raw['metrics'];D=Decimal
rev=D(a['revenue']);prior=D(a['revenue_prior_year']);gp=D(a['gross_profit']);pgp=D(a['gross_profit_prior_year'])
growth=(rev/prior-1)*100;gm=gp/rev*100;pgm=pgp/prior*100;change=gm-pgm
ref=base+'/cycles/2024Q3/2024-08-02-run-02-q3'
calc={'source':{'metadata':base+'/data/sources/2024Q3.json','raw_ref':q['raw_ref'],'raw_digest':q['raw_digest'],'identity':q['identity'],'available_at':q['available_at'],'fiscal':q['fiscal'],'source_url':raw['source_url']},'period':{'start':raw['start'],'end':raw['end'],'comparison':'prior-year three-month quarter, not YTD'},'input_unit':'USD','display_unit':'USD millions; divide USD inputs by 1000000','inputs':{k:a[k] for k in ['revenue','revenue_prior_year','gross_profit','gross_profit_prior_year']},'calculations':{'revenue_yoy_pct':{'formula':'100*(85777000000/81797000000-1)','value':str(growth)},'gross_margin_current_pct':{'formula':'100*39678000000/85777000000','value':str(gm)},'gross_margin_prior_pct':{'formula':'100*36413000000/81797000000','value':str(pgm)},'gross_margin_change_pp':{'formula':'current gross margin percent - prior gross margin percent','value':str(change)}},'method':method,'external_verification_this_run':False}
text=f'''# AAPL 2024Q3 — growth and gross margin, applied method v2

Assessment: latest eligible local evidence at 2024-08-02T23:59:59+00:00. Fiscal identity: 2024 Q3, ended 2024-06-29, accession {q['identity']}. This is a later-authored reconstruction, not a contemporaneous forecast.

Revenue grew {growth:.6f}% year over year. Gross margin was {gm:.6f}%, versus {pgm:.6f}% in the prior-year quarter: an improvement of {change:.6f} percentage points.

## Source-bound arithmetic

Retained transformed original-quarter pack: `{q['raw_ref']}`, SHA256 `{q['raw_digest']}`; metadata `{base}/data/sources/2024Q3.json`, publication date {q['available_at']}. [Original filing reference]({raw['source_url']}). This URL is retained provenance and was not opened in this run.

Read locally: metrics.revenue, revenue_prior_year, gross_profit and gross_profit_prior_year; three-month period metadata; MD&A product/geographic table_rows. USD values reconcile to USD millions: revenue 85,777 versus 81,797; gross profit 39,678 versus 36,413. Revenue growth = (85,777/81,797−1)×100. Current margin = 39,678/85,777×100; prior margin = 36,413/81,797×100. Subtract the two margins for percentage-point change, not percent growth. calculations.json retains full decimal results and input bindings; no saved percentage is used as the calculation input.

## Interpretation and opposing evidence

Revenue and gross margin both improved year over year, supporting bounded operating improvement. That is not proof of broad product demand or durable profit expansion. The retained product table shows Services +3,000 and iPad +1,371 million, offset by iPhone −373 and Wearables/Home/Accessories −187 million; Mac +169 reconciles the total +3,980 million revenue change. Greater China declined 14,728 versus 15,758 million. Mix, pricing, costs, currency and launch timing remain competing explanations; this pack does not establish their separate contributions or unit-volume growth. A higher consolidated margin alone cannot establish pricing power or durable competitive advantage. A correction to the source values/definitions or evidence of temporary mix/cost effects would change this interpretation.

## Change, authorship and limits

Predecessor: run-01-q3. Recomputed only Q3 growth because its declared growth-method dependency changed from v1 to v2; independent fiscal identity retains its complete prior unit and exact output/check paths and bytes. No managed Q2 analysis is newly completed. v2 actual authorship is {method['authored_at']}; its exact content digest is {method['content_digest']}. Generic package method and README contracts were read; hashes are in method-check.json. No local method date is treated as historical economic availability.

Only local retained transformed JSON was examined in this run, not raw filing HTML, new original passages, filing index/amendments or full statements/notes. Prior run's source-check remains historical evidence, not a new external success. Original raw-HTML/table context, full narrative, risks, governance, competition, forecasts, dated price and valuation remain gaps for the full investment-case. No later economic data, invented price, investment rating or return estimate is used. The bounded growth question is self-checked; the full investment-case remains pending.
'''
sha=hashlib.sha256(text.encode()).hexdigest()
files={'growth.md':text,'calculations.json':json.dumps(calc,indent=2),'growth-check.json':json.dumps({'version':1,'output_digest':sha,'checks':dict.fromkeys(['sources','citations','calculations','counterevidence'],True),'unresolved':[],'scope':'Author self-check of local transformed-pack growth/margin only; not independent review or external verification','calculation_evidence':ref+'/calculations.json'},indent=2),'source-check.json':json.dumps({'version':1,'external_attempted':False,'external_success':False,'external_freshness':'unverified','retained_prior_check':oldref+'/source-check.json','read_coverage':[q['raw_ref']+': period metadata, four metric inputs and MD&A table_rows'],'limitations':['Retained transformed pack, not raw HTML; no new external reading or filing-index/amendment verification.']},indent=2),'method-check.json':json.dumps({'applied':method,'content_hash_verified':True,'prior_applied':old['units']['growth']['analysis_inputs']['growth-method'],'generic_contract_hashes':{p:digest(p) for p in ['package/README.md','package/skills/finance-research/SKILL.md','package/skills/finance-research/references/research-method.md']},'authorship_not_economic_availability':True},indent=2)}
review={k:copy.deepcopy(old[k]) for k in ['version','fiscal','cutoff','research']}
review.update(id='run-02-q3',predecessor=old['id'],units={'identity':copy.deepcopy(old['units']['identity']),'growth':{'consumed':{'filing-2024Q3':{'version':q['identity'],'projection':q['projection']}},'analysis_inputs':{'growth-method':{'kind':method['kind'],'version':method['identity'],**{k:method[k] for k in ['authored_at','projection','content_ref','content_digest']}}},'output':{'path':ref+'/growth.md','digest':sha},'verification':ref+'/growth-check.json'}})
for k in ['last_attempt','last_success']:
 if k in old:review[k]=old[k]
review['research']['method']='revenue-yoy-and-gross-margin-v2; actual authorship '+method['authored_at']+'; retained pilot horizons (0,3], (3,12], (12,60] months anchored at cutoff, distinct from later one-quarter/1–3-year/5+-year convention and not user holding preference'
review['research']['changes']='Method v1→v2 invalidated growth; recomputed Q3 revenue growth and current/prior gross margin with percentage-point change from retained USD inputs. Independent identity unit reused verbatim. No whole investment-case synthesis completed.'
for h in review['research']['horizons'].values():
 h['evidence']=[ref+'/growth.md',old['units']['identity']['output']['path']]
 h['judgment']+=' Revenue and margin improvement are bounded observations; durability and investment implications remain unverified.'
try:
 saved=m.publish(r,'aapl',review,files,expected,'run-02-q3',complete=False)
except (ValueError,OSError) as e:
 put('run-02-error.json',{'run':'run-02-q3','error':str(e)});raise
put('run-02-publication.json',saved)
after=m.discover(r,'latest',review['cutoff']);put('run-02-discovery-after.json',after)
new=load(saved['review']);assert new['units']['identity']==old['units']['identity'];assert new.get('last_success')==old.get('last_success');assert ('last_success' in new)==('last_success' in old)
unchanged={p:{'before':v,'after':digest(p)} for p,v in before.items()};assert all(v['before']==v['after'] for v in unchanged.values())
u=old['units']['identity'];evidence={'all_preexisting_files_unchanged':True,'preexisting_file_count':len(before),'files':unchanged,'identity_unit_exact_equal':True,'identity_unit':u,'identity_output_actual_digest':digest(u['output']['path']),'identity_check_actual_digest':digest(u['verification']),'last_success':{'before_present':'last_success' in old,'after_present':'last_success' in new,'before':old.get('last_success'),'after':new.get('last_success')},'source_metadata_unchanged':True,'external_attempts':0,'external_successes':0}
assert evidence['identity_output_actual_digest']==u['output']['digest']
put('run-02-reuse-evidence.json',evidence)
print(json.dumps({'publication':saved,'calculations':calc['calculations'],'after':after},indent=2))
