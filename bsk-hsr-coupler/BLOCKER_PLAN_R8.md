# BSK-HSR-COUPLER R8 | 블로커 해소 계획

> 기준: 2026-10-27 KST | 전제: E6 = **(a) 노즈 직접 모델링** 확정 | 대상: `CCL_R8.md` §9의 게이트 전부
> 목표: 사용자가 손대는 일을 최소로 줄이고, 그 사이 이 세션에서 돌릴 수 있는 것은 전부 돌린다.

---

## 0. 결론 — 두 트랙으로 분리

| 트랙 | 담당 | 내용 | 결과물 |
|---|---|---|---|
| **A. 제작 선행** | 이 세션 (bpy 4.5.14, CPU) | 개념 리그 TEST A/B · W0 루프 블로킹 · 검증 코드 · 270p 애니매틱 | 베이크·QC·프리뷰. 근거 등급과 무관하게 **코드와 리그 골격은 지금 완성 가능** |
| **B. 근거·권리** | 사용자 (브라우저 10–20분) | 아래 §3 "다운로드 7건" | P/V 등급 승격. 리그에는 `rig_config.json` 수치만 갱신 |

핵심: **리그 코드는 수치를 config에서 읽으므로, 근거가 늦어도 재베이크만 하면 된다.** 근거를 기다리며 제작을 멈추는 것이 가장 비효율적이다.

**환경 제약 (확인 완료):** 이 세션은 PyPI만 열려 있다. 아래 호스트는 전부 차단되어 원문 대조를 할 수 없다.
`patents.google.com` `commons.wikimedia.org` `www.jreast.co.jp` `www.jsw.co.jp` `www.voith.com` `www.railway-technology.com` `sketchfab.com` `railway.or.kr` `en.wikipedia.org` `ko.wikipedia.org` `ambientcg.com` `polyhaven.com`
→ 환경 설정의 **Network access → Allowed domains**에 이 호스트들을 추가하면 트랙 B의 절반을 이 세션이 대신 할 수 있다. 추가하지 않으면 §3의 다운로드로 대체한다.

---

## 1. 게이트별 진단과 해법

| 게이트 | 블로커 | 지금 가진 것 | 가장 빠른 해법 | 실패 시 대안 | 품질 영향 |
|---|---|---|---|---|---|
| **G0-A** W0 실차 상태 | E5+E6 병결·노즈 개방 사진 없음 | PDF p7–8 재구성 도해(D) | Wikimedia Commons에서 E5+E6 병결 정면·측면 사진 3장(CC BY-SA) 다운로드. 도쿄역·모리오카역 사진이 많다 | 사진 없이도 W0 카메라·루프 블로킹은 가능. 노즈 형상만 보류 | 낮음. W0는 '외관'이라 기구 설명과 무관 |
| **G0-B** 시바타 피벗·접촉면 | 실차 도면 없음, 각도 HOLD | PDF p2 그림1, p3 §2.2(D) | ① J-PlatPat에서 IPC **B61G 3/xx**(밀착연결기) + "回転錠" 또는 "廻り子" 검색 ② JR East Tech-31 p.29 원문 ③ 신칸센 연결기 **근접 사진**(해방 레버·회전정이 보이는 앵글) | **CONCEPT_ONLY 워터마크 유지.** 영상 자체가 '원리 비교'라 개념 리그로도 One Big Idea는 성립한다. VO에서 '반달 모양' 제거 | 중간. 회전정 외형이 실차와 다를 수 있으나 기구 원리는 동일 |
| **G0-C** 샤르펜베르크 도면 | 제조사 도면 없음 | PDF p4–5(D) | **특허 3건 PDF 다운로드 (P등급).** 검색으로 번호 확정: **US2161724** (원판 회전 중심 오프셋 → 힘 평형), **US2214036A** (타이트락 변형), **US8800792B2** (현대 Voith 계열, 중앙판·링크·인장 스프링). IPC **B61G 3/16**이 바로 이 형식 분류다 | 이미 PDF p5의 링크 폐루프 설명으로 개념 리그는 가능 | **낮음. 사실상 해소 가능.** 특허 도면은 피벗·링크 배치가 그림으로 나오고, 참고 모델링에 권리 문제가 거의 없다 |
| **G0-D** KTX-산천 형식 (C03) | V 등급 없음 | PDF(D), 위키(S) | **Voith 보도자료 (2008경, railway-technology.com "20 Front-End Modules for 10 Trains")** 원문 확인. 검색 요약: Voith Turbo Scharfenberg가 KTX II **10편성용 전두부 모듈 20세트 + 자동연결기**를 공급, 연결기는 **one4 헤드의 type ten 버전**, 19편성 추가 옵션. + Voith 'High-speed trains' 페이지에 One4가 "Korea (KTX II)"에 쓰였다는 문장 | 확인 실패 시 R8 규칙대로 KTX 컷·VO 제외 | **낮음.** 초기 10편성(110000호대)은 제조사 자료로 V 가능. **120000호대(2세대)·KTX-이음은 별도 확인 필요**하므로 영상에서는 "KTX-산천"이라고만 말하고 호대는 특정하지 않는다 |
| **G0-N1** 한국 인프라 축 | 중련 근거·외관 없음 | 2026 KTX–SRT 중련 보도(S) | G0-D가 풀리면 자동 해소. 보도 원문 1건 저장(뉴데일리 2026-05-17 또는 SBS Biz) | FAIL 기록 후 사용자 판단 | 중간. 채널 게이트 항목 |
| **G0-E** E5 권리 | 현행 라이선스 미확인 | PDF p8 "CC BY 4.0"(D) | Sketchfab 페이지 **스크린샷 + 다운로드 zip + SHA256**. 합격선은 §4 | 유료 대안 D1/D2(Royalty Free) | 낮음 |
| **G0-E** E6 외관 | 후보 기각 → (a) 직접 모델링 | PDF p8 제원(D) | §2.4 절차. **필요 입력: E6 정면·측면·사선 사진 각 1장**(Commons) | 사진 전까지 프록시 박스로 W0 블로킹 | 중간. 화면에 걸리는 노즈 전반부만 만들면 작업량 ~8h |
| **G1** TTS | 보이스 미지정 | — | §2.5 **한 세션에 변형문까지 녹음** | 음절 추정으로 설계 예산 유지 | 높음(동기). 그러나 리그는 재베이크로 흡수 |
| **G2** 기구학 150F | 리그 없음 | 이 세션에서 bpy 설치 진행 중 | **지금 착수** (§2.1–2.3) | — | — |
| **G3·G4·G5** | G2 이후 | — | 트랙 A 안에서 연쇄 | — | — |

