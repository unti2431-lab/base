# L10 근거 원문 대조 — R9a (2026-10-29 KST, 클라우드 세션)

> 방법: 원문 페이지를 직접 열어 해당 문장을 대조했다(WebFetch). PDF 원본 파일은 이 세션 셸에서 해당 호스트가 막혀 **저장하지 못했다** → 아래 발췌·URL·열람일로 대체. 로컬에서 PDF 인쇄본을 `evidence/` 에 넣으면 L10 accept가 완전히 닫힌다.
> 등급 규칙(CCL_R8 §1): S=검색 요약, D=첨부 PDF, P=원문·특허·제조사 문서 직접 대조, V=실차 적용 독립 확인. 등급끼리 대체하지 않는다.

## 1. 열람한 원문

| # | 자료 | URL | 열람일 | 원문 발췌(축약 없음, 125자 제한 구간) | 판정 |
|---|---|---|---|---|---|
| E1 | US2161724A "Automatic car coupler", 발명자 **Karl Scharfenberg**, 우선일 1936-03-10(독), 등록 1939-06-06 | https://patents.google.com/patent/US2161724 | 2026-10-29 | 청구항 1: "a pair of mating coupling devices each having a rotatable hook plate and a coupling eye pivoted to said plate" / 설명: 각 고리(eye)가 상대 훅 원판에 걸림, 스프링이 원판을 잠금 위치로 붙듦, 기존형은 피벗점이 **평행사변형**을 이룸 | **SCH-01 → P** (원리: 회전 훅 원판 + 원판에 핀 결합된 고리 + 스프링 + 상호 체결 폐루프) |
| E2 | US8800792B2 "Mechanical coupling in a draftgear", 출원인 EGO International → **Dellner Couplers AB**, 우선일 2010-09-14 | https://patents.google.com/patent/US8800792 | 2026-10-29 | 청구항 1: "a central plate (5) turnably mounted in the coupler head;" "a coupling link (7) pivoted in the central plate (5);" / 요약: 원판 둘레 홈(8)이 상대 링크를 문다, 인장 스프링(9)이 원판을 체결 위치로 붙듦 | SCH-01 보강(P). **정정: Voith 계열 아님(Dellner)** |
| E3 | US2214036A "Automatic tight-lock coupler", Van Dorn(Dornvan Corp.), 1940 | https://patents.google.com/patent/US2214036A/en | 2026-10-29 | 청구항 1: "a link arranged in the head and having a hooked end projecting from the front end of the latter" (편심 베어링으로 링크를 당기는 타이트락) | **SCH-01 근거로 부적합**(다른 계열). 인용 목록에서 제외 권고 |
| E4 | Voith Turbo Scharfenberg 보도자료 "Unveils Coupler Head One4" (railway-technology.com 게재) | https://www.railway-technology.com/contractors/data//pressreleases/press86/ (동문 press93) | 2026-10-29 | "the new high speed trains in Korea (KTX II), Spain (Talgo) and of course the ICE 3 drive with One4 couplers" | **C03 S → P(부분)**: KTX II = Voith Scharfenberg One4 헤드. **'type 10'은 이 문장에 없음** |
| E5 | Voith "High-speed trains" (KTX as economic factor) | https://www.voith.com/corp-en/voith-turbo-perspectives/high-speed-trains.html | 2026-10-29 | "The striking front ends of the KTX II, which went into service in 2010, are also from Voith." / KTX-이음·청룡: "The technology group equipped the trains with gear units, couplers and front ends." | C03 보강(P: 전두부 Voith). 연결기 형식명 없음 |
| E6 | KSR2018F107 「철도차량 연결기 시스템의 충격 흡수장치 적용 현황 조사 및 분석」(노재택 외, 2018 한국철도학회 추계) | http://railway.or.kr/Papers_Conference/201811/pdf/KSR2018F107.pdf | 2026-10-29 | §2.5.1 Type-10 절: "국내에서는 KTX-산천부터 본격적으로 적용되기 시작하였으며 …" / "Type-10은 1500 KN의 압축하중와 1000 KN의 인장력을 견딜 수 있다." | Type-10 ↔ KTX-산천은 **절 배치로 암시**될 뿐 직접 진술 아님 → type 10은 D 유지. 1,500/1,000 kN은 **계속 화면·VO 금지** |
| E7 | 아시아경제(영문) "KTX and SRT Begin Test Runs as a Single Train… Passenger Operations Start May 15" | https://www.asiae.co.kr/en/article/real-estate-policy/2026043016234556538 | 2026-10-29 | "On the 30th, at Suseo Station, KTX-Sancheon and SRT trains are connected for a test run of coupled operation." 시범 4/30–5/14, 승객 운행 5/15 | **N1 S → P**. 연결기 형식은 언급 없음 |
| E8 | 일본제철 철도부품 — 新幹線用密着連結器 | https://www.nipponsteel.com/product/railway-automotive-machinery-parts/list/railways/04.html | 2026-10-29 | "この連結器は廻り子式と呼ばれており、連結面間には錠と呼ばれる部品により互いの連結を保持し、新幹線用をはじめ民営・公営鉄道に広く使用されております。" | **JP-01 → P(부분)**: 신칸센용 밀착연결기 = 회전 요소(廻り子)식, '錠'이 연결면 사이에서 체결 유지. **반달 형상·스프링·쐐기면은 미기재** → D 유지 |
| E9 | All About 「東北新幹線で『連結外れ』…」(野田隆) | https://news.allabout.co.jp/articles/o/92166/ | 2026-10-29 | "先頭部のカバーが自動的に開き、連結器同士でつながる。" | NOSE-01(커버 자동 개방) 보강, 등급 S→P(언론 원문). 잠금 구조는 미기재 |

