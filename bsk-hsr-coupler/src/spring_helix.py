"""L07 helical spring for the test rigs (bpy 4.5). Imported by build_*.py.

make_spring(name, lengths_per_frame, frames, wire_r, coil_r, n_coils) -> mesh object whose +y axis is the spring axis,
origin at the anchor end. Wire radius is constant in every frame: each frame is an absolute shape key with the helix
re-solved for that length (pitch changes, tube cross-section stays circular and perpendicular to the local tangent).
CONCEPT: no stiffness claim; n_coils and radii are proportions only.
"""
import math
import numpy as np
import bpy

def _helix_verts(L, wire_r, coil_r, n_coils, n_t, n_ring):
    """vertices (n_t*n_ring, 3): tube around a helix of axial length L along +y."""
    t = np.linspace(0.0, 2 * math.pi * n_coils, n_t)
    cx, cy, cz = coil_r * np.cos(t), L * t / (2 * math.pi * n_coils), coil_r * np.sin(t)
    # tangent, then an orthonormal frame (n1 = radial outward, n2 = tangent x n1)
    tx, ty, tz = -coil_r * np.sin(t), np.full_like(t, L / (2 * math.pi * n_coils)), coil_r * np.cos(t)
    tn = np.sqrt(tx * tx + ty * ty + tz * tz); tx, ty, tz = tx / tn, ty / tn, tz / tn
    n1 = np.stack([np.cos(t), np.zeros_like(t), np.sin(t)], 1)            # radial (perpendicular to tangent by construction)
    T = np.stack([tx, ty, tz], 1); n2 = np.cross(T, n1); n2 /= np.linalg.norm(n2, axis=1)[:, None]
    ang = np.linspace(0.0, 2 * math.pi, n_ring, endpoint=False)
    C = np.stack([cx, cy, cz], 1)
    V = C[:, None, :] + wire_r * (np.cos(ang)[None, :, None] * n1[:, None, :] + np.sin(ang)[None, :, None] * n2[:, None, :])
    return V.reshape(-1, 3)

def make_spring(name, lengths, frames, wire_r=0.006, coil_r=0.018, n_coils=9, n_t=None, n_ring=8, mat=None):
    n_t = n_t or int(n_coils * 16) + 1
    L0 = float(np.max(lengths))
    V0 = _helix_verts(L0, wire_r, coil_r, n_coils, n_t, n_ring)
    faces = []
    for i in range(n_t - 1):
        for j in range(n_ring):
            a, b = i * n_ring + j, i * n_ring + (j + 1) % n_ring
            faces.append((a, b, b + n_ring, a + n_ring))
    me = bpy.data.meshes.new(name); me.from_pydata(V0.tolist(), [], faces); me.update()
    for p in me.polygons: p.use_smooth = True
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    if mat is not None: me.materials.append(mat)
    # absolute shape keys: one per frame, eval_time keyed so the mesh follows the baked length exactly
    ob.shape_key_add(name="Basis", from_mix=False)
    sk = me.shape_keys; sk.use_relative = False
    for k, L in enumerate(lengths):
        key = ob.shape_key_add(name=f"L_{k:04d}", from_mix=False)
        key.data.foreach_set("co", _helix_verts(float(L), wire_r, coil_r, n_coils, n_t, n_ring).ravel().tolist())
    # absolute keys: Blender spaces them 10 apart on eval_time (Basis = 0, key k = 10*(k+1))
    sk.animation_data_create(); act = bpy.data.actions.new(name + "_sk_act")
    slot = act.slots.new(id_type='KEY', name=name); sk.animation_data.action = act; sk.animation_data.action_slot = slot
    from bpy_extras import anim_utils
    if hasattr(anim_utils, 'action_ensure_channelbag_for_slot'): cb = anim_utils.action_ensure_channelbag_for_slot(act, slot)
    else:
        layer = act.layers[0] if len(act.layers) else act.layers.new("Layer")
        strip = layer.strips[0] if len(layer.strips) else layer.strips.new(type='KEYFRAME'); cb = strip.channelbag(slot, ensure=True)
    fc = cb.fcurves.new("eval_time", index=0); n = len(frames); fc.keyframe_points.add(n)
    co = np.empty(2 * n); co[0::2] = np.asarray(frames, float); co[1::2] = [10.0 * (k + 1) for k in range(n)]   # measured in bpy 4.5.14: Basis sits at 0, key k at 10*(k+1)
    fc.keyframe_points.foreach_set('co', co.tolist()); fc.keyframe_points.foreach_set('interpolation', [0] * n)   # CONSTANT: exact key per frame
    fc.update()
    return ob
