# KTX 차축 제동 디스크 숏폼 — 대본 검토 · 다듬은 초안 · 장면 구성 v1

> 가제 **《시속 300km를 세우는 쇠 원판》**
> 55초 무한 루프 · 9:16 세로 · 1080×1920 · 24fps · Google Flow(Veo) 단독 생성 파이프라인
> 핵심 기법: **First/Last Frame 보간**(Omni 1.1 방식) — Blender 단계 없음

---

## 0. 한 줄 결론

초안의 **구성(훅 → 체결 → 발열 → 단면 냉각 → 복귀)과 루프 아이디어는 좋습니다.** 고칠 것은 세 가지입니다.

1. **사실 오류 몇 개** — 레일 캘리퍼 구조, 디스크 장수, 400톤, 나선형 핀, 근거 없는 수치(3.8bar·4.2mm·85%).
2. **분량 초과** — 내레이션 약 450음절로 1.05배속에서도 60초를 넘습니다. 300음절 안팎으로 줄여야 55초 안에 숨 쉴 틈이 생깁니다.
3. **루프 이음매 문장이 이어지지 않음** — "…디스크가 있기에 / 시속 300km로 질주하던 KTX가 급제동을 거는 순간…"은 이어 읽으면 뜻이 성립하지 않습니다.

그리고 Omni 1.1 기법은 **"같은 이미지를 시작·끝에 넣는 A→A 대칭 생성"보다 "A→B 1회 생성 + 편집에서 역재생"으로 쓰는 쪽**이 훨씬 안정적입니다. 이 방식이면 루프 이음매가 **같은 클립의 첫 프레임**이라 픽셀 단위로 맞습니다(§4).

---

## 1. 대본 검토

### 유지할 것
1. **훅의 대비** — 300km/h와 시뻘건 원판. 숫자와 열이 한 화면에 있어 첫 2초 정지율이 높은 구조.
2. **"진짜 비밀은 단면 속"** 반전 — 통풍형 디스크의 원심 송풍 원리는 실제 설계 원리이고, 단면 연출과 정확히 맞물림.
3. **3단 마무리**("식히고, 물어뜯고, 열을 뿜어내며") — 리듬이 좋음. 순서만 화면 순서에 맞게 조정.
4. HUD는 영어 단문, 내레이션은 한국어 — 역할 분리가 명확함.

### 고칠 것

