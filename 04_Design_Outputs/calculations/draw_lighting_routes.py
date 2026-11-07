"""Draw seven ceiling route polylines from common data; update circuit schedule."""
import csv,json,math
from pathlib import Path
import win32com.client,pythoncom,pywintypes
from win32com.client import VARIANT
R=Path(__file__).resolve().parents[2];data=R/"04_Design_Outputs/data"
D=win32com.client.GetActiveObject("AutoCAD.Application").ActiveDocument
assert Path(D.FullName).resolve()==(R/"04_Design_Outputs/cad/assignment_working_v02.dwg").resolve()
for c in "ABCDEFG":
 try:D.Layers.Item("E-LIGHT-ROUTE-"+c)
 except pywintypes.com_error:pass
 else:raise RuntimeError("Routes already exist; inspect before rerun")
rows=list(csv.DictReader((data/"lighting_route_segments.csv").open(encoding="utf8")))
results={r["circuit_id"]:r for r in csv.DictReader((data/"lighting_route_results.csv").open(encoding="utf8"))}
handles={}
for i,c in enumerate("ABCDEFG"):
 layer=D.Layers.Add("E-LIGHT-ROUTE-"+c);layer.Color=i+1
 selected=[r for r in rows if r["circuit_id"]=="LC-"+c]
 pts=[(float(selected[0]["x1"]),float(selected[0]["y1"]))]+[(float(r["x2"]),float(r["y2"])) for r in selected]
 for a,b in zip(selected,selected[1:]):assert abs(float(a["x2"])-float(b["x1"]))<.001 and abs(float(a["y2"])-float(b["y1"]))<.001
 e=D.ModelSpace.AddLightWeightPolyline(VARIANT(pythoncom.VT_ARRAY|pythoncom.VT_R8,[v for p in pts for v in p]));e.Layer=layer.Name
 assert abs(e.Length/1000-float(results["LC-"+c]["plan_route_m"]))<.000002
 handles["LC-"+c]=e.Handle
try:D.Layers.Item("E-LCD-ROUTE-DRAFT").LayerOn=False
except pywintypes.com_error:pass
try:layer=D.Layers.Item("E-DB-WORK")
except:layer=D.Layers.Add("E-DB-WORK")
layer.Color=1
pt=lambda x,y:VARIANT(pythoncom.VT_ARRAY|pythoncom.VT_R8,[float(x),float(y),0.])
for y in [31488.1,-17889.9]:
 e=D.ModelSpace.AddLightWeightPolyline(VARIANT(pythoncom.VT_ARRAY|pythoncom.VT_R8,[72700,y,73300,y,73300,y-150,72700,y-150]));e.Closed=True;e.Layer=layer.Name
 e=D.ModelSpace.AddMText(pt(73350,y-170),1800,"DB-O1");e.Height=200;e.Layer=layer.Name
D.Save()
with (data/"circuits.csv").open(encoding="utf8") as f:r=csv.DictReader(f);fields=r.fieldnames;cir=list(r)
for r in cir:
 if r["circuit_id"] in results:
  x=results[r["circuit_id"]];r.update(Ib_A=x["Ib_A"],MCB_A="10",cable_mm2="2.5",length_m=x["design_route_m"],installation_method="Method B single-core PVC Cu;40C;7 lighting circuits bunched; power containment separate",demand_basis="Final circuit 100% lighting; incoming diversity separately",source_or_assumption="WORKING B10 / Type A 30mA RCBO performance specification; L/N/CPC2.5; capacity and branch drop checked from proposed routes; fault/inrush/upstream checks pending")
with (data/"circuits.csv").open("w",encoding="utf8",newline="") as f:w=csv.DictWriter(f,fieldnames=fields,lineterminator="\n");w.writeheader();w.writerows(cir)
(data/"lighting_route_cad_map.json").write_text(json.dumps(dict(drawing=D.FullName,route_handles=handles,db_lighting_xy=[73000,31488.1],db_power_xy=[73000,-17889.9],saved=bool(D.Saved),status="proposed ceiling wiring; penetrations control wiring and final plotting to review"),indent=2),encoding="utf8")
print(json.dumps(dict(route_handles=handles,saved=bool(D.Saved))))
