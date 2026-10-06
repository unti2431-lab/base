# 2026 완주군 사진·AI영상 공모전 (AI영상 부문) — 장면 구성 R2

> 작품명 **《완주가 들리는 버스》** — 핵심 문장: 조용히 달리면, 완주가 들립니다
> **78초 · 16:9 · 1920×1080 · 24fps · MP4 · Google Flow(Veo) 단독 생성 — 영상과 음향 모두 Veo 출력만 사용**

---

## 0. 요강 재확인 (2026-10-06 기준)

| 항목 | 내용 (초안 조사 기준) | 연출에 반영할 점 |
|---|---|---|
| 주제 | 관광명소·축제·랜드마크 + **미래산업·캠페인** | 미래산업(수소)을 축으로 하되, **로컬푸드·만경강·한옥** 같은 생활과 장소를 함께 담음 |
| 제작 조건 | **영상·음향 모두 AI 프로그램으로 제작**, 미발표 창작물, 사용한 AI 프로그램과 제작 과정 확인 | 내레이션(TTS)·스톡 효과음·외부 음악을 쓰지 않음. **Veo가 클립과 함께 생성한 소리만으로 완성** → Flow 단독 파이프라인과 정확히 맞음 |
| 규격 | **60~120초**, 가로·세로 FHD, MP4 | 78초, 16:9. 풍경과 버스의 가로 움직임에는 가로 화면이 맞고, Veo도 16:9가 가장 안정적임 |
| 필수 문구 | 시작 부분 하단: **『2026년 완주군 AI영상 공모전』 출품작으로, 생성형 AI 기술을 활용해 제작하였습니다** | 01컷은 상단 2/3에 피사체를 두고 하단을 비워 둠. 문구는 편집에서 넣음 |
| 접수 | **10/30(금) 18:00**, 이메일 hnlim15@korea.kr | 내부 목표 10/27 |
| 시상 | AI영상 최우수 150만 원 | — |

> **확인 한계**: 이번 세션 환경에서는 공모 원문 페이지와 첨부 요강에 접속하지 못했음. 위 조건은 이전 조사 결과를 그대로 옮긴 것이며, **심사 기준·배점, 참조 사진을 입력으로 쓸 수 있는지, 저작권 이용 범위는 원문으로 재확인해야 함.**

### 이 작품이 기대는 사실
- 현대차 전주공장은 **완주군 봉동읍**에 있는 상용차 생산기지로, **수소버스를 생산**함(전북일보 보도). → "이 조용함은 완주에서 만들어집니다"의 근거. 단, 브랜드·로고는 화면에 넣지 않음.
- 완주는 2025년 **수소특화단지** 지정과 함께 산학연관 16개 기관이 참여하는 체계를 갖춤(전북일보 2025-08).
- 2012년 **전국 첫 로컬푸드 직매장**이 완주 용진면에 생김. → 05컷 '아침 장' 장면의 근거.
- 수소전기버스는 전기모터로 구동되므로 디젤버스보다 조용함. **'무소음', '배출가스 제로', '물만 나온다' 같은 표현은 쓰지 않음.**

---

## 1. 초안 《다음 정류장은, 완주》 검토

### 유지할 것
1. 버스 한 대의 외형을 끝까지 고정한다는 원칙. 정차 → 문 열림 → 승차 → 출발의 순서를 지키는 검수 기준.
2. 기술에서 사람과 일상으로 넘어가는 방향.
3. '미래 비전 창작 장면'임을 숨기지 않는 태도.

### 고칠 것

