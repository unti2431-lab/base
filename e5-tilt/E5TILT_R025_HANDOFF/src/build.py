"""E5 TILT R025 - proxy scene build (bpy, no bpy.ops except save).

Input : rig_config.json, cameras.json, tilt_bake.npz (only motion source)
Output: ../work/e5tilt_R025_proxy.blend
Run   : python build.py                      (bpy module, Blender 4.5.14)
        blender -b -P build.py -- [--out path] (Windows / Blender app)

Naming: KIND_SIDE_INDEX, e.g. BODY_01, BOGIE_01_R, SPRING_L_BELLOWS, SKIRT_01_R_L. verify_scene.py finds objects by name.
"""
import os, sys, math, json, argparse
import numpy as np
import bpy, bmesh
from mathutils import Vector, Matrix, Quaternion

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import HERE, argv, load_cfg, load_cams, bake_fcurves, SKY_SINGLE, SKY_DUST

ap = argparse.ArgumentParser()
ap.add_argument('--bake', default=os.path.join(HERE, 'tilt_bake.npz'))
ap.add_argument('--out', default=os.path.join(HERE, '..', 'work', 'e5tilt_R025_proxy.blend'))
A = ap.parse_args(argv())

CFG = load_cfg(); CAMS = load_cams()
D = dict(np.load(A.bake))
FR = D['F']
TR, TN, BG, SP, CB = CFG['track'], CFG['train'], CFG['bogie'], CFG['spring'], CFG['cabin']
np.random.seed(CFG['spec']['seed'])

# ------------------------------------------------------------------ scene reset
for ob in list(bpy.data.objects):
    bpy.data.objects.remove(ob, do_unlink=True)
for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.cameras, bpy.data.lights, bpy.data.actions,
             bpy.data.collections, bpy.data.node_groups):
    for x in list(coll):
        coll.remove(x)
SC = bpy.context.scene
SC.name = 'E5TILT_R025'
SC.frame_start = CFG['spec']['frame_start']; SC.frame_end = CFG['spec']['frame_end']
SC.render.fps = CFG['spec']['fps']
SC.unit_settings.system = 'METRIC'; SC.unit_settings.scale_length = 1.0


def coll(name, parent=None):
    c = bpy.data.collections.new(name)
    (parent or SC.collection).children.link(c)
    return c


C_TRACK, C_TRAIN, C_HERO, C_CABIN, C_ISO, C_CAM, C_LIGHT = (coll(n) for n in
    ('TRACK', 'TRAIN', 'HERO_BOGIE', 'CABIN', 'ISO', 'CAMERAS', 'LIGHTS'))


def obj(name, data, c, parent=None, loc=(0, 0, 0)):
    o = bpy.data.objects.new(name, data)
    c.objects.link(o)
    if parent is not None:
        o.parent = parent
        o.matrix_parent_inverse = Matrix.Identity(4)
    o.location = loc
    return o


def empty(name, c, parent=None, loc=(0, 0, 0)):
    o = obj(name, None, c, parent, loc)
    o.empty_display_size = 0.5
    return o


# ------------------------------------------------------------------ materials
def nodes_clear(mat):
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    return nt, out


def bsdf(nt, base, rough=0.5, metal=0.0, coat=0.0, alpha=1.0):
    b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    if isinstance(base, (tuple, list)):
        b.inputs['Base Color'].default_value = (*base[:3], 1)
    b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal
    b.inputs['Coat Weight'].default_value = coat
    return b


def attr(nt, name):
    a = nt.nodes.new('ShaderNodeAttribute'); a.attribute_type = 'OBJECT'; a.attribute_name = name
    return a.outputs['Fac']


def mth(nt, op, a, b=None, clamp=False):
    m = nt.nodes.new('ShaderNodeMath'); m.operation = op; m.use_clamp = clamp
    for i, v in enumerate((a, b)):
        if v is None:
            continue
        if isinstance(v, (int, float)):
            m.inputs[i].default_value = v
        else:
            nt.links.new(v, m.inputs[i])
    return m.outputs[0]


def mix_shader(nt, fac, s1, s2):
    m = nt.nodes.new('ShaderNodeMixShader')
    if isinstance(fac, (int, float)):
        m.inputs[0].default_value = fac
    else:
        nt.links.new(fac, m.inputs[0])
    nt.links.new(s1, m.inputs[1]); nt.links.new(s2, m.inputs[2])
    return m.outputs[0]


def mix_rgb(nt, fac, c1, c2):
    m = nt.nodes.new('ShaderNodeMix'); m.data_type = 'RGBA'
    nt.links.new(fac, m.inputs['Factor'])
    for sock, c in ((m.inputs[6], c1), (m.inputs[7], c2)):
        if isinstance(c, (tuple, list)):
            sock.default_value = (*c[:3], 1)
        else:
            nt.links.new(c, sock)
    return m.outputs[2]


def xray_shader(nt):
    lw = nt.nodes.new('ShaderNodeLayerWeight'); lw.inputs['Blend'].default_value = 0.35
    edge = mth(nt, 'POWER', lw.outputs['Facing'], 2.2)
    em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Color'].default_value = (0.92, 0.95, 1.0, 1); em.inputs['Strength'].default_value = 1.6
    tr = nt.nodes.new('ShaderNodeBsdfTransparent')
    return mix_shader(nt, edge, tr.outputs[0], em.outputs[0])


def mat_simple(name, base, rough, metal=0.0, coat=0.0, wear=False, grime=False):
    m = bpy.data.materials.new(name); nt, out = nodes_clear(m)
    b = bsdf(nt, base, rough, metal, coat)
    if wear or grime:
        col = nt.nodes.new('ShaderNodeRGB'); col.outputs[0].default_value = (*base, 1)
        c = col.outputs[0]
        if wear:
            g = nt.nodes.new('ShaderNodeNewGeometry')
            pw = mth(nt, 'SUBTRACT', g.outputs['Pointiness'], 0.52)
            pw = mth(nt, 'MULTIPLY', pw, 9.0, clamp=True)
            c = mix_rgb(nt, pw, c, tuple(min(1, x * 1.9 + 0.08) for x in base))
        if grime:
            nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 6.0; nz.inputs['Detail'].default_value = 6
            gm = mth(nt, 'SUBTRACT', nz.outputs['Fac'], 0.55)
            gm = mth(nt, 'MULTIPLY', gm, 3.0, clamp=True)
            c = mix_rgb(nt, gm, c, tuple(x * 0.45 for x in base))
        nt.links.new(c, b.inputs['Base Color'])
    nt.links.new(b.outputs[0], out.inputs[0])
    return m


def mat_xray_capable(name, base, rough, prop='xray'):
    m = bpy.data.materials.new(name); nt, out = nodes_clear(m)
    b = bsdf(nt, base, rough, 0.0, 0.3)
    nt.links.new(mix_shader(nt, attr(nt, prop), b.outputs[0], xray_shader(nt)), out.inputs[0])
    return m


def mat_ghost():
    m = bpy.data.materials.new('MAT_GHOST'); nt, out = nodes_clear(m)
    tr = nt.nodes.new('ShaderNodeBsdfTransparent')
    nt.links.new(mix_shader(nt, attr(nt, 'vis'), tr.outputs[0], xray_shader(nt)), out.inputs[0])
    return m


