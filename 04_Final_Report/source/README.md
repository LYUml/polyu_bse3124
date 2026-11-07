# Editable final answer source

Run `./build.ps1` to compile `../BSE3124_Final.pdf` with the local MiKTeX XeLaTeX installation. No earlier version or generator is required.

`main.tex` contains the official-template answer overlays and document order. `task1.tex`, `task2.tex` and `task3.tex` contain detailed answers; `lighting_basis.tex` and `installation_notes.tex` support Task2. Edit these files directly. If engineering data changes, update the corresponding answer tables and rerun the calculations and final verification before delivery.

Order: cover; Task1 answers and ground-floor drawings; Task2 answers, teacher's board template, lighting/power/DB and installation-detail sheets; Task3 calculations. Each task is one continuous part. Repeated task headers identify continuation pages, not a second answer section.

`assets/official-template.docx` is a corrected copy of the teacher's Word template: the isolated SimSun “E” in “Electricity” uses Times New Roman, matching the rest of the title. Microsoft Word exported this copy to `assets/official-template.pdf`; pages are used in their relevant task sections. `assets/continuation-template.pdf` reuses the three task pages' original vector frames, with prompt text removed and the full corresponding task heading followed by “(continued)” in 12 pt Times New Roman Bold at the original baseline. Original assignment files remain unchanged. All answer text and equations are editable LaTeX.

`assets` holds the six final drawing sheets and template needed to build the answer. These are source dependencies, not alternative submission versions. The full final DWG is in `../../03_Design_Drawings/BSE3124_Final.dwg`.

To regenerate drawing assets from the saved final DWG, run `../../05_Calculations/scripts/export_final_dwg.py` with the project Python environment, then `./build.ps1`. Re-run `verify_final_dwg.py` and `verify_final.py`; visually review the rendered PDF before release. The exporter rejects blank plots and checks that plotting does not change the DWG.

The build runs finalize_pdf.py using the installed bundled Python/PyMuPDF runtime to orient the teacher board sheet horizontally and fill its title block and circuit positions. Client is N/A because the assignment specifies no commissioning client.
