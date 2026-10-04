# 비글루 숏드라마 페스티벌 — 「내일수리점」 R2
## 1화 「아직 하지 않은 말」 / R1 검토 · 톤앤매너 · 룩앤필 · 장면 재구성 · Google Flow 제작안

- 작성: 2026-10-04, Asia/Seoul (R1: 2026-10-02, `script-r1.md`)
- 상태: SCENE_DESIGN_R2 / 이미지·영상 미생성 / 음성 미생성 / 출품 미완료
- 러닝타임: **148초(2:28)**, 타이틀 포함 · 1080×1920 · 9:16 · 24fps · **3,552프레임**
- 편집 숏: **41숏** (평균 3.6초, 최장 6.5초 → 모든 숏이 Veo 1회 생성 길이 8초 안에 들어감)
- 출연: 성호 58세(수리공), 은서 31세(딸). **R1의 '정체불명 성인' 목소리는 삭제**. 음성 자산은 2명뿐.
- 공간: 수리점 내부 + 같은 가게의 문턱. R1과 동일하게 추가 세트 없음.
- 생성 파이프라인: **Google Flow 단독**(이미지·영상·대사 음성 모두 Flow 안에서 생성). 편집기는 컷·자막·음향 가공·색 맞춤만 담당.

> 한 줄 기획(R2): 테이프 없는 녹음기에서 아버지가 아직 하지 않은 말이 먼저 흘러나온다. 딸이 문을 두드리기 전에, 그는 그 말을 바꿔야 한다. 그리고 바꾼 대가로, 녹음기는 딸의 목소리로 새 경고를 들려준다.

---

## 0. 공모 조건 재확인 (2026-10-04)

| 항목 | 확인 내용 | 이 작품에 주는 의미 |
|---|---|---|
| 공모 주제 | **'다음 화가 궁금해지는 3분'** (보도 기준) | 1화 완결성보다 **마지막 15초의 다음 화 질문**이 작품의 성패를 가른다. R1에서 가장 약했던 부분 |
| 대상 시장 | 한국·미국·일본 중심 글로벌 | 대사를 줄이고 **소리와 시선으로 읽히는 구조**가 유리. 영어 자막판을 따로 준비 |
| 규격 | 3분 이하, 정확한 9:16, 300MB 이하 (R1 기록) | 148초, 1080×1920 |
| AI 요건 | 인물·장면 AI 생성, 외부 AI 도구·일반 후반 작업 허용 (R1 기록) | Flow로 전부 생성, 편집기는 후반 작업만 |
| 심사 | Idea 35 / Pull 25 / Resonance 20 / Craft 20, 최종 1차 심사 60% + 비글루 총 시청시간 40% (R1 기록) | **Pull + 시청시간 = 사실상 절반 이상**. 예술적 룩이 이탈을 부르면 안 된다 |
| 일정 | 마감 10/11 23:59 KST (R1 기록). 보도 기준 내부 심사 통과 20팀이 10월 말 비글루에 공개되고, 시청 데이터를 반영해 11월에 최종 5팀 선정 | **오늘 기준 D-7.** 공개 후 시청시간 경쟁이 있으므로 첫 3초와 완주율이 중요 |
| 상금 | 1위 USD 10,000 / 2위 2팀 각 3,000 / 3위 2팀 각 2,000 (보도) | — |

> 확인 한계: 이 환경에서 공식 규칙 페이지(vigloostudio.com)는 네트워크 정책으로 열리지 않았다. 주제·상금·공개 일정은 보도로 재확인했고, 배점·60/40·규격·마감은 R1이 10/2에 공식 페이지에서 기록한 값을 그대로 옮겼다. **제출 전에 공식 페이지에서 자막 언어 요건과 60/40 반영 방식을 다시 볼 것.**

---

## 1. R1 검토

### 1.1 그대로 지킬 것 (R1의 강점)

1. **첫 1초에 사건 제시.** 가게 외관과 인물 소개 없이 바로 거절 대사로 시작한다.
2. **장치가 아니라 사람의 책임.** 기계를 부수는 이야기가 아니라 자신의 말을 바꾸는 이야기다.
3. **같은 소리가 두 번 들리는 구조.** 부품통·노크·대사를 같은 원본으로 반복해, 편집만으로 초현실 현상을 증명한다. AI 영상이 약한 화려한 VFX를 쓰지 않는다.
4. **딸은 도구가 아니다.** 떠나는 계획을 유지하고 즉시 용서하지 않는다.
5. **'이번엔'이라는 단서.** 녹음기 속 은서의 "이번엔… 정말 안 올게"는 과거에 같은 말이 있었음을 암시한다. 처음엔 과거 녹음으로 들리다가, 다시 볼 때 미래의 반복으로 읽힌다. 아주 좋은 대사라서 R2에서 그대로 둔다.
6. **제한된 공간·인물·소품.** 생성 일관성 측면에서 맞는 판단이다.

### 1.2 고칠 것

| # | R1의 문제 | 왜 문제인가 | R2 해결 |
|---|---|---|---|
| 1 | **마지막 훅이 본편과 끊겨 있다.** 낯선 성인의 "다음 손님에게는 문을 열어주면 안 됩니다" | 공모 주제가 '다음 화가 궁금해지는'인데, 결말이 방금 본 부녀 이야기와 상관없는 일반적인 공포 대사다. 제3의 성우가 필요해 Flow에서 음성 일관성 부담도 늘어난다 | **녹음기가 은서의 목소리로 속삭인다: "아빠… 열지 마."** 성호가 말을 바꾼 결과, 딸이 오늘 밤 가게에 남는 새 미래가 생겼고 그 미래에 위험이 있다. 화해를 뒤집지 않으면서 화해 때문에 생긴 질문이 된다. §4 SC09 |
| 2 | **은서는 녹음기 소리를 못 듣나?** (SC05) | 좁은 가게에서 녹음기가 "가. 다시는 오지 마"를 재생하는데 문간의 은서가 반응하지 않는 이유가 없다. 심사위원이 바로 짚을 설명 공백 | 성호가 **손바닥으로 스피커를 덮어** 자기 미래의 말을 틀어막는다. 설명 공백을 메우는 동시에 이 작품의 핵심 이미지가 된다 |
| 3 | **문 상태의 연속성이 모호하다** | SC04는 '문틀을 사이에 둔' 대화인데 SC06에서는 '컷이 바뀌면 문이 열린 상태'다. 은서가 밖에 있는지, 문이 열렸는지가 분명하지 않다 | 문 상태를 4단계로 고정: **닫힘 → (은서가) 한 뼘 열기 → (성호가) 활짝 열기 → 조용히 닫힘.** 은서는 초대받기 전까지 문턱을 넘지 않는다("오지 말랬잖아"의 몸짓) |
| 4 | **첫 1초가 소리에만 의존한다** | 피드를 넘기는 시청자에게 첫 프레임은 정지 이미지처럼 지나간다. 소리를 듣기 전에 넘길 수 있다 | **한 프레임에 '꽉 다문 입'과 '떨리는 스피커'를 함께 선명하게** 보여준다(세로 분할 초점, §3). 무음에서도 "입은 닫혀 있는데 누가 말한다"가 읽힌다 |
| 5 | **수리공이 녹음기를 끄지 않는다** | 평생 기계를 고친 사람이라면 가장 먼저 정지 버튼을 누른다. 안 누르면 인물이 수동적으로 보인다 | S13에서 STOP을 누르지만 **빈 릴 축이 계속 돈다.** 직업적인 반응을 보여주면서 다음 행동(손바닥으로 덮기)의 이유가 된다 |
| 6 | **부품통에 사전 설치가 없다** (SC02) | 통이 갑자기 등장하면 낙하가 우연처럼 보인다 | S05 부감에서 **통이 작업대 오른쪽 끝에 걸쳐 있는 모습을 미리** 보여준다 |
| 7 | **변화가 대사에만 있다** | "같은 광원 유지"는 옳지만, 그러면 화해의 순간에 화면이 할 일이 없다 | 색보정을 바꾸지 않고 **공간과 빛의 물리적 변화**로 보여준다: 문이 열리면 바깥의 푸른 빛이 따뜻한 가게 안으로 들어오고, 두 사람이 처음으로 작업대의 같은 쪽에 선다. **같은 구도를 상태만 바꿔 반복**한다(§3-⑥) |
| 8 | **녹음기에 시각적 '살아 있음'이 없다** | 빈 카세트실이 정지 상태면 그냥 열린 기계다 | **테이프 없이 도는 릴 축**: 미래가 재생 중이면 돌고, 미래가 바뀌면 멈춘다. 대사로 설명하지 않는 시각 규칙 하나 |
| 9 | 정지된 장면과 공포 사운드의 경계 | 140초 동안 조용한 가게가 이어지면 Pull이 떨어질 수 있다 | **'느린 프레임, 빠른 이야기'**: 프레임은 고정하되 평균 3.6초로 컷하고, 12~18초마다 새 정보를 터뜨린다(§2.3 훅 사다리) |
| 10 | 글로벌 시청자 | 한·미·일 공개인데 대사 판독을 자막 한 종류에 맡김 | **소리 출처별 자막 디자인**(녹음기 목소리 / 실제 목소리 구분)과 영어 자막판 |