| # | 문제 | 왜 문제인가 | v1 해결 |
|---|---|---|---|
| 1 | **루프 이음매 문장이 안 이어짐** | "디스크가 있기에 → 급제동을 거는 순간, 지옥이 열립니다"는 인과가 거꾸로임. 루프 숏폼은 두 번째 시청에서 문장이 매끄럽게 이어져야 재생이 반복됨 | 끝: **"…그렇게 오늘도,"** → 처음: **"시속 300킬로로 달리는 KTX를 멈춰 세우는 건, 지름 64센티 쇠 원판입니다."** 처음 문장은 단독으로도, 이어 붙여도 성립 |
| 2 | **분량 초과** (약 450음절) | 한국어 TTS 1.05배속 기준 초당 약 7음절 → 약 65초. 특히 0~6초 훅에 약 60음절(초당 10음절)이 몰려 있음 | 약 290음절로 축소. 훅은 35음절(약 5초) |
| 3 | **첫 문장이 늦게 터짐** | "시속 300km로 질주하던 400톤의 KTX가 급제동을 거는 순간, 차축 아래에서는…" — 핵심(쇠 원판)이 문장 끝에 나옴 | 첫 문장에 **주어(쇠 원판)와 숫자(300km/h)를 함께** 배치 |
| 4 | **캘리퍼 구조 오류** | 철도 디스크 브레이크는 자동차처럼 피스톤이 패드를 직접 미는 구조가 아니라, **브레이크 실린더가 집게(tong) 레버를 오므려** 패드를 양면에 압착하는 구조가 일반적. "피스톤이 몇 mm 전진해 패드를 압착"은 부정확 | "압축공기가 실린더를 밀고, **집게처럼 생긴 캘리퍼**가 패드로 원판 양면을 물어버립니다" |
| 5 | **"차축당 2~3개" 디스크** | KTX-I 객차 대차(TGV 계열)는 **차축 1개에 디스크 4장**이 일반적으로 알려진 구성 | "바퀴축 하나에 이 원판이 네 장" — **단, §1 사실 확인 메모의 검증 후 확정** |
| 6 | **"400톤"** | KTX-I(20량)는 공차 700톤대, KTX-산천(10량)은 400톤대. 화면 속 대차가 TGV 계열(KTX-I)이면 숫자가 어긋남 | **내레이션·HUD에서 질량 삭제.** 음절도 줄고 오류 위험도 사라짐 |
| 7 | **온도 수치 불일치** | 650°C(비주얼) / 680°C(HUD) / 700도(내레이션) / 677°C(Blender) — 한 영상에 4개의 숫자 | 숫자 하나로 통일. 출처 확인 전에는 "**수백 도**", 확인되면 "**700도 가까이**" (§1 메모) |
| 8 | **근거 없는 수치** | `3.8 bar`, `4.2mm`, `HEAT DISSIPATION: 85%`는 출처가 없음. 댓글에서 바로 지적당하는 유형 | 수치 HUD 삭제 → 상태 HUD(`AIR IN`, `CLAMP`, `HEAT`, `AIRFLOW`)로 교체 |
| 9 | **"나선형 방열 핀"** | 철도용 통풍형 디스크는 **방사형 핀**이나 **기둥형 핀(pin)** 배열이 일반적. 나선형은 일반적 설명이 아님 | "두 장의 판 사이에 **냉각 핀이 촘촘히 박힌** 구조" |
| 10 | **"차축과 완전히 고정되지 않은 플로팅 핀"** | 방향은 맞지만(마찰링이 열팽창 시 반경 방향으로 움직일 여유를 두고 허브에 체결) "플로팅 핀"은 제조사별 용어라 일반화하기 어려움 | "**늘어나는 만큼 바깥으로 미끄러질 여유를 두고** 허브에 체결" |
| 11 | **"회생제동 외에도, 객차 차축에…"** | KTX-I 동력차는 발전(저항)제동, KTX-산천 이후는 회생제동. 차종에 따라 달라짐 | "전기 제동"으로 묶거나 문장 삭제(v1은 삭제) |
| 12 | **"원심 송풍기 = 바퀴가 도는 회전력"** | 원리는 맞음. 다만 "스스로를 식힌다"를 너무 단정하면 열 대부분이 원판에 일단 저장된다는 점이 빠짐 | "바퀴가 돌면 원판 자체가 송풍기가 돼…" 유지, 85% 같은 효율 수치는 넣지 않음 |
| 13 | **스파크 연출** | 소결 패드에서 불꽃이 날 수는 있으나, 역재생할 클립에 불꽃이 있으면 불꽃이 원판으로 빨려 들어가는 장면이 됨 | 불꽃은 생성 클립에 넣지 않고 **CapCut 오버레이**로 정방향 구간에만 얹음 |
| 14 | **화면 하나에 동작이 너무 많음** | 00:30~44에 "외벽 분리 + 핀 노출 + 청/적 기류 시뮬레이션"을 한 번에 → AI 영상에서 형태 붕괴 확률이 가장 높은 조합 | 단면 개방(C06)과 기류(C07)를 **두 클립으로 분리** |

### 사실 확인 메모 (업로드 전 반드시 확인)
- **디스크 장수**: TGV 계열 객차(트레일러) 대차는 차축당 디스크 4장이 일반적으로 알려져 있음. KTX-I 객차 대차도 같은 계열이지만 **코레일·제작사 기술자료로 최종 확인** 후 "네 장" 사용. 확인이 안 되면 "**여러 장**"으로 대체.
- **지름 640mm**: TGV 계열 디스크 규격으로 흔히 언급되는 값. 출처 확보 전에는 HUD만 쓰고 내레이션은 "지름 60센티가 넘는"으로 바꿀 수 있음.
- **온도**: 고속 비상제동 시 디스크 마찰면이 수백 °C에 이르는 것은 일반적. "700도 가까이"는 **논문·제작사 자료 1건 이상 확보 시에만**. 붉게 빛나는 연출은 약 500°C 이상을 암시하므로 화면과 숫자를 맞출 것.
- **동력차**: KTX-I 동력차는 디스크가 아니라 답면(바퀴 표면) 제동 + 전기 제동. 이 영상의 디스크는 **객차 대차**라는 전제로 화면을 구성.
- **화면 속 형상**: 실제 KTX 부품의 정밀 재현이 아니라 **"고속열차 차축 디스크의 일반 구조"**. 고정 댓글에 한 줄 명시 권장.

