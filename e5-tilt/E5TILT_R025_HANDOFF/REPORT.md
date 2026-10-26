# REPORT

기록 양식 (라운드마다 아래에 추가): 작업ID / 변경파일 / 명령 / 게이트값 / 산출물 / 질문

---

## R025 — Claude (클라우드 CPU, 2026-10-26)

**결론**: 실차 기반 리그·카메라·프록시 씬·게이트 체계를 만들고 270p 전편 애니매틱까지 돌렸다. 리그·충돌·루프·컷 정렬은 기준을 통과했고, **동작량(평균 5.10, 목표 9)과 명사 선행 노출(단어 타임스탬프 없음)은 아직 기준에 못 미친다.**

| 항목 | 상태 | 근거 |
|---|---|---|
| G1 레퍼런스 측정 | PASS | reference/REFERENCE_NOTES.md |
| G2 음성 컷 정렬 | PASS (8개 컷 모두 무음 구간 안) | evidence/sync_qc.json `cuts_on_vo_gaps` |
| G2 단어 타임스탬프 / 명사 선행 | NOT_DECIDABLE | huggingface 차단(403)으로 whisper 모델 다운로드 불가 |
| G3 베이크 | PASS 20/20 (무미끄럼 3.7e-7, 롤 1.500°, Δh = s·sinθ 오차 2e-16 m, W0 위치차 3e-11 m) | evidence/bake_qc.json |
| G4 씬 | PASS (161프레임, 충돌 0, 카메라 최소 0.189 m) | evidence/scene_qc.json |
| 게이트 자가시험 | PASS 5/5 (카메라 튐·롤 초과·밸브 침하·가짜 에셋 충돌을 모두 FAIL로 검출) | evidence/gate_selftest.json |
| 재현성 | PASS (깨끗한 폴더 재실행, bake sha256·사건·씬 결과 동일) | evidence/repro_qc.json |
| G5 하드컷 수 | PASS (검출 6, 설계 8) | sync_qc |
| G5 루프 | PASS (첫·끝 프레임 SSIM 0.965, R024 0.862) | review/R025/loop_ssim.json |
| G5 동작량 | **FAIL** — 평균 5.10 (R024 3.5, 레퍼런스 12.1), 최저 초 0.97 | sync_qc `motion_per_s` |
| G6 핵심 4초 540p | NOT_PERFORMED (GPU 필요) | TASKS T08 |
| G7·G8 | NOT_PERFORMED | — |

### 작업 기록
- **작업ID**: R025-setup → R025a(전편 애니매틱) → R025b(카메라 키만 변경)
- **변경파일**: 패키지 전체 신규. R025b는 `src/cameras.json`만(C04·C05·C06·C07 키).
- **명령**: `scripts/run_pipeline.sh verify`, `render_frames.py -- --stage animatic`, `comp_overlays.py`, `scripts/encode.sh`, `sync_qc.py --video`, `scripts/make_review.sh`
- **게이트값**: 위 표
- **산출물**: `review/R025/e5tilt_R025_animatic_270p.mp4`(R024 원음 합본, sha256 `d1a6454e…87ae4`), `contact_270p.jpg`, `stress_2M.mp4`, 540p 오버레이 스틸 4장, `round_a/`(R025a 보관)

### R025에서 내린 판단
1. 컷 경계를 현 음성의 무음 구간 11개에 맞췄다. 마지막 두 컷은 문장 중간을 잘라 하나의 크레인 샷으로 합쳤다.
2. 1.5°를 과장하지 않았다. 대신 고스트 트윈(기울지 않은 차체 윤곽), 전방 축선, 앰버 쐐기 오버레이를 썼다. 270p에서는 여전히 약하다(T04).
3. 경사 시작을 곡선 진입 뒤 1.2 s 늦췄다(연출값). 경사 동작의 75 %가 C05 안에 들어온다. 내레이션은 지연을 암시하지 않는다.
4. 7번 내레이션을 "쏠림을 거의 느끼지 않습니다"에서 "쏠림은 그만큼 줄어듭니다"로 바꿨다. 1.5° 경사가 쏠림을 없애지는 않기 때문이다.
5. 카메라만 바꾼 R025b는 동작량을 4.86 → 5.10으로만 올렸다. 같은 처방을 반복하지 않도록 T02에 원인과 순서를 적었다.

### 질문 / 사용자 블로커
- **G-1 음성**: 현 R024 원음을 유지할지(잠정 LOCK), BEATS의 9문장 제안으로 재녹음할지.
- **G-2 레퍼런스 사진**: E5 대차, 공기스프링·보조 공기실·높이조절밸브 배치.
- **G-3 에셋**: E5 차체 모델 구매·라이선스.
- **G-4 사실**: 1.5°·R4000 320 km/h를 JR동일본 Tech 31 PDF로 확인.

---

## R026 — (Codex) 
작업ID:
변경파일:
명령:
게이트값:
산출물:
질문:
