# HANDOFF — E5 vs EMU-370 Blender 숏폼 (R1 → Codex)

## 한 문장 목표
레퍼런스(F-22 vs F-35)의 밝은 하이키 CG 질감과 1.8초 사건 리듬으로, 「현역 E5(노즈 15 m, 320) vs 목표 EMU-370(노즈 10.2 m, 370)」을 30초·900F Blender 숏폼으로 만든다. 모든 수치는 config와 베이크에서 나오고, 게이트 3층(베이크·충돌·화면)을 통과해야 한다.

## 1. 현재 상태

| 항목 | 상태 | 근거 |
|---|---|---|
| 레퍼런스 분석 | 완료 | `reference/REFERENCE_NOTES.md`, 컨택트 시트 3장 |
| 사실 검증 | 완료(공개 직전 재확인 2건 남음) | `LOCKS.md` FACT, F-CR-2·F-EMU-8 |
| 비트표 | 완료, 검사 PASS | `src/config/beats.json`, `evidence/beats_check_R1.json` |
| rig / shots / look config | 초안(시작값) | `src/config/*.json` |
| 베이크·빌드·검증 코드 | **미착수 — Codex T02–T08** | — |
| 에셋 | **미확보 — 사용자 G-ASSET-1·2** | `assets/README.md` |
| 음성 | 미녹음 | N1–N5 대본은 beats.json |

## 2. 재현 기준값 (Codex 첫 작업 = 이 값 재현)

| 검사 | 명령 | 기대값 |
|---|---|---|
| 비트 | `python3 tools/check_beats.py` | ALL true, 최대 사건 간격 50F, N1 7.25 / N2 6.68 / N3 7.15 / N4 6.99 / N5 6.83 음절/s, B5 9건 OK |
| 차륜 회전 | rig_config `wheel_rev_per_frame` | E5 1.097, EMU370 1.268 (= v / (π·0.86) / 30) |
| 링 이동 | 260 m / 340 m/s × 30 | 22.94F → 23F |
| 기둥 리듬 | 50 m / 102.78 m/s × 30 | 14.6F |

## 3. 시스템 구조

```
src/config/beats.json ──► tools/check_beats.py ──► evidence/beats_check.json   [G01]
src/config/rig_config.json ─┐
                            ├─► src/bake.py ──► src/motion_bake.npz (F0–F901)
src/config/shots.json ──────┘        │
                                     ├─► src/verify_bake.py ──► evidence/verify_bake.json   [G02]
assets/*.blend|fbx ─► src/import_assets.py (assets/asset_map.json) ─┐
src/config/look.json ───────────────────────────────────────────────┼─► src/build_scene.py ─► build/e5_emu370.blend
src/motion_bake.npz ────────────────────────────────────────────────┘          │
                                     ┌─────────────────────────────────────────┤
                                     ├─► src/verify_scene.py ──► evidence/verify_scene.json [G03]
                                     ├─► src/verify_proportion.py ──► evidence/proportion.json [G05]
                                     └─► src/render_preview.py ──► preview/*.png, *.mp4 [G04]
```

모듈 책임:
- `kin.py` — 순수 numpy. 열차 X(t)=x0+v·t, 차륜각 v·t/r, 대차 진동, 팬터 높이, 링 X(t), 카메라 Catmull-Rom. **bpy import 금지.**
- `bake.py` — kin 호출 → npz. 프레임 0–901, 키 이름 `E5_x`, `EMU370_x`, `E5_wheel_rad`, `ring_E5_x`, `ring_ghost_x`, `cam_<CUT>_pos`, `cam_<CUT>_rot`, `cam_<CUT>_lens`.
- `build_scene.py` — npz와 config만 읽어 오브젝트 생성·키 베이크. 컷 전환은 타임라인 마커 + 카메라 바인딩.
- `verify_*.py` — 생성 코드를 신뢰하지 않고 독립 계산으로 검사.

## 4. 코드 표준과 함정

### 4.1 4.4+ 슬롯 액션 (빠뜨리면 검은 화면)
```python
def bake_fcurves(ob, frames, locs, rots):            # locs/rots: (n,3) numpy
    ob.animation_data_create(); act = bpy.data.actions.new(ob.name + '_act'); n = len(frames)
    for path, arr in (('location', locs), ('rotation_euler', rots)):
        for i in range(3):
            fc = act.fcurves.new(path, index=i); fc.keyframe_points.add(n)
            co = np.empty(2*n); co[0::2] = frames; co[1::2] = arr[:, i]
            fc.keyframe_points.foreach_set('co', co.tolist())
            fc.keyframe_points.foreach_set('interpolation', [1]*n)   # LINEAR
            fc.update()
    ob.animation_data.action = act
    ad = ob.animation_data
    if hasattr(ad, 'action_slot') and ad.action_slot is None and len(act.slots):
        ad.action_slot = act.slots[0]
```

