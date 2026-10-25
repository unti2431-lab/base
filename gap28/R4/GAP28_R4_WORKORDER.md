# GAP28 R4 작업 지시서 (Claude Work 전용)

**발행** 2026-10-25 · **대상** 다음 Claude 작업 세션(클라우드 또는 로컬) · **패키지** `GAP28_R4_package.zip`
**읽는 순서** 이 문서 → `R4/LOCKS_R4.md` → `R4/GAP28_R4_REVISION_PLAN.md` → `R4/r4a/LIVE_SELECT.md` → `R4/TASKS.json` → R3 원본(`REPORT_R3.md`, `src/`)
**우선순위** 사용자 최신 지시 > `LOCKS_R4.md` > 공통 규범 v3.0 > Blender 숏폼 스킬 v2 > 이 지시서

---

## 0. 한 문장 목표

성신여대입구 승강장 실사(152209·162808)와 Blender 3D 를 **카메라 프로젝션 브리지**로 이어, 스크린도어·발판·차체가 실사와 같은 역으로 읽히는 40초 세로 쇼츠의 R4 애니매틱(270p)과 핵심 4초(540p) 2개(전환 A·B)를 만든다.

## 1. 사용자가 이미 결정한 것 (재질문 금지)

| # | 결정 | 영향 |
|---|---|---|
| D1 | 162808·162328 은 **성신여대입구**에서 열차 안에서 촬영한 것이 맞다 | L2 = 162808 F165–254 확정. 154101 은 백업 |
| D2 | CG 발판 외형을 **천공 아연도금 강판 + 시안 끝단 띠**로 바꾼다 | `rig_config.panel.look`, 재질 PLATE 신설, STYLE "시안 = 해법" 유지 |
| D3 | 전환 B = **가림 와이프**(권고안) | B13 은 설계대로 수직 부감으로 끝난다. L3 시작 F2466 의 승객 몸이 가림 |
| D4 (R4 계획서 승인분) | B10–B12 재설계안(53모듈 전개 → 법 경계 통과 시 격납 → 5개 잔존), 10cm 기준선 흰색, 인물 삭제, PSD 모델링(설명용 설정값), 문 정렬 config 이동 | §4 작업 R4b·R4d |

아직 **미결**: 음성·화자·fps(§7 사용자 할 일). 미결 항목은 30fps/1200F 설계 예산으로 진행하고 `timing_s.json` 한 파일로 리타임할 수 있게 유지한다.

## 2. 환경 세팅 (첫 10분)

```bash
unzip GAP28_R4_package.zip -d gap28 && cd gap28
python3.11 -m venv env && env/bin/pip install "bpy==4.5.14" numpy pillow
env/bin/python -c "import bpy; print(bpy.app.version_string)"   # 4.5.14 가 아니면 중단
# 재현 기준값 확인 (R3 와 동일해야 시작 가능)
env/bin/python src/retime.py && env/bin/python src/kin.py && env/bin/python src/verify_bake.py
```
기대값: `R_m 263.2529 · gap_mid 280.0 · gap_end 90.0 · ratio 0.467 · panel_deployed F628(@30)`. 하나라도 다르면 작업을 시작하지 말고 보고한다.

클라우드 제약: GPU 없음 → Cycles CPU 270p 애니매틱·540p 스틸만. 최종 1080p 는 사용자 PC(`RUN_ALL.ps1`). 프로세스 종료는 PID 로. 장시간 렌더는 `setsid nohup … &` + 이어하기.

## 3. 파일 수정 규칙

