# 스페인 우르다 고속열차 추돌 — 제작계획 R3 (검증 + 2버전)

> 가제 **「고속열차는 앞차를 보고 멈추지 않습니다」**
> 45초 · 9:16 · 1080×1920 · 24fps · 한국 45~75세 남성 · 바삭숏
> 작성 2026-10-29 · 대상 사건 2026-10-28 08:54경, 톨레도 우르다 인근 마드리드–세비야 고속선

함께 보는 파일

| 파일 | 내용 |
|---|---|
| `prompts/LOCKS.md` | FACT · SPEC · 형상 · 스타일 LOCK(정본) |
| `prompts/FLOW_A_R1.md` | 버전 A Flow 프롬프트(CLEAN · INFO · MP4) |
| `BEATS.csv` | 두 버전이 함께 쓰는 비트표(프레임 단위) |
| `vo/VO_SCRIPT_R3.txt` | 음성 합성에 바로 붙여 넣을 대본 |
| `evidence/braking_calc.py` / `.json` | 영상에 나오는 모든 거리 수치의 계산 근거 |
| `blender/rig_config.json` | 버전 B 리그 수치 초안 |

---

## 0. 결론

| | **버전 A — Flow 단독, 빠른 제작** | **버전 B — 품질 개선 (Blender + Flow 브리지)** |
|---|---|---|
| 경로 | A (Flow 단독, INFO 패스 포함) | C 실사 브리지형 |
| 소재 | Flow 클립 11개 (CLEAN 9 · INFO 5) | Blender 마스터 씬 2개에서 8컷 + Flow 3컷 |
| 기간 | 3일 (10/29~10/31) | 8~9일 (11/1~11/8) |
| 강점 | 시의성. 애도 기간이 끝난 직후 공개 가능 | 정지거리 비례(1.65 km 대 84 m)와 25 km 간격을 **좌표로 보장**. 공식 수치가 바뀌면 config만 고쳐 다시 렌더 |
| 약점 | 띠 길이·마커 위치를 AI가 대략 그림. 매 라운드 검수에 의존 | GPU 렌더 시간(대표 프레임 실측 필요), 에셋 구입 |
| 공개 | 10/31 | CIAF 1차 발표나 기록장치 속도가 공개될 때 맞춰 **후속편**으로 |

**추천**: A를 먼저 공개하고, A의 클립을 B의 애니매틱 기준으로 다시 씁니다. 대본·비트표·자막 타이밍이 두 버전에 공통이라 B에서는 화면만 바꾸면 됩니다.

---

## 1. 핵심작업 검증 결과

### 1.1 사실관계 (상세는 `prompts/LOCKS.md` FACT)

| 항목 | 확인 결과 | 상태 |
|---|---|---|
| 사고 개요 | AVE 2080이 정차 중인 Iryo 6076을 뒤에서 추돌. 08:54경 | CONFIRMED |
| 사망자 | 68명(카스티야라만차 주지사), 늘어날 수 있음. 3일 애도 기간 | CONFIRMED, 변동 중 → 내레이션은 "수십 명" |
| 08:36 지시 | 관제가 AVE에 "LZB를 껐다 켜고 **marcha normal(정상 운행)**로 재개하라"고 지시. 교신 녹음이 공개됨 | REPORTED (복수 매체) |
| 규정 속도 | LZB 없이 달릴 때는 **marcha a la vista(시계운전), 최고 40 km/h** (교통부 설명). 장관은 해당 지시를 "설명할 수 없다"고 함 | REPORTED (규정 원문은 미확인) |
| 25 km · 17분 | 08:36 재개 지시부터 충돌까지 약 17분 동안 25 km 주행 | REPORTED |
| 충돌 속도 | 137.27 km/h(직전 1분 평균, Renfe Data 인용 보도) / 장관 "최대 200 km/h였을 수 있음" | **UNVERIFIED → 쓰지 않음** |
| 대체 보호 | LZB가 꺼져도 ASFA가 신호기 지점에서 감시. ASFA 계열 상한은 200 km/h | 참고 → 설명란에만 |
| 한국 비교 | 한국 철도의 장치 장애 시 시계운전·저속운전 조항 | **UNVERIFIED → 블로커 G-1** |

※ 이번 세션에서는 elespanol.com, eldiario.es, law.go.kr 원문에 접속하지 못했습니다(네트워크 차단). 위 내용은 여러 매체 검색 결과를 서로 맞춰본 것이며, 원문은 공개 전 G9 단계에서 다시 확인합니다.

