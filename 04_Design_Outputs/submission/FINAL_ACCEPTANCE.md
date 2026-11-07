# Historical acceptance for v03

**Superseded by REVIEW_20261108.md and REVISION_V04.md.** Its blanket pass statements are not the current review disposition. The live-application note below describes an earlier session, subsequently closed.

Date:2026-11-07. Release: answer v03 / saved DWG v01.

The requirements below were checked against the original `01_Assignment/BSE3124 Mini Design Assignment-2.docx`, not inferred from previous drafts. Acceptance is for the original three-task course design under the assumptions stated in the answer. It does not certify an installed electrical system or manufacturer products.

| Original requirement | Authoritative delivered evidence | Result |
|---|---|---|
| Ten typical floors, three tenants, ground-floor plant; cooling load1000kW | Answer p2; task1_design_inputs.csv and task1_load_summary.py explicitly distinguish cooling kW, electrical kW and kVA | Pass |
| Estimate building load using CLP COP215; state assumptions | p2 calculation and clauses/appendices; task1_load_summary.csv, task1_capacity_bounds.csv:2452.216–2672.216kVA, adopted2672.216; two1500kVA units, equal allocation, no full-load N−1 | Pass |
| Draw transformer room and main LV room on supplied ground floor; justify location | pp8–9; native TASK1-GROUND-OVERVIEW and TASK1-ROOM-REVIEW; dimensions, assumed equipment, clearances, external access, doors, ventilation and HV/LV interfaces; p2 reasons/conditions | Pass |
| Select one tenant and design lighting/power layouts | Office1, pp11–12;92panels/2216W,13fused power points,7passive controls; native layouts and common devices.csv | Pass |
| Assign circuits to lighting, sockets, floorboxes, fused spurs and other fixed equipment | devices.csv/circuits.csv;112 unique components assigned exactly once to15circuits;13power locations include9floorboxes,3twin sockets,FS01 capacity reservation; no unknown appliance rating invented | Pass |
| Draw MCB board schematic | p10; native TASK2-DB-SCHEMATIC:15ways, phases, source C63,100A4P isolation, individual RCBO L/N paths, PE bypass, local controls, ring return provisions | Pass |
| Explain circuit arrangement/protective selection and assumptions | pp3–4; enclosed-space/pantry separation, phase allocation, ring/radial choices, individual13A fuse limits, inrush/energy/breaking requirements and separate emergency-system assumption | Pass |
| Calculate maximum current demand and corresponding incoming/outgoing cable sizes | pp5–7; office_design_demand.json:peak48.909091A; incoming4C35+CPC16/C63,31.5119m; all15outgoing circuits, methods/factors and lengths tabulated | Pass |
| Cable/protection consistency | calculation_result_gate.json and fault_protection_summary.json: applicable capacity, voltage, disconnection, CPC energy and breaking checks pass under declared conditions; worst full drop3.030671%; P7 fixed equipment has no socket served-area limit | Pass under stated design conditions |
| Complete answer sheets and layout drawings |12-page BSE3124_Answer_Sheets_v03.pdf: official cover +6answer pages +5A3 drawings; Group1 names/IDs verified; editable LaTeX and native DWG included | Pass |
| Native DWG save/reopen and print QA | Native AutoCAD2027 Core Console reopened assignment_submission_v01.dwg:863 registered objects found,92lamp labels,15route lengths,2incoming routes,15DB schedule rows and5required layouts verified; INSUNITS4; read-only hash unchanged. All12final PDF pages rendered and visually inspected | Pass |
| Preserve originals and provide calculation/drawing rationale | Four original manifest SHA256 values unchanged; all10previously tracked originals/references match content, with Git text EOL normalization documented. Official downloaded PDFs additionally hashed. README.md, calculation scripts, common data and LaTeX source explain methods | Pass |

## Exact artifacts and reproducible evidence

`../data/final_submission_manifest.json` records SHA256 values and page dimensions for the final PDF, DWG and included PDF assets. `../data/native_reopen_gate.json` records the native engine/version and route comparisons. Its reproducible runner is `../calculations/verify_saved_dwg_core.py`; the read-only extraction script/log/entity evidence are in `../data/native_reopen/`.

Native reopening is proved by AutoCAD2027 reading the saved DWG, not by DXF inspection. Print quality is supported separately by actual rendered PDFs, not by a plot command return value. Earlier v01 normal plans were rejected; the accepted assets use revision02 label corrections. The final PDF retains A3 landscape/portrait sheet sizes; print at actual size.

## Design conditions retained in the answer

Drawing areas are assumed UFA; equal transformer-zone allocation and equipment planning envelopes are explicit assumptions. The original1000kW is cooling capacity. COP215Rev07 remains the course basis; COP101v16 and EMSD2025 clauses/tables are identified in the answer. Cable allowances, source Ze/PFC, thermal/harmonic factors, point-fuse demand and apparatus total-clearing-energy/inrush performance are declared design conditions. Actual FS01 appliance watts are unknown; emergency/exit systems are assumed independently landlord-supplied. No certified illumination/glare/uniformity or full short-circuit discrimination is asserted. These are stated course boundaries, not unfinished procurement tasks.

## Live application note

The original interactive AutoCAD session remains at a cancelled plotting-progress dialog. Its working DWG was saved and the submitted DWG is byte-identical to that saved file. No unsaved user document was closed and AutoCAD was not restarted. The native reopen gate was completed independently in AutoCAD2027 Core Console, including MEP object-enabler loading. The live dialog issue does not invalidate the saved/reopened artifact or reviewed PDFs; resolving that application's UI session is separate from the submitted coursework.
