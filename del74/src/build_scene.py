"""DEL74 씬 빌드 (그레이박스 + 리그 + 재질 + 카메라 + 패스). bpy.ops는 저장에만 사용.
실행: blender -b -P build_scene.py -- [--out ../render/del74_scene.blend]
      또는 bpy 모듈: python build_scene.py
입력: rig_config.json, materials.json, del74_bake.npz (유일한 운동 입력), camera_keys.json(메타만)."""
import bpy, json, math, os, sys
import numpy as np
from mathutils import Vector, Matrix
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import anim, geo

LOCK = (4, 5)
assert bpy.app.version[:2] == LOCK, f"Blender {bpy.app.version_string} != LOCK {LOCK}"
V5 = bpy.app.version >= (5, 0, 0)
EEVEE_ID = 'BLENDER_EEVEE' if V5 else 'BLENDER_EEVEE_NEXT'
SKY_SINGLE = 'SINGLE_SCATTERING' if V5 else 'NISHITA'
SKY_DUST = 'aerosol_density' if V5 else 'dust_density'

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = os.path.join(ROOT, 'render', 'del74_scene.blend')
if '--out' in argv: OUT = argv[argv.index('--out') + 1]

cfg = json.load(open(os.path.join(HERE, 'rig_config.json'), encoding='utf-8'))
MAT = json.load(open(os.path.join(HERE, 'materials.json'), encoding='utf-8'))
B = np.load(os.path.join(HERE, 'del74_bake.npz'))
def V(*k):
    n = cfg
    for key in k: n = n[key]
    return n['v'] if isinstance(n, dict) and 'v' in n else n
FR = B['frames']; fps = cfg['fps']; N = cfg['total_frames']
ix = lambda f: int(np.where(FR == f)[0][0])

# ---------------- 씬 초기화 ----------------
scn = bpy.context.scene
for ob in list(bpy.data.objects): bpy.data.objects.remove(ob, do_unlink=True)
for c in list(bpy.data.collections): bpy.data.collections.remove(c)
for m in list(bpy.data.materials): bpy.data.materials.remove(m)
scn.frame_start, scn.frame_end, scn.render.fps = 1, N, fps
scn.unit_settings.system, scn.unit_settings.scale_length = 'METRIC', 1.0
scn.render.resolution_x, scn.render.resolution_y, scn.render.resolution_percentage = 1080, 1920, 100
np.random.seed(74)

def coll(name, parent=None):
    c = bpy.data.collections.new(name); (parent or scn.collection).children.link(c); return c
C_LOCO, C_BOGIE_PROTO, C_CARS, C_TRACK, C_GHOST, C_CAM, C_CUTTERS, C_RIMS = [coll(n) for n in ['LOCO', 'BOGIE_PROTO', 'CARS', 'TRACK', 'GHOSTS', 'CAMERA', 'CUTTERS', 'RIMS']]
C_ENGINE = coll('ENGINE', C_LOCO); C_GEN = coll('GENERATOR', C_LOCO); C_BODY = coll('BODY', C_LOCO); C_CABLE = coll('CABLE', C_LOCO)
C_ISO = coll('ISO_PARTS', C_BOGIE_PROTO)   # C08 고립에서 남는 부품(차축1 조립체)
def link(ob, c):
    c.objects.link(ob); return ob

# ---------------- 재질 ----------------
def principled(name, spec):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    bsdf = nt.nodes['Principled BSDF']
    bsdf.inputs['Base Color'].default_value = (*spec['base_color'], 1.0)
    bsdf.inputs['Roughness'].default_value = spec['roughness']; bsdf.inputs['Metallic'].default_value = spec['metallic']
    if spec.get('anisotropic'): bsdf.inputs['Anisotropic'].default_value = spec['anisotropic']
    if spec.get('noise_bump', 0) > 0:
        tex = nt.nodes.new('ShaderNodeTexNoise'); tex.inputs['Scale'].default_value = 40.0; tex.inputs['Detail'].default_value = 6.0
        bump = nt.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.08 * spec['noise_bump']
        nt.links.new(tex.outputs['Fac'], bump.inputs['Height']); nt.links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    if spec.get('edge_wear', 0) > 0:
        # pointiness 엣지 마모: 굽힌 베벨 지오메트리 기준(모디파이어 아님)
        g = nt.nodes.new('ShaderNodeNewGeometry'); ramp = nt.nodes.new('ShaderNodeValToRGB')
        ramp.color_ramp.elements[0].position = 0.5; ramp.color_ramp.elements[1].position = 0.5 + spec['edge_wear'] * 10
        mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'; mix.inputs[6].default_value = (*spec['base_color'], 1); mix.inputs[7].default_value = (0.7, 0.7, 0.7, 1)
        nt.links.new(g.outputs['Pointiness'], ramp.inputs['Fac']); nt.links.new(ramp.outputs['Color'], mix.inputs[0]); nt.links.new(mix.outputs[2], bsdf.inputs['Base Color'])
    m.pass_index = 0
    return m