### 1.2 R2에서 바로잡는 것

| # | R2 내용 | 검증 결과 | R3 조치 |
|---|---|---|---|
| 1 | "25 km와 17분이 앞뒤가 안 맞는다" | **틀렸습니다.** 25 km ÷ 17분 = 평균 88 km/h로, 정지 상태에서 출발한 것과 들어맞습니다 | 지적을 철회하고 N9에 그대로 사용 |
| 2 | 핵심을 "3겹 보호(LZB·ASFA·사람)"로 잡음 | 개념이 두 개(제동거리 + 보호층)라 One Big Idea 규칙 위반. 공개된 쟁점은 "시계운전 40 km/h 대신 정상 운행 지시"로 좁혀짐 | **One Big Idea = "멈출 수 있는 거리 안에서만 달린다"**. ASFA는 설명란으로 |
| 3 | "비상제동에도 1 km 넘게" | 계산값은 1.65~2.04 km(200 km/h, a = 1.0~0.8, 반응 2초) | "**1.5 km 넘게**" — 두 가정 모두에서 참인 경계값 |
| 4 | 마지막 문장 "결국 마지막 안전장치는 사람입니다" | 채널 금지 종결("결국")에 걸리고, 책임 소재를 미리 단정함 | "보이지 않으면, 속도를 낮춥니다."로 교체 |
| 5 | S01을 열차 없는 정적인 부감으로 시작 | 첫 프레임 규칙 위반(F1부터 움직임, 2.5초 안에 실루엣이 읽혀야 함) | K01은 주행 중인 열차 후방 추적 |
| 6 | 55초 | 파이프라인 범위(15~45초) 초과 | 45초 / 1080F |
| 7 | 30fps | Flow 출력은 24fps라 변환 시 끊김(저더) 발생 | A·B 모두 24fps로 LOCK |

### 1.3 제동 계산 (`evidence/braking_calc.json`)

가정: 감속도 일정 1.0 m/s²(보수 하한 0.8), 반응·체결 2초, 편성 길이 200 m. TGV(300 km/h에서 약 3.5 km)와 CRH(2.8~3.3 km) 보고치를 감속도로 환산하면 0.99~1.25 m/s²라 1.0과 들어맞습니다.

| 속도 | 정지거리 (a = 1.0) | 정지거리 (a = 0.8) | 편성 길이로 환산 | 화면 표기 |
|---|---|---|---|---|
| 40 km/h | 84 m | 99 m | 0.4~0.5편성 | **100 m 안** |
| 200 km/h | 1,654 m | 2,040 m | 8~10편성 | **1.5 km 넘게** |
| 25 km를 40 km/h로 가면 | 37.5분 | | | 쓰지 않음(추정 서사) |

스크립트에 `assert`를 넣어 두었습니다. 화면에 쓰는 값이 두 가정 중 하나라도 벗어나면 실행이 실패합니다.

### 1.4 착수 게이트 G0 점검

| 항목 | 판정 |
|---|---|
| 대상 정체 | "고속열차 추돌"(alcance = 뒤에서 들이받음) — 맞음 |
| 전제 사실 | "고속열차는 앞차를 보고 멈추지 않는다" — 물리 계산으로 성립. 40 km/h 규정은 REPORTED |
| 채널 3축 | 위협(25 km 뒤 추돌) ✅ · 일상 접점(KTX 이용) ✅ · 한국 인프라(N11) ⚠️ G-1 확인 전까지 조건부 |
| One Big Idea | "멈출 수 있는 거리 안에서만 달린다" — 1개 ✅ |
| 제외 목록 중복 | NOT_DECIDABLE (정본을 받지 못함) → 사용자 확인 |
| 대본 정합 | 습니다체 ✅ · 질문형·"결국" 종결 없음 ✅ · 출처 없는 수치 없음 ✅ (모든 수치는 FACT ID 또는 계산 근거와 연결) |

---

## 2. 공통 대본 R3 (`vo/VO_SCRIPT_R3.txt`)

