# LIFT R04 — 미해결 게이트 해결안 (작업 전달용)

- 작성: 2026-10-25 · 검토자 Claude(Fable) · 대상: 다음 작업 담당(코드·측정)
- 기준 문서: `review/R04/GATES_OPEN_R04.md`(미해결 게이트 보고), 「LIFT 종합 제작 지시서 (R03)」 §13
- 대조 소스: `LIFT_R3_R04b_sync.zip`(src·scripts·out/elem_bbox.npz·cam_keys_r02.json·events.json·SFX_CUES.csv·cam_check.json·R04 측정 JSON)
- 이 문서의 수치는 **zip 소스를 numpy로 다시 돌려 얻은 값**입니다. 보고서 값과 다르게 본 곳은 "재판정"으로 표시했습니다.
- 상태 표기는 지시서 §13 규칙(PASS / FAIL / NOT_PERFORMED / NOT_DECIDABLE)만 씁니다.

---

## 0. 검토 결과 한눈에

보고서의 우선순위(L-G14 → L-G15 → L-G22 → L-G19 → L-G12/18 → 나머지)는 맞습니다. 소스를 대조해 보니 **원인이 보고서와 다른 곳이 둘** 있어, 수정 방법이 달라집니다.

| # | 항목 | 보고서의 원인 | 재검토 결과 | 결과가 바뀌는 것 |
|---|---|---|---|---|
| 1 | L-G15 루프 | "끝 구간 감속과 첫 구간 접선 크기, 렌즈 기울기를 안 맞춤" | **C8/b 마지막 구간(F1145→1203)이 U턴**입니다. F1145 키(x −1.05)가 루프점(x −1.63)보다 앞(+X)에 있어, 카메라가 −X로 가다가 끝접선(+X, C1 방향)을 맞추려고 x −1.706(F1190)까지 넘어갔다가 되돌아옵니다. 여기에 Hermite 끝접선은 해석적 미분만 맞추므로 **이산 1F 속도**는 맞지 않습니다(렌즈 24→32 곡률 때문에 −0.0128 vs −0.0335). | 접선 값만 조정해서는 못 풉니다. **루프 창(F1179–F25) 직선 구간**을 두면 기본 경로에서 세 기준 모두 0.0(§2.1 수정안 A, 수치 검증 완료). |
| 2 | L-G12·L-G18 F1108 | "C8 F1108에서 구동 타이어가 가장자리 −0.01 u로 1F 이탈" | **측정 오류입니다.** `elem_bbox.npz`는 오브젝트 bound_box 8꼭짓점을 월드로 변환한 것이라 **회전하는 바퀴와 함께 상자가 돕니다**(z 최저가 −0.205 m, 땅 아래). `contact` 모드(최저 4꼭짓점 평균)는 바퀴 1/4회전(약 26F)마다 x가 ±0.35 m 톱니로 뜁니다(F1107 u 0.271 → F1108 u −0.008). | 카메라를 고칠 필요가 없습니다. **접지점 산출 방식을 고치면** F1108 실패가 사라지고, `<= 2` 허용치를 `== 0`으로 되돌릴 수 있습니다. |
| 3 | L-G22 | 리맵 K·R04 표시 미반영 | 보고서대로입니다. `remap.table`로 **표시 시각을 직접 계산**했습니다(§2.3 표). 범퍼 접촉 표시 F1031, SFX·events는 F1043 → 12F 차. R04 표시 사건 9개는 `build_scene_lift.py`·`ovl_lift.py`가 각자 E 값에서 계산하고 기록에 없음. | `events.json`에 `display_F`와 표시 사건을 넣는 것은 `bake_kin_lift.py` 한 곳 수정으로 됩니다(§2.3). |
| 4 | L-G19 접지 띠 | 상자가 타이어 위에 떨어짐 → Cryptomatte 필요 | 보고서대로. 참고로 `emph_post.py`에 **Cryptomatte 디코딩(`mmh3_32`, `crypto_id`, `load_exr`, `mask_for`)이 이미 있습니다.** 새로 짤 것은 측정 스크립트 30행뿐입니다. | §2.4 |

