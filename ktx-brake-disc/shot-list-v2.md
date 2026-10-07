# KTX 차축 제동 디스크 숏폼 — 세부 장면 구성 v2 (Omni 1.1 최적화)

> v1(`scene-plan-v1.md`)의 내레이션·사실 확인 메모를 그대로 쓰고, **레퍼런스 이미지 2장**을 기준으로 컷을 세분화한 버전입니다.
> 55초 무한 루프 · 9:16 · 1080×1920 · 24fps · 키프레임 이미지는 Flow 이미지 편집 / 영상은 Omni 1.1 First & Last Frame

---

## 0. 레퍼런스 2장 검토

| | **REF-1 스튜디오 표본** | **REF-2 주행 현장** |
|---|---|---|
| 역할 | 해부 세계(설명 구간 전체)의 **형상 마스터** | 현실 세계(훅·루프 이음매)의 **분위기 마스터** |
| 강점 | 단색 그레이 배경(단면 경계가 가장 깨끗하게 나옴) · 외경에 **냉각 핀 개구부가 이미 보임**(S4 배기 컷에 그대로 활용) · 마찰면의 **청보라 템퍼 컬러**(열 이력을 말해 주는 디테일) · 노란 캘리퍼의 높은 대비 · 오른쪽 위 **공압 실린더와 호스**가 보임(S2 실린더 컷에 활용) | 로우앵글 + 바닥 모션 블러 = 300km/h 체감 · 원판 외곽의 붉은 발광 · 역광 하늘 · 첫 1초 정지율이 높은 그림 |
| **문제 1** | 원판 위아래에 **세로 분할선(이음매)**이 있음 → 보간 중 균열이나 쪼개짐으로 해석될 위험이 크고, S4 쿼터 단면과 겹쳐 혼란 | **캘리퍼 디자인이 REF-1과 다름**(은색 수직 블록) → 두 세계를 잇는 전환 컷에서 형상이 바뀌어 보임 |
| **문제 2** | 허브에 **깨진 글자**("HEFT J4-G0" 비슷한 각인) | **원판이 바퀴 바깥쪽**에 보임. KTX-I 객차 같은 TGV 계열 대차는 디스크가 **양쪽 바퀴 사이(안쪽)** 차축에 달림 |
| 문제 3 | 캘리퍼 외형이 자동차용 일체형에 가까움 → 내레이션 "집게처럼"과 시각적으로 맞지 않음 | 원판 주변 연기 → 이 이미지가 들어가는 클립은 역재생하면 연기가 빨려 들어감 |
| 정비 | **REF-1′**: 분할선 제거, 허브 각인 제거, 템퍼 컬러는 옅게 유지. 캘리퍼는 그대로 두고 **S2-c X-ray 컷에서 내부 레버(집게) 구조를 드러내** 내레이션과 맞춤 | **REF-2′**: 캘리퍼를 REF-1의 노란 캘리퍼로 교체(색·형태 통일). 원판 위치 문제는 **A안** 그대로 두되 화면 노출을 3초 이하로 / **B안** 차체 아래 궤도 중앙 시점으로 다시 생성(정확, 권장) |

> 두 이미지 모두 941×1672(9:16)입니다. **키프레임으로 쓰기 전에 1080×1920으로 업스케일**하고, 이후 파생되는 모든 KF를 같은 해상도로 맞춥니다. 해상도가 다르면 시작·끝 프레임 보간에서 크롭이나 줌이 생깁니다.

### 정비용 편집 프롬프트

**REF-1′** (Flow 이미지 편집, REF-1 첨부)
```
Keep the exact same camera, composition, lighting, objects and colors.
Remove the two vertical seam lines on the brake disc so the friction face is one continuous,
uninterrupted brushed-steel surface. Remove all engraved letters and numbers on the hub flange,
leaving plain machined metal with bolt holes. Keep the faint blue-purple heat-temper ring.
```

**REF-2′** (Flow 이미지 편집, REF-2 + REF-1′ 첨부)
```
Keep the exact same camera, composition, lighting, motion blur and train.
Replace only the silver brake caliper on the right side of the glowing disc with the mustard-yellow
cast brake caliper from the second reference image, with the same small silver pneumatic cylinder and
black air hoses, sized to fit the disc. Keep the disc glow exactly as it is. No text, no logos.
```

