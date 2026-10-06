# 《얇은 한 장》 — Omni 1.1 장면설계 v3

> 입력: `GOSEONG_V2_KEYFRAMES_A/B` 채택 CLEAN 12장 (1672×941)
> 출력 목표: 50초 · 10컷 · 16:9 · 1920×1080 · 24fps · 1,200F
> 파이프라인: **Google Flow 단독** — Omni 1.1 image-to-video / first+last frame
> 내레이션·자막·라벨(`냉열 활용 개념 모형 · AI 시각화`)·브랜드명은 전부 편집에서 얹는다. 생성 오디오는 앰비언스만 받는다.

---

## 1. 한 줄 연출 원칙 — "카메라는 물길을 따라간다"

12장은 이미 두 세계로 나뉘어 있다.

| 세계 | 컷 | 빛 | 색 |
|---|---|---|---|
| **바다** | C01 · C02 · C03 · C10 | 한낮 직사광, 맑은 하늘 | 스카이 블루 → 틸 → 심해 네이비 |
| **실험대** | C04 ~ C09 | 왼쪽 창에서 들어오는 따뜻한 오후 사광 | 크림 화이트 + 틸 + 스틸 + 코퍼 |

두 세계를 잇는 공통분모는 **틸(teal) 물색**과 **크림 화이트 여백**이다. 그래서 무빙도 하나의 문법으로 묶는다.

- **한 컷에 움직임 하나.** 패닝+줌 같은 복합 무빙 금지.
- **속도는 하나.** 모든 무빙은 "slow, steady, constant speed" — 모션컨트롤 리그처럼. 가속·흔들림·핸드헬드 금지.
- **방향은 물을 따른다.** 물이 내려가면 카메라도 내려가고, 물이 판 앞에서 멈추면(열만 건너가는 순간) 카메라도 멈춘다.

### 무빙 아크 (50초 전체의 카메라 곡선)

```
C01  C02  C03 │ C04   C05   C06 │ C07   C08   C09   │ C10
 ●    ↓    ↓  │  ⇱     →     ●  │  →     ↓     →  → │  ↑
고정 하강 하강 │ 리빌  접근  정지 │ 접근  따라   접근  │ 상승
 └ 내려간다 ┘  │ └ 물러났다 다가가 멈춘다 ┘ │ └ 다시 방과 바다로 ┘ │ 풀어준다
```

- 전반부 **하강(↓)** → 리빌에서 **후퇴(⇱)** → 원리에서 **접근(→)** 후 C06에서 **완전 정지(●)** → 후반부 다시 **접근** → 엔딩 **상승(↑)**.
- C06이 영상에서 유일하게 "카메라가 숨을 멈추는" 컷이 되도록, 앞뒤 컷은 반드시 움직인다. 정지가 핵심 문장("물은 섞이지 않습니다")의 무게가 된다.

---

## 2. Omni 1.1 입력 규칙

| 항목 | 규칙 |
|---|---|
| 프롬프트 골격 | ① 시작 화면(From the …) ② 카메라 무빙 1개 ③ 피사체 동작 ④ **Preserve** 고정 요소 ⑤ 금지 ⑥ `Audio: only …` — 예시 문장과 같은 순서·문체 |
| 시작/끝 프레임 | 시작만 = 자유 무빙. 시작+끝 = 형상을 끝 프레임에 묶어야 하는 컷(C04 리빌, C05→C06, C06 a→b)에만 사용 |
| 생성 길이 | 편집 길이 **+1초 이상 핸들**. 앞 0.5초는 버린다(첫 프레임 정착 구간) |
| 해상도 | 360p 테스트 렌더로 무빙·형상 확인 → 통과 테이크만 1080p 최종 렌더 |
| 그레인 | 프롬프트에 넣지 않는다. 생성 그레인은 프레임마다 깜빡이므로 **편집에서 전 컷 동일 그레인**을 얹는다 |
| 오디오 | 각 컷 `Audio: only …` 로 앰비언스 1~2개만. **음악·목소리 금지**를 매번 명시 |
| 파일명 | `C06_R1_t2_360.mp4` (컷·라운드·테이크·해상도) |

