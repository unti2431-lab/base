# OPUS_BRIEF_R10 — 로컬 제작 세션(Claude Opus) 지시서

> 기준: 2026-10-29 | 패키지: BSK-HSR-COUPLER R10 | 역할: **당신은 제작(생성) 세션**이다. 검증은 클라우드 세션이 따로 한다. 당신은 판정하지 않고, 산출물과 로그를 남긴다.
> 이 문서는 "무엇이 끝났고, 무엇이 당신 몫이며, 어디서 멈춰야 하는지"만 말한다. 규칙 본문은 `AGENTS.md`·`LOCKS.md`, 할 일은 `TASKS.json`.

## 0. 읽는 순서 (5분)
1. 이 파일 → 2. `AGENTS.md` → 3. `LOCKS.md` → 4. `TASKS.json` → 5. `review/R09a/REVIEW_R9a_VERIFIER.md`(검증 세션의 요청 R1–R6) → 6. `COWORK_START.md` §0(실행 구조) → 7. `audio/VO_SCRIPT_R9.md`

## 1. 현재 상태 (클라우드에서 끝난 것 — 다시 하지 않는다)

| 항목 | 상태 | 증거 |
|---|---|---|
| TEST A·B 개념 리그 | 베이크 QC·씬 QC 통과, CPU 베이스라인 재현 PASS | `evidence/*_qc.json`, `src/check_baseline.py` |
| W0 루프 블로킹 (L08) | ALL_PASS, 프록시 | `evidence/w0_loop_qc.json`, `review/W0_loop_seam_270p_CONCEPT.mp4` |
| R9-1 TEST A 카메라 1.6 m (L05) | 씬 QC PASS, 540p G3 MP4 생성 | `review/R09_1/`, `review/shibA_key4s_R91_F80-199.mp4` |
| R9-2 TEST B 재질 (L06) | 씬 QC PASS, 540p G3 MP4 생성 | `review/R09_2/`, `review/schB_key4s_R92_F60-179.mp4` |
| L07 헬릭스 스프링 | 와이어 반지름 3프레임 일정, 씬 QC PASS | `src/spring_helix.py`, `review/R10_L07/` |
| L10 근거 대조 | 9건 열람, **C03은 P 기준으로 사용 승인**(조건부) | `evidence/L10_EVIDENCE_R9a.md`, `LOCKS.md` FACT |
| RUN_ALL.ps1 R9a | 하드닝 7건 | **Windows에서 아직 한 번도 실행 안 됨** |

## 2. 당신의 작업 순서 (FAIL이면 그 자리에서 멈추고 REPORT)

| 순서 | TASK | 실행 | 멈춤 조건 |
|---|---|---|---|
| 1 | L01 | `cowork\01_SETUP.cmd` | `logs\LAST_STATUS.txt`가 FAIL. **RUN_ALL.ps1 문법 오류면 그 파일만 고치고** 고친 줄을 REPORT에 |
| 2 | L02 | `cowork\02_BASELINE.cmd` | BASELINE FAIL → 다른 작업 시작 금지 |
| 3 | L03 | `cowork\03_GPU_TIMING.cmd` | OPTIX/CUDA 미검출, TDR, `logs\timing.csv` 미생성 |
| 4 | **보고 1회** | `logs\timing.csv`의 s/F·VRAM으로 G3(120F×2)·전편(1260F) 예상 시간을 계산해 REPORT에 쓰고 **멈춘다** | — |
| 5 | L04 | 사용자가 녹음 10개 + `audio\VO_LOCK.json`을 넣으면 `04_VO_SYNC` → `05_VO_APPLY` → `06_VERIFY` | `vo_sync_report.json` 위반 ≠ 0 |
| 6 | 540p 재렌더 | `07_RENDER_KEY_A`, `08_RENDER_KEY_B` (VO 반영 후 사건 F가 옮겨졌으므로 **GPU로 다시 렌더**) | 실패 청크, `decode ok` 없음 |
| 7 | L12 | 브라우저에서 L10 원문 9건을 PDF 인쇄 → `evidence\L10\E1_…pdf`~`E9` | — |
| 8 | L09 → L11 | 사용자 사진이 오면 E6 노즈, KTX 외관 30F | 사진·라이선스 없으면 시작 금지 |

