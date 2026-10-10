# r9fix — R9 미해결 보고서 해결안 패키지

먼저 `R9_RESOLUTION_PLAN.md`를 읽습니다(§0 결론, §2 강체 합성, §3 R9 질문 8개 답, §5 VO).

| 파일 | 내용 |
|---|---|
| R9_RESOLUTION_PLAN.md | 해결안 본문 (§0~§8) |
| VO_PICKUP_SCRIPT.md | VO 부분 재녹음 원고 P1~P3 (승인 전 실행 금지) |
| POC_C001_v2_wholewheel_1080p.mp4 | 바퀴 구름 v2: 타이어+림 전체 회전, R_e 238, 5초 |
| POC_C001_v1_rim_only_REJECTED.mp4 | v1 림만 회전 — 기각본(비교용) |
| COMPARE_C001_v1_vs_v2.mp4 / _frames.jpg | v1·v2 바퀴 부분 나란히 비교 |
| POC_C008_rigid_sensor_1080p.mp4 | 센서 비접촉 강체 통과, 5초 |
| POC_contact_sheet.jpg | v2 바퀴·센서 첫/끝 프레임 |
| VERIFY_C001_v2.json · VERIFY_C001_v1_rim_only.json | 출력 프레임만으로 측정한 림·옆면 회전, 누적·0.5초 구간 무미끄럼 비, 노면 고정 |
| VERIFY_C008_sensor.json | 센서 위·아래끝, 틈, 단방향 이동 측정 |
| *_motion_log.csv | 합성에 적용한 프레임별 이동·회전값 |
| rigid_roll_composite_v2.py · rigid_sensor_composite.py | 합성 스크립트 (입력: R7 패키지 04_ASSETS) |
| verify_noslip.py · verify_sensor.py | 독립 검증 스크립트 |
| rigid_roll_composite_v1_rim_only.py | 기각된 v1 (재현용 보존) |

재현: `python3 -I rigid_roll_composite_v2.py <04_ASSETS> <out> 240 5 238` → `python3 -I verify_noslip.py <out> 238`
