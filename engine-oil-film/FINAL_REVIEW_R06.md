# ENGINE_OIL_FILM R06 완성본 검수 → R07 재생성 지시
검수일: 2026-10-18
대상: `ENGINE_OIL_FILM_R06_1080_VOICE_CAPTIONS_95PX.mp4` (1080×1920, 24fps, 36.0초, H.264 / AAC 48kHz 모노)

## 결론

**훅·엔딩 실사 4컷은 살리고, 5.25~32.25초 베어링 구간(27초, 전체의 75%)은 Flow 실사 컷으로 전면 교체.**
채택 3 / 조건부 2 / 불합격 6. 장면 수 기준 확보 3/11.

이 영상의 가장 큰 문제는 개별 컷 품질이 아니라 **두 개의 영상이 이어붙은 것처럼 보인다는 점**이다.
앞뒤 9초는 Flow 실사 렌더, 가운데 27초는 플랫 셰이딩 벡터 애니메이션이다. 그리고 그 벡터 구간이
내레이션의 핵심 주장("쐐기 모양의 틈", "엄청난 압력")을 화면으로 증명하지 못한다. 유막 두께가 원 전체에서
균일해서 쐐기가 없고, 압력 표현이 없고, 하중과 회전 방향이 없다.

---

## 0. 기계 검사 결과

| 항목 | 측정값 | 판정 |
|---|---|---|
| 해상도·화면비 | 1080×1920, 9:16 | ✅ |
| 길이 | 36.0초 (Shorts 60초 이내) | ✅ |
| 컷 지점 | 1.25 / ~3.9 / 5.25 / 8.25 / 13.5 / 19.75 / 23.75 / 28.5 / 32.25 / 35.0 | 11컷 |
| 통합 음량 | **−18.3 LUFS**, TP −1.7 dBFS, LRA 2.4 LU | ⚠️ Shorts 기준 −14 LUFS 대비 4dB 작음 |
| BGM·효과음 | 없음. 문장 사이가 디지털 무음(−45dB 이하) | ❌ |
| 무음 구간 | 4.67–5.26 (0.6s), **7.30–8.43 (1.1s)**, 13.29–13.74, 19.49–19.98, 23.01–23.47, 28.17–28.64, 29.94–30.32, 31.69–32.08 | ⚠️ 총 약 4초가 공백 |
| 워터마크 | S1·S2·S11에 Flow 스파클(✦), S10에 `Veo` 문자. 베어링 구간에는 없음 | ⚠️ 컷마다 유무가 섞임 → 출처가 다른 소재라는 신호 |
| 자막 | 95px 백색+그림자, 1줄, 세로 약 1390px(72%) 위치 | ⚠️ 아래 4절 참고 |
| 참조 프레임 추출 가능 여부 | S1·S2는 전 프레임에 자막 있음 → 완성본에서 참조 추출 불가. S3 4.4–5.2초만 자막 없음 | ⚠️ 참조는 Flow 원본 클립에서 |

---

## 1. 장면별 판정

### S1 (0.00–1.25) — 한강변 고가도로 주행 세단, 저각 트래킹 · ✅ 채택 → KF-01

자막: "수천 번 폭발하는"

- 실사 품질·모션블러·도시 원경 모두 성립. S11과 같은 클립을 써서 루프가 닫히는 구조도 좋다.
- 다만 **훅 1.25초가 '평범한 주행 차'** 다. "폭발"이라는 단어가 들리는데 화면에는 폭발이 없다. 스크롤을 멈추게 할 이미지는 S2 이후에 나온다.
- 조치: 재생성 불필요. **순서만 바꾼다.** 새 훅 컷(R07-01 연소 매크로)을 0초에 놓고 S1은 엔딩 루프 전용으로 돌린다. 훅에 차를 꼭 넣고 싶으면 0.5초 이내로 줄인다.

### S2 (1.25–~3.9) — 엔진 컷어웨이 전경, 천천히 푸시인 · ✅ 채택 → KF-02 (ENGINE LOCK 기준 이미지)

자막: "엔진 속 크랭크축," / "왜 부서지지 않을까요?"

