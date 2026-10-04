# 고성 해양심층수 브랜드 AI 영상 공모전 — 장면 구성 v2

> 가제 **《얇은 한 장》** (부제: 바다는 들어오지 않습니다)
> 50초 · 16:9 · 1920×1080 · 24fps · MP4 · Google Flow(Veo) 단독 생성 파이프라인

---

## 0. 요강 재확인 (2026-10-04 기준)

| 항목 | 내용 | 초안에 주는 의미 |
|---|---|---|
| 접수 | 9/17 ~ **10/19** | **오늘 기준 D-15.** 제작 일정을 역산해야 함 |
| 주제 | '해양심층수의 가치, 브랜드로 이야기하다' — ① 청정·미네랄 가치 ② 활용 제품 브랜드 스토리 ③ 바이오·헬스케어·**친환경 등 새로운 미래** | ③을 겨냥한 방향은 맞음. 다만 **"브랜드로 이야기하다"**가 상위 주제이므로 기술 설명만으로 끝나면 안 됨 |
| 규격 | 30~60초, 가로형, FHD 1920×1080, 24/30fps MP4 | 50초 유지. 레터박스(2.39:1)는 쓰지 않고 16:9 전체를 씀 |
| 원본 | **원본 파일 제출 필수**, 미제출 시 심사 제외 가능 | Flow 프로젝트·키프레임·클립·프롬프트 로그를 처음부터 정리 |
| 자격 | 18세 이상 | — |
| 시상 | 10편 / 총 670만 원, 10/26 시상식(본인·대리인 참석) | — |

출처: 콘테스트코리아·뉴뉴스 보도 요약. 심사 배점은 공개 자료에서 확인하지 못했으므로 공식 요강 PDF에서 한 번 더 확인할 것.

---

## 1. 초안 검토

### 유지할 것 (초안의 강점)
1. **'섞이지 않고 열만 건너간다'는 단 하나의 발견**에 집중한 구조. 제품 나열형 영상과 확실히 구분됨.
2. 과장 금지 원칙(전기 없이·탄소 제로·절감률·얼음·서리 배제). 그대로 유지.
3. "개념 영상, 실제 시설 재현 아님"을 처음부터 밝히는 태도.
4. 제작 순서를 핵심 장면(C05)부터 잡은 것. AI 영상에서 가장 깨지기 쉬운 장면부터 검증하는 게 맞음.

### 고칠 것
| # | 문제 | 왜 문제인가 | v2 해결 |
|---|---|---|---|
| 1 | **첫 질문의 설득력이 약함** — "바닷물도 방 안으로 들어올까요?" | 실제로 그렇게 생각하는 관객이 거의 없음. 질문이 '만들어진 오해'처럼 들려 첫 3초 훅이 약함 | 관객이 이미 아는 것(**마시는 물**)에서 출발해 "그 차가움을 쓸 수 있다면?"으로 넘어감. 주제 ①과 ③을 함께 건드림 |
| 2 | **브랜드 존재감이 약함** | 9컷 중 6컷이 설비 설명. 심사 주체는 해양심층수 진흥 기관이고 상위 주제는 '브랜드로 이야기하다' | 물 한 잔(결로)으로 시작하고 같은 잔으로 끝나는 수미상관. 브랜드명이 마지막 한 줄이 아니라 영상 전체의 소재가 됨 |
| 3 | **면책 문구가 엔딩 브랜드 카드를 깎아먹음** | "실제 시설 재현 아님"이 브랜드명 바로 밑에 있으면 마지막 인상이 '아님'으로 끝남 | **영상 자체를 '실험대 위의 개념 모형'으로 연출**해 화면만으로도 개념 영상임을 알 수 있게 함. 면책은 모형 옆 박물관식 라벨로 처리(§3) |
| 4 | **산업 단면 CG는 AI가 가장 못하는 장면** | 배관 연결·통로 분리·단면 일관성은 Veo가 반복해서 무너뜨리는 영역. 초안도 실패 대비책을 따로 둬야 했음 | 단면 '도해'가 아니라 **실제로 있을 법한 유리·티타늄 실험 모형을 실사 촬영한 것처럼** 생성. Veo는 도표보다 사물을 훨씬 안정적으로 만듦 |
| 5 | **열을 '빛'으로 표현하면 판독이 모호함** | 판을 건너는 빛이 물이나 에너지 빔처럼 보일 위험. 초안이 가장 걱정한 '물이 판을 통과하는' 착시와 가까움 | **슐리렌(Schlieren) 광학**으로 표현: 온도 차이를 물속 굴절 무늬로 보여주는 실제 실험 기법. 물은 그대로 있고 '흔들리는 무늬'만 판을 건너감 |
| 6 | C02(개념 단면)·C07(전체 연결)이 둘 다 도식 장면이라 중복 | 50초 안에 같은 성격의 장면이 2번 나오고, 둘 다 생성 난도가 높음 | 같은 실험대 와이드 타블로 한 장면을 **두 번 다른 의미로** 사용(처음엔 공개, 나중엔 배출 경로 확인). 키프레임 1장으로 일관성도 확보 |
| 7 | 배출 경로 언급 없음 | 친환경 주제에서 "끌어올린 물은 어디로?"는 심사위원이 떠올릴 질문 | "바다는 바다로 돌아가고" 한 줄과 배출관 장면 추가. 배출수 온도 영향 등은 주장하지 않음 |
| 8 | 내레이션 밀도 | 9컷에 내레이션이 거의 빈틈없이 깔림 | 내레이션을 줄이고 **소리만 들리는 구간**을 확보(§2 사운드) |