### 셰이크와 L-G15 기준에 대한 판단 (게이트 해석, 기록 필요)
- 셰이크(`cam_paths.shake`)는 테이크 길이 231F(C8 147F + C1 84F)의 정수 주기 사인파라 **이음에서 위상이 연속**입니다(F_END+1 오프셋 = F1 오프셋, 수치 확인). 
- 그러나 셰이크 자체가 고주파(61·97 사이클/231F)라 **셰이크 포함 경로의 1F 속도 차는 테이크 어디서나 중앙값 1.5 mm/F, 최대 2.7 mm/F**(조준은 6.8 / 12.1 mm/F)입니다. 이음(1.28 / 2.04 mm/F)은 그 분포 안쪽입니다.
- 따라서 "속도 벡터 차 ≤ 0.5 mm/F"는 **기본 경로(셰이크 제외)**에만 적용할 수 있고, 셰이크는 "이음에서의 차가 테이크 내부 분포(p95) 안에 있고 위상이 연속"으로 따로 판정해야 합니다. 이 해석을 `cam_check.py` 출력과 LOCKS 기록에 명시합니다(사용자 확인 1줄).

---

## 1. 작업 순서 (의존관계 기준)

```
[코드, 렌더 불필요]                           [렌더 필요]                     [사람]
1 export_bbox 접지점 수정 ──┐
2 cam_paths 패치 + 루프 창 키 ─┼→ 3 build_scene 재빌드 → cam_check → verify_scene(G4)
4 bake_kin events display_F ──┘        │
                                        ├→ 5 새 스테이지 렌더(anim540r5, e954e98b 이후 씬)
                                        │     ├→ 6 L-G19 Cryptomatte 측정 → 부족하면 띠 상향 → 재렌더(C5·C6만)
                                        │     ├→ 7 L-G17 렌더 ΔE 표, L-G15 SSIM·바퀴 위상
                                        │     └→ 8 L-G20 스트레스본 → 사용자 폰 시청
                                        └→ 9 sync_qc(L-G13), L-G10 서브프레임, L-G03/08 게이트 JSON 편입
                                                                                 10 L-G14 5인 검수(사용자 섭외, R05 영상으로)
```

- 1·2·4는 서로 독립이라 같이 진행합니다. 3에서 한 번에 검증합니다.
- **L-G14 검수 영상을 R04로 받을지 R05(루프·사건 기록 수정본)로 받을지**는 사용자 결정입니다. 루프 이음과 SFX 시각은 Q1–Q7 이해도에 영향이 없으므로, 섭외가 빠르면 R04로 먼저 받아도 됩니다(권장: 섭외 즉시 R04로 시작, 영상을 바꾸지 않음).

---

## 2. 항목별 해결안

형식: 원인(검증) / 수정(파일·함수·값) / 검증·합격 조건 / 담당

### 2.1 L-G15 루프 — FAIL → 수정안 A (수치 검증 완료)

**원인(검증)**
- 현재 C8/b 키: F1096 (0.45, −4.40, 0.45) → F1145 (−1.05, −3.60, 0.52) → F1203 (−1.63, −3.02, 0.28). C1 첫 구간 현(chord) 접선은 (+13.56, +2.22, +2.00) mm/F.
- 카메라 x: F1145 −1.05 → F1179 −1.639 → **F1190 −1.706** → F1202 −1.643 → F1 −1.63. 루프점을 넘어갔다 되돌아오는 U턴이 마지막 13F 안에 있습니다. 그 결과 F1201→1202 속도 12.05 mm/F, 이음 13.25, F1→2 13.45.
- `camera_arrays`는 C8/b 마지막 서브샷에 `t1=t_loc`만 주고 **키별 명시 접선(5번째 원소)을 무시**합니다. 지금 keys JSON에 C8/b 접선을 넣어도 효과가 없습니다.

**수정**
1. `src/cam_paths.py` 패치(부록 A): C8 마지막 서브샷에도 `tans=` 전달, C1 첫 키에 명시 접선이 있으면 그것을 `t_loc/t_tgt/t_len`으로 사용.
2. `scripts/cam_autoframe.py` SPEC에 **루프 창 키 4개** 추가(부록 B 값). 창 폭 N = 24F, 공통 속도 V = C1 현 접선, 렌즈 32.0 고정(변화율 0):
   - C1: F1 키에 접선 [V, Vt, 0], **F25 키 추가** = F1 + 24·V, 접선 동일
   - C8/b: **F1179 키 추가** = F1 − 24·V, 접선 동일, F1203 키 접선 동일
   - 두 키 사이 Hermite는 위치차 = 24·V, 양끝 접선 = V라서 **정확히 직선**이 됩니다. 이음 양쪽 1F 속도가 V로 같아집니다.
3. U턴은 사라지지 않고 **F1145–F1179 안으로 들어갑니다**(x −1.05 → −1.955 → 직선 복귀). 34F 동안 −X 26 mm/F로 갔다가 +X 13.6 mm/F로 바뀌는 스윙입니다. 화면으로 확인해 과하면 **F1145 키를 x −1.75 ~ −1.9로 옮겨**(reveal_deck 구도 재오토프레임) 스윙 폭을 줄입니다. 이 결정은 렌더 전 `cam_check` 수치 + 270p 시험 렌더로 합니다.

