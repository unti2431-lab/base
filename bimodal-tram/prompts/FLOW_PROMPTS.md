# Flow 프롬프트 — 바이모달 트램 R3 (자동 생성)

`tools/r3_data.py`에서 만든다. LOCK 태그 자리에는 `prompts/LOCKS.md`의 본문을 그대로 붙인다.
붙이는 순서: **프롬프트 본문 → 대상·장소 LOCK → STYLE LOCK(맨 끝)**. 선행 KF가 있으면 그 확정본을 참조 이미지로 첨부한다.

## 1. 키프레임 (Flow 이미지 생성) — 생성 순서대로

### 01. KF09A — S09 · C16

```
THE SUBJECT IS ONE SMALL PATCH OF ASPHALT SLAB SURFACE directly under a test wheel, seen in extreme close-up at the height of the slab with low grazing side light. Nearest to camera the flat specimen surface shows individual angular stones. The test wheel rests on the patch, pressing it, its tread filling about a third of the frame width; beyond the wheel the same flat surface continues and falls out of focus. The empty flat surface on the near side of the wheel is as important to this frame as the wheel itself. Vertical 9:16 framing.

[LAB LOCK — WHEEL TRACKER] [STYLE LOCK — LAB]
```

### 02. KF09B — S09–S10 · C16 · **참조 첨부: KF09A 확정본**

```
Reproduce the attached reference frame exactly: same camera position, height, lens, distance, light, grade and background. Change one thing only: the wheel has rolled out of frame, and where it pressed, the surface now holds a very shallow, soft-edged depression, barely deeper than the stones around it, made visible only by a thin crescent of shadow from the grazing light. The stones keep their hard angular shapes; nothing is cracked, melted or torn.

[LAB LOCK — WHEEL TRACKER] [STYLE LOCK — LAB]
```

### 03. KF10A — S11 · C21

```
THE SUBJECT IS THE STRAIGHT WHEEL PATH ACROSS A RECTANGULAR ASPHALT SLAB SPECIMEN, seen from a 45-degree angle with low raking light along its length. The slab is clamped in a steel mould inside the test chamber; the test wheel is parked at the far end of the slab. A plain steel straightedge without markings lies across the slab at right angles to the wheel path, resting flat on the surface, with no light visible beneath it. Vertical 9:16 framing.

[LAB LOCK — WHEEL TRACKER] [STYLE LOCK — LAB]
```

### 04. KF10B — S11 · C21–C22 · **참조 첨부: KF10A 확정본**

```
Reproduce the attached reference frame exactly: same camera, light, grade, mould, wheel position and straightedge position. Change one thing only: along the wheel path the slab now carries one smooth, shallow, rounded groove about the width of the wheel, with a faint low rounded rise along each edge. Under the straightedge a thin sliver of light shows through where the groove dips. The groove edges are soft and rounded, not knife-cut; the stones stay hard and angular.

[LAB LOCK — WHEEL TRACKER] [STYLE LOCK — LAB]
```

### 05. KF01 — S01 · C01 · C33

```
THE SUBJECT IS THE ROAD SURFACE OF A BUS STOPPING ZONE, seen from just above road level looking along the bus lane. Nearest to camera lies the worn asphalt with two shallow wheel-path grooves catching the low sunlight; a little further along begins the first precast concrete slab with a straight thin joint across the lane, and more slabs continue beyond it. Further along the lane the rear of a city bus is pulling away from the island shelter. The road surface is as important to this frame as the bus; keep it wide open and sharp. Vertical 9:16 framing.

[CITY BUS LOCK] [STOP SITE LOCK] [STYLE LOCK — FIELD]
```

### 06. KF02 — S02 · C08 · **참조 첨부: KF01 확정본**

