# Visibility System - Real-Time Agent Monitoring

## Overview

Terminal-based monitoring for agent coordinator activity. Shows which agents are active, what they're working on, and system status.

## Architecture

```
Agents write to: .agents/runtime/status/{agent_name}.status
Monitor reads from:
  - .agents/runtime/status/*.status
  - .claude/agent-coordinator/runtime/state.json
  - .agents/queue/
```

## Status File Format

**Location:** `.agents/runtime/status/{agent_name}.status`

```json
{
  "agent": "glm-4.7",
  "status": "active|idle|error",
  "task": "Implementing login authentication",
  "started_at": "2025-12-26T03:15:00Z",
  "progress": 0.65,
  "last_output": "Generated auth.py module"
}
```

## Usage

### Quick Start

```bash
# Terminal 1: Start monitor (live updates every 2 seconds)
python scripts/monitor.py

# Terminal 2: Run agent task (monitor will show activity)
python scripts/multi_llm_coordinator.py --task "Implement tests for auth module"
```

**What you'll see:**
- When task starts: GLM-4.7 changes from `idle` to `active`
- During execution: Task description and time since start
- When complete: GLM-4.7 returns to `idle`

### Start Monitor

```bash
python scripts/monitor.py
```

Updates every 2 seconds. Press Ctrl+C to exit.

### Single Check

```bash
python scripts/monitor.py --once
```

Display current status once and exit.

### Status Indicators

| Status | Meaning |
|--------|---------|
| `active` | Agent is working on a task |
| `idle` | Agent available, not working |
| `error` | Agent encountered an error |

## Monitor Display

```
============================================================
  AGENT COORDINATOR - LIVE STATUS
============================================================
  System: ACTIVE | Version: 1.0.0 | Uptime: 45m
------------------------------------------------------------
  ACTIVE AGENTS
  [GREEN] GLM-4.7     | Implementing auth              | 2m ago | 65%
  [WHITE] CODEX       | Idle                           |     -  |
  [GRAY]  GEMINI      | (no status)                    |     -  |
------------------------------------------------------------
  QUEUE
  No pending tasks
------------------------------------------------------------
  Last update: 2025-12-26 03:20:15 | Press Ctrl+C to exit
============================================================
```

## Status Icons

| Icon | Meaning |
|------|---------|
| `[GREEN]` or `active` | Agent is currently working on a task |
| `[WHITE]` or `idle` | Agent is available, not working |
| `[RED]` or `error` | Agent encountered an error |
| `[GRAY]` | No status file exists |

## Implementation Notes

### Minimal Design

- Uses standard `print()` statements (no rich library)
- File-based IPC (no complex message passing)
- 2-second poll interval
- Simple status icons

### Status Writer Function

Located in `scripts/multi_llm_coordinator.py`:

```python
def update_agent_status(agent_name, status, task="", progress=None, last_output=None):
    STATUS_DIR.mkdir(parents=True, exist_ok=True)
    status_data = {
        "agent": agent_name,
        "status": status,
        "task": task,
        "started_at": datetime.now().isoformat(),
        "progress": progress,
        "last_output": last_output
    }
    status_file = STATUS_DIR / f"{agent_name}.status"
    with open(status_file, 'w') as f:
        json.dump(status_data, f, indent=2)
```

Called at:
- Before starting agent: `update_agent_status("glm-4.7", "active", task_description)`
- After completion: `update_agent_status("glm-4.7", "idle", "")`
- On error: `update_agent_status("glm-4.7", "error", error_message)`

## Testing

### Test the Monitor

```bash
# Terminal 1: Start monitor
python scripts/monitor.py

# Terminal 2: Run a task
python scripts/multi_llm_coordinator.py --task "Implement a hello world function"
```

Expected: Monitor shows GLM-4.7 becoming active, then idle after completion.

## Files

| File | Purpose |
|------|---------|
| `scripts/monitor.py` | Monitor display script |
| `scripts/multi_llm_coordinator.py` | Coordinator with status writes |
| `.agents/runtime/status/` | Status files (created at runtime) |
| `.claude/agent-coordinator/runtime/state.json` | System state |

## Future Enhancements

- Add `rich` library for prettier display
- Show agent output in real-time
- Add color coding (green=active, yellow=busy, etc.)
- Support for filtering by agent type
- Historical view of recent completions