```
N1  스페인 고속열차 추돌사고로 수십 명이 숨졌습니다.
N2  고속열차는 앞차를 보고 멈추지 않습니다.
N3  시속 200이면, 비상제동에도 1.5킬로미터 넘게 갑니다.
N4  선로 속 케이블이, 갈 수 있는 거리를 계속 알려줍니다.
N5  사고 당일 아침, 이 신호가 끊겼습니다.
N6  규정상 이럴 땐, 눈으로 보고 설 수 있는 속도, 시속 40 이하입니다.
N7  이 속도면 100미터 안에 섭니다.
N8  그런데 공개된 교신에서, 관제는 정상 속도 운행을 지시했습니다.
N9  17분, 25킬로미터. 그 앞엔 멈춰 선 열차가 있었습니다.
N10 왜 그런 지시가 나갔는지, 조사 중입니다.
N11 우리 고속철도도 같습니다. 보이지 않으면, 속도를 낮춥니다.
```

- 길이 추정: 226음절. 쉼표·문장 끝마다 0.35초를 더하면(약 7.7초) 초당 6.0음절에서 **약 45.4초**입니다(6.5음절이면 42.5초, 5.5음절이면 48.8초). 실측 후 G2에서 LOCK합니다.
- 46초를 넘으면 줄일 순서: N4 "계속" 삭제 → N10을 "조사가 진행 중입니다"로 → N6 "규정상" 삭제(화면 표기로 옮김). 세 가지를 모두 하면 약 2초가 줄어듭니다.
- **N11 대체안** (G-1 확인 실패 시): "우리 KTX도 장치가 속도를 감시합니다. 보이지 않으면, 속도를 낮춥니다." 한국 축을 유지하면서 확인되지 않은 절차는 말하지 않는 문장입니다.
- 편집에서 넣을 작은 표기(한글은 자막 레이어에서만): K03 `가정: 감속 1.0 m/s² · 반응 2초` / K05 · K09 `보도 기준 · 조사 중` / K08 `교신 내용은 보도 인용`

---

## 3. 공통 비트표 (`BEATS.csv` 요약, 24fps)

| 컷 | 프레임 | 초 | 새 정보 1개 | 내레이션 |
|---|---|---|---|---|
| K01 | 1–96 | 0.0–4.0 | 주행 중인 고속열차 (W0) | N1 |
| K02 | 97–168 | 4.0–7.0 | 운전석 전방, 앞이 비어 있음 | N2 |
| K03 | 169–276 | 7.0–11.5 | 정지거리 띠 1.5 km+ | N3 |
| K04 | 277–372 | 11.5–15.5 | LZB 케이블 + 정보 펄스 | N4 |
| K05 | 373–444 | 15.5–18.5 | 펄스가 먼 쪽부터 꺼짐 | N5 |
| K06 | 445–564 | 18.5–23.5 | 저속 전방 + 40 km/h | N6 |
| K07 | 565–636 | 23.5–26.5 | **K03과 같은 구도에** 100 m 띠 | N7 |
| K08 | 637–744 | 26.5–31.0 | 관제실(뒷모습) | N8 |
| K09 | 745–864 | 31.0–36.0 | 같은 선로 위 25 km 간격 | N9 |
| K10 | 865–936 | 36.0–39.0 | 정차 열차 + 적색 신호(충돌 없음) | N10 |
| K11 | 937–1080 | 39.0–45.0 | W0 복귀, 적색 신호 전 감속·정지 | N11 |

- 5초 이상인 컷(K06, K09, K11)은 컷 안에 사건이 하나씩 있습니다(속도 안정 / 마커 이동 / 감속 시작). 사건 간격 3초 이하 규칙을 지킵니다.
- 이 영상의 논지를 담는 짝은 **K03 ↔ K07**(같은 판 위에서 1.5 km 띠와 100 m 띠)입니다. 두 버전 모두 가장 먼저 검수합니다.

---

## 4. 버전 A — Google Flow 단독, 빠른 제작

### 4.1 경로 판정
- 경로 A(Flow 단독). 수치 그래픽은 Flow의 INFO 패스로 넣고(숫자와 단위만, 장면당 1개), 한글은 자막 레이어에만 둡니다.
- C로 올리지 않는 이유: 시의성이 우선이고, 비례 오차는 검수 기준("한눈에 길이 차이가 보이는가")으로 관리할 수 있습니다.

### 4.2 파이프라인

```
T0 기능 확인 → VO 합성·실측(G2) → CLEAN R1 → 검수 → INFO R1 → 검수 → MP4 R1 → 검수
  → 재생성 R2~R3 → capcut-dual-look 룩 → 연결 편집 → basak-shorts-caption(R08)
  → 믹스(-14 LUFS) → G9 공개 게이트
```

