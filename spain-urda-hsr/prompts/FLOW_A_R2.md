# 버전 A — 장면 구성 + 프롬프트 R2 (키프레임 imagegen → Flow 영상)

> R1(`FLOW_A_R1.md`)을 검토해 고친 판. R1은 기록용으로 남기고 **생성은 이 파일로** 한다.
> 45초 · 24fps · 1080F · 9:16. 컷 프레임은 `BEATS.csv`, 수치 근거는 `evidence/braking_calc.json`, 고정 문구는 `LOCKS.md`.

---

## 0. R1 → R2에서 바꾼 것

| # | R1 | 문제 | R2 |
|---|---|---|---|
| 1 | 키프레임을 Flow 이미지 생성으로 | 사용자가 키프레임은 imagegen으로 하기로 함 | **CLEAN·INFO 키프레임 = imagegen, 움직임 = Flow.** INFO와 짝 컷은 imagegen의 참조 이미지 편집 기능으로 |
| 2 | 프롬프트에 `[LOCK]` 태그만 | imagegen에는 완성 문장을 붙여야 함 | `build_prompts.py`가 LOCKS.md를 읽어 **붙여 넣을 완성 프롬프트 파일**을 `prompts/out/`에 만든다. 손으로 LOCK을 다시 쓰지 않는다 |
| 3 | K02·K06 "열차 맨 앞에서 본 시점" | imagegen이 화면에 열차나 운전대를 그릴 위험 | "선로 위에 낮게 놓인 카메라, 열차는 보이지 않음"으로 명시 |
| 4 | K03 INFO 숫자를 띠 끝에 | 1.5 km 띠 끝은 지평선 근처라 숫자가 작아짐 | 숫자는 띠 **옆 중간 거리**에 |
| 5 | K09에 [SITE LOCK — MAIN LINE] | 9 km 고도에서 복선·전주 서술이 맞지 않음 | 전용 `[SITE LOCK — SATELLITE]` 추가 |
| 6 | K08 STYLE LOCK을 문장으로 고쳐 쓰라고 함 | 라운드마다 문구가 흔들림 | `[STYLE LOCK — INTERIOR]` 추가 |
| 7 | K10 카메라가 정차 열차 뒤, 신호는 열차 너머 | 적색 신호가 너무 작고, "신호 앞에 섰다"가 안 읽힘 | 카메라 가장 가까이에 적색 신호기, 그 너머에 **신호 앞에 멈춰 선 열차 정면** |
| 8 | 검수 항목이 컷마다 1줄 | 장면 구성 근거가 없음 | 컷마다 목적·구성·카메라·여백·싱크·금지·검수를 적음 |

---

## 1. 작업 흐름

```
imagegen CLEAN (9장) ─┐
                      ├─ 검수(basak-shorts-review) ─ imagegen INFO (5장, CLEAN 참조 편집) ─ 검수
                      │
                      └─ Flow: Frames to Video(시작 CLEAN → 끝 INFO) 또는 Image to Video(CLEAN 1장)
                                  → MP4 11개 → 검수 → capcut-dual-look → 편집 → 자막(R08) → 믹스
```

### imagegen 규칙
- **화면비 9:16**로 생성한다. 모델이 9:16을 지원하지 않고 2:3(1024×1536 등)만 되면, 피사체를 가운데에 두고 생성한 뒤 **좌우를 각각 8%씩 잘라** 9:16으로 만든다(2:3 → 9:16은 가로 16% 손실). 프롬프트의 "가장자리" 요소(전주, 이웃 선로)는 잘려도 되지만 주 피사체와 INFO 여백은 가운데 68% 안에 있어야 한다.
- 폭 1080px 이상. 모자라면 Flow에 넣기 전에 업스케일한다.
- INFO와 짝 컷(K06, K11)은 **참조 이미지를 첨부한 편집**이다. 새로 그리게 하지 않는다. 결과가 참조와 카메라·형상이 다르면 그 라운드는 불합격이다.
- 한글·글자 생성 금지. INFO의 숫자는 라틴 숫자 + 단위 하나만.
- 파일명: `K03_CLEAN_R1_a.png`처럼 컷·패스·라운드·테이크. 채택본은 `clean/adopted/K03_CLEAN.png`로 복사.

