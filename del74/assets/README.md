# assets/ — 사용자가 넣는 에셋 (G-ASSET-1)

## 무엇을 사야 하나 (최고 품질안, 승인 2026-10-25)
외피·캡·후드·핸드레일·배장기·전조등: **EMD SD40-2 계열 고정밀 모델**(FBX 또는 .blend). GT26CW-2는 SD40-2 구동계 + 수출용 소형 차체(F10)이므로
- 그대로 쓸 수 있는 것: 대차 외형 참고(우리 대차는 자체 제작이라 참고만), 캡 전면 유리·핸드레일·연료탱크·배장기.
- 반드시 고쳐야 하는 것: 장후드 폭·높이(GT26 차체 전폭 3,127·전고 4,254 LOCK F4에 맞춰 스케일이 아니라 **치수 재모델**), 캡 폭, 라디에이터 구간 길이.
- 사지 말 것: 엔진 내부·발전기·전동기·기어 에셋(절차 모델이 이미 리그와 맞물려 있다).

후보 검색어: "EMD SD40-2 3d model fbx", "GT26CW-2", "KTX 7400 diesel locomotive". 상업 영상 사용 가능 라이선스(Royalty-free Editorial 아님)만.

## 넣는 방법
1. 파일을 `assets/<이름>/` 아래 둔다(예: `assets/sd40_body/long_hood.fbx`).
2. `assets/asset_map.json`의 `parts[]`에 항목을 쓴다: `file`, `replaces`(숨길 프록시 이름), `location/rotation_deg/scale`(기관차 로컬 좌표, 원점=차체 중심 직하 레일면, +X 전방, +Y 좌측), `collide_with`.
3. `assets/LICENSES.csv`에 한 줄 추가(라이선스 장부 없이는 공개 게이트 G9 통과 불가).
4. `.\RUN_ALL.ps1 -AssetMap -VerifyOnly` 로 통합·충돌 검사.
5. 스케일 확인: 통합 후 Blender에서 `BODY_HOOD` 프록시(숨김)를 잠시 켜고 에셋과 겹쳐 본다. 길이 20.787 / 폭 3.127 / 높이 4.254 에서 ±1% 넘으면 재조정.

## 가짜 에셋 스모크 테스트
`blender -b render\del74_scene.blend -P src\import_assets.py -- --fake --out render\smoke.blend` → 큐브로 매핑 경로만 검증. 일부러 `location`을 엔진 블록 안에 두고 `verify_scene`이 FAIL을 내는지 확인한다(게이트가 살아 있다는 증거).
