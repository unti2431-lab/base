# 《창가의 1년》 상세 장면표 R4 — 1부: 공통 사양 + H01~H06

> 기준 문서: `scene-plan-r4.md` · 55초 · 24fps · 1,320프레임 · 16:9 1920×1080 기본(9:16 전환안 병기)
> 파일 구성: **1부**(공통 사양 + H01~H06) · **2부**(H07~H12) · **3부**(내레이션·문자·사운드 큐시트, 편집 연결표, 생성 목록, 검수표)
> 타임코드 표기: `초:프레임` (24fps, 예: `13:12` = 13.5초)

---

## 0. 전체 타임라인 한눈에 보기

| 컷 | 구간(TC) | 길이 | 막 | 한 줄 내용 | 내레이션 | 화면 문자 |
|---|---|---|---|---|---|---|
| H01 | 00:00–03:00 | 3s | 1막 건너는 강 | 철교 위 지하철, 강이 가로로 스쳐 감 | N1 | `건너는 강` |
| H02 | 03:00–09:00 | 6s | 1막 | 수면에 거꾸로 선 서울 → 한강버스가 거울을 가름 | — | — |
| H03 | 09:00–13:00 | 4s | 2막 따라가는 강 | 수면 높이, 배가 강을 따라 깊이 방향으로 멀어짐 | N2 앞부분 | — |
| H04 | 13:00–17:00 | 4s | 2막 | 창가의 퇴근길 승객, 엎어 둔 휴대폰 | N2 뒷부분 | — |
| H05 | 17:00–23:00 | 6s | 2막 | 다리 밑 그늘, 빛줄기, 자연스러운 4:3 | 침묵 | — |
| H06 | 23:00–29:00 | 6s | 2막 | 그늘을 빠져나오며 16:9로 열림 | N3 | `따라가는 강` |
| H07 | 29:00–32:00 | 3s | 3막 창가의 1년 | 같은 창 · 겨울 | N4a | — |
| H08 | 32:00–35:00 | 3s | 3막 | 같은 창 · 봄 | — | — |
| H09 | 35:00–38:00 | 3s | 3막 | 같은 창 · 여름 | N4b | — |
| H10 | 38:00–41:00 | 3s | 3막 | 같은 창 · 다시 가을, 작은 미소 | — | — |
| H11 | 41:00–47:00 | 6s | 4막 바로 선 서울 | 반사 속 도시 → 틸트업 → 실제 도시 | N5 | — |
| H12 | 47:00–55:00 | 8s | 4막 | 강물 위 엔드카드 | N6 | 엔드카드 3단 |

**리듬 설계**: 3–6–4–4 | 6–6 | 3–3–3–3 | 6–8. 도입은 빠르게, 다리 밑에서 숨을 고르고, 계절 몽타주는 일정한 3초 박자로 1년을 넘기고, 결말은 길게 둡니다.

---

## 1. 공통 사양

### 1-1. STYLE LOCK (모든 영상·이미지 프롬프트 맨 앞에 붙임)
```
STYLE LOCK: quiet observational cinema in Seoul, after-work golden hour with low warm sun,
soft pastel film palette like Kodak Portra 400, slate-blue river water, steel-grey bridge structures,
apricot sunlight as the only warm accent, natural skin texture, subtle 35mm film grain, gentle contrast.
Locked-off or very slow steady camera, one camera move per shot, realistic scale and physics.
No text, no letters, no readable signage, no logos, no route maps, no subway line colors,
no fantasy distortion, no flying vehicles, no swooping drone moves, no teal-and-orange grading.
```

### 1-2. 기준 Ingredients 상세 사양

**ING-PAX: 주인공 승객** (가상 인물, 실존 인물과 닮지 않게)
- 30대 초반 한국인 여성 직장인. 어깨에 닿는 단발 흑발, 화장은 거의 없음, 안경과 장신구 없음(반사·일관성 문제 방지).
- 표정 기준값은 '무표정에 가까운 편안함'. 미소는 H10에서만 씁니다.
- 내레이션 화자는 이 인물과 같은 30대 여성의 목소리입니다.

