from pathlib import Path
import shutil,json
r=Path(__file__).resolve().parent
b=r/'before_access_clarity';b.mkdir(exist_ok=True)
for n in ['BSE3124_Final_Rev02.dwg','BSE3124_Final_Rev02.pdf']:
 assert not (b/n).exists(), 'Backup exists: inspect before rerunning'
 shutil.copy2(r/n,b/n)
from cad_common import *
guard()
lin=r/'access_clearance.lin';lin.write_text('*ACCESS_CLEAR,Clearance boundary 2mm dash 1mm gap\nA,2,-1\n')
try:doc.Linetypes.Item('ACCESS_CLEAR')
except:doc.Linetypes.Load('ACCESS_CLEAR',str(lin))
lay=layer('E-ACCESS-CLEARANCE',7,18)
expected=json.loads((r/'expected_revision_text.json').read_text())
for boundary,label,name,x,w in [('79C7','79C8','HV',9500,4000),('79C9','79CA','TX-A',14300,3000),('79CB','79CC','TX-B',18000,3000)]:
 guard();e=doc.HandleToObject(boundary);e.Layer=lay;e.Linetype='ACCESS_CLEAR';e.LinetypeScale=1;e.Color=256;e.Update()
 t=f'{name} DELIVERY ACCESS\\PKEEP CLEAR\\P{w} mm opening'
 settext(label,t,h=170);expected[label]=t
 cx=x+w/2
 line(doc.ModelSpace,(cx,14550.584),(cx,15700.584),lay)
 line(doc.ModelSpace,(cx-180,15400.584),(cx,15700.584),lay)
 line(doc.ModelSpace,(cx+180,15400.584),(cx,15700.584),lay)
(r/'expected_revision_text.json').write_text(json.dumps(expected,indent=2))
guard();doc.ActiveLayout=doc.Layouts.Item('TASK1-ROOM-REVIEW');app.ZoomExtents();app.ZoomScaled(.9,0)
finish('access')
(r/'data/access_clarity_revision.json').write_text(json.dumps({'boundary_handles':['79C7','79C9','79CB'],'label_handles':['79C8','79CA','79CC'],'arrow_handles':created,'linetype':'ACCESS_CLEAR','opening_dimensions_unchanged':True,'arrow_direction':'north into plantroom','purpose':'delivery access clearance; keep clear; not equipment footprint'},indent=2))