def mat_body():
    """E5 livery by body-local height: white / pink line / tokiwa green, procedural windows.
    Object attributes: win_ymin, win_ymax (window span), win_clear (1 = see-through, hero car)."""
    m = bpy.data.materials.new('MAT_BODY'); nt, out = nodes_clear(m)
    tc = nt.nodes.new('ShaderNodeTexCoord'); sx = nt.nodes.new('ShaderNodeSeparateXYZ')
    nt.links.new(tc.outputs['Object'], sx.inputs[0])
    z, y = sx.outputs['Z'], sx.outputs['Y']
    p0, p1 = TN['livery_pink']
    col = mix_rgb(nt, mth(nt, 'GREATER_THAN', z, p0), (0.86, 0.87, 0.88), (0.86, 0.30, 0.48))
    col = mix_rgb(nt, mth(nt, 'GREATER_THAN', z, p1), col, (0.015, 0.26, 0.15))
    paint = bsdf(nt, (1, 1, 1), 0.16, 0.0, 0.6); nt.links.new(col, paint.inputs['Base Color'])
    fy = mth(nt, 'FRACT', mth(nt, 'DIVIDE', y, TN['window_pitch']))
    f0, f1 = TN['window_frac']; w0, w1 = TN['window_z']
    msk = mth(nt, 'MULTIPLY', mth(nt, 'GREATER_THAN', fy, f0), mth(nt, 'LESS_THAN', fy, f1))
    msk = mth(nt, 'MULTIPLY', msk, mth(nt, 'GREATER_THAN', z, w0))
    msk = mth(nt, 'MULTIPLY', msk, mth(nt, 'LESS_THAN', z, w1))
    msk = mth(nt, 'MULTIPLY', msk, mth(nt, 'GREATER_THAN', y, attr(nt, 'win_ymin')))
    msk = mth(nt, 'MULTIPLY', msk, mth(nt, 'LESS_THAN', y, attr(nt, 'win_ymax')))
    glass = bsdf(nt, (0.015, 0.02, 0.025), 0.04, 0.0, 1.0)
    tr = nt.nodes.new('ShaderNodeBsdfTransparent')
    g = nt.nodes.new('ShaderNodeNewGeometry'); lp = nt.nodes.new('ShaderNodeLightPath')
    see = mth(nt, 'MAXIMUM', g.outputs['Backfacing'], mth(nt, 'SUBTRACT', 1.0, lp.outputs['Is Camera Ray']))
    glass_s = mix_shader(nt, mth(nt, 'MULTIPLY', mth(nt, 'MULTIPLY', attr(nt, 'win_clear'), see), 0.9), glass.outputs[0], tr.outputs[0])
    surf = mix_shader(nt, msk, paint.outputs[0], glass_s)
    inner = bsdf(nt, (0.62, 0.60, 0.56), 0.7)
    back = mth(nt, 'MULTIPLY', g.outputs['Backfacing'], mth(nt, 'SUBTRACT', 1.0, msk))
    nt.links.new(mix_shader(nt, back, surf, inner.outputs[0]), out.inputs[0])
    return m


def mat_glass(name, rough=0.02):
    m = bpy.data.materials.new(name); nt, out = nodes_clear(m)
    g = nt.nodes.new('ShaderNodeBsdfGlass'); g.inputs['Roughness'].default_value = rough; g.inputs['IOR'].default_value = 1.45
    nt.links.new(g.outputs[0], out.inputs[0])
    return m


def mat_concrete(name, base):
    m = bpy.data.materials.new(name); nt, out = nodes_clear(m)
    b = bsdf(nt, base, 0.88)
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 1.2; nz.inputs['Detail'].default_value = 8
    c = mix_rgb(nt, nz.outputs['Fac'], tuple(x * 0.82 for x in base), tuple(min(1, x * 1.12) for x in base))
    nt.links.new(c, b.inputs['Base Color']); nt.links.new(b.outputs[0], out.inputs[0])
    return m


def mat_ground():
    m = bpy.data.materials.new('MAT_GROUND'); nt, out = nodes_clear(m)
    b = bsdf(nt, (0.1, 0.12, 0.06), 0.95)
    tc = nt.nodes.new('ShaderNodeTexCoord')
    vo = nt.nodes.new('ShaderNodeTexVoronoi'); vo.inputs['Scale'].default_value = 0.012
    nt.links.new(tc.outputs['Object'], vo.inputs['Vector'])
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    cr = ramp.color_ramp; cr.interpolation = 'CONSTANT'
    cr.elements[0].color = (0.07, 0.10, 0.04, 1); cr.elements[1].position = 0.5; cr.elements[1].color = (0.16, 0.15, 0.07, 1)
    e = cr.elements.new(0.25); e.color = (0.10, 0.14, 0.05, 1)
    e = cr.elements.new(0.75); e.color = (0.13, 0.12, 0.09, 1)
    nt.links.new(vo.outputs['Color'], ramp.inputs[0])
    nt.links.new(ramp.outputs[0], b.inputs['Base Color']); nt.links.new(b.outputs[0], out.inputs[0])
    return m


M = dict(
    BODY=mat_body(), GHOST=mat_ghost(),
    SKIRT=mat_xray_capable('MAT_SKIRT', (0.78, 0.79, 0.80), 0.3),
    FRAME=mat_simple('MAT_FRAME', (0.36, 0.37, 0.38), 0.45, 0.55, wear=True, grime=True),
    POLISH=mat_simple('MAT_STEEL_POLISH', (0.80, 0.80, 0.80), 0.16, 1.0),
    RAILSIDE=mat_simple('MAT_RAIL_SIDE', (0.20, 0.13, 0.09), 0.7, 0.3, grime=True),
    RUBBER=mat_simple('MAT_RUBBER', (0.025, 0.025, 0.025), 0.78),
    DARK=mat_simple('MAT_DARKMETAL', (0.07, 0.07, 0.075), 0.5, 0.4, wear=True),
    CONC=mat_concrete('MAT_CONCRETE', (0.46, 0.45, 0.43)),
    SLAB=mat_concrete('MAT_SLAB', (0.36, 0.36, 0.35)),
    GROUND=mat_ground(),
    MAST=mat_simple('MAT_MAST', (0.55, 0.56, 0.57), 0.42, 0.8),
    COCKPIT=mat_simple('MAT_GLASS_DARK', (0.01, 0.012, 0.015), 0.03, 0.0, 1.0),
    CUP=mat_glass('MAT_CUP_GLASS'),
    LIQUID=mat_simple('MAT_LIQUID', (0.05, 0.022, 0.010), 0.06, 0.0, 0.5),
    SEAT=mat_simple('MAT_SEAT', (0.10, 0.15, 0.21), 0.9),
    FLOOR=mat_simple('MAT_CABIN_FLOOR', (0.22, 0.21, 0.20), 0.8),
    CEIL=mat_simple('MAT_CABIN_CEIL', (0.78, 0.77, 0.74), 0.6),
    TRAY=mat_simple('MAT_TRAY', (0.32, 0.31, 0.30), 0.4),
)


