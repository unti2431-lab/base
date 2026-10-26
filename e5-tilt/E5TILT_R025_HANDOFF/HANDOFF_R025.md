# HANDOFF R025 — E5 「작은 기울임의 원리」 프록시 리그·카메라·애니매틱

작성 2026-10-26 · 제작 Claude(클라우드, CPU) · 다음 제작 Codex · 검증 별도 세션/사용자

## 1. 한 문장 목표
320 km/h E5가 곡선에서 두 공기스프링의 높이차 약 5 cm로 차체를 1.5° 기울이는 과정을, 실차 안에서 끊기지 않는 시점으로 보여준다.

## 2. 현재 상태

| 영역 | 상태 | 근거 |
|---|---|---|
| G0 착수 판정 | 완료, 사용자 블로커 4개 남음 | PRODUCTION_PLAN_R025 P0, TASKS.json `blocked_by_user` |
| G1 레퍼런스 측정 | PASS | reference/REFERENCE_NOTES.md |
| G2 음성 | **부분** — VO 잠정 LOCK, 무음 구간 11개로 컷 정렬 PASS, 단어 타임스탬프 NOT_PERFORMED | audio/VO_LOCK.json, VO_PHRASES.json, evidence/sync_qc.json |
| G3 베이크 | PASS (20/20) | evidence/bake_qc.json |
| G4 씬 | PASS — 161프레임 전수, 충돌 0, 설계 접촉만 기록, 카메라 최소 0.218 m | evidence/scene_qc.json |
| 게이트 자가시험 | PASS — 4종 결함 주입 모두 FAIL로 검출 | evidence/gate_selftest.json |
| G5 애니매틱 | 270p 전편 + 오버레이 합성 완료, 판정은 §5 | review/R025/ |
| G6 핵심 4초 | NOT_PERFORMED (GPU 필요) | TASKS T08 |
| 히어로 대차·차체 에셋 | 프록시(절차 모델) | TASKS T05·T06 |
| 사운드 | 큐시트만 | audio/SFX_CUES.csv |

## 3. 재현 기준값 (T01에서 반드시 일치)

| 항목 | 값 |
|---|---|
| `tilt_bake.npz` sha256 (numpy 1.26.4, Linux) | `8ac9234666b22d3395939da785fcd1cc52093bf01374e8c2cd2fcc159a82c97e` — 다른 OS·numpy에서는 부동소수 차로 다를 수 있음. 그때는 아래 사건 값으로 판정 |
| 곡선 진입 / 완전 곡률 | F262 / F307 |
| 경사 시작 / 1.45° 도달 | F305 / F364 |
| 곡선 탈출 / 경사 0 복귀 | F610 / F705 |
| 최대 롤 | 1.500° |
| 스프링 높이차 최대 | 0.0497 m |
| 컵 잔여각 C04 최대 / C07 | 2.90° / 1.50° |
| 컷 F | 54, 118, 225, 319, 415, 497, 602, 713 |
| W0 일치 | 위치 차 < 1e-9 m, 각도 차 0° |
| G4 | 충돌 0, 설계 접촉 = 차축–축상, 차축–기어박스, 벨로우즈–베이스, ISO 고스트 |

## 4. 시스템 구조

```
rig_config.json ─┐
cameras.json ────┼─▶ kin.py ─▶ tilt_bake.npz ─▶ verify_bake.py (G3)
                 │      └────▶ evidence/geometry_qc.json (events)
                 │                     │
                 │                     ├─▶ sfx_cues.py ─▶ audio/SFX_CUES.csv
                 │                     └─▶ make_beats.py ─▶ BEATS_R025.csv
tilt_bake.npz ───┴─▶ build.py ─▶ work/e5tilt_R025_proxy.blend ─▶ verify_scene.py (G4)
                                   │  (+ import_assets.py + ASSET_MAP.json)
                                   ▼
                       render_frames.py (stage presets, resume) ─▶ work/frames_<stage>/
                                   ▼
                       comp_overlays.py (2.5D shapes from the bake) ─▶ frames_<stage>_comp/
                                   ▼
                       encode.sh / RUN_ALL.ps1 (BT.709) ─▶ review/R0NN/*.mp4 ─▶ sync_qc.py (G5)
```

