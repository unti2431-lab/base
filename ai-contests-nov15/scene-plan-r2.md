# 11월 중순 마감 AI영상 공모전 3편 — 장면 구성 R2

> R1(2026-10-07 DRAFT) 재검토 → 공모전별 톤앤매너 재설정 → 해외 연출 문법 적용 → 장면 전면 재구성
> 생성 파이프라인: **Google Flow 단독**(키프레임 이미지 + 영상 생성 모두 Flow 안에서). 편집·자막·사운드 믹스만 편집기에서.
> 상태: DRAFT. 키프레임·클립·음성은 아직 없음.

---

## 0. R1 재검토 — 무엇을 유지하고 무엇을 바꾸나

### 세 작품 공통으로 유지
- 과장 금지·사실 범위 구분·AI 활용 기록 템플릿·제출 게이트(R1 §04, §05)는 그대로 쓴다. R2는 **장면·룩·생성 전략**만 다시 짠다.
- 우선순위(서울 → Meta → 제주 조건부)와 내부 제출 목표(11/8 · 11/13 · 11/10)도 유지.

### R1의 구조적 약점 (세 작품 공통)

| # | 문제 | 왜 문제인가 | R2 해결 |
|---|---|---|---|
| 1 | **룩이 '설명'만 있고 '규칙'이 없음** | "따뜻한 빛과 차가운 원경" 수준이라 컷마다 Flow가 다른 영화를 만든다 | 작품별 **LOOK LOCK 블록**(영문)을 모든 프롬프트 앞에 고정 |
| 2 | **AI가 가장 못 하는 장면이 핵심 장면** | 서울 S05 색소폰 운지·입술 / Meta 다수의 한국어 대사 립싱크 / 제주 블레이드·설비 일관성 | 핵심 장면을 **AI가 잘 하는 구도로 재설계**(뒷모습 리버스 앵글, 화면 밖 대사, 정지 와이드) |
| 3 | **연출 장치가 국내 공모전 평균 문법** | 돌리아웃·야경·디오라마·매치컷은 이미 많이 본 것. 심사 항목 '영상미·연출의도'에서 차별화 약함 | 작품마다 **형식 자체가 의미가 되는 장치 1개**를 중심에 둠(아래 §0-2) |
| 4 | **도구가 섞여 있음** (imagegen, Flow/Omni, CapCut…) | 도구가 바뀔 때마다 질감·색이 달라져 일관성이 무너짐 | 이미지·영상 생성은 Flow 안에서만. 기준 이미지 = Flow Ingredients로 재사용 |

### 작품별 핵심 수정

| 작품 | R1 문제 | R2 |
|---|---|---|
| 서울 | ① 공연 장소가 '공연 공간'인데 '지나던 사람'이 박수 → 실내 공연장인지 거리인지 모호 ② 대표 무빙(S05)이 색소폰 벨 매크로 → 악기 형상·운지가 가장 깨지는 구도 ③ **R1에 서울 공모 주제 문구 자체가 적혀 있지 않음** | ① 해방촌식 **옥상 오픈마이크**(가상)로 확정 — 지나가던 사람이 멈출 수 있는 개방 공간 + 남산 방향 원경이 자연스러움 ② 대표 무빙을 **등 뒤 리버스 앵글**로 바꿔 악기는 실루엣만, 화면은 그가 보는 도시와 관객 ③ 주제 문구를 공식 공고에서 다시 확인해 §1 첫 줄에 기입(게이트) |
| Meta | ① 대사 13줄 중 화면 안 립싱크가 많음 ② 'AI로 상상했다'가 대사로만 존재 → AI 활용(30%)·책임(20%)이 화면으로 증명되지 않음 ③ 디오라마가 그냥 예쁜 삽입 장면 | ① 대사는 **뒷모습·손·화면 밖**으로 처리 ② 딸이 AI 이미지를 **출력해 오려 종이극장을 만들고**, 엄마가 틀린 부분을 **빨간 색연필로 고친다** → '사람이 검증·수정하는 AI'가 서사 자체가 됨 ③ 앨범 속 **엄마의 그림자**를 첫 장면에 심고 상상 장면에서 회수 |
| 제주 | ① 내레이션이 거의 빈틈없음 ② "낮에 만든 전기 일부를 저장" — 바람은 밤에도 불어 풍력에 '낮'은 부정확 ③ J11 아이의 관계가 불명확 | ① 내레이션 9줄 → 7줄, 무음 구간 2곳 ② "남는 시간의 전기를, 필요한 시간으로"로 수정 ③ **조카**(이모 호칭)로 확정 — 가족 관계 오독 방지 |

### 0-2. 2026 해외 연출 흐름에서 가져온 것

국내 공공·공모전 AI 영상의 평균 문법은 **하이키·고채도·드론 부감·빠른 컷·웅장한 음악·큰 자막·화려한 모핑**이다. 2026년 해외 광고·단편 쪽 트렌드 리포트들은 반대로 **절제("Keep It Stupid Cinematic"), 아날로그 질감(16mm·VHS·플래시), 하나의 시각 세계 안의 여러 프레임, 진짜처럼 느껴지는 인간 이야기**를 꼽고, AI 콘텐츠 범람에 대한 반작용으로 **손으로 만든 듯한 물성(tactile)**이 차별화 요소로 언급된다(출처 §5. 대부분 업계 리포트·블로그라 방향성 참고로만 사용).

이를 세 작품에 하나씩 배분했다. 이름은 이 문서에서 붙인 것이며 업계 표준 용어가 아니다.

