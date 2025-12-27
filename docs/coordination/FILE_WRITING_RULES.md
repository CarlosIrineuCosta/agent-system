# File Writing Rules

## Overview

The agent-coordinator enforces strict rules about where agents can write files. This prevents agents from accidentally modifying critical configuration files, documentation, or code.

## Configuration

File: `config/agent_rules.json`

## Forbidden Paths

Agents are BLOCKED from writing to these files:

| Path | Reason |
|------|--------|
| `README.md` | Project documentation, user-facing |
| `LICENSE` | Legal file |
| `CONTRIBUTING.md` | Project governance |
| `CHANGELOG.md` | Release history |
| `config/agent_routing.json` | Core routing configuration |
| `config/hooks_settings.json` | Hook configuration |
| `hooks/core/quality_gate.py` | Core quality control |
| `hooks/core/completion_checker.py` | Core validation |
| `scripts/state_manager.py` | Lifecycle management |
| `scripts/garbage_collector.py` | Cleanup system |

## Protected Paths (Require Approval)

These paths require explicit user approval before writing:

| Path | Approval Required |
|------|-------------------|
| `docs/` | Yes (except `docs/coordination/`) |
| `.env` | Yes |
| `.gitignore` | Yes |
| `setup.py` | Yes |
| `requirements.txt` | Yes |

## Allowed Paths (Free Writing)

Agents can write freely to these locations:

| Path | Purpose |
|------|---------|
| `.agents/queue/` | Pending tasks |
| `.agents/output/` | Individual agent results |
| `.agents/coordinated/` | Final aggregated outputs |
| `.agents/logs/` | Agent execution logs |
| `docs/coordination/` | Checkpoint documentation |
| `docs/analysis/` | Analysis output |
| `.claude/state/` | Session state |

## Enforcement Mechanism

### Implementation Location

File: `hooks/core/file_write_validator.py`

### How It Works

1. **Pre-write check:** Before any Write/Edit operation, the hook validates the path
2. **Blocked:** Write is rejected with error message explaining why
3. **Protected:** Warning is shown but write proceeds (future: prompt for approval)
4. **Allowed:** Write proceeds normally

### Hook Integration

The validator is invoked via PostToolUse hook for Write and Edit operations:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 hooks/core/file_write_validator.py"
          }
        ]
      }
    ]
  }
}
```

### Error Message Format

```
BLOCKED: Cannot modify protected file: {file_path}

Reason: {reason}

Allowed write locations:
- docs/coordination/
- .agents/
- docs/analysis/

If you need to modify this file, ask the user to do it manually.
```

## Examples

### Blocked Write Attempt

```bash
# Agent tries to write to README.md
# Result: BLOCKED
```

### Protected Write (Requires Approval)

```bash
# Agent tries to write to docs/guide.md
# Result: Prompt for user approval
```

### Allowed Write

```bash
# Agent writes to .agents/output/result_001.json
# Result: Success
```

## Updating Rules

To modify the rules, edit `config/agent_rules.json`:

```json
{
  "forbidden_paths": {
    "root_markdown": ["README.md", "LICENSE"]
  },
  "protected_paths": {
    "require_approval": ["docs/"]
  },
  "allowed_paths": {
    "write_freely": [".agents/", "docs/coordination/"]
  }
}
```

## Safety First

These rules exist because:
1. **Prevent accidental damage** to critical files
2. **Maintain system integrity** - agents shouldn't modify their own governance
3. **Clear separation** - agent outputs go to designated areas
4. **User control** - important changes require explicit approval
