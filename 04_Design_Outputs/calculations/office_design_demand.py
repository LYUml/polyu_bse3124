"""Adopted working demand from actual designed FCU limits, not appliance wattages."""
import csv,json
from pathlib import Path
R=Path(__file__).resolve().parents[2];D=R/"04_Design_Outputs/data"
rows=list(csv.DictReader((D/"circuits.csv").open()))
assert len(rows)==15
out=[]
for phase in ["L1","L2","L3"]:
 selected=[r for r in rows if r["phase"]==phase]
 lighting=sum(float(r["Ib_A"]) for r in selected if r["circuit_id"].startswith("LC-"))
 socket=[float(r["Ib_A"]) for r in selected if r["circuit_id"].startswith("P") and r["circuit_id"]!="P7"]
 fixed=sum(float(r["Ib_A"]) for r in selected if r["circuit_id"]=="P7")
 sockets=max(socket)+.5*(sum(socket)-max(socket)) if socket else 0
 out.append(dict(phase=phase,lighting_undiversified_A=round(lighting,6),socket_FCU_sum_A=sum(socket),socket_diversified_A=sockets,fixed_reserved_A=fixed,design_demand_A=round(.9*lighting+sockets+fixed,6),undiversified_point_capacity_A=round(lighting+sum(socket)+fixed,6)))
peak=max(r["design_demand_A"] for r in out)
report=dict(basis="EMSD2025 Table7(1): small office lighting90%; code6E circuits largest100% plus others50%; fixed P7 reserved13A without diversity",load_basis="Individually13A fused point bounds: four rings26A each; P5/P8 radials13A each; P6 radial26A; P7 fixed reserve13A. No actual appliance watts invented.",design_peak_A=peak,incoming_protective_candidate_A=63,DB_busbar_minimum_design_A=100,nondiversified_peak_A=max(r["undiversified_point_capacity_A"] for r in out),phases=out,limitations=["63A source with 4C35mm2 + CPC16; see incoming_cable_results.json and fault_protection_summary.json","Only valid with all designed13A point FCUs installed; no unfused additions","P7 actual equipment identity unknown; design capacity limited to13A","Maximum demand uses the adopted 13A assembly capacities and phase diversity"])
with (D/"office_design_demand.csv").open("w",newline="",encoding="utf8") as f:w=csv.DictWriter(f,fieldnames=out[0],lineterminator="\n");w.writeheader();w.writerows(out)
(D/"office_design_demand.json").write_text(json.dumps(report,indent=2),encoding="utf8")
assert peak<=63 and report["nondiversified_peak_A"]<=100
print(json.dumps(report))
