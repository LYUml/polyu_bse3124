"""Orient the teacher board sheet and fill its title block and circuit slots."""
from pathlib import Path
import pymupdf as fitz
S=Path(__file__).resolve().parent
doc=fitz.open(S/'build/main.pdf')
board_pages=[i for i,p in enumerate(doc) if 'DB-O1: 8-way TPN chassis' in p.get_text()]
assert len(board_pages)==1, board_pages
board_index=board_pages[0]
p=doc[board_index]
p.set_rotation(90)
p.remove_rotation()
# Replace the old portrait page number with a horizontal footer.
p.add_redact_annot(fitz.Rect(12,275,35,310),fill=(1,1,1))
p.apply_redactions(images=0,graphics=0)
p.insert_text((416,574),str(board_index+1),fontsize=9,fontname='tiro')
def put(x,y,text,size=7):p.insert_text((x,y),text,fontsize=size,fontname='helv')
put(671,74,'Office 1 DB-O1',7)
put(671,104,'15 outgoing circuits',6.5)
put(671,116,'7 lighting / 8 power',6.5)
put(671,128,'Unused ways blanked',6.5)
put(671,423,'N/A',7)
put(671,447,'BSE3124 - Group 1',7)
put(671,475,'Office 1 distribution',6.5)
put(671,485,'board schematic',6.5)
put(710,501,'10 Nov 2026',6)
put(729,516,'Group 1',6)
put(729,531,'E-03',6)
put(710,546,'NTS',6.5)
slots=['LC-A','LC-B','LC-C','LC-F','LC-E','LC-D','P1','P3','LC-G','P2','P4','P6','P5','BLK','P7','BLK','BLK','P8','BLK','BLK','BLK','BLK','BLK','BLK']
for i,label in enumerate(slots):
 rect=fitz.Rect(178+i*16.79,320,178+(i+1)*16.79,332)
 p.insert_textbox(rect,label,fontsize=5.5,fontname='helv',align=1)
put(671,140,'BLK = blanked',6.5)
# Remove rasterised template folios and reapply one current folio in the A4 footer.
for idx,page in enumerate(doc):
 if idx>0 and abs(page.rect.width-595.32)<2 and page.rect.height>800:
  page.draw_rect(fitz.Rect(240,799,325,837),color=None,fill=(1,1,1),overlay=True)
  page.insert_textbox(fitz.Rect(270,811,325,829),str(idx+1),fontsize=9,fontname='tiro',align=1)
doc.save(S.parent/'BSE3124_Final_Rev05.pdf',garbage=4,deflate=True)