**검증한 값(기본 경로, 셰이크 제외)**

| 값 | 현재 | 수정안 A | 기준 |
|---|---|---|---|
| ‖v(F1→2) − v(F_END→F1)‖ | 0.512 | **0.000** | ≤ 0.5 mm/F |
| ‖v(F_END→F1) − v(F_END−1→F_END)‖ | 1.432 | **0.000** | ≤ 0.5 mm/F |
| 방향 cos | 0.9994 | **1.0000** | ≥ 0.99 |
| 렌즈 변화율 차 | −0.0207 | **0.0000** | 0 |
| 조준점(tgt) 속도 차(이음/첫) | 0.727 / 0.369 | **0.000 / 0.000** | 기록 |
| cam_check 프레이밍 실패 | 1(F1108, 측정 오류) | 2(F1108 + **C1 F57** 리프트 타이어 u 0.862 > 0.86) | 0 |

- C1 F57 실패는 F25 키 삽입으로 F46 키의 Catmull-Rom 접선이 바뀌어 생긴 0.002 u 스침입니다. **F46 키를 y −2.92 → −2.95로 옮기거나 F46에 명시 접선을 주면** 해결됩니다(cam_autoframe 재실행 후 확인).

**`cam_check.py`에 넣을 합격 조건**
```python
seam_ok = seam["dv_end_vs_seam_mm"] <= 0.5 and seam["dv_seam_vs_F1_mm"] <= 0.5 and seam["cos"] >= 0.99 and abs(seam["dlens"]) < 1e-6
# 셰이크 연속성: 셰이크만의 오프셋(with − without)을 C8→F_END→F1→C1 순서로 이어 1F 차를 구하고,
# 이음 2개 값이 테이크 내부 p95 이하 + 오프셋(F_END+1) == 오프셋(F1) 이면 PASS
```
결과를 `loop_seam.pass`, `loop_seam.shake_continuity`로 JSON에 기록하고 FAIL이면 종료 코드 1.

**렌더 뒤 보조 기록**: F1172–1202 + F1–30 이어 붙여 SSIM·픽셀비, 노면 점선 27F 주기 확인(lane_dash F1191 → F16 = 27F ✓ 설계상 맞음). 사용자 연속 재생 확인.

담당: 작업 담당(코드·측정) → 사용자(시청)

### 2.2 L-G12 / L-G18 — 허용치 제거 + 측정 오류 수정

**원인(검증)**
- `scripts/export_bbox.py`가 `o.bound_box`(오브젝트 로컬 AABB) 8꼭짓점을 `matrix_world`로 변환합니다. 바퀴는 Y축 회전 애니메이션이 있어 **상자가 바퀴와 함께 돕니다**. 구동 타이어 C8 구간에서 상자 z 범위 −0.205 ~ 1.195(실제 0 ~ 1.1).
- `contact` 모드가 "최저 4꼭짓점 평균"을 접지점으로 쓰므로 x가 1/4회전마다 −0.348 ↔ +0.348로 뜁니다. F1108은 그 톱니의 불연속 지점이고, **다른 모든 프레임의 접지점도 최대 0.35 m 틀립니다.**
- `box` 모드도 회전 상자 때문에 최대 √2배 부풀어, 오토프레임 렌즈가 필요 이상 넓어질 수 있습니다(리프트 타이어는 고속도로에서 회전 0이라 영향 없음, 구동 타이어·C2 야드 바퀴는 영향 있음).

**수정**
1. `scripts/export_bbox.py`: 꼭짓점 8개 대신 **평가된 메시 정점의 월드 AABB**를 저장합니다(형식은 8꼭짓점 그대로 유지해 하위 호환).
   ```python
   me = o.to_mesh(); P = np.array([tuple(mw @ v.co) for v in me.vertices]); o.to_mesh_clear()
   lo, hi = P.min(0), P.max(0); arr[k, F] = [[x, y, z] for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])]
   ```
   타이어 메시 정점 수가 많으면 `[::5]` 표본으로 충분합니다(AABB 오차 < 1 cm).
