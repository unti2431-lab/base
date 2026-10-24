# AGENTS.md — SKIRT01 R02 Claude 작업 지시서

이 폴더만으로 착수한다. 이전 대화 맥락은 없다고 가정한다. Codex·다른 에이전트도 그대로 읽힌다.

## 1. 읽는 순서 (10분)
```
1. AGENTS.md              ← 지금 이 파일 (규칙·명령·완료 정의)
2. DECISIONS.md           사용자 결정 기록 — G-01·G-03·G-04 해소, 승인 항목
3. LOCKS.md               변경 금지 사실·규격·룩 (R02 갱신본)
4. PRODUCTION_PLAN_R02.md 제작 설계 전체 — §4 모델링, §5 운동학, §6 재질, §7 조명, §8 카메라, §9 비트, §10 후합성, §11 게이트
5. TASKS.json             작업 목록·의존·수용 조건
6. src/rig_config.json    기하 수치 단일 출처 (R02 확정본)
7. REFERENCE_NOTES.md     레퍼런스 측정 → 목표값
```
상위 규범은 `blender-short-3d-pipeline` 스킬. 충돌 시 **사용자 최신 지시 > LOCKS.md > 공통 규범 v3.0 > 스킬 > 이 문서** 순.

## 2. 한 문장 목표
에스컬레이터 옆면의 솔처럼 생긴 장치가 치수 하나까지 안전기준이 정한 물건임을 44초에 보여준다.

## 3. 반드시 / 금지

반드시
- 모든 기하 수치는 `src/rig_config.json`에서 읽는다. 코드에 숫자를 박지 않는다.
- 애니메이션 베이크는 `src/bake_helpers.bake_fcurves`만 쓴다. 빌드 직후 `verify_moving`으로 프레임 1·2 위치를 출력한다.
- 씬 구성은 bmesh + bpy.data. bpy.ops는 저장·임포트에만, 주석으로 표시.
- 베벨은 `bmesh.ops.bevel`로 메시에 굽는다(인스턴스에 모디파이어 없음).
- 접촉면 동일 평면 금지. 디딤판–스커트 4.0 mm, 이웃 디딤판 1.5 mm, 홀더–스커트 0.5 mm(설계 접촉).
- 검증 스크립트는 빌드 코드를 import하지 않는다(npz·PNG·JSON만 읽음). **생성자 ≠ 검증자.**
- 판정은 PASS / FAIL / NOT_PERFORMED / NOT_DECIDABLE 넷 중 하나. N/A 금지.
- 한 라운드에 변수 하나. `review/R##/CHANGELOG.md`에 변수 1개와 이유.
- 렌더 시간은 대표 프레임 1장을 **측정**해 환산한다.

금지
- 대본 문장 수정 (SCRIPT_LOCKED).
- LOCKS.md 수정 → 필요하면 보고하고 멈춘다.
- "빨려 들어간다"류 사고 연출. C07 운동화는 **옆으로 스치다 밀려나는 동작만**.
- 세부 치수(강성 18~25 / 유연 15~30, 장착 높이 28, 종료 거리 50)를 자막·치수선·내레이션에 제시.
- 3D 씬 안 글자·먼지·연기·발광·입자. 2.5D 강조는 후합성 레이어로만.
- 돌출량·틈을 형상으로 과장해 판독을 올리는 것. 수정 순서는 조명 → 카메라 거리 → 배경 명도.
- 컷별 운행 속도 조작(마스터 곡선 하나). 모션블러 셔터는 컷별 예외 허용.
- 카메라 완전 정지, 24 mm 이하 광각, 180° 규칙 위반(카메라는 항상 디딤판 쪽에서 왼쪽 스커트).
- 모델 에셋 다운로드·구매(DECISIONS 참조). CC0 텍스처·HDRI만 허용.

## 4. 지금 상태와 착수 순서
| 게이트 | 상태 |
|---|---|
| G0 | **통과** (G-01 트럭리프트 → 중복 아님, config R02 확정) |
| G1 | **통과** (Bf 109 편, REFERENCE_NOTES.md) |
| G2 | **차단 — 사용자 녹음 대기.** T-02·T-03 보류 |
| G3~G7 | 미착수 |