### 1.3 R2에서 바꾸지 않기로 한 것

- 장치의 서사 규칙(R1 §3) 1~7은 유지한다. 아래 두 줄만 추가한다.
  - 8. **릴 축 규칙**: 녹음기가 미래를 재생하는 동안 빈 릴 축이 돈다. 인물이 그 미래와 다른 선택을 하면 축이 멈춘다. 정지 버튼으로는 멈추지 않는다.
  - 9. **청취 규칙**: 녹음기 소리는 일반 스피커 소리이므로 누구나 들을 수 있다. 그래서 성호는 손으로 막는다. 마지막 경고를 은서가 듣지 못하는 것은 성호가 녹음기를 쥐고 등을 돌려 소리가 작기 때문이다(초자연적인 '성호만 들림' 규칙은 만들지 않는다).
- 대사의 핵심 문장 다섯 개("가. 다시는 오지 마." / "오지 말랬잖아." / "오늘도, 그냥 갈까?" / "그때, 오지 말라고 한 거… 미안하다." / "와 줘서 좋다.")는 그대로 둔다. 바꾸면 더 나빠진다.

---

## 2. 톤앤매너 — 공모 요강에 맞추기

### 2.1 장르 정의

**코지 미스터리(cozy mystery) × 절제된 가족 멜로.** 무섭지 않은데 계속 불안하고, 울리지 않는데 남는다.

비글루를 비롯한 세로 숏드라마 시장의 주류는 로맨스·복수·재벌·회귀물이다. 이 작품은 그 사이에서 **'조용해서 눈에 띄는' 작품**이 되는 것을 노린다. Idea(35점) 축에서는 확실한 차별점이다. 다만 조용함 때문에 이탈이 생기면 Pull(25점)과 시청시간(40%)을 잃으므로, 톤은 조용하게 하고 **훅은 장르물만큼 촘촘하게** 넣는다.

### 2.2 톤 키워드

| 이렇게 | 이렇게 하지 않는다 |
|---|---|
| 조용한 긴장, 따뜻한 불안 | 점프 스케어, 공포 BGM |
| 말보다 소리, 소리보다 침묵 | 감정을 설명하는 피아노 |
| 서툰 사람의 서툰 사과 | 눈물 폭발, 포옹, 장황한 고백 |
| 생활감 있는 실재 공간 | 네온, 글리치, 시간 포털, 홀로그램 |
| 한 번의 불가능 | 설정 설명, 규칙 내레이션 |

### 2.3 훅 사다리 (Pull · 시청시간 대응)

세로 숏드라마 시청자는 몇 초 단위로 남을지 결정한다. 아래 시점마다 **새 질문 하나를 열고, 이전 질문 하나를 닫는다.**

| 시점 | 열리는 질문 | 닫히는 질문 |
|---|---|---|
| 0:00 | 입을 다문 남자의 목소리가 어디서 나오나? 왜 딸에게 저런 말을? | — |
| 0:08 | 종소리가 들렸는데 왜 문 위의 종은 가만히 있나? | — |
| 0:16 | 테이프가 없는데 왜 릴이 도나? | 과거 녹음인가? → 아니다 |
| 0:23 | 기계가 방금 일어날 소리를 먼저 냈다 | 이건 미래의 소리다 |
| 0:33 | 딸이 실제로 왔다. 그럼 그 대화도 일어나나? | — |
| 0:40 | 정지 버튼으로도 안 꺼진다 | — |
| 1:00 | 들었는데도 같은 말을 할까? (손바닥으로 막는다) | — |
| 1:14 | 릴이 멈췄다 = 미래가 바뀌었다 | 같은 말을 할까? → 하지 않았다 |
| 1:28–1:48 | 사과 — 정서적 정점 | 부녀는 다시 이어질까? → 첫 자리 |
| 2:06 | 릴이 다시 돈다 | — |
| 2:12 | 딸의 목소리가 "열지 마"라고 한다. 누가 문을 두드리나? | — |
| 2:21 | 검은 화면에서 실제 노크 | **2화로** |

---

## 3. 룩앤필 — "어쿠스매틱 타블로(Acousmatic Tableau)"

> 이름은 이 문서에서 붙인 연출 방향의 이름이며 업계 표준 용어가 아니다. 해외 예술영화·광고·세로 영상 실험에서 쓰이는 기법 중, **국내 세로 숏드라마에서는 거의 쓰이지 않는 것**을 골라 이 이야기에 맞게 묶었다.

**한 문장 정의: 소리는 화면 밖에서 오고, 화면은 정물처럼 멈춰 있으며, 이야기는 소리와 화면이 어긋나는 틈에서 진행된다.**

### 3.1 국내 세로 숏드라마의 일반적인 문법과 비교

| 항목 | 국내 세로 숏드라마에서 흔한 방식 | 「내일수리점」 R2 |
|---|---|---|
| 조명 | 밝은 하이키, 얼굴 평면광 | **실제 광원만**: 작업등(텅스텐) + 문 유리의 해질녘 빛. 두 색온도의 충돌 |
| 카메라 | 핸드헬드, 펀치인 줌, 빠른 회전 | **고정 프레임**. 의도된 카메라 이동은 전체에서 단 1회(S26) |
| 컷 | 빠른 컷 + 휙 소리 효과음 | 빠른 컷, 효과음 없음. **정지된 프레임을 빠르게 넘기는** 리듬 |
| 초점 | 얼굴 중심 얕은 심도 | **세로 분할 초점(스플릿 디옵터)**: 위아래 두 평면을 동시에 선명하게 |
| 소리 | 대사 + 상시 BGM | **화면 밖 목소리(어쿠스매틱)**가 주인공. BGM은 마지막 1/4에만, 그것도 소품 소리에서 태어난다 |
| 시선 | 인물이 서로를 보는 일반적인 앵글/역앵글 | 대부분 렌즈를 피하다가, **사과 장면에서 처음으로 두 사람이 렌즈를 정면으로 본다** |
| 질감 | 깨끗한 디지털, 뷰티 보정 | 고운 필름 그레인, 하이라이트 번짐(헐레이션), 1/48초 셔터의 자연스러운 모션 블러 |
| 자막 | 크고 굵은 하단 자막, 강조 색 | **소리 출처별 자막 디자인**, 작고 정확하게 |

### 3.2 일곱 가지 연출 장치

