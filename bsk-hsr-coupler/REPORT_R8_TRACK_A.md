# BSK-HSR-COUPLER R8 | 트랙 A 보고 — 기구학 개념 리그 2종 (G2 개념 단계)

> 기준: 2026-10-27 KST | 작업 세션: 클라우드(CPU 4코어, bpy 4.5.14) | 상태: **TEST A·B 개념 리그 베이크·씬 QC 통과, 270p 애니매틱 생성** | 등급: **CONCEPT / T(베이크·씬 검증만)**
> 이 보고의 어떤 수치도 실차 치수가 아니다. 모든 기하는 `src/rig_config.json`에 `source`·`status` 태그로 기록되어 있고, 근거(P/V)가 오면 값만 바꿔 재베이크한다.

## 1. 결론

| 항목 | 상태 | 근거 |
|---|---|---|
| TEST B 샤르펜베르크 계열 150F(+30F) | **베이크 QC ALL_PASS · 씬 충돌 0건** | `evidence/schB_bake_qc.json`, `evidence/schB_scene_qc.json` (4,823 쌍 검사) |
| TEST A 시바타 계열 150F(+50F) | **베이크 QC ALL_PASS · 씬 충돌 0건** | `evidence/shibA_bake_qc.json`, `evidence/shibA_scene_qc.json` (2,451 쌍 검사) |
| 사건 프레임 | 설계 예산과 ±1F 일치 | B: ENGAGE 907 / LOCKED 930 · A: CONTACT 372 / PEAK 440 / LOCKED 500 (월드 F) |
| 270p 무음 애니매틱 | 생성(워터마크 후합성) | `review/schB_animatic_270p_CONCEPT.mp4`, `review/shibA_animatic_270p_CONCEPT.mp4` |
| **G2 정식 통과** | **아니오** | 기하가 CONCEPT라서 정확성 승인은 G0-B·G0-C 이후. 리그 구조·검증 코드·사건 타이밍은 준비됨 |

## 2. 만든 것

```
bsk-hsr-coupler/
  src/rig_config.json            모든 수치 (source S/D/P/V, status LOCK/HOLD/CONCEPT)
  src/kin_schB.py                TEST B 해석 기구학 → evidence/schB_bake.npz, schB_events.json
  src/verify_bake_schB.py        독립 검증(생성 코드 불신): 링크 길이·폐루프·캠 관통·점프·사건·G3 창
  src/build_schB.py              bpy 4.5 씬 빌드(bmesh, 채널백 베이크, 점대칭 인스턴스, 탑뷰 카메라)
  src/verify_scene_schB.py       월드 BVH 충돌 검사(5F 간격 + 체결 ±10F 전수)
  src/kin_shibataA.py / verify_bake_shibataA.py / build_shibataA.py / verify_scene_shibataA.py   TEST A 동일 구조
  src/run_pipeline.sh            bake → verify(게이트) → build → verify_scene(게이트) → [render+encode]
  src/encode_preview.sh          PNG → H.264(bt709 행렬 명시) + 워터마크 + 프레임 카운터 + 컨택트 시트
  src/setup_env.sh               python3.11 venv + bpy==4.5.14 + shapely
  evidence/TEST_B_SCH.blend, TEST_A_SHIB.blend
```

## 3. 기구 모델 (무엇을 어떻게 단순화했나)

### TEST B — 샤르펜베르크 계열
- 훅 원판 = 코어 원 + **캠 로브**(코사인 범프) + 노치 컷. 상대 링크 끝이 로브 옆면을 타고 오르며 원판을 밀어내고(−14.3°), 노치에 떨어지면 스프링이 복원(스냅 3.6°/F 이하).
- 링크 길이는 체결 자세의 폐루프에서 **유도**(0.326 m)해 닫힘 오차 0. 두 헤드 모두 폐루프 쇄가 된다(R8 One Big Idea의 '고리 사슬').
- 후퇴 방향은 96개 조합 격자 탐색에서 전 항목 통과 6개 중 가장 매끄러운 것을 채택. **방향 자체가 CONCEPT**다.
- 3D에서 링크는 원판 위층에 쌓이고, 훅 노즈는 고리 평면 아래에 둬서 고리가 그 위로 미끄러져 들어간다. **캠 접촉은 기구학으로만 표현**되며 메시끼리 닿지 않는다(설계 간극 1.5 mm).

