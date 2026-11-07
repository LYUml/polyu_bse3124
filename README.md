# BSE3124 — Group 1

Final submission: [Report PDF](04_Final_Report/BSE3124_Final.pdf) · [AutoCAD drawing](03_Design_Drawings/BSE3124_Final.dwg) · [中文说明](README.zh-CN.md)

| Folder | Contents |
|---|---|
| 01_Assignment_Brief | Original assignment, teacher answer-sheet template, and original building drawings in Building_Drawings. Originals are preserved byte-for-byte. |
| 02_References | Course references, downloaded regulations/manufacturer documents and source notes. |
| 03_Design_Drawings | One final editable DWG, for AutoCAD 2027. |
| 04_Final_Report | One final report PDF; editable LaTeX, corrected template and drawing assets in source. |
| 05_Calculations | Common CSV/JSON data and verification evidence in data; calculation/export scripts in scripts. |
| 06_Tools | Environment setup, dependency restoration and AutoCAD connector tools. |

The 18-page report keeps Task 1 on pp.2–5, Task 2 on pp.6–14 and Task 3 on pp.15–18. Drawing PDFs inside the report source are build dependencies, not additional submission versions.

Build: run `04_Final_Report/source/build.ps1`. Verify with `.venv/Scripts/python.exe 05_Calculations/scripts/verify_final.py`. Native drawing verification and plotting scripts are alongside it. Start with PROJECT_SPEC.md for project instructions.

Hidden .venv, .codex and .agents folders support the local environment. Earlier versions are available through Git history.