# ------------------------------------------------------------------ mesh helpers
def finish(bm, name, mats, smooth=True, sharp_deg=30.0, bevel=0.0):
    if bevel > 0:
        edges = [e for e in bm.edges if e.is_manifold and e.calc_face_angle(0) > math.radians(sharp_deg)]
        if edges:
            bmesh.ops.bevel(bm, geom=edges, offset=bevel, segments=2, affect='EDGES', profile=0.5, clamp_overlap=True)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    bm.normal_update()
    for e in bm.edges:
        e.smooth = not (e.is_manifold and e.calc_face_angle(0) > math.radians(sharp_deg)) if e.is_manifold else False
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me); bm.free()
    me.polygons.foreach_set('use_smooth', [smooth] * len(me.polygons))
    for m_ in mats:
        me.materials.append(m_)
    me.update()
    return me


def add_box(bm, c, s, mat=0):
    r = bmesh.ops.create_cube(bm, size=1.0)
    for v in r['verts']:
        v.co = Vector((v.co.x * s[0] + c[0], v.co.y * s[1] + c[1], v.co.z * s[2] + c[2]))
    for f in {f for v in r['verts'] for f in v.link_faces}:
        f.material_index = mat


def add_cyl(bm, c, r, h, axis='Z', seg=32, mat=0):
    rot = {'Z': Matrix.Identity(4), 'X': Matrix.Rotation(math.pi / 2, 4, 'Y'), 'Y': Matrix.Rotation(math.pi / 2, 4, 'X')}[axis]
    res = bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=seg, radius1=r, radius2=r, depth=h,
                                matrix=Matrix.Translation(c) @ rot)
    for f in {f for v in res['verts'] for f in v.link_faces}:
        f.material_index = mat


def add_lathe(bm, prof, seg=40, axis='Z', c=(0, 0, 0), mat=0):
    """prof: [(r, a)] along the axis; r=0 collapses to a pole."""
    rings = []
    for r, a in prof:
        ring = []
        n = 1 if r == 0 else seg
        for i in range(n):
            th = 2 * math.pi * i / seg
            p = (r * math.cos(th), r * math.sin(th), a)
            if axis == 'X':
                p = (p[2], p[0], p[1])
            elif axis == 'Y':
                p = (p[0], p[2], p[1])
            ring.append(bm.verts.new((p[0] + c[0], p[1] + c[1], p[2] + c[2])))
        rings.append(ring)
    faces = []
    for r0, r1 in zip(rings[:-1], rings[1:]):
        if len(r0) == 1 and len(r1) == 1:
            continue
        for i in range(seg):
            if len(r0) == 1:
                faces.append(bm.faces.new((r0[0], r1[i], r1[(i + 1) % seg])))
            elif len(r1) == 1:
                faces.append(bm.faces.new((r0[i], r0[(i + 1) % seg], r1[0])))
            else:
                faces.append(bm.faces.new((r0[i], r0[(i + 1) % seg], r1[(i + 1) % seg], r1[i])))
    for f in faces:
        f.material_index = mat
    return rings


def add_loft(bm, rings, cap=True, mat=0):
    vr = [[bm.verts.new(p) for p in ring] for ring in rings]
    n = len(rings[0])
    for a, b in zip(vr[:-1], vr[1:]):
        for i in range(n):
            f = bm.faces.new((a[i], a[(i + 1) % n], b[(i + 1) % n], b[i])); f.material_index = mat
    if cap:
        f = bm.faces.new(list(reversed(vr[0]))); f.material_index = mat
        f = bm.faces.new(vr[-1]); f.material_index = mat
    return vr


def add_helix_tube(bm, c, R, a, h, turns, seg=8, steps_per_turn=24, mat=0):
    n = int(turns * steps_per_turn) + 1
    pts = []
    for i in range(n):
        th = 2 * math.pi * turns * i / (n - 1)
        pts.append(Vector((c[0] + R * math.cos(th), c[1] + R * math.sin(th), c[2] + h * i / (n - 1))))
    rings = []
    for i, p in enumerate(pts):
        t = (pts[min(i + 1, n - 1)] - pts[max(i - 1, 0)]).normalized()
        radial = Vector((p.x - c[0], p.y - c[1], 0)).normalized()
        b = t.cross(radial).normalized(); nrm = b.cross(t).normalized()
        rings.append([tuple(p + a * (math.cos(2 * math.pi * k / seg) * nrm + math.sin(2 * math.pi * k / seg) * b)) for k in range(seg)])
    add_loft(bm, rings, True, mat)


# ------------------------------------------------------------------ path helpers (from bake arrays only)
PS, PX, PY, PPSI = D['path_s'], D['path_x'], D['path_y'], D['path_psi']
ZR = TR['rail_top_z']


def path_pt(s, x_off=0.0, z=0.0):
    s = np.asarray(s, float)
    p = np.interp(s, PS, PPSI)
    x = np.interp(s, PS, PX) + np.cos(p) * x_off
    y = np.interp(s, PS, PY) + np.sin(p) * x_off
    return np.stack([x, y, np.full_like(s, z)], -1), p


def ribbon(name, s_arr, prof, x_off, mats, mat_idx=None, smooth=False):
    """extrude closed 2D profile [(x,z)] along the path. x is lateral (right +), z absolute."""
    bm = bmesh.new()
    p = np.interp(s_arr, PS, PPSI)
    cx = np.interp(s_arr, PS, PX); cy = np.interp(s_arr, PS, PY)
    rings = []
    for i in range(len(s_arr)):
        r = (math.cos(p[i]), math.sin(p[i]))
        rings.append([(cx[i] + r[0] * (x_off + px), cy[i] + r[1] * (x_off + px), pz) for px, pz in prof])
    add_loft(bm, rings, True)
    if mat_idx is not None:
        n = len(prof)
        bm.faces.ensure_lookup_table()
        for fi in range((len(rings) - 1) * n):
            bm.faces[fi].material_index = mat_idx[fi % n]
    return finish(bm, name, mats, smooth=smooth)


# ------------------------------------------------------------------ TRACK & VIADUCT
s_lo, s_hi = TR['s_min'] + 1, TR['s_max'] - 1
s_samp = np.arange(s_lo, s_hi, 1.0)
x2 = TR['track_spacing'] * TR['second_track_side']
dc = TR['deck_center_offset']

deck_prof = [(-TR['deck_half_w'], -TR['deck_thickness']), (TR['deck_half_w'], -TR['deck_thickness']),
             (TR['deck_half_w'], 0.0), (-TR['deck_half_w'], 0.0)]
obj('DECK', ribbon('DECK', s_samp, deck_prof, dc, [M['CONC']]), C_TRACK)
wl = TR['wall_offset_left']; wt = TR['wall_t']; wh = TR['wall_h']
obj('WALL_L', ribbon('WALL_L', s_samp, [(wl - wt, 0), (wl, 0), (wl, wh), (wl - wt, wh)], 0.0, [M['CONC']]), C_TRACK)
wr = dc + TR['deck_half_w']
obj('WALL_R', ribbon('WALL_R', s_samp, [(wr - wt, 0), (wr, 0), (wr, wh), (wr - wt, wh)], 0.0, [M['CONC']]), C_TRACK)

# rail profile (x about rail centre, z about rail top) ; head-top faces get the polished material
hz = ZR
rail_prof = [(-0.0725, hz - 0.174), (0.0725, hz - 0.174), (0.0725, hz - 0.160), (0.0085, hz - 0.140),
             (0.0085, hz - 0.049), (0.0325, hz - 0.040), (0.0325, hz - 0.008), (0.026, hz), (-0.026, hz),
             (-0.0325, hz - 0.008), (-0.0325, hz - 0.040), (-0.0085, hz - 0.049), (-0.0085, hz - 0.140), (-0.0725, hz - 0.160)]
