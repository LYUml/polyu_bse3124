"""Rev03 native CAD schematic. Replaces only the named layout; preserves originals.

Run once after the selection data is reviewed. Every native mutation is guarded.
"""
from cad_common import *

guard()
doc.ActiveLayout = doc.Layouts.Item('TASK1-MAIN-SCHEMATIC')
sp = doc.ActiveLayout.Block
retired=[]
for i in range(sp.Count-1,-1,-1):
    e=sp.Item(i)
    if e.ObjectName!='AcDbViewport':
        retired.append(e.Handle);guard();e.Delete()
(ROOT/'rev03_retired_main_handles.json').write_text(json.dumps(retired,indent=2))

def wire(*points):
    for a,b in zip(points,points[1:]):line(sp,a,b,WIRE)
def dot(x,y):circle(sp,x,y,.5,WIRE)
def breaker(x,y,vertical=True,size=2.5):
    # Existing UK CAD breaker symbol, correct pin-to-pin span.
    block(sp,x,y,'AECBS_UK_E_Circuitb',size,math.pi/2 if vertical else 0)
    return 1.9196283379151637*size
def note(x,y,w,s,h=2):text(sp,x,y,w,s,h)

rect(sp,8,8,404,281)
note(12,285,394,'TASK 1 | MAIN DISTRIBUTION, PROTECTION AND METERING',3.6)
note(12,277,394,'REV03 | 380/220 V, 3-phase 4-wire + PE | Single-line diagram, not to scale | Normal supply only',2.2)
line(sp,(12,272),(408,272))

# The two independently fed transformers and customer main circuit breakers.
for tag,x in [('A',43),('B',177)]:
    note(x-25,268,111,'TX-'+tag+' | CLP 1500 kVA',2.5)
    wire((x,258),(x,255));circle(sp,x,251,4);circle(sp,x,245,4)
    wire((x,241),(x,232))
    circle(sp,x,235,1.5)
    breaker(x,226,True,3.125)
    wire((x,226),(x,211));dot(x,211)
    note(x+9,254,84,'Utility HV protection\P11 kV / 380 V\Puk = 6% assumed',1.85)
    note(x+9,236,87,'ACB-'+tag+' | 4P draw-out\PMTZ2 25H1 / 6.0X LSIG\P2500AF; Ir 2250 A; 66 kA',1.85)
    note(x+9,223,88,'4-pole sensors > LSIG > trip\PIsd 4500 A; tsd 0 s; I2t OFF\PIg 500 A; tg 0.2 s, I2t OFF',1.75)

# Section buses and a normally-open 4-pole coupler.
wire((20,211),(110,211));wire((132,211),(266,211))
wire((110,211),(116,211));breaker(116,211,False,3.125);wire((122,211),(132,211))
note(109,207,54,'BC | 4P, N.O.\P2500AF / 2250AT\PMTZ2 25H1, 66 kA',1.75)
note(14,203,88,'MSB-A | 2500 A section',2)
note(172,203,95,'MSB-B | 2500 A section',2)

# Riser protection; normal floor allocation remains unchanged.
for tag,x,first in [('A',26,1),('B',160,6)]:
    wire((x,211),(x,195));breaker(x,190,True,2.6)
    wire((x,190),(x,64))
    note(x+8,194,47,tag+'-FL | 1600AF\PIr 1440 A; 66 kA\PKTC2500 busway',1.65)
    for j in range(5):
        y=174-j*22;f=first+j
        dot(x,y);wire((x,y),(x+8,y));breaker(x+8,y,False,2.1)
        wire((x+12.03122,y),(x+105,y))
        note(x-11,y+2,10,'F'+str(f),2)
        note(x+16,y+4.8,92,'400AF / Ir 320 A, 4P, 70 kA',1.65)
        for k in range(3):
            xx=x+36+k*29
            dot(xx,y);wire((xx,y),(xx,y-3))
            breaker(xx,y-7,True,2.084)
            if k<2:
                wire((xx,y-7),(xx,y-10))
                block(sp,xx,y-12,'AECBS_UK_E_Meter',5.78)
                wire((xx,y-14),(xx,y-16))
                note(xx+4,y-10.5,14,'O'+str(k+1),1.65)
            else:
                wire((xx,y-7),(xx,y-16));circle(sp,xx,y-11,1)
                wire((xx+1,y-11),(xx+8,y-11))
                block(sp,xx+10,y-11,'AECBS_UK_E_Meter',5.78)
                note(xx-10,y-10,9,'O3',1.65)
                note(xx+7,y-14.5,14,'CT',1.5)
    # Plant feeder separate from floor-riser protection.
    px=x+58
    dot(px,211);wire((px,211),(px,199));breaker(px,195,True,2.084)
    note(px+5,192,43,tag+'-PL | 800/720 A\P4P, 70 kA\PPlant / public',1.5)
    wire((px,195),(px,188))
    note(x+12,67,108,'TPN MCCB BEFORE each tenant meter:\PO1/O2 100 A; O3 125 A + CT meter.\PF1/O1 63 A; all tenant MCCBs70 kA.',1.7)

