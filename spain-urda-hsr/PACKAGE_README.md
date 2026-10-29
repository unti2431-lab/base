# 스페인 우르다 고속열차 추돌 숏폼 — 통합 패키지 (2026-10-29)

이 zip 하나에 기획·검증·프롬프트·Codex 지시서가 모두 들어 있다. 읽는 순서대로 나열한다.

## 0. 읽는 순서

| 순서 | 파일 | 누가 | 무엇 |
|---|---|---|---|
| 1 | `PRODUCTION_PLAN_R3.md` | 사용자 | 검증 결과, 버전 A/B 비교, 공개 기준, 블로커 |
| 2 | `prompts/LOCKS.md` | 모두 | 사실 상태표(FACT), 규격(SPEC), 형상·스타일 고정 문구. **고치는 곳은 여기뿐** |
| 3 | `handoff/V6_OMNI/DIRECTIVE_V6.md` | 사용자·Codex | **최신 정본: Omni 단독 · 텍스트 없는 15샷 지시서** (V4 음성 LOCK) |
| 3-0 | `handoff/V5_42S/SCENES_V5.md` + `CUTS_V5.csv` | 참고 | V4 분석·사실 점검·샷 경계(V6이 이 경계를 씀) |
| 3-1 | `handoff/R4_REEDIT/AGENTS.md` | Codex | 작업 규칙·렌더러·QC 공통 지시서(60초 판 기준으로 작성, 규칙은 V5에도 적용) |
| 4 | `handoff/R4_REEDIT/VO_PATCH_R4.txt` | 사용자 | ElevenLabs로 만들 패치 3문장 |
| 5 | `prompts/FLOW_A_R2.md` + `prompts/out/*.txt` | 사용자 | 새 키프레임(imagegen)·Flow 영상이 필요할 때의 장면 구성과 완성 프롬프트 |
| 6 | `BEATS.csv`, `vo/VO_SCRIPT_R3.txt` | 참고 | 45초 R3 설계. **현재 녹음은 60초 R2 대본**이므로 R4 작업은 AGENTS.md가 우선 |
| 7 | `evidence/braking_calc.py/.json` | 참고 | 화면 수치의 유일한 근거 |
| 8 | `blender/rig_config.json` | 버전 B | Blender 리그 수치 초안 |
| 9 | `MANIFEST.json` | 검증 | 파일별 sha256 |

우선순위 충돌 시: 사용자의 최신 지시 > `AGENTS.md`(R4) > `LOCKS.md` > `PRODUCTION_PLAN_R3.md` > 나머지.

## 1. 이번 패키지에서 다시 검증한 것

| 항목 | 방법 | 결과 |
|---|---|---|
| 제동 수치 | `braking_calc.py` 재실행, assert | PASS — 200 km/h 1,654~2,040 m → "1.5 km 넘게"(60초 음성의 "1 km 넘게"도 참), 40 km/h 84~99 m → "100 m 안" |
| 25 km / 17분 정합 | 계산 | 평균 83~88 km/h, 정지 출발과 들어맞음 |
| 프롬프트 25개 | `build_prompts.py` | LOCK 태그 미해결 0, 한글 0, 2분할 유발 표현(upper/lower …) 0 |
| 18컷 설계 | CUTS_R4.csv ↔ AGENTS §7 대조 | C01~C18 모두 일치 |
| 작업 의존성 | TASKS.json | 참조 ID 누락 0 |
| 45초 비트표 | BEATS.csv | F1~F1080 연속, 빈틈·겹침 0 |
| 길이 예산 | 60.3 − S12·S13(≈8 s) + P1·P2·P3(≈10 s) + 꼬리 3 s | ≈ 65 s, 18컷 × 3~4 s(54~72 s) 안 |

확인하지 못한 것(패키지 안에 그대로 표시): 한국 「철도차량운전규칙」 조문(G-1), 스페인 규정 원문(marcha a la vista 40 km/h는 교통부 설명 보도), 충돌 속도(기록장치 분석 전), 사망자 최종 수.

