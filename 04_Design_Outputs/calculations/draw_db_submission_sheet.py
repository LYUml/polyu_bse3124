"""Editable A3 DB schematic: independent phase/neutral/PE paths from common schedule."""
import csv,json
from pathlib import Path
import win32com.client,pythoncom,pywintypes
from win32com.client import VARIANT
R=Path(__file__).resolve().parents[2];data=R/"04_Design_Outputs/data"
D=win32com.client.GetActiveObject("AutoCAD.Application").ActiveDocument
assert Path(D.FullName).resolve()==(R/"04_Design_Outputs/cad/assignment_working_v02.dwg").resolve()
name="TASK2-DB-SCHEMATIC"
try:D.Layouts.Item(name)
except pywintypes.com_error:pass
else:raise RuntimeError("Submission schematic already exists; inspect before replacing")
L=D.Layouts.Add(name);L.CopyFrom(D.Layouts.Item("TASK1-ROOM-REVIEW"));D.ActiveLayout=L
try:layer=D.Layers.Item("E-DB-SUBMISSION")
except:layer=D.Layers.Add("E-DB-SUBMISSION")
layer.Color=7
P=D.PaperSpace;handles=[];rowmap=[]
pt=lambda x,y:VARIANT(pythoncom.VT_ARRAY|pythoncom.VT_R8,[float(x),float(y),0.])
def line(x1,y1,x2,y2):
 e=P.AddLine(pt(x1,y1),pt(x2,y2));e.Layer=layer.Name;handles.append(e.Handle);return e

def box(x,y,w,h):
 e=P.AddLightWeightPolyline(VARIANT(pythoncom.VT_ARRAY|pythoncom.VT_R8,[x,y,x+w,y,x+w,y+h,x,y+h]));e.Closed=True;e.Layer=layer.Name;handles.append(e.Handle)

def text(s,x,y,w=270,h=2.5):
 e=P.AddMText(pt(x,y),w,s);e.Height=h;e.StyleName="T1-Arial";e.Layer=layer.Name;handles.append(e.Handle)

def dot(x,y):
 e=P.AddCircle(pt(x,y),.55);e.Layer=layer.Name;handles.append(e.Handle)

def circle(x,y,r):
 e=P.AddCircle(pt(x,y),r);e.Layer=layer.Name;handles.append(e.Handle)
text("TASK 2 | OFFICE 1 DISTRIBUTION BOARD DB-O1",12,286,395,4)
text("100A TPN + N/PE | 15 OUTGOING CIRCUITS | 7 LIGHTING / 8 POWER | SCHEMATIC - NOT TO SCALE",12,278,395,2.7)
box(10,264,37,9);text("MS-O1 C63 4P",12,271,35,2.6)
box(10,245,37,10);text("100A4P ISO",59,253,65,2.4)
for x in [14,20,26,40]:
 line(x,264,x,255);line(x,255,x,252);line(x,248,x,245);line(x,248,x+1.6,251)
 e=line(13,250,42,250);e.Linetype="DASHED";e.LinetypeScale=.2
text("4C35 PVC Cu + CPC16 |31.512m incl.3m allowance",59,267,240,2.5)
text("Source Ze0.20ohm /PFC<=6kA assumed; main/RCBO Icn10kA. See Task3 for conditions and I2t limits.",125,259,280,2.3)
text("Landlord emergency/exit systems: independent essential supply assumed; electrically separate from this normal DB.",250,249,155,2.2)
for x,label in [(14,"L1"),(20,"L2"),(26,"L3"),(40,"N"),(52,"PE")]:
 line(x,245 if label!="PE" else 273,x,44);text(label,x-2,242,10,2)
line(52,44,52,39)
for yy,w in [(39,8),(37.5,5),(36,2)]:line(52-w/2,yy,52+w/2,yy)
rows=list(csv.DictReader((data/"circuits.csv").open()))
lamps={r["circuit_id"]:r for r in csv.DictReader((data/"lighting_route_results.csv").open())}
for index,r in enumerate(rows):
 y=230-index*12.5;cid=r["circuit_id"];phase=r["phase"];xp={"L1":14,"L2":20,"L3":26}[phase]
 # Crossings are not junctions. Only own-bus connection has a dot.
 line(xp,y,70,y);dot(xp,y)
 line(40,y-3,70,y-3);dot(40,y-3)
 line(52,y-6,120,y-6);dot(52,y-6)
 box(70,y-4,34,8)
 for yy in [y,y-3]:
  line(70,yy,76,yy);line(76,yy,80,yy+1.5);line(82,yy,104,yy)
 circle(94,y-1.5,2.6)
 link=line(78,y+1.3,78,y-1.7);link.Linetype="DASHED";link.LinetypeScale=.2
 text("B"+r["MCB_A"],83,y+3.4,10,1.8)
 if cid.startswith("LC-"):
  line(104,y,108,y);line(108,y,112,y+1.3);line(114,y,120,y)
  text("S-"+cid[-1],106,y+3.8,12,1.7)
 else:line(104,y,120,y)
 line(104,y-3,120,y-3)
 for yy,label in [(y,"L"),(y-3,"N"),(y-6,"PE")]:text(label,121,yy+.8,6,1.5)
 if cid in lamps:
  count=lamps[cid]["lamps"];description=f"{count} lamps +S-{cid[-1]} /{r['connected_load_W']}W"
  topology="LIGHTING RADIAL"
 else:
  description=r["device_ids"].replace(";",", ")+" /13A FUSED POINTS"
  topology="A1 RING: L/N/PE BOTH ENDS AT DB" if cid in ["P1","P2","P3","P4"] else "DEDICATED RADIAL"
 text(f"{cid} [{phase}] | {description} | B{r['MCB_A']} /TYPE A30mA1P+N RCBO",132,y+3.0,275,2.45)
 text(f"L/N/PE {r['cable_mm2']}/{r['cable_mm2']}/{r['cable_mm2']}mm2 | L={float(r['length_m']):.3f}m | {topology}",132,y-1.8,275,2.25)
 rowmap.append(dict(circuit_id=cid,phase=phase,protective_A=r["MCB_A"],cable_mm2=r["cable_mm2"],length_m=r["length_m"],paper_y=y))
text("SYMBOLS: box = linked L+N RCBO; circle = residual sensing; dots = junctions; crossings without dots are not connected. PE bypasses all switches.",12,31,395,2.2)
text("Each RCBO load neutral is dedicated. Ring L/N/CPC ends return to the same circuit terminals; no mixed neutrals. All local power spurs:13A fuse +4mm2 L/N/CPC,0.5m assumed.",12,23,395,2.2)
text("S-A/B/C: separate enclosures for different phases. All manual controls20AX/LED>=600W minimum; local switching and RCBO inrush performance must meet adopted design specification.",12,15,395,2.2)
D.Regen(1);D.Save()
output=R/"04_Design_Outputs/pdf/office_DB_submission_v01.pdf";assert not output.exists()
print(D.Plot.PlotToFile(str(output),"DWG To PDF.pc3"))
(data/"db_submission_sheet_map.json").write_text(json.dumps(dict(drawing=D.FullName,layout=name,circuit_rows=rowmap,handles=handles,saved=bool(D.Saved),symbol_scope="functional schematic with explicitL/N/PE paths; no phase buses are joined; only own-bus dots create junctions"),indent=2))
