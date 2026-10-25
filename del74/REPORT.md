# REPORT.md — 작업 기록 양식 (한 작업 한 블록, 최신이 위)

## [작업ID] 제목 — 날짜, 작업자
- 변경 파일:
- 실행 명령:
- 게이트값: (bake_qc ALL / scene_qc ALL·충돌 수 / 명사 선행 / 루프 SSIM / 렌더 sec·peak VRAM)
- 산출물: (경로, sha256)
- 판정: PASS / FAIL / NOT_PERFORMED / NOT_DECIDABLE
- 질문·블로커:

---
## [R02-00] 온라인 설계·그레이박스 — 2026-10-25, Claude
- 변경 파일: 패키지 전체 신규(HANDOFF_R02.md 참조)
- 실행 명령: `python3 src/bake.py; python3 src/verify_bake.py; python src/build_scene.py; python src/render_still.py --frames 1,150,318,426,505,745,894,1100 --pct 25 --spp 8`
- 게이트값: bake_qc ALL PASS(28/28), 명사 선행 15/15 ≥6F(최소 변속기 21F), 루프 위상 잔차 차륜 0.0 / 크랭크 <1e-3 rad, scene_qc ALL PASS(step 10, 142프레임, 충돌 0, 카메라 최근접 0.4687 m @F971 DECK), 270p 8spp CPU 2.7–6.2 s/F
- 산출물: evidence/bake_qc.json, evidence/geometry_qc.json, review/R02/stills_270p/contact_graybox.png
- 판정: G3 PASS, G4 PASS(그레이박스), 후합성 파이프 PASS(2F), G5 이후 NOT_PERFORMED(오프라인)
- 질문·블로커: G-ASSET-1(외피 에셋), G-FACT-F12/F13(치수 원문), 도색 사진
