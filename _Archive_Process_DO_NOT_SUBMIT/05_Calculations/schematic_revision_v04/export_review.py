"""Replot six saved layouts through AutoCAD 2027; preserve the DWG byte-for-byte.

Reject empty plots before replacing the final report's drawing dependencies.
Visual review is a separate release check.
"""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parents[2]
DWG = Path(__file__).resolve().parent / 'BSE3124_Final_Rev04.dwg'
OUT = Path(__file__).resolve().parent / 'native_plots'
ASSETS = Path(__file__).resolve().parent / 'source/assets'
OUT.mkdir(parents=True, exist_ok=True)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
before = sha(DWG)
layouts = [
    ('TASK1-GROUND-OVERVIEW', 'ground'),
    ('TASK1-ROOM-REVIEW', 'room'),
    ('TASK1-MAIN-SCHEMATIC', 'main-schematic'),
    ('TASK2-LIGHTING-PLAN', 'office-lighting'),
    ('TASK2-POWER-PLAN', 'office-power'),
    ('TASK2-DB-SCHEMATIC', 'office-db'),
    ('DESIGN-DETAILS', 'installation-details'),
    ('REV03-ROUTE-AND-RING', 'route-and-ring'),
]
script = ['(setvar "FILEDIA" 0)', '(setvar "BACKGROUNDPLOT" 0)']
for layout, name in layouts:
    target = OUT / (name + '.pdf')
    script += [f'(setvar "CTAB" "{layout}")', '(command "_.REGENALL")']
    args = f'"_.-PLOT" "_N" "{layout}" "" "" "{target.as_posix()}"'
    script.append(f'(command {args} "_N" "_Y")')
script.append('(princ "FINAL_PLOTS_COMPLETE")')
scr = OUT / 'plot.scr'
scr.write_text('\n'.join(script) + '\n', encoding='ascii')
result = subprocess.run([
    'C:/Program Files/Autodesk/AutoCAD 2027/accoreconsole.exe',
    '/i', str(DWG), '/s', str(scr), '/l', 'en-US'
], capture_output=True)
log = result.stdout.decode('utf-16le', errors='replace')
(OUT / 'console.log').write_text(log, encoding='utf8')
assert result.returncode == 0 and 'FINAL_PLOTS_COMPLETE' in log
assert '; error:' not in log.lower()
assert sha(DWG) == before, 'Plot-only operation changed the saved drawing'
records = []
for layout, name in layouts:
    pdf = OUT / (name + '.pdf')
    reader = PdfReader(pdf)
    assert len(reader.pages) == 1 and len(reader.pages[0].extract_text()) > 500, layout
    records.append(dict(layout=layout, text_characters=len(reader.pages[0].extract_text()),
                        plot_sha256=sha(pdf)))
writer = PdfWriter()
for name in ['ground', 'room', 'main-schematic']:
    writer.append(OUT / (name + '.pdf'))
with (ASSETS / 'task1-drawings.pdf').open('wb') as stream:
    writer.write(stream)
for _, name in layouts[3:]:
    shutil.copy2(OUT / (name + '.pdf'), ASSETS / (name + '.pdf'))
(Path(__file__).resolve().parent / 'native_plot_gate.json').write_text(json.dumps(
    dict(dwg_sha256=before, saved_dwg_unchanged=True, layouts=records,
         review='Native plots generated; visual PDF review required separately'), indent=2))
print('Seven saved layouts replotted; no blank sheets; DWG unchanged.')
