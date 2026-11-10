"""Task 1 arithmetic from explicitly declared course-design assumptions."""
import csv, math
from pathlib import Path
root=Path(__file__).resolve().parents[2]
inputs={r['parameter']:float(r['value']) for r in csv.DictReader(
 (root/'05_Calculations/data/task1_design_inputs.csv').open(encoding='utf8'))}
areas=[inputs[f'office_{i}_ufa'] for i in (1,2,3)]
floors=inputs['typical_floors'];density=inputs['office_density']
q_cooling=inputs['cooling_capacity'];kw_per_tr=inputs['AC_input_per_TR']
pf=inputs['AC_power_factor'];lifts=inputs['lift_count'];public_per_lift=inputs['public_per_lift']
factor=inputs['zoning_factor'];voltage=inputs['line_voltage']
n=inputs['transformer_count'];rating=inputs['transformer_rating']
assert 0 < pf <= 1 and n == 2 and floors == 10
s_office=sum(areas)*floors*density
p_ac=q_cooling/inputs['cooling_per_TR']*kw_per_tr;s_ac=p_ac/pf;s_public=lifts*public_per_lift
base=s_office+s_ac+s_public
rows=[]
for key,value,unit,basis in [
 ('office_UFA_assumed',sum(areas)*floors,'m2','Drawing annotations 6EFD/6F00/6F03 assumed UFA; 10 identical floors'),
 ('office_ADMD',s_office,'kVA','COP215 Rev07 Appendix 2; 0.16 kVA/m2'),
 ('AC_cooling',q_cooling,'kW cooling','Assignment'),
 ('AC_electrical',p_ac,'kW electrical','COP215 Appendix 7 packaged air cooled 1.85 kW/TR; 3.51685 kW cooling/TR'),
 ('AC_apparent',s_ac,'kVA','PF 0.90 design assumption; system boundary to confirm'),
 ('public_services',s_public,'kVA','5 lifts assumed from drawing; COP215 Appendix 2 40 kVA/lift aggregate allowance'),
 ('reservation_envelope_before_zoning',base,'kVA','Office + AC + aggregate public allowance; possible lobby AC overlap retained as conservative reservation, not verified demand'),
 ('reservation_envelope_two_zones',base*factor,'kVA','COP215 3.1.7 for proposed separate supply zones; potential overlap retained'),
 ('baseline_current',base*1000/(math.sqrt(3)*voltage),'A','Balanced three-phase supply assumption in task1_design_inputs.csv'),
 ('zone_current_with_1_1',base*factor/n*1000/(math.sqrt(3)*voltage),'A','Two equal supply zones assumed'),
 ('installed_capacity_candidate',n*rating,'kVA','Proposed transformers; CLP specification and layout not verified')]:
 rows.append(dict(item=key,value=round(value,3),unit=unit,basis=basis,status='course design assumption / preliminary; see Task1 calculation basis'))
p=root/'05_Calculations/data/task1_load_summary.csv'
with p.open('w',encoding='utf8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0],lineterminator='\n');w.writeheader();w.writerows(rows)
for r in rows:print(r['item'],r['value'],r['unit'])

# X cannot exceed either of the two allowances that contain the duplicated share.
# This bound does not assert that all public-services load is air conditioning.
checks=[]
for label,x in [('conservative_no_deduction',0),('maximum_possible_deduction',min(s_ac,s_public))]:
 demand=factor*(base-x);per_zone=demand/n
 checks.append(dict(scenario=label,overlap_deduction_kVA=round(x,3),
  assessed_load_kVA=round(demand,3),per_zone_kVA=round(per_zone,3),
  per_zone_current_A=round(per_zone*1000/(math.sqrt(3)*voltage),3),
  installed_capacity_kVA=n*rating,capacity_margin_kVA=round(n*rating-demand,3),
  normal_capacity_pass=per_zone<=rating,
  full_load_N_minus_1_pass=demand<=(n-1)*rating,
  limitation='Course load model only; equal allocation assumed; equipment and site coordination pending'))
with (root/'05_Calculations/data/task1_capacity_bounds.csv').open('w',encoding='utf8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=checks[0],lineterminator='\n');w.writeheader();w.writerows(checks)
assert all(r['normal_capacity_pass'] for r in checks)
assert not any(r['full_load_N_minus_1_pass'] for r in checks)
print('Capacity bounds:',checks)
