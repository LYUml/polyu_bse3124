from pathlib import Path
import json, math, sys, time
import win32com.client as wc
import pythoncom
import pywintypes

def retry(fn):
    for attempt in range(60):
        try:return fn()
        except pywintypes.com_error as e:
            if e.hresult not in [-2147418111,-2147417846]:raise
            time.sleep(.15)
    raise RuntimeError('AutoCAD remained busy')
class CAD:
    def __init__(self,obj):object.__setattr__(self,'obj',obj)
    def __getattr__(self,key):
        v=retry(lambda:getattr(self.obj,key))
        if isinstance(v,wc.dynamic.CDispatch):return CAD(v)
        if callable(v):
            def call(*args):
                z=retry(lambda:v(*[a.obj if isinstance(a,CAD) else a for a in args]))
                return CAD(z) if isinstance(z,wc.dynamic.CDispatch) else z
            return call
        return v
    def __setattr__(self,key,value):retry(lambda:setattr(self.obj,key,value.obj if isinstance(value,CAD) else value))

ROOT=Path(__file__).resolve().parent
DWG=ROOT/'BSE3124_Review.dwg'
app=CAD(wc.GetActiveObject('AutoCAD.Application'))
doc=app.ActiveDocument
def guard():
    assert Path(app.ActiveDocument.FullName).resolve()==DWG.resolve(), 'Wrong active DWG'
guard()
def pt(x,y,z=0): return wc.VARIANT(pythoncom.VT_ARRAY|pythoncom.VT_R8,[x,y,z])
def layer(name,color=7,weight=25):
    guard()
    try:l=doc.Layers.Item(name)
    except:l=doc.Layers.Add(name)
    l.Color=color;l.Lineweight=weight
    return name
NEW=layer('E-REV-EQUIPMENT',7,30)
TXT=layer('E-REV-TEXT',7,18)
WIRE=layer('E-REV-SLD',7,30)
created=[]
def mark(e,lay=NEW):
    e.Layer=lay;e.Color=256;created.append(e.Handle);return e
def line(sp,a,b,lay=NEW):
    guard();return mark(sp.AddLine(pt(*a),pt(*b)),lay)
def rect(sp,x,y,w,h,lay=NEW):
    guard();v=wc.VARIANT(pythoncom.VT_ARRAY|pythoncom.VT_R8,[x,y,x+w,y,x+w,y+h,x,y+h])
    e=mark(sp.AddLightWeightPolyline(v),lay);e.Closed=True;return e
def circle(sp,x,y,r,lay=NEW):
    guard();return mark(sp.AddCircle(pt(x,y),r),lay)
def text(sp,x,y,w,t,h=2.8,lay=TXT):
    guard();e=mark(sp.AddMText(pt(x,y),w,t),lay);e.Height=h;e.StyleName='T1-Arial';return e
def block(sp,x,y,name,s=1,rot=0):
    guard();return mark(sp.InsertBlock(pt(x,y),name,s,s,s,rot),WIRE)
def settext(handle,t,pos=None,w=None,h=None):
    guard();e=doc.HandleToObject(handle);e.TextString=t
    if pos:e.InsertionPoint=pt(*pos)
    if w:e.Width=w
    if h:e.Height=h
    e.Update()
def finish(stage):
    guard();doc.Regen(1);doc.Save()
    (ROOT/f'stage{stage}_handles.json').write_text(json.dumps(created,indent=2))
    print('SAVED',stage,doc.FullName,len(created))

