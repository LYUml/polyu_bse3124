from cad_common import *
t='Dedicated RCBO neutrals; ring L/N/CPC ends return to their own circuit terminals. Local spurs: sockets 13 A / WH01 10 A; 4 mm2 L/N/CPC, 0.5 m assumed.'
settext('7DAF',t)
settext('8170','MAIN LV SWITCH ROOM',pos=(70,143),w=100,h=2.5)
p=ROOT/'expected_revision_text.json'
d=json.loads(p.read_text()); d['7DAF']=t;d['8170']='MAIN LV SWITCH ROOM';p.write_text(json.dumps(d,indent=2))
guard();doc.Regen(1);doc.Save()
print(doc.FullName)
