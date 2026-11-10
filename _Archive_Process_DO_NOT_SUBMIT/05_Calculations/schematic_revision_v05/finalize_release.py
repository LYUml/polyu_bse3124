from pathlib import Path
import hashlib,json,shutil,csv
import pymupdf as f
r=Path('05_Calculations/schematic_revision_v05').resolve();old=r.with_name('schematic_revision_v04');base=r.parents[1];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
b=json.loads((r/'baseline_hashes.json').read_text());assert all(sha(base/k)==v for k,v in b.items())
exclude={'final_manifest.json','native_final_gate.json','native_plot_gate.json','source_hash_gate.json'}
ps=[p for p in (r/'data').rglob('*') if p.is_file() and p.name not in exclude];assert all(sha(p)==sha(old/'data'/p.relative_to(r/'data')) for p in ps)
for n in ['native_final_gate.json','native_plot_gate.json']:shutil.copy2(r/n,r/'data'/n)
(r/'data/source_hash_gate.json').write_text(json.dumps({'checked_files':len(b),'unchanged':True},indent=2))
d=f.open(r/'BSE3124_Final_Rev05.pdf');assert len(d)==23
assert 'LUMINAIRE SCHEDULE' not in d[16].get_text()
log=(r/'source/build/main.log').read_text(errors='replace');assert 'Overfull' not in log
m={'revision':5,'scope':'Layout and label clearance repair; engineering inputs unchanged','pdf_pages':len(d),'office_device_records':112,'luminaires':92,'outgoing_circuits':15,'unchanged_data_files':len(ps),'source_and_previous_release_hashes_checked':len(b),'native_validation':json.loads((r/'native_final_gate.json').read_text()),'pdf_sha256':sha(r/'BSE3124_Final_Rev05.pdf'),'visual_review':'All source pages inspected at readable scale, revised pages rerendered and inspected; lamp schedule fragment removed from route locator; DB/C69 and SO01/SO03 annotation clearance corrected; references consolidated on page23','no_tex_overfull_boxes':True}
(r/'data/final_manifest.json').write_text(json.dumps(m,indent=2))
(r/'source/README.md').write_text('''# Rev05 editable answer source

Run build.ps1 here to build ../BSE3124_Final_Rev05.pdf (23 pages). Native drawing: ../BSE3124_Final_Rev05.dwg. This revision repairs viewport cropping, crowded labels and reference pagination. Engineering data is unchanged from Rev04/Rev03.

Manufacturer references remain at ../../schematic_revision_v03/references and course references at the workspace 02_References. export_review.py replots 8 layouts with AutoCAD 2027. verify_revision.py checks the native saved drawing. CAD edit scripts are historical one-time migrations and must not be rerun on this completed drawing.
''',encoding='utf8')
(r/'排版修复说明.txt').write_text('''Rev05 排版修复

第17页：调整路线详图视口的下边界，去掉无关且被截断的 LUMINAIRE SCHEDULE 表头；保留完整进线路线、办公室灯具及 1:170 比例。
第13及17页：拉开 DB-O1 与 C69 标注，局部文字背景遮罩避免底图网格穿字；设备、开关和线路位置不变。
第14页：分开 SO01 与 SO03 标签，略微扩展视口上缘以完整显示插座符号，保持 1:75 比例。
文末：设备选型表和参考资料统一排版到第23页，消除零碎跨页。正文内容和技术数值保留。

逐页检查正文、表格及8张CAD图纸；最终23页，无LaTeX超出版心警告。已通过 AutoCAD 2027 原生复开验证；92灯具标签、15回路表行、两条进线路径一致。20项原件与历史交付文件哈希未变。

使用 BSE3124_Final_Rev05.pdf 与 BSE3124_Final_Rev05.dwg。Rev04保留作追溯。
''',encoding='utf8')
(r.parent/'data/rev05_release.json').write_text(json.dumps({'revision':5,'directory':str(r),'pdf':str(r/'BSE3124_Final_Rev05.pdf'),'dwg':str(r/'BSE3124_Final_Rev05.dwg'),'manifest':str(r/'data/final_manifest.json')},indent=2))
print(json.dumps({'pages':len(d),'unchanged_data_files':len(ps),'hashes_passed':len(b),'native_handles':m['native_validation']['checked_entity_handles']}))