- 이 영상에서 가장 잘 나온 컷. 가공면 질감, 따뜻한 키라이트, 청록 오일 갤러리, 4기통 형상이 모두 정확하다.
- 오일 경로가 섬프 스트레이너 → 메인 갤러리 → 크랭크로 이어지는 흐름도 공학적으로 맞다.
- **이 컷의 3.0초 프레임을 `[ENGINE LOCK]` 기준 이미지로 확정한다.** 이후 엔진이 나오는 모든 컷에 참조로 첨부한다.
- 저장: `clean/adopted/KF-02_engine_cutaway_master.png` — **반드시 Flow 원본 클립(자막 없음)에서 추출한다.** 이 완성본의 S2 구간은 모든 프레임에 한글 자막이 박혀 있어서, 여기서 뽑은 프레임을 참조로 넣으면 Flow가 글자 덩어리를 재생성한다. 작업폴더에 원본 클립이 없어서 이번 검수에서는 추출하지 못했다.
- S3 마지막 프레임(5.1초)은 자막이 없어 그대로 참조 가능: `clean/reference/S3_last_frame_5.1s.png`

### S3 (~3.9–5.25) — 크랭크 저널·콘로드 매크로 · ⚠️ 조건부

질감과 조명은 S2와 완벽히 이어진다. 살릴 가치가 충분하다.

**결함:** 다음 컷(베어링 단면)으로 넘어갈 **다리 역할을 못 한다.** 크랭크 전체를 보여주다가 갑자기 플랫 그래픽 원호로 점프해서, 시청자는 "지금 어디를 보고 있는지"를 잃는다. 베어링 쉘과 오일 틈이 화면에 없다.

→ 재생성. S3 마지막 프레임을 참조로 첨부해 조명·질감·색은 그대로 두고, **메인 저널 한 곳으로 계속 파고들어 베어링 캡이 잘려 열린 상태에서 쉘과 얇은 청록 오일층이 보이는 데까지** 카메라를 밀어넣는다. 이 컷의 마지막 프레임이 R07-04(단면)의 첫 프레임과 같은 각도여야 한다. → R07-03

### S4 (5.25–8.25) / S5 (8.25–13.5) — 베어링 단면 부분 원호, 벡터 렌더 · ❌ 불합격

자막: "핵심은 바로 오일 코팅입니다." / "펌프가 오일을 쏴주면," / "회전하는 축이" / "좁아지는 틈으로" / "오일을 빨아들입니다."

1. **스타일 단절.** 앞 컷이 실사 매크로인데 여기서 단색 면·평면 셰이딩의 벡터 애니메이션으로 바뀐다. 한 편 안에서 다른 채널 영상이 끼어든 것처럼 보인다. Flow 단독 파이프라인 원칙에도 어긋난다.
2. **원의 일부만 크롭되어 구조가 안 읽힌다.** 저널(회색 큰 면)이 화면을 꽉 채워서 '축'이 아니라 '벽'이나 '터널'로 보인다. 하우징-쉘-유막-저널의 관계가 한 번도 전체로 보이지 않는다.
3. **유막 두께가 원 전체에서 균일하다.** 저널이 정중앙에 있다는 뜻이고, 이러면 "좁아지는 틈"이 존재하지 않는다. 내레이션과 화면이 정면으로 모순된다.
4. 좌상단 청색 줄무늬 블록(급유공으로 추정)과 우상단 남색 쐐기(오일 홈으로 추정)가 무엇인지 설명이 없다. 시청자에게는 장식이다.
5. 회전 방향 표시, 하중 방향 표시가 없다. 왜 한쪽 틈이 좁아지는지 원인을 보여주지 않는다.

폐기. R07-04(급유), R07-05(쐐기로 끌려 들어감)로 대체.

### S6 (13.5–19.75) — 유막 원호 초근접, 6.25초 · ❌ 불합격

자막: "이때 오일의 끈적함과" / "쐐기 모양의 틈이 만나," / "엄청난 압력의" / "오일막을 만드는데요."

- **6초 이상 거의 같은 화면.** 청록이 조금 밝아지는 것 외에 변화가 없다. 쇼츠에서 이탈이 가장 많이 나는 구간이 이런 정지성 구간이다.
- "쐐기"라는 말이 나오는 순간에도 화면의 틈은 균일한 띠다.
- "엄청난 압력"을 청록의 밝기로 표현했는데, 색 체계상 압력은 주황→적색이어야 한다. 청록은 흐름 색이라 "오일이 지나간다"로만 읽힌다.

폐기. R07-06(압력 형성)으로 대체.

### S7 (19.75–23.75) — 단면 부분 원호, S4·S5와 같은 프레이밍 · ❌ 불합격

자막: "이 얇은 막이 거대한 힘을" / "그대로 받쳐줍니다."

- S4·S5의 재사용 앵글. "거대한 힘"이 들리는데 힘(하중 화살표)도, 축이 떠오르는 움직임도 없다.

폐기. R07-07(하중을 받치며 저널이 뜸)로 대체.

