"""Northeast room candidate screening; excludes LED90; not a compliance model."""
import csv, math
from pathlib import Path
import numpy as np
OMIT=8  # LED90 in the current LC-E ordering; assert below.
ROOT=Path(__file__).resolve().parents[2]
data=ROOT/'04_Design_Outputs/data'
a=(data/'photometry/PIL_PLATO_600_840_MULTIPOWER_MEDIUMLOW_3117955.ldt').read_text(encoding='utf-8-sig').splitlines()
assert (int(a[2]),int(a[3]),int(a[5]),int(a[26])) == (4,72,181,1)
flux=float(a[28]); conversion=float(a[23]); I=np.asarray(a[295:],float).reshape(19,181)
# Quadrant symmetry: C=0..90 deg, gamma=0..180 deg, cd/klm.
integral=4*np.trapezoid(np.trapezoid(I*np.sin(np.radians(np.arange(181)))[None,:],x=np.radians(np.arange(181)),axis=1),x=np.radians(np.arange(0,91,5)))
assert abs(integral-1000)<5 and conversion==1
with (data/'devices.csv').open(encoding='utf-8-sig',newline='') as f:
 selected=[r for r in csv.DictReader(f) if r['circuit_id']=='LC-E']
assert selected[OMIT]['device_id']=='LED90'
lamps=[(float(r['x'])/1000,float(r['y'])/1000) for r in selected]
assert len(lamps)==15
lamps = [p for i,p in enumerate(lamps) if i != OMIT]
xmin,xmax,ymin,ymax=70.5259,79.8084,31.5881,36.5956
# Equal cell midpoints, within an assumed 0.5 m perimeter offset.
nx=math.ceil((xmax-xmin-1)/.25); ny=math.ceil((ymax-ymin-1)/.25)
xs=xmin+.5+(np.arange(nx)+.5)*(xmax-xmin-1)/nx
ys=ymin+.5+(np.arange(ny)+.5)*(ymax-ymin-1)/ny
X,Y=np.meshgrid(xs,ys)
rows=[]
for h in (1.7,1.9,2.2):
 E=np.zeros_like(X)
 for lx,ly in lamps:
  dx=X-lx;dy=Y-ly; rho=np.hypot(dx,dy);theta=np.degrees(np.arctan2(rho,h)); c=np.degrees(np.arctan2(dy,dx))%180; c=np.where(c>90,180-c,c)
  ci=np.minimum((c/5).astype(int),17);cf=c/5-ci
  gi=np.minimum(theta.astype(int),179);gf=theta-gi
  intensity=(I[ci,gi]*(1-cf)*(1-gf)+I[ci+1,gi]*cf*(1-gf)+I[ci,gi+1]*(1-cf)*gf+I[ci+1,gi+1]*cf*gf)*flux/1000*conversion
  E+=intensity*h/(h*h+rho*rho)**1.5
 E*=.8
 rows.append({'mounting_to_workplane_m':h,'maintenance_factor':.8,'grid_points':E.size,'mean_direct_lux':round(float(E.mean()),1),'min_direct_lux':round(float(E.min()),1),'min_mean_direct_ratio':round(float(E.min()/E.mean()),3),'scope':'direct point-source estimate only; assumptions, no interreflection or obstruction'})
out=data/'northeast_14_direct_screen.csv'
with out.open('w',encoding='utf8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys(),lineterminator='\n');w.writeheader();w.writerows(rows)
print('intensity integral cd/klm:',round(float(integral),2),'grid',nx,'x',ny)
for r in rows: print(r)

