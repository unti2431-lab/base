# PAVE R01 — 여기서 시작

「도로 까는 기계엔 거꾸로 감긴 날개가 있습니다」 Blender 3D 공학 쇼츠(40초, 9:16) 제작 패키지입니다.
이 폴더 하나로 Claude work가 착수할 수 있게 묶었습니다.

## 1. Claude work에 붙여 넣을 첫 지시

```
이 폴더(PAVE_R01_HANDOFF)는 PAVE 편 제작 패키지다. 너는 제작자다.
1) START_HERE.md → AGENTS.md → LOCKS.md → SCENARIO_v1.md → BEATS.csv 순서로 읽어라.
2) 아래 '2. 첫 실행'을 그대로 돌리고 evidence/pipeline_status.txt 와 evidence/bake_qc.json 결과를 REPORT.md 에 T01·T02 로 기록해라.
3) 착수 보고로 (a) 실행 경로(클라우드 / 내 PC PowerShell) (b) 사용자 블로커 G-PAVE-01~05 중 지금 나에게 물어야 할 것을 한 번에 질문해라.
4) 블로커 답을 받기 전에는 T04 이후를 PROVISIONAL 로만 진행하고, 에셋 구매는 하지 마라.
```

## 2. 첫 실행 (T01·T02)

Linux / macOS / 클라우드:
```bash
bash scripts/setup_env.sh --bake-only        # numpy 만. Blender 버전 결정(G-PAVE-04) 전에도 가능
bash scripts/run_pipeline.sh --bake-only     # 베이크 + 게이트 → evidence/
# 버전이 정해지면:
bash scripts/setup_env.sh --blender 4.5      # 또는 5.2 (사용자 결정)
bash scripts/run_pipeline.sh --check-bpy
```

Windows PowerShell(사용자 PC, Python 3.11+ 와 numpy 필요):
```powershell
python -m pip install numpy
powershell -ExecutionPolicy Bypass -File .\scripts\RUN_PIPELINE.ps1 -BakeOnly
```

통과 기준: `evidence/pipeline_status.txt` 에 `G3 bake: PASS`, `evidence/bake_qc.json` 의 `ALL_PASS: true`.
기준값은 `evidence/EXPECTED_bake_qc.json` 과 같아야 합니다(수치 비교. sha256 은 OS·numpy 버전에 따라 달라질 수 있어 참고용).

## 3. 폴더 구성

| 경로 | 내용 |
|---|---|
| `AGENTS.md` | 제작지시서: 반드시/금지, 작업 T01–T14, 검증 V1–V6, 블로커, 보고 형식 |
| `LOCKS.md` | FACT · SPEC · STYLE · RIG(수정 권한). 최우선 문서 |
| `SCENARIO_v1.md` | 기획 요약, 비트표 + 내레이션 예시, 샷 리스트, 룩 |
| `BEATS.csv` | 컷 경계·사건 F·명사 노출 F(검사 스크립트가 읽음) |
| `TASKS.json` | 작업 의존성·통과 조건·사용자 블로커 |
| `REPORT.md` | 작업 기록 양식(제작자가 채움) |
| `src/rig_config.json` | 리그 수치 정본(수치만 수정 가능) |
| `src/pave_kin.py` | 오거 반송 기구학 베이크 + 독립 검증(수정 금지) |
| `src/common_bpy.py` | 버전 가드, 채널백 베이크, BVH, 베이크 로더 |
| `src/build_TEMPLATE.py` | build_* 스크립트 시작 템플릿 |
| `src/spec_lock.json` | Blender 버전·fps LOCK 기록(setup_env.sh 가 씀) |
| `scripts/` | setup_env.sh, run_pipeline.sh, RUN_PIPELINE.ps1 |
| `evidence/EXPECTED_bake_qc.json` | 작성 환경에서 낸 베이크 게이트 기준값 |
| `reference/` | RANKING_v2(선정 근거), PIPELINE_EXCERPT(스킬이 없을 때 규범 요약) |
| `assets/` | 에셋 후보·라이선스 장부 양식 |
| `audio/` | 음성 락 자리(ChatGPT 대본 → ElevenLabs) |
| `review/R01/` | 라운드 리뷰 패킷 자리 |
| `MANIFEST.json` | 파일별 바이트·sha256 |

## 4. 지금 결정이 필요한 것(사용자)

1. **G-PAVE-01** RMC 나선 리그·반죽 셰이더 파일 위치 → `assets/` 에 넣거나 경로를 알려 주기
2. **G-PAVE-02** 기종: 가운데 기어박스 구동 피니셔
3. **G-PAVE-03** 그 기종의 좌우 날개 감김·회전 방향(매뉴얼·부품도)
4. **G-PAVE-04** Blender 4.5 / 5.2, fps(RMC 편과 맞출지)
5. **G-PAVE-05** 피니셔 외형 에셋 구매 승인
