"""Render frames of the built scene with stage presets. Skips PNGs that already exist (resume).

python render_frames.py -- --blend ../work/e5tilt_R025_proxy.blend --stage animatic --start 1 --end 803 --outdir ../work/frames_animatic
python render_frames.py -- --frames 30,90,160 --stage still --outdir ../work/stills
Windows:  blender.exe -b ..\\work\\e5tilt_R025_proxy.blend -P render_frames.py -- --stage final --start 1 --end 24 --gpu
"""
import os, sys, time, argparse, csv
import bpy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import HERE, argv

STAGES = {   # resolution %, samples, adaptive threshold, motion blur
    'animatic': (25, 6, 0.10, True),
    'still':    (50, 16, 0.05, True),
    'key4s':    (50, 32, 0.03, True),
    'preview':  (50, 24, 0.04, True),
    'final':    (100, 256, 0.01, True),
}

ap = argparse.ArgumentParser()
ap.add_argument('--blend', default=os.path.join(HERE, '..', 'work', 'e5tilt_R025_proxy.blend'))
ap.add_argument('--stage', default='animatic', choices=list(STAGES))
ap.add_argument('--start', type=int, default=None)
ap.add_argument('--end', type=int, default=None)
ap.add_argument('--frames', default=None, help='comma list, overrides start/end')
ap.add_argument('--outdir', default=None)
ap.add_argument('--gpu', action='store_true')
ap.add_argument('--samples', type=int, default=None)
A = ap.parse_args(argv())

if os.path.abspath(bpy.data.filepath or '') != os.path.abspath(A.blend):
    bpy.ops.wm.open_mainfile(filepath=os.path.abspath(A.blend))       # ops exception: open
SC = bpy.context.scene
pct, spp, thr, mb = STAGES[A.stage]
SC.render.resolution_percentage = pct
SC.cycles.samples = A.samples or spp
SC.cycles.adaptive_threshold = thr
SC.render.use_motion_blur = mb
SC.render.use_persistent_data = True
if A.gpu:
    prefs = bpy.context.preferences.addons['cycles'].preferences
    for dev_type in ('OPTIX', 'CUDA', 'HIP', 'METAL', 'ONEAPI'):
        try:
            prefs.compute_device_type = dev_type
            prefs.get_devices()
            if any(d.type == dev_type for d in prefs.devices):
                for d in prefs.devices:
                    d.use = d.type == dev_type
                SC.cycles.device = 'GPU'
                if dev_type == 'OPTIX':
                    SC.cycles.denoiser = 'OPTIX'
                print('GPU', dev_type)
                break
        except TypeError:
            continue
else:
    SC.cycles.device = 'CPU'

if A.frames:
    frames = [int(x) for x in A.frames.split(',')]
else:
    frames = list(range(A.start or SC.frame_start, (A.end or SC.frame_end) + 1))
out = A.outdir or os.path.join(HERE, '..', 'work', f'frames_{A.stage}')
os.makedirs(out, exist_ok=True)
log_path = os.path.join(out, 'render_log.csv')
new_log = not os.path.exists(log_path)
with open(log_path, 'a', newline='') as fh:
    w = csv.writer(fh)
    if new_log:
        w.writerow(['frame', 'sec', 'stage', 'samples', 'camera'])
    for f in frames:
        path = os.path.join(out, f'{f:04d}.png')
        if os.path.exists(path) and os.path.getsize(path) > 0:
            continue
        SC.frame_set(f)
        # marker-bound camera for this frame
        cam = None
        for m in sorted(SC.timeline_markers, key=lambda m: m.frame):
            if m.frame <= f and m.camera:
                cam = m.camera
        if cam:
            SC.camera = cam
        SC.render.filepath = path
        t0 = time.time()
        bpy.ops.render.render(write_still=True)                          # ops exception: render
        dt = time.time() - t0
        w.writerow([f, round(dt, 2), A.stage, SC.cycles.samples, SC.camera.name]); fh.flush()
        print(f'F{f:04d} {dt:6.1f}s {SC.camera.name}', flush=True)
print('RENDER DONE', out)
