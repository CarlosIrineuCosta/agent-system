# Conversation Handoff - Agent Coordinator Investigation
**Date**: 2026-01-01  
**From**: Claude Desktop (this conversation)  
**To**: Next Claude instance  
**Context**: Multi-agent system investigation and cleanup

---

## CONVERSATION CONTEXT

### What We're Working On
Charles is rebuilding his multi-LLM agent orchestration system for photography/magazine business (WASEmag). System coordinates between Claude Code, GLM, Codex, Gemini, and now MiniMax for cost-effective AI workflows.

### Current State
- **Three separate agent projects exist** (need reconciliation)
- **Permission prompts issue** (Claude Code bash tool, not agent CLIs)
- **Some wrappers broken** (Codex needs TTY, Gemini has arg limits)
- **Documentation scattered** across projects
- **Outdated references** to Cline, KiloCode need cleanup

### What Charles Wants
1. Fix permission system so it stops asking
2. Deploy agents to investigate/fix themselves (don't do it manually)
3. Strong auto-documentation system with hooks/skills
4. Integrate MiniMax M2.1 (like GLM pattern)
5. Use GLM 4.6 for cheaper tasks (4.7 has deployment limits)
6. Clean separation between Desktop coordination and Code execution

---

## KEY DOCUMENTS TO READ

**ALL LOCATED IN**: `\\100.106.201.33\cdc\Storage\projects\agent-coordinator\docs\`

### Essential Reading (Read First)
1. **DESIGN_DECISIONS.md** - System architecture and current decisions
2. **desktop-coordination/QUESTIONS_FOR_CHARLES.md** - Questions I asked
3. **desktop-coordination/INVESTIGATION_PLAN.md** - Agent deployment plan (16 tasks)
4. **SYSTEM_STATUS.md** - Authoritative task list (SSOT)

### Background Context
5. **architecture.md** - System overview with diagrams
6. **INDEX.md** - Documentation map
7. **coordination/SUMMARY.md** - Checkpoint summaries

### Investigation Results (from Claude Code)
8. **desktop-coordination/AGENT_PERMISSION_PATTERNS_2025-12-31.md** - Test results
9. **desktop-coordination/AGENT_SYSTEM_STATUS_2026-01-01.md** - Status report (has Desktop FS notes - ignore those per Charles)

### Charles's Answers (CHECK IF COMPLETED)
**Location**: Same directory where QUESTIONS_FOR_CHARLES.md is

**Expected file**: 
- `ANSWERS_FROM_CHARLES.md` (if he created separate file)
- OR inline edits to `QUESTIONS_FOR_CHARLES.md`

---

## CRITICAL RULES (FROM CHARLES)

### 1. File Writing Restrictions
- ❌ NEVER write to project root
- ❌ NEVER write to `config/*.json`, `scripts/*.py`, `hooks/*.py`
- ✅ Only write to `docs/coordination/*`
- ✅ Runtime data goes to `.agents/*` (but that's for the system, not our analysis)

### 2. Agent Philosophy
- ❌ DON'T do everything manually
- ✅ DO deploy tasks to GLM (cheap) and Codex (research/code)
- ✅ Desktop Claude coordinates, agents execute, Claude Code implements
- ✅ Use investigation plan structure (6 phases, 16 tasks)

### 3. Separation of Concerns
- Desktop coordination docs: `docs/desktop-coordination/`
- Agent operational docs: `docs/coordination/`
- Don't mix them

### 4. Network Storage Access
- Use Filesystem tool with `\\100.106.201.33\cdc\Storage\projects\` paths
- Bash tool won't work (containerized, no network mounts)
- Z: drive is Windows-side only

### 5. Don't Guess - Research
- Use web_search for current info (GLM versions, MiniMax API, etc.)
- Deploy Codex for deep research
- Don't make assumptions

---

## THREE AGENT PROJECTS (NEED RECONCILIATION)

### Project 1: agent-coordinator (Most Developed)
**Location**: `\\100.106.201.33\cdc\Storage\projects\agent-coordinator\`

**Status**: Production-ready core features
- Has hooks, quality gates, routing
- GLM direct HTTP working (`scripts/glm_direct.py`)
- Codex/Gemini wrappers broken (TTY/arg limit issues)
- Full documentation in `docs/`

### Project 2: simple-agents/agent-new
**Location**: `\\100.106.201.33\cdc\Storage\projects\simple-agents\agent-new\`

**Status**: Has working expect wrappers
- Contains `.exp` files for automation
- Less structured than agent-coordinator
- May have pieces we need

### Project 3: simple-agents/agent-system-standalone
**Location**: `\\100.106.201.33\cdc\Storage\projects\simple-agents\agent-system-standalone\`

**Status**: Unknown purpose (Charles doesn't know why it exists)
- Has full structure (commands, hooks, scripts)
- Contains backup tar.gz from Dec 8, 2025
- Needs investigation

**Question for Charles**: Which is canonical? Should we merge?

---

## PERMISSION ISSUE - EXPLAINED

### The Confusion
Charles sees prompts like:
```
Bash command: openai api chat.completions.create...
Do you want to proceed?
  1. Yes
  2. Yes, and don't ask again for openai commands in [project]
```

### The Reality
These prompts are **FROM CLAUDE CODE'S BASH TOOL**, not from the agent CLIs.

### The Solution
Select option 2 ("don't ask again") - adds to `.claude/settings.local.json`:
```json
{
  "permissions": {
    "allow": ["Bash(openai:*)", "Bash(gemini:*)", ...]
  }
}
```

### What Expect Scripts Are Actually For
Handling interactive prompts **WITHIN the agent tools themselves** (like "Continue? y/n"), NOT Claude Code permissions.

---

## AGENT ACCESS METHODS

| Agent | Method | Status | Notes |
|-------|--------|--------|-------|
| GLM | Direct HTTP via Z.ai | ✅ Working | Reference pattern in `scripts/glm_direct.py` |
| Codex | CLI tool `codex` | ⚠️ Broken | Needs TTY (stdin requirement) |
| Gemini | CLI tool `gemini` | ⚠️ Broken | Arg length limit for large context |
| MiniMax | To be implemented | 🔨 Pending | Use GLM pattern, Anthropic-compatible API |

**Important**: Charles uses CLI subscriptions, NOT APIs (to avoid per-token costs)

---

## WHAT CHARLES WANTS INVESTIGATED

### High Priority
1. Fix permission system (create safe defaults)
2. Integrate MiniMax M2.1 (Anthropic-compatible API)
3. Strong auto-documentation hook system
4. Clean up Cline/KiloCode references (not used anymore)
5. Reconcile three agent projects

### Research Needed
6. GLM 4.6 vs 4.7 differences (Charles says 4.7 has "two deployment" limit)
7. Skills system proposals (we're underutilizing it)
8. What are /dev and /api commands? (not found in current project)
9. What is agent-system-standalone for?

### Medium Priority
10. Fix Codex wrapper (TTY issue)
11. Fix Gemini wrapper (arg limit)
12. Test expect scripts integration

---

## INVESTIGATION PLAN STATUS

### Created Documents
✅ `INVESTIGATION_PLAN.md` - 16 tasks across 6 phases  
✅ `QUESTIONS_FOR_CHARLES.md` - 8 questions needing answers  
✅ `DESIGN_DECISIONS.md` - Architecture SSOT

### Awaiting
⏳ Charles's answers to questions  
⏳ Approval to execute investigation  
⏳ Clarification on canonical project

### Ready to Deploy (Once Approved)
**Phase 1**: Discovery tasks (GLM)
- File inventory
- Reference discovery (Cline/KiloCode)
- Command inventory
- Project comparison

**Phase 2**: Research tasks (Codex)
- GLM 4.6 vs 4.7
- MiniMax API docs
- Skills recommendations

**Phases 3-6**: Analysis, Implementation, Testing

---

## CURRENT AGENT ROUTING (FROM config/agent_routing.json)

```json
{
  "routing_rules": {
    "architecture": "claude",
    "implementation": "glm",
    "security": "codex",
    "large_context": "gemini",
    "documentation": "glm",
    "testing": "glm"
  }
}
```

**Rationale**: Use GLM for cheap tasks, Claude for complex reasoning, Codex for security/review

---

## CHARLES'S PREFERENCES (FROM userPreferences)

### Communication Style
- ❌ NO emojis
- ❌ NO "genial" or "brilliant" (be realistic)
- ❌ NO "You're absolutely right!" (just fix it)
- ✅ Long, detailed answers (except objective questions)
- ✅ Criticize code/ideas freely
- ✅ Ask questions before acting

### Technical
- Windows 11 PC, 64GB RAM, RTX 3080Ti
- Prefers Python and React
- Dark themes, Montserrat/Roboto fonts
- Sophisticated, not "baby colors"

### Work Context
- 58-year-old Brazilian photographer/developer
- Relaunching WASEmag (international photography magazine)
- Building AI systems for law firms
- Multi-LLM orchestration expertise
- 20+ years photography, extensive Lightroom archive

---

## IMPORTANT: WHAT NOT TO DO

### DON'T
- ❌ Write to project root or core system files
- ❌ Make assumptions about GLM versions (research it)
- ❌ Execute tasks manually (deploy to agents instead)
- ❌ Mix Desktop coordination docs with Agent operational docs
- ❌ Use Cline or KiloCode (outdated)
- ❌ Try to access bash tool for network files (use Filesystem tool)
- ❌ Recreate Serena MCP (different purpose)

### DO
- ✅ Read DESIGN_DECISIONS.md first
- ✅ Check if Charles answered questions
- ✅ Deploy investigation tasks to GLM/Codex
- ✅ Use Filesystem tool for network storage
- ✅ Research before recommending (web_search)
- ✅ Follow investigation plan structure
- ✅ Keep Desktop/Agent concerns separate

---

## IMMEDIATE NEXT STEPS FOR NEW CLAUDE

### Step 1: Read Context
1. Read DESIGN_DECISIONS.md (full context)
2. Read QUESTIONS_FOR_CHARLES.md
3. Check if Charles answered (inline or separate file)

### Step 2: Assess Status
- Did Charles approve investigation plan?
- Are answers sufficient to proceed?
- Any new instructions?

### Step 3: Act Accordingly

**If answers exist and approved**:
- Execute Phase 1 of investigation (deploy to GLM)
- Monitor results
- Proceed through phases

**If questions remain**:
- Synthesize what's unclear
- Ask Charles concisely
- Wait for guidance

**If Charles gave different direction**:
- Follow new instructions
- Update plans as needed

---

## FILES THAT NEED UPDATES (PENDING INVESTIGATION)

### Likely Updates After Investigation
1. `.claude/settings.local.json` - Permission list
2. `config/agent_routing.json` - Add MiniMax
3. `scripts/minimax_direct.py` - New file (create)
4. `hooks/core/auto_documentation.py` - New file (create)
5. Documentation cleanup (remove Cline/KiloCode references)

### Files to Create
- Auto-documentation hook + config
- MiniMax integration script
- Skills definitions (if recommended)
- Test suites for wrappers

---

## TOKEN BUDGET

**This conversation**: ~97k tokens used of 190k (still plenty)

**Reason for handoff**: Charles wants to preserve tokens that might expire, and conversation is getting long.

---

## CHARLES'S TONE

- Direct, no-nonsense
- Values realistic assessments over praise
- Appreciates when you catch your own mistakes
- Wants agents doing the work, not Claude manually
- Frustrated with over-complexity and over-engineering

---

## FINAL CHECKLIST FOR NEW CLAUDE

Before doing anything:
- [ ] Read DESIGN_DECISIONS.md
- [ ] Read QUESTIONS_FOR_CHARLES.md  
- [ ] Check for Charles's answers
- [ ] Read INVESTIGATION_PLAN.md
- [ ] Verify file access to `\\100.106.201.33\cdc\Storage\projects\`
- [ ] Understand Desktop vs Agent coordination separation
- [ ] Note: DON'T write to project root

Then ask Charles: "I've read the handoff. What should I do first?"

---

## USEFUL FILESYSTEM PATHS

**Network storage (use Filesystem tool)**:
```
\\100.106.201.33\cdc\Storage\projects\agent-coordinator\
\\100.106.201.33\cdc\Storage\projects\simple-agents\
```

**Documents to check**:
```
docs/DESIGN_DECISIONS.md
docs/desktop-coordination/QUESTIONS_FOR_CHARLES.md
docs/desktop-coordination/INVESTIGATION_PLAN.md
docs/SYSTEM_STATUS.md
```

**Charles's answers** (check if exists):
```
docs/desktop-coordination/ANSWERS_FROM_CHARLES.md
```

---

**Status**: HANDOFF READY  
**Next Claude Action**: Read context, check for answers, ask Charles what to do first
