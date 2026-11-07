# Editable final answer source

Run `./build.ps1` to compile `../BSE3124_Final.pdf` with the local MiKTeX XeLaTeX installation. No earlier version or generator is required.

`main.tex` contains the official-template answer overlays and document order. `task1.tex`, `task2.tex` and `task3.tex` contain detailed answers; `lighting_basis.tex` and `installation_notes.tex` support Task2. Edit these files directly. If engineering data changes, update the corresponding answer tables and rerun the calculations and final verification before delivery.

Order: cover; Task1 answers and ground-floor drawings; Task2 answers, teacher's board template, lighting/power/DB and installation-detail sheets; Task3 calculations. Each task is one continuous part. Repeated task headers identify continuation pages, not a second answer section.

The teacher's original five-page Word export is retained in `assets/official-template.pdf`; pages are used in their relevant task sections. Original labels/frame lettering are embedded PDF content; all new answer text and equations are editable LaTeX. This is a high-fidelity hybrid template, not pure TeX re-typesetting of every original label. Original Word files remain unchanged.

`assets` holds the six final drawing sheets and template needed to build the answer. These are source dependencies, not alternative submission versions. The full final DWG is in `../../cad/BSE3124_Final.dwg`.
