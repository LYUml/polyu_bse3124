"""Read-only native DWG device verification against shared CAD maps."""
import csv, json
from pathlib import Path
import win32com.client
root=Path(__file__).resolve().parents[2]
doc=win32com.client.GetActiveObject("AutoCAD.Application").ActiveDocument
expected=root/"04_Design_Outputs/cad/reopen_check.dwg"
assert Path(doc.FullName).resolve()==expected.resolve(), "Unexpected active drawing"
checks=[]
for name in ["office_work_cad_map.csv","pantry_11_cad_map.csv","northeast_14_cad_map.csv","power_work_cad_map.csv"]:
 rows=list(csv.DictReader((root/"04_Design_Outputs/data"/name).open(encoding="utf-8-sig")))
 missing=[];count=0
 for row in rows:
  for key,value in row.items():
   if "handle" not in key or not value:continue
   for handle in value.split(";"):
    try:
     entity=doc.HandleToObject(handle)
     assert entity.Handle.upper()==handle.upper()
     count+=1
    except Exception as error:missing.append(dict(device=row.get("device_id",row.get("sample_device")),handle=handle,error=str(error)))
 checks.append(dict(map=name,devices=len(rows),checked_handles=count,missing=missing))
report=dict(path=doc.FullName,saved=bool(doc.Saved),modelspace_entities=doc.ModelSpace.Count,checks=checks,
 limitation="Verifies mapped handles exist in native DWG; does not prove print quality or recover unsaved edits.")
out=root/"04_Design_Outputs/recovery/recovery_verification_20261107.json"
out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf8")
print(json.dumps(report,ensure_ascii=False))
assert not any(c["missing"] for c in checks)
