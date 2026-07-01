# scripts/backend-down.ps1 - Stop backend uvicorn (kill by port 8000)
# Run:  pwsh scripts/backend-down.ps1
[CmdletBinding()]
param([int]$Port = 8000)

$conns = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
if (-not $conns) {
    Write-Host "Port $Port is already free." -ForegroundColor Green
    return
}

$pids = $conns | Select-Object -ExpandProperty OwningProcess -Unique
foreach ($procId in $pids) {
    try {
        Stop-Process -Id $procId -Force -ErrorAction Stop
        Write-Host "Killed PID $procId on port $Port" -ForegroundColor Yellow
    } catch {
        Write-Host "Could not kill PID ${procId}: $_" -ForegroundColor Red
    }
}
Start-Sleep -Seconds 1
if (Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue) {
    Write-Host "WARNING: port $Port still in use" -ForegroundColor Red
} else {
    Write-Host "Port $Port is now free." -ForegroundColor Green
}
