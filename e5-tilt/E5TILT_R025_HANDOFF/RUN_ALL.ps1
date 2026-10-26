<#
E5 TILT R025 - Windows pipeline (local GPU: RTX 3060 Ti 8GB).
Blender 4.5 LTS (LOCK) for bpy stages; a Python 3.11 venv (.venv: numpy, pillow) for numpy-only stages.

  .\RUN_ALL.ps1 -Setup                         # once: create .venv
  .\RUN_ALL.ps1 -VerifyOnly                    # bake -> G3 -> build -> G4, no render
  .\RUN_ALL.ps1 -Stage animatic                # full pipeline, 270x480 frames, CPU/GPU
  .\RUN_ALL.ps1 -Stage key4s -Start 319 -End 438
  .\RUN_ALL.ps1 -Stage final -Chunk 12         # 1080x1920, GPU, chunks with resume + retry
  .\RUN_ALL.ps1 -Stage final -AssetMap src\ASSET_MAP.json

Exit code != 0 when any gate fails. Frames go to work\frames_<stage> (keep this folder OUT of Google Drive sync).
#>
param(
  [switch]$Setup, [switch]$VerifyOnly, [switch]$Rebake = $true,
  [string]$AssetMap = "",
  [ValidateSet('animatic','still','key4s','preview','final')][string]$Stage = 'animatic',
  [int]$Start = 1, [int]$End = 803, [int]$Chunk = 12,
  [string]$Blender = "C:\Program Files\Blender Foundation\Blender 4.5\blender.exe",
  [string]$Py = ".venv\Scripts\python.exe"
)
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
$Src = Join-Path $Root 'src'; $Work = Join-Path $Root 'work'; $Ev = Join-Path $Root 'evidence'
New-Item -ItemType Directory -Force -Path $Work, $Ev | Out-Null

function Gate($name, $code) { if ($code -ne 0) { Write-Host "GATE FAIL: $name" -ForegroundColor Red; exit 1 } else { Write-Host "GATE PASS: $name" -ForegroundColor Green } }

if ($Setup) {
  py -3.11 -m venv .venv
  & $Py -m pip install --upgrade pip
  & $Py -m pip install numpy==1.26.4 pillow
  Write-Host "venv ready"; exit 0
}
if (-not (Test-Path $Blender)) { Write-Host "Blender not found: $Blender  (pass -Blender path)"; exit 2 }
$ver = (& $Blender --version | Select-Object -First 1)
if ($ver -notmatch 'Blender 4\.5') { Write-Host "Blender LOCK is 4.5 LTS, found: $ver"; exit 2 }
if (-not (Test-Path $Py)) { Write-Host "run .\RUN_ALL.ps1 -Setup first"; exit 2 }

$Blend = Join-Path $Work 'e5tilt_R025_proxy.blend'
if ($Rebake) {
  & $Py "$Src\kin.py"; Gate 'kin' $LASTEXITCODE
}
& $Py "$Src\verify_bake.py"; Gate 'G3 bake' $LASTEXITCODE
& $Py "$Src\sfx_cues.py"; & $Py "$Src\make_beats.py"
& $Blender -b --factory-startup --python "$Src\build.py" -- --out $Blend; Gate 'build' $LASTEXITCODE
$Pairs = @()
if ($AssetMap -ne "") {
  $AssetBlend = Join-Path $Work 'e5tilt_R025_assets.blend'
  & $Blender -b --factory-startup --python "$Src\import_assets.py" -- --blend $Blend --map $AssetMap --out $AssetBlend; Gate 'asset import' $LASTEXITCODE
  $Blend = $AssetBlend
  $Pairs = @('--extra_pairs', ($AssetBlend -replace '\.blend$', '_pairs.json'))
}
& $Blender -b --factory-startup --python "$Src\verify_scene.py" -- --blend $Blend --step 5 @Pairs; Gate 'G4 scene' $LASTEXITCODE
if ($VerifyOnly) { Write-Host "VerifyOnly done"; exit 0 }

# ---- chunked render with resume + up to 2 retries per chunk
$Out = Join-Path $Work "frames_$Stage"; New-Item -ItemType Directory -Force -Path $Out | Out-Null
$vram = $null
if (Get-Command nvidia-smi -ErrorAction SilentlyContinue) {
  $vram = Start-Process nvidia-smi -ArgumentList '--query-gpu=memory.used','--format=csv,noheader,nounits','-l','1' -RedirectStandardOutput (Join-Path $Out 'vram.log') -PassThru -WindowStyle Hidden
}
$failed = @()
for ($a = $Start; $a -le $End; $a += $Chunk) {
  $b = [Math]::Min($a + $Chunk - 1, $End)
  $ok = $false
  for ($try = 0; $try -le 2 -and -not $ok; $try++) {
    & $Blender -b --factory-startup --python "$Src\render_frames.py" -- --blend $Blend --stage $Stage --start $a --end $b --outdir $Out --gpu
    $missing = @($a..$b | Where-Object { -not (Test-Path (Join-Path $Out ('{0:D4}.png' -f $_))) })
    $ok = ($missing.Count -eq 0)
    if (-not $ok) { Write-Host "chunk $a-$b retry $($try+1): missing $($missing.Count)" -ForegroundColor Yellow }
  }
  if (-not $ok) { $failed += $missing }
}
if ($vram) { Stop-Process -Id $vram.Id -ErrorAction SilentlyContinue }
$peak = 0; if (Test-Path (Join-Path $Out 'vram.log')) { $peak = (Get-Content (Join-Path $Out 'vram.log') | ForEach-Object { [int]$_ } | Measure-Object -Maximum).Maximum }
@{ stage = $Stage; failed_frames = $failed; vram_peak_mib = $peak } | ConvertTo-Json | Set-Content (Join-Path $Out 'render_summary.json')
if ($failed.Count -gt 0) { Write-Host "FAILED FRAMES: $($failed -join ',')" -ForegroundColor Red; exit 1 }

# ---- 2.5D overlays (shapes only) + encode (BT.709 matrix stated explicitly) + delivery QC
$Comp = Join-Path $Work "frames_${Stage}_comp"
& $Py "$Src\comp_overlays.py" --frames $Out --out $Comp; Gate 'comp' $LASTEXITCODE
$Mp4 = Join-Path $Root "review\R025\e5tilt_R025_${Stage}.mp4"
ffmpeg -y -framerate 30 -start_number $Start -i "$Comp\%04d.png" -i "audio\R024_ORIGINAL_AUDIO.m4a" `
  -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2:out_color_matrix=bt709:out_range=tv,format=yuv420p" `
  -c:v libx264 -profile:v high -crf 16 -preset slow -colorspace bt709 -color_primaries bt709 -color_trc bt709 `
  -c:a aac -b:a 320k -ar 48000 -af "apad" -shortest -movflags +faststart $Mp4
Gate 'encode' $LASTEXITCODE
$n = (ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of csv=p=0 $Mp4)
ffmpeg -v error -i $Mp4 -f null - 2> (Join-Path $Ev "decode_$Stage.log")
$dec = (Get-Item (Join-Path $Ev "decode_$Stage.log")).Length
$sha = (Get-FileHash $Mp4 -Algorithm SHA256).Hash.ToLower()
@{ file = $Mp4; frames = [int]$n; expected = ($End - $Start + 1); decode_error_bytes = $dec; sha256 = $sha } | ConvertTo-Json | Set-Content (Join-Path $Ev "delivery_qc_$Stage.json")
& $Py "$Src\sync_qc.py" --video $Mp4
Write-Host "DONE $Mp4 frames=$n sha256=$sha"