---

## 2. 트랙 A — 이 세션에서 지금 하는 일 (순서 고정)

### 2.1 환경
- `python3.11 venv + bpy==4.5.14` (설치 중). 4코어 CPU, GPU 없음 → Cycles CPU 270p 애니매틱, 540p는 핵심 120F만.
- 버전 가드·채널백 베이크·BVH 충돌 검사는 스킬 규범 코드를 그대로 쓴다.

### 2.2 `rig_config.json` 골격
모든 수치에 `value / unit / source(S|D|P|V) / status(LOCK|HOLD|CONCEPT)`를 붙인다. 초기값은 PDF(D)와 특허 비율(P 예정)로 채우고, 사용자 자료가 오면 값만 바꾼다.

### 2.3 TEST B 먼저, TEST A 다음
- **TEST B(샤르펜베르크)**는 특허 3건으로 P등급에 가장 가깝다. 폐루프 해석(원판 2 + 고리 2 = 평행사변형)을 먼저 풀어 체결 사건 F를 뽑는다.
- **TEST A(시바타)**는 CONCEPT_ONLY 워터마크로 블로킹. 회전정 1DOF, 쐐기면 접촉, θ는 HOLD.
- 둘 다 점대칭 인스턴스(Z 180°), 탑뷰 카메라, 회전 부호 +Z 반시계.
- 산출: `*_bake.npz`, `geometry_qc.json(events)`, 관통 0 보고, 270p 150F 프리뷰.

### 2.4 E6 노즈 (a) 절차
1. 사용자 사진 3장 → 정사영 레퍼런스로 Blender 배경 이미지 배치.
2. PDF p8 제원(차폭 2,945mm·노즈 13m)은 D등급이므로 **비례 기준으로만** 사용, 수치 표기 금지.
3. 화면에 걸리는 **노즈 전반부 ~4m + 열린 커버 포켓**만 SubD 모델링. 뒤쪽은 E5 차체 프록시.
4. E5(CC BY)와 같은 재질 세트, JR 표기 제거.
5. 산출: `E6_NOSE_v1.blend`, 540p 스틸 2장(W0 앵글).

### 2.5 TTS 녹음 지침 (사용자, 1회)
한 세션에 다음을 모두 녹음해 두면 재녹음이 없다.
- S1, S2(기본), **S2-대안**("…잠금부가 뒤로 밀렸다가…", '반달 모양' 제거판), S3(기본), **S3-KTX판**("한국 KTX-산천에도 쓰이는 샤르펜베르크 계열은…"), S5.
- 파일명 `VO_R8_S2_ALT.wav`처럼 변형을 구분. 각 파일 SHA256을 `VO_LOCK.json`에.
- 이후 `faster-whisper`로 단어 타임스탬프 추출은 이 세션에서 가능(모델 다운로드가 허용되면).

---

## 3. 트랙 B — 사용자 다운로드 7건 (우선순위순)

