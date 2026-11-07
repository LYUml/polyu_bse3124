"""Synchronize SO03 separation: CAD working copy plus common CSV sources."""
import csv,json
from pathlib import Path
import win32com.client,pythoncom
from win32com.client import VARIANT
R=Path(__file__).resolve().parents[2];data=R/"04_Design_Outputs/data"
def read(name):
 with (data/name).open(encoding="utf-8-sig",newline="") as f:
  reader=csv.DictReader(f);return reader.fieldnames,list(reader)
def write(name,fields,rows):
 with (data/name).open("w",encoding="utf8",newline="") as f:
  w=csv.DictWriter(f,fieldnames=fields,lineterminator="\n");w.writeheader();w.writerows(rows)
fields,circuits=read("circuits.csv");assert not any(r["circuit_id"]=="P8" for r in circuits)
D=win32com.client.GetActiveObject("AutoCAD.Application").ActiveDocument
assert Path(D.FullName).resolve()==(R/"04_Design_Outputs/cad/assignment_working_v02.dwg").resolve()
label=D.HandleToObject("7991");assert "SO03" in label.TextString;label.TextString="SO03:P8"
p6=D.HandleToObject("7670");assert "P6" in p6.TextString
p6.TextString="L3 P6 FB09 / SO01 NON-KITCHEN SOCKETS - PROTECTION TBD"
bus=D.HandleToObject("7656")
pt=lambda x,y:VARIANT(pythoncom.VT_ARRAY|pythoncom.VT_R8,[float(x),float(y),0.])
bus.EndPoint=pt(32500,-32600)
e=D.ModelSpace.AddLine(pt(32500,-32000),pt(35000,-32000));e.Layer="E-DB-CONCEPT";line_handle=e.Handle
e=D.ModelSpace.AddMText(pt(35500,-31900),11500,"PH? P8 SO03 PANTRY SOCKETS / SEPARATE CIRCUIT / PROTECTION TBD");e.Height=230;e.Layer="E-DB-CONCEPT";text_handle=e.Handle
D.Save()
for r in circuits:
 if r["circuit_id"]=="P6":
  r["device_ids"]="FB09;SO01";r["source_or_assumption"]="Non-kitchen meeting area sockets; pantry SO03 separated to P8 under EMSD2025 6E(3)(a); ratings routes and protection pending"
r={k:"" for k in fields};r.update(circuit_id="P8",DB="provisional office DB",phase="TBD",device_ids="SO03",source_or_assumption="Dedicated pantry/kitchen socket circuit; EMSD2025 6E(3)(a) printed54 PDF55; rating cable routing and demand pending; not zero load");circuits.append(r)
write("circuits.csv",fields,circuits)
for name,column in [("devices.csv","circuit_id"),("power_proposal_v5.csv","circuit_candidate"),("power_work_cad_map.csv","circuit")]:
 f,rows=read(name)
 for r in rows:
  if r["device_id"]=="SO03":r[column]="P8"
 write(name,f,rows)
f,rows=read("power_protection_concept.csv")
for r in rows:
 if r["circuit_id"]=="P6":
  r["wall_socket_ids"]="SO01";r["status"]="Non-kitchen meeting area only; SO03 on separate P8; area topology cable load and protection pending"
r={k:"" for k in f};r.update(circuit_id="P8",wall_socket_ids="SO03",candidate_arrangement="separate pantry socket circuit; radial/ring selection after served-area check",proposed_fault_protection="30 mA RCBO candidate",status="EMSD2025 6E(3)(a); rating topology served area cable and demand pending; not zero load");rows.append(r);write("power_protection_concept.csv",f,rows)
report=dict(reason="EMSD2025 6E(3)(a) printed54 PDF55: separate kitchen socket circuit",device="SO03",old_circuit="P6",new_circuit="P8",total_circuits=len(circuits),new_schematic_handles=[line_handle,text_handle],cad_label_handle="7991",cad_saved=bool(D.Saved))
(data/"pantry_circuit_separation.json").write_text(json.dumps(report,indent=2),encoding="utf8");print(json.dumps(report))
