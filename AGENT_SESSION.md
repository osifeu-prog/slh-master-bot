# SLH AGENT SESSION MANAGEMENT

## Start your session
`start-session` → enter agent name (Claude, Osif, DevBot...)

## Log your actions
`log "Fixed Redis connection"`

## Check session status
`status`

## Daily snapshot
`snapshot`  saves state to daily_snapshots/

## From Telegram
`/log "message"`

## Rules
- Always start session before work.
- Log every major change.
- Snapshot before risky changes.
- Use `todo` to update task list.