| # | 자료 | 어디서 | 푸는 게이트 | 저장 이름 |
|---|---|---|---|---|
| 1 | Voith 보도 "20 Front-End Modules for 10 Trains" 페이지 PDF 인쇄 | railway-technology.com → contractors/voith/pressreleases/press74 | **G0-D, N1** | `evidence/VOITH_KTX2_FRONTEND_2008.pdf` |
| 2 | 특허 US2161724, US2214036A, US8800792B2 PDF | patents.google.com | **G0-C** | `evidence/patents/` |
| 3 | E5+E6 병결 사진 3장 (라이선스 페이지 포함) | commons.wikimedia.org "E5 E6 coupled" | G0-A | `reference/W0/` |
| 4 | E6 정면·측면·사선 사진 3장 | commons.wikimedia.org | G0-E(E6) | `reference/E6/` |
| 5 | Sketchfab E5 라이선스 페이지 스크린샷 + zip | sketchfab.com | G0-E(E5) | `assets/E5/` + SHA256 |
| 6 | JR East Tech-31 (p.29) + 2025-12-02 보도 PDF | jreast.co.jp | G0-B(부분) | `evidence/` |
| 7 | KSR2018F107 PDF | railway.or.kr | G0-D 보강 | `evidence/` |

**대안(더 빠름):** 환경 설정 Allowed domains에 §0의 호스트를 추가하면 1·2·6·7은 이 세션이 직접 받고 대조한다. 3·4·5는 라이선스 판단이 걸려 있어 사용자가 보는 것이 맞다.

---

## 4. E5 에셋 합격선 재설정 (PDF p8 모순 해소)

- 규칙을 **2단 게이트**로 바꾼다: ① 권리 게이트(상업 이용 가능 + 저작자 표시 가능)를 **통과해야만** ② 품질 점수(외형·리깅·호환·최적화 75점 만점)를 매긴다. 라이선스 점수 25점은 폐지.
- 합격선: ② **60/75 이상**. 후보 A는 외형 26+리깅 15+호환 9+최적화 9 = 59 → **노즈 분리 리깅 완료 후 재채점**(리깅 항목이 오르면 통과). 미달 시 D1(CGTrader $20.99) 구매.

---

## 5. 순서와 소요 (추정)

| 순서 | 작업 | 담당 | 소요 | 선행 |
|---|---|---|---|---|
| 1 | bpy 환경 + rig_config 골격 + 검증 코드 | 세션 | 1–2h | — |
| 2 | TEST B 개념 리그·베이크·QC·270p | 세션 | 3–4h | 1 |
| 3 | TEST A CONCEPT_ONLY 블로킹 | 세션 | 2–3h | 1 |
| 4 | 다운로드 7건 (또는 도메인 허용) | 사용자 | 20분 | — |
| 5 | config 수치 갱신 → 재베이크 | 세션 | 30분 | 2–4 |
| 6 | E6 노즈 (a) | 세션 | ~8h | 4-③④ |
| 7 | W0 루프 블로킹 (프록시 → E5/E6) | 세션 | 2h | 1, 6 |
| 8 | TTS 녹음(변형 포함) | 사용자 | 30분 | — |
| 9 | 단어 타임스탬프 → 사건 F 재역산 → 재베이크 | 세션 | 1h | 5, 8 |
| 10 | 540p 핵심 120F×2, G3 판정 | 세션/검증자 | 2h | 9 |

사용자 몫은 **4·8 두 가지뿐**이고 서로 독립이라 오늘 안에 끝낼 수 있다.

---

## 6. 여전히 사용자 결정이 필요한 것
1. 네트워크 도메인 허용 여부 (허용하면 트랙 B의 1·2·6·7을 세션이 처리)
2. TTS 보이스명 (녹음 전 필요)
3. 실행 체계: 최종 렌더 `RUN_ALL.ps1` 수동 실행, 제작자=이 세션, 검증자=별도 세션 — 이 조합으로 갈지

## Sources (검색 요약 기준, 원문 미열람)
- [Voith press: 20 Front-End Modules for 10 Trains (railway-technology.com)](https://www.railway-technology.com/contractors/power-systems/voith/pressreleases/press74/)
- [Voith Turbo perspectives: High-speed trains](https://www.voith.com/corp-en/voith-turbo-perspectives/high-speed-trains.html)
- [US2161724A Automatic car coupler](https://patents.google.com/patent/US2161724)
- [US2214036A Automatic tight-lock coupler](https://patents.google.com/patent/US2214036A/en)
- [US8800792B2 Mechanical coupling in a draftgear](https://patents.google.com/patent/US8800792)
- [KTX-Sancheon — Wikipedia](https://en.wikipedia.org/wiki/KTX-Sancheon)
- [KTX-산천 — 위키백과](https://ko.wikipedia.org/wiki/KTX-%EC%82%B0%EC%B2%9C)
- [뉴데일리 2026-05-17 KTX·SRT 중련연결 첫 시연](https://biz.newdaily.co.kr/site/data/html/2026/05/17/2026051700002.html)

---
**정정 (R9a 검증, 2026-10-29):** §1 G0-C와 Sources의 특허 설명 중 US8800792B2는 Voith 계열이 아니라 **Dellner Couplers(EGO International)** 특허이고, US2214036A는 **Van Dorn 타이트락**으로 샤르펜베르크 계열 근거가 아니다. 샤르펜베르크 원리의 1차 근거는 US2161724(Karl Scharfenberg, 1939)이다. 상세: `evidence/L10_EVIDENCE_R9a.md`.
