#!/usr/bin/env python3
"""TEST B scene build (bpy 4.5 LTS). Geometry from rig_config.json, motion only from evidence/schB_bake.npz.

usage:  python build_schB.py [--render START END --preset animatic|key4s --out DIR]
No bpy.ops except save/render. Head B is a point-symmetric instance (Z 180 deg) of head A: same mesh data.
"""
import sys, os, json, math, argparse
import numpy as np
import bpy, bmesh
from mathutils import Vector, Matrix

LOCK = (4, 5)
assert bpy.app.version[:2] == LOCK, f"Blender {bpy.app.version_string} != LOCK {LOCK}"
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
CFG = json.load(open(os.path.join(HERE, "rig_config.json"), encoding="utf-8")); T = CFG["test_B_scharfenberg"]
G = {k: v["value"] for k, v in T["geometry"].items()}; CAM = T["camera"]; N = T["bake_frames"]
Z = np.load(os.path.join(ROOT, "evidence", "schB_bake.npz")); B = Z["bake"]; L = float(Z["link_length"])
EV = json.load(open(os.path.join(ROOT, "evidence", "schB_events.json")))
d = G["pivot_setback"]; P = Vector((0.0, -d, 0.0))

# ---------------- helpers ----------------
def _channelbag(act, slot):
    from bpy_extras import anim_utils
    if hasattr(anim_utils, 'action_ensure_channelbag_for_slot'): return anim_utils.action_ensure_channelbag_for_slot(act, slot)
    layer = act.layers[0] if len(act.layers) else act.layers.new("Layer")
    strip = layer.strips[0] if len(layer.strips) else layer.strips.new(type='KEYFRAME')
    return strip.channelbag(slot, ensure=True)

def bake_fcurves(ob, frames, chans):
    frames = np.asarray(frames, float); n = len(frames)
    ad = ob.animation_data_create(); act = bpy.data.actions.new(ob.name + '_act')
    slot = act.slots.new(id_type=ob.id_type, name=ob.name); ad.action = act; ad.action_slot = slot
    cb = _channelbag(act, slot)
    for path, arr in chans.items():
        arr = np.asarray(arr, float).reshape(n, -1)
        for i in range(arr.shape[1]):
            fc = cb.fcurves.new(path, index=i); fc.keyframe_points.add(n)
            co = np.empty(2 * n); co[0::2] = frames; co[1::2] = arr[:, i]
            fc.keyframe_points.foreach_set('co', co.tolist()); fc.keyframe_points.foreach_set('interpolation', [1] * n); fc.update()
    return act

def mesh_from_bm(name, bm, bevel=0.0):
    if bevel > 0:
        bmesh.ops.bevel(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], offset=bevel, segments=2, affect='EDGES')
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for e in me.edges: e.use_edge_sharp = False
    me.update(); return me

def box(name, sx, sy, sz, center=(0, 0, 0), bevel=0.004):
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(sx, sy, sz), verts=bm.verts); bmesh.ops.translate(bm, vec=center, verts=bm.verts)
    return mesh_from_bm(name, bm, bevel)

def cyl(name, r, h, center=(0, 0, 0), axis='Z', segs=32, bevel=0.0, r2=None):
    bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=segs, radius1=r, radius2=(r if r2 is None else r2), depth=h)
    if axis == 'Y': bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=Matrix.Rotation(-math.pi / 2, 3, 'X'), verts=bm.verts)
    if axis == 'X': bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=Matrix.Rotation(math.pi / 2, 3, 'Y'), verts=bm.verts)
    bmesh.ops.translate(bm, vec=center, verts=bm.verts); return mesh_from_bm(name, bm, bevel)

