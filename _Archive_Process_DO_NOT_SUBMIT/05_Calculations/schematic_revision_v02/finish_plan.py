from cad_common import *
guard();doc.ActiveLayout=doc.Layouts.Item('TASK2-POWER-PLAN');app.ZoomExtents();app.ZoomScaled(.9,1)
m=doc.ModelSpace
settext('7993',r'FS01 / WH01 : P7\P10 A DP FCU',(66560,-13350),3600,200)
rect(m,67160,-13200,280,270,'E-POWER-WORK')
circle(m,67300,-13120,35,'E-POWER-WORK')
line(m,(67000,-12782.416),(67300,-12782.416),'E-POWER-WORK')
line(m,(67300,-12782.416),(67300,-12930),'E-POWER-WORK')
text(m,66800,-13950,3000,'SHC10 GB | 1.4 kW',160,'E-POWER-WORK')
settext('7DE9','WH01: SHC10 GB Eltron235232, 1.4kW/220V; FS01 on P7 with B10 +10A DP FCU.')
settext('7DE6','P7 L3 RADIAL B10 4 mm2 13.107m | WH01 6.364A')
settext('7DDF','Socket assemblies:13 A FCU each. WH01:10 A DP FCU. Local spur4 mm2,0.5m allowance.')
settext('7DDE','FB01-09=floorbox; SO01-03=twin socket; FS01=WH01 heater connection assembly.')
settext('7D95','P7 [L3] | WH01 via FS01 /1.4 kW | B10 /TYPE A 30 mA 1P+N RCBO')
settext('7971','L3 P7 B10 / 4mm2 RADIAL / WH01 1.4kW / FCU10A / 30mA TYPE A RCBO')
settext('7FAA','1. EVERY POWER ASSEMBLY HAS AN UPSTREAM FCU: SOCKETS13 A / WH01 10 A')
settext('7FC3','FB01-09:13 A FCU per four-socket floorbox. SO01-03:13 A FCU per twin socket. FS01:10 A DP FCU for WH01.')
settext('7FAC','DP switched FCU at tap\P13 A sockets /10 A WH01',h=2.5)
settext('7FAE','ONE assembly: FB / SO / WH01\PSockets share13 A; WH01 load6.364 A',h=2.5)
# Remove five miniature symbols from the two rising-main cabinets; install the selected 1600 A outgoing ACB.
panel_handles=json.loads((ROOT/'stagepanels_handles.json').read_text());retired=[]
for h in panel_handles:
    e=doc.HandleToObject(h)
    if e.ObjectName=='AcDbBlockReference':
        x,y,_=e.InsertionPoint
        if ((11140<x<12280) or (14560<x<15700)) and 23400<y<23800:guard();e.Delete();retired.append(h)
    elif e.ObjectName=='AcDbPolyline':
        v=e.Coordinates;x,y=v[0:2]
        if ((11140<x<12280) or (14560<x<15700)) and abs(y-23400.584)<.01:guard();e.Delete();retired.append(h)
    elif e.ObjectName=='AcDbMText':
        if e.TextString=='5 FLOOR MCCBs':guard();e.TextString='1600A RISER ACB'
        elif e.TextString.startswith('MSB-A / MSB-B'):guard();e.InsertionPoint=pt(10000,24780.584);e.Height=130
for x in [11140,14560]:
    rect(m,x+300,23355.584,537,300)
    block(m,x+570,23405.584,'AECBS_UK_E_Circuitb',105,math.pi/2)
(ROOT/'stagepanels_handles.json').write_text(json.dumps([h for h in panel_handles if h not in retired]))
(ROOT/'retired_panel_handles.json').write_text(json.dumps(retired))
settext('8029',r'CAPACITY AND EQUIPMENT\PTX-A/B: CLP 1500 kVA distribution transformer type; 3000 kVA installed, 2672.216 kVA demand. No full-load N-1.\PHV-01: incomer + two transformer protection panels.\PMSB-A/B: 2500 A sections. IN: MTZ2 25H1; FL: MTZ2 16H1 rising-main ACB; PL: NS800N. Floor taps: NSX400N MCCBs.\PPlan outlines are installation design dimensions; utility equipment supply follows COP101 responsibilities.')
finish('office')