M = {k: principled(k, v) for k, v in MAT.items() if k.startswith('M_') and k not in ('M_GHOST', 'M_SKY')}
# 외피 고스트: Value "skin_ghost" 베이크 → Mix(Paint, Glass) / Is Camera Ray 분기(조명·그림자는 불투명 유지)
def ghost_material():
    """외피 고스트. 카메라 레이: Transparent+Glass(프레넬) 얇은 껍질 / 그림자 레이: Transparent(햇빛이 내부로 들어옴) / 그 외 레이: 불투명 도장.
    skin_ghost(베이크)로 Mix. 실내가 검게 되는 함정(불투명 외피 안에 빛이 못 들어옴)을 그림자 레이 분기로 막는다."""
    spec = MAT['M_GHOST']; base = MAT[spec['base']]
    m = bpy.data.materials.new('M_GHOST'); m.use_nodes = True; nt = m.node_tree
    out = nt.nodes['Material Output']; paint = nt.nodes['Principled BSDF']
    paint.inputs['Base Color'].default_value = (*base['base_color'], 1); paint.inputs['Roughness'].default_value = base['roughness']
    glass = nt.nodes.new('ShaderNodeBsdfGlass'); glass.inputs['IOR'].default_value = spec['glass_ior']; glass.inputs['Roughness'].default_value = spec['glass_roughness']; glass.inputs['Color'].default_value = (*spec['tint'], 1)
    transp = nt.nodes.new('ShaderNodeBsdfTransparent'); transp.inputs['Color'].default_value = (*spec['tint'], 1)
    fres = nt.nodes.new('ShaderNodeFresnel'); fres.inputs['IOR'].default_value = spec['glass_ior']
    fmul = nt.nodes.new('ShaderNodeMath'); fmul.operation = 'MULTIPLY'; fmul.inputs[1].default_value = 0.5
    shell = nt.nodes.new('ShaderNodeMixShader')          # 카메라용 껍질: Transparent ↔ Glass by fresnel*0.5
    nt.links.new(fres.outputs[0], fmul.inputs[0]); nt.links.new(fmul.outputs[0], shell.inputs[0]); nt.links.new(transp.outputs[0], shell.inputs[1]); nt.links.new(glass.outputs[0], shell.inputs[2])
    val = nt.nodes.new('ShaderNodeValue'); val.name = 'skin_ghost'; val.outputs[0].default_value = 0.0
    lp = nt.nodes.new('ShaderNodeLightPath')
    mix_cam = nt.nodes.new('ShaderNodeMixShader'); mix_shadow = nt.nodes.new('ShaderNodeMixShader'); sel_shadow = nt.nodes.new('ShaderNodeMixShader'); sel_cam = nt.nodes.new('ShaderNodeMixShader')
    nt.links.new(val.outputs[0], mix_cam.inputs[0]); nt.links.new(paint.outputs[0], mix_cam.inputs[1]); nt.links.new(shell.outputs[0], mix_cam.inputs[2])
    nt.links.new(val.outputs[0], mix_shadow.inputs[0]); nt.links.new(paint.outputs[0], mix_shadow.inputs[1]); nt.links.new(transp.outputs[0], mix_shadow.inputs[2])
    nt.links.new(lp.outputs['Is Shadow Ray'], sel_shadow.inputs[0]); nt.links.new(paint.outputs[0], sel_shadow.inputs[1]); nt.links.new(mix_shadow.outputs[0], sel_shadow.inputs[2])
    nt.links.new(lp.outputs['Is Camera Ray'], sel_cam.inputs[0]); nt.links.new(sel_shadow.outputs[0], sel_cam.inputs[1]); nt.links.new(mix_cam.outputs[0], sel_cam.inputs[2])
    nt.links.new(sel_cam.outputs[0], out.inputs['Surface'])
    m.use_backface_culling = True
    anim.bake_node_value(m, 'skin_ghost', FR, B['skin_ghost'])
    return m
M['M_GHOST'] = ghost_material()
# 케이블: 정점 속성 u → AOV 'electric' (발광 아님, 후합성 마스크)
def cable_material():
    m = principled('M_CABLE_AOV', MAT['M_CABLE']); nt = m.node_tree
    attr = nt.nodes.new('ShaderNodeAttribute'); attr.attribute_name = 'u'
    aov = nt.nodes.new('ShaderNodeOutputAOV'); aov.aov_name = 'electric'
    nt.links.new(attr.outputs['Fac'], aov.inputs['Value'])
    return m
M['M_CABLE_AOV'] = cable_material()
M['M_GHOST_PART'] = principled('M_GHOST_PART', {'base_color': [0.5, 0.5, 0.5], 'roughness': 0.5, 'metallic': 0.0})  # GHOST 뷰레이어 전용 불투명 더미
def setmat(ob, *mats):
    for mm in mats: ob.data.materials.append(M[mm])
    return ob

# ---------------- 기관차 ----------------
LOCO = bpy.data.objects.new('LOCO', None); link(LOCO, C_LOCO)
anim.bake_fcurves(LOCO, FR, {'location': np.stack([B['loco_x'], np.zeros_like(FR), np.zeros_like(FR)], 1)})
Lb, Wb, Hb = V('loco', 'length_body'), V('loco', 'width'), V('loco', 'height'); deck = V('loco', 'deck_z'); ufb = V('loco', 'underframe_bottom_z')
def child(ob, parent, c):
    ob.parent = parent; link(ob, c); return ob
# 외피: 장후드(캡 뒤) + 캡 + 단후드. 실제 외피는 G-ASSET-1 에셋으로 교체(import_assets.py). 프록시는 바닥 없는 쉘.
cab = V('loco', 'cab_x')
BODY = child(setmat(geo.box('BODY_HOOD', (cab[0] - (-Lb / 2), Wb * 0.78, Hb - deck), ((cab[0] + (-Lb / 2)) / 2, 0, deck + (Hb - deck) / 2), bevel=0.04), 'M_GHOST'), LOCO, C_BODY)
CAB = child(setmat(geo.box('BODY_CAB', (cab[1] - cab[0], Wb, Hb - deck), ((cab[0] + cab[1]) / 2, 0, deck + (Hb - deck) / 2), bevel=0.05), 'M_GHOST'), LOCO, C_BODY)
NOSE = child(setmat(geo.box('BODY_NOSE', (Lb / 2 - cab[1], Wb * 0.8, 2.2), ((cab[1] + Lb / 2) / 2, 0, deck + 1.1), bevel=0.04), 'M_GHOST'), LOCO, C_BODY)
DECK = child(setmat(geo.box('DECK', (Lb, Wb, deck - ufb), (0, 0, (deck + ufb) / 2), bevel=0.02), 'M_GHOST'), LOCO, C_BODY)
for ob in (BODY, CAB, NOSE, DECK): ob.pass_index = 1
# 엔진: 블록(프록시) + 크랭크 + 피스톤 16 + 로드 16
ex = V('loco', 'engine_x'); cz = V('loco', 'crank_axis_z'); r = V('engine', 'crank_radius'); l = V('engine', 'rod_length')
half = math.radians(V('engine', 'bank_angle_deg')) / 2; pitch = V('engine', 'throw_pitch_x'); x0 = V('engine', 'crank_x0'); bore = V('engine', 'bore')
BLOCK = child(setmat(geo.box('ENGINE_BLOCK', (ex[1] - ex[0], 1.6, 2.4), ((ex[0] + ex[1]) / 2, 0, cz + 0.5), bevel=0.03), 'M_CAST'), LOCO, C_ENGINE); BLOCK.pass_index = 2
crank_cx = (ex[0] + ex[1]) / 2 + 0.15
CRANK = bpy.data.objects.new('CRANK_SHAFT', None); CRANK.location = (crank_cx, 0, cz); child(CRANK, LOCO, C_ENGINE)   # 회전 루트(엠프티), 원점=크랭크 축선
nthrow = V('engine', 'throws')
for k in range(nthrow + 1):   # 주저널: 스로 사이 + 양끝
    xa = (x0 - pitch) + k * pitch + 0.19; xb = xa + pitch - 0.38
    if k == 0: xa = x0 - 0.75
    if k == nthrow: xb = x0 + (nthrow - 1) * pitch + 0.75
    J = setmat(geo.cylinder(f'CRANK_JOURNAL_{k:02d}', 0.075, xb - xa, 'X', ((xa + xb) / 2 - crank_cx, 0, 0), bevel=0.005), 'M_MACH'); J.parent = CRANK; link(J, C_ENGINE)
