"""Add a native editable installation detail sheet to a versioned DWG copy.
Uses AutoCAD 2027 Core Console; never accesses or closes a live user document.
"""
from pathlib import Path
import shutil,subprocess,json,hashlib
R=Path(__file__).resolve().parents[2];Q=R/'04_Design_Outputs/qa/revision_v04';Q.mkdir(exist_ok=True)
src=R/'04_Design_Outputs/cad/assignment_submission_v01.dwg';dst=R/'04_Design_Outputs/cad/assignment_submission_v02.dwg'
pdf=R/'04_Design_Outputs/submission/latex_v04/assets/installation-details.pdf'
assert not dst.exists(),'Do not overwrite a previously authored revision'
digest=hashlib.sha256(src.read_bytes()).hexdigest();shutil.copy2(src,dst)
script=[f'(if (/= (strcase (strcat (getvar "DWGPREFIX") (getvar "DWGNAME"))) (strcase "{dst.as_posix()}")) (progn (princ "WRONG_DRAWING") (quit)))',
 '(setvar "FILEDIA" 0)','(setvar "CMDDIA" 0)','(setvar "BACKGROUNDPLOT" 0)',
 '(command "_.-LAYOUT" "_Copy" "TASK2-DB-SCHEMATIC" "DESIGN-DETAILS")','(setvar "CTAB" "DESIGN-DETAILS")',
 '(setq ss (ssget "_X" (list (cons 410 "DESIGN-DETAILS") (cons 67 1))))',
 '(if ss (repeat (sslength ss) (setq en (ssname ss 0)) (ssdel en ss) (if (/= (cdr (assoc 0 (entget en))) "VIEWPORT") (entdel en))))',
 '(if (not (tblsearch "LAYER" "E-REV04-DETAIL")) (entmake (list (cons 0 "LAYER") (cons 2 "E-REV04-DETAIL") (cons 70 0) (cons 62 7))))',
 '(setq revhandles nil)',
 '(defun rt (s x y w h / e) (setq e (entmakex (list (cons 0 "MTEXT") (cons 100 "AcDbEntity") (cons 67 1) (cons 410 "DESIGN-DETAILS") (cons 8 "E-REV04-DETAIL") (cons 100 "AcDbMText") (cons 10 (list x y 0.0)) (cons 40 h) (cons 41 w) (cons 71 1) (cons 7 "T1-Arial") (cons 1 s)))) (setq revhandles (cons (cdr (assoc 5 (entget e))) revhandles)))',
 '(defun rl (x y xx yy / e) (setq e (entmakex (list (cons 0 "LINE") (cons 100 "AcDbEntity") (cons 67 1) (cons 410 "DESIGN-DETAILS") (cons 8 "E-REV04-DETAIL") (cons 100 "AcDbLine") (cons 10 (list x y 0.0)) (cons 11 (list xx yy 0.0))))) (setq revhandles (cons (cdr (assoc 5 (entget e))) revhandles)))']
def txt(s,x,y,w=390,h=3):script.append(f'(rt {json.dumps(s)} {x} {y} {w} {h})')
def line(x,y,xx,yy):script.append(f'(rl {x} {y} {xx} {yy})')
txt('OFFICE 1 | INSTALLATION DETAILS AND DESIGN CONDITIONS | REV 04',12,285,390,4)
txt('Supplement to normal lighting/power plans and DB schematic. Native editable detail; schematic, not to scale.',12,276,390,2.7)
txt('1. EVERY POWER ASSEMBLY HAS ONE UPSTREAM 13A FCU',12,264,390,3.3)
# Three separate conductors; fuse and switched neutral, unswitched PE.
txt('Accessible main/ring junction',12,252,68,2.6)
txt('13A switched FCU at tap',105,252,83,2.6)
txt(r'4mm2 L/N/CPC spur\P0.5m assumed',202,252,75,2.6)
txt(r'ONE assembly: FB / SO / FS\PAll outlets share 13A continuous capacity',290,252,110,2.6)
for y,lab in [(236,'L'),(227,'N'),(218,'PE')]:
 txt(lab,12,y+2,10,2.5);line(24,y,105,y)
 if lab=='L':
  line(105,y,115,y);line(115,y-2,135,y-2);line(115,y+2,135,y+2);line(115,y-2,115,y+2);line(135,y-2,135,y+2);line(135,y,155,y);line(155,y,162,y+3);line(165,y,390,y)
 elif lab=='N':line(105,y,155,y);line(155,y,162,y+3);line(165,y,390,y)
 else:line(105,y,390,y)