## 3. 이번 라운드에서 확정된 결정 (바꾸지 않는다)
- **C03(KTX-산천 연결기): P 등급으로 사용 승인.** 따라서 VO는 `S3a_K`("한국 케이티엑스 산천에도 쓰이는 샤르펜베르크 계열은…")를 쓰고, 샷08 앞 30F에 KTX 중련 외관(L11)을 넣는다. 금지는 그대로: "type 10", "초기 10편성", 1,500/1,000 kN, 호대 번호.
- **VO 기본 선택:** `S2b_B`(반달 제거판) + `S3a_K`. 녹음은 대본대로 **10개 전부** 받는다.
- **S3b 배치 예산** `place_F` 780 → 800 (S3a_K가 길어서). 실측 후 `vo_words.py`가 다시 계산한다.
- **스프링:** 헬릭스(절대 셰이프 키). 바 스프링으로 되돌리지 않는다.
- **카메라:** TEST A 거리 1.6 m, TEST B 2.25 m, 앙각 72° LOCK.

## 4. 반드시 / 금지 (AGENTS.md 요약 + 이번 라운드 추가)
- 수정 금지: `src/kin_*.py`, `src/verify_*.py`, `src/check_baseline.py`, **`src/spring_helix.py`의 헬릭스 수식**. 버그는 REPORT에 재현 절차로 올린다.
- 검증기를 직접 고치지 않는다(R9a에서 한 번 있었음 — 다음부터는 검증 세션에 요청).
- 한 라운드 변수 하나. `review/R##/CHANGELOG.md` 필수.
- 렌더 PNG는 git에 넣지 않는다. `review/*.mp4`, `evidence/*.json`, `MANIFEST.json`은 넣는다.
- 작업이 끝나면 **커밋·푸시**(브랜치 `ccr-5f0706ff-ncondm`) 또는 zip으로 사용자에게 전달. 검증 세션은 그것만 본다.

## 5. 보고 양식 (REPORT.md에 블록 추가)
```
## <날짜> <TASK> <한 줄>
- 변경 파일 / 실행 명령 / 게이트 값(PASS·FAIL·NOT_PERFORMED + 수치) / 산출물(sha256 12자리) / 렌더(프리셋, s/F, VRAM, 재시도) / 질문
```

## 6. 알려진 함정 (먼저 읽으면 시간을 아낀다)
- 한국어 Windows: Python 기본 인코딩이 cp949. RUN_ALL이 `PYTHONUTF8=1`을 켠다. 직접 python을 돌릴 때도 `set PYTHONUTF8=1`.
- PowerShell 5.1 `Out-File -Encoding utf8`은 BOM을 붙인다 → JSON을 직접 쓸 땐 `[IO.File]::WriteAllText`.
- `blender.exe -b -P script.py -- args`: `--` 뒤가 스크립트 인자. 빌드 스크립트가 이미 처리한다.
- GPU 첫 프레임은 커널 로드로 느리다. s/F는 두 번째 프레임으로 잰다(RUN_ALL timing이 그렇게 한다).
- 8 GB VRAM: 540p·1080p 리그 씬은 여유. W0 씬(700 m 환경)도 프록시라 여유. 피크는 `logs\timing.csv`.
- Google Drive 동기화 폴더 밖에서 작업한다.

## 7. 사용자에게 받아야 하는 것 (당신이 요청)
1. 녹음 10개 WAV + 보이스명 (`audio\VO_LOCK.json`)
2. E6 정면·측면·사선 사진 3장 + 라이선스 페이지 (L09)
3. KTX-산천 중련 외관 사진 또는 라이선스 모델 (L11)
4. 540p MP4 2종(`review/`)을 정상속도로 본 **판독 승인**(L05·L06 accept는 사용자 시청이 조건)
