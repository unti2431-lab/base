<#
DEL74 RUN_ALL.ps1 — Windows 로컬 GPU(RTX 3060 Ti) 실행 경로. PowerShell 5.1+.
사용:
  .\RUN_ALL.ps1 -VerifyOnly            # bake→verify_bake→(build)→verify_scene 만
  .\RUN_ALL.ps1 -Rebake                # 베이크부터 다시
  .\RUN_ALL.ps1 -AssetMap              # import_assets.py 로 에셋 통합본 생성 후 검증
  .\RUN_ALL.ps1 -Stills "1,318,894"    # 540p 대표 스틸
  .\RUN_ALL.ps1 -Key4s                 # 핵심 4초 F375–552 540p 24spp → MP4
  .\RUN_ALL.ps1 -Final                 # 1080p 전편 청크 렌더(이어하기) → 후합성 → 인코딩 → ffprobe + sha256
  .\RUN_ALL.ps1 -Final -Chunk 12 -Spp 256
전제: $Blender 경로, venv(python 3.11 + numpy + pillow + OpenEXR), ffmpeg PATH. 파일 거점: C:\Users\lek\Documents\claude blender\DEL74
#>
param(
  [switch]$VerifyOnly, [switch]$Rebake, [switch]$AssetMap, [string]$Stills = "", [switch]$Key4s, [switch]$Final,
  [int]$Chunk = 12, [int]$Spp = 256, [int]$Start = 1, [int]$End = 1416, [string]$Device = "OPTIX",
  [string]$Blender = "C:\Program Files\Blender Foundation\Blender 4.5\blender.exe",
  [string]$Py = ".\venv\Scripts\python.exe"
)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
function Step($msg) { Write-Host ("`n=== {0} ===" -f $msg) -ForegroundColor Cyan }
function Fail($msg) { Write-Host ("FAIL: {0}" -f $msg) -ForegroundColor Red; exit 1 }

# 0. 버전 가드
Step "Blender version guard"
$ver = & $Blender -b --version | Select-String "Blender 4\.5"
if (-not $ver) { Fail "Blender 4.5 LTS 아님: $Blender" }
$ffm = Get-Command ffmpeg -ErrorAction SilentlyContinue; if (-not $ffm) { Fail "ffmpeg 없음(PATH)" }

# 1. 베이크 + 독립 검증 (게이트 G3)
if ($Rebake -or -not (Test-Path "src\del74_bake.npz")) {
  Step "bake"; & $Py "src\bake.py" | Out-Null
}
Step "verify_bake (G3)"
& $Py "src\verify_bake.py"; if ($LASTEXITCODE -ne 0) { Fail "verify_bake FAIL — evidence\bake_qc.json 확인" }

# 2. 씬 빌드
$Scene = "render\del74_scene.blend"
if ($Rebake -or -not (Test-Path $Scene)) {
  Step "build_scene"; & $Blender -b -P "src\build_scene.py" -- --out $Scene; if ($LASTEXITCODE -ne 0) { Fail "build_scene" }
}
if ($AssetMap) {
  Step "import_assets"; & $Blender -b $Scene -P "src\import_assets.py" -- --map "assets\asset_map.json" --out "render\del74_scene_assets.blend"; if ($LASTEXITCODE -ne 0) { Fail "import_assets" }
  $Scene = "render\del74_scene_assets.blend"
}
# 3. 씬 충돌 검사 (G4)
Step "verify_scene (G4)"
& $Blender -b $Scene -P "src\verify_scene.py" -- --step 5; if ($LASTEXITCODE -ne 0) { Fail "verify_scene FAIL — evidence\scene_qc.json 확인(설계 접촉은 목록 검토)" }
if ($VerifyOnly) { Write-Host "VerifyOnly 완료" -ForegroundColor Green; exit 0 }