def cam_profile_mesh(name):
    """hook plate: cam polygon rho(a) extruded +-t/2, origin at the pivot."""
    LB = G["hook_lobe"]; core = G["plate_radius"]; t = G["plate_thickness"]
    def rho(a):
        da = (a - math.radians(G["notch_angle_deg"]) + math.pi) % (2 * math.pi) - math.pi
        if abs(da) <= math.radians(LB["notch_cut_half_width_deg"]): return G["notch_radius"]
        c, w, h = math.radians(LB["center_deg"]), math.radians(LB["half_width_deg"]), LB["height"]
        da = (a - c + math.pi) % (2 * math.pi) - math.pi
        return core + (h * 0.5 * (1 + math.cos(math.pi * da / w)) if abs(da) <= w else 0.0)
    bm = bmesh.new(); pts = []
    for i in range(180):
        a = 2 * math.pi * i / 180; r = rho(a); pts.append(bm.verts.new((-r * math.sin(a), r * math.cos(a), -t / 2)))
    f = bm.faces.new(pts); bm.faces.ensure_lookup_table()
    res = bmesh.ops.extrude_face_region(bm, geom=[f]); verts = [v for v in res["geom"] if isinstance(v, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, vec=(0, 0, t), verts=verts); bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return mesh_from_bm(name, bm, 0.003)

def link_mesh(name):
    """rigid bar from the pin (origin) along +x to the eye at distance L; eye = torus-ish ring (cylinder with hole approximated by ring of cylinders -> use a flat ring)."""
    rb = G["link_bar_radius"]; re_ = G["link_eye_radius"]; bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=16, radius1=rb, radius2=rb, depth=L - re_ * 0.6)
    bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=Matrix.Rotation(math.pi / 2, 3, 'Y'), verts=bm.verts)
    bmesh.ops.translate(bm, vec=((L - re_ * 0.6) / 2, 0, 0), verts=bm.verts)
    # eye: ring (torus) at x=L
    bm2 = bmesh.new(); bmesh.ops.create_cone(bm2, cap_ends=True, segments=24, radius1=re_, radius2=re_, depth=rb * 1.6)
    inner = bmesh.new(); bmesh.ops.create_cone(inner, cap_ends=True, segments=24, radius1=re_ - rb * 0.9, radius2=re_ - rb * 0.9, depth=rb * 2.0)
    # boolean-free ring: build torus directly
    bm2.free(); inner.free()
    tor = bmesh.new(); bmesh.ops.create_circle(tor, cap_ends=False, segments=24, radius=re_ - rb * 0.5)
    ring_verts = tor.verts[:]  # not used; build a proper torus below
    tor.free()
    tbm = bmesh.new(); major, minor = re_ - rb * 0.5, rb * 0.5; segs_u, segs_v = 24, 10; grid = []
    for i in range(segs_u):
        u = 2 * math.pi * i / segs_u; row = []
        for j in range(segs_v):
            v = 2 * math.pi * j / segs_v
            row.append(tbm.verts.new(((major + minor * math.cos(v)) * math.cos(u), (major + minor * math.cos(v)) * math.sin(u), minor * math.sin(v))))
        grid.append(row)
    for i in range(segs_u):
        for j in range(segs_v):
            tbm.faces.new((grid[i][j], grid[(i + 1) % segs_u][j], grid[(i + 1) % segs_u][(j + 1) % segs_v], grid[i][(j + 1) % segs_v]))
    bmesh.ops.translate(tbm, vec=(L, 0, 0), verts=tbm.verts)
    me_t = bpy.data.meshes.new("_t"); tbm.to_mesh(me_t); tbm.free()
    bm.from_mesh(me_t); bpy.data.meshes.remove(me_t)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces); return mesh_from_bm(name, bm, 0.0)

def mat(name, rgb, metallic=1.0, rough=0.35):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Metallic"].default_value = metallic; b.inputs["Roughness"].default_value = rough; return m

def new_ob(name, me, parent=None, mat_=None, loc=(0, 0, 0), rot=(0, 0, 0)):
    ob = bpy.data.objects.new(name, me); ob.location = loc; ob.rotation_euler = rot
    if parent: ob.parent = parent
    if mat_ and me and mat_.name not in me.materials: me.materials.append(mat_)   # mesh data is shared between heads
    bpy.context.scene.collection.objects.link(ob); return ob