# Right-hand tenant detail: protection and isolation ahead of utility metering.
rect(sp,278,132,130,136)
note(283,264,120,'F1 / OFFICE 1 | DETAILED FEEDER',2.5)
wire((292,252),(292,240));breaker(292,234,True,3.125)
note(303,250,98,'From F1 320 A floor MCCB\PMS-O1: ComPacT NSX100H\PC10H4TM063, 4P4D TM63D\PIr 63 A; Icu/Ics 70 kA\PSuitable for isolation',2)
wire((292,234),(292,221))
block(sp,292,217,'AECBS_UK_E_Meter',10)
wire((292,213.53985),(292,177))
note(303,221,98,'CLP tenant meter\PImmediately after MS-O1',2)
note(303,204,97,'4C35 mm2 PVC Cu\P+ separate CPC16 mm2\PL = 31.5119 m\P28.5119 plan + 3 m allowance',2)
rect(sp,285,153,115,24)
note(289,174,107,'DB-O1: 100 A 4P isolator\P15 x 1P+N Type A 30 mA RCBO\P7 lighting + 8 power circuits',2.2)
note(283,146,120,'PE continuous; neutral switched with phases.\PNo customer N-PE link at DB.',1.9)

# Explicit break-before-make interlock and load transfer condition.
rect(sp,278,61,130,67)
note(283,124,120,'ACB-A / ACB-B / BC INTERLOCK',2.35)
note(283,116,120,'Electrical AND mechanical interlock\PNormal:             CLOSED / CLOSED / OPEN\PTransfer from A: CLOSED / OPEN / CLOSED\PTransfer from B: OPEN / CLOSED / CLOSED\PALL THREE CLOSED: PROHIBITED',1.85)
note(283,92,120,'Open/isolate failed incomer before closing BC.\PBefore transfer, shed load to <=1480.9 kVA\P(2250 A at 380 V); no full-load N-1.\PUtility return: open BC before restoring incomer.',1.85)

# Earthing diagram, kept separate from the power conductors above.
line(sp,(12,57),(408,57))
note(14,53,91,'CUSTOMER EARTHING',2.3)
rect(sp,15,28,35,12);note(19,36.5,28,'MET',2.5)
wire((32,28),(32,21));line(sp,(26,21),(38,21));line(sp,(28,19),(36,19));line(sp,(30,17),(34,17))
note(43,22,80,'Own electrode',1.8)
wire((50,34),(62,34),(62,44),(100,44));wire((62,34),(100,34));wire((62,34),(62,24),(100,24))
note(103,47,162,'MSB enclosures / continuous riser PE',1.85)
note(103,37,162,'DB PE bar / all circuit CPCs (unswitched)',1.85)
note(103,27,162,'Main equipotential bonding to services',1.85)
note(283,53,120,'BASIS AND FAULT DUTY',2.2)
note(283,46,120,'CLP GuideToSupply v10: sections 2, 3, 7.4, 11.\PMSB PFC <=56.92 kA incl. transfer motors.\POwn MET/electrode; any CLP bond only by\Pagreement, >=70 mm2 Cu. See Task 3 for\Ploop, disconnection and conductor checks.\PCT meters: CLP ratios +16 A HRC voltage\Pfuses; Guide sections9.11 and9.16.',1.75)
note(14,13,392,'2672.216 kVA building demand | 1336.108 kVA / 2030 A per normal section | CT/sensor arrangement subject to CLP acceptance',1.8)
finish('rev03_main')
