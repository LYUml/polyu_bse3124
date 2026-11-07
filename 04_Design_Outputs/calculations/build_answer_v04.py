"""Exact retained Word page backgrounds with editable LaTeX answer overlays.

The blank template preserves all five exported pages; continuation pages and
design content are native LaTeX. No raster screenshot substitutes for text.
"""
from pathlib import Path
import csv,json,hashlib,shutil
R=Path(__file__).resolve().parents[2];D=R/'04_Design_Outputs/data';O=R/'04_Design_Outputs/submission/latex_v04'
O.mkdir(exist_ok=True);(O/'assets').mkdir(exist_ok=True)
old=R/'04_Design_Outputs/submission/latex'
for p in (old/'assets').glob('*.pdf'):shutil.copy2(p,O/'assets'/p.name)
template=O/'assets/official-template.pdf'
assert template.exists()
docx=R/'01_Assignment/BSE3124 Mini Design Answer Sheets.docx'
assert hashlib.sha256(docx.read_bytes()).hexdigest()=='da927db8e419e8639f0a89052ddf64c104011f22ce808b371756012d2f25d65d'
preamble=r'''\documentclass[11pt]{article}
\usepackage{fontspec}\setmainfont{Times New Roman}
\usepackage[paperwidth=595.32bp,paperheight=841.92bp,left=80bp,right=80bp,top=111bp,bottom=104bp]{geometry}
\usepackage{amsmath,amssymb,booktabs,longtable,array,pdfpages,hyperref,eso-pic,graphicx}
\hypersetup{hidelinks,pdftitle={BSE3124 Group 1 Answer Sheets v04}}
\pagestyle{empty}\setlength{\parindent}{0pt}\setlength{\parskip}{5pt}
\setlength{\tabcolsep}{4pt}\renewcommand{\arraystretch}{1.16}\emergencystretch=2em
\setlength{\unitlength}{1bp}
\newcommand{\slot}[4]{\put(#1,\dimexpr841.92bp-#2bp\relax){\makebox(0,0)[lt]{\begin{minipage}[t]{#3bp}\vspace{0pt}\fontsize{11}{13}\selectfont #4\end{minipage}}}}
\newcommand{\task}[1]{\section*{#1}}
\newcommand{\sheet}[2]{\long\gdef\currentsheetoverlay{#2}\includepdf[pages=#1,fitpaper=true,noautoscale=true,pagecommand={\AddToShipoutPictureFG*{\AtPageLowerLeft{\currentsheetoverlay}}}]{assets/official-template.pdf}}
\begin{document}
'''
blank=r'''\documentclass{article}
\usepackage[paperwidth=595.32bp,paperheight=841.92bp,margin=0bp]{geometry}
\usepackage{pdfpages}
\begin{document}
\includepdf[pages=-,fitpaper=true,noautoscale=true]{assets/official-template.pdf}
\end{document}
'''
(O/'template_blank.tex').write_text(blank)
parts=[preamble,r'''\sheet{1}{
\slot{220}{599}{205}{1}
\slot{220}{640}{205}{LYU Mingliang (24099296D)}
\slot{220}{668}{205}{HUANG Celine (24034414D)}
\slot{220}{696}{205}{LIU Wing Kei (24093229D)}}
\sheet{2}{\slot{80}{153}{435}{
\textbf{Basis and assumptions.} Ten identical office floors, each with usable areas assumed to be 309, 309 and 410\,m$^2$. Supplied CLP COP215 Rev07 is the course basis. The 1000\,kW in the question is cooling output, not electrical demand. Assume packaged air-cooled AC, PF 0.90, five lifts and equal allocation to two supply zones.
\begin{align*}
A&=10(309+309+410)=10\,280\ {\rm m^2},\\
S_{\rm office}&=10\,280(0.16)=1644.8\ {\rm kVA},\\
P_{\rm AC}&=(1000/3.51685)(1.85)=526.039\ {\rm kW},\\
S_{\rm AC}&=526.039/0.90=584.488\ {\rm kVA},\\
S_{\rm public}&=5(40)=200\ {\rm kVA},\\
S_{\rm design}&=1.10(1644.8+584.488+200)=2672.216\ {\rm kVA}.
\end{align*}
The 40\,kVA/lift allowance is an aggregate public-services reference, not a lift motor rating. A public-services overlap allowance of 0--200\,kVA gives 2452.216--2672.216\,kVA; adopt the upper bound. COP215: 3.1.7, 3.3.1 and Appendices 2/7.

\textbf{Selection.} Two 1500\,kVA transformers provide 3000\,kVA. Each serves five floors and half the plant/public allowance: 1336.108\,kVA per section. Full-load N--1 is not provided; a failed transformer requires load shedding. Prevent unauthorised parallel operation.

\textbf{Room location.} Use the lower-left ground-floor perimeter for the 12430$\times$5450\,mm transformer room and adjacent 12430$\times$3500\,mm main LV room (LV depth assumed). This allows external delivery/access, short LV interfaces, separation from the central lift/stair/AHU core and independent customer access.

Reserve 3\,m delivery access within 20\,m of unloading. Adopt COP101 v16 4.3 clearance envelopes, 2-hour partitions, sealed penetrations and raised floor level; these are planning conditions. Door sweeps require sequential use. Louvres provide 1.20\,m$^2$ free area at the assumed 50\% free ratio. Equipment/ventilation and 10.03/10.31\,m LV interfaces are detailed in the continuation and ground-floor drawings.
}}
\sheet{3}{\slot{80}{181}{435}{
\textbf{Selected tenant: Office 1.} See attached lighting/power plans, filled board template and detailed L/N/PE schematic.

\textbf{Lighting.} 92 PIL PLATO 600 panels: sixty 22\,W and thirty-two 28\,W, total 2216\,W. Seven circuits LC-A--LC-G have 18/17/18/11/14/10/4 lamps, each protected by B10 Type A 30\,mA 1P+N RCBO. Each has its own neutral and local manual control S-A--S-G. Different-phase switches use separate enclosures. Ceiling-grid and furniture relationships guide positions.

\textbf{Selection calculation.} Recalculation using the final device table and manufacturer LDT files gives mean maintained direct illuminance of 592.9/546.3/588.5/502.9\,lx for open office/pantry/upper east/south east. Adopt 1.9\,m luminaire-to-workplane height and MF 0.80. The south east room must not exceed this height without redesign; at 2.2\,m it falls below the 500\,lx target. The continuation records geometry, method, sensitivity and the limits of this average-illuminance check.

\textbf{Power.} Nine four-socket floorboxes, three twin sockets and FS01. Every assembly has one upstream 13\,A FCU; its outlets share that capacity. P1--P4: 6\,mm$^2$ A1 rings/B32; P5/P6/P8: 10\,mm$^2$ A2 radials/B32; P7: 4\,mm$^2$ dedicated radial/B16. Each local fused spur is 4\,mm$^2$, assumed 0.5\,m. FCUs precede the spur cable. Separate pantry circuits from ordinary office circuits. FS01 reserves 13\,A without inventing an appliance rating.

\textbf{Protection and containment.} Keep L/N/CPC ring continuity and return both ends to the same circuit. Apply EMSD Table 6(1)'s A1 conditions, not a fictitious ring-leg protective-device $I_2$. Separate the lighting group, ring banks A/B, radial bank C, P7 and incoming feeder so the stated grouping factors remain valid. See the new installation-detail sheet.

\textbf{Supply and controls.} Source C63 4P; 4C35\,mm$^2$ + CPC16; 100\,A 4P DB isolation. Dedicated neutrals pass through their own RCBO; PE is unswitched. Specify 10\,kA interruption and the stated total-energy/inrush limits. These are equipment selection requirements, not verified product certificates. Assume landlord emergency/exit systems on independent essential supplies; no normal panel is claimed as an emergency fitting.
}}
\sheet{4}{\slot{80}{139}{435}{
For lighting, $I=P/(220\times0.90)$. EMSD Table 7(1): take 90\% of lighting and 100\% of the largest Code 6E circuit plus 50\% of the remaining circuits on each phase. Reserve P7 at 100\% separately. The 13\,A per assembly is an intended maximum continuous load, not an instantaneous fuse clamp.
\begin{center}\begin{tabular}{lrrrr}\toprule
Phase & Light A$^*$ & Sockets A & Fixed A & Demand A\\\midrule
L1 & 3.444 & 45.500 & 0 & 48.600\\
L2 & 3.960 & 39.000 & 0 & 42.564\\
L3 & 3.788 & 32.500 & 13 & 48.909\\\bottomrule
\end{tabular}\end{center}
$^*$Lighting column is before the 90\% factor. Maximum demand is \textbf{48.909\,A}; select 63\,A source protection and 100\,A DB. Maximum undiversified phase allowance is 68.444\,A. Full branch currents are retained for outgoing cable sizing.
}
\slot{80}{402}{435}{
Select 4-core 35\,mm$^2$ PVC copper plus 16\,mm$^2$ CPC, Method B. Route 28.5119\,m plus assumed 3\,m vertical/termination allowance = 31.5119\,m. At 40\,$^\circ$C, $C_a=0.87$, $C_g=1$; adopt $C_h=0.86$ for the stated third-harmonic range (15--33\%).
\begin{align*}
I_{z,25}&=80(0.87)(0.86)=59.856<63\ {\rm A},\\
I_{z,35}&=99(0.87)(0.86)=74.0718\ {\rm A},\\
I_b&=48.909\le I_n=63\le I_z=74.0718\ {\rm A}.
\end{align*}
Ratings: EMSD A6(2), column 5. CPC: Table 11(2)(a). Full-size neutral retained; neutral current must remain within the adopted bound.

At 63\,A, feeder drop is 2.521606\,V. Add 2.2\,V pre-origin allowance and the calculated branch drops: worst complete drop 3.031\% of 220\,V, below 4\%. Adopt TN-S, source $Z_e=0.20\,\Omega$ and PFC $\le6$\,kA. Then DB external loop is 0.264129\,$\Omega$; source C63 disconnection and outgoing B-curve checks pass under those conditions.

\textbf{Outgoing circuits are also included}, as required by the assignment: all 15 sizes, currents, lengths, voltage drops, earth-fault checks and apparatus energy requirements are tabulated in the continuation. Original template headings do not limit the calculation to incoming cable only.
}}
''']
# Original sideways board template: preserve it and place a readable schedule in its blank area.
cir=list(csv.DictReader((D/'circuits.csv').open()));phases={p:[c for c in cir if c['phase']==p] for p in ['L1','L2','L3']}
board=r'\begin{minipage}{450bp}\fontsize{9}{11}\selectfont\textbf{DB-O1: 8-way TPN chassis; 15 used single-phase outgoing positions}\par\smallskip\begin{tabular}{llll}\toprule Way & L1 & L2 & L3\\\midrule'+'\n'
for i in range(8):
 cells=[str(i+1)]+[(f"{phases[p][i]['circuit_id']} / B{phases[p][i]['MCB_A']}" if i<len(phases[p]) else 'Spare') for p in phases]
 board+=' & '.join(cells)+r'\\'+'\n'