| # | 장치 | 무엇인가 / 해외 흐름 | 이 작품에서 하는 일 |
|---|---|---|---|
| ① | **어쿠스매틱 보이스** | 출처가 화면에 보이지 않는 목소리. 영화음향 이론에서 오래 다뤄진 개념이며, 최근 해외 예술영화에서 화면 밖 소리로 긴장을 끌고 가는 연출이 주목받았다 | 녹음기 속 목소리는 **'보이지 않는 미래의 화자'**. 이 작품의 장르 엔진. 동시에 Flow 생성에서 립싱크가 필요 없는 대사를 늘려 **제작 리스크도 줄인다** |
| ② | **세로 스플릿 디옵터** | 렌즈 절반에만 근접 렌즈를 대 앞뒤 두 평면을 동시에 선명하게 찍는 기법. 최근 해외 장편에서 다시 자주 보인다. 보통 좌우로 나누지만 **9:16에서 위아래로 나누는 사용은 드물다** | 3회 사용하는 시그니처 숏. **S01** 스피커(아래) + 꽉 다문 성호의 입(위) / **S13** 녹음기(아래) + 문 유리 너머 은서의 실루엣(위) / **S37** 녹음기(아래) + 아무것도 모르고 앉아 있는 은서(위). 같은 목소리의 두 출처를 한 프레임에 |
| ③ | **정면 타블로** | 인물을 화면 중앙에 정면으로 두고 고정하는 연출. 유럽·일본 작가 영화의 정면 구도 전통에서 왔다 | 문(위)–작업대(아래)를 세로 축에 쌓은 **'세로 깊이 무대'**. 9:16의 높이를 거리로 사용한다 |
| ④ | **단 한 번의 렌즈 응시** | 대화 장면에서 인물이 상대 대신 렌즈를 정면으로 보게 하는 앵글/역앵글. 일본 고전 영화에서 왔고, 최근 해외 작가 영화에서 다시 주목받았다 | 영화 내내 아무도 렌즈를 보지 않다가 **SC07 사과에서 처음으로** 성호, 이어서 은서가 렌즈를 본다. 시청자가 곧 은서이고, 곧 성호가 된다. 세로 화면에서 이 효과는 영상통화처럼 가깝다 |
| ⑤ | **두 색온도의 실제 광원** | 실제 광원만으로 빛을 만드는 연출 | 작업대 = 따뜻한 텅스텐(성호의 닫힌 세계), 문 = 푸른 해질녘(은서·바깥·내일). 문이 열리면 **두 빛이 한 얼굴 위에서 섞인다**(S28). 색보정은 처음부터 끝까지 그대로 |
| ⑥ | **상태 변화 타블로(같은 구도의 반복)** | 같은 구도를 여러 번 돌아오며 상태만 바꾸는 반복 | **문 타블로**: S03(소리는 나는데 종이 가만히 있음) → S11(실루엣 도착) → S39(어두워진 빈 문). **무대 타블로**: S14(작업대를 사이에 두고 분리된 두 사람) → S34(같은 쪽에 선 두 사람) |
| ⑦ | **디제틱 → 스코어 브리지** | 음악이 화면 안 소리(소품·환경음)에서 자라나 배경음악이 되는 사운드 디자인 | 녹음기의 테이프 히스를 낮게 피치다운한 지속음이 **S31 직후에야** 처음 음악으로 들어온다. 앞의 100초는 음악 없음 |

### 3.3 LOOK LOCK (화면 규칙)

- **카메라**: 삼각대 고정. 손떨림 없음. 의도된 이동은 S26의 느린 후진 1회. 드론·외관·광각 왜곡 없음.
- **렌즈 감각**: 40mm(인물), 85mm(인서트), 100mm 매크로(녹음기). 빈티지 구면렌즈의 부드러운 가장자리.
- **셔터·프레임**: 24fps, 180도 셔터(1/48초) 느낌. 깔끔한 고속 셔터의 '드라마 같은 끊김' 금지.
- **조명**: 실제 광원 2개만.
  - 작업등: 텅스텐 약 3,200K, 갓이 있는 작은 램프, 성호의 손과 녹음기를 비춤
  - 문: 반투명 유리 너머 해질녘 블루. SC09로 갈수록 조금씩 어두워짐(시간 경과 = 실제 시간 흐름, 색보정 아님)
- **팔레트**
  - 텅스텐 앰버 `#D19A5B` — 작업등, 성호의 세계
  - 해질녘 블루 `#2F4A63` — 문 유리, 바깥, 은서가 들고 오는 빛
  - 그을린 엄버 `#1F1A16` — 그림자, 낡은 목재
  - 알루미늄 그레이 `#9BA1A4` — 녹음기, 부품통
  - 황동 `#B08A4A` — 문 위 종 (작은 하이라이트)
  - 채도는 낮게. 틸&오렌지 과장 금지(두 색은 '광원'이지 보정 효과가 아님)
- **질감**: 16mm에 가까운 고운 그레인, 작업등·종 하이라이트에 약한 헐레이션, 검정은 약간 띄우되 뿌옇지 않게.
- **절대 금지**: 화면에 생성된 글자(자막·타이틀은 편집에서만) / 녹음기·공구의 실존 브랜드 로고 / 네온·글리치·홀로그램·음파 그래픽 / '미래' 자막 / 분할 화면 / 눈물 클로즈업 슬로모션.

### 3.4 자막 디자인 (소리 출처 구분)

| 출처 | 서체 방향 | 색 | 위치 |
|---|---|---|---|
| 녹음기 속 목소리 | 고정폭 서체(기계 느낌), 기울임 없이 자간 넓게 | 회색 `#A9ADB0` | 녹음기가 화면 아래에 있으면 녹음기 바로 위, 없으면 중앙 하단 |
| 실제 목소리 | 산세리프 세미볼드 | 오프화이트 `#F2EEE6` | 화면 높이 62~70% 구간 |
| 화면 밖 실제 목소리(문 너머 등) | 실제 목소리와 같은 서체, 앞에 얇은 대시 `—` | 오프화이트 | 동일 |

- 최대 2줄, 한 줄 14자 안팎. 앱 UI가 덮는 하단 약 18%와 오른쪽 버튼 영역은 비운다.
- 영어 자막판도 같은 구분을 유지한다. 녹음기 = 회색 고정폭.
- 자막 없는 마스터를 따로 보존한다(R1 유지).

---

## 4. 장면 구성 R2 — 148초 / 10씬 / 41숏

**표기**: `🔇` = 립싱크 불필요(화면 밖 목소리·입이 보이지 않음), `👄` = 립싱크 필요. 립싱크 숏은 **10개**로 제한했다.
**구도 기준(전체 고정)**: 문은 화면 **위·왼쪽**, 작업대는 **아래·오른쪽**. 성호는 작업대 뒤(화면 오른쪽), 은서는 문(화면 왼쪽 위). 시선 방향이 뒤집히면 탈락.

### 1막 — 들리다

#### SC01 「아직 하지 않은 말」 0:00–0:12.5

| 숏 | 시간 | 화면 | 소리 · 대사 | 메모 |
|---|---|---|---|---|
| **S01** ★ | 0:00–0:04 | **세로 스플릿 디옵터.** 아래 45%: 녹음기 스피커 그릴 초접사, 선명. 그릴의 먼지가 미세하게 떨린다. 위: 성호의 얼굴 미디엄 클로즈업, 역시 선명. 입을 꽉 다문 채 회로기판을 내려다보고 있다. 두 평면 사이는 부드럽게 번진 띠. 납땜인두 끝에서 가는 연기 한 줄이 올라간다. | 0:00.3 녹음기 속 성호: **"가. 다시는 오지 마."** | 🔇 입을 다물고 있어서 립싱크 없음. 첫 프레임부터 '입은 닫혔는데 목소리가 있다' |
| S02 | 0:04–0:08 | 성호 클로즈업. 돋보기안경 위로 눈만 천천히 올라간다. 시선은 렌즈 아래(녹음기). 인두를 쥔 손이 멈춰 있다. | 녹음기 속 은서: **"알았어. 이번엔… 정말 안 올게."** | 🔇 '이번엔'이 단서 |
| **S03** ★ | 0:08–0:10 | **문 타블로①** 작업대 쪽에서 본 고정 와이드. 위·왼쪽에 반투명 유리문, 문 위의 황동 종. 해질녘 블루. **종은 완전히 멈춰 있다.** | 녹음기에서: 문이 세게 닫히는 소리 + **종소리** | 🔇 소리와 화면이 어긋나는 첫 증거. 종이 흔들리면 탈락 |
| S04 | 0:10–0:12.5 | S01과 같은 구도에서 디옵터 없이. 성호가 문 쪽을 봤다가 녹음기로 시선을 내린다. | 작업등의 미세한 전기 험만. 무음에 가깝게 | 🔇 |

#### SC02 「빈 데크」 0:12.5–0:26