## 2. 접근 실패
- railway-technology.com press74 "20 Front-End Modules for 10 Trains": 사이트 오류(client_error)로 본문 0바이트. C03의 '초기 10편성 / type ten' 진술은 **여전히 S**.
- JR East Tech-31 p.29: 미열람(다음 라운드).

## 3. 등급 변경 제안 (LOCKS.md FACT 표에 반영)

| ID | R9 | R9a | 화면·VO 사용 변화 |
|---|---|---|---|
| SCH-01 | D | **P** (E1, E2) | VO S3b 원리 서술 근거 확보. 차량명은 여전히 붙이지 않음 |
| JP-01 | D | **P(부분)** (E8): 회전 요소 + 錠 체결, 신칸센용 | "반달 모양"은 **D 그대로** → VO는 **S2b_B(반달 제거판)** 권고 |
| C03 | S | **P(부분)** (E4, E5): KTX II 전두부·연결기 헤드 = Voith Scharfenberg One4. type 10 / 초기 10편성은 S·D | LOCKS 규칙상 **V 전까지 S3a_K 금지 유지** — 규칙 완화(P로 허용) 여부는 사용자 결정 |
| N1 | S | **P** (E7) | 설명란 후보 → 본편 한국 인프라 축 근거로 승격 가능(연결기 형식 주장 없이) |
| NOSE-01 | (P2) | P (E9) | W0 '노즈 커버 열린 상태' 묘사 근거 |

## 4. 상위 문서 정정
1. BLOCKER_PLAN_R8 §1 G0-C: "US8800792B2 (현대 Voith 계열)" → **Dellner Couplers(EGO International) 특허**. 원리 보강용으로는 유효.
2. BLOCKER_PLAN_R8 §1 G0-C: "US2214036A (타이트락 변형)" → Van Dorn 타이트락, 샤르펜베르크 계열 근거로 쓰지 않는다.
3. 일본제철 원문 용어는 '柴田式'이 아니라 **'廻り子式'**. VO의 "시바타 계열"은 업계 통칭이라 유지 가능하나, 설명란 근거 표기는 "廻り子式 밀착연결기(일본제철 제품 설명)"로 쓴다.