G2가 차단이어도 **T-13~T-18은 24 fps 가예산(1,056F)으로 선행한다.** 음성이 오면 fps·총 프레임만 바꾸고 재베이크한다(config의 `render.fps`·`total_frames`만 갱신). 그래서 베이크·빌드 코드는 fps를 config에서만 읽어야 한다.

착수 순서: T-13(config 재확인·환경) → T-14 kin/bake → T-15 verify_bake → T-04(CC0 텍스처·HDRI) → T-16 build → T-17 verify_scene + anchors → T-18 luma/brush → T-09 애니매틱 → T-10 핵심 4초 → T-11 프리뷰 → T-12 보고.

## 5. 실행 명령
```bash
bash scripts/setup_env.sh                 # bpy==4.5.14, Python 3.11 (한 번)
bash scripts/run_pipeline.sh              # bake → verify_bake(게이트) → build → verify_scene(게이트) → 대표 스틸
bash scripts/run_pipeline.sh --verify-only
bash scripts/run_pipeline.sh --rebake
# 애니매틱(백그라운드, 이어하기)
setsid nohup env/bin/python src/render_frames.py --res 270 --spp 4 --out render/animatic > render/animatic.log 2>&1 &
# 핵심 4초
env/bin/python src/render_frames.py --res 540 --spp 24 --frames 481-672 --out render/key4s
# 인코딩·스트레스
bash scripts/encode.sh render/key4s 24 review/R02/key4s_540p.mp4
ffmpeg -i review/R02/key4s_540p.mp4 -c:v libx264 -b:v 2M -maxrate 2M -bufsize 4M -an review/R02/stress_key4s.mp4
```
클라우드는 GPU 없음 → Cycles CPU, 270p 전편 + 540p 핵심 4초까지만. 540p 전편·1080p는 로컬 GPU(`RUN_ALL.ps1`, 사용자 실행).

## 6. 파일별 수정 허용 범위
| 파일 | 허용 |
|---|---|
| `src/rig_config.json` | DESIGN_ASSUMPTION 값만, 사유를 `_note`에. LOCKED·MODEL_ONLY 변경 금지 |
| `src/bake_helpers.py` | **수정 금지** |
| `src/kin_steps.py, bake_steps.py, build_*.py, verify_*.py, render_frames.py, export_anchors.py` | 신규 작성·수정 자유 (T-14~T-18) |
| `camera_keys.json`, `BEATS.csv` | 자유. 단 BEATS 사건 F는 베이크 역산값만 |
| `LOCKS.md`, 대본 | 금지 |

## 7. 완료 정의 (이번 인계 범위 = G7 무음 프리뷰까지)
```
evidence/bake_qc.json        G3 PASS
evidence/scene_qc.json       G4 충돌 0건 또는 설계 접촉 목록
evidence/luma_qc.json        G4.5 PASS (§6.1 L* 목표)
evidence/brush_qc.json       G4.6 PASS (가닥 ≥1.5px, 2M 스트레스 깜빡임 없음)
overlay/overlay_anchors.json 후합성 앵커 (COMB_LINE·틈·돌출 2D 좌표)
review/R0x/animatic_270p.mp4 G5
review/R0x/key4s_540p.mp4    G6 ← 핵심 게이트 (C06–C07)
review/R0x/preview_540p.mp4  G7
review/R0x/CHANGELOG.md
REPORT.md                    §17 형식
```
G6에서 "33~50 mm 돌출 + 강성·유연 2중 구조"가 540p 정상속도에서 안 읽히면 편 전체 실패다. 수치 PASS를 화면 PASS로 대체하지 않는다.

## 8. 중단 규칙
- 같은 결함이 국소 수정 2회 뒤에도 남으면 → 재설계 보고 후 멈춤.
- LOCKS를 고쳐야 할 것 같으면 → 고치지 말고 보고.
- 솔 깜빡임이 §4.4 3단 대책 후에도 남으면 → 유연부 고무립 전환을 **제안**(사용자 결정, LOCK 아님).

## 9. 사용자 보고 형식
결론 1–2문장 → 항목/상태/근거 표 → **블로커 굵게** → 사용자 할 일 번호 목록 → Sources.
