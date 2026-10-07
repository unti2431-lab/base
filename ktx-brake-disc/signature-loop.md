# 시그니처 루프 — "MECHANICAL SPECIMEN" 분해·단면 10초 루프

> 사용자가 준 10초 분해·단면 루프 프롬프트를 **채널 고유의 시그니처 포맷**으로 다시 만든 것입니다.
> - 이번 KTX 제동 편의 톤(그레이 스튜디오 표본, 머스터드 옐로 캘리퍼, 템퍼 컬러, 오른쪽 아래 1/4 단면)에 맞췄습니다.
> - 다음 영상에서는 **변수만 바꿔** 같은 형식으로 쓸 수 있게 템플릿화했습니다.
>
> 기계가 읽는 버전(프레임 단위 편집표 포함)은 `shots-v3.yaml`의 `signature_loop` 섹션에 있습니다.

---

## 1. 원본 프롬프트 진단

| 원본 표현 | 문제 | 바꾼 방향 |
|---|---|---|
| `0.0s to 5.0s … 5.0s to 10.0s` 한 번에 10초 생성 | 시작=끝 프레임(A→A)으로 생성하면 거의 움직이지 않거나, 중간에 녹았다가 돌아오는 경향이 강함. 앞뒤 5초가 정확히 대칭이 될 보장도 없음 | **키프레임 3장(A·B·C) + 클립 2개를 정방향으로 생성**하고, 편집에서 역재생해 대칭을 만듦. 대칭과 루프 이음매가 프레임 단위로 보장됨 |
| `Concurrently` — 캘리퍼 이동 + 패드 분리 + 단면 절개 동시 진행 | 한 클립에 형태 변화가 3개 겹치면 형상이 무너질 확률이 가장 높음 | **순서대로**: ① 분해(캘리퍼·패드) → ② 단면 절개. 한 클립에 동작 하나씩 |
| `by 8cm` | 생성 모델은 수치를 반영하지 못하고 프롬프트만 길어짐 | "패드 두께만큼", "캘리퍼 높이만큼" 같은 **상대 거리** |
| `vertical 180-degree section` (반 단면) | 화면의 절반이 한 번에 바뀌어 변화량이 너무 큼. 본편 4-1 컷(1/4 단면)과 모양도 달라짐 | 본편과 같은 **오른쪽 아래 1/4(3시~6시) 단면**. 허브 단면까지 함께 보여 줌 |
| `curved cooling fins` | 레퍼런스 이미지(REF-1) 외경에 보이는 핀은 **곧은 방사형**. 굽은 핀으로 생성하면 본편과 형태가 달라짐 | `straight radial cooling vanes` |
| `translates radially outward along mounting guide pins` | 철도 캘리퍼의 실제 동작은 아님. 다만 분해도(exploded view)에서는 조립 축을 따라 부품을 띄우는 게 관례라 연출로는 유효 | "**분해도 연출**"임을 명시: 캘리퍼가 차축 중심에서 멀어지는 방향(위)으로 들림 |
| `returning exactly to the state of the first frame` | 문장으로는 보장되지 않음 | 역재생으로 구조적으로 보장 |
| `Seamless loop` | 같은 이유 | 시작·끝에 6프레임 정지, 이음매에서 속도가 0이 되게 함 |

---

## 2. 시리즈 고정값 (모든 에피소드 공통)

**SERIES LOCK — 프롬프트 맨 앞에 그대로 붙임**
```
Vertical 9:16 photoreal industrial specimen render. Seamless mid-grey studio backdrop with a soft
vertical gradient, slightly lighter behind the subject. Soft key light from upper left, cool rim light
from right, one soft fixed contact shadow under the subject. The object stands on a dark machined-steel
display stand. Materials read as real metal: brushed steel, forged steel, painted cast steel.
Rigid-body engineering motion only: every part moves as one solid piece along its own assembly axis.
No text, no letters, no numbers, no logos, no people.
```

| 요소 | 고정값 | 에피소드마다 바뀌는 것 |
|---|---|---|
| 배경 | 미드 그레이 세로 그라데이션 `#8E9194 → #B4B6B8` | — |
| 받침 | 어두운 가공 강철 스탠드(표본 받침대) | — |
| 조명 | 좌상단 소프트 키 + 우측 차가운 림 + 바닥 그림자 1개 | — |
| 색의 의미 | 열 = 오렌지→레드, X-ray·공기 = 시안 | — |
| 히어로 강조색 | 에피소드당 1색 | KTX 제동 편 = 머스터드 옐로 `#C9A227` |
| 단면 규칙 | **오른쪽 아래 1/4(시계 3시~6시)**, 평평한 가공면, 조각은 카메라 쪽으로 직진해 사라짐 | 절개 대상 부품 |
| 분해 규칙 | 각 부품은 **자기 조립 축을 따라서만** 이동, 거리는 상대 표현 | 분해할 부품과 축 |
| 10초 구조 | 정지 → 분해 → 단면 → 리빌 정지 → 단면 복귀 → 조립 → 정지 | — |
| HUD | 모노스페이스 대문자, 흰색 + 시안 | 라벨 문구 |

