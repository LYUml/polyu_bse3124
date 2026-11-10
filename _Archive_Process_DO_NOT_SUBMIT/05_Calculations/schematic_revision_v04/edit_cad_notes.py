from cad_common import *
changes=[]
def replace(handle,t,**kw):
    e=doc.HandleToObject(handle);old=e.TextString
    settext(handle,t,**kw);changes.append(dict(handle=handle,before=old,after=t))
replace('79D1',r'PROPOSED\PLV ACCESS\P3000 mm\PCLEAR WIDTH',h=150,w=2600)
arrows=json.loads((ROOT/'data/access_clarity_revision.json').read_text())['arrow_handles']
deleted=[]
for h in arrows:
    guard();e=doc.HandleToObject(h)
    assert e.ObjectName=='AcDbLine' and e.Layer=='E-ACCESS-CLEARANCE'
    deleted.append(dict(handle=h,start=list(e.StartPoint),end=list(e.EndPoint)))
    guard();e.Delete()
replace('8030','LINE KEY: dashed line = HV trench; solid line = LV route; dashed box = delivery clearance. Equipment details diagrammatic.')
replace('7BBA',r'PROPOSED LOCATION\PSubstation: 12430 x 5450 mm.\PAdjacent LV room: 12430 x 3500 mm (proposed).\PSee 1:75 plantroom detail.')
replace('7BBB',r'LOCATION REASONS\PExternal plant access.\PShort transformer-to-incomer interfaces.\PSeparation from lift/stair/AHU core.\PIndependent west entrance to LV room.')
replace('7BBD',r'SITE COORDINATION\PConfirm external access, >=3 m clear delivery route and unloading within20 m.\PCoordinate openings, structure, flood/fire provisions and supplier equipment dimensions.')
replace('8029',r'EQUIPMENT\PTX-A/B: CLP1500 kVA each; demand2672.216 kVA.\PHV-01: incomer + two transformer protection panels.\PMSB: two2500 A sections, seven1140 mm bays.\PBC: normally-open4P end coupler with segregated rear links. See main schematic for interlocking.')
replace('802A',r'CLEARANCES / BUILDING WORKS\PHV: rear1000, front1800, sides750 mm.\PTX: LV terminals900, other sides750 mm.\PLV board: front1500, rear990 mm; total width7980 mm.\PProposed2 h FRR partitions, sealed penetrations and FFL150 mm above external level.')
replace('802B',r'ACCESS AND DOORS\PProposed south delivery access: >=3000 mm clear route; unloading within20 m.\PHV opening4000 mm; TX openings3000 mm each; proposed height2800 mm.\POutward-opening doors shown at90 degrees; adjacent doors used sequentially.\PTX-A wicket access; independent west LV entrance.')
replace('802C',r'VENTILATION\PEF-A/B:630 mm /30 deg /700 rpm; each4500 m3/h at70 Pa; <=58 dB(A) at1 m (COP101 6.6).\PIL-A/B:600 x2000H mm, >=50% free area; total1.20 m2.\PHigh-level ducts:900 x750 mm; discharge >=2.5 m above street. Thermal calculation: Task1.')
replace('7FED','Calculated ring-leg current14.658-15.203 A. Verify L/N/CPC continuity; A1 overload conditions apply.')
replace('7FEE','Protection: NSX100H TM63D70 kA; RCBO backup per Schneider A-198. Task3 gives fault, earth-loop and total-energy checks.')
replace('7FEF','Controls:20 AX, LED>=600 W; verify driver inrush. PE remains continuous.')
replace('7FF1','LIGHTING:92 panels /2256 W. LDT results and maintained-illuminance assumptions: Task2.')
replace('7FF2','South-east room: four38 W panels; 589.2 lx mean at2.2 m above workplane.')
replace('7C30','MS-O1: NSX100H TM63D70 kA before meter. DB assembly>=25 kA; RCBO backup per Schneider A-198. Protection checks: Task3.')
replace('7DB0','S-A/B/C in separate phase enclosures. Manual controls20 AX /LED>=600 W; verify driver inrush.')
replace('7DC0','Full MS-O1-to-DB route: see incoming-route and ring-detail sheet.')
replace('7DDD','Full MS-O1-to-DB route: see incoming-route and ring-detail sheet.')
for h in ['7BF0','7BF3']:replace(h,r'PROPOSED MS-O1\P63 A /4C35 +CPC16')
# Update the visible release label, without regenerating any schematic geometry.
for name in ['TASK1-MAIN-SCHEMATIC','REV03-ROUTE-AND-RING']:
    sp=doc.Layouts.Item(name).Block
    for n in range(sp.Count):
        e=sp.Item(n)
        if e.ObjectName=='AcDbMText' and 'REV03 |' in e.TextString:
            replace(e.Handle,e.TextString.replace('REV03 |','REV04 |'))
finish('rev04_editorial')
(ROOT/'cad_editorial_changes.json').write_text(json.dumps(dict(text_changes=changes,removed_delivery_arrow_segments=deleted,fan_airflow_arrows_preserved=True,door_arcs_preserved=True,clearance_boundaries_preserved=True),indent=2))
x=json.loads((ROOT/'data/access_clarity_revision.json').read_text());x.update(arrow_handles=[],arrow_direction=None,purpose='Delivery clearance shown by dashed boundary and labels; direction arrows removed in Rev04');(ROOT/'data/access_clarity_revision.json').write_text(json.dumps(x,indent=2))
print('Removed',len(deleted),'delivery-arrow line segments; edited',len(changes),'labels')
