import bpy, sys, math
import numpy as np
from collections import Counter
bpy.ops.wm.open_mainfile(filepath=sys.argv[-1], load_ui=False)
sc=bpy.context.scene; r=sc.render
print("res", r.resolution_x, r.resolution_y, r.resolution_percentage, "fps", r.fps, "frames", sc.frame_start, sc.frame_end, "engine", r.engine, "mblur", r.use_motion_blur, r.motion_blur_shutter, "view", sc.view_settings.view_transform, sc.view_settings.look, "exp", sc.view_settings.exposure)
if r.engine=='CYCLES': print("samples", sc.cycles.samples)
print("markers", [(m.name,m.frame,m.camera.name if m.camera else None) for m in sorted(sc.timeline_markers,key=lambda m:m.frame)])
print("types", Counter(o.type for o in bpy.data.objects), "FONT data", len(bpy.data.curves) and sum(1 for c in bpy.data.curves if c.bl_rna.identifier=='TextCurve'))
print("images", [(i.name,i.filepath) for i in bpy.data.images][:10])
print("collections", [(c.name,len(c.all_objects)) for c in bpy.data.collections][:40])
for o in sorted([o for o in bpy.data.objects if o.type=='CAMERA'],key=lambda o:o.name):
    sc.frame_set(1)
    print("cam", o.name, "lens", round(o.data.lens,1), "rotZYX deg", [round(math.degrees(a),1) for a in o.matrix_world.to_euler('XYZ')], "has_anim", bool(o.animation_data and o.animation_data.action))
names=[o.name for o in bpy.data.objects]
print("n obj", len(names))
print([n for n in names if any(k in n.upper() for k in ('WHEEL','ROOT','BOGIE','PANTO','MOTION'))][:80])
