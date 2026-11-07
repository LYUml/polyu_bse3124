"""Final schedule photometry: conditional course geometry, no reflected-light credit.

Uses every final device's actual power setting. Coordinates are from the common
device table. Room envelopes are explicitly adopted design approximations from
the retained architectural screens, not surveyed areas or the Task1 UFA.
"""
import csv, json, math
from pathlib import Path
import numpy as np
D=Path(__file__).resolve().parents[1]/'data'
lamps=[r for r in csv.DictReader((D/'devices.csv').open()) if r['circuit_id'].startswith('LC-') and float(r['power_W'])>0]
zones={
 'Open office':dict(circuits=['LC-A','LC-B','LC-C','LC-E'],rectangles=[[64.525932,75.115,16.105584,31.4881],[75.115,79.808432,19.2625,24.0569],[70.525932,79.808432,31.5881,36.595584]],target=500),
 'Pantry':dict(circuits=['LC-D'],rectangles=[[64.525932,70.425932,31.588083655,36.595583655]],target=500),
 'Upper east room':dict(circuits=['LC-F'],rectangles=[[75.215,79.808432,24.1569,31.4881]],target=500),
 'South east room':dict(circuits=['LC-G'],rectangles=[[75.215,78.783432,16.105584,17.050584],[75.215,79.808432,17.050584,19.1625]],target=500)}
profiles={}
for W,name in [(22,'LOW'),(28,'MEDIUMLOW')]:
 a=(D/f'photometry/PIL_PLATO_600_840_MULTIPOWER_{name}_3117955.ldt').read_text().splitlines()
 assert int(a[2])==4 and int(a[3])==72 and int(a[5])==181 and float(a[31])==W
 profiles[W]=(np.array(a[295:],float).reshape(19,181),float(a[28]))
 # Integrate symmetric C0..90 cd/klm over downward hemisphere: guard parser/units.
 gamma=np.deg2rad(np.arange(181));C=np.deg2rad(np.arange(0,91,5))
 integral=4*np.trapezoid(np.trapezoid(profiles[W][0]*np.sin(gamma)[None,:],gamma,axis=1),C)
 assert 950<integral<1050,integral
rows=[]
for zone,z in zones.items():
 selected=[r for r in lamps if r['circuit_id'] in z['circuits']]
 grids=[]
 for x0,x1,y0,y1 in z['rectangles']:
  nx=math.ceil((x1-x0)/.2);ny=math.ceil((y1-y0)/.2)
  X,Y=np.meshgrid(x0+(np.arange(nx)+.5)*(x1-x0)/nx,y0+(np.arange(ny)+.5)*(y1-y0)/ny)
  grids.append((X.ravel(),Y.ravel(),np.full(X.size,(x1-x0)*(y1-y0)/X.size)))
 X,Y,weight=[np.concatenate([g[i] for g in grids]) for i in range(3)]
 for h in [1.7,1.9,2.2]:
  E=np.zeros_like(X)
  for r in selected:
   I,flux=profiles[int(float(r['power_W']))]
   dx=X-float(r['x'])/1000;dy=Y-float(r['y'])/1000;rho=np.hypot(dx,dy)
   gamma=np.degrees(np.arctan2(rho,h));c=np.degrees(np.arctan2(dy,dx))%180;c=np.where(c>90,180-c,c)
   ci=np.minimum((c/5).astype(int),17);cf=c/5-ci;gi=np.minimum(gamma.astype(int),179);gf=gamma-gi
   intensity=(I[ci,gi]*(1-cf)*(1-gf)+I[ci+1,gi]*cf*(1-gf)+I[ci,gi+1]*(1-cf)*gf+I[ci+1,gi+1]*cf*gf)*flux/1000
   E+=intensity*h/(h*h+rho*rho)**1.5*.8
  avg=np.average(E,weights=weight)
  rows.append(dict(zone=zone,circuits=';'.join(z['circuits']),lamp_count=len(selected),power_W=sum(float(r['power_W']) for r in selected),area_m2=round(weight.sum(),4),height_above_workplane_m=h,maintenance_factor=.8,mean_maintained_direct_lx=round(avg,1),minimum_direct_lx=round(E.min(),1),min_mean=round(E.min()/avg,3),target_mean_lx=z['target'],mean_target_met=bool(avg>=z['target']),scope='Adopted course envelopes; no reflections, furniture shadow or verified mounting height; not glare/uniformity certification'))
assert sum(len([r for r in lamps if r['circuit_id'] in z['circuits']]) for z in zones.values())==92
with (D/'final_lighting_basis.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0],lineterminator='\n');w.writeheader();w.writerows(rows)
(D/'final_lighting_basis.json').write_text(json.dumps(dict(zones=zones,adopted_height_above_workplane_m=1.9,maintenance_factor=.8,grid_max_spacing_m=.2,method='E=sum(I(C,gamma)*cos(gamma)/d^2)*MF; LDT cd/klm scaled by actual flux. Separate zones receive only their own luminaires; approximate open-office connected geometry.',area_source='Adopted rectangle coordinates recorded in this script and final_lighting_basis.json; pantry_area_sensitivity.csv; lighting_room_rectangles_review.csv; south_east_area_review.csv',limitations='Adopted planning geometry not independent survey. MF0.8 assumes periodic cleaning/replacement. No credit for reflected light. Mean target does not establish minimum illuminance, glare or uniformity. Task1 309m2 is a different provisional UFA basis.',results=rows),indent=2))
for r in rows: print(r['zone'],r['height_above_workplane_m'],r['mean_maintained_direct_lx'],r['minimum_direct_lx'])

