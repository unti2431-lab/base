import bpy, sys
import numpy as np
bpy.ops.wm.open_mainfile(filepath=sys.argv[-1], load_ui=False)
sc=bpy.context.scene
def wverts(o):
    dg=bpy.context.evaluated_depsgraph_get(); e=o.evaluated_get(dg); me=e.to_mesh()
    v=np.array([x.co[:] for x in me.vertices]); M=np.array(e.matrix_world); e.to_mesh_clear()
    return v@M[:3,:3].T+M[:3,3]
for p in ('proxyA','proxyB'):
    sh=bpy.data.objects[p+'_PROXY_shell']; w=wverts(sh)
    print(p,'shell extent L,W,H', np.round(w.max(0)-w.min(0),3), 'min', np.round(w.min(0),3))
rail=wverts(bpy.data.objects['R6_RAILS_STATIC']); print('rail top Z',rail[:,2].max(), 'rail Y', np.unique(np.round(rail[:,1],3)))
for f in (1,40,75,100,150,300,700,810):
    sc.frame_set(f)
    row=[f]
    for p in ('proxyA','proxyB'):
        sh=bpy.data.objects[p+'_PROXY_shell']
        vis = not sh.hide_render
        wz=min(wverts(bpy.data.objects[f'{p}__BOGIE_{b}__WHEELSET_0{i}_{s}'])[:,2].min() for b in ('FRONT','REAR') for i in (1,2) for s in ('LEFT','RIGHT'))
        row.append((p,'vis' if vis else 'hid','wheelminZ',round(float(wz),4)))
    print(row)
