# DEL74 오프라인 작업 지시서 R02 (2026-10-25)

대상: 사용자 PC(Windows, RTX 3060 Ti 8GB, Blender 4.5 LTS GUI)에서 작업하는 사람 또는 에이전트. 온라인(Claude)에서 설계·베이크·그레이박스·검증 스크립트까지 끝냈다. 여기서부터는 **에셋 통합 → 룩 → 애니매틱 → 핵심 4초 → 전편 → 최종 렌더**다.
규칙은 `AGENTS.md`, 바꿀 수 없는 것은 `DEL74_LOCKS.md`, 왜 그렇게 설계했는지는 `REVISION_PLAN_R02.md`.

진행 원칙 세 가지
1. 게이트를 건너뛰지 않는다. 각 단계 끝의 "통과 조건"이 전부 PASS여야 다음 단계.
2. 한 라운드 한 변수. 바꾼 것 하나와 이유를 `review/R##/CHANGELOG.md`에.
3. 수치는 JSON에서만 바꾼다(`src/rig_config.json`, `src/camera_keys.json`, `src/materials.json`, `assets/asset_map.json`). .blend를 손으로 고친 것은 다음 빌드에서 사라진다.

---

## 0단계 — 환경 (반나절)

### 0.1 폴더
```
C:\Users\lek\Documents\claude blender\DEL74\      ← 이 패키지 전체 복사(저장소 del74/)
  audio\DEL74_VO_R2_Hyuk.mp3                       ← 드라이브 제작 폴더에서 가져와 넣는다 (sha256 96771068…1e1de 확인)
  assets\<에셋 폴더>\                               ← G-ASSET-1 구매 뒤
  render\                                          ← .blend, PNG 패스, comp (드라이브 동기화 폴더 금지)
```
### 0.2 도구
- Blender 4.5 LTS (경로가 다르면 `RUN_ALL.ps1 -Blender "<경로>"`), ffmpeg(PATH), Python 3.11.
- `py -3.11 -m venv venv` → `venv\Scripts\pip install numpy pillow OpenEXR`
- 확인: `.\RUN_ALL.ps1 -VerifyOnly` 가 "VerifyOnly 완료"로 끝나야 한다. 이게 **재현 기준값**이다(HANDOFF_R02.md §3의 값과 같아야 함: bake_qc 28/28 PASS, v0 1.47916 m/s, ω_run 6.0246 rad/s, slack 0.08/0.0422/0.0511/0.06).
- 음성 sha256: `Get-FileHash audio\DEL74_VO_R2_Hyuk.mp3 -Algorithm SHA256` 이 `audio/VO_LOCK.json`과 같아야 한다. 다르면 중단하고 보고.

### 0.3 GUI에서 한 번 열어 보기
`render\del74_scene.blend`를 Blender 4.5로 연다(저장하지 말 것). 확인:
- 타임라인 마커 C01…C11b 16개, 카메라 CAM 하나, 컬렉션 LOCO/CARS/TRACK/GHOSTS/RIMS/CUTTERS.
- F1 → F150 → F318 → F894 스크럽: 외피가 F90–120에서 투명해지고, F318에 유령 축이 체결되고(GHOSTS는 MAIN 뷰레이어에서 제외라 뷰포트엔 안 보일 수 있음 → 뷰레이어 GHOST로 전환), F894에 기어가 돌기 시작.
- 안 보이는 게 있으면 재질이 아니라 **컬렉션 가시성(hide_render 키)** 부터 의심.

---

## 1단계 — 에셋 통합 (G-ASSET-1, 1–2일)

목표: 외피·캡·후드를 구매 에셋으로 교체하고 충돌 0건.

1. `assets/README.md`대로 구매·배치. 라이선스는 `assets/LICENSES.csv`에 먼저 적는다(없으면 공개 불가).
2. `assets/asset_map.json`에 부품 항목 작성. 좌표는 기관차 로컬(원점 = 차체 중심 직하 레일면, +X 전방, +Y 좌측). 프록시 치수(`src/rig_config.json loco.*`)와 겹쳐 맞춘다.
3. 가짜 에셋 스모크: `blender -b render\del74_scene.blend -P src\import_assets.py -- --fake --out render\smoke.blend` 후 `blender -b render\smoke.blend -P src\verify_scene.py -- --step 50` → 일부러 location을 엔진 안에 두고 FAIL이 나는지 확인. (게이트가 살아 있다는 증거를 REPORT에 남긴다.)
4. 실제 통합: `.\RUN_ALL.ps1 -AssetMap -VerifyOnly`
5. 에셋 외피에 재질 `M_GHOST`를 지정한다(프록시에서 상속되지만 서브메시가 여러 개면 수동). pass_index = 1(외피)로 통일. 외피 메시는 **바닥면이 없어야**(열린 쉘) 카메라가 내부로 들어갈 때 뒷면 컬링이 먹는다.
6. 폴리 예산: 외피 ≤1.2M 삼각형. 넘으면 Decimate(Planar 2°)로 줄이되 베벨 모서리는 유지.

