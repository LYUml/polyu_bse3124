"""Synchronize native DWG labels with the compact submission legend.

Geometry, device IDs, circuits and loads are unchanged. A/B/C: 22W except
the four 28W devices marked *. D is 22W; E/F/G are all 28W.
"""
import csv
import json
import re
import time
from pathlib import Path

import pywintypes
import win32com.client

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "04_Design_Outputs/data"
EXPECTED = (ROOT / "04_Design_Outputs/cad/assignment_working_v02.dwg").resolve()


def read(fn):
    for _ in range(30):
        try:
            return fn()
        except (pywintypes.com_error, AttributeError) as exc:
            if isinstance(exc, pywintypes.com_error) and exc.hresult not in (-2147418111, -2147417846):
                raise
            time.sleep(.2)
    raise RuntimeError("AutoCAD remained busy")


doc = read(lambda: win32com.client.GetActiveObject("AutoCAD.Application").ActiveDocument)
assert Path(read(lambda: doc.FullName)).resolve() == EXPECTED
records = []
tables = []
for filename, id_field, circuit_field, label_field, handle_field in [
    ("office_work_cad_map.csv", "device_id", "circuit", "cad_label", "label_handle"),
    ("pantry_11_cad_map.csv", "sample_device", "candidate_circuit", "cad_label", "cad_label_handle"),
    ("northeast_14_cad_map.csv", "candidate_device", None, "label", "label_handle"),
]:
    with (DATA / filename).open(encoding="utf8", newline="") as f:
        reader = csv.DictReader(f)
        fields, rows = reader.fieldnames, list(reader)
    for row in rows:
        identifier = row[id_field]
        group = row[circuit_field][-1] if circuit_field else "E"
        number = int(re.search(r"\d+$", identifier)[0])
        star = group in "ABC" and row["power_W"] == "28"
        label = f"{group}{number:02d}" + ("*" if star else "")
        entity = read(lambda: doc.HandleToObject(row[handle_field]))
        before = read(lambda: entity.TextString)
        assert Path(read(lambda: doc.FullName)).resolve() == EXPECTED
        entity.TextString = label
        assert read(lambda: entity.TextString) == label
        records.append(dict(device_id=identifier, circuit="LC-" + group,
                            handle=row[handle_field], before=before, after=label))
        row[label_field] = label
    tables.append((filename, fields, rows))

assert len(records) == 92
assert len({r["device_id"] for r in records}) == 92
assert sum(r["after"].endswith("*") for r in records) == 4
assert Path(read(lambda: doc.FullName)).resolve() == EXPECTED
doc.Save()
assert read(lambda: doc.Saved)
for filename, fields, rows in tables:
    with (DATA / filename).open("w", encoding="utf8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
audit = dict(drawing=str(EXPECTED), label_count=len(records), saved=True,
             convention="A/B/C 22W except starred28W; D22W; E/F/G28W; number retains source device suffix",
             records=records)
(DATA / "luminaire_label_sync_audit.json").write_text(json.dumps(audit, indent=2), encoding="utf8")
print(json.dumps({k: v for k, v in audit.items() if k != "records"}))