# ---------------- scene ----------------
sc = bpy.context.scene
for ob in list(bpy.data.objects): bpy.data.objects.remove(ob)           # default Cube/Light/Camera live in a child collection
for col in list(bpy.data.collections): bpy.data.collections.remove(col)
for me_ in list(bpy.data.meshes): bpy.data.meshes.remove(me_)
for m_ in list(bpy.data.materials): bpy.data.materials.remove(m_)
sc.render.resolution_x, sc.render.resolution_y = 1080, 1920
sc.frame_start, sc.frame_end = 1, N; sc.render.fps = CFG["_meta"]["fps"]; sc.unit_settings.scale_length = 1.0
M_STEEL = mat("steel_cast", (0.55, 0.56, 0.58), 1.0, 0.45); M_HOUSING = mat("steel_dark", (0.22, 0.23, 0.25), 1.0, 0.6)
M_PLATE = mat("plate_orange", (0.85, 0.38, 0.08), 1.0, 0.35); M_LINK = mat("link_light", (0.80, 0.80, 0.78), 1.0, 0.3)
M_SPRING = mat("spring", (0.35, 0.36, 0.40), 1.0, 0.5); M_FLOOR = mat("floor", (0.12, 0.12, 0.12), 0.0, 0.9)

hw, hh, ft, hd = G["front_plate_half_width"], G["front_plate_half_height"], G["front_plate_thickness"], G["housing_depth"]
WX, WZ, WW, REC = G["cone_offset_x"], 0.07, 0.075, 0.0008     # two windows (cone side + funnel side), face recessed 0.8 mm so g=0 leaves a 1.6 mm gap
def face_boxes():
    cols = [(-hw, -WX - WW, True), (-WX - WW, -WX + WW, False), (-WX + WW, WX - WW, True), (WX - WW, WX + WW, False), (WX + WW, hw, True)]
    out = []
    for i, (x0, x1, full) in enumerate(cols):
        if full: out.append(box(f"FACE{i}", x1 - x0, ft, 2 * hh, center=((x0 + x1) / 2, -ft / 2 - REC, 0)))
        else:
            out.append(box(f"FACE{i}T", x1 - x0, ft, hh - WZ, center=((x0 + x1) / 2, -ft / 2 - REC, (hh + WZ) / 2)))
            out.append(box(f"FACE{i}B", x1 - x0, ft, hh - WZ, center=((x0 + x1) / 2, -ft / 2 - REC, -(hh + WZ) / 2)))
    return out
ME_FACES = face_boxes()
ME_FLOOR = box("HOUSING_FLOOR", 2 * hw * 0.9, hd, 0.02, center=(0, -ft - hd / 2, -hh * 0.55))
ME_CONE = cyl("CONE", G["cone_base_radius"], G["cone_length"], center=(G["cone_offset_x"], G["cone_length"] / 2 - REC, 0), axis='Y', r2=G["cone_tip_radius"])
def annulus(name, r_in, r_out, h, center, segs=32):
    bm = bmesh.new(); outer = [bm.verts.new((r_out * math.cos(2 * math.pi * i / segs), r_out * math.sin(2 * math.pi * i / segs), -h / 2)) for i in range(segs)]
    inner = [bm.verts.new((r_in * math.cos(2 * math.pi * i / segs), r_in * math.sin(2 * math.pi * i / segs), -h / 2)) for i in range(segs)]
    faces = [bm.faces.new((outer[i], outer[(i + 1) % segs], inner[(i + 1) % segs], inner[i])) for i in range(segs)]
    res = bmesh.ops.extrude_face_region(bm, geom=faces); vs = [v for v in res["geom"] if isinstance(v, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, vec=(0, 0, h), verts=vs); bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=Matrix.Rotation(-math.pi / 2, 3, 'X'), verts=bm.verts); bmesh.ops.translate(bm, vec=center, verts=bm.verts)
    return mesh_from_bm(name, bm, 0.0)
