# SLH-CLI v2.1 - Master Control
function slh {
    param([string]$Command, [string]$Arg = "")

    switch ($Command) {
        "status" {
            Write-Host "🔍 SLH Full Status" -ForegroundColor Cyan
            docker ps --format "table {{.Names}}\t{{.Status}}"
            Write-Host "`n🌐 FastAPI:" -ForegroundColor Green
            Invoke-RestMethod -Uri "https://slh-fastapi-production.up.railway.app/health" -TimeoutSec 10
        }
        "fastapi" {
            Write-Host "🌐 FastAPI:" -ForegroundColor Green
            Invoke-RestMethod -Uri "https://slh-fastapi-production.up.railway.app/health" -TimeoutSec 10
        }
        "bot" {
            if ($Arg -eq "logs") { docker logs slh-master-bot --tail 30 }
            else { docker ps | Select-String "slh-master-bot" }
        }
        "restart" {
            docker restart slh-master-bot slh-redis-v3 slh-db-v3
            Write-Host "✅ Restarted local core" -ForegroundColor Green
        }
        "deploy-bot" {
            Write-Host "🚀 Deploying Master Bot to Railway..." -ForegroundColor Yellow
            git -C .. add .
            git -C .. commit -m "chore: deploy bot v3.13" --allow-empty
            git -C .. push origin main
            Write-Host "✅ Push done → Railway will auto-deploy" -ForegroundColor Green
        }
        "holders" {
            $path = "D:\SLH_CONTROL_CENTER\export-tokenholders-for-contract-0xACb0A09414CEA1C879c67bB7A877E4e19480f022.csv"
            if (Test-Path $path) {
                Import-Csv $path | Sort-Object {[float]$_.Balance} -Descending | Select-Object -First 10 | Format-Table HolderAddress, Balance -AutoSize
            }
        }
        default {
            Write-Host "SLH CLI Commands:" -ForegroundColor Cyan
            Write-Host "   slh status          - סטטוס מלא"
            Write-Host "   slh fastapi         - בדיקת FastAPI"
            Write-Host "   slh bot logs        - לוגים של הבוט"
            Write-Host "   slh restart         - אתחול שירותים"
            Write-Host "   slh deploy-bot      - דחיפה ל-Railway"
            Write-Host "   slh holders         - Top Holders"
        }
    }
}

Write-Host "✅ SLH-CLI v2.1 טעון בהצלחה!" -ForegroundColor Green
