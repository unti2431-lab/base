# HANDOFF R9 — 클라우드 → 로컬 PC (Claude Code + Blender 4.5 + RTX 3060 Ti)

## 1. 한 문장 목표
클라우드에서 만든 두 개념 리그(TEST A·B)를 로컬 GPU에서 그대로 재현하고, 녹음된 VO에 사건 프레임을 맞춘 뒤 540p 핵심 120F 판독(G3)까지 진행한다.

## 2. 현재 상태
| 항목 | 상태 |
|---|---|
| TEST B 샤르펜베르크 개념 리그 | 베이크·씬 QC 통과, 270p 애니매틱 |
| TEST A 시바타 개념 리그 | 베이크·씬 QC 통과, 270p 애니매틱 (CONCEPT_ONLY) |
| VO | 대본 R9 완료(`audio/VO_SCRIPT_R9.md`), 녹음 대기 |
| 근거 | C03·SCH-01·JP-01 모두 S/D 등급. 원문 확보 대기(TASK L10) |
| W0·E6 | 미착수 (L08·L09) |

## 3. 로컬 준비 (사용자, 1회)
1. Blender **4.5 LTS** 설치(다른 버전이면 스크립트가 중단한다).
2. Python **3.11** 설치(`py -3.11` 동작 확인), ffmpeg를 PATH에.
3. 저장소 받기:
   ```powershell
   git clone https://github.com/unti2431-lab/base.git
   cd base; git checkout ccr-5f0706ff-ncondm; cd bsk-hsr-coupler
   ```
   작업 폴더는 Google Drive 동기화 폴더 **밖**에 둔다(PNG 수천 장).
4. 이 폴더에서 Claude Code를 열고 아래 첫 지시를 붙여 넣는다.

## 4. 로컬 Claude Code 첫 지시 (복사용)
```
bsk-hsr-coupler 폴더의 AGENTS.md를 읽고 그 순서대로 LOCKS.md, TASKS.json, REPORT_R8_TRACK_A.md를 읽어.
TASKS.json의 L01 → L02 → L03을 순서대로 실행해. 모든 실행은 RUN_ALL.ps1로 하고,
Blender 경로는 "<여기에 blender.exe 경로>"야. 각 TASK가 끝날 때마다 REPORT.md 양식으로 기록하고,
accept 조건이 하나라도 거짓이면 다음 TASK로 넘어가지 말고 멈춰서 보고해.
kin_*.py와 verify_*.py는 수정하지 마.
```

## 5. 시스템 구조
```
rig_config.json ──► kin_*.py (numpy/shapely, .venv) ──► evidence/*_bake.npz, *_events.json
                                                        │
                    verify_bake_*.py (독립 재계산) ◄────┘  ── FAIL이면 중단
                                                        │
                    build_*.py (blender.exe -b -P … --) ──► evidence/TEST_*.blend
                                                        │
                    verify_scene_*.py (BVH 충돌) ◄──────┘  ── FAIL이면 중단
                                                        │
                    build_*.py --render … --gpu (24F 청크·이어하기·재시도 2회) ──► render/…/####.png
                                                        │
                    ffmpeg (bt709 행렬, 워터마크 후합성, 2M 스트레스본) ──► review/*.mp4
audio/*.wav ──► vo_words.py (sha256, faster-whisper 단어 F) ──► rig_config events_target (−Apply) ──► 위 파이프라인 재실행
```

## 6. 알려진 한계
- 두 리그의 기하는 CONCEPT. 시바타의 '회전정 대 회전정 맞물림'과 '잠금실 쐐기면'은 모델링되지 않았다.
- 스프링은 직선 바(L07에서 헬릭스로 교체).
- 클라우드에서는 GPU 경로(`--gpu`)를 실행해 보지 못했다. **L03이 첫 실측**이다. OptiX 장치를 못 찾으면 CUDA로 넘어가고, 둘 다 없으면 중단한다.
- `RUN_ALL.ps1`은 이 클라우드 환경에 PowerShell이 없어 **문법 실행 검증을 못 했다.** 첫 실행에서 오류가 나면 로컬 Claude가 고치되, 고친 내용을 REPORT에 남긴다.
- 클라우드 세션의 네트워크 허용 변경이 아직 반영되지 않았다(railway-technology.com·patents.google.com·voith.com 여전히 403). 새 세션에서 반영되는지 확인하거나, L10을 로컬에서 진행한다.

## 7. 검증 담당
제작은 로컬 Claude Code가 한다. 검증은 이 클라우드 세션(또는 별도 세션)이 맡는다. 로컬에서 커밋·푸시하면, 검증 세션이 `evidence/*.json`, `review/*.mp4`, `MANIFEST.json`을 읽고 판정만 한다(직접 수정하지 않음).
