# V6 지시서 — Omni 단독 · 텍스트 없는 짧은 호흡의 공학 쇼츠

> 입력 ① `FLOW_A_R3_42_HYUK_V4.mp4` 검토(`V5_42S/SCENES_V5.md`) ② 「OMNI ONLY R4 제작 마스터플랜」(첨부)
> 출력: 42.000 s · 9:16 · 1080×1920 · 24 fps · 1008F · **15샷** · 화면 글자 0
> 작성 2026-10-29. 우선순위: 이 문서 > `prompts/LOCKS.md`(사실·형상) > 첨부 마스터플랜.

---

## 0. 두 입력의 검토 결론

### 0.1 첨부 마스터플랜에서 채택하는 것
- "실사 → 평면 도식 → 실사" 구조를 버리고 **한 철도 공간 안에서 장치가 움직이고 그 결과가 다음 샷에 남는** 연출 원칙.
- 한 샷에 물리적 사건 하나. 2~3.5초 호흡. 흔들림·급줌 금지.
- 룩: 현실 80% + 공학 시각화 20%, 아침 앰버 + 네이비 그림자 + 절제된 틸.
- 시작·끝 프레임 고정으로 S12(두 열차 간격)를 가장 먼저 잠그는 순서.
- 수정용 짧은 FIX 프롬프트 4종, 같은 오류 3회 상한.

### 0.2 첨부 마스터플랜에서 **고치는 것**

| # | 마스터플랜 | 문제 | V6 결정 |
|---|---|---|---|
| 1 | 새 내레이션 10문장 | 이미 42.0 s로 녹음·측정된 V4 음성이 있고 내용도 통과. 새 대본은 42초를 넘을 가능성이 크다고 스스로 적음 | **V4 음성 LOCK.** 샷 경계는 V4 실측 무음 구간(`CUTS_V5.csv`)에서 가져옴. 재녹음은 S8 한 문장만 권장(§6) |
| 2 | 오버레이 `제동거리 약 2.6 km` | 우리 계산(a = 1.0 m/s², 반응 2 s)은 1.65 km, 보수값(0.8)도 2.04 km. 2.6 km는 a ≈ 0.6 m/s²로 근거 없음 | 숫자 자체를 쓰지 않음(텍스트 배제). 설명란에만 "1.5 km 넘게(가정 명시)" |
| 3 | 선행 열차 "dark burgundy" | Iryo 실제 도장(빨강)과 바로 연결됨. LOCKS 금지 항목 | 두 열차 모두 흰색 계열. 구분은 **선행 = 흰 차체·그라파이트 띠 / 후속 = 밝은 은회색 차체·짙은 코**로만 |
| 4 | S07 운전실 속도 표시, S08 차상장치 상태 표시 | Omni가 계기판 글자·숫자를 지어냄 → 텍스트 배제 원칙과 충돌, 판독 불가 | 계기판을 쓰지 않는다. 정보 수신은 **안테나–케이블 펄스**, 감시·제동은 **차륜 감속**으로만 보여줌(물리 사건) |
| 5 | S07 "차체 일부 반투명" | Omni 취약 구간이라고 스스로 표시 | 반투명 투시는 뺀다. 차량 하부를 **실제 저각 카메라**로 보여주면 충분 |
| 6 | 14샷 / 새 대본 기준 타임코드 | V4 음성과 맞지 않음 | 15샷, V4 문장 경계 기준(§3) |
| 7 | 오버레이 표 9종 텍스트 | 사용자 지시: 텍스트 배제 | 화면 글자 0. 공학 오버레이는 **글자 없는 도형 2종**만(§2.3) |
| 8 | 모든 샷 신규 생성 | 크레딧·검수 부담 | V4에서 통과한 K01·K02·K08·K10은 **재사용 후보**. 룩이 새 샷과 이어지면 그대로 쓴다 |

### 0.3 V5(제 이전 피드백)에서 바꾸는 것
- V5는 "원리 무대"(부채꼴·띠·리본 + 숫자·라벨)를 중심으로 했다. 텍스트 배제 지시에 맞춰 **라벨·숫자·범례 아이콘을 모두 제거**하고, 부채꼴과 띠 두 도형만 남긴다. 리본(LZB 허가 거리)은 Omni가 생성하는 케이블 펄스로 대체한다.
- 정적 무대 대신 Omni 실사 움직임 위에 도형을 얹는다. 도형은 샷당 1개, 선로에 붙어 원근을 따른다.

