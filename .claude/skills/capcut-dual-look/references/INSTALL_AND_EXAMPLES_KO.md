# 설치 · 실행 · 검수 안내

## Claude Code 설치

**개인 모든 프로젝트:** 압축 해제한 `capcut-dual-look` 폴더를 다음에 넣습니다.

- Windows: `%USERPROFILE%\.claude\skills\capcut-dual-look\SKILL.md`
- macOS/Linux: `~/.claude/skills/capcut-dual-look/SKILL.md`

**특정 프로젝트 전용:** `<프로젝트 경로>/.claude/skills/capcut-dual-look/SKILL.md`

Claude Code에서 `/capcut-dual-look`로 호출하거나 "이 영상에 4K+자동 조정 적용해"처럼 요청합니다.

## Claude.ai 업로드

Custom Skills를 지원하는 환경에서는 설정의 스킬 관리 화면에서 **이 폴더를 압축한 ZIP**을 업로드합니다. 스킬이 실행 환경에 접근할 수 있어야 MP4를 실제로 변환할 수 있으며, FFmpeg/FFprobe가 없는 클라우드 환경에서는 자동 적용을 보장하지 않습니다.

## 요구사항

- Python 3.9 이상(추가 pip 라이브러리 없음)
- FFmpeg 5+ 및 FFprobe (`ffmpeg -version`, `ffprobe -version`으로 확인)
- 선택: NVIDIA GPU/드라이버와 FFmpeg NVENC 지원. 미지원 시 `--encoder auto`가 CPU로 전환
- 가용 저장공간: 출력 MP4 크기 이상의 여유 공간

## Windows — 편집툴 없이 바로 변환

1. FFmpeg와 Python 3 설치(명령 프롬프트에서 `ffmpeg -version`, `py -3 --version` 확인).
2. 영상을 `Run_Compare_Windows.bat` 위에 끌어다 놓아 `_BSK_COMPARE_1s.jpg`(4분할 비교 이미지)와 `_BSK_COMPARE_2s.mp4`(2초 비교 영상) 생성. 좌상 원본, 우상 4K, 좌하 Auto, 우하 4K→Auto.
3. 영상을 `Run_Preview_2s_Windows.bat` 위에 끌어다 놓아 `_PREVIEW.mp4` 생성.
4. 프리뷰 확인 후 `Run_Dual_Look_Windows.bat` 위에 영상(복수 가능)을 끌어다 놓아 `_BSK_4K_AUTO.mp4` 생성.
5. 결과 MP4 옆 `_BSK_4K_AUTO.grade.json`에서 사용한 LUT 및 인코더 확인.

> 드래그 앤 드롭은 해당 `.bat`와 `scripts` / `assets`를 포함한 전체 스킬 폴더를 유지해야 동작합니다. 입력 파일명을 바꾸거나 원본을 편집하지 않습니다.

## 명령줄 추가 예시

```bash
# 4분할 비교(원본 | 4K / Auto | 4K→Auto) 이미지와 2초 비교 영상
python scripts/compare.py "D:/Videos/BRK_R3.mp4" --at 1.0 --video 2

# 결합 룩, 빠른 검수
python scripts/apply.py "D:/Videos/BRK_R3.mp4" --preview-seconds 2

# 전체 폴더 변환, 하위 폴더는 제외
python scripts/apply.py "D:/Render/approved" --output-dir "D:/Final/graded"

# 4K / Auto 조정 각각 따로 비교
python scripts/apply.py "D:/Render/test.mp4" --mode 4k
python scripts/apply.py "D:/Render/test.mp4" --mode auto

# 순서를 거꾸로 적용
python scripts/apply.py "D:/Render/test.mp4" --order auto-4k

# 디테일이 부족한 소스에 한해서 약한 선명화
python scripts/apply.py "D:/Render/test.mp4" --sharpen mild

# CPU 고품질: NVENC가 없는 컴퓨터도 작동
python scripts/apply.py "D:/Render/test.mp4" --encoder cpu --quality 17

# FFmpeg 실행은 하지 않고 처리 계획만 확인
python scripts/apply.py "D:/Render/test.mp4" --dry-run
```

## 주의사항

- 출력 포맷은 항상 SDR H.264 MP4. 원본 프레임레이트와 해상도는 기본 유지하고 `-r` 또는 `scale`로 강제 변경하지 않습니다.
- H.264 압축으로 재인코딩하기 때문에 무손실은 아닙니다. 소리의 코덱이 MP4 컨테이너에 맞으면 copy, 호환성이 없을 때만 AAC로 변환합니다.
- 여러 오디오 스트림은 복사하지만 자막 및 데이터 스트림은 기본 출력에서 제외합니다.
- 영상의 자동 조정은 **이번 샘플 영상에서 학습한 고정 컬러 변환**으로, 모든 신규 소스를 분석해 최적화하는 동적 엔진이 아닙니다.
- 네온 2.5D 합성이나 자막까지 LUT 적용하면 채도가 커질 수 있으므로, 가능하면 CLEAN 영상에 룩을 적용하고 자막/오버레이는 그 뒤에 합성하세요.
- Google Flow(Veo) 출력은 색공간 태그가 비어 있는 경우가 많아 "Rec.709 태그 미확인" 경고가 뜹니다. 1080p SDR 소재라면 정상이며, 4분할 비교와 프리뷰로 눈 검수를 대신합니다.
- `compare.py`의 라벨은 FFmpeg `drawtext`(libfreetype)와 시스템 글꼴이 필요합니다. 글꼴이 없으면 자동으로 라벨 없이 생성되며, 패널 순서는 항상 좌상 원본·우상 4K·좌하 Auto·우하 4K→Auto입니다.
- 테스트: 스킬 폴더에서 `python -m unittest discover -s tests -v` (FFmpeg 필요, 약 5초).
