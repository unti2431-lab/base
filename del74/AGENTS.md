# AGENTS.md — DEL74 오프라인 작업 규칙 (Codex / Sol / dot / 사용자 공통)

## 읽는 순서
1. `DEL74_LOCKS.md` (R02) — 바꿀 수 없는 것.
2. `WORK_INSTRUCTIONS_R02.md` — 무엇을 어떤 순서로, 어떤 명령으로, 통과 조건은 무엇인지.
3. `HANDOFF_R02.md` — 현재 상태, 재현 기준값, 시스템 구조.
4. `REVISION_PLAN_R02.md` — 왜 이렇게 설계했는지(컷별 의도). 수정 판단이 필요할 때만.
5. `TASKS.json` — 작업 id·의존·수락 기준. 완료하면 `REPORT.md` 양식으로 기록.

## 반드시
- 모든 수치는 `src/rig_config.json` 에서만. 코드·.blend에 수치를 직접 박지 않는다. 치수 바꾸면 `bake → verify_bake → build` 재실행.
- 운동 입력은 `src/del74_bake.npz` 하나. .blend에서 키프레임을 손으로 옮기지 않는다(다음 빌드에서 사라진다).
- 카메라는 `src/camera_keys.json`을 고친다. 뷰포트에서 찾은 값을 JSON에 옮기고 재베이크한다.
- 게이트 순서: G3 verify_bake PASS → G4 verify_scene PASS → G5 270p 애니매틱 → G6 핵심 4초 540p → G7 전편 540p → G8 1080p. 통과 못 한 게이트 위에 다음 단계를 쌓지 않는다.
- 한 라운드에 변수 하나. `review/R##/CHANGELOG.md`에 바꾼 변수 1개와 이유.
- 생성자 ≠ 검증자. 검증자는 고치지 않고 수정 요청만 낸다.
- Blender **4.5 LTS만**. 5.x로 열어 저장하지 않는다(액션 슬롯·하늘 노드가 바뀐다).

## 금지
- 컷 경계(F) 변경, 음성 재녹음 없는 길이 변경.
- 3D 씬 안 발광·입자·연기·주황/황록 색. 청록은 후합성 전기 전용.
- 문자·로고·차번. 점화 순서·기어비·마력·중량 수치 언급.
- `bpy.ops` 로 씬 구성(저장·임포트만 허용). 셰이더 베벨 노드(CPU 비용) — 베벨은 메시에 굽는다.
- PNG 시퀀스를 드라이브 동기화 폴더에 두기.
- 테스트를 끄거나 임계를 올려 PASS 만들기. FAIL은 FAIL로 보고.

## 실행 명령 (Windows, 작업 폴더 `C:\Users\lek\Documents\claude blender\DEL74`)
```
py -3.11 -m venv venv && venv\Scripts\pip install numpy pillow OpenEXR
.\RUN_ALL.ps1 -VerifyOnly              # G3·G4
.\RUN_ALL.ps1 -Stills "1,150,318,426,505,745,894,1100"
.\RUN_ALL.ps1 -Key4s                   # G6 산출물 review\R02\key4s_540p.mp4
.\RUN_ALL.ps1 -AssetMap -VerifyOnly    # 에셋 통합 후 G4
.\RUN_ALL.ps1 -Final -Chunk 12 -Spp 256
```
리눅스/클라우드(CPU)는 `scripts/setup_env.sh` → `scripts/run_pipeline.sh`.

## 완료 정의
- 해당 TASKS.json 항목의 `accept` 전부 충족 + `REPORT.md` 기록 + 산출물이 `MANIFEST.json`(sha256)에 포함.
- 질문은 REPORT의 "질문" 란에. 추측으로 LOCK을 바꾸지 않는다.