### S8 (23.75–28.5) — 유막 원호 초근접 · ❌ 불합격

자막: "즉, 금속끼리 직접 닿지 않고," / "오일 위에서" / "미끄러지듯 도는 거죠."

- S6와 사실상 같은 화면의 반복. "금속끼리 닿지 않는다"를 증명하려면 **두 금속 표면 사이의 빈 틈 자체**가 피사체여야 하는데, 여기서는 원호 띠만 보인다.

폐기. R07-08(최소 틈 초근접, 틈을 피사체로 선언)로 대체.

### S9 (28.5–32.25) — 단면 부분 원호, 네 번째 재사용 · ❌ 불합격

자막: "오일을 보내는 펌프," / "압력을 만드는 회전."

- 정리 문장인데 펌프도 회전도 화면에 따로 강조되지 않는다. 같은 앵글 네 번째 등장.

폐기. R07-09(정리 + 실패 시나리오)로 대체.

### S10 (32.25–35.0) — 엔진 컷어웨이 두 번째 · ⚠️ 조건부

자막: "이 두 가지가 동시에 작동해야" / "엔진이 멈추지 않습니다."

사진은 좋다. 금색 베어링 쉘이 여기서 처음 보이는 것도 의미 있다.

**결함:** S2와 **다른 엔진**이다. 실린더 간격·피스톤 크기·카메라 높이가 달라서, 시작과 끝을 같은 엔진으로 회수하는 구조가 약해진다. 우하단 `Veo` 문자도 있다.

→ 두 가지 중 하나.
- **비용 0 안(권장):** S2 클립을 역재생해 "파고들었던 카메라가 빠져나오는" 풀백으로 쓴다. 엔진이 S2와 100% 같아진다.
- **재생성 안:** S2를 참조로 첨부하고 금색 쉘이 보이게 메인 저널 쪽에서 풀백하는 컷을 새로 뽑는다. → R07-10

### S11 (35.0–36.0) — S1 재사용 · ✅ 채택 → KF-11

루프 엔딩. 그대로 둔다. 마지막 0.65초가 완전 무음이라 루프 재생 시 끊김이 느껴진다 → 4절 오디오 참고.

---

## 2. 공학 정확도 — 대본 수정이 필요한 곳

화면을 다시 뽑기 전에 대본부터 고친다. 화면은 대본을 증명하는 용도이므로 대본이 틀리면 화면도 틀린다.

| 현재 표현 | 문제 | 수정 |
|---|---|---|
| "수천 번 폭발하는" | 단위가 없다. 일생 수천 번이 아니라 **1분에** 수천 번이다 (4기통 3000rpm ≈ 분당 6000회 연소) | "1분에 수천 번 폭발을 받아내는" |
| "핵심은 바로 오일 **코팅**입니다" | **틀린 개념.** 코팅은 표면에 붙어 있는 고정 층이다. 이 원리는 움직이는 유체가 압력을 만들어 축을 띄우는 **유체 윤활(유막)** 이다. 공학 채널에서 가장 먼저 지적받을 문장 | "비밀은 머리카락 굵기 수십 분의 일짜리 **오일막**입니다" |
| "오일을 **빨아들입니다**" | 흡입(진공)처럼 들린다. 실제로는 회전면이 점성으로 오일을 **끌고 들어간다** | "좁아지는 틈 속으로 오일을 끌고 들어갑니다" |
| "엄청난 압력" | 수치가 없어 체감이 안 된다 | "수백 기압의 압력" (엔진 베어링 유막 최대압은 수십~100MPa급) |
| "이 얇은 막이 거대한 힘을 그대로 받쳐줍니다" | 무엇이 어떻게 받치는지 빠져 있다 | "이 압력이 축을 살짝 **띄워** 폭발의 힘을 받아냅니다" |
| "엔진이 멈추지 않습니다" | 결과가 막연하다. 유막이 깨지면 금속이 닿아 **녹아 붙는다(소착)** | "막이 깨지는 순간, 금속은 녹아 붙습니다" + 엔딩 |
| (없음) | 화면 증명 포인트인 **저널 편심**이 대본에 없어서 쐐기가 왜 생기는지 설명이 안 된다 | "폭발의 힘에 축이 한쪽으로 밀리면, 틈이 쐐기처럼 좁아지고" |

### R07 대본 (목표 33~34초, 문장 간 공백 0.2초 이내)