| # | 문제 | 왜 문제인가 | R2 해결 |
|---|---|---|---|
| 1 | **물방울로 시작하는 도입** | 수소차 광고에서 이미 많이 쓴 상투적 장면이고, '물만 나온다'는 과장으로 읽힐 위험이 있음 | 물방울을 빼고, 수소버스의 체감 가능한 특징인 **조용함**으로 바꿈 |
| 2 | **연료전지 원리 설명 14초** | Veo가 가장 자주 무너뜨리는 도해 장면이고, 지자체 홍보 심사에서 원리 설명은 점수가 되지 않음 | 원리 설명을 모두 뺌. 기술은 **'조용함'이라는 결과**로만 느끼게 함 |
| 3 | **완주라는 장소가 약함** | 정류장, 실습실, 공장은 어느 도시에서나 찍을 수 있는 장면이라 다른 지역 이름을 붙여도 성립함 | **로컬푸드 직매장, 만경강 철교, 한옥마을, 수소버스를 만드는 공장**을 한 노선으로 이음. 모두 완주에만 있는 조합임 |
| 4 | **'영상·음향 모두 AI' 조건과 내레이션의 충돌** | 내레이션을 쓰려면 TTS가 필요하고, Flow만으로는 한국어 내레이션 톤을 일정하게 유지하기 어려움 | **내레이션을 없애고 소리가 주인공**이 되게 함. Veo 네이티브 오디오의 강점과 정확히 맞물림 |
| 5 | '배우는 손 → 만드는 손' 매치컷 | 아이디어는 좋지만 손 클로즈업이 버스 장면과 따로 놀고, 손가락 오류가 생기기 쉬움 | 주인공 한 명(공장 기술자)이 **출근 버스를 타고 가서 같은 버스를 만드는 자리에 도착**하는 고리로 대체함 |
| 6 | 9:16 세로 | 버스가 화면을 가로지르는 장면과 넓은 풍경을 세로 화면에 담으면 답답해짐 | 16:9 |

---

## 2. 톤앤매너 — 요강에서 나온 결론

- **심사 주체가 지자체**이므로 관건은 "완주 사람이 봤을 때 우리 동네가 맞다"는 정확성과 따뜻함임. 서울식 미래도시, 홀로그램, 드론 쇼는 오히려 감점 요인임.
- **'미래산업'을 공장 굴뚝이나 공학 도해가 아니라 아침 출근길의 감각으로** 보여줌.
- **목표 톤**: 이른 아침의 조용함, 생활 소리의 해상도, 과장 없는 자부심.

---

## 3. 룩앤필 — "소리로 그린 노선도(Sound-first Route)"

> 근거: Filmsupply *Commercial Filmmaking Trend Report 2026*의 **Keep It Stupid Cinematic**(적은 카메라 이동, 깨끗한 구도, 압축된 이야기)과 **Unconventional POV**(사물에 단 카메라). 여기에 이 작품만의 장치 두 가지를 더했음. 이름은 이 문서에서 붙인 것이며 업계 표준 용어가 아님. '국내에서 드물다'는 판단에 통계 근거는 없음.

| 장치 | 방법 | 효과 |
|---|---|---|
| **① 역전된 통과 장면(Inverted Pass-by)** | 장소마다 고정된 와이드 타블로. 버스가 화면을 천천히 가로질러 지나가는데, **버스 소리가 커지는 대신 그 장소의 소리가 또렷해짐** | 일반 자동차 광고의 문법(엔진음이 커짐)을 뒤집음. 기술 설명 없이 '조용한 버스'가 전달됨 |
| **② 문에 단 카메라(Door-mount POV)** | 카메라가 버스 출입문 틀에 붙어 있는 시점. 문이 열릴 때마다 **문틀이 액자처럼** 새 장소를 보여주고, 그 장소의 소리가 안으로 쏟아져 들어옴 | 버스 = 완주를 여는 창. 장면 전환 장치가 곧 이야기 장치임 |
| **③ 소리 자막(Sound Captions)** | 청각장애인용 자막처럼 `[만경강 갈대 바람]` 형식으로 **소리를 글자로 적음**. 해외 브랜드 필름에서 접근성과 디자인 요소로 쓰이는 방식 | 소리 없이 보는 사람도 주제를 이해함. 배리어프리 태도는 공공 심사에서 가점 요인이 될 수 있음 |
| **④ 이어폰을 빼는 손** | 주인공이 버스에 타서 이어폰 한쪽을 뺌. 대사 없는 동기 부여 | "들을 만한 것이 있다"는 이 작품의 선언 |

### 화면 규칙 (LOOK LOCK)
- **카메라**: 타블로는 완전히 고정. 버스 안은 고정 또는 아주 느린 슬라이드. 드론과 빠른 추격은 쓰지 않음(마지막 원경 한 컷만 높은 고정 시점).
- **렌즈 감각**: 타블로는 35~40mm 와이드(왜곡 없음), 문 POV는 24mm, 인물은 50mm.
- **시간대**: 영상 전체가 **해 뜨기 직전부터 해 뜬 직후까지**의 한 아침 안에서 진행됨. 컷이 넘어갈수록 빛이 조금씩 밝아짐(푸른 새벽 → 금빛 아침).
- **팔레트**
  - 새벽 남청 `#2E3A4A`
  - 들판 연두 `#A9B98A`
  - 아침 금빛 `#E3B76B`
  - 버스 차체 오프화이트 `#F2F1EC` + 포인트 청록 `#2F7F86`