anim.bake_fcurves(CRANK, FR, {'rotation_euler': np.stack([B['crank_theta'], np.zeros_like(FR), np.zeros_like(FR)], 1)})
phases = np.deg2rad(V('engine', 'throw_phase_deg'))
for k in range(V('engine', 'throws')):
    xk = x0 + k * pitch
    web = setmat(geo.box(f'CRANK_WEB_{k+1:02d}', (0.16, 0.30, 2 * r + 0.24), (xk - crank_cx, 0, 0), bevel=0.01), 'M_CAST')   # 크랭크 로컬: 원점이 크랭크 축 위, 핀은 +Z에서 phase만큼 회전
    pin = setmat(geo.cylinder(f'CRANK_PIN_{k+1:02d}', 0.06, 0.34, 'X', (xk - crank_cx, 0, 0), bevel=0.005), 'M_MACH')
    for ob in (web, pin):
        ob.parent = CRANK; link(ob, C_ENGINE)
        # 웹·핀은 자기 스로 위상만큼 X축 회전(정적), 핀 중심은 반경 r
        ob.rotation_euler = (phases[k], 0, 0)
    pin.data.transform(Matrix.Translation((0, 0, r)))     # 핀을 반경 위치로
    web.data.transform(Matrix.Translation((0, 0, r / 2 - 0.02)))
pist = B['piston']
for i in range(V('engine', 'cylinders')):
    k = i // 2; bank = +half if i % 2 == 0 else -half
    xk = x0 + k * pitch + (0.14 if i % 2 == 0 else -0.14)
    b_dir = np.array([0.0, math.sin(bank), math.cos(bank)])
    P = child(setmat(geo.cylinder(f'PISTON_{i+1:02d}', bore / 2 - 0.0005, 0.26, 'Z', (0, 0, 0.13), bevel=0.004), 'M_MACH'), LOCO, C_ENGINE)
    P.rotation_euler = (-bank, 0, 0)   # 로컬 +Z를 뱅크 축으로
    loc = np.stack([np.full_like(FR, xk), cz * 0 + pist[:, i] * b_dir[1], cz + pist[:, i] * b_dir[2]], 1)
    anim.bake_fcurves(P, FR, {'location': loc})
    ROD = child(setmat(geo.cylinder(f'ROD_{i+1:02d}', 0.035, l, 'Z', (0, 0, l / 2), bevel=0.003), 'M_MACH'), LOCO, C_ENGINE)
    phi = B['crank_theta'] + phases[k]
    pin_y, pin_z = r * np.sin(phi), r * np.cos(phi)
    vy, vz = pist[:, i] * b_dir[1] - pin_y, pist[:, i] * b_dir[2] - pin_z
    rodrot = anim.continuous_euler(np.stack([np.arctan2(-vy, vz), np.zeros_like(FR), np.zeros_like(FR)], 1))
    anim.bake_fcurves(ROD, FR, {'location': np.stack([np.full_like(FR, xk), pin_y, cz + pin_z], 1), 'rotation_euler': rodrot})
    LINER = child(setmat(geo.tube(f'LINER_{i+1:02d}', bore / 2 + 0.02, bore / 2, 0.40, 'Z', (0, 0, 0)), 'M_CAST'), LOCO, C_ENGINE)
    LINER.rotation_euler = (-bank, 0, 0); LINER.location = (xk, (r + l + 0.05) * b_dir[1], cz + (r + l + 0.05) * b_dir[2]); LINER.pass_index = 2
# 엔진 공회전 진동(가정 씬): 블록 Z
anim.bake_fcurves(BLOCK, FR, {'location': np.stack([np.zeros_like(FR), np.zeros_like(FR), B['engine_vib']], 1)})
# 발전기: 회전자(크랭크 1:1) + 고정자 코일(구리) + 케이스(커터 링 불리언)
gx = V('generator', 'rotor_x'); gr = V('generator', 'rotor_radius'); gcr = V('generator', 'case_radius'); flange = V('engine', 'coupling_flange_x')
ROTOR = child(setmat(geo.cylinder('GEN_ROTOR', gr, gx[1] - gx[0], 'X', ((gx[0] + gx[1]) / 2, 0, cz), segments=64, bevel=0.01), 'M_CAST'), LOCO, C_GEN)
for s in range(12):   # 회전자 극편(회전 가시화)
    a = 2 * math.pi * s / 12
    pole = setmat(geo.box(f'GEN_POLE_{s+1:02d}', (gx[1] - gx[0] - 0.2, 0.12, 0.08), (0, (gr + 0.04) * math.sin(a), (gr + 0.04) * math.cos(a)), bevel=0.005), 'M_COPPER')
    pole.rotation_euler = (a, 0, 0); pole.parent = ROTOR; link(pole, C_GEN)   # 회전자 로컬(원점=회전축)
