# 바삭숏 — 로드스터 흡착팬·냉가스 편 · 대본 후보 2안

> 9:16 · 40초 · 4초 클립 × 10 · Google Flow(Veo) 단독 파이프라인
> LOCK 본문은 `prompts/LOCKS.md`에 있다. 프롬프트에는 태그만 붙인다.

---

## 0. 소재 선별

원문 소재를 바삭숏 기준(첫 2초 충격 컷, 40초 안에 한 문장 논지, 일상 체감, 쾌감 컷, 화면으로 증명 가능)으로 걸렀다.

| 원문 항목 | 판정 | 이유 |
|---|---|---|
| 블랙아이스 긴급 제동 | **✅ 1안 핵심** | 누구나 겪는 공포다. 11~12월 결빙철 직전이라 지금 올리기 좋다. 제동거리는 숫자 한 개로 바로 보여줄 수 있다 |
| 고속버스·트럭 전복 방지 | ✅ 1안 클라이맥스 | 판이 크다. 다만 실제 연구 사례가 없어서 '이론상'으로만 말한다 |
| 오토바이 슬립 방지(보쉬) | ✅ 1안 증거 컷 | **실제 시제품**(2018)이라 영상 전체의 신뢰를 받쳐준다 |
| 교량 하부·터널·댐 점검 로봇 | **✅ 2안 핵심** | 천장에 거꾸로 붙은 기계라는 훅이 강하고, 고압 세척 쾌감 컷을 넣을 수 있다 |
| 선박 외판 따개비 제거 | ⚠️ 2안에서 비중 축소 | 강철 선체는 이미 **자석 크롤러**가 흔하다. "흡착팬이라서 된다"는 논리가 약하다 → 2안에서는 오히려 "철판엔 자석, 콘크리트엔 팬"이라는 대비로 쓴다 |
| 철도 점착력 | ❌ 제외 | 축중·점착 개념을 먼저 설명해야 해서 40초에 안 들어간다. 따로 철도 편으로 만들 만하다 |
| 수직 물류 AGV / UAM 착륙 | ❌ 제외 | 실물 사례가 약하고, 화면이 미래 도시 CG처럼 흘러가기 쉽다 |
| 달·소행성 로버 | ❌ 제외 | 체감이 멀다. 시리즈로 이어갈 때 쓸 수 있다 |

### 사실 확인 메모 (대본에 들어간 것만)
- **테슬라 신형 로드스터 공개 = 2026-10-15**, 텍사스 SpaceX 시험장(보도에 따라 Waco 또는 McGregor). 흡착팬으로 곡면 램프 **천장을 거꾸로 주행**했고, 냉가스 스러스터로 공중에서 돌고 착지했으며, 주차된 차량들을 뛰어넘었다. 트림은 Performance(팬만), Thrust(후방 냉가스 추가), Rocket(둘레 전체 스러스터, 초청 한정). 비행 기능은 공도 승인이 없다. → 내레이션에서는 "10월 15일 공개" 정도만 말하고 가격·0-60 수치는 쓰지 않는다(보도마다 다르다).
- **보쉬 '슬라이딩 미티게이션'**: 2018년 시제품. 옆으로 미끄러지는 것을 감지하면 에어백용 냉가스 발생기(아르곤·헬륨)를 노즐로 분사해 차체를 되돌린다. 한 번 쓰면 교체나 재충전이 필요하고, 양산 계획은 발표되지 않았다.
- **맥머트리 스피어링**: 정지 상태에서 팬으로 약 2,000kg의 다운포스를 낸다고 **회사가 밝혔다**. 2025년 회전 리그 위에서 거꾸로 붙은 채 주행했다. 독립 검증은 없으므로 "회사 발표" 화법으로만 쓴다.
- **제동거리(1안 INFO 수치)**: 50km/h, 반응시간 제외, d = v²/(2μg)로 계산했다.
  - 건조 μ≈0.8 → **약 12m** / 빙판 μ≈0.1 → **약 98m** (8배)
  - 누르는 힘 2배 → **약 49m**
  - 실제 타이어는 누르는 힘이 커질수록 μ가 조금 떨어진다(하중 민감도). 그래서 "절반 가까이"는 낙관적인 값이다. 내레이션은 "이론상"으로 말한다.