| 의상 ID | 계절 | 의상 | 사용 컷 |
|---|---|---|---|
| PAX-A25 | 2025 가을 | 카멜색 울 코트, 흰 니트 | H04, H05, H06 |
| PAX-W | 겨울 | 남색 롱패딩, 회색 머플러 | H07 |
| PAX-SP | 봄 | 연베이지 트렌치코트 | H08 |
| PAX-SU | 여름 | 흰 셔츠, 소매를 걷음 | H09 |
| PAX-A26 | 2026 가을 | 회색 울 재킷(PAX-A25와 다른 옷) | H10 |

공통 소품은 검은 휴대폰(화면을 아래로 엎어 둠)과 남색 업무용 토트백(옆 좌석)입니다.

**캐릭터 시트 생성 프롬프트 (Flow 이미지)**
```
[STYLE LOCK] Character reference sheet on a plain light-grey background: the same fictional Korean
woman in her early thirties, shoulder-length straight black hair, no glasses, no jewelry, minimal makeup,
calm neutral expression. Three views side by side: front, three-quarter, profile. She wears a camel wool
coat over a white knit sweater. Even soft studio light. No text.
```
→ 확정 후 같은 얼굴로 의상만 바꾼 시트 4장을 만듭니다(Flow 이미지 편집: `same person, same face and hair, change outfit to …`).

**ING-WINDOW: 창가 좌석 플레이트**
- 승객 없는 빈 창가 좌석과 창틀. **카메라 위치는 통로 쪽 좌석 높이, 창과 45°.** 창이 화면 오른쪽 2/3를 차지하고, 좌석 등받이가 왼쪽 아래에 들어옵니다.
- 이 이미지 한 장이 H04~H10 일곱 컷 모두의 기준이 됩니다.
- ☐ 실제 한강버스 객실 창 구조(창 크기, 프레임 색, 좌석 배열)와 대조합니다.
```
[STYLE LOCK] Empty window seat inside a modern river ferry cabin at golden hour, camera at seated eye
height from the aisle side, angled 45 degrees to a large rectangular window that fills the right two
thirds of the frame; the back of the seat in the lower left. Outside: the Han River and a calm riverbank
in autumn. Clean, quiet, no people, no text.
```

**ING-BOAT: 한강버스 선박** — 부감 1장 + 측면 1장
- ☐ 실사 사진을 참조 이미지로 써도 되는지는 요강에서 확인해야 합니다. 허용되지 않으면 공식 사진을 보며 **선체 형태(쌍동선 여부, 창 배열, 도색 구획)를 글로 묘사**해 생성하고, 공식 사진과 나란히 놓고 검수합니다.

**ING-RIVER: 퇴근길 수면 톤**
- 늦은 오후 해가 낮게 깔리고, 수면은 잔잔한 슬레이트 블루, 하늘은 아이보리에서 옅은 살구색으로 넘어가는 톤. H02, H03, H11, H12가 공유합니다.

### 1-3. 생성 설정 기본값
- 화면비: 결정 게이트(`scene-plan-r4.md` §6) 결과대로. 아래 샷 카드는 16:9 기준이고, 각 카드에 9:16 대응을 적었습니다.
- 모델 운용: 초안·구도 탐색은 **Veo 빠른 모드**로, 최종 테이크는 **품질 모드**로 생성한 뒤 1080p로 업스케일합니다.
- 클립 길이: Veo 클립(8초)을 생성해 필요한 구간만 씁니다. 각 카드의 '사용 구간'은 생성 클립 안에서 잘라 쓸 위치입니다.
- 파일명 규칙: `H05_R1_t3.mp4`(컷_라운드_테이크).

---

## 2. 샷 카드 H01~H06

---

### H01 · 건너는 강 · `00:00–03:00` (3s / 72f)

