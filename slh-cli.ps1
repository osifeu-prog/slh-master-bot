function slh {
    param([string]$Command, [string]$Arg = "")
    switch ($Command) {
        "status" {
            Write-Host "`n📊 SLH Status" -ForegroundColor Cyan
            docker ps --format "table {{.Names}}\t{{.Status}}"
            try {
                $h = Invoke-RestMethod -Uri "https://slh-fastapi-production.up.railway.app/health" -TimeoutSec 5
                Write-Host "FastAPI: OK" -ForegroundColor Green
            } catch { Write-Host "FastAPI: UNREACHABLE" -ForegroundColor Red }
        }
        "deploy-bot" {
            Write-Host "🚀 Deploying Master Bot..." -ForegroundColor Yellow
            git add .
            git commit -m "Deploy $(Get-Date -Format 'HH:mm')" --allow-empty
            git push origin main
            Write-Host "✅ Pushed to Railway!" -ForegroundColor Green
        }
        "help" { Write-Host "slh status | deploy-bot" -ForegroundColor Cyan }
        default { slh help }
    }
}
Write-Host "✅ SLH-CLI v2.5 Loaded" -ForegroundColor Green
