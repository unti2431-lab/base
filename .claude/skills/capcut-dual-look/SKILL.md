---
name: capcut-dual-look
description: 캡컷(CapCut)을 열지 않고 FFmpeg로 "캡컷 4K 필터 + 자동 조정(Auto Adjust)" 룩을 SDR Rec.709 MP4/MOV에 적용하고, 2초 프리뷰·4분할 비교·grade.json·QC 보고까지 내는 바삭숏(BASAK SHORTS) 색보정 스킬. 바삭숏 쇼츠, Google Flow(Veo) 생성 클립을 이어 붙인 CLEAN 영상, 캡컷 4K 룩, 자동 조정 룩, LUT 적용, 룩 일괄 적용, 색보정, 톤 통일, "캡컷 느낌으로", 프리뷰 먼저, 4분할 비교가 언급되면 사용자가 스킬 이름을 대지 않아도 반드시 사용한다. Flow 소재 검수(basak-shorts-review)와 자막 합성(basak-shorts-caption) 사이에 오는 단계이며, 자막·오버레이가 이미 얹힌 영상에는 적용 전에 반드시 확인한다.
---

# CapCut Dual Look — 4K + Auto Adjust 룩을 FFmpeg로 적용

## 이 스킬이 하는 일과 하지 않는 일

캡컷에서 뽑은 전/후 영상 두 쌍을 픽셀 단위로 비교해 **4K 필터 룩(33³ LUT)** 과 **자동 조정 룩(49³ LUT)** 을 고정 색 변환으로 근사했고, 둘을 `4K → Auto` 순서로 구운 **65³ 통합 LUT**를 FFmpeg `lut3d`로 1회 적용한다. 결과는 원본 옆에 새 MP4와 `.grade.json` 보고서로 남는다. 필요한 것은 Python 3, FFmpeg, FFprobe뿐이다.

이 값들은 **역산한 근사치**다. 아래 사실을 결과 보고에서 흐리지 않아야 사용자가 다음 판단(재촬영·재생성·수동 보정)을 올바르게 내릴 수 있다.

- 캡컷의 내부 수치나 콘텐츠마다 다르게 작동하는 AI 자동 조정 엔진을 복원한 것이 아니다. 영상마다 장면 분석·마스킹을 하지 않는 **고정 프리셋**이다.
- 통합 LUT는 두 근사 LUT를 이어 붙인 것이다. 캡컷에서 두 효과를 동시에 켠 실제 출력과 비교 검증된 적은 없다(게이트 G6 미확보). "캡컷과 동일"이라고 말하지 않는다.
- 4K LUT는 **색과 톤만** 바꾼다. 공간 선명화·AI 업스케일·네이티브 4K 출력이 아니므로 1080p 결과를 4K라고 부르지 않는다. `--sharpen mild`는 선택적 연출이지 역산값이 아니다.
- 기본 입력은 SDR Rec.709다. HDR/PQ/HLG/BT.2020/Log는 스크립트가 거부한다. 색이 엉뚱하게 뒤집히기 때문이며, 먼저 SDR로 명시 변환한 뒤 적용한다.
- 원본은 절대 수정하거나 덮어쓰지 않는다. 해상도·프레임레이트·종횡비·오디오는 그대로 유지하고 H.264 MP4로 새 파일을 만든다.
- **고채도 시안·마젠타·네온 색은 Auto 룩과 통합 룩에서 검정으로 무너진다**(LUT 조회로 실측, `MEASUREMENTS_KO.md` 5절). 피팅에 쓴 실영상에 없던 색이라 외삽되기 때문이다. 피부·금속·탁한 청록 같은 자연색은 색상 변화 ±8° 이내로 안정적이다. 네온·LED·UI 화면·형광색이 든 소재는 4분할 비교에서 그 영역을 먼저 보고, 무너지면 `--mode 4k` 단독이나 미적용을 택한다.

측정 근거와 한계의 숫자는 `references/MEASUREMENTS_KO.md`에 있다. 결과에 수치를 인용할 때는 그 파일의 값을 쓴다.

## 바삭숏 파이프라인에서의 위치

```
Flow(Veo) 클립 생성 ─▶ basak-shorts-review 검수·채택 ─▶ 컷 편집·병합 (CLEAN, 무자막, 1080×1920)
        ─▶ [이 스킬] 2초 프리뷰·4분할 비교 → QC → 전체 룩 적용
        ─▶ basak-shorts-caption 자막(R08) 합성 ─▶ 네온·2.5D 오버레이 ─▶ 최종 QC·공개
```

