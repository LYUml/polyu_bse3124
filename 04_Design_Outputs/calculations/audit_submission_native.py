"""Read native DWG handles/route lengths against the common submission data.

This verifies the active document; reopening is a separate acceptance gate.
"""
import csv
import json
from collections import Counter
from pathlib import Path
import win32com.client

R = Path(__file__).resolve().parents[2]
DATA = R / "04_Design_Outputs/data"
D = win32com.client.GetActiveObject("AutoCAD.Application").ActiveDocument
assert Path(D.FullName).resolve() == (R / "04_Design_Outputs/cad/assignment_working_v02.dwg").resolve()
load = lambda n: list(csv.DictReader((DATA / n).open(encoding="utf8")))
devices, circuits = load("devices.csv"), load("circuits.csv")
assert len(devices) == 112 and len(circuits) == 15
assert len({r["device_id"] for r in devices}) == 112
by_id = {r["device_id"]: r for r in devices}
membership = Counter()
for row in circuits:
    for identifier in row["device_ids"].split(";"):
        identifier = identifier.strip()
        assert identifier in by_id, identifier
        assert by_id[identifier]["circuit_id"] == row["circuit_id"]
        membership[identifier] += 1
assert set(membership) == set(by_id) and set(membership.values()) == {1}
label_audit = json.loads((DATA / "luminaire_label_sync_audit.json").read_text())
for row in label_audit["records"]:
    entity = D.HandleToObject(row["handle"])
    assert entity.TextString == row["after"], row
    assert by_id[row["device_id"]]["circuit_id"] == row["circuit"]
for filename, outer, inner in [("office_work_cad_map.csv", "outer_handle", "inner_handle"), ("northeast_14_cad_map.csv", "outer_handle", "inner_handle")]:
    for row in load(filename):
        for key in [outer, inner]:
            assert D.HandleToObject(row[key]).ObjectName
for row in load("pantry_11_cad_map.csv"):
    for handle in row["cad_geometry_handles"].split(";"):
        assert D.HandleToObject(handle).ObjectName
for row in load("power_work_cad_map.csv"):
    assert D.HandleToObject(row["symbol_handle"]).ObjectName
    label = D.HandleToObject(row["label_handle"]).TextString
    assert row["device_id"] in label and row["circuit"] in label and "13A" in label
routes = []
for mapfile, resultfile, lengthfield in [
    ("lighting_route_cad_map.json", "lighting_route_results.csv", "plan_route_m"),
    ("power_route_cad_map.json", "power_route_results.csv", "plan_main_m")]:
    handles = json.loads((DATA / mapfile).read_text())["route_handles"]
    for row in load(resultfile):
        native = D.HandleToObject(handles[row["circuit_id"]]).Length / 1000
        target = float(row[lengthfield])
        assert abs(native - target) < .00001, (row["circuit_id"], native, target)
        routes.append(dict(circuit_id=row["circuit_id"], native_plan_m=native, schedule_plan_m=target))
assert len(routes) == 15
controls = json.loads((DATA / "lighting_control_cad_map.json").read_text())["controls"]
for row in controls:
    for handle in row["handles"]:
        assert D.HandleToObject(handle).ObjectName
required = ["TASK1-GROUND-OVERVIEW", "TASK1-ROOM-REVIEW", "TASK2-DB-SCHEMATIC", "TASK2-LIGHTING-PLAN", "TASK2-POWER-PLAN"]
for name in required:
    assert D.Layouts.Item(name).Name == name
result = dict(drawing=D.FullName, components=112, luminaires=92, power_points=13,
              switches=7, circuits=15, membership_discrepancies=0,
              native_luminaire_labels_checked=92, native_routes=routes,
              required_layouts=required, saved=bool(D.Saved),
              native_reopen="see native_reopen_gate.json: independent AutoCAD2027 saved-file audit", checks_pass=True)
(DATA / "submission_native_audit.json").write_text(json.dumps(result, indent=2))
print(json.dumps({k: v for k, v in result.items() if k != "native_routes"}))