| 작품 | 중심 장치 | 해외에서의 쓰임 | 국내 공모전에서 드문 이유 | 이 작품에서의 의미 |
|---|---|---|---|---|
| 서울 | **화면비 서사(Aspect-Ratio Shift)** — 낮 4:3 → 첫 음에 16:9로 열림 | 장편·뮤직비디오·브랜드 필름에서 '해방/전환'의 순간에 사용 | 규격(16:9)을 꽉 채워야 한다는 관성, 검은 여백을 실수로 볼까 하는 우려 | **필러박스 = 셔터.** 낮에 내려간 셔터가, 밤의 첫 음에 화면 양옆에서 올라간다 |
| Meta | **플래시 아카이브 + 종이극장** — 2000년대 콤팩트카메라 직광 플래시·날짜 각인 / AI 출력물을 손으로 오려 만든 토이 시어터 | 직광 플래시·Y2K 디지털 질감은 해외 패션·광고에서 강세. AI 결과물을 물리적 공예로 옮기는 'tactile AI'는 AI 반작용 흐름 | AI 공모전은 AI 결과를 '매끈한 실사'로 보여주려는 경향 | 상상(종이)과 기억(사진)과 현재(실사)를 **질감으로 구분** → 책임 있는 AI 활용을 화면으로 증명 |
| 제주 | **근미래 관찰 다큐(Near-Future Vérité)** + **현무암 숨구멍 프레임** | 미래 기술을 배경의 평범한 일상으로 두는 스페큘러티브 다큐 문법, 북유럽식 정지 와이드 | 미래 = 홀로그램·드론·미래도시라는 공식 | 기술이 아니라 **섬의 시간이 주인공**. 돌담 구멍 프레임이 과거·현재·미래를 같은 시점으로 묶음 |

공통 원칙: **한 컷 한 움직임 / 광원은 화면 안에 보이는 것만(practical light) / 소리가 먼저 오고 화면이 따라옴(J-cut) / 생성된 글자 0개(모든 글자는 편집 삽입)**.

---

# 1. 서울 29초영화제 — 《밤에는, 신인》 R2

## 1-1. 작품 계약 (R1 유지 + 수정)
- **[게이트] 공모 주제 문구:** _공식 공고에서 원문 확인 후 기입._ R1은 주제를 '서울의 밤'으로 해석해 설계했으나 문서에 원문이 없다. 원문이 다르면 S08 자막과 §1-6 설명을 먼저 고친다.
- 29.000초 / 1920×1080 / 24fps / 696프레임 / 8컷. 제목은 본편 마지막 장면 위에 얹는다(R1 유지).
- 화면비 서사: 0~12.5초는 **1440×1080(4:3) 필러박스**, 12.5초에 16:9로 열림. 파일 자체는 1920×1080 그대로. 필러박스 사용이 규격 위반이 아닌지 접수 화면에서 확인.
- 한 줄: 낮에는 철물점 사장인 50대 남자가 서울의 밤, 옥상 오픈마이크에서 첫 무대에 서고 하루의 첫 박수를 받는다.
- 공간: 철물점(셔터·형광등) → 경사 골목 계단 → **가상의 옥상 오픈마이크**(전구 줄, 의자 대여섯 개, 남산 방향 원경). 실존 장소·행사로 표현하지 않는다.

## 1-2. 톤앤매너 — "셔터 프레임"

| | 낮 (S01–S04) | 밤 (S05–S08) |
|---|---|---|
| 화면비 | 4:3, 좌우 검은 셔터 | 16:9 전체 |
| 빛 | 천장 형광등, 녹청색 기운, 평평함 | 텅스텐 전구 줄의 앰버 + 먼 도시의 차가운 청회색 |
| 카메라 | 완전 고정. 인물은 프레임 안에 갇힌 느낌 | 단 한 번의 느린 후퇴·상승(S05) 후 다시 고정 |
| 질감 | 16mm 그레인 약하게, 하이라이트 헐레이션 없음 | 16mm 그레인 + **전구 주변 헐레이션** |
| 소리 | 금속음·형광등 험·발소리. 음악 없음 | 첫 음 이후 색소폰 + 현장음. 박수 1~2명 |

국내 29초 출품작에서 흔한 **빠른 컷·자막 개그·반전 펀치라인**을 버리고, 29초를 **한 번의 '열림'**으로 설계한다. 심사 항목(주제부합성·연출의도·작품성·영상미·임팩트 각 20%) 중 '연출의도'와 '영상미'를 화면비 하나로 동시에 설명할 수 있다.

**팔레트:** 형광 녹청 `#9FB3A8` / 셔터 강철 `#5B6064` / 텅스텐 앰버 `#D9964B` / 서울 원경 청회 `#2E3A4A` / 밤 검정은 완전한 검정이 아닌 `#0F1216`

## 1-3. 장면 구성 — 29초 / 8컷

| 컷 | 시간 / 프레임 | 화면비 | 화면 · 카메라 | 소리 · VO |
|---|---|---|---|---|
| **S01** | 0.0–3.0 / 1–72 | 4:3 | 철물점 외부 정면, 고정. 셔터가 마지막 구간을 내려오며 안쪽 형광등 빛이 **가로 한 줄**로 가늘어지다 사라진다. 손은 화면에 없음 | 셔터 마찰음 → 바닥 닿는 금속음. VO "매일, 문을 닫습니다." |
| **S02** | 3.0–6.0 / 73–144 | 4:3 | 가게 안, 측면 출입문 쪽 중간 구도. 앞치마가 이미 못에 걸려 있고, 남자가 검은 악기 케이스를 든 채 형광등 스위치를 끈다 → 화면이 어두워짐 | VO "낮에는 사장님." 스위치 딸깍. **암전 위로 먼 곳의 조율음이 먼저 들림(J-cut)** |
| **S03** | 6.0–9.0 / 145–216 | 4:3 | 경사진 서울 골목 계단을 오르는 뒷모습, 고정 로우앵글. 창마다 다른 색의 생활 불빛. 간판 글자는 판독 불가 수준으로 흐림 | 발소리, 조율음이 점점 가까워짐 |
| **S04** | 9.0–12.5 / 217–300 | 4:3 | 옥상 무대 옆, 순서를 기다리는 옆얼굴 클로즈업. 전구 줄이 배경에서 둥근 보케. **크게 한 번 들이쉬는 숨** | VO "밤에는, 신인입니다." → 0.5초 완전 무음 |
| **S05 ★** | 12.5–19.0 / 301–456 | **4:3→16:9** | **첫 음과 동시에 좌우 셔터가 12프레임 동안 바깥으로 열림.** 카메라는 남자 등 뒤 어깨 높이에서 시작해 천천히 뒤로 물러나며 약간 상승 → 연주하는 그의 실루엣, 의자 몇 개의 관객, 그 너머 남산 방향 서울 야경이 한 화면에 | 새로 만든 짧은 색소폰 선율. 호흡음·키 소리 약하게 |
| **S06** | 19.0–22.5 / 457–540 | 16:9 | 리버스: 옥상 난간 쪽, 퇴근길 헬멧을 손에 든 사람이 멈춰 서 있다. 중간 거리, 고정. 천천히 손을 모아 두 번 박수 | 선율의 마지막 음 → 실제 공간 크기의 박수 1~2명 |
| **S07** | 22.5–26.0 / 541–624 | 16:9 | **처음으로 남자의 정면.** 악기를 내리고 웃음을 참다 작게 웃는다. 중간 클로즈업, 고정 | VO "오늘의 첫 박수는, 밤에 왔습니다." |
| **S08** | 26.0–29.0 / 625–696 | 16:9 | 대칭 와이드 타블로: 무대의 남자 / 난간의 사람 / 서울의 밤. 전구 줄이 화면 상단을 가로지름 | 잔향. 자막(편집) "서울의 밤은 계속된다." + 작품명 작게 |