---

## 1. 절대 규칙

1. **화면 글자 0.** 생성 프롬프트에도, 후반 오버레이에도 문자·숫자·로고·계기판 글자를 넣지 않는다. 예외는 §1-2뿐.
2. 자막: 채널 규격(basak-shorts-caption R08) **내레이션 자막 한 줄**만 허용. 사용자가 자막도 빼기로 하면 그 단계만 생략한다(생성물은 바뀌지 않음).
3. 사실 표기("보도 기준" 등)를 화면에 쓸 수 없으므로 **설명란 첫 단락**에 고정 문구를 넣는다(§7). 이것이 없으면 공개 불가.
4. 충돌·파손·연기·불꽃·사람 얼굴·실제 도장·실존 기관 로고 금지.
5. 한 샷 = 물리 사건 하나 + 카메라 동작 하나. 샷 안에서 컷 없음.
6. 두 열차가 나오는 샷은 **같은 선로, 선행 열차 정지, 후속 열차만 이동, 접촉 없음**.
7. 같은 증상 3회 실패 → 샷의 동작을 줄이거나 시점을 바꾼다. 4회째 생성 금지.
8. 생성 전 화면에서 모델명(Omni 1.1 Flash)·계정·크레딧을 확인해 `CREDIT_LEDGER.csv`에 기록한다.

---

## 2. 룩 LOCK

### 2.1 공통 스타일(모든 프롬프트 맨 앞)
```
MASTER STYLE — SPANISH HSR ENGINEERING V6
Premium cinematic engineering documentary about high-speed railway safety.
Photorealistic European high-speed railway across a wide flat dry plain of ochre
fields in early autumn morning: low warm sun, long raking shadows, light haze,
deep navy shadows, warm steel highlights, restrained teal only for information pulses.
Documentary camera: one deliberate movement per shot, realistic focal length,
natural motion blur, no speed ramps, no shake.
Engineering elements are attached to real equipment, never floating.
One coherent railway corridor: same track geometry, same trains, same travel direction.
Vertical 9:16. No text, no letters, no numbers, no logos, no subtitles, no dialogue.
```

### 2.2 형상 LOCK
```
[TRAIN LOCK — LEAD]   plain matte white body, one thin graphite-grey stripe below the
                      windows, long smooth tapered nose, no lettering, no logos.
[TRAIN LOCK — FOLLOW] pale silver-grey body, dark graphite nose and roof line,
                      otherwise the same shape as the lead train, no lettering, no logos.
[SITE LOCK]           electrified double-track high-speed line on a low ballast
                      embankment, grey concrete sleepers, slender catenary masts,
                      straight alignment to the horizon, ochre fields, sparse olive trees.
[TRACK MACRO LOCK]    between the rails one flat dark cable lies exactly along the
                      centre line, clipped to the sleepers; a second thin cable runs
                      along the foot of one rail.
[CONTROL ROOM LOCK]   dim control room, one operator from behind with a headset,
                      wide wall of soft out-of-focus screens, cool blue-grey light,
                      no faces, no readable screens.
```

### 2.3 후반 오버레이 — 글자 없는 도형 2종만
| 도형 | 모양 | 색 | 쓰는 샷 |
|---|---|---|---|
| **보이는 거리** | 후속 열차 코에서 앞으로 옅어지는 부채꼴, 선로 폭 3배 → 1.5배 | 청백 `#CFE3F2` 35% | S03, S09, S10 |
| **멈추는 거리** | 선로 위에 깔려 자라는 띠 | 금색 `#E9B949` 60% | S05(길게, 부채꼴 밖), S10(짧게, 부채꼴 안) |

- 도형은 선로에 붙어 원근을 따르고, 열차 **진행 방향**으로만 뻗는다(V4의 거꾸로 그려진 선 재발 금지).
- 띠 길이 비율 S05 : S10 = 1654 : 84 (±5%). 숫자는 없지만 비율은 지킨다.
- 틸 펄스(LZB 정보)는 Omni 생성물 안에서만. 후반에 덧그리지 않는다.
- 깜빡임 금지. 붉은색은 선로변 적색 신호등에만.