| 숏 | 시간 | 화면 | 소리 · 대사 | 메모 |
|---|---|---|---|---|
| S05 | 0:12.5–0:15.5 | **수직 부감.** 작업대 위 정리된 공구들, 가운데 녹음기. **오른쪽 끝에 찌그러진 알루미늄 부품통이 반쯤 걸쳐 있다**(사전 설치). 성호의 엄지가 EJECT 키를 누르면 카세트 덮개가 스프링으로 튀어 오른다. | 기계식 키의 딸깍 소리 | 🔇 손동작은 '누르기' 하나로 제한 |
| **S06** ★ | 0:15.5–0:18 | 카세트실 초접사. **비어 있다. 그런데 두 릴 축이 천천히 돌고 있다.** | 성호(화면 밖, 작게): **"테이프도 없는데…"** | 🔇 이 작품의 시각 규칙이 처음 등장 |
| S07 | 0:18–0:21 | S01의 위쪽 구도(성호). 녹음기에서 소리가 나자 성호가 움찔하며 몸을 뒤로 뺀다. | 녹음기에서: 금속통이 떨어져 **두 번 부딪히고 길게 울리는** 소리 | 🔇 |
| S08 | 0:21–0:23 | S05와 같은 부감. 성호의 팔꿈치가 들어와 부품통이 화면 오른쪽 밖으로 밀려 나간다. | (소리는 S09로 넘김) | 🔇 통은 프레임 밖으로 미끄러질 뿐, 낙하를 화면에 보여주지 않음(R1 유지) |
| S09 | 0:23–0:26 | 낮은 앵글, 낡은 리놀륨 바닥. 부품통이 마지막으로 흔들리다 멈춘다. 나사 두세 개만. | **S07과 완전히 같은 소리** (같은 원본, 녹음기 가공 없는 버전) | 🔇 소리 반복으로 '미래의 소리'가 증명됨 |

#### SC03 「노크가 먼저 온다」 0:26–0:40.5

| 숏 | 시간 | 화면 | 소리 · 대사 | 메모 |
|---|---|---|---|---|
| S10 | 0:26–0:30 | 녹음기 미디엄 인서트(85mm). 릴 축 회전. 작업등 빛. | 녹음기에서: **두 번의 노크**(똑—, 긴 간격, 똑) / 녹음기 속 은서: **"아빠. 나야."** | 🔇 |
| S11 | 0:30–0:33.5 | **문 타블로②** S03과 같은 구도. 1.5초 정적. 반투명 유리 오른쪽에서 사람의 그림자가 미끄러져 들어와 멈춘다. 이어 실제 노크. 이번엔 노크에 맞춰 종이 아주 조금 떨린다. | 실제 노크: **같은 리듬** | 🔇 |
| S12 | 0:33.5–0:37 | 문 유리 미디엄 클로즈업. 흐릿한 여성의 실루엣, 유리에 닿은 손가락 마디. | 문밖 은서: **"아빠. 나야."** (S10과 같은 원본, 유리 너머의 자연스러운 음색) | 🔇 실루엣이라 립싱크 없음 |
| **S13** ★ | 0:37–0:40.5 | **세로 스플릿 디옵터②** 아래: 녹음기(선명). 위: 문 유리 속 은서의 실루엣(선명). 성호의 손이 들어와 **STOP 키를 누른다. 키는 내려갔는데 릴 축은 계속 돈다.** | 키 소리. 테이프 히스가 아주 조금 커짐 | 🔇 수리공의 직업적 반응 + 에스컬레이션 |

### 2막 — 되풀이

#### SC04 「문턱」 0:40.5–0:57.5

| 숏 | 시간 | 화면 | 소리 · 대사 | 메모 |
|---|---|---|---|---|
| **S14** ★ | 0:40.5–0:45.5 | **무대 타블로①** 가게 안쪽에서 정면, 세로 깊이 구도. 아래·오른쪽 전경에 작업대와 성호의 등과 어깨, 위·왼쪽 깊은 곳에 문. 은서가 문을 **한 뼘만** 연다. 종이 부드럽게 한 번. 은서는 문턱 밖에 그대로 서 있다. | 실제 종(부드러움 — 녹음기 속 쾅·종소리와 대비) / 은서: **"나 내일 떠나."** | 🔇 원거리라 입 모양이 판독되지 않음 |
| S15 | 0:45.5–0:49 | 문틈 사이의 은서, 4분의 3 측면 미디엄 클로즈업. 얼굴 반은 바깥의 블루, 반은 가게의 앰버. | 은서: **"얼굴은 보고 가려고."** | 👄 1 |
| S16 | 0:49–0:52 | 성호 클로즈업. 고개를 숙인 채 손의 기판만 본다. 작업등 갓이 입가를 반쯤 가린다. | 성호: **"그걸 왜 이제야…"** | 👄 2 (입 일부만 보이게 → 실패 시 화면 밖 처리 가능) |
| S17 | 0:52–0:55 | S15와 같은 구도의 은서. 표정 변화 없이. | 은서: **"오지 말랬잖아."** | 👄 3 |
| S18 | 0:55–0:57.5 | 인서트. 성호의 손이 드라이버를 다시 집어 꽉 쥔다. 손등 힘줄. | 공구가 나무 작업대에 끌리는 소리 | 🔇 "또 같은 말을 할까?" |

#### SC05 「되감기 없는 재생」 0:57.5–1:14

| 숏 | 시간 | 화면 | 소리 · 대사 | 메모 |
|---|---|---|---|---|
| S19 | 0:57.5–1:00 | 녹음기 초접사, 릴 축 회전. | 녹음기 속 성호: **"가. 다시는—"** | 🔇 SC01과 같은 원본. 첫 장면 전체를 다시 틀지 않음(R1 유지) |
| **S20** ★ | 1:00–1:03 | 측면. 성호의 손바닥이 **스피커를 덮어 누른다.** 시선은 문 쪽 은서. | 손바닥 아래로 먹먹하게: **"—오지 마."** | 🔇 자기 미래의 말을 틀어막는 몸짓. R1의 청취 공백 해결 |
| S21 | 1:03–1:07 | 문틈의 은서. 작업대 쪽을 흘끗 본다(무엇인가 들었을지도 모른다는 여지). | 은서: **"오늘도… 그냥 갈까?"** | 👄 4 |
| S22 | 1:07–1:11.5 | 성호 정면 클로즈업. 시선은 렌즈 살짝 옆(은서). 입술이 열린다. 첫 음절 뒤에 말이 멈춘다. 턱에 힘. | 성호: **"가…"** (끊김) | 👄 5 |
| **S23** ★ | 1:11.5–1:14 | 카세트실 초접사. **릴 축이 느려지다 멈춘다.** | 가게의 모든 환경음이 빠지는 '진공' 0.8초 | 🔇 미래가 바뀌었다는 것을 대사 없이 증명 |

### 3막 — 바꾸다

#### SC06 「작업대 밖으로」 1:14–1:28.5

| 숏 | 시간 | 화면 | 소리 · 대사 | 메모 |
|---|---|---|---|---|
| S24 | 1:14–1:16.5 | S05 부감. 드라이버가 작업대에 놓인다. | 작은 금속 접촉음 하나 | 🔇 |
| S25 | 1:16.5–1:19 | 성호 클로즈업. 고개를 든다. | 성호: **"잠깐만."** | 👄 6 |
| **S26** ★ | 1:19–1:25 | **이 영화의 유일한 카메라 이동.** 선반 사이 통로에서 본 세로 풀샷. 성호가 작업대 뒤에서 나와 카메라 쪽(=문 쪽)으로 걸어온다. 카메라는 그의 속도로 천천히 뒤로 물러난다. **처음으로 보이는 그의 전신**: 낡은 앞치마, 실내화, 생각보다 작은 사람. | 실내화 발소리. 작업등 험이 멀어짐 | 🔇 작업대라는 '방패'를 떠나는 순간 |
| S27 | 1:25–1:28.5 | 문 안쪽. 성호의 손이 문 가장자리를 잡고 문을 **활짝** 연다. 바깥의 푸른 빛이 가게 바닥에 길게 쏟아진다. | 종, 부드럽게 한 번 | 🔇 손은 하나만, 동작도 하나만 |

#### SC07 「처음으로 렌즈를 본다」 1:28.5–1:48.5

> 이 씬에서만 인물이 렌즈를 정면으로 본다. 두 사람 모두 화면 중앙, 같은 크기, 같은 높이. 음악 없음. 환경음을 낮추고 숨소리와 작업등 험만 남긴다.