mat_idx = [1] * len(rail_prof); mat_idx[7] = 0; mat_idx[6] = 0; mat_idx[8] = 0
rx = TR['gauge'] / 2 + TR['rail_head_offset']
for tname, xo in (('A', 0.0), ('B', x2)):
    for side, sx in (('L', -1), ('R', 1)):
        nm = f'RAIL_{tname}_{side}'
        obj(nm, ribbon(nm, s_samp, rail_prof, xo + sx * rx, [M['POLISH'], M['RAILSIDE']], mat_idx), C_TRACK)


def slabs(name, xo, pitch, phase):
    bm = bmesh.new()
    k0 = math.ceil((s_lo - phase) / pitch); k1 = math.floor((s_hi - phase) / pitch)
    hw = TR['slab_w'] / 2; zt = TR['slab_top_z']
    for k in range(k0, k1):
        sa = phase + k * pitch + TR['slab_gap'] / 2; sb = sa + pitch - TR['slab_gap']
        (pa, _), (pb, _) = path_pt([sa], xo - hw), path_pt([sb], xo - hw)
        (qa, _), (qb, _) = path_pt([sa], xo + hw), path_pt([sb], xo + hw)
        pts = [pa[0], qa[0], qb[0], pb[0]]
        lo = [bm.verts.new((p[0], p[1], 0.0)) for p in pts]
        hi = [bm.verts.new((p[0], p[1], zt)) for p in pts]
        bm.faces.new(list(reversed(lo))); bm.faces.new(hi)
        for i in range(4):
            bm.faces.new((lo[i], lo[(i + 1) % 4], hi[(i + 1) % 4], hi[i]))
    return finish(bm, name, [M['SLAB']], smooth=False)


obj('SLAB_A', slabs('SLAB_A', 0.0, float(D['slab_pitch']), float(D['phase0'])), C_TRACK)
obj('SLAB_B', slabs('SLAB_B', x2, float(D['slab_pitch']), float(D['phase0'])), C_TRACK)

# masts with cantilever arms (instances)
bm = bmesh.new()
mh = TR['mast_h']; mo = TR['mast_offset']
add_box(bm, (0, 0, mh / 2), (0.30, 0.30, mh))
add_box(bm, ((-0.6 - mo) / 2 + 0.0, 0, mh - 1.0), (mo + 0.6, 0.12, 0.14))
add_box(bm, ((-0.6 - mo) / 2 + 0.0, 0, mh - 1.6), (mo + 0.6, 0.08, 0.08))
mast_me = finish(bm, 'MAST', [M['MAST']], smooth=False, bevel=0.01)
k0 = math.ceil((s_lo - float(D['phase0'])) / float(D['mast_pitch']))
k1 = math.floor((s_hi - float(D['phase0'])) / float(D['mast_pitch']))
for k in range(k0, k1 + 1):
    s = float(D['phase0']) + k * float(D['mast_pitch'])
    (p, psi) = path_pt([s], mo)
    o = obj(f'MAST_{k - k0:03d}', mast_me, C_TRACK, loc=tuple(p[0]))
    o.rotation_euler = (0, 0, float(psi[0]))

# piers
bm = bmesh.new(); add_box(bm, (0, 0, (TR['ground_z'] - TR['deck_thickness']) / 2), (3.2, 2.4, -TR['ground_z'] - TR['deck_thickness']))
pier_me = finish(bm, 'PIER', [M['CONC']], smooth=False, bevel=0.03)
for k, s in enumerate(np.arange(s_lo + 5, s_hi, TR['pier_spacing'])):
    p, psi = path_pt([s], dc)
    o = obj(f'PIER_{k:03d}', pier_me, C_TRACK, loc=tuple(p[0])); o.rotation_euler = (0, 0, float(psi[0]))

# ground
bm = bmesh.new()
cxm, cym = float(np.mean(PX)), float(np.mean(PY))
add_box(bm, (cxm, cym, TR['ground_z'] - 0.5), (9000, 9000, 1.0))
obj('GROUND', finish(bm, 'GROUND', [M['GROUND']], smooth=False), C_TRACK)


# ------------------------------------------------------------------ TRAIN BODIES
def body_section(w, h, zb, rb, rt, N=40):
    pts = []
    q = N // 4
    for cxs, czs, a0, r in ((w / 2 - rb, zb + rb, -90, rb), (w / 2 - rt, zb + h - rt, 0, rt),
                            (-w / 2 + rt, zb + h - rt, 90, rt), (-w / 2 + rb, zb + rb, 180, rb)):
        for i in range(q):
            a = math.radians(a0 + 90 * i / (q - 1))
            pts.append((cxs + r * math.cos(a), czs + r * math.sin(a)))
    return pts


BW = TN['body_w']; BH = TN['body_top_above_rail'] - TN['body_bottom_above_rail']


def body_mesh(name, L, kind, y_lo=None, y_hi=None):
    """kind: mid | nose_front | nose_rear. Local origin = body bottom centre (roll centre)."""
    bm = bmesh.new()
    nl = TN['nose_len']
    ys, prm = [], []
    y0, y1 = (-L / 2, L / 2) if y_lo is None else (y_lo, y_hi)
    flat_end = L / 2 - nl if kind != 'mid' else L / 2
    for y in np.linspace(max(y0, -L / 2), min(y1, flat_end), max(3, int((min(y1, flat_end) - max(y0, -L / 2)) / 2.5) + 2)):
        ys.append(y); prm.append((1.0, 1.0, 0.0))
    if kind != 'mid' and (y_hi is None or y_hi > flat_end):
        for u in np.linspace(0, 1, 26)[1:]:
            wf = max(math.sqrt(max(1 - u ** 2.0, 0.0)), 0.035)
            ht = 1 - 0.72 * u ** 1.4
            zb = 0.20 * u ** 2
            ys.append(flat_end + u * nl); prm.append((wf, ht, zb))
    rings = []
    for y, (wf, ht, zb) in zip(ys, prm):
        w = BW * wf; h = BH * ht - zb
        rb = min(0.25, 0.45 * min(w, h)); rt = min(0.62, 0.48 * min(w, h))
        sec = body_section(w, h, zb, rb, rt)
        rings.append([(x, y, z) for x, z in sec])
    if kind == 'nose_rear':
        rings = [[(x, -y, z) for x, y, z in r] for r in reversed(rings)]
    add_loft(bm, rings, True)
    return finish(bm, name, [M['BODY']], smooth=True, sharp_deg=50)


def gangway(bm, y_end, sgn):
    add_box(bm, (0, y_end + sgn * 0.13, 1.45), (2.5, 0.26, 2.3))


