#!/usr/bin/env python3
"""TEST A scene build (bpy 4.5 LTS, CONCEPT_ONLY). Geometry from rig_config.json + the polygons saved by kin_shibataA,
motion only from evidence/shibA_bake.npz.

usage:  python build_shibataA.py [--render START END --preset animatic|key4s --out DIR]
No bpy.ops except save/render. Head B = point-symmetric instance (Z 180 deg) of head A, same mesh data.
"""
import sys, os, json, math, argparse, time
import numpy as np
import bpy, bmesh
from mathutils import Vector, Matrix

LOCK = (4, 5); assert bpy.app.version[:2] == LOCK, f"Blender {bpy.app.version_string} != LOCK {LOCK}"
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
CFG = json.load(open(os.path.join(HERE, "rig_config.json"))); T = CFG["test_A_shibata"]
G = {k: v["value"] for k, v in T["geometry"].items()}; CAM = T["camera"]; N = T["bake_frames"]
Z = np.load(os.path.join(ROOT, "evidence", "shibA_bake.npz")); B = Z["bake"]; LOCK_POLY = Z["lock_poly"]; PROT_POLY = Z["prot_poly"]
EV = json.load(open(os.path.join(ROOT, "evidence", "shibA_events.json")))
Pv = Vector((G["lock_pivot"][0], G["lock_pivot"][1], 0.0)); xc = G["protrusion_x"]

# ---------------- helpers (same as build_schB) ----------------
def _channelbag(act, slot):
    from bpy_extras import anim_utils
    if hasattr(anim_utils, 'action_ensure_channelbag_for_slot'): return anim_utils.action_ensure_channelbag_for_slot(act, slot)
    layer = act.layers[0] if len(act.layers) else act.layers.new("Layer")
    strip = layer.strips[0] if len(layer.strips) else layer.strips.new(type='KEYFRAME')
    return strip.channelbag(slot, ensure=True)
def bake_fcurves(ob, frames, chans):
    frames = np.asarray(frames, float); n = len(frames)
    ad = ob.animation_data_create(); act = bpy.data.actions.new(ob.name + '_act')
    slot = act.slots.new(id_type=ob.id_type, name=ob.name); ad.action = act; ad.action_slot = slot; cb = _channelbag(act, slot)
    for path, arr in chans.items():
        arr = np.asarray(arr, float).reshape(n, -1)
        for i in range(arr.shape[1]):
            fc = cb.fcurves.new(path, index=i); fc.keyframe_points.add(n)
            co = np.empty(2 * n); co[0::2] = frames; co[1::2] = arr[:, i]
            fc.keyframe_points.foreach_set('co', co.tolist()); fc.keyframe_points.foreach_set('interpolation', [1] * n); fc.update()
    return act
def mesh_from_bm(name, bm, bevel=0.0):
    if bevel > 0: bmesh.ops.bevel(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], offset=bevel, segments=2, affect='EDGES')
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.update(); return me
def box(name, sx, sy, sz, center=(0, 0, 0), bevel=0.004):
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0); bmesh.ops.scale(bm, vec=(sx, sy, sz), verts=bm.verts)
    bmesh.ops.translate(bm, vec=center, verts=bm.verts); return mesh_from_bm(name, bm, bevel)
def cyl(name, r, h, center=(0, 0, 0), axis='Z', segs=32):
    bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=segs, radius1=r, radius2=r, depth=h)
    if axis == 'Y': bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=Matrix.Rotation(-math.pi / 2, 3, 'X'), verts=bm.verts)
    bmesh.ops.translate(bm, vec=center, verts=bm.verts); return mesh_from_bm(name, bm)
