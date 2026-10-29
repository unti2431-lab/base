# START_HERE — PC의 Claude에게 이 폴더를 넘길 때

## 1. 사용자가 할 일 (한 번)
1. 이 zip을 **Google Drive 동기화 폴더 밖**에 풉니다. 예: `C:\Users\lek\Documents\claude blender\BSK-HSR-COUPLER`
2. Blender 4.5 LTS, Python 3.11(py launcher), ffmpeg가 설치되어 있어야 합니다. 경로가 기본값과 다르면 `blender_path.txt`에 blender.exe 경로를 적습니다.
3. Claude(Cowork 또는 Claude Code)에서 이 폴더를 연결하고, 아래 지시문을 그대로 붙여 넣습니다.

## 2. Claude에게 붙여 넣을 지시문

```
이 폴더는 BSK-HSR-COUPLER(고속열차 연결기 비교 3D 쇼츠) 제작 패키지 R10이야.
OPUS_BRIEF_R10.md를 먼저 읽고, 거기 적힌 순서대로 AGENTS.md, LOCKS.md, TASKS.json,
review/R09a/REVIEW_R9a_VERIFIER.md, COWORK_START.md §0, audio/VO_SCRIPT_R9.md를 읽어.

너는 제작 세션이야. OPUS_BRIEF_R10.md §2의 순서(L01 → L02 → L03)로 진행해.
- Blender가 필요한 단계는 cowork 폴더의 .cmd를 실행하고(셸에서 Windows Blender를 못 돌리면 컴퓨터 사용으로 더블클릭),
  끝나면 logs\LAST_STATUS.txt로 PASS/FAIL을 확인해.
- FAIL이면 그 자리에서 멈추고 로그의 오류 부분을 요약해서 보고해.
- src/kin_*.py, src/verify_*.py, src/check_baseline.py, src/spring_helix.py의 수식은 수정하지 마.
  RUN_ALL.ps1이 Windows에서 문법 오류를 내면 그 파일만 고치고 REPORT.md에 고친 줄을 적어.
- L03이 끝나면 logs\timing.csv의 초/프레임과 VRAM으로 G3(120F×2)와 전편(1260F) 렌더 예상 시간을 계산해
  REPORT.md에 쓰고 멈춰. 그다음은 내가 녹음 파일을 넣으면 이어서 해.
```

## 3. 이후 사용자가 넣을 것
- `audio\` 에 녹음 10개 WAV + `audio\VO_LOCK.json`(템플릿 복사 후 보이스명 기입) → Claude에게 "L04 진행해"
- `review\` 의 540p MP4 2종을 보고 판독 승인 → L05·L06 종료
- E6 사진 3장, KTX-산천 외관 사진/모델 → L09·L11