line(160,227,160,236)
script.append('(setq me (entlast) md (entget me))')
script.append('(entmod (append md (list (cons 6 "DASHED") (cons 48 0.2))))')
txt('For rings: both L/N/CPC ends return to their own DB terminals. FCU is before the spur; no unfused extra taps. Main terminals must accept 6/10mm2.',12,208,390,2.6)
txt('FB01-09: one FCU per four-socket floorbox. SO01-03: one FCU per twin socket. FS01: one switched FCU. 13A is not an instantaneous current clamp.',12,198,390,2.6)
txt('2. SEPARATE CONTAINMENT BANKS - OVERLAPPING PLAN LINES ARE ROUTING CORRIDORS',12,183,390,3.1)
banks=[('Lighting LC-A..G','7 circuits / Cg0.54'),('A: P1/P2','4 ring legs / Cg0.65'),('B: P3/P4','4 ring legs / Cg0.65'),('C: P5/P6/P8','3 radials / Cg0.70'),('P7 alone','Cg1.00'),('Feeder alone','Cg1.00')]
for i,(a,b) in enumerate(banks):
 x=12+i*65
 for x1,y1,x2,y2 in [(x,165,x+59,165),(x,151,x+59,151),(x,151,x,165),(x+59,151,x+59,165)]:line(x1,y1,x2,y2)
 txt(a,x+2,162,57,2.3);txt(b,x+2,157,57,2.1)
txt('Method B, no insulation contact. Keep L/N/CPC of each circuit together. Between banks provide horizontal cable clearance >2x largest adjacent cable OD',12,144,390,2.6)
txt('(EMSD A5(3) Note2); separate enclosures and verify cable clearance. A partition alone is not thermal separation. If grouping changes, recalculate sizes.',12,134,390,2.6)
txt('3. A1 RING DESIGN BASIS AND CONDITIONAL EQUIPMENT SPECIFICATION',12,119,390,3.1)
txt('EMSD 6C/6E, Table6(1): B32; 6mm2 copper; corrected leg Iz23.1855A >=20A; each service envelope <=100m2; intact L/N/CPC rings; two fused taps per ring.',12,110,390,2.6)
txt('Nominal leg-current calculation14.658-15.203A is supplementary. No invented ring-leg protective-device I2. Verify ring continuity before energisation.',12,100,390,2.6)
txt('TN-S source Ze0.20ohm/PFC<=6kA are design conditions. Main and RCBO Icn10kA. Required total I2t: B10/B16<=70000; B32/FCU<=90000; C63<=1000000 A2s.',12,90,390,2.6)
txt('These are apparatus selection requirements, not manufacturer certificates. Control20AX/LED>=600W; confirm driver inrush. PE bypasses switching.',12,80,390,2.6)
txt('4. FINAL LIGHTING BASIS - COURSE GEOMETRY AND HEIGHT ASSUMPTIONS',12,65,390,3.1)
txt('92 panels /2216W. Final LDT calculation, MF0.80, luminaires1.9m above workplane: mean direct lux open592.9 /pantry546.3 /upper east588.5 /south east502.9.',12,56,390,2.6)
txt('South east: keep luminaire-to-workplane height <=1.9m; at2.2m mean447.2lx fails adopted500lx target. Low perimeter uniformity is disclosed, not certified.',12,46,390,2.6)
txt('No reflected-light credit. Room envelopes, height and maintenance are declared assumptions. See answer continuation for sensitivity and photometric limits.',12,36,390,2.6)
txt('GROUP 1 | BSE3124 | 2026-11-08 | DETAILS / NTS | Read with Task1-3 answer v04',12,16,390,2.5)
script += [f'(setq f (open "{(R/"04_Design_Outputs/data/installation_detail_handles_v04.txt").as_posix()}" "w"))','(foreach h revhandles (write-line h f))','(close f)',
 f'(if (/= (strcase (strcat (getvar "DWGPREFIX") (getvar "DWGNAME"))) (strcase "{dst.as_posix()}")) (quit))',
 '(command "_.QSAVE")',
 f'(command "_.-PLOT" "_No" "DESIGN-DETAILS" "" "" "{pdf.as_posix()}" "_No" "_Yes")',
 '(princ "BSE_REV04_SAVED")']
# Normalise native Windows separators, and enclose ALL mutations in the guard.
script=[line for line in script if not line.startswith('(if (/= (strcase (strcat')]
guard='(= (strcase (vl-string-translate '+json.dumps('\\')+' "/" (strcat (getvar "DWGPREFIX") (getvar "DWGNAME")))) (strcase '+json.dumps(dst.as_posix())+'))'
script=['(if '+guard+' (progn']+script+[') (princ "WRONG_DRAWING_NO_WRITE"))']
scr=Q/'add_details.scr';scr.write_text('\n'.join(script)+'\n',encoding='ascii')
result=subprocess.run(['C:/Program Files/Autodesk/AutoCAD 2027/accoreconsole.exe','/i',str(dst),'/s',str(scr),'/l','en-US'],capture_output=True,timeout=120)
log=result.stdout.decode('utf-16le',errors='replace');(Q/'detail_console.log').write_text(log,encoding='utf8')
assert hashlib.sha256(src.read_bytes()).hexdigest()==digest
assert result.returncode==0 and 'BSE_REV04_SAVED' in log and '; error:' not in log.lower(),log[-2000:]
print(log[-2500:]);print('PDF exists:',pdf.exists())
