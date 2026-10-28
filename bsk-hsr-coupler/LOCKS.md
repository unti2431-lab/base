# LOCKS.md — R9a (2026-10-29, FACT 등급은 evidence/L10_EVIDENCE_R9a.md 원문 대조 결과)

## SPEC (LOCK)
| 항목 | 값 |
|---|---|
| 길이 / fps / 프레임 | 42.0s / 30 / 1260F, Blender `frame_start=1`, 양끝 포함, `t=(F−1)/30` |
| 해상도 | 최종 1080×1920 · 검수 540×960 · 애니매틱 270×480 |
| Blender | **4.5 LTS** (스크립트가 버전 가드로 강제) |
| 렌더 | Cycles, 로컬 RTX 3060 Ti 8GB, OptiX(없으면 CUDA), 적응 샘플링, 최종 시작값 256spp, AgX Medium High Contrast |
| 인코딩 | H.264 CFR, `out_color_matrix=bt709`, bt709 태그, 자막본·무자막본 |
| 음량 | −14 LUFS integrated, −1 dBTP, SFX ↔ 사건 F ±1F |
| 자막 | basak-shorts-caption R08, 후합성만 |
| VO | `audio/VO_SCRIPT_R9.md`, TTS 1.1배속, 문장 1파일 |

## FACT (근거 등급)
| ID | 내용 | 등급 | 화면·VO 사용 |
|---|---|---|---|
| JP-01 | 시바타 계열: 수직 피벗 회전정, 복원 스프링, 쐐기 접촉 | **P(부분)** — 신칸센용 밀착연결기 = 廻り子式, 錠이 연결면 사이 체결 유지(일본제철 E8). 반달 형상·스프링·쐐기면은 D | 원리로만. '반달 모양'은 D → **VO S2b_B** |
| JP-02 | 대기각 약 45°, 후퇴 10–15° | D (HOLD) | **금지** |
| SCH-01 | 콘·펀넬, 훅 원판·고리·스프링, 폐루프 | **P** — US2161724(K. Scharfenberg) 회전 훅 원판+고리+스프링, 피벗 평행사변형 / US8800792B2(Dellner) 보강 | 원리로만(차량명 없이) |
| C03 | KTX-산천(KTX II) 연결기 = Voith Scharfenberg One4 | **P(부분)** — Voith 보도자료 "KTX II … drive with One4 couplers", 전두부 Voith. 'type 10'·초기 10편성은 S/D | **V 전까지 금지** → `VO_R9_S3a_K` 미사용 (P 허용으로 완화할지는 사용자 결정) |
| N1 | 2026 KTX-산천–SRT 중련 시범운행(4/30–5/14), 5/15 승객 운행 | **P** (아시아경제 원문 E7) | 설명란·한국 축 근거(연결기 형식 주장 금지) |
| ABS | 완충·확관 | OUT | 본편 제외 |

## RIG (수정 금지 파일)
- `src/kin_schB.py`, `src/kin_shibataA.py`, `src/verify_bake_*.py`, `src/verify_scene_*.py`, `src/check_baseline.py`
- 수정 허용: `src/rig_config.json`(값·태그), `src/build_*.py`(재질·조명·카메라·메시 형상, 단 씬 QC 재통과 필수), `RUN_ALL.ps1`

## STYLE
- 일본 계열 = 청록, 샤르펜베르크 계열 = 주황 (한 색 = 한 의미)
- 기구 샷은 탑뷰·고앙각 ≥60°, 회전 부호 = 로컬 +Z에서 내려다본 반시계 +
- 07·11 홀드는 저속 푸시인 + 중간 미세 사건, 완전 정지 금지
- 하중 펄스·워터마크·자막은 후합성 레이어
- 샷10 카메라 호 ≤30°, 체결 ±15F 각속도≈0

## 재현 기준값 (클라우드 R8, CPU)
| 항목 | 값 |
|---|---|
| TEST B 사건 local F | ENGAGE 97, LOCKED 120 (world 907 / 930) |
| TEST B 링크 길이 | 0.325852562953138 m |
| TEST A 사건 local F | CONTACT 12, PEAK 80, LOCKED 140 (world 372 / 440 / 500) |
| TEST A 후퇴각 | 10.035° |
| 씬 QC 쌍 검사 | B 4,823 / A 2,451, 충돌 0 |
`RUN_ALL.ps1 -Step baseline`이 이 값을 자동 비교한다.
