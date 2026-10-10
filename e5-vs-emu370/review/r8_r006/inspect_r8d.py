import bpy, sys, math
import numpy as np
bpy.ops.wm.open_mainfile(filepath=sys.argv[-1], load_ui=False)
sc=bpy.context.scene; O=bpy.data.objects
def mark_center(o):
    dg=bpy.context.evaluated_depsgraph_get(); e=o.evaluated_get(dg); me=e.to_mesh()
    v=np.array([x.co[:] for x in me.vertices]); M=np.array(e.matrix_world); e.to_mesh_clear()
    return (v@M[:3,:3].T+M[:3,3]).mean(0)
def check(pfx, frames, r):
    root=O[pfx+'_BODY_ROOT']; wheel=O[pfx+'_BOGIE_0_AXLE_0_WHEEL_1']; mark=O[pfx+'_BOGIE_0_AXLE_0_WHEEL_1_MARK']
    xs=[];ang=[]
    for f in frames:
        sc.frame_set(f)
        c=np.array(wheel.matrix_world.translation); m=mark_center(mark)
        ang.append(math.atan2(m[2]-c[2], m[0]-c[0])); xs.append(root.matrix_world.translation.x)
    xs=np.array(xs); ang=np.unwrap(ang)
    dx=np.diff(xs); da=np.diff(ang)
    ok=np.abs(dx)>1e-4
    ratio=(-da[ok]*r)/dx[ok]
    print(pfx, 'frames',frames[0],frames[-1],'rolling ratio (1.0=no slip) min/med/max', np.round([ratio.min(),np.median(ratio),ratio.max()],3), 'n',ok.sum())
    print('   dθ per frame deg med', round(math.degrees(np.median(np.abs(da))),1), ' expected', round(math.degrees(np.median(np.abs(dx))/r),1))
check('E5_S01_CAR_00', list(range(1,50)), 0.43)
check('E5_S01_CAR_00', list(range(55,91)), 0.43)
check('E5_S02_CAR_00', list(range(91,120)), 0.43)
check('E5_S06_CAR_00', list(range(505,540)), 0.43)