anim.bake_fcurves(ROTOR, FR, {'rotation_euler': np.stack([B['rotor_gen'], np.zeros_like(FR), np.zeros_like(FR)], 1)})
SHAFT_C = child(setmat(geo.cylinder('COUPLING_SHAFT', 0.11, gx[0] - ex[1] + 0.4, 'X', ((ex[1] + gx[0]) / 2 - 0.0, 0, cz), bevel=0.01), 'M_MACH'), LOCO, C_GEN)
anim.bake_fcurves(SHAFT_C, FR, {'rotation_euler': np.stack([B['crank_theta'], np.zeros_like(FR), np.zeros_like(FR)], 1)})
FLANGE = child(setmat(geo.cylinder('COUPLING_FLANGE', 0.26, 0.08, 'X', (flange, 0, cz), bevel=0.01), 'M_MACH'), LOCO, C_GEN)
anim.bake_fcurves(FLANGE, FR, {'rotation_euler': np.stack([B['crank_theta'], np.zeros_like(FR), np.zeros_like(FR)], 1)})
STATOR = child(setmat(geo.tube('GEN_STATOR', gr + 0.25, gr + 0.10, gx[1] - gx[0] - 0.1, 'X', ((gx[0] + gx[1]) / 2, 0, cz)), 'M_COPPER'), LOCO, C_GEN)
CASE = child(setmat(geo.tube('GEN_CASE', gcr, gr + 0.28, gx[1] - gx[0] + 0.2, 'X', ((gx[0] + gx[1]) / 2, 0, cz)), 'M_CAST'), LOCO, C_GEN); CASE.pass_index = 3
# 케이블 6본
cpath = V('cable', 'path_xyz'); cr_ = V('cable', 'radius')
for i in range(V('cable', 'count')):
    off = np.array([0, 0.03 * (i - 2.5) * 0.9, 0.045 * (i % 2)])
    pts = [np.array(p) + off for p in cpath]
    CAB_i = child(setmat(geo.polyline_tube(f'CABLE_{i+1:02d}', pts, cr_), 'M_CABLE_AOV'), LOCO, C_CABLE); CAB_i.pass_index = 4
hole = link(geo.cylinder('CUT_DECK_CABLE', V('cable', 'deck_hole_radius'), 1.0, 'Z', tuple(V('cable', 'deck_hole_xy')) + (deck - 0.15,), segments=32), C_CUTTERS)
hole.parent = LOCO; hole.display_type = 'WIRE'; hole.hide_render = True; hole.visible_camera = False
md = DECK.modifiers.new('deck_cable_hole', 'BOOLEAN'); md.object = hole; md.operation = 'DIFFERENCE'; md.solver = 'EXACT'
TERM = child(setmat(geo.box('GEN_TERMINAL', (0.25, 0.18, 0.12), tuple(V('generator', 'terminal_xyz')), bevel=0.01), 'M_COPPER'), LOCO, C_CABLE)
JBOX = child(setmat(geo.box('JUNCTION_BOX', (0.3, 0.25, 0.2), tuple(V('cable', 'junction_box_xyz')), bevel=0.01), 'M_DARK'), LOCO, C_CABLE)
# 연결기(기관차 후미)
Lc = V('loco', 'length_over_couplers'); ch_ = V('loco', 'coupler_height')
CPL_L = child(setmat(geo.box('CPL_LOCO_REAR', (0.55, 0.16, 0.16), (-Lc / 2 + 0.275, 0, ch_), bevel=0.01), 'M_MACH'), LOCO, C_BODY)
kc = V('coupler', 'knuckle_clearance')
KN_L = child(setmat(geo.box('KNUCKLE_LOCO_REAR', (0.24, 0.12, 0.24), (-Lc / 2 + 0.04, 0.06 + kc / 2, ch_), bevel=0.01), 'M_MACH'), LOCO, C_BODY)   # 너클은 좌우로 맞물림(y 간극 = knuckle_clearance), 유격은 x 방향 미끄럼으로 보임

# ---------------- 대차 프로토타입 (원점 = 대차 중심, 레일면) ----------------
R = V('wheel', 'radius'); sink = V('wheel', 'sink'); gauge = V('wheel', 'gauge_inner_rail'); tw = V('wheel', 'tread_width')
axles = V('pivots', 'axle_offsets_in_bogie'); gr_ = V('drive', 'gear_pitch_radius'); pr_ = V('drive', 'pinion_pitch_radius')
gy = V('drive', 'gear_side_y'); mr = V('drive', 'motor_housing_radius'); ml = V('drive', 'motor_length'); fw = V('drive', 'gear_face_width')
BOGIE_FRAME = link(setmat(geo.box('BOGIE_FRAME', (V('pivots', 'fixed_wheelbase') + 1.0, 2.6, 0.30), (0, 0, R + 0.35), bevel=0.02), 'M_CAST'), C_BOGIE_PROTO); BOGIE_FRAME.pass_index = 5
for side in (-1, 1):
    link(setmat(geo.box(f'BOGIE_SIDEFRAME_{"L" if side > 0 else "R"}', (V('pivots', 'fixed_wheelbase') + 1.2, 0.18, 0.55), (0, side * 1.25, R + 0.15), bevel=0.02), 'M_CAST'), C_BOGIE_PROTO)
