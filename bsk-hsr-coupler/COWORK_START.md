# COWORK_START — Claude Cowork로 바로 제작 진행하기

> 패키지: BSK-HSR-COUPLER R9 | 2026-10-28 | 이 폴더 하나에 리그·검증·렌더·VO 동기 도구가 모두 들어 있다.

## 0. 실행 구조 (먼저 알아 둘 것)

Cowork의 셸은 **PC 안의 Linux VM**이다. 이 폴더를 읽고 쓸 수 있고 Python도 돌지만, **Windows의 blender.exe와 GPU는 직접 실행하지 못한다.** 그래서 역할을 이렇게 나눈다.

| 일 | 어디서 | 방법 |
|---|---|---|
| 파일 읽기·수정, 보고서 작성 | Cowork VM | 직접 |
| 베이크 수치 자체 점검 | Cowork VM | `bash tools/vm_check.sh` |
| Blender 빌드·씬 충돌 검사·GPU 렌더·인코딩 | Windows | `cowork\0N_*.cmd` 더블클릭 — Cowork가 **컴퓨터 사용**으로 실행하거나, 사용자가 직접 실행 |
| 결과 확인 | Cowork VM | `logs\LAST_STATUS.txt`, `logs\RUN_*.log`, `evidence\*.json`, `review\*.mp4` 읽기 |

모든 `.cmd`는 끝나면 `logs\LAST_STATUS.txt`에 `PASS` 또는 `FAIL`을 남긴다. Cowork는 이 한 줄로 다음 단계 진행 여부를 판단한다.

## 1. 사용자 준비 (1회, 약 15분)

1. **Blender 4.5 LTS** 설치. 다른 버전이면 스크립트가 멈춘다.
2. **Python 3.11** 설치(설치 시 "py launcher" 체크). 명령 프롬프트에서 `py -3.11 --version`이 나오면 된다.
3. **ffmpeg**를 PATH에 추가(`ffmpeg -version`이 나오면 된다).
4. 이 zip을 **Google Drive 동기화 폴더 밖**에 푼다. 예: `C:\Users\lek\Documents\claude blender\BSK-HSR-COUPLER`
5. 폴더 안 `blender_path.txt`에 blender.exe 전체 경로를 한 줄로 적는다(기본값이 이미 들어 있다. 설치 경로가 같으면 그대로 둔다).
6. Cowork에서 이 폴더를 작업 폴더로 연결하고, 컴퓨터 사용을 허용한다.

## 2. Cowork 첫 지시 (복사해서 붙여 넣기)

```
이 폴더는 BSK-HSR-COUPLER 3D 공학 쇼츠 제작 패키지야. COWORK_START.md, AGENTS.md, LOCKS.md, TASKS.json,
REPORT_R8_TRACK_A.md 순서로 읽고 시작해.

실행 규칙:
- 네 셸(VM)에서는 Windows Blender를 못 돌리니까, Blender가 필요한 단계는 컴퓨터 사용으로
  cowork 폴더의 .cmd 파일을 더블클릭해서 실행하고, 창이 "계속하려면 아무 키나…"에서 멈추면
  logs\LAST_STATUS.txt를 읽어 PASS/FAIL을 확인해.
- 단계 순서: tools/vm_check.sh(VM) → 01_SETUP → 02_BASELINE → 03_GPU_TIMING.
  하나라도 FAIL이면 다음으로 넘어가지 말고 로그의 오류 부분을 요약해서 나한테 보고해.
- src/kin_*.py, src/verify_*.py, src/check_baseline.py는 절대 수정하지 마.
  RUN_ALL.ps1이 Windows에서 문법 오류를 내면 그 파일만 고치고, 고친 내용을 REPORT.md에 적어.
- 각 단계가 끝나면 REPORT.md 양식으로 기록해.
- 03까지 끝나면 렌더 시간 실측값(초/프레임, VRAM)으로 G3 렌더와 최종 렌더 예상 시간을 계산해서 보고하고 멈춰.
```

## 3. 단계표

| 순서 | 실행 | 하는 일 | 통과 조건 | 사용자 입력 |
|---|---|---|---|---|
| 0 | `bash tools/vm_check.sh` (VM) | 두 리그 재베이크 + 독립 검증 | `VM_CHECK: PASS` | — |
| 1 | `cowork\01_SETUP.cmd` | Blender 4.5 확인, `.venv` 생성(numpy·shapely·faster-whisper·soundfile) | `PASS setup` | — |
| 2 | `cowork\02_BASELINE.cmd` | 베이크→검증→빌드→씬 충돌 검사, 클라우드 기준값 비교 | `BASELINE PASS` | — |
| 3 | `cowork\03_GPU_TIMING.cmd` | 체결 프레임 1장 GPU 렌더(540p 128spp), 시간·VRAM | 장치 OPTIX 또는 CUDA 표시, 크래시 없음 | — |
| 4 | `cowork\04_VO_SYNC.cmd` | 녹음 해시·길이, 단어 타임스탬프, 사건 F 재계산 | `vo_sync_report.json` 위반 0 | **녹음 10개 파일 + `audio\VO_LOCK.json` 보이스명** |
| 5 | `cowork\05_VO_APPLY.cmd` → `06_VERIFY.cmd` | 사건 F를 config에 반영 → 재베이크·재검증 | `PASS verify` | — |
| 6 | `cowork\07_RENDER_KEY_A.cmd`, `08_RENDER_KEY_B.cmd` | G3 창 120F를 540p GPU 렌더, 인코딩, 2M 스트레스본 | 실패 청크 0, `decode ok` | — |
| 7 | 판독 | `review\*.mp4`를 정상속도로 보고 G3 판정 | 후퇴·복원·체결이 읽힘 | **사용자 시청 승인** |

그 다음은 `TASKS.json`의 L05–L10(라운드 변수, 스프링 헬릭스, W0 루프, E6 노즈, 근거 원문)을 순서대로 진행한다.

## 4. 멈춤 규칙
- FAIL이 나면 그 단계에서 멈추고 보고한다. 같은 결함이 국소 수정 2회 뒤에도 남으면 재설계 보고.
- 한 라운드에 변수 하나만 바꾼다(`review\R##\CHANGELOG.md`).
- CONCEPT·HOLD 수치를 화면·VO·설명란에 실측값처럼 쓰지 않는다.
- 최종 1080p 렌더와 공개는 사용자 승인 후에만.

## 5. 녹음 파일 넣는 법
`audio\VO_SCRIPT_R9.md`의 10개 문장을 파일명 그대로 `audio\`에 넣는다. `audio\VO_LOCK.TEMPLATE.json`을 `VO_LOCK.json`으로 복사해 `voice_name`, `engine`, `model`을 채운다. 그다음 4번 단계를 실행한다.

## 6. 검증 담당
제작은 Cowork가 한다. 검증은 다른 세션(클라우드 Claude Code 세션 등)이 `evidence\*.json`, `review\*.mp4`, `MANIFEST.json`을 읽고 판정만 한다. 같은 세션이 만들고 승인하지 않는다.
