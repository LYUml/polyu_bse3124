"""Generate the unified answer-sheet source from current course design data."""
import csv
import json
import re
import shutil
import hashlib
from pathlib import Path
from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "04_Design_Outputs/data"
OUT = ROOT / "04_Design_Outputs/submission/latex"
ASSETS = OUT / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)

def read(name):
    return list(csv.DictReader((DATA / name).open(encoding="utf8")))

def esc(value):
    return str(value).replace("&", r"\&").replace("%", r"\%").replace("_", r"\_").replace("#", r"\#")

def num(value, digits=3):
    return f"{float(value):.{digits}f}"

def row(*values):
    return " & ".join(str(v) for v in values) + r" \\"

circuits = read("circuits.csv")
lights = read("lighting_route_results.csv")
powers = read("power_route_results.csv")
voltage = {r["circuit_id"]: r for r in read("all_circuits_voltage_drop.csv")}
fault = {r["circuit_id"]: r for r in read("fault_protection_results.csv")}
demand = json.loads((DATA / "office_design_demand.json").read_text(encoding="utf8"))
devices = read("devices.csv")
assert len(circuits) == 15 and len(devices) == 112
cover_asset = ASSETS / "official-cover.pdf"
cover_source = ROOT / "01_Assignment/BSE3124 Mini Design Answer Sheets.docx"
provenance_path = DATA / "official_cover_provenance.json"
source_digest = hashlib.sha256(cover_source.read_bytes()).hexdigest()
if cover_asset.exists() and provenance_path.exists():
    provenance = json.loads(provenance_path.read_text(encoding="utf8"))
    assert provenance["source_docx_sha256"] == source_digest, "Official cover source changed"
    assert provenance["cover_pdf_sha256"] == hashlib.sha256(cover_asset.read_bytes()).hexdigest(), "Cover PDF changed"
elif not cover_asset.exists():
    writer = PdfWriter()
    cover = ROOT / "04_Design_Outputs/qa/template_render/BSE3124 Mini Design Answer Sheets.pdf"
    writer.add_page(PdfReader(cover).pages[0])
    with cover_asset.open("wb") as stream:
        writer.write(stream)
if not provenance_path.exists():
    provenance_path.write_text(json.dumps(dict(
        source_docx="01_Assignment/BSE3124 Mini Design Answer Sheets.docx",
        source_docx_sha256=source_digest,
        cover_pdf_sha256=hashlib.sha256(cover_asset.read_bytes()).hexdigest(),
        method="Native Word read-only PDF export, official page1 preserved",
        scope="Group identity blanks retained; no identities invented"), indent=2), encoding="utf8")
shutil.copy2(ROOT / "04_Design_Outputs/submission/Task1_drawings_review.pdf", ASSETS / "task1-drawings.pdf")
shutil.copy2(ROOT / "04_Design_Outputs/pdf/office_DB_submission_v01.pdf", ASSETS / "office-db.pdf")
for kind in ["lighting", "power"]:
    shutil.copy2(ROOT / f"04_Design_Outputs/pdf/office_{kind}_submission_v02.pdf", ASSETS / f"office-{kind}.pdf")