wheel_rot = np.stack([np.zeros_like(FR), -B['wheel_theta'], np.zeros_like(FR)], 1)   # +X 진행 → Y축 음의 회전
pin_rot = np.stack([np.zeros_like(FR), -B['pinion_theta'], np.zeros_like(FR)], 1)
for a, ax in enumerate(axles):
    grp = C_ISO if a == 2 else C_BOGIE_PROTO     # 앞 대차 1축(=전방, +x 쪽) 조립체는 C08 고립용
    AX = link(setmat(geo.cylinder(f'AXLE_{a+1:02d}', 0.09, gauge + 0.5, 'Y', (ax, 0, R - sink), bevel=0.005), 'M_DARK'), grp)
    anim.bake_fcurves(AX, FR, {'rotation_euler': wheel_rot})
    for side in (-1, 1):
        W = setmat(geo.cylinder(f'WHEEL_{a+1:02d}_{"L" if side > 0 else "R"}', R, tw, 'Y', (0, side * (gauge / 2 + tw / 2 - 0.02), 0), segments=96, bevel=0.01), 'M_MACH')
        W.parent = AX; link(W, grp)
        FL = setmat(geo.cylinder(f'FLANGE_{a+1:02d}_{"L" if side > 0 else "R"}', R + 0.028, 0.03, 'Y', (0, side * (gauge / 2 + tw - 0.02 + 0.015), 0), segments=96), 'M_DARK')
        FL.parent = AX; link(FL, grp)
        BOXJ = link(setmat(geo.box(f'AXLEBOX_{a+1:02d}_{"L" if side > 0 else "R"}', (0.42, 0.26, 0.42), (ax, side * (gauge / 2 + tw + 0.16), R - sink), bevel=0.02), 'M_CAST'), grp)
    G = setmat(geo.gear(f'GEAR_{a+1:02d}', gr_, V('drive', 'gear_teeth'), fw, 'Y', (0, gy, 0)), 'M_DARK', 'M_MACH'); G.parent = AX; link(G, grp)
    mx = ax - (gr_ + pr_ + V('drive', 'tooth_clearance')) * (1 if ax > 0 else -1)   # 전동기는 대차 중심 쪽(피치원 접촉 + 치면 간극)
    MOT = link(setmat(geo.cylinder(f'MOTOR_{a+1:02d}', mr, ml, 'Y', (mx, -0.1, R - sink), segments=64, bevel=0.02), 'M_CAST'), grp); MOT.pass_index = 20 + a
    PIN = link(setmat(geo.gear(f'PINION_{a+1:02d}', pr_, V('drive', 'pinion_teeth'), fw, 'Y', (mx, gy, R - sink)), 'M_DARK', 'M_MACH'), grp)
    ph = 0.0 if ax > 0 else math.pi / V('drive', 'pinion_teeth')   # 피니언이 -X(ax>0) 쪽이면 대치차 톱니(각 π)↔피니언 홈(각 0) 정렬, +X 쪽이면 반피치 보정
    anim.bake_fcurves(PIN, FR, {'rotation_euler': pin_rot + np.array([0, ph, 0])})
    RTR = link(setmat(geo.cylinder(f'MOTOR_ROTOR_{a+1:02d}', mr * 0.55, ml * 0.8, 'Y', (mx, -0.1, R - sink), segments=48), 'M_MACH'), grp)
    anim.bake_fcurves(RTR, FR, {'rotation_euler': np.stack([np.zeros_like(FR), -B['rotor_motor'][:, a], np.zeros_like(FR)], 1)})
BOGIE_F = bpy.data.objects.new('BOGIE_FRONT', None); BOGIE_F.instance_type = 'COLLECTION'; BOGIE_F.instance_collection = C_BOGIE_PROTO
BOGIE_R = bpy.data.objects.new('BOGIE_REAR', None); BOGIE_R.instance_type = 'COLLECTION'; BOGIE_R.instance_collection = C_BOGIE_PROTO
bc = V('pivots', 'bogie_center_half')
BOGIE_F.location = (bc, 0, 0); BOGIE_R.location = (-bc, 0, 0)
for bg in (BOGIE_F, BOGIE_R): bg.parent = LOCO; link(bg, C_LOCO)
scn.collection.children.unlink(C_BOGIE_PROTO)   # 프로토타입은 인스턴스로만 보임
# 가정 구동축 (유령): 홀드아웃 대신 GHOST 뷰레이어에서만 렌더
H = cfg['hypothetical_shaft']; hx0, hx1, hz, hr = V('hypothetical_shaft', 'x_engine_end'), V('hypothetical_shaft', 'x_axle_end'), V('hypothetical_shaft', 'axis_z'), V('hypothetical_shaft', 'radius')
GS = child(setmat(geo.cylinder('GHOST_SHAFT', hr, abs(hx1 - hx0), 'X', ((hx0 + hx1) / 2, 0, hz)), 'M_GHOST_PART'), LOCO, C_GHOST); GS.pass_index = 11
anim.bake_fcurves(GS, FR, {'location': np.stack([B['ghost_x'] + (hx0 + hx1) / 2, np.zeros_like(FR), np.full_like(FR, hz)], 1), 'rotation_euler': np.stack([B['ghost_theta'], np.zeros_like(FR), np.zeros_like(FR)], 1)})
anim.bake_fcurves(GS, FR, {'hide_render': (B['ghost_vis'] <= 0).astype(float)}, interp='CONSTANT')
GB = child(setmat(geo.box('GHOST_GEARBOX', (0.9, 0.9, 0.9), (ex[0] - 0.6, 0, cz - 0.3), bevel=0.02), 'M_GHOST_PART'), LOCO, C_GHOST); GB.pass_index = 12
GC = child(setmat(geo.cylinder('GHOST_CLUTCH', 0.45, 0.25, 'X', (flange + 0.1, 0, cz)), 'M_GHOST_PART'), LOCO, C_GHOST); GC.pass_index = 13
GD = child(setmat(geo.cylinder('GHOST_DRIVESHAFT', hr, abs(hx1 - hx0), 'X', ((hx0 + hx1) / 2, 0, hz)), 'M_GHOST_PART'), LOCO, C_GHOST); GD.pass_index = 14
for ob, key in ((GB, 'gearbox'), (GC, 'clutch'), (GD, 'driveshaft')):
    anim.bake_fcurves(ob, FR, {'hide_render': (B[key] <= 0).astype(float)}, interp='CONSTANT')
# 커터(불리언) + 림(IndexOB 전용 토러스 대용 얇은 튜브)
def cutter(name, target, center, axis, length, r_col, idx_rim, rim_parent='target'):
    cut = link(geo.cylinder(name, 1.0, length, axis, center, segments=64), C_CUTTERS)
    cut.display_type = 'WIRE'; cut.hide_render = True; cut.visible_camera = False
    cut.parent = target.parent if (target.parent and rim_parent == 'target') else None
    rr = B['cutter_r'][:, r_col]
    anim.bake_fcurves(cut, FR, {'scale': np.stack([np.maximum(rr, 1e-4)] * 3, 1)})
    mod = target.modifiers.new(name + '_bool', 'BOOLEAN'); mod.object = cut; mod.operation = 'DIFFERENCE'; mod.solver = 'EXACT'
    rim = link(setmat(geo.tube(name + '_RIM', 1.0, 0.985, length * 0.98, axis, center, segments=96), 'M_GHOST_PART'), C_RIMS)
    rim.parent = cut.parent if rim_parent == 'target' else rim_parent; rim.pass_index = idx_rim
    anim.bake_fcurves(rim, FR, {'scale': np.stack([np.maximum(rr, 1e-4)] * 3, 1), 'hide_render': (rr <= 1e-4).astype(float)}, interp='LINEAR')
    return cut