### 제목 후보
1. **시속 300km KTX를 세우는 건 '쇠 원판'이다** — 내레이션 첫 문장과 일치 (추천)
2. 300km/h를 멈추는 원판 속 비밀
3. KTX 브레이크가 녹지 않는 이유 — 단, "700°C" 수치는 출처 확인 후에만 제목에 사용

---

## 2. 다듬은 내레이션 v1

ElevenLabs 안정도 0.45 / 속도 1.05x 유지. 문장 사이 0.3~0.5초 여백. 약 290음절 ≈ 42~45초 발화 → 55초 안에 효과음만 들리는 구간 확보.

```
[S1 · 0:00]  시속 300킬로로 달리는 KTX를 멈춰 세우는 건,
             지름 64센티 쇠 원판입니다.

[S2 · 0:06]  객차 바퀴축 하나에, 이 원판이 네 장.
             제동이 걸리면 압축공기가 실린더를 밀고,
             집게처럼 생긴 캘리퍼가 원판 양면을 꽉 물어버립니다.

[S3 · 0:18]  열차의 운동에너지는 고스란히 마찰열이 됩니다.
             원판 표면은 순식간에 수백 도.
             그래서 마찰판은 허브에 통째로 고정되지 않고,
             늘어나는 만큼 미끄러질 여유를 두고 체결됩니다.

[S4 · 0:30]  진짜 비밀은 원판 속에 있습니다.
             두 장의 판 사이에, 냉각 핀이 촘촘히 박힌 통풍 구조.
             바퀴가 돌면 원판 자체가 송풍기가 돼,
             안쪽의 찬 공기를 빨아들여 바깥으로 열을 뿜어냅니다.

[S5 · 0:44]  패드가 떨어지면, 원판은 다시 차가운 강철로.
             물고, 달아오르고, 스스로 식히고.
             그렇게 오늘도,
                                    → (S1로 이어짐)
```

**루프 이음매 확인**: "그렇게 오늘도, / 시속 300킬로로 달리는 KTX를 멈춰 세우는 건, 지름 64센티 쇠 원판입니다." — 이어 읽어도, 처음부터 읽어도 문장이 성립합니다.

**대체 문장 (사실 확인 결과에 따라 교체)**
- "네 장" 미확인 → "이 원판이 여러 장."
- 700°C 출처 확보 → "원판 표면은 순식간에 700도 가까이."
- 640mm 미확인 → "지름 60센티가 넘는 쇠 원판입니다."

---

## 3. 장면 구성 — 55초 / 10클립 (S1~S5)

### LOOK LOCK (화면 규칙)
- **비율**: 9:16 세로. 피사체는 화면 가운데 1/3, 상단 15%는 HUD, 하단 20%는 자막 안전영역으로 비워 둠.
- **배경**: 다크 차콜 단색 스튜디오 `#1A1C1E`. 구조물·레일·풍경 없음(단면 경계 정확도가 가장 높음).
- **조명**: 좌상단 소프트 키 + 차가운 림라이트. 그림자 위치 고정.
- **카메라**: 한 클립에 움직임 하나. 대부분 **고정(locked-off)**. 움직임은 상태 변화(체결·발열·단면)에만 씀.
- **팔레트**
  - 차콜 `#1A1C1E` — 배경
  - 스틸 블루그레이 `#8A9AA6` — 식은 원판
  - 세이프티 옐로 `#E2B007` — 캘리퍼(형상 추적용 대비색, 실차 색상 재현 아님)
  - 열 오렌지 `#FF6A1A` → 레드 `#C8261B` — 발열(이 두 색은 열 표현에만 사용)
  - 냉기 시안 `#3FC5F0` — 유입 공기(S4에서만)
- **회전 표현**: 원판 회전은 **표면 특징이 보이지 않는 균일한 회전 블러**로. 회전 방향이 화면에서 읽히지 않아야 역재생 클립이 자연스러움.
- **절대 금지**: 생성 이미지 안의 글자·숫자·로고 / 부품이 공중에 흩어지는 분해 / 원판이 휘거나 녹아내리는 형태 / 역재생 예정 클립 안의 불꽃·연기·입자.

### 키프레임 (Flow 이미지 생성 → 기준 1장에서 편집으로 파생)

