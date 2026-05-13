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
