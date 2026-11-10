from cad_common import *

m=doc.ModelSpace
guard();doc.ActiveLayout=doc.Layouts.Item('TASK1-ROOM-REVIEW');app.ZoomExtents();app.ZoomScaled(.9,1)
if sys.argv[1]=='panels':
    # Equipment internals are plan representations; the retained cabinet envelope is a design dimension.
    for i,(h,x,label) in enumerate(zip(['77DB','77DD','77DF','77E1','77E3','77E5'],[10000,11140,12280,13420,14560,15700],['A-IN','A-FL','A-PL','B-IN','B-FL','B-PL'])):
        settext(h,label,(x+110,24445.584),950,150)
        rect(m,x+65,23120.584,1010,880)
        line(m,(x+100,23205.584),(x+1040,23205.584))
        # Front door, handle and rear busbar compartment.
        rect(m,x+900,23135.584,95,35)
        line(m,(x+100,23885.584),(x+1040,23885.584))
        if i%3==0:
            rect(m,x+300,23355.584,537,300)
            block(m,x+570,23405.584,'AECBS_UK_E_Circuitb',105,math.pi/2)
            block(m,x+160,23600.584,'AECBS_UK_E_Meter',180)
        elif i%3==1:
            for j in range(5):
                xx=x+125+j*190
                rect(m,xx,23400.584,140,300)
                block(m,xx+70,23445.584,'AECBS_UK_E_Circuitb',105,math.pi/2)
        else:
            rect(m,x+310,23355.584,520,380)
            block(m,x+570,23400.584,'AECBS_UK_E_Circuitb',130,math.pi/2)
        text(m,x+80,22955.584,1100,['2500A ACB','5 FLOOR MCCBs','800A MCCB'][i%3],110)
    text(m,10000,25065.584,7000,'MSB-A / MSB-B | 2500 A independent bus sections',170)
    # HV front-panel single-line mimic, operating handle and cable terminations.
    for j,x in enumerate([10000,11000,12000]):
        # Existing small panels already occupy the centre: add functional symbols within them.
        xx=x+500
        line(m,(xx,18955.584),(xx,19055.584))
        block(m,xx,19055.584,'AECBS_UK_E_Circuitb',150,math.pi/2)
        line(m,(xx,19343.528),(xx,19405.584))
        circle(m,xx+220,19025.584,35)
    settext('80B2','IN',(10180,19705.584),650,120)
    settext('80B4','TX-A',(11180,19705.584),650,120)
    settext('80B6','TX-B',(12180,19705.584),650,120)
    settext('8029',r'CAPACITY AND EQUIPMENT\PTX-A/B: CLP 1500 kVA distribution transformer type; 3000 kVA installed, 2672.216 kVA demand. No full-load N-1.\PHV-01: incomer + two transformer protection panels.\PMSB-A/B: 2500 A sections. IN: MTZ2 25H1 ACB; FL: five floor MCCBs; PL: plant/public MCCB.\PPlan outlines are installation design dimensions; utility equipment supply follows COP101 responsibilities.')
    finish('panels')
elif sys.argv[1]=='vent':
    for tag,x in [('A',15800),('B',19500)]:
        y=16505.584
        circle(m,x,y,85)
        for k in range(4):
            a=k*math.pi/2
            p1=(x+85*math.cos(a),y+85*math.sin(a))
            p2=(x+285*math.cos(a+.35),y+285*math.sin(a+.35))
            p3=(x+190*math.cos(a+.85),y+190*math.sin(a+.85))
            line(m,p1,p2);line(m,p2,p3);line(m,p3,p1)
        # High-level exhaust duct in plan; no obstruction of low-level door opening.
        rect(m,x-450,16005.584,900,815)
        line(m,(x,16300.584),(x,15910.584))
        line(m,(x,15910.584),(x-65,16040.584));line(m,(x,15910.584),(x+65,16040.584))
        text(m,x-700,17405.584,1600,'EF-'+tag+' | HIGH LEVEL',120)
        text(m,x-700,17225.584,1600,'630 / 30 deg / 4500 m3/h',100)
    for tag,x in [('A',13600),('B',17350)]:
        for k in range(1,6):line(m,(x+k*100,16005.584),(x+k*100-55,16205.584))
        text(m,x-120,16555.584,1050,'IL-'+tag,130)
        text(m,x-120,16375.584,1050,'600 x 2000H',100)
    settext('802C',r'VENTILATION\PEF-A/B: COP101 v16 6.6 type 630 mm / 30 deg / 700 rpm; each 4500 m3/h at 70 Pa, <=58 dB(A) at 1 m.\PDesign heat: 2 x 15 kW x 1.25 = 37.5 kW. Combined 9000 m3/h gives 12.44 K air rise.\PIL-A/B: each 600 W x 2000H, minimum 50% free area; combined 1.20 m2 >=1.12 m2.\PHigh-level ducts: 900 x 750 mm; discharge >=2.5 m above street, away from people. See ventilation calculation.')
    settext('79DF',r'EF-A/B: 630 mm / 30 deg / 700 rpm; 4500 m3/h at 70 Pa each, COP101 v16 6.6.\PIL-A/B: 600 x 2000H; 50% minimum free area.\P900 x 750 high-level exhaust ducts; discharge >=2.5 m above street. See ventilation calculation for heat and pressure checks.')
    settext('802F',r'CLP COP215 Rev07; COP101 v16, 4.3 and 6.1-6.7.\PEquipment selections and calculations accompany this drawing.')
    finish('vent')
