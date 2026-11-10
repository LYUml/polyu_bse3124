"""Proposed orthogonal ceiling routes, all 92 lamps; distributed-load voltage drop."""
import csv,json,math
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/"data"
I=json.loads((D/"lighting_route_design_inputs.json").read_text())
devices=list(csv.DictReader((D/"devices.csv").open(encoding="utf8")))
DB=tuple(I["DB_lighting_xy_mm"])
portals={"LC-A":[(73550,31488.1)],"LC-B":[(73950,31488.1)],"LC-C":[(74350,31488.1)],
 "LC-E":[(71000,31488.1),(71000,32095.584),(70525.932,32095.584),(71000,32095.584)],
 "LC-F":[(73000,24800),(76000,24800),(76000,25400),(75215,25400)],"LC-G":[(73000,18700),(75600,18700),(75600,18000),(75215,18000)]}
segments=[];results=[]
for cid in ["LC-"+c for c in "ABCDEFG"]:
 lamps={r["device_id"]:r for r in devices if r["circuit_id"]==cid and float(r["power_W"] or 0)>0};power=sum(float(r["power_W"]) for r in lamps.values())
 current=power/I["voltage_V"]/I["PF"];remaining=power;previous=DB;visited=[];local=[];drop=0;length=0
 def segment(end,node="WAYPOINT"):
  global previous,remaining,drop,length
  if math.dist(previous,end)<.001:return
  assert abs(previous[0]-end[0])<.001 or abs(previous[1]-end[1])<.001
  L=math.dist(previous,end)/1000;A=remaining/I["voltage_V"]/I["PF"]
  local.append(dict(circuit_id=cid,segment=len(local)+1,to_node=node,x1=previous[0],y1=previous[1],x2=end[0],y2=end[1],plan_length_m=round(L,9),downstream_W=remaining,current_A=round(A,9),drop_V=round(I["table_drop_mV_A_m"]*A*L/1000,9)))
  drop+=I["table_drop_mV_A_m"]*A*L/1000;length+=L;previous=end
 if cid=="LC-D":
  old=list(csv.DictReader((D/"pantry_route_basis.csv").open(encoding="utf8")))
  for r in old:
   assert math.dist(previous,(float(r["x1"]),float(r["y1"])))<.001
   end=(float(r["x2"]),float(r["y2"]));node=r["to_node"]
   if node in lamps and math.dist(end,(float(lamps[node]["x"]),float(lamps[node]["y"])))>=.001:node="WAYPOINT"
   segment(end,node)
   if r["to_node"]=="ENTRY-Y":
    segment((70425.932,32095.584));segment(end)
   if node in lamps and node not in visited and math.dist(end,(float(lamps[node]["x"]),float(lamps[node]["y"])))<.001:
    visited.append(node);remaining-=float(lamps[node]["power_W"])
 else:
  for p in portals[cid]:segment(p)
  by_y={}
  for name,r in lamps.items():by_y.setdefault(float(r["y"]),[]).append((float(r["x"]),name))
  # Start at the nearest row and snake monotonically through the zone.
  yy=sorted(by_y,reverse=cid not in ["LC-E","LC-F"])
  for y in yy:
   row=sorted(by_y[y]);row=row if abs(row[0][0]-previous[0])<=abs(row[-1][0]-previous[0]) else row[::-1]
   for x,name in row:
    segment((previous[0],y));segment((x,y),name)
    if local and local[-1]["to_node"]=="WAYPOINT":local[-1]["to_node"]=name
    assert name not in visited;visited.append(name);remaining-=float(lamps[name]["power_W"])
 assert set(visited)==set(lamps) and abs(remaining)<.001
 Iz=I["methodB_It_A"]*I["Ca"]*I["Cg"];design_length=length+I["common_vertical_allowance_m"]
 total_drop=drop+I["table_drop_mV_A_m"]*current*I["common_vertical_allowance_m"]/1000
 Rloop=2*I["R20_2p5_ohm_km"]*(1+I["copper_temp_coefficient_per_C"]*(I["operating_C"]-I["R_reference_C"]))*design_length/1000
 results.append(dict(circuit_id=cid,lamps=len(lamps),power_W=power,Ib_A=round(current,6),candidate_In_A=I["candidate_B_RCBO_A"],candidate_line_N_CPC_mm2=2.5,Iz_A=round(Iz,6),plan_route_m=round(length,6),vertical_allowance_m=I["common_vertical_allowance_m"],design_route_m=round(design_length,6),distributed_drop_V=round(total_drop,6),branch_budget_V=I["branch_drop_budget_V"],capacity_pass=current<=I["candidate_B_RCBO_A"]<=Iz,branch_drop_pass=total_drop<=I["branch_drop_budget_V"],R1_R2_70C_ohm=round(Rloop,6),max_external_loop_Ze_at_DB_ohm=round(I["reference_B10_Zs_limit_ohm"]-Rloop,6),CPC_permissible_I2t_A2s=(I["PVC_CPC_k"]*2.5)**2,status="Adopted route; see fault_protection_summary.json and all_circuits_voltage_drop.csv; stated installation conditions apply"))
 segments+=local
for filename,rows in [("lighting_route_segments.csv",segments),("lighting_route_results.csv",results)]:
 with (D/filename).open("w",encoding="utf8",newline="") as f:
  w=csv.DictWriter(f,fieldnames=rows[0],lineterminator="\n");w.writeheader();w.writerows(rows)
assert sum(r["lamps"] for r in results)==92
assert all(r["capacity_pass"] and r["branch_drop_pass"] for r in results)
print(json.dumps(results))
