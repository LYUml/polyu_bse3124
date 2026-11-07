# Task 3 — Maximum demand, incoming and all outgoing cables

Complete working answer for the current 92 normal luminaires +13 power points +7 passive switches /15 final circuits. All stated passes apply to the adopted course design conditions below; they are not site measurements or certification of installed products. Refresh this answer if loads, control/emergency provisions, routes or assumptions change.

## 1. Design basis and adopted conditions

Office 1 is supplied by a tenant meter/switch position MS-O1 on the same typical floor. Its proposed coordinate is near the source METER label, not a measured cabinet termination. MS-O1 to DB-O1 is a proposed 28.5119 m orthogonal route plus an assumed 3 m total vertical/termination allowance: 31.5119 m. The upstream ground-to-floor distribution is outside this cable segment; its effects are retained as a 2.2 V pre-origin voltage-drop allowance and the following source fault conditions.

Adopt TN-S, external loop impedance Ze=0.20 ohm at MS-O1, maximum prospective fault current 6 kA, 220/380 V supply, cable containment ambient 40°C without thermal-insulation contact, individual apparatus panel ambient <=30°C and FCU ambient <=35°C. Incoming containment is not grouped with outgoing circuits. Four-core incoming cable third-harmonic content is assumed >15% and <=33%; use Ch=0.86 and a full-sized neutral. These are explicit course design assumptions, not asserted site readings. Conditions outside these bounds require redesign.

Each floor box/twin socket is fed through its own 13 A fused connection; FS01 also has a 13 A fused connection. Intended continuous point demand is <=13 A. A fuse is not an instantaneous current limiter: cable overload checks use its conventional fusing current. Actual appliance wattages remain unknown; no appliance watts are invented. P7 is a fixed-equipment connection reserved up to13 A. P6 and P8 both serve the source PANTRY, separately from normal office circuits.

## 2. Maximum demand and phase allocation

Lighting circuit Ib=P/(220×0.90). Outgoing lighting circuits use100% connected load. Incoming diversity follows EMSD2025 Table7(1):90% office lighting; Code6E socket circuits100% largest current plus50% remaining circuit currents, evaluated per phase. Reserve P7 at100% separately. Socket currents derive from designed13 A point limits, not 32 A breaker nameplates.

| Phase | Lighting before diversity / A | Socket demand after diversity / A | P7 reserve / A | Design demand / A | Without diversity / A |
|---|---:|---:|---:|---:|---:|
| L1 | 3.444444 | 45.500 | 0.000 | 48.600000 | 68.444444 |
| L2 | 3.959596 | 39.000 | 0.000 | 42.563636 | 55.959596 |
| L3 | 3.787879 | 32.500 | 13.000 | 48.909091 | 55.787879 |

Maximum design phase demand = **48.909091 A**. Select C63 four-pole overcurrent protection **at MS-O1, before the incoming cable**, then a100 A four-pole isolator at DB-O1. DB busbar design rating100 A exceeds the maximum undiversified phase point-capacity allowance 68.444444 A. Neutral is switched only with the phases; PE is never switched. Older63/80 A nominal-capacity scenarios are historical; this answer uses the designed fused-point topology.

## 3. Incoming cable selection

Select **4-core35 mm² PVC copper L1/L2/L3/N plus separate16 mm² PVC copper CPC**, Method B, mechanically protected in enclosed containment. EMSD TableA6(2) col5 gives25 mm² It=80 A and35 mm² It=99 A. With Ca=0.87, Cg=1 and Ch=0.86:

- 25 mm²: Iz=80×0.87×0.86=59.856 A <63 A, reject.
- 35 mm²: Iz=99×0.87×0.86=74.0718 A;48.909091<=63<=74.0718 A, pass.
- Table11(2)(a),16<S<=35, gives16 mm² same-material CPC minimum. Its energy withstand is also checked below.

Use the three-phase35 mm² voltage-drop impedance value1.10 mV/A/m from TableA6(2) continued. For an unbalanced phase-neutral envelope with neutral current<=63 A, use(2/sqrt3)×1.10=1.270170592 mV/A/m rather than treating a balanced line-line drop as a phase-neutral result. At the full63 A protective rating, incoming drop=1.270170592×63×31.5119/1000=2.521606 V. At design current it is1.957610 V. This is a fundamental-frequency voltage-drop check, not a harmonic-distortion assessment.

## 4. All outgoing circuits

All final circuits use B-curve TypeA30 mA1P+N RCBOs with10 kA breaking capacity and the total-energy performance limits in section6. Each circuit has its own neutral; no neutrals are shared across RCBO load sides. CPCs return to the unswitched PE bar. Power point spurs are4 mm² L/N/CPC, assumed0.5 m each, behind13 A BS1362 fused connections.