ME_FUNNEL = annulus("FUNNEL_RING", G["cone_base_radius"] + 0.004, G["funnel_mouth_radius"] + 0.006, 0.03, center=(-G["cone_offset_x"], 0.015 - REC, 0))
LZ = G["plate_thickness"] / 2 + G["link_bar_radius"] + 0.006          # link rides on top of the plate (stacked)
ME_PLATE = cam_profile_mesh("HOOK_PLATE"); ME_PIN = cyl("PIN", 0.012, 2 * (LZ + 0.02), bevel=0.0)
# hook nose: top stays below the eye plane; the eye slides over it and sits on it at lock (CONCEPT: capture is kinematic)
ME_POST = cyl("NOTCH_POST", 0.010, 2 * (LZ - G["link_bar_radius"] - 0.003)); ME_LINK = link_mesh("LINK")
ME_SPRING = cyl("SPRING_BAR", 0.010, 1.0, center=(0, 0.5, 0), axis='Y', segs=12)   # unit length along +y, scaled per frame (CONCEPT, not a helix)
ME_MAINPIN = cyl("MAIN_PIN", 0.02, G["plate_thickness"] + 0.08)

def build_head(tag):
    root = new_ob(f"HEAD_{tag}", None)
    for i, me_ in enumerate(ME_FACES): new_ob(f"FACE{i}_{tag}", me_, root, M_STEEL)
    new_ob(f"HFLOOR_{tag}", ME_FLOOR, root, M_HOUSING)
    new_ob(f"CONE_{tag}", ME_CONE, root, M_STEEL); new_ob(f"FUNNEL_{tag}", ME_FUNNEL, root, M_STEEL)
    piv = new_ob(f"PIVOT_{tag}", None, root, loc=P); new_ob(f"MAINPIN_{tag}", ME_MAINPIN, piv, M_HOUSING)
    new_ob(f"PLATE_{tag}", ME_PLATE, piv, M_PLATE)
    a_lp = math.radians(G["link_pin_angle_ready_deg"]); a_n = math.radians(G["notch_angle_deg"])
    new_ob(f"LINKPIN_{tag}", ME_PIN, piv, M_HOUSING, loc=(-G["link_pin_radius"] * math.sin(a_lp), G["link_pin_radius"] * math.cos(a_lp), 0))
    new_ob(f"POST_{tag}", ME_POST, piv, M_HOUSING, loc=(-G["notch_radius"] * math.sin(a_n), G["notch_radius"] * math.cos(a_n), 0))
    link = new_ob(f"LINK_{tag}", ME_LINK, root, M_LINK)
    spr = new_ob(f"SPRING_{tag}", ME_SPRING, root, M_SPRING, loc=(G["spring_anchor"][0], G["spring_anchor"][1], 0))
    return root, piv, link, spr

A = build_head("A"); Bh = build_head("B"); Bh[0].rotation_euler = (0, 0, math.pi)
floor = new_ob("STUDIO_FLOOR", box("FLOORBOX", 4, 4, 0.02, center=(0, 0, -hh - 0.12), bevel=0), None, M_FLOOR)

# ---------------- motion from bake ----------------
F = B[:, 0]; g = B[:, 1]; th = B[:, 2]; px, py, tx, ty, la, sl = B[:, 3], B[:, 4], B[:, 5], B[:, 6], B[:, 7], B[:, 8]
sa = np.array(G["spring_anchor"]); spx = P.x - G["spring_plate_radius"] * np.sin(math.radians(G["spring_plate_angle_deg"]) + th)
spy = P.y + G["spring_plate_radius"] * np.cos(math.radians(G["spring_plate_angle_deg"]) + th)
sp_ang = np.arctan2(spy - sa[1], spx - sa[0]) - math.pi / 2          # bar mesh points along +y
for (root, piv, link, spr), sgn in ((A, -1), (Bh, +1)):
    bake_fcurves(root, F, {"location": np.stack([np.zeros_like(g), sgn * g / 2, np.zeros_like(g)], 1)})
    bake_fcurves(piv, F, {"rotation_euler": np.stack([np.zeros_like(th), np.zeros_like(th), th], 1)})
    bake_fcurves(link, F, {"location": np.stack([px, py, np.full_like(px, LZ)], 1), "rotation_euler": np.stack([np.zeros_like(la), np.zeros_like(la), la], 1)})
    bake_fcurves(spr, F, {"rotation_euler": np.stack([np.zeros_like(sp_ang), np.zeros_like(sp_ang), sp_ang], 1), "scale": np.stack([np.ones_like(sl), sl, np.ones_like(sl)], 1)})