2. `framing_req.py`·`cam_check.py`·`verify_scene_lift.py`의 `contact` 모드: "최저 4꼭짓점 평균" 대신 **AABB 바닥면 중심** `[(lo+hi)/2 x, (lo+hi)/2 y, lo z]`를 씁니다(세 파일 같은 식).
3. `verify_scene_lift.py` 100–102행: `len(bad) <= 2` → **`len(bad) == 0`**, `tolerance` 키 삭제. L-G12와 L-G18을 **다른 bad 목록**으로 나눕니다.
   - L-G12 `relation_elements_in_frame`: 화면 안(0 ≤ u ≤ 1, 0 ≤ v ≤ 1, z > 0) 판정
   - L-G18 `new_info_bbox_outside_ui_mask`: UI 마스크(u ≤ 0.86, v ≤ 0.78) 판정
4. L-G18 추가 기록: CU 간극 ≥ 4%(C8/a F1056–1095, 리프트 타이어 바닥 ↔ 노면 투영 차), F1 썸네일 판독 항목(간극 휘도비 23.7 PASS는 이미 있음 → `thumbnail_F1` 체크에 간극 %·휘도비·바퀴 식별 bbox를 같이 기록).

**검증**: `cam_check` 프레이밍 실패 0, `verify_scene` L-G12·L-G18 각각 fail_frames 0. 완화가 정말 필요해지면 LOCKS 절차(사유·날짜·영향)로 사용자 승인 뒤에만.

담당: 작업 담당

### 2.3 L-G22 사건 기록 = 화면

**표시 시각(검증, `remap.table`)**

| 사건 | events.F(베이크) | 화면 표시 F | 차 | 비고 |
|---|---|---|---|---|
| lift_axle_liftoff | 1019 | 1019 | 0 | K 구간 시작, src 1019.0 |
| (범퍼 진입 가속) | — | 1025–1030 | — | src 1022.9 → 1035.1, 속도 1.06 → 5.72 |
| **lift_complete(범퍼 접촉)** | **1043** | **1031** | **−12F** | `bump_frame` = liftoff + 12, src 1043.0 도달 |
| (정착) | — | 1032–1055 | — | src 1043.5 → 1055, 속도 0.5(슬로우) |

SFX `lift_fill` 끝 1043 → 1031, `lift_complete` 1043 → 1031. 셰이크 히트는 이미 `bump_frame`(1031)이라 맞습니다.

**R04 표시 사건(현재 코드에서 계산되는 값, 기록에 없음)**

| 이름(제안) | F | 계산식(현재 코드) | 파일 |
|---|---|---|---|
| ghost_preview_in | 189 | tA+4 (tA = '가변축이' 185) | build_scene_lift |
| ghost_drop_start | 203 | tA+18 | build_scene_lift |
| ghost_touch | 222 | tA+37 (약한 발광 6F) | build_scene_lift |
| ghost_fade_out | 235–245 | C3−12 → C3−2 | build_scene_lift |
| limit_blink_1/2/3 | 163 / 618 / 928 | down_condition / drive_below_limit / p_raise_below_rel, 각 12F | ovl_lift |
| ghost_bar_rise | 783 | sensor_info_at_ctrl, 18F | ovl_lift |
| ghost_bar_shrink + deny_shake + stop_sign | 853 | deny_display, 9F / 12F / 페이드 | ovl_lift |
| bars_out_C2 | 197 | GHOST_WIN[0]+8 | build_scene_lift(bars_to) |

**수정**
1. `src/bake_kin_lift.py` `main()`: 사건마다 `display_F` 필드 추가. 기본 `display_F = F`, K 구간은 `remap.table(C)`를 역으로 찾아 **src가 사건 F에 처음 도달하는 출력 F**. 리맵은 표시 층이지만 `remap`은 numpy 전용이라 bake 단계에서 import 가능(순서 의존 없음). 위 표의 R04 표시 사건을 `DESC`에 추가(`physical_F: null`, `layer: "display"`).
2. `SFX` 표의 `F_of()`가 `display_F`를 읽게 하고(`lift_fill` 끝·`lift_complete`가 1031이 됨), CSV에 `display_F` 열 추가.
3. `build_scene_lift.py`(G_IN 등)·`ovl_lift.py`(blink_at, 유령 막대, 흔들림)·`cam_paths.shake`(히트 시각)가 **`evidence/events.json`에서 읽도록** 바꿉니다. 현재는 각자 `E[...] + 상수`로 계산하므로, events.json의 값을 쓰는 한 줄씩이면 됩니다. 중복 계산을 없애야 L-G22 검사가 의미를 가집니다.
4. `verify_scene_lift.py` L-G22 검사 추가: `sfx_start_eq_display_F_1F`(모든 SFX 행), `display_events_present`(위 9개 이름 존재), `shots_bump_eq_display`(shots.json에서 src가 lift_complete에 도달하는 F == display_F).
5. SFX 소리는 큐만 있고 소스가 없습니다(`source_file`·`license` 빈칸). **사용자 방침(라이선스 음원 사용 여부) 필요** → T21.

