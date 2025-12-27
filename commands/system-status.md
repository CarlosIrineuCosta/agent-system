---
description: Show Agent Coordinator system status
---

# System Status

## Show Status

```bash
python3 scripts/state_manager.py status
```

Displays:
- System status (STOPPED, STARTING, ACTIVE, STOPPING)
- Version
- Active agents
- Task summary (if TaskManager is available)
- Next task to work on

## Show Status as JSON

```bash
python3 scripts/state_manager.py status --json
```

Output raw state JSON for programmatic access.

## Status Values

| Status | Meaning |
|--------|---------|
| STOPPED | System is not running |
| STARTING | System is initializing |
| ACTIVE | System is running and ready |
| STOPPING | System is shutting down |

## State File Location

`~/.claude/agent-coordinator/runtime/state.json`

## Example Output

```
System Status: ACTIVE
Version: 1.0.0
Active Agents: glm-4.7

Tasks:
  Total: 10
  Pending: 3
  In Progress: 1
  Completed: 6

Next: Implement feature X
  Priority: high
```

## AI Assistant Instructions

When showing status:
1. Always display the full status output
2. Highlight any issues (no agents, errors, etc.)
3. Offer next actions based on status
4. If ACTIVE, show what to work on next
