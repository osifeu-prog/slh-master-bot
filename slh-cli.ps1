function prompt { "🚀 [SLH-MASTER] $((Split-Path -Leaf $pwd)) > " }
function st { railway status }
function reload { . $profile }

function power {
    Write-Host "`n📊 PRODUCTIVITY REPORT (Since Midnight)" -ForegroundColor Cyan
    $commits = git log --since="midnight" --oneline
    if ($commits) { $commits } else { Write-Host "No commits today yet." -ForegroundColor Gray }
    Write-Host "---------------------------------------"
    $done = Select-String -Path "TODO.md" -Pattern "\[x\]"
    Write-Host "Tasks completed: $($done.Count)" -ForegroundColor Green
}

function snapshot {
    $date = Get-Date -Format "yyyy-MM-dd_HHmm"
    $path = "D:\SLH_MASTER_BOT\snapshots"
    if (!(Test-Path $path)) { New-Item $path -ItemType Directory }
    git status > "$path\snapshot_$date.txt"
    Write-Host "✅ System state captured in snapshots/ folder." -ForegroundColor Green
}

function todo { notepad D:\SLH_MASTER_BOT\TODO.md }

# תצוגת פתיחה לסוכן
Clear-Host
Write-Host @"
  ██████  ██      ██   ██ 
 ██       ██      ██   ██ 
  █████   ██      ███████ 
      ██  ██      ██   ██ 
 ██████   ███████ ██   ██  v7.5 MASTER-CONTROL
 ---------------------------------------------------------
 [ OWNER: OSIF ] | [ STATUS: MODULAR TRANSITION ]
 ---------------------------------------------------------
 COMMANDS:
  st       - View Railway & Local Status
  power    - Daily summary (Commits/Tasks)
  snapshot - Backup current system state
  todo     - Edit the task list
  reload   - Refresh CLI after changes

 AGENT ONBOARDING:
  1. Always work in D:\SLH_MASTER_BOT
  2. Use 'todo' to see pending tasks.
  3. Deploy via 'git push' (Railway auto-builds).
  4. Check health with 'railway logs'.
 ---------------------------------------------------------
"@ -ForegroundColor Cyan

# ============================================================
# SESSION & LOGGING SYSTEM (Agent Collaboration)
# ============================================================

$global:SessionFile = "$PSScriptRoot\session_log.json"

function Start-AgentSession {
    $agentName = Read-Host "Enter your agent name (e.g., Osif, Claude, DevBot)"
    $session = @{
        agent = $agentName
        start = (Get-Date).ToString("o")
        actions = @()
    }
    if (Test-Path $global:SessionFile) {
        $all = Get-Content $global:SessionFile -Raw | ConvertFrom-Json
    } else {
        $all = @()
    }
    $all += $session
    $all | ConvertTo-Json -Depth 10 | Set-Content $global:SessionFile -Encoding UTF8
    Write-Host "✅ Session started for agent: $agentName at $(Get-Date)" -ForegroundColor Green
    Write-Host "📝 Use 'log <message>' to record actions." -ForegroundColor Cyan
}

function Log-Action {
    param([string]$message)
    if (-not (Test-Path $global:SessionFile)) {
        Write-Host "❌ No active session. Run 'start-session' first." -ForegroundColor Red
        return
    }
    $all = Get-Content $global:SessionFile -Raw | ConvertFrom-Json
    $last = $all[-1]
    $last.actions += @{
        time = (Get-Date).ToString("o")
        action = $message
    }
    $all[-1] = $last
    $all | ConvertTo-Json -Depth 10 | Set-Content $global:SessionFile -Encoding UTF8
    Write-Host "📝 Logged: $message" -ForegroundColor Green
}

function Show-SessionStatus {
    if (-not (Test-Path $global:SessionFile)) {
        Write-Host "No session log found." -ForegroundColor Yellow
        return
    }
    $all = Get-Content $global:SessionFile -Raw | ConvertFrom-Json
    $last = $all[-1]
    Write-Host "`n👤 Current agent: $($last.agent)" -ForegroundColor Cyan
    Write-Host "🕒 Started at: $($last.start)" -ForegroundColor Yellow
    Write-Host "📋 Actions this session: $($last.actions.Count)" -ForegroundColor Magenta
    if ($last.actions.Count -gt 0) {
        Write-Host "Latest action: $($last.actions[-1].action)" -ForegroundColor White
    }
}

function Daily-Snapshot {
    $date = Get-Date -Format "yyyy-MM-dd"
    $snapshotDir = "$PSScriptRoot\daily_snapshots"
    if (-not (Test-Path $snapshotDir)) { New-Item -ItemType Directory -Path $snapshotDir -Force | Out-Null }
    $snapshotFile = "$snapshotDir\state_$date.json"
    $state = @{
        date = (Get-Date).ToString("o")
        todo = Get-Content "$PSScriptRoot\TODO.md" -Raw -ErrorAction SilentlyContinue
        railway_status = (railway status 2>&1 | Out-String)
        docker_containers = (docker ps -a --format "table {{.Names}}\t{{.Status}}" | Out-String)
        session_log = Get-Content $global:SessionFile -Raw -ErrorAction SilentlyContinue
    }
    $state | ConvertTo-Json -Depth 5 | Set-Content $snapshotFile -Encoding UTF8
    Write-Host "📸 Daily snapshot saved to $snapshotFile" -ForegroundColor Green
}

# Override prompt to show session agent (optional, uncomment if desired)
function prompt {
    $path = Split-Path -Leaf $pwd
    $sessionInfo = ""
    if (Test-Path $global:SessionFile) {
        $all = Get-Content $global:SessionFile -ErrorAction SilentlyContinue | ConvertFrom-Json
        if ($all -and $all.Count -gt 0) {
            $agent = $all[-1].agent
            $sessionInfo = " [$agent]"
        }
    }
    Write-Host "`n  ██████  ██      ██   ██" -ForegroundColor Cyan -NoNewline
    Write-Host "`n ██       ██      ██   ██" -ForegroundColor Cyan -NoNewline
    Write-Host "`n  █████   ██      ███████" -ForegroundColor Cyan -NoNewline
    Write-Host "`n      ██  ██      ██   ██" -ForegroundColor Cyan -NoNewline
    Write-Host "`n ██████   ███████ ██   ██  v8.0 COLLABORATIVE" -ForegroundColor Cyan
    Write-Host " ---------------------------------------------------------" -ForegroundColor DarkGray
    Write-Host " [ OWNER: OSIF ] | [ STATUS: ONLINE$sessionInfo ]" -ForegroundColor Yellow
    Write-Host " ---------------------------------------------------------" -ForegroundColor DarkGray
    Write-Host " COMMANDS: st, todo, power, log, status, session, snapshot, deploy, reload" -ForegroundColor White
    "🚀 [SLH-MASTER] $path > "
}
