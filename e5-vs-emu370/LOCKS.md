# LOCKS — E5 vs EMU-370 (R1, 2026-10-09)

LOCK 항목은 사용자 승인 없이 바꾸지 않는다. 상태: CONFIRMED / CONFIRMED-목표(계획치) / UNVERIFIED / CONFLICT / DESIGN(연출 가정).

## FACT

| ID | 사실 | 상태 | 화면·내레이션 표기 | 출처 |
|---|---|---|---|---|
| F-E5-1 | E5 영업 최고속도 320 km/h | CONFIRMED | "시속 320km", 태그 '현역' | JORSA JRI, Railway Gazette |
| F-E5-2 | E5 노즈 길이 약 15 m | CONFIRMED / CONFLICT(일부 16 m) | "15미터" | JORSA, JRPass 블로그, Railway Gazette(ALFA-X 16 m 언급) |
| F-E5-3 | E5 10량 8M2T(동력분산식) | CONFIRMED | 표기 안 함. 단 "동력분산=한국의 차별점" 서술 **금지** | JORSA |
| F-E5-4 | 긴 노즈 목적 = 터널 미기압파(출구 폭음) 저감 | CONFIRMED | "터널 출구의 폭음을 줄이려고" | JORSA, RTRI(TRID) |
| F-SK-1 | 신칸센 개업 1964-10-01 → 2026년 62년 | CONFIRMED | "62년 신칸센" | 일반 사실 |
| F-PH-1 | 압축파는 음속으로 터널을 지나 출구에서 미기압파로 방사 | CONFIRMED | C2b·C2c 시각화 | TRID 382872, 290392 |
| F-EMU-1 | EMU-370 상업운행 목표속도 370 km/h | CONFIRMED-목표 | "370km를 노립니다", 태그 '목표' | 한국철도일보, Daum |
| F-EMU-2 | 상업운행 시점 2030년대 초(2031 / 2032-06 보도 상충) | CONFLICT → 범위 표기 | "운행 목표는 2030년대 초" | 조달경제신문, 리뷰타임스 |
| F-EMU-3 | 노즈 10.2 m (KTX-청룡 6.5 m), 돌고래형 노즈 | CONFIRMED(보도) | "10.2미터" | 더빅데이터 2026-10-03 |
| F-EMU-4 | 560 kW급 고속 전동기 | CONFIRMED(보도) | "560kW급 전동기" | 더빅데이터 2026-10-03 |
| F-EMU-5 | 전동기 방식(PMSM 등) | UNVERIFIED | **표기 금지** | — |
| F-EMU-6 | 동력차 배치(호차별) | UNVERIFIED | X-Ray 점등 패턴은 DESIGN. 하단 'CG 재현 · 2026 공개 콘셉트 기준' 필수 | — |
| F-EMU-7 | 설계 최고속도 400 / 407 | CONFLICT | **표기 금지** | — |
| F-EMU-8 | 외관 색·헤드라이트 디자인 | UNVERIFIED | 공개 이미지 확보 전 중립 화이트 | G-ASSET-2 |
| F-CR-1 | CR450 목표 영업속도 400 km/h, 시험 453 km/h | CONFIRMED-목표 | "400km", 태그 '목표·시험 중' | Railway News 2026-03 |
| F-CR-2 | CR450 상업운행 개시 | UNVERIFIED (2026-03 기준 미개시) | **공개 직전 재확인 (G-FACT-1)**. 개시됐으면 태그를 '현역'으로 바꾸고 N4 유지 | — |
| F-X-1 | "세계 2위 영업속도" | 거짓 | **사용 금지** | — |
| F-X-2 | "370km를 찍었다/달린다"(과거·현재 시제) | 거짓 | **사용 금지** | — |
| F-X-3 | 정상 주행 중 차륜–레일 불꽃 | 비현실 | **사용 금지** | — |

## SPEC

| 항목 | 값 |
|---|---|
| 렌더 | 1080×1440, 30fps, F1–F900, Cycles, AgX Base Contrast (4.5에 Medium Contrast 없음) |
| 납품 | 1080×1920 (위아래 240px 레터박스), H.264 High, AAC 48k, −14 LUFS |
| 시간 규약 | t = (F−1)/30, 프레임 범위 양끝 포함 |
| 비트 원본 | `src/config/beats.json` |
| 렌즈 | 비교 샷(C1·C5b) ≥70mm, 20mm 이하 금지 |

## RIG (풀이 코드 수정 범위)

- 수치 변경은 `src/config/*.json`에서만 한다. 풀이 코드(`src/kin.py`, `src/bake.py`)는 버그 수정일 때만 고치고 REPORT에 근거를 남긴다.
- `motion_bake.npz`가 빌드의 유일한 운동 입력이다. 빌드 스크립트 안에서 위치를 계산하지 않는다.
- 주행 속도는 실제 속도다(슬로모션 금지). 링 속도는 340 m/s.

## STYLE

- 밝은 주간 하이키, 볼류메트릭 금지, 단일 액센트 녹색 #7CF07C (+ 고스트 빨강 #FF5A4F, X-Ray 시안 #5FD7FF, 전동기 골드 #FFB23F).
- 인월드 텍스트는 흰색 + 검정 외곽선. 2D 텍스트는 레터박스 안에만.
- 카메라 정지 금지. 마지막 컷은 원경으로 빠지지 않는다.
