"""빌드 스크립트 템플릿 — 복사해서 src/build_<단계>.py 로 만든다(T04-T08).

실행: scripts/run_pipeline.sh (bpy 모듈) 또는 blender -b --factory-startup --python src/build_<단계>.py
규칙: bpy.ops 로 씬을 만들지 않는다(bmesh + bpy.data). 예외는 저장·임포트뿐이며 주석으로 표시한다.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))   # Blender 실행 파일로 돌릴 때도 common_bpy 를 찾게 한다
import bpy
import numpy as np
import common_bpy as C          # import 시점에 버전 가드가 돈다

BLEND = C.ROOT / 'blend' / 'PAVE_scene.blend'


def main():
    if BLEND.exists():
        bpy.ops.wm.open_mainfile(filepath=str(BLEND))                 # 예외: 파일 열기
    sc = bpy.context.scene
    sc.frame_start, sc.frame_end, sc.render.fps = 1, int(C.SPEC['frames']), C.FPS
    bake = C.load_bake('A_real')
    # ... 이 단계의 오브젝트 생성(bmesh + bpy.data) ...
    # 예: 오거 회전 베이크
    # F = np.arange(len(bake['theta_r']))                               # F0..frames+1 (모션블러용 앞뒤 1F)
    # C.bake_fcurves(bpy.data.objects['AUGER_R_FWD'], F, {'rotation_euler': np.c_[bake['theta_r'], 0*F, 0*F]})
    # C.motion_probe(['AUGER_R_FWD'])                                   # MOVES 가 찍혀야 한다
    BLEND.parent.mkdir(exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))                  # 예외: 저장


if __name__ == '__main__':
    main()
