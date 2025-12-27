# Task Tracking System

**Version:** 1.0.0
**Last Updated:** 2025-12-27

## Overview

The Task Tracking System ensures tasks are never lost across sessions. It provides persistent storage for tasks that agents and humans can query, update, and track.

## Architecture

```
.claude/agent-coordinator/runtime/
├── tasks.json          # Active task database
└── backups/            # Automatic backups on save
    ├── tasks_20231227_120000.json
    └── tasks_corrupt_20231227_120500.json  # Corrupt file backups
```

## Components

| Component | File | Purpose |
|-----------|------|---------|
| Task Manager | `scripts/task_manager.py` | Core task storage and queries |
| State Integration | `scripts/state_manager.py` | Task summary in `/status` |
| Command Interface | `commands/tasks.md` | `/tasks` slash command |
| Storage | `~/.claude/agent-coordinator/runtime/tasks.json` | Persistent task database |

## Task Schema

Each task has the following structure:

```json
{
  "id": "task_20231227120000123456",
  "content": "Implement user authentication",
  "status": "pending",
  "priority": "high",
  "category": "implementation",
  "context": "Add OAuth2 login flow",
  "created_at": "2025-12-27T12:00:00.123456",
  "updated_at": "2025-12-27T12:00:00.123456",
  "completed_at": null,
  "blocked_by": [],
  "tags": []
}
```

## Status Values

| Status | Symbol | Meaning |
|--------|--------|---------|
| `pending` | `[ ]` | Not started yet |
| `in_progress` | `[>]` | Currently being worked on |
| `completed` | `[x]` | Finished |
| `blocked` | `[!]` | Waiting for something else |
| `cancelled` | `[_]` | Cancelled/invalid |

## Priority Levels

| Priority | Symbol | Description |
|----------|--------|-------------|
| `critical` | `!` | Must be done immediately |
| `high` | `+` | Important, do soon |
| `medium` | `-` | Standard priority (default) |
| `low` | `o` | Nice to have |

## Usage

### Command Line Interface

```bash
# Show task summary
python3 scripts/task_manager.py summary

# Add a new task
python3 scripts/task_manager.py add "Implement feature X" --priority high --category implementation

# List active tasks
python3 scripts/task_manager.py list --active

# List by status
python3 scripts/task_manager.py list --status pending
python3 scripts/task_manager.py list --status completed

# List by priority
python3 scripts/task_manager.py list --priority critical

# Start a task
python3 scripts/task_manager.py start task_20231227120000123456

# Complete a task
python3 scripts/task_manager.py complete task_20231227120000123456

# Show next task to work on
python3 scripts/task_manager.py next

# Show task details
python3 scripts/task_manager.py show task_20231227120000123456

# Cancel a task
python3 scripts/task_manager.py cancel task_20231227120000123456

# Remove a task (permanent)
python3 scripts/task_manager.py remove task_20231227120000123456
```

### Slash Command

Invoke `/tasks` to:
1. See task summary
2. View active tasks
3. Get next recommended task
4. Add/manage tasks

### Python API

```python
from scripts.task_manager import TaskManager

mgr = TaskManager()

# Add a task
task_id = mgr.add(
    content="Implement feature X",
    priority="high",
    category="implementation",
    context="Needed for Q1 release"
)

# Query tasks
active_tasks = mgr.get_active()
next_task = mgr.get_next()

# Update tasks
mgr.start(task_id)
mgr.complete(task_id)

# Get summary
stats = mgr.summary()
# Returns: {"total": 10, "pending": 3, "in_progress": 1, ...}
```

## Integration with State Manager

The `state_manager.py` integrates with task tracking:

```python
mgr = StateManager()

# Get task summary
task_summary = mgr.get_task_summary()

# Get next task
next_task = mgr.get_next_task()

# Get formatted status including tasks
status = mgr.format_status_with_tasks()
```

## Common Categories

- `implementation` - Writing code
- `review` - Code review
- `docs` - Documentation
- `testing` - Writing or running tests
- `debug` - Fixing bugs
- `refactor` - Code cleanup
- `general` - Uncategorized (default)

## Task Selection Algorithm

When `get_next()` is called, tasks are sorted by:
1. Priority (critical > high > medium > low)
2. Creation date (earlier tasks first)

Only tasks with status `pending` or `in_progress` are considered.

## Automatic Backups

Every save creates a backup:
- Normal backup: `tasks_YYYYMMDD_HHMMSS.json`
- Corrupt file backup: `tasks_corrupt_YYYYMMDD_HHMMSS.json`

Backups are stored in `~/.claude/agent-coordinator/runtime/backups/`

## Persistence

- Tasks persist across all sessions
- Stored in user home directory (`~/.claude/...`)
- Survives project reboots
- Accessible from any project using agent-coordinator

## Best Practices

1. **Always add tasks before working** - Don't work on untracked tasks
2. **Use priorities wisely** - Reserve `critical` for blockers
3. **Mark blocked tasks** - Use `block` command with dependency IDs
4. **Add context** - Include notes for future reference
5. **Use categories** - Helps filter by work type
6. **Review regularly** - Use `/tasks` to check progress

## Examples

### Typical Workflow

```bash
# Start of session
python3 scripts/task_manager.py next

# Start working on shown task
python3 scripts/task_manager.py start task_20231227120000123456

# When done
python3 scripts/task_manager.py complete task_20231227120000123456

# Check what's next
python3 scripts/task_manager.py next
```

### Managing Blocked Work

```bash
# Add blocking task
python3 scripts/task_manager.py add "Fix API endpoint" --priority critical

# Mark dependent task as blocked
python3 scripts/task_manager.py block task_20231227120000123456 \
    --by task_20231227120000999999
```

### Agent Usage

Agents should:
1. Query `next` before starting work
2. `start` the task they're working on
3. `complete` when done
4. `add` new tasks they discover need doing

## File Locations

| Item | Location |
|------|----------|
| Tasks database | `~/.claude/agent-coordinator/runtime/tasks.json` |
| Backups | `~/.claude/agent-coordinator/runtime/backups/` |
| Script | `scripts/task_manager.py` |
| Command | `commands/tasks.md` |
| Documentation | `docs/coordination/TASK_SYSTEM.md` |
