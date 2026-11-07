"""Course-design reservations, not a fan selection or measured cable schedule."""
import csv,json,math
from pathlib import Path
R=Path(__file__).resolve().parents[2];D=R/"04_Design_Outputs/data"
# Explicit proposed dimensions; certified free-area ratio remains to confirm.
vent={"installed_kVA":3000,"louvre_count":2,"width_mm":600,"height_mm":2000,"assumed_free_area_ratio":0.50,
 "source":"COP101 v16 6.3 printed p23 PDF p25; dimensions/free-area ratio are design assumptions"}
vent["gross_area_m2"]=vent["louvre_count"]*vent["width_mm"]*vent["height_mm"]/1e6
vent["effective_area_m2"]=vent["gross_area_m2"]*vent["assumed_free_area_ratio"]
vent["required_effective_area_m2"]=1.12*vent["installed_kVA"]/3000
vent["minimum_certified_free_area_ratio"]=vent["required_effective_area_m2"]/vent["gross_area_m2"]
vent["conditional_area_pass"]=vent["effective_area_m2"]>=vent["required_effective_area_m2"]
vent["limitation"]="Area check conditional on certified free-area ratio >=0.466667; actual losses, fan duty, weather louvres and noise not established"
routes=[dict(id="LV-A-MCT",points=[[15800,20255.584],[15800,21455.584],[10570,21455.584],[10570,23055.584]]),
 dict(id="LV-B-MCT",points=[[19500,20255.584],[19500,22555.584],[13990,22555.584],[13990,23055.584]])]
for r in routes:
 r["plan_length_m"]=sum(math.dist(a,b) for a,b in zip(r["points"],r["points"][1:]))/1000
 r["termination_allowance_m"]=2.0
 r["design_length_m"]=r["plan_length_m"]+r["termination_allowance_m"]
 r["max_length_m"]=20;r["length_pass"]=r["design_length_m"]<=20
 r["trench_width_mm"]=1000;r["trench_depth_mm"]=1100
 r["source"]="COP101 v16 5.5.2.2 printed p16 PDF p18; proposed plan route plus assumed 2m total vertical/termination allowance"
 r["limitation"]="MCT/cable sizing by supplier; coordinate covered trenches, wall fire sealing and structure; not measured installed length"
assert vent["conditional_area_pass"] and all(r["length_pass"] for r in routes)
report=dict(ventilation=vent,LV_interfaces=routes)
(D/"task1_ventilation_interfaces.json").write_text(json.dumps(report,indent=2),encoding="utf8")
print(json.dumps(report))
