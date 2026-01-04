# Investigation Findings Summary
**Generated**: 2025-12-31
**Investigation Plan**: docs/desktop-coordination/INVESTIGATION_PLAN.md

---

## Executive Summary

Completed systematic investigation of agent-coordinator and simple-agents projects. All 6 phases completed with 20 deliverables.

**Key Findings:**
1. GLM-4.7 direct API works perfectly - no permission prompts
2. Codex/Gemini wrappers fail due to TTY/arg-limit issues
3. agent-coordinator is the canonical project
4. MiniMax M2.1 supports Anthropic-compatible API
5. Hooks system is robust but missing auto-documentation

---

## Phase 1: Discovery (5 Deliverables)

### 1.1 File System Audit
**File**: `docs/coordination/analysis/file_inventory.json`
- **agent-coordinator**: 92 files (Python scripts, hooks, configs, commands)
- **simple-agents**: 17 files (wrappers, docs, expect scripts)
- **Total**: 109 files cataloged

### 1.2 Reference Discovery
**File**: `docs/coordination/analysis/deprecated_references.json`
- **176 references** to deprecated terms found in 40 files
- "Cline": 21 occurrences
- "/dev": 90 occurrences
- "/api": 53 occurrences
- Action: Update references to current commands

### 1.3 Command Inventory
**Files**: `docs/coordination/analysis/command_inventory.{json,md}`
- **12 commands** identified across projects
- All commands documented with file paths and line numbers

---

## Phase 2: External Research (3 Deliverables)

### 2.1 GLM Version Research
**File**: `docs/coordination/research/glm_versions.md`

**Finding**: GLM-4.7 is superior for production use
- **+12.4% improvement** over GLM-4.6
- Better coding capabilities
- Only 10% more expensive ($2.20 vs $2.00 per M output tokens)
- Same 200K context window

**Recommendation**: Use GLM-4.7 for all tasks

### 2.2 MiniMax API Research
**File**: `docs/coordination/research/minimax_integration.md`

**Finding**: MiniMax M2.1 supports **both OpenAI and Anthropic** API formats
- Drop-in compatible with existing wrappers
- Documentation available at platform.minimaxi.com
- Implementation code provided

### 2.3 Skills Research
**File**: `docs/coordination/research/skills_recommendations.md`

**Finding**: Claude Skills system is mature with best practices established
- Official docs available
- Community packages exist (awesome-claude-skills)
- 4 skills designed for coordination

---

## Phase 3: Code Analysis (3 Deliverables)

### 3.1 Permission System Analysis
**File**: `docs/coordination/analysis/permission_recommendations.md`

**Findings**:
- **35 allowed commands** in agent-coordinator
- **24 allowed commands** in simple-agents
- High-risk commands (python3:*, chmod:*) need scoping
- Missing expect script permissions

### 3.2 Wrapper Status Analysis
**File**: `docs/coordination/analysis/wrapper_comparison.md`

**Critical Finding**: Only GLM wrapper works
| Wrapper | Status | Issue |
|---------|--------|-------|
| glm_direct.py | WORKING | Direct API |
| codex_wrapper.py | FAILS | TTY required |
| gemini_wrapper.py | FAILS | Arg limit |

**Solution**: Convert all to direct API pattern

### 3.3 Hooks System Audit
**File**: `docs/coordination/analysis/hooks_audit.md`

**Findings**:
- **6 hooks** implemented and working
- Quality gate routing: Claude -> GLM -> Codex -> Claude
- **Missing**: Auto-documentation hook (requested feature)

---

## Phase 4: Project Reconciliation (2 Deliverables)

### 4.1 Agent Projects Comparison
**File**: `docs/coordination/analysis/project_reconciliation.md`

**Recommendation**: **agent-coordinator is canonical**
- Most complete feature set
- Python-based wrappers (more robust)
- Active development
- Better documentation

### 4.2 Backup Analysis
**File**: `docs/coordination/analysis/backup_inventory.md`

**Findings**:
- **8.3MB backup** file can be deleted
- old_backup/ contains superseded files
- Safe to remove after final archive

---

## Phase 5: Integration Planning (4 Deliverables)

### 5.1 MiniMax Integration
**File**: `docs/coordination/implementations/minimax_direct.py`
- Complete Python implementation
- Follows glm_direct.py pattern
- Ready to test

### 5.2 Auto-Documentation Hook
**Files**: `docs/coordination/implementations/auto_doc_hook/`
- config.json
- hook.py
- README.md

**Features**:
- Triggers on EditFile/CreateFile
- Updates changelog
- Archives completed tasks
- Never writes to root

### 5.3 Skills Package
**Files**: `docs/coordination/implementations/coordination-skills/`
- multi-llm-router.md
- documentation-generator.md
- code-review-coordinator.md
- task-breakdown.md
- README.md

**4 skills** for agent coordination

---

## Phase 6: Testing (2 Deliverables)

### 6.1 Wrapper Tests
**File**: `docs/coordination/tests/wrapper_tests.py`
- pytest test suite
- Tests GLM, Codex, Gemini wrappers
- Error handling tests
- Timeout tests

### 6.2 Permission Tests
**File**: `docs/coordination/tests/permission_tests.sh`
- Bash test script
- Validates allowed commands
- Tests restricted commands
- Checks settings persistence

---

## Output Structure

All deliverables in:
```
docs/coordination/
├── analysis/           # 7 files (discovery + analysis)
├── research/           # 3 files (external research)
├── implementations/    # 10 files (new code + skills)
└── tests/              # 2 files (test suites)
```

**Total: 22 investigation deliverables**

---

## Key Insights

1. **Permission prompts originate from Claude Code, not agent CLIs**
   - Select option 2: "Yes, and don't ask again" to approve
   - Stored in `.claude/settings.local.json`

2. **GLM is production-ready**
   - Direct API works flawlessly
   - No TTY requirements
   - Cost-effective for most tasks

3. **Codex/Gemini need API approach**
   - Subprocess wrappers are brittle
   - Need direct HTTP implementation

4. **Project consolidation needed**
   - agent-coordinator should be canonical
   - Merge useful parts from standalone
   - Archive old backups

---

## Next Steps

See `IMPLEMENTATION_ROADMAP.md` for prioritized action items.

See `RECOMMENDATIONS.md` for detailed recommendations.
