<#
BSK-HSR-COUPLER local runner (Windows, RTX 3060 Ti). Blender 4.5 LTS for build/scene QC/render, a Python 3.11 venv for bake/verify/VO.

Steps (-Step):
  setup    : create .venv (numpy, shapely, faster-whisper, soundfile), check blender/ffmpeg/nvidia-smi
  verify   : bake -> verify_bake -> build -> verify_scene for -Test (A|B|all). Stops on the first FAIL.  (= -VerifyOnly)
  baseline : verify + compare with reference values in HANDOFF (reproduction check)
  timing   : render ONE representative frame with -Preset on GPU, print seconds/frame and peak VRAM
  render   : verify, then chunked GPU render (-Chunk frames per blender process, resume, 2 retries), encode preview
  vo       : audio/VO_LOCK.json -> sha256/duration, word timestamps, event retime report (add -Apply to write rig_config)
Examples:
  .\RUN_ALL.ps1 -Step setup -Blender "C:\Program Files\Blender Foundation\Blender 4.5\blender.exe"
  .\RUN_ALL.ps1 -Step baseline -Test all
  .\RUN_ALL.ps1 -Step timing -Test A -Preset key4s_gpu
  .\RUN_ALL.ps1 -Step render -Test A -Preset key4s_gpu -Range 80,199
  .\RUN_ALL.ps1 -Step vo -Apply
#>
param(
  [ValidateSet("setup","verify","baseline","timing","render","vo")] [string]$Step = "verify",
  [ValidateSet("A","B","all")] [string]$Test = "all",
  [ValidateSet("animatic","key4s","key4s_gpu","final")] [string]$Preset = "animatic",
  [int[]]$Range = @(),
  [int]$Chunk = 24,
  [string]$Blender = $(if ($env:BLENDER_EXE) { $env:BLENDER_EXE } else { "C:\Program Files\Blender Foundation\Blender 4.5\blender.exe" }),
  [switch]$Apply,
  [switch]$VerifyOnly
)
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
$Py = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if ($VerifyOnly) { $Step = "verify" }

$Cfg = Get-Content "src\rig_config.json" -Raw -Encoding utf8 | ConvertFrom-Json      # bake length can change after -Step vo -Apply
$Tests = @{
  "B" = @{ tag="schB";  kin="kin_schB.py";     vb="verify_bake_schB.py";     build="build_schB.py";     vs="verify_scene_schB.py";     frames=$Cfg.test_B_scharfenberg.bake_frames; label="CONCEPT_ONLY TEST B" };
  "A" = @{ tag="shibA"; kin="kin_shibataA.py"; vb="verify_bake_shibataA.py"; build="build_shibataA.py"; vs="verify_scene_shibataA.py"; frames=$Cfg.test_A_shibata.bake_frames;      label="CONCEPT_ONLY TEST A" }
}
$Sel = if ($Test -eq "all") { @("B","A") } else { @($Test) }

function Run-Py([string]$script, [string[]]$a = @()) {
  & $Py "src\$script" @a; if ($LASTEXITCODE -ne 0) { throw "FAIL: $script (exit $LASTEXITCODE)" }
}
function Run-Blender([string]$script, [string[]]$a = @()) {
  $args_ = @("-b", "--factory-startup", "--python-exit-code", "1", "-P", "src\$script")
  if ($a.Count) { $args_ += "--"; $args_ += $a }
  & $Blender @args_ 2>&1 | Where-Object { $_ -match '^(F\d+:|GPU:|rendered|Traceback|Error|\s+"|\{|\})' } | ForEach-Object { Write-Host $_ }
  if ($LASTEXITCODE -ne 0) { throw "FAIL: blender $script (exit $LASTEXITCODE)" }
}
function Verify-Test($t) {
  Write-Host "== $($t.tag): bake -> verify_bake -> build -> verify_scene" -ForegroundColor Cyan
  Run-Py $t.kin; Run-Py $t.vb; Run-Blender $t.build; Run-Blender $t.vs
}
function Peak-VRAM { try { [int](& nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits | Select-Object -First 1) } catch { -1 } }

