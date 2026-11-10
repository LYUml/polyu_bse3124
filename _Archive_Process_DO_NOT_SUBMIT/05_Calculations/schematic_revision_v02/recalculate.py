from pathlib import Path
import csv,json,subprocess,sys,math
P=Path(__file__).parent; D=P/'data'; S=P/'scripts';S.mkdir(exist_ok=True)
def table(name):return list(csv.DictReader((D/name).open(encoding='utf8')))
def write(name,rows):
    with (D/name).open('w',newline='',encoding='utf8') as f:
        w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
ib=1400/220
rows=table('circuits.csv')
for r in rows:
    r['source_or_assumption']=r['source_or_assumption'].replace('COURSE DESIGN','DESIGN')
    if r['circuit_id']=='P7':
        r.update(connected_load_W='1400',Ib_A=str(ib),MCB_A='10',demand_basis='100% SHC 10 GB Eltron 235232; 1.4kW at 220V, PF1; use P/V conservatively versus rounded manufacturer 6.2A',source_or_assumption='SHC10 GB manual section15.7: 10A protection; dedicated FS01 10A DP FCU with accessible earthed connection; 4mm2 radial retained')
write('circuits.csv',rows)
rows=table('devices.csv')
for r in rows:
    if r['device_id']=='FS01':
        r['type']='WH01 heater connection via DP FCU, 10A';r['rated_power_W']='1400' if 'rated_power_W' in r else r.get('rated_power_W','')
        # Use the existing common-data schema.
        for k in list(r):
            if k in ['power_W','load_W']:r[k]='1400'
            if k in ['power_factor','pf']:r[k]='1'
            if 'source' in k:r[k]='WH01: STIEBEL ELTRON SHC10 GB Eltron 235232; 1.4kW/220V, 10L, 280W x270D x430H mm; manufacturer manual15.7; dedicated B10 / DP FCU10; 100% demand'
        if 'rated_power_W' not in rows[0]:r.pop('rated_power_W',None)
write('devices.csv',rows)
rows=table('power_points.csv')
for r in rows:
    if r['device_id']=='FS01':
        for k in r:
            if k=='type':r[k]='10A DP FCU / WH01 SHC10 GB heater connection'
            if 'assumption' in k or 'source' in k or k=='status':r[k]='Selected WH01 1.4kW/220V; fixed connection assembly, not spare load'
write('power_points.csv',rows)
inp=json.loads((D/'power_route_design_inputs.json').read_text());inp.update(fixed_protection_A=10,fixed_design_current_A=ib,fixed_FCU_A=10)
(D/'power_route_design_inputs.json').write_text(json.dumps(inp,indent=2))
for name in ['build_power_routes.py','office_design_demand.py','incoming_cable_design.py','fault_protection_design.py']:
    s=(P.parent/'scripts'/name).read_text()
    s=s.replace('R=Path(__file__).resolve().parents[2];D=R/"05_Calculations/data"','R=Path(__file__).resolve().parents[1];D=R/"data"')
    if name=='build_power_routes.py':
        s=s.replace('ib=len(members)*I["point_FCU_A"]','ib=I["fixed_design_current_A"] if cid=="P7" else len(members)*I["point_FCU_A"]')
        s=s.replace('I["spur_mV_A_m"]*I["point_FCU_A"]*I["spur_assumed_length_m"]','I["spur_mV_A_m"]*(ib if cid=="P7" else I["point_FCU_A"])*I["spur_assumed_length_m"]')
        s=s.replace('In=16 if fixed else 32','In=I["fixed_protection_A"] if fixed else 32')
        s=s.replace('remaining-=I["point_FCU_A"]','remaining-=(ib if fixed else I["point_FCU_A"])').replace('assert remaining==0','assert abs(remaining)<1e-8')
        s=s.replace('dedicated fixed radial +13A FCU','SHC10 GB heater radial +10A DP FCU')
        s=s.replace('all point currents are fuse-capacity bounds, not appliance ratings; fault/upstream/control/terminal reviews pending','socket points use FCU bounds; P7 uses selected heater nameplate power; see completed protection checks')
    if name=='office_design_demand.py':
        s=s.replace('fixed_reserved_A','fixed_equipment_A').replace('fixed P7 reserved13A without diversity','fixed WH01 P7 at1400/220A without diversity').replace('P7 fixed reserve13A. No actual appliance watts invented.','P7 SHC10 GB heater 1400W at220V.').replace('P7 actual equipment identity unknown; design capacity limited to13A','P7: SHC10 GB Eltron235232; B10 and10A DP FCU')
    if name=='fault_protection_design.py':
        s=s.replace('reference_Zs_limit_ohm=2.61 if fixed else 1.31','reference_Zs_limit_ohm=4.17 if fixed else 1.31')
    (S/name).write_text(s)
    result=subprocess.run([sys.executable,str(S/name)],capture_output=True,text=True)
    (S/(name+'.log')).write_text(result.stdout+result.stderr)
    assert result.returncode==0,result.stderr