# ---------------- camera (world mode, top-ish, azimuth arc with hold around the lock event) ----------------
E = EV["SCH_LOCKED"]["local_F"]; hold = CAM["azimuth_hold_frames_around_lock"]
def ss(x): x = min(max(x, 0.0), 1.0); return x * x * (3 - 2 * x)
az = np.empty(len(F)); a0, a1 = math.radians(CAM["azimuth_deg_start"]), math.radians(CAM["azimuth_deg_end"])
for i, f in enumerate(F):
    if f <= E - hold: s = 0.5 * ss((f - 1) / max(1, (E - hold - 1)))
    elif f <= E + hold: s = 0.5
    else: s = 0.5 + 0.5 * ss((f - (E + hold)) / max(1, (N - (E + hold))))
    az[i] = a0 + (a1 - a0) * s
el = math.radians(CAM["elevation_deg"]); dist = CAM["distance"]; tgt = Vector(CAM["target"])
cam_data = bpy.data.cameras.new("CAM"); cam_data.lens = CAM["lens_mm"]; cam_data.sensor_fit = 'VERTICAL'; cam_data.sensor_height = 24.0
cam = new_ob("CAMERA", cam_data); sc.camera = cam
locs, rots = [], []; prev = None
for a in az:
    pos = tgt + Vector((dist * math.cos(el) * math.sin(a), -dist * math.cos(el) * math.cos(a), dist * math.sin(el)))
    q = (tgt - pos).to_track_quat('-Z', 'Y'); e = q.to_euler('XYZ', prev) if prev else q.to_euler('XYZ'); prev = e
    locs.append(pos[:]); rots.append(e[:])
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

# sanity: things actually move
for f in (1, E):
    sc.frame_set(f); print(f"F{f}: HEAD_B y={Bh[0].matrix_world.translation.y:+.4f} PLATE_A rz={math.degrees(A[1].rotation_euler.z):+.2f} LINK_A tip=({(A[2].matrix_world @ Vector((L,0,0))).x:+.4f},{(A[2].matrix_world @ Vector((L,0,0))).y:+.4f}) cam=({cam.location.x:+.3f},{cam.location.y:+.3f},{cam.location.z:+.3f})")
os.makedirs(os.path.join(ROOT, "evidence"), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT, "evidence", "TEST_B_SCH.blend"))   # bpy.ops allowed: save

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
    R = CFG["render"][args.preset]; sc.render.resolution_x, sc.render.resolution_y = R["res"]; sc.render.resolution_percentage = 100
    sc.cycles.samples = R["samples"]; sc.cycles.use_adaptive_sampling = R.get("adaptive", False); sc.render.use_motion_blur = R["motion_blur"]; out = args.out or os.path.join(ROOT, "render", f"schB_{args.preset}")
    os.makedirs(out, exist_ok=True); import time
    for f in range(args.render[0], args.render[1] + 1):
        fp = os.path.join(out, f"{f:04d}.png")
        if os.path.exists(fp): continue
        sc.frame_set(f); sc.render.filepath = fp; t0 = time.time(); bpy.ops.render.render(write_still=True)   # bpy.ops allowed: render
        print(f"rendered {f} in {time.time() - t0:.1f}s", flush=True)