# 4. 스틸 / 핵심 4초
if ($Stills -ne "") {
  Step "stills 540p"; & $Blender -b -P "src\render_still.py" -- --blend $Scene --frames $Stills --pct 50 --spp 24 --device $Device --out "review\R02\stills_540p" --passes 1
}
if ($Key4s) {
  Step "key 4s F375-552 540p 24spp"
  $frames = (375..552) -join ","
  & $Blender -b -P "src\render_still.py" -- --blend $Scene --frames $frames --pct 50 --spp 24 --device $Device --out "render\key4s" --passes 1
  & $Py "src\post_comp.py" --frames 375-552 --root "render" 
  ffmpeg -y -framerate 30 -start_number 375 -i "render\comp\%04d.png" -vf "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p" -c:v libx264 -crf 16 -preset slow -colorspace bt709 -color_primaries bt709 -color_trc bt709 "review\R02\key4s_540p.mp4"
}

# 5. 최종 1080p 청크 렌더(이어하기, 실패 청크 재시도 2회, 프레임 로그)
if ($Final) {
  Step "final 1080p chunks $Chunk spp $Spp device $Device"
  New-Item -ItemType Directory -Force "render\passes","render\passes_exr","render\comp","evidence" | Out-Null
  $log = "render\render_log.csv"; if (-not (Test-Path $log)) { "frame,sec,peak_vram_mb,retries" | Out-File $log -Encoding ascii }
  $failed = @()
  for ($f = $Start; $f -le $End; $f += $Chunk) {
    $to = [Math]::Min($f + $Chunk - 1, $End)
    $todo = @(); for ($k = $f; $k -le $to; $k++) { if (-not (Test-Path ("render\passes\combined{0:d4}.png" -f $k))) { $todo += $k } }
    if ($todo.Count -eq 0) { continue }
    $ok = $false
    for ($try = 0; $try -le 2 -and -not $ok; $try++) {
      $t0 = Get-Date
      $vram = Start-Job { param($d) while ($true) { (nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits) | Out-File -Append $d; Start-Sleep 1 } } -ArgumentList ("$Root\render\vram_tmp.txt")
      & $Blender -b $Scene -P "src\render_still.py" -- --blend $Scene --frames ($todo -join ",") --pct 100 --spp $Spp --device $Device --out "render\final_tmp" --passes 1
      Stop-Job $vram; Remove-Job $vram
      $peak = 0; if (Test-Path "render\vram_tmp.txt") { $peak = (Get-Content "render\vram_tmp.txt" | ForEach-Object { [int]$_ } | Measure-Object -Maximum).Maximum; Remove-Item "render\vram_tmp.txt" }
      $ok = ($LASTEXITCODE -eq 0)
      $sec = ((Get-Date) - $t0).TotalSeconds / [Math]::Max($todo.Count, 1)
      foreach ($k in $todo) { "{0},{1:n1},{2},{3}" -f $k, $sec, $peak, $try | Out-File $log -Append -Encoding ascii }
    }
    if (-not $ok) { $failed += $todo }
  }
  if ($failed.Count -gt 0) { Write-Host ("실패 프레임: {0}" -f ($failed -join ",")) -ForegroundColor Red }
  Step "post_comp"; & $Py "src\post_comp.py" --frames "$Start-$End" --root "render"
  Step "encode (bt709 행렬 명시)"
  $vo = "audio\DEL74_VO_R2_Hyuk.mp3"; $mix = if (Test-Path "audio\mix.wav") { "audio\mix.wav" } else { $vo }
  ffmpeg -y -framerate 30 -i "render\comp\%04d.png" -i $mix -vf "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p" -c:v libx264 -profile:v high -crf 16 -preset slow -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a aac -b:a 320k -ar 48000 -shortest -movflags +faststart "review\final_1080x1920.mp4"
  Step "delivery_qc"
  $probe = ffprobe -v error -count_frames -show_entries stream=width,height,r_frame_rate,nb_read_frames -of csv=p=0 "review\final_1080x1920.mp4"
  ffmpeg -v error -i "review\final_1080x1920.mp4" -f null - 2> "evidence\decode_errors.txt"
  $sha = (Get-FileHash "review\final_1080x1920.mp4" -Algorithm SHA256).Hash
  $qc = @{ probe = $probe; sha256 = $sha; decode_errors = (Get-Content "evidence\decode_errors.txt" | Measure-Object -Line).Lines; failed_frames = $failed; spp = $Spp; chunk = $Chunk }
  $qc | ConvertTo-Json | Out-File "evidence\delivery_qc.json" -Encoding utf8
  Write-Host ($qc | ConvertTo-Json) -ForegroundColor Green
}