- 수치는 `src/rig_config.json`·`src/camera_plan.json`·`src/timing_s.json` 에만. 풀이 코드에 상수 금지.
- `src/shots.json` 은 `set_travel.py` 가 생성한다. 직접 수정 금지.
- 모든 스크립트 첫 줄에 `BLENDER_LOCK=(4,5)` 가드. 베이크는 채널백 API(`bake_fcurves`).
- 재현 기준값 5개는 R4 끝까지 그대로여야 한다(문 정렬로 히어로 x 가 바뀌어도 반경·틈·비율은 불변).
- 한 라운드에 한 축, 축 안에서 변수 1개씩. 같은 결함이 국소 수정 2회 뒤에도 남으면 멈추고 보고.
- 검증 상태는 PASS / FAIL / NOT_PERFORMED / NOT_DECIDABLE 만. 실행 안 한 검사를 N/A 로 쓰지 않는다.
- 생성자 ≠ 검증자: 각 라운드 끝에 결론을 모르는 별도 에이전트에게 §6 게이트를 재측정시켜 수치 일치를 확인한다.

## 4. 작업 순서 (TASKS.json 과 1:1)

### R4a-2 실사 확정 (입력: 사용자 540p 발췌본 5개, `R4a_proxies/x540_*.mp4`)
1. `r4a/analyze_proxies.py` 를 540p 에도 돌릴 수 있게 `PROXY_W/H` 를 입력 해상도에서 읽도록 고친다(환산 배율 1080/W).
2. In/Out 1F 확정: L1 F2240–2329 · L2 F165–254 · L3 F2466–2555 · L4 F3230–3319 를 540p 에서 재검토. 문 열림 시작(L1 끝), 가림 비율(L3 시작 F2466 ±5F 에서 승객 몸이 차지하는 화소 비율 ≥ 60% 인 프레임을 F1021 로), 빈 발판 상태(L3 끝·L4 시작) 확인.
3. 루프: L4 끝 프레임 ↔ L1 첫 프레임 SSIM 측정(`ffmpeg -lavfi ssim`). 기록만 한다(목표값은 LOCK 미정).
4. 매치무브: 162808 F230–254 를 Blender 모션 트래킹으로 솔브. 특징점: 차내 문턱 스테인리스 모서리·나사, 발판 천공 격자, 승강장 타일 줄눈. 축척 = 점자블록 600mm(G-05) 또는 문턱 폭(실측 PENDING 이면 점자블록). 솔브 에러 ≤ 0.5px. 결과를 `src/solved_pose_L2.json`(프레임별 위치·회전·렌즈)로 저장하는 `src/track_import.py` 작성. 솔브 실패 시 폴백 1(2D 안정화 + 4점 플래너) → 폴백 2(Flow) 순으로, 각 시도와 실패 증상을 보고.
5. 재질 레퍼런스 스틸 7장을 `reference/live_material/` 에 추출(LIVE_SELECT §4 표).
6. `rig_config.json` 에 실측 추가: `psd`(프레임 폭·문턱 발판 폭·쉐브론 폭), `car.threshold`(차내 문턱 폭), `textures`(타일 모듈). 모두 `"_src": "live 152209 F…"` 와 `"_fact": "설명용 설정값, 사실 주장 아님"` 을 단다.
산출물: `R4a/LIVE_SELECT_FINAL.md`, `src/solved_pose_L2.json`, `evidence/loop_ssim.json`, `reference/live_material/*.png`
통과: In/Out 4개 확정, 솔브 재투영 ≤ 2px(또는 폴백 명시), 스틸 7장

