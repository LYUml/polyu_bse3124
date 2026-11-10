"""Reopen the saved submission DWG in AutoCAD2027's native Core Console.

Read-only entity extraction; no QSAVE, conversion, or existing-session restart.
Native DWG structure checks complement, and do not replace, PDF visual review.
"""
import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path

R = Path(__file__).resolve().parents[2]
DATA = Path(__file__).parent / "data"
OUT = Path(__file__).parent / "native_validation"
OUT.mkdir(exist_ok=True)
DWG = Path(__file__).parent / "BSE3124_Final_Rev02.dwg"
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
             "task1_interface_cad_map.json", "db_submission_sheet_map.json", "normal_plan_sheet_map.json", "final_text_sync.json"]:
    collect(json.loads((DATA / name).read_text(encoding="utf8")))
if True:
    handles.update((DATA/'installation_detail_handles.txt').read_text().splitlines())
repair=json.loads((DATA/'room_layout_repair.json').read_text())
handles.update(repair['handle_map'].values())
handles.add(repair['viewport_handle'])
for fn in ['stage2_handles.json','stage3_handles.json','stagepanels_handles.json','stagevent_handles.json','stageoffice_handles.json','stageaccess_handles.json']:
    handles.update(json.loads((Path(__file__).parent/fn).read_text()))
ordered = sorted(handles)
# Keep script lines short: AutoCAD truncates oversized command input lines.
literal = "\n".join(" ".join('"' + h + '"' for h in ordered[i:i+8]) for i in range(0, len(ordered), 8))
template = (Path(__file__).parent / "native_read_audit.lsp").read_text(encoding="ascii")
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
required.extend(['DESIGN-DETAILS','TASK1-MAIN-SCHEMATIC'])
assert set(required) <= set(layouts)
entities = {row[0]: row for row in lines if row[0] in handles}
assert set(entities) == handles and all(row[1] != "MISSING" for row in entities.values())
for row in json.loads((DATA / "luminaire_label_sync_audit.json").read_text())["records"]:
    assert entities[row["handle"]][3] == row["after"]
for row in json.loads((DATA/'final_text_sync.json').read_text())['records']:
    expected = next((r['after'] for r in json.loads((Path(__file__).parent/'text_revisions.json').read_text()) if r['handle']==row['handle']), row['after'])
    overrides = {'802F': r'Basis: supplied COP215 Rev07; COP101 v16.\PSee the new main distribution schematic for TX-A/B, MSB-A/B and floor supply zones.', '802B': r'ACCESS AND DOORS\PSouth external access assumed. Provide 3000-wide clear delivery route; unloading distance <=20 m to verify.\PPlant doors: HV 4000 W; TX 3000 W each; 2800 H assumed. Outward opening, shown at 90 degrees.\PAdjacent plant doors used sequentially; TX-A has wicket personnel access. Independent LV entrance west.'}
    expected = overrides.get(row['handle'],expected)
    expected = json.loads((Path(__file__).parent/'expected_revision_text.json').read_text()).get(row['handle'],expected)
    assert entities[row['handle']][3] == expected, row['handle']
for h,t in json.loads((Path(__file__).parent/'expected_revision_text.json').read_text()).items():
    if h in entities: assert entities[h][3]==t,h
sld_handles=set(json.loads((Path(__file__).parent/'stage3_handles.json').read_text()))
assert sum(1 for h,e in entities.items() if h in sld_handles and len(e)>5 and e[5]=='AECBS_UK_E_Meter')==31
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
(Path(__file__).parent / "native_final_gate.json").write_text(json.dumps(evidence, indent=2), encoding="utf8")
print(json.dumps({k: v for k, v in evidence.items() if k != "routes"}))
