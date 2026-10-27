"""PAVE 빌드 스크립트 공통 모듈 — 모든 src/build_*.py, verify_*.py 는 이것만 import 한다.

- 버전 가드: src/spec_lock.json 의 blender LOCK 과 실행 중인 bpy 버전이 다르면 즉시 중단.
- 버전 상수: EEVEE_ID, SKY_SINGLE, SKY_DUST (4.5 / 5.x 차이).
- bake_fcurves: 채널백 API + 슬롯 명시 베이크(4.5.14·5.2.2 공통). act.fcurves 직접 사용 금지.
- world_bvh: 월드 좌표 삼각형 BVH(씬 충돌 검사용).
- load_bake / motion_probe: 베이크 npz 로드, 빌드 직후 움직임 확인.
"""
import json, pathlib
import numpy as np
import bpy

SRC = pathlib.Path(__file__).resolve().parent
ROOT = SRC.parent
SPEC = json.loads((SRC / 'spec_lock.json').read_text(encoding='utf-8'))
if not SPEC.get('blender'):
    raise SystemExit('G-PAVE-04 미결: Blender 버전 LOCK 없음. 사용자 결정 후 scripts/setup_env.sh --blender <4.5|5.2>')
LOCK = tuple(int(v) for v in str(SPEC['blender']).split('.')[:2])
assert bpy.app.version[:2] == LOCK, f"Blender {bpy.app.version_string} != LOCK {LOCK}"

V5 = bpy.app.version >= (5, 0, 0)
EEVEE_ID = 'BLENDER_EEVEE' if V5 else 'BLENDER_EEVEE_NEXT'
SKY_SINGLE = 'SINGLE_SCATTERING' if V5 else 'NISHITA'
SKY_DUST = 'aerosol_density' if V5 else 'dust_density'
FPS = int(SPEC['fps'])


def _channelbag(act, slot):
    from bpy_extras import anim_utils
    if hasattr(anim_utils, 'action_ensure_channelbag_for_slot'):            # 5.0+
        return anim_utils.action_ensure_channelbag_for_slot(act, slot)
    layer = act.layers[0] if len(act.layers) else act.layers.new("Layer")   # 4.4 / 4.5
    strip = layer.strips[0] if len(layer.strips) else layer.strips.new(type='KEYFRAME')
    return strip.channelbag(slot, ensure=True)


def bake_fcurves(ob, frames, chans):
    """chans: {'location': (n,3), 'rotation_euler': (n,3), ...}  보간은 LINEAR"""
    frames = np.asarray(frames, float); n = len(frames)
    ad = ob.animation_data_create()
    act = bpy.data.actions.new(ob.name + '_act')
    slot = act.slots.new(id_type=ob.id_type, name=ob.name)
    ad.action = act
    ad.action_slot = slot                      # 자동 할당에 기대지 않는다
    cb = _channelbag(act, slot)
    for path, arr in chans.items():
        arr = np.asarray(arr, float).reshape(n, -1)
        for i in range(arr.shape[1]):
            fc = cb.fcurves.new(path, index=i); fc.keyframe_points.add(n)
            co = np.empty(2 * n); co[0::2] = frames; co[1::2] = arr[:, i]
            fc.keyframe_points.foreach_set('co', co.tolist())
            fc.keyframe_points.foreach_set('interpolation', [1] * n)   # LINEAR
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
    eo.to_mesh_clear()                          # 수천 프레임 반복 시 메모리 누적 방지
    return tree


def load_bake(variant):
    """variant: 'A_real' | 'B_noRev' | 'AB_fill'. 키: x, h(F,x), coarse, theta_l, theta_r (F = 0..frames+1)."""
    return np.load(SRC / 'bake' / f'pave_{variant}_bake.npz')


def motion_probe(names, frames=(1, 2)):
    """빌드 직후 호출: 오브젝트 위치·회전이 프레임 사이에 실제로 바뀌는지 출력하고 반환."""
    sc = bpy.context.scene; out = {}
    for F in frames:
        sc.frame_set(F)
        for nm in names:
            ob = bpy.data.objects[nm]
            out.setdefault(nm, []).append((tuple(round(c, 5) for c in ob.matrix_world.translation),
                                           tuple(round(c, 5) for c in ob.matrix_world.to_euler())))
    for nm, v in out.items():
        print(f'[motion_probe] {nm}: {"MOVES" if v[0] != v[-1] else "STATIC"} {v}')
    return out