담당: 작업 담당(코드), 사용자(SFX 방침)

### 2.4 L-G19 접지 띠 — Cryptomatte 정식 측정

**원인**: 보고서대로. 띠는 타이어 바로 밑(폭 0.46 × 0.50 m, 카메라 쪽으로 5 cm 돌출)이라 C5 측면 구도에서 보이는 녹색은 560–604 px(0.1%)뿐.

**수정(측정)**
1. 새 스크립트 `scripts/measure_band_crypto.py`: `src/emph_post.py`의 `crypto_id`, `load_exr`, `mask_for`를 import. on 프레임(F640·F700)은 `mask_for(F, ["CONTACT_BAND_R"])` 커버리지 ≥ 0.5 픽셀의 선형 휘도 평균, off 프레임(F585, 같은 컷 C5/a)은 **같은 화면 좌표의 노면**(F585에는 띠가 꺼져 있어 Cryptomatte에 띠가 안 잡히면 F640 마스크 좌표를 그대로 사용 — 카메라 드리프트 ≤ 1 mm/F라 30F 동안 2 px 이내).
2. 거절 적색은 `out/<stage>/ovl/F0853.png`의 **알파 채널**에서 빨간 픽셀을 세면 막대와 분리됩니다(`ovl` 폴더에 OVL 레이어가 따로 저장됨). 막대는 u 0.26·0.74 세로 직사각형이라 bbox로 제외.
3. 판정은 **같은 컷 비교(C5 F640:F585, F700:F585)를 정본**으로. C6:C2 비교는 `luma_grade` 게인(C6 어둡게·C2 밝게)이 끼므로 **rgb(게인 전) 값만 참고 기록**. 기준 3 미만이면:
   - 1차: `build_scene_lift.py` `cg_vis` 바닥값 0.35 → 0.5(표시층 값, LOCKS 아님)
   - 2차: `lift_geo.mat_contact` 발광 계수 2.2 → 3.0
   - 3차: 띠 폭 0.46 → 0.60 m(카메라 쪽 돌출 +7 cm) — 형상 변경이라 CHANGELOG 기록
4. 측정 결과 `review/R05/band_measure_crypto.json`과 마스크 확인 시트(마스크를 빨간색으로 덮은 F585·F640·F700·F800 JPG).

**검증**: C5 on:off ≥ 3(rgb·comp 둘 다), 거절 링 ≥ 400 px(링만). 통과하면 L-G19 PASS, 아니면 띠 상향 후 C5·C6만 재렌더.

담당: 작업 담당

### 2.5 L-G10 충돌 — 서브프레임 2

- `verify_scene_lift.py` 위험 구간 루프에서 `sc.frame_set(F, subframe=0.5)`를 추가해 **서브프레임 2**(F, F+0.5)로 검사. 위험 구간에 **리맵 K 구간 F1019–1031의 소스 프레임(src 1019.0 → 1043.0, `remap.table`)**을 포함합니다. 렌더는 `frame_set(int, subframe)`로 소스 상태를 보여 주므로 소스 프레임 범위 1019–1043을 소수점 포함으로 검사하는 것이 맞습니다.
- 그때까지는 L-G10 항목 상태를 **PASS_WITH_NOT_PERFORMED**로 정직하게 기록(`put(..., status="NOT_PERFORMED")`로 subframes 체크를 별도 항목으로).

### 2.6 L-G09 팝 — 해석 기록 + 렌더 씬 일치

- "서브샷 전환 = 컷 경계" 해석을 LOCKS에 1줄 기록(사용자 승인). 코드는 이미 그 기준으로 검사합니다.
- 렌더한 씬 `4ed690f6`에는 고스트 hide_render 키가 남아 있었습니다. **다음 렌더(anim540r5)는 `e954e98b` 이후 씬**으로 하고 `render_log.csv`의 render_key가 verify_scene 대상 blend sha와 같은지 체크를 `verify_scene`에 추가(`scene_sha_eq_render_log`).

### 2.7 L-G13 명사 선행 — sync_qc 작성 (스크립트 없음)