### 사실 확인 메모
- 해수 냉방(SWAC)의 기본 구조: 심층수 ↔ 열교환기 ↔ 건물 순환수, 두 물은 섞이지 않음 — Makai Ocean Engineering 기술자료와 일치.
- 해수용 판형 열교환기는 부식 때문에 **티타늄 판**을 흔히 씀 → 모형의 판을 티타늄 질감으로 표현하는 근거. 단, 실제 열교환기는 판이 여러 장 겹친 구조이고 '한 장'은 원리를 단순화한 표현이라는 점을 의식할 것.
- 동해 중층수 수온은 약 1.1~2.7℃ 범위로 보고됨(koreascience 논문). "일 년 내내 차갑다"는 표현은 가능하나, **고성 취수 지점의 수심·수온 수치는 화면이나 내레이션에 넣지 않음**(진흥원 공식 수치를 확인하기 전까지).
- 열의 방향: 건물 쪽 물(따뜻함) → 판 → 심층수 쪽(차가움). 슐리렌 무늬는 **건물 쪽에서 출발해 심층수 쪽 흐름에 흩어지도록** 연출.

---

## 2. 룩앤필 — "표본 시네마(Specimen Cinema)"

> 해외 광고·모션 작업에서 늘어나고 있는 몇 가지 흐름을 이 작품에 맞게 묶은 연출 방향입니다. 이름은 이 문서에서 붙인 것이며, 업계 표준 용어는 아닙니다.

국내 지자체·공공 브랜드 영상은 대체로 **밝은 하이키, 고채도 블루, 드론 부감, 빠른 컷, 웅장한 음악, 큰 자막**의 문법을 씁니다. 이번 작품은 그 반대편에서 **'조용하고, 정확하고, 만질 수 있을 것 같은'** 쪽으로 갑니다. 2026년 해외 광고·모션 쪽에서는 화려한 CG 대신 진정성, 촉감이 느껴지는 질감, 이야기 중심 연출로 옮겨가는 흐름이 보고되고 있고, AI 영상에서는 매크로와 풍경 스케일을 끊김 없이 잇는 카메라 이동이 새로운 문법으로 언급됩니다(출처는 문서 끝).

### 다섯 가지 연출 장치

