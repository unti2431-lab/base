# E5TILT_R025_HANDOFF

E5 신칸센 공기스프링 차체경사(최대 1.5°) 3D 공학 쇼츠 — R025 프록시 리그·카메라·270p 애니매틱 인계 패키지.

**에이전트는 `AGENTS.md`부터 읽는다.** 사람은 아래 세 개만 보면 된다.

| 보고 싶은 것 | 파일 |
|---|---|
| 지금 영상 | `review/R025/e5tilt_R025_animatic_270p.mp4` (R024 원음 합본) |
| 컷별 한 장 요약 | `review/R025/contact_270p.jpg` |
| 무엇이 됐고 무엇이 남았나 | `REPORT.md`, `HANDOFF_R025.md` §2·§5 |

빠른 실행
```
Windows (Blender 4.5 LTS 설치 후)    .\RUN_ALL.ps1 -Setup ; .\RUN_ALL.ps1 -VerifyOnly ; .\RUN_ALL.ps1 -Stage key4s -Start 319 -End 438
Linux / 클라우드                     scripts/setup_env.sh ; scripts/run_pipeline.sh verify ; scripts/run_pipeline.sh animatic
```

폴더
```
AGENTS.md  LOCKS.md  HANDOFF_R025.md  PRODUCTION_PLAN_R025.md  BEATS_R025.csv  TASKS.json  REPORT.md  MANIFEST.json  RUN_ALL.ps1
src/        kin · verify_bake · build · verify_scene · render_frames · comp_overlays · import_assets · selftest_gates · sync_qc · sfx_cues · make_beats
            rig_config.json · cameras.json · tilt_bake.npz · ASSET_MAP.TEMPLATE.json
scripts/    setup_env.sh · run_pipeline.sh · encode.sh · vo_words.py · make_manifest.py
audio/      R024_ORIGINAL_AUDIO.m4a · VO_LOCK.json · VO_PHRASES.json · SFX_CUES.csv
evidence/   geometry_qc · bake_qc · scene_qc · gate_selftest · sync_qc (.json)
reference/  REFERENCE_NOTES.md · 레퍼런스/R024 컨택트 시트 · R024 프리뷰 mp4
review/R025 애니매틱 mp4 · 컨택트 시트 · 540p 핵심 스틸 · qc_summary.json · CHANGELOG.md
work/       e5tilt_R025_proxy.blend (재생성 가능: src/build.py)
assets/     README.md · LICENSES.csv
```