- **쓰지 않은 원문 수치**: 120dB 폭음, 0.1초 분사, 수백 kg 탑재. 출처를 확인하지 못했다.

### 공통 연출 규칙
- 실존 차량을 재현하지 않는다. 로드스터는 `[ROADSTER LOCK]`(배지·로고 없는 일반형 실루엣)으로만 그린다. 테슬라 공식 영상은 저작권 때문에 쓰지 않는다.
- 한글은 **편집에서만** 넣는다. INFO에는 숫자·단위만 있고, 장면당 수치는 0~1개다.
- **쌍 컷은 순차로 생성한다.** A를 확정한 뒤 A를 참조로 첨부해 B를 돌린다. 각 안의 생성 순서는 §3에 있다.

---

## 1안 — 《브레이크가 안 듣는 길》 · 도로 위 대형사고 방어

**한 문장 논지**: 빙판에서 차가 안 서는 건 '누르는 힘'이 모자라서다. 흡착팬은 그 힘을 직접 만든다.

**제목 후보**
1. 빙판길에서 브레이크 밟아도 안 서는 진짜 이유
2. 테슬라가 차를 천장에 붙인 기술, 진짜 쓸모는 빙판길이다
3. 제동거리 98m를 49m로 줄이는 방법 (썸네일: 빙판 위 세단 + 금색 `98m → 49m`)

**구조**: 공포 훅(0~4) → 원인 숫자(4~8) → 뉴스 전환(8~12) → 원리(12~16) → 해결 쌍 컷(16~24) → 실증(24~28) → 클라이맥스(28~32) → 정직한 한계(32~36) → 첫 컷 구도로 회귀(36~40)

| KF · 시간 | 화면 / 카메라 | 내레이션 | 자막(편집) | INFO |
|---|---|---|---|---|
| **A01** 0:00–0:04 | 밤 빙판길. 회색 세단이 브레이크등을 켠 채 미끄러지고, 앞에 정차한 트럭 후미가 커진다. 세단 뒤 낮은 위치에서 느린 푸시인 | 빙판길에선 브레이크를 끝까지 밟아도, 차가 안 섭니다. | 밟았는데 안 선다 | 없음(CLEAN만) |
| **A02** 0:04–0:08 | 얼음 위 타이어 접지면 극접사. 바퀴는 잠겼는데 차는 계속 미끄러진다 | 타이어가 길을 붙잡는 힘이, 마른 길의 8분의 1로 떨어지니까요. | 붙잡는 힘 1/8 | 백색 얼음면 위 짧은 적색 마찰 화살표, 금색 `98 m` |
| **A03** 0:08–0:12 | 황혼의 시험장. 로드스터가 곡면 램프를 타고 올라 **천장에 거꾸로 붙은 채** 지나간다. 측면 고정 | 그런데 지난 10월 15일, 테슬라가 차를 천장에 붙여 달리게 했습니다. | 10월 15일 공개 | 없음 |
| **A04** 0:12–0:16 | 로드스터 하부 로우앵글. 바닥 팬이 돌고 먼지가 차 밑에서 뒤로 빨려 나간다. 차체가 살짝 내려앉는다 | 바닥 공기를 빨아내 차를 땅에 짓누르는 팬, 그리고 가스를 뿜어 차를 직접 미는 분사구. | 흡착팬 + 냉가스 | 청록 유선이 차 밑에서 뒤로 빠짐, 적색 하향 화살표 3개 |
| **A05** 0:16–0:20 | **A01과 같은 빙판, 같은 세단.** 이번엔 세단 하부에서 팬이 돈다. 서리 가루가 차 밑으로 빨려 들고 차체가 눌린다 | 이걸 빙판길에 쓰면? 누르는 힘이 두 배면, 같은 얼음에서도 붙잡는 힘이 두 배. | 누르는 힘 ×2 | 적색 하향 화살표, 금색 `×2` |
| **A06** 0:20–0:24 | **A01 쌍 컷(구도 동일).** 세단 앞범퍼 아래에서 짧은 가스 분사가 나오고, 세단은 트럭 후미 앞 넉넉한 거리에서 멈춘다 | 앞에서 가스를 뿜어 뒤로 밀면, 이론상 제동거리는 절반 아래로. | 98m → 49m | 차와 트럭 사이 빈 노면에 금색 `49 m`, 청록 분사 흐름 |
| **A07** 0:24–0:28 | 젖은 산길 코너. 오토바이 앞바퀴가 옆으로 미끄러지는 순간, 차체 옆 노즐에서 흰 가스가 터지고 오토바이가 라인으로 돌아온다 | 실제로 보쉬는 2018년, 미끄러지는 오토바이를 가스 분사로 세우는 시제품을 공개했습니다. | 보쉬 2018 시제품 | 청록 분사 화살표 1개(바깥쪽), 적색 미끄럼 화살표 1개 |
| **A08** 0:28–0:32 | **★ 쾌감 컷.** 강풍 부는 사장교 위 고속버스가 바람 쪽으로 기운다. 지붕 옆선에서 흰 가스가 한 번에 터지고 버스가 다시 선다. 측면 망원 고정, 분사 순간에 0.5초 슬로 | 다리 위 강풍에 기우는 고속버스도, 위쪽 옆구리에서 가스를 뿜으면 다시 세울 수 있습니다. | 기울기 직전 한 방 | 적색 바람 화살표, 청록 분사 화살표가 반대쪽으로 |
| **A09** 0:32–0:36 | 세단 하부 단면 느낌의 실사 컷. 트렁크 밑 고압 탱크 두 개와 배관. 느린 패닝 | 다만 탱크는 몇 초면 바닥나고, 분사음은 폭음 수준. 늘 켜두는 장치는 아닙니다. | 몇 초짜리 장치 | 담청 지시선 1개가 탱크에 |
| **A10** 0:36–0:40 | 대시보드 에어백이 터지는 슬로모션 → 매치컷으로 **A06의 멈춘 세단** 와이드. 천천히 풀백 | 에어백처럼, 사고 직전 2초만 일하는 장치. 슈퍼카 묘기가 아니라, 다음 안전장치일지 모릅니다. | 사고 직전 2초 | 없음 |