통과 조건: `evidence/scene_qc.json` ALL PASS(충돌 0 또는 설계 접촉 목록만), 외피 치수 ±1%(길이 20.787 / 폭 3.127 / 높이 4.254), `REPORT.md` 기록.

---

## 2단계 — 모델 디테일 승격 (절차 모델 → 레퍼런스급, 2–3일)

프록시(그레이박스)는 리그가 맞는지 보려고 만든 것이다. 아래 순서대로 **같은 오브젝트 이름·원점·회전축을 유지한 채** 형상만 고도화한다. 방법은 둘 중 하나: (a) `src/geo.py`에 함수를 추가해 `build_scene.py`에서 생성(권장, 재현 가능) (b) Blender에서 모델링한 메시를 `assets/parts/<name>.blend`로 저장하고 `asset_map.json`으로 교체.

우선순위(화면 점유 × 컷 수):
1. **크랭크축·피스톤·커넥팅로드**(C02·C04·C10a·C11a): 크랭크 웹을 실제 단면(타원 카운터웨이트), 핀 저널에 필렛, 커넥팅로드 I-단면 + 대단부 캡 볼트 2개, 피스톤 링 홈 3줄(얕게, 고주파 금지). 원점: CRANK_SHAFT = 크랭크 축선, ROD_xx = 크랭크 핀 중심, PISTON_xx = 피스톤 핀. 회전축 바꾸지 말 것.
2. **대치차·피니언**(C08): `geo.gear`의 사다리꼴 치형을 인벌류트로 교체(모듈 = 2·0.380/57, 압력각 20°). 치면 폴리곤 material_index 1(M_MACH) 유지 — 맞물림 판독은 치면 명도에서 나온다. 치면 간극 0.3mm LOCK.
3. **차륜**(C07a·C08·C09): 답면 1:20 기울기, 플랜지 R, 림 뒷면 오목, 허브. 답면만 M_MACH.
4. **전동기 하우징**(C07b): 원통 → 노즈 서스펜션 돌기 + 환기구 리브 + 단자함. 회전자(MOTOR_ROTOR) 보이도록 커터 링 쪽 하우징은 튜브.
5. **발전기**(C05): 회전자 극편 12 → 실제 극편 형상 + 고정자 코일 엔드(구리 M_COPPER). 케이스 커터 링이 열릴 때 코일 단면이 보여야 한다.
6. **케이블·클램프·정션박스**(C06a/b): 6본 다발 유지, 클램프 간격 0.6m, 대틀 관통부 그로밋. 정점 속성 `u`는 `geo.polyline_tube`가 쓴다 — 에셋 교체 시 같은 속성을 굽는다(없으면 청록 펄스가 안 나온다).
7. **대차 프레임·축상·브레이크**(C07a): HT-C 측프레임 윤곽, 축상 스프링, 브레이크 슈. 커터 링 불리언이 측프레임(`BOGIE_SIDEFRAME_L`)에 걸려 있으니 이름 유지.
8. **연결기**(C09): 너클·셰ンク·드래프트기어 박스. 유격은 리그(car_x)가 만든다 — 모델은 정적.
9. **객차**(C01·C09·C11b): 창·문 음각, 대차 LOD1, 연결면 23.5m LOCK.
10. 레일·침목·자갈: 자갈은 변위 대신 범프 유지(흰 점 함정).

금지: 모디파이어 베벨(인스턴스에 안 먹음) → `bmesh.ops.bevel`로 굽기. 30° 초과만 sharp.
통과 조건: 540p 대표 스틸 8장(`.\RUN_ALL.ps1 -Stills "1,150,318,426,505,745,894,1100"`)에서 명도 3층이 구분되고, `verify_scene` 충돌 0.

