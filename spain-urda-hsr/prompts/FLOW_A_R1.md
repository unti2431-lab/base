# 버전 A — Google Flow 단독 프롬프트 R1

> 사용법: `[... LOCK]` 태그 자리에 `prompts/LOCKS.md`의 해당 블록을 **그대로 복사해** 붙인다. 문구를 고치지 않는다.
> 모든 생성은 9:16 세로. CLEAN에는 그래픽을 넣지 않는다. INFO는 CLEAN을 참조 이미지로 붙여 그래픽만 더하는 두 번째 패스다. MP4는 Frames to Video(시작 = CLEAN, 끝 = INFO)로 만든다.
> 검수는 라운드마다 basak-shorts-review 스킬로 한다(CLEAN_REVIEW_R*.md).

---

## T0. 착수 전 기능 확인 (10분)

| 확인 | 방법 | 실패 시 |
|---|---|---|
| Frames to Video가 9:16 시작·끝 프레임을 받는가 | 아무 9:16 이미지 2장으로 4초 클립 1개 생성 | Ingredients to Video(9:16 지원 확인됨)에 CLEAN과 INFO를 참조로 넣고, 아래 타임라인 문장을 그대로 사용 |
| 4 / 6 / 8초 길이를 고를 수 있는가 | 생성 옵션 확인 | 8초로 생성하고 편집에서 자름 |
| 1080p 업스케일 | 다운로드 메뉴 확인 | 720p로 받아 편집에서 1080×1920으로 업스케일(화질 손실을 리포트에 기록) |

---

## 생성 순서 (위험한 컷부터, 짝 컷은 반드시 순차)

```
1  K09  25 km 부감          ← 논지 핵심. 같은 선로 위 두 지점이 성립하는지
2  K04  케이블 매크로       → K05는 새 이미지 없이 K04 INFO→K04 CLEAN 클립으로
3  K03  정지거리 1.5 km     → 4  K07 (K03 확정본을 참조로 첨부, 순차)
5  K02  운전석 전방 고속    → 6  K06 (K02 확정본을 참조로 첨부, 순차)
7  K01  W0 훅               → 8  K11 (K01 확정본을 참조로 첨부, 순차)
9  K10  정차 열차 + 적색 신호
10 K08  관제실
```

이미지 수: CLEAN 9장(K05는 K04, K07은 K03 재사용) · INFO 5장(K03, K04, K06, K07, K09) · MP4 11개

---

## K01 — W0 훅 (F1–96, 4초)

**CLEAN**
```
The camera is low on the ballast shoulder beside the line, a little behind a high-speed
train that is already moving away at speed. Nearest to camera, the ballast and sleeper
ends streak with motion blur. The train fills the middle distance, seen from its rear
three-quarter, sharp and clearly readable as a long high-speed train. Beyond the train
the straight double track continues open toward a hazy horizon; that open track ahead of
the train is as important to this frame as the train itself.
[TRAIN LOCK] [SITE LOCK — MAIN LINE]
[STYLE LOCK]
```

**MP4** (이미지 → 영상, 4초)
```
The camera tracks along the line at the same speed as the train, keeping the same
distance. The train runs away along the straight track; ballast streaks past nearest to
camera. Steady, smooth, no shake. The train is already moving in the very first frame.
```

검수: F1에 열차 실루엣이 읽히는가 / 레일이 프레임 밖으로 끊기지 않는가 / 도장에 글자·로고가 없는가

---

## K02 — 운전석 전방, 고속 (F97–168, 3초)

**CLEAN**
```
The view from just above the rails at the very front of a fast train, looking straight
down the single track the train is running on. The camera is centred exactly over the
middle of the track, no sideways offset. Nearest to camera, sleepers blur into streaks;
further along the line the rails converge to a vanishing point on the centre line.
THE SUBJECT IS THE LONG EMPTY TRACK AHEAD: it runs to the horizon and nothing is visible
on it. The neighbouring track and catenary masts pass at the edge of frame.
[SITE LOCK — MAIN LINE]
[STYLE LOCK]
```

**MP4**
```
Fast continuous forward motion along the track, sleepers streaming toward and under the
camera, the vanishing point fixed on the centre line. No cab interior, no dashboard,
no driver.
```

---

## K03 — 시속 200 정지거리 (F169–276, 4.5초 → 6초로 생성 후 자르기)

**CLEAN**
```
A high oblique aerial view from about 150 m up, looking along the line at a shallow
angle. Nearest to camera stands a high-speed train on the near track, seen from its side
and rear. In front of the train a very long stretch of empty track runs away from its
nose toward the far distance and a hazy horizon. THE SUBJECT IS THAT LONG EMPTY STRETCH
OF TRACK IN FRONT OF THE TRAIN; it must be wide open and clear for a long distance and
occupy most of the frame.
[TRAIN LOCK] [SITE LOCK — MAIN LINE]
[STYLE LOCK]
```