### Flow 규칙
- Frames to Video는 시작·끝 프레임이 **같은 화면비**여야 한다(9:16). T0에서 1회 확인.
- 클립 길이는 컷 길이보다 한 단계 길게(3초 컷 → 4초, 4.5초 컷 → 6초) 뽑고 편집에서 자른다.
- 영상 프롬프트에는 장면 묘사를 다시 쓰지 않는다. **움직임과 타임라인만** 쓴다. 장면은 프레임이 이미 담고 있다.
- 같은 증상 3회 연속이면 샷을 재설계한다(`prompt-repair.md` 기준).

### 생성 순서 (위험한 것부터, 짝은 순차)

| 순서 | 컷 | 이유 |
|---|---|---|
| 1 | K09 CLEAN → INFO | 같은 선로 위 두 지점이 성립해야 영상이 성립 |
| 2 | K03 CLEAN → K03 INFO → **K07 INFO**(같은 CLEAN) | 영상의 논지 쌍 |
| 3 | K04 CLEAN → INFO | 케이블 형상. K05는 새 이미지 없음 |
| 4 | K02 CLEAN → **K06 CLEAN**(K02 참조) → K06 INFO | 쌍 |
| 5 | K01 CLEAN → **K11 CLEAN**(K01 참조) | 루프 쌍 |
| 6 | K10, K08 | 단독 컷 |

CLEAN 9장(K01 K02 K03 K04 K06 K08 K09 K10 K11) · INFO 5장(K03 K04 K06 K07 K09) · MP4 11개

---

## 2. 컷별 장면 구성과 프롬프트

표기: **근**(카메라에 가장 가까운 것) / **중** / **원**(가장 먼 것). 프레임을 위·아래로 나눠 말하지 않는다 — 2분할 유발.
`[...]` 태그는 `build_prompts.py`가 LOCKS.md 본문으로 바꾼다.

---

### K01 — W0 훅 · 주행 중인 고속열차 (F1–96 · 4.0s · N1)

**목적** 첫 프레임에서 "고속열차"가 읽히고 이미 움직이고 있어야 한다. 추모 톤이라 낮은 해, 긴 그림자, 조용한 색.
**구성** 근: 도상 어깨와 침목 끝이 모션블러로 흐름 / 중: 열차 후방 3/4, 선명, 편성이 길게 보임 / 원: 직선 복선이 지평선 안개 속으로. 열차 앞의 빈 선로가 열차와 같은 비중.
**카메라** 선로 옆 도상 어깨, 높이 1.2 m, 열차 뒤쪽 약 60 m, 35 mm 느낌. 열차 진행 방향으로 추적.
**빛** 동남쪽 낮은 해(고도 7°), 열차 측면에 긴 그림자.
**여백** INFO 없음. 자막은 화면 아래 1/4(열차가 거기 걸리지 않게 열차는 중간 거리에).
**싱크** N1 "스페인 고속열차 추돌사고로…" — 명사 "고속열차" 발화 전에 열차가 보여야 하므로 F1부터 열차.
**금지** 실제 도장색(보라·빨강), 글자, 승객 얼굴, 파손.

**CLEAN (imagegen)**
```
The camera stands low on the ballast shoulder beside a high-speed railway line, about
sixty metres behind a high-speed train that is already running away from the camera at
full speed. Nearest to camera the ballast stones and sleeper ends streak with motion blur.
In the middle distance the train is sharp and clearly readable as one long high-speed
train seen from its rear three-quarter, its full length visible. Beyond the train the
straight double track continues open and empty toward a hazy horizon; that open track
ahead of the train is as important to this frame as the train itself. The horizon sits a
little above the middle of the frame.
[TRAIN LOCK]
[SITE LOCK — MAIN LINE]
[STYLE LOCK]
```

**MP4 (Flow · Image to Video · K01 CLEAN · 4s)**
```
The camera tracks along the line at the same speed as the train and keeps the same
distance behind it. The train runs steadily away along the straight track; ballast streaks
past nearest to camera. Smooth, steady, no shake, no cut. The train is already moving in
the very first frame and never slows.
```

**검수** F1에 열차 실루엣 ✔ / 레일이 프레임 밖으로 끊기지 않음 / 차체에 글자·로고 0 / 열차가 자막 영역(아래 1/4)에 걸리지 않음 / 지평선이 가운데 근처(K11 쌍 기준)

---

### K02 — 선로 시점, 고속 · 앞이 비어 있다 (F97–168 · 3.0s · N2)