switch ($Step) {
  "setup" {
    if (-not (Test-Path $Blender)) { throw "Blender not found: $Blender (pass -Blender or set BLENDER_EXE)" }
    & $Blender -b --factory-startup --python-expr "import bpy,sys; v=bpy.app.version; print('BLENDER', bpy.app.version_string); sys.exit(0 if v[:2]==(4,5) else 3)"
    if ($LASTEXITCODE -ne 0) { throw "Blender is not 4.5 LTS (version LOCK)" }
    if (-not (Test-Path $Py)) { & py -3.11 -m venv .venv }
    & $Py -m pip install --upgrade pip; & $Py -m pip install numpy shapely faster-whisper soundfile
    & $Py -c "import numpy, shapely; print('venv ok', numpy.__version__, shapely.__version__)"
    foreach ($tool in @("ffmpeg","ffprobe","nvidia-smi")) { if (-not (Get-Command $tool -ErrorAction SilentlyContinue)) { Write-Warning "$tool not on PATH" } }
  }
  "verify"   { foreach ($k in $Sel) { Verify-Test $Tests[$k] }; Write-Host "VERIFY PASS: $Test" -ForegroundColor Green }
  "baseline" {
    foreach ($k in $Sel) { Verify-Test $Tests[$k] }
    Run-Py "check_baseline.py"
  }
  "timing" {
    foreach ($k in $Sel) {
      $t = $Tests[$k]; $ev = Get-Content "evidence\$($t.tag)_events.json" | ConvertFrom-Json
      $f = if ($k -eq "A") { $ev.JP_LOCKED.local_F } else { $ev.SCH_LOCKED.local_F }
      $out = "render\_timing_$($t.tag)_$Preset"; Remove-Item -Recurse -Force $out -ErrorAction SilentlyContinue
      $sw = [Diagnostics.Stopwatch]::StartNew(); Run-Blender $t.build @("--render", "$f", "$f", "--preset", $Preset, "--out", $out, "--gpu"); $sw.Stop()
      Write-Host ("TIMING {0} F{1} {2}: {3:N1}s wall (includes scene build) | VRAM now {4} MiB" -f $t.tag, $f, $Preset, $sw.Elapsed.TotalSeconds, (Peak-VRAM)) -ForegroundColor Yellow
    }
  }
  "render" {
    foreach ($k in $Sel) {
      $t = $Tests[$k]; Verify-Test $t
      $r0, $r1 = if ($Range.Count -eq 2) { $Range[0], $Range[1] } else { 1, $t.frames }
      $out = "render\$($t.tag)_$Preset"; New-Item -ItemType Directory -Force $out | Out-Null
      $log = "render\$($t.tag)_$Preset`_render_log.csv"; if (-not (Test-Path $log)) { "chunk_start,chunk_end,seconds,vram_mib,retries,status" | Out-File $log -Encoding utf8 }
      $failed = @()
      for ($s = $r0; $s -le $r1; $s += $Chunk) {
        $e = [Math]::Min($s + $Chunk - 1, $r1); $try = 0; $ok = $false
        while (-not $ok -and $try -le 2) {
          $sw = [Diagnostics.Stopwatch]::StartNew()
          try { Run-Blender $t.build @("--render", "$s", "$e", "--preset", $Preset, "--out", $out, "--gpu"); $ok = $true } catch { $try++ ; Write-Warning "chunk $s-$e failed (try $try): $_" }
          $sw.Stop(); "$s,$e,$([Math]::Round($sw.Elapsed.TotalSeconds,1)),$(Peak-VRAM),$try,$(if($ok){'OK'}else{'RETRY'})" | Out-File $log -Append -Encoding utf8
        }
        if (-not $ok) { $failed += "$s-$e" }
      }
      if ($failed.Count) { Write-Warning "FAILED CHUNKS: $($failed -join ', ')"; continue }
      $mp4 = "review\$($t.tag)_$Preset`_$r0-$r1.mp4"; New-Item -ItemType Directory -Force review | Out-Null
      & ffmpeg -v error -y -framerate 30 -start_number $r0 -i "$out\%04d.png" `
        -vf "drawtext=fontfile='C\:/Windows/Fonts/arial.ttf':text='$($t.label)':fontsize=18:fontcolor=white@0.85:box=1:boxcolor=black@0.5:x=10:y=h-th-10,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p" `
        -c:v libx264 -profile:v high -crf 16 -preset slow -colorspace bt709 -color_primaries bt709 -color_trc bt709 -movflags +faststart $mp4
      & ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=width,height,r_frame_rate,nb_read_frames -of compact=p=0 $mp4
      & ffmpeg -v error -i $mp4 -f null -; if ($LASTEXITCODE -eq 0) { Write-Host "decode ok: $mp4" -ForegroundColor Green }
      & ffmpeg -v error -y -i $mp4 -c:v libx264 -b:v 2M -maxrate 2M -bufsize 4M -an ($mp4 -replace '\.mp4$','_stress2M.mp4')
    }
  }
  "vo" {
    if (-not (Test-Path "audio\VO_LOCK.json")) { Copy-Item "audio\VO_LOCK.TEMPLATE.json" "audio\VO_LOCK.json"; throw "Fill audio\VO_LOCK.json (voice name/engine) and put the 10 WAV files in audio\, then re-run" }
    $a = @(); if ($Apply) { $a += "--apply" }
    & $Py "src\vo_words.py" @a; $code = $LASTEXITCODE
    if ($Apply -and $code -eq 0) { Write-Host "events retimed -> re-run: .\RUN_ALL.ps1 -Step verify" -ForegroundColor Green }
    elseif ($code -ne 0) { Write-Warning "VO sync violations: see audio\vo_sync_report.json" }
  }
}
# manifest (sha256) of evidence + review + audio
Get-ChildItem evidence, review, audio -File -Recurse -ErrorAction SilentlyContinue | Where-Object { $_.Extension -notin ".blend1" } |
  ForEach-Object { [pscustomobject]@{ path = (Resolve-Path -Relative $_.FullName); bytes = $_.Length; sha256 = (Get-FileHash $_.FullName -Algorithm SHA256).Hash.ToLower() } } |
  ConvertTo-Json | Out-File MANIFEST.json -Encoding utf8
