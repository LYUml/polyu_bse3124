from pathlib import Path
import json,csv
R=Path(__file__).resolve().parent;D=R/'data'
read=lambda n:json.loads((D/n).read_text())
def put(n,v):(D/n).write_text(json.dumps(v,indent=2),encoding='utf8')
q=read('system_design_results_rev03.json');i=read('system_design_inputs_rev03.json')
e=read('equipment_selection.json')
for x in e:
    if x['id']=='ACB-A;ACB-B':x['selection']='Schneider MTZ2 25H1 4P draw-out + MicroLogic6.0X LSIG';x.update(Ig_A=500,tg_s=.2)
    if x['id']=='MS-O1':
        x.update(selection='Schneider ComPacT NSX100H C10H4TM063 4P4D TM63D',curve='TM-D LI',Icu_kA=70,Ics_kA=70,location='Immediately before F1/O1 CLP meter',source='C10H4TM063 datasheet; DOCA0187EN-04 p235')
        x.pop('Icn_kA',None)
e=[x for x in e if x['id'] not in ['BC','Riser busways','Other O1/O2 tenant controls','O3 tenant controls']]
e.extend([
 dict(id='BC',qty=1,selection=i['coupler']['model'],frame_A=2500,Ir_A=2250,Icu_kA=66,normal_state='OPEN',source=i['coupler']['source']),
 dict(id='Riser busways',qty=2,selection=i['riser']['selection'],nominal_A=2500,corrected_A=1940,source=i['riser']['sources']),
 dict(id='Other O1/O2 tenant controls',qty=19,selection='ComPacT NSX100H 4P4D TM100D',Ir_A=100,Icu_kA=70,basis='COP215 preliminary area demand; selected F1/O1 excluded; detailed outgoing circuits outside scope'),
 dict(id='O3 tenant controls',qty=10,selection='ComPacT NSX160H C16H4TM125 4P4D TM125D',Ir_A=125,Icu_kA=70,basis='COP215 preliminary area demand; detailed outgoing circuits outside scope')])
put('equipment_selection.json',e)
s=read('main_equipment_checks.json');s['normal_operation_PFC_kA']=s['MSB_prospective_upper_kA']+s['motor_contribution_kA'];s['transfer_operation_PFC_kA']=s['MSB_prospective_upper_kA']+2*s['motor_contribution_kA'];s['total_PFC_design_kA']=s['transfer_operation_PFC_kA'];s['riser_busway_corrected_A']=1940;s['bus_coupler_Ir_A']=2250;put('main_equipment_checks.json',s)
c=read('incoming_design_inputs.json');c.update(floor_basis='First-floor Office1; source via declared28m busway route allowance, see system_design_inputs_rev03.json',candidate_curve='TM63D',candidate_breaking_capacity_kA=70,source_protective_device=i['incoming_MCCB']['model'],pre_origin_drop_allowance_V=q['upstream_drop_V'],upstream_drop_basis='Calculated busway envelope, not independently selected allowance',DB_assembly_fault_rating_kA=25)
c['limitations']=[x for x in c['limitations'] if '2.2V' not in x and 'C63' not in x]+['Rev03 system design inputs/results govern upstream fault and voltage conditions; original C63 reference fields are superseded.']
c.pop('reference_C63_Zs_limit_ohm',None);c['reference_TM63D_Zs_limit_ohm']=209/600;put('incoming_design_inputs.json',c)
# Reconcile existing minimum-fault table with the revised upstream hot loop.
with (D/'fault_protection_results.csv').open() as f:r=csv.DictReader(f);fields=r.fieldnames;faults=list(r)
for row in faults:
    z=q['Ze_at_DB_upper_ohm']+float(row['Zloop_70C_bound_ohm']);row['Zs_design_ohm']=round(z,6);row['minimum_earth_fault_A']=round(209/z,3)
    if row['In_A']=='10':row['reference_Zs_limit_ohm']=4.17
    row['scope']='Rev03 system model; RCBO backup per Schneider A-198; declared total-energy conditions retained'
with (D/'fault_protection_results.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(faults)
inc=read('incoming_cable_results.json');inc.update(max_external_loop_Ze_at_meter_ohm=q['Ze_at_MS_O1_upper_ohm'],worst_total_drop_percent=q['max_total_63A_stress_percent'],design_demand_total_drop_percent=q['max_total_design_percent'],protective_device=i['incoming_MCCB']['model'],revision='Rev03; system_design_results_rev03.json governs upstream bounds');put('incoming_cable_results.json',inc)
put('rev03_data_index.json',dict(authoritative_system_inputs='system_design_inputs_rev03.json',authoritative_system_results='system_design_results_rev03.json',voltage_table='voltage_drop_rev03.csv',point_fault_table='point_fault_bounds_rev03.csv',origin='Versioned snapshot of 05_Calculations/data; equipment/circuit IDs unchanged; Rev03 overrides recorded here',superseded_snapshots=['all_circuits_voltage_drop.csv','fault_protection_summary.json','fault_design_conditions.json','final_manifest.json','native_final_gate.json','native_plot_gate.json'],note='Superseded snapshots retained for provenance only. Release gate must replace their status before final handover.'))
print('Rev03 selection and data synchronized; release gates pending.')
