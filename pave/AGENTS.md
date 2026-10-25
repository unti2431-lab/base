# PAVE 제작지시서 — Claude work 실행용

너는 PAVE 편의 **제작자**다. 검증자는 따로 있다(생성자 ≠ 검증자). 검증자는 직접 고치지 않고 수정 요청만 낸다. 너는 검증 결과를 이유로 FACT·STYLE을 바꾸지 않는다.

## 0. 읽는 순서 (작업 전 전부)

1. `pave/LOCKS.md` — 이 파일보다 우선한다.
2. `pave/SCENARIO_v1.md` — 비트표, 샷 리스트, 룩.
3. `pave/BEATS.csv` — 컷 경계와 사건 F.
4. `pave/src/rig_config.json`, `pave/src/pave_kin.py` — 운동 정본과 프로토타입 베이크.
5. 스킬 `blender-short-3d-pipeline` §3.1(버전 차이), §5(빌드·베이크 코드), §10(검증), §11(렌더·인코딩).
6. `heavy-mech-series/RANKING_v2.md` §3 — 원안에서 바뀐 이유.

## 1. 반드시

- 모든 Blender 스크립트 첫 줄에 버전 가드(LOCK 밖이면 중단). 버전 상수(EEVEE ID, 하늘 타입)를 쓴다.
- 운동 입력은 `pave_kin.py`가 만든 `src/bake/*` **하나뿐**이다. 손 키프레임을 쓰지 않는다(카메라 제외). 카메라도 BEATS.csv 사건 F에 키를 박는다.
- 애니메이션은 스킬 §5 `bake_fcurves`(채널백 API, 슬롯 명시)로 넣는다. 빌드 직후 프레임 2개에서 카메라·오거 위치와 회전을 출력해 실제로 움직이는지 확인한다.
- 오거 날개는 **절차적 나선**으로 만든다. RMC 리그가 있으면 그것을 가져와 `hand`, `pitch`, 구간 길이만 바꾼다. 날개 메시의 감김 부호를 메시에서 다시 측정해 config의 `hand_*`와 대조한다(§4 V2).
- 회전 위상: 오거 회전각 = `theta_l/theta_r`(npz). 반죽 표면의 물결과 골재 들림이 이 위상에 묶여 있으므로 다른 값을 쓰지 않는다.
- 베벨은 메시에 굽는다(인스턴스에는 모디파이어가 없다). 맞닿는 부품은 1–2 mm 간극을 둔다.
- 이름 규칙 `종류_측면_번호`: `AUGER_R_FWD`, `AUGER_R_REV`, `AUGER_L_FWD`, `AUGER_L_REV`, `GEARBOX_C`, `ENDGATE_L/R`, `SLAT_L_###`, `HEAD_MIX`, `STONES_A_real` 등.
- 라운드마다 `review/R##/`에 contact_270p.jpg, key4s_540p.mp4, qc_summary.json, CHANGELOG.md(바꾼 변수 1개와 이유)를 남긴다.

## 2. 금지

- `pave_kin.py`의 풀이·검증 로직 수정(버그는 보고만 한다).
- 3D 씬 안의 화살표·발광·연기·수증기·파티클 시스템. 골재는 인스턴스 물체로만 표현한다.
- 화면 안 글자, 브랜드·로고·제조사명.
- 시뮬레이션(유체·리지드바디)으로 반죽 흐름 만들기. 결과가 PC마다 달라진다.
- PNG 시퀀스를 드라이브 동기화 폴더에 두기, 드라이브에서 같은 이름 덮어쓰기.
- 실행하지 않은 검사를 PASS나 N/A로 적기. 상태는 PASS / FAIL / NOT_PERFORMED / NOT_DECIDABLE 넷뿐이다.

## 3. 작업 순서 (TASKS.json과 같은 ID)

| ID | 작업 | 산출물 | 통과 조건 |
|---|---|---|---|
| T01 | 환경: LOCK 버전 bpy(클라우드는 PyPI `bpy==4.5.14` 또는 `5.2.2`), numpy | `scripts/setup_env.sh` 작성·실행 로그 | 버전 가드 통과 |
| T02 | 베이크 재현: `python3 src/pave_kin.py` | `src/bake/*`, `bake_qc.json` | `ALL_PASS: true`, AB_fill `fill_90_F` = events ±1 |
| T03 | 에셋: 피니셔 외형 후보 3개 비교(Fab 유료/CC0) → 사용자 선택 대기 | `assets/CANDIDATES.md`, `assets/LICENSES.csv` | 상업 영상 사용 가능 확인. **사용자 승인 전 구매 금지** |
| T04 | 오거 리그: 좌우 정방향(FWD)·역방향(REV) 날개, 축, 기어박스 하우징, 엔드게이트. 변형 B는 REV 자리에 FWD 날개 | `src/build_auger.py` | V1·V2 PASS |
| T05 | 내부: 호퍼, 슬랫 컨베이어 2열(체인 피치 보존, 스킬 §4.1), 스크리드는 형상만 | `src/build_internals.py` | V3 PASS |
| T06 | 반죽 표면: `pave_*_bake.npz`의 h(x,F)를 float EXR(가로 x, 세로 F)로 굽고, GN 그리드가 프레임별로 샘플해 변위 | `src/build_head.py`, `bake/head_*.exr` | 샘플 높이 = npz 값 ±1 mm |
| T07 | 골재: `stones_*.pc2` → 정점 메시 + Mesh Cache 모디파이어 → GN Instance on Points(굵은/잔 골재 컬렉션, `coarse` 속성) | `src/build_stones.py` | 프레임 3개에서 정점 = pc2 값 |
| T08 | 카메라·컷: SCENARIO §3 샷 리스트, 마커 + 카메라 바인딩, Catmull-Rom | `src/build_cameras.py` | 사건 F에 키, 180° 규칙 |
| T09 | 씬 QC: 스킬 §10.2 BVH 충돌, 5F 간격 전수 | `evidence/scene_qc.json` | V4 PASS |
| T10 | 애니매틱 270p 전편(무음) + 컨택트 시트 | `review/R01/animatic_270p.mp4`, `contact_270p.jpg` | V5 PASS |
| T11 | 핵심 4초 540p 24spp: F661–780(B 비움)과 F961–1080(AB 채움), 같은 구도·노출 | `review/R01/key4s_540p.mp4` | 검증자 판독 PASS(G6) |
| T12 | 음성 락 이후: VO_WORDS.json으로 명사 선행 노출 재검사, events ±6F 조정 → 재베이크 | `audio/sync_qc.json` | 위반 0 |
| T13 | 후합성 레이어(흰·파랑·청록·빨강 도형) 렌더 패스 분리, 자막은 basak-shorts-caption | `comp/` | 색 의미 LOCK 준수 |
| T14 | 최종 렌더 패키지: `RUN_ALL.ps1`(청크 렌더·이어하기·VRAM 로그), 납품 인코딩 | `PAVE_R##_HANDOFF/` | 스킬 §11·§14 |