---

## 3단계 — 룩 (1일)

1. `src/materials.json`만 고친다. 값 바꾸고 `RUN_ALL -Rebake` 없이 `build_scene`만 재실행(`-Rebake`는 베이크까지).
2. 도색: 현행 실차 사진(좌측면, 정면) 2장 확보 → `M_PAINT.base_color` 확정. 사진은 `reference/paint/`에 두고 LOCKS STYLE에 "도색 확정 R03"으로 올린다. 로고·차번은 넣지 않는다.
3. 하늘·태양: `M_SKY`의 zenith/horizon/sun_elevation/sun_strength. 답면·치면에 하이라이트가 걸리는 방위(현재 215°)를 유지.
4. 540p 스틸에서 확인할 것 — 외피 고스트 상태에서 내부가 어둡지 않은가(그림자 레이 투과가 작동), 커터 링 절단면이 다크 스틸로 보이는가, 크랭크 저널·치면·답면이 **가장 밝은** 세 곳인가.
5. 저비트레이트 스트레스: `ffmpeg -i preview.mp4 -c:v libx264 -b:v 2M -maxrate 2M -bufsize 4M -an stress.mp4` 로 고주파 깜빡임 확인.

통과 조건: 540p 스틸 8장 + 리뷰어(제작 비관여) 판독 "3층 구분·주인공 판독 OK".

---

## 4단계 — 후합성 파이프 검증 (반나절)

1. 패스 포함 스틸: `blender -b -P src\render_still.py -- --blend render\del74_scene.blend --frames 150,318,520,600,810,1140 --pct 50 --spp 24 --device OPTIX --out render\test --passes 1`
   → `render\passes\combined####.png`, `render\passes_exr\{depth,normal,index,ghost_index,electric}####.exr`
2. `venv\Scripts\python src\post_comp.py --frames 150-150 --root render` 등 프레임별 실행 → `render\comp\0150.png`
3. 확인: F150 엣지 라인(무채색)이 내부 부품에만, F318 유령 축 점선 윤곽, F520 커터 림 흰선 + 청록 펄스 없음(F540부터), F600 케이블 위 청록 펄스, F810 전동기 3번 테두리 펄스, F1140 변속기 유령.
4. 색 의미 점검: 청록은 전기에만. 주황·황록이 어디에도 없어야 한다.
5. 강도 조정은 `post_comp.py`의 `STYLE` 딕셔너리와 각 장치의 곱 계수(0.55 / 0.9 / 1.4 / 1.2)만.

통과 조건: 6프레임 comp PNG가 REVISION_PLAN P2 표와 일치, 리뷰어 OK.

---

## 5단계 — G5 애니매틱 270p 전편 (반나절, GPU 약 20–40분)

```
blender -b -P src\render_still.py -- --blend render\del74_scene.blend --frames (1..1416 -join ",") --pct 25 --spp 6 --device OPTIX --out render\animatic --passes 0
ffmpeg -framerate 30 -i render\animatic\F%04d.png -i audio\DEL74_VO_R2_Hyuk.mp3 -vf "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p" -c:v libx264 -crf 18 -c:a aac -shortest review\R02\animatic_270p.mp4
```
확인(무음 → 유음 순서):
- 무음: 컷 경계가 BEATS.csv F와 맞는가(마커), 카메라가 멈추는 구간이 없는가, 사건 간격 ≤2 s.
- 유음: 명사 전에 대상이 보이는가(`evidence/bake_qc.json noun_pre_exposure` 값으로 재확인), F318 체결·F894 기동·F983 연결기가 들리는 말과 맞는가.
- 루프: `ffmpeg -sseof -0.04 -i animatic.mp4 last.png` 와 F1 SSIM ≥0.85.
통과 조건: `review/R02/animatic_270p.mp4` + `evidence/sync_qc.json`(명사 선행 표, 카메라 정지 0, 루프 SSIM).

---

## 6단계 — G6 핵심 4초 F375–552 540p (1일)

`.\RUN_ALL.ps1 -Key4s` → `review\R02\key4s_540p.mp4`. 정상속도로 3회 본다. 판독 질문 세 개에 "예"여야 통과:
1. 유령 축이 빠져나가는 되감기가 "가정을 지운다"로 읽히는가(F370–393).
2. 하늘 앞 크랭크+피스톤만 남는 고립이 "16기통"으로 읽히는가(F394–487, 자막 없이).
3. 카메라가 커플링을 지나 회전자로 미끄러질 때 "같은 축"으로 읽히는가(F487–551).
아니오가 있으면 `camera_keys.json`의 C_C04_C06b 체인 키만 조정(한 라운드 한 변수) → 재베이크 → 재렌더.

