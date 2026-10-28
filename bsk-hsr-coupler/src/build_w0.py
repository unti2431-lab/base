#!/usr/bin/env python3
"""L08 W0 loop blocking (bpy 4.5 LTS). Proxy E5+E6 coupled noses (covers open), running, camera Z-axis entry and return.

usage:  python build_w0.py [--render START END --preset animatic --out DIR] [--gpu] [--workbench]
Shown frames: shot01 F1-50 (low-angle follow), shot02 F51-120 (Z-axis entry into the coupler gap),
              shot13 F1186-1260 (return). Virtual F1261 must equal F1 (pose, velocity, FOV, env phase).
F121-F1185 belong to the mechanism scenes; this file only keys guard frames 121 and 1185 for motion blur.
No bpy.ops except save/render. No markings, no text, no emissive arrows in the scene.
"""
import sys, os, json, math, argparse
import numpy as np
import bpy, bmesh
from mathutils import Vector, Matrix, Quaternion

LOCK = (4, 5)
assert bpy.app.version[:2] == LOCK, f"Blender {bpy.app.version_string} != LOCK {LOCK}"
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
CFG = json.load(open(os.path.join(HERE, "rig_config.json"), encoding="utf-8")); W = CFG["w0_loop"]
G = {k: v["value"] for k, v in W["geometry"].items()}; C = {k: (v["value"] if isinstance(v, dict) else v) for k, v in W["camera"].items()}
SP = {k: v["value"] for k, v in W["speed"].items()}
SEAM = W["frames"]["virtual_seam_F"]                    # 1261
SEG_A = (1, 50); SEG_B = (50, 120); SEG_C = (1186, SEAM)
KEY_FRAMES = list(range(1, 122)) + list(range(1185, SEAM + 1))   # 121 / 1185 = motion-blur guards

# ---------------- motion (pure functions, also used by verify_w0.py through the baked keys only) ----------------
P0, T0 = np.array(C["P0"]), np.array(C["T0"]); V0, VT0 = np.array(C["v0_per_frame"]), np.array(C["vt0_per_frame"])
P_IN, T_IN = np.array(C["P_in"]), np.array(C["T_in"])

def quintic(p0, v0, a0, p1, v1, a1, f0, f1, f):
    """quintic Hermite in frame units: position, velocity (per frame), acceleration (per frame^2) at both ends."""
    D = f1 - f0; u = (f - f0) / D
    m0, m1, c0, c1 = v0 * D, v1 * D, a0 * D * D, a1 * D * D
    h0 = 1 - 10*u**3 + 15*u**4 - 6*u**5; h1 = u - 6*u**3 + 8*u**4 - 3*u**5; h2 = 0.5*u**2 - 1.5*u**3 + 1.5*u**4 - 0.5*u**5
    h3 = 0.5*u**3 - u**4 + 0.5*u**5;    h4 = -4*u**3 + 7*u**4 - 3*u**5;     h5 = 10*u**3 - 15*u**4 + 6*u**5
    return h0*p0 + h1*m0 + h2*c0 + h3*c1 + h4*m1 + h5*p1

z3 = np.zeros(3)
dolly = (P_IN - (P0 + V0 * (SEG_A[1] - 1))); dolly_dir = dolly / np.linalg.norm(dolly)
V_IN = dolly_dir * C["entry_end_speed"]

def cam_pos(f):
    if f <= SEG_A[1]: return P0 + V0 * (f - 1)
    if f <= SEG_B[1] + 1: return quintic(P0 + V0 * (SEG_A[1] - 1), V0, z3, P_IN, V_IN, z3, SEG_B[0], SEG_B[1], f)
    if f >= SEG_C[0] - 1: return quintic(P_IN, -V_IN, z3, P0, V0, z3, SEG_C[0], SEG_C[1], f)
    raise ValueError(f)

def cam_tgt(f):
    if f <= SEG_A[1]: return T0 + VT0 * (f - 1)
    if f <= SEG_B[1] + 1: return quintic(T0 + VT0 * (SEG_A[1] - 1), VT0, z3, T_IN, z3, z3, SEG_B[0], SEG_B[1], f)
    if f >= SEG_C[0] - 1: return quintic(T_IN, z3, z3, T0, VT0, z3, SEG_C[0], SEG_C[1], f)
    raise ValueError(f)