### R4b 지오메트리 (`src/build.py`, `rig_config.json`)
순서대로, 각 단계 뒤 `verify_scene.py`(STEP=15) 미선언 충돌 0 을 유지한다.
1. **문 정렬**: `car.x_offset_m = 2.225` 신설(문 중심이 x=0, 4.45 에 오도록). `panel.x_center_m` 0 유지, `DIM_X`·`SHOE_X` 를 build.py 상수에서 빼 `measure.x_m = 4.45`, `foot.x_m = 4.55` 로 config 화. `verify_bake.py` 에 "히어로 x·측정 x 가 문 개구 안" 검사 추가.
2. **스크린도어(PSD)**: 연단 전장에 `psd.module_pitch_m`(= 차량 문 피치 4.45, 차량 간 보정) 으로 모듈 배치. 구성: 고정 유리벽, 문짝 2매(히어로 구간 ±12m 열림 고정, 나머지 닫힘), 프레임(회색), 상부 헤더, **문턱 발판**(천공 강판, 연단 끝에서 선로 쪽으로 `psd.step_w_m`, 쉐브론 띠는 노랑 단색). 실사 152209 와 같은 자리에 스티커 **빈 면**. 충돌 쌍 PSD×PLATFORM 선언 접촉, PSD_DOOR×CAR 0건.
3. **차체 프로파일 스윕**: 박스 → 단면 폴리라인(스커트 곡률, 창 리세스 12mm, 문 포켓 리세스, 도색 띠 — 색은 `reference/live_material` 에서). 문턱 스텝(차내 바닥 ↔ 문턱 스테인리스 띠), 문 아래 **검은 고무 빗살**(실사 154101·152835 와 같은 요소, `car.comb`), 하부 기기함, 대차·차륜(플랜지가 레일 위, WHEEL×RAIL 선언 접촉). 히어로 1량만 고정밀, 나머지 4량 인스턴스.
4. **연단·틈**: 립 챔퍼 10mm, 연단면 패널 이음 1.2m, 슬롯 테두리 스틸 프레임. 틈 바닥은 실사에서 확인될 때까지 `track.bed_type = "concrete"` 로.
5. **점자블록 돌기**: 히어로 구간(±6m) 실체 기하, 그 밖은 노멀. 치수는 KS F 4551 을 확인해 config 에 넣고 출처를 적는다(확인 못 하면 `UNVERIFIED` 로 표시하고 실사 비율로).
6. **발판(D2)**: 판 상면을 천공 패턴(지오메트리 아님, 셰이더), 끝단에 시안 띠 `panel.edge_band_m = 0.04`, 끝단 고무 립. 하우징 슬롯 프레임. 상태 순서만(RIG LOCK).
7. **레일** I형 프로파일 + 체결구, **조명기구** 루버, **인물 삭제**(`figures.count = 0`), **신발** 에셋 자리(`assets/README.md` 에 요구 규격, 없으면 R3 박스 유지).
8. 배열 발판 `array.count = 53`, `survive_indices` 5개(간격은 균등하지 않게, 시드 고정), 동작은 수평 격납(R3 히어로와 같은 리그 인스턴스).
산출물: `evidence/verify_scene_r4b.json`, `evidence/verify_bake_r4b.json`, 540p 스틸 16장(`evidence/stills_r4b_540p_sheet.png`)
통과: 미선언 충돌 0, 문 정렬 검사 PASS, 생존 비율 5/53 PASS, 카메라 경계 PASS, 재현 기준값 5개 불변

### R4c 재질·텍스처 (`src/build.py` 재질부, 또는 `src/materials.py` 로 분리)
`exp_texture.py` 의 실험을 본 씬으로 옮기고 계획서 §7 표대로 12종. 이미지 텍스처는 CC0 2K 상한, `assets/LICENSES.csv` 에 기록. 색은 `reference/live_material` 과 CIEDE2000 ΔE ≤ 6 (`src/measure_match_color.py` 신설: 540p 스틸의 지정 영역 평균색 vs 레퍼런스 스틸).
고주파(돌기·천공·빗살)는 카메라 거리로 노멀 강도 페이드. 명도 3층 유지.
산출물: `evidence/look_anim_r4c.json`(13/13 목표), `evidence/color_match_r4c.json`, `evidence/rhythm_anim_r4c.json`
통과: G-LOOK ≥ 12/13, ΔE ≤ 6 (타일·점자블록·차체 3종), G-RHYTHM 움직임 median ≥ 6.0 **또는** 미달 시 샷별 수치와 다음 레버를 보고

