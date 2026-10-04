# 한강버스 AI 영상 공모전 — 장면 구성 R3

> 가제 **《강의 눈높이》** (부제: 건너던 강을, 따라가는 날)
> 50초 · 16:9 · 1920×1080 · 24fps(1,200프레임) · MP4 · **Google Flow(Veo) 단독 생성 파이프라인**

---

## 0. 요강 상태 (2026-10-04 기준)

| 항목 | R2에 적힌 조건 | 이번 세션 확인 결과 |
|---|---|---|
| 주제 | 한강버스를 타고 만나는 새로운 서울 | 독립 재확인 **실패**. 검색에 2026 AI 공모 공고가 잡히지 않음 |
| 길이·규격 | 30~60초, 16:9 또는 9:16, FHD 이상 | 위와 같음 |
| AI 조건 | 본편의 모든 시각 장면을 생성형 AI로 제작 | 위와 같음 |
| 마감 | 10/21 | 위와 같음. **오늘 기준 D-17** |
| 활용 | 수상작은 선착장 옥외 전광판 송출 | 위와 같음 |

**⚠ 혼동 주의.** 서울시가 2025년 11월에 연 **「한강버스 숏폼 공모전」은 생성형 AI 작품을 심사에서 제외**했습니다([내 손안에 서울](https://mediahub.seoul.go.kr/hangangbus)). 지금 준비하는 공모전은 AI 제작이 필수인 별개 공모전입니다. 제출 전에 **주최처, 공고 원문 URL, 첨부 요강 PDF**를 직접 열어 두 공모전을 섞어 보지 않았는지 확인하세요. R2가 남긴 확인 과제도 그대로 유효합니다.
1. 후편집 문자와 공식 로고를 넣어도 되는지
2. 실사 사진을 참조 이미지로 써도 되는지
3. 전광판의 화면비와 음향 재생 여부

---

## 1. R2 검토

### 유지할 것
1. **명소를 나열하지 않는 원칙.** "같은 장소를 다르게 보는 작품"이라는 방향이 맞습니다.
2. **"서울은 그대로. 시선은 새롭게."** 엔딩 카피가 좋아서 그대로 씁니다.
3. **"늘 건너던 강을, 오늘은 따라갑니다."** 이 문장이 사실 작품 전체의 열쇠입니다. R3는 이 문장을 **구조 전체로** 키웁니다.
4. 10초 안에 선박을 공개한다는 규칙, 한 시간대로 빛을 통일하는 규칙, 반사 효과를 남발하지 않는 원칙.

### 고칠 것

| # | R2의 문제 | 왜 문제인가 | R3 해결 |
|---|---|---|---|
| 1 | **파이프라인이 imagegen + 독립 영상 도구** | Google Flow 단독 원칙과 충돌함. 도구가 섞이면 선박·인물 일관성이 깨지고, 'AI 제작 이력' 증빙도 흩어짐 | 키프레임부터 클립·연장까지 **Flow 안에서만** 생성. 이미지 생성·Ingredients·Frames to Video·Extend를 쓰고, 프로젝트 하나에 이력을 보존(§5) |
| 2 | **H04~H08의 23초 동안 한 사람이 앉아만 있음** | 전광판은 소리 없이 **지나가며 보는** 매체임. 인물의 미세한 시선 변화는 실외 LED에서 읽히지 않음 | 사건을 **빛과 화면비의 변화**로 만듦. 다리 그늘 속 줄무늬 빛, 4:3 창틀에서 16:9로 열리는 화면(§2) |
| 3 | **'새로운 서울'의 '서울'이 사라짐** | 명소를 빼다가 서울 고유성까지 빠짐. 어느 강이나 될 수 있는 영상이 됨 | 랜드마크 대신 **서울 사람만 아는 생활 장면**을 씀. 지하철로 한강을 건너는 몇 초, 둔치의 텐트·자전거·러너, 강변 아파트 스카이라인 |
| 4 | **'시선이 바뀐다'가 추상적임** | '바라보는 자리'가 무엇에서 무엇으로 바뀌는지 화면에 대비가 없음 | **축의 전환**으로 구체화. 서울 사람에게 한강은 늘 **가로질러 건너는 강**(직각)이었지만, 한강버스에서는 **따라가는 강**(평행)이 됨. 첫 4초와 나머지를 이 대비로 설계 |
| 5 | **H05 '유리에 얼굴과 도시가 겹치는' 장면이 핵심인데 AI 실패율이 가장 높음** | Veo는 반사상 속 얼굴의 일관성을 자주 무너뜨림. 얼굴 복제·변형이 생김 | 반사 연출을 **수면 반사 하나**로 줄임. 인물 쪽 핵심 장면은 **빛이 얼굴을 지나가는 것**으로 바꿈(Veo가 안정적으로 처리하는 유형) |
| 6 | **'서울이 뒤집혔습니다' 수면 반사 도입이 흔한 트릭** | SNS에서 흔한 반사 사진 문법이라, 반전을 알고 나면 남는 것이 없음(R2도 스스로 지적함) | 반사를 **선박이 가르는 거울**로 씀. 부감에서 한강버스의 항적이 거꾸로 선 도시를 접었다 펴는 장면. 반사의 정체 공개와 한강버스 공개가 한 컷에서 동시에 일어남 |
| 7 | **반사로 열고 카피로 닫음** | 시작의 반사 이미지가 엔딩에서 회수되지 않음 | 엔딩에서 항적이 가라앉으며 거울 속 도시가 다시 완성되고, 카메라가 **수직으로 틸트업**해 실제 도시를 바로 세움. "그대로"(같은 도시)와 "새롭게"(뒤집혀 본 경험)를 화면이 증명 |
| 8 | **'만나는'이 비어 있음** | 주제 문장은 '타고 **만나는** 새로운 서울' | H01에서는 승객 모두 휴대폰을 봄. 후반의 승객은 휴대폰을 무릎에 엎어 두고 바깥을 봄. 서울을 **만나는 일 = 주의를 돌려주는 일**로 해석 |

---

## 2. 룩앤필 — "코모레비 트랜싯(Komorebi Transit)"

> 이름은 이 문서에서 붙인 것입니다. 업계 표준 용어가 아닙니다. 아래 기법은 **2025~26년 해외 광고·패션 필름·독립영화에서 눈에 띄게 쓰이는 연출을 관찰한 것**이며, '국내에서 드물다'는 사용 빈도 통계는 없습니다. 국내 공공·관광 홍보 영상의 일반적 문법(드론 부감, 빠른 컷, 랜드마크 몽타주, 고채도, 웅장한 음악)과 **반대 방향**이라는 점이 이번 선택의 근거입니다.

### 다섯 가지 연출 장치

| 장치 | 무엇인가 | 해외 맥락 | 이 작품에서 하는 일 |
|---|---|---|---|
| **① 관찰자 시네마 + 코모레비 리듬** | 사건 대신 **빛의 변화를 사건으로** 다루는 조용한 관찰. 코모레비(木漏れ日)는 나뭇잎 사이로 새는 빛을 뜻하는 일본어 | 빔 벤더스 〈퍼펙트 데이즈〉(2023) 이후 '조용한 일상 관찰' 톤이 해외 브랜드 필름에서 자주 인용됨 | 나뭇잎 대신 **다리 하부 구조물 사이로 새는 빛줄기**가 승객의 얼굴과 객실을 일정한 리듬으로 쓸고 지나감. 한강버스에서만 겪는 빛 |
| **② 서사적 화면비 전환(Open Matte Reveal)** | 좁은 화면비로 가두었다가 **감정이 열리는 순간 화면이 넓어짐** | 자비에 돌란 〈마미〉(2014)의 화면 확장 이후, 패션 필름·뮤직비디오에서 쓰이는 고급 문법. 국내 공공 영상에서는 보기 드묾 | 다리 그늘 아래 어두운 객실 → 밝은 창만 남아 **자연스러운 4:3**. 그늘을 빠져나오는 순간 **16:9 전체로 강변이 열림.** "따라가는 강"이 시작되는 순간 |
| **③ 축의 전환 매치컷(Axis Cut)** | 움직임의 **방향 벡터**로 의미를 대비 | 그래픽 매치컷 자체는 고전 기법. 의미 대비 장치로 쓰는 방식이 최근 해외 광고에서 정교해짐 | H01은 지하철이 화면을 **가로로 빠르게** 지나감(건너는 강). 이후 한강버스는 화면 **깊이 방향으로 느리게** 나아감(따라가는 강) |
| **④ AI 네이티브 카메라(불가능한 연속 이동)** | 실제 촬영으로는 불가능한 카메라 경로를 컷 없이 이어 붙임 | 2026 AI 영상 트렌드 자료들이 'AI-native cinematography'로 꼽는 문법([LTX](https://ltx.io/blog/ai-video-trends), [Envato](https://elements.envato.com/learn/motion-design-trends)) | **딱 한 번만** 씀. 엔딩에서 수면 반사 속 거꾸로 선 도시 → 카메라가 수면을 스치며 위로 틸트 → 실제 도시. 반사(뒤집힘)가 원래대로 돌아오는 장면 |
| **⑤ 필드 레코딩 사운드** | 음악보다 **현장음을 먼저** 세움. 다리 밑 울림, 선체에 부딪는 물, 객실 정적 | 해외 브랜드 필름의 'quiet luxury' 사운드 경향 | 다리 밑 진입 시 소리가 **낮고 울리게 바뀌는 순간**이 청각적 클라이맥스. 음악은 화면비가 열릴 때 처음 들어옴 |

### 화면 규칙 (LOOK LOCK)
- **시간대**: 10월 늦은 오후, 해가 낮게 깔린 한 시간대. 일몰·야경 전환은 넣지 않음.
- **카메라**: 한 컷에 움직임 하나. 객실 안은 고정 또는 아주 느린 푸시인. 부감은 **수직 고정 부감**(탑다운)만 허용. 스윙하는 드론 비행은 금지.
- **렌즈 감각**: 객실 35~50mm, 수면 부감 장초점 압축, 강변 측면 트래킹 85mm. 광각 왜곡은 금지.
- **팔레트**
  - 강물 슬레이트 `#4E6470`: 수면, 그늘
  - 스틸 그레이 `#9AA3A8`: 다리 구조, 창틀
  - 살구빛 오후 `#E9B48A`: 햇빛, 피부 하이라이트(**유일한 따뜻한 색**)
  - 종이 아이보리 `#EEE9DF`: 타이포, 하늘 하이라이트
  - 그늘 먹색 `#1C2328`: 다리 밑, 4:3 구간의 좌우 어둠
- **질감**: 포트라 계열 필름처럼 부드러운 파스텔, 약한 35mm 그레인, 피부 결 유지. 청록 보정(teal & orange)과 HDR 과채도는 금지.
- **전광판 판독 규칙**: 소리 없이 3초만 봐도 **큰 형태(배·항적·빛줄기·화면비 변화)**가 읽혀야 함. 핵심 정보를 작은 표정에 맡기지 않음.
- **절대 금지**: 도시가 접히거나 변신하는 판타지 왜곡 / 실존 선박과 다른 선체 / 생성된 글자·간판·노선 표기 / 실존 지하철 노선 색·로고 / 시간대 급변 / 얼굴 반사 합성.

---

## 3. 내레이션 R3

차분한 30대 화자 한 명이 맡습니다. 전체 **네 문장**뿐입니다. 소리 없이 송출될 것을 고려해 같은 문장을 화면 문자로도 둡니다(편집 레이어 분리. 허용 범위는 §0 확인 후 확정).

```
한강은 늘, 건너는 강이었습니다.          (H01–H02)

오늘은, 따라갑니다.                    (H05)

                                     ── 화면비가 열리는 구간은 침묵 ──

서울은 그대로. 시선은 새롭게.            (H10)
한강버스.                             (H11)
```

- R2의 "서울이 뒤집혔습니다 / 달라진 건, 도시가 아니라 바라보는 자리"는 뺐습니다. 화면이 보여주는 것을 다시 말하는 문장이기 때문입니다.
- **화면 문자는 두 쌍으로 대구**를 이룹니다. H01 `건너는 강` ↔ H07 `따라가는 강`. 작은 크기로 화면 하단 1/3 지점에 둡니다. 소리 없는 전광판에서도 이야기가 성립하게 하는 최소 장치입니다.

---

## 4. 장면 구성 — 50초 / 11컷

구조: **가로지르기(4초) → 뒤집힌 거울과 배(8초) → 다리 그늘(14초) → 열림·따라가기(14초) → 거울 회수(5초) → 엔딩(5초)**

| 컷 · 시간 | 화면 / 카메라 | 내레이션 · 소리 | 화면 문자(편집) | 목적 |
|---|---|---|---|---|
| **H01** 0:00–0:03 | **지하철 객실 측면, 철교 위.** 승객들이 휴대폰을 봄. 창밖으로 한강이 빠르게 **가로질러** 지나가고, 트러스 구조물이 빛을 빠르게 끊음(빠른 스트로브). 카메라 고정, 움직임은 창밖뿐. | N1 "한강은 늘, 건너는 강이었습니다." / 철교 위 레일 소리 | `건너는 강` | 서울 사람의 공통 경험으로 첫 훅. **화면 가로 방향의 빠른 움직임**으로 '건넘'을 각인. 우울하게 그리지 않음(밝은 오후, 평범한 일상) |
| **H02** 0:03–0:06 | **수직 고정 부감.** 잔잔한 수면에 다리와 고층 스카이라인이 **거꾸로** 비침. 수평선은 프레임 밖. 아주 미세한 잔물결. | 레일 소리가 잘리고 **정적 + 물 소리**(사운드 컷이 화면 컷보다 먼저 옴) | — | 낯설게 보기. "뒤집힌 서울"을 말 없이 보여줌 |
| **H03** 0:06–0:11 | **★ 같은 부감. 한강버스 선수가 프레임 아래에서 진입**해 거꾸로 선 도시를 가르며 지나감. 항적의 V자 물결이 반사된 빌딩들을 접었다 펴듯 일렁이게 함. | 물을 가르는 소리, 낮은 엔진음 | — | **반사의 정체 공개 + 한강버스 공개를 한 컷에서 동시에.** 전광판에서 가장 강한 그래픽 이미지. 선박 외형은 기준자료와 일치해야 함 |
| **H04** 0:11–0:15 | **수면 높이 측면.** 카메라가 수면 30cm 위에 고정. 한강버스가 화면 **깊이 방향으로** 천천히 멀어지며 강을 따라 나아감. 뒤로 강변 아파트 스카이라인. | 물결이 렌즈 앞에서 찰랑이는 소리 | — | **축의 전환.** H01의 가로 움직임과 반대되는 '깊이 방향' 움직임. 제목 '강의 눈높이'의 시점 |
| **H05** 0:15–0:20 | 객실 안. 창가 승객(가상의 30대 성인) 뒷모습에서 옆모습으로 이어지는 구도. 무릎 위에 **휴대폰이 화면을 아래로 엎어져** 있음. 창밖에 다가오는 다리가 보임. | N2 "오늘은, 따라갑니다." / 객실 정적, 선체에 닿는 물 | — | H01(휴대폰 보는 승객들)과 대비. 이 사람은 바깥을 '만나러' 왔음 |
| **H06** 0:20–0:26 | **★ 다리 밑 진입. 코모레비 리듬.** 객실이 어두워지고, 다리 하부 구조물 사이로 새는 **빛줄기가 일정한 간격으로** 승객의 얼굴과 좌석을 쓸고 지나감. 밝은 창만 남아 화면이 **자연스러운 4:3**처럼 보임(좌우는 그늘 먹색). 카메라 고정. | 소리가 **낮고 울리게** 바뀜(다리 밑 공명), 물 소리가 교각에 반사됨 | — | 이 작품의 청각·시각 클라이맥스 1. 사건은 '빛'. 승객은 눈만 살짝 들어 올림 |
| **H07** 0:26–0:32 | **★ 오픈 매트 리빌.** 다리 그늘을 빠져나오는 순간, 객실에 빛이 들어차며 **4:3 → 16:9 전체로 화면이 열림.** 카메라가 창 쪽으로 아주 느리게 다가가고, 넓게 열린 강변 풍경이 화면 전체를 채움. | **음악이 처음 들어옴**(얇은 피아노 또는 기타 한 줄). 내레이션 없음 | `따라가는 강` | 클라이맥스 2. '새로운 서울'이 열리는 순간. 열린 뒤 바로 자르지 않고 3초 이상 유지 |
| **H08** 0:32–0:38 | **두루마리 트래킹.** 85mm 압축 측면 트래킹으로 강변 생활이 배의 속도로 옆으로 펼쳐짐. 둔치의 텐트, 자전거 타는 사람, 러너, 개와 산책하는 사람, 갈대와 억새, 그 뒤 아파트 스카이라인. 사람들은 작게. | 음악 + 멀리서 들리는 생활음(자전거 벨, 웃음소리 아주 작게) | — | 랜드마크가 아니라 **생활의 서울.** 다리 위나 지하철에서는 보이지 않던 높이와 속도 |
| **H09** 0:38–0:41 | 승객 옆얼굴 클로즈업. 오후 햇빛이 얼굴에 닿음. 미소를 요구하지 않음. 시선이 강변을 따라 천천히 이동함(눈만 움직임). | 음악 유지 | — | '만남'의 반응. 감정은 과하지 않게 |
| **H10** 0:41–0:46 | **★ 거울 회수(AI 네이티브 틸트).** H02와 같은 수직 부감. 항적이 가라앉으며 거꾸로 선 도시가 다시 온전해짐 → 카메라가 수면을 스치며 **위로 틸트**해 실제 도시가 바로 선 모습으로 끝남. 멀어지는 한강버스가 화면 안에 남음. | N3 "서울은 그대로. 시선은 새롭게." / 음악이 가라앉음 | — | 반사(뒤집힘)를 바로 세우며 마무리. "그대로"와 "새롭게"를 한 동작으로 증명 |
| **H11** 0:46–0:50 | 잔잔한 강물 위 엔드카드. 카피와 브랜드. | N4 "한강버스." / 물 소리 하나로 끝 | 중앙: `서울은 그대로. 시선은 새롭게.` / 아래: `한강버스`(공식 로고는 허용 확인 시에만) | 브랜드 각인 |

### 컷 길이 메모
- 24fps 기준 프레임 구간: H01 0–72, H02 72–144, H03 144–264, H04 264–360, H05 360–480, H06 480–624, H07 624–768, H08 768–912, H09 912–984, H10 984–1104, H11 1104–1200.
- 내레이션 녹음이 길어지면 **H09를 먼저 삭제**합니다(47초). H06과 H07은 줄이지 않습니다.

---

## 5. Google Flow 제작 파이프라인

### 원칙
- **모든 화면을 Flow 안에서 생성**합니다. 순서는 Flow 이미지 생성으로 키프레임 → **Frames to Video**(시작·끝 프레임) / **Ingredients to Video**(선박·인물·객실 일관성) → 필요할 때 **Extend**입니다.
- 한글·로고는 Veo가 깨뜨리므로 **편집 단계에서만** 넣습니다(허용 범위는 §0 확인).
- Veo 3.1 생성 오디오는 앰비언스 참고용으로만 씁니다. 최종 사운드는 편집에서 믹스합니다.
- Flow에서 1080p로 업스케일해 내려받습니다. 16:9로 생성합니다.
- **4:3 구간(H06)**은 조명 연출로 만드는 것이 1순위입니다. 어두운 객실과 밝은 창의 대비로 자연스러운 4:3을 만듭니다. 이것이 안 되면 편집에서 검은 매트를 열고 닫는 방식으로 대체합니다. 다만 '모든 시각 장면 AI 생성' 조항과 충돌하는지 확인한 뒤에만 씁니다.

### 기준 Ingredients (먼저 잠글 것)
| ID | 내용 | 비고 |
|---|---|---|
| ING-BOAT | 한강버스 선박 외형(측면·부감) | 실사 사진을 참조 이미지로 넣어도 되는지 §0에서 확인. 안 되면 공식 사진을 **보고 묘사한 텍스트**로 Flow에서 생성하고, 공식 사진과 나란히 비교 검수 |
| ING-CABIN | 창가 좌석·창틀 구조 | 한 가지 모델로만 고정 |
| ING-PAX | 가상 승객 캐릭터 시트(정면·측면·뒷모습, 같은 의상) | 무채색 코트, 장신구 없음 |
| ING-RIVER | 늦은 오후 수면·스카이라인 톤 | H02·H03·H10 공용 |

### 생성 순서 (위험한 것부터)
1. **H03 부감 + 선박 진입.** 선박 형태가 무너지지 않는 컷을 먼저 확보합니다. 실패하면 작품 성립 자체가 흔들립니다.
2. **H06 → H07 다리 그늘 → 열림.** Frames to Video로 시작 프레임(그늘 속 4:3 느낌)과 끝 프레임(밝게 열린 객실)을 지정합니다.
3. **H10 거울 회수 틸트업.** 시작은 H02 키프레임, 끝은 실제 스카이라인 키프레임으로 두고 Frames to Video를 씁니다.
4. H04, H05, H09 (ING-BOAT·ING-CABIN·ING-PAX 사용)
5. H01 지하철, H08 두루마리 트래킹, H02 정지 부감

### 공통 스타일 블록
```
STYLE LOCK: quiet observational cinema in Seoul, mid-October late afternoon with low warm sun,
soft pastel film palette like Kodak Portra 400, slate-blue river water, steel-grey bridge structures,
apricot sunlight as the only warm color, natural skin texture, subtle 35mm film grain, gentle contrast.
Locked-off or very slow steady camera, one camera move per shot, realistic scale and physics.
No text, no letters, no readable signage, no logos, no subway line colors, no fantasy distortion,
no swooping drone moves, no teal-and-orange grading, no lens-flare overload.
```

### 컷별 프롬프트 초안 (영문, Flow 입력용)

**H03: 부감 거울 + 선박 진입 (최우선)**
```
[STYLE LOCK] Use the boat from the reference image exactly; do not change its hull shape or colors.
Perfectly top-down locked-off overhead shot of the calm Han River surface. The water mirrors an
upside-down reflection of a long bridge and distant high-rise apartment skyline with soft blue sky.
From the bottom edge of the frame, the bow of the passenger ferry slowly enters and glides upward
through the reflection. Its V-shaped wake ripples bend and fold the reflected buildings, which then
gently re-form behind it. Calm, precise, no other boats.
```
검수: 선체 좌우 대칭 붕괴, 선체가 물에 녹아드는 현상, 반사 속 도시가 실제 하늘처럼 보이는 현상 중 하나라도 있으면 탈락.

**H06: 다리 밑 빛줄기 (Frames to Video 시작부)**
```
[STYLE LOCK] Use the cabin and passenger from the reference images.
Inside the ferry cabin passing under a large steel bridge. The cabin becomes dark; only the bright
window rectangle remains, so the frame reads almost like a 4:3 picture with deep shadow at both sides.
Regular bands of sunlight slip through gaps in the bridge structure and sweep slowly across the seated
passenger's face and the seat backs in a steady rhythm. The passenger stays still and only lifts
their eyes slightly. Locked-off camera.
```

**H07: 열림 (끝 프레임 → 이어서 생성)**
```
[STYLE LOCK] Continue from the start frame. The ferry exits the shadow of the bridge; warm afternoon
light floods the cabin from the windows, the dark edges of the frame fill with light, and the wide
riverbank opens across the full width of the frame. Very slow push-in toward the window.
The passenger, window frame and seats stay identical.
```

**H10: 거울 회수 틸트업**
```
[STYLE LOCK] Start: top-down view of the calm river reflecting the upside-down skyline, a faint wake
settling. The camera continuously tilts upward, skimming just above the water surface, until the real
skyline stands upright across the horizon, with the ferry small in the middle distance moving away.
One seamless move, no cut, physically plausible light.
```

**H01: 철교 위 지하철**
```
[STYLE LOCK] Side view inside a modern subway car crossing a steel truss bridge over a wide river
in the afternoon. Passengers sit looking at their phones, ordinary and calm. Through the windows the
river rushes past horizontally and the truss beams strobe the light quickly across the car.
Locked-off camera. No line colors, no signage, no text on screens.
```

**H08: 두루마리 트래킹**
```
[STYLE LOCK] 85mm compressed lateral tracking shot from a ferry moving along the river at water level.
The riverbank park scrolls past like a horizontal scroll painting: small tents on the grass, people
cycling, a runner, a person walking a dog, silver pampas grass, and beyond them a calm line of
high-rise apartments. People are small in frame. Smooth, constant speed.
```

**H02 / H04 / H05 / H09**: STYLE LOCK + §4 화면 설명을 영문으로 옮겨 씁니다. H05의 휴대폰은 `phone placed face-down on the lap, screen hidden`으로 명시합니다.

---

## 6. 리스크와 대안

| 리스크 | 신호 | 대안 |
|---|---|---|
| 선박 외형 불일치 | 선체 모양·창 배열이 컷마다 다름 | ING-BOAT를 모든 선박 컷에 고정. 그래도 흔들리면 선박을 **원경 실루엣 위주**로 줄이고, H03 한 컷에서만 크게 보여줌 |
| 4:3 효과가 안 생김 | 객실 벽이 밝게 보여 그냥 16:9로 읽힘 | 프롬프트에 `deep black cabin interior, only window lit` 강조. 실패하면 편집 매트(§5 원칙의 조건부 대체안) |
| 빛줄기가 플래시·스트로브 조명처럼 보임 | 빛이 깜빡임 | `slow sweeping bands of sunlight`로 표현하고 속도를 낮춤. 간격은 일정하게 |
| 틸트업에서 도시가 변형됨 | 반사와 실제 도시의 건물 배치가 다름 | 끝 프레임을 H02 반사 이미지를 **상하 반전한 것을 기준**으로 생성해 배치를 맞춤 |
| 실외 전광판에서 안 읽힘 | 소리 없이 봤을 때 이야기가 안 잡힘 | 지인 3명에게 **음소거 + 휴대폰 화면 크기**로 블라인드 시청. "배를 타고 강을 따라가는 이야기"라고 말하면 통과 |
| 지하철 장면이 브랜드 대비 공격처럼 보임 | 지하철을 답답하게 그림 | H01을 밝고 평범하게 유지. 건너는 것이 나쁜 게 아니라 **늘 그것뿐이었던** 것 |

---

## 7. 원본·이력 관리

```
hangang-bus/
  01_keyframes/   H01~H11 확정 키프레임 + ING 시트 (Flow 생성 원본)
  02_clips/       Flow 원본 MP4 (예: H06_R2_take3.mp4)
  03_prompts.md   컷별 최종 프롬프트 + 사용 기능(Frames/Ingredients/Extend) 기록
  04_audio/       내레이션, 앰비언스
  05_edit/        편집 프로젝트, 최종 MP4, 문자 레이어 분리본
```
'모든 시각 장면 AI 생성' 증빙을 위해 Flow 프로젝트를 삭제하지 않고 유지합니다.

---

## 8. 일정 (D-17, 고성 공모전 10/19 마감과 병행)

| 날짜 | 작업 |
|---|---|
| 10/4–5 | **공고 원문·첨부 요강 확보**(§0의 ⚠ 항목). ING 시트 4종 잠금 |
| 10/6–7 | H03 확정 (고성 C06과 같은 날 병행) |
| 10/8–10 | H06→H07, H10 Frames to Video |
| 10/11–12 | H01·H04·H05·H08·H09·H02 |
| 10/13 | 내레이션 → 가편집 |
| 10/14–16 | 고성 마감 집중 (한강버스는 재생성만) |
| 10/17–18 | 사운드 믹스, 문자 레이어, 음소거 블라인드 테스트 |
| 10/19 | 최종본 + 원본 패키징 |
| 10/20 | **제출** (마감 1일 전) |

---

### 참고 자료
- 2025 한강버스 숏폼 공모전(생성형 AI 제외 조건, 혼동 방지용): [내 손안에 서울](https://mediahub.seoul.go.kr/hangangbus)
- 2026 AI 영상·광고 트렌드: [LTX — AI Video Trends](https://ltx.io/blog/ai-video-trends), [Envato — Motion Design Trends 2026](https://elements.envato.com/learn/motion-design-trends), [Envato — Advertising Trends 2026](https://elements.envato.com/learn/advertising-trends), [Awakened Films — Video Marketing Trends 2026](https://awakenedfilms.com/video-marketing-trends-for-2026/)
- Flow 기능(Frames to Video·Ingredients·Extend·오디오): [Google 블로그 — Veo 3.1 updates in Flow](https://blog.google/innovation-and-ai/products/veo-updates-flow/)
- 연출 레퍼런스: 빔 벤더스 〈퍼펙트 데이즈〉(2023), 자비에 돌란 〈마미〉(2014). 구도·장면은 복제하지 않고 문법만 참고
