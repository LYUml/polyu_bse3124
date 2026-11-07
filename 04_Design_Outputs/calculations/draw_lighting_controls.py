"""Add seven passive local switches and synchronize controlled ceiling routes."""
import csv,json
from pathlib import Path
import win32com.client,pythoncom,pywintypes
from win32com.client import VARIANT
R=Path(__file__).resolve().parents[2];data=R/"04_Design_Outputs/data"
D=win32com.client.GetActiveObject("AutoCAD.Application").ActiveDocument
assert Path(D.FullName).resolve()==(R/"04_Design_Outputs/cad/assignment_working_v02.dwg").resolve()
try:D.Layers.Item("E-LIGHT-CONTROLS")
except pywintypes.com_error:pass
else:raise RuntimeError("Controls already drawn; inspect before rerun")
l=D.Layers.Add("E-LIGHT-CONTROLS");l.Color=6
pt=lambda x,y:VARIANT(pythoncom.VT_ARRAY|pythoncom.VT_R8,[float(x),float(y),0.])
controls=list(csv.DictReader((data/"lighting_controls.csv").open()))
segments=list(csv.DictReader((data/"lighting_route_segments.csv").open()));maps=json.loads((data/"lighting_route_cad_map.json").read_text());out=[]
for r in controls:
 cid=r["circuit_id"];ss=[s for s in segments if s["circuit_id"]==cid]
 points=[(float(ss[0]["x1"]),float(ss[0]["y1"]))]+[(float(s["x2"]),float(s["y2"])) for s in ss]
 x,y=float(r["x_mm"]),float(r["y_mm"])
 assert any(abs(a-x)<.001 and abs(b-y)<.001 for a,b in points),(cid,"switch not on route")
 e=D.HandleToObject(maps["route_handles"][cid]);e.Coordinates=VARIANT(pythoncom.VT_ARRAY|pythoncom.VT_R8,[v for p in points for v in p])
 handles=[]
 e=D.ModelSpace.AddCircle(pt(x,y),80);e.Layer=l.Name;handles.append(e.Handle)
 e=D.ModelSpace.AddLine(pt(x,y),pt(x+100,y+130));e.Layer=l.Name;handles.append(e.Handle)
 tx=x-100;ty=y+320
 if cid=="LC-D":tx=x-900;ty=y-150
 if cid=="LC-E":tx=x+180;ty=y-150
 if cid in ["LC-F","LC-G"]:tx=x-900;ty=y+200
 e=D.ModelSpace.AddMText(pt(tx,ty),800,r["control_id"]);e.Height=140;e.Layer=l.Name;handles.append(e.Handle)
 out.append(dict(control_id=r["control_id"],circuit_id=cid,handles=handles))
D.Save()
with (data/"circuits.csv").open(encoding="utf8") as f:r=csv.DictReader(f);fields=r.fieldnames;cir=list(r)
results={r["circuit_id"]:r for r in csv.DictReader((data/"lighting_route_results.csv").open())}
for r in cir:
 if r["circuit_id"] in results:
  rr=results[r["circuit_id"]];r["length_m"]=rr["design_route_m"];r["source_or_assumption"]="ADOPTED COURSE DESIGN: local20AX/LED600W minimum control on circuit;5m vertical allowance including switch down/up; B10 TypeA30mA RCBO;2.5 L/N/CPC; lighting_route_results.csv and fault_design_conditions.json"
with (data/"circuits.csv").open("w",encoding="utf8",newline="") as f:w=csv.DictWriter(f,fieldnames=fields,lineterminator="\n");w.writeheader();w.writerows(cir)
(data/"lighting_control_cad_map.json").write_text(json.dumps(dict(drawing=D.FullName,controls=out,saved=bool(D.Saved),scope="seven passive switches; no power demand added; routes explicitly visit each switch plan point and include5m vertical allowance"),indent=2))
print(json.dumps(dict(controls=len(out),saved=bool(D.Saved))))