| 장치 | 무엇인가 | 이 작품에서 하는 일 |
|---|---|---|
| **① 슐리렌 광학** | 점광원과 칼날(knife-edge)로 공기·물의 밀도(온도) 차이를 은회색 굴절 무늬로 보이게 하는 실험 촬영법 | 열을 '빛'이 아니라 **실제로 보이는 물리 현상**으로 표현. 판을 건너는 것은 물이 아니라 흔들리는 무늬뿐이라 초안의 핵심 규칙을 화면이 스스로 지킴 |
| **② 디오라마 리빌(스케일 브레이크)** | 진짜 심해처럼 보이던 화면에서 카메라가 물러나며 그것이 실험대 위 유리 기둥 속 물이었음을 드러냄 | "이건 실제 시설이 아니라 제안입니다"를 **문구 없이 연출로** 선언. 영상의 시그니처 순간 |
| **③ 표본 라벨 타이포** | 자막을 화면 하단에 띄우지 않고, 모형 옆 박물관 라벨처럼 공간 안에 놓음 | 면책 문구("개념 모형")가 라벨 형식이라 고급스럽고 자연스러움 |
| **④ 모형 → 실재 매치컷** | 흰 건축 모형 방의 창 → 실제 방의 창. 같은 구도·같은 커튼 | 개념(모형)이 현실(방)로 이어지는 순간 = "가능성은 안으로" |
| **⑤ 사운드 퍼스트** | 수중 마이크·접촉 마이크 질감, 음악은 지속음 하나. 핵심 장면에서는 음악을 완전히 뺌 | 고급 브랜드 영상의 '정적' 문법. 내레이션 사이 침묵이 판독 시간을 만듦 |

### 화면 규칙 (LOOK LOCK)
- **카메라**: 한 컷에 움직임 하나. 핸드헬드 금지. 고정 또는 모션컨트롤처럼 매우 느린 슬라이더·푸시인. 드론 금지.
- **렌즈 감각**: 실내·실험대는 100mm 매크로 / 50mm, 얕은 심도. 광각 왜곡 금지.
- **조명**: 실험대는 검은 배경 + 측면 단일 키라이트 + 슐리렌용 점광원. 실내는 북향 창 같은 부드러운 자연광.
- **팔레트**(색은 의미 구분용으로만)
  - 심해 잉크 `#0B1A22` — 깊은 바다, 배경
  - 티타늄 실버 `#A7ADB0` — 금속판, 슐리렌 무늬
  - 종이 화이트 `#ECEAE4` — 건축 모형, 라벨, 실내
  - 해수 그레이블루 `#3E5A66` — 심층수 쪽 통로(아주 옅게)
  - 체온 앰버 `#C9894A` — **열을 나타내는 유일한 따뜻한 색**, 슐리렌 무늬 끝에 아주 옅게만
- **질감**: 35mm 필름 그레인 약하게, 하이라이트 헐레이션 약하게, 채도 낮게. 쨍한 디지털 블루 금지.
- **절대 금지**: 파란 물이 판을 통과하는 장면 / 두 통로가 합쳐지는 장면 / 얼음·서리·김 / 홀로그램·미래 도시·UI 인포그래픽 / 생성된 글자(모든 글자는 편집에서 삽입) / 실존 제품 라벨·로고 무단 노출.

---

## 3. 내레이션 v2

(차분한 단일 화자, 문장 사이 0.5~1초 여백. 실제 녹음 후 컷 길이 재조정)

```
깊은 바다의 물을, 우리는 마셔왔습니다.
빛이 닿지 않는 곳, 그 물은 일 년 내내 차갑습니다.
그 차가움을, 쓸 수 있다면.

바닷물은 바다의 길로.
건물의 물은 건물의 길로.
그 사이, 얇은 금속판 한 장.
물은 섞이지 않고, 열만 건너갑니다.

식은 물이 돌아와, 방의 열을 데려갑니다.
바다는 바다로 돌아가고,

바다는 밖에. 가능성은 안으로.
고성 해양심층수.
```

- 초안의 엔딩 카피("바다는 밖에. 가능성은 안으로.")는 좋아서 유지.
- "물은 섞이지 않고, 열만 건너갑니다"가 이 영상의 한 문장. 슐리렌 장면과 정확히 맞물리게 배치.
- 수치·효과 주장 없음. "~할 수 있다면"으로 제안형 화법 유지.

---

## 4. 장면 구성 — 50초 / 10컷

전체 구조는 **수미상관 + U자 하강·상승**: 물 한 잔 → 바다 아래로 하강 → (리빌) 실험대 위 모형 → 핵심 원리 → 모형 방 → 실제 방의 물 한 잔.

