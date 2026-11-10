from cad_common import *
for h in json.loads((ROOT/'stagepanels_handles.json').read_text()):
    e=doc.HandleToObject(h)
    if e.ObjectName=='AcDbMText' and e.TextString.startswith('MSB-A / MSB-B'):
        guard();e.TextString='MSB-A / MSB-B\P2500 A bus sections';e.InsertionPoint=pt(17400,24000.584);e.Width=3000;e.Height=160
# Place rising-main breakers inside the main switchroom boundary.
for h in json.loads((ROOT/'stage3_handles.json').read_text()):
    e=doc.HandleToObject(h)
    if e.ObjectName=='AcDbBlockReference':
        x,y,z=e.InsertionPoint
        if x in [55,180] and y==151:guard();e.InsertionPoint=pt(x,137)
    elif e.ObjectName=='AcDbLine':
        a=list(e.StartPoint);b=list(e.EndPoint)
        if a[0] in [55,180] and a[0]==b[0]:
            if a[1]==130 and b[1]==151:guard();e.EndPoint=pt(b[0],137)
            elif abs(a[1]-(151+1.9196283379151637*3.5))<1e-7:guard();e.StartPoint=pt(a[0],137+1.9196283379151637*3.5)
    elif e.ObjectName=='AcDbMText' and e.TextString.startswith('Riser: MTZ2'):
        guard();e.TextString='MSB-FL: MTZ2 16H1, Ir 1440 A'
settext('818E',r'SYSTEM BASIS\PMSB design PFC 51.67 kA: TX uk=6%, -10% tolerance, c=1.1, plus 8 x plant/public current. Independent sections. Main/riser ACBs 66 kA; floor/plant MCCBs 70 kA. AF=frame; AT=long-time setting. Utility supply and protection follow COP101.',h=2.2)
e=doc.HandleToObject('8029');settext('8029',e.TextString.replace('NS800N','NS800H').replace('NSX400N','NSX400H'))
e=doc.HandleToObject('7FEE');settext('7FEE',e.TextString.replace('B10/B16','B10'))
# Revisions are explicit rather than mislabeled as the preceding version.
e=doc.HandleToObject('8190')
try:
    if 'REV 01' in e.TextString:settext('8190',e.TextString.replace('REV 01','REV 02'))
except:pass
guard();doc.Regen(1);doc.Save()
print('Saved layout refinements')
