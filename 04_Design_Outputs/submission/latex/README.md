# BSE3124 answer source

This folder contains assignment source and drawing assets. MiKTeX is installed separately in the Windows user profile.

Run build.ps1 from PowerShell. It regenerates tables from current common CSV/JSON data, compiles twice using the installed XeLaTeX, checks diagnostics, and writes the parent folder's BSE3124_Answer_Sheets_v01.pdf. Auxiliary files stay in the ignored build folder.

The official answer-sheet cover is retained. Its source hash is recorded in data/official_cover_provenance.json; identity blanks await group details. The source DOCX remains unchanged. Body text follows the original Task 1–3 structure.

After design changes, update common data and affected calculations, replot the affected CAD sheets, then rebuild this report. The builder does not silently redraw the DWG. Included assets allow rebuilding without the internal QA folder.

Text pages are A4. Drawing sheets retain their A3 landscape dimensions and scales; print them at actual size.

Current v01 is a working submission. Normal-plan PDF reviews and final DWG save/reopen/source-hash gates remain.