def extrude_poly(name, coords, z0, z1, bevel=0.003):
    """closed 2D polygon (x,y) -> prism between z0 and z1"""
    bm = bmesh.new(); pts = [bm.verts.new((x, y, z0)) for x, y in coords[:-1]] if tuple(coords[0]) == tuple(coords[-1]) else [bm.verts.new((x, y, z0)) for x, y in coords]
    f = bm.faces.new(pts); res = bmesh.ops.extrude_face_region(bm, geom=[f]); vs = [v for v in res["geom"] if isinstance(v, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, vec=(0, 0, z1 - z0), verts=vs); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); return mesh_from_bm(name, bm, bevel)
def mat(name, rgb, metallic=1.0, rough=0.35):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Metallic"].default_value = metallic; b.inputs["Roughness"].default_value = rough; return m
def new_ob(name, me, parent=None, mat_=None, loc=(0, 0, 0), rot=(0, 0, 0)):
    ob = bpy.data.objects.new(name, me); ob.location = loc; ob.rotation_euler = rot
    if parent: ob.parent = parent
    if mat_ and me and mat_.name not in me.materials: me.materials.append(mat_)
    bpy.context.scene.collection.objects.link(ob); return ob

# ---------------- scene ----------------
sc = bpy.context.scene
for ob in list(bpy.data.objects): bpy.data.objects.remove(ob)
for col in list(bpy.data.collections): bpy.data.collections.remove(col)
for me_ in list(bpy.data.meshes): bpy.data.meshes.remove(me_)
for m_ in list(bpy.data.materials): bpy.data.materials.remove(m_)
sc.render.resolution_x, sc.render.resolution_y = 1080, 1920; sc.frame_start, sc.frame_end = 1, N; sc.render.fps = CFG["_meta"]["fps"]
M_STEEL = mat("steel_cast", (0.55, 0.56, 0.58), 1.0, 0.45); M_HOUSING = mat("steel_dark", (0.22, 0.23, 0.25), 1.0, 0.6)
M_LOCK = mat("lock_teal", (0.05, 0.55, 0.60), 1.0, 0.35); M_PROT = mat("knuckle_light", (0.80, 0.80, 0.78), 1.0, 0.3)
M_SPRING = mat("spring", (0.35, 0.36, 0.40), 1.0, 0.5); M_FLOOR = mat("floor", (0.12, 0.12, 0.12), 0.0, 0.9)

hw, hh, ft, hd = G["front_plate_half_width"], G["front_plate_half_height"], G["front_plate_thickness"], G["housing_depth"]
W = G["chamber_window_half"]; REC = 0.0008; LT = G["lock_thickness"]
# face: solid except a square window at x=-xc (chamber mouth); the knuckle grows from the face at x=+xc
cols = [(-hw, -xc - W, True), (-xc - W, -xc + W, False), (-xc + W, hw, True)]
ME_FACES = []
for i, (x0, x1, full) in enumerate(cols):
    if full: ME_FACES.append(box(f"FACE{i}", x1 - x0, ft, 2 * hh, center=((x0 + x1) / 2, -ft / 2 - REC, 0)))
    else:
        ME_FACES.append(box(f"FACE{i}T", x1 - x0, ft, hh - W, center=((x0 + x1) / 2, -ft / 2 - REC, (hh + W) / 2)))
        ME_FACES.append(box(f"FACE{i}B", x1 - x0, ft, hh - W, center=((x0 + x1) / 2, -ft / 2 - REC, -(hh + W) / 2)))
ME_FLOOR = box("HOUSING_FLOOR", 2 * hw * 0.9, hd, 0.02, center=(0, -ft - hd / 2, -hh * 0.55))
# knuckle: the top-view stadium (with neck) extruded +-rh in z (CONCEPT: square-ish section; a round section would need a lathe)
ME_PROT = extrude_poly("KNUCKLE", PROT_POLY, -G["protrusion_head_radius"], G["protrusion_head_radius"], bevel=0.0)   # no bevel: a bevel fills the concave neck corner and eats the 1.5 mm clearance
ME_LOCK = extrude_poly("ROTARY_LOCK", LOCK_POLY, -LT / 2, LT / 2, bevel=0.003)
ME_MAINPIN = cyl("MAIN_PIN", 0.018, LT + 0.08); ME_SPRING = cyl("SPRING_BAR", 0.010, 1.0, center=(0, 0.5, 0), axis='Y', segs=12)