- **질감**: 16mm 느낌의 약한 그레인, 낮은 대비. 하늘이 날아가는 HDR 금지.
- **버스 고정 사양(BUS LOCK)**: 오프화이트 차체 + 청록 띠 하나, 둥근 전면, **지붕 위 수소탱크 덮개**, 저상 2도어, 행선지 LED는 꺼진 상태, 로고 없음. 바퀴 수와 문 위치는 모든 컷에서 같아야 함.
- **사운드**: 각 클립의 Veo 오디오를 그대로 사용함. 음악 없음. 버스 소리는 '젖은 노면을 지나는 타이어 소리, 낮은 모터 소리, 부드러운 문 소리' 세 가지로 제한함.
- **절대 금지**: 배기구 물방울, 연료전지 도해, 미래도시·홀로그램, 실존 기업 로고, 생성된 한글(정류장 표지판·LED는 비우거나 초점 밖), 외부 음원.

---

## 4. 장면 구성 (78초 · 13컷)

| 컷 · 시간 | 화면과 동작 | 카메라 | 소리 (모두 Veo 생성) | 자막 |
|---|---|---|---|---|
| **01 · 0–6** | 안개 낀 새벽, 논 사이 시골 정류장. 작업복 점퍼를 입은 20대 여성 기술자가 보온병을 들고 기다림. 하늘에 남청빛이 남아 있음 | 고정 와이드. 피사체는 화면 위쪽 2/3에 두고 하단을 비움 | 새벽 새소리, 멀리서 개 짖는 소리, 논물 소리 | **하단 필수 문구** / `[새벽 새소리]` |
| **02 · 6–12** | 같은 구도. 버스가 오른쪽에서 천천히 들어와 정류장에 **완전히 멈춤** | 고정. 버스가 들어와도 카메라는 움직이지 않음 | 새소리가 그대로 들림. 젖은 노면 위 타이어 소리만 아주 작게 | 작품명 작게: **완주가 들리는 버스** |
| **03 · 12–16** | **문 POV.** 문이 열리고 문틀 안으로 여성이 올라탐 | 문틀에 고정된 24mm | 부드러운 문 소리, 계단 밟는 소리 | — |
| **04 · 16–22** | 창가 자리. 여성이 창밖을 보다가 **이어폰 한쪽을 뺌** | 50mm, 고정 | 이어폰을 빼는 순간 버스 안의 낮은 정적과 바깥 소리가 열림 | — |
| **05 · 22–30** | **통과 장면 1 — 로컬푸드 직매장 아침.** 농민들이 채소 상자를 내리고, 첫 손님이 장바구니를 들고 들어감. 뒤로 버스가 천천히 지나감 | 고정 와이드 타블로 | 상자 내려놓는 소리, 대화 웅성임, 비닐 소리. 버스가 지나가도 이 소리가 줄지 않음 | `[아침 장 보는 소리]` |
| **06 · 30–34** | **문 POV.** 문이 열리고 상추 상자를 든 할머니가 올라탐 | 문틀 고정 | 문이 열리자 시장 소리가 안으로 쏟아짐 | — |
| **07 · 34–42** | **통과 장면 2 — 만경강.** 넓은 강, 갈대, 강을 건너는 낡은 철교. 강변 길을 따라 버스가 작게 지나감 | 고정 와이드, 수평선은 화면 1/3 | 갈대 바람, 물살 | `[만경강 갈대 바람]` |
| **08 · 42–47** | 버스 안. 옆자리 할머니가 상자에서 오이 하나를 꺼내 여성에게 건넴. 여성이 웃으며 받음 | 50mm 투샷, 고정 | 작은 웃음소리, 오이를 받는 소리 | — |
| **09 · 47–53** | **통과 장면 3 — 한옥마을 아침.** 기와지붕 너머 산 능선, 마당을 쓰는 비질. 담장 밖으로 버스가 지나감 | 고정 와이드 | 대빗자루 소리, 처마의 새소리 | `[마당 쓰는 소리]` |
| **10 · 53–59** | 산업단지 정류장. 해가 막 떠오름. 여성이 내리고 버스가 조용히 출발함 | **버스 안 문 POV**로 시작해 문이 닫히는 순간 컷 → 바깥 고정 와이드에서 버스가 멀어짐 | 문 닫히는 소리, 멀어지는 타이어 소리 | **조용히 달리면, / 완주가 들립니다.** |
| **11 · 59–66** | 공장 안. 조립 중인 같은 사양의 버스 차체가 줄지어 있음(로고 없음). 여성이 새 차체 옆면에 **손바닥을 대고** 올려다봄 | 50mm, 아주 느린 전진 하나 | 넓은 공장 공간의 잔향, 멀리서 공구 소리 | **이 조용함은, / 완주에서 만들어집니다.** |
| **12 · 66–72** | 높은 고정 시점의 원경. 금빛 아침, 들판과 산 사이 길로 버스 한 대가 작게 지나감 | 고정. 버스는 화면의 1/20 크기 | 들판 바람, 새소리. 버스 소리는 들리지 않음 | `[완주의 아침]` |
| **13 · 72–78** | 12의 마지막 프레임을 멈추고 엔드카드를 얹음 | 편집 | 12의 바람 소리가 이어짐 | **수소로 달리는 완주** / 《완주가 들리는 버스》 / 완주의 내일을 상상한 AI 영상 |

