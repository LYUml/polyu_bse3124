# Task 1 — Building load and plantroom proposal

Status: consolidated course-design answer draft with a two-sheet drawing review. This is not final assignment acceptance; conditional equipment/site interfaces and Tasks 2/3 remain.

## Design basis and assumptions

The building has ten identical office floors and one ground floor. Adopt the drawing annotations of 309, 309 and 410 m² as the provisional office usable floor areas for the course load estimate. This is an explicit assumption: the annotations have not been independently reconciled with the UFA exclusions in COP215 clause 3.1.2. Do not add the separately measured partial office rectangles to these areas.

Use the supplied CLP COP215 Rev07 (September 2012) as the course load-assessment basis. Adopt packaged air-cooled central air conditioning, with a preliminary electrical power factor of 0.90. The assignment specifies 1000 kW of total building cooling capacity. Five lifts are assumed from the ground-floor drawing; use the COP215 general public-services reference of 40 kVA per lift until individual plant schedules are available.

## Calculation

| Component | Calculation | Result |
|---|---|---:|
| Office UFA | 10 × (309 + 309 + 410) | 10,280 m² |
| Office ADMD | 10,280 × 0.16 kVA/m², Appendix 2 | 1644.800 kVA |
| Cooling capacity | Assignment | 1000 kW cooling |
| Air-conditioning electrical input | (1000 / 3.51685) × 1.85 kW/TR, Appendix 7 | 526.039 kW |
| Air-conditioning apparent load | 526.039 / 0.90 | 584.488 kVA |
| Public-services reference | 5 × 40 kVA/lift, clauses 3.1.6 and 3.3.1 | 200.000 kVA |
| Unreconciled reservation envelope | 1644.800 + 584.488 + 200.000 | 2429.288 kVA |
| Two-zone reservation envelope | 2429.288 × 1.1, clause 3.1.7 | 2672.216 kVA |

The public-services reference includes lobby air conditioning, as well as public lighting, lifts, pumps and fire services. As the specified cooling capacity is for the whole building, the sum may contain overlapping lobby AC load. Let X kVA be the duplicated share. The reconciled assessed load for the proposed two-zone arrangement is `1.1 × (2429.288 − X)` kVA, with X requiring confirmation from the mechanical-services schedule. For preliminary space and capacity reservation, retain X = 0 as a conservative envelope. This does not mean the true overlap is zero, or that the envelope is a verified maximum demand. No additional public lighting/pump/fire-service allowance is added on top of the aggregate reference.

The possible duplicated share is bounded by the smaller of the two overlapping allowances: `0 ≤ X ≤ min(584.488, 200) = 200 kVA`. Thus this course assessment model gives a two-zone load between 2452.216 and 2672.216 kVA. This is a mathematical bound, not a prediction that the lobby consumes 200 kVA. Adopt the upper bound, 2672.216 kVA, for the proposed transformer capacity reservation. Resolving lobby AC overlap would reduce the assessment within this range and does not change the proposed two-transformer capacity under the equal-zone assumption. Other assumptions, including UFA, plant type and public-services assessment, remain applicable.

| Capacity check | Lower load bound | Adopted upper load bound |
|---|---:|---:|
| Building assessment | 2452.216 kVA | 2672.216 kVA |
| Equal load per transformer | 1226.108 kVA | 1336.108 kVA |
| Margin against combined 3000 kVA | 547.784 kVA | 327.784 kVA |
| Normal operation at 1500 kVA per unit | Within rating | Within rating |
| Full-load operation with one unit unavailable | Exceeds remaining rating | Exceeds remaining rating |

These checks establish capacity within the declared assessment model. They do not establish fault duty, protection settings, manufacturer dimensions, installation approval or the actual distribution of mechanical plant between supply zones.

## Transformer and LV arrangement

Study two 1500 kVA transformers supplying two separate LV bus sections. Their combined 3000 kVA nameplate capacity exceeds the 2672.216 kVA reservation envelope by 327.784 kVA. Under an equal split, each section carries 1336.108 kVA, approximately 2030 A at balanced 380 V three-phase supply; each transformer has a nominal current of about 2279 A. The equal split is a planning assumption and must be replaced by a floor/central-plant allocation before setting protection.

