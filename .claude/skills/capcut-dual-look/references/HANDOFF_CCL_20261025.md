---
document_type: CCL_context_continuity_log
project: BSK-CAPCUT-DUAL-LOOK
as_of: 2026-10-25
revision: 1.0
status: completed_with_known_limitations
language: ko
owner_workflow: 바삭숏 공학 3D 숏폼 / Claude Code / FFmpeg
primary_deliverable: Claude_Skill_CapCut_4K_AutoAdjust_v1.0.zip
---

# CCL — 캡컷 4K 필터 + 자동 조정 역분석 및 Claude 스킬 전체 인수인계

**기준일:** 2026-10-25 (KST) · **프로젝트:** BSK-CAPCUT-DUAL-LOOK · **상태:** 두 단독 효과 역분석, 통합 LUT 합성, Claude Code 스킬 제작, 제한적 실영상 인코딩 테스트 완료

## 0. 한 문장 결론

캡컷에서 추출한 전/후 영상 2쌍을 픽셀 단위로 비교해 4K 룩(33³ LUT)과 Auto Adjust 룩(49³ LUT)을 고정 색상 변환으로 근사했고, 이를 `4K → Auto` 순서의 65³ 통합 LUT와 Claude Code용 FFmpeg 스킬로 만들어 **캡컷을 열지 않고 MP4에 적용하는 작업 흐름**을 구축했다. **캡컷의 실제 내부 수치나 콘텐츠별로 새로 작동하는 AI 자동 조정 엔진을 복원한 것은 아니다.**

## 1. 작업별 진행 요약과 핵심 수치

| 단계 | 입력 쌍 / 범위 | 확정 측정 결과 | 산출물 / 상태 |
|---|---|---|---|
| A. 4K 필터 | `no filter.mp4` ↔ `yes filter.mp4`, 각각 1080×1920·30fps·434F·14.489초·Rec.709. 35개 대응 프레임 약 35만 픽셀 비교 | 평균 휘도 -6.0%(상대), HSV 채도 +34.7%, P90–P10 밝기 폭 +1.3%, 윤곽선 신호 RMS 약 +24%(색·대비 영향 포함) | `CapCut_4K_Filter_Approx_Rec709_33.cube` 및 보고서·그래프 생성 완료 |
| B. 자동 조정 | `before.mp4` ↔ `after.mp4`, 같은 영상 규격. 74개 프레임 약 960만 표본 픽셀 | 평균 휘도 +2.01%(상대), HSV 채도 +33.88%, P90–P10 명암 폭 +17.67%. 단순 밝기 증가가 아닌 S형 톤커브 | `CapCut_Auto_Adjust_Fixed_49.cube`, 보고서·그래프·샘플 생성 완료 |
| C. 자동 조정 재현 검증 | 학습에 미사용한 15개 프레임 × 5,000픽셀 | 평균 RGB MAE 13.432/255(원본) → 3.394/255(49³ LUT) | 단독 자동 조정 LUT의 **동일 영상 재현** 시험 통과 |
| D. 통합 LUT | 4K 33³ 컬러 LUT → Auto 49³ 컬러 LUT, tetrahedral 보간 후 65³로 굽기 | 무작위 RGB 약 10만 점에서 2단 LUT 체인 대비 평균 채널 오차 약 0.000175 (0–1 스케일) | `BSK_4K_then_Auto_65.cube`를 Claude 스킬 ZIP에 포함 |
| E. FFmpeg 실영상 처리 | 통합 LUT와 두 LUT를 순차 적용한 테스트 출력 비교 | 두 방식 간 평균 RGB 차이 0.61/255. 원본 해상도·30fps·BT.709 태그·오디오 보존 확인 | 실행 스크립트/테스트/샘플 포함, 기본 파이프라인 동작 확인 |

**측정 해석 주의:** 각 수치는 서로 다른 실험의 차이를 나타낸다. `4K와 Auto 효과를 합한 수치`로 단순 산술 합산하면 안 된다. 통합 LUT 오차는 *두 근사 LUT 사이의 일치도*이지 *캡컷에서 두 필터를 실제로 동시에 적용한 결과와의 오차*가 아니다.

