"""Native A3 portrait 1:75 normal plans; never rerun over existing layouts.

Reference layers are greyed on this versioned working DWG only. Legacy
electrical annotation is hidden; adopted editable E-* design layers remain.
PDF success requires separate visual review, not this script's return value.
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
names = ["TASK2-LIGHTING-PLAN", "TASK2-POWER-PLAN"]
existing = [x.Name for x in D.Layouts]
assert not any(n in existing for n in names), "Inspect existing sheets; do not duplicate"
pt = lambda x, y, z=0: VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [float(x), float(y), float(z)])
style_audit = []
for name, grey in [("ARCH", 160), ("Furniture", 185), ("Ceiling Grid", 210)]:
    layer = D.Layers.Item(name)
    old = layer.TrueColor
    style_audit.append(dict(layer=name, previous_color=int(layer.Color), previous_rgb=[old.Red, old.Green, old.Blue], new_rgb=[grey]*3))
    color = layer.TrueColor
    color.SetRGB(grey, grey, grey)
    layer.TrueColor = color
D.ActiveLayer = D.Layers.Item("0")
for name in ["Lighting", "Power", "circuitory"]:
    layer = D.Layers.Item(name)
    style_audit.append(dict(layer=name, previous_on=bool(layer.LayerOn), new_on=False))
    layer.LayerOn = False
layer = D.Layers.Add("E-NORMAL-PLAN-PAPER")
layer.Color = 7
circuits = {r["circuit_id"]: r for r in csv.DictReader((DATA / "circuits.csv").open())}
light = list(csv.DictReader((DATA / "lighting_route_results.csv").open()))
power = list(csv.DictReader((DATA / "power_route_results.csv").open()))
out = []
for name, offset, kind in [(names[0], 0, "LIGHTING"), (names[1], -49378, "POWER")]:
    assert Path(D.FullName).resolve() == (R / "04_Design_Outputs/cad/assignment_working_v02.dwg").resolve()
    L = D.Layouts.Add(name)
    L.CopyFrom(D.Layouts.Item("TASK1-ROOM-REVIEW"))
    D.ActiveLayout = L
    L.ConfigName = "DWG To PDF.pc3"
    L.RefreshPlotDeviceInfo()
    L.CanonicalMediaName = "ISO_full_bleed_A3_(297.00_x_420.00_MM)"
    L.PlotRotation = 0
    L.PlotType = 5
    L.UseStandardScale = True
    L.StandardScale = 16
    L.PlotOrigin = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [0., 0.])
    L.StyleSheet = "monochrome.ctb"
    P = D.PaperSpace
    handles = []
    def text(s, x, y, w=273, h=2.5):
        e = P.AddMText(pt(x, y), w, s)
        e.Height = h
        e.StyleName = "T1-Arial"
        e.Layer = layer.Name
        handles.append(e.Handle)
    text(f"TASK 2 | OFFICE 1 NORMAL {kind}", 12, 409, h=4)
    text("A3 PORTRAIT | 1:75 at actual size | mm | DB-O1 | COURSE DESIGN", 12, 400, h=2.6)
    viewport = P.AddPViewport(pt(148.5, 240), 220, 285)
    viewport.Layer = "E-T1-VPORT-NOPLOT"
    viewport.Display(True)
    viewport.Target = pt(72167.182, 26350.584 + offset)
    viewport.Direction = pt(0, 0, 1)
    viewport.CustomScale = 1 / 75
    viewport.DisplayLocked = True
    handles.append(viewport.Handle)
    text("Supply continues to MS-O1 at meter location; incoming route on model / DB schematic.", 12, 391, h=2.25)
    if kind == "LIGHTING":
        text("600x600 LED panel: A/B/C=22W, *=28W; D=22W; E/F/G=28W.", 12, 90)
        text("Label prefix gives LC-A ... LC-G; suffix retains device ID. S-A ... S-G = local switches.", 12, 84, h=2.35)
        for i, r in enumerate(light):
            c = circuits[r["circuit_id"]]
            text(f"{r['circuit_id']}  {c['phase']}  {r['lamps']} lamps /{float(r['power_W']):.0f}W  B10  2.5mm2  {float(r['design_route_m']):.3f}m", 12, 76-i*5, h=2.5)
        text("92 panels /2216W. All circuits: Type A30mA1P+N RCBO; L/N/CPC all2.5mm2.", 12, 36, h=2.35)
        text("Manual controls20AX, LED rating>=600W; separate phase enclosures. Inrush compatibility required.", 12, 30, h=2.25)
        text("Normal lighting only. Landlord emergency/exit system independently supplied (course assumption).", 12, 24, h=2.25)
    else:
        text("FB01-09=floorbox; SO01-03=twin socket; FS01=dedicated fused spur.", 12, 90)
        text("Each point:13A fuse; intended continuous demand<=13A. Local spur4mm2,0.5m allowance.", 12, 84, h=2.3)
        for i, r in enumerate(power):
            c = circuits[r["circuit_id"]]
            topology = "RING" if i < 4 else "RADIAL"
            text(f"{r['circuit_id']} {c['phase']} {topology} B{c['MCB_A']} {c['cable_mm2']}mm2 {float(r['main_with_vertical_m']):.3f}m", 12+(i//4)*139, 76-(i%4)*6, w=135, h=2.4)
        text("Ring L/N/CPC both ends return to same circuit. Radial L/N/CPC same stated size.", 12, 45, h=2.35)
        text("FB09/SO01/SO03 serve pantry: P6/P8. P7 is reserved equipment capacity, appliance rating unknown.", 12, 38, h=2.25)
        text("Containment: rings P1/P2 bank A; P3/P4 bank B; radials P5/P6/P8 bank C; P7 separate.", 12, 31, h=2.25)
        text("Individually fused point assemblies and terminals must accept selected conductor size or rated junctions.", 12, 24, h=2.25)
    text("Proposed routes follow plan; vertical/tail allowances and conditions are in Task3. Architecture retained as reference.", 12, 16, h=2.2)
    text("BSE3124 | 2026-11-07 | Read with15-way DB schematic and common circuit schedule", 12, 10, h=2.2)
    D.Regen(1)
    D.SetVariable("BACKGROUNDPLOT", 0)
    D.Save()
    output = R / f"04_Design_Outputs/pdf/office_{kind.lower()}_submission_v01.pdf"
    assert not output.exists()
    success = bool(D.Plot.PlotToFile(str(output), "DWG To PDF.pc3"))
    out.append(dict(layout=name, pdf=str(output), plot_return=success, scale="1:75", format="A3 portrait full bleed", handles=handles))
(DATA / "normal_plan_sheet_map.json").write_text(json.dumps(dict(drawing=D.FullName, sheets=out, reference_style_changes=style_audit, visual_review="pending"), indent=2), encoding="utf8")
print(json.dumps(out))
