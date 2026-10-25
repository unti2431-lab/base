# HANDOFF_R02.md — DEL74 인계 (온라인 Claude → 오프라인 작업, 2026-10-25)

## 1. 한 문장 목표
"카메라가 한 번도 멈추지 않고 기관차 밖→안→대차→밖으로 흘러가는 동안, 엔진에서 바퀴까지의 길에 기계 연결이 없다는 것이 다섯 번의 투시로 눈에 박힌다." (REVISION_PLAN_R02 P1)

## 2. 현재 상태표
| 게이트 | 상태 | 근거 |
|---|---|---|
| G0 착수 | PASS | LOCKS R02, 풀3D형 확정, 에셋=구매+자체 리그 승인 |
| G1 레퍼런스 | PASS | reference/REFERENCE_NOTES.md (Bf 109 쇼츠 실측 → 목표값) |
| G2 음성 락 | PASS | audio/VO_LOCK.json, VO_WORDS.json, BEATS.csv(C07b 문구만 수정) |
| G3 베이크 | **PASS 28/28** | evidence/bake_qc.json (무미끄럼·기어·1:1·사건 F·루프·카메라·명사 선행) |
| G4 씬 충돌 | **PASS**(그레이박스, step 10 · 142프레임 · 충돌 0 · 카메라 최근접 0.4687 m) | evidence/scene_qc.json |
| G5 애니매틱 | NOT_PERFORMED (오프라인 T08) | |
| G6 핵심 4초 | NOT_PERFORMED (T09) | |
| G7/G8/G9 | NOT_PERFORMED | |
| 후합성 파이프 | PASS(2프레임 실측) | review/R02/postcomp_test_318_1140.png — F318 유령 축 점선, F1140 변속기 유령 |
| 그레이박스 렌더 | PASS(8장 270p) | review/R02/stills_270p/contact_graybox.png |

## 3. 재현 기준값 (받는 쪽의 첫 작업 = 이 값 그대로 재현)
| 항목 | 값 |
|---|---|
| bake_qc | ALL PASS, 28/28 |
| v0(주행 속도, 루프 역산) | 1.47916 m/s, 차륜 6회전/1416F, 위상 잔차 0.0 rad |
| ω_run(크랭크 시각 속도, 루프 역산) | 6.02464 rad/s, 39회전, 위상 잔차 <1e-3 rad |
| 기동 가속도 a1 | 0.01818 m/s² |
| 연결기 유격 S1–S4 | 0.08 / 0.0422 / 0.0511 / 0.06 m |
| 사건 F | 정지 187, 체결 318, 크랭크 정지 330, 되감기 370–393, 기동 894, 유격 해소 983/1004/1025/1046 |
| 명사 선행 최소 lead | 변속기 21F (기준 ≥6F) |
| 카메라 | 정지 프레임 0, 좌측(Y>0) 전 프레임, 하드컷 점프 5곳만(187·394·706·965·1078), F1417 == F1(W0) |
| scene_qc | ALL PASS, 충돌 0 / 142프레임(step 10), 카메라 최근접 0.4687 m |
| 빌드 | 602 오브젝트, 마커 16, 뷰레이어 MAIN+GHOST, AOV electric, 패스 Z/Normal/IndexOB/Crypto |
| 270p 8spp CPU 4코어 | 2.7–6.2 s/프레임(그레이박스) |

재현 명령(Windows): `.\RUN_ALL.ps1 -VerifyOnly` → evidence/bake_qc.json·scene_qc.json 이 위와 같아야 한다.