def look_quat(p, t):
    d = Vector(t) - Vector(p); return d.to_track_quat('-Z', 'Y')

def env_offset(f):
    """world shift of the scrolling environment (train runs toward +y, the world slides toward -y). Periodic: offset(1261) == offset(1)."""
    ff = f if f <= 600 else f - (SEAM - 1)       # second visible block counted back from the seam -> F1261 maps to F1
    return -SP["env_speed_m_per_frame"] * (ff - 1)

R_W = SP["wheel_radius"]; TOTAL = SP["env_speed_m_per_frame"] * (SEAM - 1)
N_TURN = round(TOTAL / R_W / (2 * math.pi / 6)); OMEGA = N_TURN * (2 * math.pi / 6) / (SEAM - 1)   # 6-fold marker repeats exactly
def wheel_angle(f):
    ff = f if f <= 600 else f - (SEAM - 1)
    return -OMEGA * (ff - 1)

# ---------------- helpers (same conventions as build_schB.py) ----------------
def _channelbag(act, slot):
    from bpy_extras import anim_utils
    if hasattr(anim_utils, 'action_ensure_channelbag_for_slot'): return anim_utils.action_ensure_channelbag_for_slot(act, slot)
    layer = act.layers[0] if len(act.layers) else act.layers.new("Layer")
    strip = layer.strips[0] if len(layer.strips) else layer.strips.new(type='KEYFRAME')
    return strip.channelbag(slot, ensure=True)

def bake_fcurves(idb, frames, chans, id_type=None):
    frames = np.asarray(frames, float); n = len(frames)
    ad = idb.animation_data_create(); act = bpy.data.actions.new(idb.name + '_act')
    slot = act.slots.new(id_type=id_type or idb.id_type, name=idb.name); ad.action = act; ad.action_slot = slot
    cb = _channelbag(act, slot)
    for path, arr in chans.items():
        arr = np.asarray(arr, float).reshape(n, -1)
        for i in range(arr.shape[1]):
            fc = cb.fcurves.new(path, index=i); fc.keyframe_points.add(n)
            co = np.empty(2 * n); co[0::2] = frames; co[1::2] = arr[:, i]
            fc.keyframe_points.foreach_set('co', co.tolist()); fc.keyframe_points.foreach_set('interpolation', [1] * n)
            fc.extrapolation = 'LINEAR'; fc.update()
    return act

def mesh_from_bm(name, bm, smooth=False):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    if smooth:
        for p in me.polygons: p.use_smooth = True
    me.update(); return me

def add_box(bm, sx, sy, sz, c):
    r = bmesh.ops.create_cube(bm, size=1.0); vs = r["verts"]
    bmesh.ops.scale(bm, vec=(sx, sy, sz), verts=vs); bmesh.ops.translate(bm, vec=c, verts=vs); return vs

def box(name, sx, sy, sz, c=(0, 0, 0)):
    bm = bmesh.new(); add_box(bm, sx, sy, sz, c); return mesh_from_bm(name, bm)

def cyl(name, r, h, c=(0, 0, 0), axis='Z', segs=32):
    bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=segs, radius1=r, radius2=r, depth=h)
    if axis == 'Y': bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=Matrix.Rotation(-math.pi / 2, 3, 'X'), verts=bm.verts)
    if axis == 'X': bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=Matrix.Rotation(math.pi / 2, 3, 'Y'), verts=bm.verts)
    bmesh.ops.translate(bm, vec=c, verts=bm.verts); return mesh_from_bm(name, bm, smooth=True)

