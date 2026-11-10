# Final validation and design conditions

Final answer: BSE3124_Final.pdf, 18 pages. Native drawing: BSE3124_Final.dwg. Order: cover; Task 1 (pp.2-5); Task 2 (pp.6-14); Task 3 (pp.15-18).

Lighting: 92 panels, 2256 W (60 x 22 W, 28 x 28 W, 4 x 38 W). The four south-east panels use the manufacturer HIGH LDT profile at 4685.55 lm each. At the adopted 1.9 m luminaire-to-workplane height and MF 0.80, mean maintained direct illuminances are 592.9/546.3/588.5/662.6 lx. At 2.2 m they are 573.0/505.8/545.0/589.2 lx. The south-east room retains a 17.8% margin above the 500 lx mean target at 2.2 m. Direct-light perimeter minimum/mean ratios are retained; mean results are distinct from task-area uniformity and glare.

LC-G: four 38 W panels, 152 W, 0.767677 A, B10 RCBO, 2.5 mm2 L/N/CPC. Its route remains 27.378646 m including allowances. Distributed outgoing drop is 0.345159 V. Maximum office demand is 49.090909 A; retain C63, 4C35 mm2 plus CPC16 and 100 A DB isolation. Corrected feeder capacity is 74.0718 A; worst full-path drop remains 3.030671%. All 15 outgoing protection checks pass under the adopted installation and source conditions.

AutoCAD 2027 Core Console reopened the saved final DWG: 962 registered entities found, 92 lamp labels, 15 routes, two incoming routes and 15 DB schedule rows checked. Updated drawing notes were verified against final_text_sync.json. The room-detail paper layout was rebuilt with a valid overall paper viewport and enabled 1:75 model viewport; its geometry and notes were retained. All six saved layouts were replotted successfully after reopening, including the repaired room detail. See native_final_gate.json, native_plot_gate.json and room_layout_repair.json.

Final PDF pages were rendered and visually reviewed. XeLaTeX reports no overfull boxes or undefined references. Repeated task titles, duplicate demand calculations and operational instructions were removed. Template cover lettering uses consistent Times New Roman; continuation pages reuse the teacher's frame and full task heading plus (continued).

Design assumptions retained: adopted UFA and equipment envelopes; MF0.80 with cleaning/replacement; TN-S source Ze0.20 ohm and PFC <=6 kA; cable grouping and temperature factors; route allowances and apparatus energy/inrush requirements. Ring overload checks use EMSD 6C/6E/Table 6(1) A1 conditions. Source documents remain unchanged. Final file hashes are in data/final_manifest.json.