### 2.4 색보정 목표(첨부 표 채택)
색온도 4800–5300 K, 채도 −10%, 흰 차체 클리핑 금지, 블랙은 네이비, 미세 그레인, 틸 발광은 펄스에만. V4 통과 클립과 신규 Omni 클립을 같은 LUT로 묶는다(capcut-dual-look, 4분할 비교 1회).

---

## 3. 15샷 구성 (V4 음성 경계 기준)

경계는 V4 실측 무음 구간 안(`V5_42S/CUTS_V5.csv`와 동일). 24 fps.
표기: `OMNI` 신규 생성 / `V4:Kxx` V4에서 통과한 클립 재사용 후보 / `OVL` 후반 도형.

| 샷 | 프레임 | 길이 | 내레이션(V4) | 화면 사건 (하나) | 소스 | 끝 상태 → 다음 샷 |
|---|---|---|---|---|---|---|
| S01 | 1–50 | 2.1 | 앞에는 멈춘 열차. | 적색 신호등 앞에 멈춘 선행 열차 정면, 아주 느린 푸시 | V4:K10 (룩 통과 시) | 정지 열차가 화면에 남음 |
| S02 | 51–103 | 2.2 | 뒤 열차는 왜 달렸을까요? | 높은 3/4 후방 앵글: **같은 선로** 먼 곳에 정지한 선행 열차, 가까이서 후속 열차가 달려감 | OMNI (★ 시작·끝 프레임 고정) | 간격이 조금 줄어듦. 접촉 없음 |
| S03 | 104–181 | 3.2 | 시속 200. 보고 멈추긴 어렵죠. | 운전실 전방 시점, 레일이 빠르게 모임, 전방은 안개. `OVL` 부채꼴이 코 앞에서 펼쳐짐 | V4:K02 또는 OMNI | 안개 속 소실점 |
| S04 | 182–246 | 2.7 | 제동거리는 1,000m를 넘기도 합니다. | **차륜·디스크·캘리퍼 매크로**: 고속 회전 → 제동 체결 → 회전이 줄지만 열차는 계속 전진 | OMNI (★) | 감속 중인 차륜 |
| S05 | 247–306 | 2.5 | 선로와 열차가 정보를 주고받고, | 차륜 높이에서 카메라가 **위로 상승**해 긴 직선 선로 부감. 열차는 감속하며 전진. `OVL` 금색 띠가 코 앞으로 멀리(부채꼴 밖) | OMNI | 긴 선로 + 움직이는 열차 |
| S06 | 307–372 | 2.7 | LZB가 속도를 감시하죠. | 부감에서 내려와 **레일 사이 케이블 매크로**, 카메라가 케이블을 따라 1 m 이동, 위로 차량 하부 안테나가 들어옴. 틸 펄스가 케이블→안테나→케이블 양방향 | OMNI (★) | 안테나가 케이블 위에 있음 |
| S07 | 373–451 | 3.3 | 그런데 이날, 정보 전달에 장애가 났습니다. | 같은 케이블·안테나 구도. **펄스가 먼 쪽부터 사라짐**, 케이블은 그대로. 카메라 미세 후진 | OMNI (S06 끝 프레임을 시작 프레임으로) | 펄스 없는 케이블 |
| S08 | 452–511 | 2.5 | 열차들이 (자동으로) 멈췄습니다. | 차륜으로 짧은 팬 → 회전이 줄어 **정지**. 바람에 마른 풀만 흔들림 | OMNI (S04 차륜과 같은 기준 프레임) | 정지한 차륜 |
| S09 | 512–573 | 2.6 | 재출발엔 제한 운전이 필요했죠. | 정지한 열차 측면 저각 → 선로변 신호기로 팬. `OVL` 부채꼴만 켜짐 | OMNI | 신호기와 정차 열차 |
| S10 | 574–641 | 2.8 | 당시 제한은 시속 40 이하. | 후속 열차가 **아주 천천히** 측면 트래킹, 침목이 하나씩 보임. `OVL` 짧은 금색 띠가 **부채꼴 안**에서 멈춤 | OMNI 또는 V4:K06 선명 구간 | 저속 주행 |
| S11 | 642–717 | 3.2 | 하지만 뒤 열차엔 정상 운행 지시. | 관제실 뒷모습, 손이 헤드셋으로, 화면은 흐림 | V4:K08 | 모니터 속 선로 소실점 |
| S12 | 718–785 | 2.8 | 17분 동안 약 25km. | 수직 부감: 한 줄 선로, 먼 곳 정지한 선행 열차(작게), 후속 열차가 아래에서 전진. **선행 고정, 후속만 이동** | OMNI (★★ 최우선, 시작·끝 프레임 고정) | 간격이 줄었지만 넓게 남음 |
| S13 | 786–858 | 3.0 | 앞 열차는 같은 선로에 멈춰 있었습니다. | S12와 같은 선로를 더 높은 곳에서. 선행 열차와 적색 신호가 화면 안, 후속 열차는 아래 가장자리에서 들어오다 **간격을 남기고 끝** | OMNI (S12 끝 프레임 → 시작) | 간격 유지, 접촉 없음 |
| S14 | 859–924 | 2.8 | 지시 경위는 조사 중입니다. 핵심은, | 정차 열차와 신호등, 거의 정지. 안개·풀만 | V4:K10 다른 구간 | 정적 |
| S15 | 925–1008 | 3.5 | 장애 때의 운행 절차입니다. (+꼬리 1.5 s) | **안전한 예시**: 후속 열차가 정지한 선행 열차 훨씬 앞에서 감속해 멈춤. 카메라가 뒤로 물러나며 S01 구도로 복귀 | OMNI (끝 프레임 = S01 F1) | 루프 |

