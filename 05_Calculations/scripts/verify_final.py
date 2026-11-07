"""Reproducible content/integrity checks; visual review is recorded separately."""
from pathlib import Path
import csv,json,hashlib
from pypdf import PdfReader
R=Path(__file__).resolve().parents[2];D=R/'05_Calculations/data';S=R/'04_Final_Report'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sources=json.loads((D/'source_hash_gate.json').read_text())['files']
for r in sources:assert sha(R/r['file'])==r['expected'],r['file']
dev=list(csv.DictReader((D/'devices.csv').open()));lamps=[r for r in dev if r['circuit_id'].startswith('LC-') and float(r['power_W'])>0]
assert len(dev)==112 and len(lamps)==92 and sum(float(r['power_W']) for r in lamps)==2256
fault=list(csv.DictReader((D/'fault_protection_results.csv').open()));assert len(fault)==15
for r in fault:
 assert all(r[k]=='True' for k in ['overload_pass','adiabatic_pass','disconnection_pass','breaking_capacity_pass'])
 if r['circuit_id'] in ['P1','P2','P3','P4']:assert r['I2_A']=='' and 'Table6(1)' in r['overload_basis']
light=list(csv.DictReader((D/'final_lighting_basis.csv').open()));adopted=[r for r in light if r['height_above_workplane_m']=='1.9']
assert len(adopted)==4 and sum(int(r['lamp_count']) for r in adopted)==92 and all(r['mean_target_met']=='True' for r in adopted)
assert next(r for r in light if r['zone']=='South east room' and r['height_above_workplane_m']=='2.2')['mean_target_met']=='True'
pdf=S/'BSE3124_Final.pdf';reader=PdfReader(pdf);assert len(reader.pages)==18
text='\n'.join(p.extract_text() for p in reader.pages)
assert 'Task 1' in reader.pages[1].extract_text()
assert 'Task 2' in reader.pages[5].extract_text()
assert 'Task 3' in reader.pages[14].extract_text()
for token in ['24099296D','24034414D','24093229D','592.9','662.6','589.2','49.091','13A FCU']:
 assert token in text,token
assert 'Ring leg conventional-current bounds' not in text
for old in ['2216W', '2216 W', '502.9', '447.2', '48.909', 'PROTECTION TBD', 'Task1_answer_draft']:
 assert old not in text, old
assert sum(1 for r in lamps if float(r['power_W'])==38)==4
circuits={r['circuit_id']:r for r in csv.DictReader((D/'circuits.csv').open())}
for cid,r in circuits.items():
 members=[v for v in dev if v['circuit_id']==cid]
 assert set(r['device_ids'].split(';'))=={v['device_id'] for v in members}
 if cid.startswith('LC-'):
  power=sum(float(v['power_W'] or 0) for v in members)
  assert abs(float(r['connected_load_W'])-power)<1e-6
  assert abs(float(r['Ib_A'])-power/220/.9)<1e-6
for r in csv.DictReader((D/'office_work_cad_map.csv').open()):
 assert float(r['power_W'])==float(next(v['power_W'] for v in lamps if v['device_id']==r['device_id']))
plot=json.loads((D/'native_plot_gate.json').read_text())
assert plot['dwg_sha256']==sha(R/'03_Design_Drawings/BSE3124_Final.dwg')
assert len(plot['layouts'])==6 and all(r['text_characters']>500 for r in plot['layouts'])
native=json.loads((D/'native_final_gate.json').read_text());dwg=R/'03_Design_Drawings/BSE3124_Final.dwg'
assert native['sha256']==sha(dwg) and native['checked_entity_handles']==962 and native['missing_handles']==0
files=[pdf,dwg]+sorted((S/'source/assets').glob('*.pdf'))
manifest=dict(release='Group1 final',date='2026-11-08',files=[dict(file=str(p.relative_to(R)),sha256=sha(p),bytes=p.stat().st_size) for p in files],pdf_pages=18,original_sources_unchanged=True,source_checks=sources,native_reopen_gate='native_final_gate.json',conditional_protection_checks=15,lighting_adopted_mean_checks=4,lighting_height_sensitivity_disclosed=True,template_fidelity='template_fidelity.json',visual_review='All18 final rendered pages visually inspected; reviewed again after layout-sensitive changes',scope='Course design under VALIDATION declared conditions; not unrestricted site/product/photometric certification')
(D/'final_manifest.json').write_text(json.dumps(manifest,indent=2))
print('Verified:18pages,112components,92lamps/2256W,15conditional circuit checks,4lighting means,962native objects,unchanged originals.')
