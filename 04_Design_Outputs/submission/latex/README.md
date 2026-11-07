# BSE3124 answer source

This folder contains assignment source and drawing assets. MiKTeX is installed separately in the Windows user profile.

Run build.ps1 from PowerShell. It regenerates tables from current common CSV/JSON data, compiles twice using the installed XeLaTeX, checks diagnostics, and writes the parent folder's BSE3124_Answer_Sheets_v03.pdf. Auxiliary files stay in the ignored build folder.

The official answer-sheet cover is retained. Its source hash is recorded in data/official_cover_provenance.json; Group1 names and student IDs are overlaid from data/group_identity.json without changing the official cover asset. The source DOCX remains unchanged. Body text follows the original Task 1–3 structure.

After design changes, update common data and affected calculations, replot the affected CAD sheets, then rebuild this report. The builder does not silently redraw the DWG. Included assets allow rebuilding without the internal QA folder.

Text pages are A4. Drawing sheets retain their A3 landscape/portrait dimensions and scales; print them at actual size.

Final v03 includes all five drawing sheets. PDF visual review and native AutoCAD2027 Core Console reopening are recorded in FINAL_ACCEPTANCE.md. The four original-source manifest hashes match; the source DOCX and cover asset remain unchanged.