### R4d 카메라·컷 (`src/camera_plan.json`, `src/set_travel.py`)
1. `camera_plan.json` 에 블록 신설: `lens_groups`(gap 20 / truck 28–35 / read 40), `ease`(경계 종류별), `noise`(진폭·주파수·시드, 판독 컷 50%), `ramp`(CUT_THROUGH 앞 8F 가속 유지), `solved_pose`(B01 p0 ← `solved_pose_L2.json` 마지막 포즈).
2. B05 낮은 트럭(z = 1.135+0.15), B08 문턱 높이 돌리(follow), B12 45mm 장축 — 세 장축의 눈높이를 다르게.
3. B10–B12 를 D4 재설계로: 53개 전개 상태 시작 → 경계 통과 시 격납 → 5개 잔존. 카메라는 경계와 동행하는 높은 부감. `law_boundary.sweep_*` 유지.
4. B03·B09 치수선·기준선 성장 12F 사건을 `timing_s.json events` 에 추가, `SFX_CUES.csv` 큐 추가. 기준선 색 흰색(`palette.rule_white`).
5. B13 은 수직 부감 유지(D3). B13 마지막 24F 에 핸드헬드 노이즈 0(삼각대 실사로 컷).
산출물: `render/anim_r4d/` 270p 애니매틱, `evidence/rhythm_anim_r4d.json`, `evidence/verify_cam_bounds_r4d.json`, `evidence/verify_projection_r4d.json`
통과: 경계·판독 비 PASS, 판독 5컷 계기 전부 UI 안전영역 안, G-RHYTHM 수치 보고

### R4e 전환 A·B 프로젝션 브리지 (`src/projection_bridge.py`, `src/verify_match.py` 신설)
1. **전환 A**: L2 마지막 프레임(540p 발췌본의 F254 상당)을 솔브 카메라에서 프록시 기하(차내 바닥·문턱·발판·틈 벽)에 UV 투영. Base Color 로 넣고 F181–F192 에 Mix 팩터 1→0 드라이버. B01 p0·속도 벡터를 솔브 마지막 6F 에서 잇는다.
2. **전환 B**: 가림 와이프. B13 마지막 프레임(F1020) 과 L3 F2466 프레임을 1F 컷. 와이프 전후 6F 의 평균 밝기 차 ≤ 15, 가림 비율 ≥ 60% 를 `verify_match.py` 로 기록.
3. 핵심 4초 540p MP4 2개: `review/R4/key4s_transitionA_540p.mp4`(F151–F270, 실사 L2 + CG), `review/R4/key4s_transitionB_540p.mp4`(F960–F1080). 실사 구간은 540p 발췌본을 그대로 붙인다(색 보정 전).
4. 2 Mbps 스트레스 재인코딩 후 정상속도 판독 기록.
산출물: 위 MP4 2개, `evidence/verify_match_r4e.json`
통과: 투영 프레임 SSIM ≥ 0.80(전환 A), 속도 불연속 0, 가림 와이프 조건 충족

### R4f 조명 (변수 1개)
림 라이트를 열차 뒤(y≈5.4)에서 승강장 뒷벽 상단(dy −3.8, z ez+3.0)으로. 동일 210프레임 비교로 G-LOOK·색채도 전후 기록.
통과: G-LOOK 13/13 또는 미달 항목 수치 보고

### R4 마감
- `REPORT_R4.md`(R3 보고서 양식: 결론 → 작업 결과표 → 게이트 R3→R4 → 결정 필요 → 재현 명령), `LOCKS_R4.md` 변경 이력 갱신, `MANIFEST.json` sha256, 깨끗한 폴더 재현(§10.6).
- 검증 에이전트 재측정 수치 첨부.
- 드라이브 `보강작업/R4/` 에 패키지 zip·리뷰 패킷 업로드(쓰기 권한 없으면 사용자에게 업로드 요청).

## 5. 수정 파일 목록 (예상)

