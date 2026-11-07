# Task 1 — Building load and plantroom proposal

Status: consolidated answer draft for review; plantroom drawing and equipment interfaces require completion.

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

## Equipment and room coordination criteria

COP101 v16 clause 4.3 (printed page 4, PDF page 6) gives HV panel clearances of 1000 mm at the rear, 1800 mm at the front and 750 mm on the other sides. Distribution transformers require 900 mm around LV terminals and 750 mm on the other sides. These requirements must be checked against actual equipment and take precedence over treating isolated typical-layout dimensions as general clearances.

Clause 4.4.3 gives a minimum transformer plinth of 1800 × 1350 mm; the actual foundation depends on transformer type and rating. This is not the transformer equipment footprint. The foundation requires at least 9000 kg support capacity under clause 4.4.1. Clause 5.1.2 requires at least 3 m plant-delivery width and no more than 20 m from the nearest loading/unloading area. Under clause 5.1.5, minimum clear headroom is 3.6 m with transformers and 630 mm exhaust fans, or 3.8 m with 800 mm fans. The actual building section and external site arrangement must be coordinated.

The customer LV room currently contains six planning cabinet envelopes: three for Zone A and three for Zone B. Each is assumed 1140 mm wide and uses the course ABB MD190 rear-access reference depth of 1010 mm. The combined envelope is 6840 mm long, at x=10000–16840 and y=23055.584–24065.584 mm. The room envelope provides nominal front/rear allowances of 1500/990 mm before wall construction and door checks. Panel widths and quantities are planning allowances requiring confirmation from the actual feeder schedule and switchboard supplier.

## Work required before final submission

The current working drawing is `04_Design_Outputs/cad/assignment_working_v02.dwg`; the recovered `reopen_check.dwg` has been retained. The v02 study adds one 3000 × 1000 mm HV equipment reservation and two 2200 × 1800 mm transformer reservations. These are explicitly assumed space allowances, not manufacturer dimensions. They are recorded in `data/task1_equipment_reservations.csv`. The required directional clearance envelopes fit inside the reserved room: HV envelope (9250,17005.584)–(13750,20805.584), transformer A envelope (13950,17705.584)–(17650,21155.584), and transformer B envelope (17650,17705.584)–(21350,21155.584) mm. These three envelopes do not overlap in plan. Transformer LV terminals face north toward the customer switchroom. This proves geometric room containment for the assumed equipment envelopes only.

Proposed south-side access reservations are 4000 mm wide for HV equipment and 3000 mm for each transformer, with a 3000 mm external apron depth. A separate 3000 mm LV access reservation is shown west of the LV room. Their locations and the availability of external open space are design proposals; existing architectural walls have not been removed. Door leaves/openings, structural works, fire separation, ventilation, trenches and the complete route from the unloading area remain to detail. The original schematic transformer labels have been moved onto a hidden superseded layer so that the new reservation IDs are unambiguous. The additive drawing script and CAD-handle report document how the geometry was produced.

Complete the actual transformer/HV equipment outlines, LV switchboard sections, doors, maintenance clearances, external route and ventilation indications on the ground-floor drawing; verify them against the CLP standard drawing and selected equipment. Reconcile the UFA assumption and public-services/AC overlap, allocate loads between sections, and visually inspect the final plotted sheet. Current room rectangles and schematic labels alone do not establish these checks.

Reproduction: edit the sourced parameters in `04_Design_Outputs/data/task1_design_inputs.csv`, then run `04_Design_Outputs/calculations/task1_load_summary.py`. Numerical outputs are `task1_load_summary.csv` and `task1_capacity_bounds.csv` in the same data directory. The script checks normal capacity at both overlap bounds and confirms that full-load N−1 operation is unavailable. Detailed evidence and historical checks are in `Task1计算依据.md`.
