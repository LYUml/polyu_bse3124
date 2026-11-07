# Office 1 â€” circuit and cable design basis

Working record, 2026-11-07. The current working cable calculations pass under explicit course design conditions; Task3_answer_working.md is the consolidated answer. Final answer sheets and drawing/control/emergency reconciliation remain.

## Circuit separation

The common device table contains 92 luminaires and 13 power locations. The circuit list now has seven lighting circuits and eight power circuits, P1â€“P8. Pantry wall socket SO03 is assigned to separate P8; P6 serves pantry FB09 and SO01. Their coordinates fall inside the same source PANTRY rectangle; the earlier meeting-area/non-kitchen description is superseded. Fixed equipment connection FS01 remains on separate P7. EMSD Wiring CoP 2025 clause 6E(3)(a), printed p54/PDF p55, requires separate circuits for kitchen socket outlets and fixed appliances. Treat the pantry as a kitchen for this design. P8 is retained as an additional independently protected pantry socket group by design choice. Clause 6E(3)(a) does not require a separate final circuit for every individual pantry outlet. Both P6 and P8 are separated from ordinary office sockets. The CAD label, device table, circuit list and concept schematic were updated together.

FS01 has no confirmed appliance rating. A 13 A reservation is a connection-capacity allowance, not a claimed appliance current or electrical wattage. No zero load is assumed. Product identification remains necessary before calling this a selected equipment circuit.

## Historical nominal-capacity scenario

Use `data/office_capacity_scenario.csv` for the earlier nominal-capacity study. It preserves actual lighting powers at 220 V and conservative PF 0.90; seven socket groups are each provisionally reserved at 32 A, and P7 at 13 A. These socket ratings and phase assignments are scenario inputs, not the adopted protective-device schedule.

EMSD Table 7(1), small offices, permits 90% of lighting current (printed p65/PDF p66). For Code 6E final circuits, use 100% of the largest circuit current plus 50% of all other circuit currents (printed p67/PDF p68). Apply this per phase; reserve P7 at 100% separately. Do not replace this rule by 75% of the sum: that happens to give the same answer for two equal circuits, but gives the wrong answer for three.

| Phase | Lighting before diversity | Socket circuit capacity | Socket demand | P7 reserve | Total demand |
|---|---:|---:|---:|---:|---:|
| L1 | 3.444444 A | 3 Ã— 32 A | 32 + 0.5 Ã— 64 = 64 A | 0 A | 67.100 A |
| L2 | 3.959596 A | 2 Ã— 32 A | 32 + 0.5 Ã— 32 = 48 A | 13 A | 64.563636 A |
| L3 | 3.787879 A | 2 Ã— 32 A | 32 + 0.5 Ã— 32 = 48 A | 0 A | 51.409091 A |

This scenario requires more than 63 A; 80 A is the next planning candidate. Without diversity, the largest phase capacity is 99.444444 A. The choice to apply diversity, switchgear thermal duty and actual circuit demand must be carried into the final answer. Old 14-circuit incoming studies are superseded for current planning. Reproduce with `calculations/office_capacity_reservation.py`; results are in `data/office_capacity_phase_results.csv` and `office_capacity_reservation.json`.

## Working power topology and updated incoming demand

P1–P4 use A1 rings with 6 mm² L/N/CPC and individually 13 A fused point connections. Each ring serves two floor boxes, so its total point-capacity bound is 26 A. P1/P2 ring legs form one uniform bank of four current-carrying pairs; P3/P4 form another. At 40°C and Cg=0.65, each leg has Iz=41×0.87×0.65=23.1855 A, exceeding the Table6(1) 20 A minimum. Solving the intact uniform ring network with both points at 13 A gives maximum leg currents 14.658, 14.885, 15.198 and 15.203 A respectively. Do not apply the radial `In≤Iz` rule to a single ring leg without the standard ring provisions; the calculated leg currents and ring continuity are essential conditions.