**목적** "앞차를 보고 멈추지 않는다"의 전제: 아무리 봐도 앞은 비어 있고, 보이는 거리는 제동거리보다 짧다.
**구성** 근: 침목이 줄무늬로 흐름 / 중: 두 레일이 빠르게 모임 / 원: 소실점, 안개. 선로 위에 아무것도 없다.
**카메라** 선로 정중앙, 레일 상면에서 1.0 m 높이, 진행 방향을 똑바로 봄. **열차·운전대·유리창은 보이지 않는다.** 선로 자체가 시점이다.
**여백** 없음(K06 INFO가 같은 구도를 쓰므로 중간 거리 레일 사이 도상이 비어 있어야 한다).
**싱크** N2 전체 3초.
**금지** 운전실 내부, 계기판, 손, 와이퍼.

**CLEAN (imagegen)**
```
A forward view along a high-speed railway track from a camera placed exactly over the
centre line of one track, one metre above the rail tops, looking straight ahead along the
rails. No train, no cab, no windscreen and no dashboard are visible; the view is the track
itself. Nearest to camera the concrete sleepers blur into streaks of fast motion; further
along, the two rails converge smoothly to a vanishing point on the centre line, far away
in light haze. THE SUBJECT IS THE LONG EMPTY TRACK AHEAD: it runs to the horizon and
nothing stands on it. The neighbouring track and the catenary masts pass at the very
edges of the frame.
[SITE LOCK — MAIN LINE]
[STYLE LOCK]
```

**MP4 (Flow · Image to Video · K02 CLEAN · 4s → 3s)**
```
Fast, continuous forward motion along the track. Sleepers stream toward and under the
camera; the vanishing point stays fixed on the centre line. No cab, no dashboard, no
driver appears. Steady, no shake.
```

**검수** 열차·운전대 0 / 카메라가 선로 정중앙(좌우 레일 대칭) / 레일 사이 중간 거리가 비어 있음

---

### K03 — 시속 200, 정지거리 1.5 km 넘게 (F169–276 · 4.5s · N3)

**목적** 영상의 첫 숫자. 열차 길이와 비교해 정지거리가 얼마나 긴지 한 화면에.
**구성** 근: 열차(측후방, 길이 200 m가 한눈에) / 중~원: 열차 코 앞으로 **빈 선로가 아주 멀리** 뻗음, 지평선 안개. 열차는 화면 아래쪽 1/3 안, 빈 선로가 나머지를 차지.
**카메라** 고도 150 m, 선로 축에서 옆으로 약 25°, 아래로 약 30° 내려다봄, 50 mm 느낌. 열차 진행 방향으로 선로를 따라 봄.
**여백** 열차 코 앞 선로 전체가 INFO 띠 자리. 띠 옆 도상·들판에 숫자 자리.
**싱크** N3 "시속 200이면"(띠 시작) → "1.5킬로미터 넘게 갑니다"(띠 완성 F≈240, 숫자).
**금지** 커브, 터널, 역, 두 번째 열차.

**CLEAN (imagegen)**
```
A high oblique aerial view from about one hundred and fifty metres above the ground,
looking along a straight high-speed railway line in the direction the train is travelling.
Nearest to camera stands one high-speed train on the near track, seen from above and from
its side and rear, its whole two-hundred-metre length clearly readable. In front of the
train's nose a very long stretch of empty, straight track runs away toward the far
distance and a hazy horizon. THE SUBJECT IS THAT LONG EMPTY STRETCH OF TRACK IN FRONT OF
THE TRAIN: it must be wide open and clear for a very long distance and occupy most of the
frame, with open ballast and dry fields on both sides of it. No curve, no station, no
other train.
[TRAIN LOCK]
[SITE LOCK — MAIN LINE]
[STYLE LOCK]
```

**INFO (imagegen 편집 · K03 CLEAN 첨부)**
```
Edit the attached photograph. Keep the camera, framing, light, train, track and landscape
exactly as they are. Add one graphic only: a translucent gold band lying flat on the
ballast of the near track, starting at the nose of the train and running far ahead along
that same track toward the distance, following the perspective of the rails and fading
slightly as it gets further away. Beside the band, at mid distance on the open ground
next to the track, one gold number "1.5 km" in clean Latin digits, lying flat on the
ground in perspective. Nothing else is added.
[INFO LOCK]
```