def build_head(tag):
    root = new_ob(f"HEAD_{tag}", None)
    for i, me_ in enumerate(ME_FACES): new_ob(f"FACE{i}_{tag}", me_, root, M_STEEL)
    new_ob(f"HFLOOR_{tag}", ME_FLOOR, root, M_HOUSING); new_ob(f"KNUCKLE_{tag}", ME_PROT, root, M_PROT)
    piv = new_ob(f"PIVOT_{tag}", None, root, loc=Pv); new_ob(f"MAINPIN_{tag}", ME_MAINPIN, piv, M_HOUSING)
    lock = new_ob(f"LOCK_{tag}", ME_LOCK, piv, M_LOCK, loc=(-Pv.x, -Pv.y, 0))      # mesh is in A-local coords; parent pivot at Pv
    spr = new_ob(f"SPRING_{tag}", ME_SPRING, root, M_SPRING, loc=(G["spring_anchor"][0], G["spring_anchor"][1], 0))
    return root, piv, lock, spr
A = build_head("A"); Bh = build_head("B"); Bh[0].rotation_euler = (0, 0, math.pi)
new_ob("STUDIO_FLOOR", box("FLOORBOX", 4, 4, 0.02, center=(0, 0, -hh - 0.12), bevel=0), None, M_FLOOR)

# ---------------- motion from bake ----------------
F, g, al, sl = B[:, 0], B[:, 1], B[:, 2], B[:, 3]
sa = np.array(G["spring_anchor"]); spx = Pv.x - G["spring_lock_radius"] * np.sin(math.radians(G["spring_lock_angle_deg"]) + al)
spy = Pv.y + G["spring_lock_radius"] * np.cos(math.radians(G["spring_lock_angle_deg"]) + al); sp_ang = np.arctan2(spy - sa[1], spx - sa[0]) - math.pi / 2
for (root, piv, lock, spr), sgn in ((A, -1), (Bh, +1)):
    bake_fcurves(root, F, {"location": np.stack([np.zeros_like(g), sgn * g / 2, np.zeros_like(g)], 1)})
    bake_fcurves(piv, F, {"rotation_euler": np.stack([np.zeros_like(al), np.zeros_like(al), al], 1)})
    bake_fcurves(spr, F, {"rotation_euler": np.stack([np.zeros_like(sp_ang), np.zeros_like(sp_ang), sp_ang], 1), "scale": np.stack([np.ones_like(sl), sl, np.ones_like(sl)], 1)})

# ---------------- camera ----------------
E = EV["JP_LOCKED"]["local_F"]; hold = CAM["azimuth_hold_frames_around_lock"]
def ss(x): x = min(max(x, 0.0), 1.0); return x * x * (3 - 2 * x)
a0c, a1c = math.radians(CAM["azimuth_deg_start"]), math.radians(CAM["azimuth_deg_end"]); az = np.empty(len(F))
for i, f in enumerate(F):
    if f <= E - hold: s = 0.5 * ss((f - 1) / max(1, (E - hold - 1)))
    elif f <= E + hold: s = 0.5
    else: s = 0.5 + 0.5 * ss((f - (E + hold)) / max(1, (N - (E + hold))))
    az[i] = a0c + (a1c - a0c) * s
el = math.radians(CAM["elevation_deg"]); dist = CAM["distance"]; tgt = Vector(CAM["target"])
cam_data = bpy.data.cameras.new("CAM"); cam_data.lens = CAM["lens_mm"]; cam_data.sensor_fit = 'VERTICAL'; cam_data.sensor_height = 24.0
cam = new_ob("CAMERA", cam_data); sc.camera = cam; locs, rots, prev = [], [], None
for a in az:
    pos = tgt + Vector((dist * math.cos(el) * math.sin(a), -dist * math.cos(el) * math.cos(a), dist * math.sin(el)))
    q = (tgt - pos).to_track_quat('-Z', 'Y'); e = q.to_euler('XYZ', prev) if prev else q.to_euler('XYZ'); prev = e; locs.append(pos[:]); rots.append(e[:])