**설계 포인트**
- 정면 얼굴은 S07에서 처음 공개 → 29초 안에 '보상'의 순간이 하나 더 생김.
- 색소폰은 S05에서 **등 뒤 실루엣**, S07에서는 **내려놓은 상태** → 운지·입술 접촉 생성이 필요 없음. R1의 최대 리스크 제거.
- S06의 헬멧 든 사람 = 또 다른 '밤에 일하는 사람'. 대사 없이 서울의 밤을 사는 사람들끼리의 연대로 읽힘.

## 1-4. Flow 제작

**Ingredients (먼저 확정)**
1. `SEOUL_MAN` — 50대 초반 한국 남성, 회색 작업 셔츠, 짧은 희끗한 머리. 정면·측면·뒷모습 3장
2. `SEOUL_CASE` — 낡은 검은 색소폰 케이스
3. `SEOUL_ROOF` — 옥상 오픈마이크 와이드(전구 줄, 접이식 의자, 낮은 난간, 남산 방향 원경). **S05 끝 프레임 = S08 기준 이미지**

**LOOK LOCK**
```
LOOK LOCK: restrained naturalistic short-film cinematography, 16mm film emulation, fine grain,
practical light sources only (fluorescent tubes by day, tungsten string bulbs by night),
locked-off camera unless stated, one camera move per shot, no drone, no handheld shake,
muted palette: fluorescent green-grey, shutter steel, tungsten amber, distant blue-grey city,
blacks lifted slightly, gentle halation around bulbs only at night.
Keep the main subject inside the central 4:3 area of the frame.
No readable text, no signage letters, no logos, no crowds.
```
> "central 4:3 area" 지시는 낮 컷(S01–S04)에만 필수. 편집에서 좌우를 잘라도 인물이 안 잘리게.

**S05 대표 무빙 — Frames to Video (첫 프레임 + 끝 프레임)**
```
[LOOK LOCK] Use SEOUL_MAN and SEOUL_ROOF.
Over-the-shoulder from directly behind a middle-aged man in a grey work shirt playing a saxophone
on a small rooftop open-mic stage at night. The saxophone is mostly hidden by his body; only the bell
edge is visible as a silhouette. Camera slowly pulls back and rises slightly, revealing a few folding
chairs with five or six listeners, tungsten string bulbs overhead, and beyond a low railing the
night skyline of Seoul with Namsan in the distance. Gentle breathing motion in his shoulders.
Calm, intimate, 6 seconds.
```
- 첫 프레임: 등 + 어깨 너머 흐린 전구 보케(타이트) / 끝 프레임: `SEOUL_ROOF` 와이드
- 실패 시: 고정 와이드 4초 + 등 클로즈업 2초로 분리(원테이크 고집 금지)
- 검수: 악기가 다른 악기로 변함 / 관객이 10명 이상 / 남산 방향 원경이 지형상 불가능한 배치 → 탈락

**S01 셔터**
```
[LOOK LOCK] Locked-off frontal view of a small Korean hardware store at dusk. A metal roller shutter
descends the last section; the cold fluorescent light from inside narrows to a thin horizontal line
under the shutter, then disappears. No people, no hands. 3 seconds.
```

**S06 리버스**
```
[LOOK LOCK] Use SEOUL_ROOF from the reverse angle. At the rooftop railing, a person in a plain jacket
holding a motorbike helmet in one hand has stopped to listen, seen at medium distance. They slowly
bring their hands together and clap twice. Tungsten bulbs, city haze behind. Locked-off.
```

**생성 순서:** S05 → S08(S05 끝 프레임 재사용) → S04 → S06 → S07 → S01 → S02 → S03

## 1-5. 편집·사운드
- 화면비 전환: 12.5초(301프레임) 첫 음 트랜지언트에 맞춰 좌우 바가 12프레임 동안 바깥으로 이동(이징: 처음 느리게). **셔터가 올라가는 금속음을 아주 작게 섞는다** → S01과 수미상관.
- J-cut 2곳: S02 암전 위 조율음 / S04 무음 0.5초 뒤 첫 음.
- 썸네일(575×323): S05 끝 프레임 — 실루엣 + 전구 + 야경. 글자 없이.

## 1-6. 제출 설명 R2
《밤에는, 신인》은 낮에는 철물점 사장인 중년 남성이 서울의 밤 작은 옥상 무대에서 처음 연주자가 되는 29초 영화입니다. 낮의 장면은 좁은 4:3 화면에, 밤의 첫 음부터는 넓은 16:9 화면에 담았습니다. 가게의 셔터가 내려가며 닫힌 화면이, 연주가 시작되는 순간 양옆으로 열리도록 설계해 퇴근이 하루의 끝이 아니라 또 다른 시작일 수 있음을 화면의 형식으로 보여주고자 했습니다. 화려한 야경 대신 한 사람의 첫 박수와 그 박수를 보낸 또 다른 밤의 사람에 집중했습니다.