| KF | 화면 | 파생 방법 |
|---|---|---|
| **KF-A** ★루프 기준 | 3/4 접사. 회전 블러 원판 + 노란 캘리퍼, 패드 열림, 차가운 강철 | 마스터 1장. 이후 모든 원판 KF의 참조 이미지 |
| KF-B | KF-A와 같은 구도. 패드 닫힘, 마찰면 외곽이 둔한 오렌지로 발광 | KF-A 편집 |
| KF-C | 객차 대차 측면 와이드. 대차 프레임·차축·원판 4장·캘리퍼 4개, 솔리드 | 새로 생성(KF-A를 참조로) |
| KF-D | KF-C와 같은 구도. 대차 프레임만 반투명 X-ray, 차축·원판·캘리퍼는 솔리드로 강조 | KF-C 편집 |
| KF-E | 캘리퍼 단면 클로즈업. 실린더 로드 수축, 집게 레버 열림, 패드–원판 간극 보임 | KF-A 참조로 생성 |
| KF-F | KF-E와 같은 구도. 실린더 로드 신장, 레버 닫힘, 패드 밀착 | KF-E 편집 |
| KF-G | 원판 정면. 차가운 스틸 블루그레이 | KF-A 참조로 생성 |
| KF-H | KF-G와 같은 구도. 마찰면 오렌지-레드 발광, 허브 쪽은 어두운 금속 | KF-G 편집 |
| KF-I | 허브–마찰링 체결부 매크로. 링은 발광, 허브는 차가움 | KF-H 참조로 생성 |
| KF-J | 원판 3/4 뷰, 발열 상태, 캘리퍼 없음 | KF-H 참조로 생성 |
| KF-K | KF-J와 같은 구도. **90° 쿼터 단면 절개**, 두 판 사이 냉각 핀 노출 | KF-J 편집 |
| KF-L | KF-K + 허브 쪽 시안 기류, 외경 쪽 오렌지 열기 | KF-K 편집 |

> 원칙: **같은 구도의 쌍(A/B, C/D, E/F, G/H, J/K)은 반드시 "편집"으로 파생**합니다. 새로 생성하면 형상이 미세하게 달라져 보간 중 모핑이 생깁니다.

### 타임라인

| 시간 | 클립 (생성 방식) | 화면 / 카메라 | 내레이션 | HUD (CapCut) | SFX (CapCut) |
|---|---|---|---|---|---|
| **0:00–0:06** S1 훅 | **C01** KF-A → KF-B · 6s · 정방향 | 회전 블러 원판. 노란 캘리퍼가 닫히며 마찰면 외곽부터 오렌지로 달아오름. 고정. *불꽃은 CapCut 오버레이* | 시속 300킬로로 달리는 KTX를 멈춰 세우는 건, 지름 64센티 쇠 원판입니다. | `300 km/h` → `BRAKE` | Deep Sub Whoosh, Metal Clang, Friction Squeal |
| **0:06–0:12** S2-a | **C02** KF-C → KF-D · 6s | 대차 와이드. 프레임이 반투명해지며 원판 4장과 캘리퍼만 남음. 고정 | 객차 바퀴축 하나에, 이 원판이 네 장. | `DISC ×4 / AXLE` `Ø 640 mm` | Low Drone, Scan Sweep |
| **0:12–0:18** S2-b | **C03** KF-E → KF-F · 6s · ★C09에서 역재생 재사용 | 캘리퍼 단면. 실린더 로드가 밀려나고 집게 레버가 오므라들며 패드가 원판에 밀착. 고정 | 제동이 걸리면 압축공기가 실린더를 밀고, 집게처럼 생긴 캘리퍼가 원판 양면을 꽉 물어버립니다. | `AIR IN` → `CLAMP` | Pneumatic Hiss, Heavy Mechanical Click |
| **0:18–0:24** S3-a | **C04** KF-G → KF-H · 6s · ★C10 대체용 | 원판 정면. 바깥에서 안쪽으로 강철 → 오렌지 → 레드. 마찰면에 아지랑이. 고정 | 열차의 운동에너지는 고스란히 마찰열이 됩니다. 원판 표면은 순식간에 수백 도. | `E_k → HEAT` | High Pitch Friction, Fire Burst Low |
| **0:24–0:30** S3-b | **C05** KF-I 단일 이미지 → 영상 · 6s | 체결부 매크로로 느린 푸시인. 발광 링 아래 체결 부싱. *팽창 화살표는 CapCut* | 그래서 마찰판은 허브에 통째로 고정되지 않고, 늘어나는 만큼 미끄러질 여유를 두고 체결됩니다. | `THERMAL EXPANSION ↔` | Metal Creak, Warning Beep(1회) |
| **0:30–0:37** S4-a | **C06** KF-J → KF-K · 7s · ★C08에서 역재생 재사용 | 발열 원판의 위쪽 1/4이 깔끔한 평면으로 절개되며 사라지고, 두 판 사이의 냉각 핀이 드러남. 고정 | 진짜 비밀은 원판 속에 있습니다. 두 장의 판 사이에, 냉각 핀이 촘촘히 박힌 통풍 구조. | `CUTAWAY` `COOLING VANES` | Reverse Whoosh, Metal Slice |
| **0:37–0:44** S4-b | **C07** KF-L 단일 이미지 → 영상 · 7s | 단면 유지. 허브 쪽에서 시안 기류가 빨려 들어가 핀 사이를 지나 외경에서 오렌지 열기로 뿜어짐. 고정 | 바퀴가 돌면 원판 자체가 송풍기가 돼, 안쪽의 찬 공기를 빨아들여 바깥으로 열을 뿜어냅니다. | `AIR IN ↘` `HEAT OUT ↗` | Air Flow Whoosh, Turbine Whine |
| **0:44–0:47** S5-a | **C08** = **C06 역재생** · 2배속 3.5s | 단면이 닫히며 원판이 다시 온전해짐 | 패드가 떨어지면, 원판은 다시 차가운 강철로. | — | Reverse Whoosh |
| **0:47–0:50** S5-b | **C09** = **C03 역재생** · 2배속 3s | 레버가 열리고 패드가 떨어짐 | 물고, 달아오르고, 스스로 식히고. | `RELEASE` | Pneumatic Release |
| **0:50–0:55** S5-c ★루프 | **C10** = **C01 역재생** · 1.2배속 5s | 발광이 식고 패드가 열리며 **KF-A와 같은 프레임으로 끝남** | 그렇게 오늘도, | `300 km/h` (S1과 같은 위치) | Heartbeat Thump → (S1 Whoosh로 이어짐) |

