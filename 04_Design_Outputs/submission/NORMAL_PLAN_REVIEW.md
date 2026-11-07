# Normal-plan drawing and review record

2026-11-07. Working DWG: `../cad/assignment_working_v02.dwg`.

The normal lighting and power sheets use native AutoCAD paper-space layouts,
A3 portrait full bleed, with locked 1:75 viewports. Plot at actual size to retain
scale. Reference architecture, furniture and ceiling-grid layers are greyed in
the versioned working copy; originals are untouched. Legacy Lighting, Power and
circuitory layers are hidden to avoid mixing source annotations with adopted
E-* design layers. The script records the previous layer settings in its sheet
map when plotting returns.

## Labels and design traceability

All92 lighting labels were read back from native objects after synchronization.
The audit is `../data/luminaire_label_sync_audit.json`, with old/new text and
handles. Labels retain the numerical part of the device ID; their prefix is
the circuit letter. Thus LED23 on LC-A is A23*, not a newly numbered device.
A/B/C are22W except four starred28W panels; D is22W and E/F/G are28W.
This matches the report legend and does not change the92-panel/2216W load.
Device positions, circuit assignment and route lengths remain unchanged.

The lighting legend is generated from `lighting_route_results.csv`; the power
legend uses `power_route_results.csv` and `circuits.csv`. These provide the
same phases, conductor sizes and lengths as the calculations and DB schematic.
The common schedule still contains112 components and15 final circuits.

## First rendered PDF review: not accepted for final issue

Both `office_lighting_submission_v01.pdf` and
`office_power_submission_v01.pdf` are readable one-page A3 portrait PDFs.
They were rasterized and visually inspected. Architecture is suitably lighter
than adopted electrical devices; lighting IDs and the bottom circuit schedules
are generally legible.

Corrections required before inclusion in the answer:

- Three northern power-point labels are clipped at the viewport top. Move
  their text below the top wall without moving their points.
- FB03/FB04 text overlaps. Stagger their labels.
- S-A/B/C text crowds at the DB. Stack their labels to the right.
- Recheck route intersections, label-to-point association and all92/13 device
  labels after replotting. Route intersections alone do not prove connection.

`refine_normal_plan_labels.py` defines these label-only corrections and records
their native positions. It must run only after the current plot finishes.
The first plot generated both files, but the AutoCAD plot call remained active;
an automatic PDF open-with prompt was dismissed and cancellation was requested
through the visible progress dialog. Do not restart AutoCAD or rerun the sheet
creation script while this call is live. The layouts and label synchronization
were saved before plotting. Final DWG reopen and source-hash gates remain open.
