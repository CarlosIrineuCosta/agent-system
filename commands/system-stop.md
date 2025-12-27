---
description: Stop the Agent Coordinator system
---

# Stop Agent Coordinator

## Stop the System

```bash
python3 scripts/state_manager.py stop
```

This will:
1. Set system status to STOPPING
2. Wait for active agents to finish (default: 30 second timeout)
3. Archive current session to `.agents/runtime/logs/`
4. Run garbage collection on old outputs/logs
5. Set system status to STOPPED

## Stop with Custom Timeout

```bash
python3 scripts/state_manager.py stop --timeout 60
```

Wait up to 60 seconds for agents to finish.

## What Gets Cleaned Up

The garbage collection removes:
- Output files older than 7 days
- Log files older than 30 days
- Empty status files

## Session Archive

Before stopping, the current state is archived to:
`.agents/runtime/logs/session_YYYYMMDD_HHMMSS.json`

## AI Assistant Instructions

After stopping the system:
1. Verify shutdown was successful (check exit code)
2. Display session archive location
3. Show garbage collection results
4. Confirm system is STOPPED