룩은 **자막과 오버레이를 얹기 전 CLEAN 영상**에 건다. LUT가 자막의 흰색·청록 강조색과 네온까지 과채도로 밀어 버리기 때문이다. 이미 자막이 들어간 영상을 받았다면 CLEAN 버전이 있는지 먼저 묻고, 없을 때만 그 사실을 보고에 명시하고 진행한다.

Flow/Veo 출력은 색공간 태그가 비어 있는 경우가 많다. 스크립트가 "Rec.709 태그 미확인" 경고를 내도 Flow 1080p SDR 소재라면 정상이니, 프리뷰를 눈으로 확인하는 것으로 대체한다. 클립의 24fps/30fps는 그대로 보존되므로 병합 전에 프레임레이트를 통일해 두는 편이 안전하다.

## 실행 절차

스크립트는 이 `SKILL.md`가 있는 폴더 기준 `scripts/`에 있다. 스킬 루트를 먼저 확인하고, 입력 영상 경로를 받아 아래 순서로 진행한다. 실행 환경이 없으면 "실행했다"고 쓰지 말고 명령과 예상 결과만 안내한다.

1. **전제 점검.** `ffmpeg -version`, `ffprobe -version`, `python3 --version`(Windows는 `py -3 --version`). 입력이 CLEAN인지, SDR인지, 이미 `_BSK_` 접미사가 붙은 결과물은 아닌지 확인한다.
2. **계획 확인.** `--dry-run`으로 필터 그래프·출력 경로·인코더 후보를 보여 준다. 폴더 입력이면 처리 대상 목록이 사용자 의도와 맞는지 이 단계에서 잡는다.
3. **프리뷰와 4분할 비교.** 새 소재 유형(새 Flow 프롬프트 계열, 새 조명, 실사 혼합)이면 반드시 거친다.
   ```bash
   python scripts/compare.py "/path/to/clean.mp4" --at 1.0 --video 2
   python scripts/apply.py   "/path/to/clean.mp4" --preview-seconds 2
   ```
   비교 이미지는 좌상 원본, 우상 4K, 좌하 Auto, 우하 4K→Auto 순서다. 아래 QC 체크리스트로 본다.
4. **전체 처리.** QC를 통과한 설정으로 전체 길이를 처리한다. 기본은 `--mode both --order 4k-auto --encoder auto`.
5. **출력 검증과 보고.** `.grade.json`과 ffprobe로 해상도·fps·오디오 유지 여부를 확인하고 아래 보고 형식으로 정리한다.

### 명령 모음

| 의도 | 명령 |
|---|---|
| 기본: 두 룩, 통합 LUT, NVENC 우선·CPU 폴백 | `python scripts/apply.py IN --mode both --order 4k-auto --encoder auto` |
| 두 룩을 원본 LUT 2개로 순차 적용(검증용) | `--mode both --engine chain` |
| 순서 반대(Auto → 4K) 비교 | `--mode both --order auto-4k` |
| 4K 룩만 / Auto 룩만 | `--mode 4k` / `--mode auto` |
| 앞부분 N초만 | `--preview-seconds 2` |
| 흐릿한 소스에 한해 약한 선명화 | `--sharpen mild` |
| CPU 고품질 기준본 | `--encoder cpu --quality 17` |
| 다른 폴더로 출력 | `--output-dir "/path/to/exports"` |
| 폴더 일괄(하위 폴더 포함) | `python scripts/apply.py "/folder" --recursive` |
| 4분할 비교 이미지만 | `python scripts/compare.py IN --at 1.5` |
| 4분할 비교 2초 영상 포함 | `python scripts/compare.py IN --video 2` |

Windows 비개발자는 `Run_Compare_Windows.bat` → `Run_Preview_2s_Windows.bat` → `Run_Dual_Look_Windows.bat` 순서로 영상을 끌어다 놓으면 같은 흐름이 된다. macOS/Linux는 `bash Run_Dual_Look_Mac_Linux.sh IN [옵션]`.

출력 파일명은 `원본이름_BSK_4K_AUTO.mp4`처럼 모드별 접미사가 붙고, 프리뷰는 `_PREVIEW`, 비교는 `_BSK_COMPARE_…`가 붙는다. `_BSK_`가 들어간 파일은 폴더 일괄 처리에서 자동 제외되어 이중 적용을 막는다. 기존 결과가 있으면 건너뛰며, 다시 만들려면 `--overwrite`를 붙인다(원본은 어떤 경우에도 덮지 않는다).

## QC 체크리스트 (프리뷰·4분할에서 본다)

