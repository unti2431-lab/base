# 《창가의 1년》 상세 장면표 R4 — 2부: H07~H12

> 1부(`shot-sheet-r4-part1.md`)의 STYLE LOCK·Ingredients 사양을 그대로 씁니다. 타임코드 표기는 `초:프레임`(24fps)입니다.

---

## 3막 공통: 계절 창 몽타주 (H07~H10, 12초)

**한 문장 설계**: 카메라·창틀·좌석·시간대(퇴근 골든아워)는 고정하고, **창밖의 계절과 승객의 옷만** 바뀝니다. 계절은 **다리 그늘이 객실을 덮는 순간(오클루전 와이프)**에 넘어갑니다.

### 계절 컷의 공통 박자 (각 3초 = 72프레임)
| 구간 | 프레임 | 화면 |
|---|---|---|
| 그늘에서 나옴 | 0–12 | 거의 검정 → 빛이 들어참(직전 컷의 그늘과 이어짐) |
| 계절 노출 | 12–60 | 같은 창, 바뀐 계절, 바뀐 옷. 이 2초가 계절을 읽는 시간 |
| 그늘로 들어감 | 60–72 | 다음 다리 그늘이 오른쪽에서 덮어 거의 검정 |

편집에서는 **어두운 프레임 위에서 컷**하므로 이음새가 보이지 않습니다. 그늘 프레임이 짧으면 2~3프레임 늘립니다.

### 계절 컷 공통 제작법: 창 플레이트
1. ING-WINDOW(빈 좌석, 가을)를 기준으로 Flow 이미지 편집에서 **창밖만** 겨울/봄/여름/가을26로 바꾼 플레이트 4장을 만듭니다. 프롬프트: `keep everything inside the cabin identical; change only the view outside the window to …`
2. 각 플레이트에 해당 의상의 ING-PAX를 앉혀 키프레임 4장을 만듭니다.
3. Frames to Video로 생성합니다. 시작 = 키프레임, 끝 = 같은 키프레임에 그늘을 덮은 버전(Flow 이미지 편집으로 오른쪽부터 어둡게).
4. 네 키프레임을 한 화면에 나란히 놓고 **창틀 모서리 위치, 좌석 높이, 인물 머리 위치**가 같은지 검수한 뒤 영상을 생성합니다.

### 계절 컷 공통 영상 프롬프트 (괄호만 바꿈)
```
[STYLE LOCK] Use the window seat and the woman wearing [WARDROBE] from the references exactly; same
camera position, same window frame, same seat. The clip starts in the dark shadow of a bridge and light
returns within half a second. She sits by the window after work, phone face-down on her lap, looking
out. Outside at golden hour: [SEASON DETAIL]. The river water is open and flowing, never frozen.
In the last half second the shadow of the next bridge sweeps in from the right and the frame goes
almost black. Locked-off camera.
```

---

### H07 · 겨울 · `29:00–32:00` (3s / 72f)

| 항목 | 내용 |
|---|---|
| **목적** | 1년의 첫 장. 1주년을 **시간의 경과**로 보여주기 시작 |
| **[WARDROBE]** | a long navy padded winter coat and a grey scarf (PAX-W) |
| **[SEASON DETAIL]** | light snow on the riverbank grass and paths, bare trees, pale low winter sun, a few people walking in coats |
| **빛·색** | 해가 가장 낮고 색온도가 차가움. 살구빛은 아주 옅게. 하얀 둔치 |
| **연기** | 승객이 머플러에 턱을 묻고 바깥을 봄 |
| **소리** | 음악 유지 + 아주 작은 겨울바람. 창 유리에 닿는 미세한 바람 소리 |
| **내레이션** | N4a `29:12–30:12` "같은 창가." |
| **연결** | IN: H06 끝 그늘. OUT: 그늘 → H08 |
| **사실 확인** | ☐ **겨울철 실제 운항 여부**(결빙·운항 중단 기간). 확인 전까지 보류하고, 운항하지 않았다면 이 컷을 빼고 52초 버전으로 편집 |
| **합격 / 탈락** | 합격: 눈 덮인 둔치와 흐르는 강물이 함께 보임 / 탈락: 강이 얼어 있음, 창에 성에, 눈이 객실 안에 내림 |
| **9:16** | 창 위쪽에 눈 덮인 둔치, 아래쪽에 머플러에 묻은 옆얼굴 |

---

### H08 · 봄 · `32:00–35:00` (3s / 72f)