| 숏 | 시간 | 화면 | 소리 · 대사 | 메모 |
|---|---|---|---|---|
| **S28** ★ | 1:28.5–1:35 | 성호 정면 미디엄 클로즈업, **렌즈 응시.** 얼굴 오른쪽엔 뒤쪽 작업등의 앰버, 왼쪽엔 문에서 들어온 블루. 말하다가 눈이 한 번 아래로 떨어졌다가 다시 렌즈로 돌아온다. | 성호: **"그때, 오지 말라고 한 거…"** (숨) **"미안하다."** | 👄 7 |
| S29 | 1:35–1:40 | 은서 정면 미디엄 클로즈업, **렌즈 응시.** 2초 정적. | 은서: **"지금은?"** | 👄 8 |
| S30 | 1:40–1:43.5 | 성호 정면. 짧은 숨. | 성호: **"와 줘서… 좋다."** | 👄 9 |
| S31 | 1:43.5–1:48.5 | 은서 정면. 굳어 있던 입가가 아주 조금 풀린다. 눈가가 젖지만 울지 않는다. 대사 없음. | 무음에 가까움 → 끝 1초에 **테이프 히스를 피치다운한 지속음**이 처음으로 들어온다(음악의 시작) | 🔇 정서적 정점. 슬로모션 금지 |

#### SC08 「자리」 1:48.5–2:06.5

| 숏 | 시간 | 화면 | 소리 · 대사 | 메모 |
|---|---|---|---|---|
| S32 | 1:48.5–1:52.5 | 문턱을 사이에 둔 투숏, 정측면. 은서는 밖, 성호는 안. 렌즈 응시는 끝났다. | 은서: **"그래도 내일은 가."** | 👄 10 (측면이라 판독 부담 적음) |
| S33 | 1:52.5–1:57 | 인서트. 성호의 손이 보조의자 위 주황색 공구상자를 바닥으로 내려놓는다. 둥근 나무 의자가 비워진다. | 성호(화면 밖): **"알아. 오늘 밥은, 같이 먹자."** | 🔇 행동이 대사를 증명 |
| **S34** ★ | 1:57–2:03 | **무대 타블로②** S14와 같은 구도. 은서가 문턱을 넘어 들어온다. 문이 조용히 닫힌다. 바닥의 푸른 빛줄기가 문과 함께 가늘어진다. 은서가 작업대 옆 의자에 앉는다. **두 사람이 처음으로 작업대의 같은 쪽에 있다.** | 종, 아주 가볍게 한 번 / 지속음 계속 | 🔇 S14와 나란히 놓으면 변화가 한눈에 보임 |
| S35 | 2:03–2:06.5 | 미디엄. 은서가 바닥에 굴러가 있던 부품통을 주워 작업대 위에 내려놓는다. | 통을 내려놓는 **한 번의 부드러운 소리** (두 번 부딪히고 울리던 소리와 대비) | 🔇 딸도 무언가를 '고친다' |

### 클리프행어

#### SC09 「세 번의 노크」 2:06.5–2:21

| 숏 | 시간 | 화면 | 소리 · 대사 | 메모 |
|---|---|---|---|---|
| S36 | 2:06.5–2:09.5 | 녹음기 초접사. 따뜻한 빛 속, **멈췄던 릴 축이 저절로 다시 돌기 시작한다.** | 지속음이 끊기고 테이프 히스가 차오름 | 🔇 |
| **S37** ★ | 2:09.5–2:15 | **세로 스플릿 디옵터③** 아래: 녹음기(선명). 위: 의자에 앉아 선반의 오래된 라디오들을 둘러보는 은서(선명). 입은 다물고 있고 아무것도 모른다. | 녹음기에서: **세 번의 노크**(똑. 똑. 똑. — 은서의 두 번과 다른, 느리고 고른 리듬) / 녹음기 속 은서, 속삭임: **"아빠… 열지 마."** | 🔇 S01의 '닫힌 입'과 정확히 짝. 화해로 생긴 새 미래 |
| S38 | 2:15–2:18 | 성호 클로즈업. 시선이 녹음기 → 은서 → 문으로. 녹음기를 쥐고 몸을 돌려 소리를 가린다. | 히스가 줄어든다 | 🔇 청취 규칙(§1.3-9) |
| **S39** ★ | 2:18–2:21 | **문 타블로③** S03·S11과 같은 구도. 유리는 더 어두운 남색. 아무도 없다. 종은 멈춰 있다. | 완전한 정적 | 🔇 |

#### SC10 「타이틀」 2:21–2:28

| 숏 | 시간 | 화면 | 소리 | 메모 |
|---|---|---|---|---|
| S40 | 2:21–2:23 | **하드 컷 투 블랙.** | 0.6초 정적 → **실제 노크 한 번** (S37의 첫 노크와 같은 원본, 녹음기 가공 없는 버전) | 미래가 지금 도착했다 |
| S41 | 2:23–2:28 | 검정 위 타이틀: **내일수리점** / 작게: **1화 — 아직 하지 않은 말** / 영어판: *The Tomorrow Repair Shop — Ep.1 "Words Not Yet Said"* | 2:25에 **두 번째 노크**. 세 번째 노크 직전에 끝 | 세 번째 노크는 2화의 첫 프레임 |

> 2화 연결 메모(참고, 본편에 넣지 않음): 2화는 세 번째 노크로 시작한다. 성호는 이번에도 들은 미래와 다른 선택을 할 수 있지만, 이번엔 딸이 옆에 있다. 1화의 테마 "알면서도 되풀이하는 말"은 2화에서 "알면서도 열어야 하는 문"으로 이어진다.

### 4.1 시간·프레임 표

프레임은 1부터, 양 끝 포함, 24fps 편집 목표값.

| 씬 | 시작–끝 | 길이 | 프레임 | 숏 |
|---|---|---:|---|---|
| SC01 | 0:00–0:12.5 | 12.5 | 1–300 | S01–S04 |
| SC02 | 0:12.5–0:26 | 13.5 | 301–624 | S05–S09 |
| SC03 | 0:26–0:40.5 | 14.5 | 625–972 | S10–S13 |
| SC04 | 0:40.5–0:57.5 | 17.0 | 973–1380 | S14–S18 |
| SC05 | 0:57.5–1:14 | 16.5 | 1381–1776 | S19–S23 |
| SC06 | 1:14–1:28.5 | 14.5 | 1777–2124 | S24–S27 |
| SC07 | 1:28.5–1:48.5 | 20.0 | 2125–2604 | S28–S31 |
| SC08 | 1:48.5–2:06.5 | 18.0 | 2605–3036 | S32–S35 |
| SC09 | 2:06.5–2:21 | 14.5 | 3037–3384 | S36–S39 |
| SC10 | 2:21–2:28 | 7.0 | 3385–3552 | S40–S41 |
| **합계** | | **148.0** | **3,552** | **41** |

R1(140초) 대비 +8초. 늘어난 시간은 클리프행어(SC09–10)와 STOP 버튼·손바닥 숏에 썼다. 러프 편집에서 길어지면 **S04 → S24 → S35** 순서로 줄인다(각 숏을 빼도 이야기는 성립한다). **SC07의 침묵은 줄이지 않는다.**

### 4.2 소리 원본 재사용 맵

| 원본 | 첫 등장(가공) | 반복(원본) | 주의 |
|---|---|---|---|
| 성호 "가. 다시는 오지 마." | S01 녹음기 | S19–S20 녹음기 + 손바닥 먹먹함 | 실제로 끝까지 말하는 장면은 없음 |
| 부품통 낙하음 | S07 녹음기 | S09 실제 | 두 번 부딪힘 + 긴 울림, 타이밍 동일 |
| 노크 2회 + "아빠. 나야." | S10 녹음기 | S11–S12 실제 | 원본은 S12에서 생성한 테이크. 녹음기판은 그것을 가공 |
| 문 쾅 + 종 | S03 녹음기 | — (실현되지 않은 미래) | 실제 종은 끝까지 부드럽게만 울림 |
| 노크 3회 | S37 녹음기 | S40–S41 실제 | 은서의 노크와 리듬이 구분되어야 함 |
| 은서 "아빠… 열지 마." | S37 녹음기 | — (2화) | 속삭임 |