if sys.argv[1]=='plan':
    doc.ActiveLayout=doc.Layouts.Item('TASK1-ROOM-REVIEW');app.ZoomExtents();app.ZoomScaled(.9,1)
    m=doc.ModelSpace
    # Preserve the dimensioned outer equipment extents and clearance geometry.
    for h in ['79BE','79C1','79C4']:
        guard();e=doc.HandleToObject(h);e.Layer=NEW;e.Color=256
    for tag,x,handle in [('TX-A',14700,'79C3'),('TX-B',18400,'79C6')]:
        y=18455.584
        rect(m,x+350,y+260,1500,1180)
        # Generic plan tank, radiator banks and north LV terminal box.
        for yy in range(350,1400,150):
            line(m,(x+60,y+yy),(x+350,y+yy));line(m,(x+1850,y+yy),(x+2140,y+yy))
        rect(m,x+750,y+1440,700,360)
        rect(m,x+350,y+750,260,380)
        text(m,x+850,y+1740,600,'LV',140)
        text(m,x+385,y+1020,300,'HV',115)
        block(m,x+1120,y+850,'AECBS_UK_E_transfmr',850)
        settext(handle,tag+' | 1500 kVA',(x+60,y-120),2900,170)
        text(m,x+60,y-370,2900,'2200 x 1800 mm',145)
        doc.Regen(1);time.sleep(.5)
    # HV switchboard compartment plan. Labels are functions, not invented ratings.
    for xx in [11000,12000]:line(m,(xx,18805.584),(xx,19805.584))
    for xx,lab in [(10000,'IN'),(11000,'TX-A'),(12000,'TX-B')]:
        rect(m,xx+160,18965.584,680,580)
        text(m,xx+250,19395.584,650,lab,150)
    settext('79C0','HV-01 | HV SWITCHGEAR',(10000,18655.584),3600,170)
    text(m,10000,18395.584,3400,'3000 x 1000 mm',145)
    settext('79C8','HV DELIVERY ACCESS\\P4000 mm opening')
    settext('79CA','TX-A DELIVERY ACCESS\\P3000 mm opening')
    settext('79CC','TX-B DELIVERY ACCESS\\P3000 mm opening')
    settext('79CE','EQUIPMENT PLAN SYMBOLS / CLEARANCE ENVELOPES\\PAdopted overall dimensions; internal details diagrammatic, not fabrication drawings.')
    settext('8029','CAPACITY AND EQUIPMENT\\PTX-A / TX-B: 1500 kVA each. Total 3000 kVA; design load 2672.216 kVA. No full-load N-1.\\PHV-01: 3000 x 1000 mm; TX-A/B: 2200 x 1800 mm.\\PEquipment is drawn as generic plan symbols. Overall dimensions remain adopted design assumptions; internal details are diagrammatic.')
    settext('802B','ACCESS AND DOORS\\PSouth external access assumed. Provide 3000-wide clear delivery route; unloading distance <=20 m to verify.\\PPlant doors: HV 4000 W; TX 3000 W each; 2800 H assumed. Outward opening, shown at 90 degrees.\\PAdjacent plant doors used sequentially; TX-A has wicket personnel access. Independent LV entrance west.')
    settext('802F','Basis: supplied COP215 Rev07; COP101 v16.\\PSee the new main distribution schematic for TX-A/B, MSB-A/B and floor supply zones.')
    settext('8030','LINE KEY: dashed = HV trench; solid = LV route; chain = clearance. Equipment details are diagrammatic.')
    # Link the six compartments to the system diagram without moving cabinets.
    for e in []:
        if e.ObjectName in ['AcDbText','AcDbMText']:
            try:t=e.TextString
            except:continue
            if t in ['A-1','A-2','A-3','B-1','B-2','B-3']:
                guard();e.TextString={'A-1':'A-IN','A-2':'A-FL','A-3':'A-PL','B-1':'B-IN','B-2':'B-FL','B-3':'B-PL'}[t]
    finish('1')

if sys.argv[1]=='sld-main':
    guard()
    try:
        old=doc.Layouts.Item('TASK1-MAIN-SCHEMATIC')
        doc.ActiveLayout=doc.Layouts.Item('TASK1-ROOM-REVIEW')
        old.Delete()
    except pywintypes.com_error:pass
    lay=doc.Layouts.Add('TASK1-MAIN-SCHEMATIC')
    lay.CopyFrom(doc.Layouts.Item('TASK2-DB-SCHEMATIC'))
    doc.ActiveLayout=lay
    sp=lay.Block
    text(sp,12,285,395,'TASK 1 | MAIN ELECTRICAL DISTRIBUTION SCHEMATIC',4)
    text(sp,12,277,395,'A3 LANDSCAPE | NOT TO SCALE | 2 x 1500 kVA | 380/220 V LV DESIGN BASIS',2.7)
    line(sp,(12,272),(408,272))
    text(sp,12,268,245,'NORMAL SUPPLY: 2672.216 kVA total; two independent LV sections.\\PEqual allocation: 1336.108 kVA / approx. 2030 A per section.',2.8)
    text(sp,280,268,128,'TYPICAL OFFICE 1 SUPPLY\\PSelected tenant detail; applicable to its floor supply zone.',2.8)
    # The reference drawing places transformers below the main switchboard.
    rect(sp,12,50,247,42);text(sp,15,89,230,'GROUND FLOOR | TRANSFORMER ROOM',2.6)
    rect(sp,12,97,247,49);text(sp,15,143,230,'GROUND FLOOR | MAIN LV SWITCH ROOM',2.6)
    for x,tag in [(55,'A'),(180,'B')]:
        text(sp,x+14,83,67,'TX-'+tag+' | 1500 kVA\\PLV 380/220 V\\P3-phase, 4-wire',2.6)
        block(sp,x,74,'AECBS_UK_E_transfmr',17,math.pi/2)
        line(sp,(x,74-(0.1656540622379712+0.2179975960063713)*17),(x,56),WIRE)
        text(sp,x-30,54.5,93,'HV feeder from HV-01',2.3)
        # Two-winding generic symbol has no asserted vector group.
        line(sp,(x,74+(0.1656540622379712+0.2179975960063713)*17),(x,105),WIRE)
        block(sp,x,105,'AECBS_UK_E_Circuitb',6,math.pi/2)
        text(sp,x+8,114,43,'ACB-'+tag+'\\PMain incomer',2.7)
        line(sp,(x,105+1.9196283379151637*6),(x,130),WIRE)
        e=line(sp,(x-26,130),(x+58,130),WIRE);e.Lineweight=60
        text(sp,x-25,126,90,'MSB-'+tag+' | SECTION '+tag,2.7)
        # Protective earth from transformer enclosure; N is kept distinct.
        line(sp,(x+7.0833,68),(x+24,68),WIRE)
        block(sp,x+24,65,'AECBS_UK_E_gnd',6)
        line(sp,(x+24,68),(x+24,65),WIRE)
        text(sp,x+28,68,45,'PE',2.1)
        doc.Regen(1)
    text(sp,123,121,42,'SEPARATE\\PLV SECTIONS\\PNo bus coupler',2.4)
    text(sp,12,39,247,'SYSTEM BASIS\\PHV supply voltage and upstream protection: utility interface. Capacities and LV voltage follow Task 1. Main ACB ratings/settings and fault duties require coordinated equipment selection. PE denotes equipment bonding; source earthing arrangement to be coordinated.',2.4)
    text(sp,12,17,247,'REFERENCE: Electrical Schematic 1 - transformer, main switchboard and floor-metering arrangement.\\PRead with the plantroom layout and Office 1 distribution-board schematic.',2.3)
    text(sp,280,35,128,'DESIGN LIMITS\\PNo full-load N-1. Central plant/public load is split equally as a design assumption. This sheet shows normal supply; emergency systems are separate.',2.4)
    text(sp,280,14,128,'GROUP 1 | E-04 | REV 01 | 10 NOV 2026',2.4)
    app.ZoomExtents();app.ZoomScaled(.9,1)
    finish('2')