parts = [r"""
% !TeX program = xelatex
\documentclass[11pt,a4paper]{article}
\usepackage{fontspec}
\setmainfont{Times New Roman}
\usepackage[margin=25.4mm]{geometry}
\usepackage{amsmath,amssymb,booktabs,longtable,array,pdfpages,hyperref,eso-pic}
\hypersetup{hidelinks,pdftitle={BSE3124 Electrical Design Answer Sheets}}
\setlength{\parindent}{0pt}
\setlength{\parskip}{5pt}
\renewcommand{\arraystretch}{1.18}
\setlength{\tabcolsep}{5pt}
\newcommand{\task}[1]{\clearpage\section*{#1}}
\begin{document}
\includepdf[pages=1]{assets/official-cover.pdf}
\task{Task 1 Loading estimation and transformer room location}
\textbf{Working submission v02.} This answer follows the three supplied tasks and retains the official answer-sheet cover. Group1 identities are entered on the cover. The stated course assumptions define the calculations; they are not site measurements or certification of installed products.
\subsection*{Building load assessment}
Adopt the drawing areas 309, 309 and 410\,m$^2$ as usable floor areas for ten identical office floors. This is a course assumption: the UFA exclusions have not been independently reconciled. Use supplied CLP COP215 Rev07. The assignment's 1000\,kW is cooling capacity. Assume packaged air-cooled central AC, electrical PF 0.90 and five lifts. The 40\,kVA/lift public-services allowance is aggregate, not a lift motor rating.
\begin{align*}
A_{\rm UFA}&=10(309+309+410)=10\,280\ {\rm m^2},\\
S_{\rm office}&=10\,280(0.16)=1644.800\ {\rm kVA},\\
P_{\rm AC}&=\frac{1000}{3.51685}(1.85)=526.039\ {\rm kW},\\
S_{\rm AC}&=526.039/0.90=584.488\ {\rm kVA},\\
S_{\rm public}&=5(40)=200.000\ {\rm kVA}.
\end{align*}
COP215 Appendix 2 supplies the office density; Appendix 7 supplies the AC reference. Public services follow clauses 3.1.6 and 3.3.1 and include lobby AC. Let $X$\,kVA be the duplicated AC share. Because it cannot exceed either overlapping allowance, $0\le X\le200$. For the proposed two independent supply zones, apply clause 3.1.7:
\[
S_{\rm assessment}=1.1(1644.800+584.488+200-X).
\]
The range is 2452.216--2672.216\,kVA. Adopt the upper bound \textbf{2672.216\,kVA} for capacity reservation. This does not assert that actual overlap is zero. Do not add public lighting/pumps/fire-service allowances again on top of the aggregate reference.
\subsection*{Transformer and main LV room proposal}
Propose two1500\,kVA transformers with separate LV sections. Combined3000\,kVA capacity gives327.784\,kVA margin against the upper assessment. Zone A serves floors1--5 and zone B floors6--10, each with half the central plant/public allowance as a planning allocation. Each is1336.108\,kVA, approximately2030\,A at balanced380\,V. Full-load N--1 is not provided; load shedding is needed on loss of one transformer. Any coupler must prevent unauthorised parallel operation.
Locate the rooms at the lower-left perimeter of the supplied ground-floor plan. The substation is12430 by5450\,mm; the adjacent customer LV room is12430 by3500\,mm, its depth assumed. This supports external plant access, short transformer-to-LV interfaces, separation from the lift/stair/AHU core and an independent LV entrance. A3m clear external delivery route and unloading distance no more than20m are explicit site conditions, not inferred road geometry.
The drawing appendix shows doors, dimensions, equipment reservations and HV/LV interfaces. HV3000 by1000\,mm, two transformer2200 by1800\,mm envelopes and six LV cabinets are assumed planning reservations, not manufacturer footprints. COP101 v16 clause4.3 requires HV rear1000/front1800/sides750\,mm and transformer LV terminal900/other sides750\,mm. Their envelopes fit without overlap. Provide proposed2-hour fire-resisting partitions, sealed service penetrations and FFL150\,mm above assumed external level. Outward180-degree plant doors have shared swing zones requiring sequential use.
Two600 by2000\,mm inlet louvres give $2(0.6)(2.0)(0.50)=1.20$\,m$^2$ effective area at assumed50\% free area, exceeding the1.12\,m$^2$ reference for3000\,kVA under clause6.3. Certified free area must be at least46.67\%. Fan symbols are conditional reference provisions, not actual loss calculations. LV interface routes including assumed tails are10.03 and10.31m, below the20m limit in5.5.2.2. Structures, actual equipment, ventilation and openings must satisfy these declared conditions.
\task{Task 2 Layout drawings and MCB board schematics}
\textbf{The office tenant chosen for layout design: Office 1.}
\subsection*{Normal lighting and local controls}
The design contains92 working600mm-grid panel positions using PIL PLATO600 MultiPower3117955: sixty22W and thirty-two28W, total2216W. The retained LDT manifest gives nominal flux2843.45 and3555.30lm respectively. Match the ceiling grid, partitions and furniture, with separate enclosed-space circuits and distributed main-office circuits. A500lx task-plane target is a design assumption; certified photometric uniformity/glare compliance is not claimed. Connected lighting density at the provisional309m$^2$ is7.172W/m$^2$; this arithmetic alone is not energy-code compliance.
Seven local passive manual switches S-A--S-G control their corresponding circuits. Specify minimum20AX, LED switching at least600W and make/break/inrush compatibility for the selected drivers. S-A/B/C use separate enclosures because their phases differ. No borrowed neutral is allowed. Routes visit each switch; include2m DB rise plus1.5m down/1.5m back at the switch, giving5m assumed vertical allowance per lighting radial. Passive controls add no operating power.
\begin{center}\begin{tabular}{lrrrrl}\toprule
Circuit & Lamps & W & Phase & RCBO & Control\\\midrule
"""]
for lamp in lights:
    c = next(c for c in circuits if c["circuit_id"] == lamp["circuit_id"])
    parts.append(row(c["circuit_id"], lamp["lamps"], num(lamp["power_W"], 0), c["phase"], "B10", "S-" + c["circuit_id"][-1]))