## 1-7. 리스크

| 리스크 | 대안 |
|---|---|
| 필러박스가 '규격 미달'로 오해될 가능성 | 접수 안내 확인. 불안하면 4:3 구간을 **좌우 어둠(셔터 실물 그림자)**으로 연출해 화면 안에서 해결 |
| 남산 원경이 생성마다 달라짐 | `SEOUL_ROOF` 한 장을 끝까지 Ingredient로 고정. 원경이 무너지면 S08은 S05 끝 프레임 정지 + 미세 줌으로 대체 |
| 29초 초과 | S03을 2초로 줄임(발소리만 남김) |

---

# 2. Meta와 함께하는 AI 페스티벌 — 《사진 밖의 사람》 R2

## 2-1. 작품 계약 (R1 유지 + 수정)
- 약 90초 / 16:9 / 1920×1080 / 24fps — **형식별 제출 기준 미확인(R1 유보 그대로).** 규격 확인 전 본 생성 착수 금지.
- 창작 가족 단편. 실제 가족 이야기라고 주장하지 않는다.
- 인물: 딸(20대 후반), 엄마(50대 후반), 사진 속 어린 딸.
- 한 줄: 앨범에 엄마가 없다는 걸 발견한 딸이 엄마의 이야기를 AI 이미지로 그려 **종이극장**으로 만들고, 엄마가 그걸 **고쳐 주면서** 둘은 처음 듣는 이야기를 나눈다. 마지막엔 과거를 고치는 대신 오늘 함께 사진을 찍는다.

## 2-2. 톤앤매너 — "플래시 아카이브 + 종이극장"

심사 배점(기획·AI 활용 30 / 작품성 50 / 책임 있는 활용 20)을 **세 가지 질감**으로 대응한다. 관객은 질감만 보고도 무엇이 기록이고 무엇이 상상인지 구분할 수 있다.

| 층 | 무엇 | 룩 |
|---|---|---|
| **기억 (사진)** | 2000년대 앨범 사진 | 3:2 인화지 테두리, 콤팩트카메라 **직광 플래시**, 빨간 눈 없음, 약간의 노출 과다, 날짜 각인(편집 삽입) |
| **상상 (종이극장)** | 엄마의 이야기를 딸이 AI로 그리고, 출력해 오려 세운 토이 시어터 | 종이 결·가위 자국·연필선·접힌 경첩이 보이는 레이어. 책상 스탠드 한 개의 빛. 카메라가 그 안으로 들어가면 종이 인물이 살짝 움직임 |
| **현재 (실사)** | 오늘의 집 | 고레에다식 생활 실사: 낮은 카메라 높이, 문틀 너머로 보는 고정 구도, 오후 자연광, 35mm 질감. 클로즈업보다 '거리' |

**팔레트:** 인화지 화이트 `#F2EDE3` / 플래시 하이라이트 `#FFF8EC` / 종이 크래프트 `#C8B79A` / 엄마의 빨강(고깔) `#C2412F` — **이 빨강은 영화 전체에서 단 하나의 원색.** 종이극장에서 엄마가 색칠하는 순간 처음 등장하고, 마지막 사진에서 다시 나온다.

## 2-3. 장면 구성 — 약 90초 / 12구간

| 구간 | 시간 | 층 | 화면 · 행동 | 음성 · 소리 |
|---|---|---|---|---|
| **M01** | 0–7 | 기억 | 직광 플래시 사진 3장이 한 장씩 탁, 탁, 탁 놓인다(돌잔치 상 / 생일 / 해변). 어디에도 엄마는 없다. 세 번째 해변 사진에서 **모래 위로 길게 드리운 촬영자의 그림자**에서 멈춤 | 인화지 놓이는 소리. 딸 VO "우리 앨범엔 엄마가 없다. …그림자만 있다." |
| **M02** | 7–15 | 현재 | 거실 문틀 너머 낮은 고정 와이드. 식탁에서 앨범을 보는 딸, 안쪽 부엌에서 일하는 엄마(살아 있고 같은 공간에 있음을 분명히) | 딸(뒷모습) "엄마, 이때 어디 있었어?" 부엌 물소리 멈춤 |
| **M03** | 15–23 | 현재 | 인서트: 엄마의 손가락이 해변 사진의 그림자를 짚는다. 이어서 둘의 어깨 너머 투샷, 엄마의 작은 웃음(옆얼굴) | 엄마(화면 밖/옆얼굴) "여기. 이게 엄마야." |
| **M04** | 23–31 | 현재 | 밤, 딸의 책상 탑뷰. 출력된 AI 이미지, 가위, 테이프, 종이 무대 틀. 딸의 손이 종이 인물을 세운다. 화면 UI는 보이지 않음 | 가위 소리, 프린터 소리. 딸 VO "엄마한테 들은 얘기를 AI로 그려서, 오리고 세웠다." |
| **M05 ★** | 31–41 | 상상 | **종이극장 리빌.** 생일 사진과 같은 구도의 종이 무대 정면 → 카메라가 프로시니엄 안으로 들어가며 사진 '바깥' 레이어가 드러남: 카메라를 든 엄마가 아이를 웃기려 **흰 종이 고깔**을 쓰고 있다 | 엄마 "네가 하도 울어서… 내가 고깔을 썼지." 종이 스치는 소리 |
| **M06** | 41–50 | 현재 | 식탁에 옮겨 놓은 종이극장 앞, 둘. 엄마가 고개를 갸웃 "근데 그거, 빨간 거였어." **빨간 색연필로 종이 고깔을 칠한다.** 딸이 웃는다 | 색연필 사각거림. 딸 웃음 |
| **M07** | 50–60 | 상상 | 해변 종이극장. 아이는 마른 모래, 엄마는 사진을 찍다 운동화가 파도에 젖는다. **엄마의 그림자가 아이 쪽으로 길게 뻗음 → M01 그림자의 회수** | 엄마 "엄마 신발은 다 젖었고." 딸 "내 건 뽀송했고." 종이 파도 소리 |
| **M08** | 60–67 | 현재 | 문틀 너머 와이드. 엄마가 일어나 서랍에서 **M01을 찍은 그 낡은 콤팩트카메라**를 꺼낸다 | 딸 VO "사진 밖은 상상이었지만, 이야기는 처음 들었다." 엄마 "자, 엄마가 찍어 줄게." |
| **M09** | 67–74 | 현재 | 카메라 뒤로 가는 엄마 / 딸이 옆 빈 의자를 손바닥으로 두 번 두드린다(시선 편집) | 딸 "엄마. 거기 말고… 여기." |
| **M10** | 74–80 | 현재 | 책 더미 위에 올린 카메라. 셀프타이머 램프가 주황색으로 깜빡이기 시작. 망설이는 엄마의 발 | 엄마 "그럼 누가 찍어?" 딸 "오늘은 카메라가." 타이머 삐— 삐— |
| **M11** | 80–86 | 현재 | **카메라 POV(뷰파인더 프레이밍).** 나란히 앉은 둘. 엄마가 빨갛게 칠한 종이 고깔을 쓴다. 딸이 터지듯 웃는다. 타이머 간격이 빨라짐 | 삐삐삐삐 — 웃음 |
| **M12** | 86–90 | 기억(새) | **플래시.** 하얗게 번쩍 → 정지 → 직광 플래시 질감의 새 사진. 살짝 흔들렸지만 둘 다 웃고, 빨간 고깔. 날짜 각인(편집) | 셔터. 딸 VO "이번 사진엔, 엄마도 있다." 제목 + AI 고지 |