P5/P6/P8 are A2 32 A radials with 10 mm² L/N/CPC in a separate uniform three-circuit bank: Iz=57×0.87×0.70=34.713 A. P5 and P8 each have one 13 A fused point; P6 has two. P7 uses a separate 4 mm² radial, B16 protection and a 13 A fused equipment connection; Iz=32×0.87=27.84 A. All point spurs use assumed 0.5 m of 4 mm² cable; the conservative three-circuit spur factor gives Iz=32×0.87×0.70=19.488 A. Actual accessory fuse characteristics and terminal acceptance remain to check. Main 6/10 mm² cables terminate in accessible rated junction/FCU assemblies; they are not assumed to fit ordinary socket terminals. No unfused additional points are permitted by this load model.

The designed service envelopes are 93.378/68.771/72.934/97.001 m² for P1–P4, below the 100 m² A1 limit, and 46.482/29.544/29.544 m² for P5/P6/P8, below the 50 m² A2 limit. These polygons define circuit service coverage on the source coordinate system; they are not surveyed room net areas. The overlap intentionally provides interleaved circuits, so their areas must not be added as office UFA. All associated points lie inside their respective envelopes. Native CAD lengths and polygon areas match the common data.

| Circuit | Main route including vertical allowance | Worst outgoing drop including local spur |
|---|---:|---:|
| P1 | 28.620 m ring | 1.269 V |
| P2 | 35.520 m ring | 1.675 V |
| P3 | 45.220 m ring | 1.937 V |
| P4 | 34.220 m ring | 1.428 V |
| P5 | 15.607 m radial | 0.964 V |
| P6 | 13.864 m radial | 1.310 V |
| P7 | 13.107 m radial | 1.946 V |
| P8 | 15.107 m radial | 0.936 V |

Ring lengths include 2 m at each DB end; radials include 2 m total vertical allowance. These are declared assumptions. Ring voltage drops use a two-feed constant-current network with the same cable along the loop; radial drops sum downstream currents segment by segment. All pass the allocated 4.4 V outgoing budget, which does not establish full upstream voltage drop or fault protection. Containment, furniture/partition coordination and final plotting remain to review. Reproduce with `build_power_routes.py`; source files are `power_route_design_inputs.json`, `power_route_topology.json`, `power_route_segments.csv` and `power_route_results.csv`.

### Adopted working demand after point-fuse limits

With P7 on L3 for balance, the designed point-capacity bounds give phase demands of L1=48.600 A, L2=42.563636 A and L3=48.909091 A after the stated Table7(1) diversity. Use 63 A as the incoming protective-device candidate, subject to cable/fault checks, and a 100 A minimum design busbar rating. The maximum phase point capacity without diversity is 68.444444 A. The historical 80 A scenario above used 32 A nominal capacity for every socket final circuit. The lower working demand is justified by the now-drawn individual 13 A fuses; it is not valid if those fuses are omitted or unfused points are added. P7 remains a capacity reservation, not a known appliance. See `office_design_demand.py` and `data/office_design_demand.json`.

## Original selection notes and remaining coordination

### Lighting routes and working cable selection

Seven native CAD ceiling-route polylines now connect DB-O1 to all 92 working luminaires. DB-O1 is at (73000,31488.1) mm on the lighting plan and (73000,-17889.9) mm on the power plan, using the previously screened south-wall candidate. The 600 Ã— 150 mm cabinet envelope is an assumed planning allowance; access and final cabinet selection remain to coordinate. The route generator uses orthogonal ceiling paths and zonal entry points; LC-D retains the previously checked pantry path. A path crossing a partition denotes a proposed ceiling/service penetration requiring coordination, not proof of a clear opening.

Select 2.5 mmÂ² single-core PVC copper L/N/CPC as the working lighting cable and B10/Type A 30 mA RCBO performance specification. Keep power circuits in separate containment. For seven bunched lighting circuits at assumed 40Â°C, `Iz=24Ã—0.87Ã—0.54=11.2752 A`; every lighting design current is below 10 A, so `Ibâ‰¤Inâ‰¤Iz` passes under these installation conditions. The earlier 1.5 mmÂ² proposal is superseded for this grouped arrangement.

