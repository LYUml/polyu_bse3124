# BSE3124 Electrical Installation Design

**English** | [简体中文](README.zh-CN.md)

Group 1 mini-design assignment for BSE3124 Electricity and Buildings, The Hong Kong Polytechnic University, 2026/27 Semester 1.

## Final deliverables

- [Final answer sheets — 19-page PDF](04_Design_Outputs/submission/BSE3124_Answer_Sheets_v04.pdf)
- [Blank teacher-template facsimile](04_Design_Outputs/submission/BSE3124_Template_LaTeX.pdf)
- [Editable AutoCAD drawing](04_Design_Outputs/cad/assignment_submission_v02.dwg)
- [Requirement-by-requirement acceptance record](04_Design_Outputs/submission/REVISION_V04.md)
- [Calculation and drawing guide (Chinese)](04_Design_Outputs/submission/README.md)
- [Editable LaTeX source and build instructions](04_Design_Outputs/submission/latex_v04/README.md)

Tasks 1–3 have been checked against the original assignment under the course-design assumptions stated in the answer. The package covers building load estimation, transformer/LV room layouts, Office 1 lighting and power layouts, the distribution-board schematic, and incoming/outgoing demand and cable sizing. It is a course submission, not certification of an installed system.

## Repository layout

| Directory | Contents |
|---|---|
| [01_Assignment](01_Assignment/) | Original assignment and answer-sheet template |
| [02_Building_Drawings](02_Building_Drawings/) | Original DWG and reference drawing, preserved unchanged |
| [03_Technical_References](03_Technical_References/) | Course references, official documents and download records |
| [04_Design_Outputs](04_Design_Outputs/) | Shared data, calculation scripts, current CAD/PDF drawings, submission files and archived working outputs |
| [05_Tools](05_Tools/) | Tool scripts, dependency snapshots and third-party AutoCAD MCP source |
| [06_Research](06_Research/) | Resource catalog and environment-verification records |

The `cad` folder retains versioned submission DWGs and the working DWG; `pdf` retains the three adopted Office 1 sheets. Superseded drafts, test plots and recovery copies are collected in the [dated output archive](04_Design_Outputs/archive/2026-11-07/README.md). Temporary QA files and crash logs remain local. Historical studies do not define the final adopted design.

## Working with the project

Use AutoCAD 2027 for DWG files. The LaTeX report builds with XeLaTeX; MiKTeX is installed in the local Windows user profile, outside this repository. Run `04_Design_Outputs/submission/latex_v04/build.ps1` to rebuild the answer from the shared data and included drawing assets.

The [project specification (Chinese)](PROJECT_SPEC.md) defines the execution contract, data rules and acceptance gates. [AGENTS.md](AGENTS.md) supplies instructions for subsequent agent work. `.venv` contains the local Python environment, `.codex` the project configuration, and `.agents` the project skills.

Environment/tool checks, run from the repository root:

```powershell
.venv/Scripts/python.exe 05_Tools/verify_setup.py
.venv/Scripts/python.exe 05_Tools/smoke_mcp.py
```

These are setup checks; final design acceptance is recorded separately in the submission evidence.

## References and verification

- [Resource catalog](06_Research/RESOURCE_CATALOG.md)
- [Environment-verification record](06_Research/verification/setup_verification.json)
- [MCP smoke-test record](06_Research/verification/mcp_smoke_test.json)
- [Final artifact hashes and verification index](04_Design_Outputs/data/revision_v04_manifest.json)
