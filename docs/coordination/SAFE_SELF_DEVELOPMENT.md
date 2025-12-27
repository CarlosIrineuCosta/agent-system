# Safe Self-Development

## Problem

The **bootstrap problem**: You can't safely use the agent system to develop itself. If agents modify `agent-coordinator` files directly, you risk breaking the source that all projects depend on via symlinks.

## Solution

**Sandbox development pattern:** Create a copy (sandbox) of the canonical install. Make changes there, test them, then promote back to canonical only after validation.

## Architecture

```
~/Storage/projects/
├── agent-coordinator/          # Canonical (all projects symlink here)
│   ├── scripts/
│   ├── config/
│   └── ...
└── agent-coordinator-dev/       # Sandbox (for testing changes)
    ├── scripts/
    ├── config/
    └── ...
```

## Workflow

### 1. Create Sandbox

```bash
cd ~/Storage/projects/agent-coordinator
python scripts/sandbox_manager.py create
```

Creates `agent-coordinator-dev/` as a copy of canonical.

### 2. Develop in Sandbox

```bash
# Work on sandbox files
cd ~/Storage/projects/agent-coordinator-dev
# Edit files, test changes, etc.
```

### 3. Test Changes

```bash
# Use agent system to work on sandbox files
# (Point tasks to agent-coordinator-dev, not agent-coordinator)
python scripts/multi_llm_coordinator.py --task "Improve the monitor script" \
  --files ~/Storage/projects/agent-coordinator-dev/scripts/monitor.py
```

### 4. Promote to Canonical

```bash
python scripts/sandbox_manager.py promote
```

After you're satisfied with the changes:
- Promote copies sandbox files to canonical
- Review with `git diff` in canonical
- Commit if satisfied

### 5. Clean Sandbox (Optional)

```bash
python scripts/sandbox_manager.py clean
```

Remove the sandbox after promotion to save space.

## Sandbox Manager Commands

| Command | Description |
|---------|-------------|
| `create` | Create sandbox from canonical |
| `sync` | Sync canonical → sandbox (update sandbox) |
| `promote` | Promote sandbox → canonical (merge tested changes) |
| `status` | Show sandbox status and changes |
| `clean` | Remove sandbox |

## Example Session

```bash
# 1. Create sandbox
python scripts/sandbox_manager.py create

# 2. Make a test change in sandbox
echo "# TEST COMMENT" >> ~/Storage/projects/agent-coordinator-dev/README.md

# 3. Check status
python scripts/sandbox_manager.py status
# Output shows: Modified: 1 file (README.md)

# 4. Promote change to canonical
python scripts/sandbox_manager.py promote
# Output: Promoted 1 files to canonical

# 5. Review in canonical
cd ~/Storage/projects/agent-coordinator
git diff
# Shows: + # TEST_COMMENT

# 6. Clean up
python scripts/sandbox_manager.py clean
```

## Important Notes

### Symlinks vs Sandbox

- **Canonical** (`agent-coordinator`): All projects symlink to this. DO NOT edit directly.
- **Sandbox** (`agent-coordinator-dev`): Testing ground. Safe to make changes here.

### When to Use Sandbox

Use sandbox when:
- Asking agents to modify agent-coordinator code
- Testing new features or bug fixes
- Refactoring or significant changes

Skip sandbox when:
- Editing documentation only
- Making trivial/trivial changes
- Working on non-agent-coordinator projects

### Git Workflow

1. Changes are made in sandbox
2. Promote to canonical (copies files)
3. `git diff` in canonical to review
4. `git commit` in canonical when satisfied
5. Sandbox can be cleaned after commit

## Safety Features

- **Read-only comparison:** Status command shows differences without modifying anything
- **Confirmation required:** Promote and clean commands require explicit confirmation
- **Binary files skipped:** Won't try to compare `.pyc`, images, etc.
- **Markers preserved:** `.SANDBOX` file tracks sandbox origin

## Files

| File | Purpose |
|------|---------|
| `scripts/sandbox_manager.py` | Sandbox management CLI |
| `docs/SAFE_SELF_DEVELOPMENT.md` | This document |
| `agent-coordinator-dev/` | Sandbox directory (created on demand) |

## Success Criteria

- ✅ Can modify system using itself (via sandbox)
- ✅ Changes don't break production projects (canonical isolated)
- ✅ Easy rollback if something breaks (just don't promote)