nc = TN['n_cars']; hk = TN['hero_car'] - 1
BODY, GHOST = [], None
bm_g = bmesh.new()
gangway(bm_g, 0, 1)
gang_me = finish(bm_g, 'GANGWAY', [M['RUBBER']], smooth=False)
for k in range(nc):
    L = float(D['car_len'][k])
    kind = 'nose_front' if k == 0 else ('nose_rear' if k == nc - 1 else 'mid')
    me = body_mesh(f'BODY_{k + 1:02d}', L, kind)
    b = obj(f'BODY_{k + 1:02d}', me, C_TRAIN)
    b.rotation_mode = 'QUATERNION'
    b['win_ymin'] = -L / 2 + 1.2 if kind != 'nose_rear' else -L / 2 + TN['nose_len'] + 0.8
    b['win_ymax'] = L / 2 - 1.2 if kind != 'nose_front' else L / 2 - TN['nose_len'] - 0.8
    b['win_clear'] = 1.0 if k == hk else 0.0
    b['xray'] = 0.0
    BODY.append(b)
    for sgn, present in ((1, kind != 'nose_front'), (-1, kind != 'nose_rear')):
        if present:
            g = obj(f'GANGWAY_{k + 1:02d}_{"F" if sgn > 0 else "R"}', gang_me, C_TRAIN, parent=b, loc=(0, sgn * L / 2 - (0.0 if sgn > 0 else 0), 0))
            g.scale = (1, sgn, 1)
    if kind != 'mid':
        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=1.0)
        for v in bm.verts:
            v.co = Vector((v.co.x * 0.95, v.co.y * 2.6, v.co.z * 0.42))
        cm = finish(bm, f'COCKPIT_{k + 1:02d}', [M['COCKPIT']])
        sgn = 1 if kind == 'nose_front' else -1
        u = 0.36; yy = sgn * (L / 2 - TN['nose_len'] + u * TN['nose_len'])
        obj(f'COCKPIT_{k + 1:02d}', cm, C_TRAIN, parent=b, loc=(0, yy, BH * (1 - 0.72 * u ** 1.4) - 0.22))

GHOST = obj('GHOST_01', BODY[hk].data, C_TRAIN)
GHOST.rotation_mode = 'QUATERNION'; GHOST['vis'] = 0.0
GHOST.data = BODY[hk].data.copy(); GHOST.data.name = 'GHOST_01'
GHOST.data.materials.clear(); GHOST.data.materials.append(M['GHOST'])
GHOST.visible_shadow = False

# skirts (bogie covers) - children of bodies
zsk0 = TN['skirt_bottom_above_rail'] - TN['body_bottom_above_rail']
bm = bmesh.new(); add_box(bm, (0, 0, (zsk0 + 0.06) / 2), (TN['skirt_t'], 2 * TN['skirt_half_len'], 0.06 - zsk0))
skirt_me = finish(bm, 'SKIRT', [M['SKIRT']], smooth=False, bevel=0.004)
hb = TN['bogie_half_spacing']
SKIRTS_HERO = []
for k in range(nc):
    for j, yb in (('F', hb), ('R', -hb)):
        if (k == 0 and j == 'F') or (k == nc - 1 and j == 'R'):
            continue                                   # nose bogies: covered by the nose fairing in the proxy
        for side, sx in (('L', -1), ('R', 1)):
            s_ = obj(f'SKIRT_{k + 1:02d}_{j}_{side}', skirt_me, C_TRAIN, parent=BODY[k], loc=(sx * (BW / 2 - 0.05), yb, 0))
            s_['xray'] = 0.0
            if k == hk and j == 'R':
                SKIRTS_HERO.append(s_)

# ------------------------------------------------------------------ BOGIES
wr_, gap = BG['wheel_r'], BG['wheel_contact_gap']
zax = wr_ + gap
bm = bmesh.new()
for sx in (-1, 1):
    a = lambda x: sx * x
    add_lathe(bm, [(0.0, a(0.62)), (0.12, a(0.62)), (0.33, a(0.65)), (0.33, a(0.69)), (BG['flange_r'], a(0.69)),
                   (BG['flange_r'], a(0.72)), (wr_, a(0.72)), (wr_ - 0.004, a(0.855)), (0.33, a(0.855)),
                   (0.33, a(0.895)), (0.12, a(0.895)), (0.0, a(0.895))], seg=48, axis='X', mat=0)
add_cyl(bm, (0, 0, 0), 0.09, 2.16, axis='X', seg=24, mat=1)
wheel_me = finish(bm, 'WHEELSET', [M['POLISH'], M['FRAME']], smooth=True, sharp_deg=40)

bm = bmesh.new()
for sx in (-1, 1):
    add_box(bm, (sx * 1.0, 0, 0.66), (0.2, 3.6, 0.36))
add_box(bm, (0, 0.38, 0.5), (1.8, 0.16, 0.18)); add_box(bm, (0, -0.38, 0.5), (1.8, 0.16, 0.18))
bogie_proxy_me = finish(bm, 'BOGIE_FRAME_PROXY', [M['FRAME']], smooth=False, bevel=0.01)


def side_beam(bm, x):
    ft = BG['frame_top_above_rail']
    prof = [(-1.85, 0.74), (-0.95, 0.74), (-0.6, ft - 0.22), (0.6, ft - 0.22), (0.95, 0.74), (1.85, 0.74),
            (1.85, 0.92), (0.95, 0.92), (0.6, ft), (-0.6, ft), (-0.95, 0.92), (-1.85, 0.92)]
    rings = [[(x - 0.1, y, z) for y, z in prof], [(x + 0.1, y, z) for y, z in prof]]
    vr = [[bm.verts.new(p) for p in r] for r in rings]
    n = len(prof)
    bm.faces.new(list(reversed(vr[0]))); bm.faces.new(vr[1])
    for i in range(n):
        bm.faces.new((vr[0][i], vr[0][(i + 1) % n], vr[1][(i + 1) % n], vr[1][i]))


def bellows_mesh(name):
    """lathe whose basis = h_min stroke; shape key 'stroke' = h_max. Local origin = base plate top."""
    pt = SP['plate_t']; g = SP['bellows_top_gap']
    L0 = SP['h_min'] - 2 * pt - g; L1 = SP['h_max'] - 2 * pt - g
    def prof(L, bulge):
        return [(0.0, 0.0), (0.22, 0.0), (0.27, 0.12 * L), (bulge, 0.45 * L), (bulge - 0.01, 0.62 * L),
                (0.27, 0.88 * L), (0.24, L), (0.0, L)]
    bm = bmesh.new()
    add_lathe(bm, prof(L0, SP['bellows_r'] + 0.025), seg=40)
    me = finish(bm, name, [M['RUBBER']], smooth=True, sharp_deg=60)
    o = bpy.data.objects.new(name, me)
    o.shape_key_add(name='Basis')
    sk = o.shape_key_add(name='stroke')
    bm2 = bmesh.new(); add_lathe(bm2, prof(L1, SP['bellows_r'] - 0.01), seg=40)
    co = [v.co.copy() for v in bm2.verts]; bm2.free()
    for i, c in enumerate(co):
        sk.data[i].co = c
    sk.slider_min = 0.0; sk.slider_max = 1.0
    return o


SL = SP['s_lat'] / 2
FT = BG['frame_top_above_rail']
PT = SP['plate_t']


