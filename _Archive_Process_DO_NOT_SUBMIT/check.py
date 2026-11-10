from pathlib import Path
import csv,json,math,hashlib,shutil,subprocess,sys
R=Path(__file__).resolve().parent
B=R.parents[1]
S=B/'05_Calculations/schematic_revision_v05'
D=S/'data'
read=lambda n:json.loads((D/n).read_text(encoding='utf8'))
rows=lambda n:list(csv.DictReader((D/n).open(encoding='utf-8-sig')))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
devices=rows('devices.csv');circuits=rows('circuits.csv')
ids=[x['device_id'] for x in devices]
members=[v for c in circuits for v in c['device_ids'].split(';')]
assert len(ids)==112 and len(set(ids))==112 and sorted(ids)==sorted(members)
lights=[c for c in circuits if c['circuit_id'].startswith('LC-')]
assert sum(float(c['connected_load_W']) for c in lights)==2256
phase={}
for ph in ['L1','L2','L3']:
 cs=[c for c in circuits if c['phase']==ph]
 light=sum(float(c['connected_load_W'])/198 for c in cs if c['circuit_id'].startswith('LC-'))
 sockets=[float(c['Ib_A']) for c in cs if c['circuit_id'].startswith('P') and c['circuit_id']!='P7']
 fixed=sum(float(c['connected_load_W'])/220 for c in cs if c['circuit_id']=='P7')
 phase[ph]=.9*light+.5*sum(sockets)+.5*max(sockets)+fixed
assert abs(max(phase.values())-48.6)<1e-8
Sbuilding=1.1*(10*(309+309+410)*.16+(1000/3.51685)*1.85/.9+5*40)
q=read('system_design_results_rev03.json')
I=read('system_design_inputs_rev03.json')
up=5*164.48*1.1*1000/(math.sqrt(3)*380)*1.1*.000021*28*1.1+.05
feed=2/math.sqrt(3)*1.1/1000*31.5119*48.6
maxbranch=max([float(x['distributed_drop_V']) for x in rows('lighting_route_results.csv')]+[float(x['worst_branch_drop_V']) for x in rows('power_route_results.csv')])
assert abs((up+feed+maxbranch)/2.2-q['max_total_design_percent'])<1e-7
faults=rows('fault_protection_results.csv')
for x in faults:
 z=q['Ze_at_DB_upper_ohm']+float(x['Zloop_70C_bound_ohm'])
 assert abs(z-float(x['Zs_design_ohm']))<1e-6
 assert 209/z>5*float(x['In_A'])
 assert float(x['required_max_I2t'])<=(115*float(x['CPC_mm2']))**2
 # This verifies specified energy limits, not measured manufacturer performance.
baseline=json.loads((S/'baseline_hashes.json').read_text())
hashes=[{'path':k,'matches':sha(B/k)==v} for k,v in baseline.items()]
assert all(x['matches'] for x in hashes)
assert sha(S/'BSE3124_Final_Rev05.pdf')==read('final_manifest.json')['pdf_sha256']
out={'review_target':str(S),'device_records':len(ids),'circuit_count':len(circuits),'lighting_W':2256,'phase_demand_A':phase,'building_kVA':Sbuilding,'feeder_Iz_A':99*.87*.86,'distribution_percent':(up+feed)/2.2,'max_total_design_percent':(up+feed+maxbranch)/2.2,'fault_rows_arithmetic_checked':len(faults),'energy_check_scope':'Requirement bounds only; not proof of selected RCBO total clearing energy','source_hashes':hashes,'LPD_W_m2':{r['zone']:float(r['power_W'])/float(r['area_m2']) for r in rows('final_lighting_basis.csv') if r['height_above_workplane_m']=='1.9'}}
# Replay current system calculation on an isolated snapshot.
W=R/'recompute';W.mkdir(exist_ok=True)
shutil.copytree(D,W/'data',dirs_exist_ok=True)
shutil.copy2(S/'system_design_rev03.py',W/'system_design_rev03.py')
p=subprocess.run([sys.executable,str(W/'system_design_rev03.py')],capture_output=True,text=True)
(R/'recompute.log').write_text(p.stdout+p.stderr,encoding='utf8');assert p.returncode==0
for n in ['system_design_results_rev03.json','voltage_drop_rev03.csv','point_fault_bounds_rev03.csv']:
 assert (W/'data'/n).read_bytes()==(D/n).read_bytes(),n
out['system_replay_exact_match']=True
(R/'checks.json').write_text(json.dumps(out,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in out.items() if k!='source_hashes'},indent=2))