**구조 해설**
- **그림자 복선(M01→M07):** '엄마가 없다'를 사별 미끼로 쓰지 않고 "사실 처음부터 있었다"는 발견(Discovery)으로 바꿈.
- **AI 수정 장면(M06):** AI가 그린 이미지가 틀렸고, 사람이 고친다. 이 한 컷이 '책임 있는 활용'의 시연이자, 엄마가 처음으로 자기 기억을 주도하는 순간(Connection). 고깔의 빨강이 결말까지 이어짐(Entertainment).
- **카메라의 주인이 바뀜:** M01은 엄마가 찍은 사진, M12는 카메라가 찍은 사진. 같은 기계, 다른 자리.

**고지:** M05·M07 하단에 작게 `엄마의 이야기로 그린 장면` (편집). 결말: `등장인물과 사연은 창작입니다. 이미지·영상 생성에 Google Flow를 사용했습니다.` — 실제 사용 범위대로 수정.

## 2-4. Flow 제작

**Ingredients**
1. `MOM` 50대 후반 한국 여성 / `DAUGHTER` 20대 후반 한국 여성 / `KID` 5~7세 딸 — 각 정면·측면·뒷모습
2. `CAMERA` 2000년대 은색 콤팩트 디지털카메라(브랜드 로고 없음)
3. `PAPER_STAGE` 종이극장 틀(크래프트지, 경첩, 테이프)
4. `HOME` 거실·부엌 와이드(문틀 프레이밍)

**LOOK LOCK — 현재**
```
LOOK LOCK PRESENT: quiet Japanese-Korean domestic realism in the style of observational family drama,
low static camera height, framed through doorways, soft afternoon window light, 35mm film texture,
muted warm neutrals, unhurried, people seen at a distance more than in close-up.
No readable text, no logos, no screens with visible UI.
```
**LOOK LOCK — 상상(종이극장)**
```
LOOK LOCK PAPER: handmade toy theatre made of printed and hand-cut paper layers, visible scissor edges,
pencil lines, tape, folded hinges, kraft paper texture, lit by a single warm desk lamp, shallow depth
of field, gentle parallax between paper layers. Figures move only slightly like paper puppets.
Only one saturated color allowed: a red paper party hat when specified. No text.
```
**LOOK LOCK — 사진**
```
LOOK LOCK PHOTO: mid-2000s compact digital camera snapshot, harsh direct on-camera flash,
slightly overexposed foreground, dark falloff background, printed on 3:2 glossy photo paper with white border.
No date stamp, no text (added in edit).
```

**M05 종이극장 리빌 — Frames to Video**
```
[LOOK LOCK PAPER] Use PAPER_STAGE, MOM, KID.
Front view of a small paper toy theatre whose stage recreates a child's birthday snapshot.
The camera slowly pushes in through the paper proscenium; layers separate in parallax and reveal,
beyond the edge of the original photo, a paper cut-out mother holding a compact camera,
wearing a white paper party hat to make the child laugh. The paper child turns slightly toward her.
Warm desk-lamp light. 8 seconds.
```
- 첫 프레임: 생일 사진(PHOTO 룩)을 종이에 인쇄해 무대에 세운 정면 / 끝 프레임: 무대 안쪽 레이어 공개
- 실패 시: 정면 고정 3초 → 종이 테두리 인서트(가림 컷) → 내부 와이드 4초로 분리

**M06 빨간 색연필 — 이미지 편집 활용**
- 종이극장 키프레임에서 고깔만 Flow 편집(부분 수정/Insert 계열 기능)으로 흰색→빨강 버전 생성 → 두 키프레임을 Frames to Video 첫/끝으로. 손과 색연필은 별도 클로즈업 컷(손은 화면 가장자리에서 진입, 칠하는 동작 2초)
- 이 수정 과정 스크린샷을 **AI 활용 기록**에 그대로 첨부 → 제출 서류의 '인간 기여' 근거

**대사 처리 원칙**
- 화면 안 립싱크 0~2컷. 대사는 뒷모습·옆얼굴·손·화면 밖에서.
- Veo의 한국어 음성 생성은 **M02 한 컷으로 시험**. 발음·감정이 안 되면 대사는 녹음(또는 TTS)으로 교체. 어느 쪽이든 실제 사용 내역대로 기록.

**생성 순서:** 인물·카메라·종이틀 Ingredients → M05(리빌) → M06(수정) → M12(플래시) → M01 사진 3장 → M07 → 현재 실사 컷들

