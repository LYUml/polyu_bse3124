"""Reproducible content/integrity checks; visual review is recorded separately."""
from pathlib import Path
import csv,json,hashlib
from pypdf import PdfReader
R=Path(__file__).resolve().parents[2];D=R/'04_Design_Outputs/data';S=R/'04_Design_Outputs/submission'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sources=json.loads((D/'source_hash_gate_20261107.json').read_text())['files']
for r in sources:assert sha(R/r['file'])==r['expected'],r['file']
dev=list(csv.DictReader((D/'devices.csv').open()));lamps=[r for r in dev if r['circuit_id'].startswith('LC-') and float(r['power_W'])>0]
assert len(dev)==112 and len(lamps)==92 and sum(float(r['power_W']) for r in lamps)==2216
fault=list(csv.DictReader((D/'fault_protection_results.csv').open()));assert len(fault)==15
for r in fault:
 assert all(r[k]=='True' for k in ['overload_pass','adiabatic_pass','disconnection_pass','breaking_capacity_pass'])
 if r['circuit_id'] in ['P1','P2','P3','P4']:assert r['I2_A']=='' and 'Table6(1)' in r['overload_basis']
light=list(csv.DictReader((D/'final_lighting_basis.csv').open()));adopted=[r for r in light if r['height_above_workplane_m']=='1.9']
assert len(adopted)==4 and sum(int(r['lamp_count']) for r in adopted)==92 and all(r['mean_target_met']=='True' for r in adopted)
assert next(r for r in light if r['zone']=='South east room' and r['height_above_workplane_m']=='2.2')['mean_target_met']=='False'
pdf=S/'BSE3124_Answer_Sheets_v04.pdf';reader=PdfReader(pdf);assert len(reader.pages)==19
text='\n'.join(p.extract_text() for p in reader.pages)
for token in ['24099296D','24034414D','24093229D','592.9','502.9','447.2','48.909','13A FCU']:
 assert token in text,token
assert 'Ring leg conventional-current bounds' not in text
blank=PdfReader(S/'BSE3124_Template_LaTeX.pdf');original=PdfReader(S/'latex_v04/assets/official-template.pdf');assert len(blank.pages)==5
for a,b in zip(blank.pages,original.pages):assert max(abs(float(x)-float(y)) for x,y in zip(a.mediabox,b.mediabox))<.001
native=json.loads((D/'native_reopen_gate_v02.json').read_text());dwg=R/'04_Design_Outputs/cad/assignment_submission_v02.dwg'
assert native['sha256']==sha(dwg) and native['checked_entity_handles']==940 and native['missing_handles']==0
files=[pdf,S/'BSE3124_Template_LaTeX.pdf',dwg]+sorted((S/'latex_v04/assets').glob('*.pdf'))
manifest=dict(release='Group1 v04',date='2026-11-08',files=[dict(file=str(p.relative_to(R)),sha256=sha(p),bytes=p.stat().st_size) for p in files],pdf_pages=19,original_sources_unchanged=True,source_checks=sources,native_reopen_gate='native_reopen_gate_v02.json',conditional_protection_checks=15,lighting_adopted_mean_checks=4,lighting_height_sensitivity_disclosed=True,template_fidelity='template_fidelity_v04.json',visual_review='All19 final rendered pages visually inspected; reviewed again after layout-sensitive changes',scope='Course design under REVISION_V04 declared conditions; not unrestricted site/product/photometric certification')
(D/'revision_v04_manifest.json').write_text(json.dumps(manifest,indent=2))
print('Verified:19pages,112components,92lamps/2216W,15conditional circuit checks,4lighting means,940native objects,unchanged originals.')