| Circuit | Lamps | Power | Proposed plan path | Path + assumed 2 m vertical allowance | Distributed-load outgoing drop |
|---|---:|---:|---:|---:|---:|
| LC-A | 18 | 402 W | 53.301 m | 55.301 m | 1.340 V |
| LC-B | 17 | 392 W | 55.284 m | 57.284 m | 1.063 V |
| LC-C | 18 | 396 W | 37.299 m | 39.299 m | 0.754 V |
| LC-D | 11 | 242 W | 21.382 m | 23.382 m | 0.337 V |
| LC-E | 14 | 392 W | 28.516 m | 30.516 m | 0.657 V |
| LC-F | 10 | 280 W | 25.453 m | 27.453 m | 0.508 V |
| LC-G | 4 | 112 W | 21.197 m | 23.197 m | 0.212 V |

For each segment, `Î”V=18Ã—I_downstreamÃ—length/1000`, using Table A6(1) continued, col3 (printed p282/PDF p283). Sum segment drops and add the full circuit current through the assumed 2 m common vertical section. All seven outgoing drops are within a deliberately reserved 4.4 V (2% of 220 V) budget; this budget does not establish the actual upstream drop or prove the complete 4% installation check. The data CSV, not this rounded summary, is authoritative. Control wiring, final penetrations and installation details remain to coordinate.

The route result table also reports the maximum permissible external loop impedance at DB-O1 for the reference B10 Zs limit, after subtracting the proposed circuit R1+R2 at 70Â°C. These are acceptance limits, not measured Ze values or passed fault checks. CPC energy withstand and actual device let-through must still be compared. Reproduce with `calculations/build_lighting_routes.py`; shared sources are `lighting_route_design_inputs.json`, `lighting_route_segments.csv`, `lighting_route_results.csv` and `lighting_route_cad_map.json`. The native CAD audit confirms all 92 device endpoints and seven polyline lengths.

EMSD Table 6(1), printed p56/PDF p57, limits A1 30/32 A rings to 100 mÂ², A2 30/32 A radials to 50 mÂ², and A3 20 A radials to 20 mÂ². Increasing conductor size for temperature/grouping does not remove the served-area limit. The note requires corrected capacity at least 20 A for A1/A3 and 30/32 A for A2. Confirm each served area and draw the actual ring/radial topology before adopting it.

For the source single-core PVC copper Method B table, ambient 40Â°C with Ca=0.87 and three bunched circuits with Cg=0.70 gives: 4 mmÂ² capacity `32Ã—0.87Ã—0.70=19.488 A`, 6 mmÂ² `41Ã—0.87Ã—0.70=24.969 A`, and 10 mmÂ² `57Ã—0.87Ã—0.70=34.713 A`. Thus 4 mmÂ² fails the 20 A corrected-capacity condition in this grouping; 6 mmÂ² is a capacity candidate for a ring leg, while a 32 A radial requires at least the 10 mmÂ² candidate under these assumptions. This comparison does not verify ring loading, accessory terminals, cable routes, voltage drop or fault protection.

Neutral conductors must be full sized under 6B(6)(c). Table A5(7), printed p278/PDF p279, addresses triple harmonics in four-/five-core cables; do not silently apply its 0.86 factor to a different cable arrangement. The adopted incoming design is four-core35mm2 PVC copper plus CPC16. Full incoming/outgoing checks now pass under the explicit source and device-performance conditions in fault_design_conditions.json; see Task3_answer_working.md. These are course design conditions, not claimed site measurements or arbitrary product certificates. Controls/emergency loads and final drawings still require reconciliation.


## Task 3 consolidated working answer

See `Task3_answer_working.md`. C63 is at MS-O1 before the incoming cable; DB-O1 has a100A4-pole isolator. Working incoming cable is4C35 PVC Cu+CPC16,31.5119m including an assumed3m allowance,Iz74.0718A. With pre-origin allowance2.2V and feeder drop bound2.521606V, all15 complete circuit drops are within4%; worst3.030671%. Source Ze0.20ohm and PFC<=6kA are adopted course assumptions. Apparatus total clearing energy limits are explicit selection requirements. Local13A fuse conventional fusing current24.7A is below1.45Iz28.2576A for4mm2 spurs; the fuse reference typical pre-arcing figure is not used as total energy. Native incoming route lengths match the common data on both office plans.
