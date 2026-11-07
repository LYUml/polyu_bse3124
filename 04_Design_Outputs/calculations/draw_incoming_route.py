"""Native proposed meter-to-DB incoming route on both office plans."""
import json
from pathlib import Path
import win32com.client,pythoncom,pywintypes
from win32com.client import VARIANT
R=Path(__file__).resolve().parents[2];data=R/"04_Design_Outputs/data"
I=json.loads((data/"incoming_design_inputs.json").read_text());Q=json.loads((data/"incoming_cable_results.json").read_text())
D=win32com.client.GetActiveObject("AutoCAD.Application").ActiveDocument
assert Path(D.FullName).resolve()==(R/"04_Design_Outputs/cad/assignment_working_v02.dwg").resolve()
name="E-INCOMING-WORK"
try:D.Layers.Item(name)
except pywintypes.com_error:pass
else:raise RuntimeError("Incoming route already exists; inspect before rerun")
l=D.Layers.Add(name);l.Color=30;maps={}
pt=lambda x,y:VARIANT(pythoncom.VT_ARRAY|pythoncom.VT_R8,[float(x),float(y),0.])
for plan,dy in [("lighting",0),("power",I["power_plan_y_offset_mm"])]:
 points=[[x,y+dy] for x,y in I["route_lighting_xy_mm"]]
 e=D.ModelSpace.AddLightWeightPolyline(VARIANT(pythoncom.VT_ARRAY|pythoncom.VT_R8,[v for p in points for v in p]));e.Layer=name;e.Lineweight=35
 assert abs(e.Length/1000-Q["plan_route_m"])<1e-6;maps[plan]=dict(route_handle=e.Handle)
 x,y=points[0]
 e=D.ModelSpace.AddLightWeightPolyline(VARIANT(pythoncom.VT_ARRAY|pythoncom.VT_R8,[x-300,y,x+300,y,x+300,y-150,x-300,y-150]));e.Layer=name;e.Closed=True;maps[plan]["source_box_handle"]=e.Handle
 e=D.ModelSpace.AddMText(pt(x+400,y-200),3000,"MS-O1 (ASSUMED)\\P63A / 4C35 + CPC16");e.Height=200;e.Layer=name;maps[plan]["source_label_handle"]=e.Handle
incomer=D.HandleToObject("7655");assert "INCOM" in incomer.TextString.upper()
incomer.TextString="WORKING INCOMER: C63 4P / 4C35 PVC Cu + CPC16 / 100A DB / PFC & SELECTIVITY TO VERIFY"
D.Save()
(data/"incoming_route_cad_map.json").write_text(json.dumps(dict(drawing=D.FullName,plans=maps,plan_length_m=Q["plan_route_m"],saved=bool(D.Saved),limitation="Proposed source/cable route, actual board position and penetrations unverified"),indent=2),encoding="utf8")
print(json.dumps(dict(plans=maps,saved=bool(D.Saved))))