- 샷 길이 2.1~3.5 s. 첨부 플랜의 "3초 이상 변화 없는 구간 없음" 규칙과 일치.
- S07은 S06의 끝 프레임을 시작 프레임으로, S13은 S12의 끝 프레임을 시작 프레임으로 **이어서 생성**한다. 끊김 없는 인과가 이 영상의 품질이다.
- 비율: 실사 철도(S01·S02·S03·S11·S14) 13.5 s / 공학 사건(S04~S10) 18.9 s / 경위·결론(S12·S13·S15) 9.3 s. 첨부 플랜의 목표 15/18/9와 맞다.

---

## 4. 샷별 Omni 프롬프트

모든 프롬프트 = `MASTER STYLE` + 해당 `[LOCK]` 본문 + 아래 동작 지시. 글자 생성 금지 문구는 MASTER STYLE에 있으므로 반복하지 않는다. 길이는 샷보다 한 단계 길게(2 s 샷 → 4 s, 3 s 샷 → 4 s) 생성해 자른다.

**S02 — 같은 선로 위 두 열차 (시작·끝 프레임 고정)**
```
[TRAIN LOCK — LEAD] [TRAIN LOCK — FOLLOW] [SITE LOCK]
Elevated three-quarter rear view along one straight track. Far along the track the lead
train stands completely still in front of a trackside signal showing one red lamp.
Nearest to camera the following train runs forward along exactly the same track.
Only the following train moves; the lead train never moves. The gap closes slightly
but stays wide. The camera dollies forward slowly, parallel to the track.
```
끝 프레임: 같은 구도, 후속 열차가 한 편성 길이만큼 전진. **검수: 레일을 눈으로 따라가 두 열차가 한 선로인지 확인. 접촉·겹침 0.**

**S03 — 운전실 전방 (V4:K02 재사용 실패 시)**
```
[SITE LOCK]
Forward view from the cab of a fast train, camera steady over the centre of the track.
Rails converge quickly to a vanishing point lost in morning haze. Nothing is visible
ahead on the track. Natural faint glass reflection. No dashboard, no instruments.
```

**S04 — 차륜·제동 매크로 (★)**
```
Extreme photorealistic macro of one high-speed train wheel, brake disc and caliper,
camera low and level, tracking alongside at the same speed. The wheel spins fast;
the caliper closes on the disc and the rotation gradually slows while the ballast
keeps streaming past, showing the train is still moving forward. Realistic steel,
grease, fine vibration. No glow, no sparks, no smoke.
```
기준 프레임: 차륜·디스크·캘리퍼만 보이는 정지 이미지 1장을 먼저 확정(imagegen 가능). S08도 같은 기준 프레임을 쓴다.