| 항목 | 내용 |
|---|---|
| **목적** | 가장 '새로운 서울'다운 계절색. 서울 사람이 아는 강변 벚꽃 |
| **[WARDROBE]** | a light beige trench coat (PAX-SP) |
| **[SEASON DETAIL]** | cherry trees in full bloom along the riverbank, soft pink blossoms, a few petals floating on the water, people strolling |
| **빛·색** | 연분홍은 채도를 한 단계 낮춤(파스텔). 해가 겨울보다 높고 따뜻함 |
| **연기** | 승객이 창밖 꽃잎이 흘러가는 쪽으로 시선을 천천히 옮김(눈만) |
| **소리** | 음악. 바람 소리가 부드러워짐 |
| **내레이션 / 문자** | 없음 |
| **합격 / 탈락** | 합격: 벚꽃이 강변을 따라 이어짐 / 탈락: 꽃잎이 객실 안에 날림, 채도 과다(형광 분홍) |
| **9:16** | 창 위쪽에 벚꽃 띠, 아래쪽에 승객 |

---

### H09 · 여름 · `35:00–38:00` (3s / 72f)

| 항목 | 내용 |
|---|---|
| **목적** | 생활의 서울. 퇴근 후에도 해가 길게 남은 여름 강변 |
| **[WARDROBE]** | a white shirt with sleeves rolled up (PAX-SU) |
| **[SEASON DETAIL]** | deep green riverside park, small tents on the grass, people cycling and jogging, long warm evening light |
| **빛·색** | 해가 가장 높고 길게 남음. 초록은 한 단계 낮춰 올리브 쪽으로 |
| **연기** | 승객이 걷은 소매에 팔꿈치를 창틀에 걸침(1년 사이 편해진 자세) |
| **소리** | 음악이 가장 풍성한 지점. 아주 먼 생활음(자전거 벨) |
| **내레이션** | N4b `35:12–37:12` "매번, 처음 보는 서울." |
| **합격 / 탈락** | 합격: 텐트·자전거가 작게 / 탈락: 사람이 너무 커서 관광 영상처럼 보임, 수상 레저가 화면을 차지 |
| **9:16** | 창 위쪽에 초록 둔치와 텐트, 아래쪽에 창틀에 걸친 팔 |

---

### H10 · 다시 가을 · `38:00–41:00` (3s / 72f)

| 항목 | 내용 |
|---|---|
| **목적** | 1년이 한 바퀴 돎(2026 가을 = 1주년). 감정의 정점이지만 **아주 작게** |
| **[WARDROBE]** | a grey wool jacket (PAX-A26, different from the camel coat) |
| **[SEASON DETAIL]** | silver pampas grass glowing along the riverbank in low autumn sun, the same calm skyline as the first autumn |
| **빛·색** | H04~H06과 같은 가을빛(시작점으로 돌아옴) |
| **연기** | 1.5s 지점부터 승객이 **입꼬리만 아주 작게** 올림. 이를 보이며 웃지 않음 |
| **소리** | 음악이 한 단계 내려감(H11 내레이션 자리 확보) |
| **내레이션 / 문자** | 없음 |
| **연결** | **이 컷은 그늘로 끝나지 않음.** 미소 뒤 1초를 유지하고 하드 컷 → H11 부감(1년의 순환이 끝났다는 표시) |
| **영상 프롬프트 수정** | 공통 프롬프트에서 마지막 문장(그늘 진입)을 빼고 `After a moment she smiles very slightly, lips closed, still looking out.`를 추가 |
| **합격 / 탈락** | 합격: 미소가 '알아챌 듯 말 듯' / 탈락: 크게 웃음, 카메라를 봄, 얼굴이 H04와 다른 사람 |
| **9:16** | 옆얼굴 클로즈업 비중을 높임 |

---

## 4막: 바로 선 서울

### H11 · 거울 회수 · `41:00–47:00` (6s / 144f) ★

| 항목 | 내용 |
|---|---|
| **목적** | 오프닝의 '거꾸로 선 서울'을 **바로 세우며** 마무리. "그대로"(같은 도시)와 "새롭게"(뒤집어 본 경험)를 한 동작으로 증명 |
| **구도** | 시작: H02와 같은 수직 부감, 항적이 가라앉는 수면에 거꾸로 선 스카이라인 → 끝: 수면 바로 위 눈높이에서 바로 선 실제 스카이라인, 화면 가운데 멀리 작게 멀어지는 한강버스 |
| **비트** | 0.0–1.5s 잔물결이 가라앉으며 반사 속 도시가 온전해짐 → 1.0s N5 시작 → 1.5–5.0s 카메라가 수면을 스치듯 **연속 틸트업**(약 90°) → 5.0–6.0s 바로 선 도시에서 정지 |
| **카메라·렌즈** | 이 작품에서 유일한 **AI 네이티브 연속 이동**. 속도는 처음과 끝이 느리고 가운데가 빠름(이즈 인/아웃) |
| **빛·색** | 해가 수평선에 가장 가까운 골든아워. 이 작품에서 가장 따뜻한 컷 |
| **소리** | 음악이 가라앉고 물소리가 다시 앞으로. 틸트업 정점에서 바람 한 번 |
| **내레이션** | N5 `42:12–45:12` "서울은 그대로. 시선은 새롭게." |
| **연결** | IN: H10 하드 컷. OUT: 디졸브 12프레임 → H12 |
| **Flow 제작** | Frames to Video: 시작 = H02 키프레임 A(잔물결 버전), 끝 = **키프레임 A를 위아래로 뒤집은 이미지를 기준으로 생성한 실제 스카이라인**(반사와 실제 건물 배치를 일치시키기 위해). ING-BOAT 원경. 테이크 6 |