**녹음기 가공 기준**(편집기): 대역 약 300Hz–3.4kHz, 약한 와우·플러터, 테이프 히스, 작은 스피커의 공진. 알아듣기 쉬워야 한다.

---

## 5. Google Flow 단독 제작 파이프라인

### 5.1 원칙

- **생성은 전부 Flow 안에서**: 기준 이미지(Flow 이미지 생성) → 클립(Veo, 9:16 네이티브) → 필요 시 Extend. 대사 음성도 Veo 네이티브 오디오로 생성한다.
- 편집기는 **컷·자막·녹음기 음향 가공·색 맞춤**만 담당한다(공모 규칙의 일반 후반 작업 범위).
- 화면 속 글자는 생성하지 않는다. 프롬프트에 항상 `no subtitles, no on-screen text`를 넣는다.
- Flow 프로젝트, 기준 이미지, 모든 테이크, 프롬프트 로그를 지우지 않는다(생성 이력 보존).
- Flow의 메뉴 이름(Ingredients to Video / Frames to Video / Extend 등)은 업데이트로 바뀔 수 있다. 기능 기준으로 읽을 것.

### 5.2 어쿠스매틱 설계가 Flow 제작을 쉽게 만드는 이유

Veo는 클립마다 목소리 음색이 달라질 수 있고, 한국어 립싱크는 테이크마다 품질 차이가 크다. R2는 대사 19줄 중 **9줄이 화면 밖이거나 입이 보이지 않는 구도(녹음기·문 너머·원거리·인서트)**라 립싱크가 필요 없다. 이 대사들은 가장 좋은 음성 테이크 하나를 골라 오디오만 쓰면 된다. 립싱크가 필요한 10숏도 실패하면 **입이 보이지 않는 구도로 바꾸는 대안**을 표에 표시해 두었다(§5.6). 연출 콘셉트가 곧 AI 제작 리스크 관리다.

### 5.3 기준 자산 (Ingredients) — 생성 1일차에 고정

| ID | 내용 | 고정 포인트 |
|---|---|---|
| `CH_SUNGHO` | 58세 한국인 남성. 짧은 회색 머리, 희끗한 수염 자국, 줄 달린 돋보기안경, 빛바랜 네이비 작업 점퍼 위에 짙은 회색 캔버스 앞치마, 실내화 | 정면 / 4분의 3 / 측면 / 전신 4장 |
| `CH_EUNSEO` | 31세 한국인 여성. 낮게 묶은 어깨 길이 검은 머리, 오트밀색 니트에 베이지 트렌치코트, 작은 크로스백, 화장 거의 없음 | 정면 / 4분의 3 / 측면 3장 |
| `SET_SHOP` | 좁은 전자제품 수리점. 위·왼쪽 반투명 유리문과 황동 종, 아래·오른쪽 낡은 나무 작업대, 오래된 라디오·TV가 쌓인 선반, 리놀륨 바닥 | 문 타블로 1장 + 무대 타블로 1장 + 부감 1장 |
| `PROP_REC` | 무상표 1980년대 휴대용 카세트 녹음기. 은회색, **왼쪽 원형 스피커 그릴, 오른쪽 투명 창 카세트실, 위쪽 6개 피아노 키**, 손잡이 | 3면. 키 개수·스피커 위치가 바뀌면 탈락 |
| `PROP_BIN` | 찌그러진 둥근 알루미늄 부품통 | 1장 |
| `PROP_STOOL` | 둥근 나무 보조의자 + 주황색 금속 공구상자 | 1장 |

### 5.4 공통 프롬프트 블록

```
[STYLE LOCK]
Quiet cinematic realism, vertical 9:16 frame, locked-off tripod camera.
A small old electronics repair shop at dusk. Only practical light sources:
a small shaded tungsten work lamp (warm amber) and blue-hour daylight through a frosted glass door.
Low saturation, soft highlight roll-off, gentle halation on bright points, fine 16mm film grain,
24fps with natural 180-degree shutter motion blur. Vintage spherical lens, 40mm look.
No music. Realistic room tone.
No subtitles, no on-screen text, no logos or brand names, no neon, no glitch, no hologram,
no waveform graphics, no split screen, no slow motion.

[VOICE LOCK — SUNGHO]
A 58-year-old Korean man's voice: low, slightly hoarse, speaks slowly and curtly, standard Seoul Korean.

[VOICE LOCK — EUNSEO]
A 31-year-old Korean woman's voice: calm, clear mid-range, restrained, standard Seoul Korean.
```

- 대사가 있는 숏: `He says in Korean, quietly: "잠깐만."` 형식으로 쓴다.
- 녹음기 소리 숏: `A man's voice comes from the small speaker of the cassette recorder, saying in Korean: "…". The man in frame keeps his mouth closed.`

### 5.5 숏별 프롬프트 (영문, Flow 입력용)

각 프롬프트 앞에 `[STYLE LOCK]`을 붙이고, 해당하는 Ingredients(인물·세트·소품 기준 이미지)를 첨부한다.

**S01 · S13 · S37 — 세로 스플릿 디옵터 (최우선 테스트)**
1단계: Flow 이미지로 정지 키프레임 생성 → 2단계: 그 이미지로 클립 생성(움직임 최소).
```
S01 keyframe: Split-diopter shot in a vertical frame. Lower 45% of the frame: extreme close-up of the
round speaker grille of a vintage unbranded silver cassette recorder on a wooden workbench, in sharp focus.
Upper part: a 58-year-old Korean repairman's face in medium close-up, also in sharp focus, mouth firmly
closed, looking down at a circuit board, reading glasses. Between the two focal planes, a soft blurred band.
A thin thread of solder smoke rises. Warm tungsten work lamp light.

S01 motion: Locked-off. The dust on the speaker grille trembles slightly. The man does not move his lips.
A man's voice comes from the small speaker, saying in Korean: "가. 다시는 오지 마."
Only the smoke thread and the grille dust move.
```
```
S13 keyframe: Split-diopter vertical frame. Lower part: the same cassette recorder in sharp focus.
Upper part: a frosted glass shop door with the blurred silhouette of a woman standing outside, also in focus,
blue-hour light. S13 motion: A man's hand enters from the right and presses the STOP key of the recorder.
The key goes down, but the two empty reel spindles inside the clear cassette window keep turning.

S37 keyframe: Split-diopter vertical frame. Lower part: the cassette recorder in sharp focus, spindles turning.
Upper part: the 31-year-old Korean woman sitting on a round wooden stool inside the shop, looking at old
radios on a shelf, mouth closed, unaware, also in sharp focus.
S37 audio: three slow, even knocks come from the recorder's speaker, then a woman's whisper from the speaker
in Korean: "아빠… 열지 마." The woman in frame does not speak.
```
대안: 디옵터의 경계가 망가지면 `deep focus, both foreground recorder and background face sharp, f/11`로 깊은 심도 구도로 바꾼다. 같은 의미가 유지된다.

**S03 · S11 · S39 — 문 타블로 (같은 기준 이미지 공유)**
```
Locked-off wide view from behind the workbench toward the shop entrance. The frosted glass door is in the
upper-left of the vertical frame, a small brass bell on a curved spring above it. Blue-hour light through the glass.
S03: The bell stays completely still. Sound: from off-screen, a muffled door slam and a bell ring
(as if from a small speaker).
S11: After a still moment, a human shadow slides in from the right on the frosted glass and stops. Two knocks
on the glass, the bell trembles very slightly.
S39: The same frame, the glass now darker navy. Nobody. The bell is still. Silence.
```

**S06 · S23 · S36 — 테이프 없는 릴 축**
```
Extreme macro of the open cassette compartment of a vintage cassette recorder. It is empty: no tape.
S06: The two empty reel spindles slowly rotate by themselves. A man's voice off-screen says quietly in Korean:
"테이프도 없는데…"
S23: The spindles slow down and stop. All ambient sound drops out.
S36: In warm lamp light, the stopped spindles begin to rotate again on their own. Soft tape hiss rises.
```
S23은 Frames to Video로 시작(회전 중)·끝(정지) 프레임을 같은 이미지로 주고 `spindles slowing to a stop`만 지시하면 안정적이다.

