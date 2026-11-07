"""Capacity scenario after separating pantry sockets; no invented appliance watts."""
import csv,json,math
from pathlib import Path
R=Path(__file__).resolve().parents[2];D=R/"04_Design_Outputs/data"
rows=list(csv.DictReader((D/"office_capacity_scenario.csv").open(encoding="utf8")))
assert len(rows)==15 and len({r["circuit_id"] for r in rows})==15
out=[]
for phase in ["L1","L2","L3"]:
 selected=[r for r in rows if r["phase_scenario"]==phase]
 lights=sum(float(r["capacity_or_lamp_current_A"]) for r in selected if r["role"]=="lighting")
 sockets=[float(r["capacity_or_lamp_current_A"]) for r in selected if r["role"]=="socket_reserved"]
 fixed=sum(float(r["capacity_or_lamp_current_A"]) for r in selected if r["role"]=="fixed_reserved")
 socket_md=max(sockets)+.5*(sum(sockets)-max(sockets)) if sockets else 0
 out.append(dict(phase=phase,lighting_A=round(lights,6),socket_capacity_sum_A=sum(sockets),
  socket_diversified_A=socket_md,fixed_reserved_A=fixed,
  diversified_total_A=round(.9*lights+socket_md+fixed,6),
  undiversified_capacity_A=round(lights+sum(sockets)+fixed,6),
  basis="EMSD2025 Table7(1) small offices lighting90% PDF66; Code6E circuits largest100%+others50% PDF68; P7 no diversity",
  status="Scenario only; actual appliance load and final circuit areas/topologies not established"))
with (D/"office_capacity_phase_results.csv").open("w",encoding="utf8",newline="") as f:
 w=csv.DictWriter(f,fieldnames=out[0],lineterminator="\n");w.writeheader();w.writerows(out)
peak=max(r["diversified_total_A"] for r in out)
summary=dict(peak_phase_A=peak,planning_protective_rating_A=next(x for x in [63,80,100,125] if x>=peak),
 no_diversity_peak_A=max(r["undiversified_capacity_A"] for r in out),
 previous_63A_scenario_valid=False,reason="15 circuits now include separate P8; scenario must not reuse old 14-circuit demand",phases=out)
(D/"office_capacity_reservation.json").write_text(json.dumps(summary,indent=2),encoding="utf8")
print(json.dumps(summary))
