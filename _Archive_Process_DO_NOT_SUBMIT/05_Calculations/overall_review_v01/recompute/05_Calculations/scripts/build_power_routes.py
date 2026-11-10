"""Proposed power topology, served envelopes, ring current split and radial drops."""
import csv,json,math
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[2];D=R/"05_Calculations/data"
I=json.loads((D/"power_route_design_inputs.json").read_text());db=I["DB_xy_mm"];x,y=db
points={r["device_id"]:[float(r["x_mm"]),float(r["y_mm"])] for r in csv.DictReader((D/"power_points.csv").open())}
routes={
"P1":[db,[66000,y],[66000,-21350],points["FB01"],[68000,-23200],points["FB02"],[72000,-23200],[72000,y],db],
"P2":[db,[66000,y],[66000,-26650],points["FB03"],[69100,-26650],points["FB04"],[72000,-26600],[72000,y],db],
"P3":[db,[65000,y],[65000,-30431.7],points["FB05"],[66114.1,-30500],points["FB06"],[73000,-30500],db],
"P4":[db,[73000,-26500],points["FB07"],[79200,-26500],points["FB08"],[79500,-26300],[79500,-24578],[74500,-24578],[74500,y],db],
"P5":[db,[71000,y],[71000,-12782.416],points["SO02"]],
"P6":[db,[70000,y],points["FB09"],[64525.932,-15100],points["SO01"]],
"P7":[db,[70000,y],[70000,-12782.416],points["FS01"]],
"P8":[db,[70000,y],[70000,-12782.416],points["SO03"]]}
limits={"P1":[64525.932,-24000,79808.432,-17889.9],"P2":[64525.932,-28500,79808.432,-24000],"P3":[64525.932,-33272.416,79808.432,-28500],"P4":[72500,-33272.416,79808.432,-20000],"P5":[70525.932,-17789.916345,79808.432,-12782.416345],"P6":[64525.932,-17789.916345,70425.932,-12782.416345],"P8":[64525.932,-17789.916345,70425.932,-12782.416345]}
cir={r["circuit_id"]:r for r in csv.DictReader((D/"circuits.csv").open())}
segments=[];results=[];details={}
for cid,path in routes.items():
 members=cir[cid]["device_ids"].split(";");tap={};L=0;ss=[]
 for a,b in zip(path,path[1:]):
  if math.dist(a,b)<.001:continue
  assert abs(a[0]-b[0])<.001 or abs(a[1]-b[1])<.001
  length=math.dist(a,b)/1000;L+=length
  at=next((name for name in members if math.dist(points[name],b)<.001),"")
  if at:assert at not in tap;tap[at]=L
  ss.append(dict(circuit_id=cid,segment=len(ss)+1,x1=a[0],y1=a[1],x2=b[0],y2=b[1],plan_length_m=round(length,9),to_device=at))
 assert set(tap)==set(members),(cid,tap,members)
 ring=cid in ["P1","P2","P3","P4"]
 ib=len(members)*I["point_FCU_A"]
 spur_drop=I["spur_mV_A_m"]*I["point_FCU_A"]*I["spur_assumed_length_m"]/1000
 if ring:
  ordered=sorted(tap,key=tap.get);positions=[tap[n]+I["ring_vertical_each_end_m"] for n in ordered]
  total=L+2*I["ring_vertical_each_end_m"]
  section_lengths=np.diff([0]+positions+[total]);resistance=section_lengths*I["ring_mV_A_m"]/1000
  G=np.zeros((len(ordered),len(ordered)))
  for j in range(len(ordered)):
   G[j,j]=1/resistance[j]+1/resistance[j+1]
   if j:G[j,j-1]=-1/resistance[j]
   if j+1<len(ordered):G[j,j+1]=-1/resistance[j+1]
  drops=np.linalg.solve(G,np.full(len(ordered),I["point_FCU_A"]))
  potentials=np.r_[0,drops,0];currents=np.diff(potentials)/resistance
  assert abs(abs(currents[0])+abs(currents[-1])-ib)<1e-8
  Iz=I["ring_It_A"]*I["Ca"]*I["ring_Cg"];max_leg=max(abs(currents))
  capacity=Iz>=20 and max_leg<=Iz
  drop=max(drops)+spur_drop;size=I["ring_line_N_CPC_mm2"];In=32;topology="A1 ring + individually13A fused points"
  details[cid]=dict(node_order=ordered,node_plan_chainages_m=tap,ring_total_with_two_vertical_ends_m=total,section_lengths_m=section_lengths.tolist(),section_currents_A=currents.tolist(),node_main_drops_V=drops.tolist(),max_leg_A=float(max_leg),ring_rule="EMSD Table6(1): Iz>=20A per leg; additionally calculated worst leg<=Iz; intact uniform ring, every tap13A fused")
 else:
  total=L+I["radial_vertical_allowance_m"]
  fixed=cid=="P7";size=I["fixed_line_N_CPC_mm2"] if fixed else I["radial_line_N_CPC_mm2"]
  It=I["fixed_It_A"] if fixed else I["radial_It_A"];Cg=I["fixed_Cg"] if fixed else I["radial_Cg"]
  mv=I["fixed_mV_A_m"] if fixed else I["radial_mV_A_m"]
  In=16 if fixed else 32
  Iz=It*I["Ca"]*Cg;capacity=ib<=In<=Iz
  remaining=ib;drop=mv*ib*I["radial_vertical_allowance_m"]/1000
  for r in ss:
   drop+=mv*remaining*r["plan_length_m"]/1000
   if r["to_device"]:remaining-=I["point_FCU_A"]
  assert remaining==0
  drop+=spur_drop;topology="dedicated fixed radial +13A FCU" if fixed else "A2 radial + individually13A fused points"
 area=None;maximum=100 if ring else 50
 if cid in limits:
  x0,y0,x1,y1=limits[cid];area=(x1-x0)*(y1-y0)/1e6
  assert area<=maximum
  for name in members:
   xx,yy=points[name];assert x0-.01<=xx<=x1+.01 and y0-.01<=yy<=y1+.01,(cid,name)
 results.append(dict(circuit_id=cid,topology=topology,Ib_FCU_capacity_A=ib,protective_A=In,line_N_CPC_mm2=size,corrected_Iz_A=round(Iz,6),max_ring_leg_A=round(float(max_leg),6) if ring else "",plan_main_m=round(L,6),main_with_vertical_m=round(total,6),spur_each_assumed_m=I["spur_assumed_length_m"],worst_branch_drop_V=round(float(drop),6),capacity_pass=bool(capacity),branch_drop_pass=bool(drop<=I["branch_drop_budget_V"]),served_envelope_m2=round(area,6) if area else "",standard_area_max_m2=maximum if area else "",served_area_pass=area<=maximum if area else "not applicable",status="Proposed geometry; all point currents are fuse-capacity bounds, not appliance ratings; fault/upstream/control/terminal reviews pending"))
 segments+=ss
for name,rows in [("power_route_segments.csv",segments),("power_route_results.csv",results)]:
 with (D/name).open("w",encoding="utf8",newline="") as f:w=csv.DictWriter(f,fieldnames=rows[0],lineterminator="\n");w.writeheader();w.writerows(rows)
(D/"power_route_topology.json").write_text(json.dumps(dict(routes=routes,served_envelopes_mm=limits,ring_solutions=details,area_basis="Design service envelopes on supplied coordinate system, not surveyed net room areas. Overlap is intentional for interleaved circuits; do not sum as office UFA.",pantry_classification="P6 and P8 both serve source PANTRY; P8 retained as separate circuit by design choice, not required for each outlet."),indent=2))
assert all(r["capacity_pass"] and r["branch_drop_pass"] for r in results)
print(json.dumps(results))