| 컷 | 시간 | 내레이션 | 자막(강조어는 금색) |
|---|---|---|---|
| R07-01 | 0.0–2.0 | 1분에 수천 번, 폭발을 받아내는 크랭크축. | 1분에 **수천 번** 폭발을 받아내는 크랭크축 |
| R07-02 | 2.0–4.5 | 그런데 이 축, 사실 아무것에도 닿아 있지 않습니다. | 사실 **아무것에도** 닿아 있지 않습니다 |
| R07-03 | 4.5–7.5 | 비밀은 머리카락 굵기 수십 분의 일, 오일막입니다. | 비밀은 **오일막** |
| R07-04 | 7.5–11.0 | 펌프가 베어링 안으로 오일을 밀어 넣고, | 펌프가 오일을 밀어 넣고 |
| R07-05 | 11.0–15.0 | 폭발의 힘에 축이 한쪽으로 밀리면, 틈이 쐐기처럼 좁아집니다. 회전하는 축이 그 틈으로 오일을 끌고 들어가면, | 틈이 **쐐기**처럼 좁아지고 |
| R07-06 | 15.0–19.0 | 빠져나갈 곳 없는 오일이 수백 기압의 압력을 만듭니다. | **수백 기압** |
| R07-07 | 19.0–22.5 | 이 압력이 축을 띄워, 폭발의 힘을 받아냅니다. | 압력이 축을 **띄운다** |
| R07-08 | 22.5–26.0 | 금속은 서로 닿지 않고, 오일 위에서 미끄러지듯 돕니다. | 금속끼리 **닿지 않는다** |
| R07-09 | 26.0–30.0 | 그래서 오일이 부족하거나 낡으면, 막이 깨지고 금속은 녹아 붙습니다. | 막이 깨지면 → **소착** |
| R07-10 | 30.0–32.5 | 오일을 보내는 펌프, 압력을 만드는 회전. | 펌프 + 회전 |
| KF-11 | 32.5–34.0 | 이 둘이 엔진을 살립니다. | 이 둘이 엔진을 살린다 |

---

## 3. 짚어둘 것 — 구조 문제

**① 실사 ↔ 벡터 혼용.** 이번 라운드의 결정적 실패. 원인은 "단면 원리 설명은 실사로 안 된다"는 가정인데, Flow(Veo)는 *실사 질감의 공학 컷어웨이 단면*을 충분히 만든다. 오히려 S2·S3가 그 증거다. 원리 컷도 **같은 실사 매크로 룩 안에서, 단면을 잘라 보여주는 방식**으로 통일한다. 그래픽(화살표·압력색)은 평면 HUD가 아니라 단면 안에 빛나는 유체와 공간 화살표로 결합한다.

**② 같은 앵글 반복.** 27초 동안 사실상 앵글 두 개(부분 원호 / 초근접 원호)가 번갈아 6번 나온다. 새 구성은 컷마다 **카메라 거리가 한 단계씩 바뀌도록** 설계했다: 엔진 전경 → 저널 → 단면 전체 → 쐐기 → 압력 → 전체(뜸) → 최소 틈 초근접 → 실패 → 엔진 풀백 → 차.

**③ 화면이 대본을 증명하지 못함.** 컷마다 "이 화면이 증명할 것 한 가지"를 정하고 프롬프트의 피사체로 선언한다(아래 프롬프트 주석의 '증명' 항목).

**대응:** 베어링 구간은 개별 땜질이 아니라 `[BEARING LOCK]` `[OIL LOCK]`을 새로 만들어 한 번에 고정한다 (`prompts/LOCKS.md`). 단면 마스터 이미지(R07-04 CLEAN)를 먼저 확정하고, 이후 단면 컷은 전부 그 이미지를 참조로 물고 간다.

---

## 4. 편집·자막·오디오 (재생성 없이 고칠 것)

### 자막
- **위치:** 현재 세로 1390px. Shorts 하단 UI(채널명·설명·구독 버튼)가 1500px 부근부터 덮기 시작해 기기에 따라 아슬아슬하다. **1180–1250px**로 올린다.
- **강조색:** 핵심어 1개만 금색(`#F2C14E` 계열)으로. 색 체계의 '핵심 수치=금색'과 맞춘다. 지금은 전부 흰색이라 무엇이 중요한지 안 보인다.
- **크기:** 95px 유지. 한 줄 최대 14자 안쪽으로 끊는다(현재 "즉, 금속끼리 직접 닿지 않고,"가 가장 길다).
- **화면 내 숫자 카드:** R07-03 "≈ 0.005 mm", R07-06 "≈ 수백 atm" 같은 수치는 생성 이미지 안에 넣지 말고(글자 깨짐) 편집에서 금색 숫자로 얹는다. 한글은 생성 단계에서 절대 넣지 않는다.