# Synchronize the DB schedule inputs used by the native verifier.
b=json.loads((D/'db_submission_sheet_map.json').read_text())
for r in b['circuit_rows']:
    if r['circuit_id']=='P7':r['protective_A']='10'
(D/'db_submission_sheet_map.json').write_text(json.dumps(b,indent=2))
md=json.loads((D/'office_design_demand.json').read_text());inc=json.loads((D/'incoming_cable_results.json').read_text())
vent={'source':'COP101 v16 clauses6.3,6.4,6.6, printedp23','heat_kW_per_TX_reference':15,'units':2,'overload_margin_assumed':1.25,'design_heat_kW':37.5,'fan_type':'630mm /30deg /700rpm','fan_m3h_each':4500,'fan_Pa_each':70,'air_density_assumed_kgm3':1.2,'air_cp_JkgK':1005,'air_rise_K':37500/(1.2*1005*2*4500/3600),'duct_mm':[900,750],'duct_area_m2':.675,'duct_route_design_m_each':1.4,'free_louvre_area_m2':1.2,'free_inlet_velocity_ms':2.5/1.2,'design_loss_coefficients':{'inlet':2.0,'outlet':1.0,'bend_and_transition':1.0,'friction_factor':.025},'pressure_note':'Loss coefficients are declared design assumptions; factory louvre/fan curves and actual duct fittings must satisfy this duty.'}
vf=1.25/.675;vi=2.5/1.2;dh=2*.9*.75/(.9+.75)
vent['estimated_Pa']=2*.5*1.2*vi**2+2*.5*1.2*vf**2+.025*1.4/dh*.5*1.2*vf**2
vent['available_Pa']=70;assert vent['estimated_Pa']<70
(D/'ventilation_selection.json').write_text(json.dumps(vent,indent=2))
main={'source':'Task1 COP215 load; manufacturer selected apparatus listed in equipment schedule','section_kVA':1336.108,'section_Ib_A':1336.108e3/(math.sqrt(3)*380),'ACB_frame_A':2500,'ACB_longtime_Ir_A':2250,'TX_full_load_A_at380':1500e3/(math.sqrt(3)*380),'assumed_TX_uk_percent':6,'minimum_uk_with_minus10percent':5.4,'voltage_factor':1.1,'MSB_prospective_upper_kA':1.1*1500/(math.sqrt(3)*.380*.054)/1000,'ACB_Icu_kA':66,'floor_kVA':164.48*1.1,'floor_Ib_A':164.48*1.1*1000/(math.sqrt(3)*380),'floor_MCCB_frame_A':400,'floor_longtime_setting_A':320,'plant_kVA':392.244*1.1,'plant_Ib_A':392.244*1.1*1000/(math.sqrt(3)*380),'plant_MCCB_frame_A':800,'plant_longtime_setting_A':720,'MCCB_Icu_kA':70,'scope':'Assignment conceptual main distribution selection. Transformer uk and bus PFC are design assumptions, not utility-issued data; outgoing building feeder cable design beyond selected tenant is not claimed.'}
assert main['section_Ib_A']<2250<main['TX_full_load_A_at380']<2500
assert main['floor_Ib_A']<320<400 and main['plant_Ib_A']<720<800 and main['MSB_prospective_upper_kA']<70
main.update(riser_Ib_A=main['floor_Ib_A']*5,riser_ACB_A=1600,riser_Ir_A=1440,motor_current_multiplier_assumed=8,motor_contribution_kA=8*main['plant_Ib_A']/1000)
main['total_PFC_design_kA']=main['MSB_prospective_upper_kA']+main['motor_contribution_kA']
assert main['total_PFC_design_kA']<66 and main['MCCB_Icu_kA']==70
(D/'main_equipment_checks.json').write_text(json.dumps(main,indent=2))
print(json.dumps({'demand':md['phases'],'peak':md['design_peak_A'],'worst_VD_percent':inc['worst_total_drop_percent'],'ventilation':vent,'main':main},indent=2))
