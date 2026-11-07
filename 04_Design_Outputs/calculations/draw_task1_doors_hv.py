"""Course proposal: door openings and segregated HV trench centre-lines."""
import json,math
from pathlib import Path
import win32com.client,pythoncom,pywintypes
from win32com.client import VARIANT
R=Path(__file__).resolve().parents[2]
d=win32com.client.GetActiveObject("AutoCAD.Application").ActiveDocument
assert Path(d.FullName).resolve()==(R/"04_Design_Outputs/cad/assignment_working_v02.dwg").resolve()
name="E-T1-DOORS-HV"
try:d.Layers.Item(name)
except pywintypes.com_error:pass
else:raise RuntimeError("Layer already exists: inspect before rerun")
l=d.Layers.Add(name);l.Color=4
h=[]
def pt(x,y):return VARIANT(pythoncom.VT_ARRAY|pythoncom.VT_R8,[x,y,0.])
def line(a,b):
 e=d.ModelSpace.AddLine(pt(*a),pt(*b));e.Layer=name;h.append(e.Handle)
def poly(points):
 e=d.ModelSpace.AddLightWeightPolyline(VARIANT(pythoncom.VT_ARRAY|pythoncom.VT_R8,[v for p in points for v in p]));e.Layer=name;h.append(e.Handle)
def note(s,x,y,w=12000):
 e=d.ModelSpace.AddMText(pt(x,y),w,s);e.Height=160;e.Layer=name;h.append(e.Handle)
# Replace only our trial single-line room boundaries; architectural drawing is retained.
for handle in ["75C2","75CB"]:
 e=d.HandleToObject(handle);assert e.Layer=="E-TRIAL-ROOM";e.Layer="E-T1-SUPERSEDED"
y=16105.584;n=21555.584;top=25055.584
for a,b in [((9000,y),(9500,y)),((13500,y),(14300,y)),((17300,y),(18000,y)),((21000,y),(21430,y)),((9000,y),(9000,n)),((21430,y),(21430,top)),((9000,n),(21430,n)),((9000,top),(21430,top)),((9000,n),(9000,21755.584)),((9000,24755.584),(9000,top))]:line(a,b)
doors=[]
for id,x0,x1 in [("D-HV",9500,13500),("D-TXA",14300,17300),("D-TXB",18000,21000)]:
 radius=(x1-x0)/2
 # Open 90-degree leaves, with full 180-degree outward sweep arcs.
 line((x0,y),(x0,y-radius));line((x1,y),(x1,y-radius))
 for x in [x0,x1]:
  e=d.ModelSpace.AddArc(pt(x,y),radius,math.pi,2*math.pi);e.Layer=name;h.append(e.Handle)
 doors.append(dict(id=id,opening_width_mm=x1-x0,height_assumed_mm=2800,swing_degrees=180,
  basis="Proposed width; COP101 5.6.1.1/5.6.1.2 reference sizes; actual plant and frame clearance to coordinate"))
# LV independent plant entrance, shown with leaves at 90 degrees.
for yy in [21755.584,24755.584]:
 line((9000,yy),(7500,yy))
 e=d.ModelSpace.AddArc(pt(9000,yy),1500,math.pi/2,3*math.pi/2);e.Layer=name;h.append(e.Handle)
# HV segregated on south side, LV interfaces remain on north side.
routes=[dict(id="HV-ENTRY",width_mm=1000,points=[[11200,y],[11200,18805.584]]),
 dict(id="HV-TRUNK",width_mm=600,points=[[11200,17405.584],[18000,17405.584]]),
 dict(id="HV-TXA",width_mm=600,points=[[14300,17405.584],[14300,19355.584]]),
 dict(id="HV-TXB",width_mm=600,points=[[18000,17405.584],[18000,19355.584]]),
 dict(id="HV-TXA-TERM",width_mm=300,points=[[14300,19355.584],[14700,19355.584]]),
 dict(id="HV-TXB-TERM",width_mm=300,points=[[18000,19355.584],[18400,19355.584]])]
for r in routes:
 poly(r["points"]);r["depth_mm"]=1400;r["source"]="COP101 v16 5.5.1 printed p16 PDF p18; proposed route"
note("CYAN: PROPOSED ROOM WALLS / OUTWARD DOORS / HV TRENCH CENTRE-LINES\\PHV: 1000W AT PANELS; 600W TO TRANSFORMERS; FINAL SECTION 300W; GENERALLY 1400D.\\PHV SOUTH / LV NORTH. COVER ALL TRENCHES; NO CIVIL BEAM SHALL REDUCE CROSS-SECTION.",9500,31955.584)
note("DOORS: WIDTHS ARE PROPOSED CLEAR OPENINGS; 2800H PLANT DOORS ASSUMED.\\P180-DEGREE OUTWARD SWING; LEAVES SHOWN AT 90 DEGREES. SHARED SWING ZONES: OPEN ADJACENT PLANT DOORS SEQUENTIALLY.\\PD-TXA: DESIGNATED PERSONNEL ENTRANCE WITH 700W x 2100H WICKET, PANIC HARDWARE; OTHER EXITS OPENABLE FROM INSIDE.\\PLV ROOM HAS SEPARATE WEST ENTRANCE. ACTUAL FRAMES, FIRE RATING, EXTERNAL ROUTE AND ARCHITECTURAL OPENINGS REQUIRE COORDINATION.",9500,8505.584)
d.Save()
report=dict(drawing=d.FullName,handles=h,doors=doors,HV_trenches=routes,
 limitations=["Single-line proposed partitions: wall thickness not detailed","Architectural walls retained; openings are proposed alteration work","Shared door sweeps require sequential use; unobstructed emergency escape to be checked","HV cable selection and CLP supply entry remain supplier interfaces"])
(R/"04_Design_Outputs/data/task1_doors_hv_cad.json").write_text(json.dumps(report,indent=2),encoding="utf8")
print(json.dumps(dict(saved=bool(d.Saved),new_objects=len(h),doors=doors)))