### 오디오
- **BGM 없음, 효과음 없음 → 반드시 추가.** 낮은 미니멀 신스 드론(−28 LUFS 정도로 깔기) + 컷 전환 우시(whoosh) + 연소 "쿵" + 압력 상승 구간 하이피치 라이저 + 소착 컷 금속 긁힘. Veo가 생성한 클립 오디오(기계음)를 SFX 레이어로만 쓰는 것도 방법이다. 보이스와 겹치는 대사·음악은 끈다.
- **음량:** 최종 믹스 **−14 LUFS / True Peak −1.0 dBTP**로 노멀라이즈. 지금은 다른 쇼츠 사이에서 작게 들린다.
- **공백 정리:** 7.30–8.43초(1.1초)는 핵심 전환 직전의 이탈 구간이다. 모든 문장 사이 공백을 0.15–0.25초로 줄이면 약 3초가 줄고 템포가 확 산다.
- **루프:** 마지막 0.65초 완전 무음 → 드론을 끝까지 끌고 가고, 첫 프레임의 연소 "쿵"으로 다시 이어지게 한다.

### 컷 연결
- 실사 컷끼리 하드컷 대신 **매치컷/푸시인 연속**으로: R07-02 끝 = R07-03 시작, R07-03 끝 = R07-04 시작이 같은 각도가 되도록 Flow **Frames to Video**의 시작 프레임으로 직전 클립 마지막 프레임을 넣는다.

---

## 5. R07 프롬프트

모든 컷은 2단계로 만든다.
1. **CLEAN 이미지** — Flow 이미지 생성. 참조 이미지(Ingredients) 첨부. 그래픽·글자 없음.
2. **영상** — Flow Frames to Video, 시작 프레임 = 1단계 CLEAN. 생성 후 필요한 구간만 트림.

`[ENGINE LOCK]` `[BEARING LOCK]` `[OIL LOCK]` `[STYLE LOCK]` 본문은 `prompts/LOCKS.md`. Flow에 넣을 때 태그 자리에 본문을 붙여넣는다.

**생성 순서 (순차 강제):**
R07-04 CLEAN을 **가장 먼저** 확정한다 → 이것이 단면 마스터. R07-05·06·07·08·09는 전부 R07-04 CLEAN을 참조로 첨부하고 **한 장씩 순차로** 돌린다(병렬 금지: 저널 편심 위치와 회전 방향이 컷마다 달라지면 쌍이 깨진다). 그 다음 R07-03(다리 컷, 끝 프레임을 R07-04에 맞춤) → R07-01 → R07-10.

```text
================================================================
R07-01 — HOOK / 연소 → 크랭크 회전   [참조: KF-02 첨부]
output: R07-01_hook_combustion.mp4
증명: "1분에 수천 번 폭발" — 폭발과 크랭크 회전이 한 화면에서 이어진다
================================================================
--- CLEAN IMAGE ---
Match the attached reference image for engine geometry, lighting, metal texture and
colour grade.
Extreme close view of one cylinder of the sectioned engine, camera level with the
piston crown. Nearest to camera is the cut cylinder wall; inside it the piston sits at
the very top of its stroke, the combustion chamber just above the crown filled with a
compact bright orange-white flame front at the instant of ignition. Beyond the piston
the connecting rod runs down toward the crankshaft, which is visible further along in
soft focus with its glowing cyan oil passages.
[ENGINE LOCK]
[STYLE LOCK]

--- VIDEO (Frames to Video, start frame = CLEAN) ---
The flame front expands violently and drives the piston down its bore in a fraction of
a second; the connecting rod swings and the crankshaft whips round once, its cyan oil
passages streaking with motion. Camera simultaneously makes a fast push along the
connecting rod toward the crankshaft main journal and settles on it.
0.0-0.3 ignition flash
0.3-1.0 piston driven down, rod swings
1.0-2.0 camera rushes along the rod and settles on the spinning crankshaft
No morphing, the engine keeps exactly four cylinders, piston and rod stay rigid.
[STYLE LOCK]
```

```text
================================================================
R07-02 — S2 재사용 (채택본)
output: S2 원본 클립 1.25–3.9초 트림
================================================================
재생성 없음. R07-01 마지막 프레임과 각도가 다르면 R07-02 시작을 0.3초 잘라 푸시인 도중부터 시작.
```