bake_fcurves(cam, F, {"location": np.array(locs), "rotation_euler": np.array(rots)})

# ---------------- light / world / render ----------------
sun_d = bpy.data.lights.new("SUN", 'SUN'); sun_d.energy = 4.0; sun_d.angle = math.radians(8)
sun = new_ob("SUN", sun_d, loc=(1.5, -1.0, 2.5)); sun.rotation_euler = (math.radians(35), math.radians(20), math.radians(30))
fill_d = bpy.data.lights.new("FILL", 'AREA'); fill_d.energy = 150; fill_d.size = 2.5
fill = new_ob("FILL", fill_d, loc=(-1.5, 1.0, 2.0)); fill.rotation_euler = (math.radians(30), math.radians(-30), 0)
w = bpy.data.worlds.new("W"); w.use_nodes = True; w.node_tree.nodes["Background"].inputs[0].default_value = (0.08, 0.09, 0.10, 1); sc.world = w
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.render.use_motion_blur = True; sc.render.motion_blur_shutter = 0.5
sc.cycles.use_denoising = True; sc.render.image_settings.file_format = 'PNG'; sc.render.dither_intensity = 1.0
for f in (1, EV["JP_RETRACT_PEAK"]["local_F"], E):
    sc.frame_set(f); print(f"F{f}: HEAD_B y={Bh[0].matrix_world.translation.y:+.4f} LOCK_A rz={math.degrees(A[1].rotation_euler.z):+.2f} cam=({cam.location.x:+.3f},{cam.location.y:+.3f},{cam.location.z:+.3f})")
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT, "evidence", "TEST_A_SHIB.blend"))   # bpy.ops allowed: save

ap = argparse.ArgumentParser(); ap.add_argument("--render", nargs=2, type=int); ap.add_argument("--preset", default="animatic"); ap.add_argument("--out", default=None); ap.add_argument("--gpu", action="store_true")
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]     # blender.exe -b -P script.py -- args
args = ap.parse_args(argv)
if args.gpu:   # local RTX: OptiX, fall back to CUDA
    cp = bpy.context.preferences.addons["cycles"].preferences
    for dev_type in ("OPTIX", "CUDA"):
        try:
            cp.compute_device_type = dev_type; cp.get_devices()
            gpus = [d for d in cp.devices if d.type == dev_type]
            if gpus:
                for d in cp.devices: d.use = d.type == dev_type
                sc.cycles.device = 'GPU'; print(f"GPU: {dev_type} {[d.name for d in gpus]}"); break
        except TypeError: continue
    else: raise SystemExit("--gpu given but no OPTIX/CUDA device found")
if args.render:
    Rr = CFG["render"][args.preset]; sc.render.resolution_x, sc.render.resolution_y = Rr["res"]; sc.render.resolution_percentage = 100
    sc.cycles.samples = Rr["samples"]; sc.cycles.use_adaptive_sampling = Rr.get("adaptive", False); sc.render.use_motion_blur = Rr["motion_blur"]; out = args.out or os.path.join(ROOT, "render", f"shibA_{args.preset}")
    os.makedirs(out, exist_ok=True)
    for f in range(args.render[0], args.render[1] + 1):
        fp = os.path.join(out, f"{f:04d}.png")
        if os.path.exists(fp): continue
        sc.frame_set(f); sc.render.filepath = fp; t0 = time.time(); bpy.ops.render.render(write_still=True)   # bpy.ops allowed: render
        print(f"rendered {f} in {time.time() - t0:.1f}s", flush=True)
