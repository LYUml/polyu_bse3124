from cad_common import *
settext('7BD2','DB-O1',pos=(73950,31200),w=1350,h=160)
for h in ['7BD2','78ED','798D']:
 guard();doc.HandleToObject(h).BackgroundFill=True
finish('rev05_final_spacing')
