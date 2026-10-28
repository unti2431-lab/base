# COWORK_NEXT — R9a 이후 로컬 진행 순서 (2026-10-29)

## 이미 끝난 것 (클라우드)
- VM_CHECK PASS, 클라우드 BASELINE PASS (bpy 4.5.14, CPU)
- RUN_ALL.ps1 R9a 하드닝 (한국어 Windows cp949 크래시 등 7건, REPORT.md 참조)
- L08 W0 루프 블로킹: `w0_loop_qc.json` ALL_PASS, `review/W0_loop_seam_270p_CONCEPT.mp4`
- L10 근거 원문 9건 대조: `evidence/L10_EVIDENCE_R9a.md`, LOCKS FACT 갱신

## 로컬에서 할 것 (순서 고정, FAIL이면 멈춤)
| 순서 | 실행 | 통과 조건 |
|---|---|---|
| 1 | `cowork\01_SETUP.cmd` | `PASS setup` (BLENDER 4.5.x, venv ok, ffmpeg·ffprobe·nvidia-smi 모두 있음) |
| 2 | `cowork\02_BASELINE.cmd` | `PASS baseline` (= 클라우드와 같은 기준값) |
| 3 | `cowork\03_GPU_TIMING.cmd` | `PASS timing` 2회(key4s_gpu, final), `logs\timing.csv`에 s/F·피크 VRAM·장치(OPTIX/CUDA) |
| 4 | 녹음 10개 + `audio\VO_LOCK.json` → `04_VO_SYNC.cmd` → `05_VO_APPLY.cmd` → `06_VERIFY.cmd` | 위반 0, `PASS verify` |
| 5 | `07_RENDER_KEY_A.cmd`, `08_RENDER_KEY_B.cmd` | 실패 청크 0, `decode ok` (R9a부터 실패 시 FAIL로 기록됨) |

## W0 로컬 재현 (선택)
`.venv`가 아니라 Blender로 실행한다: `blender -b --factory-startup -P src\build_w0.py` → `blender -b --factory-startup -P src\verify_w0.py`

## 사용자 결정 대기
1. C03 사용 기준: 현행 V 유지(권장) / P 허용으로 완화
2. VO 기본 선택 S2b_B(반달 제거판) — 녹음은 대본대로 10개 모두 받는다