def mat(name, rgb, rough=0.45, metal=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal
    m.diffuse_color = (*rgb, 1); return m

def new_ob(name, data, m=None, loc=(0, 0, 0), parent=None):
    ob = bpy.data.objects.new(name, data); ob.location = loc
    if m is not None: ob.data.materials.append(m)
    if parent is not None: ob.parent = parent
    bpy.context.scene.collection.objects.link(ob); return ob

def nose_mesh(name, L, Wb, H, sign, w_tip=0.50, z_tip=1.42, body_extra=8.0, nsec=48, nring=40):
    """loft from the nose tip (|y| = tip) to the body. sign=-1 -> E5 (y<0), +1 -> E6 (y>0). Superelliptic sections."""
    zb = G["skirt_z"]; tip = G["nose_tip_y"]; bm = bmesh.new(); rings = []
    ss = [i / (nsec - 1) for i in range(nsec)]
    for s in ss + [None]:
        if s is None: y_abs = tip + L + body_extra; w, zt = Wb / 2, H
        else:
            y_abs = tip + L * s; w = w_tip + (Wb / 2 - w_tip) * (1 - (1 - s) ** 2.4); zt = z_tip + (H - z_tip) * (1 - (1 - s) ** 1.5)
        a, b, zc = w, (zt - zb) / 2, (zt + zb) / 2; ring = []
        for k in range(nring):
            th = 2 * math.pi * k / nring; c, sn = math.cos(th), math.sin(th)
            x = a * math.copysign(abs(c) ** (2 / 3.0), c); z = zc + b * math.copysign(abs(sn) ** (2 / 3.0), sn)
            ring.append(bm.verts.new((x, sign * y_abs, max(z, zb))))
        rings.append(ring)
    for r0, r1 in zip(rings, rings[1:]):
        for k in range(nring):
            q = (r0[k], r0[(k + 1) % nring], r1[(k + 1) % nring], r1[k]); bm.faces.new(q if sign < 0 else q[::-1])
    bm.faces.new(rings[0][::-1] if sign < 0 else rings[0]); bm.faces.new(rings[-1] if sign < 0 else rings[-1][::-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces); return mesh_from_bm(name, bm, smooth=True)

# ---------------- scene ----------------
sc = bpy.context.scene
for ob in list(bpy.data.objects): bpy.data.objects.remove(ob, do_unlink=True)
sc.frame_start, sc.frame_end = 1, 1260; sc.render.fps = 30
M = {"e5": mat("E5_BODY", (0.80, 0.81, 0.80), 0.30), "e6": mat("E6_BODY", (0.70, 0.69, 0.68), 0.30),
     "pocket": mat("POCKET_DARK", (0.03, 0.03, 0.035), 0.7), "cover": mat("COVER", (0.62, 0.63, 0.63), 0.35),
     "steel": mat("COUPLER_STEEL", (0.42, 0.43, 0.45), 0.35, 0.8), "rail": mat("RAIL", (0.30, 0.30, 0.31), 0.3, 0.9),
     "slab": mat("SLAB", (0.46, 0.45, 0.43), 0.85), "slab2": mat("SLAB_ALT", (0.40, 0.395, 0.38), 0.85),
     "ground": mat("GROUND", (0.20, 0.19, 0.17), 0.95), "pole": mat("POLE", (0.36, 0.37, 0.38), 0.5, 0.4),
     "wall": mat("WALL", (0.55, 0.55, 0.53), 0.8), "bogie": mat("BOGIE", (0.10, 0.10, 0.11), 0.6),
     "wheel": mat("WHEEL", (0.33, 0.33, 0.34), 0.35, 0.9), "mark": mat("WHEEL_MARK", (0.75, 0.75, 0.74), 0.4)}
tip = G["nose_tip_y"]; zc = G["coupler_height"]
TRAIN = []
for car, sign, L, Wb in (("E5", -1, G["e5_nose_length"], G["e5_body_width"]), ("E6", +1, G["e6_nose_length"], G["e6_body_width"])):
    k = car.lower(); w_tip = 0.50 if car == "E5" else 0.46
    TRAIN.append(new_ob(f"{car}_NOSE", nose_mesh(f"{car}_NOSE", L, Wb, G["body_height"], sign, w_tip=w_tip, z_tip=1.42 if car == "E5" else 1.50), M[k]))
    TRAIN.append(new_ob(f"{car}_POCKET", box(f"{car}_POCKET", 0.80, 0.30, 0.66, (0, sign * (tip + 0.12), zc - 0.02)), M["pocket"]))
    def half_w(y_abs): s_ = max(0.0, (y_abs - tip) / L); return w_tip + (Wb / 2 - w_tip) * (1 - (1 - s_) ** 2.4)
    for sx in (-1, 1):   # two cover halves (each ~ half the pocket width) swung back flat against the nose skin; open state only (NOSE-01)
        TRAIN.append(new_ob(f"{car}_COVER_{'L' if sx < 0 else 'R'}", box(f"{car}_COVER_{sx}", 0.035, 0.42, 0.70, (sx * (half_w(tip + 0.46) + 0.03), sign * (tip + 0.27), zc - 0.02)), M["cover"]))
    TRAIN.append(new_ob(f"{car}_SHANK", cyl(f"{car}_SHANK", 0.075, tip + 0.10, (0, sign * (0.30 + (tip + 0.10) / 2), zc), 'Y'), M["steel"]))
    TRAIN.append(new_ob(f"{car}_HEAD", box(f"{car}_HEAD", 0.58, 0.30, 0.42, (0, sign * 0.152, zc)), M["steel"]))
    yb = sign * (tip + (12.6 if car == "E5" else 10.6))
    TRAIN.append(new_ob(f"{car}_BOGIE", box(f"{car}_BOGIE", 2.2, 3.6, 0.55, (0, yb, 0.62)), M["bogie"]))
    for ax in (-1.25, 1.25):
        for xs in (-0.7535, 0.7535):
            wo = new_ob(f"{car}_WHEEL_{ax:+.2f}_{xs:+.2f}", cyl("WHEEL", R_W, 0.13, (0, 0, 0), 'X', 48), M["wheel"], loc=(xs, yb + ax, R_W))
            mk = new_ob(wo.name + "_MARK", box("MARK", 0.135, 0.06, R_W * 1.7), M["mark"], parent=wo)   # 2-fold marker bar, 6-fold-safe phase
            TRAIN.append(wo)
# track (static rails: uniform along y) + ground
for xs in (-0.7175, 0.7175): new_ob(f"RAIL_{xs:+.3f}", box("RAIL", 0.07, 700, 0.16, (xs, 0, -0.08)), M["rail"])
new_ob("GROUND", box("GROUND", 60, 700, 0.1, (0, 0, -0.42)), M["ground"])
# scrolling environment, period = env_tile_m; built over y in [-300, 300] (offsets stay within [-67 m, +42 m])
TILE = SP["env_tile_m"]; Y0, Y1 = -300.0, 300.0
bm1, bm2, bmp, bmw = bmesh.new(), bmesh.new(), bmesh.new(), bmesh.new()
i = 0; y = Y0
while y < Y1:
    add_box(bm1 if i % 2 == 0 else bm2, 2.34, 4.92, 0.19, (0, y + 2.5, -0.255)); i += 1; y += 5.0
y = Y0
while y < Y1:
    add_box(bmp, 0.30, 0.30, 7.2, (4.4, y, 3.25)); add_box(bmp, 3.6, 0.12, 0.12, (2.7, y, 6.4)); y += TILE
y = Y0
while y < Y1:
    add_box(bmw, 0.16, 0.16, 2.2, (-5.2, y, 0.75)); y += 2.5
ENV = [new_ob("ENV_SLABS", mesh_from_bm("ENV_SLABS", bm1), M["slab"]), new_ob("ENV_SLABS_ALT", mesh_from_bm("ENV_SLABS_ALT", bm2), M["slab2"]),
       new_ob("ENV_POLES", mesh_from_bm("ENV_POLES", bmp), M["pole"]), new_ob("ENV_WALL_POSTS", mesh_from_bm("ENV_WALL_POSTS", bmw), M["pole"]),
       new_ob("ENV_WALL", box("ENV_WALL", 0.12, 700, 1.9, (-5.32, 0, 0.6)), M["wall"])]

# ---------------- bake animation ----------------
F = np.array(KEY_FRAMES, float)
for ob in ENV:
    bake_fcurves(ob, F, {"location": np.array([[0.0, env_offset(f), 0.0] for f in KEY_FRAMES])})
for ob in TRAIN:
    if "_WHEEL_" in ob.name and not ob.name.endswith("_MARK"):
        x0, y0, z0 = ob.location; ob.rotation_mode = 'XYZ'
        bake_fcurves(ob, F, {"rotation_euler": np.array([[wheel_angle(f), 0.0, 0.0] for f in KEY_FRAMES])})
cam_d = bpy.data.cameras.new("CAM_W0"); cam_d.lens = C["lens_mm"]; cam_d.sensor_fit = 'AUTO'   # 36 mm across the long (vertical) side
cam_d.clip_start = 0.05; cam_d.clip_end = 600
cam = new_ob("CAM_W0", cam_d); cam.rotation_mode = 'QUATERNION'; sc.camera = cam
pos = np.array([cam_pos(f) for f in KEY_FRAMES]); quats = []; prev = None
for f in KEY_FRAMES:
    q = look_quat(cam_pos(f), cam_tgt(f))
    if prev is not None and prev.dot(q) < 0: q.negate()
    quats.append(list(q)); prev = q
bake_fcurves(cam, F, {"location": pos, "rotation_quaternion": np.array(quats)})
bake_fcurves(cam_d, F, {"lens": np.full(len(KEY_FRAMES), C["lens_mm"])}, id_type='CAMERA')   # FOV is keyed so the seam check reads it

# ---------------- light / world / render ----------------
sun_d = bpy.data.lights.new("SUN", 'SUN'); sun_d.energy = 3.5; sun_d.angle = math.radians(3)
sun = new_ob("SUN", sun_d, loc=(10, -10, 20)); sun.rotation_euler = (math.radians(50), math.radians(10), math.radians(-35))
w = bpy.data.worlds.new("W"); w.use_nodes = True; w.node_tree.nodes["Background"].inputs[0].default_value = (0.55, 0.60, 0.66, 1)
w.node_tree.nodes["Background"].inputs[1].default_value = 0.6; sc.world = w
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.render.use_motion_blur = True; sc.render.motion_blur_shutter = 0.5
sc.cycles.use_denoising = True; sc.render.image_settings.file_format = 'PNG'; sc.render.dither_intensity = 1.0

meta = {"seam_F": SEAM, "env_speed_m_per_frame": SP["env_speed_m_per_frame"], "env_tile_m": TILE, "env_total_shift_m": TOTAL,
        "wheel_marker_turns_6fold": N_TURN, "wheel_omega_rad_per_frame": OMEGA, "wheel_effective_radius_m": SP["env_speed_m_per_frame"] / OMEGA,
        "dolly_dir": dolly_dir.tolist(), "keyed_frames": [KEY_FRAMES[0], 121, 1185, KEY_FRAMES[-1]], "grade": "CONCEPT_ONLY proxy blocking"}
os.makedirs(os.path.join(ROOT, "evidence"), exist_ok=True)
json.dump(meta, open(os.path.join(ROOT, "evidence", "w0_build_meta.json"), "w"), indent=2)
for f in (1, 50, 120, 1186, 1260):
    sc.frame_set(f); print(f"F{f}: cam=({cam.location.x:+.3f},{cam.location.y:+.3f},{cam.location.z:+.3f}) env_y={ENV[0].location.y:+.3f}")
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT, "evidence", "W0_BLOCK.blend"))   # bpy.ops allowed: save

