# assets/

R02 결정: **모델 에셋 없음.** 전 부품 자체 생성(`src/build_parts.py`, config 기반).
외부 입력은 CC0 텍스처·HDRI만 — 목록과 경제성 비교는 `ASSET_ORDER.md`.

```
assets/
  textures/   ambientCG·Poly Haven CC0 PBR (2K 이하)
  hdri/       Poly Haven CC0 실내 HDRI (2K)
  LICENSES.csv  파일명, 출처 URL, 라이선스, 구매ID(없음), 상업 영상 OK, 표기 의무, 용도
```
모델 파일을 들여올 일이 생기면(G7 룩 격차 시 유료 예비안) 가짜 큐브 스모크 테스트를 먼저 하고 `ASSET_MAP.json`에 충돌 쌍을 등록한다.