### TEST A — 시바타 계열 (CONCEPT_ONLY)
- 회전정 = D형 몸통 + **노즈 이빨**. 상대 **돌기(너클)**는 머리(r 45 mm)와 밑동 **목 홈**(r 30 mm, 길이 36 mm)이 있는 스타디움 단면.
- 돌기 머리가 들어오며 이빨을 옆으로 밀어 회전정이 10.0° 후퇴(F12→F80), 면이 맞닿기 직전(간극 10.8 mm→0) 머리 어깨가 이빨을 지나면 스프링이 복원해 **이빨이 목 홈에 걸린다**(F134→F140, 마지막 8F에 10° 복귀).
- 회전 각도는 매 프레임 **기하에서 풀린 값**이다(스크립트로 꽂은 자세 없음). 검증기는 "+0.5° 더 돌리면 반드시 막힌다"를 전 프레임 확인한다.
- **실제 시바타의 '회전정 대 회전정 맞물림'과 '잠금실 내벽 쐐기면'은 모델링하지 않았다.** PDF p3 설명과의 차이: 이 모델에서는 **내 회전정이 내 잠금실 안에서 상대 돌기를 문다.**

## 4. 발견한 것 / 상위 문서에 되돌릴 것

| # | 내용 | 영향 | 조치 |
|---|---|---|---|
| F1 | **VO S2 "상대편 잠금실에 쐐기처럼 맞물립니다"**는 PDF의 '회전정이 상대 잠금실 오목부에 진입' 서술을 따른 것인데, 현재 개념 모델은 '상대 돌기를 내 잠금실에서 문다'. 둘 중 무엇이 실차인지 G0-B 없이는 결정 불가 | VO·화면 불일치 가능 | G0-B 도면 확인 전까지 S2를 **"…스프링 힘으로 돌아와 상대편을 쐐기처럼 물어 고정합니다"**처럼 대상을 특정하지 않는 문장으로 녹음 변형 추가 권고 |
| F2 | 270p에서 시바타 회전정이 작아 10° 후퇴가 잘 안 읽힘 | G3 판독 위험 | 다음 라운드 변수 1개: 카메라 거리 2.25→1.6 m(또는 회전정 반경 확대). 한 라운드에 하나만 |
| F3 | TEST B 링크(연한 회색)가 전면판(밝은 강철)과 명도가 비슷 | 판독 | 다음 라운드 변수: 링크를 주황 액센트, 원판을 중간 회색으로 교체(한 색 = 한 의미 원칙 유지) |
| F4 | 두 리그 모두 하우징 윗면을 두지 않았다(아이솔레이션) | R8 §5 "절개보다 아이솔레이션 우선"과 일치 | 유지 |
| F5 | 스프링은 직선 바(길이만 변함). 규범의 '헬릭스·와이어 지름 일정'은 미구현 | 애니매틱 단계 허용 | G5 이전에 Geometry Nodes 헬릭스로 교체 |
| F6 | PDF p1의 시바타 대기각 "약 45°"는 **사용하지 않았다**(원점·방향 불명) | 수치 HOLD 유지 | — |

## 5. 검증 수치 요약

| 검사 | TEST B | TEST A |
|---|---|---|
| 링크 길이 오차 / 폐루프 닫힘 | 1.1e-16 m / 0 | — |
| 캠·돌기 관통(설계 간극 1.5 mm 기준) | 0 | 0 (정확 폴리곤 교차 면적 0) |
| 회전 최대 스텝 | 3.56°/F | <8°/F |
| 후퇴량 / 후퇴 프레임 | 14.3° / 17F | 10.0° / 122F |
| 사건 오차(설계 대비) | ENGAGE +1F, LOCKED 0F | CONTACT 0F, LOCKED 0F, PEAK +15F(허용 ±20) |
| G3 창 [E−60, E+59] | [60,179] ⊂ 1..180 | [80,199] ⊂ 1..200 |
| 씬 BVH 충돌 | 0 / 4,823 | 0 / 2,451 |
| 카메라 최근접 표면 | 1.99 m | 1.99 m |
| 렌더 시간(270p 6spp CPU) | ≈1.4 s/F | ≈1.4 s/F |

## 6. 다음 단계 (트랙 A)

1. **540p 핵심 120F 렌더**(G3 창)로 판독 검수 — 먼저 F2·F3 라운드 변수 1개씩 반영.
2. 스프링 헬릭스(Geometry Nodes) 교체.
3. 샷06·10 본편 카메라 경로를 테스트 카메라에서 분리(현재는 테스트 전용 궤도).
4. W0 루프 블로킹(E5 에셋·E6 (a) 노즈는 사용자 자료 대기 → 프록시 박스로 선행).
5. G0-B·G0-C 자료 도착 시: `rig_config.json` 값 교체 → `src/run_pipeline.sh <python> all --render` 재실행.

## 7. 재현

```bash
src/setup_env.sh ~/bpyenv                       # 1회
src/run_pipeline.sh ~/bpyenv/bin/python all --render
```
증거 파일 해시는 인계 패키지 단계(§14 규범)에서 `MANIFEST.json`으로 묶는다. 이 세션의 렌더 PNG는 저장소에 넣지 않았다(`.gitignore: render/`).