```
THE SUBJECT IS THE BUS LANE SEEN STRAIGHT DOWN FROM HIGH ABOVE, running from the bottom edge of the frame to the top edge. Nearest the start of the lane the reddish-brown asphalt carries two darker wheel-path bands; then the lane changes to a run of pale precast concrete slabs with straight joints beside the island shelter roof; after the slabs the asphalt resumes. General traffic lanes on both sides are empty. Vertical 9:16 framing.

[STOP SITE LOCK] [STYLE LOCK — FIELD]
```

### 07. KF03 — S03 · C05 · C23 · C24 · **참조 첨부: KF01 확정본**

```
THE SUBJECT IS THE CONTACT BETWEEN ONE FRONT TYRE OF A CITY BUS AND THE ROAD, seen from the side at tyre height. The tyre is rolling slowly into the shallow groove just before the first concrete slab; the slab joint is visible a short distance ahead of the tyre. The tyre sidewall, the contact patch and the groove are all sharp. Vertical 9:16 framing.

[CITY BUS LOCK] [STOP SITE LOCK] [STYLE LOCK — FIELD]
```

### 08. KF05 — S05 · C04 · C09 · C36

```
THE SUBJECT IS A GUIDED ARTICULATED VEHICLE APPROACHING ALONG ITS OWN LANE, seen from a low front three-quarter angle. Nearest to camera the empty lane with its single centre line of small flush round plugs runs toward the vehicle; the vehicle is further along the lane, its whole length visible including the one bellows joint and all three axles. The empty lane in front of the vehicle is as important to this frame as the vehicle itself. Vertical 9:16 framing.

[VEHICLE LOCK — GUIDED ARTICULATED] [GUIDEWAY SITE LOCK] [STYLE LOCK — FIELD]
```

### 09. KF06 — S06 · C10 · C11 · **참조 첨부: KF05 확정본**

```
THE SUBJECT IS THE GAP BETWEEN A FLAT SENSOR UNIT UNDER THE FRONT OF THE VEHICLE AND ONE ROUND FLUSH PLUG IN THE ROAD, seen from road level beside the front tyre. The sensor unit is a plain dark rectangular box mounted crosswise under the floor a hand's width above the road; the round plug sits flush in the lane centre directly below it. Nothing touches; no light, no beam, no glow passes between them. The front tyre stands to one side of the plug. Vertical 9:16 framing.

[VEHICLE LOCK — GUIDED ARTICULATED] [GUIDEWAY SITE LOCK] [STYLE LOCK — FIELD]
```

### 10. KF07 — S07 · C19 · C20 · C41

```
THE SUBJECT IS THE PATTERN OF TYRE MARKS ON TWO NEIGHBOURING LANES, seen straight down from high above, both lanes running from the bottom edge of the frame to the top edge. On the guided lane the tyre marks form two narrow, sharply defined darker bands on either side of the line of round plugs. Across the low kerb, on the ordinary lane, the tyre marks are spread into two much wider, softer, fainter bands. No vehicles in frame. Vertical 9:16 framing.

[GUIDEWAY SITE LOCK — ADJACENT LANE VARIANT] [STYLE LOCK — FIELD]
```

### 11. KF04 — S04 · C07

```
THE SUBJECT IS ONE PRECAST CONCRETE SLAB BEING SET DOWN INTO AN EMPTY RECTANGULAR BED IN THE BUS LANE at night, hanging level from four chains under a small mobile crane, a hand's width above its bed. Work lights give a soft white glow; two workers in plain high-visibility vests stand far away with their backs to camera. Neighbouring slabs already laid continue beyond. No logos, no text on vests, crane or barriers. Vertical 9:16 framing.

[STOP SITE LOCK] [STYLE LOCK — FIELD]
```

### 12. KF08 — S08 · C15 · **참조 첨부: KF10A 확정본**

```
Using the attached reference for machine design, light and grade: THE SUBJECT IS THE WHOLE WHEEL-TRACKING MACHINE seen from the front at bench height, the glass chamber doors open, the test wheel mid-stroke on the slab. Wide dark space on both sides of the machine. Vertical 9:16 framing.

[LAB LOCK — WHEEL TRACKER] [STYLE LOCK — LAB]
```

