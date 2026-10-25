"""bmesh 프리미티브 (bpy.ops 미사용). 모든 메시는 베벨을 굽고 30° 초과 모서리만 sharp."""
import bpy, bmesh, math
import numpy as np
from mathutils import Vector, Matrix

def _finish(bm, name, bevel=0.0, segments=2, center=(0, 0, 0)):
    """메시는 로컬 원점 중심으로 만들고 오브젝트 location=center. 회전 부품의 원점이 곧 회전축이 된다."""
    if bevel > 0:
        geom = [e for e in bm.edges]
        bmesh.ops.bevel(bm, geom=geom, offset=bevel, segments=segments, affect='EDGES', profile=0.7)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = True
    me.update()
    # 30° 초과 모서리 sharp
    me.calc_normals_split() if hasattr(me, 'calc_normals_split') else None
    try:
        me.set_sharp_from_angle(angle=math.radians(30))
    except Exception:
        pass
    ob = bpy.data.objects.new(name, me)
    ob.location = center
    return ob

def box(name, size, center=(0, 0, 0), bevel=0.0):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=Vector(size), verts=bm.verts)
    return _finish(bm, name, bevel, center=center)

def cylinder(name, radius, length, axis='Z', center=(0, 0, 0), segments=48, bevel=0.0, radius2=None):
    """axis 방향으로 length, 중심 center"""
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=segments, radius1=radius, radius2=radius if radius2 is None else radius2, depth=length)
    rot = {'Z': Matrix.Identity(4), 'X': Matrix.Rotation(math.radians(90), 4, 'Y'), 'Y': Matrix.Rotation(math.radians(-90), 4, 'X')}[axis]
    bmesh.ops.transform(bm, matrix=rot, verts=bm.verts)
    return _finish(bm, name, bevel, center=center)

def tube(name, r_out, r_in, length, axis='Z', center=(0, 0, 0), segments=64):
    bm = bmesh.new()
    verts_o = []; verts_i = []
    for s in range(segments):
        a = 2 * math.pi * s / segments
        for zsgn in (-1, 1):
            verts_o.append(bm.verts.new((r_out * math.cos(a), r_out * math.sin(a), zsgn * length / 2)))
            verts_i.append(bm.verts.new((r_in * math.cos(a), r_in * math.sin(a), zsgn * length / 2)))
    bm.verts.ensure_lookup_table()
    for s in range(segments):
        n = (s + 1) % segments
        o0, o1, n0, n1 = verts_o[2 * s], verts_o[2 * s + 1], verts_o[2 * n], verts_o[2 * n + 1]
        i0, i1, m0, m1 = verts_i[2 * s], verts_i[2 * s + 1], verts_i[2 * n], verts_i[2 * n + 1]
        bm.faces.new((o0, n0, n1, o1)); bm.faces.new((i1, m1, m0, i0))
        bm.faces.new((o1, n1, m1, i1)); bm.faces.new((i0, m0, n0, o0))
    rot = {'Z': Matrix.Identity(4), 'X': Matrix.Rotation(math.radians(90), 4, 'Y'), 'Y': Matrix.Rotation(math.radians(-90), 4, 'X')}[axis]
    bmesh.ops.transform(bm, matrix=rot, verts=bm.verts)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return _finish(bm, name, center=center)

