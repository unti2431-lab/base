import bpy, sys, math
import numpy as np
bpy.ops.wm.open_mainfile(filepath=sys.argv[-1], load_ui=False)
sc=bpy.context.scene; O=bpy.data.objects
def track(prefix, frames):
    root=None
    cands=[o for o in O if o.name.startswith(prefix) and o.name.endswith('BODY_ROOT')]
    root=sorted(cands,key=lambda o:o.name)[0]
    axle=O[root.name.replace('BODY_ROOT','BOGIE_0_AXLE_0')]
    xs=[];ang=[]
    for f in frames:
        sc.frame_set(f); xs.append(root.matrix_world.translation.x)
        q=axle.matrix_world.to_quaternion(); 
        ang.append(axle.matrix_world.to_euler('XYZ').y)
    return root.name, np.array(xs), np.unwrap(np.array(ang))
def report(prefix, fr, r):
    n,xs,ang=track(prefix, fr)
    dx=np.diff(xs); da=np.diff(ang)
    v=dx*30
    ratio=np.where(np.abs(dx)>1e-6, np.abs(da)*r/np.maximum(np.abs(dx),1e-9), np.nan)
    print(n, 'v m/s min/med/max', np.round([v.min(), np.median(v), v.max()],2), 'km/h med', round(np.median(np.abs(v))*3.6,1))
    print('  roll ratio |dθ|r/|dx| min/med/max', np.round([np.nanmin(ratio), np.nanmedian(ratio), np.nanmax(ratio)],3))
    return v
fr=list(range(1,91))
e=report('E5_S01_CAR_00', fr, 0.43)
m=report('EMU_S01', fr, 0.460645) if any(o.name.startswith('EMU_S01') for o in O) else None
print('EMU names sample', [o.name for o in O if o.name.startswith('EMU') and 'ROOT' in o.name][:8])
print('E5 S01 per-frame speed km/h', np.round(np.abs(e)*3.6,0).astype(int).tolist())
for sh,rng in [('S02',range(91,199)),('S05',range(397,505)),('S06',range(505,604)),('S07',range(604,703))]:
    report(f'E5_{sh}_CAR_00', list(rng), 0.43)
