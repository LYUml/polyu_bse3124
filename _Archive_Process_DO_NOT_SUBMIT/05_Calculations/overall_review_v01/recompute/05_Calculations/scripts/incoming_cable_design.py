"""Incoming capacity and unbalanced phase-neutral drop envelope; source constraints explicit."""
import csv,json,math
from pathlib import Path
R=Path(__file__).resolve().parents[2];D=R/"05_Calculations/data"
I=json.loads((D/"incoming_design_inputs.json").read_text());M=json.loads((D/"office_design_demand.json").read_text())
points=I["route_lighting_xy_mm"]
assert points[0]==I["source_lighting_xy_mm"] and points[-1]==I["DB_lighting_xy_mm"]
plan=0
for a,b in zip(points,points[1:]):
 assert a[0]==b[0] or a[1]==b[1]
 plan+=math.dist(a,b)/1000
length=plan+I["vertical_termination_allowance_m"]
factor=I["Ca"]*I["Cg"]*I["Ch"]
Iz25=I["It_25_A"]*factor;Iz=I["It_35_A"]*factor
# Convert three-phase table impedance to a phase+neutral bound; assumes I_N<=In.
pair_mV=2/math.sqrt(3)*I["threephase_35_z_mV_A_m"]
feeder_drop_at_In=pair_mV*I["candidate_In_A"]*length/1000
feeder_drop_at_Ib=pair_mV*M["design_peak_A"]*length/1000
# Upper resistance approximation: same route for phase35 and CPC16.
Rphase=I["threephase_35_r_mV_A_m"]/math.sqrt(3)
Rcpc=I["CPC16_pair_mV_A_m_reference"]/2
Rloop=(Rphase+Rcpc)*length/1000
Zsource_max=I["reference_C63_Zs_limit_ohm"]-Rloop
branch=[]
for name,drop_key in [("lighting_route_results.csv","distributed_drop_V"),("power_route_results.csv","worst_branch_drop_V")]:
 for r in csv.DictReader((D/name).open()):
  outgoing=float(r[drop_key]);total=I["pre_origin_drop_allowance_V"]+feeder_drop_at_In+outgoing
  branch.append(dict(circuit_id=r["circuit_id"],pre_origin_allowance_V=I["pre_origin_drop_allowance_V"],incoming_bound_at63A_V=round(feeder_drop_at_In,6),outgoing_V=outgoing,total_bound_V=round(total,6),total_percent=round(total/I["voltage_LN_V"]*100,6),within4percent_under_conditions=total<=.04*I["voltage_LN_V"],status="Conditional on pre-origin drop<=2.2V, feeder neutral<=63A and documented route/installation assumptions"))
report=dict(cable=I["cable"],line_neutral_mm2=35,CPC_mm2=16,plan_route_m=round(plan,6),vertical_termination_assumed_m=3,design_length_m=round(length,6),design_Ib_A=M["design_peak_A"],protective_In_A=63,Iz25_A=round(Iz25,6),Iz35_A=round(Iz,6),capacity_pass=M["design_peak_A"]<=63<=Iz,pair_drop_coefficient_bound_mV_A_m=pair_mV,incoming_drop_bound_at63A_V=round(feeder_drop_at_In,6),incoming_drop_bound_at_designIb_V=round(feeder_drop_at_Ib,6),Rphase_plus_CPC_70C_ohm=round(Rloop,6),max_external_loop_Ze_at_meter_ohm=round(Zsource_max,6),CPC_permissible_I2t_A2s=(I["PVC_CPC_k"]*16)**2,all15_total_drop_checks_pass_under_conditions=all(r["within4percent_under_conditions"] for r in branch),worst_total_drop_percent=max(r["total_percent"] for r in branch),limitations=I["limitations"])
assert Iz25<63<=Iz and len(branch)==15 and report["capacity_pass"] and report["all15_total_drop_checks_pass_under_conditions"] and Zsource_max>0
(D/"incoming_cable_results.json").write_text(json.dumps(report,indent=2),encoding="utf8")
with (D/"all_circuits_voltage_drop.csv").open("w",encoding="utf8",newline="") as f:w=csv.DictWriter(f,fieldnames=branch[0],lineterminator="\n");w.writeheader();w.writerows(branch)
print(json.dumps(report))