**REF-2′ B안** (정확도 우선, 새로 생성, REF-1′ 첨부)
```
Vertical 9:16 photoreal low-angle shot from the middle of the track, under a high-speed train
running at full speed, looking sideways at one wheelset: two wheels on the rails at the edges of frame,
the axle between them carrying ventilated brake discs, the nearest disc glowing orange-red at its rim,
gripped by a mustard-yellow caliper like the reference. Golden backlight, strong motion blur on sleepers
and ballast, sharp disc and caliper. No text, no logos.
```

---

## 1. 연출 콘셉트 — "두 세계, 한 원판"

- **현실 세계(REF-2′)**: 햇빛, 속도, 소음. 훅과 루프 이음매에만 등장.
- **해부 세계(REF-1′)**: 그레이 스튜디오, 정지된 표본. X-ray, 열, 단면, 기류 같은 CG가 모두 여기서 일어남.
- **월드 스위치**: 주행 장면이 순간 **정지(타임 프리즈)** → 원판·캘리퍼만 제자리에 남고 열차·선로·하늘이 회색 스튜디오로 벗겨짐. 이 클립을 영상 끝에서 **역재생**하면 스튜디오가 다시 주행 장면으로 돌아가며 **REF-2′와 같은 프레임으로 끝남** → 첫 컷과 픽셀 단위로 이어지는 루프.

### Omni 1.1 최적화 규칙 (모든 컷 공통)
1. **동작 하나 = 클립 하나.** 형태 변화(체결·발열·절개·전환) 중 하나만 넣음. 카메라는 FL 클립에서 무조건 고정.
2. **KF 쌍은 같은 캔버스에서 편집으로 파생.** 새로 생성한 두 장을 시작·끝에 넣으면 형상이 달라져 모핑이 생김.
3. **변화량 제한**: 한 클립에서 바뀌는 면적은 화면의 약 30% 이하가 안정적. 월드 스위치처럼 배경 전체가 바뀌는 컷은 **피사체 위치·크기를 완전히 고정**해 변화를 배경에만 몰아 줌.
4. **5초로 생성 → 편집에서 배속.** 1.5~4초 컷도 5초로 뽑고 **잘라내지 말고 배속**으로 줄임. 자르면 끝 프레임이 사라져 역재생 루프가 깨짐. *(콘솔이 지원하는 길이 단위는 직접 확인. 10초만 된다면 10초로 뽑아 2~4배속)*
5. **양 끝 정지(hold)**: 프롬프트에 "holds still for a moment at the start and at the end"를 넣거나, 편집에서 시작·끝 프레임을 4~6프레임 정지. 역재생 이음매에서 속도가 0이 되어 덜컥거리지 않음.
6. **역재생할 클립(★REV)은 불꽃·연기·입자·아지랑이 금지.** 이런 효과는 정방향 구간에서 CapCut 오버레이로만 추가.
7. **글자·숫자는 생성하지 않음.** HUD·라벨·화살표·지시선은 모두 CapCut.
8. **360p 초안 → 최종 해상도**: 초안은 동작과 형태 유지 여부만 판단하는 용도. 최종본은 최종 해상도에서 2~4개 뽑아 고름.

---

## 2. 컷 사이즈 배분

9:16 작은 화면에서는 와이드가 정보 전달력이 낮아 **CU·ECU 중심**으로 짜되, 공간을 알려 주는 와이드를 구간 경계마다 하나씩 둡니다.

| 사이즈 | 컷 | 합계 | 비율 | 용도 |
|---|---|---|---|---|
| **WS** (와이드) | 1-1, 1-2, 2-1, 5-5 | 11.5s | 21% | 현실 세계, 대차 전체 X-ray, 루프 이음매 |
| **MS** (미디엄) | 4-1, 4-4, 5-1 | 7.5s | 14% | 원판 전체 + 단면 개방, 측면 배기 |
| **MCU** (미디엄 클로즈업) | 2-3, 4-3, 5-2 | 8.5s | 15% | 캘리퍼 X-ray, 단면 기류 |
| **CU** (클로즈업) | 2-2, 3-1, 3-2, 4-2, 5-3 | 16.0s | 29% | 실린더, 원판 정면 발열, 열화상, 단면 구조 |
| **ECU / 매크로** | 2-4, 3-3, 3-4, 5-4 | 11.5s | 21% | 패드 접촉, 허브 체결부, 리듬 몽타주 |

