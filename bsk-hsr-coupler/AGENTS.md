# AGENTS.md — BSK-HSR-COUPLER 로컬 작업 규칙 (Claude Code on Windows / Codex 공통)

## 읽는 순서
1. 이 파일
2. `LOCKS.md` — 고정값, 근거 등급, 금지 사항
3. `TASKS.json` — 할 일, 선행 관계, 완료 조건
4. `REPORT_R8_TRACK_A.md` — 현재 리그 모델과 알려진 한계
5. `CCL_R8.md` §4(샷 LOCK)·§5(리그 LOCK), `audio/VO_SCRIPT_R9.md`

## 반드시
- 모든 실행은 `RUN_ALL.ps1`로 한다. 첫 작업은 **`-Step setup` → `-Step baseline -Test all`** (클라우드 결과 재현). BASELINE FAIL이면 다른 작업을 시작하지 않는다.
- 수치를 바꿀 때는 `src/rig_config.json`의 `value`만 바꾸고, 같은 항목의 `source`(S/D/P/V)와 `status`를 함께 갱신한다.
- 수치를 바꾼 뒤에는 `-Step verify`가 통과해야 렌더한다. 게이트 FAIL 위에 다음 단계를 쌓지 않는다.
- **한 라운드에 변수 하나.** `review/R##/CHANGELOG.md`에 바꾼 변수 1개와 이유를 적는다.
- 같은 결함이 국소 수정 2회 뒤에도 남으면 수정을 멈추고 재설계 보고를 쓴다.
- 렌더 시간은 추정하지 말고 `-Step timing`으로 대표 프레임 1장을 측정해 환산한다.
- 결과 보고는 `REPORT.md` 양식(작업ID / 변경 파일 / 명령 / 게이트 값 / 산출물 / 질문).

## 금지
- `src/kin_*.py`, `src/verify_*.py`의 풀이·판정 로직 수정 (버그를 찾으면 수정하지 말고 REPORT에 재현 절차와 함께 올린다).
- CONCEPT·HOLD 수치를 화면 글자·VO·설명란에 실측값처럼 쓰기.
- 3D 씬 안에 발광 화살표·입자·글자 넣기 (하중 펄스·워터마크는 후합성만).
- 거울 복제(음수 스케일)로 헤드 B 만들기 — 헤드 B는 Z축 180° 회전 인스턴스.
- 기각된 에셋(E6·KTX 3D Warehouse 후보)을 최종 렌더에 쓰기.
- PNG 시퀀스를 Google Drive 동기화 폴더에 두기.
- 검증 담당이 직접 고치기 (검증 담당은 수정 요청만 낸다).

## 역할
- 제작(생성): 로컬 Claude Code (이 PC).
- 검증: 별도 세션(클라우드 세션 또는 다른 로컬 세션). 검증 세션은 `evidence/*.json`, `review/` 영상, `MANIFEST.json`을 읽고 판정만 한다.

## 완료 정의
- 각 TASK의 `accept` 조건이 모두 참이고, 산출물이 `MANIFEST.json`에 sha256으로 기록되어 있으며, git에 커밋·푸시됨(렌더 PNG 제외).