**S05 — 상승 부감 + 긴 선로**
```
[TRAIN LOCK — FOLLOW] [SITE LOCK]
The camera starts at wheel height beside the moving train and rises smoothly into a
high aerial view looking along the line, revealing a very long straight stretch of
empty track ahead of the train's nose toward a hazy horizon. The train keeps moving
forward in one direction while slowing. The long empty track ahead is the subject.
```
검수: 열차 **앞** 선로가 프레임 대부분을 차지해야 금색 띠 오버레이 자리가 생긴다.

**S06 — LZB 케이블·안테나 (★, S07의 기준)**
```
[TRACK MACRO LOCK]
Engineering macro twenty centimetres above the sleepers, camera gliding one metre along
the flat dark centre cable. From above, the underside of a train enters the frame and a
small flat antenna box hangs directly over the cable. Thin teal pulses travel along the
cable and up into the antenna, and a fainter pulse returns from the antenna to the cable.
The cable and rails stay physically realistic; only the thin pulses are teal.
```

**S07 — 펄스 소멸 (시작 프레임 = S06 마지막 프레임)**
```
Same cable and antenna, camera drifting back very slightly. The teal pulses stop
arriving from the far end; the remaining pulses fade out one by one toward the antenna
until the cable is plain and dark. The cable itself does not change. No red light,
no sparks, no flicker.
```

**S08 — 차륜 정지 (시작 프레임 = S04 기준 프레임)**
```
The same wheel, disc and caliper at track level. The rotation slows steadily to a
complete stop; the ballast stops streaming. Dry grass at the edge of the ballast
moves in a light wind. Nothing else moves.
```

**S09 — 정차 열차 → 신호기**
```
[TRAIN LOCK — FOLLOW] [SITE LOCK]
Low angle beside the stationary wheel of the following train, then the camera pans and
moves smoothly toward a slender trackside signal post ahead showing one red lamp.
The train does not move during the shot. Subtle ambient movement in dry grass only.
```

**S10 — 저속 운행 (V4:K06 선명 구간 재사용 실패 시)**
```
[TRAIN LOCK — FOLLOW] [SITE LOCK]
Stable side-tracking view at coach height. The train travels slowly and steadily;
individual sleepers and ballast stones are sharp and countable, catenary masts pass
slowly. Generic safe low-speed operation. No stop signal is passed.
```

**S12 — 수직 부감, 두 열차 (★★ 최우선, 시작·끝 프레임 고정)**
```
[TRAIN LOCK — LEAD] [TRAIN LOCK — FOLLOW] [SITE LOCK]
Near-vertical aerial view of one continuous straight railway line crossing dry fields.
Far along the line the lead train stands motionless, small, just before a red signal.
Nearer to camera the following train moves forward along precisely the same line.
Only the following train moves. The gap narrows but remains clearly open.
No overlapping bodies, no second track used, no contact.
```
시작 프레임: 간격 = 화면 높이 55%. 끝 프레임: 간격 = 35%. 두 프레임을 imagegen(동일 참조)으로 먼저 잠근다.

**S13 — 더 높은 부감, 간격 남기고 끝 (시작 프레임 = S12 끝 프레임)**
```
The camera rises higher over the same line. The stationary lead train and the red
signal stay in the upper part of the line; the following train enters from the near
edge and advances. The shot ends while a clear open stretch of track still separates
the two trains. The lead train never moves.
```

**S15 — 안전한 예시 + 루프 복귀 (끝 프레임 = S01 F1)**
```
[TRAIN LOCK — LEAD] [TRAIN LOCK — FOLLOW] [SITE LOCK]
Elevated rear view along one track. The lead train stands still far ahead before its red
signal. The following train approaches slowly and comes to a controlled stop well
before the lead train, leaving a long open stretch of track. The camera then retreats
smoothly toward the opening composition: same horizon, same vanishing point, same camera
height, same warm morning light.
```

**FIX 프롬프트(첨부 4종 채택)** — 형상·기술 정확성·카메라·기계 동작. 전체 스타일을 다시 쓰지 않고 수정 대상만 지시한다.

---

## 5. 제작 순서

