from cad_common import *
t='LINE KEY: dashed path = HV trench; solid path = LV route. Dashed boxes = delivery clearance; arrows = delivery direction. Equipment details diagrammatic.'
settext('8030',t)
e=json.loads((ROOT/'expected_revision_text.json').read_text());e['8030']=t;(ROOT/'expected_revision_text.json').write_text(json.dumps(e,indent=2))
for h in json.loads((ROOT/'stageaccess_handles.json').read_text()):
 guard();doc.HandleToObject(h).Lineweight=35
nguard=guard();doc.Regen(1);doc.Save()
p=ROOT/'verify_revision.py';s=p.read_text();s=s.replace("'stageoffice_handles.json']", "'stageoffice_handles.json','stageaccess_handles.json']");p.write_text(s)