### 13. KF01-D — C02 · C03 · **참조 첨부: KF01 확정본**

```
Using the attached reference for place, light and grade: the camera now sits closer to the road, travelling sideways across the worn asphalt just before the first concrete slab. The two shallow wheel-path grooves and a faint low ripple of shoved asphalt beside them fill the frame. No potholes, no cracks wider than a hairline, no water. Horizontal 16:9 framing.

[STOP SITE LOCK] [STYLE LOCK — FIELD]
```

### 14. KF11 — S12–S13 · C25–C26

```
THE SUBJECT IS AN EMPTY PATCH OF DARK WOODEN TABLETOP under a desk lamp, kept clear for a document to be placed later. Around that clear patch: plain closed grey folders, a magnifying glass, reading glasses. The clear tabletop patch is as important to this frame as the objects. Vertical 9:16 framing.

[ARCHIVE LOCK] [STYLE LOCK — LAB]
```

### 15. KF19 — S14 · C28 · **참조 첨부: KF10B 확정본**

```
Using the attached lab reference only for the straightedge: THE SUBJECT IS A PLAIN STEEL STRAIGHTEDGE BEING LAID ACROSS ONE WHEEL PATH OF THE GUIDED LANE by a gloved hand, seen from road level. The line of round plugs is visible beside the wheel path. Only the glove and forearm of the person appear. Vertical 9:16 framing.

[GUIDEWAY SITE LOCK] [STYLE LOCK — FIELD]
```

### 16. KF12 — S15 · C42 · **참조 첨부: KF01 확정본**

```
Reproduce the attached reference frame exactly: same camera position, height, lens, light, grade, shelter, slabs and grooves. Change one thing only: the vehicle pulling away further along the lane is now the guided articulated vehicle instead of the city bus. Vertical 9:16 framing.

[VEHICLE LOCK — GUIDED ARTICULATED] [STOP SITE LOCK] [STYLE LOCK — FIELD]
```

### 17. KF01-H — C06 · C23 · **참조 첨부: KF01 확정본**

```
Using the attached reference for place and composition: midsummer noon, hard high sun, faint natural heat shimmer just above the asphalt, a city bus idling at the shelter with its front wheel resting in the groove before the first slab. No thermal colours, no glow. Horizontal 16:9 framing.

[CITY BUS LOCK] [STOP SITE LOCK] [STYLE LOCK — FIELD]
```

### 18. KF13 — C13 · C14

```
THE SUBJECT IS THE SAW-CUT FACE OF AN ASPHALT SLAB seen straight on in macro, filling the frame from edge to edge, the stones sharp and angular, the black binder a thin film between them, low side light raking across the cut face. Horizontal 16:9 framing.

[SPECIMEN LOCK — CUT SLAB] [STYLE LOCK — LAB]
```

### 19. KF06-C — C10 · C26

```
THE SUBJECT IS A CYLINDRICAL CORE SAMPLE OF ROAD PAVEMENT STANDING ON A MATTE BLACK BENCH, sliced in half lengthwise so its cut face looks at the camera. In the top layer of the core a small plain cylindrical magnet sits in a drilled pocket sealed flush with the road surface. Around the core is wide empty black space. Horizontal 16:9 framing.

[SPECIMEN LOCK — CUT SLAB] [STYLE LOCK — LAB]
```

### 20. KF07B — C20 · **참조 첨부: KF07 확정본**

```
Reproduce the attached reference frame exactly: same camera, height, light, grade and lanes. Change one thing only: on the guided lane the two narrow bands are now slightly darker and very slightly sunken, catching a thin line of shadow; the ordinary lane is unchanged. Horizontal 16:9 framing.

[GUIDEWAY SITE LOCK — ADJACENT LANE VARIANT] [STYLE LOCK — FIELD]
```

### 21. KF08-W — C17 · **참조 첨부: KF08 확정본**