### 이 작품의 승부 장면
- **02 (조용한 도착)**: 버스가 들어와 멈출 때까지 새소리가 계속 들려야 함. 이 6초가 성립하면 작품 전체의 규칙을 관객이 이해함. **가장 먼저 시험할 컷.**
- **06 (문이 열리자 시장 소리가 쏟아짐)**: 문 POV 장치가 소리 장치와 처음으로 결합하는 순간.
- **10 → 11 (내림 → 손바닥)**: 출근길 승객이 사실은 이 버스를 만드는 사람이었다는 짧은 반전. 미래산업과 생활이 한 사람 안에서 이어짐.

---

## 5. Google Flow 제작 순서 (Flow 단독)

### 5-1. 기준 이미지 고정
| ID | 내용 |
|---|---|
| **ING-BUS** | BUS LOCK 사양의 버스를 측면, 전면 3/4, 문 클로즈업 세 장으로 생성. 이 중 측면 이미지를 모든 버스 컷의 참조로 씀 |
| **ING-W 기술자** | 20대 한국인 여성, 짧은 단발, 남색 작업 점퍼, 보온병. 장신구 없음 |
| **ING-G 할머니** | 70대, 꽃무늬 조끼, 상추 상자 |

### 5-2. 생성 순서
1. **01 → 02** (같은 구도, Frames to Video): 버스가 멈췄을 때 형상이 유지되는지, 새소리가 계속되는지 확인함.
2. **03·06·10 문 POV 3종**: 문틀 위치를 고정하는 것이 관건임. 03의 첫 프레임 이미지를 06·10의 시작 프레임으로 고쳐서 재사용함.
3. **통과 장면 05·07·09**: 버스가 작게 나오므로 형상 오류가 덜 보임. 장소 특징이 맞는지에 집중함.
4. 08·11·12.

Veo 3.1 Fast로 시험하고 채택 컷만 Quality로 다시 생성함. 클립은 8초로 생성해서 잘라 씀. Extend는 02처럼 버스가 멈춘 뒤의 여운이 부족할 때만 사용함.

### 5-3. 오디오 원칙 (영상·음향 모두 AI 조건)
- 모든 소리는 **해당 컷 Veo 클립의 오디오**에서 가져옴. 소리를 다른 컷으로 옮기는 J컷·L컷 편집은 가능함(원천은 여전히 Veo 출력이기 때문).
- 프롬프트마다 `No music.`을 넣고, 원하지 않는 배경음악이 생성되면 다시 뽑음.
- 사람 대사는 생성하지 않음. 웅성임처럼 알아들을 수 없는 생활 소음만 허용함.
- 제출 시 '사용 AI 프로그램: Google Flow(Veo 3.1, 이미지 생성 포함) / 편집: ○○(자르기·자막·필수 문구)'로 제작 과정을 기록함.

### 5-4. 컷별 Flow 프롬프트 (영문)

공통 끝문장: `Shot on 16mm film, soft low-contrast early-morning light, subtle grain, no text, no signage text, no logos, no watermark. No music.`

