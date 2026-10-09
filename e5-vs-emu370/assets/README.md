# assets — 사용자가 넣는 에셋

| 폴더 | 내용 | 블로커 |
|---|---|---|
| `e5/` | 구매한 E5 모델(.blend/.fbx) + `LICENSE.txt`(상업 영상 사용 가능 확인) | G-ASSET-1 |
| `emu370/ref/` | 이노트란스 2026 공개 이미지(측면·정면·상면 3장 이상) + `SOURCES.txt` | G-ASSET-2 |
| `emu370/` | 블루프린트 로프트 베이스(.blend) — Codex 생성 후 사람이 노즈 곡면 보정 | T11 |
| `cr450/` | C4 축소 모델용 실루엣 메시(공개 사진 수준) | — |
| `fonts/` | Pretendard, Black Han Sans (OFL) | — |

E5 에셋 구매 체크리스트:
- 대차·차륜·팬터그래프가 분리된 메시(리깅용)
- 노즈 곡면이 서브디비전 친화 토폴로지(반사 품질)
- 실측 스케일(노즈 약 15 m, 선두차 약 26.5 m)에 가까울 것 — import_assets.py가 3% 넘게 벗어나면 FAIL
- 실제 운영사 로고는 지우거나 비활성화

`asset_map.json`은 `asset_map.TEMPLATE.json`을 복사해 채운다.
