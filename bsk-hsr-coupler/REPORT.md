# REPORT — 로컬 작업 기록 양식

복사해서 작업마다 한 블록씩 위에 추가한다.

```
## <날짜> <TASK id> <한 줄 요약>
- 변경 파일:
- 실행 명령:
- 게이트 값: (PASS/FAIL/NOT_PERFORMED + 핵심 수치)
- 산출물: (경로, sha256 앞 12자리)
- 렌더 기록: (프리셋, s/frame, peak VRAM, 재시도)
- 질문 / 블로커:
```

## 2026-10-29 L10 근거 원문 대조 (클라우드, 부분 완료)
- 변경 파일: `evidence/L10_EVIDENCE_R9a.md`(신규), `LOCKS.md`(FACT 표), `audio/VO_LOCK.TEMPLATE.json`(selection S2b → S2b_B)
- 실행 명령: 원문 페이지 직접 열람 9건 (특허 3, Voith 2, KSR2018F107, 아시아경제, 일본제철, All About)
- 게이트 값: SCH-01 D→**P** · JP-01 D→**P(부분)** · C03 S→**P(부분, type 10은 S/D)** · N1 S→**P** · press74 접근 실패(C03 '10편성·type ten'은 S 유지)
- 산출물: `evidence/L10_EVIDENCE_R9a.md`
- 질문 / 블로커: ① C03 사용 기준을 V→P로 완화할지(완화 시 S3a_K·샷08 KTX 컷 사용 가능, 단 "type 10" 표기는 계속 금지) ② PDF 원본 파일 저장은 로컬 브라우저 인쇄로 대체 필요 ③ BLOCKER_PLAN의 특허 2건 설명 오류 정정(US8800792B2=Dellner, US2214036A=Van Dorn 타이트락, 샤르펜베르크 근거 아님)

## 2026-10-29 L08 W0 루프 블로킹 (클라우드 CPU, bpy 4.5.14)
- 변경 파일: `src/build_w0.py`, `src/verify_w0.py`, `src/encode_w0_seam.sh`(신규), `src/rig_config.json`에 `w0_loop` 블록 추가(전 항목 CONCEPT)
- 실행 명령: `python src/build_w0.py` → `python src/verify_w0.py` → `python src/build_w0.py -- --render 1 1260 --preset animatic` → `src/encode_w0_seam.sh`
- 게이트 값: `w0_loop_qc.json` ALL_PASS — F1↔F1261 위치 0 m / 회전 0° / FOV 동일 / 속도차 8.6e-5 m/F(기준 5e-4) / 각속도차 4.4e-5 °/F / 환경·바퀴 위상 0 / 조명 동일 / F50 연결부 꺾임 6.8e-5 m/F / 카메라 최근접 0.33 m (E5 헤드, F1186)
- 설계: 열차 정지 + 환경 스크롤 60 km/h(1260F × 0.556 m = 700 m = 50 m 타일 × 14 → 이음매 위상 자동 일치). 카메라는 F1–50 선형 팔로우 → F50–120 5차 에르미트 Z축 진입(F50에서 위치·속도·가속도 일치) → F1186–1261 5차 에르미트 복귀(끝점 = F1 위치·속도, 가속도 0)
- 산출물: `evidence/W0_BLOCK.blend`, `evidence/w0_loop_qc.json`, `evidence/w0_build_meta.json`, `review/W0_loop_seam_270p_CONCEPT.mp4`(+ `_stress2M`, `_contact.jpg`) — sha256은 MANIFEST.json
- 렌더 기록: animatic(270×480, Cycles CPU 6spp) 2코어 약 2–4 s/F, 195F
- 질문 / 블로커: E5·E6는 프록시(노즈 로프트·포켓·커버 반쪽 2장). L09(E6 노즈 실모델)는 사진+라이선스 페이지 대기. 검증기 1차 실행에서 회전 지표가 float32 acos 조건수 문제로 0.034° 오탐 → atan2(스큐, 트레이스) 방식으로 수정 후 재판정(생성 코드는 무변경)