```
Using the attached reference for machine design, light and grade: two identical wheel-tracking machines stand side by side in the same room, both at the same distance from camera and both fully visible. Identical slabs, identical wheels, identical weight stacks. One single continuous photograph, no split, no seam. Horizontal 16:9 framing.

[LAB LOCK — WHEEL TRACKER] [STYLE LOCK — LAB]
```

### 22. KF13-R — C22 · **참조 첨부: KF13 확정본**

```
Reproduce the attached reference frame exactly in camera, light and grade. Change one thing only: the slab surface along the top of the cut face now dips in one smooth shallow rounded groove; under the groove the stones sit slightly closer together, and beside the groove the surface rises very slightly. The stones keep their shapes. Horizontal 16:9 framing.

[SPECIMEN LOCK — CUT SLAB] [STYLE LOCK — LAB]
```

### 23. KF14 — C18 · **참조 첨부: KF02 확정본**

```
Using the attached reference for place, height and grade: the bus lane seen straight down between stops, on plain reddish-brown asphalt. One city bus is passing, slightly left of the lane centre. The worn tyre bands on the asphalt are wide and soft-edged. Horizontal 16:9 framing.

[CITY BUS LOCK] [STOP SITE LOCK] [STYLE LOCK — FIELD]
```

### 24. KF15 — C12 · C35 · C23

```
THE SUBJECT IS THE CLEAN VERTICAL WALL OF A NARROW ROAD-WORKS TRENCH cut across a city lane, seen straight on in daylight: the dark asphalt surface layer at the top, a thicker grey crushed-stone base below it, compacted earth further down, and a plain drainage pipe end visible near the bottom. No people, no machines, no signs. Horizontal 16:9 framing.

[STYLE LOCK — FIELD]
```

### 25. KF16 — C27 · C34 · **참조 첨부: KF06-C 확정본**

```
THE SUBJECT IS TWO ROAD SAMPLE BLOCKS STANDING SIDE BY SIDE on a matte black bench at the same distance from camera: on the left a dark asphalt block, on the right a pale concrete block, each with the same small round flush plug set into its top surface. Equal light, equal size, wide empty space around them. Horizontal 16:9 framing.

[SPECIMEN LOCK — CUT SLAB] [STYLE LOCK — LAB]
```

### 26. KF17 — C29 · C32 · **참조 첨부: KF05 확정본**

```
Using the attached reference for vehicle shape: THE SUBJECT IS THE VEHICLE STANDING ALONE INSIDE A CLEAN, DIM MAINTENANCE DEPOT, seen side-on at waist height, full length visible, concrete floor, high roof lights off, soft daylight from a far doorway. Horizontal 16:9 framing.

[VEHICLE LOCK — GUIDED ARTICULATED] [STYLE LOCK — FIELD]
```

### 27. KF17-P — C30 · C31 · **참조 첨부: KF17 확정본**

```
Using the attached reference for depot, vehicle and grade: seen from inside the inspection pit under the vehicle, one plain work lamp lighting the underside of the floor and the drive area. Nothing broken, nothing leaking, no warning lights, no people. Horizontal 16:9 framing.

[VEHICLE LOCK — GUIDED ARTICULATED] [STYLE LOCK — FIELD]
```

### 28. KF18 — C37–C39

```
THE SUBJECT IS A TABLETOP SCALE MODEL OF ONE CITY TRANSIT CORRIDOR on a matte grey bench: a single model road with one small white articulated vehicle, two small station shelters, and a small depot building at one end, all in plain white and grey model materials. No numbers, no labels, no charts. Wide empty bench space around it. Horizontal 16:9 framing.

[STYLE LOCK — LAB]
```

### 29. KF20 — C40

```
THE SUBJECT IS ONE LANE OF A MULTI-LANE HIGHWAY SEEN STRAIGHT DOWN FROM HIGH ABOVE, with a few plain unbranded cars and trucks spaced far apart, each sitting at a slightly different position across the width of the lane. Plain white lane lines only. No text, no signs. Horizontal 16:9 framing.

[STYLE LOCK — FIELD]
```