| 컷 · 시간 | 화면 / 카메라 | 내레이션 · 소리 | 라벨(편집 삽입) | 목적 |
|---|---|---|---|---|
| **C01** 0:00–0:05 | **극접사.** 창가 탁자 위 유리잔 표면의 결로 한 방울. 방울 안에 창밖 바다가 거꾸로 맺혀 있음. 방울이 천천히 흘러내림. 고정. | N1 "깊은 바다의 물을, 우리는 마셔왔습니다." / 여름 실내 룸톤, 먼 파도 | — | 첫 3초 훅. 차가움을 '결로'로 정직하게 표현(얼음·서리 아님). 브랜드의 본업(마시는 물)에서 출발 |
| **C02** 0:05–0:09 | **오버-언더(반수중) 샷.** 수면이 화면을 가로로 가르고, 위는 고성 바다의 밝은 하늘, 아래는 푸른 수중. 카메라가 천천히 수면 아래로 가라앉음. | N2 "빛이 닿지 않는 곳," / 파도 소리가 수면 아래에서 먹먹하게 바뀜 | — | 실제 렌즈 기법이라 분할 화면이 아님. 일상 → 심해로 넘어가는 문턱 |
| **C03** 0:09–0:14 | **하강.** 빛이 점점 사라지고, 검은 물속에 마린 스노우(부유 입자)가 천천히 위로 흐름(카메라가 내려가므로). 마지막엔 거의 암흑. | N2 "그 물은 일 년 내내 차갑습니다." / 저역 수압음, 음악 지속음 시작 | — | 깊이를 숫자 없이 감각으로 |
| **C04** 0:14–0:20 | **★ 디오라마 리빌.** 암흑 속 입자 → 카메라가 계속 물러나면 그것이 **검은 실험대 위 키 큰 유리 기둥 속의 물**이었음이 드러남. 와이드 타블로: 유리 기둥(심층수) – 가는 관 – 티타늄 열교환 모형 – 순환관 – 흰 건축 모형 방. 좌우 대칭에 가깝게. | N3 "그 차가움을, 쓸 수 있다면." / 실내 실험실 정적, 미세한 펌프 소리 | 기둥 옆: `표본 01 · 동해 심층수` / 하단 작게: `고성 해양심층수 냉열 활용 · 개념 모형` | 시그니처 장면. 연출만으로 '개념 영상'임을 선언. 시스템 전체를 한 화면에 |
| **C05** 0:20–0:25 | 열교환 모형으로 느린 푸시인. 투명한 두 통로가 티타늄 판을 사이에 두고 나란히. 왼쪽(심층수, 아주 옅은 그레이블루)은 위→아래, 오른쪽(건물 물, 투명)은 아래→위로 **서로 반대 방향**으로 흐름. 각 흐름은 자기 통로 안에만 머묾. | N4 "바닷물은 바다의 길로. 건물의 물은 건물의 길로." / 두 가지 다른 물소리(좌우 스테레오 분리) | `심층수` / `건물 순환수` 작은 라벨 | 두 물길을 먼저 구분시킴. 반대 방향 흐름(대향류)은 실제 열교환기 구조와도 맞음 |
| **C06** 0:25–0:33 | **★ 핵심. 슐리렌 고정 샷 8초.** 화면은 은회색 단색. 가운데 수직의 티타늄 판. 오른쪽 물속에서 아지랑이 같은 굴절 무늬가 판으로 모여, 판을 지나 왼쪽 흐름 속으로 흩어져 사라짐. 무늬 끝에만 아주 옅은 앰버. **물 입자·색은 판을 건너지 않음.** | N5 "그 사이, 얇은 금속판 한 장." … (1초 침묵) … "물은 섞이지 않고, 열만 건너갑니다." / **음악 완전히 빠짐**, 흐름 소리와 금속의 미세한 울림만 | — | 이 영상의 반전이자 존재 이유. 판독이 화려함보다 우선 |
| **C07** 0:33–0:38 | 순환관을 따라 흰 건축 모형 방으로 이동. 모형 방 천장의 작은 팬코일 아래에서 **실 한 가닥(또는 아주 얇은 커튼)**이 바람에 흔들림. | N6 "식은 물이 돌아와, 방의 열을 데려갑니다." / 작은 팬 소리 | — | 방을 식히는 단계까지 인과 완성. 공기 흐름을 '흔들리는 커튼'으로 보여줌(C01·C09의 커튼과 연결) |
| **C08** 0:38–0:42 | C04와 **같은 와이드 타블로**. 이번엔 열교환 모형을 지난 심층수 쪽 관이 유리 기둥으로 다시 이어지는 배출 경로에 시선이 감. 카메라 아주 느리게 물러남. | N7 "바다는 바다로 돌아가고," / 지속음 다시 들어옴 | — | 친환경 주제에서 나올 "그 물은 어디로?"에 대한 답. 전체 시스템 재확인 |
| **C09** 0:42–0:46 | **★ 모형 → 실재 매치컷.** 흰 모형 방의 창(종이 질감) → 같은 구도의 실제 방 창. 같은 커튼이 같은 방향으로 흔들림. 탁자 위 C01의 물 한 잔. | N8 "바다는 밖에. 가능성은 안으로." / 실내 룸톤 + 먼 파도 | — | 개념이 일상이 되는 순간. 엔딩 카피의 의미를 화면이 증명 |
| **C10** 0:46–0:50 | 물 한 잔 쪽으로 아주 느린 푸시인 후 심해 잉크색으로 페이드. 브랜드 타이포. | N9 "고성 해양심층수." / 마지막 물방울 소리 하나 | 중앙: `고성 해양심층수` / 그 아래 얇게: `차가움도 자원이 됩니다` | 브랜드 각인. 면책 문구는 여기 넣지 않음(C04에서 이미 처리) |

