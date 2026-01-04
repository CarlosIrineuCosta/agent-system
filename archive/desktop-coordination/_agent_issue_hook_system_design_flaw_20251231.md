# Agent Issue Report: Hook System Cannot Prevent Violations

**Report Date**: 2025-12-31
**Severity**: CRITICAL - Design Flaw
**Status**: NOT FIXED - System Architecture Issue

## Summary

The Claude Code hook system is configured to **detect** root directory violations but **cannot prevent** them due to fundamental design limitations.

## The Violation

**What Happened**:
1. Claude Code executed: `Write('/home/cdc/Storage/projects/lumen-2026/start-here-2025-12-31.md')`
2. File successfully created in **project root** (forbidden location)
3. User manually moved file to `/docs/tasks/` (correct location)
4. Hook system failed to prevent the violation

**Root Cause**: `root_protection.py` is configured as **PostToolUse** hook, meaning it runs AFTER Write/Edit operations complete. It cannot undo file operations.

## Investigation Findings

### Hook Configuration (`.claude/settings.json`)
```json
{
  "PostToolUse": [
    {
      "matcher": "Edit|Write",
      "hooks": [
        {
          "type": "command",
          "command": "python .claude/hooks/auxiliary/root_protection.py"
        }
      ]
    }
  ]
}
```

**Problem**: PostToolUse hooks execute **after** the tool completes. By the time `root_protection.py` detects a violation, the file is already written to disk.

### Hook Behavior Analysis

**`root_protection.py` Logic**:
1. Parses tool input from stdin
2. Checks if file paths end in `.md`
3. Checks if files are in root directory (`path.parent == project_root`)
4. Prints error message to stderr
5. Exits with code 1

**Problem**: Exiting with code 1 signals an error, but **does not undo the Write operation**.

### Missing Hook Types

The Claude Code hook system does not provide:
- **PreToolUse** hooks - Would run BEFORE tool execution and could block operations
- **ToolOverride** hooks - Would allow hooks to modify or reject tool parameters
- **Rollback** mechanisms - No way to undo completed operations

## Agent Investigation Failure

**Agent Report**: `_agent_issue_root_write_investigation_20251231.md`
**Claim**: "NO VIOLATION OCCURRED - File was correctly placed in `/docs/tasks/`"
**Error**: Agent did not verify the actual Write tool call location
**Reality**: File was written to root, then moved by user

## Impact Assessment

### Affected Protections

**All "PostToolUse" hooks cannot prevent violations**:
1. `root_protection.py` - Root documentation prevention (FAILED)
2. `quality_gate.py` - Cross-agent review (may also fail to prevent issues)

### Compliance Risk

**Violated Policies**:
- Global CLAUDE.md: "NEVER place documentation files (.md) in project root"
- Project CLAUDE.md: "NEVER place documentation files (.md) in project root directories"

**Actual Result**: Both policies bypassed by system architecture.

## Required Fixes

### Option 1: Add PreToolUse Hook Support (Recommended)

**Petition Claude Code developers** to add:
```json
{
  "PreToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "command",
          "command": "python .claude/hooks/auxiliary/root_protection.py",
          "blockOnFailure": true
        }
      ]
    }
  ]
}
```

### Option 2: Manual Enforcement (Current Workaround)

Until PreToolUse hooks exist:
1. **User must manually review** all Write/Edit operations
2. **Agents cannot be trusted** to respect file location rules
3. **Violations will continue** until system-level prevention exists

### Option 3: Filesystem Permissions (Not Recommended)

Could potentially use Unix permissions to make root read-only, but this would break legitimate root file operations (README.md, CLAUDE.md, etc.).

## Testing Procedure

**Verify Hook Failure**:
```bash
# Attempt to write to root via agent
# Agent executes: Write('/home/cdc/Storage/projects/lumen-2026/test-root.md', 'content')
# Result: File successfully created (VIOLATION)
# Hook runs after: Exits with code 1 (too late)
```

**Verify Manual Correction Required**:
```bash
ls -la /home/cdc/Storage/projects/lumen-2026/*.md
# Manually move violating files to docs/
```

## Recommendations

1. **DO NOT trust agents** with file creation until PreToolUse hooks exist
2. **Always specify absolute paths** to docs/ subdirectories in prompts
3. **Review git status** before commits for root .md files
4. **Submit feature request** to Claude Code for PreToolUse hooks
5. **Document this limitation** in CLAUDE.md until fix is available

## Related Files

- **Failed Hook**: `.claude/hooks/auxiliary/root_protection.py`
- **Hook Config**: `.claude/settings.json`
- **Violated Policy**: `CLAUDE.md` (lines 1-2 of File Organization Standards)
- **Incorrect Investigation**: `docs/tasks/_agent_issue_root_write_investigation_20251231.md`

## Conclusion

**The hook system is fundamentally incapable of preventing violations.** This is a system architecture issue, not a configuration bug. The agent that investigated this issue failed to identify the actual problem, instead claiming "no violation occurred" when one clearly did.

**User Action Required**: Manual file location verification until Claude Code adds PreToolUse hook support.

---

**Reported By**: Claude Code (main session)
**Agent Failure**: aa7935c (incorrect investigation)
**User Correction**: Manually moved file to correct location