| 항목 | 내용 |
|---|---|
| **목적** | 서울 사람의 공통 경험으로 첫 3초 훅. **화면을 가로지르는 빠른 움직임 = 강을 '건너기만' 하던 일상**. 창의성(구조 대비)과 주제 연결 |
| **구도** | 지하철 객실 측면. 좌석에 앉은 승객 3~4명이 화면 아래 1/3에 있고, 창이 화면 위 2/3를 차지. 창밖으로 한강이 **왼쪽→오른쪽**으로 빠르게 흐름 |
| **비트** | 0.0s 트러스 그림자가 빠르게 객실을 끊으며 시작 → 0.5s N1 시작 → 2.5s 창밖에 강 수면이 가장 넓게 보이는 순간 → 3.0s 컷 |
| **카메라·렌즈** | 고정 / 35mm 감각. 움직이는 것은 창밖과 빛뿐 |
| **빛·색** | 골든아워 측광이 트러스에 끊겨 **빠른 줄무늬(초당 4~6회)**로 객실을 지나감. 객실 형광등은 아주 약하게 |
| **인물** | 휴대폰을 보는 평범한 승객들(엑스트라). 주인공은 **나오지 않음**(주인공의 과거를 일반화한 장면) |
| **소리** | 철교 레일 소리(덜컹이는 리듬), 객실 웅웅거림. **마지막 2프레임 전에 소리를 먼저 끊음** → H02 정적 |
| **내레이션** | N1 `00:12–02:20` "한강은 늘, 건너는 강이었습니다." |
| **문자** | `건너는 강` `00:12–02:23` (하단 1/3, §3부 문자 사양) |
| **연결** | OUT: 하드 컷. 소리 선행 정적 |
| **Flow 제작** | Text to Video 또는 키프레임 → Frames to Video(시작 프레임만). 테이크 4 |
| **사용 구간** | 생성 8초 중 강이 가장 넓게 보이는 3초 |

**영상 프롬프트**
```
[STYLE LOCK] Side view inside a modern subway car crossing a steel truss bridge over a wide river at
golden hour. Three or four ordinary passengers sit in the lower third, calmly looking at their phones.
Through the large windows the river rushes past from left to right, and the truss beams strobe warm
sunlight quickly across the car in fast stripes. Locked-off camera. No line colors, no signage,
no text on screens, no logos.
```
- **합격**: 강 수면이 분명히 보임 / 빛 줄무늬가 리듬 있게 지나감 / 승객 표정이 평범함(우울하지 않음)
- **탈락**: 노선 색 띠·안내 화면 글자 생성 / 창밖이 터널 / 승객 얼굴 변형
- **대안**: 객실 대신 **창 하나만 클로즈업**(창틀 + 빠르게 스치는 강 + 트러스 그림자)으로 단순화
- **9:16**: 창 하나를 세로로 크게, 트러스 그림자가 위에서 아래로 떨어지게

---

### H02 · 거울을 가르는 배 · `03:00–09:00` (6s / 144f) ★ 작품의 얼굴

| 항목 | 내용 |
|---|---|
| **목적** | '뒤집힌 서울'의 낯섦과 **반사의 정체 공개, 한강버스 등장**을 한 컷에서. 전광판·SNS 썸네일 대표 이미지 |
| **구도** | 완전 수직 부감. 수면이 프레임 전체. 반사된 다리가 화면을 대각선으로 가로지르고, 반사된 스카이라인이 화면 위쪽에 거꾸로 섬. 수평선과 실제 하늘은 **프레임 밖** |
| **비트** | 0.0–2.0s 정지에 가까운 거울(미세한 잔물결만) → 2.0s 화면 아래 가장자리로 선수 진입 → 2.0–5.0s 선박이 화면 아래에서 위로 가로지름, V자 항적이 반사된 빌딩을 접었다 폄 → 5.0–6.0s 선미가 빠지고 거울이 다시 모이기 시작할 때 컷 |
| **카메라·렌즈** | 고정 부감, 장초점 압축감(원근 왜곡 없음) |
| **빛·색** | 반사된 하늘은 아이보리~살구, 수면 그늘은 슬레이트 블루. 선박 상판에 골든아워 하이라이트 |
| **소리** | 0.0–2.0s **거의 무음 + 물 표면의 아주 작은 찰랑임** → 선박 진입과 함께 물 가르는 소리, 낮은 엔진음이 아래에서 위로 이동(스테레오가 아니라 볼륨으로) |
| **내레이션 / 문자** | 없음 |
| **연결** | IN: H01 소리 선행 정적. OUT: 움직임 방향 매치(화면 위 = 전진) → H03 깊이 방향 전진 |
| **Flow 제작** | ① 키프레임 A(배 없는 거울) 확정 → ② Frames to Video: 시작 = A, 끝 = A에 항적 잔물결만 남은 B → ③ Ingredients에 ING-BOAT 부감. 테이크 6~8(최우선 투자) |
| **사용 구간** | 배가 2초 지점에 들어오는 테이크를 고름 |

