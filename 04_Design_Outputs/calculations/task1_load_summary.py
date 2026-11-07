"""Task 1 arithmetic from explicitly declared course-design assumptions."""
import csv, math
from pathlib import Path
root=Path(__file__).resolve().parents[2]
areas=[309,309,410];floors=10;density=.16
q_cooling=1000;kw_per_tr=1.85;pf=.90;lifts=5;public_per_lift=40
s_office=sum(areas)*floors*density
p_ac=q_cooling/3.51685*kw_per_tr;s_ac=p_ac/pf;s_public=lifts*public_per_lift
base=s_office+s_ac+s_public
rows=[]
for key,value,unit,basis in [
 ('office_UFA_assumed',sum(areas)*floors,'m2','Drawing annotations 6EFD/6F00/6F03 assumed UFA; 10 identical floors'),
 ('office_ADMD',s_office,'kVA','COP215 Rev07 Appendix 2; 0.16 kVA/m2'),
 ('AC_cooling',q_cooling,'kW cooling','Assignment'),
 ('AC_electrical',p_ac,'kW electrical','COP215 Appendix 7 packaged air cooled 1.85 kW/TR; 3.51685 kW cooling/TR'),
 ('AC_apparent',s_ac,'kVA','PF 0.90 design assumption; system boundary to confirm'),
 ('public_services',s_public,'kVA','5 lifts assumed from drawing; COP215 Appendix 2 40 kVA/lift aggregate allowance'),
 ('baseline',base,'kVA','Office + AC + public; no repeated public-services addition'),
 ('multi_zone_assessment',base*1.1,'kVA','COP215 3.1.7 only if supplied by multiple transformers for separate zones'),
 ('baseline_current',base*1000/(math.sqrt(3)*380),'A','Balanced 380 V assumed'),
 ('zone_current_with_1_1',base*1.1/2*1000/(math.sqrt(3)*380),'A','Two equal supply zones assumed'),
 ('installed_capacity_candidate',3000,'kVA','2 x 1500 kVA candidate; CLP specification and layout not verified')]:
 rows.append(dict(item=key,value=round(value,3),unit=unit,basis=basis,status='course design assumption / preliminary; see Task1 calculation basis'))
p=root/'04_Design_Outputs/data/task1_load_summary.csv'
with p.open('w',encoding='utf8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0],lineterminator='\n');w.writeheader();w.writerows(rows)
for r in rows:print(r['item'],r['value'],r['unit'])