### 4.2 카메라
- 키 `[F, [px,py,pz, tx,ty,tz, lens, fstop]]`, Catmull-Rom(끝점 접선 0). 회전은 look-at 쿼터니언 → `to_euler('XYZ', prev_euler)`로 연속화한다.
- `hull:<TRAIN>` 공간은 베이크 단계에서 월드로 변환한다(노즈 X(t) 더하기). 빌드에서 parent constraint를 쓰지 않는다(모션블러 서브프레임 일관성).
- 마지막 F+1까지 베이크해야 F900 블러가 정상이다.

### 4.3 인스턴스와 모디파이어
- 중간차는 링크 복제 인스턴스다. 프로토타입의 베벨 모디파이어는 따라가지 않으므로 `bmesh.ops.bevel`로 메시에 굽는다.
- X-Ray 클립은 셰이더에서 `Texture Coordinate(Object=XRAY_CLIP)`를 쓴다. 인스턴스 전체에 같은 평면이 적용된다.

### 4.4 텍스트·카운터
- Text 오브젝트 + frame_change 핸들러는 백그라운드 렌더에서 누락될 수 있으므로 금지한다. GN `Value to String` → `String to Curves`를 쓴다. 한글은 폰트 경로를 `look.json` 기준으로 로드한다.

### 4.5 충돌 검사 (G03)
```python
def world_bvh(ob):
    me = ob.evaluated_get(dg).to_mesh(); me.calc_loop_triangles()
    v = np.array([x.co[:] for x in me.vertices]); M = np.array(ob.matrix_world)
    w = v @ M[:3,:3].T + M[:3,3]
    return BVHTree.FromPolygons([tuple(p) for p in w], [tuple(t.vertices) for t in me.loop_triangles])
```
- 쌍: 차륜–레일, 차체–대차, 차체–인접 차체, 팬터 습판–전차선, 열차–터널, 열차–카테너리 기둥, 열차–반대 선로 열차(C1), 카메라–모든 표면(≥0.15 m).
- 5프레임 간격 전수. hide_render 오브젝트는 제외한다. 충돌 위치는 상대 오브젝트 로컬 좌표(반경, y범위)로 출력한다.
- 1 mm 이하 구름 접촉은 '설계 접촉'으로 별도 분류한다.

### 4.6 렌더 환경
- 클라우드에 Blender가 없으면 `scripts/setup_env.sh`(PyPI bpy)를 쓴다. GPU가 없으면 Cycles CPU 270p 4spp 애니매틱까지만 한다. 대표 1프레임을 먼저 측정해 900F로 환산한 시간을 REPORT에 쓴다.
- 장시간 렌더는 `setsid nohup`, 이미 있는 PNG는 건너뛰는 이어하기. 종료는 PID로 한다(`pkill -f` 금지).

## 5. 에셋 통합 절차
1. 사용자가 `assets/`에 E5 모델(구매)과 EMU-370 베이스(블루프린트)를 넣고 `assets/asset_map.json`을 채운다(템플릿: `assets/asset_map.TEMPLATE.json`).
2. `import_assets.py`는 노즈 끝을 원점(레일 상면, X+ 진행방향)에 맞추고, 실측 노즈 길이를 출력한다. config와 3% 넘게 다르면 FAIL.
3. 차륜·팬터·대차를 이름 규칙(`WHEEL_<car>_<axle>_<L|R>`, `PANTO_<car>`, `BOGIE_<car>_<F|R>`, `MOTOR_<car>_<n>`)으로 다시 붙인다.
4. **가짜 에셋 스모크 테스트**: 큐브로 된 가짜 열차로 파이프라인 전체를 돌린다. 일부러 차륜을 레일에 5 mm 박아 G03이 FAIL을 내는지 확인한다.

## 6. 알려진 한계
- EMU-370은 구매 에셋이 없다. 블루프린트 로프트 베이스는 노즈 곡면 반사 품질이 레퍼런스에 못 미친다 → 사람이 다듬는 단계가 필요하다.
- 동력차 배치와 외관 색은 공개 자료가 없다(LOCKS F-EMU-6·8). 화면에 'CG 재현 · 콘셉트 기준'을 넣어야 한다.
- C2b 터널은 설명용 축약 길이(260 m)다. 실제 미기압파는 수 km 슬래브 궤도 터널에서 커진다. 내레이션은 길이를 주장하지 않는다.
- 음성 녹음 전 컷 경계는 설계 예산이다.