**키프레임 A 프롬프트 (이미지)**
```
[STYLE LOCK] Perfectly top-down view of the calm Han River surface at golden hour, acting as a mirror:
an upside-down reflection of a long bridge crossing diagonally and a distant line of high-rise
apartments, under a soft ivory-to-apricot sky reflection. Tiny ripples only. The real horizon and sky
are outside the frame. No boats, no text.
```
**영상 프롬프트**
```
[STYLE LOCK] Use the ferry from the reference image exactly; do not change its hull shape or colors.
Locked-off top-down shot of the mirror-like river from the start frame. For two seconds nothing moves
except tiny ripples. Then the bow of the passenger ferry enters from the bottom edge and glides straight
upward through the reflection. Its V-shaped wake bends and folds the reflected buildings, which gently
re-form behind it. The ferry exits at the top. No other boats.
```
- **합격**: 첫 2초는 '거꾸로 선 도시'로 읽힘 / 선체 좌우 대칭 / 항적이 반사를 휘게 함
- **탈락**: 선체가 물에 녹아듦 / 배가 위아래로 뒤집힘 / 반사가 실제 하늘처럼 보여 반전이 안 됨
- **대안**: 배 전체가 아니라 **선수와 항적만** 지나가는 구도(실패율 하락). 그래도 실패하면 거울만 6초(배는 H03에서 처음 공개)
- **9:16**: 세로에 가장 유리한 컷. 배가 아래에서 위로 긴 거리를 지나감

---

### H03 · 따라가는 강 · `09:00–13:00` (4s / 96f)

| 항목 | 내용 |
|---|---|
| **목적** | **축의 전환.** H01의 '가로지르기'와 반대로, 배가 화면 **깊이 방향**으로 강을 따라 나아감. 제목 '강의 눈높이'의 시점 |
| **구도** | 수면 위 30cm 높이에서 뒤쪽을 봄. 선박이 화면 중앙에서 소실점 쪽으로 멀어짐. 좌우로 강변, 멀리 아파트 스카이라인. 수면이 화면 아래 1/3을 차지 |
| **비트** | 0.0s 선박이 화면 높이 1/3 크기 → 4.0s 1/5 크기로 멀어짐. 0.5s N2 시작 |
| **카메라·렌즈** | 고정 / 50mm. 렌즈 앞 수면이 살짝 찰랑임(물방울은 렌즈에 맺히지 않음) |
| **빛·색** | 역광에 가까운 골든아워. 항적에 살구빛 반짝임 |
| **소리** | 렌즈 앞 찰랑이는 물(근접), 멀어지는 엔진음 |
| **내레이션** | N2 앞부분 `09:12–` "1년 전 가을, 처음으로…" |
| **연결** | IN: H02 움직임 방향 매치. OUT: 하드 컷 → 객실 |
| **Flow 제작** | Ingredients(ING-BOAT 측후면 + ING-RIVER). 테이크 4 |

**영상 프롬프트**
```
[STYLE LOCK] Use the ferry from the reference image. Locked-off camera thirty centimetres above the
river surface, looking along the river. The passenger ferry moves away from the camera into the depth
of the frame, following the river toward a distant line of apartments at golden hour. Gentle wake
sparkles with low sun. Small ripples lap just in front of the lens. No other boats.
```
- **합격**: 배가 '강을 따라' 가는 방향성 / 수면 높이 시점
- **탈락**: 배가 옆으로 지나감(H01과 같은 축이 됨) / 배 크기가 갑자기 변함
- **9:16**: 소실점을 화면 위쪽 1/3에 두고 수면을 길게

---

### H04 · 창가의 퇴근길 · `13:00–17:00` (4s / 96f)