- 새 `scripts/sync_qc.py`(numpy 전용, Blender 불필요):
  1. 명사 → 오브젝트 표(제안): 센서→`DRV_SENSOR_R`, 제어기→`CTRL_BOX_R`, 밸브/공기 길→`VALVE_BLOCK_R`, 공기주머니(들던)→`LIFT_BAG_LIFT_R`, 주머니(누르는)→`LIFT_BAG_RIDE_R`, 가변축/바퀴→`WHL_L_R_TIRE`, 옆 차축→`WHL_D_R_TIRE`, 짐/하중→`COIL`, 땅/접지→`CONTACT_BAND_R`.
  2. 첫 발화 F = `remap.word_frames(C)` (문장 k, 단어). 첫 노출 F = `elem_bbox.npz` + `shots.json` 카메라로 투영해 **화면 안·UI 마스크 밖·폭 ≥ 0.03 u**인 첫 프레임(해당 컷의 레이어가 보이는지 `wX`로 확인: XRI 전용 요소는 wX = 1인 프레임만).
  3. 합격: 첫 노출 ≤ 첫 발화 − 6. 결과 `evidence/sync_qc.json`, `verify_scene`의 L-G13이 이 파일을 읽어 판정.
- R04 변경(C2 고스트, C4 구도)이 반영된 `elem_bbox.npz`(재빌드 후 export) 기준으로 계산.

### 2.8 L-G17 색 역할 — 렌더 표본 ΔE00

- `scripts/measure_de_crypto.py`: Cryptomatte 마스크(`emph_post.mask_for`)로 상태색 면 표본 → sRGB 평균 → `verify_scene_lift.de00` 재사용. 표본 프레임: 녹색 띠 F640, 청록 주머니 F400(리프트)·F660(하중용), 호박 링 F315·F763, 적색 링 F856, 흰 기준선 F170, 노랑(해당 요소 F 확인).
- OVL 요소(막대·링·유령 막대·금지 도형)는 `out/<stage>/ovl/*.png` 알파 > 0.9 픽셀에서 직접 표본(렌더를 거치지 않으니 설계값과 같아야 함 — 다르면 리사이즈 LANCZOS 번짐).
- 추가 확인: 고스트 바퀴 외곽 발광(0.80, 0.90, 1.0 → 거의 흰 청색)과 공기 청록 `#00C2F2`의 ΔE00. 15 미만이면 고스트 색을 흰색(`#F3F3F3`) 쪽으로 옮깁니다(비상태 요소이므로 ≥ 15 또는 비중첩 기준).
- OVL on/off FULL 차이: `rgb` vs `comp`에서 OVL 알파 0인 픽셀만 비교 → ≤ 1/255(luma_grade 게인 1.0인 프레임에서).

### 2.9 L-G20 저비트레이트 · L-G16 인코딩 · L-G21 재현성

- L-G20: `ffmpeg -i LIFT_R0x.mp4 -c:v libx264 -b:v 2M -maxrate 2M -bufsize 4M -pix_fmt yuv420p -movflags +faststart stress_2M.mp4` → 블라인드 보조(새 에이전트) → 사용자 폰 1회. 점검 포인트: 노면 줄무늬(C1·C8), 고스트 반투명 밴딩(F189–245), 유령 막대 깜빡임(F783–862).
- L-G16(G8): `scripts/delivery_qc.py` — 프레임 수 1202, `ffprobe` 디코드 오류 0, 색 태그 bt709/bt709/bt709, 오디오 패킷 연속, `ebur128` I −14 ±1 LUFS·TP ≤ −1 dBTP. SFX 믹스 후 재측정.
- L-G21(G9): `run_pipeline.sh`에 HANDOFF §2 순서 그대로(타이밍 → 베이크 → 검증 → 믹스 → 빌드 → bbox → autoframe → 재빌드 → cam_check → verify_scene). `MANIFEST.json`은 npz·events·게이트 JSON의 sha256(시각·절대 경로 키 제외, `sort_keys=True`). 새 폴더 재실행 비교.

### 2.10 L-G03 · L-G08을 게이트 JSON에 편입

- `verify_bake_lift.py`에 R04 발광 정의(`emission_curve_R04.csv`의 `lift_R04_abs`, `ride_R04_abs`)로 하강 구간 F406–591 단조성 검사 추가(리프트 비증가, 하중용 비감소). 보고서 값 0.758→0.665 / 0.148→0.277 PASS.
- L-G08 사건 간격: `events.json`의 `visible: true` 사건 **display_F** + 컷 경계로 최대 간격 ≤ 3 s, C7b 최소 간격 ≥ 9F(beat_group 제외). 2.3 완료 뒤 계산해야 리맵·R04 표시가 반영됩니다.

---

## 3. 사용자 결정 요청 (짧게)