| Circuit | Phase | Ib / A | Protective / A | L/N/CPC mm² | Main design route / m | Topology |
|---|---|---:|---:|---:|---:|---|
| LC-A | L1 | 2.030303 | B10 | 2.5/2.5/2.5 | 58.300948 | lighting radial |
| LC-B | L2 | 1.979798 | B10 | 2.5/2.5/2.5 | 62.184084 | lighting radial |
| LC-C | L3 | 2.000000 | B10 | 2.5/2.5/2.5 | 44.999052 | lighting radial |
| LC-D | L3 | 1.222222 | B10 | 2.5/2.5/2.5 | 27.233416 | lighting radial |
| LC-E | L2 | 1.979798 | B10 | 2.5/2.5/2.5 | 34.464052 | lighting radial |
| LC-F | L1 | 1.414141 | B10 | 2.5/2.5/2.5 | 32.709658 | lighting radial |
| LC-G | L3 | 0.565657 | B10 | 2.5/2.5/2.5 | 27.378646 | lighting radial |
| P1 | L1 | 26 | B32 | 6/6/6 | 28.620200 | A1 ring + individually13A fused points |
| P2 | L1 | 26 | B32 | 6/6/6 | 35.520200 | A1 ring + individually13A fused points |
| P3 | L2 | 26 | B32 | 6/6/6 | 45.220200 | A1 ring + individually13A fused points |
| P4 | L2 | 26 | B32 | 6/6/6 | 34.220200 | A1 ring + individually13A fused points |
| P5 | L1 | 13 | B32 | 10/10/10 | 15.607484 | A2 radial + individually13A fused points |
| P6 | L3 | 26 | B32 | 10/10/10 | 13.863968 | A2 radial + individually13A fused points |
| P7 | L3 | 13 | B16 | 4/4/4 | 13.107484 | dedicated fixed radial +13A FCU |
| P8 | L3 | 13 | B32 | 10/10/10 | 15.107484 | A2 radial + individually13A fused points |

Lighting2.5 mm²: Iz=24×0.87×0.54=11.2752 A for seven grouped circuits; all Ib<=10<=Iz. P1–P4 are uniform6 mm² A1 rings with four current-carrying ring legs per containment bank; Iz=41×0.87×0.65=23.1855 A per leg, exceeding Table6(1)'s20 A minimum. Exact ring-network calculations at13 A per point give maximum leg currents14.658–15.203 A, below Iz. Ring overload verification uses the ring provisions and calculated leg currents, not a radial In<=one-leg Iz comparison. The ring conductor, neutral and CPC must all be continuous; no additional unfused points are allowed by this design.

P5/P6/P8 are10 mm²32 A A2 radials: Iz=57×0.87×0.70=34.713 A. P7 is a separate4 mm² B16 radial: Iz=32×0.87=27.84 A. Defined service envelopes for the four A1 rings are93.378/68.771/72.934/97.001 m², each<=100 m²; the three A2 envelopes are46.482/29.544/29.544 m², each<=50 m². These are designed circuit coverage polygons on the source coordinates, not room UFA; overlapping coverage is intentional and must not be added as office area.

## 5. Full voltage-drop check

Outgoing radial drops sum each segment's downstream current; ring drops solve the two-feed uniform-cable network. Include5 m total DB/switch vertical allowance per lighting radial,2 m per power radial,2 m at each power-ring DB end, and0.5 m local point spurs as stated. Add the2.2 V pre-origin allowance and the conservative2.521606 V incoming bound to each outgoing result. Compare the complete phase-neutral result with4%×220=8.8 V.

| Circuit | Outgoing drop / V | Full design bound / V | Full drop / % | Result |
|---|---:|---:|---:|---|
| LC-A | 1.449689 | 6.171295 | 2.805134 | pass under conditions |
| LC-B | 1.237142 | 5.958748 | 2.708522 | pass under conditions |
| LC-C | 0.958766 | 5.680372 | 2.581987 | pass under conditions |
| LC-D | 0.421535 | 5.143141 | 2.337791 | pass under conditions |
| LC-E | 0.797483 | 5.519089 | 2.508677 | pass under conditions |
| LC-F | 0.641700 | 5.363306 | 2.437866 | pass under conditions |
| LC-G | 0.254328 | 4.975934 | 2.261788 | pass under conditions |
| P1 | 1.268756 | 5.990362 | 2.722892 | pass under conditions |
| P2 | 1.674847 | 6.396453 | 2.907479 | pass under conditions |
| P3 | 1.936871 | 6.658477 | 3.026580 | pass under conditions |
| P4 | 1.427920 | 6.149526 | 2.795239 | pass under conditions |
| P5 | 0.964248 | 5.685854 | 2.584479 | pass under conditions |
| P6 | 1.310101 | 6.031707 | 2.741685 | pass under conditions |
| P7 | 1.945870 | 6.667476 | 3.030671 | pass under conditions |
| P8 | 0.935648 | 5.657254 | 2.571479 | pass under conditions |

Worst complete design drop=3.030671%, below4%. The pre-origin allowance is not zero or a measured result; it is a constraint on the upstream supply design.

## 6. Fault, overload and energy verification

At MS-O1, adopted Ze=0.20 ohm. The incoming phase+CPC impedance bound at70°C is0.064129 ohm, giving DB external loop impedance0.264129 ohm. For C63, reference Zs limit0.33 ohm; minimum fault current0.95×220/0.264129=791.28 A exceeds10×63=630 A. This satisfies the reference instantaneous-disconnection condition. Selected C63 apparatus must have10 kA breaking capacity and certified total clearing energy<=1,000,000 A²s over the relevant fault range; this is an explicit design performance specification, not an invented manufacturer datum.