**편집 호흡** (내레이션은 클립당 30~35음절 기준. 녹음 후 넘치는 줄부터 줄인다)
- A01은 0.3초 안에 미끄러지는 움직임이 시작돼야 한다. 정지 프레임으로 시작하지 않는다.
- A03은 이 편에서 유일하게 '구경거리'인 컷이다. 음악 드롭을 여기 둔다.
- A05~A06은 A01과 구도가 같아 **같은 장소에서 결과만 바뀌는** 쾌감을 준다. 클립 경계에서 화면이 튀지 않게 맞춘다.
- A08 분사 순간은 효과음을 크게(가스 '팡'), 그 직후 0.3초는 무음.

---

## 2안 — 《자석이 안 붙는 벽》 · 극한 토목 중장비

**한 문장 논지**: 다리·터널·댐은 콘크리트라 자석이 안 붙는다. 그래서 공기로 붙는다.

**제목 후보**
1. 강 위 다리 밑바닥에 거꾸로 붙어 다니는 기계의 정체
2. 자석도 안 붙는 콘크리트 천장에 기계가 어떻게 매달려 있을까
3. 테슬라가 차를 천장에 붙인 원리, 다리 밑에선 이미 쓰고 있다

> 원래 후보였던 "200m 대교 천장", "수백 킬로 기계", "선박 외벽"은 뺐다. 수치 근거가 없고, 강철 선체는 자석 장비가 주력이라 논지와 어긋난다.

**구조**: 기묘한 훅(0~4) → 뉴스 연결(4~8) → 원리(8~12) → 실증 2톤(12~16) → 왜 드론은 안 되나(16~20) → 왜 자석은 안 되나(20~24) → 점검(24~28) → **쾌감 컷 세척(28~32)** → 확장(32~36) → 한계 + 회귀(36~40)