**리듬 설계**
- 훅(0~6초): 와이드 2컷이지만 1-2는 같은 구도에서 세계만 바뀌는 연속 컷이라 실제 체감은 "와이드 → 변신".
- 설명 구간: **사이즈가 2단계 이상 점프**하도록 배열(WS → CU → MCU → ECU …). 같은 사이즈를 연속으로 쓰는 경우는 FL 연속 동작일 때만.
- 평균 컷 길이 약 2.9초. 훅과 엔딩 몽타주는 1~2.5초, 단면 설명은 3~4초로 길게 잡아 판독 시간을 확보.

---

## 3. 세부 컷 리스트 — 19컷 (생성 13 / CapCut 2 / 역재생 재사용 4)

배속 표기는 **원본 5초 클립 기준**입니다.

범례 — **FL**: First & Last Frame 보간 · **I2V**: 단일 이미지 → 영상 · **REV**: 기존 클립 역재생 · **POST**: CapCut 효과만 · **★REV**: 나중에 역재생으로 재사용되는 클립(불꽃·연기 금지)

### S1 훅 · 0:00–0:06 — "시속 300킬로로 달리는 KTX를 멈춰 세우는 건, 지름 64센티 쇠 원판입니다."

| 컷 | 시간 | 사이즈 · 앵글 | 생성 | 시작 KF → 끝 KF | 화면 · 동작 | CG — 생성 안 | CG — CapCut | SFX |
|---|---|---|---|---|---|---|---|---|
| **1-1** | 0:00–0:02.5 | **WS** 로우앵글, 광각 | FL (A→A) | REF-2′ → REF-2′ | 질주하는 열차, 바닥 블러가 흐르고 원판 외곽이 맥동하듯 빛남 | 모션 블러, 발광 맥동 | `300 km/h` 숫자가 0→300으로 빠르게 카운트(상단). 화면 가장자리 속도선 | Train Rush, Brake Screech 시작 |
| **1-2** ★REV | 0:02.5–0:06 | **WS** 동일 구도 | FL | REF-2′ → **KF-S0** | **타임 프리즈 → 월드 스위치.** 원판·캘리퍼·바퀴는 제자리에 고정, 열차·선로·하늘이 바깥쪽부터 회색 스튜디오로 벗겨짐 | 배경 전환(피사체 고정) | 시작 2프레임 흰 플래시 + 크로매틱 수차. 끝에서 원판 둘레에 원형 스트로크가 그려지며 `Ø 640 mm` | Time-Freeze Hit, Sub Drop, Reverse Whoosh |

- 1-1은 A→A가 거의 움직이지 않으면 **I2V(REF-2′)**로 대체. 그러면 1-1 끝과 1-2 시작 사이에 미세한 점프가 생기는데, 1-2 첫 프레임의 플래시와 "정지" 효과음으로 의도된 프리즈처럼 보이게 처리.
- 내레이션 "멈춰 세우는 건"의 "멈춰"에 프리즈 타이밍(0:02.5)을 맞춤.

### S2 체결 · 0:06–0:18 — "객차 바퀴축 하나에, 이 원판이 네 장. 제동이 걸리면 압축공기가 실린더를 밀고, 집게처럼 생긴 캘리퍼가 원판 양면을 꽉 물어버립니다."