def build_hero_bogie(prefix, root, c):
    """all hero-bogie parts as children of root (bogie-local coords, rail-top origin). Returns dict of spring parts."""
    parts = {}
    bm = bmesh.new()
    side_beam(bm, -BG['side_beam_x']); side_beam(bm, BG['side_beam_x'])
    for yy in (-BG['cross_beam_y'], BG['cross_beam_y']):
        add_cyl(bm, (0, yy, BG['frame_top_above_rail'] - 0.12), BG['cross_beam_r'], 1.84, axis='X', seg=20)
    obj(f'{prefix}FRAME', finish(bm, f'{prefix}FRAME', [M['FRAME']], smooth=False, bevel=0.012), c, root)
    bm = bmesh.new()
    for sx in (-1, 1):
        for sy in (-1, 1):
            add_box(bm, (sx * BG['axlebox_x'], sy * BG['wheelbase'] / 2, zax + 0.0), (0.16, 0.30, 0.26))
    obj(f'{prefix}AXLEBOX', finish(bm, f'{prefix}AXLEBOX', [M['DARK']], smooth=False, bevel=0.01), c, root)
    bm = bmesh.new()
    for sx in (-1, 1):
        for sy in (-1, 1):
            z0 = zax + 0.13 + 0.016; z1 = 0.74 - 0.016
            add_helix_tube(bm, (sx * BG['axlebox_x'], sy * BG['wheelbase'] / 2, z0), 0.075, 0.014, z1 - z0, 3.5)
    obj(f'{prefix}COIL', finish(bm, f'{prefix}COIL', [M['FRAME']], smooth=True), c, root)
    bm = bmesh.new()
    for sy in (-1, 1):
        add_box(bm, (-0.15, sy * 0.72, 0.55), (0.6, 0.24, 0.36))
        add_box(bm, (0.30, sy * BG['wheelbase'] / 2, zax), (0.22, 0.42, 0.34))
    obj(f'{prefix}MOTOR', finish(bm, f'{prefix}MOTOR', [M['DARK']], smooth=False, bevel=0.015), c, root)
    bm = bmesh.new()
    for sx in (-1, 1):
        add_cyl(bm, (sx * 1.25, 1.35, 0.83), 0.05, 0.5, axis='Y', seg=16)      # yaw damper at the beam end, clear of the spring sight line
    obj(f'{prefix}YAWDAMP', finish(bm, f'{prefix}YAWDAMP', [M['DARK']], smooth=True), c, root)
    for side, sx in (('L', -1), ('R', 1)):
        bm = bmesh.new(); add_cyl(bm, (0, 0, PT / 2), SP['plate_r'], PT, seg=40)
        parts[f'BASE_{side}'] = obj(f'{prefix}SPRING_{side}_BASE', finish(bm, f'{prefix}SPRING_{side}_BASE', [M['DARK']], bevel=0.004), c, root, (sx * SL, 0, FT + 0.001))
        bo = bellows_mesh(f'{prefix}SPRING_{side}_BELLOWS'); c.objects.link(bo)
        bo.parent = root; bo.matrix_parent_inverse = Matrix.Identity(4); bo.location = (sx * SL, 0, FT + 0.001 + PT)
        parts[f'BELLOWS_{side}'] = bo
        ar = SP['aux_res']
        bm = bmesh.new(); add_cyl(bm, (0, 0, 0), ar['r'], ar['len'], axis='Y', seg=28)
        parts[f'AUXRES_{side}'] = obj(f'{prefix}AUXRES_{side}', finish(bm, f'{prefix}AUXRES_{side}', [M['FRAME']]), c, root,
                                      (sx * (SL + ar['offset'][0]), ar['offset'][1], FT + ar['offset'][2]))
        bm = bmesh.new(); add_box(bm, (0, 0, 0), (0.10, 0.08, 0.08))
        parts[f'LVALVE_{side}'] = obj(f'{prefix}LVALVE_{side}', finish(bm, f'{prefix}LVALVE_{side}', [M['DARK']], bevel=0.006), c, root,
                                      (sx * SL, 0.50, FT + 0.041))
        bm = bmesh.new(); add_cyl(bm, (0, 0, 0.05 + SP['lrod_len'] / 2), 0.012, SP['lrod_len'], seg=10)
        parts[f'LROD_{side}'] = obj(f'{prefix}LROD_{side}', finish(bm, f'{prefix}LROD_{side}', [M['MAST']]), c, root,
                                    (sx * SL, 0.56, FT + 0.04))
    return parts


BOGIES, WHEELS = {}, {}
HERO_PARTS = None
for k in range(nc):
    for j, tag in enumerate(('F', 'R')):
        nm = f'BOGIE_{k + 1:02d}_{tag}'
        is_hero = (k == hk and tag == 'R')
        root = empty(nm, C_HERO if is_hero else C_TRAIN)
        root.rotation_mode = 'QUATERNION'
        BOGIES[(k, j)] = root
        if is_hero:
            HERO_PARTS = build_hero_bogie('', root, C_HERO)
        else:
            obj(f'BOGIEFRAME_{k + 1:02d}_{tag}', bogie_proxy_me, C_TRAIN, root)
        for a_, sy in ((1, 1), (2, -1)):
            w = obj(f'WHEELSET_{k + 1:02d}_{tag}_{a_}', wheel_me, C_HERO if is_hero else C_TRAIN, root, (0, sy * BG['wheelbase'] / 2, zax))
            WHEELS.setdefault((k, j), []).append(w)

# spring top plates ride on the hero body (body-local: bottom face at z = 0 minus nothing -> plate below floor)
TOPS = {}
for side, sx in (('L', -1), ('R', 1)):
    bm = bmesh.new(); add_cyl(bm, (0, 0, -PT / 2 - 0.001), SP['plate_r'], PT, seg=40)     # 1 mm below the floor: no coplanar contact
    TOPS[side] = obj(f'SPRING_{side}_TOP', finish(bm, f'SPRING_{side}_TOP', [M['DARK']], bevel=0.004), C_HERO, BODY[hk], (sx * SL, -hb, 0))

# ------------------------------------------------------------------ CABIN (hero car, body-local)
fz = CB['floor_above_rail'] - TN['body_bottom_above_rail']
y_cab0, y_cab1 = -float(D['car_len'][hk]) / 2 + 0.4, float(D['car_len'][hk]) / 2 - TN['nose_len'] - 0.3
bm = bmesh.new(); add_box(bm, (0, (y_cab0 + y_cab1) / 2, fz - 0.025), (BW - 0.12, y_cab1 - y_cab0, 0.05))
obj('CABIN_FLOOR', finish(bm, 'CABIN_FLOOR', [M['FLOOR']], smooth=False), C_CABIN, BODY[hk])
bm = bmesh.new(); add_box(bm, (0, (y_cab0 + y_cab1) / 2, BH - 0.32), (BW - 0.5, y_cab1 - y_cab0, 0.04))
obj('CABIN_CEIL', finish(bm, 'CABIN_CEIL', [M['CEIL']], smooth=False), C_CABIN, BODY[hk])
cupx, cupy = CB['cup_local']
pitch = CB['seat_pitch']
yk0 = cupy - (pitch - 0.15)                     # passenger seat back (rear face) so that the cup sits on the tray ahead
bm = bmesh.new()
rows = [yk0 + i * pitch for i in range(-7, 5)]
for yk in rows:
    if yk < y_cab0 + 0.1 or yk + 0.65 > y_cab1:
        continue
    for x0, x1 in ((-1.50, -0.50), (0.45, 1.50)):
        add_box(bm, ((x0 + x1) / 2, yk + 0.06, fz + 0.80), (x1 - x0, 0.12, 0.80), 0)    # back
        add_box(bm, ((x0 + x1) / 2, yk + 0.37, fz + 0.30), (x1 - x0, 0.50, 0.20), 0)    # cushion
        add_box(bm, ((x0 + x1) / 2, yk + 0.37, fz + 0.10), (x1 - x0 - 0.2, 0.30, 0.20), 0)