| ID | 질문 | 권장 |
|---|---|---|
| D-R5-1 | L-G14 5인 검수를 R04 영상으로 바로 시작할지, 루프·사건 기록 수정본(R05)까지 기다릴지 | **R04로 즉시 시작**(이해도 문항과 무관한 수정) |
| D-R5-2 | L-G15 셰이크 판정 해석: 속도 기준은 기본 경로, 셰이크는 위상 연속 + 분포 내로 별도 판정 | 승인 요청 |
| D-R5-3 | L-G09 "서브샷 전환 = 컷 경계" 문구 | 승인 요청 |
| D-R5-4 | L-G12/L-G18 허용치 `<= 2` → `== 0` 복원(측정 오류 수정으로 완화 불필요) | 복원 |
| D-R5-5 | SFX 소스 방침(라이선스 음원 / 직접 합성 / 무음 유지) | T21 착수 전 필요 |
| D-R5-6 | G0 미기록 사항: D-C1 고정 댓글 문구, 위협 축 판정, G-1 중복 확인 → `LOCKS.md`·`TASKS.json` 생성 | 결정 기록 |
| D-R5-7 | 루프 창 때문에 C8/b 스윙(F1145–1179)이 커 보이면 F1145 키 이동 허용(reveal_deck 구도 소폭 변경) | 270p 시험 후 판단 |

---

## 4. 완료 정의 (체크리스트)

- [ ] `cam_check.json`: `loop_seam.pass` true, 프레이밍 실패 0, 정지 0, 접지창 ≤ 1 mm/F
- [ ] `verify_scene.json`: L-G12·L-G18 fail 0(허용치 없음), L-G22 display 검사 PASS, L-G10 서브프레임 PASS 또는 상태 정직 표기, L-G13 sync_qc PASS
- [ ] `events.json` v2: `display_F` 전 사건, R04 표시 사건 9개, SFX_CUES `display_F` 열, lift_complete 1031
- [ ] 렌더 `anim540r5`: 씬 sha = verify_scene 대상 sha(`e954e98b` 이후)
- [ ] L-G19 Cryptomatte: C5 on:off ≥ 3, 거절 링 ≥ 400 px
- [ ] L-G17 렌더 ΔE 표, L-G15 SSIM·바퀴 위상, L-G20 스트레스본 + 폰 시청 기록
- [ ] `review/R05/CHANGELOG.md` 변수별 기록, LOCKS 변경(D-R5-2·3) 기록
- [ ] L-G14: 사용자 섭외 → `human_test.md` R04 표 채움 → 4/5 재현·같은 오해 0
- [ ] G7 PASS + 사용자 승인 → 1080p(G8) 착수

---

## 부록 A. `src/cam_paths.py` 패치 (수정안 A 전제)

```diff
@@ def camera_arrays(C, with_shake=True):
     c1 = K["C1"]; n1 = c1[1][0] - c1[0][0]
-    t_loc = (c1[1][1] - c1[0][1]) / n1; t_tgt = (c1[1][2] - c1[0][2]) / n1; t_len = np.array([(c1[1][3] - c1[0][3]) / n1])
+    if len(c1[0]) > 4:                                                  # explicit C1 start tangent (loop take) → shared by the C8 end
+        t_loc, t_tgt, t_len = c1[0][4][0], c1[0][4][1], np.array([c1[0][4][2]])
+    else:
+        t_loc = (c1[1][1] - c1[0][1]) / n1; t_tgt = (c1[1][2] - c1[0][2]) / n1; t_len = np.array([(c1[1][3] - c1[0][3]) / n1])
     last = {c: max((l for l in K if l == c or l.startswith(c + "/")), key=lambda l: K[l][0][0]) for c in cuts}
     for lab, c, a, b in subshots(C):
         ks = K[lab]
         Fs = np.arange(a, b + 1)
-        if lab == last["C8"]:
-            Lp = hermite(Fs, [(k[0], k[1]) for k in ks], t1=t_loc)
-            Tp = hermite(Fs, [(k[0], k[2]) for k in ks], t1=t_tgt)
-            Ln = hermite(Fs, [(k[0], k[3]) for k in ks], t1=t_len)[:, 0]
+        tl = {i: k[4][0] for i, k in enumerate(ks) if len(k) > 4}; tt = {i: k[4][1] for i, k in enumerate(ks) if len(k) > 4}
+        tn = {i: np.array([k[4][2]]) for i, k in enumerate(ks) if len(k) > 4}
+        if lab == last["C8"]:                                           # loop seam: C8 end tangent = C1 start tangent (explicit per-key tangents kept)
+            Lp = hermite(Fs, [(k[0], k[1]) for k in ks], t1=t_loc, tans=tl)
+            Tp = hermite(Fs, [(k[0], k[2]) for k in ks], t1=t_tgt, tans=tt)
+            Ln = hermite(Fs, [(k[0], k[3]) for k in ks], t1=t_len, tans=tn)[:, 0]
         else:
-            tl = {i: k[4][0] for i, k in enumerate(ks) if len(k) > 4}; tt = {i: k[4][1] for i, k in enumerate(ks) if len(k) > 4}
-            tn = {i: np.array([k[4][2]]) for i, k in enumerate(ks) if len(k) > 4}
             Lp = hermite(Fs, [(k[0], k[1]) for k in ks], tans=tl); Tp = hermite(Fs, [(k[0], k[2]) for k in ks], tans=tt)
             Ln = hermite(Fs, [(k[0], k[3]) for k in ks], tans=tn)[:, 0]
```