| 컷 | 시간 | 사이즈 · 앵글 | 생성 | 시작 KF → 끝 KF | 화면 · 동작 | CG — 생성 안 | CG — CapCut | SFX |
|---|---|---|---|---|---|---|---|---|
| **2-1** | 0:06–0:09 | **WS** 3/4 부감 | FL | KF-B1 → KF-B2 | 스튜디오 위 객차 대차 한 대. 대차 프레임·스프링이 **반투명 X-ray**로 바뀌고 차축 2개와 원판 8장, 캘리퍼만 솔리드로 남음 | X-ray 투명화, 원판 가장자리 시안 림 발광 | 앞쪽 차축의 원판 4장에 순서대로 하이라이트 + `1 2 3 4` 카운트, 마지막에 `×4 / AXLE` | Scan Sweep, Tick ×4 |
| **2-2** | 0:09–0:12 | **CU** 측면 | FL | KF-C1 → KF-C2 | REF-1′의 공압 실린더 확대. 실린더 몸체가 반투명해지며 내부에 **시안 압축공기**가 차오르고 로드가 밀려 나옴 | 반투명 실린더, 시안 기체 충전 | 호스를 따라 흐르는 점선 화살표, `AIR IN` | Pneumatic Hiss(치익-) |
| **2-3** ★REV | 0:12–0:15 | **MCU** 정면 약간 위 | FL | KF-E → KF-F | 캘리퍼 하우징이 X-ray로 비치며 **양쪽 레버가 집게처럼 오므라들고** 패드가 원판 양면으로 다가감 | 하우징 반투명, 레버 구조 노출 | 레버 회전축에 작은 원호 화살표, `CLAMP` | Heavy Mechanical Click |
| **2-4** | 0:15–0:18 | **ECU** 원판 가장자리 정측면(엣지온) | FL | KF-P1 → KF-P2 | 원판 두께 단면과 양쪽 패드 사이 간극이 보이는 앵글. 패드가 닫히며 **양면을 동시에** 물고, 접촉선에서 첫 불꽃 | 접촉면 오렌지 발광 시작 | **충격 프레임**: 접촉 순간 2프레임 흰 플래시 + 6프레임 화면 흔들림. 불꽃 오버레이 | Metal Clang, Friction Squeal |

### S3 발열 · 0:18–0:30 — "열차의 운동에너지는 고스란히 마찰열이 됩니다. 원판 표면은 순식간에 수백 도. 그래서 마찰판은 허브에 통째로 고정되지 않고, 늘어나는 만큼 미끄러질 여유를 두고 체결됩니다."

| 컷 | 시간 | 사이즈 · 앵글 | 생성 | 시작 KF → 끝 KF | 화면 · 동작 | CG — 생성 안 | CG — CapCut | SFX |
|---|---|---|---|---|---|---|---|---|
| **3-1** ★REV | 0:18–0:21.5 | **CU** 원판 정면 | FL | KF-H1 → KF-H2 | 차가운 강철 → 외경부터 안쪽으로 **오렌지 → 레드** 발광이 번짐. 허브는 어두운 금속 그대로 | 에미션 발광 그라데이션 | 아지랑이(디스플레이스먼트) 오버레이, `E_k → HEAT` | High Pitch Friction, Fire Burst Low |
| **3-2** | 0:21.5–0:24 | **CU** 동일 | POST | 3-1 마지막 프레임 정지 | **열화상 모드 전환**: 3-1 끝 프레임을 정지시키고 그라데이션 맵(검정→보라→빨강→노랑→흰색)을 0.3초 와이프로 적용 | — | 오른쪽에 세로 온도 막대 `COLD ↔ HOT`(숫자 없음), 스캔 라인 1회 | Thermal Beep, Low Hum |
| **3-3** | 0:24–0:27 | **ECU** 매크로 허브 체결부 | I2V | KF-J1 | 빛나는 마찰링과 차가운 허브가 만나는 체결부로 **아주 느린 푸시인** | 링 발광, 허브 냉색 | 링 → 바깥 방향으로 맥동하는 방사형 화살표 `↔` | Metal Creak |
| **3-4** | 0:27–0:30 | **ECU** X-ray | FL | KF-J2 → KF-J3 | 허브가 반투명해지고 체결 부싱이 보임. 마찰링이 **바깥으로 아주 조금 밀려나며** 부싱 간극이 벌어짐 | 반투명 허브, 링의 미세 이동 | 간극에 노란 하이라이트 + `THERMAL EXPANSION`, Warning Beep 1회 | Warning Beep |

- 3-4는 미세 변위라 모델이 무시할 확률이 높은 컷입니다. 2회 실패하면 **3-3과 3-4를 I2V 6초 1컷으로 합치고** 팽창은 CapCut 화살표로만 표현.

### S4 내부 · 0:30–0:44 — "진짜 비밀은 원판 속에 있습니다. 두 장의 판 사이에, 냉각 핀이 촘촘히 박힌 통풍 구조. 바퀴가 돌면 원판 자체가 송풍기가 돼, 안쪽의 찬 공기를 빨아들여 바깥으로 열을 뿜어냅니다."