parts.append(r"""
\bottomrule\end{tabular}\end{center}
Plan A/B/C numeric labels map to corresponding LED IDs and LC-A/B/C. D01--D11 map to PN01--PN11, E82--E96 excluding E90 to northeast LEDs, F01--F10 to UE01--UE10, G01--G04 to SE01--SE04. Power settings follow the common device schedule. Every luminaire and control has one circuit assignment.
\subsection*{Small power and fixed equipment}
Provide nine four-socket floor boxes, three twin wall sockets and fixed connection FS01. Each floor-box/socket assembly is individually13A fused. This defines intended continuous demand, not an instantaneous current clamp. FS01 reserves equipment up to13A; appliance identity/watts are not invented. Building central AC is supplied as central plant and not duplicated in this office DB.
P1--P4 are A1 rings with fused floor-box connections. P5/P6/P8 are A2 radials; P7 is a fixed radial. Both P6 and P8 serve the source PANTRY; the previous meeting-room description of FB09/SO01 is superseded. P8 is retained as a separate socket group by design choice, not because each pantry outlet requires its own final circuit. Kitchen sockets are separated from ordinary office circuits under EMSD6E(3)(a).
\begin{center}\begin{tabular}{llllr}\toprule
Circuit & Points & Phase & Topology & Protection\\\midrule
""")
for power in powers:
    c = next(c for c in circuits if c["circuit_id"] == power["circuit_id"])
    kind = "A1 ring" if c["circuit_id"] in ["P1", "P2", "P3", "P4"] else ("Fixed radial" if c["circuit_id"] == "P7" else "A2 radial")
    parts.append(row(c["circuit_id"], esc(c["device_ids"].replace(";", ", ")), c["phase"], kind, "B" + c["MCB_A"]))
parts.append(r"""
\bottomrule\end{tabular}\end{center}
Defined service envelopes satisfy A1 maximum100m$^2$ and A2 maximum50m$^2$. These are designed coverage polygons, not net UFA, with intentional overlap. Ring L/N/CPC return to their own circuit terminals. Main6/10mm$^2$ cables terminate in suitable accessible junction/FCU assemblies, not assumed ordinary socket terminals. Local connections use4mm$^2$ L/N/CPC and assumed0.5m per point.
\subsection*{Protection and board arrangement}
The complete schematic shows C63 four-pole protection at MS-O1, 4-core35mm$^2$ plus CPC16, a100A four-pole DB isolator, independent L1/L2/L3/N/PE bars and15 separate1P+N TypeA30mA RCBOs. Every load neutral passes through its own RCBO; none are shared downstream. PE bypasses all switches. Label circuits/phases and allow one final circuit to be isolated without interrupting the rest.
Use B-curve final protection and require compatible driver inrush. Do not change to a C curve without recalculation. Apparatus must meet Task3 breaking/energy limits. Ratings/curves alone do not prove full short-circuit discrimination; none is claimed.
\subsection*{Emergency lighting assumption}
Assume landlord emergency lighting/exit signage on independent essential systems, electrically separated under EMSD6B(4). No ordinary tenant panel is an emergency fitting. Emergency feeds must not pass through tenant normal-lighting switches or these RCBO load sides. Emergency load is excluded from this normal DB under this explicit course boundary; installed escape coverage, autonomy and illuminance are not certified.
\task{Task 3 Maximum current demand calculation and cable sizing}
\subsection*{Maximum current demand}
For lighting, $I_b=P/(220\times0.90)$. Incoming diversity follows EMSD Table7(1):90\% of office lighting, and100\% of the largest Code6E circuit plus50\% of the remaining circuit currents on each phase. Reserve P7 at100\% separately. Use designed fused-point demand bounds, not breaker nameplates as appliance loads.
\begin{center}\begin{tabular}{lrrrr}\toprule
Phase & Lighting A & Socket demand A & P7 A & Total demand A\\\midrule
""")
for phase in demand["phases"]:
    parts.append(row(phase["phase"], num(phase["lighting_undiversified_A"]), num(phase["socket_diversified_A"]), num(phase["fixed_reserved_A"]), num(phase["design_demand_A"])))
