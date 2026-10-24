"""
SKIRT01 — 애니메이션 베이크 헬퍼

이 파일은 수정 금지(LOCKS.md RIG). 호출만 한다.

왜 이 파일이 따로 있는가:
  - Blender 4.4+에서 액션 슬롯을 지정하지 않으면 아무것도 움직이지 않고
    카메라가 원점에 남아 "렌더가 새까맣고 10분 넘게 걸리는" 증상이 난다.
  - 5.0에서 레거시 action.fcurves API가 제거되어 AttributeError가 난다.
  아래 구현은 4.5.14와 5.2.2 양쪽에서 실측 통과한 형태다.
"""

import bpy
import numpy as np

# ── 버전 가드 ────────────────────────────────────────────────
# LOCKS.md SPEC.blender 와 일치시킨다. LOCK 밖 버전이면 즉시 중단.
LOCK = (4, 5)
assert bpy.app.version[:2] == LOCK, \
    f"Blender {bpy.app.version_string} != LOCK {LOCK}"

V5 = bpy.app.version >= (5, 0, 0)
EEVEE_ID   = 'BLENDER_EEVEE' if V5 else 'BLENDER_EEVEE_NEXT'
SKY_SINGLE = 'SINGLE_SCATTERING' if V5 else 'NISHITA'
SKY_DUST   = 'aerosol_density' if V5 else 'dust_density'
# 하늘 노드는 위 상수로 만든다. 문자열을 코드에 직접 박지 않는다.


def _channelbag(act, slot):
    from bpy_extras import anim_utils
    if hasattr(anim_utils, 'action_ensure_channelbag_for_slot'):            # 5.0+
        return anim_utils.action_ensure_channelbag_for_slot(act, slot)
    layer = act.layers[0] if len(act.layers) else act.layers.new("Layer")   # 4.4 / 4.5
    strip = layer.strips[0] if len(layer.strips) else layer.strips.new(type='KEYFRAME')
    return strip.channelbag(slot, ensure=True)


def bake_fcurves(ob, frames, chans):
    """chans: {'location': (n,3), 'rotation_euler': (n,3), ...}  보간은 LINEAR"""
    frames = np.asarray(frames, float)
    n = len(frames)
    ad = ob.animation_data_create()
    act = bpy.data.actions.new(ob.name + '_act')
    slot = act.slots.new(id_type=ob.id_type, name=ob.name)
    ad.action = act
    ad.action_slot = slot                      # 자동 할당에 기대지 않는다
    cb = _channelbag(act, slot)
    for path, arr in chans.items():
        arr = np.asarray(arr, float).reshape(n, -1)
        for i in range(arr.shape[1]):
            fc = cb.fcurves.new(path, index=i)
            fc.keyframe_points.add(n)
            co = np.empty(2 * n)
            co[0::2] = frames
            co[1::2] = arr[:, i]
            fc.keyframe_points.foreach_set('co', co.tolist())
            fc.keyframe_points.foreach_set('interpolation', [1] * n)   # LINEAR
            fc.update()
    return act


def world_bvh(ob, dg):
    """월드 좌표 삼각형 BVH. 프리뷰에서 안 보이는 관통을 잡는다."""
    from mathutils.bvhtree import BVHTree
    eo = ob.evaluated_get(dg)
    me = eo.to_mesh()
    me.calc_loop_triangles()
    v = np.empty(len(me.vertices) * 3)
    me.vertices.foreach_get('co', v)
    v = v.reshape(-1, 3)
    M = np.array(eo.matrix_world)
    w = v @ M[:3, :3].T + M[:3, 3]
    t = np.empty(len(me.loop_triangles) * 3, dtype=np.int32)
    me.loop_triangles.foreach_get('vertices', t)
    tree = BVHTree.FromPolygons(w.tolist(), t.reshape(-1, 3).tolist())
    eo.to_mesh_clear()          # 수천 프레임 반복 시 메모리 누적 방지
    return tree


def verify_moving(objs, frames=(1, 2)):
    """빌드 직후 호출. 실제로 움직이는지 2프레임만 찍어 확인한다.
    검은 화면 함정을 1분 안에 걸러낸다."""
    scn = bpy.context.scene
    out = {}
    for f in frames:
        scn.frame_set(f)
        out[f] = {o.name: tuple(round(c, 6) for c in o.matrix_world.translation)
                  for o in objs}
    for name in out[frames[0]]:
        if out[frames[0]][name] == out[frames[1]][name]:
            print(f"[WARN] {name} 가 프레임 {frames} 사이에 움직이지 않음")
    return out
