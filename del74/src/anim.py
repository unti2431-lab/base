"""채널백 API 베이크 (Blender 4.5 LTS / 5.2 LTS 공용, 스킬 §5). 슬롯 명시."""
import bpy, numpy as np

def _channelbag(act, slot):
    from bpy_extras import anim_utils
    if hasattr(anim_utils, 'action_ensure_channelbag_for_slot'):
        return anim_utils.action_ensure_channelbag_for_slot(act, slot)
    layer = act.layers[0] if len(act.layers) else act.layers.new("Layer")
    strip = layer.strips[0] if len(layer.strips) else layer.strips.new(type='KEYFRAME')
    return strip.channelbag(slot, ensure=True)

def bake_fcurves(ob, frames, chans, interp='LINEAR'):
    """chans: {'location': (n,3), 'rotation_euler': (n,3), 'scale': (n,3), 'hide_render': (n,)} 보간 LINEAR 또는 CONSTANT"""
    frames = np.asarray(frames, float); n = len(frames)
    ad = ob.animation_data_create()
    act = ob.animation_data.action or bpy.data.actions.new(ob.name + '_act')
    if ob.animation_data.action is None:
        slot = act.slots.new(id_type=ob.id_type, name=ob.name)
        ad.action = act; ad.action_slot = slot
    slot = ad.action_slot
    cb = _channelbag(act, slot)
    code = 1 if interp == 'LINEAR' else 0
    for path, arr in chans.items():
        arr = np.asarray(arr, float).reshape(n, -1)
        for i in range(arr.shape[1]):
            idx = i if arr.shape[1] > 1 else -1
            fc = cb.fcurves.find(path, index=max(idx, 0)) if idx >= 0 else cb.fcurves.find(path)
            if fc is None:
                fc = cb.fcurves.new(path, index=max(idx, 0)) if idx >= 0 else cb.fcurves.new(path)
            elif len(fc.keyframe_points):
                fc.keyframe_points.clear()          # 같은 채널 재베이크 = 교체(누적 금지)
            fc.keyframe_points.add(n)
            co = np.empty(2 * n); co[0::2] = frames; co[1::2] = arr[:, i]
            fc.keyframe_points.foreach_set('co', co.tolist())
            fc.keyframe_points.foreach_set('interpolation', [code] * n)
            fc.update()
    return act

def bake_node_value(node_socket_owner_mat, node_name, frames, values):
    """재질 노드 Value 출력 베이크 (node_tree 액션)."""
    nt = node_socket_owner_mat.node_tree
    node = nt.nodes[node_name]
    ad = nt.animation_data_create()
    act = nt.animation_data.action or bpy.data.actions.new(node_socket_owner_mat.name + '_nt_act')
    if nt.animation_data.action is None:
        slot = act.slots.new(id_type='NODETREE', name=node_name); ad.action = act; ad.action_slot = slot
    cb = _channelbag(act, ad.action_slot)
    path = f'nodes["{node_name}"].outputs[0].default_value'
    fc = cb.fcurves.find(path) or cb.fcurves.new(path)
    n = len(frames); fc.keyframe_points.add(n)
    co = np.empty(2 * n); co[0::2] = frames; co[1::2] = values
    fc.keyframe_points.foreach_set('co', co.tolist()); fc.keyframe_points.foreach_set('interpolation', [1] * n); fc.update()

def continuous_euler(eulers):
    """프레임 간 ±π 점프 제거"""
    e = np.asarray(eulers, float).copy()
    for i in range(1, len(e)):
        d = e[i] - e[i - 1]
        e[i] -= 2 * np.pi * np.round(d / (2 * np.pi))
    return e
