# scripts/backend-up.ps1 - Start backend uvicorn (dev mode)
# Run:  pwsh scripts/backend-up.ps1   or   powershell -ExecutionPolicy Bypass -File scripts\backend-up.ps1
[CmdletBinding()]
param(
    [string]$BackendDir = (Resolve-Path "$PSScriptRoot\..\backend").Path,
    [int]$Port = 8000,
    [string]$Host_ = "127.0.0.1"
)

$ErrorActionPreference = "Stop"

Write-Host "==> Starting backend in $BackendDir on ${Host_}:$Port" -ForegroundColor Cyan

# Check if port is in use; if so, stop the existing process first
$existing = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue | Select-Object -First 1
if ($existing) {
    Write-Host "!! Port $Port is in use by PID $($existing.OwningProcess) - stopping..." -ForegroundColor Yellow
    Stop-Process -Id $existing.OwningProcess -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 1
}

Push-Location $BackendDir
try {
    & uv run uvicorn app.main:app --host $Host_ --port $Port --reload
}
finally {
    Pop-Location
}