parts.append(r"""
\bottomrule\end{tabular}\end{center}
Maximum phase demand is \textbf{48.909A}; select C63 at the source and100A DB isolation/busbars. Maximum undiversified phase point allowance68.444A is below the board rating. Earlier80A nominal-capacity studies are historical; this design uses the now-drawn13A fused-point restrictions.
\subsection*{Incoming cable}
Select4-core35mm$^2$ PVC copper L1/L2/L3/N plus separate16mm$^2$ PVC copper CPC, MethodB in protected enclosed containment. Proposed same-floor meter-to-DB route28.5119m plus assumed3m total vertical/termination allowance gives31.5119m. The proposed source is near the supplied METER label, not a measured termination. Upstream ground-to-floor distribution is retained through explicit voltage/fault conditions.
For40\,degrees C take $C_a=0.87$, $C_g=1$, and $C_h=0.86$ for assumed third-harmonic content greater than15\% and at most33\% in this four-core cable (A5(7)). Keep a full-size neutral and reselect if this range is exceeded.
\begin{align*}
I_{z,25}&=80(0.87)(0.86)=59.856\,{\rm A}<63\,{\rm A},\quad\text{reject},\\
I_{z,35}&=99(0.87)(0.86)=74.0718\,{\rm A},\\
48.9091&\le63\le74.0718\,{\rm A},\quad\text{pass}.
\end{align*}
TableA6(2) column5 supplies ratings. Table11(2)(a) gives CPC16 for $16<S\le35$; energy is checked below. For unbalanced phase-neutral drop with neutral current at most63A, derive $(2/\sqrt3)(1.10)=1.270170592$\,mV/A/m from the three-phase table impedance. Feeder drop at63A is2.521606V; at design current1.957610V. This fundamental-frequency check is not harmonic-distortion assessment.
\subsection*{All outgoing cables}
All sizes are PVC copper L/N/CPC. Lighting grouped separately has $I_z=24(0.87)(0.54)=11.2752$A for seven2.5mm$^2$ circuits; all $I_b\le10\le I_z$. Lighting lengths include5m DB/switch vertical allowance.
Uniform ring banks count four current-carrying legs: $I_z=41(0.87)(0.65)=23.1855$A per6mm$^2$ leg, above the standard20A minimum. Ring-network solution at13A per point gives maximum leg currents14.658--15.203A, below $I_z$. Do not compare radial $I_n\le I_z$ against just one ring leg. Continuity and fused-point restrictions are essential.
The10mm$^2$ A2 radials have $I_z=57(0.87)(0.70)=34.713$A; P7's separate4mm$^2$ radial has $I_z=32(0.87)=27.84$A. Power radial allowance is2m vertical, rings2m at each DB end; all local point spurs add0.5m of4mm$^2$ cable.
\begin{longtable}{llrrrr}\toprule
Circuit & Phase & $I_b$ A & RCBO A & L/N/CPC mm$^2$ & Main length m\\\midrule\endhead
""")
for c in circuits:
    parts.append(row(esc(c["circuit_id"]), c["phase"], num(c["Ib_A"]), c["MCB_A"], c["cable_mm2"], num(c["length_m"])))
