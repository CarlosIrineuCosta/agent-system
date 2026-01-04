# Investigation Recommendations
**Generated**: 2025-12-31
**Based on**: Investigation findings

---

## Update 2026-01-01: Current Assessment and Corrections
**Status**: Claude Code now uses Anthropic models again (base URL override removed).

### Overall Assessment
The system drifted into an API-centric design (Z.ai/MiniMax Anthropic-compatible endpoints) while the project constraint is "no APIs ever." That caused model identity confusion (Anthropic labels pointing to non-Anthropic endpoints) and led to wrapper implementations that must be retired. Going forward, the agentic system should be CLI-only: Claude Code as primary, and OpenCode or other CLI tools as secondary, with hooks and routing done via bash. This clarifies model provenance, aligns with plan/CLI usage, and avoids hidden endpoint swaps.

### Immediate Corrections (No-API Rule)
1. **Archive direct API wrappers**: `scripts/glm_direct.py`, `scripts/glm_cli.py`, `scripts/glm_internal.py`, `scripts/test_parallel_agents.py` are legacy and should stay archived.
2. **Do not reference Anthropic-compatible endpoints** (e.g., `ANTHROPIC_BASE_URL=https://api.z.ai/api/anthropic`) in production configs.
3. **Prefer `/model opus` and `/model sonnet`** inside Claude Code instead of pinning model IDs that go stale.

### Recommendations That No Longer Make Sense (Remove or Rewrite)
1. **Priority 1.1 Fix Codex/Gemini Wrappers**: The current plan says "direct API endpoint" and "glm_direct.py pattern." This violates the no-API rule. Must be rewritten to CLI-only or dropped.
2. **Priority 2.6 Add MiniMax Integration**: The existing approach is direct API and should be removed; if MiniMax is needed, route through a CLI wrapper instead.
3. **Priority 4.11 Update to GLM-4.7**: This is no longer relevant; GLM should only be used via a CLI path if at all.
4. **Any guidance referencing `ANTHROPIC_BASE_URL` overrides** should be removed or moved into a "legacy notes" section.

### Notes to Keep for Later Review
- `scripts/ai-agent.sh` and `scripts/state_manager.py` still reference external endpoints, but they are not being removed yet. Leave as-is and annotate later if kept.

---

## Priority 1: Critical (Do First)

### 1. Fix Codex and Gemini Wrappers
**Problem**: Subprocess calls fail with TTY/arg-limit errors

**Solution**:
1. Research Codex direct API endpoint
2. Research Gemini direct API endpoint (likely OpenAI-compatible)
3. Rewrite wrappers using glm_direct.py pattern
4. Remove subprocess dependencies

**Files to modify**:
- `scripts/codex_wrapper.py`
- `scripts/gemini_wrapper.py`

**Expected outcome**: Non-interactive agent execution

---

### 2. Integrate Expect Wrappers (Fallback)
**Problem**: Useful expect scripts not integrated

**Solution**:
1. Copy from `simple-agents/` to `agent-coordinator/scripts/wrappers/`
2. Document as fallback option
3. Update permissions to allow expect

**Expected outcome**: Backup TTY automation if direct API unavailable

---

### 3. Implement Auto-Documentation Hook
**Problem**: Documentation updates are manual

**Solution**:
1. Review `docs/coordination/implementations/auto_doc_hook/`
2. Enable hook in config
3. Test with file edits
4. Customize documentation mapping

**Expected outcome**: Automatic doc updates after changes

---

## Priority 2: High (Do Soon)

### 4. Consolidate Projects
**Problem**: Three separate agent projects causing confusion

**Solution**:
1. Copy useful files from agent-system-standalone to agent-coordinator
2. Archive simple-agents/old_backup/
3. Update all references to point to agent-coordinator
4. Delete agent-new/ (single MD file)

**Expected outcome**: Single source of truth

---

### 5. Update Deprecated References
**Problem**: 176 outdated references found

**Solution**:
1. Review `docs/coordination/analysis/deprecated_references.json`
2. Update "/dev" references to current commands
3. Update "/api" references to current commands
4. Remove Cline/KiloCode references if unused

**Expected outcome**: Clean, consistent codebase

---

### 6. Add MiniMax Integration
**Problem**: Missing MiniMax M2.1 agent

**Solution**:
1. Set `MINIMAX_API_KEY` environment variable
2. Copy `docs/coordination/implementations/minimax_direct.py` to scripts/
3. Test with simple prompt
4. Add to multi_llm_coordinator

**Expected outcome**: Fourth agent available for coordination

---

## Priority 3: Medium (Do When Time)

### 7. Install Claude Skills
**Problem**: Skills package designed but not installed

**Solution**:
1. Copy `docs/coordination/implementations/coordination-skills/` to `~/.claude/skills/user/`
2. Test each skill
3. Customize for workflow

**Expected outcome**: Reusable agent coordination patterns

---

### 8. Tighten Permissions
**Problem**: Wildcard permissions too broad

**Solution**:
1. Scope `python3:*` to `python3 scripts/*:*`
2. Remove `chmod:*` from auto-approve
3. Add expect script permissions

**Expected outcome**: Safer agent operations

---

### 9. Run Test Suite
**Problem**: Tests created but not executed

**Solution**:
1. Run `bash docs/coordination/tests/permission_tests.sh`
2. Run `pytest docs/coordination/tests/wrapper_tests.py`
3. Fix any failures
4. Add to CI/CD

**Expected outcome**: Validated system health

---

## Priority 4: Low (Nice to Have)

### 10. Clean Up Old Backups
**Problem**: 8.3MB backup file consuming space

**Solution**:
1. Create final archive
2. Delete `simple-agents/agent-system-standalone-backup-*.tar.gz`
3. Delete `simple-agents/old_backup/`

**Expected outcome**: Cleaner project structure

---

### 11. Update to GLM-4.7
**Problem**: Currently using GLM-4.6 or unspecified

**Solution**:
1. Update `ANTHROPIC_MODEL` environment variable to `glm-4.7`
2. Update default in `glm_direct.py`
3. Test to verify improvement

**Expected outcome**: Better coding performance (+12.4%)

---

### 12. Document Agent Workflows
**Problem**: Agent coordination patterns not documented

**Solution**:
1. Create `docs/coordination/workflows.md`
2. Document common multi-agent patterns
3. Include examples

**Expected outcome**: Easier onboarding and usage

---

## Summary

| Priority | Items | Focus |
|----------|-------|-------|
| 1 (Critical) | 3 | Fix broken wrappers |
| 2 (High) | 3 | Consolidate projects |
| 3 (Medium) | 3 | Add new capabilities |
| 4 (Low) | 3 | Cleanup and polish |

**Total**: 12 actionable recommendations

---

## Implementation Order

1. **Week 1**: Fix wrappers (Priority 1.1-1.3)
2. **Week 2**: Consolidate projects (Priority 2.4-2.6)
3. **Week 3**: Add capabilities (Priority 3.7-3.9)
4. **Week 4**: Cleanup (Priority 4.10-4.12)
