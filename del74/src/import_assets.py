"""에셋 통합 (G-ASSET-1). asset_map.json이 지정한 FBX/OBJ/BLEND 부품을 불러와 프록시 자리에 놓고 프록시를 숨긴다.
실행: blender -b ../render/del74_scene.blend -P import_assets.py -- --map ../assets/asset_map.json --out ../render/del74_scene_assets.blend
스모크 테스트: --fake 를 주면 큐브 몇 개로 매핑 경로를 검증한다(일부러 충돌시켜 verify_scene이 FAIL을 내는지 확인)."""
import bpy, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd(); ROOT = os.path.dirname(HERE)   # exec() 호출 호환
argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
mp = argv[argv.index('--map') + 1] if '--map' in argv else os.path.join(ROOT, 'assets', 'asset_map.json')
out = argv[argv.index('--out') + 1] if '--out' in argv else os.path.join(ROOT, 'render', 'del74_scene_assets.blend')
fake = '--fake' in argv
LOCK = (4, 5); assert bpy.app.version[:2] == LOCK
amap = json.load(open(mp, encoding='utf-8'))
added = []
for entry in amap['parts']:
    proxy = bpy.data.objects.get(entry['replaces'])
    parent = bpy.data.objects.get(entry.get('parent', 'LOCO'))
    if fake:
        me = bpy.data.meshes.new(entry['name']); import bmesh; bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0); bm.to_mesh(me); bm.free()
        obs = [bpy.data.objects.new(entry['name'], me)]; bpy.context.scene.collection.objects.link(obs[0])
    else:
        path = os.path.join(ROOT, 'assets', entry['file']); ext = os.path.splitext(path)[1].lower()
        before = set(bpy.data.objects)
        if ext == '.fbx': bpy.ops.import_scene.fbx(filepath=path)          # bpy.ops 허용 예외: 에셋 임포트
        elif ext == '.obj': bpy.ops.wm.obj_import(filepath=path)
        elif ext == '.blend':
            with bpy.data.libraries.load(path, link=False) as (src, dst): dst.objects = [n for n in src.objects if n in entry.get('objects', src.objects)]
            for ob in dst.objects: bpy.context.scene.collection.objects.link(ob)
        obs = [o for o in bpy.data.objects if o not in before]
    for ob in obs:
        ob.parent = parent; ob.location = entry.get('location', [0, 0, 0]); ob.rotation_euler = entry.get('rotation_deg', [0, 0, 0]); ob.scale = [entry.get('scale', 1.0)] * 3
        ob.rotation_euler = [__import__('math').radians(x) for x in ob.rotation_euler]
        ob.pass_index = proxy.pass_index if proxy else 0
        if proxy and proxy.data.materials and not ob.data.materials: ob.data.materials.append(proxy.data.materials[0])
        added.append(ob.name)
    if proxy: proxy.hide_render = True; proxy.hide_viewport = True
# 충돌 쌍 자동 추가
pairs_path = os.path.join(HERE, 'collision_pairs.json'); pairs = json.load(open(pairs_path, encoding='utf-8'))
for entry in amap['parts']:
    for other in entry.get('collide_with', []): pairs['pairs'].append([entry['name'], other])
json.dump(pairs, open(pairs_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
bpy.ops.wm.save_as_mainfile(filepath=out)   # 허용 예외: 저장
print('ASSETS', added, 'SAVED', out)
