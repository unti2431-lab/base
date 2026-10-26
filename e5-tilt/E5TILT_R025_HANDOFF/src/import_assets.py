"""Swap proxies for purchased / hand-built assets without touching the rig.

Asset map (see ASSET_MAP.TEMPLATE.json): each entry binds one asset object to one rig object.
  {"slot": "BODY_01", "file": "assets/e5_lead.blend", "object": "E5_Car1", "kind": "blend",
   "matrix": [16 floats, asset->rig local], "hide_proxy": true, "collide_with": ["SPRING_?_TOP", "FRAME"]}
- kind 'blend' is appended with bpy.data.libraries.load (no ops). kind 'glb'/'fbx' uses the import operator (ops exception).
- The asset is parented to the slot with the given local matrix, so all motion still comes from tilt_bake.npz.
- collide_with globs are written to <out>_pairs.json for verify_scene --extra_pairs.

Smoke test (no real assets needed):  python import_assets.py -- --smoke --out /tmp/smoke.blend
  builds fake cube assets: one clean, one deliberately placed inside FRAME (verify_scene must FAIL).
"""
import os, sys, json, argparse
import bpy, bmesh
from mathutils import Matrix
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import HERE, argv

ap = argparse.ArgumentParser()
ap.add_argument('--blend', default=os.path.join(HERE, '..', 'work', 'e5tilt_R025_proxy.blend'))
ap.add_argument('--map', default=os.path.join(HERE, 'ASSET_MAP.json'))
ap.add_argument('--out', default=os.path.join(HERE, '..', 'work', 'e5tilt_R025_assets.blend'))
ap.add_argument('--smoke', action='store_true')
A = ap.parse_args(argv())
bpy.ops.wm.open_mainfile(filepath=os.path.abspath(A.blend))            # ops exception: open


def fake_asset_lib(path):
    """write a tiny .blend with two cube 'assets' using bpy.data only"""
    for nm, size in (('FAKE_CLEAN', 0.10), ('FAKE_COLLIDE', 0.20)):
        bm = bmesh.new(); bmesh.ops.create_cube(bm, size=size)
        me = bpy.data.meshes.new(nm); bm.to_mesh(me); bm.free()
        ob = bpy.data.objects.new(nm, me)
    objs = {bpy.data.objects[n] for n in ('FAKE_CLEAN', 'FAKE_COLLIDE')}
    bpy.data.libraries.write(path, objs, fake_user=True)
    for o in objs:
        me = o.data; bpy.data.objects.remove(o); bpy.data.meshes.remove(me)


if A.smoke:
    lib = os.path.splitext(A.out)[0] + '_fakelib.blend'
    fake_asset_lib(lib)
    amap = [
        {"slot": "BODY_01", "file": lib, "object": "FAKE_CLEAN", "kind": "blend",
         "matrix": [1, 0, 0, 0, 0, 1, 0, 2.0, 0, 0, 1, 1.5, 0, 0, 0, 1], "hide_proxy": False, "collide_with": ["BODY_01"]},
        {"slot": "BOGIE_01_R", "file": lib, "object": "FAKE_COLLIDE", "kind": "blend",
         "matrix": [1, 0, 0, 1.0, 0, 1, 0, 0.0, 0, 0, 1, 0.62, 0, 0, 0, 1], "hide_proxy": False, "collide_with": ["FRAME"]},
    ]
else:
    amap = json.load(open(A.map, encoding='utf-8'))['assets']

pairs = []
for e in amap:
    slot = bpy.data.objects[e['slot']]
    if e['kind'] == 'blend':
        with bpy.data.libraries.load(e['file'], link=False) as (src, dst):
            dst.objects = [e['object']]
        ob = dst.objects[0]
        bpy.data.collections['TRAIN'].objects.link(ob)
    else:
        before = set(bpy.data.objects)
        if e['kind'] == 'glb':
            bpy.ops.import_scene.gltf(filepath=e['file'])                 # ops exception: asset import
        elif e['kind'] == 'fbx':
            bpy.ops.import_scene.fbx(filepath=e['file'])                  # ops exception: asset import
        new = [o for o in bpy.data.objects if o not in before and o.name.startswith(e['object'])]
        ob = new[0]
    name = f"ASSET_{e['slot']}_{e['object']}"
    ob.name = name
    ob.parent = slot
    ob.matrix_parent_inverse = Matrix.Identity(4)
    ob.matrix_basis = Matrix([e['matrix'][0:4], e['matrix'][4:8], e['matrix'][8:12], e['matrix'][12:16]])
    if e.get('hide_proxy'):
        slot.hide_render = True if slot.type == 'MESH' else slot.hide_render
        for ch in slot.children:
            if not ch.name.startswith('ASSET_') and ch.type == 'MESH' and e.get('hide_proxy_children', False):
                ch.hide_render = True
    for g in e.get('collide_with', []):
        pairs.append([name, g])
    print('imported', name, '->', e['slot'])

json.dump(pairs, open(os.path.splitext(A.out)[0] + '_pairs.json', 'w'), indent=1)
if A.smoke:
    json.dump(pairs, open(os.path.join(os.path.dirname(A.out), 'smoke_pairs.json'), 'w'), indent=1)
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(A.out))            # ops exception: save
print('IMPORT OK', A.out)