| 컷 | 시간 | 사이즈 · 앵글 | 생성 | 시작 KF → 끝 KF | 화면 · 동작 | CG — 생성 안 | CG — CapCut | SFX |
|---|---|---|---|---|---|---|---|---|
| **4-1** ★REV | 0:30–0:33 | **MS** REF-1′ 앵글(원판 전체) | FL | KF-K0 → KF-K1 | 발열 상태 원판의 **오른쪽 위 1/4이 평면으로 절개되어** 카메라 쪽으로 빠져나가며 사라지고, 두 판과 냉각 핀이 드러남 | 쿼터 컷어웨이 | 시작 0.5초: 시안 레이저 절단선이 1/4 경계를 따라 그려짐(정방향에서만) | Metal Slice, Reverse Whoosh |
| **4-2** | 0:33–0:37 | **CU** 단면 정면 | I2V | KF-K2 | 단면을 향한 **느린 푸시인**. 위아래 두 장의 마찰판, 그 사이 방사형 핀, 핀 사이 공기 통로 | 단면 금속 질감 | 지시선 라벨 `FRICTION PLATE ×2`, `COOLING VANES` 순차 등장 | Low Drone |
| **4-3** | 0:37–0:41 | **MCU** 단면 3/4 | I2V | KF-K3 | 원판은 정지. 허브 쪽에서 **시안 기류가 빨려 들어와** 핀 사이를 지나며 오렌지로 바뀌어 외경으로 나감 | 기류 스트림(시안→오렌지) | `AIR IN ↘` (허브), `HEAT OUT ↗` (외경) | Air Flow Whoosh, Turbine Whine |
| **4-4** | 0:41–0:44 | **MS** 측면(원판 두께 방향) | I2V | KF-K4 | REF-1에 이미 보이는 **외경 핀 개구부**에서 오렌지 열기가 방사형으로 뿜어져 나옴 | 열기 플룸 | 외경을 따라 바깥으로 퍼지는 화살표 링 | Vortex Wind |

- "바퀴가 돌면"이지만 원판은 **회전시키지 않습니다.** 단면이 회전하면 절개된 1/4이 함께 돌아 구조 판독이 무너집니다. 회전 느낌은 4-3의 기류가 소용돌이치는 방향으로만 전달합니다.

### S5 복귀 · 0:44–0:55 — "패드가 떨어지면, 원판은 다시 차가운 강철로. 물고, 달아오르고, 스스로 식히고. 그렇게 오늘도,"

| 컷 | 시간 | 사이즈 | 생성 | 소스 | 화면 · 동작 | CG — CapCut | SFX |
|---|---|---|---|---|---|---|---|
| **5-1** | 0:44–0:45.5 | **MS** | REV | 4-1 역재생 · ×3.3 | 1/4 조각이 돌아와 원판이 온전해짐 | 레이저선 없음 | Reverse Whoosh |
| **5-2** | 0:45.5–0:47 | **MCU** | REV | 2-3 역재생 · ×3.3 | 레버가 열리고 패드가 떨어짐 | `RELEASE` | Pneumatic Release |
| **5-3** | 0:47–0:50 | **CU** | REV | 3-1 역재생 · ×1.7 | 발광이 외경 쪽으로 물러나며 차가운 강철로 | 푸른 톤 컬러 그레이딩 살짝 | Cooling Tick(금속 수축음) |
| **5-4** | 0:50–0:52.5 | **ECU** 몽타주 | POST | 2-4 / 3-2 / 4-3 일부 | **"물고 / 달아오르고 / 식히고"에 0.8초씩 맞춘 플래시백**: 패드 접촉 → 열화상 → 기류 | 컷마다 2프레임 플래시, 단어 자막 강조 | Hit ×3 |
| **5-5** ★루프 | 0:52.5–0:55 | **WS** | REV | 1-2 역재생 · ×2 | 스튜디오가 다시 주행 장면으로 덮이며 **REF-2′ 프레임으로 끝남** | `300 km/h`가 1-1과 같은 위치·크기로 다시 등장 | Heartbeat Thump → 1-1 Train Rush로 이어짐 |

**루프 이음매**: 5-5의 마지막 프레임 = 1-2의 첫 프레임 = REF-2′ = 1-1의 첫 프레임. 세 장 모두 같은 이미지에 고정되어 있어 시각적 이음매가 생기지 않습니다. 오디오는 Heartbeat 꼬리를 1-1의 Train Rush 앞 0.2초에 겹쳐 숨깁니다.

---

## 4. 키프레임 목록 — 20장 (+ §0의 REF-1′)

**공통 블록** — 모든 KF 프롬프트 앞에 붙임