## 2-5. 제출 설명 R2
《사진 밖의 사람》은 가족 앨범에 엄마가 거의 없다는 발견에서 시작하는 창작 단편입니다. 딸은 엄마에게 들은 이야기를 생성형 AI로 그리고, 그 이미지를 직접 출력해 오려 작은 종이극장을 만듭니다. 엄마는 AI가 그린 장면을 보며 "그 고깔은 빨간색이었어"라고 고쳐 주고, 그 수정이 두 사람이 처음 나누는 대화가 됩니다. 기억은 사진의 질감으로, 상상은 종이의 질감으로, 현재는 실사로 구분해 AI가 만든 장면을 사실처럼 보이게 하지 않았습니다. 결말에서 딸은 과거 사진에 엄마를 합성하는 대신 오늘 함께 사진을 찍습니다. 기록하던 사람도 기록 안에 있어야 한다는 이야기입니다.

## 2-6. 리스크

| 리스크 | 대안 |
|---|---|
| 종이극장이 '그냥 CG 일러스트'처럼 보임 | 프롬프트에 가위 자국·테이프·경첩 반복. 책상 탑뷰(M04)에서 실제 물건임을 먼저 보여 줌 |
| 인물 일관성(엄마 얼굴) | 현재 컷은 거리 두기 원칙으로 얼굴 크기를 작게. 클로즈업은 M03 옆얼굴 1컷만 |
| 빨강이 다른 컷에 번짐 | 상상·현재 LOOK LOCK에 "no red objects" 추가, 고깔 컷에만 해제 |
| 90초 초과 | M04를 5초로 줄임(손 인서트 2컷) |

---

# 3. 5극3특 성장엔진 미래지도 — 《바람을 저축하는 사람들》 R2

## 3-1. 작품 계약 (R1 유지 + 수정)
- 제주 / 재생에너지 융복합시스템 / 90초 / 16:9 / 1920×1080 / 24fps / MP4 / 600MB 이하.
- 주인공: 30대 여성 에너지 기술자(제주 출신). 조카(8세 전후) 1명.
- 2035년은 창작상의 시간. 정책 달성·공식 일정으로 제시하지 않음(R1 유지).
- **표현 수정:** "낮에 만든 전기 일부를 저장" → **"남는 시간의 전기를, 필요한 시간으로"**. 풍력은 낮에만 발전하지 않으므로.
- R1 §5 금지 표현 목록 전부 유지.

## 3-2. 톤앤매너 — "근미래 관찰 다큐 + 현무암 숨구멍 프레임"

- **미래는 배경에 있다.** 하늘을 나는 차·홀로그램·미래도시 금지. 2035년의 제주는 지금의 돌담·억새·감귤밭 그대로이고, 새것은 설비와 사람들의 일뿐.
- **정지 와이드에 작은 사람.** 북유럽 다큐식으로 인물은 풍경 속에 작게. 클로즈업은 손과 표정 3컷 이내.
- **현무암 숨구멍 프레임(시그니처):** 제주 돌담의 구멍 사이로 바깥을 보는 프레임-인-프레임. **J01(과거)·J03(현재)·J12(내일)를 정확히 같은 구멍, 같은 렌즈로** 찍어 시간을 하나의 시점으로 묶는다.
- **바람을 보이게:** 바람 자체를 그래픽으로 그리지 않는다. 리본·억새·빨래·방풍림으로만. **노란 리본 하나**가 어린 시절 병 → 기술자의 작업 가방 → 창가의 병으로 이어지는 소품 연결선.
- **사운드:** 음악 대신 바람 녹음을 가공한 지속음(에올리언 하프 질감). 설비 장면에는 접촉 마이크 같은 낮은 험.

**팔레트:** 현무암 차콜 `#2B2A28` / 억새 은회 `#B9B3A3` / 제주 바다 청록(채도 낮게) `#4C6E6C` / 작업복 오프화이트 `#E6E2D8` / 리본 노랑 `#E2B13C`(유일한 원색) / 저녁 창 앰버 `#D49A5A`

## 3-3. 장면 구성 — 90초 / 12구간

| 구간 | 시간 | 화면 · 카메라 | 내레이션 · 소리 |
|---|---|---|---|
| **J01 ★** | 0–6 | **돌담 숨구멍 프레임.** 구멍 너머, 아이가 노란 리본을 묶은 열린 유리병을 바람 쪽으로 높이 든다. 얼굴은 부분 노출. 고정 | 바람. 성인 VO "어릴 땐, 바람을 병에 담으려 했습니다." |
| **J02** | 6–11 | 돌담 위에 놓인 닫힌 병. 병 속은 정지, 병 뒤 억새는 크게 흔들림(안/밖 대비). 고정 매크로 | VO "병 안엔, 조용한 공기만 남았죠." 바람 소리가 병 속처럼 먹먹해짐 |
| **J03** | 11–17 | **J01과 같은 구멍·같은 렌즈.** 안전모를 든 성인 기술자가 지나간다. 작업 가방에 **바랜 노란 리본**. 하드 매치컷 | 자막(편집) `2035, 제주 — 상상한 미래`. VO "지금도 바람을 잡지는 않습니다." |
| **J04** | 17–26 | 해안 정지 와이드: 천천히 도는 풍력 설비 몇 기, 해안도로 위 작은 인물. 이어서 타워 아래에서 올려다보는 그의 뒷모습 | VO "대신, 바람이 만든 전기를 모아 둡니다." |
| **J05** | 26–34 | 닫힌 에너지 저장 설비 외부 통로. 두 기술자가 안전 거리에서 태블릿으로 상태 확인(화면 내용은 안 보임). 측면 고정 | 낮은 험. VO "남는 시간의 전기를," |
| **J06** | 34–41 | 디테일: 닫힌 캐비닛, 케이블 트레이, 일정하게 켜진 작은 정상 표시등. 아주 느린 슬라이드 | VO "필요한 시간으로." |
| **J07** | 41–48 | **같은 위치의 시간 경과:** 설비 + 하늘이 낮 → 해질 무렵. 설비 형상은 고정 | **무음 구간.** 바람 지속음만 |
| **J08** | 48–57 | 해 질 녘 마을. 감귤 선별장 작업등, 빵집 전기 오븐 창, 버스정류장 조명이 **차례로** 켜진다(3컷, 각 3초) | VO "저녁이 필요한 곳에, 지역의 공급을 보탭니다." |
| **J09** | 57–65 | 교육실. 주인공과 신입 동료가 책상 위 교육용 소형 모형(작은 풍력 모형 + 배터리 모듈 모형)을 본다. 탁상 선풍기 바람에 모형 날개가 돌고 작은 LED가 켜짐 → 신입이 웃는다 | VO "설비를 돌보고, 기술을 배우고, 이 섬에서 새 일을 만드는 사람들." |
| **J10** | 65–74 | 블루아워 돌담길 정지 와이드. 억새 사이를 걸어가는 작은 인물 | **무음 구간 후** VO "제가 자란 섬에서, 제 일을 찾았습니다." |
| **J11** | 74–83 | 집 대문 앞. 조카가 빈 병을 들고 기다린다. 둘 사이 거리 1m, 같은 프레임. 포옹 없음 | 조카 "이모, 오늘도 바람 잡았어?" 주인공 "아니. 오늘 쓸 전기를 모아 왔지." |
| **J12 ★** | 83–90 | **다시 같은 돌담 숨구멍.** 너머로 불 켜진 집의 창, 창턱의 병, 병에 묶인 노란 리본이 바람에 흔들림. 고정 | VO "바람은 지나가도, 우리의 내일은 여기에." 자막 `제주 · 재생에너지 융복합시스템` |