---

## 7단계 — G7 전편 540p 프리뷰 + 사용자 리뷰 (1일)

- 540p 24spp 전편(약 1–2시간 GPU) → 후합성 → MP4 + UI 마스크 겹침 확인(쇼츠 실기 스크린샷 마스크 PNG를 `reference/ui_mask.png`로 만들어 키프레임 시트에 겹친다) + 저비트레이트 2 Mbps 재인코딩 판독 + 휴대폰 실기 1회.
- 리뷰 패킷 `review/R02/`: contact_270p.jpg, key4s_540p.mp4, preview_540p.mp4, qc_summary.json, CHANGELOG.md.

---

## 8단계 — G8 최종 1080p (GPU 3–6시간, 청크·이어하기)

1. 대표 프레임 실측: `blender -b -P src\render_still.py -- --frames 1100 --pct 100 --spp 256 --device OPTIX --passes 1` 시간과 `nvidia-smi` 피크 VRAM을 REPORT에 적고 전체 환산(×1416).
2. `.\RUN_ALL.ps1 -Final -Chunk 12 -Spp 256` — 이미 있는 PNG는 건너뛴다(중단 뒤 다시 실행하면 이어서). 실패 청크는 2회 재시도 후 목록 보고. `render\render_log.csv`(frame, sec, peak_vram, retries).
3. 사운드: `audio/SFX_CUES.csv`(F·초 확정)대로 효과음을 깔고 `audio/mix.wav`를 만든다(내레이션 > 기계 폴리 > 전환 > 공간음, 덕킹). 측정 `ffmpeg -nostats -i mix.wav -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null -`.
4. 인코딩은 RUN_ALL이 bt709 행렬 명시로 수행. `evidence/delivery_qc.json`: 1080×1920, 30fps, 1416 프레임, 디코드 오류 0, sha256.
5. 재현성: 패키지를 깨끗한 폴더에 복사해 `-VerifyOnly`를 다시 돌리고 bake_qc 수치가 같은지 확인.

---

## 9단계 — G9 공개 전 (사용자)
- 사실 재확인(F8 출처 URL 1건 보강, F12 원문 이미지), 라이선스 장부, 자막(basak-shorts-caption, 별도 레이어), CTA 고정 댓글 1️⃣/2️⃣, AI 라벨 판단(풀3D는 실사 아님).

---

## 자주 겪는 문제
| 증상 | 원인 | 조치 |
|---|---|---|
| 렌더가 검고 오래 걸림 | 액션 슬롯 미지정/카메라 원점 | build 로그의 `F1: CAM=` 출력 확인. (14.5, 6.5, 1.1)이어야 함 |
| 외피 안이 검게 나옴 | M_GHOST 그림자 레이 분기 깨짐 | materials.json 손대지 말고 build 재실행. 에셋 외피는 M_GHOST 지정 확인 |
| 유령·림이 뷰포트에 안 보임 | GHOSTS/RIMS는 MAIN 뷰레이어 제외 | 뷰레이어 GHOST로 보기. 렌더는 정상 |
| 기어가 차륜에 가려 안 보임 | 대치차는 차륜 안쪽(inboard) | C08 고립이 좌측 차륜·축상을 숨긴다(설계). 다른 컷에서 보이게 하려 하지 말 것 |
| 회전 부품이 분홍 스미어 | 각속도 과다 | `engine.omega_run_target` 6.0 rad/s 유지(2.5 rev/s 실패 실측) |
| 청록 펄스가 안 나옴 | 케이블 메시에 `u` 속성 없음 / electric AOV 미출력 | geo.polyline_tube로 생성하거나 속성 굽기, 뷰레이어 AOV 'electric' 확인 |
| 충돌 수천 건 | 접촉면 동일평면 | rig_config 간극 값(침하 0.1mm, 치면 0.3mm, 라이너 0.5mm, 너클 1mm) |
| PNG 색이 틀어짐 | ffmpeg BT.601 기본 행렬 | RUN_ALL 인코딩 명령 그대로(out_color_matrix=bt709) |