사용자 블로커(`blocked_by_user`): G-PAVE-01 ~ 05. 블로커가 걸린 작업은 가짜 값(config 기본값)으로 진행하되, 산출물에 `PROVISIONAL`을 표시한다.

## 4. 검증 항목 (검증자가 판정, 제작자는 증거만 제출)

| ID | 검사 | 방법 | 기준 |
|---|---|---|---|
| V1 | 오거 회전 | 프레임별 오거 회전각 vs npz `theta_*` | 오차 < 0.1° |
| V2 | **감김 부호** | 날개 외경 정점의 (x, atan2(z, y))를 펴서 dx/dθ 부호 측정 → `hand_*`와 대조. 반송 방향 = `−hand × sign(ω)` | 4구간(R/L × FWD/REV) 전부 일치 |
| V3 | 슬랫 체인 | 피치 오차, 스프로킷 위상(스킬 §4.1) | 피치 오차 < 0.5 mm |
| V4 | 충돌 | 날개–기어박스 하우징, 날개–엔드게이트, 골재–하우징, 골재–날개 외경 원통 | 0건 또는 1 mm 이하 설계 접촉 목록 |
| V5 | 사건·판독 | BEATS 사건 간격 ≤ 90F, 명사 선행 ≥ 6F, 9:16 UI 마스크 겹침 없음, 저비트레이트 2M 재인코딩 판독 | 전부 PASS |
| V6 | 루프 | F1 vs F1200 SSIM 기록, 소리 이음 청취 | 값 기록(목표는 R01 이후 LOCK) |

## 5. 사용자 블로커

| ID | 내용 | 막히는 작업 |
|---|---|---|
| G-PAVE-01 | RMC 나선 리그·반죽 셰이더 파일 위치와 재사용 가능 여부 | T04, T06 (불가 시 제작용이성 하락 → RANKING_v2 §0-4) |
| G-PAVE-02 | 기종 LOCK: 가운데 기어박스 구동 기종 | T04, 대본 C07 |
| G-PAVE-03 | 그 기종의 좌우 감김·회전 방향(매뉴얼·부품도) | 대본 C06 확정, V2 기준값 |
| G-PAVE-04 | fps LOCK(RMC와 맞출지), Blender 버전(RMC LOCK 확인) | T01 이후 전부 |
| G-PAVE-05 | 피니셔 외형 에셋 구매 승인 | T03 이후 외관 컷(C03, C10) |

## 6. 실행 환경

- **클라우드(Claude 작업 공간)**: GPU 없음. Cycles CPU 270p 애니매틱과 540p 대표 스틸까지만. 장시간 렌더는 `setsid nohup`으로 백그라운드에서 돌리고, 이미 있는 PNG는 건너뛴다(이어하기). 프로세스는 PID로 종료한다.
- **사용자 PC**(`C:\Users\lek\Documents\claude blender\PAVE`): 최종 렌더. 원격 셸은 Linux VM이라 Windows Blender를 못 돌린다. 사용자가 `RUN_ALL.ps1`을 실행하거나, 컴퓨터 사용으로 PowerShell에서 실행한다. 어느 쪽인지 착수 시 REPORT.md에 적는다.
- 파일 거점: 드라이브 = 교환·보관(`R##/` 하위 폴더 + MANIFEST.json sha256), 로컬 = 베이크·.blend·PNG.

## 7. 보고 형식 (`REPORT.md`, 작업마다 추가)

```
## T0x <작업명> — <PASS|FAIL|NOT_PERFORMED|NOT_DECIDABLE>
- 변경 파일:
- 실행 명령:
- 게이트 값: (수치 + 파일 경로)
- 산출물:
- 질문 / 블로커:
```

## 8. 완료 정의

T01–T11이 PASS이고 G6(핵심 4초) 검증자 판독 PASS면 **R01 완료**로 보고한다. 음성 락(T12) 이후 T13–T14는 R02에서 진행한다. 최종 1080p 렌더와 공개 승인은 사용자 몫이다.