**R1 대비 핵심 변화**
- 숨구멍 프레임 3회(J01·J03·J12)로 **"같은 자리, 다른 시간"** — 다른 지역으로 바꿀 수 없는 제주만의 시점.
- 노란 리본 1개가 30년을 잇는 소품. 물체 모핑 없이 연속성 확보(R1 원칙 유지).
- 발전 → 저장 → 필요한 시간 공급 → 마을의 저녁 → 교육·일자리의 인과는 R1과 동일. 내레이션만 줄이고 무음 2구간으로 판독 시간 확보.

## 3-4. Flow 제작

**Ingredients**
1. `TECH` 30대 한국 여성 기술자, 오프화이트 작업복, 흰 안전모 / `NIECE` 8세 전후 아이 / `KID_TECH` 같은 인물의 어린 시절(얼굴 부분 노출이라 유사성 요구 낮음)
2. `JAR` 노란 리본 묶인 유리병
3. `WALL_HOLE` **돌담 숨구멍 프레임 기준 이미지** — J01·J03·J12 공용. 구멍 모양·위치 절대 고정
4. `ESS` 저장 설비 외부 기준 이미지 — J05·J06·J07 파생
5. `TURBINE` 해안 풍력 와이드 — 블레이드 3개, 기수 고정

**LOOK LOCK**
```
LOOK LOCK: near-future observational documentary, Nordic-style static wide shots with small human figures,
natural overcast or golden-hour light, Jeju volcanic basalt walls, silver eulalia grass, low-saturation
sea teal, charcoal basalt, off-white workwear; the only saturated color is a small yellow ribbon.
Technology is quiet and ordinary, never spectacular. Locked-off camera unless stated, one move per shot.
No flying cars, no holograms, no futuristic skyline, no drones, no readable text, no logos.
```

**J01/J03/J12 숨구멍 3연작 — 같은 프레임에서 파생**
```
[LOOK LOCK] Use WALL_HOLE as the exact framing. Shot through an irregular gap in a Jeju black basalt
stone wall; the gap frames the scene beyond like a natural window, wall stones dark and slightly out
of focus in the foreground. Locked-off.
J01: beyond the gap, a young girl holds up an open glass jar with a yellow ribbon tied to it toward
     the wind; the ribbon flutters; face partly hidden.
J03: same gap, same lens; a woman in off-white workwear carrying a white hard hat walks past from
     left to right; a faded yellow ribbon is tied to her work bag.
J12: same gap, same lens, blue hour; beyond it a house window glows warm; on the windowsill
     a glass jar with a yellow ribbon moving in the wind.
```
- `WALL_HOLE` 이미지를 먼저 한 장 확정 → 세 컷 모두 그 이미지를 Ingredient 또는 첫 프레임으로. 구멍 윤곽이 달라지면 탈락.

**J07 시간 경과 — Frames to Video**
- `ESS` 낮 키프레임 → 같은 이미지에서 하늘·빛만 해질 무렵으로 바꾼 편집본 → 첫/끝 프레임
```
[LOOK LOCK] Locked-off. The same quiet energy storage facility as the light changes from midday
to dusk. The structure, doors, and cables stay exactly the same; only the sky and light change.
```

**J09 교육 모형**
```
[LOOK LOCK] Interior training room. Two technicians at a table look at a small desktop teaching
model: a miniature wind turbine and a small battery module model connected by a thin cable.
A desk fan turns on; the miniature blades spin and a tiny LED on the module lights up.
The younger technician smiles. Calm natural window light.
```

**생성 순서:** `WALL_HOLE` → J01·J03·J12 → `TURBINE` J04 → `ESS` J05·J06·J07 → J08 3컷 → J09 → J10 → J11

## 3-5. 내레이션 R2
```
어릴 땐, 바람을 병에 담으려 했습니다.
병 안엔, 조용한 공기만 남았죠.
지금도 바람을 잡지는 않습니다.
대신, 바람이 만든 전기를 모아 둡니다.
남는 시간의 전기를, 필요한 시간으로.
저녁이 필요한 곳에, 지역의 공급을 보탭니다.
설비를 돌보고, 기술을 배우고, 이 섬에서 새 일을 만드는 사람들.
제가 자란 섬에서, 제 일을 찾았습니다.
[조카] 이모, 오늘도 바람 잡았어?
[주인공] 아니. 오늘 쓸 전기를 모아 왔지.
바람은 지나가도, 우리의 내일은 여기에.
```
'바람이 만든 전기'·'일부/보탭니다' 계열 표현을 생략하지 않는다(R1 원칙).

