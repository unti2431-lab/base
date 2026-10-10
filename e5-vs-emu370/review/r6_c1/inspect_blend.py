import bpy, sys, math, json
from mathutils import Vector
p = sys.argv[-1]
bpy.ops.wm.open_mainfile(filepath=p, load_ui=False)
sc = bpy.context.scene
r = sc.render
print("scene", sc.name, "frames", sc.frame_start, sc.frame_end, "fps", r.fps, "res", r.resolution_x, r.resolution_y, r.resolution_percentage)
print("engine", r.engine, "motion_blur", r.use_motion_blur, "shutter", r.motion_blur_shutter, "view", sc.view_settings.view_transform, sc.view_settings.look)
if r.engine == 'CYCLES': print("samples", sc.cycles.samples, "device", sc.cycles.device)
print("markers", [(m.name, m.frame, m.camera.name if m.camera else None) for m in sc.timeline_markers])
print("world", sc.world.name if sc.world else None, [n.bl_idname for n in sc.world.node_tree.nodes] if sc.world and sc.world.use_nodes else None)
from collections import Counter
print("types", Counter(o.type for o in bpy.data.objects))
print("collections", [(c.name, len(c.all_objects)) for c in bpy.data.collections])
for o in bpy.data.objects:
    if o.type == 'MESH' and o.parent is None or o.type in ('CAMERA','EMPTY') and o.parent is None:
        pass
names = sorted(o.name for o in bpy.data.objects)
print("n objects", len(names)); print(names[:200])
print("materials", sorted(m.name for m in bpy.data.materials))
# root motion per shot
roots = [o for o in bpy.data.objects if o.type=='EMPTY' and 'ROOT' in o.name.upper()]
print("roots", [o.name for o in roots])
dg = bpy.context.evaluated_depsgraph_get()
for f in (1,40,75,76,150,151,270,391,540,541,661,700,810,811,856,900):
    sc.frame_set(f)
    cam = sc.camera
    row = {"F":f, "cam":cam.name, "lens":round(cam.data.lens,1), "cam_loc":[round(v,2) for v in cam.matrix_world.translation]}
    for o in roots:
        row[o.name] = [round(v,3) for v in o.matrix_world.translation] + ["vis" if not o.hide_render else "hid"]
    print(row)
# mesh extents of visible bodies
sc.frame_set(1)
for o in bpy.data.objects:
    if o.type=='MESH' and any(k in o.name.upper() for k in ('BODY','WHEEL','RAIL','GROUND','SLEEP','TIE')):
        bb=[o.matrix_world @ Vector(c) for c in o.bound_box]
        mn=[min(v[i] for v in bb) for i in range(3)]; mx=[max(v[i] for v in bb) for i in range(3)]
        print("bbox", o.name, [round(a,3) for a in mn], [round(b,3) for b in mx])