**MP4 (Flow · Frames to Video · 시작 K03 CLEAN → 끝 K03 INFO · 6s → 4.5s)**
```
Camera almost still, a very slow push forward along the line. The train does not move.
0.0-0.6 clean scene only
0.6-1.6 a thin gold line appears at the nose of the train
1.6-4.2 the gold band extends along the track, away from the train, toward the far
        distance
4.2-5.0 the number assembles beside the band at mid distance
5.0-6.0 hold on the final composition
Nothing else changes.
```

**검수** 띠가 **열차와 같은 선로** 위 / 띠가 열차 길이의 7배 이상으로 읽힘 / 숫자 "1.5 km" 하나, 한글 0 / 열차가 자막 영역과 겹치지 않음

---

### K04 — 선로 속 케이블, 정보 펄스 (F277–372 · 4.0s · N4)

**목적** "앞을 보는 대신 선로가 알려준다"는 장치를 실물로 보여준다. LZB는 궤간 중앙에 깔린 케이블이다.
**구성** 근: 침목 하나와 클립, 납작한 검은 케이블이 선명 / 중: 케이블이 침목을 지나며 정중앙 선으로 이어짐 / 원: 소실점. 케이블이 전 구간 보인다.
**카메라** 침목 위 20 cm, 궤간 정중앙, 진행 방향으로 봄, 매크로 느낌(얕은 심도, 근경만 선명).
**여백** 케이블 자체가 INFO 펄스 자리. 숫자 없음.
**싱크** N4 "선로 속 케이블이"(케이블 선명) → "계속 알려줍니다"(펄스 흐름).
**금지** 케이블이 레일 위로 올라가거나 끊김, 발광 과다, 전선 뭉치.

**CLEAN (imagegen)**
```
A low macro photograph about twenty centimetres above the sleepers of one high-speed
track, looking straight along the track. Nearest to camera one grey concrete sleeper and
the small metal clip holding a flat dark cable are in sharp focus; beyond it the same
cable continues along the exact centre line of the track, sleeper after sleeper, toward
a vanishing point, softening with shallow depth of field. The cable is the subject and
must be clearly visible over its whole length. The two steel rails frame it on both
sides.
[SITE LOCK — TRACK MACRO]
[STYLE LOCK]
```

**INFO (imagegen 편집 · K04 CLEAN 첨부)**
```
Edit the attached photograph. Keep everything exactly as it is. Add only: a row of small,
soft teal light pulses travelling along the centre cable toward the camera, evenly
spaced, lying on the cable itself and passing behind the sleeper clips where a clip is
nearer to camera than the cable. The glow is subtle and does not light the sleepers.
No numbers, no text.
[INFO LOCK]
```

**MP4 (Flow · Frames to Video · 시작 K04 CLEAN → 끝 K04 INFO · 4s)**
```
Very slow forward dolly along the track, a few centimetres per second.
0.0-0.4 clean scene only
0.4-1.2 the far end of the cable begins to glow faintly teal
1.2-3.4 teal pulses travel along the cable toward the camera, one after another, evenly
        spaced
3.4-4.0 a steady stream of pulses, hold
```

**검수** 케이블이 궤간 정중앙에서 벗어나지 않음 / 펄스가 케이블 위에만 있음 / 침목 간격이 균일

---

### K05 — 신호가 끊김 (F373–444 · 3.0s · N5) — 새 이미지 없음

**목적** 장애를 "폭발·경고등"이 아니라 **정보가 사라지는 것**으로 보여준다. 사고 원인을 묘사하지 않는다.
**구성** K04와 동일. 펄스가 먼 쪽부터 꺼진다.
**싱크** N5 "사고 당일 아침,"(펄스 유지) → "이 신호가 끊겼습니다"(마지막 펄스 소멸 F≈420).
**금지** 붉은 점멸, 스파크, 연기, 케이블 손상.

**MP4 (Flow · Frames to Video · 시작 K04 INFO → 끝 K04 CLEAN · 4s → 3s)**
```
Camera completely still.
0.0-1.0 teal pulses keep travelling along the cable as before
1.0-2.6 no new pulses appear at the far end; the remaining pulses fade out one by one,
        from the far end toward the camera
2.6-4.0 the cable is plain and dark, nothing moves
No flashing, no red light, no sparks, no smoke. The cable itself does not change.
```

**검수** 붉은색 0 / 끝 프레임 = K04 CLEAN / 케이블 형상 변화 0

---

### K06 — 저속, 눈으로 보고 설 수 있는 속도 (F445–564 · 5.0s · N6)

