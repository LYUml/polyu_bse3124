"""Orient the teacher board sheet and fill its title block and circuit slots."""
from pathlib import Path
import pymupdf as fitz
S=Path(__file__).resolve().parent
doc=fitz.open(S/'build/main.pdf')
p=doc[9]
p.set_rotation(90)
p.remove_rotation()
# Replace the old portrait page number with a horizontal footer.
p.add_redact_annot(fitz.Rect(12,275,35,310),fill=(1,1,1))
p.apply_redactions(images=0,graphics=0)
p.insert_text((416,574),'10',fontsize=9,fontname='tiro')
def put(x,y,text,size=7):p.insert_text((x,y),text,fontsize=size,fontname='helv')
put(671,74,'Office 1 DB-O1',7)
put(671,104,'15 outgoing circuits',6.5)
put(671,116,'7 lighting / 8 power',6.5)
put(671,128,'Spare ways reserved',6.5)
put(671,423,'N/A',7)
put(671,447,'BSE3124 - Group 1',7)
put(671,475,'Office 1 distribution',6.5)
put(671,485,'board schematic',6.5)
put(710,501,'08 Nov 2026',6)
put(729,516,'Group 1',6)
put(729,531,'E-03',6)
put(710,546,'NTS',6.5)
slots=['LC-A','LC-B','LC-C','LC-F','LC-E','LC-D','P1','P3','LC-G','P2','P4','P6','P5','SP','P7','SP','SP','P8','SP','SP','SP','SP','SP','SP']
for i,label in enumerate(slots):
 rect=fitz.Rect(178+i*16.79,320,178+(i+1)*16.79,332)
 p.insert_textbox(rect,label,fontsize=5.5,fontname='helv',align=1)
put(671,140,'SP = spare',6.5)
doc.save(S.parent/'BSE3124_Final.pdf',garbage=4,deflate=True)