## 2. 4K 필터 상세 진단

- 적용본은 원본보다 평균적으로 **어둡고 채도가 높은 경향**. 0.4~0.6 밝기 영역은 약 0.055~0.058 절대 단위만큼 감소.
- 윤곽선 지표 +24%에는 국소 명암·채도 변화와 H.264 재인코딩 영향도 있으므로 실제 샤프닝 수치로 환산 불가.
- 캡컷 조정 슬라이더를 수동으로 흉내 낼 경우의 **근사 출발점**: 밝기 -5, 노출 0, 대비 +5, 채도 +30, 하이라이트 -3, 그림자 -8, 선명도 +12, 색온도/색조 0. 공식 내부 파라미터가 아님.
- 배포 33³ LUT는 **색상과 비선형 톤 변환만** 포함한다. 공간 선명화나 AI 업스케일링, 네이티브 4K 출력이 아니다.
- 필터의 원래 강도(%)가 제공되지 않았으므로 **이 샘플에서 적용된 강도 기준의 근사**이다.

## 3. 자동 조정 상세 진단

- 암부는 더 어둡게, 중간톤~명부는 밝아지는 **S커브와 채도 상승**이 핵심. 예시 톤 구간(밝기 구간→적용 후 평균 변화): 10–20% -6.4%p, 20–30% -5.0%p, 40–50% +3.2%p, 60–70% +6.2%p.
- 실제 별도 검증 프레임에서 원본 대비 픽셀 재현 오차를 **약 74.7% 감소**시켰다. 이는 원본 영상 데이터 분포에 대한 근사 성능이다.
- 마지막 430~433프레임(14.333초 이후)은 원본/적용본이 거의 같아지는 **예외 구간**. 편집 범위/미적용 가능성이 있으며 LUT의 보편 규칙으로 학습하지 않음.
- 색상 보정 후 공간 샤프닝의 추가 이득은 일관적이지 않아 기본 Auto LUT에는 별도 선명화·노이즈 제거 없음.
- Auto LUT는 영상마다 자동 분석·국소 마스킹·피부/물체 판별·복원 등을 수행하지 않는 **고정 스타일 프리셋**이다.

## 4. 결합 처리 규칙 (LOCK)

1. 기본 입력은 **CLEAN / 무자막 / 오버레이 이전의 SDR Rec.709 영상**.
2. 기본 처리 순서는 **4K → Auto Adjust**; 두 LUT를 합친 `BSK_4K_then_Auto_65.cube`를 `lut3d`로 1회 적용.
3. 4K만 적용 또는 Auto만 적용 가능. 반대 순서 `Auto → 4K`는 두 LUT를 순차 적용하는 별도 모드.
4. 샤프닝은 **기본 끔**. 자산이 흐릿할 때만 `--sharpen mild` 사용; 이것은 선택적 연출이며 캡컷 효과 역산값이 아니다.
5. 원본 해상도, 프레임레이트, 종횡비와 오디오를 유지하고 출력은 H.264 MP4로 새 파일 생성. 원본 변경 금지.
6. HDR/PQ/HLG/BT.2020/Log 소스는 직접 적용 금지. Rec.709 SDR 확인 및 명시적 변환 후 처리.
7. 자막·네온 2.5D 오버레이는 **색보정 뒤 후합성**. 자막과 효과까지 과채도 처리하지 않음.
8. 새로운 촬영·렌더 스타일에는 **2초 프리뷰 → QC → 전체 처리** 게이트.

## 5. Claude Code 스킬 — 설치, 명령, 내용

**주요 파일:** `Claude_Skill_CapCut_4K_AutoAdjust_v1.0.zip` (압축 안의 최상위 폴더는 `capcut-dual-look`).