| 단계 | 내용 | 통과 조건 |
|---|---|---|
| T0 | Omni에서 9:16 시작·끝 프레임 지정, 4 s 생성, 360p 프리뷰, 업스케일 옵션 확인 | 4 s 테스트 1개 |
| 1 | **S12** 시작·끝 프레임 imagegen → Omni 생성 | 같은 선로·선행 고정·접촉 0 |
| 2 | S04 기준 프레임 → S04 → S08 | 차륜 결합 유지, 회전 감속이 보임 |
| 3 | S06 → S07(이어서) | 케이블 실사 유지, 펄스가 케이블 위에만 |
| 4 | S02 → S13(S12 끝에서) → S15 | 루프 SSIM ≥ 0.95 |
| 5 | S05, S09, S10, (필요 시 S03) | — |
| 6 | V4 재사용 클립(K01·K02·K06·K08·K10) 룩 대조 → 불일치 시 신규 생성 | 4분할 비교 승인 |
| 7 | 오버레이 2종(S03·S05·S09·S10), 자막 R08(선택), 믹스, 색보정, 인코딩(bt709 행렬) | §8 QC |

360p 프리뷰로 룩 통일을 먼저 확인(S02·S04·S06)한 뒤 본 생성한다. 크레딧은 샷마다 기록한다.

---

## 6. 음성

- V4 음성 42.000 s 그대로. 자르거나 늘리지 않는다.
- 권장 재녹음 1문장: S8 "열차들이 **자동으로** 멈췄습니다" → "열차들이 멈춰 섰습니다." ("자동으로"는 미확인). 같은 보이스·설정, 1.4~2.0 s. 없으면 그대로 두되 설명란에 "정지 경위는 조사 중"을 적는다.
- 효과음(첨부 표 채택, 글자 없음): 레일 주행음 → 제동 마찰(절제) → S06 틸 펄스에 은은한 정보음 → S07 펄스 소멸과 함께 음 소거 → S11 무전 클릭 → S15 잔향이 S01 환경음으로 이어짐. 통합 −14 LUFS, TP −1 dBTP.

---

## 7. 설명란 고정 문구 (화면 글자 대신)

```
스페인 우르다 고속열차 추돌(2026.10.28) 공학 설명 영상입니다.
· 장면은 개념 재구성이며 실제 사고 장면·차량·노선 배치를 재현한 것이 아닙니다.
· 제동거리는 감속 1.0 m/s², 반응 2초 가정의 계산 예시입니다(시속 200 → 약 1.65 km).
· LZB 장애, 운행 재개 지시, 17분·25 km는 보도(교신 녹음 공개) 기준이며 조사 중입니다.
· 시속 40 이하 제한은 스페인 교통부 설명에 따른 것입니다.
· LZB 외에 ASFA 등 다른 보호 장치도 있습니다. 설명을 위해 단순화했습니다.
```
고정 댓글 Binary CTA: 1⃣ KTX 열차제어 편 / 2⃣ 고속열차 제동장치 편.

---

## 8. QC (PASS / FAIL / NOT_PERFORMED)

| 항목 | 기준 |
|---|---|
| 글자 | 모든 프레임에서 문자·숫자·로고 0 (샷당 3프레임 육안 + 자막 레이어 제외) |
| 두 열차 | S02·S12·S13·S15 전 프레임: 같은 선로, 선행 정지, 접촉 0 |
| 오버레이 방향 | 부채꼴·띠가 열차 진행 방향 |
| 띠 비율 | S05 : S10 = 1654 : 84 ± 5% |
| 인과 연결 | S06→S07, S12→S13 이음에서 케이블·열차 위치 불연속 0 |
| 리듬 | 3 s 이상 변화 없는 구간 0 |
| 룩 | V4 재사용 클립과 신규 클립 4분할 비교 승인 |
| 루프 | S15 마지막 ↔ S01 F1 SSIM ≥ 0.95, 환경음 이음 |
| 규격 | 1080×1920 · 24 fps · 1008F · bt709 행렬 · 디코드 오류 0 · −14 LUFS |
| 사실 | 설명란 §7 문구 포함, S8 재녹음 여부 기록 |

---

## 9. 사용자 결정 2건

1. **내레이션 자막(R08 한 줄)도 뺄 것인가.** 기본은 유지(45~75세 시청자, 무음 재생 대비). 빼면 자막 단계만 생략.
2. **S8 "자동으로" 재녹음 여부.**
