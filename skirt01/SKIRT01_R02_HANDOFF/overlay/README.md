# overlay/ — 2.5D 후합성 레이어 (도형까지. 문자는 자막 레이어 basak-shorts-caption R08)

- `overlay_anchors.json` — `src/export_anchors.py`가 프레임별로 출력: COMB_LINE 양끝, 틈 양끝(C03·C04 양쪽), 돌출 양끝(C06), 강성·유연 구획점(C07), 끝단·스커트면 기준점(C09)의 2D 픽셀 좌표(1080×1920). 손으로 맞추지 않는다.
- 도형 사양은 PRODUCTION_PLAN_R02 §10. 흰 1.5px 치수선, 양끝 틱, 구획 브래킷(파랑 `#3D7BFF` 강성 / 주황 `#F08A24` 유연).
- 쇼츠 UI 마스크(`reference/shorts_ui_mask.png`, 사용자 휴대폰 스크린샷) 밖에만 배치.
- 숫자는 자막 레이어에서: 4mm, 7mm, 33~50mm **만**. 세부 치수·장착 높이·종료 거리 금지.