| KF · 시간 | 화면 / 카메라 | 내레이션 | 자막(편집) | INFO |
|---|---|---|---|---|
| **B01** 0:00–0:04 | 강 위 고속도로 교량 밑면. 주황색 로봇이 콘크리트 천장에 **거꾸로 붙어** 굴러간다. 카메라는 아래에서 올려다보며 느린 틸트 | 강 위 수십 미터, 다리 밑바닥에 거꾸로 붙어서 달리는 기계. | 이거 왜 안 떨어짐? | 없음 |
| **B02** 0:04–0:08 | A03과 같은 로드스터 천장 주행 컷(공용 KF) | 지난 10월 15일, 테슬라가 차를 천장에 붙여 달린 것과 같은 원리입니다. | 같은 원리 | 없음 |
| **B03** 0:08–0:12 | 로봇 극접사. 등의 팬이 돌고, 스커트 가장자리의 먼지가 안쪽으로 빨려 든다 | 몸 밑 공기를 빨아내면, 바깥 공기가 기계를 벽 쪽으로 꾹 눌러줍니다. | 공기가 눌러준다 | 청록 유선이 팬으로 빠져나감, 적색 화살표가 로봇을 벽으로 |
| **B04** 0:12–0:16 | 맥머트리식 팬카가 회전 리그 위에 거꾸로 붙어 있다(일반형, 로고 없음) | 영국 맥머트리는 이 방식으로, 멈춘 채 2톤을 눌러 붙인다고 밝혔죠. | 정지 상태 2톤 | 금색 `2000 kg` |
| **B05** 0:16–0:20 | 교량 아래 바람 속에서 흔들리는 점검 드론. 같은 공간, 측면 와이드 | 드론은 다리 밑 바람에 흔들리고, 무거운 장비를 오래 못 듭니다. | 바람·배터리 | 적색 바람 화살표 1개 |
| **B06** 0:20–0:24 | 쌍 컷 느낌: 강철 선체를 자석 크롤러가 타는 장면 → 같은 크롤러가 콘크리트 벽에서 미끄러져 떨어지는 장면(2클립 각 2초) | 철판이면 자석으로 붙지만, 다리·터널·댐은 콘크리트. 자석이 안 붙습니다. | 콘크리트엔 자석 X | 없음 |
| **B07** 0:24–0:28 | 로봇이 교량 밑면 균열 위에 멈추고, 센서 팔을 균열에 대고 스캔한다 | 그래서 공기로 붙어서, 천장의 금을 바로 앞에서 들여다봅니다. | 균열 직접 점검 | 주황 균열 하이라이트, 지시선 1개 |
| **B08** 0:28–0:32 | **★ 쾌감 컷 3초+.** 댐 수직벽을 로봇이 위에서 아래로 내려오며 고압수를 쏜다. 검푸른 이끼 벽에 **깨끗한 회색 띠**가 한 번에 생긴다. 정면 고정 | 수직 댐 벽은 비계 없이, 위에서부터 쭉 씻어 내립니다. | 비계 없이 | 담청 물줄기 강조만(수치 없음) |
| **B09** 0:32–0:36 | 터널 천장을 따라가는 로봇 → 풍력 블레이드 표면의 로봇 (2초 + 2초) | 터널 천장, 풍력발전기 날개까지. 크레인 대신 로봇 한 대. | 크레인 대신 | 없음 |
| **B10** 0:36–0:40 | **B01 구도 회귀**: 다리 밑 로봇, 위로 차들이 지나가는 소리와 그림자. 노란 안전줄이 보이게 풀백 | 팬이 멈추면 떨어지니 안전줄은 필수. 천장을 달린 그 기술, 진짜 무대는 다리 밑입니다. | 진짜 무대는 다리 밑 | 담청 지시선 1개가 안전줄에 |

> **B04 길이 조정**: B04를 빼면 36초가 되고 논지는 그대로 선다. 40초를 넘기면 가장 먼저 B04를 자른다.

**편집 호흡**
- B01은 거꾸로 매달린 그림이 0.5초 안에 읽혀야 한다. 강물이 화면 안에 보이면 높이가 저절로 전달된다.
- B06은 '붙는다 → 떨어진다'를 2초씩 끊는다. 떨어지는 소리(쿵)는 크게 넣는다.
- B08이 이 편의 승부처다. 세척 띠가 화면을 가로지르는 3초 동안 내레이션을 짧게 하고, 물소리를 크게 키운다.

---

## 1안 vs 2안 — 추천

