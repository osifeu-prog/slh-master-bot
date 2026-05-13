function Show-SLH-Dashboard {
    Clear-Host
    Write-Host "  ??????+ ??+      ??+  ??+" -ForegroundColor Cyan
    Write-Host " ??+----+ ???      ???  ???" -ForegroundColor Cyan
    Write-Host " +?????+  ???      ????????" -ForegroundColor Cyan
    Write-Host "  +---??+ ???      ??+--???" -ForegroundColor Cyan
    Write-Host " ??????++ ???????+ ???  ???" -ForegroundColor Cyan
    Write-Host " +-----+  +------+ +-+  +-+ v2.2" -ForegroundColor Cyan
    Write-Host " ---------------------------------------------------------"
    Write-Host " [ OWNER: OSIF ] | [ SSoT: GitHub + Railway ]" -ForegroundColor Yellow
    Write-Host " ---------------------------------------------------------"
    
    if (Test-Path "D:\SLH_MASTER_BOT\backlog.md") {
        Write-Host "
>> CURRENT BACKLOG:" -ForegroundColor Magenta
        Get-Content "D:\SLH_MASTER_BOT\backlog.md" | Where-Object { $_ -match "^- " } | Select-Object -First 5
    }
    
    Write-Host "
>> SMART COMMANDS:" -ForegroundColor White
    Write-Host " todo   - Edit backlog & Sync to GitHub" -ForegroundColor Green
    Write-Host " st     - System Status (Local + Cloud)"
    Write-Host " deploy - Push all changes to Railway"
    Write-Host " reload - Refresh this Dashboard"
    Write-Host " ---------------------------------------------------------"
}

function todo {
    Write-Host ">> Opening Backlog..." -ForegroundColor Cyan
    notepad "D:\SLH_MASTER_BOT\backlog.md"
    Write-Host ">> Syncing changes to GitHub..." -ForegroundColor Yellow
    git add "D:\SLH_MASTER_BOT\backlog.md"
    git commit -m "v2.2: Backlog updated at 12:14" --allow-empty
    git push origin main
    Write-Host "OK: Backlog Synced." -ForegroundColor Green
    Show-SLH-Dashboard
}

function st {
    Write-Host "
>> LOCAL DOCKER STATUS:" -ForegroundColor Cyan
    docker ps --format "table {{.Names}}\t{{.Status}}"
    Write-Host "
>> RAILWAY CLOUD STATUS:" -ForegroundColor Yellow
    railway status
}

function reload { . "D:\SLH_MASTER_BOT\slh-cli.ps1" }

# Auto-start dashboard
Show-SLH-Dashboard