핵심 설계
- **이벤트 역산**: 곡선 위치는 `curve_entry_F`·`curve_exit_F`에서 속도 곡선을 적분해 정한다. 비트를 옮기려면 F만 바꾸고 재베이크한다.
- **앵커 카메라**: 샷 키는 앵커 좌표계에 있다. `hero`(차체 중심의 궤도 좌표계, 롤 없음), `hero_body`(롤 포함, 객실), `world`, `ramp`(정지→열차 합류, C01), `iso`(공중 분해 세트), `w0`(C01 첫 프레임과 같은 상대 포즈로 끝남). 리그를 바꿔도 카메라가 따라온다.
- **W0 루프**: C09 끝 프레임이 C01 첫 프레임과 열차 기준으로 같은 포즈다. 슬래브·전주 간격을 전체 이동거리에 맞춰 배경 위상까지 반복된다.
- **X-ray·고스트·컵**: 오브젝트 커스텀 속성(`xray`, `vis`)과 셰이프키(`stroke`, `tilt`)를 베이크 키로 구동한다.
- **ISO 세트**: 고도 300 m의 분해용 대차 사본. 구름층은 C03 프레임에서만 렌더된다.

## 5. 알려진 한계 (정직한 격차)

1. **프록시 품질**: 차체·대차가 절차 모델이다. 레퍼런스 품질의 절반은 고정밀 에셋에서 나오므로 T05·T06 전에는 따라잡을 수 없다.
2. **1.5° 판독**: C06에서 실제 각도 그대로라 270p에서는 앰버 쐐기가 몇 픽셀이다. 형상 과장 없이 렌즈·높이·오버레이로 푼다(T04).
3. **동작량**: 애니매틱 측정값은 `evidence/sync_qc.json`. 목표(평균 ≥ 9) 미달 항목은 T02.
4. **명사 선행 노출**: 단어 타임스탬프가 없어 NOT_DECIDABLE. 클라우드에서 whisper 모델 다운로드가 차단됐다(huggingface 403). T03.
5. **경사 지연 1.2 s**는 연출값이다. 실제 E5 제어는 완화곡선 진입과 함께 움직인다. 내레이션이 "늦게 기운다"를 암시하면 안 된다.
6. **곡선 반경**: 화면의 R1000은 연출 축소다. 실제는 R4000. 수치를 화면에 쓰지 않는다.
7. **애니매틱 해상도**: 270×480, 6spp + OIDN. 재질 판독은 540p 이상에서만 판정한다.
8. **음성 길이 26.749 s vs 영상 26.767 s**: 인코딩에서 `apad` + `-shortest`로 맞춘다.

## 6. 통합 절차 (에셋이 들어올 때)
1. `src/ASSET_MAP.TEMPLATE.json` → `src/ASSET_MAP.json` 복사, 슬롯·행렬·`collide_with` 작성.
2. 가짜 에셋 스모크: `python src/import_assets.py -- --smoke --out work/smoke.blend` → `verify_scene.py --extra_pairs work/smoke_pairs.json`가 FAIL을 내는지 확인(자가시험 4번과 같음).
3. 실제 에셋: `RUN_ALL.ps1 -VerifyOnly -AssetMap src\ASSET_MAP.json` → G4 PASS.
4. 히어로 대차를 교체할 때는 같은 오브젝트 이름·피벗을 유지한다. `SPRING_?_BELLOWS`는 셰이프키 `stroke`(basis = h_min, key = h_max)를 반드시 가진다.

## 7. 렌더 예산 (실측)

| 단계 | 장비 | 실측 |
|---|---|---|
| 270p 6spp 애니매틱 | 클라우드 CPU 4코어 | 2.3–3.6 s/F (전편 약 40분) |
| 540p 16spp 스틸 | 같은 장비 | 33–73 s/F |
| 1080p 최종 | RTX 3060 Ti | **미측정** — 대표 프레임 F345 1장을 먼저 찍고 ×803으로 환산(추정 금지) |