**목적** 규정상의 "시계운전 40 km/h"를 K02와 같은 구도에서 **속도만 바꿔** 보여준다. 쌍 컷.
**구성** K02와 동일. 침목이 하나하나 셀 수 있게 선명. 레일 사이 중간 거리에 숫자.
**싱크** N6 "규정상 이럴 땐, 눈으로 보고 설 수 있는 속도,"(저속 주행) → "시속 40 이하입니다"(숫자 F≈530).
**금지** K02와 다른 카메라 높이·렌즈·배경.

**CLEAN (imagegen 편집 · K02 CLEAN 첨부 · 순차)**
```
Reproduce the attached photograph exactly: same camera position, same height above the
rails, same lens, same centre line, same light, same colour grade, same landscape.
Change one thing only — the speed. The track is now seen at a slow walking-to-cycling
pace: the sleepers nearest to camera are sharp and individually countable, with no motion
blur anywhere. The track ahead remains empty.
[STYLE LOCK]
```

**INFO (imagegen 편집 · K06 CLEAN 첨부)**
```
Edit the attached photograph. Keep everything exactly as it is. Add only: one gold number
"40 km/h" in clean Latin digits lying flat on the ballast between the two rails at mid
distance, foreshortened by perspective like a painted road marking. Nothing else.
[INFO LOCK]
```

**MP4 (Flow · Frames to Video · 시작 K06 CLEAN → 끝 K06 INFO · 6s → 5s)**
```
Slow, steady forward motion along the track; sleepers pass one by one, clearly visible.
0.0-1.0 clean scene only
1.0-3.0 the number assembles on the ballast ahead and slowly approaches with the track
3.0-6.0 slow steady motion continues, the number holds and stays readable
```

**검수** K02와 나란히 놓고 레일 소실점·전주 위치 일치 / 침목이 셀 수 있게 선명 / 숫자 하나

---

### K07 — 이 속도면 100 m 안에 선다 (F565–636 · 3.0s · N7) — K03 CLEAN 재사용

**목적** 영상의 결정적 비교. **K03과 같은 판** 위에 짧은 띠. 1.5 km 띠와 100 m 띠의 차이가 숫자 없이도 보여야 한다.
**구성** K03 CLEAN 그대로. 열차 코 앞에 열차 길이의 **절반**(약 100 m)짜리 띠, 끝에 주황-적색 정지선, 옆에 숫자.
**싱크** N7 "이 속도면"(띠 시작) → "100미터 안에 섭니다"(정지선 F≈620).

**CLEAN** 새로 뽑지 않는다. `clean/adopted/K03_CLEAN.png`를 쓴다.

**INFO (imagegen 편집 · K03 CLEAN 첨부)**
```
Edit the attached photograph. Keep everything exactly as it is. Add only: a short
translucent gold band lying flat on the ballast of the near track, starting at the nose
of the train and ending a short distance ahead — about half the length of the train —
with a thin orange-red stop line drawn across the track at its far end. Beside the short
band, on the open ground next to the track, one gold number "100 m" in clean Latin
digits lying flat in perspective. Nothing else is added.
[INFO LOCK]
```

**MP4 (Flow · Frames to Video · 시작 K03 CLEAN → 끝 K07 INFO · 4s → 3s)**
```
Camera still. The train does not move.
0.0-0.5 clean scene only
0.5-1.8 a short gold band draws out from the nose of the train and stops after a short
        distance
1.8-2.6 a thin orange-red stop line appears across the track at its end, then the number
2.6-4.0 hold
```

**검수** K03 INFO와 나란히: 같은 열차·같은 카메라, 띠 길이만 다름 / 띠 ≈ 열차 길이의 절반 / 정지선이 선로를 가로지름 / 숫자 하나

---

### K08 — 관제실, 교신 (F637–744 · 4.5s · N8)

**목적** "정상 운행" 지시가 나온 곳. 사람을 비난하는 그림이 아니라 **판독할 수 없는 화면 앞의 뒷모습**.
**구성** 근: 헤드셋을 쓴 운영자의 어깨·뒷머리 윤곽(어둡게) / 중~원: 흐릿한 대형 스크린 벽, 추상적인 선 다이어그램.
**카메라** 운영자 뒤 약 1.5 m, 어깨 높이, 약간 옆, 50 mm, 얕은 심도(스크린은 초점 밖).
**싱크** N8 "그런데 공개된 교신에서,"(손이 헤드셋으로) → "관제는 정상 속도 운행을 지시했습니다".
**금지** 얼굴, 읽히는 글자·지도, 실존 기관 로고·제복, 붉은 경보.