**끝 프레임 키프레임 프롬프트 (이미지, 뒤집은 키프레임 A를 참조로 첨부)**
```
[STYLE LOCK] Eye-level view just above the calm Han River at golden hour: the same long bridge and the
same line of high-rise apartments as in the reference, now upright, with the same building positions.
The passenger ferry is small in the middle distance, moving away. Soft ivory-to-apricot sky. No text.
```
**영상 프롬프트**
```
[STYLE LOCK] Start: top-down view of the calm river reflecting the upside-down skyline, a faint wake
settling until the reflection is whole. The camera then tilts upward in one continuous, smooth move,
skimming just above the water, until the real skyline stands upright across the horizon, with the
ferry small in the middle distance. Ease in and ease out. One seamless move, no cut.
```
- **합격**: 반사 속 건물 배치와 실제 건물 배치가 이어짐 / 이동 중 수면이 끊기지 않음
- **탈락**: 중간에 다른 도시로 바뀜 / 틸트 도중 컷처럼 튐 / 배가 2척이 됨
- **대안**: 연속 틸트가 실패하면 **반사 정지(1.5초) → 실제 도시(3초)**로 하드 컷. 대신 두 화면의 건물 배치를 정확히 상하 대칭으로 맞춰 '뒤집힘이 바로 섰다'는 매치컷으로 처리
- **9:16**: 세로 틸트가 더 길게 보여 효과가 커짐

---

### H12 · 엔드카드 · `47:00–55:00` (8s / 192f)

| 항목 | 내용 |
|---|---|
| **목적** | 카피, 1주년, 브랜드 각인. 전광판에서 마지막으로 읽히는 화면 |
| **배경** | **AI 생성 영상**(본편 시각 장면 AI 조건 충족): 정면 눈높이의 잔잔한 강물, 화면 아래 1/3에 수면, 위 2/3는 해가 막 진 아이보리~옅은 살구빛 하늘. 아주 느린 잔물결만 |
| **비트** | 47:00–48:12 H11에서 디졸브 → 48:12–50:18 카피 1 → 50:18–52:00 카피 1 페이드아웃·카피 2 페이드인 → 52:00 브랜드명 + N6 → 54:00–55:00 물소리만 남고 화면 유지(검정으로 끝내지 않음, 전광판 반복 재생 대비) |
| **문자 1** | `서울은 그대로. 시선은 새롭게.` (중앙, 48:12–50:18) |
| **문자 2** | `함께한 첫 1년 · 누적 탑승 60만` (중앙, 50:18–55:00) ☐ 수치 사용 허용 시 |
| **문자 3** | `한강버스` (문자 2 아래, 52:00–55:00) / 공식 로고 파일은 ☐ 허용 시에만 교체 |
| **소리** | 음악 마지막 음 52:00에서 끝, 물소리 하나로 55:00까지 |
| **내레이션** | N6 `52:06–53:06` "한강버스." |
| **Flow 제작** | Text to Video(ING-RIVER 참조). 테이크 2 |

**배경 영상 프롬프트**
```
[STYLE LOCK] Locked-off eye-level view of the calm Han River just after sunset: water in the lower
third, a clean ivory-to-faint-apricot sky in the upper two thirds with a thin distant skyline on the
horizon. Only very slow gentle ripples. Lots of empty space for titles. No boats, no text.
```
- **합격**: 문자가 들어갈 빈 공간 / 움직임이 거의 없음
- **9:16**: 하늘 영역을 위로 길게, 문자 3단을 세로로 쌓음

---

## 52초 버전 (겨울 H07 삭제 시)

| 변경 | 내용 |
|---|---|
| H06 | 끝 그늘 → 바로 H08 봄 |
| N4a "같은 창가." | H08 `32:12`로 이동 |
| 이후 컷 | 전부 3초 앞당김(H11 `38:00–44:00`, H12 `44:00–52:00`) |
| 음악 | 계절 구간을 9초로 편곡(3박 × 3) |

---

→ **3부(내레이션·문자·사운드 큐시트, 편집 연결표, 생성 목록, 검수표)**는 `shot-sheet-r4-part3.md`에 이어집니다.