| 단계 | 담당 | 도구 / 스킬 | 통과 조건 |
|---|---|---|---|
| T0 | 사용자 | Flow | 9:16 Frames to Video 가능 여부와 클립 길이 옵션 확인 (`FLOW_A_R1.md` T0) |
| VO | 사용자 | ElevenLabs | 파일 sha256·길이 기록, 40~46초 |
| 생성 | 사용자 | Flow | `FLOW_A_R1.md`의 순서대로. 짝 컷은 순차 |
| 검수 | Claude | basak-shorts-review | 라운드마다 `CLEAN_REVIEW_R*.md`, 조건부 컷은 참조 첨부로 재생성 |
| 룩 | Claude | capcut-dual-look | 2초 프리뷰와 4분할 비교 후 승인 |
| 자막 | Claude | basak-shorts-caption | 확정 음성 타이밍에 맞춤 |

### 4.3 검수 최우선 (매 라운드)
1. **K09**: 두 마커가 같은 선로 위에 있는가(레일을 따라가 확인). 끝에 간격이 남는가.
2. **K03 ↔ K07**: 같은 판 위에서 1.5 km 띠와 100 m 띠의 차이가 한눈에 보이는가.
3. 도장에 글자·로고가 없는가 / INFO에 한글이 0자인가.
4. 충돌·손상·연기·사람 얼굴이 없는가.

### 4.4 일정

| 날짜 | 작업 |
|---|---|
| 10/29 (목) | T0 → VO 합성·실측 → 비트표 LOCK → CLEAN R1 (K09 · K04 · K03 · K02 · K01 → 짝 K06 · K11 → K10 · K08) |
| 10/30 (금) | INFO R1 · MP4 R1 → 검수 → R2 재생성 |
| 10/31 (토) | R3 마무리 → 룩 → 자막 → 믹스 → G9 사실 재확인 → **공개** (스페인 애도 기간 10/28~10/30 이후) |

### 4.5 리스크

| 리스크 | 대응 |
|---|---|
| K09 두 점이 다른 선로로 나뉨 | CLEAN을 단선처럼 보이는 고고도 부감으로 생성, "Both dots sit exactly on the same railway line" 유지. 3회 실패하면 K09를 K03 구도의 지상 부감으로 재설계 |
| Frames to Video가 9:16을 받지 않음 | Ingredients to Video(9:16 지원 확인)로 같은 타임라인 문장 사용 |
| K05에 붉은 점멸이 생김 | 즉시 불합격. "No flashing, no red warning lights" 유지 |
| 도장이 실제 Renfe·Iryo 색으로 끌려감 | [TRAIN LOCK]의 흰 차체 + 회색 띠 유지. 브랜드명·형식명은 쓰지 않음 |
| 유튜브 AI 라벨 | 전편이 AI 생성이므로 신고하고 라벨을 받아들임 |

---

## 5. 버전 B — 품질 개선 (blender-short-3d-pipeline 기준 P0–P11)

### P0 판정
- **경로 C로 올리는 근거(§0-3)**: ① 치수 비례가 FAIL 기준(K03과 K07의 1,654 m 대 84 m) ② 부품 간 상대 위치가 핵심(K09 같은 선로 위 25 km) ③ 철도 자산을 3편 이상 재사용(신호·제동·열차제어 후속편).
- **구성: 실사 브리지형.** 사람(관제실)과 실사 풍경 훅은 Flow가 싸게 만들고, 비례와 위치가 중요한 컷은 Blender가 맡습니다.
- 대안: 풀3D형(K01 · K08 · K11도 3D로). AI 라벨을 피할 수 있지만, 관제실은 사람 없이 장비 클로즈업으로 바꿔야 하고 2일이 더 걸립니다. → G0에서 사용자가 선택(G-6).

### P1 목표
45초 안에 "고속열차는 멈출 수 있는 거리 안에서만 달린다 → 그 거리를 알려주던 신호가 끊기면 눈으로 멈출 수 있는 속도로 달려야 한다"를 정확한 축척으로 보여줍니다.

### P2 LOCK 요약
FACT · SPEC · STYLE은 `prompts/LOCKS.md`. RIG는 `blender/rig_config.json`(트랙 중심 간격, LZB 교차 간격 등 UNVERIFIED 항목은 G1에서 확인).