**생성 클립 7개, 역재생 재사용 3개.** 대칭 구간(S2-b↔S5-b, S1↔S5-c, S4-a↔S5-a)이 모두 같은 클립이라 형상이 어긋날 수 없습니다.

---

## 4. Omni 1.1 기법 적용 — 초안 세팅에 대한 피드백

> 아래 세팅 항목 중 **Native 4K, 시드 고정, Isometric Locked, Uniform/Linear 같은 콘솔 옵션의 실제 이름과 지원 여부는 확인하지 못했습니다.** 실제 콘솔 화면 기준으로 한 번 더 맞춰 보세요. 기법 자체(시작·끝 프레임 보간)는 Google Flow의 Frames to Video에서도 똑같이 쓸 수 있으므로 v1은 Flow 단독으로 설계했습니다.

| 초안 세팅 | 문제 | 권장 |
|---|---|---|
| 같은 이미지를 시작·끝 슬롯에 중복 등록(A→A) | 보간 모델은 시작=끝이면 **거의 움직이지 않거나**, 중간에 형태가 녹았다 돌아오는 경향이 큼. 대칭도 보장되지 않음 | **A→B 1회 생성 → 편집에서 역재생해 B→A** 이어 붙이기. 대칭이 수학적으로 보장되고 생성 비용도 절반 |
| 10초 한 클립에 단면 + 축 방향 분해 + 기어 회전 동시 | 동작이 3개 겹치면 형태 붕괴 확률이 급격히 오름 | **한 클립 = 동작 1개**. 단면 개방 / 분해 / 회전을 별도 클립으로 |
| Uniform/Linear(이징 금지) | 왕복 운동(분해→조립)을 등속으로 하면 **반환점에서 속도가 순간 반전**돼 덜컥거림. 등속은 한 방향으로 계속 도는 회전에만 맞음 | 왕복 클립은 **양 끝 0.3초 정지(hold) 또는 ease-in-out**. 역재생 이음매에서 속도가 0이 되어 자연스러움 |
| 360p 검증 → 같은 시드로 4K 확정 | 해상도가 바뀌면 같은 시드여도 결과가 달라지는 경우가 많음 | 저해상도는 "구도·동작이 되는지" 판단용으로만. 확정은 **최종 해상도에서 여러 개 뽑아 고르기** |
| "+15cm", "sub-millimeter precision", "zero tolerance" | 생성 모델은 수치·정밀도 문구를 거의 반영하지 못함. 프롬프트만 길어져 핵심 지시가 묻힘 | 상대 표현으로: "slides a short distance along its own axis", "stays rigid" |
| "completing exact integer revolutions" | 모델은 회전 수를 세지 못함. 루프에서 톱니 위치가 어긋나는 원인 | 분해 클립에서는 **회전을 빼고**, 회전은 표면 특징이 없는 블러로 표현 |
| 4K 출력 | 쇼츠 최종 규격은 1080×1920 | Flow 1080p 업스케일로 충분. 크레딧을 재생성에 쓰는 게 이득 |

