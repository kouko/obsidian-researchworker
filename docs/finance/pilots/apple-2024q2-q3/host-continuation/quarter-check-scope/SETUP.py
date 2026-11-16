from pathlib import Path
import json,hashlib,shutil,sys,importlib.util
from datetime import datetime,timezone
parent=Path('/private/tmp/finance-host-public-20261116');root=parent/'quarter-check-scope'
root.mkdir(exist_ok=False)
base='investing/assets/equities/aapl'
def put(ref,obj):
 p=root/ref;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2)+'\n')
def hashes():return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (root/'investing').rglob('*') if p.is_file()}
(root/'SCOPE.md').write_text('''# Initial bounded quarterly research scope

This separate public root is defined FROM INITIALIZATION as fiscal-quarter
revenue/gross-margin arithmetic and original fiscal-identity checking only.
It is not complete company investment research, recommendations, or the A–G
program. The original main root retains investment-case required questions and
all gaps unchanged. Here the only required questions are growth and identity.
Mode latest; assessment cutoff 2024-08-02T23:59:59+00:00. Q2 baseline adopts
actual substantive verified run03 Q2 units, with original imports retained.
A controlled Q3 source arrival follows a saved Q2 baseline, using real adjacent
original accessions and distinct original publication dates. External freshness
is unverified; original filing identity/date and selected-source coverage limits
remain explicit. All investment horizons are outside this narrow conclusion's
advisory sufficiency; no rating/target/return is claimed.

Source skill: ../package/skills/finance-research/SKILL.md, its method and README.
Helper: ../package/scripts/research_store.py (fixed source b4ee26d). Source-invoked,
not installed-plugin evidence. Current applied method v3 was actually revised
2026-11-16T02:08:46.931664+00:00. Earlier v1/v2 exact author declarations were
wrong, preserved in the main root and imported historical records; they are
not historical economic availability. This root never changes old requirements
or old reviews to remove a question: it creates its own scope and new baseline.
''')
put('investing/research.json',dict(version=1,assets=['aapl']))
put(base+'/asset.json',dict(version=1,id='aapl',issuer='AAPL',questions=[dict(id='growth',required_sources=['filing-{fiscal}'],required_analysis=['growth-method'],depends_on=[]),dict(id='identity',required_sources=['filing-{fiscal}'],depends_on=[])]))
for ref in [base+'/data/2024Q2.json',base+'/data/sources/2024Q2.json',base+'/data/analysis/growth-method.json',base+'/data/growth-method-v3.txt']:
 p=root/ref;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(parent/ref,p)
original=parent/(base+'/cycles/2024Q2/2024-08-02-run-03-q2')
shutil.copytree(original,root/'imports/original-q2-review')
old=json.loads((original/'review.json').read_text());review_id='bounded-baseline-q2';target=base+'/cycles/2024Q2/2024-08-02-'+review_id
units=json.loads(json.dumps(old['units']));files={}
for name,u in units.items():
 for field in ['output','verification']:
  ref=u['output']['path'] if field=='output' else u['verification'];filename=Path(ref).name;files[filename]=(parent/ref).read_text()
  if field=='output':u['output']['path']=target+'/'+filename
  else:u['verification']=target+'/'+filename
for name in ['source-check.json','calculations.json','method-check.json']:
 if (original/name).exists():files[name]=(original/name).read_text()
review=dict(version=1,id=review_id,fiscal=old['fiscal'],cutoff=old['cutoff'],units=units,research=dict(method='Bounded adopted actual run03 Q2 growth/fiscal-identity study under verified local method v3; source-invoked finance method. Not complete investment research.',assumptions=['Only growth and fiscal identity are required in this separately initialized scope','Actual original unit texts/checks and source/method identities adopted verbatim from real run03 Q2; only new final output paths differ','External freshness/full raw filing/date-index verification remain unverified; no advisory sufficiency or holding period inferred'],changes='New independent bounded scope adopts completed substantive Q2 units; imports/original-q2-review retains original full-scope review and requirements unchanged. No original main-root question is removed.',gaps=[],horizons={h:dict(judgment='insufficient_evidence: investment judgment outside this arithmetic/fiscal-identity scope',evidence=['filing-2024Q2'],invalidation_triggers=['Original-quarter corrections or fiscal-identity conflict']) for h in ['short','medium','long']}))
sys.path.insert(0,str(parent/'package/scripts'));spec=importlib.util.spec_from_file_location('research_store',parent/'package/scripts/research_store.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
expected=m.publication_snapshot(root);put('baseline-before-publication.json',expected)
saved=m.publish(root,'aapl',review,files,expected,'bounded-baseline-q2',complete=True)
put('baseline-publication.json',saved);before=m.discover(root,'latest',review['cutoff']);put('baseline-discovery.json',before);assert not before['gaps'] and all(d['action']=='no_analysis_update' for d in before['decisions']),before
before_hash=hashes();put('arrival-before.json',before_hash)
for ref in [base+'/data/2024Q3.json',base+'/data/sources/2024Q3.json']:
 p=root/ref;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(parent/ref,p)
assert all(hashlib.sha256((root/p).read_bytes()).hexdigest()==h for p,h in before_hash.items())
put('arrival-added.json',{'recorded_at':datetime.now(timezone.utc).isoformat(),'new_files':{p:h for p,h in hashes().items() if p not in before_hash},'preexisting_baseline_unchanged':True,'meaning':'controlled real-original-source arrival in historical isolated fixture, not newly published 2026 filing'})
put('arrival-discovery.json',m.discover(root,'latest',review['cutoff']))
print('Separate scope created; legitimate adopted Q2 complete baseline, zero initial pending work, then real Q3 originals added; main root untouched.')
