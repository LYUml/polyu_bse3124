# Review corrections and template fidelity

Date: 2026-11-08. Current release: answer v04, native DWG v02. This record supersedes the blanket acceptance wording for v03. It records course-design checks under declared assumptions, not site or manufacturer certification.

| Review item | Resolution and evidence |
|---|---|
| R1 Ring overload proof | Removed synthetic ring-leg I2 from fault_protection_design.py. A1 now checks 32A protection, minimum conductor size, corrected Iz>=20A, service envelope<=100m² and nominal leg current<=Iz, with explicit 6C/6E/Table6(1) arrangement conditions. Exactly two individually fused taps per ring; continuity remains an installation condition. The nominal network solution is supplementary, not a fuse operating characteristic. |
| R2 Final lighting basis | final_lighting_basis.py uses all92 final lamps and actual22/28W settings with retained manufacturer LDT. Profiles are checked by solid-angle integration; separate zone grids use0.2m maximum spacing, MF0.8 and assumed1.9m height above the workplane. Mean direct maintained values592.9/546.3/588.5/502.9lx meet the adopted500lx average target. At2.2m the south-east result447.2lx fails: height restriction is explicit. Approximate room geometry and poor perimeter uniformity remain disclosed; no glare/uniformity certification is asserted. |
| R3 Conditional apparatus checks | Answer and CAD detail distinguish required Ze/PFC, breaking capacity, total energy and inrush specifications from independently verified manufacturer products. No all-product-compliance claim. |
| R4 Fused assemblies | New native DESIGN-DETAILS sheet illustrates one switched13A FCU before each4mm² spur, all four floorbox outlets/twin socket outlets sharing that capacity, unswitched PE and appropriate main terminals. Capacity is intended continuous demand, not instantaneous clamping. |
| R5 Grouping | Detail and answer identify six separated banks, within-bank counts/factors, Method B and horizontal cable separation per EMSD A5(3) Note2. Coincident plan routes mean routing corridors, not common containment. A partition alone is not thermal separation. Recalculate if installation conditions differ. |
| R6 Evidence claims | Saved-DWG checks, source preservation, conditional engineering calculations, lighting assumptions and visual PDF review are reported separately. Designed coverage envelopes are not called measured UFA. |
| Word template | All five original exported pages retained, including task frames/prompts and sideways8-way TPN graphic. Native LaTeX answers occupy blank slots; the board page contains a phase/way allocation table, with the detailed appended schematic governing L/N/PE. Eight technical continuation pages and six CAD sheets follow. Blank facsimile supplied separately. |

## Verification

- AutoCAD2027 Core Console independently reopened v02:940 registered handles found,92labels,15route lengths,2incoming routes,15DB rows and6required layouts. Read-only hash unchanged. No live user document was closed or changed in this revision.
- Lamp/circuit count and connected load remain92/15/2216W. Demand remains48.909091A; feeder selection and voltage-drop values are unchanged. All15 conditional protection checks pass using the corrected ring method.
- The19-page answer was rendered and visually reviewed, including the six drawing pages. No overfull boxes or undefined references in the LaTeX build. Original template page dimensions are retained; CAD sheets remain their original A3 sizes.
- Blank-template144dpi comparison: page5 pixel-identical; pages1–4 mean absolute channel difference<=0.023/255 due to glyph rendering. This is high-fidelity reuse, not a claim of universal pixel identity or fully native re-typesetting.
- Original source hashes and current artifact hashes are checked in revision_v04_manifest.json. Earlier v03 PDF/DWG remain intact as versioned history.

## Remaining declared conditions

Office UFA, equipment footprints, source Ze/PFC, vertical cable allowances, equal transformer-zone allocation and apparatus performance remain stated course assumptions/specifications. Lighting average checks use adopted geometry and mounting height, not a surveyed/certified lighting model. The south-east height condition is essential. No full-load N−1, full short-circuit selectivity, glare/uniformity certification or installed-system compliance is claimed.

The current deliverables are complete for the stated course-design scope with these explicit boundaries. Read this record rather than treating a Boolean script result as unrestricted engineering approval.