**S05 · S08 · S24 — 부감 (같은 기준 이미지 공유)**
```
Top-down overhead view of a tidy wooden workbench: screwdrivers, tweezers, a soldering iron laid in a row,
the cassette recorder in the center, a dented round aluminum parts tin half over the right edge of the bench.
S05: A thumb presses the eject key; the cassette lid springs open.
S08: An elbow enters from the left and pushes the parts tin off the right edge, out of frame.
S24: A hand sets a screwdriver down on the bench. One small metal click.
```

**S07 · S09 — 부품통**
```
S07: Medium close-up of the repairman behind the bench. A metallic clatter comes from the recorder's small
speaker (a tin hitting the floor twice and ringing). He flinches and pulls his arm back.
S09: Low angle on worn linoleum floor. A dented aluminum parts tin wobbles a last time and settles.
Two or three small screws nearby. Metallic clatter, two hits and a long ring.
```

**S10 · S12 — 노크와 "아빠. 나야."**
```
S10: Medium insert of the cassette recorder on the bench, spindles turning. From its speaker: two knocks,
then a woman's voice in Korean: "아빠. 나야."
S12: Medium close-up of the frosted glass door from inside. A woman's blurred silhouette, her knuckles touching
the glass. Her voice through the glass, in Korean: "아빠. 나야."
```
**S12에서 생성한 음성 테이크가 원본.** 편집에서 가공해 S10에 넣는다(S10 생성 음성은 쓰지 않음).

**S14 · S34 — 무대 타블로 (같은 기준 이미지 공유)**
```
Locked-off frontal view from deep inside the shop, vertical deep staging. Foreground lower-right: the wooden
workbench and the repairman's back and shoulder. Background upper-left: the frosted glass door.
S14: A 31-year-old Korean woman outside opens the door only a hand's width. The bell rings softly once.
She stays outside the threshold. She says in Korean: "나 내일 떠나."
S34: The woman steps over the threshold; the door closes gently; the bell rings very lightly once.
The strip of blue light on the floor narrows as the door closes. She sits on the round wooden stool beside
the bench. Both are now on the same side of the workbench.
```

**S15 · S17 · S21 — 문틈의 은서**
```
Three-quarter profile medium close-up of the woman standing in the narrow gap of a half-open glass door.
Half of her face in blue-hour light, half in warm amber light from inside. She stays outside.
S15: She says in Korean, calmly: "얼굴은 보고 가려고."
S17: Same framing, no change in expression. She says in Korean: "오지 말랬잖아."
S21: She glances toward the workbench, then says in Korean, quietly: "오늘도… 그냥 갈까?"
```

**S16 · S22 · S25 — 작업대 뒤의 성호**
```
S16: Close-up of the repairman, head down, eyes on the circuit board; the lamp shade partly covers his mouth.
He says in Korean, curtly: "그걸 왜 이제야…"
S22: Frontal close-up, eyes just off the lens toward the door. His lips part; he says only "가…" in Korean and
stops; jaw tightens. Silence.
S25: Close-up. He lifts his head and says in Korean, quietly: "잠깐만."
```

**S18 · S20 · S33 · S35 — 손 인서트**
```
S18: Insert. His hand picks up a screwdriver again and grips it hard.
S20: Side view. His palm presses down over the round speaker grille of the recorder, muffling it. His eyes look
toward the door. From under the palm, a muffled man's voice in Korean: "오지 마."
S33: Insert. His hands lift an orange metal toolbox off a round wooden stool and set it on the floor.
The stool is now empty.
S35: Medium. The woman picks up the dented parts tin from the floor and sets it on the bench. One soft sound.
```

**S26 — 유일한 카메라 이동**
```
Vertical full shot from the narrow aisle between shelves of old radios. The repairman comes out from behind
the workbench and walks toward the camera. The camera slowly dollies backward at his pace. Full body visible
for the first time: worn apron, house slippers, a smaller man than expected. Slipper footsteps.
```

**S27 — 문을 활짝**
```
Inside the door. A man's hand takes the edge of the half-open glass door and swings it wide open.
Blue-hour light spills in a long strip across the shop floor. The bell rings softly once.
```

**S28–S31 — 렌즈 응시 (SC07)**
```
S28: Frontal medium close-up, centered. The 58-year-old repairman looks directly into the camera lens.
Warm amber lamp light on one side of his face, cool blue-hour light from the open door on the other.
He says in Korean, slowly: "그때, 오지 말라고 한 거…" — breathes, eyes drop for a moment then return to
the lens — "미안하다." No music.
S29: Frontal medium close-up, centered. The 31-year-old woman looks directly into the lens. Two seconds of
stillness, then she says in Korean: "지금은?"
S30: Same framing as S28. A short breath. He says in Korean: "와 줘서… 좋다."
S31: Same framing as S29. No words. Her tight mouth softens very slightly; her eyes are wet but she does not cry.
Real-time, no slow motion.
```

**S32 — 문턱 투숏**
```
Strict profile two-shot across the threshold of the open door. She is outside, he is inside.
She says in Korean: "그래도 내일은 가."
```

**S38**
```
Close-up of the repairman. His eyes move from the recorder to the woman to the door. He picks up the recorder
and turns his body away to cover its sound.
```

### 5.6 립싱크 숏 실패 시 대안

| 숏 | 1안 | 실패 시 대안 |
|---|---|---|
| S15 | 은서 4분의 3 측면 | 문틈 사이 뒷모습 + 대사 |
| S16 | 작업등 갓이 입을 반쯤 가림 | 손 인서트 + 화면 밖 대사 |
| S17 | 은서 미디엄 | 성호의 반응 숏 + 화면 밖 대사 |
| S21 | 은서 미디엄 | 은서 실루엣(문 유리) |
| S22 | 정면 "가…" | 입술만 열리는 초접사(음절 하나라 판독 부담 낮음) |
| S25 | 정면 "잠깐만." | 드라이버를 놓는 손 + 화면 밖 대사 |
| S28–S30 | 정면 렌즈 응시 | **대안 없음 — 최우선 재생성.** 이 작품의 정서적 정점이므로 테이크를 가장 많이 쓴다 |
| S32 | 정측면 | 실루엣 투숏 |

### 5.7 생성 순서 (가장 위험한 것부터)

1. **기준 자산 고정**: `CH_SUNGHO` · `CH_EUNSEO` · `PROP_REC` · `SET_SHOP` 3장 타블로
2. **S01 스플릿 디옵터** + **S06 릴 축**: 이 두 숏이 안 되면 콘셉트를 바꿔야 하므로 먼저 확인
3. **S28–S31 렌즈 응시**: 정서적 정점, 립싱크 최난도
4. 문 타블로 3종(S03 · S11 · S39) / 무대 타블로 2종(S14 · S34) — 같은 기준 이미지로
5. S13 · S37 스플릿 디옵터, S20 손바닥, S23 정지
6. 나머지 립싱크 숏 → 인서트 → S26 이동
7. 대사 음성 테이크 선정 후 **음성 원본 재사용 맵(§4.2)** 대로 편집

---

## 6. 공모 적합성 대응 (R2)

예상 점수가 아니라 자체 연출 판단이다.

| 심사 축 | R2의 대응 | 남는 위험 | 보완 |
|---|---|---|---|
| **Idea 35** | 미래를 듣는 장치 × 자기 말을 바꾸는 수리공 × **바꾼 결과로 생긴 새 위험** | '미래를 들려주는 기계'는 익숙한 장르 장치 | 손바닥으로 막기·릴 축 규칙·노크 리듬 구분 같은 **구체적 행동과 소리 규칙**으로 차별화 |
| **Pull 25** | 첫 프레임 '닫힌 입 + 떨리는 스피커', 12~18초 간격 훅, 블랙 위 노크로 끝 | 고정 카메라가 느리게 느껴질 수 있음 | 평균 3.6초 컷. 정지된 프레임을 빠르게 넘긴다 |
| **Resonance 20** | 단 한 번의 렌즈 응시, 서툰 사과, 의자를 비우는 행동, 부품통을 주워 올리는 딸 | 음악 없는 감정 장면이 밋밋해질 위험 | 음악 대신 두 빛의 충돌과 침묵의 길이로. S31 끝에서야 첫 음악 |
| **Craft 20** | 한 공간, 두 인물, 소품 고정, 같은 구도 반복, 소리 원본 재사용 | 녹음기 형태·문 방향·의상 드리프트 | 기준 자산 고정 + §8 T03 연속성 검수 |
| **시청시간 40%** | 148초에 완주를 유도하는 클리프행어 | 3분까지 늘리면 시청시간은 늘어도 완주율이 떨어질 수 있음 | 148초 유지. 늘리지 않는다 |