def gear(name, pitch_radius, teeth, width, axis='Y', center=(0, 0, 0), module=None, bevel=0.0):
    """사다리꼴 치형 단순 기어(모듈 = 2·r/z). 인벌류트는 오프라인 에셋 단계에서 교체 가능. 치면 명도 분리를 위해 치면 폴리곤은 material index 1."""
    m = module or (2 * pitch_radius / teeth)
    ra, rf = pitch_radius + 0.75 * m, pitch_radius - 1.1 * m   # 사다리꼴 치형은 비공액이라 어덴덤을 줄여 회전 중 간섭을 막는다(인벌류트 교체 시 1.0/1.25)
    bm = bmesh.new(); rings = []
    for zsgn in (-1, 1):
        ring = []
        for k in range(teeth):
            a0 = 2 * math.pi * k / teeth; da = 2 * math.pi / teeth
            pts = [(rf, a0), (rf, a0 + 0.28 * da), (ra, a0 + 0.38 * da), (ra, a0 + 0.62 * da), (rf, a0 + 0.72 * da)]
            for r, a in pts:
                ring.append(bm.verts.new((r * math.cos(a), r * math.sin(a), zsgn * width / 2)))
        rings.append(ring)
    n = len(rings[0]); bm.verts.ensure_lookup_table()
    side = []
    for i in range(n):
        j = (i + 1) % n
        f = bm.faces.new((rings[0][i], rings[0][j], rings[1][j], rings[1][i])); side.append(f)
        f.material_index = 1 if (i % 5) in (1, 2, 3) else 0
    bm.faces.new(rings[0][::-1]).material_index = 0
    bm.faces.new(rings[1]).material_index = 0
    rot = {'Z': Matrix.Identity(4), 'X': Matrix.Rotation(math.radians(90), 4, 'Y'), 'Y': Matrix.Rotation(math.radians(-90), 4, 'X')}[axis]
    bmesh.ops.transform(bm, matrix=rot, verts=bm.verts)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return _finish(bm, name, bevel, center=center)

def polyline_tube(name, points, radius, segments=12, attr_name='u'):
    """폴리라인을 따라 튜브. 정점 float 속성 u∈[0,1] (길이 비례) 기록."""
    pts = [Vector(p) for p in points]
    L = [0.0]
    for a, b in zip(pts[:-1], pts[1:]): L.append(L[-1] + (b - a).length)
    total = L[-1]
    bm = bmesh.new(); rings = []; us = []
    for i, p in enumerate(pts):
        d = (pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)]).normalized()
        up = Vector((0, 0, 1)) if abs(d.z) < 0.9 else Vector((1, 0, 0))
        n1 = d.cross(up).normalized(); n2 = d.cross(n1).normalized()
        ring = [bm.verts.new(p + radius * (math.cos(2 * math.pi * s / segments) * n1 + math.sin(2 * math.pi * s / segments) * n2)) for s in range(segments)]
        rings.append(ring); us.append(L[i] / total)
    for r0, r1 in zip(rings[:-1], rings[1:]):
        for s in range(segments):
            t = (s + 1) % segments
            bm.faces.new((r0[s], r0[t], r1[t], r1[s]))
    bm.faces.new(rings[0][::-1]); bm.faces.new(rings[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    attr = me.attributes.new(attr_name, 'FLOAT', 'POINT')
    vals = [u for u in us for _ in range(segments)]
    attr.data.foreach_set('value', vals)
    for p in me.polygons: p.use_smooth = True
    return bpy.data.objects.new(name, me)

def rail_profile(name, length, center=(0, 0, 0)):
    """단순 레일 단면(두부 폭 0.07, 높이 0.15, 저부 0.14) X 방향 압출"""
    prof = [(-0.07, 0.0), (0.07, 0.0), (0.07, 0.015), (0.012, 0.03), (0.012, 0.11), (0.035, 0.115), (0.035, 0.15), (-0.035, 0.15), (-0.035, 0.115), (-0.012, 0.11), (-0.012, 0.03), (-0.07, 0.015)]
    bm = bmesh.new()
    a = [bm.verts.new((-length / 2, y, z)) for y, z in prof]
    b = [bm.verts.new((length / 2, y, z)) for y, z in prof]
    n = len(prof)
    for i in range(n):
        j = (i + 1) % n; bm.faces.new((a[i], a[j], b[j], b[i]))
    bm.faces.new(a[::-1]); bm.faces.new(b)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    ob = _finish(bm, name, center=center)
    # 두부 상면(로컬 z=0.15)만 material 1 (M_MACH)
    for p in ob.data.polygons:
        if all(abs(ob.data.vertices[v].co.z - 0.15) < 1e-6 for v in p.vertices): p.material_index = 1
    return ob