**유지할 것**: 기계 결합 축을 명시해 분해 방향을 통제하는 원칙("along the axle", "along the cylinder axis"), 단색 그레이 배경, 고정 화각. 모두 맞는 방향입니다.

---

## 5. Google Flow 제작 파이프라인

### 원칙
- **모든 화면은 Flow 안에서**: Flow 이미지 생성으로 KF → Frames to Video(시작·끝 프레임) / 단일 이미지 → 영상.
- **글자·숫자는 편집에서만**: HUD, 자막, 화살표, 불꽃 오버레이는 CapCut.
- **Veo 생성 오디오는 끔**(또는 음소거). 사운드는 TTS + CapCut SFX.
- **역재생 예정 클립(C01, C03, C06)**: 불꽃·연기·입자·아지랑이 금지 프롬프트를 반드시 넣음. 아지랑이·불꽃은 정방향 구간에서만 오버레이.

### 생성 순서 (위험한 것부터)
1. **KF-A 마스터** 확정 — 모든 원판 KF의 기준. 원판 형상(두 판 + 핀 + 허브)이 그럴듯하지 않으면 여기서 멈추고 다시 뽑기.
2. **C06 단면 개방** (KF-J → KF-K) — 가장 어려운 클립. 절개면이 평평하게 유지되는지 확인.
3. **C01 훅** (KF-A → KF-B) — 루프 기준 클립.
4. **C03 캘리퍼** (KF-E → KF-F).
5. **C04 발열**, **C02 대차 X-ray**.
6. **C05, C07** — 단일 이미지 → 영상(가장 쉬움).

### 공통 스타일 블록 (모든 프롬프트 앞에 붙임)
```
STYLE LOCK: vertical 9:16, photoreal technical 3D visualization, rigid-body engineering animation,
plain dark charcoal studio backdrop, soft key light from upper left, cool rim light, fixed shadows,
locked-off camera, shallow depth of field. Subject: a high-speed train axle-mounted ventilated brake disc
(two steel friction plates joined by internal radial cooling fins, bolted to a central hub on the axle)
and a safety-yellow pneumatic brake caliper unit (tong-type levers, brake cylinder, two sintered pads).
All parts stay solid and rigid. No text, no numbers, no logos, no people, no rails, no scenery.
```

### 키프레임 프롬프트 (Flow 이미지)

**KF-A — 마스터**
```
[STYLE LOCK]
Three-quarter macro view of the brake disc and caliper. The disc is spinning so fast that its surface is
a smooth, uniform rotational blur with no distinct features. The caliper is open, both pads separated
from the disc by a small visible gap. Cool brushed steel, blue-grey tones, no glow. The disc fills the
middle third of the vertical frame, empty dark space above and below.
```

**KF-B — KF-A 편집**
```
Keep the exact same camera, composition, object shapes and lighting.
Change only: the caliper is closed, both pads pressed against the disc faces;
the outer friction ring glows dull orange, fading to dark steel toward the hub.
```

**KF-K — KF-J 편집 (쿼터 단면)**
```
Keep the exact same camera, composition, object shapes and lighting.
Change only: a clean 90-degree quarter section of the disc is cut away with perfectly flat cut faces,
revealing two parallel steel plates connected by evenly spaced radial cooling fins, air channels between
the fins running from the hub outward to the rim. Cut faces are bright machined steel.
```

### 클립 프롬프트 (Frames to Video)