## 2026-10-29 L01–L03 준비 / RUN_ALL.ps1 R9a (클라우드 사전 점검)
- 변경 파일: `RUN_ALL.ps1`, `cowork/03_GPU_TIMING.cmd`, `src/build_schB.py`·`src/build_shibataA.py`(config UTF-8 읽기 1줄)
- 실행 명령: `bash tools/vm_check.sh` → **VM_CHECK: PASS**, 클라우드 전체 베이스라인(bake→verify→build→scene QC→check_baseline, bpy 4.5.14 CPU) → **BASELINE PASS** (B 4,823쌍·A 2,451쌍 충돌 0, 사건 F·링크 길이·후퇴각 기준값 일치)
- RUN_ALL.ps1 R9a 수정 내역 (PowerShell 파서 실행 검증은 이 환경에서 불가 — 첫 로컬 실행이 실검증):
  1. **`$env:PYTHONUTF8=1`** — 한국어 Windows 기본 cp949로 `rig_config.json`(§, 回転錠 등)을 열면 `UnicodeDecodeError` (클라우드에서 재현 확인). kin_*/verify_*는 수정 금지라 실행기에서 해결
  2. 네이티브 실행을 `Invoke-Native`로 통일 — PS 5.1에서 `2>&1` + `ErrorActionPreference=Stop`이면 stderr 한 줄(경고)에도 즉시 FAIL하던 문제 제거, 판정은 종료 코드로만. 모든 출력이 트랜스크립트 로그에 남고 Blender 전체 로그는 `logs\blender_*.log`
  3. render: 실패 청크·누락 PNG가 있어도 **PASS로 기록되던 결함** → FAIL로 기록. MP4에 월드 F 카운터 후합성
  4. vo: 동기 위반이 경고만 내고 PASS → **FAIL**로 기록 (단계표의 통과 조건과 일치)
  5. timing: Blender 종료 후의 유휴 VRAM을 읽던 것 → 렌더 중 250 ms 샘플링 **실제 피크**. 첫 프레임(커널 로드) 제외하고 두 번째 프레임만 s/F로 기록, `logs\timing.csv` 누적
  6. `MANIFEST.json`·`LAST_STATUS.txt`를 BOM 없는 UTF-8로 기록 (PS 5.1 `Out-File -Encoding utf8`은 BOM → Python `json.load` 실패)
  7. setup: ffmpeg/ffprobe/nvidia-smi 누락 시 경고만 → FAIL (L01 accept와 일치)
- 게이트 값: L01·L02·L03 **NOT_PERFORMED (로컬)** — `D:\claude blender` 폴더 연결 대기


## 2026-10-29 R10 (클라우드 검증 세션이 제작 역할로 전환해 진행) L05·L06·L07·C03 결정
- 변경 파일: `src/rig_config.json`(test_A 카메라 distance 1.6), `src/build_schB.py`(재질 2줄, 스프링 블록), `src/build_shibataA.py`(스프링 블록), `src/spring_helix.py`(신규), `audio/VO_LOCK.TEMPLATE.json`(selection S3a_K, S3b place_F 800), `LOCKS.md`(C03 R10 규칙), `TASKS.json`(R10 상태, L11·L12 신설), `CCL_R10_DELTA.md`, `OPUS_BRIEF_R10.md`
- 실행 명령: build→verify_scene (A·B), 540p 24spp CPU 렌더 G3 창(A F80–199, B F60–179), encode_preview
- 게이트 값: 씬 QC A·B ALL_PASS(충돌 0, A 카메라 최근접 1.34 m) / 스프링 와이어 반지름 0.00600 m 일정(3프레임×2리그) / 길이 추종 오차 <0.5 mm
- 렌더 기록: key4s(540×960, 24spp, CPU 4코어) A 17–28 s/F, B 23–25 s/F
- 산출물: `review/shibA_key4s_R91_F80-199.mp4`, `review/schB_key4s_R92_F60-179.mp4`(+stress2M, contact), `review/R09_1|R09_2|R10_L07/CHANGELOG.md`
- 질문 / 블로커: L05·L06 accept의 "정상속도 판독"은 사용자 시청이 조건. 스프링 앵커 끝에 브래킷이 없음(개념 단계, G5 전 보강 후보). 이 라운드는 검증 세션이 제작을 겸했으므로 **다음 검증은 다른 세션(로컬 Opus 또는 신규 클라우드)**이 맡는다.