> 면책 처리 기준: C04 라벨로 충분하다고 판단하지만, 심사 리스크를 줄이고 싶다면 C10 최하단에 8pt 크기로 `냉열 활용 개념 영상`만 한 줄 추가. '아님'이라는 부정어는 쓰지 않음.

---

## 5. Google Flow 제작 파이프라인

### 원칙
- **모든 화면은 Flow 안에서 생성**(Flow 이미지 생성으로 키프레임 → Frames to Video / Ingredients to Video → 필요 시 Extend).
- 글자(라벨·브랜드명)는 Veo가 한글을 깨뜨리므로 **편집 단계에서만** 삽입.
- Veo 생성 오디오는 앰비언스 참고용. 최종 사운드는 내레이션 + 앰비언스를 편집에서 믹스.
- 최종 출력 1920×1080, 24fps. Flow에서 1080p 업스케일 후 내려받기.

### 생성 순서 (가장 위험한 것부터)
1. **C06 슐리렌 판** — 키프레임 5~10장 뽑아 '물이 판을 건너는 것처럼 보이지 않는' 1장 확정
2. **C04 / C08 와이드 타블로** — 같은 키프레임 1장 공유 (실험대 세트의 기준 이미지 = 이후 모든 모형 컷의 Ingredient)
3. **C05 열교환 모형 근접** — C04 키프레임을 Ingredient로
4. **C07 모형 방** → **C09 실제 방** (같은 구도로 두 장을 짝지어 생성)
5. **C01 결로 접사**, **C02 오버-언더**, **C03 하강** — 일반적인 장면이라 마지막
6. **C03 끝 프레임 = C04 첫 프레임**이 되도록 Frames to Video로 리빌 연결 (실패 시 대안은 §6)

### 공통 스타일 블록 (모든 프롬프트 앞에 붙임)
```
STYLE LOCK: quiet scientific still-life cinematography, museum specimen aesthetic,
matte black lab bench, single soft side key light, deep negative space, near-symmetrical framing,
100mm macro lens feel, shallow depth of field, subtle 35mm film grain, gentle halation,
low saturation, colors limited to deep ink navy, titanium silver, paper white,
faint grey-blue for seawater, a faint amber only for heat.
Locked-off or extremely slow motion-control camera, one camera move per shot.
No text, no letters, no logos, no holograms, no UI graphics, no ice, no frost, no steam.
```