| 기준 | 1안 도로 | 2안 토목 |
|---|---|---|
| 첫 2초 훅 | 빙판 미끄러짐(공포, 공감) | 거꾸로 매달린 기계(기묘함) |
| 체감도 | **매우 높음.** 운전자라면 다 안다 | 중간 |
| 시의성 | **결빙철 직전 + 공개 3일 차** | 공개 3일 차 |
| 쾌감 컷 | 버스 분사 1컷 | **댐 세척 3초**(중장년 남성 지속시간에 강함) |
| 사실 리스크 | 버스 전복 방지는 아이디어 수준이라 '이론상' 처리 필요 | 낮음. 흡착 로봇은 실제로 있다 |
| Veo 생성 난도 | 중: 쌍 컷 3장(A01·A05·A06) 구도 맞추기 | 상: '거꾸로' 방향이 자주 뒤집힘(B01·B03·B07·B10) |

**추천은 1안 먼저, 2안은 1~2주 뒤 후속편**이다. 이유는 셋이다.
1. 공개 직후라 검색 유입이 있고, 겨울 직전이라 "빙판"이 지금 가장 크게 먹힌다.
2. A03(로드스터 천장 주행)을 B02에서 그대로 다시 쓸 수 있다. 1안을 먼저 만들면 2안 비용이 줄어든다.
3. 2안의 "거꾸로 붙은 로봇"은 Veo에서 중력 방향이 뒤집히는 실패가 잦다. 1안을 만드는 동안 B01 테스트를 먼저 돌려 성공률을 확인해 두면 좋다.

---

## 2. CLEAN 키프레임 프롬프트

모든 프롬프트 끝에 `[STYLE LOCK]`을 붙인다. 화면을 영역(upper/lower/top/bottom)으로 나누지 않고, 카메라로부터의 거리로만 배치를 적는다.

### 1안

**A01 — 빙판 미끄러짐 (쌍 컷 기준 프레임, 가장 먼저 확정)**
```
[ICE ROAD LOCK] [CAR LOCK] [TRUCK LOCK]
Night. Low camera close behind the grey sedan, centered on the lane.
Nearest to camera the sedan slides forward with brake lights fully on and front wheels locked,
a faint smear of reflected light trailing behind its tyres on the black ice.
Beyond the sedan, a short run of glossy empty icy lane, and beyond that the stationary truck,
close enough to feel dangerous. That empty strip of ice between the sedan and the truck
is as important to this frame as the car itself.
[STYLE LOCK]
```

**A02 — 타이어 극접사**
```
[ICE ROAD LOCK]
Extreme close-up at road level of one front tyre of the grey sedan on clear black ice.
The tyre is not rotating, the tread is locked, yet the whole tyre is visibly sliding across
the glassy surface, fine ice crystals skittering away from the contact patch.
Clear empty ice surface stretches ahead of the tyre.
[STYLE LOCK]
```

**A03 — 로드스터 천장 주행 (2안 B02 공용)**
```
[RAMP LOCK] [ROADSTER LOCK]
Side view, locked-off camera at a distance. The roadster is upside down on the ceiling section
of the curved ramp, wheels pressed against the concrete overhead, driving across it,
fine dust being pulled toward its floor. The dusk sky shows through the open ends of the ramp.
Clear open sky around the ramp.
[STYLE LOCK]
```

**A04 — 하부 팬**
```
[ROADSTER LOCK]
Very low ground-level camera looking under the roadster parked on a dusty concrete apron at dusk.
The round floor fan is spinning, loose dust and small dry leaves stream from under the sides of the car
toward the fan opening and blow out behind. The body sits visibly lower on its suspension.
[STYLE LOCK]
```

**A05 — 흡착팬 작동 세단 (A01 참조 첨부, 순차)**
```
Reproduce the attached reference frame exactly: same camera position, height, lens, distance,
same road, same sedan, same truck, same light, same grade.
Change one thing only — beneath the sedan a fan is running: fine frost dust from the ice is being
pulled in under its side skirts and the car body sits clearly lower and pressed down onto the ice.
The car is still moving forward but steadier.
[STYLE LOCK]
```

