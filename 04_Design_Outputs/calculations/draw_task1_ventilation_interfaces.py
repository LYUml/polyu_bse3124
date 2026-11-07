"""Add proposed LV trench centre-lines and ventilation reservations to native DWG."""
import json
from pathlib import Path
import win32com.client,pythoncom
from win32com.client import VARIANT
R=Path(__file__).resolve().parents[2];data=R/"04_Design_Outputs/data"
d=win32com.client.GetActiveObject("AutoCAD.Application").ActiveDocument
assert Path(d.FullName).resolve()==(R/"04_Design_Outputs/cad/assignment_working_v02.dwg").resolve()
name="E-T1-INTERFACES"
try:d.Layers.Item(name);raise RuntimeError("Already drawn: inspect existing layer")
except win32com.client.pywintypes.com_error:pass
l=d.Layers.Add(name);l.Color=6
h=[]
def pt(x,y):return VARIANT(pythoncom.VT_ARRAY|pythoncom.VT_R8,[x,y,0.])
def poly(points,closed=False):
 e=d.ModelSpace.AddLightWeightPolyline(VARIANT(pythoncom.VT_ARRAY|pythoncom.VT_R8,[v for p in points for v in p]));e.Closed=closed;e.Layer=name;h.append(e.Handle)
def note(s,x,y,width=12000):
 e=d.ModelSpace.AddMText(pt(x,y),width,s);e.Height=170;e.Layer=name;h.append(e.Handle)
report=json.loads((data/"task1_ventilation_interfaces.json").read_text())
for route in report["LV_interfaces"]:poly(route["points"])
for x in [13900,17650]:poly([[x-300,16005.584],[x+300,16005.584],[x+300,16205.584],[x-300,16205.584]],True)
for x in [15800,19500]:
 e=d.ModelSpace.AddCircle(pt(x,16505.584),315);e.Layer=name;h.append(e.Handle)
note("MAGENTA: PROPOSED LV TRENCH CENTRE-LINES / 1000W x 1100D / COVERED\\PA: 8.03m PLAN + 2m ALLOWANCE = 10.03m; B: 8.31m + 2m = 10.31m (<20m)\\PSEPARATE HV/LV TRENCHES. FIRE-SEAL ROOM PENETRATIONS; COORDINATE STRUCTURE.",9500,29455.584)
note("VENTILATION RESERVATION: 2 INLET LOUVRES, EACH 600W x 2000H\\P2.4m2 GROSS x ASSUMED 50% FREE AREA = 1.20m2 >= 1.12m2 REQUIRED.\\PCERTIFIED FREE AREA >=46.67% REQUIRED. LOW LEVEL INTAKE / HIGH LEVEL EXHAUST.\\P2 x 630 DIA FAN SYMBOLS ARE CONDITIONAL REFERENCES (ACTUAL TRANSFORMER LOSSES / FAN DUTY TBD).\\PEXHAUST OUTLET >=2.5m ABOVE STREET; DIRECT AWAY FROM PERSONNEL. SEE COP101 6.1-6.7.",9500,11605.584)
d.Save()
(data/"task1_interface_cad_map.json").write_text(json.dumps(dict(drawing=d.FullName,handles=h),indent=2),encoding="utf8")
print(json.dumps(dict(handles=h,saved=bool(d.Saved))))
