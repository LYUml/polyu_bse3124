# BSE3124 Electrical Installation Design

**English** | [简体中文](README.zh-CN.md)

Group1 — BSE3124 Electricity and Buildings, PolyU,2026/27 Semester1.

## Final submission

- [Final answer PDF](04_Design_Outputs/submission/BSE3124_Final.pdf)
- [Final editable AutoCAD DWG](04_Design_Outputs/cad/BSE3124_Final.dwg)
- [Editable LaTeX source and build instructions](04_Design_Outputs/submission/source/README.md)
- [Validation and design conditions](04_Design_Outputs/submission/VALIDATION.md)

The19-page answer groups each task continuously: cover,p1; Task1,p2–5; Task2,p6–14; Task3,p15–19. Relevant drawings sit within their task. Only one final submission is retained; older versions and temporary outputs have been removed from the working folder. Git history retains earlier work.

## Workspace

01_Assignment,02_Building_Drawings and03_Technical_References contain preserved originals.04_Design_Outputs contains the final submission, source assets, common engineering data and calculation/verification scripts.05_Tools contains environment tools;06_Research contains reference research. Hidden environment/configuration folders support the workflow.

Build the answer with `04_Design_Outputs/submission/source/build.ps1`. Check final content/integrity with `.venv/Scripts/python.exe 04_Design_Outputs/calculations/verify_final.py`; native DWG checking uses `verify_final_dwg.py` and AutoCAD2027 Core Console. Rendering and visual review remain separate from calculation checks.

The result is a course design under explicitly stated conditions, not installed-system or product certification. See [PROJECT_SPEC.md](PROJECT_SPEC.md) and [AGENTS.md](AGENTS.md) for execution rules.