- **원색·네온 붕괴**: 시안·마젠타·형광색 영역이 검정이나 엉뚱한 색으로 바뀌었는가. Auto·통합 룩의 알려진 외삽 한계이며, 해당 영역이 중요하면 `--mode 4k` 단독으로 바꾼다.
- **과채도**: 청록·주황 계열이 번지거나 피부·금속이 플라스틱처럼 보이는가. 두 LUT 모두 채도를 약 34% 올리므로 이미 채도가 높은 Flow 소재에서는 `--mode auto` 단독이나 미적용이 나을 수 있다.
- **블랙 클리핑**: 암부 디테일(기계 하부, 그림자 속 배관)이 뭉개지는가. Auto 룩은 암부를 더 내린다.
- **흰 엣지·하이라이트**: 금속 반사, 네온 예정 영역, 하늘이 날아가는가.
- **메탈·텍스처 디테일**: 3D 렌더의 미세 질감이 유지되는가. 렌더 단계에서 이미 샤프닝했다면 `--sharpen`은 쓰지 않는다.
- **클립 간 일관성**: 여러 Flow 클립을 병합한 영상이면 컷 경계에서 톤이 튀지 않는가. 튀면 룩 문제가 아니라 소재 톤 차이이므로 basak-shorts-review 단계로 되돌린다.
- **순서 비교**: `4k-auto`와 `auto-4k` 중 어느 쪽이 소재에 맞는지. 기본값은 설계상 선택이지 측정 결과가 아니다.

## 보고 형식

처리를 마치면 아래 틀로 보고한다. 수치는 `.grade.json`과 ffprobe에서 읽은 값만 쓴다.

```
## 룩 적용 결과
- 입력: <파일> (<가로x세로>, <fps>, <길이>s, 오디오 <코덱>)
- 출력: <파일> (<가로x세로>, <fps>, 오디오 유지/AAC 변환, 인코더 <nvenc|cpu>, 품질 <값>)
- 설정: 모드 <both|4k|auto>, 순서 <4k-auto|auto-4k>, 엔진 <fused|chain>, 선명화 <none|mild>
- LUT: <파일명과 sha256 앞 8자리>
- QC: 과채도 / 블랙 클리핑 / 흰 엣지 / 디테일 / 클립 일관성 — 각각 통과·주의·실패와 한 줄 근거
- 한계 고지: 고정 LUT 근사치, 캡컷 동시 적용본과 미검증, 네이티브 4K 아님
- 다음 단계: 자막(R08) 합성 전 CLEAN 룩본으로 사용 / 재조정 필요 항목
```

## 실패 시 진단 순서

1. FFmpeg/FFprobe/Python이 PATH에 없음 → 설치 안내. 스킬 루트나 `bin/`에 ffmpeg 실행 파일을 두면 PATH 없이도 잡는다.
2. "HDR/BT.2020/PQ/HLG 소스" 오류 → 소스 색공간 확인 후 SDR 변환. `--force-sdr`은 색 왜곡을 감수하는 경우에만.
3. NVENC 실패 → `--encoder auto`면 자동으로 CPU 전환된다. 드라이버 문제는 Windows 쪽에서 별도 확인(게이트 G5 미검증).
4. 오디오 mux 오류 → 스크립트가 AAC 재인코딩으로 자동 재시도한다. 보고에 "오디오 AAC 변환"으로 표기.
5. "기존 파일 유지(건너뜀)" → 같은 이름 결과가 이미 있다. `--overwrite` 또는 `--output-dir`.
6. 출력 해상도 불일치 오류 → 스크립트가 스스로 실패 처리한다. 소스의 회전 메타데이터나 SAR을 확인한다.

## 필요할 때 읽는 파일

- `references/MEASUREMENTS_KO.md`: 4K·Auto 룩의 측정 수치, 홀드아웃 오차, 통합 LUT 오차, 운영 가이드. 결과에 숫자를 인용하거나 한계를 설명할 때.
- `references/INSTALL_AND_EXAMPLES_KO.md`: Claude Code·claude.ai 설치 위치, Windows 드래그 앤 드롭 절차, 명령 예시, 주의사항.
- `references/HANDOFF_CCL_20261025.md`: 역분석 전 과정의 인수인계 기록, 게이트 G0~G7 상태, 다음 작업에서 금지·권장 사항, 재개용 프롬프트. 정밀도를 더 올리거나 LUT를 다시 피팅할 때.
- `assets/luts/CapCut_4K_Approx_33.cube`, `CapCut_Auto_Approx_49.cube`, `BSK_4K_then_Auto_65.cube`: 각각 4K 룩, Auto 룩, 기본 통합 룩. 다른 도구(DaVinci, Premiere)에서 같은 룩을 쓸 때 그대로 불러온다.
- `tests/test_skill.py`: `python -m unittest discover -s tests -v`. 환경을 옮겼을 때 FFmpeg 파이프라인이 살아 있는지 3초 안에 확인한다.