The 1500 kVA rating is a proposed course design basis requiring confirmation against CLP available equipment. Normal operation uses separate sources. Any bus coupler requires supplier acceptance, suitable four-pole devices and mechanical/electrical interlocking to prevent unauthorised parallel operation, consistent with EMSD Wiring CoP 2025 clause 6B(1)(c). The arrangement does not provide full-load N−1 capacity: with one transformer unavailable, load shedding or restricted operation is required.

## Ground-floor location and justification

The current CAD study reserves a transformer/HV room at (9000,16105.584) to (21430,21555.584) mm, using the 12430 × 5450 mm two-transformer standard-layout reference T-COP-10250-D-E33-0101-03 (COP101 v16 drawings, PDF page 2). The adjacent customer LV room study occupies (9000,21555.584) to (21430,25055.584) mm. Its 3500 mm depth is a planning assumption, not a dimension specified by CLP.

The proposed perimeter location can support direct external access, short interfaces between transformers and customer switchgear, and separation from tenant accommodation, subject to the following site assumptions being shown and checked on the final drawing: the south side provides open-air access; a clear equipment transport route can be reserved; structural elements and services permit the room; and the LV room has an independent suitable entrance. COP101 v16 clauses 9.3.1–9.3.2.1 require perimeter separation and direct outdoor ground-floor access; clause 5.11 includes a 3 m × 3 m transport route requirement. The supplied plan does not prove the external road or route, so these remain explicit proposal conditions.

COP101 clauses 6.1–6.4 require ventilation design. For the proposed total 3000 kVA capacity, the cited effective inlet-louvre area reference is at least 1.12 m²; effective area is not the gross louvre frame area. Actual transformer losses, airflow, outlet arrangements and any mechanical ventilation must be coordinated. Service openings between rooms require the relevant fire-resisting sealing under clause 9.3.3.

Reserve two low-level inlet louvres, each 600 mm wide × 2000 mm high, in the south-wall piers between the proposed plant openings. At an explicitly assumed 50% free-area ratio, the effective area is `2 × 0.6 × 2.0 × 0.50 = 1.20 m²`, exceeding the 1.12 m² reference in clause 6.3 (printed p23/PDF p25). A selected louvre must have certified free area of at least `1.12 / 2.4 = 46.67%`; the present assumption is not a product certificate. Two high-level 630 mm fan symbols indicate the clause 6.4 reference arrangement for ground-level transformers dissipating about 15 kW each. Actual losses have not been obtained, so fan selection, pressure loss and acoustic performance remain conditional. Clause 6.2 places the exhaust outlet at least 2.5 m above footpath/street level and directs the discharge away from personnel.

The proposed LV interface routes terminate at the two LV incomer reservations. Route A is 8.03 m in plan and route B is 8.31 m. Adding an assumed total 2.0 m per route for vertical changes and terminations gives design allowances of 10.03 m and 10.31 m respectively, within the 20 m limit in clause 5.5.2.2 (printed p16/PDF p18). That clause specifies a 1000 mm wide × 1100 mm deep trench for four MCTs. The two proposed parallel route centre-lines are separated by 1100 mm in their common horizontal region, allowing 100 mm between the nominal 1000 mm trench widths. These are covered trench reservations requiring structural coordination; clear working passages must remain usable. HV and LV cables require segregated trenches under clause 5.5. The magenta lines show the LV interfaces only; they do not establish HV cable routing or conductor sizes. Reproduce the calculations with `calculations/task1_ventilation_interfaces.py`; source values, routes and limitations are in `data/task1_ventilation_interfaces.json`.

## Equipment and room coordination criteria

COP101 v16 clause 4.3 (printed page 4, PDF page 6) gives HV panel clearances of 1000 mm at the rear, 1800 mm at the front and 750 mm on the other sides. Distribution transformers require 900 mm around LV terminals and 750 mm on the other sides. These requirements must be checked against actual equipment and take precedence over treating isolated typical-layout dimensions as general clearances.

