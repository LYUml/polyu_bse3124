"""Add an end-mounted bus-coupler bay without changing transformer/access envelopes."""
from cad_common import *
import csv
guard();m=doc.ModelSpace
x=16840;y=23055.584
rect(m,x,y,1140,1010)
rect(m,x+65,y+65,1010,880)
line(m,(x+100,y+150),(x+1040,y+150))
line(m,(x+100,y+830),(x+1040,y+830))
rect(m,x+900,y+80,95,35)
rect(m,x+300,y+300,537,300)
block(m,x+570,y+350,'AECBS_UK_E_Circuitb',105,math.pi/2)
text(m,x+110,24445.584,950,'BC / N.O.',150)
text(m,x+80,22955.584,1100,'2500A TIE ACB',110)
settext('8253',r'MSB-A / MSB-B\P2500 A sections\PBC: end-mounted\Psegregated rear links',(18150,24100.584),2600,140)
text(m,10000,24850.584,7800,'A-IN / B-IN / BC: electrical + mechanical interlock; break before make',135)
text(m,18150,23000.584,2600,'7 bays x 1140 = 7980\PFront aisle 1500\PRear aisle 990',130)
settext('8029',r'CAPACITY AND EQUIPMENT\PTX-A/B: CLP 1500 kVA; 3000 kVA installed, 2672.216 kVA demand. No full-load N-1.\PHV-01: incomer + two transformer protection panels.\PMSB: seven 1140 mm bays; 2500 A bus sections. BC: 4P normally-open end coupler, segregated insulated rear links to A/B.\PA-IN/B-IN/BC electrically and mechanically interlocked. Transfer after isolation and load shedding.\PInstallation envelopes are design assumptions, not certified manufacturer dimensions.')
finish('rev03_room')
p=ROOT/'data/task1_lv_board_envelope.csv'
with p.open(newline='',encoding='utf-8-sig') as f:
    r=csv.DictReader(f);fields=r.fieldnames;rows=list(r)
assert not any(r['section_id']=='LV-BC' for r in rows),'Already applied'
rows.append(dict(zip(fields,['LV-BC','Normally-open 4P bus coupler; segregated insulated rear bus links',1140,1010,2185,'same planning envelope; CLP GuideToSupply v10 section 3','design envelope; final assembly manufacturer verification',16840,23055.584,17980,24065.584])))
with p.open('w',newline='',encoding='utf8') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
(ROOT/'data/rev03_room_checks.json').write_text(json.dumps(dict(bays=7,width_mm=7980,room_width_mm=12430,front_clear_mm=1500,rear_clear_mm=990,east_clear_mm=3450,existing_transformer_tails_unchanged=True,bus_link_arrangement='End coupler with separately insulated A/B rear links within switchboard; assembly construction to be verified',basis='Layout envelope only; no unverified product envelope claimed'),indent=2))