obj('CABIN_SEATS', finish(bm, 'CABIN_SEATS', [M['SEAT']], smooth=False, bevel=0.03), C_CABIN, BODY[hk])
tray_top = fz + CB['table_h']
bm = bmesh.new()
for yk in rows:
    if yk + pitch < y_cab0 + 0.1 or yk + pitch + 0.65 > y_cab1:
        continue
    add_box(bm, (-1.0, yk + pitch - 0.15, tray_top - 0.012), (0.42, 0.30, 0.024))
obj('CABIN_TRAYS', finish(bm, 'CABIN_TRAYS', [M['TRAY']], smooth=False, bevel=0.004), C_CABIN, BODY[hk])
bm = bmesh.new()
cr, ch = CB['cup_r'], CB['cup_h']
add_lathe(bm, [(0.0, 0.0), (cr - 0.004, 0.0), (cr, 0.003), (cr, ch), (cr - 0.002, ch), (cr - 0.002, 0.004), (0.0, 0.004)], seg=48)
cup = obj('CUP', finish(bm, 'CUP', [M['CUP']], smooth=True, sharp_deg=70), C_CABIN, BODY[hk], (cupx, cupy, tray_top + 0.0005))
bm = bmesh.new()
lr = cr - 0.0025
rings = add_lathe(bm, [(0.0, 0.0045), (lr, 0.0045), (lr, CB['liquid_h']), (0.0, CB['liquid_h'])], seg=48)
liq_me = finish(bm, 'LIQUID', [M['LIQUID']], smooth=True, sharp_deg=60)
liq = obj('LIQUID', liq_me, C_CABIN, cup)
liq.shape_key_add(name='Basis'); lk = liq.shape_key_add(name='tilt')
tmax = math.tan(math.radians(CB['tilt_key_max_deg']))
for i, v in enumerate(liq.data.vertices):
    if v.co.z > CB['liquid_h'] - 1e-5:
        lk.data[i].co.z = v.co.z + v.co.x * tmax
lk.slider_min = -1.0; lk.slider_max = 1.0

lt = bpy.data.lights.new('CABIN_LIGHT', 'AREA'); lt.shape = 'RECTANGLE'; lt.size = 0.5; lt.size_y = y_cab1 - y_cab0 - 1
lt.energy = 900; lt.color = (1.0, 0.96, 0.9)
obj('CABIN_LIGHT', lt, C_CABIN, BODY[hk], (0, (y_cab0 + y_cab1) / 2, BH - 0.36))

# ------------------------------------------------------------------ ISO set (isolated bogie in the sky)
iso_o = CFG['iso']['origin']
ISO_ROOT = empty('ISO_ROOT', C_ISO, loc=tuple(iso_o)); ISO_ROOT.rotation_mode = 'QUATERNION'
ISO_PARTS = build_hero_bogie('ISO_', ISO_ROOT, C_ISO)
for a_, sy in ((1, 1), (2, -1)):
    obj(f'ISO_WHEELSET_{a_}', wheel_me, C_ISO, ISO_ROOT, (0, sy * BG['wheelbase'] / 2, zax))
for side, sx in (('L', -1), ('R', 1)):
    bm = bmesh.new(); add_cyl(bm, (0, 0, -PT / 2), SP['plate_r'], PT, seg=40)
    ISO_PARTS[f'TOP_{side}'] = obj(f'ISO_SPRING_{side}_TOP', finish(bm, f'ISO_SPRING_{side}_TOP', [M['DARK']], bevel=0.004), C_ISO, ISO_ROOT,
                                   (sx * SL, 0, FT + SP['h0']))
gb = obj('ISO_GHOST_BODY', body_mesh('ISO_GHOST_BODY', 6.0, 'mid'), C_ISO, ISO_ROOT, (0, 0, TN['body_bottom_above_rail']))
gb.data.materials.clear(); gb.data.materials.append(M['GHOST']); gb['vis'] = CFG['iso']['ghost_vis']; gb.visible_shadow = False

# cloud deck under the ISO set - rendered only during the ISO shot (reference look: parts floating above clouds)
mc = bpy.data.materials.new('MAT_CLOUD'); nt_, out_ = nodes_clear(mc)
nzc = nt_.nodes.new('ShaderNodeTexNoise'); nzc.inputs['Scale'].default_value = 0.035; nzc.inputs['Detail'].default_value = 10; nzc.inputs['Roughness'].default_value = 0.62
tcc = nt_.nodes.new('ShaderNodeTexCoord'); nt_.links.new(tcc.outputs['Object'], nzc.inputs['Vector'])
mrc = nt_.nodes.new('ShaderNodeMapRange'); mrc.inputs['From Min'].default_value = 0.42; mrc.inputs['From Max'].default_value = 0.62
nt_.links.new(nzc.outputs['Fac'], mrc.inputs['Value'])
dfc = bsdf(nt_, (0.92, 0.93, 0.95), 0.9); trc = nt_.nodes.new('ShaderNodeBsdfTransparent')
nt_.links.new(mix_shader(nt_, mrc.outputs[0], trc.outputs[0], dfc.outputs[0]), out_.inputs[0])
bm = bmesh.new(); add_box(bm, (0, 0, 0), (6000, 6000, 0.01))
cloud = obj('CLOUD_DECK', finish(bm, 'CLOUD_DECK', [mc], smooth=False), C_ISO, loc=(iso_o[0], iso_o[1], iso_o[2] + CFG['iso']['cloud_deck_z']))
cloud.visible_shadow = False
cv0, cv1 = CFG['iso']['cloud_visible_F']
bake_fcurves(cloud, FR, {'hide_render': np.where((FR >= cv0) & (FR <= cv1), 0.0, 1.0)}, interp_const=True)

# ------------------------------------------------------------------ WORLD + SUN
W = bpy.data.worlds.new('WORLD_R025') if not bpy.data.worlds else bpy.data.worlds[0]
SC.world = W; W.use_nodes = True
nt = W.node_tree
for n in list(nt.nodes):
    nt.nodes.remove(n)
