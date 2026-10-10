import bpy, sys
import numpy as np
from mathutils.bvhtree import BVHTree
from mathutils import Vector
bpy.ops.wm.open_mainfile(filepath=sys.argv[-1], load_ui=False)
sc=bpy.context.scene; O=bpy.data.objects; sc.frame_set(145)
dg=bpy.context.evaluated_depsgraph_get()
def wv(o):
    e=o.evaluated_get(dg); me=e.to_mesh(); v=np.array([x.co[:] for x in me.vertices]); M=np.array(e.matrix_world); e.to_mesh_clear(); return v@M[:3,:3].T+M[:3,3]
def bvh(o):
    e=o.evaluated_get(dg); me=e.to_mesh(); me.calc_loop_triangles()
    v=[tuple((e.matrix_world@x.co)) for x in me.vertices]; t=[tuple(lt.vertices) for lt in me.loop_triangles]; e.to_mesh_clear(); return BVHTree.FromPolygons(v,t)
body=O['E5_S02_CAR_00_BODY']; B=bvh(body)
for n in ['E5_S02_CAR_00_GLASS_1','E5_S02_CAR_00_GLASS_-1','E5_S02_CAR_00_PINK_1']:
    g=wv(O[n]); 
    d=[B.find_nearest(Vector(p))[3] for p in g]
    print(n,'X',np.round([g[:,0].min(),g[:,0].max()],2),'Z',np.round([g[:,2].min(),g[:,2].max()],2),'dist to body min/max',round(min(d),3),round(max(d),3))
bv=wv(body)
for x in (157,155,152,150,148,146):
    sl=bv[np.abs(bv[:,0]-x)<0.6]
    if len(sl): print('body at X',x,'Z',np.round([sl[:,2].min(),sl[:,2].max()],2),'Y',np.round([sl[:,1].min(),sl[:,1].max()],2))
w=wv(O['E5_S02_CAR_00_BOGIE_0_AXLE_0_WHEEL_1']); w2=wv(O['E5_S02_CAR_00_BOGIE_0_AXLE_0_WHEEL_-1'])
print('wheel Y', np.round([w[:,1].min(),w[:,1].max()],3), np.round([w2[:,1].min(),w2[:,1].max()],3))
rails=[o for o in O if o.name.startswith('S02') or ('RAIL' in o.name.upper() and o.name.startswith(('ENV','S02','TRACK')))]
rn=[o.name for o in O if 'RAIL' in o.name.upper()][:10]; print('rail objs', rn)
for n in rn[:4]:
    r=wv(O[n]); print(n,'Y uniq', np.unique(np.round(r[:,1],3))[:12], 'Ztop', round(r[:,2].max(),3))