Clause 4.4.3 gives a minimum transformer plinth of 1800 × 1350 mm; the actual foundation depends on transformer type and rating. This is not the transformer equipment footprint. The foundation requires at least 9000 kg support capacity under clause 4.4.1. Clause 5.1.2 requires at least 3 m plant-delivery width and no more than 20 m from the nearest loading/unloading area. Under clause 5.1.5, minimum clear headroom is 3.6 m with transformers and 630 mm exhaust fans, or 3.8 m with 800 mm fans. The actual building section and external site arrangement must be coordinated.

The customer LV room currently contains six planning cabinet envelopes: three for Zone A and three for Zone B. Each is assumed 1140 mm wide and uses the course ABB MD190 rear-access reference depth of 1010 mm. The combined envelope is 6840 mm long, at x=10000–16840 and y=23055.584–24065.584 mm. The room envelope provides nominal front/rear allowances of 1500/990 mm before wall construction and door checks. Panel widths and quantities are planning allowances requiring confirmation from the actual feeder schedule and switchboard supplier.

## Work required before final submission

The current working drawing is `04_Design_Outputs/cad/assignment_working_v02.dwg`; the recovered `reopen_check.dwg` has been retained. The v02 study adds one 3000 × 1000 mm HV equipment reservation and two 2200 × 1800 mm transformer reservations. These are explicitly assumed space allowances, not manufacturer dimensions. They are recorded in `data/task1_equipment_reservations.csv`. The required directional clearance envelopes fit inside the reserved room: HV envelope (9250,17005.584)–(13750,20805.584), transformer A envelope (13950,17705.584)–(17650,21155.584), and transformer B envelope (17650,17705.584)–(21350,21155.584) mm. These three envelopes do not overlap in plan. Transformer LV terminals face north toward the customer switchroom. This proves geometric room containment for the assumed equipment envelopes only.

Proposed south-side access reservations are 4000 mm wide for HV equipment and 3000 mm for each transformer, with a 3000 mm external apron depth. A separate 3000 mm LV access reservation is shown west of the LV room. Their locations and the availability of external open space are design proposals; existing architectural walls have not been removed. Door leaves/openings, structural works, fire separation, ventilation, trenches and the complete route from the unloading area remain to detail. The original schematic transformer labels have been moved onto a hidden superseded layer so that the new reservation IDs are unambiguous. The additive drawing script and CAD-handle report document how the geometry was produced.

The two-sheet review is `submission/Task1_drawings_review.pdf`: ground-floor overview at 1:200 and room detail at 1:75 on A3. Both sheets were rendered and visually checked. The detail includes native room dimensions 12430, 5450 and 3500 mm, proposed outward doors and separate HV/LV route centre-lines. Plant door proposals are 4000 mm wide for the HV bay and 3000 mm for each transformer, with assumed 2800 mm height; actual clear openings depend on frames and equipment. Shared 180-degree sweep zones require sequential opening of adjacent plant doors. A designated personnel wicket is proposed at TX-A; detailed escape/hardware coordination remains. COP101 5.6.1.1–5.6.1.2 (printed p18/PDF p20) provides the transformer/HV door references. The drawing preserves architectural walls and identifies the openings as proposed alteration work.

For final coordination, confirm actual transformer/HV equipment, cabinet ratings and dimensions, certified louvre/fan performance, external access route and architectural openings. Carry the UFA, system and equal supply-zone assumptions into the answer sheets. The AC/public overlap is bounded and the conservative assessment adopted above; it is not an unresolved arithmetic input to the capacity reservation. Full-load N−1 is not provided.

Reproduction: edit the sourced parameters in `04_Design_Outputs/data/task1_design_inputs.csv`, then run `04_Design_Outputs/calculations/task1_load_summary.py`. Numerical outputs are `task1_load_summary.csv` and `task1_capacity_bounds.csv` in the same data directory. The script checks normal capacity at both overlap bounds and confirms that full-load N−1 operation is unavailable. Detailed evidence and historical checks are in `Task1计算依据.md`.