### P3 레퍼런스
NOT_PERFORMED — 기준 레퍼런스 영상을 아직 받지 못했습니다(G-2). 받으면 §1의 측정 명령으로 샷 길이 중앙값, 10초당 컷 수, LUFS, 루프 SSIM을 재고 목표값 열을 채웁니다.

### P4 비트표
§3과 같습니다. 음성은 A에서 LOCK한 파일을 재사용합니다. 사실이 바뀌어 대본이 바뀌면 새로 LOCK합니다.

### P5 컷 분담 · 리그 · 에셋

| 컷 | 소스 | 핵심 |
|---|---|---|
| K01 · K11 | Flow 브리지 (순차 짝) | W0 훅·루프 |
| K02 · K03 · K04 · K05 · K06 · K07 | **Blender M1 "선로 마스터"** | 선로 하나에 카메라만 분기. K03과 K07은 같은 카메라, 띠 길이만 다름 |
| K08 | Flow 브리지 | 관제실 |
| K09 · K10 | **Blender M2 "25 km 회랑"** | 30 × 6 km 지형, 같은 선로 좌표 위의 두 마커, 고도 9 km 카메라 |

- **M1**: 표준궤 1,435 mm, UIC60 근사 레일, 침목 0.6 m 간격(인스턴스), 도상은 산포. LZB 케이블은 궤간 중앙 + 레일 하부, 100 m 교차(UNVERIFIED-minor). 열차는 구매 또는 CC0 일반형 1종을 [TRAIN LOCK] 도장으로 다시 칠함.
- **베이크**: K03(200 km/h, a = 1.0, 12배속)과 K07(40 km/h, 4배속)은 등감속 해석해. K09는 08:36→08:53 선형 시간축(255배속)이며 실제 속도 곡선은 재현하지 않습니다. 사건 F는 베이크에서 역산해 `geometry_qc.json.events`에 기록합니다.
- **2.5D 강조**(청록 펄스, 금색 띠, 숫자)는 후합성 레이어로만 넣습니다. 3D 씬 안에는 발광물을 넣지 않습니다.
- 에셋 영수증과 라이선스는 `assets/LICENSES.csv`에 기록합니다.

### P6 룩 · 카메라
- AgX + Medium High Contrast. 해는 고도 약 7°, 방위 약 110°(10/28 08:45 CET 톨레도 근사, 룩 기준일 뿐 사실 주장 아님).
- 명도 3층: 흰 차체(밝음) / 도상·침목(중간 회색) / 황토 들판(중간~어두움). LZB 케이블 albedo ≤ 0.05, 침목 0.35. 케이블이 540p 인코딩본에서 읽혀야 합니다.
- 카메라: K02 · K06은 follow, K03 · K07 · K09 · K10은 world. K03과 K07은 **같은 카메라 키**를 씁니다.
- 판독 컷은 저속 푸시인. 완전 정지는 금지합니다. K10만 예외로 거의 정지(추모 톤).

### P7 사운드
레일 이음 리듬(K02 고속 → K06 저속으로 간격이 늘어남)을 제동 원리의 청각 단서로 씁니다. 교신은 실제 녹음을 쓰지 않고 무전 잡음 질감만 씁니다. K10은 바람 소리만. 통합 −14 LUFS, TP −1 dBTP.

### P8 Flow 브리지
`FLOW_A_R1.md`의 K01 · K11 · K08을 그대로 씁니다. K01 → K02(3D)는 하드컷입니다. 3D에서 실사로 넘어가는 K07 → K08 이음에서 Flow 시작 입력이 필요하면 **최종 렌더본의 실제 마지막 프레임**을 씁니다.

### P9 게이트

| 게이트 | 통과 조건 | 담당 |
|---|---|---|
| G0 | 이 문서 + 블로커 G-1~G-6 정리 | Claude → 사용자 승인 |
| G1 | 트랙 중심 간격·LZB 배치 문헌 확인, 레퍼런스 측정 | Claude |
| G2 | VO LOCK(sha256), 단어 타임스탬프, 명사 선행 노출(대상 노출 F ≤ 명사 F − 6) | 사용자 + Claude |
| G3 | 베이크 검증: 정지거리 1,654.3 m / 84.0 m 오차 ±0.5 m, 마커가 선로 곡선에서 벗어나지 않음 | Claude (cloud bpy 4.5.14) |
| G4 | 씬 충돌 0건(열차–레일, 케이블–침목) | Claude |
| G5 | 270p 애니매틱, A 클립과 나란히 비교 | 검증 세션 |
| G6 | **핵심 4초 = K09 F745–840** 540p 24spp, 정상 속도로 판독 | 검증 세션 |
| G7 | 540p 전편, UI 마스크·저비트레이트 스트레스·루프 SSIM | 검증 + 사용자 |
| G8 | 1080p 최종, 프레임 1080개·디코드 오류 0·bt709 행렬 | 사용자 GPU (RUN_ALL.ps1) |
| G9 | 사실 재확인(사망자·CIAF·기록장치 속도), AI 라벨, 라이선스 | 사용자 승인 |