- **01**: `Locked-off wide shot of a small rural bus stop between misty rice paddies in rural Korea before sunrise, deep blue sky. A young Korean woman in a navy work jacket waits holding a thermos. Subject in the upper two-thirds of frame, empty road in the lower third. Sound: dawn birdsong, distant dog bark, trickling paddy water.` + ING-W
- **02**: `Same locked-off composition. An off-white low-floor city bus with a single teal stripe and a roof-mounted hydrogen tank housing glides in from the right and comes to a complete stop at the stop. The camera does not move. Sound: the birdsong continues uninterrupted; only a faint hiss of tires on wet asphalt, almost silent motor.` + ING-BUS, ING-W
- **03**: `Point of view from a camera mounted on the bus door frame. The door folds open, framing the misty stop, and the young woman steps aboard. Sound: soft pneumatic door sigh, footsteps on the step.` + ING-BUS, ING-W
- **04**: `Medium shot inside a quiet bus by the window, morning blue light. The young woman looks outside and slowly removes one earbud. Locked camera. Sound: quiet cabin tone opening up to faint outside ambience.` + ING-W
- **05**: `Locked-off wide tableau of a Korean local food direct market at early morning. Farmers unload crates of fresh greens; a first customer walks in with a shopping bag. In the background the off-white bus passes slowly. Sound: crates set down, murmured chatter, plastic rustle; the bus is barely audible.` + ING-BUS
- **06**: `Point of view from the bus door frame. The door opens and an elderly Korean woman in a floral vest climbs aboard holding a crate of lettuce. Sound: market ambience pours in as the door opens.` + ING-BUS, ING-G
- **07**: `Locked-off wide shot of a broad river with reeds and an old iron railway bridge crossing it, morning haze. The off-white bus passes small along the riverside road. Horizon on the lower third. Sound: wind through reeds, flowing water.` + ING-BUS
- **08**: `Two-shot inside the bus. The elderly woman takes a cucumber from her crate and offers it to the young woman, who smiles and accepts it. Locked camera. Sound: soft laughter, a quiet thank-you murmur without clear words.` + ING-W, ING-G
- **09**: `Locked-off wide shot of a traditional Korean hanok village at morning, tiled roofs against a mountain ridge, someone sweeping a courtyard with a bamboo broom. Beyond the stone wall the off-white bus passes. Sound: broom strokes, birds under the eaves.` + ING-BUS
- **10**: `Point of view from inside the bus at the door as the young woman steps off at an industrial-park stop at sunrise; the door closes. Then a locked-off wide shot as the bus pulls away quietly. Sound: door closing, receding tire hiss.` + ING-BUS, ING-W
- **11**: `Inside a bright bus assembly hall, rows of identical off-white bus bodies without logos. The young woman places her palm on the side panel of a new bus and looks up. Very slow push-in. Sound: large hall reverb, distant tool sounds.` + ING-BUS, ING-W
- **12**: `High locked-off extreme wide shot of golden morning farmland and low mountains in rural Korea; one small off-white bus travels along a road between the fields. Sound: wind over fields, birdsong; the bus is inaudible.` + ING-BUS

---

## 6. 검수 기준 (반려 조건)

- 버스의 바퀴 수, 문 위치, 지붕 덮개, 띠 색이 컷마다 달라짐
- 정차하기 전에 문이 열리거나, 사람이 다 타기 전에 출발함
- 배기구에서 물이나 김이 나옴
- 표지판·LED·차체에 글자나 로고가 생김
- 배경음악이 생성됨, 또는 알아들을 수 있는 한국어 대사가 어색하게 생성됨
- 만경강 철교·한옥마을이 다른 지역(서양식 다리, 일본식 지붕)처럼 보임

## 7. 일정

| 기간 | 작업 |
|---|---|
| 10/12–14 | 한의약 접수 후 착수. ING 고정, **02 조용한 도착** 시험 |
| 10/15–19 | 문 POV 3종, 통과 장면 3종 |
| 10/20–23 | 인물 컷, Quality로 재생성 |
| 10/24–26 | 편집, 소리 자막, 필수 문구, 제작 과정 기록 |
| **10/27** | 내부 접수 목표 (마감 10/30 18:00) |

---

### 출처
- [전북일보 — 완주 수소특화단지 지정, 산학연관 16개 기관](https://www.jjan.kr/articleAmp/20250805580139)
- [전북일보 — 현대차 전주공장 수소버스](https://www.jjan.kr/articleAmp/20240427580036)
- [경향신문 — 완주 로컬푸드 직매장](https://www.khan.co.kr/article/201505052212525)
- [Filmsupply — The Commercial Filmmaking Trend Report 2026](https://wpengine.fm.co/filmsupply/commercial-filmmaking-trend-report-2026/)
