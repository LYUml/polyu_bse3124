from cad_common import *
for name in ['TASK2-POWER-PLAN','TASK2-LIGHTING-PLAN','REV03-ROUTE-AND-RING']:
 sp=doc.Layouts.Item(name).Block
 for i in range(sp.Count):
  e=sp.Item(i)
  if e.ObjectName=='AcDbViewport':
   print(name,e.Handle,'center',e.Center,'size',e.Width,e.Height,'target',e.Target,'scale',e.CustomScale)
for i in range(doc.ModelSpace.Count):
 e=doc.ModelSpace.Item(i)
 if e.ObjectName in ['AcDbText','AcDbMText']:
  t=e.TextString
  if any(x in t for x in ['SO01','SO03','DB-O1','S-A','S-B','S-C']):
   print(e.Handle,e.ObjectName,str(t)[:160],e.InsertionPoint)
