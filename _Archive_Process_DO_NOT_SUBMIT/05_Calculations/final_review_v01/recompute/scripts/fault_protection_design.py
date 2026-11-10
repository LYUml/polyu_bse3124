"""Course protection verification under explicit source and device-performance conditions."""
import csv,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/"data"
F=json.loads((D/"fault_design_conditions.json").read_text());inc=json.loads((D/"incoming_cable_results.json").read_text());pi=json.loads((D/"power_route_design_inputs.json").read_text());li=json.loads((D/"lighting_route_design_inputs.json").read_text())
ZeDB=F["Ze_at_MS_assumed_ohm"]+inc["Rphase_plus_CPC_70C_ohm"]
schedule={r['circuit_id']:r for r in csv.DictReader((D/'circuits.csv').open())}
results=[]
for r in csv.DictReader((D/"lighting_route_results.csv").open()):
 Zloop=li["table_drop_mV_A_m"]*float(r["design_route_m"])/1000
 results.append(dict(circuit_id=r["circuit_id"],curve="B",In_A=10,CPC_mm2=2.5,Zloop_70C_bound_ohm=Zloop,Iz_A=float(r["Iz_A"]),I2_A=14.5,required_max_I2t=F["required_B10_B16_max_total_I2t_A2s"],reference_Zs_limit_ohm=4.17))
for r in csv.DictReader((D/"power_route_results.csv").open()):
 cid=r["circuit_id"];ring=cid in ["P1","P2","P3","P4"];fixed=cid=="P7"
 if ring:
  # Uniform phase and CPC rings: worst parallel path at half circumference.
  Zloop=pi["ring_mV_A_m"]*float(r["main_with_vertical_m"])/4000+pi["spur_mV_A_m"]*pi["spur_assumed_length_m"]/1000
  # A1 uses the standard ring arrangement, not a fictitious ring-leg device I2.
  I2=None
 else:
  mv=pi["fixed_mV_A_m"] if fixed else pi["radial_mV_A_m"]
  Zloop=mv*float(r["main_with_vertical_m"])/1000+pi["spur_mV_A_m"]*pi["spur_assumed_length_m"]/1000
  I2=1.45*float(r["protective_A"])
 results.append(dict(circuit_id=cid,curve="B",In_A=int(r["protective_A"]),CPC_mm2=float(r["line_N_CPC_mm2"]),Zloop_70C_bound_ohm=Zloop,Iz_A=float(r["corrected_Iz_A"]),I2_A=I2,required_max_I2t=F["required_B10_B16_max_total_I2t_A2s"] if fixed else F["required_B32_max_total_I2t_A2s"],reference_Zs_limit_ohm=4.17 if fixed else 1.31))
for r in results:
 r["Zs_design_ohm"]=round(ZeDB+r["Zloop_70C_bound_ohm"],6)
 r["minimum_earth_fault_A"]=round(.95*220/r["Zs_design_ohm"],3)
 r["required_instantaneous_A"]=5*r["In_A"]
 r["disconnection_pass"]=r["Zs_design_ohm"]<=r["reference_Zs_limit_ohm"] and r["minimum_earth_fault_A"]>=r["required_instantaneous_A"]
 r["CPC_withstand_A2s"]=(115*r["CPC_mm2"])**2
 r["adiabatic_pass"]=r["required_max_I2t"]<=r["CPC_withstand_A2s"]
 if r["I2_A"] is None:
  pr=next(p for p in csv.DictReader((D/"power_route_results.csv").open()) if p["circuit_id"]==r["circuit_id"])
  r["overload_pass"]=(r["In_A"]==32 and r["CPC_mm2"]>=2.5 and r["Iz_A"]>=20 and float(pr["served_envelope_m2"])<=100 and float(pr["max_ring_leg_A"])<=r["Iz_A"] and pi['point_FCU_A']==13 and len(schedule[r['circuit_id']]['device_ids'].split(';'))==2)
  r["overload_basis"]="EMSD2025 6C,6E and Table6(1) A1/Note1(i): intact uniform L/N/CPC rings, 32A protection, corrected Iz>=20A, area<=100m2; two individually13A fused taps per ring. Nominal network load split is supplementary, not protective-device I2. No unfused extra taps permitted."
 else:
  r["overload_pass"]=r["I2_A"]<=1.45*r["Iz_A"]
  r["overload_basis"]="Conventional protective-device I2<=1.45Iz; capacity Ib<=In<=Iz checked in route calculations"
 r["breaking_capacity_pass"]=F["MCB_RCBO_Icn_A"]>=F["PFC_max_assumed_A"]
 r["scope"]="Pass under adopted source/device-performance conditions; not a site test or arbitrary product certification"
I2f=F["FCU13_conventional_fusing_factor"]*13
Izspur=pi["spur_It_A"]*pi["Ca"]*pi["spur_Cg"]
spur=dict(In_A=13,Iz_A=Izspur,I2_A=I2f,I2_limit_A=1.45*Izspur,overload_pass=I2f<=1.45*Izspur,CPC_mm2=4,CPC_withstand_A2s=(115*4)**2,required_FCU_total_I2t_A2s=F["required_FCU13_max_total_I2t_A2s"],adiabatic_pass=F["required_FCU13_max_total_I2t_A2s"]<=(115*4)**2,breaking_capacity_pass=F["FCU_fuse_breaking_A"]>=F["PFC_max_assumed_A"],note="Eaton reference gives typical pre-arcing energy only; total FCU assembly energy bound remains explicit design specification")
incoming=dict(Zs_design_ohm=ZeDB,Zs_limit_ohm=.33,minimum_earth_fault_A=.95*220/ZeDB,instantaneous_threshold_A=10*63,CPC_mm2=16,CPC_withstand_A2s=(115*16)**2,required_C63_total_I2t_A2s=F["required_incoming_C63_max_total_I2t_A2s"],disconnection_pass=ZeDB<=.33,adiabatic_pass=F["required_incoming_C63_max_total_I2t_A2s"]<=(115*16)**2,breaking_capacity_pass=F["MCB_RCBO_Icn_A"]>=F["PFC_max_assumed_A"])
assert len(results)==15 and all(all(r[k] for k in ["disconnection_pass","adiabatic_pass","overload_pass","breaking_capacity_pass"]) for r in results)
assert all(spur[k] for k in ["overload_pass","adiabatic_pass","breaking_capacity_pass"]) and all(incoming[k] for k in ["disconnection_pass","adiabatic_pass","breaking_capacity_pass"])
with (D/"fault_protection_results.csv").open("w",newline="",encoding="utf8") as f:w=csv.DictWriter(f,fieldnames=results[0],lineterminator="\n");w.writeheader();w.writerows(results)
summary=dict(conditions=F,source_Ze_assumed_ohm=F["Ze_at_MS_assumed_ohm"],Ze_DB_design_ohm=ZeDB,outgoing_circuits_checked=15,incoming=incoming,point_spurs=spur,all_design_checks_pass_under_conditions=True,selectivity="Full short-circuit discrimination is not claimed; individual RCBO residual protection and separation reduce fault consequences. Curve/rating alone do not prove all-current selectivity.")
(D/"fault_protection_summary.json").write_text(json.dumps(summary,indent=2));print(json.dumps(dict(Ze_DB=ZeDB,checked=15,incoming=incoming,point_spurs=spur)))
