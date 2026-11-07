"""Audit shared lighting IDs, circuit allocation and CAD handle maps."""
import csv,json
from pathlib import Path
D=Path(__file__).resolve().parents[1]/'data'
def read(p):
 with (D/p).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
a=[r for r in read('devices.csv') if r['circuit_id'].startswith('LC-')];c=[r for r in read('circuits.csv') if r['circuit_id'].startswith('LC-')]
assert len(a)==len({r['device_id'] for r in a})==92
ids={r['device_id'] for r in a};assigned=[];summary=[]
for r in c:
 listed=r['device_ids'].split(';');actual=[x for x in a if x['circuit_id']==r['circuit_id']];power=sum(float(x['power_W']) for x in actual)
 assert set(listed)=={x['device_id'] for x in actual}
 assert abs(power-float(r['connected_load_W']))<.001
 assigned+=listed;summary.append(dict(circuit=r['circuit_id'],count=len(actual),power_W=power))
assert len(assigned)==len(set(assigned))==92 and set(assigned)==ids
main=read('office_work_cad_map.csv');pantry=read('pantry_11_cad_map.csv');ne=read('northeast_14_cad_map.csv')
mapped=[r['device_id'] for r in main]+[r['sample_device'] for r in pantry]+[r['candidate_device'] for r in ne]
assert len(mapped)==len(set(mapped))==92 and set(mapped)==ids
handles=[h for r in main for h in [r['outer_handle'],r['inner_handle'],r['label_handle']]]+[h for r in pantry for h in r['cad_geometry_handles'].split(';')+[r['cad_label_handle']]]+[h for r in ne for h in [r['outer_handle'],r['inner_handle'],r['label_handle']]]
assert len(handles)==len(set(handles))==276
result=dict(lighting_devices=92,lighting_power_W=sum(float(r['power_W']) for r in a),circuits=summary,mapped_working_entities=276,status='shared tables and handle maps consistent; live handles and print checks separate; controls emergency and protection incomplete')
(D/'lighting_data_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8');print(json.dumps(result))
