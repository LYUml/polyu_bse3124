"""Preliminary radial cable check; values must come from the selected cable table.

EMSD Wiring CoP 2025 Code 13A(3), Appendix 5 and Appendix 6.
This does not check fault withstand, disconnection, harmonics or ring circuits.
"""
import argparse
import json

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--ib', type=float, required=True, help='design current, A')
p.add_argument('--in-rating', type=float, required=True, help='protective device rating, A')
p.add_argument('--it', type=float, required=True, help='tabulated ampacity, A')
p.add_argument('--factors', type=float, nargs='+', required=True, help='applicable correction factors')
p.add_argument('--mv-per-a-m', type=float, required=True, help='table mV/A/m for actual circuit')
p.add_argument('--length-m', type=float, required=True, help='one-way circuit route length, m')
p.add_argument('--nominal-v', type=float, required=True, help='nominal supply voltage, V')
p.add_argument('--upstream-drop-v', type=float, required=True, help='known/assumed upstream drop, V')
p.add_argument('--source', required=True, help='exact table, column and input source')
a = p.parse_args()
if min(a.ib, a.in_rating, a.it, a.mv_per_a_m, a.length_m, a.nominal_v) <= 0 or a.upstream_drop_v < 0:
 p.error('currents, table values, length and voltage must be positive; upstream drop must be nonnegative')
if any(not 0 < x <= 1 for x in a.factors):
 p.error('each derating factor must be greater than zero and no greater than one')
product = 1.0
for f in a.factors: product *= f
corrected = a.it * product
branch_drop = a.mv_per_a_m * a.ib * a.length_m / 1000
total_drop = a.upstream_drop_v + branch_drop
print(json.dumps({'table_source': a.source, 'derating_product': product,
 'corrected_ampacity_A': corrected, 'ib_le_in_le_iz': a.ib <= a.in_rating <= corrected,
 'radial_drop_V': branch_drop, 'total_drop_V': total_drop,
 'total_drop_percent': total_drop / a.nominal_v * 100,
 'within_4_percent_simplified': total_drop <= .04 * a.nominal_v,
 'status': 'PRELIMINARY: verify tables, operating conditions, upstream, faults and disconnection'}, indent=2))