### P10 일정 · 렌더 예산

| 날짜 | 작업 |
|---|---|
| 11/1–2 | G0·G1, 에셋 구입, 베이크·빌드 스크립트 |
| 11/3 | G3·G4 (클라우드), 270p 애니매틱(G5) |
| 11/4 | Flow 브리지 3컷(사용자, 병렬), K03 ↔ K07 짝 540p |
| 11/5 | G6 핵심 4초 |
| 11/6 | G7 전편 프리뷰, 리뷰 R## |
| 11/7 | G8 로컬 GPU 최종 렌더 |
| 11/8 | G9 → 공개(또는 CIAF 발표 시점까지 보류) |

렌더 예산: Blender 프레임 **732F**(M1 540F + M2 192F). 대표 프레임 1장을 RTX 3060 Ti에서 실측한 뒤 환산합니다. 예를 들어 프레임당 30초면 약 6.1시간, 60초면 약 12.2시간입니다. 추정치로 일정을 확정하지 않습니다.

### P11 리스크
| 리스크 | 대응 |
|---|---|
| 9 km 고도에서 선로가 안 보임 | 실제 폭 대신 후합성 선(청백)으로 선로를 강조. 3D 씬에는 넣지 않음 |
| 흰 차체와 하늘이 섞임 | 배경 명도 → 카메라 거리 → 조명 순서로 수정(형상은 바꾸지 않음) |
| 사실이 바뀜(속도·원인) | rig_config와 대본만 고치고 다시 렌더. 대본 변경은 VO 재LOCK |
| 에셋 라이선스 | 상업 영상 사용 가능 여부를 확인하지 않은 에셋은 G8 전에 교체 |

---

## 6. 공개 게이트 G9 (두 버전 공통)

- **시점**: 스페인 애도 기간(10/28~10/30)이 끝난 뒤. 공개 직전에 사망자 수, CIAF·법원 발표, 기록장치 속도를 다시 확인합니다.
- **제목 후보**: ① 「고속열차는 앞차를 보고 멈추지 않습니다」(추천, 단정 없음) ② 「시속 40으로 가야 했던 25km」(REPORTED 규정에 기댄 제목이라 G9에서 재판단)
- **썸네일**: K03 ↔ K07 띠 비교 한 장(긴 금색 띠 / 짧은 금색 띠). 충돌, 사망자 숫자, "충격"이라는 단어는 쓰지 않습니다.
- **설명란**: 추모 문장 한 줄 → "개념 재현이며 실제 사고 장면이 아닙니다" → 가정(감속 1.0 m/s², 반응 2초) → ASFA 등 대체 보호 체계가 있다는 설명 → 출처 목록.
- **고정 댓글(Binary CTA)**: 1⃣ KTX 열차제어 편이 궁금하다 / 2⃣ 고속열차 제동 장치 편이 궁금하다.

---

## 7. 블로커와 사용자 할 일

1. **G-1** 한국 규정 확인: 「철도차량운전규칙」의 시계운전·신호 장애 시 운전 조항, 코레일 운전취급규정. 이 세션에서는 law.go.kr에 접속하지 못했습니다. 확인하지 못하면 N11 대체안을 씁니다.
2. **G-2** 버전 B 기준 레퍼런스 영상 지정(측정용).
3. **G-3** ElevenLabs 보이스 LOCK과 VO 합성(`vo/VO_SCRIPT_R3.txt`).
4. **G-4** Flow 생성(`prompts/FLOW_A_R1.md` 순서대로). 결과물을 폴더나 채팅으로 주시면 basak-shorts-review로 검수합니다.
5. **G-5** 버전 B 열차 에셋 구입 또는 CC0 선택.
6. **G-6** 버전 B 구성(실사 브리지형 / 풀3D형)과 검증 주체(생성자와 다른 세션 또는 Codex) 지정.

