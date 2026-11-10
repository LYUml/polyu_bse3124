from pathlib import Path
import json, math, sys, time
import win32com.client as wc
import pythoncom
import pywintypes

def retry(fn):
    for attempt in range(60):
        try:return fn()
        except pywintypes.com_error as e:
            if e.hresult not in [-2147418111,-2147417846]:raise
            time.sleep(.15)
    raise RuntimeError('AutoCAD remained busy')
class CAD:
    def __init__(self,obj):object.__setattr__(self,'obj',obj)
    def __getattr__(self,key):
        v=retry(lambda:getattr(self.obj,key))
        if isinstance(v,wc.dynamic.CDispatch):return CAD(v)
        if callable(v):
            def call(*args):
                z=retry(lambda:v(*[a.obj if isinstance(a,CAD) else a for a in args]))
                return CAD(z) if isinstance(z,wc.dynamic.CDispatch) else z
            return call
        return v
    def __setattr__(self,key,value):retry(lambda:setattr(self.obj,key,value.obj if isinstance(value,CAD) else value))

ROOT=Path(__file__).resolve().parent
DWG=ROOT/'BSE3124_Final_Rev05.dwg'
app=CAD(wc.GetActiveObject('AutoCAD.Application'))
doc=app.ActiveDocument
def guard():
    assert Path(app.ActiveDocument.FullName).resolve()==DWG.resolve(), 'Wrong active DWG'
guard()
def pt(x,y,z=0): return wc.VARIANT(pythoncom.VT_ARRAY|pythoncom.VT_R8,[x,y,z])
def layer(name,color=7,weight=25):
    guard()
    try:l=doc.Layers.Item(name)
    except:l=doc.Layers.Add(name)
    l.Color=color;l.Lineweight=weight
    return name
NEW=layer('E-REV-EQUIPMENT',7,30)
TXT=layer('E-REV-TEXT',7,18)
WIRE=layer('E-REV-SLD',7,30)
created=[]
def mark(e,lay=NEW):
    e.Layer=lay;e.Color=256;created.append(e.Handle);return e
def line(sp,a,b,lay=NEW):
    guard();return mark(sp.AddLine(pt(*a),pt(*b)),lay)
def rect(sp,x,y,w,h,lay=NEW):
    guard();v=wc.VARIANT(pythoncom.VT_ARRAY|pythoncom.VT_R8,[x,y,x+w,y,x+w,y+h,x,y+h])
    e=mark(sp.AddLightWeightPolyline(v),lay);e.Closed=True;return e
def circle(sp,x,y,r,lay=NEW):
    guard();return mark(sp.AddCircle(pt(x,y),r),lay)
def text(sp,x,y,w,t,h=2.8,lay=TXT):
    guard();e=mark(sp.AddMText(pt(x,y),w,t),lay);e.Height=h;e.StyleName='T1-Arial';return e
def block(sp,x,y,name,s=1,rot=0):
    guard();return mark(sp.InsertBlock(pt(x,y),name,s,s,s,rot),WIRE)
def settext(handle,t,pos=None,w=None,h=None):
    guard();e=doc.HandleToObject(handle);e.TextString=t
    if pos:e.InsertionPoint=pt(*pos)
    if w:e.Width=w
    if h:e.Height=h
    e.Update()
def finish(stage):
    guard();doc.Regen(1);doc.Save()
    (ROOT/f'stage{stage}_handles.json').write_text(json.dumps(created,indent=2))
    print('SAVED',stage,doc.FullName,len(created))