**INFO** (CLEAN 첨부)
```
Match the attached reference image exactly: same camera, same framing, same light,
same train, same track. Keep all of that identical.
Add one graphic only: a translucent gold band lying flat on the ballast of the near track,
starting at the nose of the train and running far ahead along the track toward the
distance, following perspective. At the far end of the band, one gold number "1.5 km".
[INFO LOCK]
```

**MP4** (Frames to Video: 시작 = K03 CLEAN, 끝 = K03 INFO, 6초)
```
Camera almost still, a very slow push forward along the line.
0.0-0.6 clean scene only
0.6-1.6 a thin gold line appears at the nose of the train
1.6-4.2 the gold band extends along the track, away from the train, toward the far distance
4.2-5.0 the number assembles at the far end of the band
5.0-6.0 hold on the final composition
The train does not move. Nothing else changes.
```

검수: 띠가 **같은 선로 위**에 있는가 / 숫자가 "1.5 km" 하나뿐인가 / 한글 0자

---

## K04 — LZB 케이블과 정보 펄스 (F277–372, 4초)

**CLEAN**
```
A low macro view about 20 cm above the sleepers of one track, looking along the track.
Nearest to camera, a concrete sleeper and the flat dark cable clipped to it are sharp;
beyond them the cable continues along the exact centre line of the track, past sleeper
after sleeper, toward a vanishing point. The cable is the subject and must be clearly
visible over its whole length.
[SITE LOCK — TRACK MACRO]
[STYLE LOCK]
```

**INFO** (CLEAN 첨부)
```
Match the attached reference image exactly. Keep everything identical.
Add only: small soft teal light pulses travelling along the centre cable toward the
camera, evenly spaced, lying on the cable itself, passing behind the sleeper clips where
the clips are nearer to camera. No numbers.
[INFO LOCK]
```

**MP4** (시작 = K04 CLEAN, 끝 = K04 INFO, 4초)
```
Very slow forward dolly along the track.
0.0-0.4 clean scene only
0.4-1.2 the cable begins to glow faintly teal at the far end
1.2-3.4 teal pulses travel along the cable toward the camera, one after another
3.4-4.0 steady stream of pulses, hold
```

## K05 — 신호가 끊김 (F373–444, 3초) — 새 이미지 없음

**MP4** (시작 = K04 INFO, 끝 = K04 CLEAN, 4초 생성 후 3초로 자르기)
```
Camera completely still.
0.0-1.0 teal pulses keep travelling along the cable as before
1.0-2.6 the pulses stop being emitted at the far end; the remaining pulses fade out one
        by one, from the far end toward the camera
2.6-4.0 the cable is plain and dark, nothing moves
No flashing, no red warning lights, no sparks.
```

검수: 붉은 점멸 0 / 케이블 형상 동일 / 끝 프레임이 K04 CLEAN과 같은가

---

## K06 — 저속 시계운전 40 km/h (F445–564, 5초 → 6초로 생성)

**CLEAN** (K02 확정본 첨부, 순차 생성)
```
Reproduce the attached reference frame exactly: same camera position, same height,
same lens, same centre line, same light, same grade, same background.
Change one thing only — the speed: the train is now moving slowly. Sleepers nearest to
camera are sharp and individually countable, no motion blur. The track ahead is empty.
[STYLE LOCK]
```

**INFO** (K06 CLEAN 첨부)
```
Match the attached reference image exactly. Keep everything identical.
Add only: one gold number "40 km/h" lying flat on the ballast between the rails at mid
distance, following perspective like a road marking.
[INFO LOCK]
```

**MP4** (시작 = K06 CLEAN, 끝 = K06 INFO, 6초)
```
Slow steady forward motion along the track; sleepers pass one by one.
0.0-1.0 clean scene only
1.0-3.0 the number assembles on the ballast ahead and approaches with the track
3.0-6.0 slow steady motion continues, the number holds
```

## K07 — 100 m 안에 정지 (F565–636, 3초) (K03 확정본 재사용)

**CLEAN** — 새로 뽑지 않는다. **K03 CLEAN을 그대로 쓴다.** 같은 판 위에서 띠 길이만 달라야 1.5 km와 100 m가 한눈에 비교된다.

**INFO** (K03 CLEAN 첨부)
```
Match the attached reference image exactly. Keep everything identical.
Add only: a short translucent gold band lying flat on the ballast of the near track,
starting at the nose of the train and ending a short distance ahead, about half the
length of the train, with a small orange-red stop line across the track at its end.
One gold number "100 m" beside the band.
[INFO LOCK]
```

