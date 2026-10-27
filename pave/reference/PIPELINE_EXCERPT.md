# Blender 3D 공학 숏폼 공통 규범 — PAVE용 요약

원본: 스킬 `blender-short-3d-pipeline` v2. 스킬이 있으면 스킬이 우선한다. 여기에는 PAVE R01–R02에 필요한 조항만 옮겼다.

## 게이트
| 게이트 | 통과 조건 | 산출물 |
|---|---|---|
| G3 베이크 | 베이크 독립 검증 PASS | evidence/bake_qc.json |
| G4 씬 | 충돌 0건 또는 1 mm 이하 설계 접촉 목록 | evidence/scene_qc.json |
| G5 애니매틱 | 270p 전편: 사건 간격 ≤3초, 명사 선행 ≥6F, 카메라 규범 | review/R##/animatic_270p.mp4 |
| G6 핵심 4초 | 540p 24spp+ 정상속도 판독 PASS | review/R##/key4s_540p.mp4 |
| G7 전편 | 무음 구조 → 유음 인과, UI 마스크, 저비트레이트, 루프 | preview_540p.mp4 |
| G8 최종 | 프레임 수·fps·해상도 일치, 디코드 오류 0, 음량 | final_1080x1920.mp4 |

## 시간
`t = (F − 1) / fps`, 프레임 범위 양끝 포함. 모션블러용으로 F0과 F+1까지 베이크(t<0은 선형 외삽).

## 빌드
- bpy.ops 금지(bmesh + bpy.data). 예외: 저장·임포트.
- 애니메이션은 `common_bpy.bake_fcurves`(슬롯 명시). 빌드 직후 `motion_probe`로 MOVES 확인. 슬롯 미지정 → 카메라 원점 → 검은 화면 사고가 있었다.
- 인스턴스에는 모디파이어가 없다 → 베벨을 메시에 굽는다(30° 넘는 모서리만 sharp).
- 동일평면 접촉 금지: 지면 0.1 mm 침하, 맞닿는 부품 1–2 mm 간극.
- 난수 시드 고정, 단위 m, 스케일 1.0, frame_start = 1.
- 디버그: 의심 재질 Base Color를 순빨강으로 바꿔 한 장 찍는다.

## 검증
- 수치 PASS를 화면 PASS로 대체하지 않는다. 핵심 4초는 인코딩된 MP4를 정상속도로 본다.
- 씬 충돌: `common_bpy.world_bvh`로 월드 좌표 BVH, 5F 간격 전수. 원인 위치는 상대 오브젝트 로컬 좌표로 출력.
- 저비트레이트: `ffmpeg -i preview.mp4 -c:v libx264 -b:v 2M -maxrate 2M -bufsize 4M -an stress.mp4`
- 루프: 첫·끝 프레임 SSIM 기록.
  `ffmpeg -i first.png -i last.png -lavfi ssim -f null - 2>&1 | grep -o "All:[0-9.]*"`

## 룩
- AgX + `AgX - Medium High Contrast`, 디노이저 OIDN/OptiX, 렌더 디더 유지.
- 3D 씬에 먼지·연기·발광 화살표·입자 금지. 2.5D 강조는 후합성 레이어. 글자는 자막 레이어만.
- 움직이는 고주파 텍스처는 인코딩 후 깜빡인다 → 저비트레이트본으로 확인.

## 렌더
| 단계 | 해상도/샘플 |
|---|---|
| 애니매틱 | 270p, 3–6spp, 모션블러 켬 |
| 대표 스틸 | 540p, 12–24spp |
| 핵심 4초 | 540p, 24spp+ |
| 최종 | 1080p, 로컬 GPU(RTX 3060 Ti 8GB), OptiX, 적응 샘플링, 최대 256spp, 10–24F 청크·이어하기·실패 청크 2회 재시도 |

- 클라우드는 GPU가 없다: Cycles CPU 저해상도만. 렌더 시간은 대표 프레임 1장 실측 → 환산.
- 원격 셸은 사용자 PC 안 Linux VM이라 Windows blender.exe를 못 돌린다 → 사용자가 PowerShell 실행 또는 컴퓨터 사용.
- 프레임별 `render_log.csv`(frame, sec, peak_vram, retries).

## 납품 인코딩 (색 행렬 명시 — BT.601 함정)
```bash
ffmpeg -framerate <FPS> -i frames/%04d.png -i mix.wav \
  -vf "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p" \
  -c:v libx264 -profile:v high -crf 16 -preset slow \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 \
  -c:a aac -b:a 320k -ar 48000 -shortest -movflags +faststart final_1080x1920.mp4
```
음량: 통합 −14 LUFS 근처, 트루피크 −1 dBTP 이하.

## 라운드 운영
- 한 라운드에 변수 하나. review/R##/CHANGELOG.md에 바꾼 변수와 이유.
- 같은 결함이 국소 수정 2회 뒤에도 남으면 재설계 보고.
- 파일 거점: 드라이브 = 교환·보관(R## 폴더 + MANIFEST sha256, 덮어쓰기 금지), 로컬 = 베이크·.blend·PNG(PNG 시퀀스는 동기화 폴더 금지).