**CLEAN (imagegen)**
```
[CONTROL ROOM LOCK]
The camera is about one and a half metres behind and slightly to one side of the
operator, at shoulder height, with a 50 mm lens and shallow depth of field. Nearest to
camera the dark outline of the operator's shoulder, headset and the back of the head;
beyond, filling the rest of the frame, the wide wall of large screens, out of focus and
unreadable, glowing cool blue-grey. The operator's face is never visible.
[STYLE LOCK — INTERIOR]
```

**MP4 (Flow · Image to Video · K08 CLEAN · 6s → 4.5s)**
```
Very slow push-in toward the screens. The operator barely moves; one hand rises slowly to
the headset and stays there. The screens stay soft and unreadable. No face is shown.
Steady, no shake.
```

**검수** 얼굴 0 / 읽히는 글자 0 / 로고 0 / 어깨 윤곽이 자막 영역과 겹치지 않음

---

### K09 — 같은 선로 위, 25 km (F745–864 · 5.0s · N9) ★ 최우선

**목적** 두 열차가 **같은 선로** 위에 있었고, 그 사이가 25 km였다는 것. 충돌은 보여주지 않는다.
**구성** 위성 사진처럼 거의 수직 부감. 한 줄의 선로가 화면 가운데를 세로로 관통. 열차는 보이지 않는 크기. 근 쪽 선로 위에 청백 점(후속 열차), 원 쪽에 주황-적색 점(정차 열차), 그 사이 금색 선과 "25 km".
**카메라** 고도 약 9 km, 수직 아래, 선로가 화면 세로축과 일치.
**여백** 선로 양옆 들판 전체가 숫자 자리. 숫자는 선로 옆 중간.
**싱크** N9 "17분, 25킬로미터."(선·숫자) → "그 앞엔 멈춰 선 열차가 있었습니다"(청백 점 이동, 간격을 남기고 정지 F≈850).
**금지** 두 점이 닿음, 선로가 둘로 갈라짐, 도시, 글자.

**CLEAN (imagegen)**
```
A straight-down aerial photograph taken from very high altitude, like a satellite image.
THE SUBJECT IS ONE STRAIGHT RAILWAY LINE that runs through the exact centre of the frame
along its whole length, from nearest the camera to the far edge, unbroken and without
branching, curving or crossing another railway. Wide dry fields lie on both sides of it
for the full height of the frame. No train is visible at this height. No town, no
motorway in frame.
[SITE LOCK — SATELLITE]
[STYLE LOCK]
```

**INFO (imagegen 편집 · K09 CLEAN 첨부)**
```
Edit the attached photograph. Keep everything exactly as it is. Add only three small
graphics, all placed exactly on the railway line itself: one small blue-white marker dot
on the part of the line nearest to camera; one small orange-red marker dot further along
the same line, about three quarters of the way toward the far edge; and one thin gold
line traced precisely on top of the railway between the two dots. Beside the gold line,
on the fields next to the railway at mid distance, one gold number "25 km" in clean Latin
digits. Both dots sit on the same single railway line. Nothing else is added.
[INFO LOCK]
```

**MP4 (Flow · Frames to Video · 시작 K09 CLEAN → 끝 K09 INFO · 6s → 5s)**
```
Camera nearly still, a very slow descent.
0.0-0.6 clean scene only
0.6-1.6 the orange-red dot appears on the far part of the line and stays fixed
1.6-2.4 the blue-white dot appears on the near part of the line
2.4-3.4 the gold line traces along the railway between them and the number appears
3.4-6.0 the blue-white dot moves along the railway toward the orange-red dot and the gold
        line shortens behind it; the clip ends while a clear gap still remains between
        the two dots. The dots never touch. The orange-red dot never moves.
```

**검수** 두 점이 **같은 선로 위**(선로를 눈으로 따라감) / 끝 프레임에 간격 유지 / 선로가 한 줄 / 숫자 하나 / 영상에서 주황 점이 움직이지 않음

---

### K10 — 신호 앞에 멈춰 선 열차 (F865–936 · 3.0s · N10)

