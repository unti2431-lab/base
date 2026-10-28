<#
BSK-HSR-COUPLER local runner (Windows, RTX 3060 Ti). Blender 4.5 LTS for build/scene QC/render, a Python 3.11 venv for bake/verify/VO.
R9a (2026-10-29, Cowork): Windows PowerShell 5.1 hardening - see REPORT.md "R9a RUN_ALL.ps1".

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
  [string]$Blender = "",
  [switch]$Apply,
  [switch]$VerifyOnly
)
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
# R9a: Korean Windows defaults Python open() to cp949; rig_config.json holds UTF-8 (section sign, Japanese terms) -> force UTF-8 mode
$env:PYTHONUTF8 = "1"; $env:PYTHONIOENCODING = "utf-8"
# R9a: UTF-8 without BOM (Out-File -Encoding utf8 in PS 5.1 writes a BOM, which Python json.load rejects)
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
function Write-Utf8([string]$path, [string]$text) { [IO.File]::WriteAllText((Join-Path $PSScriptRoot $path), $text + "`r`n", $Utf8NoBom) }
function Add-Utf8([string]$path, [string]$text) { [IO.File]::AppendAllText((Join-Path $PSScriptRoot $path), $text + "`r`n", $Utf8NoBom) }

# Blender path: -Blender > blender_path.txt > $env:BLENDER_EXE > default install path
if (-not $Blender) {
  if (Test-Path "blender_path.txt") { $Blender = (Get-Content "blender_path.txt" -Raw).Trim().Trim('"') }
  elseif ($env:BLENDER_EXE) { $Blender = $env:BLENDER_EXE }
  else { $Blender = "C:\Program Files\Blender Foundation\Blender 4.5\blender.exe" }
}
# every run leaves a log the agent (Cowork / Claude Code) can read back from the folder
New-Item -ItemType Directory -Force logs | Out-Null
$Stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$LogFile = "logs\RUN_{0}_{1}_{2}.log" -f $Step, $Test, $Stamp
Start-Transcript -Path $LogFile | Out-Null
trap { Write-Host "RUN_STATUS: FAIL $_" -ForegroundColor Red; Write-Utf8 "logs\LAST_STATUS.txt" "FAIL $Step $Test $(Get-Date -Format s) $_"; Stop-Transcript | Out-Null; exit 1 }
$Py = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if ($VerifyOnly) { $Step = "verify" }

# R9a: run a native exe without letting PS 5.1 turn stderr lines into terminating errors; every line goes to the transcript.
#      Returns the output lines; throws only on a non-zero exit code.
function Invoke-Native([string]$exe, [string[]]$a, [string]$what, [scriptblock]$filter = { $true }) {
  $old = $ErrorActionPreference; $ErrorActionPreference = "Continue"
  $lines = @(& $exe @a 2>&1 | ForEach-Object { "$_" })
  $code = $LASTEXITCODE; $ErrorActionPreference = $old
  $lines | Where-Object $filter | ForEach-Object { Write-Host $_ }
  if ($code -ne 0) { throw "FAIL: $what (exit $code)" }
  return ,$lines
}

$Cfg = Get-Content "src\rig_config.json" -Raw -Encoding utf8 | ConvertFrom-Json      # bake length can change after -Step vo -Apply
$Tests = @{
  "B" = @{ tag="schB";  kin="kin_schB.py";     vb="verify_bake_schB.py";     build="build_schB.py";     vs="verify_scene_schB.py";     frames=$Cfg.test_B_scharfenberg.bake_frames; label="CONCEPT_ONLY TEST B" };
  "A" = @{ tag="shibA"; kin="kin_shibataA.py"; vb="verify_bake_shibataA.py"; build="build_shibataA.py"; vs="verify_scene_shibataA.py"; frames=$Cfg.test_A_shibata.bake_frames;      label="CONCEPT_ONLY TEST A" }
}
$Sel = if ($Test -eq "all") { @("B","A") } else { @($Test) }

