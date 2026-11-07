"""Download verified public reference links; preserve metadata and SHA256."""
from pathlib import Path
import hashlib, json, urllib.request

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / '03_Technical_References' / 'Official'
SOURCES = [
    ('EMSD_COP_2025_EN.pdf', 'https://www.emsd.gov.hk/filemanager/en/content_443/COP_E_2025.pdf', 'EMSD wiring CoP 2025'),
    ('CLP_COP101_v16_text.pdf', 'https://www.clp.com.hk/content/dam/clphk/documents/customer-service-site/open-and-close-account-site/cop-101-distribution-substation-design-site/Cop101%20version%2016%20document.pdf', 'CLP COP101 v16 text'),
    ('CLP_COP101_v16_drawings.pdf', 'https://www.clp.com.hk/content/dam/clphk/documents/customer-service-site/open-and-close-account-site/cop-101-distribution-substation-design-site/COP%20101%20version%2016%20drawings.pdf', 'CLP COP101 v16 drawings'),
    ('EMSD_BEC_2024_EN.pdf', 'https://www.emsd.gov.hk/beeo/en/pee/BEC_2024_ENG.pdf', 'EMSD BEC 2024'),
    ('CLP_Supply_Rules_Aug2026.pdf', 'https://www.clp.com.hk/content/dam/clphk/documents/customer-service-site/open-and-close-account-site/supply-rules-site/supplyrules_eng_aug26_R3.pdf', 'CLP Supply Rules linked by official index'),
    ('CLP_Metering_Guide_v10.pdf', 'https://www.clp.com.hk/content/dam/clphk/documents/customer-service-site/open-and-close-account-site/meter-installation-guideline-site/GuideToSupply_(V10)_Eng_Final.pdf', 'CLP metering guide v10'),
]

if __name__ == '__main__':
    DEST.mkdir(parents=True, exist_ok=True)
    records = []
    for filename, url, title in SOURCES:
        record = dict(file=filename, url=url, title=title, retrieved_date='2026-11-07')
        try:
            target = DEST / filename
            if target.exists():
                data = target.read_bytes()
            else:
                request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(request, timeout=50) as response:
                    data = response.read()
            if not data.startswith(b'%PDF-'):
                raise ValueError('Response is not a PDF')
            target.write_bytes(data)
            record.update(status='downloaded', bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
        except Exception as exc:
            record.update(status='failed', error=str(exc))
        records.append(record)
        print(filename, record['status'], flush=True)
    (DEST / 'sources.json').write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