**MP4** (시작 = K03 CLEAN, 끝 = K07 INFO, 4초 → 3초)
```
Camera still.
0.0-0.5 clean scene only
0.5-1.8 a short gold band draws out from the nose of the train and stops quickly
1.8-2.6 the orange-red stop line appears at its end, then the number
2.6-4.0 hold
```

검수: **K03의 1.5 km 띠와 같은 구도에서 길이 차이가 한눈에 보이는가**(이 쌍이 영상의 논지)

---

## K08 — 관제실 (F637–744, 4.5초 → 6초 생성)

**CLEAN**
```
[CONTROL ROOM LOCK]
The camera is behind and slightly to the side of the operator, at shoulder height.
Nearest to camera, the dark outline of the operator's shoulder and headset; beyond, the
wide wall of soft, out-of-focus screens.
[STYLE LOCK — replace the morning-sun sentence with: dim interior, cool screen light]
```

**MP4**
```
Very slow push-in toward the screens. The operator moves only slightly, one hand rising
to the headset. Screens stay soft and unreadable. No faces.
```

---

## K09 — 같은 선로 위 25 km (F745–864, 5초 → 6초 생성) ★ 최우선

**CLEAN**
```
A very high vertical aerial view, like a satellite photograph, looking almost straight
down. A single straight railway line runs from nearest to camera to the far distance
across a wide ochre and pale-brown plain with field patterns and sparse olive groves.
THE SUBJECT IS THE LONG STRETCH OF THIS ONE RAILWAY LINE: it runs through the centre of
the frame for its whole length, unbroken, without branching. The trains themselves are
too small to see at this height.
[SITE LOCK — MAIN LINE]
[STYLE LOCK]
```

**INFO** (CLEAN 첨부)
```
Match the attached reference image exactly. Keep everything identical.
Add only: on the railway line itself, nearest to camera, one small blue-white marker dot;
further along the same line, one small orange-red marker dot. Between them, a thin gold
line traced exactly on top of the railway. One gold number "25 km" beside that gold line.
Both dots sit exactly on the same railway line.
[INFO LOCK]
```

**MP4** (시작 = K09 CLEAN, 끝 = K09 INFO, 6초)
```
Camera nearly still, very slow descent.
0.0-0.6 clean scene only
0.6-1.6 the orange-red dot appears on the far part of the line and stays fixed
1.6-2.4 the blue-white dot appears on the near part of the line
2.4-3.4 the gold line traces along the railway between them and the number appears
3.4-6.0 the blue-white dot moves along the line toward the orange-red dot; the gold line
        shortens behind it. The clip ends while a clear gap still remains between the
        two dots. The dots never touch.
```

검수: 두 점이 **같은 선로 위**인가(레일을 따라가서 확인) / 끝에 간격이 남는가(충돌 묘사 금지) / 숫자 하나

---

## K10 — 정차 열차와 적색 신호 (F865–936, 3초)

**CLEAN**
```
Ground level on the ballast shoulder, far behind a high-speed train that stands still on
the track. THE SUBJECT IS THE LONG EMPTY STRETCH OF TRACK between the camera and the rear
of the standing train; it occupies the near and middle distance. Beyond the train, a
trackside signal shows a single red light. The train is small in the frame, at rest,
undamaged. Quiet, still morning.
[TRAIN LOCK] [SITE LOCK — MAIN LINE]
[STYLE LOCK]
```

**MP4**
```
Camera locked off. Only the haze drifts slightly and the grass at the edge of the
ballast moves in a light wind. The train does not move. Nothing approaches.
```

검수: 다가오는 열차 0 / 손상·연기·사람 0 / 신호는 적색 하나

---

## K11 — W0 복귀, 감속·정지 (F937–1080, 6초) (K01 확정본 첨부, 순차)

**CLEAN**
```
Reproduce the attached reference frame exactly: same camera position, same height,
same lens, same distance, same light, same grade, same background.
Change one thing only — the state: the train is slowing smoothly, the ballast is sharp,
and far ahead on the line a trackside signal shows a single red light.
[STYLE LOCK]
```

**MP4** (이미지 → 영상, 시작 = K11 CLEAN, 6초)
```
The camera keeps the same position relative to the line as the start frame. The train
decelerates smoothly and comes to rest well before the far red signal. Steady, no shake.
The framing at the end matches the start frame.
```
끝 프레임을 K01 CLEAN으로 강제하지 않는다(K01은 고속 블러 상태라 "감속"과 충돌). 루프는 K01과 K11 CLEAN을 같은 구도의 쌍으로 만들어 확보한다.

검수: 마지막 프레임과 K01 첫 프레임의 SSIM 기록(루프) / 적색 신호는 화면에서 작게