### 컷별 프롬프트 초안 (영문, Flow 입력용)

**C06 — 슐리렌 판 (최우선)**
```
[STYLE LOCK]
Schlieren photography of a tabletop glass heat-exchanger model, locked-off frame, 8 seconds.
Monochrome silver-grey field. A single thin vertical titanium plate divides the frame in the center.
Clear water flows downward on the left side of the plate and upward on the right side, each flow staying
strictly within its own glass channel. From the right-side water, delicate refractive heat-shimmer
striations gather toward the plate, appear on the other side and dissolve into the left-side flow.
Only the shimmer pattern crosses the plate; no water, no particles, no color passes through the plate.
The plate is solid, unbroken and opaque. Tips of the shimmer carry a barely visible warm amber tint.
Calm, precise, scientific.
```
검수 포인트: 판에 구멍·틈이 보이면 탈락 / 입자가 판을 통과하면 탈락 / 좌우 흐름 방향이 섞이면 탈락.
반복 실패 시: Flow 이미지로 정지 키프레임을 확정 → Frames to Video에 **같은 프레임을 시작·끝으로** 넣고 "only subtle shimmer motion"으로 움직임을 최소화.

**C04 — 디오라마 리빌 와이드 (C08 공용)**
```
[STYLE LOCK]
Wide tableau of a minimalist conceptual model on a matte black lab bench, museum display style.
From left to right: a tall cylindrical glass column filled with dark deep-sea water with tiny suspended
particles; a thin transparent tube leading from its base to a compact rectangular heat-exchanger model
made of clear glass and brushed titanium plates; a second separate closed loop of thin transparent tube
leading from the heat exchanger to a small white paper architectural model of a room with one window
and a thin curtain. The two tube loops never connect to each other. Soft side light, dark background,
generous negative space, near-symmetrical composition. Camera slowly pulls back.
```

**C03→C04 리빌 연결 (Frames to Video)**
- 시작 프레임: C03 마지막 프레임(암흑 + 입자)
- 끝 프레임: C04 키프레임을 크게 확대해 유리 기둥 내부만 보이게 자른 이미지 → 이어서 C04 본 클립
```
Continuous camera pull-back: what looked like the open deep ocean is revealed to be the inside of a
tall glass column standing on a black lab bench. Seamless, slow, no cut.
```

**C05 — 대향류 두 통로**
```
[STYLE LOCK] Use the heat-exchanger from the reference image.
Slow push-in on two parallel transparent glass channels separated by one titanium plate.
Left channel: faint grey-blue seawater flowing downward. Right channel: clear water flowing upward.
Each flow stays inside its own channel. Fine particles reveal the flow direction. No mixing.
```

**C07 — 모형 방**
```
[STYLE LOCK] Use the white paper room model from the reference image.
Close view inside the small white architectural model of a room. A tiny ceiling fan-coil unit;
below it a thin curtain at the paper window sways gently in a cool breeze. Paper and matte textures.
```

**C09 — 모형 → 실재 (짝 생성)**
- 먼저 실제 방 키프레임 생성 → 같은 구도를 지시해 모형 방 키프레임 생성(Ingredient로 실제 방 이미지 사용)
```
[REAL] Calm minimal room facing the East Sea in Korea, summer afternoon, soft north light,
thin white curtain gently moving, a glass of water with condensation on a pale wooden table by the window,
calm sea outside. Locked-off, centered window, same composition as reference.
[MODEL] The exact same composition rebuilt as a white paper architectural model: paper walls,
paper window frame, thin fabric curtain, tiny glass on a tiny table. Studio light. Locked-off.
```
편집에서 커튼 움직임 위상에 맞춰 컷(같은 방향으로 흔들리는 프레임에서 붙이기).

**C01 — 결로 접사**
```
[STYLE LOCK, but warm natural daylight instead of lab light]
Extreme macro of a single condensation droplet on the side of a glass of cold water on a windowsill.
Inside the droplet, a tiny inverted refracted image of the window and the calm sea. The droplet slowly
slides down the glass. No ice, no frost, no steam. Locked-off.
```

