# SKIRT01 — 로컬 GPU 렌더 (RTX 3060 Ti). 사용자 PC의 PowerShell에서 실행.
# 사용: .\RUN_ALL.ps1 [-VerifyOnly] [-Rebake] [-Res 1080] [-Spp 256] [-Chunk 24]
# 골격이다. T-19에서 완성한다 (청크 렌더·이어하기·실패 청크 재시도 2회·render_log.csv·ffprobe+sha256).
param([switch]$VerifyOnly,[switch]$Rebake,[int]$Res=1080,[int]$Spp=256,[int]$Chunk=24)
$ErrorActionPreference="Stop"
$Blender="C:\Program Files\Blender Foundation\Blender 4.5\blender.exe"   # LOCK 4.5
$Root=Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
if(-not (Test-Path $Blender)){ throw "Blender 4.5 LTS 경로 확인: $Blender" }
if($Rebake -or -not (Test-Path "src\step_bake.npz")){ & $Blender -b --python src\bake_steps.py -- --config src\rig_config.json --out src\ }
& $Blender -b --python src\verify_bake.py -- --config src\rig_config.json --bake src\step_bake.npz --out evidence\bake_qc.json
if($VerifyOnly){ exit 0 }
if(-not (Test-Path "scene.blend")){ & $Blender -b --python src\build_scene.py -- --config src\rig_config.json --bake src\ --keys camera_keys.json --out scene.blend }
$cfg=Get-Content src\rig_config.json | ConvertFrom-Json
$total=$cfg.render.total_frames.value; if(-not $total){ throw "render.total_frames 미확정 (G2)" }
New-Item -ItemType Directory -Force render\final | Out-Null
"frame,sec,peak_vram,retries" | Out-File render\render_log.csv -Encoding utf8
for($s=1;$s -le $total;$s+=$Chunk){
  $e=[Math]::Min($s+$Chunk-1,$total)
  $missing=@(); for($f=$s;$f -le $e;$f++){ if(-not (Test-Path ("render\final\{0:d4}.png" -f $f))){ $missing+=$f } }
  if($missing.Count -eq 0){ continue }
  $tries=0
  do { $tries++; $t0=Get-Date
       & $Blender -b scene.blend --python src\render_frames.py -- --res $Res --spp $Spp --frames "$s-$e" --out render\final --gpu optix
       $ok=$LASTEXITCODE -eq 0
  } while(-not $ok -and $tries -le 2)
  "$s-$e,$([int]((Get-Date)-$t0).TotalSeconds),,$($tries-1)" | Out-File render\render_log.csv -Append -Encoding utf8
}
bash scripts/encode.sh render/final $cfg.render.fps.value final_1080x1920.mp4 audio/mix.wav
Get-FileHash final_1080x1920.mp4 -Algorithm SHA256 | Format-List