ap = argparse.ArgumentParser(); ap.add_argument("--render", nargs=2, type=int); ap.add_argument("--preset", default="animatic"); ap.add_argument("--out", default=None)
ap.add_argument("--gpu", action="store_true"); ap.add_argument("--workbench", action="store_true")
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
args = ap.parse_args(argv)
if args.gpu:
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
    if args.workbench: sc.render.engine = 'BLENDER_WORKBENCH'; sc.display.shading.light = 'STUDIO'; sc.display.shading.color_type = 'MATERIAL'
    else: sc.cycles.samples = R["samples"]; sc.cycles.use_adaptive_sampling = R.get("adaptive", False)
    sc.render.use_motion_blur = R["motion_blur"]; out = args.out or os.path.join(ROOT, "render", f"w0_{args.preset}")
    os.makedirs(out, exist_ok=True); import time
    frames = [f for f in range(args.render[0], args.render[1] + 1) if f <= 120 or f >= 1186]
    for f in frames:
        fp = os.path.join(out, f"{f:04d}.png")
        if os.path.exists(fp): continue
        sc.frame_set(f); sc.render.filepath = fp; t0 = time.time(); bpy.ops.render.render(write_still=True)   # bpy.ops allowed: render
        print(f"rendered {f} in {time.time() - t0:.1f}s", flush=True)
