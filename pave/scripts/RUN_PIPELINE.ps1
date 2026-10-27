# PAVE 파이프라인 (Windows PowerShell) — 사용자 PC 용
#   .\scripts\RUN_PIPELINE.ps1            베이크 -> 베이크 게이트 -> build_* -> verify_scene
#   .\scripts\RUN_PIPELINE.ps1 -BakeOnly  베이크와 게이트만
#   .\scripts\RUN_PIPELINE.ps1 -Blender "C:\Program Files\Blender Foundation\Blender 4.5\blender.exe"
#       build_* 를 bpy 모듈 대신 Blender 실행 파일(백그라운드)로 돌린다(GPU 렌더 단계에서 사용).
# 주의: 이 스크립트는 작성 환경(Linux)에서 실행 검증하지 못했다. 첫 실행 결과를 REPORT.md 에 기록할 것.
param([switch]$BakeOnly, [string]$Python = "python", [string]$Blender = "")
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Evd = Join-Path $Root "evidence"; New-Item -ItemType Directory -Force $Evd | Out-Null
$Status = Join-Path $Evd "pipeline_status.txt"; Set-Content $Status ""
function Log($m) { Write-Host $m; Add-Content $Status $m }

& $Python (Join-Path $Root "src\pave_kin.py") | Out-File (Join-Path $Evd "bake_qc_stdout.json") -Encoding utf8
$ok = $LASTEXITCODE -eq 0
Copy-Item (Join-Path $Root "src\bake\bake_qc.json") (Join-Path $Evd "bake_qc.json") -ErrorAction SilentlyContinue
if (-not $ok) { Log "G3 bake: FAIL (evidence\bake_qc.json 확인)"; exit 1 }
Get-ChildItem (Join-Path $Root "src\bake") | Get-FileHash -Algorithm SHA256 |
  ForEach-Object { "{0}  {1}" -f $_.Hash.ToLower(), (Split-Path -Leaf $_.Path) } |
  Set-Content (Join-Path $Evd "bake_sha256.txt")
Log "G3 bake: PASS"
if ($BakeOnly) { exit 0 }

foreach ($st in "build_auger","build_internals","build_head","build_stones","build_cameras","verify_scene") {
  $f = Join-Path $Root "src\$st.py"
  if (-not (Test-Path $f)) { Log "${st}: NOT_PERFORMED (src\$st.py 없음)"; continue }
  if ($Blender) { & $Blender -b --factory-startup --python $f } else { & $Python $f }
  if ($LASTEXITCODE -ne 0) { Log "${st}: FAIL"; exit 1 }
  Log "${st}: DONE"
}