## 3-6. 제출 설명 R2
《바람을 저축하는 사람들》은 제주 재생에너지 융복합시스템을 한 지역 기술자의 성장과 일상으로 풀어낸 근미래 단편입니다. 어린 시절 바람을 병에 담으려던 아이는 자란 섬에서 바람이 만든 전기를 모아 두고 필요한 시간에 쓰도록 돌보는 기술자가 됩니다. 제주 돌담의 같은 구멍을 통해 과거와 현재, 내일을 같은 시점으로 바라보며, 산업의 성장이 마을의 저녁과 새로운 일자리로 이어지는 모습을 그렸습니다. 2035년의 인물과 생활상은 생성형 AI로 시각화한 창작이며, 특정 정책 성과나 기술의 완전한 달성을 단정하지 않습니다.

---

# 4. 공통 — Google Flow 단독 파이프라인

## 4-1. 원칙
- **이미지(키프레임·Ingredients)와 영상 모두 Flow 안에서 생성.** 외부 이미지 생성기를 섞지 않는다 → 질감·색 일관성.
- 사용 기능(앱 화면에서 현재 지원 여부 확인 후): 이미지 생성, **Ingredients to Video**(인물·소품·장소 고정), **Frames to Video**(첫/끝 프레임), **Extend**, **Jump To**, 카메라 컨트롤, 부분 편집(Insert/Remove 등), Scenebuilder(가편집 확인용).
  - 과거 FAQ에는 일부 기능(첫/끝 프레임, 카메라 컨트롤, Extend, Ingredients)이 특정 Veo 버전에서 지원되지 않아 이전 모델로 전환된다는 안내가 있었다. **기능별로 실제 쓰인 모델명을 AI 활용 기록에 적는다.**
- 글자는 생성하지 않는다. 자막·날짜 각인·라벨·제목은 편집에서 삽입.
- Veo 생성 오디오는 앰비언스·폴리 참고용. 최종 VO·대사는 별도 녹음 또는 TTS로 하고 기록.
- Flow 프로젝트·생성 이력을 삭제하지 않는다(심사·증빙용).

## 4-2. 작품별 시험 컷 (본 생성 전 반드시 통과)

| 작품 | 시험 컷 | 통과 기준 | 실패 시 |
|---|---|---|---|
| 서울 | S05 등 뒤 리버스 6초 | 악기 형상 유지, 관객 10명 미만, 원경 지형 합리적 | 고정 와이드 + 등 클로즈업 분리 |
| Meta | M05 종이극장 리빌 8초 | 종이 질감(가위 자국·테이프) 유지, 인물이 종이 인형처럼 움직임 | 정면 고정 → 가림 인서트 → 내부 와이드 |
| 제주 | J01·J03 숨구멍 짝 | 같은 구멍 윤곽, 같은 렌즈감 | 숨구멍을 편집에서 마스크로 합성(구멍 이미지 1장을 전경 레이어로) |

같은 문제가 3회 반복되면 프롬프트 반복 대신 **구도를 단순화**(R1 원칙 유지).

## 4-3. 파일 구조 (작품별)
```
ai-contests-nov15/
  seoul-29s/  01_ingredients/ 02_keyframes/ 03_clips/ 04_audio/ 05_edit/ prompts.md
  meta-family/ (동일)
  jeju-wind/   (동일)
```
클립 파일명: `S05_R2_take3.mp4`처럼 컷·라운드·테이크 표기. `prompts.md`에는 **실행본 프롬프트**와 사용 기능(Frames/Ingredients/Extend 등)·모델명을 기록 → R1 §04 AI 활용 기록 템플릿에 그대로 옮김.

## 4-4. 일정 (오늘 10/7 기준)

| 기간 | 작업 |
|---|---|
| 10/7–10/9 | 서울 주제 원문·필러박스 허용 확인 / Meta 형식별 규격 확인 / 세 작품 Ingredients 확정 |
| 10/10–10/13 | 시험 컷 3종(S05 · M05 · J01+J03) |
| 10/14–10/24 | 서울 본 생성·편집 → **11/8 이전 완료 목표로 여유 확보** |
| 10/20–11/5 | Meta 본 생성(M06 수정 과정 기록 포함) |
| 기존 작업 여유 시 | 제주 본 생성 |
| 11/8 · 11/10 · 11/13 | 서울 · 제주 · Meta 내부 제출 목표(R1 유지) |

---

# 5. 참고 자료

- R1 출처 등록부(공식 공고 3건·보도 3건)는 그대로 유효. 이번 재검토에서 서울시·Meta 공식 페이지는 네트워크 제한으로 재열람하지 못했으므로, **서울 주제 원문과 Meta 형식별 규격은 여전히 미확인 게이트**다.
- 해외 연출 흐름(방향성 참고, 대부분 업계 리포트·블로그):
  - [Filmsupply — Commercial Filmmaking Trend Report 2026](https://www.filmsupply.com/articles/commercial-filmmaking-trend-report-2026/) (아날로그 질감, "Keep It Stupid Cinematic", 다중 프레임 단일 시각 세계)
  - [Deck.gallery — Commercial Filmmaking TR 2026 요약](https://www.deck.gallery/commercial-filmmaking-tr-2026/)
  - [IndieWire — How 58 Cinematographers Shot Their 2026 Fall Festival Favorites](https://www.indiewire.com/lists/how-cinematographers-shot-2026-fall-festival-movies/) (16mm 질감, 대칭, 과도한 스타일 배제)
  - [Envato — 10 filmmaking trends shaping cinema in 2026](https://elements.envato.com/learn/filmmaking-trends)
  - [FinalBit — The State of Cinema 2026](https://finalbitai.com/blog/the-state-of-cinema-2026-5-trends-redefining-filmmaking-from-ai-to) (AI 반작용으로서의 물리적·실물 질감)
- Google Flow 기능:
  - [Google 블로그 — Meet Flow](https://blog.google/technology/ai/google-flow-veo-ai-filmmaking-tool/)
  - [Flow FAQ (labs.google)](https://labs.google/fx/en-gb/tools/flow/faq)
  - [Chrome Unboxed — Flow Veo 3.1 및 편집 도구 업데이트](https://chromeunboxed.com/googles-ai-video-maker-flow-just-got-a-massive-upgrade-with-veo-3-1-and-powerful-new-editing-tools/)