**목적** 정차 열차는 **규정대로 적색 신호 앞에 서 있었다**. 조용한 추모 컷. 아무것도 다가오지 않는다.
**구성** 근: 선로변 신호기 기둥, 적색 등 하나(화면에서 또렷하지만 작게) / 중: 신호기 조금 뒤에 멈춰 선 열차 정면, 손상 없음 / 원: 안개 속 직선 선로. 열차와 신호기 사이 짧은 빈 선로가 보인다.
**카메라** 도상 어깨, 높이 1.5 m, 신호기에서 약 15 m 앞, 선로 축에서 약 20° 옆, 85 mm 느낌(압축).
**싱크** N10 "왜 그런 지시가 나갔는지, 조사 중입니다." 화면은 거의 정지.
**금지** 다가오는 열차, 사람, 연기, 파손, 적색 외 다른 등 점등.

**CLEAN (imagegen)**
```
Ground level on the ballast shoulder of a high-speed line, early morning, very still.
Nearest to camera a slender trackside signal post with a single lit red lamp, sharp and
clearly red but small in the frame. A short stretch of empty track lies beyond the signal,
and beyond that one high-speed train stands completely still on the same track, facing
the camera, stopped a little short of the signal, undamaged, lights off. Further along,
the straight line fades into light haze. Nothing moves and nothing approaches on the line.
[TRAIN LOCK]
[SITE LOCK — MAIN LINE]
[STYLE LOCK]
```

**MP4 (Flow · Image to Video · K10 CLEAN · 4s → 3s)**
```
Camera locked off. Only the haze drifts slightly and the dry grass at the edge of the
ballast moves in a light wind. The red lamp stays lit and steady. The train does not move.
Nothing approaches.
```

**검수** 적색 등 하나, 점멸 없음 / 열차가 신호기 **뒤**(신호를 넘지 않음) / 다가오는 열차·사람·연기 0

---

### K11 — W0 복귀, 보이지 않으면 속도를 낮춘다 (F937–1080 · 6.0s · N11)

**목적** K01과 같은 구도로 돌아와 루프를 닫는다. 이번엔 열차가 **적색 신호 앞에서 감속·정지**한다 — 정상적인 보호가 작동하는 모습.
**구성** K01과 동일 카메라. 열차는 감속 중(도상 선명), 먼 선로에 적색 신호 하나.
**싱크** N11 "우리 고속철도도 같습니다."(감속 시작 F≈980) → "보이지 않으면, 속도를 낮춥니다."(정지).
**금지** K01과 다른 지평선 높이·카메라 거리.

**CLEAN (imagegen 편집 · K01 CLEAN 첨부 · 순차)**
```
Reproduce the attached photograph exactly: same camera position, same height, same lens,
same distance behind the train, same light, same colour grade, same landscape and
horizon.
Change one thing only — the state of motion. The train is now slowing smoothly: the
ballast and sleeper ends nearest to camera are sharp with no motion blur, and far ahead
on the line a slender trackside signal shows a single small red lamp.
[STYLE LOCK]
```

**MP4 (Flow · Image to Video · K11 CLEAN · 6s)**
```
The camera keeps the same position relative to the track as in the start frame. The train
decelerates smoothly and comes to rest well before the far red signal. Steady, no shake.
The framing at the end matches the start frame.
```

**검수** K01과 나란히: 지평선·레일 소실점·전주 간격 일치 / 마지막 프레임 ↔ K01 첫 프레임 SSIM 기록 / 열차가 신호를 넘지 않음

---

## 3. 편집에서 넣는 것 (생성하지 않음)

| 컷 | 자막 레이어 작은 표기 |
|---|---|
| K03 · K07 | `가정: 감속 1.0 m/s² · 반응 2초` |
| K05 · K09 | `보도 기준 · 조사 중` |
| K08 | `교신 내용은 보도 인용` |

본 자막은 basak-shorts-caption(R08)으로 확정 음성에 맞춘다. 룩은 capcut-dual-look(2초 프리뷰 → 4분할 비교 → 승인 → 일괄).

---

## 4. 라운드 1 체크리스트 (사용자)

1. `python3 prompts/build_prompts.py` → `prompts/out/` 확인
2. T0: Flow Frames to Video에 9:16 이미지 2장 → 4초 클립 1개
3. imagegen: K09 CLEAN 3~4장 → 채팅 또는 폴더로 전달 → 검수 리포트 → 채택본 저장
4. 순서표대로 진행. 짝 컷은 앞 컷 채택본을 참조로 첨부
5. CLEAN 9장 채택 후 INFO 5장 → MP4 11개
