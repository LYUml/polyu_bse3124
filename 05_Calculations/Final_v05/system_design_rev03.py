"""Reproducible Rev03 system fault and voltage-drop envelopes.

Input snapshots originate in 05_Calculations/data; Rev03 overrides are versioned
alongside the release. No source drawing, original reference or Rev02 is edited.
"""
from pathlib import Path
import json,csv,math
R=Path(__file__).resolve().parent;D=R.parent/'data'
read=lambda n:json.loads((D/n).read_text(encoding='utf8'))
rows=lambda n:list(csv.DictReader((D/n).open(encoding='utf-8-sig')))
def save(n,d):(D/n).write_text(json.dumps(d,indent=2),encoding='utf8')
I=read('system_design_inputs_rev03.json');S=read('main_equipment_checks.json')
C=read('incoming_design_inputs.json');M=read('office_design_demand.json')
bus=I['riser'];ear=I['earthing'];cold=I['cold_fault_bound'];mccb=I['incoming_MCCB']
length=sum(math.dist(a,b)/1000 for a,b in zip(C['route_lighting_xy_mm'],C['route_lighting_xy_mm'][1:]))+C['vertical_termination_allowance_m']
zbus=bus['hot_positive_sequence_Z_mohm_per_m']*.001*bus['main_to_F1_developed_route_allowance_m']*bus['impedance_factor']
up_drop=S['riser_Ib_A']*(1+bus['fundamental_neutral_current_fraction_of_max_phase'])*zbus+bus['internal_floor_links_and_connections_drop_allowance_V']
pair=2/math.sqrt(3)*C['threephase_35_z_mV_A_m']/1000
feeder_design=pair*length*M['design_peak_A'];feeder_rated=pair*length*63
# Triangle inequality gives a conservative hot loop upper envelope.
bus_loop=(bus['hot_phase_PE_R_mohm_per_m']+bus['phase_PE_X_mohm_per_m'])*.001*bus['main_to_F1_developed_route_allowance_m']*bus['impedance_factor']+bus['internal_connections_earth_loop_allowance_ohm']
zeMS=ear['maximum_main_origin_external_loop_ohm']+bus_loop
feeder_loop=(C['threephase_35_r_mV_A_m']/math.sqrt(3)+C['CPC16_pair_mV_A_m_reference']/2)*length/1000
zeDB=zeMS+feeder_loop
rho=cold['equivalent_resistivity_lower_bound_ohm_mm2_per_m'];rphase=rho*length/35
maxLN=1.1*220/(2*rphase);maxLL=1.1*380/(2*rphase);max3=1.1*380/(math.sqrt(3)*rphase)
maxLE=1.1*220/(rho*length*(1/35+1/16))
# Calculate FCU fault at the actual tap, before the local protected spur.
top=read('power_route_topology.json');pr={r['circuit_id']:r for r in rows('power_route_results.csv')}
fcus=[]
for p in rows('power_points.csv'):
    cid=p['circuit_candidate'];point=[float(p['x_mm']),float(p['y_mm'])]
    if cid in top['ring_solutions']:
        ring=top['ring_solutions'][cid];a=ring['node_plan_chainages_m'][p['device_id']]+2
        total=ring['ring_total_with_two_vertical_ends_m'];equiv=a*(total-a)/total;size=6
    else:
        route=top['routes'][cid];chain=0;found=False
        for a,b in zip(route,route[1:]):
            if math.isclose(math.dist(a,point)+math.dist(point,b),math.dist(a,b),abs_tol=.001):
                chain+=math.dist(a,point)/1000;found=True;break
            chain+=math.dist(a,b)/1000
        assert found,(cid,point)
        equiv=chain+2;size=float(pr[cid]['line_N_CPC_mm2'])
    totalR=2*rphase+2*rho*equiv/size;fault=1.1*220/totalR
    fcus.append(dict(id=p['device_id'],circuit=cid,branch_equivalent_length_m=equiv,cable_mm2=size,maximum_LN_fault_A=fault,fuse_breaking_A=6000,pass_breaking=fault<=6000))
assert all(x['pass_breaking'] for x in fcus)
drop=[]
for name,key in [('lighting_route_results.csv','distributed_drop_V'),('power_route_results.csv','worst_branch_drop_V')]:
    for row in rows(name):
        branch=float(row[key]);total=up_drop+feeder_design+branch;stress=up_drop+feeder_rated+branch
        drop.append(dict(circuit_id=row['circuit_id'],upstream_V=up_drop,feeder_at_design_demand_V=feeder_design,final_V=branch,distribution_percent=(up_drop+feeder_design)/2.2,final_percent=branch/2.2,total_design_percent=total/2.2,total_63A_feeder_stress_percent=stress/2.2,distribution_pass=(up_drop+feeder_design)<=3.3,final_pass=branch<=5.5,total_pass=stress<=8.8))
assert len(drop)==15 and all(r['distribution_pass'] and r['final_pass'] and r['total_pass'] for r in drop)
transfer=2250*380*math.sqrt(3)/1000
out=dict(selected_tenant=I['selected_tenant'],assumptions=I,feeder_length_m=length,riser_corrected_capacity_A=bus['harmonic_15_to_33_percent_capacity_A']*bus['40C_daily_average_factor'],upstream_drop_V=up_drop,feeder_design_drop_V=feeder_design,feeder_63A_drop_V=feeder_rated,distribution_design_percent=(up_drop+feeder_design)/2.2,max_total_design_percent=max(r['total_design_percent'] for r in drop),max_total_63A_stress_percent=max(r['total_63A_feeder_stress_percent'] for r in drop),main_earth_fault_min_A=209/ear['maximum_main_origin_external_loop_ohm'],main_ground_pickup_upper_A=ear['Ig_A']*ear['pickup_upper_tolerance'],main_ground_max_time_s=ear['maximum_breaking_time_s'],upstream_hot_loop_addition_ohm=bus_loop,Ze_at_MS_O1_upper_ohm=zeMS,Ze_at_DB_upper_ohm=zeDB,incoming_minimum_earth_fault_A=209/zeDB,incoming_magnetic_upper_A=mccb['magnetic_pickup_A']*mccb['magnetic_upper_tolerance'],DB_max_LN_fault_A=maxLN,DB_max_LE_fault_A=maxLE,DB_max_LL_fault_A=maxLL,DB_max_3phase_fault_A=max3,DB_required_assembly_fault_kA=25,RCBO_reinforced_B10_kA=40,RCBO_reinforced_B32_kA=25,normal_section_Ib_A=S['section_Ib_A'],single_transformer_transfer_limit_kVA=transfer,minimum_shed_kVA=2*S['section_kVA']-transfer,checks_scope='Calculated under declared design assumptions. No site/utility acceptance or full selectivity claimed. I2t apparatus performance remains an explicit procurement/coordination condition for all fault types.')
assert out['riser_corrected_capacity_A']>=1440 and max3<25000 and maxLN<10000
assert out['incoming_minimum_earth_fault_A']>out['incoming_magnetic_upper_A']
assert out['main_earth_fault_min_A']>out['main_ground_pickup_upper_A'] and out['main_ground_max_time_s']<5
save('system_design_results_rev03.json',out)
for name,data in [('point_fault_bounds_rev03.csv',fcus),('voltage_drop_rev03.csv',drop)]:
    with (D/name).open('w',encoding='utf8',newline='') as f:w=csv.DictWriter(f,fieldnames=data[0]);w.writeheader();w.writerows(data)
print(json.dumps({k:v for k,v in out.items() if k!='assumptions'},indent=2))