board+=r'''\bottomrule\end{tabular}\par\smallskip
Positions indicate phase allocation; each RCBO also needs its own N path. Confirm chassis/module capacity for 1P+N devices. Incoming: C63 4P at MS-O1; local main switch is 100A 4P (including N), supplementing the template's TP SW symbol. The detailed appended schematic governs neutral/PE connections and ring returns. All final RCBOs: Type A, 30mA, 10kA; see energy/inrush specifications.\end{minipage}'''
parts.append(r'\sheet{5}{\put(105,190){\rotatebox{90}{'+board+'}}}\n')
# Reuse the complete editable calculations, correcting only the reviewed content.
body=(old/'main.tex').read_text(encoding='utf8');body=body[body.index(r'\task{Task 1'):]
body=body.replace('Final submission v03.','Technical continuation v04.')
body=body.replace('Official cover and task structure are retained.','The original five-page template precedes this continuation.')
body=body.replace('Ring leg conventional-current bounds also remain below $1.45I_z$ for the declared fused-point design.',r'For P1--P4, overload suitability uses the standard A1 arrangement in EMSD 6C, 6E and Table 6(1), Note 1(i): 32 A protection, copper size at least 2.5 mm$^2$, corrected per-leg capacity at least 20 A, served area at most 100 m$^2$, intact L/N/CPC rings and evenly distributed outlets. The adopted 6 mm$^2$ rings meet these conditions. Exactly two individually 13 A fused connections are allowed per ring; no extra unfused taps. The nominal leg-current solution is supplementary load-distribution evidence, not a protective-device $I_2$.')
body=body.replace(r'\subsection*{Small power and fixed equipment}',r'\input{lighting_basis.tex}'+'\n'+r'\subsection*{Small power and fixed equipment}')
body=body.replace(r'\subsection*{Protection and board arrangement}',r'\input{installation_notes.tex}'+'\n'+r'\subsection*{Protection and board arrangement}')
body=body.replace('earlier','earlier')
# Persistent frame on continuation pages, matching the original table edges.
frame=r'''\AddToShipoutPictureBG{\AtPageLowerLeft{\put(72.264,92.904){\linethickness{0.48bp}\framebox(450.916,649.156){}}\put(72.024,759){\fontsize{12}{14}\selectfont\bfseries BSE3124 -- Group 1 technical continuation}}}
'''
# Clear continuation furniture before mixed-size drawing appendices.
body=body.replace(r'\includepdf[pages=-,fitpaper=true]{assets/task1-drawings.pdf}',r'\clearpage\ClearShipoutPictureBG\includepdf[pages=-,fitpaper=true]{assets/task1-drawings.pdf}')
detail=O/'assets/installation-details.pdf'
if detail.exists():body=body.replace(r'\end{document}',r'\includepdf[pages=-,fitpaper=true]{assets/installation-details.pdf}'+'\n'+r'\end{document}')
parts.extend([frame,body])
(O/'main.tex').write_text(''.join(parts).replace('}\\n','}\n'),encoding='utf8')
lr=list(csv.DictReader((D/'final_lighting_basis.csv').open()))
t=r'''\subsection*{Final lighting selection basis}
Use the final device table (92 panels, 2216 W), not legacy candidate schedules. Manufacturer LDT intensity is in cd/klm; scale by each selected setting's flux (22 W: 2843.45 lm; 28 W: 3555.30 lm). Integrating the intensity distribution confirms the parser's normalisation. At each 0.2 m grid cell, sum $E=I(C,\gamma)\cos\gamma/d^2$ and apply MF 0.80. No reflected-light contribution is counted.

Adopt 1.9 m between luminaires and the task plane, e.g. 2.7 m ceiling and 0.8 m workplane. Heights, periodic cleaning/replacement supporting MF, and room envelopes are explicit course assumptions. The connected main-office region and three side-room envelopes are drawn from retained geometry screens; their summed area is not the separate 309 m$^2$ UFA assumption. Lamps from other rooms are excluded.
\begin{center}\begin{tabular}{lrrrr}\toprule
Zone & Lamps & Area m$^2$ & Mean lx & Min/mean\\\midrule
'''
for r in lr:
 if r['height_above_workplane_m']=='1.9':t+=' & '.join([r['zone'],r['lamp_count'],f"{float(r['area_m2']):.2f}",r['mean_maintained_direct_lx'],r['min_mean']])+r'\\'+'\n'
