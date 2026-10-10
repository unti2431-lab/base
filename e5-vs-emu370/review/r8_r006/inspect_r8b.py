import bpy, sys, math
import numpy as np
bpy.ops.wm.open_mainfile(filepath=sys.argv[-1], load_ui=False)
sc=bpy.context.scene
def wv(o):
    dg=bpy.context.evaluated_depsgraph_get(); e=o.evaluated_get(dg); me=e.to_mesh()
    v=np.array([x.co[:] for x in me.vertices]); M=np.array(e.matrix_world); e.to_mesh_clear()
    return v@M[:3,:3].T+M[:3,3]
def lv(o):
    return np.array([x.co[:] for x in o.data.vertices])
O=bpy.data.objects
# wheel shape (local)
for n in ['E5_S06_CAR_00_BOGIE_0_AXLE_0_WHEEL_1','E5_S05_CAR_00_BOGIE_0_AXLE_0_WHEEL_1']:
    if n in O:
        o=O[n]; v=lv(o); ext=v.max(0)-v.min(0); print(n,'local extent',np.round(ext,3),'nverts',len(v),'scale',tuple(round(s,3) for s in o.scale))
# list S06 objects near camera target
print([o.name for o in O if o.name.startswith('E5_S06') and 'CAR_00' in o.name][:40])
# E5 body / nose vs bogie positions in S02 at F145
sc.frame_set(145)
body=[o for o in O if o.name.startswith('E5_S02_CAR_00') and o.type=='MESH' and 'BOGIE' not in o.name]
print('E5 S02 car00 meshes', [o.name for o in body][:20])
allv=np.vstack([wv(o) for o in body]) if body else None
if allv is not None:
    print('E5 car00 body X range', np.round([allv[:,0].min(), allv[:,0].max()],2), 'Z range', np.round([allv[:,2].min(), allv[:,2].max()],2))
for b in (0,1):
    n=f'E5_S02_CAR_00_BOGIE_{b}_FRAME_ROOT'
    if n in O: print(n,'world',np.round(O[n].matrix_world.translation,2))
for a in (0,1):
    n=f'E5_S02_CAR_00_BOGIE_0_AXLE_{a}_WHEEL_1'
    if n in O:
        w=wv(O[n]); print(n,'X',np.round([w[:,0].min(),w[:,0].max()],2),'Zmin',round(w[:,2].min(),4))