## 2. 최고 품질을 내는 선택 (권장 순서)

이 패키지의 기본 경로는 "새 생성 0건 + 결정론적 2.5D"다. 그 위에서 품질을 더 올리는 선택지를 비용 순으로 적는다. 각각은 독립이라 하나씩 적용할 수 있다.

| # | 선택 | 효과 | 비용 | 적용 시점 |
|---|---|---|---|---|
| Q1 | **음성 패치 3문장**(P1·P2·P3) | 사실 오류·채널 규칙 위반 제거, 사고 핵심(40 km/h) 추가. 품질보다 **공개 가능 여부**를 가른다 | ElevenLabs 3회 | 지금 |
| Q2 | 2.5D를 **2160×3840으로 렌더 후 1080×1920 다운샘플** | 선·숫자 가장자리가 깨끗해져 저비트레이트에서도 읽힘 | 렌더 시간 4배(Python 렌더러라 수 분 단위) | T05 |
| Q3 | Flow 클립 구간을 **Flow 1080p 업스케일**로 다시 받기 | 현재 720p 원본 확대보다 질감이 좋음 | 크레딧 0(이미 생성된 클립의 다운로드 옵션) — 옵션이 없으면 생략 | T01 직후 |
| Q4 | 질감 통일 패스(§6.6)를 **Flow 구간엔 샤프닝 없이 그레인만** | 확대된 Flow 클립의 아티팩트 강조 방지 | 없음 | T06 |
| Q5 | C06~C08(선로 단면·신호기) 3컷만 **Blender(bpy 4.5.14) 지오메트리**로 교체 | 침목·레일·도체·신호기 형상이 사진급. 나머지 2.5D와 색·카메라 규칙은 동일 | 1~2일, 버전 B 자산을 미리 만드는 효과 | R4 PASS 후 R5 |
| Q6 | K01·K02·K06·K10 네 컷만 **Veo 3.1(일반)로 재생성** | Fast보다 움직임 지시 준수율이 높고 K11 감속 정지도 재시도 가능 | 컷당 크레딧, 사용자 승인 필요(AGENTS §2-2) | R5 |
| Q7 | 버전 B 전면 이행(`PRODUCTION_PLAN_R3.md` §5) | 비례·위치 보장, 후속편 자산 재사용 | 8~9일 + GPU 렌더 | CIAF 발표 시점 후속편 |

권장: **Q1 → Q2 → Q4는 이번 R4에 모두 적용**, Q3는 옵션이 있을 때만, Q5·Q6은 R4가 QC를 통과한 뒤 별도 라운드로.

## 3. 사용자가 지금 할 일

1. `handoff/R4_REEDIT/VO_PATCH_R4.txt`로 P1·P2·P3 음성 생성 → 작업 루트 `input/VO_PATCH_R4/`
2. `handoff/R4_REEDIT/` 4개 파일을 작업 루트에 복사하고 Codex에게 `AGENTS.md`부터 읽게 함 (1과 동시 진행 가능)
3. 한국 규정 조문 확인(G-1) — 공개 전까지
4. 공개 전 `FACT_GATE_R4.md` 서명

## 4. 폴더 구조

```
spain-urda-hsr/
  PACKAGE_README.md            ← 이 파일
  PRODUCTION_PLAN_R3.md
  BEATS.csv
  MANIFEST.json
  vo/VO_SCRIPT_R3.txt
  evidence/braking_calc.py  braking_calc.json
  prompts/LOCKS.md  FLOW_A_R2.md  FLOW_A_R1.md(기록)  build_prompts.py  out/*.txt(25)
  blender/rig_config.json
  handoff/R4_REEDIT/AGENTS.md  SCENES_R4b.md  CUTS_R4.csv  TASKS.json  VO_PATCH_R4.txt
  handoff/V5_42S/SCENES_V5.md  CUTS_V5.csv
```