| 파일 | 작업 |
|---|---|
| `src/rig_config.json` | `car.x_offset_m`, `measure`, `foot.x_m`, `psd`, `car.profile/threshold/comb/bogie`, `tactile.dots`, `track.bed_type`, `panel.look/edge_band_m`, `array 53/5`, `figures.count 0`, `palette.rule_white`, `textures` |
| `src/camera_plan.json` | `lens_groups`, `ease`, `noise`, `ramp`, `solved_pose`, B05·B08·B12·B10–B12 재구도 |
| `src/timing_s.json` | 치수선·기준선 성장 사건 |
| `src/build.py` | PSD·차체 프로파일·대차·연단·점자블록 돌기·발판 외형·루버·인물 삭제·재질 노드 |
| `src/set_travel.py` | 노이즈·램프·솔브 포즈 |
| `src/track_import.py`, `projection_bridge.py`, `verify_match.py`, `measure_match_color.py`, `verify_flicker.py` | 신설 |
| `src/verify_bake.py`, `verify_scene.py`, `verify_cam_bounds.py` | 문 정렬·생존 비율·PSD 쌍·PSD 내부 금지 |
| `audio/SFX_CUES.csv` | 사건 추가 |
| `assets/LICENSES.csv`, `assets/README.md` | 신설 |
| `r4a/analyze_proxies.py` | 해상도 일반화 |

## 6. 게이트 (R4 종료 조건)

| 게이트 | 통과 조건 | 근거 파일 |
|---|---|---|
| G3 베이크 | PASS + 문 정렬·생존 비율 | `evidence/verify_bake_r4*.json` |
| G4 씬 | 미선언 충돌 0 | `evidence/verify_scene_r4*.json` |
| G4+ 경계·판독 | PASS, 판독 5컷 계기 UI 안전영역 | `verify_cam_bounds`, `verify_projection` |
| G-GEO | PSD 개구 ∋ 히어로·측정 x, PSD 내부 카메라 0 | 위와 동일 |
| G-MATCH | 재투영 ≤ 2px, 전환 A SSIM ≥ 0.80, 전환 B 가림 ≥ 60% | `evidence/verify_match_r4e.json` |
| G-TEX | ΔE ≤ 6 (3종), 2 Mbps 판독 기록 | `evidence/color_match_r4c.json` |
| G-LOOK | 13/13 (최소 12/13 + 사유) | `evidence/look_anim_r4*.json` |
| G-RHYTHM | 움직임 median ≥ 6.0, 정지 ≤ 3F. p90 은 레퍼런스 실측 전 가목표 | `evidence/rhythm_anim_r4*.json` |
| G-RATIO | 5/53 (9.43%) | `verify_bake` |
| N8 독립 재검증 | 수치 일치 | 별도 에이전트 |

## 7. 사용자 할 일 (작업 세션이 기다리는 입력)

`R4/USER_TODO.md` 에 명령어와 함께 정리. 요약: ① 540p 발췌본 5개 업로드(R4a-2 선행) ② 음성·화자·fps ③ 레퍼런스 2편 ④ 쇼츠 UI 실기 스크린샷 ⑤ 에셋 라이선스 답 ⑥ 검증자 지정·드라이브 편집자 공유 ⑦ 최종 렌더 실행 경로.
①이 없으면 R4b·R4c·R4d·R4f 는 진행 가능하고 R4a-2·R4e 만 대기한다. 대기 중에는 R4b 부터 시작한다.

## 8. 보고 형식

R3 보고서(`REPORT_R3.md`)와 같은 양식. 결론 1–2문장(됐는지, 무엇이 기준 미달인지 정직하게) → 작업 결과표(항목/상태/근거) → 게이트표 → 결정 필요(우선순위) → 재현 명령. 블로커는 굵게, 사용자 할 일은 번호 목록. 모델 식별자는 커밋·파일에 쓰지 않는다.