function Run-Py([string]$script, [string[]]$a = @()) {
  $null = Invoke-Native $Py (@("src\$script") + $a) $script
}
function Run-Blender([string]$script, [string[]]$a = @()) {
  $args_ = @("-b", "--factory-startup", "--python-exit-code", "1", "-P", "src\$script")
  if ($a.Count) { $args_ += "--"; $args_ += $a }
  $lines = Invoke-Native $Blender $args_ "blender $script" { $_ -match '^(F\d+:|GPU:|rendered|Traceback|Error|\s+"|\{|\})' }
  # full Blender output kept for debugging (the console shows only the filtered lines)
  $full = "logs\blender_{0}_{1}.log" -f ($script -replace '\.py$',''), (Get-Date -Format "yyyyMMdd_HHmmss_fff")
  [IO.File]::WriteAllLines((Join-Path $PSScriptRoot $full), [string[]]$lines, $Utf8NoBom)
  return ,$lines
}
function Verify-Test($t) {
  Write-Host "== $($t.tag): bake -> verify_bake -> build -> verify_scene" -ForegroundColor Cyan
  Run-Py $t.kin; Run-Py $t.vb; $null = Run-Blender $t.build; $null = Run-Blender $t.vs
}
function Peak-VRAM { try { [int](& nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits | Select-Object -First 1) } catch { -1 } }
# R9a: real peak VRAM - sample nvidia-smi every 250 ms while Blender runs (the old Peak-VRAM read the idle value after exit)
function Start-VramLog([string]$csv) {
  if (-not (Get-Command nvidia-smi -ErrorAction SilentlyContinue)) { return $null }
  $p = Join-Path $PSScriptRoot $csv; Remove-Item $p -ErrorAction SilentlyContinue
  Start-Process nvidia-smi -ArgumentList @("--query-gpu=memory.used", "--format=csv,noheader,nounits", "-lms", "250", "-f", "`"$p`"") -WindowStyle Hidden -PassThru
}
function Stop-VramLog($proc, [string]$csv) {
  if ($null -eq $proc) { return -1 }
  try { Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue } catch {}
  Start-Sleep -Milliseconds 300
  $p = Join-Path $PSScriptRoot $csv
  if (-not (Test-Path $p)) { return -1 }
  $v = Get-Content $p | Where-Object { $_ -match '^\s*\d+\s*$' } | ForEach-Object { [int]$_ } | Measure-Object -Maximum
  if ($v.Count) { [int]$v.Maximum } else { -1 }
}

switch ($Step) {
  "setup" {
    if (-not (Test-Path $Blender)) { throw "Blender not found: $Blender (pass -Blender or set BLENDER_EXE)" }
    $null = Invoke-Native $Blender @("-b", "--factory-startup", "--python-expr", "import bpy,sys; v=bpy.app.version; print('BLENDER', bpy.app.version_string); sys.exit(0 if v[:2]==(4,5) else 3)") "Blender is not 4.5 LTS (version LOCK)" { $_ -match '^BLENDER' }
    if (-not (Test-Path $Py)) { $null = Invoke-Native "py" @("-3.11", "-m", "venv", ".venv") "py -3.11 -m venv (install Python 3.11 with the py launcher)" }
    $null = Invoke-Native $Py @("-m", "pip", "install", "--upgrade", "pip") "pip upgrade" { $_ -match 'Successfully|ERROR' }
    $null = Invoke-Native $Py @("-m", "pip", "install", "numpy", "shapely", "faster-whisper", "soundfile") "pip install" { $_ -match 'Successfully|ERROR|already satisfied: (numpy|shapely|faster-whisper|soundfile) ' }
    $null = Invoke-Native $Py @("-c", "import numpy, shapely, soundfile, faster_whisper; print('venv ok', numpy.__version__, shapely.__version__)") "venv import check"
    $missing = @()
    foreach ($tool in @("ffmpeg","ffprobe","nvidia-smi")) { if (-not (Get-Command $tool -ErrorAction SilentlyContinue)) { Write-Warning "$tool not on PATH"; $missing += $tool } }
    if ($missing.Count) { throw "missing tools on PATH: $($missing -join ', ')" }   # R9a: L01 accept = no missing-tool warning
    $null = Invoke-Native "nvidia-smi" @("--query-gpu=name,driver_version,memory.total", "--format=csv,noheader") "nvidia-smi"
  }
  "verify"   { foreach ($k in $Sel) { Verify-Test $Tests[$k] }; Write-Host "VERIFY PASS: $Test" -ForegroundColor Green }
  "baseline" {
    foreach ($k in $Sel) { Verify-Test $Tests[$k] }
    Run-Py "check_baseline.py"
  }
  "timing" {
    $rows = @()
    foreach ($k in $Sel) {
      $t = $Tests[$k]; $ev = Get-Content "evidence\$($t.tag)_events.json" -Raw | ConvertFrom-Json
      $f = if ($k -eq "A") { $ev.JP_LOCKED.local_F } else { $ev.SCH_LOCKED.local_F }
      $out = "render\_timing_$($t.tag)_$Preset"; Remove-Item -Recurse -Force $out -ErrorAction SilentlyContinue
      $vcsv = "logs\vram_timing_$($t.tag)_$Preset`_$Stamp.csv"; $vp = Start-VramLog $vcsv
      $sw = [Diagnostics.Stopwatch]::StartNew()
      # R9a: render F-1 then F and time only F (the first Cycles frame includes GPU kernel load/compile)
      try { $lines = Run-Blender $t.build @("--render", "$($f - 1)", "$f", "--preset", $Preset, "--out", $out, "--gpu") } finally { $sw.Stop(); $peak = Stop-VramLog $vp $vcsv }
      $dev = ($lines | Where-Object { $_ -match '^GPU:' } | Select-Object -First 1)
      $times = @($lines | ForEach-Object { if ($_ -match '^rendered \d+ in ([\d.]+)s') { [double]$Matches[1] } })
      $rs = if ($times.Count) { $times[-1] } else { $null }
      if ($times.Count -ge 2) { Write-Host ("first frame {0}s (warm-up), measured frame {1}s" -f $times[0], $times[-1]) }
      if (-not $dev) { throw "timing $($t.tag): no 'GPU:' line - render did not run on OPTIX/CUDA" }
      Write-Host ("TIMING {0} F{1} {2}: render {3}s/frame | wall {4:N1}s (incl. scene build) | peak VRAM {5} MiB | {6}" -f $t.tag, $f, $Preset, $rs, $sw.Elapsed.TotalSeconds, $peak, $dev) -ForegroundColor Yellow
      $rows += "{0},{1},{2},{3},{4:N1},{5},{6}" -f $t.tag, $f, $Preset, $rs, $sw.Elapsed.TotalSeconds, $peak, ($dev -replace ',', ';')
    }
    $tcsv = "logs\timing.csv"; if (-not (Test-Path $tcsv)) { Write-Utf8 $tcsv "tag,frame,preset,render_s_per_frame,wall_s,peak_vram_mib,device,stamp" }
    foreach ($r in $rows) { Add-Utf8 $tcsv "$r,$Stamp" }
  }
  "render" {
    $allFailed = @()
    foreach ($k in $Sel) {
      $t = $Tests[$k]; Verify-Test $t
      if ($Range.Count -eq 2) { $r0, $r1 = $Range[0], $Range[1] }
      elseif ($Preset -like "key4s*") {   # G3 window [E-60, E+59] from the fresh bake (moves after -Step vo -Apply)
        $ev = Get-Content "evidence\$($t.tag)_events.json" -Raw | ConvertFrom-Json
        $E = if ($k -eq "A") { $ev.JP_LOCKED.local_F } else { $ev.SCH_LOCKED.local_F }; $r0, $r1 = ($E - 60), ($E + 59)
        Write-Host "G3 window $($t.tag): F$r0-F$r1 (E=$E)" -ForegroundColor Cyan
      } else { $r0, $r1 = 1, $t.frames }
      $out = "render\$($t.tag)_$Preset"; New-Item -ItemType Directory -Force $out | Out-Null
      $log = "render\$($t.tag)_$Preset`_render_log.csv"; if (-not (Test-Path $log)) { Write-Utf8 $log "chunk_start,chunk_end,seconds,peak_vram_mib,retries,status" }
      $failed = @()
      for ($s = $r0; $s -le $r1; $s += $Chunk) {
        $e = [Math]::Min($s + $Chunk - 1, $r1); $try = 0; $ok = $false
        while (-not $ok -and $try -le 2) {
          $vcsv = "logs\vram_$($t.tag)_$s.csv"; $vp = Start-VramLog $vcsv
          $sw = [Diagnostics.Stopwatch]::StartNew()
          try { $null = Run-Blender $t.build @("--render", "$s", "$e", "--preset", $Preset, "--out", $out, "--gpu"); $ok = $true } catch { $try++ ; Write-Warning "chunk $s-$e failed (try $try): $_" }
          $sw.Stop(); $peak = Stop-VramLog $vp $vcsv
          Add-Utf8 $log "$s,$e,$([Math]::Round($sw.Elapsed.TotalSeconds,1)),$peak,$try,$(if($ok){'OK'}else{'RETRY'})"
        }
        if (-not $ok) { $failed += "$s-$e" }
      }
      if ($failed.Count) { Write-Warning "FAILED CHUNKS $($t.tag): $($failed -join ', ')"; $allFailed += "$($t.tag):$($failed -join '/')"; continue }
      $missingPng = @($r0..$r1 | Where-Object { -not (Test-Path ("{0}\{1:D4}.png" -f $out, $_)) })
      if ($missingPng.Count) { $allFailed += "$($t.tag): $($missingPng.Count) PNG missing"; continue }
      $mp4 = "review\$($t.tag)_$Preset`_$r0-$r1.mp4"; New-Item -ItemType Directory -Force review | Out-Null
      $vf = "drawtext=fontfile='C\:/Windows/Fonts/arial.ttf':text='$($t.label)':fontsize=18:fontcolor=white@0.85:box=1:boxcolor=black@0.5:x=10:y=h-th-10,drawtext=fontfile='C\:/Windows/Fonts/arial.ttf':text='F %{eif\:n+$r0\:d}':fontsize=18:fontcolor=white@0.85:box=1:boxcolor=black@0.5:x=w-tw-10:y=h-th-10,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p"
      $null = Invoke-Native "ffmpeg" @("-v", "error", "-y", "-framerate", "30", "-start_number", "$r0", "-i", "$out\%04d.png", "-vf", $vf,
        "-c:v", "libx264", "-profile:v", "high", "-crf", "16", "-preset", "slow", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-movflags", "+faststart", $mp4) "ffmpeg encode $mp4"
      $null = Invoke-Native "ffprobe" @("-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=width,height,r_frame_rate,nb_read_frames", "-of", "compact=p=0", $mp4) "ffprobe $mp4"
      $null = Invoke-Native "ffmpeg" @("-v", "error", "-i", $mp4, "-f", "null", "-") "decode check $mp4"; Write-Host "decode ok: $mp4" -ForegroundColor Green
      $null = Invoke-Native "ffmpeg" @("-v", "error", "-y", "-i", $mp4, "-c:v", "libx264", "-b:v", "2M", "-maxrate", "2M", "-bufsize", "4M", "-an", ($mp4 -replace '\.mp4$','_stress2M.mp4')) "stress encode"
    }
    if ($allFailed.Count) { throw "render incomplete: $($allFailed -join '; ')" }   # R9a: was reported as PASS before
  }
  "vo" {
    if (-not (Test-Path "audio\VO_LOCK.json")) { Copy-Item "audio\VO_LOCK.TEMPLATE.json" "audio\VO_LOCK.json"; throw "Fill audio\VO_LOCK.json (voice name/engine) and put the 10 WAV files in audio\, then re-run" }
    $a = @("src\vo_words.py"); if ($Apply) { $a += "--apply" }
    $null = Invoke-Native $Py $a "vo_words.py - VO sync violations, see audio\vo_sync_report.json"   # R9a: violations now FAIL (was a warning + PASS)
    if ($Apply) { Write-Host "events retimed -> re-run: .\RUN_ALL.ps1 -Step verify" -ForegroundColor Green }
  }
}
# manifest (sha256) of evidence + review + audio
$man = Get-ChildItem evidence, review, audio -File -Recurse -ErrorAction SilentlyContinue | Where-Object { $_.Extension -notin ".blend1" } |
  ForEach-Object { [pscustomobject]@{ path = (Resolve-Path -Relative $_.FullName); bytes = $_.Length; sha256 = (Get-FileHash $_.FullName -Algorithm SHA256).Hash.ToLower() } } |
  ConvertTo-Json
Write-Utf8 "MANIFEST.json" $man
Write-Utf8 "logs\LAST_STATUS.txt" "PASS $Step $Test $(Get-Date -Format s) log=$LogFile"
Write-Host "RUN_STATUS: PASS ($Step $Test) log=$LogFile" -ForegroundColor Green
Stop-Transcript | Out-Null
