"""Recalculate proposed LC-D conductor-route drops; not a final compliance check."""
import csv,json,math
from pathlib import Path
root=Path(__file__).resolve().parents[2];d=root/'04_Design_Outputs/data'
with (d/'LC-D_route_proposal.csv').open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
with (d/'devices.csv').open(encoding='utf-8-sig',newline='') as f:devices={r['device_id']:r for r in csv.DictReader(f) if r['circuit_id']=='LC-D'}
assert len(devices)==11
visited=[];previous=None;load=11;drop=0.;length=0.
for i,r in enumerate(rows):
 a=(float(r['x1']),float(r['y1']));b=(float(r['x2']),float(r['y2']))
 assert previous is None or math.dist(previous,a)<.001,'discontinuous route'
 assert abs(a[0]-b[0])<.001 or abs(a[1]-b[1])<.001,'nonorthogonal segment'
 L=math.dist(a,b)/1000;assert abs(L-float(r['plan_length_m']))<1e-5
 assert int(r['downstream_lamps'])==load
 current=load*22/(220*.9);v=.029*current*L;drop+=v;length+=L
 name=r['to_node'];at_device=name in devices and math.dist(b,(float(devices[name]['x']),float(devices[name]['y'])))<.001
 if at_device:
  assert name not in visited,'duplicate device arrival';visited.append(name);load-=1
 previous=b
assert set(visited)==set(devices) and load==0
result={'route_plan_m':round(length,6),'lamp_count':len(visited),'power_W':242,'voltage_V':220,'PF_assumed':.9,'copper_candidate_mm2':1.5,'table_mV_A_m':29,'plan_distributed_drop_V':round(drop,6),'common_vertical_assumed_m':2,'total_with_vertical_V':round(drop+.029*(242/(220*.9))*2,6),'status':'proposal arithmetic only; installation, control wiring, correction factors, upstream drop and fault checks incomplete'}
(d/'LC-D_route_check.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8');print(json.dumps(result))
