"""Native power routes and service envelopes from common design data."""
import csv,json
from pathlib import Path
import win32com.client,pythoncom,pywintypes
from win32com.client import VARIANT
R=Path(__file__).resolve().parents[2];data=R/"04_Design_Outputs/data"
D=win32com.client.GetActiveObject("AutoCAD.Application").ActiveDocument
assert Path(D.FullName).resolve()==(R/"04_Design_Outputs/cad/assignment_working_v02.dwg").resolve()
T=json.loads((data/"power_route_topology.json").read_text());Q={r["circuit_id"]:r for r in csv.DictReader((data/"power_route_results.csv").open())}
for cid in T["routes"]:
 try:D.Layers.Item("E-POWER-ROUTE-"+cid)
 except pywintypes.com_error:pass
 else:raise RuntimeError("Power routes already exist; inspect before rerun")
handles={};areas={}
for i,(cid,points) in enumerate(T["routes"].items()):
 l=D.Layers.Add("E-POWER-ROUTE-"+cid);l.Color=(i%6)+1
 e=D.ModelSpace.AddLightWeightPolyline(VARIANT(pythoncom.VT_ARRAY|pythoncom.VT_R8,[v for p in points for v in p]));e.Layer=l.Name
 assert abs(e.Length/1000-float(Q[cid]["plan_main_m"]))<2e-6;handles[cid]=e.Handle
l=D.Layers.Add("E-POWER-SERVICE-ENVELOPES");l.Color=251;l.Plottable=False
for cid,(x0,y0,x1,y1) in T["served_envelopes_mm"].items():
 e=D.ModelSpace.AddLightWeightPolyline(VARIANT(pythoncom.VT_ARRAY|pythoncom.VT_R8,[x0,y0,x1,y0,x1,y1,x0,y1]));e.Closed=True;e.Layer=l.Name
 assert abs(e.Area/1e6-float(Q[cid]["served_envelope_m2"]))<2e-6;areas[cid]=e.Handle
l.LayerOn=False
maps=list(csv.DictReader((data/"power_work_cad_map.csv").open()))
for r in maps:
 e=D.HandleToObject(r["label_handle"]);assert r["device_id"] in e.TextString
 e.TextString=r["device_id"]+":"+r["circuit"]+"\\P13A FCU";e.Height=180
p6=D.HandleToObject("7670");assert "P6" in p6.TextString;p6.TextString="L3 P6 PANTRY FB09 / SO01 - A2 RADIAL / 13A FUSED POINTS"
D.Save()
with (data/"circuits.csv").open() as f:r=csv.DictReader(f);fields=r.fieldnames;rows=list(r)
phase={"P1":"L1","P2":"L1","P3":"L2","P4":"L2","P5":"L1","P6":"L3","P7":"L3","P8":"L3"}
for r in rows:
 cid=r["circuit_id"]
 if cid not in Q:continue
 q=Q[cid];r.update(phase=phase[cid],Ib_A=q["Ib_FCU_capacity_A"],MCB_A=q["protective_A"],cable_mm2=q["line_N_CPC_mm2"],length_m=q["main_with_vertical_m"],installation_method="MethodB PVC Cu40C; banks per power_route_design_inputs.json; individually13A fused points",demand_basis="Upper bound from point FCU capacities, not appliance nameplates; incoming diversity separate",source_or_assumption="WORKING "+q["topology"]+"; routes and served envelopes checked; ring leg capacity rule where applicable; fault upstream and fuse let-through pending")
with (data/"circuits.csv").open("w",encoding="utf8",newline="") as f:w=csv.DictWriter(f,fieldnames=fields,lineterminator="\n");w.writeheader();w.writerows(rows)
# Correct room classification and replace obsolete ring-only concepts.
with (data/"power_protection_concept.csv").open() as f:r=csv.DictReader(f);fields=r.fieldnames;rows=list(r)
for r in rows:
 cid=r["circuit_id"]
 if cid in Q:r["candidate_arrangement"]=Q[cid]["topology"];r["status"]="Working topology and capacity; full fault/terminal/fuse and upstream checks pending"
 if cid=="P6":r["status"]+="; pantry FB09/SO01; previous non-kitchen classification corrected"
with (data/"power_protection_concept.csv").open("w",encoding="utf8",newline="") as f:w=csv.DictWriter(f,fieldnames=fields,lineterminator="\n");w.writeheader();w.writerows(rows)
report=dict(drawing=D.FullName,route_handles=handles,service_envelope_handles=areas,point_FCU_labels=len(maps),native_length_and_area_checks=True,saved=bool(D.Saved),limitations="Proposed containment; penetrations/terminals/FCU product/fault checks pending. All point spurs4mm2 and0.5m assumed, not measured.")
(data/"power_route_cad_map.json").write_text(json.dumps(report,indent=2));print(json.dumps(report))
