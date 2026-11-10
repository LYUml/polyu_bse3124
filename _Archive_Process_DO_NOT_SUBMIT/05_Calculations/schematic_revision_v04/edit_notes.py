"""Editorial changes only: retain all design inputs, formulae and circuit tables."""
from pathlib import Path
import re,json
R=Path(__file__).resolve().parent;T=R/'source';log=[]
def edit(name,pairs):
    p=T/name;s=p.read_text();before=s
    for old,new in pairs:
        assert old in s,(name,old)
        s=s.replace(old,new)
    p.write_text(s)
    log.append(dict(file=name,before_words=len(before.split()),after_words=len(s.split())))

edit('task1.tex',[
 ('The proposal starts with','The design uses'),
 ('However, full-load N--1 is not provided, so load shedding is required if one unit is lost.','Full-load N--1 is not provided.'),
 ('The schematic identifies this exception. ',''),
 ('The utility supply equipment is specified as two CLP 1500 kVA distribution-transformer units and an HV incomer with two transformer-protection panels. COP101 v16\'s responsibility schedule, items 7.1--7.8, assigns the transformer, switchgear and utility metering to CLP. Consequently, the drawings identify their functions and installation envelopes; they do not falsely nominate a commercially selected transformer as CLP-approved. The retained 2200 by 1800 mm transformer and 3000 by 1000 mm HV installation dimensions are declared design assumptions.',
  'CLP supplies the transformers, HV switchgear and utility metering under COP101 v16, responsibility schedule 7.1--7.8. The equipment outlines and proposed access dimensions are design allowances, subject to supplier and site coordination.'),
 ('The nominal 2500 A busway rating must not be confused with the riser protective-device frame. ',''),
 ('Transformer impedance, motor multiplier and transfer operation are assumptions, not utility measurements. Full short-circuit discrimination is not claimed.','The impedance and motor-contribution assumptions define this fault-duty bound.'),
 ('These are stated design coefficients, not laboratory louvre data; the installed louvre/duct combination must maintain this duty.','The installed louvre/duct combination must maintain this duty.'),
 (' The plan shows high-level ducts above the delivery openings.','')
])
edit('task2.tex',[
 ('The lighting proposal starts with','The lighting design uses'),
 (' Their nominal fluxes are 2843.45, 3555.30 and 4685.55 lm respectively.',''),
 ('With this arrangement, the connected lighting density is','The connected lighting density is'),
 ('Similarly, ','') ,
 (' Power settings follow the common device schedule. Every luminaire and control has one circuit assignment.',''),
 ('Accordingly, the demand calculation uses','The demand calculation uses'),
 ('Meanwhile, building central AC','Building central AC'),
 ('In comparison, P5/P6/P8','P5/P6/P8'),
 ('In terms of coverage, the defined service envelopes satisfy the A1 maximum of 100 m$^2$ and the A2 maximum of 50 m$^2$. Coverage is assessed by service envelope, allowing overlap between circuits. Ring L/N/CPC return to their own circuit terminals. Main 6/10 mm$^2$ cables terminate in accessible junction/FCU assemblies rated for those conductor sizes. At each point, the local connections use 4 mm$^2$ L/N/CPC, with an assumed length of 0.5 m per point.',
  'Circuit service envelopes meet the A1 limit of 100 m$^2$ and A2 limit of 50 m$^2$. Envelopes may overlap; they are not summed as office area. Connection and containment details follow.'),
 ('As shown in the complete schematic, the arrangement includes','The DB schematic shows'),
 ('Every load neutral passes through its own RCBO;  none are shared downstream. Meanwhile, PE bypasses all switches. Additionally, the circuits and phases are to be labelled, and the arrangement must allow each final circuit to be isolated without interrupting the others.',
  'Each circuit has a dedicated RCBO neutral and labelled phase; PE is unswitched.'),
 ('Device selection must ensure that the proposed B-curve final protection is compatible with driver inrush and the breaking-capacity/energy limits established in Task 3. Individual RCBOs limit the effect of a residual-current fault to its own circuit; however, full short-circuit selectivity requires manufacturer coordination data.',
  'Check driver inrush and protective-device coordination against the Task 3 requirements.')
])
edit('lighting_basis.tex',[
 ('Meanwhile, the maintenance factor','The maintenance factor'),
 ('When interpreting these results, the minimum/mean ratios include perimeter cells. Overall, the assessment covers mean direct illuminance; a detailed task-area check would also account for furniture, reflections and glare.',
  'Min/mean ratios include perimeter cells. These direct-light results do not establish task-area uniformity or glare performance.')
])
edit('task3.tex',[
 ('The upstream drop is calculated from the stated busway model below; the previous arbitrary 2.2 V allowance is superseded.','The upstream drop is calculated from the busway model below.'),
 ('However, the radial criterion $I_n\\le I_z$ must not be applied to just one ring leg. Continuity and fused-point restrictions are essential.',r'Ring overload protection follows the A1 conditions below.'),
 ('Meanwhile, the 10 mm','The 10 mm'),
 ('Additionally, each local point spur','Each local point spur'),
 (' (design allowance, not surveyed height)',' (design allowance)'),
 ('; this is not a measured value',' (design acceptance condition)'),
 (' This replaces the former C63 reference-table test.',''),
 ('This does not require treating the fuse\'s typical pre-arcing value as total clearing energy. ',''),
 ('On this basis, the adopted 6 mm$^2$ rings meet these conditions. Exactly two individually 13 A fused connections are allowed per ring; no additional unfused taps are permitted. Here, the leg-current calculation checks load distribution; the A1 standard arrangement governs ring overload protection.',
  'The 6 mm$^2$ rings meet these conditions, with exactly two individually 13 A fused taps per ring.'),
 (' However, its typical pre-arcing 870 A$^2$s is \\emph{not} total clearing energy.',''),
 ('Finally, the design assumes','The design assumes'),
 ('Spur short-circuit thermal protection is checked using the upstream RCBO bound above.',''),
 ('The main and rising-supply ACBs require the specified MicroLogic control units; a bare breaker frame is not a complete protective device. The DB retains the specified 100 A four-pole isolator and eight-way TPN arrangement, with 15 installed outgoing devices. Unused positions have blanking plates and no connected loads. The apparatus schedule is an electrical design selection, not evidence of utility approval or installed equipment.',
  'ACBs include the listed MicroLogic units. DB-O1 has a 100 A four-pole isolator, eight-way TPN chassis and 15 outgoing devices; unused positions are blanked.'),
 (' Product coordination must satisfy the declared source and total-energy bounds; full discrimination is not inferred from model numbers.','')
])
edit('system_protection_rev03.tex',[
 ('For a deliberately conservative cold-copper bound, assume','For the cold-copper fault bound, assume'),
 (' This is a material/temperature envelope, not a measured cable resistance.',''),
 ('; its 100 A continuous rating alone is insufficient',''),
 (' The point-by-point calculation is retained with the common circuit data.',''),
 ('; no fictitious external protection CT ratio is assigned',''),
 (' The course COP215 Rev07 load basis remains unchanged; these equipment references do not replace it.',''),
 (' Thus no intentional short-time delay is added to seek discrimination.',''),
 (' Full discrimination is not claimed.',''),
 ('The 309/309/410 m$^2$ values are retained as the supplied-plan annotation-based UFA assumptions used by COP215; they are not independently surveyed net areas. Lighting calculation rectangles and circuit service envelopes have different purposes and must not be substituted for UFA. Any kitchen or common-area exclusion must follow the course COP215 definition when a verified boundary is available. Keeping this explicit assumption is within the assignment\'s requested assumptions; the load result must not be described as independently measured UFA.',
  'COP215 loading uses assumed UFA values of 309/309/410 m$^2$, based on the plan annotations. Verify boundaries and applicable kitchen/common-area exclusions before replacing these assumptions; lighting and circuit service envelopes are not UFA measurements.')
])
edit('main.tex',[
 ('Additionally, the calculation assumes','The calculation assumes'),
 ('Additionally, the pantry circuits','The pantry circuits'),
 ('Accordingly, the selected apparatus must meet the specified 10\\,kA breaking capacity and total-energy/inrush limits.','RCBO ratings and backup protection are checked in Task 3.'),
 ('Additionally, the chassis/module capacity for 1P+N devices must be confirmed.','Confirm chassis capacity for the selected 1P+N devices.'),
 ('Accordingly, ','') if 'Accordingly, ' in (T/'main.tex').read_text().replace('Accordingly, the selected apparatus must meet the specified 10\\,kA breaking capacity and total-energy/inrush limits.','') else ('The continuation gives maximum-fault and manufacturer backup checks.','Maximum-fault and backup checks follow.')
])
# Consolidate connection details rather than repeating them in both adjacent sections.
p=T/'installation_notes.tex';before=p.read_text();p.write_text(r'''% !TeX root = main.tex
\subsection*{FCU and containment details}
Each FB01--FB09 floorbox and SO01--SO03 twin socket shares one upstream 13 A FCU. FS01 uses a 10 A DP FCU and accessible earthed socket for WH01; retain the appliance cord and plug. Use accessible terminals rated for the 6/10 mm$^2$ main conductors. Place each FCU before its 4 mm$^2$, 0.5 m local spur; switch N with L and keep PE continuous. The demand basis is 13 A per socket assembly and 6.364 A for WH01.

Keep separate Method B containment banks: LC-A--G (seven circuits, $C_g=0.54$); P1/P2 and P3/P4 (four ring legs per bank, 0.65); P5/P6/P8 (three radials, 0.70); P7 alone (1.00); incoming feeder alone (1.00). Overlapping plan routes indicate corridors, not shared enclosures.

Under EMSD A5(3), Note 2, provide horizontal cable clearance between banks exceeding twice the largest adjacent cable diameter. Space enclosures to maintain that clearance; partitions alone do not provide thermal separation. Keep each circuit's L/N/CPC together and clear of thermal insulation. Recalculate grouping factors if this arrangement changes.
''');log.append(dict(file=p.name,before_words=len(before.split()),after_words=len(p.read_text().split())))
(R/'editorial_changes.json').write_text(json.dumps(log,indent=2))
print(json.dumps(log))
