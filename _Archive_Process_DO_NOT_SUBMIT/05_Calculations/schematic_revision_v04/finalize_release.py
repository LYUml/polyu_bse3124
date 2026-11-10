from pathlib import Path
import hashlib,json,csv,shutil
from collections import Counter
import pymupdf
r=Path('05_Calculations/schematic_revision_v04').resolve(); old=r.with_name('schematic_revision_v03'); base=r.parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
b=json.loads((r/'baseline_hashes.json').read_text());assert all(sha(base/k)==v for k,v in b.items())
exclude={'access_clarity_revision.json','final_manifest.json','native_final_gate.json','native_plot_gate.json','source_hash_gate.json'}
comp=[p for p in (r/'data').rglob('*') if p.is_file() and p.name not in exclude]
assert all(sha(p)==sha(old/'data'/p.relative_to(r/'data')) for p in comp)
cs=list(csv.DictReader((r/'data/circuits.csv').open())); ds=list(csv.DictReader((r/'data/devices.csv').open())); assigned=Counter(x for c in cs for x in c['device_ids'].split(';'))
assert len(cs)==15 and len(ds)==112 and all(assigned[d['device_id']]==1 for d in ds)
for n in ['native_final_gate.json','native_plot_gate.json']:shutil.copy2(r/n,r/'data'/n)
source_gate={'checked_files':len(b),'unchanged':True};(r/'data/source_hash_gate.json').write_text(json.dumps(source_gate,indent=2))
m={'revision':4,'scope':'Editorial simplification; Rev03 engineering inputs and results unchanged','pdf_pages':len(pymupdf.open(r/'BSE3124_Final_Rev04.pdf')),'office_device_records':112,'luminaires':92,'outgoing_circuits':15,'assigned_once':True,'original_and_rev03_hashes_unchanged':len(b),'unchanged_data_files':len(comp),'native_validation':json.loads((r/'native_final_gate.json').read_text()),'pdf_sha256':sha(r/'BSE3124_Final_Rev04.pdf'),'visual_review':'24-page overview inspected; revised room and installation sheets inspected at readable scale','delivery_arrows_removed':3}
(r/'data/final_manifest.json').write_text(json.dumps(m,indent=2))
(r/'source/README.md').write_text('''# Rev04 editable answer source

Run build.ps1 here to build ../BSE3124_Final_Rev04.pdf. The matching native drawing is ../BSE3124_Final_Rev04.dwg. This release simplifies annotations; Rev03 engineering inputs and results are unchanged in ../data. Additional manufacturer reference files remain in ../../schematic_revision_v03/references; original course references remain in 02_References.

CAD migration/edit scripts are historical one-time operations. Do not rerun them on the completed drawing. The PDF build does not run them. Plot refresh uses ../export_review.py with AutoCAD 2027 Core Console. Native audit uses ../verify_revision.py.
''',encoding='utf8')
(r/'修改说明.txt').write_text('''Rev04 修改说明

1. LV ACCESS 的 assumed 改为 PROPOSED LV ACCESS / 3000 mm / CLEAR WIDTH，表明拟议净通道宽度，未将其改称实测门洞尺寸。
2. 删除 HV/TX 门前的三支运输方向箭头（共九条线）。保留门扇开启弧、虚线净空边界和风机气流箭头。
3. 通读并精简正文及图面注释：删除旧版本修改过程、重复的假设提醒和重复设备解释；相关说明集中在计算或设计条件章节。
4. 保留计算公式、表格、关键假设、保护条件、联锁要求和 references。计算数据与 Rev03 一致。
5. 最终 PDF 24 页；原生 DWG 经 AutoCAD 2027 重新打开校验，92 盏灯、15 个回路及 112 条设备记录一致。已检查 PDF 排版和修改后的图页。
6. 原始资料及 Rev03 PDF/DWG 的 18 项基准哈希未变。

使用 BSE3124_Final_Rev04.pdf 和 BSE3124_Final_Rev04.dwg；Rev03 保留供追溯。本次为文字和图面表达修订，沿用既有课程设计假设及适用条件。
''',encoding='utf8')
pointer={'revision':4,'release_directory':str(r),'pdf':str(r/'BSE3124_Final_Rev04.pdf'),'dwg':str(r/'BSE3124_Final_Rev04.dwg'),'manifest':str(r/'data/final_manifest.json'),'engineering_basis':'Rev03 unchanged'}
(r.parent/'data/rev04_release.json').write_text(json.dumps(pointer,indent=2))
print(json.dumps({'baseline_hashes':len(b),'unchanged_data_files':len(comp),'devices':len(ds),'circuits':len(cs),'pdf_pages':m['pdf_pages']}))