cg = cutter('CUT_GEN', CASE, ((gx[0] + gx[1]) / 2, 0.2, cz), 'Y', 4.0, 0, 30)
mod = STATOR.modifiers.new('CUT_GEN_bool_stator', 'BOOLEAN'); mod.object = cg; mod.operation = 'DIFFERENCE'; mod.solver = 'EXACT'   # 고정자도 같이 열어 회전자가 보이게
# 대차 커터: 프로토타입 로컬 좌표(프로토타입은 원점에 있으므로 월드=로컬), 불리언은 두 인스턴스에 같이 적용. 림은 앞 대차 인스턴스 엠프티에 부모.
for a, ax in enumerate(axles):
    cutter(f'CUT_AXLE_{a+1:02d}', bpy.data.objects['BOGIE_SIDEFRAME_L'], (ax, 1.25, R - sink), 'Y', 1.0, 1 + a, 31 + a, rim_parent=BOGIE_F)
cutter('CUT_MOTOR', bpy.data.objects['MOTOR_03'], (axles[2] - (gr_ + pr_ + V('drive', 'tooth_clearance')), 0.9, R - sink), 'Y', 2.0, 4, 34, rim_parent=BOGIE_F)

# ---------------- 객차 ----------------
cL, cW, cH, cfz, cR = V('car', 'length_over_couplers'), V('car', 'body_width'), V('car', 'body_height'), V('car', 'floor_z'), V('car', 'wheel_radius')
cbs = V('car', 'bogie_center_spacing'); cch = V('car', 'coupler_height')
for i in range(V('car', 'count')):
    CAR = bpy.data.objects.new(f'CAR_{i+1:02d}', None); link(CAR, C_CARS)
    anim.bake_fcurves(CAR, FR, {'location': np.stack([B['car_x'][:, i], np.zeros_like(FR), np.zeros_like(FR)], 1)})
    body = child(setmat(geo.box(f'CAR_{i+1:02d}_BODY', (cL - 1.2, cW, cH), (0, 0, cfz + cH / 2), bevel=0.05), 'M_PAINT'), CAR, C_CARS)
    for s, bx in enumerate((cbs / 2, -cbs / 2)):
        bf = child(setmat(geo.box(f'CAR_{i+1:02d}_BOGIE_{s+1}', (2.8, 2.4, 0.3), (bx, 0, cR + 0.3), bevel=0.02), 'M_CAST'), CAR, C_CARS)
        for a2, ax2 in enumerate((bx + 1.0, bx - 1.0)):
            axc = child(setmat(geo.cylinder(f'CAR_{i+1:02d}_AXLE_{s+1}{a2+1}', 0.07, gauge + 0.45, 'Y', (ax2, 0, cR - sink)), 'M_DARK'), CAR, C_CARS)
            anim.bake_fcurves(axc, FR, {'rotation_euler': np.stack([np.zeros_like(FR), -B['car_wheel_theta'][:, i], np.zeros_like(FR)], 1)})
            for side in (-1, 1):
                w = setmat(geo.cylinder(f'CAR_{i+1:02d}_WHEEL_{s+1}{a2+1}{"L" if side > 0 else "R"}', cR, 0.13, 'Y', (0, side * (gauge / 2 + 0.045), 0), segments=64), 'M_MACH')
                w.parent = axc; link(w, C_CARS)
    for e, sgn in (('F', 1), ('R', -1)):
        child(setmat(geo.box(f'CAR_{i+1:02d}_CPL_{e}', (0.55, 0.16, 0.16), (sgn * (cL / 2 - 0.275), 0, cch), bevel=0.01), 'M_MACH'), CAR, C_CARS)
        child(setmat(geo.box(f'CAR_{i+1:02d}_KNUCKLE_{e}', (0.24, 0.12, 0.24), (sgn * (cL / 2 - 0.04), -(0.06 + kc / 2) * sgn, cch), bevel=0.01), 'M_MACH'), CAR, C_CARS)

# ---------------- 궤도·지면 (고립 하강 리그) ----------------
GROUND_RIG = bpy.data.objects.new('GROUND_RIG', None); link(GROUND_RIG, C_TRACK)
anim.bake_fcurves(GROUND_RIG, FR, {'location': np.stack([np.zeros_like(FR), np.zeros_like(FR), -B['iso_drop']], 1)})
x_min, x_max = float(B['car_x'].min()) - 40, float(B['loco_x'].max()) + 60
trk_len = x_max - x_min; trk_c = (x_min + x_max) / 2
for side in (-1, 1):
    rail = child(setmat(geo.rail_profile(f'RAIL_{"L" if side > 0 else "R"}', trk_len, (trk_c, side * (gauge / 2 + 0.035), -0.15)), 'M_DARK', 'M_MACH'), GROUND_RIG, C_TRACK)
SLP = setmat(geo.box('SLEEPER_PROTO', (0.26, 2.5, 0.16), (0, 0, -0.23), bevel=0.01), 'M_GROUND')
C_SLP = coll('SLEEPER_PROTO_COL'); C_SLP.objects.link(SLP); scn.collection.children.unlink(C_SLP)
n_slp = int(trk_len / 0.6)
for k in range(n_slp):
    e = bpy.data.objects.new(f'SLEEPER_{k:04d}', None); e.instance_type = 'COLLECTION'; e.instance_collection = C_SLP
    e.location = (x_min + k * 0.6, 0, 0); e.parent = GROUND_RIG; link(e, C_TRACK)
GROUND = child(setmat(geo.box('GROUND', (trk_len + 200, 400, 0.4), (trk_c, 0, -0.51)), 'M_GROUND'), GROUND_RIG, C_TRACK)
# 자갈: 그라운드 재질에 Voronoi F1(임계 0.4) 변위 대신 범프
gnt = M['M_GROUND'].node_tree; vor = gnt.nodes.new('ShaderNodeTexVoronoi'); vor.inputs['Scale'].default_value = 25.0
thr = gnt.nodes.new('ShaderNodeMath'); thr.operation = 'LESS_THAN'; thr.inputs[1].default_value = 0.4
bmp = gnt.nodes.new('ShaderNodeBump'); bmp.inputs['Strength'].default_value = 0.35
gnt.links.new(vor.outputs['Distance'], thr.inputs[0]); gnt.links.new(thr.outputs[0], bmp.inputs['Height']); gnt.links.new(bmp.outputs['Normal'], gnt.nodes['Principled BSDF'].inputs['Normal'])

