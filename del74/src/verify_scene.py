"""씬 충돌 검사 (월드 좌표 삼각형 BVH, 스킬 §10.2). 실행: blender -b ../render/del74_scene.blend -P verify_scene.py -- [--step 5] [--pairs collision_pairs.json]
결과 ../evidence/scene_qc.json. 설계 접촉(≤1mm 구름)은 결함이 아니라 목록으로 기록."""
import bpy, json, os, sys, time
import numpy as np
from mathutils.bvhtree import BVHTree
HERE = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd(); ROOT = os.path.dirname(HERE)   # exec() 호출 호환
argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
step = int(argv[argv.index('--step') + 1]) if '--step' in argv else 5
pairs_file = argv[argv.index('--pairs') + 1] if '--pairs' in argv else os.path.join(HERE, 'collision_pairs.json')
LOCK = (4, 5); assert bpy.app.version[:2] == LOCK
scn = bpy.context.scene
cfg = json.load(open(os.path.join(HERE, 'rig_config.json'), encoding='utf-8'))

def world_bvh(ob, dg):
    eo = ob.evaluated_get(dg); me = eo.to_mesh()
    if me is None or len(me.polygons) == 0: return None
    me.calc_loop_triangles()
    v = np.empty(len(me.vertices) * 3); me.vertices.foreach_get('co', v); v = v.reshape(-1, 3)
    M = np.array(eo.matrix_world); w = v @ M[:3, :3].T + M[:3, 3]
    t = np.empty(len(me.loop_triangles) * 3, dtype=np.int32); me.loop_triangles.foreach_get('vertices', t)
    tree = BVHTree.FromPolygons(w.tolist(), t.reshape(-1, 3).tolist())
    eo.to_mesh_clear(); return tree

def instanced_world_bvh(proto_ob, inst_empty, dg):
    """컬렉션 인스턴스 안의 프로토타입: 인스턴서 행렬을 곱한다."""
    eo = proto_ob.evaluated_get(dg); me = eo.to_mesh()
    if me is None or len(me.polygons) == 0: return None
    me.calc_loop_triangles()
    v = np.empty(len(me.vertices) * 3); me.vertices.foreach_get('co', v); v = v.reshape(-1, 3)
    M = np.array(inst_empty.evaluated_get(dg).matrix_world @ eo.matrix_world); w = v @ M[:3, :3].T + M[:3, 3]
    t = np.empty(len(me.loop_triangles) * 3, dtype=np.int32); me.loop_triangles.foreach_get('vertices', t)
    tree = BVHTree.FromPolygons(w.tolist(), t.reshape(-1, 3).tolist()); eo.to_mesh_clear(); return tree

pairs = json.load(open(pairs_file, encoding='utf-8'))['pairs'] if os.path.exists(pairs_file) else []
frames = list(range(1, cfg['total_frames'] + 1, step))
results = {'step': step, 'pairs': len(pairs), 'frames_checked': len(frames), 'collisions': [], 'design_contacts': [], 'camera_min_surface_dist': None}
cam = scn.camera; cam_min = 1e9; cam_min_at = None; t0 = time.time()
for F in frames:
    scn.frame_set(F); dg = bpy.context.evaluated_depsgraph_get()
    trees = {}
    def tree_of(spec):
        key = json.dumps(spec)
        if key not in trees:
            if isinstance(spec, dict):
                trees[key] = instanced_world_bvh(bpy.data.objects[spec['proto']], bpy.data.objects[spec['instancer']], dg)
            else:
                ob = bpy.data.objects[spec]
                trees[key] = None if ob.hide_render else world_bvh(ob, dg)
        return trees[key]
    for a, b in pairs:
        ta, tb = tree_of(a), tree_of(b)
        if ta is None or tb is None: continue
        ov = ta.overlap(tb)
        if ov:
            results['collisions'].append({'F': F, 'a': a, 'b': b, 'n_tri_pairs': len(ov)})
    # 카메라 최근접 표면 거리 (주요 메시만)
    cp = cam.matrix_world.translation
    for name in ['BODY_HOOD', 'BODY_CAB', 'BODY_NOSE', 'DECK', 'ENGINE_BLOCK', 'GEN_CASE', 'GROUND', 'CAR_01_BODY']:
        ob = bpy.data.objects.get(name)
        if ob is None or ob.hide_render: continue
        tr = tree_of(name)
        if tr is None: continue
        hit = tr.find_nearest(cp)
        if hit[0] is not None and hit[3] < cam_min: cam_min, cam_min_at = hit[3], {'F': F, 'object': name}
results['camera_min_surface_dist'] = round(float(cam_min), 4); results['camera_min_at'] = cam_min_at
results['PASS'] = {'collisions_zero': len(results['collisions']) == 0, 'camera_clearance_ge_0.15': cam_min >= 0.15}
results['ALL'] = 'PASS' if all(results['PASS'].values()) else 'FAIL'
results['sec'] = round(time.time() - t0, 1)
json.dump(results, open(os.path.join(ROOT, 'evidence', 'scene_qc.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps({k: results[k] for k in ['ALL', 'PASS', 'frames_checked', 'camera_min_surface_dist', 'camera_min_at', 'sec']}, ensure_ascii=False))
print('collisions', len(results['collisions']), results['collisions'][:10])
sys.exit(0 if results['ALL'] == 'PASS' else 1)