t+=r'''\bottomrule\end{tabular}\end{center}
All four adopted mean values meet the course target of 500 lx. At 2.2 m above the task plane, the means become 573.0, 505.8, 545.0 and 447.2 lx respectively. Therefore the south east room requires a height no greater than 1.9 m for this selection; do not assume 2.2 m is acceptable. Its margin is small, and changed dimensions or maintenance assumptions require recalculation.

Low perimeter minimum/mean ratios are disclosed, not called a uniformity pass. This average-illuminance selection check does not establish glare, furniture-shadow performance or maintained task-area uniformity. Those are distinct from the present course assumption. Reproduce with \texttt{final\_lighting\_basis.py}; the final lamp powers and counts are checked against the common table.
'''
(O/'lighting_basis.tex').write_text(t)
(O/'installation_notes.tex').write_text(r'''\subsection*{FCU and containment details}
Every FB01--FB09 assembly shares one 13 A FCU upstream of all four socket ways. Each twin SO01--SO03 likewise shares one 13 A FCU; FS01 has its own switched 13 A FCU. Terminate ring/main L/N/CPC in an accessible junction assembly rated for 6/10 mm$^2$ cables. Put the FCU at the tap before the 4 mm$^2$ local spur; its neutral is switched with line, and PE is continuous. A fuse permits transient overcurrent: 13 A is the intended continuous capacity, not an instantaneous clamp. No additional unrecorded points are allowed without recalculation.

Containment banks: lighting LC-A--G (seven circuits, $C_g=0.54$); A: P1/P2 (four ring legs, 0.65); B: P3/P4 (four ring legs, 0.65); C: P5/P6/P8 (three radials, 0.70); P7 alone (1.00); incoming feeder alone (1.00). Co-located plan paths show routing corridors, not a shared enclosure. Provide separate Method B runs with horizontal clear space exceeding twice the largest adjacent overall cable diameter between groups, using EMSD A5(3), Note 2; where enclosure dimensions govern, space the enclosures at least as conservatively and confirm the cable separation. Do not treat a mere partition in one warm trunking as thermal separation. Each individual circuit's L/N/CPC stays together. Avoid thermal insulation contact. If these conditions cannot be achieved, regroup and resize before installation.
''')
contract=dict(source=str(docx),source_sha256=hashlib.sha256(docx.read_bytes()).hexdigest(),background_sha256=hashlib.sha256(template.read_bytes()).hexdigest(),pages=5,page_bp=[595.32,841.92],method='Original Word-exported PDF pages retained at native size; editable LaTeX overlays. This is a hybrid facsimile, not a fully native re-typesetting of original labels.',slots={'1':'Group/name blanks','2':'Answer below y153bp','3':'Answer below y181bp','4':'Demand y139..365bp; cable y402..735bp','5':'Blank area beside original sideways board; original graphic preserved'},continuation='Original frame geometry repeated; additional pages and A3 drawings intentionally extend the original template.')
(O/'template_contract.json').write_text(json.dumps(contract,indent=2))
(O/'artifact.md').write_text('# Template fidelity contract\n\nReference: '+str(docx)+'\n\nFive original Word-exported pages are the immutable background. Page geometry 595.32 x 841.92 bp; Times New Roman body12, headings12 bold, title14.04 bold. Answer frames x72.024..523.420, y99.620..749.256 bp from top. No headers/footers added to original pages. Page5 retains the embedded sideways board graphic. Source text, lines and image are preserve-only; group/name blanks and empty answer space are editable. Full measurements/hashes and slot map: template_contract.json.\n\nThe blank LaTeX compilation must match all five original page renders; filled overlays may only change answer slots. Continuation pages are intentional additions with the same frame. Original labels remain embedded PDF content rather than editable TeX; all new answers are editable TeX.\n')
print('Generated v04 editable overlays, blank facsimile, continuation and template contract')
