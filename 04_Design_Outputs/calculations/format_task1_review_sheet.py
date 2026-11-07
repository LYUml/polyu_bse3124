"""Format A3 review: model geometry left, fixed-size paper notes right."""
from pathlib import Path
import json
import win32com.client,pythoncom
from win32com.client import VARIANT
R=Path(__file__).resolve().parents[2]
D=win32com.client.GetActiveObject("AutoCAD.Application").ActiveDocument
assert Path(D.FullName).resolve()==(R/"04_Design_Outputs/cad/assignment_working_v02.dwg").resolve()
L=D.Layouts.Item("TASK1-ROOM-REVIEW");D.ActiveLayout=L
try:n=D.Layers.Item("E-T1-MODEL-NOTES-HIDDEN")
except:n=D.Layers.Add("E-T1-MODEL-NOTES-HIDDEN")
old=["79CD","79CE","79CF","79DE","79DF","77D1","77D2"]
old+=json.loads((R/"04_Design_Outputs/data/task1_doors_hv_cad.json").read_text())["handles"][-2:]
for h in old:D.HandleToObject(h).Layer=n.Name
n.LayerOn=False
D.HandleToObject("7620").TextString="PROPOSED SUBSTATION"
D.HandleToObject("7621").TextString="PROPOSED LV SWITCH ROOM"
for e in list(L.Block):
 if e.ObjectName=="AcDbViewport" and e.Width<400:e.Delete()
try:vpl=D.Layers.Item("E-T1-VPORT-NOPLOT")
except:vpl=D.Layers.Add("E-T1-VPORT-NOPLOT")
vpl.Plottable=False
try:notes=D.Layers.Item("E-T1-PAPER-NOTES")
except:notes=D.Layers.Add("E-T1-PAPER-NOTES")
notes.Color=7
try:style=D.TextStyles.Item("T1-Arial")
except:style=D.TextStyles.Add("T1-Arial")
style.SetFont("Arial",False,False,0,0)
pt=lambda x,y:VARIANT(pythoncom.VT_ARRAY|pythoncom.VT_R8,[float(x),float(y),0.])
V=D.PaperSpace.AddPViewport(pt(132,166),245,190);V.Layer=vpl.Name
V.Display(True);V.Target=pt(14500,19500);V.Direction=VARIANT(pythoncom.VT_ARRAY|pythoncom.VT_R8,[0.,0.,1.]);V.CustomScale=1/75;V.DisplayLocked=True
# Dedicated paper notes can be replaced without touching model geometry.
for e in list(L.Block):
 if e.Layer==notes.Name:e.Delete()
def text(s,x,y,w=140,h=2.7):
 e=D.PaperSpace.AddMText(pt(x,y),w,s);e.Height=h;e.StyleName=style.Name;e.Layer=notes.Name
text("TASK 1 | PROPOSED SUBSTATION AND MAIN LV ROOM",12,285,395,4)
text("Office building: 10 typical floors + ground | COURSE DESIGN REVIEW | All dimensions in mm",12,276,395,2.8)
text("CAPACITY AND EQUIPMENT\\P2 x 1500 kVA proposed; normal load envelope 2672.216 kVA. No full-load N-1.\\PHV: 3000 x 1000 reservation.\\PTX-A/B: 2200 x 1800 each.\\PThese are assumed equipment envelopes, not manufacturer footprints.",270,262)
text("CLEARANCES / BUILDING WORKS\\PHV rear 1000, front 1800, sides 750. TX LV terminals north: 900; other sides 750.\\PProposed 2h FRR partitions; fire-seal penetrations. FFL +0.15 vs external +0.00 assumed.\\PActual structures, wall thickness and equipment dimensions require coordination.",270,210)
text("ACCESS AND DOORS\\PSouth external access assumed. Reserve 3000-wide delivery route; unloading distance <=20m to verify.\\PPlant doors: HV 4000W; TX 3000W each; 2800H assumed. 180-degree outward sweep, shown open 90 degrees.\\PShared sweeps: use adjacent doors sequentially. TX-A designated wicket personnel access. Independent LV entrance west.",270,153)
text("VENTILATION\\P2 low-level 600W x 2000H inlet louvres: 2.4m2 gross x assumed 50% free area = 1.20m2 >=1.12m2. Certified free area >=46.67% required.\\P2 high-level 630-dia fan symbols are conditional references. Actual losses, fan duty and noise to confirm; outlet >=2.5m above street, away from people.",270,85)
text("LV INTERFACES / HV ROUTES\\PLV trench: 1000W x 1100D, four MCTs per interface. A: 8.03+2=10.03m; B: 8.31+2=10.31m (<20m). 2m is assumed total termination/vertical allowance.\\PHV centre-lines: 1000W at panels; 600W branches; final 300W; generally 1400D. Segregate HV/LV. Covered trenches; no beam obstruction.",12,60,245,2.7)
text("DETAIL 1:75 AT A3 | NOT A CONSTRUCTION DRAWING",12,18,245,2.7)
text("Basis: supplied COP215 Rev07; COP101 v16 clauses 4.3, 5.5, 5.6, 6.1-6.7.\\PSee Task1_answer_draft.md and shared data for assumptions/calculations.",270,24,140,2.4)
D.HandleToObject("7621").InsertionPoint=pt(10000,24650)
D.HandleToObject("7621").Height=250
D.HandleToObject("7620").InsertionPoint=pt(9500,17055)
D.HandleToObject("7620").Height=250
L.CanonicalMediaName="ISO_full_bleed_A3_(420.00_x_297.00_MM)"
for lt in ["DASHED","DASHDOT"]:
 try:D.Linetypes.Item(lt)
 except:D.Linetypes.Load(lt,"acadiso.lin")
try:hv=D.Layers.Item("E-T1-HV-TRENCH")
except:hv=D.Layers.Add("E-T1-HV-TRENCH")
hv.Linetype="DASHED"
for handle in json.loads((R/"04_Design_Outputs/data/task1_doors_hv_cad.json").read_text())["handles"][-8:-2]:
 e=D.HandleToObject(handle);e.Layer=hv.Name;e.LinetypeScale=.2
D.Layers.Item("E-T1-CLEARANCE").Linetype="DASHDOT"
for handle in ["79BF","79C2","79C5"]:D.HandleToObject(handle).LinetypeScale=.2
text("LINE KEY: dashed = HV trench; solid = LV route; chain = clearance envelope.",12,70,245,2.6)
L.StyleSheet="monochrome.ctb"
D.SetVariable("BACKGROUNDPLOT",0);D.Regen(1);D.Save()
p=R/"04_Design_Outputs/pdf/task1_room_review_v03.pdf"
assert not p.exists(), "Preserve prior output version"
print(D.Plot.PlotToFile(str(p),"DWG To PDF.pc3"))
