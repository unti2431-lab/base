# LOCKS — 바이모달 트램 R3 (Google Flow / Veo)

이 파일이 LOCK 문구의 유일한 원본이다. 프롬프트에는 태그만 적고, Flow에 넣을 때 이 본문을 그대로 붙인다.
문구를 고치면 이 파일만 고치고, 고친 날짜와 이유를 맨 아래 변경 기록에 남긴다. 라운드마다 다시 타이핑하면 형상이 흔들린다.

붙이는 순서는 **피사체 선언 → 장면 기술 → 대상 LOCK → 장소 LOCK → STYLE LOCK(맨 끝)**이다. 스타일을 앞에 두면 뒤의 구체 기술에 밀린다.

---

## [STYLE LOCK — FIELD]

현장(도로·정류장·차량) 장면 공통.

```
Calm documentary realism, like a careful broadcast science documentary.
Soft overcast daylight or low late-afternoon sun; raking light that reveals
small height differences in the road surface. Neutral, slightly cool colour
grade, true-to-life asphalt and concrete texture, fine film grain, moderate
contrast. Locked-off or slow dolly camera, one camera move per shot, no
handheld shake, no drone swoop. One single continuous photograph, no split,
no seam, no panel, no border. No text, no letters, no numbers, no logos, no
route signs, no painted words on the road, no UI, no HUD, no glowing
effects, no arrows.
```

## [STYLE LOCK — LAB]

시험실·시편·기록실 장면 공통.

```
Quiet pavement-materials laboratory look. Matte grey and black surfaces,
one soft side key light at a low grazing angle plus faint fill, deep
negative space. 100mm macro lens feel for close shots, 50mm for wide
shots, shallow depth of field, true-to-life stone and bitumen texture,
fine film grain, neutral grade. Locked-off or very slow motion-control
camera, one camera move per shot. One single continuous photograph, no
split, no seam, no panel, no border. No text, no letters, no numbers, no
logos, no UI, no HUD, no glowing stress colours, no arrows.
```

---

## [STOP SITE LOCK]

도심 중앙버스전용차로 정류장. 훅(S01·S02)과 엔딩(S15)에서 같은 장소로 돌아온다.

```
A median bus-only lane in the centre of a wide Korean city avenue, beside a
raised island bus shelter with a plain glass and steel canopy. The bus lane
asphalt is a muted reddish-brown. Along the stopping zone the lane is paved
with rectangular precast concrete slabs, each about one lane wide, laid end
to end with straight thin joints between them. The asphalt just before the
first slab carries two shallow wheel-path grooves and a faint low ripple.
Plain white lane lines only. Apartment blocks and street trees soft and far
away.
```

## [GUIDEWAY SITE LOCK]

유도 주행 전용 차로. 정류장과 같은 도시 룩을 유지한다.

```
A dedicated lane for a guided vehicle on the same Korean city avenue,
separated from general traffic by a low kerb. Plain dark grey asphalt. A
single line of small flush round sealed plugs runs along the exact centre
of the lane at short regular intervals, level with the surface; the two
wheel paths run on either side of that line, never on it. Plain white lane
lines only.
```

## [GUIDEWAY SITE LOCK — ADJACENT LANE VARIANT]

KF07 전용. 유도 차로와 일반 차로가 한 장면에 나란히 보인다. **이 변종은 KF07·KF07B에만 쓴다.**

```
[GUIDEWAY SITE LOCK] plus: directly beside the guided lane, across the low
kerb, runs one ordinary general traffic lane of the same width, paved with
the same dark grey asphalt.
```

---

## [VEHICLE LOCK — GUIDED ARTICULATED]

설명용 일반화 외형. 실제 차량의 도색·로고·형식을 복제하지 않는다.

```
A long low-floor rubber-tyred articulated vehicle: two body sections joined
by one flexible bellows joint, three axles, a rounded-rectangular tram-like
front with one large flat panoramic windscreen, flush side windows in one
continuous band, matte pearl-white body with a single thin charcoal stripe
along the side. No logos, no numbers, the destination screen is dark.
```

## [CITY BUS LOCK]

```
A standard twelve-metre low-floor city bus with a plain light silver-grey
body and dark windows. No logos, no numbers, the destination screen is dark.
```

---

## [LAB LOCK — WHEEL TRACKER]

실험실 휠트래킹 시험 장비(일반형). 바퀴는 **절대 옆으로 움직이지 않는다.**

```
A pavement wheel-tracking test machine: one small solid-rubber test wheel
about a hand wide, mounted on a horizontal steel arm with a short stack of
dead-weight plates above it, rolling back and forth along one fixed
straight line over a rectangular dark asphalt slab specimen clamped in a
steel mould, inside a glass-walled temperature chamber. The wheel never
moves sideways.
```

## [SPECIMEN LOCK — CUT SLAB]

```
The sawn cross-section face of an asphalt pavement slab: densely packed
angular grey stones of many sizes held together by a thin film of black
binder, a clean flat saw-cut face. The stones stay hard and angular; nothing
melts, nothing flows.
```

## [ARCHIVE LOCK]

문서 구간 배경. **가짜 문서를 만들지 않는다.** 실제 문서는 편집에서 캡처를 합성한다.

```
A quiet records-room table: a green-shaded desk lamp, plain closed grey
folders, a magnifying glass, a pair of reading glasses. Every paper surface
is blank or face down. No readable text anywhere.
```

---

## 변경 기록

| 날짜 | LOCK | 변경 | 이유 |
|---|---|---|---|
| 2026-10-08 | 전체 | R3 최초 작성 | R2 Blender 설계를 Google Flow 단독 파이프라인으로 전환 |