---

## 8. 출처

- 교신·타임라인: [El Español — 미닛바이미닛](https://www.elespanol.com/invertia/observatorios/movilidad/20261028/accidente-minuto-ave-impacto-iryo-kmh-recibir-orden-adif-rebasar-semaforo-rojo/1003744438265_0.html), [elDiario.es — 교신 녹음](https://www.eldiario.es/castilla-la-mancha/centro-control-adif-maquinista-iryo-reanude-marcha-normal_1_13623014.html), [El Constitucional — 교신 녹음](https://elconstitucional.es/es/nacional/audios-sala-control-adif-recogen-orden-marcha-normal-ave-aviso-iryo-minutos-antes-accidente-ferroviaro-en-urda-toledo_9541_102.html), [elDiario.es — 장관 "설명할 수 없다"](https://www.eldiario.es/castilla-la-mancha/puente-apunta-error-humano-inexplicable-decision-reanudar-marcha-ave-accidente-iryo-urda-toledo_1_13621754.html)
- 시계운전 40 km/h: [Herqles](https://herqles.com/2026/10/28/marcha-vista-protocolo-choque-urda/), [El periódico de la ingeniería](https://elperiodicodelaingenieria.es/puente-situa-el-origen-del-accidente-de-urda-en-el-operario-que-permitio-al-ave-reanudar-la-marcha-normal/), [La Ciutat](https://laciutat.cat/es/espana/audios-urda-revelan-adif-ordeno-ave-reanudar-marcha-velocidad-normal_903956_102.html)
- 상충 보도: [Demócrata — Iryo 측 반박](https://www.democrata.es/actualidad/iryo-seguia-esperando-instrucciones-adif-cuando-fue-alcanzado-por-ave-en-urda/), [El Español — Iryo는 지시를 받지 못함](https://www.elespanol.com/invertia/observatorios/movilidad/20261028/iryo-arrollado-ave-no-recibido-orden-adif-reanudar-marcha-momento-accidente/1003744438459_0.html)
- 사망자·애도: [La Voz del Sur — 공식 68명](https://www.lavozdelsur.es/actualidad/sociedad/la-cifra-oficial-de-fallecidos-sube-hasta-los-68-por-el-accidente-de-tren-de-urda-hay-15-heridos-graves.html), [El Progreso](https://www.elprogreso.es/articulo/espana/directo-grave-accidente-tren-toledo-dos-trenes-chocan-urda-ordaz-ultima-hora/202610280931312009828.html), [Público 라이브](https://www.publico.es/sociedad/ultima-hora-accidente-trenes-toledo-directo.html)
- LZB·ASFA: [Wikipedia — LZB](https://en.wikipedia.org/wiki/Linienzugbeeinflussung), [Wikipedia — ASFA](https://en.wikipedia.org/wiki/Anuncio_de_Se%C3%B1ales_y_Frenado_Autom%C3%A1tico), [Xataka — 신형 차량은 ETCS·ASFA, ASFA 200 km/h 상한](https://www.xataka.com/movilidad/renfe-va-a-gastarse-1-362-millones-euros-30-trenes-ave-mayor-compra-su-historia-uno-peores-momentos), [Libertad Digital — LZB 설명](https://www.libertaddigital.com/espana/2026-10-28/que-es-el-lzb-el-sistema-que-se-desactivo-antes-del-brutal-accidente-de-urda-7483406/)
- 제동거리: [Chang'an Univ. — CRH 비상제동 거리](https://transport.chd.edu.cn/en/article/doi/10.19818/j.cnki.1671-1637.2011.03.008), [JR East 기술 보고](https://www.jreast.co.jp/e/development/tech/pdf%5F12/Tec-12-12-15eng.pdf), [Trains.com — TGV 3.5 km 인용](https://forum.trains.com/t/stopping-distance/139033)
- Flow / Veo: [TechCrunch — Veo 3.1 9:16 Ingredients](https://www.techcrunch.com/2026/01/13/googles-update-for-veo-3-1-lets-users-create-vertical-videos-through-reference-images/), [RunDiffusion — Veo 3.1 길이·Frames to Video](https://learn.rundiffusion.com/google-new-veo-3-1-model)
- 한국 규정(미확인 상태): [철도안전공단 운전면허 표준교재 PDF](https://www.srail.or.kr/editor/2022/09/27/file3.pdf), [나무위키 — TVM](https://namu.wiki/w/TVM)