```
S-LOCK (studio): vertical 9:16, photoreal industrial product render, seamless mid-grey studio backdrop
with a soft vertical gradient, soft key light from upper left, cool rim light from right,
fixed soft contact shadows, rigid solid metal parts. No text, no letters, no numbers, no logos, no people.

HERO: ventilated railway brake disc with continuous brushed-steel friction faces and a faint
blue-purple heat-temper ring, radial cooling-vane openings around the outer edge, bolted central hub
flange on a dark forged-steel axle; mustard-yellow cast brake caliper bridging the top of the disc
with two dark sintered pads, a small silver pneumatic cylinder with black air hoses on its right side.
```

**편집 파생 공통 문장** — 같은 구도 쌍의 두 번째 장

```
Keep the exact same camera, framing, object positions, object sizes, shapes, materials and lighting.
Change only: …
```

| KF | 원본 | 방법 | 내용 (Change only 이하) |
|---|---|---|---|
| **REF-2′** | REF-2 | 편집 | §0 참조 |
| **KF-S0** | REF-2′ | 편집 | the train body, rails, sleepers, ballast, overhead wires and sky are replaced by a seamless mid-grey studio backdrop with soft contact shadow; the wheel, axle, glowing brake disc and yellow caliper remain in exactly the same position, size and glow, now perfectly sharp with no motion blur |
| **KF-B1** | 신규(REF-1′ 참조) | 생성 | S-LOCK + 3/4 high-angle wide view of a simplified high-speed passenger-car bogie on the studio floor: solid grey bogie frame with springs, two axles, each axle carrying four ventilated brake discs between its two wheels, each disc with a yellow caliper |
| **KF-B2** | KF-B1 | 편집 | the bogie frame, springs and dampers become a translucent glowing cyan X-ray wireframe; axles, wheels, discs and calipers stay solid and opaque |
| **KF-C1** | REF-1′ | 크롭 + 편집 | close-up of the silver pneumatic cylinder and hoses; the cylinder body is semi-transparent, showing an empty chamber and a retracted piston rod |
| **KF-C2** | KF-C1 | 편집 | the chamber is filled with softly glowing cyan compressed air and the piston rod is extended |
| **KF-E** | REF-1′ | 크롭 + 편집 | medium close-up of the caliper; its yellow housing is semi-transparent, revealing two internal lever arms shaped like tongs on both sides of the disc, open, with a clear gap between each pad and the disc |
| **KF-F** | KF-E | 편집 | the two tong levers are closed and both pads press flat against both disc faces |
| **KF-P1** | 신규(REF-1′ 참조) | 생성 | S-LOCK + HERO, extreme close-up looking along the disc face edge-on: disc thickness with cooling vanes visible in the middle, one sintered pad on each side with a small visible gap |
| **KF-P2** | KF-P1 | 편집 | both pads touch both disc faces; a thin orange glowing line along each contact edge |
| **KF-H1** | REF-1′ | 크롭 | close-up frontal view of the disc friction face, cool brushed steel, caliper partly visible at the top |
| **KF-H2** | KF-H1 | 편집 | the friction face glows orange at the outer rim blending into red toward the middle; the hub stays dark cool metal |
| **KF-J1** | KF-H2 | 크롭 + 편집 | macro of the joint where the glowing friction ring meets the dark cool hub flange, bolts and bushings visible |
| **KF-J2** | KF-J1 | 편집 | the hub flange is semi-transparent, revealing radial sliding bushings connecting ring and hub, tight |
| **KF-J3** | KF-J2 | 편집 | the friction ring sits slightly further outward, small visible gaps opening at each bushing |
| **KF-K0** | REF-1′ | 편집 | the whole friction face glows orange-red, hub dark; caliper unchanged |
| **KF-K1** | KF-K0 | 편집 | the upper-right quarter of the disc is cut away with perfectly flat machined cut faces, revealing two parallel friction plates joined by evenly spaced radial cooling vanes with air channels between them |
| **KF-K2** | KF-K1 | 크롭 | close-up of the cut face (two plates + vanes) |
| **KF-K3** | KF-K1 | 편집 | translucent cyan air streams entering near the hub and turning orange as they exit between the vanes at the rim |
| **KF-K4** | REF-1′ | 크롭 + 편집 | side view of the disc edge with vane openings (as in the reference), the disc glowing; faint orange heat plumes leaving the openings |

