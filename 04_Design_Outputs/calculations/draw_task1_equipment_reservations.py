"""Native AutoCAD: additive, versioned Task 1 planning geometry; no original edits."""
import csv,json,math
from pathlib import Path
import win32com.client,pythoncom
from win32com.client import VARIANT
root=Path(__file__).resolve().parents[2]
source=root/"04_Design_Outputs/cad/reopen_check.dwg"
output=root/"04_Design_Outputs/cad/assignment_working_v02.dwg"
app=win32com.client.GetActiveObject("AutoCAD.Application");doc=app.ActiveDocument
assert Path(doc.FullName).resolve()==source.resolve(), "Unexpected active document"
assert doc.Saved, "Unsaved document: preserve before proceeding"
assert not output.exists(), "Do not overwrite an existing version"
doc.SaveAs(str(output))
assert Path(doc.FullName).resolve()==output.resolve()
rows=list(csv.DictReader((root/"04_Design_Outputs/data/task1_equipment_reservations.csv").open()))
handles=[]
def point(x,y):return VARIANT(pythoncom.VT_ARRAY|pythoncom.VT_R8,[x,y,0.0])
def layer(name,color):
 try:l=doc.Layers.Item(name)
 except Exception:l=doc.Layers.Add(name)
 l.Color=color
layer("E-T1-EQUIPMENT-RESERVE",1);layer("E-T1-CLEARANCE",3);layer("E-T1-ACCESS",5);layer("E-T1-NOTES",7)
def rect(x0,y0,x1,y1,layer):
 e=doc.ModelSpace.AddLightWeightPolyline(VARIANT(pythoncom.VT_ARRAY|pythoncom.VT_R8,[x0,y0,x1,y0,x1,y1,x0,y1]));e.Closed=True;e.Layer=layer;handles.append(e.Handle);return e

def text(s,x,y,width=3200,height=170):
 e=doc.ModelSpace.AddMText(point(x,y),width,s);e.Height=height;e.Layer="E-T1-NOTES";handles.append(e.Handle)
checks=[]
for r in rows:
 x0,y0,x1,y1=[float(r[k]) for k in ["xmin_mm","ymin_mm","xmax_mm","ymax_mm"]]
 w,e,s,n=[float(r[k]) for k in ["clear_west_mm","clear_east_mm","clear_south_mm","clear_north_mm"]]
 envelope=[x0-w,y0-s,x1+e,y1+n]
 assert envelope[0]>=9000 and envelope[1]>=16105.584 and envelope[2]<=21430 and envelope[3]<=21555.584
 rect(x0,y0,x1,y1,"E-T1-EQUIPMENT-RESERVE");rect(*envelope,"E-T1-CLEARANCE")
 text(r["id"]+"\\P"+str(int(x1-x0))+"x"+str(int(y1-y0))+" RESERVED",x0+100,y1-100,width=x1-x0-200,height=170)
 checks.append(dict(id=r["id"],clearance_envelope_mm=envelope,inside_room=True,basis=r["basis"]))
# Independent 3000 mm external equipment access openings proposed, not surveyed.
for name,x0,x1 in [("HV",9500,13500),("TX-A",14300,17300),("TX-B",18000,21000)]:
 rect(x0,13105.584,x1,16105.584,"E-T1-ACCESS")
 text(name+" ACCESS RESERVE\\P"+str(x1-x0)+" mm opening",x0+100,14205.584,width=x1-x0-200)
text("SOUTH EXTERNAL ACCESS / DELIVERY APRON ASSUMED\\P3000 mm clear route; unloading distance <=20 m to be verified",9500,12805.584,width=11500)
text("GREEN: REQUIRED CLEARANCE ENVELOPES / RED: ASSUMED EQUIPMENT RESERVATIONS\\PNOT MANUFACTURER FOOTPRINTS. MATCH ACTUAL CLP EQUIPMENT BEFORE CONSTRUCTION.",9500,26555.584,width=11500,height=190)
text("LV TERMINALS FACE NORTH TO CUSTOMER SWITCHROOM\\P2h FRR separation; seal bus/cable penetrations",14300,21455.584,width=6500,height=150)
# Adjacent LV room independent entry, clear of six cabinet envelopes.
rect(6000,21755.584,9000,24755.584,"E-T1-ACCESS")
text("LV ACCESS\\P3000 mm\\Passumed",6200,24155.584,width=2600)
# Preserve superseded schematic labels on a hidden history layer.
layer("E-T1-SUPERSEDED",7)
for handle in ["762A","762B","762C","762D"]:
 entity=doc.HandleToObject(handle)
 assert entity.Layer=="E-TRIAL-EQUIP"
 entity.Layer="E-T1-SUPERSEDED"
doc.Layers.Item("E-T1-SUPERSEDED").LayerOn=False
entity=doc.HandleToObject("77D2")
entity.InsertionPoint=point(9500,16805.584)
assert Path(doc.FullName).resolve()==output.resolve()
doc.Save()
report=dict(drawing=str(output),handles=handles,equipment_checks=checks,
 limitations=["Reservations are explicit design assumptions, not selected equipment dimensions","External access route and opening works require site confirmation","Overlapping clearance zones require coordinated operating and replacement procedures","Door leaves, wall openings, fire-rated construction, ventilation and trenches remain to detail"])
(root/"04_Design_Outputs/data/task1_equipment_reservation_cad.json").write_text(json.dumps(report,indent=2),encoding="utf8")
print(json.dumps(report))