For outgoing circuits, use the official table impedance per metre as a conservative phase+CPC route bound. Ring worst-path equivalent length is at most one quarter of the uniform circumference; add the local spur impedance. Table11(10) reference limits are B10=4.17 ohm, B16=2.61 ohm, B32=1.31 ohm. Evaluate at operating temperature and minimum voltage factor0.95.

| Circuit | Zs design / ohm | Reference limit / ohm | Minimum earth fault / A | Required magnetic threshold / A | Result |
|---|---:|---:|---:|---:|---|
| LC-A | 1.313546 | 4.17 | 159.111 | 50 | pass under conditions |
| LC-B | 1.383443 | 4.17 | 151.072 | 50 | pass under conditions |
| LC-C | 1.074112 | 4.17 | 194.579 | 50 | pass under conditions |
| LC-D | 0.754330 | 4.17 | 277.067 | 50 | pass under conditions |
| LC-E | 0.884482 | 4.17 | 236.296 | 50 | pass under conditions |
| LC-F | 0.852903 | 4.17 | 245.045 | 50 | pass under conditions |
| LC-G | 0.756945 | 4.17 | 276.110 | 50 | pass under conditions |
| P1 | 0.321861 | 1.31 | 649.349 | 160 | pass under conditions |
| P2 | 0.334453 | 1.31 | 624.901 | 160 | pass under conditions |
| P3 | 0.352156 | 1.31 | 593.487 | 160 | pass under conditions |
| P4 | 0.332081 | 1.31 | 629.365 | 160 | pass under conditions |
| P5 | 0.338302 | 1.31 | 617.791 | 160 | pass under conditions |
| P6 | 0.330630 | 1.31 | 632.127 | 160 | pass under conditions |
| P7 | 0.413811 | 2.61 | 505.061 | 80 | pass under conditions |
| P8 | 0.336102 | 1.31 | 621.835 | 160 | pass under conditions |

Use k=115 for PVC copper protective conductors bunched with cables, initial70°C (Table11(2)(c)); require total I²t<=(kS)². The specified B10/B16 overcurrent functions must limit total energy to<=70,000 A²s, B32 to<=90,000 A²s, consistent with the published class3 B-curve10 kA limits. This is a functional requirement for the selected RCBO; a generic RCBO is not assumed certified merely because its curve is B. Individual thresholds are below the respective CPC withstands:2.5 mm²82,656.25;4 mm²211,600;6 mm²476,100;10 mm²1,322,500 A²s. Incoming CPC16 withstand3,385,600 A²s exceeds its specified1,000,000 A²s device limit.

For13 A point fuses, I2=1.9×13=24.7 A. The4 mm² spur Iz=32×0.87×0.70=19.488 A gives1.45Iz=28.2576 A; overload protection passes. Require complete FCU/fuse total clearing energy<=90,000 A²s, below the4 mm² CPC withstand211,600 A²s. The Eaton reference's typical pre-arcing870 A²s is not used as total clearing energy. Its6 kA interrupting reference is compatible with the assumed PFC<=6 kA. Main MCBS/RCBOs are specified10 kA. Full short-circuit selectivity is not claimed from ratings/curves alone; individual RCBO residual protection and separate circuit neutrals limit fault consequences. No PE conductor is switched.

## 7. Sources and reproduction

- EMSD WiringCoP2025: Table7(1), printed65–67/PDF66–68; Table6(1), printed56/PDF57;9B, printed79/PDF80; Table11(2), printed99–100/PDF100–101; Table11(10), printed105/PDF106; A5 factors PDF274–279; A6(1)/(2) PDF282–285. Supplied PDF retained in03_Technical_References.
- [ABB MCB energy-limitation table,9AKK108468A3912, printed130](https://library.e.abb.com/public/4009e91864554accb8c325cb552f18e0/9AKK108468A3912_en_9AKK108468A3912_B01_D_B01%20Electrical%20installation%20solutions%20for%20buildings_part%20B01%20MCBs%20_EN_%20%28PDF%29.pdf). Used for class3 B-curve energy bounds, not an assumed certificate for a particular RCBO.
- [Eaton TDC180 TechnicalData2042, August2024, p2](https://www.eaton.com/content/dam/eaton/products/electronic-components/resources/data-sheet/eaton-tdc180-fuse-data-sheet.pdf). Used for conventional fusing and interruption references, not total clearing energy.
- Common design conditions: data/incoming_design_inputs.json and fault_design_conditions.json. Apparatus limits are adopted course specifications; matching certification is an implementation condition, not a claimed purchased product.
- Reproduce in order: build_lighting_routes.py; build_power_routes.py; office_design_demand.py; incoming_cable_design.py; fault_protection_design.py; write_task3_working_answer.py. Drawing scripts are guarded mutations and must not be rerun blindly. Existing DWG native lengths/areas have been checked against common data.