parts.append(r"""
\bottomrule\end{longtable}
\subsection*{Complete voltage drop and fault checks}
Sum segment downstream-current drops on radials and solve the two-feed ring network. Include stated vertical/local allowances. Add2.2V pre-origin allowance,2.521606V feeder bound and outgoing drop. The full limit is $0.04(220)=8.8$V.
Adopt TN-S, external source loop impedance0.20ohm and PFC at most6kA at MS-O1/downstream. These are course conditions, not measurements. Incoming phase+CPC bound0.064129ohm gives DB external loop0.264129ohm. Table11(10) reference limits are B10=4.17, B16=2.61, B32=1.31 and C63=0.33ohm. Use operating-temperature paths and minimum voltage factor0.95. Worst uniform-ring parallel path is at most quarter circumference.
\begin{longtable}{lrrrrr}\toprule
Circuit & Out drop V & Total drop \% & $Z_s$ ohm & Min fault A & $Z_s$ limit ohm\\\midrule\endhead
""")
for c in circuits:
    cid = c["circuit_id"]
    v, q = voltage[cid], fault[cid]
    parts.append(row(esc(cid), num(v["outgoing_V"]), num(v["total_percent"]), num(q["Zs_design_ohm"]), num(q["minimum_earth_fault_A"], 1), num(q["reference_Zs_limit_ohm"], 2)))
parts.append(r"""
\bottomrule\end{longtable}
All15 full voltage bounds pass; worst3.031\%. Each B-curve final circuit exceeds minimum earth-fault threshold $5I_n$. Incoming C63 gives $Z_s=0.264129<0.33$ohm and $I_{f,\min}=791.28>10(63)=630$A, satisfying reference instantaneous disconnection under the adopted conditions.
\subsection*{Overload and total clearing energy}
Use $k=115$ for bunched PVC copper CPCs initially70\,degrees C (11(2)(c)); require total $I^2t\le(kS)^2$. Specify10kA main/RCBO interruption. Require class3-equivalent B-curve total energy at most70,000A$^2$s for B10/B16,90,000 for B32. These are functional selection requirements, not automatic certification of any RCBO. CPC withstands are82,656.25 (2.5mm$^2$),211,600 (4),476,100 (6),1,322,500 (10), each above the required device bound.
Incoming C63 total energy must be at most1,000,000A$^2$s over the relevant fault range, below CPC16 withstand3,385,600. Complete13A FCU energy must be at most90,000, below the4mm$^2$ spur withstand211,600. The incoming/FCU limits are explicit apparatus performance specifications, not invented manufacturer data.
For fuse overload, $I_2=1.9(13)=24.7$A. Spur $I_z=32(0.87)(0.70)=19.488$A gives $1.45I_z=28.2576>24.7$A. Ring leg conventional-current bounds also remain below $1.45I_z$ for the declared fused-point design. The fuse reference6kA interruption meets assumed PFC at most6kA. Its typical pre-arcing870A$^2$s is \emph{not} total clearing energy. Assume FCU ambient at most35\,degrees C and board apparatus at most30\,degrees C; containment40\,degrees C remains the conservative cable condition.
\subsection*{Sources and reproducibility}
Cite supplied COP215 Rev07 and downloaded COP101 v16 as above. EMSD Wiring CoP2025: Table6(1), printed56/PDF57;7(1), printed65--67/PDF66--68;9B, printed79/PDF80;11(2), printed99--100/PDF100--101;11(10), printed105/PDF106; A5 factors PDF274--279; A6 tables PDF282--285.
ABB guide9AKK108468A3912 printed130 gives the class3 B-curve energy references. Eaton TDC180 Technical Data2042 August2024 p2 gives conventional-fusing/interruption references, not total energy. URLs and explicit conditions are in the common data file \texttt{fault\_design\_conditions.json}.
Tables are generated from current common CSV/JSON data. Reproduce the lighting/power route, demand, incoming and fault scripts before rebuilding this answer. Guarded DWG mutations must not be rerun blindly. Original source documents are retained. Normal lighting/power layout PDFs have been visually reviewed. Final native DWG save/reopen consistency verification is recorded separately in the acceptance evidence.
\clearpage\section*{Drawing appendix}
The following sheets show the ground-floor proposal, complete Office1 DB schematic, normal lighting plan and power plan. Print at actual size to preserve the stated drawing scales. Group1 identities are shown on the official cover.
\includepdf[pages=-]{assets/task1-drawings.pdf}
\includepdf[pages=-]{assets/office-db.pdf}
\includepdf[pages=-]{assets/office-lighting.pdf}
\includepdf[pages=-]{assets/office-power.pdf}
\end{document}
""")
source = "\n".join(parts)
identity = json.loads((DATA / "group_identity.json").read_text(encoding="utf8"))
cover_items = [(232, str(identity["group_number"]))] + [
    (191 - 28*i, m["name"] + " (" + m["student_id"] + ")")
    for i, m in enumerate(identity["members"])]