---

## 7. 출품용 작품설명 (R2)

> 수리공 성호는 테이프도 없는 녹음기에서 자신의 목소리를 듣는다. 딸에게 "다시는 오지 마"라고 말하는, 아직 하지 않은 말이다. 잠시 뒤 실제로 딸이 문을 두드린다. 평생 기계를 고쳐온 그는 이번에는 자신의 다음 말을 고쳐야 한다. 그리고 말을 바꾼 대가로, 녹음기는 딸의 목소리로 새로운 경고를 들려준다. 「내일수리점」은 미래의 소리를 듣는 수리공을 통해, 알면서도 되풀이하는 말과 그것을 바꾸는 선택을 그리는 미스터리 드라마다.

영문(초안):
> A repairman hears his own voice from a cassette recorder with no tape inside: words he hasn't said yet, telling his daughter never to come back. Moments later, she knocks. He has fixed machines all his life; now he has to fix what he says next. But changing it opens a new future, and the recorder warns him in his daughter's voice.

---

## 8. 제작 전 테스트 (R1의 3개 + 1개)

| ID | 확인할 것 | 방법 | 통과 기준 |
|---|---|---|---|
| T01 소리 선행 | '기계가 먼저 낸 소리가 현실에서 반복됐다'가 읽히나 | S05–S12 러프 편집을 해설 없이 3명에게 보여줌 | 3명 중 2명 이상이 "미래의 소리"라고 말함 |
| T02 감정의 변화 | 음악 없이 사과가 읽히나 | S17–S31 러프 | "아버지가 같은 말을 하려다 바꿨다"를 설명할 수 있음 |
| T03 연속성 | 녹음기 키 6개·스피커 왼쪽·카세트실 오른쪽, 문 위·왼쪽, 의상, 부품통 위치, 의자 위 상자 유무, **문 상태 4단계** | 전 숏 나란히 비교 | 한 번이라도 되돌아가면 해당 숏 반려 |
| **T04 무음 판독** (신규) | 소리를 끄고 자막만으로 이야기가 읽히나 | 무음 재생 + 출처별 자막 | 녹음기 목소리와 실제 목소리를 구분할 수 있음 |

> 아직 어떤 테스트도 시행하지 않았다.

---

## 9. 리스크와 대안

| 리스크 | 신호 | 대안 |
|---|---|---|
| Veo가 스플릿 디옵터를 이해 못함 | 화면이 반으로 갈라짐, 분할 화면처럼 보임 | 정지 키프레임을 이미지로 먼저 확정 → 움직임 최소 클립. 그래도 실패하면 깊은 심도 구도(§5.5) |
| 테이프 없이 도는 릴 축이 안 나옴 | 테이프가 생겨남, 축이 안 돎 | Frames to Video에 같은 프레임을 시작·끝으로 넣고 `only the two spindles rotate`. 그래도 안 되면 카세트실 초접사 + 회전 소리 |
| 렌즈 응시 숏의 한국어 립싱크 | 입 모양 어긋남, 발음 뭉개짐 | 대사를 끊어 짧은 테이크 2개로 생성 후 편집에서 연결(S28을 "그때… 한 거…" / "미안하다."로 분리) |
| 목소리 음색이 숏마다 다름 | 성호가 다른 사람처럼 들림 | 화면 밖 대사는 대표 테이크 하나로 통일. 립싱크 숏끼리 음색이 가장 가까운 테이크 조합 선택 |
| 노크 리듬이 구분 안 됨 | 2회와 3회가 비슷하게 들림 | 편집에서 간격 조정(2회: 길게–짧게 / 3회: 고르게 느리게) |
| 148초 초과 | 대사 실측 후 길어짐 | S04 → S24 → S35 순서로 삭제 (−8초) |
| 문 방향 뒤집힘 | 문이 오른쪽에 생성됨 | 좌우 반전으로 해결하지 말 것(공구·키 배열이 뒤집힘). 재생성 |

---

## 10. D-7 일정 (10/4 → 10/11 23:59 마감)

| 날짜 | 작업 |
|---|---|
| **10/4 (토)** | 공식 규칙 페이지 재확인(자막 언어·60/40). 기준 자산 6종 생성·확정 |
| **10/5 (일)** | **콘셉트 게이트**: S01 디옵터 · S06 릴 축 · S28 렌즈 응시 테스트. 셋 중 둘이 안 되면 대안 구도로 전환 결정 |
| **10/6–7** | 타블로 5종 → 립싱크 숏 → 인서트 → S26 |
| **10/8 (목)** | 음성 테이크 선정, 녹음기 가공, 러프 편집. T01·T02·T04 |
| **10/9 (금)** | 실패 숏 재생성, T03 연속성, 자막(한·영), 타이틀, 마스터 |
| **10/10 (토)** | 공개 SNS 게시·공식 계정 태그 → 출품 폼 접수 |
| 10/11 (일) | 예비일. 제출 후 수정·철회 불가이므로 10/10 접수를 목표로 함 |

### 제출 점검 (R1 유지 + 추가)

- [ ] 총 재생시간(타이틀 포함) 3분 이하, 9:16 정확, 300MB 이하
- [ ] 화면에 생성된 글자·로고가 없는지 전 프레임 확인
- [ ] 자막 있는 본편 / 자막 없는 마스터 / 영어 자막판 분리 보존
- [ ] Flow 프로젝트·기준 이미지·전 테이크·프롬프트 로그 보존
- [ ] 실존 인물·브랜드를 닮은 요소가 없는지 확인
- [ ] 공개 SNS URL, 태그, 출품 영상 일치 확인
- [ ] 실제 접수 증거가 있을 때만 제출 완료로 기록

---

## 출처

- [R1] Vigloo Studio, 「2026 비글루 숏드라마 페스티벌 공모전 참가 규칙」, 2026-10-02 열람(R1 문서 기록). `https://vigloostudio.com/ko/contests/2026-short-drama-festival/rules` — 이번 작성 환경에서는 직접 열람하지 못함.
- 공모 주제·상금·공개 일정 보도: [벤처스퀘어 — '다음 화가 궁금해지는 3분' 찾는다…비글루, 글로벌 AI 숏드라마 공모](https://www.venturesquare.net/1113486/)
- 세로 숏드라마 형식 동향: [Spectrum News — Vertical microdramas rise (2026-01)](https://spectrumlocalnews.com/ca/california/entertainment/2026/01/17/vertical-microdramas-rise), [Hillary Marek — Vertical Micro-Drama for 2026](https://hillarymarek.substack.com/p/the-zero-budget-goldmine-a-masterclass) (1/48초 셔터 등 촬영 관행), [Majalla — The age of the microdrama: why slow cinema matters more than ever](https://en.majalla.com/node/331975)
- 세로 영화 실험: [Vertical Movie Festival 2026, Rome](https://festhome.com/blog-article/36020) (Vertical AI 부문 포함)
- 스플릿 디옵터의 재유행: [Deeper Into Movies — the 70s camera technique you've been seeing](https://deeperintomovies.substack.com/p/the-70s-camera-technique-youve-been)
- Veo 3.1 / Flow 기능(9:16, Ingredients·Frames to Video·Extend의 오디오 지원): [9to5Google — Veo 3.1](https://9to5google.com/2025/10/15/veo-3-1/), [Android Authority — Veo vertical video output](https://www.androidauthority.com/google-veo-vertical-video-output-3632187)

이 문서의 줄거리·대사·연출은 창작 초안이다. '어쿠스매틱 타블로'는 이 문서에서 붙인 이름이며, 인용한 기법(화면 밖 목소리, 스플릿 디옵터, 정면 타블로, 렌즈 응시)은 특정 작품의 장면을 옮긴 것이 아니라 일반적인 영화 기법이다. 수상 가능성은 산정하지 않는다.
