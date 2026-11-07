"""A3 ground-floor overview; native DWG viewport at 1:200."""
from pathlib import Path
import win32com.client,pythoncom
from win32com.client import VARIANT
R=Path(__file__).resolve().parents[2]
D=win32com.client.GetActiveObject("AutoCAD.Application").ActiveDocument
assert Path(D.FullName).resolve()==(R/"04_Design_Outputs/cad/assignment_working_v02.dwg").resolve()
L=D.Layouts.Add("TASK1-GROUND-OVERVIEW");L.CopyFrom(D.Layouts.Item("TASK1-ROOM-REVIEW"));D.ActiveLayout=L
pt=lambda x,y:VARIANT(pythoncom.VT_ARRAY|pythoncom.VT_R8,[float(x),float(y),0.])
V=D.PaperSpace.AddPViewport(pt(155,153),290,220);V.Layer="E-T1-VPORT-NOPLOT";V.Display(True);V.Target=pt(30000,30000);V.Direction=VARIANT(pythoncom.VT_ARRAY|pythoncom.VT_R8,[0.,0.,1.]);V.CustomScale=.005;V.DisplayLocked=True
h=[]
def text(s,x,y,w=102,size=2.8):
 e=D.PaperSpace.AddMText(pt(x,y),w,s);e.Height=size;e.StyleName="T1-Arial";e.Layer="E-T1-PAPER-NOTES";h.append(e.Handle)
text("TASK 1 | GROUND-FLOOR PLANTROOM LOCATION",12,285,395,4)
text("PROPOSAL ON SUPPLIED ARCHITECTURAL PLAN | COURSE DESIGN REVIEW | PLAN 1:200 AT A3",12,276,395,2.8)
text("PROPOSED LOCATION\\PLower-left perimeter of supplied ground-floor plan. Substation 12430 x 5450; adjacent LV room 12430 x 3500 assumed. See separate 1:75 room detail.",305,260)
text("LOCATION REASONS\\PDirect external plant access can be reserved subject to site confirmation.\\PAdjacent LV room keeps transformer-to-incomer interfaces short.\\PPerimeter plantrooms separate supply equipment from the upper lift/stair/AHU core and remaining accommodation.\\PLV room has its own proposed west entrance.",305,212)
text("LOAD ASSESSMENT\\POffices: 1644.800 kVA.\\PAC: 1000 kW cooling -> 526.039 kW electrical -> 584.488 kVA at assumed PF 0.90.\\PPublic services: 200 kVA aggregate allowance.\\PTwo-zone conservative envelope: 2672.216 kVA.\\PPropose 2 x 1500 kVA, with equal zone allocation; no full-load N-1.",305,143)
text("SITE CONDITIONS TO VERIFY\\PExternal apron, road and <=20m unloading route are not given by the source plan. Maintain >=3m clear delivery route.\\PArchitectural wall openings, structural/flood/fire provisions, ventilation and supplier equipment approval require coordination.",305,68)
text("DRAWING REFERENCES: assignment_working_v02.dwg | TASK1-GROUND-OVERVIEW + TASK1-ROOM-REVIEW",12,20,395,2.6)
text("Calculation sources and declared assumptions: Task1_answer_draft.md; data/task1_design_inputs.csv. Original drawings retained.",12,12,395,2.4)
D.Regen(1);D.Save()
output=R/"04_Design_Outputs/pdf/task1_ground_overview_v01.pdf"
assert not output.exists()
print(D.Plot.PlotToFile(str(output),"DWG To PDF.pc3"))
