from cad_common import *
e=doc.HandleToObject('78ED');print(e.ObjectName,e.TextString,e.InsertionPoint,e.Height)
settext('7BD2','DB-O1',pos=(73700,31450),w=1350,h=160)
guard();e.InsertionPoint=pt(73950,30450);e.Update()
v=doc.HandleToObject('86B7');guard();v.DisplayLocked=False;v.Width=202;v.Height=166;v.Center=pt(113,178);v.Target=pt(79200,29690);v.CustomScale=1/170;v.DisplayLocked=True
finish('rev05_label_clearance')