## 2. 쇼츠 영상 (Frames to Video) — 움직임 지시

시작 프레임(필요하면 끝 프레임)에 해당 KF를 넣고, 아래 움직임 지시 뒤에 같은 KF의 LOCK 태그를 다시 붙인다. 8초로 생성해 편집에서 트림한다.

### SH-S01 — KF01 · F2V 시작=KF01

```
0.0-0.6 the bus rear is already moving away; 0.6-3.0 the bus shrinks into the distance; the camera stays still on the road surface; 3.0-4.0 an extremely slow push-in toward the first slab joint. The road does not change.
```

### SH-S02 — KF02 · F2V 시작=KF02

```
Locked overhead view; the camera descends very slightly; one distant car crosses in a general lane. The lane surface does not change.
```

### SH-S03 — KF03 · F2V 시작=KF03

```
The front tyre rolls slowly into frame, decelerates and stops inside the groove just before the slab joint; the tyre rotation matches its speed exactly; the bus body settles slightly on its suspension.
```

### SH-S04 — KF04 · F2V 시작=KF04

```
The hanging slab descends slowly the last hand's width and settles into its bed; the chains slacken; the camera stays locked.
```

### SH-S05 — KF05 · F2V 시작=KF05

```
The vehicle advances steadily toward camera along the lane until its front fills most of the frame; the bellows joint flexes only slightly; the camera stays locked.
```

### SH-S06 — KF06 · F2V 시작=KF06

```
The camera travels forward at road level together with the vehicle; the sensor unit passes over one round plug and then the next; nothing touches, nothing glows.
```

### SH-S07 — KF07 · F2V 시작=KF07

```
Locked overhead view; one guided vehicle passes along its lane with its tyres exactly on the narrow bands; moments later one bus passes in the ordinary lane slightly off-centre.
```

### SH-S08 — KF08 · F2V 시작=KF08

```
The test wheel rolls back and forth along its one straight line, steady rhythm; the camera stays locked; the wheel never moves sideways.
```

### SH-S09 — KF09A→KF09B · F2V 시작=KF09A 끝=KF09B

```
Start on the first frame with the wheel pressing; the wheel rolls away out of frame; the camera does not follow; the slab surface settles into the end frame.
```

### SH-S10 — KF09B · TRIM(S09 클립 끝 2초) 또는 F2V 시작=끝=KF09B

신규 생성 없음 — TRIM(S09 클립 끝 2초) 또는 F2V 시작=끝=KF09B

### SH-S11 — KF10A→KF10B · F2V 시작=KF10A 끝=KF10B

```
Time-lapse: the test wheel passes back and forth many times, faster and faster, as the groove deepens smoothly; the wheel parks; a gloved hand lays the straightedge across and a thin sliver of light appears beneath it, matching the end frame.
```

### SH-S12 — KF11 · F2V 시작=KF11

```
The desk lamp switches on once; dust motes drift; nothing else moves.
```

### SH-S13 — KF11 + 실제 문서 캡처 · TRIM(S12 클립) + 편집 합성

신규 생성 없음 — TRIM(S12 클립) + 편집 합성

### SH-S14 — KF19 · F2V 시작=KF19

```
A gloved hand lowers the straightedge across the wheel path and holds it still; a car passes far away.
```

### SH-S15 — KF12 · F2V 시작=KF12

```
The guided vehicle pulls away and shrinks into the distance; after it has gone the camera holds still on the road for one more second. The road surface does not change.
```

## 3. 16:9 쌍둥이 (롱폼용)

쇼츠에서 확정한 9:16 KF를 참조로 첨부하고 아래 문장 + 원래 LOCK 태그로 다시 생성한다.

```
Reproduce the attached reference scene exactly: same place, same objects, same light, same grade, same camera height and direction. Widen the framing sideways to a horizontal 16:9 composition; add only more of the same surroundings at the sides. Change nothing else.
```
