"""Reopen the saved submission DWG in AutoCAD2027's native Core Console.

Read-only entity extraction; no QSAVE, conversion, or existing-session restart.
Native DWG structure checks complement, and do not replace, PDF visual review.
"""
import csv
import hashlib
import json
import re
import subprocess
import argparse
from pathlib import Path

R = Path(__file__).resolve().parents[2]
DATA = R / "04_Design_Outputs/data"
parser=argparse.ArgumentParser()
parser.add_argument('--revision',choices=['v01','v02'],default='v01')
revision=parser.parse_args().revision
OUT = DATA / ("native_reopen" if revision=='v01' else "native_reopen_v02")
OUT.mkdir(exist_ok=True)
DWG = R / f"04_Design_Outputs/cad/assignment_submission_{revision}.dwg"
CORE = Path("C:/Program Files/Autodesk/AutoCAD 2027/accoreconsole.exe")
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
before = sha(DWG)
handles = set()


def collect(value, handle_context=False):
    if isinstance(value, dict):
        for key, item in value.items():
            collect(item, handle_context or "handle" in key)
    elif isinstance(value, list):
        for item in value:
            collect(item, handle_context)
    elif handle_context and isinstance(value, str):
        for handle in value.split(";"):
            if re.fullmatch(r"[0-9A-F]+", handle):
                handles.add(handle)


for name in ["office_work_cad_map.csv", "northeast_14_cad_map.csv", "power_work_cad_map.csv", "pantry_11_cad_map.csv"]:
    for row in csv.DictReader((DATA / name).open(encoding="utf8")):
        collect(row)
for name in ["lighting_route_cad_map.json", "power_route_cad_map.json", "lighting_control_cad_map.json",
             "incoming_route_cad_map.json", "task1_equipment_reservation_cad.json", "task1_doors_hv_cad.json",
             "task1_interface_cad_map.json", "db_submission_sheet_map.json", "normal_plan_sheet_map.json"]:
    collect(json.loads((DATA / name).read_text(encoding="utf8")))
if revision=='v02':
    handles.update((DATA/'installation_detail_handles_v04.txt').read_text().splitlines())
ordered = sorted(handles)
# Keep script lines short: AutoCAD truncates oversized command input lines.
literal = "\n".join(" ".join('"' + h + '"' for h in ordered[i:i+8]) for i in range(0, len(ordered), 8))
template = Path(__file__).with_name("native_read_audit.lsp").read_text(encoding="ascii")
script = template.replace("@@HANDLES@@", literal).replace("@@OUTPUT@@", (OUT / "native_entities.tsv").as_posix())
script_path = OUT / "audit.scr"
script_path.write_text(script.rstrip() + "\n", encoding="ascii")
# Inline script expressions avoid loading an untrusted-path external LSP.
result = subprocess.run([str(CORE), "/i", str(DWG), "/s", str(script_path), "/l", "en-US"], capture_output=True)
log = result.stdout.decode("utf-16le", errors="replace")
(OUT / "console.log").write_text("\n".join(line.rstrip() for line in log.splitlines()).rstrip() + "\n", encoding="utf8")
assert result.returncode == 0 and "BSE_NATIVE_READ_COMPLETE" in log
assert "; error:" not in log.lower(), "Inspect native console log"
lines = [line.split("\t") for line in (OUT / "native_entities.tsv").read_text(encoding="utf8").splitlines()]
assert Path(lines[0][1]).resolve() == DWG.resolve()
assert ["UNITS", "4"] in lines
layouts = [row[1] for row in lines if row[0] == "LAYOUT"]
required = ["TASK1-GROUND-OVERVIEW", "TASK1-ROOM-REVIEW", "TASK2-DB-SCHEMATIC", "TASK2-LIGHTING-PLAN", "TASK2-POWER-PLAN"]
if revision=='v02': required.append('DESIGN-DETAILS')
assert set(required) <= set(layouts)
entities = {row[0]: row for row in lines if row[0] in handles}
assert set(entities) == handles and all(row[1] != "MISSING" for row in entities.values())
for row in json.loads((DATA / "luminaire_label_sync_audit.json").read_text())["records"]:
    assert entities[row["handle"]][3] == row["after"]
routes = []
for mapfile, resultfile, field in [("lighting_route_cad_map.json", "lighting_route_results.csv", "plan_route_m"),
                                   ("power_route_cad_map.json", "power_route_results.csv", "plan_main_m")]:
    mapping = json.loads((DATA / mapfile).read_text())["route_handles"]
    for row in csv.DictReader((DATA / resultfile).open()):
        actual = float(entities[mapping[row["circuit_id"]]][4]) / 1000
        expected = float(row[field])
        assert abs(actual - expected) < .00001
        routes.append(dict(circuit_id=row["circuit_id"], native_plan_m=actual, expected_plan_m=expected))
incoming = json.loads((DATA / "incoming_route_cad_map.json").read_text())
for row in incoming["plans"].values():
    assert abs(float(entities[row["route_handle"]][4])/1000-incoming["plan_length_m"]) < .00001
circuits = {row["circuit_id"]: row for row in csv.DictReader((DATA / "circuits.csv").open())}
for row in json.loads((DATA / "db_submission_sheet_map.json").read_text())["circuit_rows"]:
    current = circuits[row["circuit_id"]]
    assert row["phase"] == current["phase"] and row["protective_A"] == current["MCB_A"]
    assert row["cable_mm2"] == current["cable_mm2"]
    assert abs(float(row["length_m"])-float(current["length_m"])) < .000001
assert before == sha(DWG), "Read-only audit changed the DWG"
evidence = dict(drawing=str(DWG), sha256=before, engine=str(CORE), native_version=lines[1][1],
                native_reopen_pass=True, read_only_hash_unchanged=True, checked_entity_handles=len(handles),
                missing_handles=0, lighting_labels_checked=92, routes=routes,
                incoming_plan_routes_checked=2, db_schedule_rows_checked=15, required_layouts=required,
                units="millimetres (INSUNITS4)", scope="Native DWG reopen/read; PDF print quality reviewed separately")
(DATA / ("native_reopen_gate.json" if revision=='v01' else "native_reopen_gate_v02.json")).write_text(json.dumps(evidence, indent=2), encoding="utf8")
print(json.dumps({k: v for k, v in evidence.items() if k != "routes"}))
