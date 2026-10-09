# RUN_ALL.ps1 — Windows 최종 렌더 진입점 (T12에서 Codex가 완성)
# 사용: powershell -File RUN_ALL.ps1 [-VerifyOnly] [-Rebake] [-AssetMap assets\asset_map.json] [-Blender "C:\Program Files\Blender Foundation\Blender 4.5\blender.exe"]
param(
  [switch]$VerifyOnly,
  [switch]$Rebake,
  [string]$AssetMap = "",
  [string]$Blender = "C:\Program Files\Blender Foundation\Blender 4.5\blender.exe",
  [string]$OutDir = "render\final"
)
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
function Gate($name, $json) {
  $r = Get-Content $json -Raw | ConvertFrom-Json
  if (-not $r.ALL) { Write-Error "$name FAIL — $json"; exit 1 }
  Write-Host "$name PASS"
}
python tools\check_beats.py --json evidence\beats_check.json; Gate "G01" "evidence\beats_check.json"
if ($Rebake -or -not (Test-Path src\motion_bake.npz)) { & $Blender -b --python src\bake.py }
& $Blender -b --python src\verify_bake.py -- --json evidence\verify_bake.json; Gate "G02" "evidence\verify_bake.json"
$am = @(); if ($AssetMap) { $am = @("--asset-map", $AssetMap) }
& $Blender -b --python src\build_scene.py -- --out build\e5_emu370.blend @am
& $Blender -b build\e5_emu370.blend --python src\verify_scene.py -- --json evidence\verify_scene.json; Gate "G03" "evidence\verify_scene.json"
& $Blender -b build\e5_emu370.blend --python src\verify_proportion.py -- --json evidence\proportion.json; Gate "G05" "evidence\proportion.json"
if ($VerifyOnly) { Write-Host "VerifyOnly: 렌더 생략"; exit 0 }
New-Item -ItemType Directory -Force $OutDir | Out-Null
# 이어하기: render_final.py는 이미 있는 PNG 프레임을 건너뛴다 (Cycles GPU, look.json samples_final)
& $Blender -b build\e5_emu370.blend --python src\render_final.py -- --out $OutDir
ffmpeg -y -framerate 30 -i "$OutDir\%04d.png" -vf "pad=1080:1920:0:240:black" -c:v libx264 -profile:v high -pix_fmt yuv420p -crf 16 render\picture_1080x1920.mp4
ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=width,height,r_frame_rate,nb_read_frames -of compact render\picture_1080x1920.mp4
ffmpeg -v error -i render\picture_1080x1920.mp4 -f null -
Get-FileHash render\picture_1080x1920.mp4 -Algorithm SHA256 | Format-List