```text
================================================================
R07-03 — 다리 컷 / 메인 저널로 파고들기   [참조: S3 마지막 프레임 + R07-04 CLEAN 첨부]
output: R07-03_journal_dive.mp4
증명: 축과 베어링 사이에 '틈'이 있고 그 틈이 오일로 차 있다
================================================================
--- VIDEO (Frames to Video, start frame = S3 last frame, end frame = R07-04 CLEAN) ---
Match the first attached reference for lighting, texture, motion-blur strength and
colour grade. Keep all of that identical.
The camera keeps diving toward one crankshaft main journal. The bearing cap around that
journal is sectioned open, revealing the thin bronze-gold bearing shell and, between the
shell and the spinning steel journal, a thin glowing cyan layer of oil. The camera swings
round smoothly until it looks straight along the shaft axis at the cut face, arriving
exactly at the composition of the second attached reference.
0.0-1.5 continuous dive toward the journal, crankshaft spinning
1.5-3.0 orbit onto the shaft axis, cut face comes square to camera, hold
No morphing of parts, no added parts, journal keeps rotating at constant speed.
[ENGINE LOCK]
[BEARING LOCK]
[OIL LOCK]
[STYLE LOCK]
```

```text
================================================================
R07-04 — 단면 마스터 / 급유   [최우선 생성 · 참조: KF-02 첨부(질감·색만)]
output: R07-04_section_master_CLEAN.png → R07-04_oil_feed.mp4
증명: 하우징-쉘-유막-저널 전체 원과 급유공이 한 화면에 다 보인다
================================================================
--- CLEAN IMAGE ---
Match the attached reference only for metal texture, lighting and colour grade.
Looking straight along the axis of a crankshaft at the sectioned cut face of one main
bearing. THE SUBJECT IS THE COMPLETE RING OF THE BEARING ASSEMBLY, shown whole and
centred, with generous dark empty space all around it so nothing touches the frame edge:
that surrounding empty space is as important as the bearing itself.
From the outside in: cast-aluminium housing, thin bronze-gold bearing shell, a crescent
of glowing cyan oil, and the polished steel journal. The crescent is clearly wide on one
side and narrows to a hairline on the opposite side. One oil feed hole passes through the
shell on the wide side.
[BEARING LOCK]
[OIL LOCK]
[STYLE LOCK]

--- VIDEO (Frames to Video, start frame = CLEAN) ---
Locked-off camera with a very slow 5-degree orbit. The journal turns clockwise at steady
speed. A pulse of fresh glowing cyan oil is pushed in through the feed hole and spreads
into the wide side of the crescent gap, streamlines following the rotation.
0.0-0.6 clean scene, rotation only
0.6-1.6 oil pulse enters through the feed hole
1.6-3.5 fresh oil spreads around the wide side of the gap
No change to the crescent position, no morphing, journal never touches the shell.
[STYLE LOCK]
```

```text
================================================================
R07-05 — 쐐기 / 회전이 오일을 끌고 들어감   [참조: R07-04 CLEAN 필수, 순차]
output: R07-05_wedge_drag.mp4
증명: 틈이 한쪽으로 '좁아진다' + 회전이 오일을 그 좁은 쪽으로 끌고 간다
================================================================
--- CLEAN IMAGE ---
Reproduce the attached reference frame exactly: same camera axis, same bearing, same
light, same grade. Change one thing only — the camera moves closer.
THE SUBJECT IS THE CONVERGING SIDE OF THE CRESCENT OIL GAP: the stretch where the gap
between the turning journal and the bearing shell narrows steadily from wide to hairline.
That narrowing gap sits in the middle of the frame. The wide end of the gap is nearest
the feed hole; further round the circle the gap tightens until the journal and shell are
separated by only a glowing hairline of oil.
[BEARING LOCK]
[OIL LOCK]
[STYLE LOCK]

--- VIDEO (Frames to Video, start frame = CLEAN) ---
The journal turns clockwise. Cyan streamlines in the oil are visibly dragged along by
the moving journal surface from the wide end of the gap into the narrowing end, bunching
closer together as the gap tightens. A thin pale blue-white curved arrow appears around
the journal showing the rotation direction.
0.0-0.5 clean scene, rotation only
0.5-1.5 rotation arrow draws in along the journal surface
1.5-3.5 streamlines are dragged into the narrowing gap and crowd together
3.5-4.0 hold
Camera slow 8-degree drift along the gap. No morphing, crescent stays in place.
[STYLE LOCK]
```