**A06 — 정지 성공 (A05 참조 첨부, 순차)**
```
Reproduce the attached reference frame exactly: same camera position, height, lens, distance,
same road, same sedan, same truck, same light, same grade.
Change one thing only — the sedan has come to a full stop well back from the truck,
a short soft burst of white gas venting forward from under its front bumper and fading.
A long clear stretch of empty ice now lies between the sedan and the truck.
[STYLE LOCK]
```

**A07 — 오토바이 슬립 복구**
```
A wet mountain road corner in grey daylight. A sport-touring motorcycle with rider, leaning into the bend,
its front tyre sliding sideways on the wet asphalt. A sharp white jet of gas bursts sideways from a nozzle
on the outer side of the bike, pushing it back toward its line. Camera low on the outside of the corner,
panning slightly with the bike. Open wet road ahead of the bike.
[STYLE LOCK]
```

**A08 — 버스 전복 직전 복원 (쾌감 컷)**
```
[BRIDGE DECK LOCK] [BUS LOCK]
Long-lens side view of the coach on the bridge deck, crosswind from the left.
The coach is tilted visibly away from the wind, its right-side wheels starting to lighten.
A powerful short white burst of gas fires sideways from nozzles along the upper edge of its roofline
on the leaning side, and the coach is pushed back level. Rain streaks across the frame.
Clear space above and around the coach.
[STYLE LOCK]
```

**A09 — 고압 탱크**
```
[CAR LOCK]
The grey sedan lifted on a workshop hoist, camera looking up at its rear underbody.
Two long cylindrical carbon-wrapped high-pressure gas tanks are mounted under the boot floor
with short braided lines running forward. Clean workshop light. Slow lateral camera move.
[STYLE LOCK]
```

**A10 — 에어백 → 회귀**
- A10a: `Interior of the grey sedan, dashboard airbag bursting open in extreme slow motion, soft daylight. [STYLE LOCK]`
- A10b: A06 확정 이미지를 그대로 첫 프레임으로 쓰고 Frames to Video에 `slow pull-back, the sedan stays stopped, the gas has fully faded`.

### 2안

**B01 — 교량 밑면 거꾸로 주행 (최우선 테스트)**
```
[BRIDGE UNDERSIDE LOCK] [ROBOT LOCK]
Camera far below, looking straight up at the concrete underside of the bridge deck.
The orange crawler is pressed flat against that concrete ceiling, its wheels on the concrete,
its back and fan facing down toward the camera, rolling slowly along an expansion joint.
The river is visible at the edge of the view beyond the bridge piers, showing the height.
The crawler is clearly upside down relative to gravity, holding on by suction.
Wide open concrete ceiling ahead of the crawler.
[STYLE LOCK]
```
실패하면: 로봇이 상판 **위**에 올라가 있으면 즉시 탈락이다. 다음 라운드에는 `the wheels touch the concrete that is ABOVE the crawler`를 추가한다.

**B03 — 흡착 극접사**
```
[ROBOT LOCK]
Close-up of the crawler pressed against a vertical grey concrete wall. The fan on its back spins,
a faint ring of dust at the edge of its flexible skirt is being drawn inward under the body.
Plain concrete surrounds the crawler with space on all sides.
[STYLE LOCK]
```

**B04 — 팬카 거꾸로**
```
A low single-seat fan-assisted electric hypercar with no badges and no logos, fixed upside down
to the underside of a large rotating steel test rig inside a bright workshop, fan exhaust visible at the rear.
Side view, locked-off.
[STYLE LOCK]
```

**B05 — 흔들리는 드론**
```
[BRIDGE UNDERSIDE LOCK]
Side view beneath the bridge. A small grey quadcopter inspection drone hovers close below the concrete deck,
visibly buffeted and tilting in gusting wind, a camera gimbal under it. Open space around the drone.
[STYLE LOCK]
```

**B06 — 자석 크롤러 대비 (2클립)**
- B06a: `A magnetic crawler with four steel-rimmed magnetic wheels climbing the vertical steel hull of a cargo ship in dry dock, rust patches, daylight. [STYLE LOCK]`
- B06b: B06a를 참조로 첨부. `Same crawler, same camera framing, now on a vertical grey concrete wall: its wheels lose hold and it slides down and drops out of frame. [STYLE LOCK]`