---

## 3. 10초 구조 (240프레임, 24fps)

```
프레임   0 ─  6  SIG-A 정지                         (조립 상태)
         6 ─ 60  SIG-1 정방향  A → B   ×2.22        (분해: 캘리퍼 들림 + 패드 분리)
        60 ─114  SIG-2 정방향  B → C   ×2.22        (단면: 1/4 조각 빠짐)
       114 ─126  SIG-C 정지 + 절개면 흰 글린트 1회     (리빌 비트 0.5초)
       126 ─180  SIG-2 역재생  C → B   ×2.22        (단면 닫힘)
       180 ─234  SIG-1 역재생  B → A   ×2.22        (조립·체결)
       234 ─240  SIG-A 정지 → 0프레임으로 루프
```

- 생성은 **5초 클립 2개**뿐입니다. 정방향·역방향이 같은 클립이라 앞뒤 5초가 완벽하게 대칭이고, 240프레임째가 0프레임과 같은 이미지입니다.
- 두 클립 모두 **역재생되므로 불꽃·연기·입자 금지**입니다.
- 사운드(CapCut): 6f `Mechanical Release` · 60f `Metal Slice` · 114f `Ping(글린트)` · 126f `Reverse Whoosh` · 230f `Heavy Clamp`.

---

## 4. KTX 제동 편 인스턴스 (바로 사용)

### 키프레임

**SIG-A** = `REF-1′` 그대로(분할선·각인 제거, 1080×1920). 조립·체결·차가운 상태.

**SIG-B** — SIG-A 편집
```
Keep the exact same camera, framing, object positions, object sizes, shapes, materials and lighting.
Change only: exploded view: the yellow caliper with its pneumatic cylinder and hoses has lifted straight up,
away from the axle center, by about the caliper's own height; the two sintered pads have moved straight
outward away from each disc face by about one pad thickness and float in line with their original positions;
the disc, hub, axle and stand are unchanged.
```

**SIG-C** — SIG-B 편집
```
Keep the exact same camera, framing, object positions, object sizes, shapes, materials and lighting.
Change only: the lower-right quarter of the disc, from the 3 o'clock to the 6 o'clock position, is cut away
with perfectly flat machined cut faces, revealing two parallel friction plates joined by evenly spaced
straight radial cooling vanes, and the cut hub flange showing the axle bore; everything else unchanged.
```

> SIG-B에서 캘리퍼가 위로 들리면 9:16 프레임 상단에 닿을 수 있습니다. 잘리면 SIG-A를 먼저 **위쪽 여백 15%를 늘린 버전**으로 아웃페인팅한 뒤 A·B·C를 모두 그 캔버스에서 파생하세요. 세 장의 캔버스가 다르면 보간 중에 화면이 출렁입니다.

### 클립 (Omni 1.1 First & Last Frame, 5초)

**SIG-1 (SIG-A → SIG-B)**
```
[SERIES LOCK]
Exploded-view motion: the yellow caliper with its pneumatic cylinder lifts straight up along its mounting axis,
away from the axle center, while the two sintered pads slide straight outward away from the disc faces.
Every part stays rigid and moves only along its own assembly axis. The disc, hub, axle and stand do not move.
Camera locked. Holds still at the start and at the end.
No morphing, no melting, no bending or warping of metal, no new parts appearing, no floating debris, no text.
No sparks, no smoke, no particles, no heat haze, no dust.
```

**SIG-2 (SIG-B → SIG-C)**
```
[SERIES LOCK]
A flat cut separates the lower-right quarter of the disc, from the 3 o'clock to the 6 o'clock position;
that quarter slides straight toward the camera and out of frame, revealing two parallel plates joined by
straight radial cooling vanes and the cut hub. The lifted caliper, the floating pads and the rest of the disc
stay perfectly still. Camera locked. Holds still at the start and at the end.
No morphing, no melting, no bending or warping of metal, no new parts appearing, no floating debris, no text.
No sparks, no smoke, no particles, no heat haze, no dust.
```

### 한 번에 생성해야 할 때 (원본 프롬프트의 개선판)
콘솔 제약으로 클립 하나로 뽑아야 한다면 아래를 쓰세요. 성공률은 위의 2클립 방식보다 낮습니다.
**시작 = SIG-A, 끝 = SIG-C**로 5초 생성한 뒤 편집에서 역재생을 붙입니다. A→A 10초 생성은 권장하지 않습니다.
```
[SERIES LOCK]
Exploded-view and cutaway sequence of a railway brake assembly, in two clear steps.
First, the mustard-yellow caliper with its pneumatic cylinder lifts straight up along its mounting axis while
the two sintered pads slide straight outward away from the disc faces; then everything pauses briefly.
Second, a flat cut separates the lower-right quarter of the brushed-steel disc and that quarter slides straight
toward the camera and out of frame, revealing two parallel plates joined by straight radial cooling vanes and
the cut hub. Only one step happens at a time. All parts stay rigid. Camera locked.
No morphing, no melting, no bending of metal, no floating debris, no text, no sparks, no smoke, no particles.
```

---

## 5. 다음 영상용 템플릿

