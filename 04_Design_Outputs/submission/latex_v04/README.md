# Word-template facsimile in LaTeX

Run `./build.ps1` with the local MiKTeX installation and project Python environment. It generates the 19-page answer v04 and the five-page blank template. It does not start AutoCAD or modify drawings.

The original Word-exported pages are retained in `assets/official-template.pdf` at their original size. `template_blank.tex` reproduces those five pages; `main.tex` fills their blank areas and adds framed technical continuation pages and six CAD sheets. This hybrid method preserves original wording, frame placement, fonts and the embedded board image more faithfully than reflow conversion. The original labels are embedded PDF content, not newly editable LaTeX text. All answers, equations, tables and continuation text are editable LaTeX.

The generator is `../../calculations/build_answer_v04.py`. Edit that file for persistent changes to generated content, or edit generated `.tex` files and compile directly if regeneration is not desired. The complete technical body currently derives from retained `../latex/main.tex`, with the v04 corrections applied by the new generator. Do not delete that historical source dependency. `template_contract.json` and `artifact.md` record the source hash, geometry and editable slots.

The five-page blank template has the same page dimensions as the Word export. At 144 dpi, page 5 is pixel-identical; pages 1–4 have small glyph-edge rendering differences (mean absolute channel difference at most 0.023 on the 0–255 scale). This is not a claim that every pixel or PDF byte is identical. The filled answer intentionally adds text and continuation pages.

The source Word file remains unchanged in `01_Assignment`. Pandoc is not needed for this approach. A pure native TeX recreation of every original label is not what this implementation claims.

Reproducing the new CAD detail sheet is a separate guarded operation in `add_revision_details.py`; it refuses to overwrite an existing v02 DWG. Use `verify_saved_dwg_core.py --revision v02` for read-only native validation. Review every final rendered page after changing layout or content.
