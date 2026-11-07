# Office 1 — circuit and cable design basis

Working record, 2026-11-07. This is not the completed answer sheet or a passed cable design.

## Circuit separation

The common device table contains 92 luminaires and 13 power locations. The circuit list now has seven lighting circuits and eight power circuits, P1–P8. Pantry wall socket SO03 is assigned to separate P8; P6 serves meeting-area FB09 and SO01 only. Fixed equipment connection FS01 remains on separate P7. EMSD Wiring CoP 2025 clause 6E(3)(a), printed p54/PDF p55, requires separate circuits for kitchen socket outlets and fixed appliances. Treat the pantry as a kitchen for this design. This corrects the previous shared pantry/meeting socket proposal. The CAD label, device table, circuit list and concept schematic were updated together.

FS01 has no confirmed appliance rating. A 13 A reservation is a connection-capacity allowance, not a claimed appliance current or electrical wattage. No zero load is assumed. Product identification remains necessary before calling this a selected equipment circuit.

## Current-demand calculation

Use `data/office_capacity_scenario.csv` for the current capacity study. It preserves actual lighting powers at 220 V and conservative PF 0.90; seven socket groups are each provisionally reserved at 32 A, and P7 at 13 A. These socket ratings and phase assignments are scenario inputs, not the adopted protective-device schedule.

EMSD Table 7(1), small offices, permits 90% of lighting current (printed p65/PDF p66). For Code 6E final circuits, use 100% of the largest circuit current plus 50% of all other circuit currents (printed p67/PDF p68). Apply this per phase; reserve P7 at 100% separately. Do not replace this rule by 75% of the sum: that happens to give the same answer for two equal circuits, but gives the wrong answer for three.

| Phase | Lighting before diversity | Socket circuit capacity | Socket demand | P7 reserve | Total demand |
|---|---:|---:|---:|---:|---:|
| L1 | 3.444444 A | 3 × 32 A | 32 + 0.5 × 64 = 64 A | 0 A | 67.100 A |
| L2 | 3.959596 A | 2 × 32 A | 32 + 0.5 × 32 = 48 A | 13 A | 64.563636 A |
| L3 | 3.787879 A | 2 × 32 A | 32 + 0.5 × 32 = 48 A | 0 A | 51.409091 A |

This scenario requires more than 63 A; 80 A is the next planning candidate. Without diversity, the largest phase capacity is 99.444444 A. The choice to apply diversity, switchgear thermal duty and actual circuit demand must be carried into the final answer. Old 14-circuit incoming studies are superseded for current planning. Reproduce with `calculations/office_capacity_reservation.py`; results are in `data/office_capacity_phase_results.csv` and `office_capacity_reservation.json`.

## Cable and protection decisions still required

EMSD Table 6(1), printed p56/PDF p57, limits A1 30/32 A rings to 100 m², A2 30/32 A radials to 50 m², and A3 20 A radials to 20 m². Increasing conductor size for temperature/grouping does not remove the served-area limit. The note requires corrected capacity at least 20 A for A1/A3 and 30/32 A for A2. Confirm each served area and draw the actual ring/radial topology before adopting it.

For the source single-core PVC copper Method B table, ambient 40°C with Ca=0.87 and three bunched circuits with Cg=0.70 gives: 4 mm² capacity `32×0.87×0.70=19.488 A`, 6 mm² `41×0.87×0.70=24.969 A`, and 10 mm² `57×0.87×0.70=34.713 A`. Thus 4 mm² fails the 20 A corrected-capacity condition in this grouping; 6 mm² is a capacity candidate for a ring leg, while a 32 A radial requires at least the 10 mm² candidate under these assumptions. This comparison does not verify ring loading, accessory terminals, cable routes, voltage drop or fault protection.

Neutral conductors must be full sized under 6B(6)(c). Table A5(7), printed p278/PDF p279, addresses triple harmonics in four-/five-core cables; do not silently apply its 0.86 factor to a different cable arrangement. Actual harmonic content and the selected incoming cable arrangement remain inputs. Fault level, external loop impedance, CPC size, disconnection, device breaking capacity and installation lengths remain to verify; no final cable passes are claimed.