## 4. 시스템 구조
```
rig_config.json ──┐                      materials.json ─┐
camera_keys.json ─┼→ bake.py → del74_bake.npz ──→ build_scene.py → render/del74_scene.blend
                  │     └→ verify_bake.py (G3)        │   └→ import_assets.py(+asset_map.json) → *_assets.blend
                  │     └→ geometry_qc.json.events    └→ verify_scene.py (G4, collision_pairs.json)
                  └→ audio/SFX_CUES.csv                      render_still.py → passes/ passes_exr/
                                                             post_comp.py(npz 채널 + IndexOB/AOV) → comp/ → ffmpeg(bt709)
```
- 베이크 채널(npz): loco_x, loco_v, wheel_theta, gear_theta, pinion_theta, rotor_motor[6], crank_theta, crank_omega, piston[16], rotor_gen, engine_vib, ghost_x, ghost_vis, ghost_theta, skin_ghost, cutter_r[5], iso_drop, electric_u, motor_pulse[6], light_link, car_x[4], car_wheel_theta[4], coupler_slack[4], gearbox, clutch, driveshaft, cam_pos, cam_target, cam_lens, cam_fstop, cam_chain.
- 오브젝트 이름 = 검증·후합성 키: BODY_*(pass 1) ENGINE_BLOCK(2) GEN_CASE(3) CABLE_xx(4) BOGIE_FRAME(5) GHOST_SHAFT(11) GHOST_GEARBOX(12) GHOST_CLUTCH(13) GHOST_DRIVESHAFT(14) MOTOR_01..03(20–22) *_RIM(30–34).
- 좌표: 기관차 로컬 원점 = 차체 중심 직하 레일면, +X 전방, +Y 좌측(카메라), +Z 상. 대차 프로토타입 원점 = 대차 중심. 회전 부품 원점 = 회전축(geo.py가 보장).
- 장치: D1 외피 고스트(M_GHOST skin_ghost + 후합성 엣지) / D2 커터 링(불리언 + RIM IndexOB) / D3 고립(hide_render 키 + GROUND_RIG 하강) / D4 조립(ghost_x·cutter) / D5 청록(전 케이블 u 속성 → AOV + npz electric_u) / D6 유령 점선(GHOST 뷰레이어 IndexOB × npz 강도).

## 5. 통합 절차 (에셋)
assets/README.md → asset_map.json → `RUN_ALL -AssetMap -VerifyOnly`. 프록시는 hide_render로만 숨기고 지우지 않는다(검증·커터가 이름을 참조).

## 6. 알려진 한계 (정직하게)
- 그레이박스다. 외피·캡·대차·전동기·발전기는 치수만 맞는 상자·원통. 레퍼런스급 형상은 WORK_INSTRUCTIONS §1–2.
- 기어 치형은 사다리꼴(어덴덤 0.75m) — 인벌류트 교체 전까지 맞물림 근접샷은 "맞물리는 느낌"까지만.
- 크랭크 주축은 저널 세그먼트 + 웹 상자. 실제 EMD 645 크랭크 형상 아님.
- 외피 고스트는 "카메라 레이 투명 + 그림자 레이 투명 + 나머지 불투명" 트릭이라 내부 간접광이 실제보다 적다. 룩 단계에서 월드 강도로 보정.
- 커터 링은 불리언 EXACT라 프레임당 비용이 있다. 1080p에서 느리면 solver FAST로 바꾸고 절단면 재확인.
- 하늘은 그라디언트 + 노이즈 구름(저주파). 레퍼런스의 실사 구름 질감은 HDRI 없이 재현하지 않았다(3D 내 입자 금지와 무관, 선택 사항).
- 카메라 키는 초안이다. 뷰포트에서 다듬되 `camera_keys.json`으로 되돌려 재베이크(F·anchor·체인 구조 유지).
- BEATS mode 열과 다른 점: C01·C11b·C10a~C11a를 follow로 구현(루프 프레임 일치와 가속 중 프레임 이탈 방지). 경계 F는 그대로.
- 음성 mp3는 저장소에 없다(드라이브). 자막은 공개 직전 별도 레이어.

## 7. 사용자 블로커 (G-*)
- G-ASSET-1 외피 에셋 구매·라이선스. G-FACT-F12/F13 원문 이미지. G-PAINT 실차 사진 2장. G-SFX 효과음 소스. G-REVIEW 핵심 4초·전편 판독.