---

## 3. 컷별 장면설계

각 프롬프트는 그대로 복사해 Omni 프롬프트 칸에 붙인다.

### C01 · 차가운 잔의 결로 — 0:00–0:05 · F0001–0120 · 5s

- **입력**: 시작 `C01_CLEAN.png`
- **무빙**: 고정. 움직이는 것은 물방울 하나. 아래로 흐르는 물방울이 다음 컷의 "하강"을 예고한다.

```
From the fixed extreme macro of the chilled drinking glass, the camera stays completely still. The large condensation droplet in the center slowly slides a short way down the glass along its thin wet trail, keeping the small upside-down image of the sea inside it. The tiny beads around it stay in place, and the out-of-focus rocky coast behind the glass glitters softly in the sun. Preserve the glass curvature, the droplet size and the inverted reflection. No ice, no frost, no steam, no text. Audio: only a faint glassy trickle and distant soft waves, no music, no voice.
```

- **검수**: 방울 속 바다가 뒤집힌 상태 유지 / 방울이 커지거나 둘로 갈라지지 않음 / 잔에 김·서리 없음
- **실패 시**: 방울이 너무 빨리 빠져나가면 `slides very slowly, only about a tenth of the frame height` 추가

### C02 + C03 · 반수중 → 깊은 바다 — 0:05–0:14 · F0121–0336 · 9s

**A안 (권장) — 한 번의 연속 하강으로 두 컷을 생성**

- **입력**: 시작 `C02_CLEAN.png` + 끝 `C03_CLEAN.png`, 10초 이상 생성 → 편집에서 0:05/0:09 경계(F0216)에 내레이션 쉼을 둔다. 컷 없이 하강이 이어지는 것이 이 영상 전반부의 쾌감.

```
From the half-underwater view at the calm surface of a rocky, pine-lined coast, the camera sinks slowly and continuously below the waterline and keeps descending at a steady speed. The sunlit shoreline slides up and out of view, the clear teal water darkens through deep blue to near-black navy, and fine suspended particles drift gently upward past the lens as the light fades from above. Preserve the level horizon and the coastline shape while they are visible. No fish, no seabed, no divers, no text. Audio: only lapping waves above the surface that muffle into a low, quiet underwater hush, no music, no voice.
```

**B안 — 컷 분리 (A안이 중간에 형체를 만들어낼 때)**

C02 (시작 `C02_CLEAN.png`, 4s):
```
From the half-underwater view at the calm surface of a rocky, pine-lined coast, the camera sinks slowly until the waterline rises above the frame and the view is fully underwater in clear teal light. Small waves keep moving at the surface. Preserve the coastline, sand inlet and level horizon while visible. Audio: only lapping waves that turn muffled as the camera goes under, no music, no voice.
```
C03 (시작 `C03_CLEAN.png`, 5s):
```
From the dark navy deep-water view, the camera drifts slowly and steadily downward. Fine suspended particles float gently upward past the lens, and the faint light from above fades further toward black. Nothing else appears. No fish, no seabed, no light rays, no text. Audio: only a low, calm underwater hush, no music, no voice.
```
C02→C03 연결은 12F 디졸브.

- **검수**: 수면선이 화면을 수평으로 가르며 올라감(2분할 레이아웃 아님) / 해안이 다른 해안으로 바뀌지 않음 / 심해에 물고기·해저·관로 등장 없음 / 마지막 1초가 거의 암흑

### C04 · 개념 모형 리빌 — 0:14–0:20 · F0337–0480 · 6s ★시그니처

- **입력**: 시작 `omni_frames/C04_START_TANK.jpg` + 끝 `C04_MASTER_CLEAN.png`
  - `C04_START_TANK.jpg` 는 C04 키프레임의 수조 내부를 1920×1080 으로 잘라 키운 프레임(이 저장소에 포함). 같은 이미지에서 잘랐으므로 끝 프레임과 색·조명이 정확히 이어진다.
- **무빙**: 연속 풀백. C03의 "깊은 바다"가 실은 실험대 수조 안의 물이었다는 것을 문구 없이 보여준다.

