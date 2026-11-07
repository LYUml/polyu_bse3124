"""Read-only setup evidence; never starts AutoCAD or opens a drawing."""
import hashlib, importlib.metadata, json
from pathlib import Path
import win32com.client

root = Path(__file__).resolve().parents[1]
report = {'packages': {}, 'autocad_executable_exists': Path('C:/Program Files/Autodesk/AutoCAD 2027/acad.exe').exists()}
for name in ['autocad-mcp-pro', 'ezdxf', 'pywin32', 'fastmcp']:
    report['packages'][name] = importlib.metadata.version(name)
try:
    app = win32com.client.GetActiveObject('AutoCAD.Application')
    report['live_autocad'] = {'connected': True, 'version': str(app.Version), 'documents': app.Documents.Count}
except Exception as exc:
    report['live_autocad'] = {'connected': False, 'reason': str(exc)}
files = [p for folder in ['01_Assignment_Brief', '01_Assignment_Brief/Building_Drawings'] for p in (root / folder).glob('*') if p.is_file()]
report['source_sha256'] = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
output = root / '06_Tools/.cache/setup_verification.json'
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(report, ensure_ascii=False, indent=2))