**설치:** ZIP 압축을 풀어 `capcut-dual-look/SKILL.md`가 Windows에서는 `%USERPROFILE%\\.claude\\skills\\capcut-dual-look\\SKILL.md`, macOS/Linux에서는 `~/.claude/skills/capcut-dual-look/SKILL.md`에 있도록 배치한다.

**필요:** Python 3.9+, FFmpeg 5+, FFprobe. NVIDIA GPU NVENC는 선택 사항(미지원 시 CPU fallback).

**Claude 호출 예시:** `/capcut-dual-look` 후 "이 MP4에 4K+자동 조정을 2초 프리뷰부터 적용. 프레임레이트·오디오 유지".

**CLI (스킬 폴더 기준):**

```bash
python scripts/apply.py "/path/to/input.mp4" --mode both --order 4k-auto --encoder auto --preview-seconds 2
python scripts/apply.py "/path/to/input.mp4" --mode both --order 4k-auto --encoder auto
python scripts/apply.py "/path/to/input.mp4" --mode 4k
python scripts/apply.py "/path/to/input.mp4" --mode auto
python scripts/apply.py "/path/to/input.mp4" --mode both --order auto-4k
python scripts/apply.py "/path/to/input.mp4" --encoder cpu --quality 17
python scripts/apply.py "/path/to/input.mp4" --dry-run
```

**Windows 비개발자 사용:** `Run_Preview_2s_Windows.bat`에 영상 드래그 → 프리뷰 검사 → `Run_Dual_Look_Windows.bat`에 영상(복수 가능)을 드래그. 같은 폴더의 `scripts/`, `assets/`를 유지해야 한다.

**스킬 내부 구조:**

```text
capcut-dual-look/
├── SKILL.md
├── Run_Dual_Look_Windows.bat
├── Run_Preview_2s_Windows.bat
├── Run_Dual_Look_Mac_Linux.sh
├── scripts/apply.py
├── assets/luts/
│   ├── CapCut_4K_Approx_33.cube
│   ├── CapCut_Auto_Approx_49.cube
│   └── BSK_4K_then_Auto_65.cube
├── references/INSTALL_AND_EXAMPLES_KO.md
├── references/MEASUREMENTS_KO.md
└── tests/test_skill.py
```

**실행 조건:** 루트 경로와 실행 파일 이름은 스킬 내부 기준. 내보내기 시 `.grade.json` 메타데이터 로그 기록. 오디오는 MP4 호환 코덱이면 복사, 아니면 AAC 변환. 기본 출력에서 자막/데이터 스트림은 제외될 수 있음.

## 6. 산출물 전체 인덱스

### 현재 인수인계 패키지에 포함된 파일
- `Claude_Skill_CapCut_4K_AutoAdjust_v1.0.zip`: Claude에서 직접 사용하는 최종 스킬; **1순위 필수 파일**.
- `CapCut_4K_Reverse_Analysis_20261025.md` + `CapCut_4K_Filter_Approx_Rec709_33.cube`: 4K 측정 보고서와 33³ LUT.
- `AUTO_ADJUST_ANALYSIS_KO.md` + `CapCut_Auto_Adjust_Fixed_49.cube`: 자동 조정 분석 보고서와 49³ LUT.
- `CapCut_AutoAdjust_ReverseEngineered_FFmpeg_Kit.zip`: Auto 단돀 재현 도구의 기존 패키지.
- `4k_filter_comparison.jpg`, `filter_metric_charts.png`, `frame_filter_metrics.csv`: 4K 전후 비교·프레임 데이터.
- `auto_adjust_3way_comparison.jpg`, `auto_adjust_measurement_charts.png`, `auto_adjust_luma_curve.csv`, `auto_adjust_frame_metrics.csv`: Auto 비교·측정 데이터.
- `AutoAdjust_Recreation_SAMPLE_4sec_1080.mp4`, `before_BSK_4K_AUTO_PREVIEW.mp4`, `DUAL_LOOK_COMPARE.jpg`: 검증 결과 샘플.
- `BSK_CAPCUT_CCL_SUMMARY_20261025.md`: 이 CCL 인수인계 문서.