**B07 — 균열 스캔**
```
[BRIDGE UNDERSIDE LOCK] [ROBOT LOCK]
Camera below, looking up close at the crawler holding on to the concrete underside.
Its front sensor arm touches a thin dark hairline crack running across the concrete.
Clear concrete around the crack on both sides.
[STYLE LOCK]
```

**B08 — 댐 세척 (쾌감 컷, 4초 꽉)**
```
[DAM LOCK] [ROBOT LOCK]
Frontal locked-off view of the vertical dam face. The crawler holds on to the dam wall and moves slowly
downward while blasting a wide fan-shaped high-pressure water jet onto the concrete.
Behind it, a single sharp-edged clean pale grey stripe has been washed through the dark algae,
the stripe growing as the crawler descends. Mist and spray catch the morning light.
The dirty algae wall on both sides of the stripe fills the rest of the frame.
[STYLE LOCK]
```

**B09 — 터널 / 블레이드 (2클립)**
- B09a: `Inside a long concrete road tunnel, camera on the road looking up: the crawler drives along the tunnel ceiling, lights passing. [ROBOT LOCK] [STYLE LOCK]`
- B09b: `The crawler holding on to the curved white surface of an offshore wind turbine blade, sea far below, wind. [ROBOT LOCK] [STYLE LOCK]`

**B10 — 회귀**
- B01 확정 이미지를 참조로 첨부. `Reproduce the attached reference frame, then slow pull-back revealing the yellow safety tether running from the crawler to an anchor on the pier, shadows of passing cars on the deck edge. [STYLE LOCK]`

---

## 3. 생성 순서 (위험도 순)

**1안**
1. **A01 → A05 → A06** 순차(쌍 컷, 병렬 금지). A01이 확정되기 전에는 A05를 돌리지 않는다.
2. A03 (2안 공용) → A04
3. A08 (쾌감 컷, 분사 방향 검수: 기우는 쪽 상단에서 바깥으로 쏴야 한다)
4. A02, A07, A09, A10a
5. INFO 패스: A02, A04, A05, A06, A07, A08, A09 (A01, A03, A10은 CLEAN만)

**2안**
1. **B01** 5~10장 → 중력 방향 성공률 확인. 3라운드 안에 안 나오면 B01을 "벽면 수직 주행"으로 낮추고 제목 1을 버린다.
2. B08 (쾌감 컷) → B07 → B10 (B01 참조)
3. B06a → B06b 순차
4. B03, B04, B05, B09

### 검수 포인트 (이 편 전용)
- **분사 방향**: 냉가스 흰 기둥은 미는 방향의 **반대**로 뿜는다. A06은 앞으로 뿜고, A07과 A08은 기운 쪽 바깥으로 뿜는다. 반대로 나오면 불합격이다.
- **팬 위치**: A04와 A05의 팬은 차 **밑**에 있어야 한다. 지붕이나 뒤쪽 날개에 팬이 생기면 형상 드리프트다.
- **로고·배지**: 로드스터, 세단, 버스 어디에도 엠블럼이 보이면 불합격이다.
- **2안 중력 방향**: 바퀴가 콘크리트 **위쪽 면**에 닿아 있는지 본다.

---

### 출처
- 로드스터 공개: [TechCrunch](https://techcrunch.com/2026/10/15/tesla-reveals-spacex-powered-roadster-that-flies-and-falls-with-style/), [Electrek](https://electrek.co/2026/10/15/tesla-unveils-cyberfied-new-roadster-kickflip/), [CNBC](https://www.cnbc.com/2026/10/15/tesla-roadster-reveal-what-to-know-about-the-delayed-ev.html), [NBC News](https://www.nbcnews.com/tech/tech-news/elon-musk-shows-flying-tesla-roadster-years-delays-rcna603905)
- 보쉬 슬라이딩 미티게이션: [New Atlas](https://newatlas.com/bosch-motorcycle-side-thrusters/54676/), [The Drive](https://www.thedrive.com/motorcycles/21012/jet-thrusters-could-help-prevent-motorcycle-crashes-in-the-future)
- 맥머트리 스피어링: [McMurtry 공식](https://mcmurtry.com/upside-down-driving/), [The Drive](https://www.thedrive.com/news/watch-the-mcmurtry-speirling-fan-car-drive-upside-down)