```text
================================================================
R07-06 — 압력 형성   [참조: R07-05 CLEAN 필수, 순차]
output: R07-06_pressure_build.mp4
증명: 좁아지는 쪽 직전에서 압력이 '뜨겁게' 솟는다 (청록 → 주황·적색)
================================================================
--- VIDEO (Frames to Video, start frame = R07-05 CLEAN) ---
Reproduce the attached reference exactly: same framing, same light, same grade.
Change one thing only — the pressure in the oil.
On the converging side, just before the narrowest point of the gap, the oil trapped
between the turning journal and the shell begins to glow: cyan warms through amber to
deep orange-red, forming a smooth hump of heat-coloured pressure that is strongest just
before the hairline and fades on either side. The rest of the film stays cyan.
0.0-0.6 cyan film only, rotation continues
0.6-2.0 amber glow rises on the converging side
2.0-3.2 glow intensifies to orange-red just before the narrowest point
3.2-4.0 pressure hump holds and pulses gently with each rotation
No colours other than cyan, amber, orange and red. No morphing.
[BEARING LOCK]
[OIL LOCK]
[STYLE LOCK]
```

편집: 3.0초부터 금색 숫자 "≈ 수백 atm" 대신 영문 단위 `100+ MPa` 를 편집에서 얹는다(생성 이미지에는 넣지 않음).

```text
================================================================
R07-07 — 하중을 받치며 축이 뜸   [참조: R07-04 CLEAN 필수, 순차]
output: R07-07_load_lift.mp4
증명: 위에서 누르는 힘(주황 화살표)을 압력이 받아 축이 쉘에 닿지 않고 떠 있다
================================================================
--- VIDEO (Frames to Video, start frame = R07-04 CLEAN) ---
Reproduce the attached reference exactly: complete bearing ring centred, same light,
same grade. Change one thing only — load and pressure appear.
One thick orange arrow presses on the journal from the unloaded side toward the loaded
side. The orange-red pressure hump in the oil on the converging side swells to meet it,
and the journal, instead of touching the shell, rides on that pressure with a clear
glowing gap remaining all the way round.
0.0-0.6 bearing ring, rotation only
0.6-1.6 orange load arrow drives in and presses on the journal
1.6-2.8 pressure hump swells on the converging side
2.8-3.5 journal holds afloat, a thin glowing gap visible all around
Camera slow 6-degree orbit. The journal never touches the shell. No morphing.
[BEARING LOCK]
[OIL LOCK]
[STYLE LOCK]
```

```text
================================================================
R07-08 — 최소 틈 초근접 / 금속끼리 안 닿음   [참조: R07-06 마지막 프레임 필수, 순차]
output: R07-08_min_gap_macro.mp4
증명: 두 금속 표면 사이에 빈 틈이 있고, 오일이 그 틈을 채운 채 흐른다
================================================================
--- CLEAN IMAGE ---
Match the attached reference for lighting, texture, colour grade and oil colour.
Change the framing only — move in to an extreme macro of the narrowest point of the gap.
THE SUBJECT IS THE THIN GLOWING SEAM OF OIL between two metal surfaces. It runs
straight across the middle of the frame. Nearest to camera on one side of the seam is the
polished steel journal surface with fine grinding marks; on the other side of the seam is
the dull bronze-gold bearing lining. The two metal surfaces never meet: the seam of oil
between them is the most important thing in the frame.
[BEARING LOCK]
[OIL LOCK]
[STYLE LOCK]

--- VIDEO (Frames to Video, start frame = CLEAN) ---
The steel journal surface slides past steadily in one direction while the bronze lining
stays still. Inside the glowing seam, faint streamlines flow with the moving surface.
The seam keeps a constant thickness: the metals never touch, never spark.
Camera locked off with a very slow push-in. No morphing.
[STYLE LOCK]
```

```text
================================================================
R07-09 — 실패 시나리오 / 유막 붕괴 → 소착   [참조: R07-08 CLEAN 필수, 순차]
output: R07-09_film_collapse.mp4
증명: 오일막이 없으면 금속이 닿아 긁히고 녹아 붙는다 (원리의 반증)
================================================================
--- VIDEO (Frames to Video, start frame = R07-08 CLEAN) ---
Reproduce the attached reference exactly: same macro framing, same light, same grade.
Change one thing only — the oil runs out.
The glowing cyan seam thins and dims, then breaks into patches. Where it breaks, the
steel journal surface scrapes the bronze lining: tiny bright sparks, the lining smears and
discolours dark blue-brown with heat, and the two surfaces seize together.
0.0-0.8 healthy glowing seam, sliding
0.8-1.8 seam thins and dims, breaks into patches
1.8-3.0 metal contact, sparks, lining smears and discolours
3.0-3.5 surfaces locked, motion stops abruptly
No morphing outside the contact zone.
[BEARING LOCK]
[OIL LOCK]
[STYLE LOCK]
```