### 원본 영상(마스터 ZIP에는 용량 중복 방지를 위해 제외)
- 4K 분석 소스: `no filter.mp4`, `yes filter.mp4`.
- Auto 분석 소스: `before.mp4`, `after.mp4`.
- 이 4개는 **과거 채팅 첨부 원본**에 보존된 자료다. ZIP에 없으므로 다른 환경에서 추가 역분석을 하려면 원본 4개를 별도 받아야 한다.

## 7. 검증 상태 (게이트 기록)

| 게이트 | 상태 | 근거 / 미확인 부분 |
|---|---|---|
| G0 원본 두 쌍 동영상 정합 | PASS | 각 쌍 1080×1920 / 30fps / 434프레임 |
| G1 4K 정량 측정 | PASS | 프레임·픽셀 기반 분석 및 추정 LUT |
| G2 Auto 정량 측정·홀드아웃 | PASS | 별도 프레임 75,000픽셀에서 RGB MAE 3.394/255 |
| G3 합성 65³ LUT 생성 | PASS | 2-LUT 순차 적용과 RGB 차이 실험 |
| G4 FFmpeg 인코딩 테스트 | PASS (샘플 범위) | 0.61/255(합성 대 체인), 영상 규격·오디오 점검 |
| G5 Windows 사용자 PC 실사용 | NOT VERIFIED HERE | Windows BAT, CUDA 드라이버 및 NVENC 실제 환경 별도 시험 필요 |
| G6 실제 캡컷 4K+Auto 동시 적용본 정답 비교 | NOT AVAILABLE | 두 효과가 동시에 걸린 레퍼런스 영상이 미제공 상태 |
| G7 임의 신규 소재에서 동적 AI Auto와 동등성 | NOT CLAIMED | 고정 LUT의 한계상 불가 |

## 8. 다음 작업에서 해서는 안 되는 것 / 해야 하는 것

**금지:** 이 LUT를 캡컷 공식 수치 또는 원본 AI 엔진으로 설명, 신규 영상에서 동일 오차 보장, 필터 이름만으로 네이티브 4K 주장, 4K 룩에 기본 강한 샤프닝 추가, 모르는 HDR 소스에 바로 적용, 원본 덮어쓰기.

**권장:** ① 다른 소재 영상(예: 다큐 톤 3D 기계숏폼)에 2초 프리뷰 → ② 원본/4K/Auto/결합 4분할 평가 → ③ 과채도·블랙 클리핑·하얀 엣지·메탈 디테일 손실 점검 → ④ 최종 선택 룩 고정 → ⑤ 1080×1920 24/30fps H.264 내보내기 → ⑥ 자막·네온 합성 → ⑦ 오디오/화질 QC.

**정밀도 보강이 필요하다면:** 동일 CLEAN 원본에 캡컷에서 **4K와 Auto를 실제로 동시에 적용한 참조 영상을 추가 확보**하여 `combined`의 직접 정확도를 검증한다. 이 때 필터 강도와 순서, export 설정을 같이 기록.

---

## 9. CCL 재개용 초단기 프롬프트

> 프로젝트 `BSK-CAPCUT-DUAL-LOOK`을 이어서 진행한다. 기준 문서는 `BSK_CAPCUT_CCL_SUMMARY_20261025.md`, 실행 자산은 `Claude_Skill_CapCut_4K_AutoAdjust_v1.0.zip`이다. 4K 33³, Auto 49³, 기본 4K→Auto 합성 65³ LUT를 FFmpeg로 적용하라. 모든 값은 캡컷 효과를 **고정 LUT로 역산한 근사치**이며, 공식 내부 설정 및 AI 동적 자동 조정과 동일하지 않다. 2초 프리뷰부터 검사하고 원본·FPS·해상도·오디오를 유지하며 HDR은 거부하라. 별도 추가 승인이 없으면 샤프닝은 끄고, 자막/네온 오버레이 전에 CLEAN 영상에 적용하라. 결과는 MP4 + grade.json + QC 요약으로 보고하라.