| 항목 | 내용 |
|---|---|
| **목적** | **생활 교통(정책 반영)**을 대사 없이 제시. 업무용 가방 + 퇴근 시간대 + 엎어 둔 휴대폰 = 일하고 돌아가는 사람이 바깥을 '만나러' 고개를 돌림 |
| **구도** | ING-WINDOW 구도 그대로 + PAX-A25가 앉음. 승객은 창을 향한 3/4 뒷옆모습. 무릎 위 엎어 둔 휴대폰, 옆 좌석에 토트백 |
| **비트** | 0.0s 창밖을 보는 승객 → 2.0s 창밖 멀리 다리가 다가오기 시작 → 3.5s 다리 그늘의 앞 가장자리가 창틀에 닿음 → 4.0s 컷(그늘이 화면 오른쪽부터 덮기 시작) |
| **카메라·렌즈** | 고정 / 50mm, 얕은 심도(승객 선명, 창밖 약간 부드럽게) |
| **빛·색** | 창으로 들어온 골든아워가 승객 머리카락 가장자리에 림라이트 |
| **소리** | 객실 정적, 선체에 닿는 물소리 저음, 아주 먼 엔진음 |
| **내레이션** | N2 뒷부분 `~14:12` "…강을 따라 퇴근했습니다." |
| **연결** | OUT: **오클루전**(다리 그늘이 덮는 순간 컷) → H05 |
| **Flow 제작** | 키프레임 = ING-WINDOW + PAX-A25 합성(Flow 이미지 편집) → Frames to Video(시작만), Ingredients로 인물 고정. 테이크 4 |

**영상 프롬프트**
```
[STYLE LOCK] Use the window seat and the woman (camel coat outfit) from the references exactly.
Locked-off shot: she sits by the ferry window after work, seen three-quarter from behind, looking out.
Her phone lies face-down on her lap; a navy work tote bag rests on the next seat. Outside, the autumn
riverbank glides by at golden hour and a large bridge slowly approaches. In the final half second the
leading edge of the bridge's shadow starts to cover the window from the right.
```
- **합격**: 휴대폰이 엎어져 있음 / 가방이 보임 / 끝에서 그늘이 들어오기 시작
- **탈락**: 휴대폰 화면이 켜짐 / 인물이 카메라를 봄 / 창틀 위치가 ING-WINDOW와 다름
- **9:16**: 승객 옆얼굴과 창을 세로로 쌓음(위 = 창밖, 아래 = 무릎 위 휴대폰)

---

### H05 · 다리 밑 · `17:00–23:00` (6s / 144f) ★ 클라이맥스 1

| 항목 | 내용 |
|---|---|
| **목적** | 빛의 변화가 곧 사건. 한강버스에서만 겪는 **다리 밑의 빛과 소리**. 4:3의 좁음이 다음 컷의 열림을 준비함 |
| **구도** | H04와 같은 카메라 위치. 객실은 거의 검정, **밝은 창 직사각형만 남아 화면 중앙에 4:3 비율로 보임**(좌우 약 12.5%씩 그늘 먹색 `#1C2328`) |
| **비트** | 0.0–1.0s 어둠에 눈이 적응하듯 창 바깥(교각, 다리 하부)이 드러남 → 1.0–5.0s 다리 하부 틈으로 새는 **빛줄기가 약 1.2초 간격으로** 승객 얼굴과 좌석을 왼쪽→오른쪽으로 쓸고 지나감(4회) → 4.0s 승객이 눈만 살짝 들어 올림 → 5.5s 창 바깥 끝이 밝아지기 시작 |
| **카메라·렌즈** | 고정 |
| **빛·색** | 빛줄기는 살구빛, 경계가 부드러운 띠. 깜빡이는 섬광이 아님 |
| **소리** | **침묵 구간.** 엔진·물소리가 다리 하부에 반사되어 낮고 넓게 울림(리버브 2.5초 감각). 음악 없음 |
| **내레이션 / 문자** | 없음 |
| **연결** | IN: 오클루전. OUT: **연속**(H06과 같은 흐름. 끝 프레임 = H06 시작 프레임) |
| **Flow 제작** | Frames to Video: 시작 = 어두운 객실 + 밝은 창 키프레임, 끝 = 빛이 들어차기 직전 키프레임. 테이크 6 |

