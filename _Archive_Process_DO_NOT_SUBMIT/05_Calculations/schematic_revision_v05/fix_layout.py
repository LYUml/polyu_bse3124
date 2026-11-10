from cad_common import *
a=[]
def move(h,pos,w=None,hgt=None):
 e=doc.HandleToObject(h);a.append({'handle':h,'before_position':list(e.InsertionPoint),'after_position':pos});settext(h,e.TextString,pos=pos,w=w,h=hgt)
# Clip only the unrelated schedule below the locator; preserve plan scale and top/left limits.
v=doc.HandleToObject('86B7');guard();v.DisplayLocked=False
v.Width=214;v.Height=163;v.Center=pt(119,179.5);v.Target=pt(80220,29945);v.CustomScale=1/170;v.DisplayLocked=True
move('798D',(64275.932,-14800),w=2300)
move('7BD2',(73900,31050),w=1450,hgt=170)
# More breathing space above pantry devices, without changing scale or bottom limit.
v=doc.HandleToObject('7DDB');guard();v.DisplayLocked=False;v.Height=288;v.Center=pt(148.5,241.5);v.Target=pt(72167.182,-22914.916);v.CustomScale=1/75;v.DisplayLocked=True
for name in ['TASK1-MAIN-SCHEMATIC','REV03-ROUTE-AND-RING']:
 sp=doc.Layouts.Item(name).Block
 for i in range(sp.Count):
  e=sp.Item(i)
  if e.ObjectName=='AcDbMText' and 'REV04 |' in e.TextString:settext(e.Handle,e.TextString.replace('REV04 |','REV05 |'))
finish('rev05_layout')
(ROOT/'layout_changes.json').write_text(json.dumps({'text_positions':a,'locator_viewport':'86B7: crop unrelated schedule, expand right to show source label; scale retained 1:170','power_viewport':'7DDB: extend top 3mm; scale retained 1:75'},indent=2))
