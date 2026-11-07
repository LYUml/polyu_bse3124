"""Idempotent native label-position corrections from first PDF visual review.

Run only when AutoCAD is idle. Does not move devices or cable routes.
Plot a new PDF version afterwards and visually inspect it separately.
"""
import csv
import json
from pathlib import Path
import pythoncom
import win32com.client
from win32com.client import VARIANT

R = Path(__file__).resolve().parents[2]
DATA = R / "04_Design_Outputs/data"
D = win32com.client.GetActiveObject("AutoCAD.Application").ActiveDocument
assert Path(D.FullName).resolve() == (R / "04_Design_Outputs/cad/assignment_working_v02.dwg").resolve()
assert D.GetVariable("CMDACTIVE") == 0, "Finish active command first"
pt = lambda x, y: VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [float(x), float(y), 0.])
changes = []
rows = list(csv.DictReader((DATA / "power_work_cad_map.csv").open()))
positions = {"SO02": (77100, -13350), "SO03": (64600, -13350),
             "FS01": (66600, -13350), "FB03": (67450, -26800),
             "FB04": (69200, -25900)}
for row in rows:
    if row["device_id"] not in positions:
        continue
    entity = D.HandleToObject(row["label_handle"])
    old = list(entity.InsertionPoint)
    xy = positions[row["device_id"]]
    entity.InsertionPoint = pt(*xy)
    changes.append(dict(id=row["device_id"], handle=row["label_handle"], before=old, after=list(entity.InsertionPoint)))
controls = json.loads((DATA / "lighting_control_cad_map.json").read_text())
for row in controls["controls"]:
    if row["control_id"] not in ["S-A", "S-B", "S-C"]:
        continue
    i = ["S-A", "S-B", "S-C"].index(row["control_id"])
    entity = D.HandleToObject(row["handles"][-1])
    old = list(entity.InsertionPoint)
    entity.InsertionPoint = pt(74650, 32200 - i * 260)
    changes.append(dict(id=row["control_id"], handle=entity.Handle, before=old, after=list(entity.InsertionPoint)))
D.Regen(1)
D.Save()
(DATA / "normal_plan_label_refinement.json").write_text(json.dumps(dict(drawing=D.FullName, changes=changes, saved=bool(D.Saved), visual_review="replot pending"), indent=2))
print(json.dumps(dict(changed_labels=len(changes), saved=bool(D.Saved))))