```
Starting inside the teal water of a tall glass tank, with a thin column of bubbles rising, the camera pulls back slowly and continuously to reveal the whole tabletop model on a pale bench: the glass tank on the left, the small steel pump, the steel-and-glass heat exchanger in the center, and the white paper model room on the right. Water keeps pouring from the arched tube into the tank. Preserve every tube, port and connection exactly as in the final frame; the two tube loops never touch each other. No text, no people, no hands. Audio: only soft room tone and a quiet, steady pump hum, no music, no voice.
```

- **검수**: 관이 새로 생기거나 두 회로가 이어지지 않음 / 열교환기 중앙 판 끊김 없음 / 마지막 1초가 `C04_MASTER_CLEAN` 과 같은 구도
- **실패 시**: 풀백 중 장치가 녹아내리듯 형성되면 → 시작 프레임 없이 `C04_MASTER_CLEAN.png` 만 넣고 아래 프롬프트로 "고정 와이드 + 미세 푸시인", C03→C04는 하드컷(§4)
```
From the fixed wide view of the tabletop model on a pale bench, the camera pushes in very slowly, almost imperceptibly. Water keeps pouring from the arched tube into the glass tank, and the clear tubes catch the soft window light. Preserve every tube, port and connection exactly; the two tube loops never touch. Audio: only soft room tone and a quiet, steady pump hum, no music, no voice.
```

### C05 · 서로 다른 두 물길 — 0:20–0:25 · F0481–0600 · 5s

**A안 (권장) — C06 매크로까지 한 번에 밀고 들어감**

- **입력**: 시작 `C05_CLEAN.png` + 끝 `C06a_CLEAN.png`
- **무빙**: 판 중앙을 향한 직선 푸시인. 끝 프레임이 C06의 첫 프레임이라 C05→C06이 컷 없이 이어진다.

```
From the medium view of the steel-and-glass heat exchanger, the camera pushes in slowly and straight toward the central titanium plate until the two glass channels fill the frame. Inside the left teal channel, faint refractive ripples drift upward; inside the right clear channel, they drift downward. The fine dot pattern behind the glass stays fixed and never crosses the plate. Water keeps pouring into the tank at the left edge. Preserve the opaque plate, frame bolts, ports and tubes. Audio: only a small, steady pump and gentle flowing water, no music, no voice.
```

**B안 — 단독 푸시인 후 C06로 하드컷**

- **입력**: 시작 `C05_CLEAN.png`
```
From the medium view of the steel-and-glass heat exchanger, the camera pushes in very slowly toward the central titanium plate. Inside the left teal channel, faint refractive ripples drift upward; inside the right clear channel, they drift downward. The fine dot pattern behind the glass stays fixed and never crosses the plate. Water keeps pouring into the tank at the left. Preserve the opaque plate, frame bolts, ports and tubes. Audio: only a small, steady pump and gentle flowing water, no music, no voice.
```

- **검수**: **왼쪽(해수) 위로 · 오른쪽(건물수) 아래로** — 방향이 바뀌면 탈락 / 점무늬가 물속 입자처럼 흘러가면 탈락 / 판에 틈·투명 구간 생기면 탈락

### C06 · 얇은 판과 굴절 변화 — 0:25–0:33 · F0601–0792 · 8s ★핵심

- **입력**: 시작 `C06a_CLEAN.png` + 끝 `C06b_CLEAN.png`
- **무빙**: **완전 고정.** 영상에서 유일하게 카메라가 멈추는 컷.
- **8초 리듬**: 2초 정지(두 물길 인지) → 4초 각 유로 안 굴절 변화 → 2초 가라앉음(분리된 경계 확인)

```
Locked-off macro of the opaque titanium plate between two glass channels; the camera does not move at all. For the first two seconds everything is almost still. Then the black-and-white dot pattern behind each channel shimmers softly by refraction only: strongly in the right clear channel at first, gradually calming, while a faint local shimmer appears in the left teal channel close to the plate. The dots themselves stay fixed in place. In the last two seconds everything settles. Nothing crosses the plate: no water, no dots, no light. The plate stays solid, opaque and unbroken. Audio: near silence, only a very faint flowing hum, no music, no voice.
```