**영상 프롬프트**
```
[STYLE LOCK] Same cabin, same camera position and the same woman (camel coat) as the references.
The ferry is passing under a large steel bridge: the cabin is almost black and only the bright window
rectangle remains in the centre, so the image reads like a 4:3 picture with deep shadow on both sides.
Every second or so a soft band of warm sunlight slips through a gap in the bridge structure and sweeps
slowly across her face and the seat backs from left to right. She stays still and only lifts her eyes
slightly. Toward the end, the far edge of the window begins to brighten.
```
- **합격**: 좌우가 충분히 어두워 4:3처럼 읽힘 / 빛이 '쓸고 지나가는' 띠 / 인물 얼굴 유지
- **탈락**: 플래시처럼 깜빡임 / 객실 조명이 켜져 4:3 효과가 사라짐 / 얼굴이 빛에 녹음
- **대안**: 4:3 효과가 약하면 편집 매트 사용 ☐(요강상 '시각 장면 AI 생성' 조건과 충돌하는지 확인 후에만)
- **9:16**: 1:1 정사각 창으로 보이게(위아래가 어둠)

---

### H06 · 열리는 강 · `23:00–29:00` (6s / 144f) ★ 클라이맥스 2

| 항목 | 내용 |
|---|---|
| **목적** | '새로운 서울'이 열리는 순간. **화면비가 감정이 됨.** 내레이션으로 노선(정책)을 처음 언급 |
| **구도** | H05 끝과 같은 위치에서 시작 → 객실에 빛이 들어차며 좌우 어둠이 사라지고 16:9 전체가 열림 → 카메라가 창 쪽으로 아주 느리게 다가가 넓은 강변 풍경이 화면 대부분을 채움 |
| **비트** | 0.0–1.5s 좌우 어둠이 빛으로 채워짐(화면이 '열림') → 1.5s 음악 첫 음 → 2.0–6.0s 느린 푸시인, 넓은 강변과 스카이라인 → 5.5s 멀리 다음 다리가 보이기 시작 |
| **카메라·렌즈** | 1.5s 이후 느린 푸시인(전체 6초 동안 화면 크기 약 10% 확대) |
| **빛·색** | 골든아워가 객실 전체에 들어참. 이 작품에서 **가장 밝은 컷** |
| **소리** | 다리 밑 울림이 열리는 공간감으로 바뀜(리버브 감소, 바람 소리) + **음악 시작**(피아노 또는 나일론 기타 단선율) |
| **내레이션** | N3 `26:00–28:12` "마곡에서 잠실까지, 강 위로 난 길." |
| **문자** | `따라가는 강` `23:18–26:00` (H01의 `건너는 강`과 같은 위치·크기) |
| **연결** | IN: H05 연속. OUT: 마지막 12프레임에 다음 다리 그늘이 덮음 → **오클루전 와이프** → H07 겨울 |
| **Flow 제작** | Frames to Video: 시작 = H05 끝 프레임, 끝 = 밝게 열린 객실과 강변 키프레임 → 필요하면 Extend로 마지막 그늘 진입. 테이크 6 |

**영상 프롬프트**
```
[STYLE LOCK] Continue from the start frame. The ferry exits the shadow of the bridge: warm golden-hour
light floods the cabin, the dark edges on both sides fill with light, and the wide autumn riverbank
and distant skyline open across the full width of the frame. The camera very slowly pushes in toward
the window. The woman, the window frame and the seat stay identical. Near the end, another bridge
appears in the distance.
```
- **합격**: '열림'이 1.5초 안에 분명함 / 인물·창틀 유지 / 가장 밝고 넓은 컷
- **탈락**: 열리는 순간 컷처럼 튐 / 다른 객실로 바뀜 / 창밖 장소가 갑자기 다른 강
- **9:16**: 1:1 → 9:16(위아래로 열림). 하늘과 수면이 위아래로 펼쳐짐

---

→ **2부(H07~H12)**는 `shot-sheet-r4-part2.md`에 이어집니다.