```text
================================================================
R07-10 — 엔진 풀백 (S10 대체)   [참조: KF-02 필수]
output: R07-10_engine_pullback.mp4  (또는 S2 클립 역재생으로 대체 — 권장)
================================================================
--- VIDEO (Frames to Video, end frame = KF-02 3.0s frame) ---
Match the attached reference for engine geometry, camera height, lighting, texture and
colour grade. Keep all of that identical.
The camera pulls back steadily from a close view of one crankshaft main journal, where
the bronze-gold bearing shell and a thin glowing cyan oil layer are visible, out to the
full sectioned engine exactly as in the reference. The crankshaft spins; cyan oil pulses
through the galleries from the sump strainer up to the crankshaft.
0.0-3.0 continuous pull-back, oil pulses travel through the galleries
No morphing, exactly four cylinders throughout.
[ENGINE LOCK]
[STYLE LOCK]
```

---

## 6. 진행 현황

| | ID | 내용 | 라운드 |
|---|---|---|---|
| ⬜ | R07-01 | 훅: 연소 → 크랭크 회전 | R07 신규 |
| ✅ | KF-02 | 엔진 컷어웨이 푸시인 (ENGINE LOCK 기준) | R06 S2 |
| ⬜ | R07-03 | 메인 저널로 파고드는 다리 컷 | R07 (S3 조건부, 참조 첨부) |
| ⬜ | R07-04 | 단면 마스터 + 급유 | R07 **최우선** |
| ⬜ | R07-05 | 쐐기 / 오일 끌려 들어감 | R07 (R07-04 참조, 순차) |
| ⬜ | R07-06 | 압력 형성 | R07 (R07-05 참조, 순차) |
| ⬜ | R07-07 | 하중 + 축 뜸 | R07 (R07-04 참조, 순차) |
| ⬜ | R07-08 | 최소 틈 초근접 | R07 (R07-06 참조, 순차) |
| ⬜ | R07-09 | 유막 붕괴 → 소착 | R07 (R07-08 참조, 순차) |
| ⬜ | R07-10 | 엔진 풀백 | S2 역재생(권장) 또는 R07 재생성 |
| ✅ | KF-01/11 | 세단 주행 루프 | R06 S1 |

확보 3/11 (KF-01, KF-02, KF-11).

**생성 순서:** R07-04 → 05 → 06 → 07 → 08 → 09 (모두 순차) → 03 → 01 → 10
**편집 순서:** 대본 녹음 재수정 → 컷 배치 → 공백 0.2초 정리 → 자막 1200px·금색 강조 → BGM/SFX → −14 LUFS

---

## 7. 실패 대응표 갱신

이전 라운드 표(`CLEAN_REVIEW_R*.md`)가 이 저장소에 없어 R06에서 새로 시작한다. 이전 표가 있으면 아래를 이어 붙인다.

| 증상 | 원인 | 대응 |
|---|---|---|
| 한 편 안에 실사 컷과 플랫 벡터 컷이 섞임 | 원리 설명 컷을 Flow 밖(또는 다른 스타일)에서 제작 | 원리 컷도 실사 단면 컷어웨이로 Flow에서 생성. `[STYLE LOCK]`에 `no flat graphic illustration, no cartoon shading` 고정 |
| "쐐기"라고 말하는데 틈이 균일 | 저널 편심을 지정하지 않음 → 동심원 기본값 | `[BEARING LOCK]`에 편심·초승달 틈 고정. 쐐기 컷은 **좁아지는 틈 자체를 피사체로 선언** |
| 원의 일부만 크롭돼 구조가 안 읽힘 | 여백 지시 없음 | 단면 마스터에 "complete ring … generous empty space … as important as the bearing itself" |
| 압력을 청록 밝기로 표현 | 색 체계 미고정 | `[OIL LOCK]`: 흐름=청록, 압력·하중=주황→적색 |
| 같은 앵글 4~6회 반복 | 컷 수 부족을 재사용으로 메움 | 컷마다 카메라 거리 단계를 다르게 설계, 컷당 '증명 1개' 지정 |
| 시작·끝 엔진이 서로 다름 | 엔딩 엔진을 참조 없이 새로 생성 | 엔딩은 S2 역재생 또는 KF-02 참조 필수 |
| 문장 사이 무음 1초+ | 보이스 무편집 + BGM 없음 | 공백 0.15–0.25초, 드론 BGM 상시 |