- **검수 (하나라도 걸리면 탈락)**: 판을 넘는 무늬·빛·물 / 판이 투명해지거나 틈 / 점이 떠다님(입자로 읽힘) / 화살표·글로우·색 번짐 / 카메라 미세 흔들림
- **실패 시**: 무늬가 과하게 요동치면 `the shimmer is subtle, like heat haze seen through glass` 로 강도를 낮춘다. 그래도 판을 넘으면 시작·끝 모두 `C06a_CLEAN.png` 로 넣고 굴절을 오른쪽 채널에만 한정.

### C07 · 모형 방의 팬코일 — 0:33–0:38 · F0793–0912 · 5s

- **입력**: 시작 `C07_CLEAN.png`
- **무빙**: 창 쪽으로 느린 푸시인. 바람이 코일에서 방 안으로 가는 방향을 카메라가 따라간다. 창으로 다가가는 끝 감각이 C09 창 매치컷을 예고한다.

```
From the three-quarter view of the white paper model room, the camera pushes in slowly toward the window. The small fan behind the copper coil turns softly, and the gentle airflow makes the sheer curtain sway lightly into the room. Water stays inside the clear tubes and the copper coil; nothing sprays, drips or mists. Preserve the four coil rows, the fins, the window frame, the armchair and the rug. No text, no people. Audio: only a small, soft fan whir and quiet room tone, no music, no voice.
```

- **검수**: 코일 밖으로 물·안개 없음 / 커튼이 팬 쪽(왼쪽)에서 오는 바람 방향으로 움직임 / 의자·창 위치 고정

### C08 · 해수의 출구 — 0:38–0:42 · F0913–1008 · 4s

- **입력**: 시작 `C08_CLEAN.png`
- **무빙**: 물줄기를 따라 느린 틸트다운. 후반부 유일한 "내려가는" 무빙으로 C02·C03 하강과 운을 맞춘다(바다로 돌아간다).

```
From the close view of the curved glass outlet tube, the camera tilts slowly down, following the clear stream as it pours into the open glass tank. Concentric ripples spread calmly across the teal surface. The stream stays clear and cool-looking, never steaming, boiling or glowing. Preserve the tube bend, the tank rim and the soft window light behind. Audio: only a steady, gentle pouring of water, no music, no voice.
```

- **검수**: 배출수가 붉거나 김이 나지 않음 / 화면에 두 번째 관·포트가 생기지 않음

### C09 · 모형 방 → 실제 방 — 0:42–0:46 · F1009–1104 · 4s (2s + 2s)

- **입력**: 두 번 따로 생성. `C09_MODEL_CLEAN.png` 시작 / `C09_REAL_CLEAN.png` 시작
- **무빙**: 두 테이크 모두 **같은 속도의 아주 느린 푸시인**. 같은 속도로 움직이는 두 화면을 붙여야 하드 매치컷이 "같은 방이 현실이 됐다"로 읽힌다. 두 프롬프트는 재질 단어만 다르다.

MODEL:
```
From the frontal view of the white paper model room, the camera pushes in very slowly toward the window, about five percent over the whole shot. The sheer curtain sways gently once to the right in a soft breeze, and sunlight glints on the sea outside. Preserve the window frame position and size, the curtain rod, the armchair and the rug exactly. No people. Audio: only quiet room tone and distant soft waves, no music, no voice.
```
REAL:
```
From the frontal view of the real sunlit room, the camera pushes in very slowly toward the window, about five percent over the whole shot. The sheer curtain sways gently once to the right in a soft breeze, and sunlight glints on the sea outside. Preserve the window frame position and size, the curtain rod, the armchair and the rug exactly. No people. Audio: only quiet room tone and distant soft waves, no music, no voice.
```