## 부록 B. 루프 창 키 값 (수정안 A, `cam_keys_r02.json` 형식)

V = (0.013556, 0.002222, 0.002000) m/F, Vt = (−0.002, −0.004, −0.001333) m/F, 렌즈 32.0 고정. `TAN = [V, Vt, 0.0]`

```json
"C1": [
 [1,   [-1.63, -3.02, 0.28],        [1.45, -0.56, 0.74],   32.0, TAN],
 [25,  [-1.30467, -2.96667, 0.328], [1.402, -0.656, 0.708], 32.0, TAN],
 [46,  [-1.02, -2.92, 0.37],        [1.36, -0.74, 0.68],   30.5],
 [85,  [1.08, -2.1, 0.65],          [1.32, -1.05, 0.65],   30.0, [[0.08, 0.03, 0.012], [0.0, -0.004, -0.003], 0.0]]
],
"C8/b": [
 [1096, [0.45, -4.4, 0.45],          [1.0, -1.0, 0.36],     24.0],
 [1145, [-1.05, -3.6, 0.52],         [1.05, -0.62, 0.7],    24.0],
 [1179, [-1.95533, -3.07333, 0.232], [1.498, -0.464, 0.772], 32.0, TAN],
 [1203, [-1.63, -3.02, 0.28],        [1.45, -0.56, 0.74],   32.0, TAN]
]
```

`cam_autoframe.py` SPEC에서는 C1 F1·F25, C8/b F1179·F_END+1 항목을 `(tgt, lens)` 튜플 + 7번째 원소 `TAN`으로 넣으면 같은 JSON이 나옵니다. F46 키는 F57 스침(u 0.862) 해소를 위해 y −2.95 또는 명시 접선으로 재조정 후 `cam_check` 확인.

## 부록 C. 검증에 쓴 명령 (numpy만, Blender 불필요)

```bash
# 이음 수치 (셰이크 포함/제외)
python3 -I - <<'EOF'
import sys, json, numpy as np; sys.path.insert(0, 'src'); import cam_paths as CP
C = json.load(open('src/rig_config_lift.json')); F_END = C['plan']['F_END']
for ws in (False, True):
    _, loc, tgt, lens = CP.camera_arrays(C, with_shake=ws)
    v_end = loc[F_END]-loc[F_END-1]; v_1 = loc[2]-loc[1]; v_seam = loc[F_END+1]-loc[F_END]
    print(ws, np.linalg.norm(v_seam-v_end)*1000, np.linalg.norm(v_1-v_seam)*1000,
          v_seam@v_1/np.linalg.norm(v_seam)/np.linalg.norm(v_1), (lens[2]-lens[1])-(lens[F_END]-lens[F_END-1]))
EOF
# 구동 타이어 접지점 톱니 확인
python3 -I -c "
import numpy as np; b=np.load('out/elem_bbox.npz')['WHL_D_R_TIRE']
print([round(float(b[F][np.argsort(b[F][:,2])[:4]].mean(0)[0]),3) for F in range(1100,1112)])"
```

## 부록 D. 지키는 제약 (지시서 그대로, 변경 없음)
- `lift_kin.solve()` 수정 금지, 수치는 `rig_config_lift.json`으로만. 이 문서의 수정은 모두 표시층(카메라·OVL·측정·기록)입니다.
- LOCKS 절차 밖 임계값 완화 금지. 허용치 `<= 2`는 제거합니다.
- 1080p는 G7 PASS + 5인 검수 보고 + 사용자 승인 뒤.
- PC 폴더 삭제 불가 → 새 렌더는 새 스테이지 이름(`anim540r5`).
- 한 라운드 변수 여럿이면 CHANGELOG에 변수별 분리 기록.
