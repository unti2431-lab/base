"""대표 스틸/구간 렌더. 사용: python render_still.py --blend ../render/del74_scene.blend --frames 1,150,318 --pct 25 --spp 8 --out ../review/R02/stills [--device CPU|OPTIX] [--passes 0|1]"""
import bpy, sys, os, time, json
argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
def arg(k, d):
    return argv[argv.index(k) + 1] if k in argv else d
blend = os.path.abspath(arg('--blend', '../render/del74_scene.blend')); frames = [int(f) for f in arg('--frames', '1').split(',')]
pct = int(arg('--pct', '25')); spp = int(arg('--spp', '8')); out = os.path.abspath(arg('--out', '../review/R02/stills')); device = arg('--device', 'CPU'); passes = arg('--passes', '0') == '1'
bpy.ops.wm.open_mainfile(filepath=blend)
scn = bpy.context.scene; LOCK = (4, 5); assert bpy.app.version[:2] == LOCK
scn.render.resolution_percentage = pct; scn.cycles.samples = spp; scn.cycles.use_adaptive_sampling = False
scn.cycles.device = 'GPU' if device != 'CPU' else 'CPU'
if device != 'CPU':
    prefs = bpy.context.preferences.addons['cycles'].preferences; prefs.compute_device_type = device; prefs.get_devices()
    for d in prefs.devices: d.use = True
scn.use_nodes = passes                      # 패스 PNG/EXR 출력은 요청 시에만
os.makedirs(out, exist_ok=True); log = []
for f in frames:
    scn.frame_set(f); scn.render.filepath = os.path.join(out, f'F{f:04d}.png')
    t0 = time.time(); bpy.ops.render.render(write_still=True); dt = time.time() - t0
    log.append({'frame': f, 'sec': round(dt, 1), 'pct': pct, 'spp': spp, 'device': device}); print('RENDERED', f, f'{dt:.1f}s', flush=True)
json.dump(log, open(os.path.join(out, 'render_log.json'), 'w'), indent=1)