wo = nt.nodes.new('ShaderNodeOutputWorld')
sky = nt.nodes.new('ShaderNodeTexSky'); sky.sky_type = SKY_SINGLE; sky.sun_disc = False
sky.sun_elevation = math.radians(38); sky.sun_rotation = math.radians(230)
setattr(sky, SKY_DUST, 0.8); sky.altitude = 50
bg_l = nt.nodes.new('ShaderNodeBackground'); bg_l.inputs['Strength'].default_value = 0.55
nt.links.new(sky.outputs[0], bg_l.inputs[0])
tc = nt.nodes.new('ShaderNodeTexCoord'); sx_ = nt.nodes.new('ShaderNodeSeparateXYZ')
nt.links.new(tc.outputs['Generated'], sx_.inputs[0])
ramp = nt.nodes.new('ShaderNodeValToRGB'); cr_ = ramp.color_ramp
cr_.elements[0].position = 0.0; cr_.elements[0].color = (0.62, 0.70, 0.78, 1)
cr_.elements[1].position = 0.55; cr_.elements[1].color = (0.16, 0.33, 0.62, 1)
nt.links.new(sx_.outputs['Z'], ramp.inputs[0])
nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 3.5; nz.inputs['Detail'].default_value = 8; nz.inputs['Roughness'].default_value = 0.6
nt.links.new(tc.outputs['Generated'], nz.inputs['Vector'])
cl = nt.nodes.new('ShaderNodeMapRange'); cl.inputs['From Min'].default_value = 0.55; cl.inputs['From Max'].default_value = 0.75
nt.links.new(nz.outputs['Fac'], cl.inputs['Value'])
hor = nt.nodes.new('ShaderNodeMapRange'); hor.inputs['From Min'].default_value = 0.0; hor.inputs['From Max'].default_value = 0.25
nt.links.new(sx_.outputs['Z'], hor.inputs['Value'])
cm_ = nt.nodes.new('ShaderNodeMath'); cm_.operation = 'MULTIPLY'
nt.links.new(cl.outputs[0], cm_.inputs[0]); nt.links.new(hor.outputs[0], cm_.inputs[1])
mixc = nt.nodes.new('ShaderNodeMix'); mixc.data_type = 'RGBA'
nt.links.new(cm_.outputs[0], mixc.inputs['Factor']); nt.links.new(ramp.outputs[0], mixc.inputs[6]); mixc.inputs[7].default_value = (0.95, 0.96, 0.98, 1)
bg_c = nt.nodes.new('ShaderNodeBackground'); bg_c.inputs['Strength'].default_value = 1.0
nt.links.new(mixc.outputs[2], bg_c.inputs[0])
lp = nt.nodes.new('ShaderNodeLightPath')
ms = nt.nodes.new('ShaderNodeMixShader')
nt.links.new(lp.outputs['Is Camera Ray'], ms.inputs[0]); nt.links.new(bg_l.outputs[0], ms.inputs[1]); nt.links.new(bg_c.outputs[0], ms.inputs[2])
nt.links.new(ms.outputs[0], wo.inputs[0])

sun = bpy.data.lights.new('SUN', 'SUN'); sun.energy = 3.6; sun.angle = math.radians(0.8); sun.color = (1.0, 0.97, 0.92)
so = obj('SUN', sun, C_LIGHT)
sdir = Vector((-0.62, 0.42, 0.66)).normalized()          # towards the sun: left-front-up of the train's start heading
so.rotation_mode = 'QUATERNION'; so.rotation_quaternion = sdir.to_track_quat('Z', 'Y')

# ------------------------------------------------------------------ APPLY BAKE
def q(arr):
    return np.asarray(arr)


for k in range(nc):
    bake_fcurves(BODY[k], FR, {'location': D['body_loc'][k], 'rotation_quaternion': D['body_quat'][k]})
    for j in range(2):
        bake_fcurves(BOGIES[(k, j)], FR, {'location': D['bog_loc'][k, j], 'rotation_quaternion': D['bog_quat'][k, j]})
        for w in WHEELS[(k, j)]:
            bake_fcurves(w, FR, {'rotation_euler': np.stack([D['wheel_angle'][k, j], np.zeros(len(FR)), np.zeros(len(FR))], 1)})
bake_fcurves(GHOST, FR, {'location': D['ghost_loc'], 'rotation_quaternion': D['ghost_quat'], '["vis"]': D['ghost_vis']})
for s_ in SKIRTS_HERO:
    bake_fcurves(s_, FR, {'["xray"]': D['skirt_xray']})
for side in ('L', 'R'):
    bake_fcurves(HERO_PARTS[f'BELLOWS_{side}'].data.shape_keys, FR, {'key_blocks["stroke"].value': D[f'stroke_{side}']})
    ISO_PARTS[f'BELLOWS_{side}'].data.shape_keys.key_blocks['stroke'].value = (SP['h0'] - SP['h_min']) / (SP['h_max'] - SP['h_min'])
bake_fcurves(liq.data.shape_keys, FR, {'key_blocks["tilt"].value': D['liquid_key']})
bake_fcurves(ISO_ROOT, FR, {'rotation_quaternion': D['iso_quat']})
ex = CFG['explode']['offsets']
e = D['explode']
for side, sx in (('L', -1), ('R', 1)):
    for part, key in (('TOP', 'SPRING_TOP'), ('BELLOWS', 'BELLOWS'), ('AUXRES', 'AUXRES'), ('LVALVE', 'LVALVE'), ('LROD', 'LROD')):
        o = ISO_PARTS[f'{part}_{side}']
        base = np.array(o.location)
        off = np.array(ex[key], float)
        if side == 'R':
            off[0] = -off[0]                      # config offsets are written for the left side
        bake_fcurves(o, FR, {'location': base[None, :] + e[:, None] * off[None, :]})

# ------------------------------------------------------------------ CAMERAS + MARKERS
SC.timeline_markers.clear()
sens = CFG['spec']['sensor_height_mm']
for shot in CAMS['shots']:
    cid = shot['id']
    cd = bpy.data.cameras.new(f'CAM_{cid}')
    cd.sensor_fit = 'VERTICAL'; cd.sensor_height = sens; cd.sensor_width = sens
    cd.clip_start = 0.02; cd.clip_end = 6000
    cd.dof.use_dof = True
    co = obj(f'CAM_{cid}', cd, C_CAM); co.rotation_mode = 'QUATERNION'
    Fr = D[f'cam_{cid}_F']
    bake_fcurves(co, Fr, {'location': D[f'cam_{cid}_loc'], 'rotation_quaternion': D[f'cam_{cid}_quat']})
    bake_fcurves(cd, Fr, {'lens': D[f'cam_{cid}_lens'], 'dof.aperture_fstop': D[f'cam_{cid}_fstop'],
                          'dof.focus_distance': D[f'cam_{cid}_focus']})
    mk = SC.timeline_markers.new(cid, frame=shot['F'][0]); mk.camera = co
SC.camera = bpy.data.objects[f'CAM_{CAMS["shots"][0]["id"]}']

# ------------------------------------------------------------------ RENDER DEFAULTS (stage presets live in render_frames.py)
R = SC.render
R.engine = 'CYCLES'
R.resolution_x, R.resolution_y = CFG['spec']['resolution']
R.resolution_percentage = 25
R.use_motion_blur = True; R.motion_blur_shutter = 0.5
R.dither_intensity = 1.0
R.film_transparent = False
SC.cycles.samples = 6; SC.cycles.use_denoising = True; SC.cycles.denoiser = 'OPENIMAGEDENOISE'
SC.cycles.max_bounces = 6; SC.cycles.diffuse_bounces = 2; SC.cycles.glossy_bounces = 2
SC.cycles.transmission_bounces = 6; SC.cycles.transparent_max_bounces = 12
SC.cycles.use_adaptive_sampling = True
SC.view_settings.view_transform = 'AgX'; SC.view_settings.look = 'AgX - Medium High Contrast'
R.use_persistent_data = True
R.image_settings.file_format = 'PNG'; R.image_settings.color_depth = '8'

# ------------------------------------------------------------------ sanity: things actually move (black-frame trap)
for f in (1, 300):
    SC.frame_set(f)
    cam = SC.camera
    print(f'F{f}: BODY_01 {tuple(round(x, 2) for x in BODY[hk].matrix_world.translation)} '
          f'CAM_C01 {tuple(round(x, 2) for x in bpy.data.objects["CAM_C01"].matrix_world.translation)}')

os.makedirs(os.path.dirname(os.path.abspath(A.out)), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(A.out), compress=True)       # ops exception: save
print('BUILD OK', os.path.abspath(A.out), 'objects', len(bpy.data.objects))
