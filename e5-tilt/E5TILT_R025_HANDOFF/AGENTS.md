# AGENTS.md — E5 TILT R025 인계 작업 규칙 (Codex 기준, 다른 에이전트도 그대로 적용)

## 0. 한 문장 목표
320 km/h E5가 곡선에서 두 공기스프링의 높이차 약 5 cm로 차체를 1.5° 기울이는 과정을, 실차 안에서 끊기지 않는 시점으로 보여주는 26.77초 세로 쇼츠를 레퍼런스(Bf 109 컷어웨이) 수준으로 끌어올린다.

## 1. 읽는 순서
1. `LOCKS.md` — 사실·규격·수정 금지 파일·스타일
2. `HANDOFF_R025.md` — 현재 상태, 재현 기준값, 구조도, 알려진 한계
3. `PRODUCTION_PLAN_R025.md` — 기획 전체(P0–P12)
4. `BEATS_R025.csv` — 컷·사건·음성 대응
5. `TASKS.json` — 할 일과 완료 조건
6. `review/R025/` — 현재 애니매틱과 컨택트 시트

## 2. 첫 작업 = 베이스 재현 (다른 작업보다 먼저)
```bash
scripts/setup_env.sh                 # Linux: python3.11 venv + bpy==4.5.14
scripts/run_pipeline.sh verify       # kin → G3 → build → G4 → sfx → sync
```
Windows: `.\RUN_ALL.ps1 -Setup` 후 `.\RUN_ALL.ps1 -VerifyOnly`.
`HANDOFF_R025.md` §3 재현 기준값과 일치해야 다음 작업으로 넘어간다. 불일치하면 REPORT.md에 기록하고 멈춘다.

## 3. 반드시
- 모든 운동은 `src/tilt_bake.npz`에서만 온다. 시간·사건을 바꾸려면 `rig_config.json`을 고치고 `kin.py`로 재베이크한다.
- 수치를 바꾸면 `verify_bake.py`(G3) → `build.py` → `verify_scene.py`(G4)를 다시 통과시킨다. 실패하면 다음 단계로 가지 않는다.
- 한 라운드에 변수 하나. `review/R0NN/CHANGELOG.md`에 바꾼 변수와 이유를 적는다. 라운드 폴더는 덮어쓰지 않고 새로 만든다.
- 씬 구성은 bmesh + bpy.data. bpy.ops는 저장·열기·렌더·에셋 임포트에만 쓰고 주석으로 표시한다.
- 애니메이션 키는 `common.bake_fcurves`(채널백 + 슬롯 명시)로만 쓴다. `action.fcurves`는 쓰지 않는다.
- 새 오브젝트 이름은 `KIND_SIDE_INDEX` 규칙. 검증 스크립트가 이름으로 찾는다.
- 에셋을 넣으면 `import_assets.py`로 리그 슬롯에 붙이고 `collide_with`를 채워 G4를 다시 돌린다.
- 인코딩은 `scripts/encode.sh` 또는 RUN_ALL의 BT.709 행렬 명시 명령만 쓴다.
- 판정은 PASS / FAIL / NOT_PERFORMED / NOT_DECIDABLE. 돌리지 않은 검사를 N/A나 PASS로 쓰지 않는다.

## 4. 금지
- `LOCKS.md` RIG 목록의 파일 수정(풀이·검증 코드). 버그를 찾으면 REPORT.md에 재현 절차와 함께 보고만 한다.
- 형상·각도 과장으로 판독 문제를 해결하는 것. 1.5°는 1.5°로 둔다. 조명 → 카메라 거리·렌즈 → 배경 명도 → 후합성 도형 순서로 고친다.
- 3D 씬 안에 글자·발광 화살표·먼지·연기 넣기. 글자는 자막 레이어(R08)만.
- 디졸브 전환. 카메라 완전 정지(6F 이상).
- UNVERIFIED 수치를 화면·내레이션에 쓰는 것.
- 게이트를 끄거나 임계값을 완화해서 통과시키는 것. 임계값 변경은 사유와 함께 사용자 승인 후.
- 사용자 블로커(G-1~G-4)를 추측으로 메우는 것.
- Blender 버전 변경(4.5 LTS LOCK).

## 5. 명령 요약
| 목적 | 명령 |
|---|---|
| 베이크 | `python src/kin.py` |
| G3 | `python src/verify_bake.py` |
| 빌드 | `python src/build.py` (Windows: `blender -b --factory-startup --python src/build.py --`) |
| G4 | `python src/verify_scene.py -- --step 5` |
| 게이트 자가시험 | `python src/selftest_gates.py` (모든 항목 ok=true여야 함) |
| 스틸 | `python src/render_frames.py -- --stage still --frames 345,450` |
| 애니매틱 | `scripts/run_pipeline.sh animatic` |
| 핵심 4초 | `.\RUN_ALL.ps1 -Stage key4s -Start 319 -End 438` |
| 최종 | `.\RUN_ALL.ps1 -Stage final -Chunk 12` (사용자 GPU) |
| 비트표 재생성 | `python src/make_beats.py` |
| 단어 타임스탬프(로컬) | `python scripts/vo_words.py` |

## 6. 완료 정의 (작업 하나당)
1. 해당 TASKS.json 항목의 `accept`를 모두 만족한다.
2. G3·G4가 PASS이고 `evidence/*.json`이 갱신됐다.
3. 화면에 영향이 있으면 `review/R0NN/`에 270p 컨택트 시트 + 변경 컷 540p 스틸 2장을 남겼다.
4. `REPORT.md`에 작업ID / 변경파일 / 명령 / 게이트값 / 산출물 / 질문을 적었다.
5. `MANIFEST.json`을 `python scripts/make_manifest.py`로 갱신했다.

## 7. 보고 형식 (REPORT.md)
결론 1–2문장 → 표(항목/상태/근거 수치·파일) → 블로커 굵게 → 사용자 할 일 번호 목록.