if sys.argv[1]=='sld-feeders':
    doc.ActiveLayout=doc.Layouts.Item('TASK1-MAIN-SCHEMATIC');sp=doc.ActiveLayout.Block
    for x,tag,floors in [(55,'A',range(1,6)),(180,'B',range(6,11))]:
        # Normal office riser and representative floor take-offs.
        line(sp,(x,130),(x,151),WIRE)
        block(sp,x,151,'AECBS_UK_E_Circuitb',3.5,math.pi/2)
        line(sp,(x,151+1.9196283379151637*3.5),(x,244),WIRE)
        text(sp,x-39,249,120,'ZONE '+tag+' | FLOORS '+('1-5' if tag=='A' else '6-10'),2.8)
        for j,floor in enumerate(floors):
            y=169+j*16
            circle(sp,x,y,.65,WIRE)
            line(sp,(x,y),(x+21-.34601492740721573*7,y),WIRE)
            block(sp,x+21,y,'AECBS_UK_E_Meter',7)
            line(sp,(x+21+.34601492740721573*7,y),(x+52,y),WIRE)
            text(sp,x-16,y+2,15,'F'+str(floor),2.6)
            text(sp,x+28,y+6,48,'3 TENANTS',2.3)
        text(sp,x+2,164,87,'Floor metering shown collectively',2.0)
        # Separate branch for the plant/public service allocation.
        xx=x+58
        line(sp,(xx,130),(xx,124),WIRE)
        block(sp,xx,124,'AECBS_UK_E_Circuitb',3.5,-math.pi/2)
        line(sp,(xx,124-1.9196283379151637*3.5),(xx,115),WIRE)
        text(sp,xx-15,113,34,'PLANT / PUBLIC\\P392.244 kVA*',2.2)
    # Office inset is explicitly typical, not connected to both zones.
    rect(sp,278,57,130,195)
    text(sp,282,248,122,'FROM THE RELEVANT FLOOR METERING',2.6)
    x=300
    line(sp,(x,235),(x,224+.34601492740721573*10),WIRE)
    block(sp,x,224,'AECBS_UK_E_Meter',10)
    line(sp,(x,224-.34601492740721573*10),(x,196+1.9196283379151637*4),WIRE)
    block(sp,x,196,'AECBS_UK_E_Circuitb',4,math.pi/2)
    text(sp,313,227,87,'Office 1 tenant meter',2.6)
    text(sp,313,205,88,'MS-O1 | C63, 4P\\P10 kA specified',2.7)
    line(sp,(x,196),(x,155),WIRE)
    text(sp,313,184,88,'4C35 mm2 PVC Cu\\P+ CPC16 mm2\\P31.512 m design length',2.7)
    rect(sp,289,117,108,38)
    text(sp,294,151,99,'DB-O1 | 100 A, 4P isolator\\P15 outgoing RCBO circuits\\P7 lighting + 8 small power\\PIb(max phase) = 49.091 A',2.7)
    line(sp,(x,117),(x,102),WIRE)
    text(sp,313,111,84,'See detailed DB schematic\\Pand Office 1 layouts.',2.5)
    text(sp,283,88,120,'TN-S design assumption; dedicated N and PE. PE bypasses switching.\\PAt MS-O1: Ze = 0.20 ohm; PFC <=6 kA; upstream drop allowance <=2.2 V.',2.4)
    text(sp,12,47,247,'* Per section: AC 292.244 + public services 100 = 392.244 kVA before the 1.1 zoning factor.',2.1)
    finish('3')