**C02 — 오버-언더**
```
Split-level over-under shot with a dome port at the calm surface of the East Sea, Korea, clear summer day.
The waterline cuts the frame horizontally: soft sky and coastline above, clear blue water below.
The camera slowly sinks until fully underwater. Natural, documentary, low saturation.
```

**C03 — 하강**
```
Slow continuous descent into the deep ocean. Light fades from blue to near-black.
Marine snow particles drift slowly upward across the frame. Calm, silent, no animals, no ice.
```

---

## 6. 리스크와 대안

| 리스크 | 신호 | 대안 |
|---|---|---|
| 슐리렌을 Veo가 이해 못함 | 무지개색 사이키델릭, 연기처럼 보임 | 'schlieren' 대신 "heat haze shimmer in water, shadowgraph, monochrome" 위주로 서술. 그래도 실패 시 C06을 정지 키프레임 + 최소 모션으로 |
| 리빌 연결이 어색 | 기둥이 갑자기 나타남 | 심해 암흑에서 **암전 매치컷**(검은 화면 → 같은 위치의 입자 → 기둥)으로 끊어 붙임 |
| 모형 일관성 붕괴 | 관이 서로 연결됨, 모형 개수 변화 | C04 키프레임을 모든 모형 컷의 Ingredient로 고정. 관 연결 오류 컷은 무조건 탈락 |
| 모형 방 ↔ 실제 방 구도 불일치 | 창 위치가 다름 | 실제 방을 먼저 확정하고 모형을 실제에 맞춤(반대 순서 금지) |
| 50초 초과 | 내레이션 녹음 후 길어짐 | C08을 삭제해도 서사가 성립(배출 문장은 C07 끝으로 이동) → 46초 |

---

## 7. 원본 제출물 관리 (심사 제외 방지)

```
goseong-dsw/
  01_keyframes/   C01~C10 확정 키프레임 (Flow 생성 원본)
  02_clips/       Flow 원본 MP4 (재생성 포함, 파일명에 컷·라운드 표기: C06_R3_take2.mp4)
  03_prompts.md   컷별 최종 프롬프트 + 사용 기능(Frames/Ingredients/Extend) 기록
  04_audio/       내레이션 원본, 앰비언스
  05_edit/        편집 프로젝트 파일, 최종 MP4
```
Flow 프로젝트 자체도 삭제하지 말고 유지(생성 이력 증빙).

---

## 8. D-15 일정 (10/4 → 10/19 마감)

| 날짜 | 작업 |
|---|---|
| 10/4–5 | 공식 요강 PDF로 심사기준·원본 제출 형식·AI 도구 표기 의무 확인. C06 키프레임 확정 |
| 10/6–7 | C04/C08 타블로 확정 → C05 |
| 10/8–9 | C07·C09 짝 생성, 매치컷 테스트 |
| 10/10–11 | C01·C02·C03, 리빌 연결 |
| 10/12 | 내레이션 녹음(또는 AI 음성) → 가편집, 길이 조정 |
| 10/13–14 | 실패 컷 재생성, 사운드 믹스, 라벨·타이포 |
| 10/15 | 최종본 + 원본 파일 패키징, 지인 2~3명에게 "물이 판을 건너는 것처럼 보이는지" 블라인드 확인 |
| 10/16 | **제출** (마감 3일 전 여유 확보) |

---

### 참고 자료
- 공모 요강 요약: [뉴뉴스 보도](https://www.nnewss.com/news/articleView.html?idxno=6937), [콘테스트코리아](https://www.contestkorea.com)
- 해수 냉방 구조: Makai Ocean Engineering 기술자료(초안 인용)
- 동해 중층수 수온: [koreascience](https://koreascience.kr/article/JAKO200744947970584.pdf)
- 해외 트렌드 참고: [Envato — Motion Design Trends 2026](https://elements.envato.com/learn/motion-design-trends), [Luma — Cinematic AI Video Prompts](https://lumalabs.ai/news/cinematic-ai-video-prompts), [Versely — 30 AI Video Trends 2026](https://www.versely.studio/blog/30-ai-video-trends-to-watch-2026), [Awakened Films — Video Marketing Trends 2026](https://awakenedfilms.com/video-marketing-trends-for-2026/)