cover_overlay = "".join(r"\put(220," + str(y) + r"){\fontsize{11}{13}\selectfont " + esc(value) + "}" for y, value in cover_items)
source = source.replace(r"\includepdf[pages=1]{assets/official-cover.pdf}",
    r"\includepdf[pages=1,pagecommand={\thispagestyle{empty}\AddToShipoutPictureFG*{\AtPageLowerLeft{" + cover_overlay + r"}}}]{assets/official-cover.pdf}")
start = source.index(r"\subsection*{Transformer and main LV room proposal}")
end = source.index(r"\task{Task 2")
source = source[:start] + r"""
\subsection*{Transformer and main LV room proposal}
Propose two1500kVA transformers with separate LV sections:3000kVA total gives327.784kVA margin. Allocate floors1--5 to A and6--10 to B, each with half the central plant/public allowance. Each section is1336.108kVA, about2030A at380V. The equal split is assumed. Full-load N--1 is not provided; load shedding is required on loss of one unit. Any coupler must prevent parallel operation.
Place the rooms at the lower-left perimeter of the supplied plan: substation12430 by5450mm and adjacent LV room12430 by3500mm, the latter depth assumed. Reasons are external plant access, short LV interfaces, separation from the lift/stair/AHU core and independent LV access. Reserve a3m delivery route within20m of unloading, subject to external site confirmation.
The appendix shows assumed HV3000 by1000mm and transformer2200 by1800mm equipment reservations and six LV cabinets; these are not manufacturer footprints. Their clearance envelopes fit without overlap. COP101 v16 clause4.3 requires HV rear1000/front1800/sides750mm and transformer LV terminals900/others750mm. Propose2-hour partitions, sealed penetrations and FFL150mm above external level. Outward180-degree doors have shared sweeps requiring sequential use.
Two600 by2000mm louvres at assumed50\% free area provide1.20m$^2$, above clause6.3's1.12m$^2$ reference; certified free area must be at least46.67\%. Fan symbols are conditional provisions, not actual heat-loss calculations. LV interfaces including assumed tails are10.03/10.31m, below the20m limit in5.5.2.2. Actual equipment, structures, openings and ventilation must satisfy these declared conditions.
""" + source[end:]
source = source.replace(
    r"\textbf{Working submission v02.} This answer follows the three supplied tasks and retains the official answer-sheet cover. Group1 identities are entered on the cover. The stated course assumptions define the calculations; they are not site measurements or certification of installed products.",
    r"\textbf{Working submission v02.} Official cover and task structure are retained. The stated assumptions define a course design, not site certification.")
source = source.replace("the previous meeting-room description of FB09/SO01 is superseded.", "including FB09 and SO01.")
source = source.replace("Earlier80A nominal-capacity studies are historical; this design uses the now-drawn13A fused-point restrictions.", "This demand depends on the specified13A fused-point restrictions.")
source = source.replace(r"\setlength{\parskip}{5pt}", r"\setlength{\parskip}{5pt}" + "\n" + r"\emergencystretch=1em")
# Normalize prose spacing without altering commands, file paths, equations or IDs.
formatted = []
for line in source.splitlines():
    if line and line[0].isalpha() and "&" not in line and not line.endswith(r" \\"):
        line = line.replace("A3m clear", "A 3m clear").replace("PLATO600", "PLATO 600")
        line = re.sub(r"(?<=[a-z])(?=\d)", " ", line)
        line = re.sub(r"(?<=\d)(?=(?:mm|kVA|kW|kA|ohm|lm|lx|W\b|A\b|V\b|m\b))", " ", line)
        line = re.sub(r"PDF(?=\d)", "PDF ", line)
        line = line.replace(";", "; ")
    formatted.append(line)
source = "\n".join(formatted)
source = source.replace(r"\clearpage\section*{Drawing appendix}", r"\paragraph*{Drawing appendix}")
source = source.replace(r"\includepdf[pages=-]{", r"\includepdf[pages=-,fitpaper=true]{")
(OUT / "main.tex").write_text(source, encoding="utf8")
print("Unified LaTeX answer generated from112 components and15 circuits")