# ---------------- 하늘·조명 ----------------
world = bpy.data.worlds.new('World'); scn.world = world; world.use_nodes = True; wnt = world.node_tree
for n in list(wnt.nodes): wnt.nodes.remove(n)
wout = wnt.nodes.new('ShaderNodeOutputWorld'); sky = wnt.nodes.new('ShaderNodeTexSky'); sky.sky_type = SKY_SINGLE
S = MAT['M_SKY']; sky.sun_elevation = math.radians(S['sun_elevation_deg']); sky.sun_rotation = math.radians(S['sun_azimuth_deg']); sky.sun_disc = False
setattr(sky, SKY_DUST, 2.0)
bg_light = wnt.nodes.new('ShaderNodeBackground'); bg_light.inputs['Strength'].default_value = 0.6
bg_cam = wnt.nodes.new('ShaderNodeBackground')
grad = wnt.nodes.new('ShaderNodeTexGradient'); grad.gradient_type = 'LINEAR'
mapn = wnt.nodes.new('ShaderNodeMapping'); texco = wnt.nodes.new('ShaderNodeTexCoord')
mapn.inputs['Rotation'].default_value = (0, math.radians(90), 0)   # x' = z: 지평선 0 → 천정 1; mapn.inputs['Scale'].default_value = (1.2, 1, 1)
ramp = wnt.nodes.new('ShaderNodeValToRGB'); ramp.color_ramp.elements[0].color = (*S['horizon'], 1); ramp.color_ramp.elements[1].color = (*S['zenith'], 1); ramp.color_ramp.elements[0].position = S.get('horizon_pos', 0.12); ramp.color_ramp.elements[1].position = S.get('zenith_pos', 0.65)
cloud = wnt.nodes.new('ShaderNodeTexNoise'); cloud.inputs['Scale'].default_value = 1.6; cloud.inputs['Detail'].default_value = 4
cmix = wnt.nodes.new('ShaderNodeMix'); cmix.data_type = 'RGBA'; cmix.inputs[0].default_value = S['cloud_strength']; cmix.inputs[7].default_value = (0.9, 0.93, 0.97, 1)
lp = wnt.nodes.new('ShaderNodeLightPath'); mixw = wnt.nodes.new('ShaderNodeMixShader')
wnt.links.new(texco.outputs['Generated'], mapn.inputs['Vector']); wnt.links.new(mapn.outputs['Vector'], grad.inputs['Vector'])
cthr = wnt.nodes.new('ShaderNodeMath'); cthr.operation = 'SUBTRACT'; cthr.inputs[1].default_value = 0.55
cmul = wnt.nodes.new('ShaderNodeMath'); cmul.operation = 'MULTIPLY'; cmul.inputs[1].default_value = 3.0 * S['cloud_strength']; cmul.use_clamp = True
wnt.links.new(cloud.outputs['Fac'], cthr.inputs[0]); wnt.links.new(cthr.outputs[0], cmul.inputs[0])
wnt.links.new(grad.outputs['Fac'], ramp.inputs['Fac']); wnt.links.new(ramp.outputs['Color'], cmix.inputs[6]); wnt.links.new(cmul.outputs[0], cmix.inputs[0])   # 구름: 노이즈 임계 위만, 강도 제한
wnt.links.new(cmix.outputs[2], bg_cam.inputs['Color']); wnt.links.new(sky.outputs['Color'], bg_light.inputs['Color'])
wnt.links.new(lp.outputs['Is Camera Ray'], mixw.inputs[0]); wnt.links.new(bg_light.outputs[0], mixw.inputs[1]); wnt.links.new(bg_cam.outputs[0], mixw.inputs[2]); wnt.links.new(mixw.outputs[0], wout.inputs['Surface'])
sun = bpy.data.lights.new('SUN', 'SUN'); sun.energy = S['sun_strength']; sun.angle = math.radians(1.5)
SUN = bpy.data.objects.new('SUN', sun); link(SUN, C_CAM); SUN.rotation_euler = (math.radians(90 - S['sun_elevation_deg']), 0, math.radians(S['sun_azimuth_deg']))
# C11a 라이트 링킹: 엔진+발전기에만 추가 태양(발광 금지의 합법적 대체)
boost = bpy.data.lights.new('SUN_BOOST', 'SUN'); boost.energy = 0.0; boost.angle = math.radians(3)
BOOST = bpy.data.objects.new('SUN_BOOST', boost); link(BOOST, C_CAM); BOOST.rotation_euler = SUN.rotation_euler
rc = bpy.data.collections.new('LL_ENGINE_GEN'); scn.collection.children.link(rc)
for ob in list(C_ENGINE.objects) + list(C_GEN.objects): rc.objects.link(ob)
BOOST.light_linking.receiver_collection = rc   # 라이트 링킹은 Object 속성
anim.bake_fcurves(boost, FR, {'energy': B['light_link'] * S['sun_strength'] * 1.0})

# ---------------- 카메라 ----------------
cam = bpy.data.cameras.new('CAM'); cam.sensor_fit = 'VERTICAL'; cam.sensor_height = cfg['camera']['sensor_width_mm']; cam.sensor_width = cfg['camera']['sensor_width_mm']
cam.dof.use_dof = True
CAM = bpy.data.objects.new('CAM', cam); link(CAM, C_CAM); scn.camera = CAM
pos, tgt = B['cam_pos'], B['cam_target']
eul = []
for p, t_ in zip(pos, tgt):
    d = Vector(t_) - Vector(p); q = d.to_track_quat('-Z', 'Y'); eul.append(q.to_euler('XYZ'))
eul = anim.continuous_euler(np.array([[e.x, e.y, e.z] for e in eul]))
anim.bake_fcurves(CAM, FR, {'location': pos, 'rotation_euler': eul})
anim.bake_fcurves(cam, FR, {'lens': B['cam_lens'], 'dof.aperture_fstop': B['cam_fstop'], 'dof.focus_distance': np.linalg.norm(tgt - pos, axis=1)})
# 하드컷 전이에서 보간 금지: 카메라 fcurve를 CONSTANT로 두면 프레임 사이 블러가 생기지 않지만 1F 단위 베이크라 LINEAR 유지, 대신 컷 경계 F에 모션블러 셔터 분할 — 마커로 기록
for name, F in [('C01', 1), ('C02', 79), ('C03a', 187), ('C03b', 281), ('C04', 394), ('C05', 488), ('C06a', 552), ('C06b', 642), ('C07a', 706), ('C07b', 774), ('C08', 865), ('C09', 965), ('C10a', 1078), ('C10b', 1138), ('C11a', 1257), ('C11b', 1324)]:
    mk = scn.timeline_markers.new(name, frame=F); mk.camera = CAM

