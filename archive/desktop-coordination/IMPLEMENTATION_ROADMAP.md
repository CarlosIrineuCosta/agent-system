# Implementation Roadmap
**Generated**: 2025-12-31
**Source**: Investigation findings and recommendations

---

## Overview

This roadmap converts investigation findings into actionable implementation steps.

---

## Week 1: Fix Broken Wrappers

### Day 1-2: Codex Direct API
**Task**: Implement Codex direct HTTP calls

**Steps**:
1. Research Codex API documentation
2. Create `scripts/codex_direct.py` following glm_direct.py pattern
3. Test with simple prompt
4. Replace subprocess calls in codex_wrapper.py

**Success criteria**: Codex works without TTY

### Day 3-4: Gemini Direct API
**Task**: Implement Gemini direct HTTP calls

**Steps**:
1. Research Gemini API (OpenAI-compatible endpoint)
2. Create `scripts/gemini_direct.py`
3. Test with simple prompt
4. Replace subprocess calls in gemini_wrapper.py

**Success criteria**: Gemini works without arg limit issues

### Day 5: Integrate Expect Wrappers
**Task**: Add expect scripts as fallback

**Steps**:
1. Create `scripts/wrappers/` directory
2. Copy expect scripts from simple-agents/
3. Add README with usage instructions
4. Update permissions if needed

**Success criteria**: Expect scripts available as backup

---

## Week 2: Project Consolidation

### Day 6-7: Merge Useful Files
**Task**: Consolidate agent-system-standalone

**Steps**:
1. Compare hooks for unique features
2. Merge any useful documentation
3. Archive agent-system-standalone to backup/
4. Update all references

**Success criteria**: agent-coordinator is sole project

### Day 8-9: Update Deprecated References
**Task**: Clean up 176 outdated references

**Steps**:
1. Review deprecated_references.json
2. Bulk replace "/dev" with current commands
3. Remove unused Cline/KiloCode references
4. Verify no breakage

**Success criteria**: No outdated references remain

### Day 10: Clean Up Backups
**Task**: Remove old backup files

**Steps**:
1. Create final archive at /backup/
2. Delete 8.3MB backup file
3. Delete old_backup/ directory
4. Update .gitignore

**Success criteria**: 8MB+ space saved

---

## Week 3: Add New Capabilities

### Day 11-12: Auto-Documentation Hook
**Task**: Implement and enable auto-doc

**Steps**:
1. Review auto_doc_hook design
2. Copy to hooks/auxiliary/
3. Configure in settings.local.json
4. Test with file edits
5. Customize doc mapping

**Success criteria**: Documentation auto-updates

### Day 13-14: MiniMax Integration
**Task**: Add MiniMax M2.1 agent

**Steps**:
1. Get MiniMax API key
2. Copy minimax_direct.py to scripts/
3. Test with prompt
4. Add to agent routing config
5. Update multi_llm_coordinator

**Success criteria**: Fourth agent operational

### Day 15: Claude Skills Installation
**Task**: Install coordination skills

**Steps**:
1. Create ~/.claude/skills/user/coordination-skills/
2. Copy all skill files
3. Test each skill
4. Customize for workflow

**Success criteria**: Skills available in Claude Code

---

## Week 4: Testing and Polish

### Day 16-17: Run Test Suite
**Task**: Validate system health

**Steps**:
1. Run permission_tests.sh
2. Run wrapper_tests.py with pytest
3. Fix any failures
4. Document test results

**Success criteria**: All tests pass

### Day 18: Tighten Permissions
**Task**: Secure permission system

**Steps**:
1. Scope python3 wildcard
2. Remove chmod from auto-approve
3. Add agent wrapper permissions
4. Test all operations

**Success criteria**: Safer, scoped permissions

### Day 19: Upgrade to GLM-4.7
**Task**: Switch to latest GLM

**Steps**:
1. Update ANTHROPIC_MODEL to glm-4.7
2. Update glm_direct.py default
3. Test with coding tasks
4. Measure improvement

**Success criteria**: Using GLM-4.7 with better results

### Day 20: Documentation
**Task**: Document workflows and usage

**Steps**:
1. Create workflows.md
2. Document multi-agent patterns
3. Add troubleshooting guide
4. Update main README

**Success criteria**: Complete documentation

---

## Milestones

| Week | Milestone | Deliverable |
|------|-----------|-------------|
| 1 | Wrappers Fixed | All agents work non-interactively |
| 2 | Projects Consolidated | Single canonical project |
| 3 | New Capabilities | Auto-doc, MiniMax, Skills |
| 4 | Production Ready | Tested, documented, secured |

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Codex API unavailable | Keep expect wrapper fallback |
| Breaking changes | Test before deploying |
| Permission issues | Scope gradually |
| Documentation gaps | Document as we go |

---

## Success Metrics

- All 4 agents (GLM, Codex, Gemini, MiniMax) working
- Zero TTY-related errors
- Auto-documentation functional
- All tests passing
- Single project maintained
- Complete documentation

---

## Next Actions

1. **Today**: Research Codex API documentation
2. **Tomorrow**: Begin Codex direct API implementation
3. **This week**: Complete wrapper fixes

**Status**: Ready to implement