> **크롭 KF의 해상도 주의**: REF-1′에서 잘라낸 크롭은 반드시 1080×1920으로 다시 업스케일하고, **그 업스케일본을 기준으로** 짝 KF를 편집합니다. 짝끼리 해상도·디테일 수준이 다르면 보간 중에 선명도가 출렁입니다.

---

## 5. 클립 프롬프트 (Omni 1.1 입력용)

**형식**: `[LOCK] + START + MOTION(동사 하나) + END + CAMERA + TIMING + NEGATIVE`. 수치·정밀도 문구는 넣지 않습니다.

**공통 NEGATIVE**: `No morphing, no melting, no bending of metal, no new parts appearing, no floating debris, no text.`
**★REV 클립 추가 NEGATIVE**: `No sparks, no smoke, no particles, no heat haze.`

**1-1 (A→A)**
```
Photoreal high-speed train at full speed, low angle beside the bogie. Ballast and rails stream past with
strong motion blur, the brake disc rim pulses with orange-red glow. The train, wheel, disc and caliper stay
in the same place in frame. Camera locked. Ends exactly as it started. [NEGATIVE]
```

**1-2 ★REV (REF-2′ → KF-S0)**
```
Time freezes: the speeding scene stops completely. Then the train body, rails, ballast, wires and sky peel
away from the edges of the frame and are replaced by a seamless grey studio. The wheel, axle, glowing disc
and yellow caliper stay perfectly fixed in position and size the whole time. Camera locked.
Holds still at the start and at the end. [NEGATIVE] [REV NEGATIVE]
```

**2-1 (KF-B1 → KF-B2)**
```
[S-LOCK] The solid bogie frame, springs and dampers gradually turn into a translucent cyan X-ray wireframe,
revealing two axles with four brake discs each. Axles, wheels, discs and calipers remain solid and unchanged.
Camera locked. Smooth, even transition. [NEGATIVE]
```

**2-2 (KF-C1 → KF-C2)**
```
[S-LOCK] Inside the semi-transparent pneumatic cylinder, glowing cyan compressed air flows in from the hose
and fills the chamber, pushing the piston rod straight out along the cylinder axis. Only the air and rod move.
Camera locked. [NEGATIVE]
```

**2-3 ★REV (KF-E → KF-F)**
```
[S-LOCK] Inside the semi-transparent yellow caliper, the two tong-shaped levers pivot inward around their pins
and close like pincers, moving both pads straight onto both faces of the disc. Disc and housing stay still.
Camera locked. Holds still at the start and at the end. [NEGATIVE] [REV NEGATIVE]
```

**2-4 (KF-P1 → KF-P2)**
```
[S-LOCK] Extreme close-up, edge-on. Both sintered pads move straight toward the disc and clamp both faces at
the same instant; a thin orange glow line appears along each contact edge. Camera locked. [NEGATIVE]
```

**3-1 ★REV (KF-H1 → KF-H2)**
```
[S-LOCK] The brushed-steel friction face heats up: orange glow appears at the outer rim and spreads inward,
deepening to red; the hub stays dark and cool. Shape and surface details stay identical. Camera locked.
Holds still at the start and at the end. [NEGATIVE] [REV NEGATIVE]
```

**3-3 (KF-J1, I2V)**
```
[S-LOCK] Very slow push-in toward the joint between the glowing friction ring and the cool hub flange.
Nothing else moves. [NEGATIVE]
```

**3-4 (KF-J2 → KF-J3)**
```
[S-LOCK] The glowing friction ring expands and slides slightly outward along the radial bushings,
small gaps opening at each bushing; the hub stays still. Camera locked. [NEGATIVE]
```

**4-1 ★REV (KF-K0 → KF-K1)**
```
[S-LOCK] A flat cut separates the upper-right quarter of the glowing disc; that quarter slides straight
toward the camera and out of frame, revealing two parallel plates joined by radial cooling vanes.
The rest of the disc, hub and caliper stay perfectly still and rigid. Camera locked.
Holds still at the start and at the end. [NEGATIVE] [REV NEGATIVE]
```

**4-2 (KF-K2, I2V)**
```
[S-LOCK] Slow push-in on the cut face showing two friction plates and the evenly spaced cooling vanes between
them. Nothing moves except the camera. [NEGATIVE]
```

