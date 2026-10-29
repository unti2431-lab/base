# LOCKS — 스페인 우르다 고속열차 추돌 (R3)

> 프롬프트에는 태그만 붙인다. 본문은 여기 한 곳에서만 고친다. 고칠 때는 날짜·사유·영향 컷을 아래 변경 이력에 적고 라운드 번호를 올린다.

---

## FACT

상태: CONFIRMED(공식 발표·복수 매체 일치) / REPORTED(보도, 조사 중) / UNVERIFIED(확인 못 함, 사용 금지 또는 블로커)

| ID | 내용 | 상태 | 영상에서 쓰는 방식 |
|---|---|---|---|
| F01 | 2026-10-28 08:54경, 톨레도 우르다 인근 마드리드–세비야 고속선. Renfe AVE 2080이 정차 중인 Iryo 6076을 뒤에서 추돌 | CONFIRMED | N1 "추돌사고" |
| F02 | 사망 68명(카스티야라만차 주지사 발표), 늘어날 수 있음. 정부가 3일 애도 기간 선포 | CONFIRMED (수치는 변동 중) | N1 "수십 명". 숫자는 쓰지 않음 |
| F03 | 노선의 LZB 전송이 끊겼고, Iryo 기관사가 "전송 끊김"을 보고하고 우르다 진입 신호 앞에 정차 | REPORTED | N5 "이 신호가 끊겼습니다" + 화면 표기 "보도 기준" |
| F04 | 08:36 Atocha 관제가 AVE 2080에 LZB를 껐다 켜고 "marcha normal(정상 운행)"로 재개하라고 지시(교신 녹음 공개) | REPORTED (녹음 공개, 복수 매체) | N8 "공개된 교신에서" |
| F05 | LZB 없이 달릴 때는 marcha a la vista(시계운전), 최고 40 km/h (교통부 설명) | REPORTED (규정 원문 미확인) | N6 "규정상… 시속 40 이하" |
| F06 | 운행 재개부터 충돌까지 약 17분, 25 km 주행(교통부 장관) | REPORTED | N9. 계산 검증: 평균 83–88 km/h, 정지 상태 출발과 들어맞음 |
| F07 | 충돌 직전 1분 평균 137.27 km/h(Renfe Data 인용 보도) / 장관 "최대 200 km/h였을 수 있음" | UNVERIFIED (기록장치 분석 전) | **쓰지 않음** |
| F08 | Iryo는 08:41에 같은 재개 지시를 받았지만 정차를 유지했다는 보도와, 응답을 받지 못했다는 보도가 엇갈림 | REPORTED, 서로 상충 | 쓰지 않음 |
| F09 | LZB가 꺼져도 ASFA(신호기 지점 감시)가 남음. ASFA 계열의 상한은 200 km/h | REPORTED/참고 | 설명란에만 적음. 내레이션의 "200"은 물리 설명용 가정 |
| F10 | LZB는 궤도 가운데의 루프 케이블로 열차 위치를 받고, 목표 속도·거리를 열차에 계속 보냄 | CONFIRMED (기술 문헌) | N4 |
| F11 | LZB 루프 케이블은 100 m마다 교차 | UNVERIFIED-minor | 형상 디테일. B의 rig_config에만 반영하고 내레이션에는 쓰지 않음 |
| F12 | 한국 철도도 신호·열차제어 장치 장애 시 시계운전 또는 저속 주의운전으로 전환 | **UNVERIFIED — 블로커 G-1** | N11. 확인 실패 시 대체 문장 사용(PLAN §2) |
| F13 | 제동 수치는 evidence/braking_calc.json에서만 가져옴(a = 1.0 / 0.8 m/s², 반응 2 s) | 계산값(가정 명시) | N3 "1.5 km 넘게", N7 "100 m 안에" |

---

## SPEC

```
duration_design : 45.0 s  (음성 실측 후 G2에서 LOCK, 컷 경계는 ±6F 안에서 조정)
fps             : 24      (Flow 출력이 24fps라 A·B 모두 24로 고정. 프레임레이트 변환 금지)
frames          : 1080F   (t = (F-1)/24, F1–F1080)
resolution      : 1080x1920 9:16
voice           : ElevenLabs 한국어 남성 차분 톤(보이스명은 사용자 LOCK) · 습니다체
caption         : basak-shorts-caption R08 (Pretendard Bold, 흰색 + 청록 강조)
grade           : A = capcut-dual-look / B = AgX Medium High Contrast → capcut-dual-look 약하게
blender         : 4.5 LTS (bpy 4.5.14) — 버전 B만 해당
loudness        : 통합 -14 LUFS 근처, TP <= -1 dBTP
```

---

## [TRAIN LOCK]

```
a modern electric high-speed passenger train, long smooth tapered nose that narrows
to a rounded tip, low flat roofline, flush side windows in one continuous dark band,
plain matte white body with one thin graphite-grey stripe below the windows,
smooth underbody skirts, pantograph folded on the roof, no lettering, no logos,
no numbers on the body
```

- 실제 Renfe·Iryo 도장, 브랜드 색(보라·빨강)은 쓰지 않는다.
- 앞뒤 두 편성 모두 같은 LOCK을 쓴다. 두 열차의 구분은 INFO 마커 색으로만 한다.

## [SITE LOCK — MAIN LINE]

```
a modern electrified double-track high-speed railway on a slightly raised ballast
embankment crossing a wide flat dry plain of ochre and pale-brown fields, sparse
olive trees, low distant hills; continuous welded rails on grey concrete sleepers,
clean grey ballast; slender steel catenary masts with overhead wires at regular
intervals; straight alignment running toward the horizon
```

## [SITE LOCK — TRACK MACRO]

```
camera close above one track of the high-speed line: two steel rails, grey concrete
sleepers evenly spaced, clean grey ballast; one thin flat dark cable lies exactly
along the centre line of the track between the rails, clipped to each sleeper,
running away toward the vanishing point; a second thin cable runs along the foot of
one rail
```

## [CONTROL ROOM LOCK]

```
a dim modern railway traffic control room, one operator seen from behind wearing a
headset, a wide wall of large screens showing soft abstract line diagrams that are
out of focus and unreadable, cool blue-grey light, calm and quiet
```

- 실존 기관 로고·제복 금지. 얼굴이 보이지 않는다. 화면 글자는 판독 불가.

## [STYLE LOCK]  ← 프롬프트 맨 끝에 둔다

```
one single continuous vertical 9:16 photograph, no split, no seam, no panel, no border.
documentary photorealism, early autumn morning, low sun just above the horizon from the
east-south-east, long raking shadows, light haze, muted natural colours, soft contrast,
subtle film grain, calm and respectful mood, no text, no letters, no logos.
```

## [INFO LOCK]  ← INFO 패스에만

```
graphics are built into the real 3D space of the scene, follow perspective and
occlusion, and lie on or float just above the real surfaces they refer to.
colour code: teal = information flow along the cable; gold = the single key number;
orange-red = the stopped train / stop point only; restrained blue-white = neutral marks.
at most one number with a unit, written in Latin digits; no words, no Korean, no Hangul,
no letters except the unit.
```

---

## 변경 이력

| 날짜 | 라운드 | 변경 | 사유 | 영향 컷 |
|---|---|---|---|---|
| 2026-10-29 | R3 | 최초 작성 | R2 검증 결과 반영 | 전체 |
