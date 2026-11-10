"""Native full-route locator and explicit ring-return detail, A3 landscape."""
from cad_common import *
name='REV03-ROUTE-AND-RING'
guard()
try:layout=doc.Layouts.Item(name)
except:guard();layout=doc.Layouts.Add(name);guard();layout.CopyFrom(doc.Layouts.Item('TASK1-MAIN-SCHEMATIC'))
layout=doc.Layouts.Item(name)
guard();doc.ActiveLayout=layout;sp=doc.ActiveLayout.Block
for j in range(sp.Count-1,-1,-1):
    e=sp.Item(j)
    if e.ObjectName!='AcDbViewport' or e.Width>30:guard();e.Delete()
rect(sp,8,8,404,281)
text(sp,12,284,395,'TASK 2 | FULL INCOMING ROUTE AND RING RETURN DETAIL',3.5)
text(sp,12,275,395,'REV03 | F1 / Office 1 | Locator viewport 1:170; electrical detail not to scale',2.4)
guard();vp=sp.AddPViewport(pt(113,171),202,180);guard();vp.Layer='E-T1-VPORT-NOPLOT';guard();vp.Display(True)
guard();vp.Direction=pt(0,0,1);guard();vp.Target=pt(79200,28500);guard();vp.CustomScale=1/170
guard();vp.DisplayLocked=True
text(sp,15,77,198,'MS-O1 -> DB-O1 | complete proposed route',2.8)
text(sp,15,69,198,r'Plan: 2.600 + 20.000 + 5.9119 = 28.5119 m.\PAdd 3.000 m vertical/meter-tail allowance.\PDesign length = 31.5119 m; not as-built.\PSource and DB positions are proposed on supplied plan.\POrigin -> F1 tap: separate 28 m busway allowance;\Pnot inferred from this tenant-plan viewport.',2.6)
text(sp,15,24,198,'4C35 PVC Cu + CPC16 | TM63D 63 A at MS-O1\PCLP meter follows source MCCB; DB has 4P isolation.',2.4)

rect(sp,230,141,177,123)
text(sp,235,259,166,'P1-P4 | L, N AND CPC RINGS',2.8)
text(sp,235,250,166,'Both ends return to the SAME circuit terminals.',2.2)
for k,(label,base) in enumerate([('L OUT OF RCBO',226),('N OUT OF SAME RCBO',201),('CPC TO PE BAR',176)]):
    text(sp,235,base+9,150,label+' | 6 mm2',2.2)
    circle(sp,248,base,1);circle(sp,248,base-10,1)
    line(sp,(248,base),(386,base),WIRE);line(sp,(386,base),(386,base-10),WIRE);line(sp,(386,base-10),(248,base-10),WIRE)
    line(sp,(248,base),(244,base),WIRE);line(sp,(244,base),(244,base-10),WIRE);line(sp,(244,base-10),(248,base-10),WIRE)
    for xx in [290,346]:circle(sp,xx,base,.6);line(sp,(xx,base),(xx,base-4),WIRE)
text(sp,257,151,143,'Two individually fused taps per ring; no unfused additions.',2.0)
rect(sp,230,63,177,73)
text(sp,235,131,165,'EACH FLOORBOX / SOCKET TAP',2.6)
line(sp,(240,114),(258,114),WIRE);rect(sp,258,108,55,12);text(sp,261,117,50,'13 A DP FCU',2.3)
line(sp,(313,114),(337,114),WIRE);rect(sp,337,106,61,16);text(sp,341,118,54,'SO / FLOORBOX',2.1)
text(sp,235,100,165,r'Fuse in L; N linked to DP isolation; PE continuous.\PAfter FCU: 4 mm2 L/N/CPC, 0.5 m allowance.\PP7 is a separate radial: 10 A DP FCU -> WH01.\PDo not mix RCBO neutrals or circuit ring ends.\PVerify L/N/CPC ring continuity before energising.',2.2)
text(sp,235,54,165,r'PROTECTION REFERENCE\PMain diagram and Task3 govern the MS-O1 MCCB,\Pmanufacturer backup, fault bounds and earthing.\PThis sheet adds route visibility and connection detail;\Pdevice and circuit counts remain 112 / 15.',2.3)
finish('rev03_details')
