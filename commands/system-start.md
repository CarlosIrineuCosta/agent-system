---
description: Start the Agent Coordinator system
---

# Start Agent Coordinator

## Start the System

```bash
python3 scripts/state_manager.py start
```

This will:
1. Create required directory structure
2. Verify environment (GLM, Codex, Gemini availability)
3. Check for updates
4. Set system status to ACTIVE

## Verify Environment Only

```bash
python3 scripts/state_manager.py start --verify
```

Check what agents are available without starting the system.

## What Gets Created

- `.agents/runtime/status/` - Agent status files
- `.agents/runtime/outputs/` - Agent output logs
- `.agents/runtime/logs/` - Session archives
- `.agents/sessions/` - Session data

## State File

The system state is stored in: `~/.claude/agent-coordinator/runtime/state.json`

## AI Assistant Instructions

After starting the system:
1. Verify startup was successful (check exit code)
2. Display the current status
3. Show available agents
4. Show any update notifications
5. Proceed with task work
