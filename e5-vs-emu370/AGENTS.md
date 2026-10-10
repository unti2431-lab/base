# AGENTS.md — Codex 작업 규칙 (E5 vs EMU-370, R1)

## 읽는 순서
0. `CODEX_R7_ALIGNMENT.md` — 현재 단계(C1.5) 지시서. R6 runtime 위에서 작업한다
1. `LOCKS.md` — 바꾸면 안 되는 사실·규격
2. `PRODUCTION_PLAN_R1.md` — 콘티, 컷별 제작법, 게이트
3. `HANDOFF_E5_EMU370.md` — 시스템 구조, 코드 표준, 함정
4. `src/config/*.json` — beats / rig_config / shots / look
5. `TASKS.json` — 작업 순서와 완료 조건

## 반드시
- 씬 구성은 bpy 스크립트(bmesh + bpy.data)로 한다. bpy.ops는 에셋 임포트·저장에만 쓰고 주석으로 표시한다.
- 4.4+ 슬롯 액션 규칙을 따른다(HANDOFF §4.1). 빌드 직후 F1·F450에서 카메라·열차 위치를 출력해 원점에 멈춰 있지 않은지 확인한다.
- 모든 수치는 `src/config/*.json`에서 읽는다. 코드에 숫자를 하드코딩하지 않는다(단위 변환 상수 제외).
- 게이트 스크립트는 `{"PASS": {...}, "ALL": bool}` JSON을 `evidence/`에 쓰고, 실패하면 exit 1로 끝낸다. 파이프라인은 실패 시 중단한다.
- 상태는 PASS / FAIL / NOT_PERFORMED / NOT_DECIDABLE 중 하나로 쓴다. 실행하지 않은 검사를 N/A나 PASS로 쓰지 않는다.
- `src/*.py`는 `env/bin/python script.py args`와 `blender -b --python script.py -- args` 두 방식 모두로 실행되게 한다(`sys.argv`에서 `--` 뒤만 파싱).
- 작업마다 `REPORT.md`에 기록한다.

## 금지
- `LOCKS.md` FACT 표에서 '표기 금지' 또는 '사용 금지'인 문구·수치를 화면·텍스트·파일명에 넣는 것.
- 볼류메트릭, 휠–레일 불꽃, Wireframe 노드 오버레이, 20mm 이하 광각 비교 샷 (look.json `banned`).
- 실제 브랜드 로고(JR East, KORAIL, 현대로템 CI) 데칼. 채널 로고만 허용한다.
- 슬로모션으로 열차 속도를 바꾸는 것.
- 같은 결함을 국소 수정 2회 넘게 반복하는 것. 2회 뒤에도 남으면 수정을 멈추고 REPORT에 재설계 제안을 쓴다.
- 한 라운드에 변수 두 개 이상을 바꾸는 것.

## 실행 명령
```bash
bash scripts/setup_env.sh                 # bpy==4.5.x 설치 (Blender 미설치 환경)
python3 tools/check_beats.py --json evidence/beats_check.json
bash scripts/run_pipeline.sh --preview     # bake → verify_bake → build → verify_scene → 270p 스틸
```
Windows 최종: `powershell -File RUN_ALL.ps1` (`-VerifyOnly`, `-Rebake`, `-AssetMap assets/asset_map.json`)

## 완료 정의
- TASKS.json에서 `blocked_by_user`가 아닌 작업의 `accept`가 모두 충족된다.
- G01–G05 증거 JSON이 `evidence/`에 있고 ALL=true다.
- 깨끗한 폴더에 복사해 `run_pipeline.sh --preview`를 다시 돌렸을 때 증거 수치와 bake npz md5가 일치한다.
- 최종 1080p 렌더와 공개 승인은 사용자 몫이다. Codex는 하지 않는다.