- **편집**: MODEL 2초 → REAL 2초. **커튼이 같은 위상(오른쪽으로 가장 많이 젖혀진 순간)인 프레임에서** 자른다. 창틀 외곽 오차는 REAL 쪽을 1~2% 스케일·위치 보정으로 맞춘다.
- **B안 (실험용)**: 시작 MODEL + 끝 REAL 한 테이크로 `the paper walls, frame and fabric quietly turn into real plaster, wood and linen` — 모핑이 눈에 띄면 폐기하고 하드컷 유지.

### C10 · 고성 해양심층수 — 0:46–0:50 · F1105–1200 · 4s

- **입력**: 시작 `C10_CLEAN.png`
- **무빙**: 천천히 상승하며 살짝 틸트업. 수평선이 하단 1/3로 내려가며 하늘 여백이 타이틀 자리가 된다. 영상 전체에서 유일한 "위로" 무빙 = 해방감.

```
From the wide view of the rocky, pine-lined coast, the camera rises slowly and tilts up slightly, letting the calm horizon settle toward the lower third and opening clean sky for a title. Small waves break softly over the granite rocks and the sea glitters in the sun. Preserve the coastline, the distant headland and the straight horizon. No text, no boats, no people. Audio: only gentle waves and a soft breeze, no music, no voice.
```

- **검수**: 수평선 기울지 않음 / 하늘에 글자·새 떼 등 잡요소 없음

---

## 4. 편집 연결

| 경계 | 방법 | 사운드 브리지 |
|---|---|---|
| C01 → C02 | 하드컷. 흘러내리는 물방울(↓) → 가라앉는 카메라(↓) 모션 매치 | 먼 파도를 C01부터 깔아 C02로 이어줌 |
| C02 → C03 | A안: 연속 / B안: 12F 디졸브 | 수면음 → 수중 저역 |
| C03 → C04 | A안 리빌이면 컷 위치에서 바로 C04 시작. **암흑→틸** 밝기 점프가 리빌의 박자 | J컷: 펌프 험을 6F 먼저 |
| C04 → C05 | 하드컷(같은 축, 같은 장치) | 펌프 지속 |
| C05 → C06 | A안: 연속 / B안: 하드컷 | **C06 진입과 동시에 음악 완전 제거** |
| C06 → C07 | 내레이션 "…전달됩니다." 끝난 뒤 0.5초 정지 후 하드컷 | 팬 소리 진입 |
| C07 → C08 | 하드컷 | 팬 → 물 붓는 소리 크로스페이드 |
| C08 → C09 | 하드컷 | 룸톤 + 먼 파도 |
| C09 MODEL → REAL | 커튼 위상 매치 하드컷 | 파도가 한 단계 커짐(창밖 바다가 현실이 됨) |
| C09 → C10 | 하드컷 | 파도 + 낮은 음악 한 박 |

### 그레이딩 (전 컷 동일 규칙)
- 바다 컷(C01·C02·C10)은 채도 −10%, 하이라이트를 실험대의 크림 화이트 쪽으로 살짝 따뜻하게 → 두 세계의 온도차 축소
- 실험대 컷의 틸과 바다 컷의 틸을 같은 색상값으로 맞춤(벡터스코프에서 한 점)
- 블랙은 살짝 들어 C03 네이비도 "검정"이 아니라 "깊은 남색"으로 유지
- 그레인·약한 헐레이션은 마지막에 전 컷 동일 값으로

---

## 5. 생성 순서

위험한 것부터, 기준 형상을 먼저 잠근다.

1. **C06** (a→b) — 판·무늬 규칙 통과가 영상 성립 조건
2. **C05** A안 (→C06a) — 통과하면 C05/C06이 한 덩어리로 확정
3. **C04** 리빌 — 실패 시 고정 와이드 B안
4. **C07 · C08**
5. **C09** MODEL/REAL — 두 테이크 속도 비교 후 쌍으로 채택
6. **C02+C03** A안 → 실패 시 B안
7. **C01 · C10**

각 컷: 360p 2~4테이크 → 검수표 통과 1개 → 1080p 렌더 → 프롬프트·입력 프레임·테이크 번호를 `03_prompts.md` 에 기록(출품 시 제작 과정 증빙).