**C01 — 훅 (KF-A → KF-B, 6s)**
```
[STYLE LOCK]
The yellow caliper levers close smoothly and the pads clamp onto the spinning disc.
Starting at the outer rim, the friction ring heats from cool steel to dull glowing orange.
The disc keeps a uniform rotational blur. Camera does not move.
No sparks, no smoke, no particles, no heat haze. Ease in and ease out.
```

**C03 — 캘리퍼 체결 (KF-E → KF-F, 6s)**
```
[STYLE LOCK]
Cutaway view of the caliper. The brake cylinder rod extends along the cylinder axis, the tong levers
pivot inward around their pins, and the two pads move straight toward the disc until they touch both faces.
Only these parts move, along their own axes. Camera does not move.
No sparks, no smoke, no particles. Ease in and ease out.
```

**C06 — 단면 개방 (KF-J → KF-K, 7s)**
```
[STYLE LOCK]
A clean flat cutting plane sweeps through one quarter of the glowing disc and that quarter slides away
and disappears, revealing the internal radial cooling fins between the two plates.
The rest of the disc stays perfectly still and rigid. Camera does not move.
No sparks, no smoke, no particles, no heat haze. Ease in and ease out.
```

**C07 — 원심 기류 (KF-L 단일 이미지, 7s)**
```
[STYLE LOCK]
Keep the cutaway disc completely still. Thin translucent cyan air streams are drawn in near the hub,
flow outward through the channels between the cooling fins, turn orange as they pass the hot plates,
and are expelled from the outer rim. Steady, continuous flow. Camera does not move.
```

**C02, C04, C05**는 같은 형식("Keep camera still. Change only: …")으로 작성.

### 검수 포인트 (클립별 탈락 기준)
- 원판 외곽이 타원·물결로 일그러짐 → 탈락
- 패드나 레버가 축을 벗어나 떠다님 → 탈락
- 단면 절개면이 곡면으로 휘거나 핀 개수가 프레임마다 바뀜 → 탈락
- 역재생 예정 클립에 불꽃·입자 발생 → 탈락
- 첫 프레임이 KF와 눈에 띄게 다름(특히 C01) → 탈락 (루프 이음매가 깨짐)

### 루프 이음매 마무리 (CapCut)
1. C10은 **C01을 그대로 역재생**하므로 마지막 프레임 = C01 첫 프레임 → 이음매가 픽셀 단위로 일치.
2. 그래도 회전 블러 방향이 튀어 보이면: **KF-B → KF-A로 별도 생성**한 클립으로 C10을 교체하고, C10 끝과 C01 시작 사이에 **4~6프레임 크로스 디졸브**.
3. 오디오: S5 마지막 Heartbeat Thump의 꼬리를 S1 Whoosh 앞 0.2초에 겹쳐 소리 이음매도 숨김.
4. HUD `300 km/h`를 S5-c와 S1에서 **같은 위치·같은 크기**로 두어 시선 이음매 고정.

---

## 6. 부록 — 감속 구동장치(기어박스) 프롬프트

이번 쇼츠 주제(제동 디스크)와 다른 부품이라 **별도 에피소드로 분리**를 권장합니다. 한 쇼츠에 두 부품을 넣으면 55초 안에서 둘 다 설명이 얕아집니다.

다음 에피소드용 수정 방향:
- 기어비 "약 2.5~3:1"은 **출처 미확인** — 수치는 화면과 내레이션에서 빼거나 출처 확보 후 사용.
- KTX-I는 동력차에만 견인 전동기·감속기가 있음. "bogie axle"을 "**power car motor bogie**"로 명시.
- A→A 대칭 대신 **3클립 분리 + 역재생**:
  1. 하우징 쿼터 단면 개방 (A → B)
  2. 피니언·대기어 축 방향 분리 (B → C), 회전 없음
  3. 별도 클립: 단면 상태에서 기어 치합 회전 (C 단일 이미지 → 영상, 블러 처리)
  4. 편집: 1 → 2 → 3 → 2 역재생 → 1 역재생

---

## 7. 업로드 전 체크리스트
- [ ] §1 사실 확인 메모 4개 항목 출처 확보 또는 대체 문장으로 교체
- [ ] 내레이션 TTS 실측 길이 ≤ 46초
- [ ] HUD에 출처 없는 수치 없음
- [ ] 루프 이음매 3회 연속 재생해서 시각·청각 튐 없음
- [ ] 고정 댓글: "일반적인 고속열차 차축 디스크 구조를 단순화한 시각화입니다"