# ---------------- 고립(D3) 가시성 ----------------
def hide_intervals(objs, intervals):
    h = np.zeros_like(FR)
    for a, b in intervals: h[(FR >= a) & (FR <= b)] = 1.0
    for ob in objs: anim.bake_fcurves(ob, FR, {'hide_render': h}, interp='CONSTANT')
iso04 = [(394, 551)]; iso08 = [(865, 964)]
hide_intervals([BODY, CAB, NOSE, DECK, BLOCK, TERM, JBOX, CPL_L, KN_L] + list(C_CABLE.objects) + [o for o in C_ENGINE.objects if o.name.startswith('LINER')], iso04 + iso08)
hide_intervals([CASE, STATOR], [(394, 487)] + iso08)   # C05(488–551)에는 케이스·고정자를 남겨 커터 링이 회전자를 드러낸다
hide_intervals([ROTOR, SHAFT_C, FLANGE] + [o for o in C_GEN.objects if o.name.startswith('GEN_POLE')], iso08)
hide_intervals([CRANK] + [o for o in C_ENGINE.objects if o.name.startswith(('PISTON', 'ROD', 'CRANK_'))], iso08)
hide_intervals([BOGIE_R] + list(C_CARS.objects), iso04 + iso08)
hide_intervals([o for o in C_BOGIE_PROTO.objects if not o.name.startswith('CUT_')] , iso08)   # 프로토타입 전체 숨김 후 고립 부품만 다시 노출
hide_intervals([o for o in C_ISO.objects if not o.name.endswith('_L')], [])                # 고립 조립체는 유지
hide_intervals([o for o in C_ISO.objects if o.name.endswith('_L')], iso08)                 # 카메라 쪽(좌) 차륜·플랜지·축상은 숨겨 기어 맞물림 노출

# ---------------- 렌더 설정·패스 ----------------
scn.render.engine = 'CYCLES'; cy = scn.cycles
cy.samples = 256; cy.use_adaptive_sampling = True; cy.adaptive_threshold = 0.01; cy.use_denoising = True
cy.denoiser = 'OPENIMAGEDENOISE'; scn.render.use_persistent_data = True; scn.render.use_motion_blur = True; scn.render.motion_blur_shutter = 0.5
scn.view_settings.view_transform = 'AgX'; scn.view_settings.look = 'AgX - Medium High Contrast'; scn.render.dither_intensity = 1.0
scn.render.film_transparent = False
vl = scn.view_layers[0]; vl.name = 'MAIN'
vl.use_pass_z = True; vl.use_pass_normal = True; vl.use_pass_object_index = True; vl.use_pass_cryptomatte_object = True
aov = vl.aovs.add(); aov.name = 'electric'; aov.type = 'VALUE'
# GHOST 뷰레이어: 유령·림만 가시, 나머지 홀드아웃(가림 유지), IndexOB만 필요, 샘플 4
gl = scn.view_layers.new('GHOST'); gl.use_pass_object_index = True; gl.use_pass_combined = False; gl.samples = 4
for lc in gl.layer_collection.children:
    if lc.name not in ('GHOSTS', 'RIMS'):
        lc.holdout = True
# 메인 레이어에서 유령·림 제외
for lc in vl.layer_collection.children:
    if lc.name in ('GHOSTS', 'RIMS'): lc.exclude = True
# 컴포지터 File Output: 패스별 16-bit PNG (후합성 입력)
scn.use_nodes = True; ct = scn.node_tree
for n in list(ct.nodes): ct.nodes.remove(n)
rl = ct.nodes.new('CompositorNodeRLayers'); rl.layer = 'MAIN'
rg = ct.nodes.new('CompositorNodeRLayers'); rg.layer = 'GHOST'
fo = ct.nodes.new('CompositorNodeOutputFile'); fo.base_path = '//passes/'; fo.format.file_format = 'PNG'; fo.format.color_depth = '16'; fo.format.color_mode = 'RGB'
fo.file_slots.clear()
for slot, src, out_name in [('combined', rl, 'Image'), ('depth', rl, 'Depth'), ('normal', rl, 'Normal'), ('index', rl, 'IndexOB'), ('electric', rl, 'electric'), ('ghost_index', rg, 'IndexOB')]:
    fo.file_slots.new(slot); ct.links.new(src.outputs[out_name], fo.inputs[slot])
comp = ct.nodes.new('CompositorNodeComposite'); ct.links.new(rl.outputs['Image'], comp.inputs['Image'])
# 깊이·인덱스는 16-bit PNG 정규화 한계가 있으므로 EXR 슬롯도 병행
fo2 = ct.nodes.new('CompositorNodeOutputFile'); fo2.base_path = '//passes_exr/'; fo2.format.file_format = 'OPEN_EXR'; fo2.format.color_depth = '16'
fo2.file_slots.clear()
for slot, src, out_name in [('depth', rl, 'Depth'), ('index', rl, 'IndexOB'), ('ghost_index', rg, 'IndexOB'), ('electric', rl, 'electric'), ('normal', rl, 'Normal')]:
    fo2.file_slots.new(slot); ct.links.new(src.outputs[out_name], fo2.inputs[slot])

# ---------------- 저장·검증 출력 ----------------
os.makedirs(os.path.dirname(OUT), exist_ok=True)
for f in (1, 318, 894):
    scn.frame_set(f); dg = bpy.context.evaluated_depsgraph_get()
    print(f'F{f}: LOCO x={LOCO.matrix_world.translation.x:.3f}  CAM={tuple(round(v,3) for v in CAM.matrix_world.translation)}  lens={cam.lens:.1f}  CRANK rx={CRANK.rotation_euler.x:.3f}  WHEEL ry={bpy.data.objects["AXLE_01"].rotation_euler.y:.3f}  GHOST x={GS.location.x:.3f} hide={GS.hide_render}')
scn.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=OUT)   # bpy.ops 허용 예외: 저장
print('SAVED', OUT, 'objects', len(bpy.data.objects))