**4-3 (KF-K3, I2V)**
```
[S-LOCK] The cutaway disc stays completely still. Translucent cyan air streams are drawn in near the hub,
swirl outward through the channels between the vanes, turn orange as they pass the hot plates and stream out
from the rim. Steady, continuous flow. Camera locked. [NEGATIVE]
```

**4-4 (KF-K4, I2V)**
```
[S-LOCK] Side view of the glowing disc edge. Orange heat plumes flow steadily outward from every vane opening
around the rim, radiating away from the disc. Disc stays still. Camera locked. [NEGATIVE]
```

---

## 6. CG 연출 — 생성 안 vs CapCut 분담

| CG 요소 | 어디서 | 이유 / 방법 |
|---|---|---|
| 월드 스위치, X-ray 투명화, 발광, 쿼터 단면, 기류, 열기 플룸 | **Omni 생성 안** | 형태와 빛이 함께 바뀌어야 하는 효과. KF 쌍으로 끝 상태를 고정해 두고 보간에 맡김 |
| `300 km/h` 카운터, `Ø 640 mm` 원형 스트로크, `×4` 카운트, 지시선 라벨 | CapCut 텍스트 + 키프레임 | 생성 모델은 글자를 깨뜨림. 모노스페이스 폰트, 흰색 + 시안 강조 |
| 레이저 절단선(4-1), 방사형·흐름 화살표 | CapCut 도형 + 마스크 | 정방향 구간에서만. 5-1 역재생 구간에는 넣지 않음 |
| 불꽃(2-4), 아지랑이(3-1) | CapCut 오버레이(스크린 블렌드) / 왜곡 효과 | ★REV 클립에 직접 생성하면 역재생 때 거꾸로 빨려 들어감 |
| 열화상 전환(3-2) | CapCut 정지 프레임 + 그라데이션 맵 | 생성 불필요, 색 팔레트를 정확히 통제 가능 |
| 충격 프레임(2-4), 플래시(1-2, 5-4) | CapCut 흰색 단색 2프레임 + 흔들림 | 타격감은 편집이 더 정확함 |

### HUD 배치 (9:16 쇼츠 안전영역)
- **상단 8~18%**: 상태 HUD(`300 km/h`, `AIR IN`, `CLAMP`, `HEAT` …). 왼쪽 정렬.
- **하단 22~32%**: 내레이션 자막(한 줄 최대 14자, 2줄까지).
- **하단 22% 아래, 오른쪽 15%**: 쇼츠 UI가 가리므로 비워 둠.
- 라벨·지시선은 피사체 옆에 두되 위 영역과 겹치지 않게.

---

## 7. 제작 순서 (위험도 순)

| 순서 | 작업 | 통과 기준 |
|---|---|---|
| 1 | REF-1′, REF-2′ 정비 → 1080×1920 업스케일 | 분할선·글자 없음, 캘리퍼가 두 이미지에서 같은 디자인 |
| 2 | **KF-S0 → 1-2 월드 스위치** | 원판·캘리퍼 위치가 전환 내내 고정. *루프의 핵심이라 이것부터 확정* |
| 3 | **KF-K0/K1 → 4-1 쿼터 단면** | 절개면이 평평, 핀 개수가 프레임마다 일정 |
| 4 | KF-E/F → 2-3 캘리퍼 집게 | 레버가 회전축을 벗어나지 않음 |
| 5 | 3-1 발열, 2-1 대차 X-ray, 2-2 실린더, 2-4 패드 접촉 | 형태 유지, 변화가 하나뿐 |
| 6 | I2V 컷(3-3, 4-2, 4-3, 4-4), 1-1 | 가장 쉬움 |
| 7 | 3-4 체결부 미세 이동 | 2회 실패 시 3-3과 합쳐 I2V 1컷 |
| 8 | CapCut 조립 → 루프 3회 연속 재생 검수 | 5-5 → 1-1 이음매에서 화면·소리 모두 튀지 않음 |

### 클립 검수 탈락 기준
- 원판 외곽이 타원·물결로 일그러짐
- 캘리퍼 색이나 형태가 클립 중간에 바뀜
- 레버·패드·로드가 자기 축을 벗어나 움직임
- 단면 절개면이 휘거나 핀 개수가 변함
- ★REV 클립에 불꽃·연기·입자가 생김
- FL 클립의 첫 프레임 또는 끝 프레임이 KF와 눈에 띄게 다름(특히 1-2)
