"""Conditional desk block insertion-point screening; not actual task-area validation."""
import csv,math,json
from pathlib import Path
import numpy as np
D=Path(__file__).resolve().parents[1]/'data'
with (D/'devices.csv').open(encoding='utf-8-sig',newline='') as f: lamps=[r for r in csv.DictReader(f) if r['circuit_id'] in ('LC-A','LC-B','LC-C','LC-E')]
assert len(lamps)==67
rows=[]
for mainW,file in [(22,'LOW'),(28,'MEDIUMLOW')]:
 with (D/'desk_footprint_samples.csv').open(encoding='utf-8-sig',newline='') as f: desks=[r for r in csv.DictReader(f) if r['block']=='desk B']
 X=np.array([float(r['lighting_x_mm'])/1000 for r in desks]);Y=np.array([float(r['lighting_y_mm'])/1000 for r in desks]);weights=np.ones(len(desks))
 for h in (1.7,1.9,2.2):
  E=np.zeros_like(X)
  for r in lamps:
   setting='MEDIUMLOW' if r['circuit_id']=='LC-E' else file
   a=(D/f'photometry/PIL_PLATO_600_840_MULTIPOWER_{setting}_3117955.ldt').read_text().splitlines();I=np.array(a[295:],float).reshape(19,181);flux=float(a[28])
   dx=X-float(r['x'])/1000;dy=Y-float(r['y'])/1000;rho=np.hypot(dx,dy);gamma=np.degrees(np.arctan2(rho,h));c=np.degrees(np.arctan2(dy,dx))%180;c=np.where(c>90,180-c,c)
   ci=np.minimum((c/5).astype(int),17);cf=c/5-ci;gi=np.minimum(gamma.astype(int),179);gf=gamma-gi
   inten=(I[ci,gi]*(1-cf)*(1-gf)+I[ci+1,gi]*cf*(1-gf)+I[ci,gi+1]*(1-cf)*gf+I[ci+1,gi+1]*cf*gf)*flux/1000
   E+=inten*h/(h*h+rho*rho)**1.5*.8
  area=weights.sum();power=53*mainW+14*28;avg=np.average(E,weights=weights)
  rows.append(dict(main_lamp_W=mainW,NE_lamp_W=28,height_above_workplane_m=h,sample_count=len(desks),mean_direct_lux=round(avg,1),minimum_direct_lux=round(E.min(),1),min_x_mm=round(float(X[E.argmin()])*1000,1),min_y_mm=round(float(Y[E.argmin()])*1000,1),min_mean=round(E.min()/avg,3),status='desk block bounding-box interior samples; chairs may be included; not validated task areas'))
with (D/'desk_footprint_direct_comparison.csv').open('w',encoding='utf8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0],lineterminator='\n');w.writeheader();w.writerows(rows)
for r in rows: print(r)
