# GAP28 R4 — 사용자 할 일 (우선순위 순)

| # | 할 일 | 막고 있는 작업 | 방법 |
|---|---|---|---|
| 1 | **540p 발췌본 5개 생성·업로드** | R4a-2(In/Out 1F 확정, 매치무브), R4e(전환 A·B) | 아래 명령 5줄을 촬영본 폴더에서 실행 → 드라이브 `보강작업/R4a_proxies/` 에 업로드 |
| 2 | **내레이션 녹음 + 화자(Jay Lee / Hyuk / MJS) + fps(24/30)** | 시간축 확정, 샷 길이 분산, 본렌더 | 녹음 파일(wav 48kHz)을 드라이브 `보강작업/audio/` 에. ElevenLabs 정렬 출력(단어 타임스탬프)이 있으면 함께 |
| 3 | 레퍼런스 2편 mp4 | G-RHYTHM 목표값 확정 | 드라이브 `보강작업/reference/` |
| 4 | 쇼츠 UI 실기 스크린샷(휴대폰, 세로 1080×1920 이상) | 판독 구도 UI 마스크 교체 | 드라이브 `보강작업/reference/ui_shorts.png` |
| 5 | 에셋 라이선스 답: CC0 텍스처(ambientCG·Poly Haven) 사용 가능? 운동화 에셋 구매/CC0? | R4b 신발, R4c 텍스처 | 한 줄 답이면 됨. 미답이면 절차적 텍스처 + R3 박스 신발로 진행 |
| 6 | 검증자 지정(생성자 ≠ 검증자), 드라이브 폴더를 커넥터 계정에 **편집자**로 공유 | G0, 라운드 패킷 업로드 | 공유 대상: 작업 세션에 연결된 구글 계정 |
| 7 | 최종 1080p 렌더 실행 경로 결정: (a) 직접 `RUN_ALL.ps1` 실행 / (b) 컴퓨터 사용으로 Claude 가 실행 | R5 본렌더 | 한 줄 답 |

## 1번 — 540p 발췌본 명령 (PowerShell, 촬영본 폴더에서)

```powershell
ffmpeg -y -ss 73.0 -i 20260824_152209.mp4 -t 6.0 -vf "scale=540:960:out_color_matrix=bt709,format=yuv420p" -r 30 -c:v libx264 -crf 22 -preset veryfast -c:a aac -b:a 64k -ac 1 R4a_proxies\x540_152209_L1.mp4
ffmpeg -y -ss 81.0 -i 20260824_152209.mp4 -t 6.0 -vf "scale=540:960:out_color_matrix=bt709,format=yuv420p" -r 30 -c:v libx264 -crf 22 -preset veryfast -c:a aac -b:a 64k -ac 1 R4a_proxies\x540_152209_L3.mp4
ffmpeg -y -ss 106.5 -i 20260824_152209.mp4 -t 5.0 -vf "scale=540:960:out_color_matrix=bt709,format=yuv420p" -r 30 -c:v libx264 -crf 22 -preset veryfast -c:a aac -b:a 64k -ac 1 R4a_proxies\x540_152209_L4.mp4
ffmpeg -y -ss 4.5 -i 20260824_162808.mp4 -t 5.0 -vf "scale=540:960:out_color_matrix=bt709,format=yuv420p" -r 30 -c:v libx264 -crf 22 -preset veryfast -c:a aac -b:a 64k -ac 1 R4a_proxies\x540_162808_L2.mp4
ffmpeg -y -ss 0 -i 20260824_154101.mp4 -t 7.5 -vf "scale=540:960:out_color_matrix=bt709,format=yuv420p" -r 30 -c:v libx264 -crf 22 -preset veryfast -c:a aac -b:a 64k -ac 1 R4a_proxies\x540_154101_L2alt.mp4
```

각 파일은 2–4 MB 로 10 MiB 상한 아래에 들어간다. 업로드 후 "540p 올렸음" 한 줄이면 작업 세션이 이어서 진행한다.

## 이미 결정된 것 (다시 묻지 않음)
- 162808·162328 = 성신여대입구, 열차 안 촬영 → L2 확정
- CG 발판 = 천공 강판 + 시안 끝단 띠
- 전환 B = 가림 와이프
- B10–B12 재설계안, 10cm 기준선 흰색, 인물 삭제, PSD 모델링, 문 정렬 config 이동 (R4 계획서 승인)
