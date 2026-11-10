from cad_common import *
guard();doc.ActiveLayout=doc.Layouts.Item('TASK1-MAIN-SCHEMATIC');sp=doc.ActiveLayout.Block
old=json.loads((ROOT/'stage3_handles.json').read_text())
for h in old:guard();doc.HandleToObject(h).Delete()
(ROOT/'retired_stage3_handles.json').write_text(json.dumps(old))
for tag,x,floors in [('A',55,range(1,6)),('B',180,range(6,11))]:
    line(sp,(x,130),(x,151),WIRE);block(sp,x,151,'AECBS_UK_E_Circuitb',3.5,math.pi/2)
    line(sp,(x,151+1.9196283379151637*3.5),(x,247),WIRE)
    text(sp,x-40,258,118,'ZONE '+tag+' | FLOORS '+('1-5' if tag=='A' else '6-10'),2.6)
    text(sp,x-40,253,118,'1600 A rising main; floor MCCBs 400AF / 320AT',1.9)
    for j,floor in enumerate(floors):
        y=176+j*16
        circle(sp,x,y,.6,WIRE);line(sp,(x,y),(x+7,y),WIRE)
        block(sp,x+7,y,'AECBS_UK_E_Circuitb',3)
        line(sp,(x+7+1.9196283379151637*3,y),(x+65,y),WIRE)
        text(sp,x-14,y+2,12,'F'+str(floor),2.4)
        for k in range(3):
            xx=x+23+k*19;yy=y-5
            circle(sp,xx,y,.45,WIRE);line(sp,(xx,y),(xx,yy+.34601492740721573*6),WIRE)
            block(sp,xx,yy,'AECBS_UK_E_Meter',6)
            line(sp,(xx,yy-.34601492740721573*6),(xx,yy-4),WIRE)
            text(sp,xx-5,yy-4.4,16,'O'+str(k+1),1.7)
    text(sp,x+7,160,66,'Riser: MTZ2 16H1, Ir 1440 A',1.8)
    xx=x+58;line(sp,(xx,130),(xx,124),WIRE)
    block(sp,xx,124,'AECBS_UK_E_Circuitb',3.5,-math.pi/2)
    line(sp,(xx,124-1.9196283379151637*3.5),(xx,115),WIRE)
    text(sp,xx-15,113,37,'PLANT / PUBLIC\P800AF / 720AT\P392.244 kVA*',2.0)
rect(sp,278,57,130,195)
text(sp,282,248,122,'OFFICE 1 | FROM ITS FLOOR METER',2.6)
x=300
line(sp,(x,235),(x,224+.34601492740721573*10),WIRE);block(sp,x,224,'AECBS_UK_E_Meter',10)
line(sp,(x,224-.34601492740721573*10),(x,196+1.9196283379151637*4),WIRE);block(sp,x,196,'AECBS_UK_E_Circuitb',4,math.pi/2)
text(sp,313,227,87,'Office 1 tenant meter',2.6)
text(sp,313,205,88,'MS-O1 | C63, 4P\PA9F54463 | 10 kA',2.5)
line(sp,(x,196),(x,155),WIRE)
text(sp,313,184,88,'4C35 mm2 PVC Cu\P+ CPC16 mm2\P31.512 m design length',2.7)
rect(sp,289,117,108,38)
text(sp,294,151,99,'DB-O1 | 100 A, 4P isolator\P15 outgoing RCBO circuits\P7 lighting + 8 small power\PIb(max phase) = 48.600 A',2.7)
line(sp,(x,117),(x,102),WIRE)
text(sp,313,111,84,'P7: WH01 via FS01\PSHC10 GB | 1.4 kW\PB10 / 10 A DP FCU',2.4)
text(sp,283,88,120,'TN-S; dedicated N and PE. PE bypasses switching.\PDesign source: Ze = 0.20 ohm; PFC <=6 kA at MS-O1; upstream drop allowance <=2.2 V.',2.3)
text(sp,12,47,247,'* Per section: AC 292.244 + public services 100 = 392.244 kVA before the 1.1 zoning factor.',2.1)
for h,tag in [('8177','A'),('8185','B')]:
    settext(h,'ACB-'+tag+r'\PMTZ2 25H1\P2500AF / 2250AT',h=2.1,w=46)
settext('818E',r'SYSTEM BASIS\PMSB fault-duty design bound 46.43 kA: uk=6%, -10% tolerance, c=1.1; non-parallel transformers. Main/riser ACBs 66 kA; floor/plant MCCBs 50 kA. AF=frame; AT=long-time setting. Utility HV protection and approved transformer supply follow COP101.',h=2.2)
finish('3')
