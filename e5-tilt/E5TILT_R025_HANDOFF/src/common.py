"""Shared helpers for bpy stages (build / verify_scene / render / import). Blender 4.5 LTS LOCK."""
import os, sys, json
import bpy
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LOCK = (4, 5)                      # LOCKS.md SPEC.blender
assert bpy.app.version[:2] == LOCK, f"Blender {bpy.app.version_string} != LOCK {LOCK}"
V5 = bpy.app.version >= (5, 0, 0)
EEVEE_ID = 'BLENDER_EEVEE' if V5 else 'BLENDER_EEVEE_NEXT'
SKY_SINGLE = 'SINGLE_SCATTERING' if V5 else 'NISHITA'
SKY_DUST = 'aerosol_density' if V5 else 'dust_density'


def argv():
    """script args after '--'. Inside the Blender app without '--' there are none."""
    a = sys.argv
    if '--' in a:
        return a[a.index('--') + 1:]
    if os.path.basename(a[0]).lower().startswith('blender'):
        return []
    return a[1:]


def load_cfg(path=None):
    return json.load(open(path or os.path.join(HERE, 'rig_config.json'), encoding='utf-8'))


def load_cams(path=None):
    return json.load(open(path or os.path.join(HERE, 'cameras.json'), encoding='utf-8'))


def _channelbag(act, slot):
    from bpy_extras import anim_utils
    if hasattr(anim_utils, 'action_ensure_channelbag_for_slot'):            # 5.0+
        return anim_utils.action_ensure_channelbag_for_slot(act, slot)
    layer = act.layers[0] if len(act.layers) else act.layers.new("Layer")   # 4.4 / 4.5
    strip = layer.strips[0] if len(layer.strips) else layer.strips.new(type='KEYFRAME')
    return strip.channelbag(slot, ensure=True)


def bake_fcurves(idb, frames, chans, interp_const=False):
    """idb: any ID (Object, Camera, Key...). chans: {'location': (n,3), '["xray"]': (n,), ...}. LINEAR keys."""
    frames = np.asarray(frames, float); n = len(frames)
    ad = idb.animation_data_create()
    act = bpy.data.actions.new(idb.name + '_act')
    slot = act.slots.new(id_type=idb.id_type, name=idb.name)
    ad.action = act
    ad.action_slot = slot                      # never rely on auto assignment (black-frame trap)
    cb = _channelbag(act, slot)
    for path, arr in chans.items():
        arr = np.asarray(arr, float).reshape(n, -1)
        for i in range(arr.shape[1]):
            fc = cb.fcurves.new(path, index=i if arr.shape[1] > 1 else 0)
            fc.keyframe_points.add(n)
            co = np.empty(2 * n); co[0::2] = frames; co[1::2] = arr[:, i]
            fc.keyframe_points.foreach_set('co', co.tolist())
            fc.keyframe_points.foreach_set('interpolation', [0 if interp_const else 1] * n)
            fc.update()
    return act


def world_bvh(ob, dg):
    from mathutils.bvhtree import BVHTree
    eo = ob.evaluated_get(dg); me = eo.to_mesh(); me.calc_loop_triangles()
    v = np.empty(len(me.vertices) * 3); me.vertices.foreach_get('co', v); v = v.reshape(-1, 3)
    M = np.array(eo.matrix_world); w = v @ M[:3, :3].T + M[:3, 3]
    t = np.empty(len(me.loop_triangles) * 3, dtype=np.int32)
    me.loop_triangles.foreach_get('vertices', t)
    tree = BVHTree.FromPolygons(w.tolist(), t.reshape(-1, 3).tolist())
    eo.to_mesh_clear()
    return tree