`{ }` 안만 바꿉니다. 나머지 문장, 단면 규칙, 10초 구조는 그대로 둡니다.

**변수**

| 변수 | 뜻 | KTX 제동 편 값 |
|---|---|---|
| `{HERO}` | 주인공 부품 묘사(형태·재질·색) | ventilated railway brake disc … mustard-yellow cast-steel caliper … |
| `{ACCENT}` | 에피소드 강조색 부품 | the mustard-yellow caliper with its pneumatic cylinder |
| `{EXPLODE_1}` | 분해 부품 1 + 축 + 거리 | lifts straight up along its mounting axis, away from the axle center, by about its own height |
| `{EXPLODE_2}` | 분해 부품 2 + 축 + 거리 | the two sintered pads slide straight outward away from the disc faces by about one pad thickness |
| `{STATIC}` | 움직이지 않는 부품 | the disc, hub, axle and stand |
| `{CUT_TARGET}` | 절개 대상 | the disc |
| `{REVEAL}` | 단면에서 드러나는 내부 | two parallel plates joined by straight radial cooling vanes and the cut hub |

**SIG-B 편집**
```
Keep the exact same camera, framing, object positions, object sizes, shapes, materials and lighting.
Change only: exploded view: {ACCENT} has {EXPLODE_1}; {EXPLODE_2}; {STATIC} are unchanged.
```
**SIG-C 편집**
```
Keep the exact same camera, framing, object positions, object sizes, shapes, materials and lighting.
Change only: the lower-right quarter of {CUT_TARGET}, from the 3 o'clock to the 6 o'clock position, is cut away
with perfectly flat machined cut faces, revealing {REVEAL}; everything else unchanged.
```
**SIG-1 클립**
```
[SERIES LOCK]
Exploded-view motion: {ACCENT} {EXPLODE_1}, while {EXPLODE_2}. Every part stays rigid and moves only along its
own assembly axis. {STATIC} do not move. Camera locked. Holds still at the start and at the end. [NEGATIVE]
```
**SIG-2 클립**
```
[SERIES LOCK]
A flat cut separates the lower-right quarter of {CUT_TARGET}, from the 3 o'clock to the 6 o'clock position;
that quarter slides straight toward the camera and out of frame, revealing {REVEAL}. All other parts stay
perfectly still. Camera locked. Holds still at the start and at the end. [NEGATIVE]
```

### 예시 — 다음 편 후보: 견인 감속기(기어박스)
| 변수 | 값 |
|---|---|
| `{HERO}` | a high-speed train traction reduction gearbox on a power-car motor bogie axle: dark charcoal cast-iron split housing, a small helical pinion on the motor input shaft meshing with a large helical gear on the axle, tapered roller bearings, **deep teal** painted housing bolts and lifting lugs |
| `{ACCENT}` | the upper half of the cast-iron housing with its teal bolts |
| `{EXPLODE_1}` | lifts straight up along its bolt axis by about its own height |
| `{EXPLODE_2}` | the pinion with its shaft slides straight out along the motor input axis by about one gear width |
| `{STATIC}` | the large gear, the lower housing, the axle and the stand |
| `{CUT_TARGET}` | the large helical gear |
| `{REVEAL}` | the helical tooth profile, the gear web and the bearing seated on the axle |

- 강조색만 머스터드 옐로 → 딥 틸로 바꾸고 나머지(배경·받침·조명·단면 규칙·10초 구조)는 그대로 둡니다. 시청자가 썸네일 첫 프레임만 봐도 같은 시리즈임을 알아봅니다.
- 기어는 **회전시키지 않습니다.** 분해와 회전이 겹치면 톱니 위치가 어긋나 루프가 깨집니다. 회전이 필요하면 별도 I2V 컷으로 따로 만듭니다.

---

## 6. 이번 영상과 자연스럽게 잇는 방법

시그니처 루프는 본편과 **같은 원판, 같은 받침대, 같은 단면 위치**를 씁니다. 그래서 따로 만들어도 같은 세계로 읽힙니다.

| 쓰임 | 방법 |
|---|---|
| **본편 고정 댓글 / 커뮤니티 탭 GIF** | 10초 루프 그대로 |
| **본편 직전 티저 쇼츠(10초)** | 루프 위에 자막 "300km/h를 세우는 원판, 속은 이렇게 생겼다" |
| **다음 편 콜드오픈 0~2초** | 이번 편 SIG 루프의 마지막 1초(조립·체결) → 하드컷 → 다음 편 SIG-A. 시리즈가 이어진다는 신호 |
| 본편 S4 대체(선택) | 본편 4-1(1/4 단면)을 SIG-2로 바꾸면 S4 진입 직전에 캘리퍼가 들리는 비트가 생김. 다만 이 경우 본편 대사 "집게처럼 … 물어버립니다"와 순서가 어긋나지 않도록 S2는 그대로 둠 |

**키프레임 재사용**: SIG-A = REF-1′(본편 공용), SIG-C의 단면 형태 = 본편 KF-K1과 같은 규칙. 새로 생성할 것은 **SIG-B·SIG-C 편집 2장 + 클립 2개**뿐입니다.
