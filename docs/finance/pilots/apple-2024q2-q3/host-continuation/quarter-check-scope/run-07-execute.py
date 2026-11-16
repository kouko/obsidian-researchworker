from pathlib import Path
import json, hashlib, importlib.util
from decimal import Decimal, getcontext
from datetime import datetime, timezone
r=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('research_store',r.parent/'package/scripts/research_store.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def load(p):return json.loads((r/p).read_text())
def digest(p):return hashlib.sha256((r/p).read_bytes()).hexdigest()
def save(p,v):
 with (r/p).open('x') as f:f.write(json.dumps(v,indent=2)+'\n')
def enc(v):return json.dumps(v,indent=2)+'\n'
expected=load('run-07-publication-before.json')
assert m.publication_snapshot(r)==expected
old=load('before-run-07.json');assert all(digest(p)==h for p,h in old.items())
arrival=load('arrival-before.json');added=load('arrival-added.json')['new_files']
assert all(digest(p)==h for p,h in arrival.items())
assert set(old)==set(arrival)|set(added)
assert all(digest(p)==h for p,h in added.items())
b='investing/assets/equities/aapl';q2=load(b+'/cycles/2024Q2/2024-08-02-bounded-baseline-q2/review.json');imp=load('imports/original-q2-review/review.json')
for q in ['growth','identity']:
 u=q2['units'][q];orig=imp['units'][q]
 assert u['consumed']==orig['consumed']
 assert u.get('analysis_inputs',{})==orig.get('analysis_inputs',{})
 assert u['output']['digest']==orig['output']['digest']==digest(u['output']['path'])
 assert (r/u['output']['path']).read_bytes()==(r/'imports/original-q2-review'/Path(orig['output']['path']).name).read_bytes()
 assert (r/u['verification']).read_bytes()==(r/'imports/original-q2-review'/Path(orig['verification']).name).read_bytes()
source=load(b+'/data/sources/2024Q3.json');raw=load(source['raw_ref']);assert raw==source['projection'];assert digest(source['raw_ref'])==source['raw_digest']
method=load(b+'/data/analysis/growth-method.json');assert digest(method['content_ref'])==method['content_digest']
generic={p:hashlib.sha256((r.parent/'package'/p).read_bytes()).hexdigest() for p in ['README.md','skills/finance-research/SKILL.md','skills/finance-research/references/research-method.md']}
assert generic=={k.removeprefix('package/'):v for k,v in load('imports/original-q2-review/method-check.json')['generic_method_hashes'].items()}
getcontext().prec=40
v=raw['metrics'];D=Decimal
rev=D(v['revenue']);prior=D(v['revenue_prior_year']);gp=D(v['gross_profit']);pgp=D(v['gross_profit_prior_year'])
growth=(rev/prior-1)*100;gm=gp/rev*100;pgm=pgp/prior*100;delta=gm-pgm
assert abs(growth-(rev-prior)/prior*100)<D('1e-35')
assert rev-D(46099000000)==gp and prior-D(45384000000)==pgp
cats=['iphone','mac','ipad','wearables_home_and_accessories','services'];diff={k:v[k]-v[k+'_prior_year'] for k in cats}
assert sum(v[k] for k in cats)==rev and sum(v[k+'_prior_year'] for k in cats)==prior and sum(diff.values())==rev-prior
calc=dict(version=1,units='USD; percentage results in percent; margin change in percentage points',inputs={k:v[k] for k in ['revenue','revenue_prior_year','gross_profit','gross_profit_prior_year']},formulas={'growth':'(revenue/revenue_prior_year-1)*100','margin':'gross_profit/revenue*100','prior_margin':'gross_profit_prior_year/revenue_prior_year*100','change':'margin-prior_margin'},results={k:str(x) for k,x in [('growth_pct',growth),('margin_pct',gm),('prior_margin_pct',pgm),('change_pp',delta)]},category_dollar_changes=diff,checks={'category_totals_reconcile':True,'sales_less_original_cost_of_sales_reconciles':True,'alternative_growth_formula_agrees':True},source='Original Q3 statements of operations and MD&A three-month columns; no YTD subtraction; stored derived percentages not used')
now=datetime.now(timezone.utc).isoformat();url=raw['source_url'];idx=url.rsplit('/',1)[0]+'/0000320193-24-000081-index.html';idx2='https://www.sec.gov/Archives/edgar/data/320193/000032019324000069/0000320193-24-000069-index.html'
sourcecheck=dict(version=1,checked_at=now,channel='web.run open/find',external_attempted=True,page_access_success=True,urls=[url,idx,idx2,'https://www.sec.gov/Archives/edgar/data/320193/000032019324000069/aapl-20240330.htm'],successful_unique_pages=4,read_coverage=['Q3 rendered DEI declaration prefix line 0: false/2024/Q3/0000320193; cover lines 11-56: Form 10-Q, June 29 2024, Apple/AAPL','Q3 statements of operations lines 120-139: millions, three/nine-month distinction, revenue/gross profit and costs','Q3 fiscal Q3 2024 footer line 662; MD&A category rows 739-769 and geographic rows 710-725; gross-margin rows/narrative 775-804','Q2 and Q3 SEC accession indexes lines 9-34: original form, accession, official filing date, acceptance date, period and primary document link','Q2 original page opened; Q2 prior analysis is adopted verified run03 work, not newly performed analysis'],publication_dates={'Q2':'2024-05-03','Q3':'2024-08-02'},acceptance_dates={'Q2':'2024-05-02 18:04:25','Q3':'2024-08-01 18:03:34'},exclusions=['Raw inline-XBRL contextRef agreement/semantics not revalidated','No raw HTML retained or original-HTML digest recomputed','Amendment inventory and complete current SEC coverage not checked','Full notes, risk factors, governance/proxy, valuation and other full-company questions not researched','No later economic supplements or future comparative rows used'],sec_acquisition={'configured_identity':False,'attempted':False,'reason':'SEC_USER_AGENT absent; no fabricated identity or private credential/config read; normal public web tools used successfully'},freshness='Selected historical original pages/indexes corroborated; external inventory freshness remains unverified',source_raw_kind='Retained transformed JSON quarter pack, not original HTML')
target=b+'/cycles/2024Q3/2024-08-02-run-07-q3'
growthtext=f'''# AAPL fiscal 2024 Q3: bounded growth and margin

At latest-mode cutoff 2024-08-02T23:59:59+00:00, [original Q3 filing]({url}) statements of operations, three-month columns, report revenue USD 85,777m versus 81,797m and gross profit 39,678m versus 36,413m. Dollar recomputation gives revenue growth {growth:.12f}%, margin {gm:.12f}% versus {pgm:.12f}%, an increase of {delta:.12f} percentage points. Sales less costs and category totals independently reconcile (calculations.json).

MD&A category changes in USD millions: iPhone -373, Mac +169, iPad +1,371, Wearables/Home/Accessories -187, Services +3,000; sum +3,980. Greater China decreased 1,030m. Services and iPad outweigh declining categories; this is not broad-based product strength. Management attributes Services margin expansion to mix. Causality and durability are not independently isolated. Product margin is approximately flat, a counterexample to extrapolating consolidated improvement into universal pricing power. Corrected source values or period definitions would invalidate the arithmetic.

Cross-quarter interpretation uses the preserved Q2 run03-derived baseline: Q2 revenue growth -4.305327090978% and margin expansion 2.316401771522pp; Q3 returns to year-over-year growth with smaller year-over-year margin expansion. This is a comparison of separate year-over-year rates, not seasonally adjusted sequential growth or a forecast. Q2 output/check/source/method identities agree; no Q2 bytes were rewritten. Its full-scope wording remains historical context, not this root's requirements.

Source binding: {source['raw_ref']}, SHA256 {source['raw_digest']}; retained transformed JSON equals declared typed projection. Original page corroboration and exclusions are in source-check.json. Read only the selected cover, statements, category/geographic and gross-margin passages; downloading/opening is not full filing reading. No EPS/share or cumulative subtraction used.

Applied v3 content digest {method['content_digest']}; actual local revision {method['authored_at']}. Generic method/README hashes agree with adopted checks (method-check.json). This is a 2026-authored reconstruction using economic sources eligible in 2024, not historical method availability. Earlier erroneous v1/v2 declarations remain untouched. Assumptions: reported rounded million-dollar amounts are adequate for this bounded arithmetic; no restatement is inferred. Rounding limits precision. Full-company investment diligence, forecasts and security returns are outside scope, not silently completed. No bounded required gap remains.
'''
identitytext=f'''# AAPL fiscal 2024 Q3: bounded original identity

The [original filing]({url}) rendered DEI prefix declares fiscal 2024/Q3 and issuer 0000320193; cover identifies Apple Inc., AAPL, Form 10-Q and June 29, 2024 endpoint. Its Q3 2024 footer corroborates the quarter. The three-month statement comparison ends July 1, 2023; nine-month columns are separate. Retained start 2024-03-31 agrees with the page's rendered duration context. Identity comes from declarations and labels, not filename, calendar month, quote date or local file time.

[Q3 SEC index]({idx}) binds accession 0000320193-24-000081, Form 10-Q, period 2024-06-29 and official filing 2024-08-02. [Q2 SEC index]({idx2}) separately binds 0000320193-24-000069, period 2024-03-30 and filing 2024-05-03. Acceptance occurred on the preceding evenings; acceptance/signature times do not replace the official filing dates for this cutoff. Both original publication dates are eligible at 2024-08-02T23:59:59+00:00; intraday tradability is not established.

The Q3 transformed pack and metadata agree on fiscal identity, accession, period and raw digest {source['raw_digest']}. This is bounded corroboration, not a full acquisition resolution: raw inline-XBRL same-context validation, raw HTML digest, amendments and current filing inventory remain unverified exclusions. Contradictory original declarations or an accession/date correction would invalidate this conclusion. No such conflict was observed in the selected passages. source-check.json distinguishes actual successful page checks from an unattempted acquisition CLI.

Provenance: SETUP.py/output, baseline-publication/discovery and arrival-before/added/discovery show Q2 was normally adopted first, then the two Q3 retained input files were added without baseline changes at 2026-11-16T02:24:59.073284+00:00. That is controlled local historical arrival, not a new 2026 filing or new economic publication. Q2 originated in actual imported run03 units; imported investment-case requirements remain unchanged. This completes only this root's original bounded identity question.
'''
files={'growth.md':growthtext,'identity.md':identitytext,'calculations.json':enc(calc),'source-check.json':enc(sourcecheck),'method-check.json':enc(dict(version=1,applied=method,generic_method_hashes=generic,content_digest_verified=True,substantive_contract='Recomputed revenue YoY and both margins from original-quarter amounts; unit and counterevidence reconciliation; bounded identity and reading exclusions',actual_authorship_not_economic_availability=True))}
units={}
for q,text in [('growth',growthtext),('identity',identitytext)]:
 h=hashlib.sha256(text.encode()).hexdigest();files[q+'-check.json']=enc(dict(version=1,output_digest=h,checks={k:True for k in ['sources','citations','calculations','counterevidence']},unresolved=[],scope='Author self-check of bounded required question, not independent review',evidence=['source-check.json','calculations.json','method-check.json']))
 units[q]=dict(consumed={source['id']:dict(version=source['identity'],projection=source['projection'])},output=dict(path=target+'/'+q+'.md',digest=h),verification=target+'/'+q+'-check.json')
units['growth']['analysis_inputs']={'growth-method':{k:method[k] for k in ['kind','authored_at','projection','content_ref','content_digest']}}
units['growth']['analysis_inputs']['growth-method']['version']=method['identity']
review=dict(version=1,id='run-07-q3',fiscal=source['fiscal'],cutoff='2024-08-02T23:59:59+00:00',units=units,last_attempt=now,research=dict(method='Source-invoked finance-research and method/README; revenue-yoy-and-gross-margin-v3-authorship-corrected, actual local revision '+method['authored_at'],assumptions=['Only originally configured growth and identity questions are required','Reported rounded USD millions support bounded arithmetic; no unobserved amendment/restatement asserted','Pilot windows retained: short (0,3], medium (3,12], long (12,60] months from 2024-08-02 cutoff, not user holding preference; differs from later exploratory one-quarter/1–3-year/5+-year convention','Historical economic cutoff differs from actual 2026 method authorship, local controlled arrival and verification time'],changes='First normal managed Q3 review after controlled retained-source arrival. Q3 growth and bounded fiscal identity newly executed; Q2 run03-derived adopted baseline preserved and reusable; original full-scope imports/requirements untouched.',gaps=[],horizons={h:dict(judgment='insufficient_evidence for investment advice; '+window+' months from 2024-08-02. Q3 arithmetic supports observed growth/margin improvement only; no dated valuation, price or horizon-specific forecast. Not hold, zero return, rating or target.',evidence=[target+'/growth.md',target+'/identity.md'],invalidation_triggers=['Original data or fiscal/date correction','Services or category mix reversal','Obtain separate horizon-specific drivers and dated suitable valuation before any investment conclusion']) for h,window in [('short','(0,3]'),('medium','(3,12]'),('long','(12,60]')]}))
save('run-07-proposal.json',dict(review=review,files=files,complete=True))
try:result=m.publish(r,'aapl',review,files,expected,'run-07',complete=True)
except (ValueError,OSError) as e:
 save('run-07-publication-error.json',dict(type=type(e).__name__,error=str(e)));raise
save('run-07-publication.json',result)
after=m.discover(r,'latest',review['cutoff']);save('run-07-after-discovery.json',after)
assert not after['gaps'] and len(after['reusable'])==4
before=load('run-07-root-before.json');unchanged={p:digest(p)==h for p,h in before.items()};assert all(unchanged.values())
save('run-07-preservation.json',dict(version=1,checked_at=datetime.now(timezone.utc).isoformat(),all_preexisting_root_files_unchanged=all(unchanged.values()),files=unchanged,managed_before=expected,managed_after=m.publication_snapshot(r),q2_adopted_units_outputs_checks_and_dependencies_agree_with_imports=True,controlled_arrival_old_files_unchanged=True,controlled_arrival_only_expected_q3_files=True,method_generic_hashes_agree=True))
print(json.dumps(dict(publication=result,discovery_status=after['status'],reusable=after['reusable'],growth=str(growth),margin=str(gm),change_pp=str(delta),preserved_files=len(unchanged)),indent=2))
