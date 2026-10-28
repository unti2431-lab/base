# R09a CHANGELOG (2026-10-29, 클라우드 세션)

이 라운드는 **렌더 룩·리그 변수를 바꾸지 않았다.** 바꾼 것은 실행기 안정화와 신규 블로킹(W0)·근거 대조뿐이라, R9-1(L05)·R9-2(L06)의 "한 라운드 변수 하나" 원칙과 충돌하지 않는다.

| 범주 | 파일 | 바꾼 것 | 이유 |
|---|---|---|---|
| 실행기 | `RUN_ALL.ps1` | R9a 하드닝(아래 REPORT 참조) | 한국어 Windows cp949에서 L02가 첫 단계부터 FAIL하는 결함 등 |
| 실행기 | `cowork/03_GPU_TIMING.cmd` | `final` 프리셋 측정 추가 | L03 accept "both presets measured" |
| 빌드 | `src/build_schB.py`, `src/build_shibataA.py` | `rig_config.json`을 `encoding="utf-8"`로 읽기 (1줄씩) | 위와 같은 인코딩 위험. 형상·재질·카메라 무변경 → 씬 QC 수치 동일 |
| 신규 | `src/build_w0.py`, `src/verify_w0.py`, `src/encode_w0_seam.sh`, `rig_config.json["w0_loop"]` | L08 W0 루프 블로킹 | TASKS L08 |
| 근거 | `evidence/L10_EVIDENCE_R9a.md`, `LOCKS.md` FACT 표 | SCH-01 P, JP-01 P(부분), C03 P(부분), N1 P | TASKS L10 (원문 문장이 말하는 범위만 승격) |
| VO | `audio/VO_LOCK.TEMPLATE.json` | 기본 선택 `S2b_A` → `S2b_B` | '반달 모양'은 여전히 D. 대본 R9의 사용 조건("G0-B에서 반달형 확인 시")을 따른 것 |
