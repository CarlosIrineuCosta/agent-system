---
description: Show and manage agent system tasks
---

# Task Management Command

## Show Task Summary

```bash
python3 scripts/task_manager.py summary
```

## Show Active Tasks

```bash
python3 scripts/task_manager.py list --active
```

## Show Next Task

```bash
python3 scripts/task_manager.py next
```

## Show Tasks by Status

```bash
# Pending tasks
python3 scripts/task_manager.py list --status pending

# In progress
python3 scripts/task_manager.py list --status in_progress

# Completed
python3 scripts/task_manager.py list --status completed
```

## Show Tasks by Priority

```bash
# Critical tasks
python3 scripts/task_manager.py list --priority critical

# High priority
python3 scripts/task_manager.py list --priority high
```

## Task Operations

### Add a New Task
```bash
python3 scripts/task_manager.py add "Task description" --priority high --category implementation
```

### Start a Task
```bash
python3 scripts/task_manager.py start task_YYYYMMDDHHMMSSssssss
```

### Complete a Task
```bash
python3 scripts/task_manager.py complete task_YYYYMMDDHHMMSSssssss
```

### Cancel a Task
```bash
python3 scripts/task_manager.py cancel task_YYYYMMDDHHMMSSssssss
```

### Show Task Details
```bash
python3 scripts/task_manager.py show task_YYYYMMDDHHMMSSssssss
```

## AI Assistant Instructions

When the `/tasks` command is invoked:

1. **Display Summary**: Always show `task_manager.py summary` first
2. **Show Active Tasks**: List all pending/in-progress tasks
3. **Show Next Task**: Highlight what should be worked on next
4. **Offer Actions**: Ask if the user wants to:
   - Add a new task
   - Start/complete a task
   - Filter by status/priority/category

## Task File Location

Tasks are stored in: `~/.claude/agent-coordinator/runtime/tasks.json`

Backups are kept in: `~/.claude/agent-coordinator/runtime/backups/`

## Priority Levels

- `critical` - Must be done immediately
- `high` - Important, do soon
- `medium` - Standard priority (default)
- `low` - Nice to have

## Status Values

- `pending` - Not started yet
- `in_progress` - Currently being worked on
- `completed` - Finished
- `blocked` - Waiting for something else
- `cancelled` - Cancelled/invalid

## Categories

Common categories (you can use any):
- `implementation` - Writing code
- `review` - Code review
- `docs` - Documentation
- `testing` - Writing or running tests
- `debug` - Fixing bugs
- `refactor` - Code cleanup
- `general` - Uncategorized (default)
