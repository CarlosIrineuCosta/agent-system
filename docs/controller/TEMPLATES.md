# PROMPT TEMPLATES REFERENCE

Quick-reference templates for Desktop Claude + Claude Code coordination workflow.

---

## 1. PROJECT KICKOFF TEMPLATE

**Use when:** Starting new checkpoint-based project

**Paste to Desktop Claude:**

```
I'm working on [PROJECT_NAME].

Current state: [1-2 sentence description]

Goal: [specific objective]

Create checkpoint-based prompts for Claude Code to:
1. [First analysis/task]
2. [Second analysis/task]  
3. [Implementation/test]

Each checkpoint should:
- Output to: \\100.106.201.33\cdc\Storage\projects\[project]\docs\coordination\
- Have clear success criteria
- Stop for review before continuing

Start with Checkpoint 1: [name]
```

**Example:**
```
I'm working on agent-coordinator.

Current state: Basic multi-LLM orchestration working, but no visibility.

Goal: Build real-time agent monitoring system.

Create checkpoint-based prompts for Claude Code to:
1. Analyze current status tracking capabilities
2. Design monitoring architecture
3. Implement basic terminal dashboard

Each checkpoint should:
- Output to: \\100.106.201.33\cdc\Storage\projects\agent-coordinator\docs\coordination\
- Have clear success criteria
- Stop for review before continuing

Start with Checkpoint 1: Status Tracking Analysis
```

---

## 2. CHECKPOINT PROMPT TEMPLATE

**Use when:** Desktop Claude generates prompts for Claude Code

**Structure:**

```markdown
# CHECKPOINT N: [Clear, Descriptive Name]

## CONTEXT
[What we've accomplished so far]
[Key decisions made in previous checkpoints]
[Relevant files/information available]

## TASK
[Single, specific, bounded objective]

## OUTPUT FORMAT
Create: \\100.106.201.33\cdc\Storage\projects\[project]\docs\coordination\CHECKPOINT_N_[NAME].md

Include:
1. [Specific section name and what it should contain]
2. [Specific section name and what it should contain]
3. [Specific section name and what it should contain]

## CONSTRAINTS
- NO code dumps (only pseudocode or skeleton)
- Use diagrams where possible (mermaid format)
- Focus on WHAT not HOW
- Maximum [X] pages
- [Other specific limitations]

## SUCCESS CRITERIA
- [ ] [Measurable criterion 1]
- [ ] [Measurable criterion 2]
- [ ] [Measurable criterion 3]
```

**Example:**
```markdown
# CHECKPOINT 2: State Management Design

## CONTEXT
Checkpoint 1 revealed that environment is configured via ~/.config/secrets/ai.env and GLM is accessible via Z.ai Anthropic-compatible endpoint. We need proper lifecycle management with start/stop commands.

## TASK
Design state management system for agent coordinator with clear lifecycle states.

## OUTPUT FORMAT
Create: \\100.106.201.33\cdc\Storage\projects\agent-coordinator\docs\coordination\CHECKPOINT_2_STATE.md

Include:
1. State diagram (mermaid) showing transitions
2. State schema (JSON format)
3. Startup sequence (numbered steps)
4. Stop sequence (numbered steps)
5. Environment checks list

## CONSTRAINTS
- NO implementation code (only skeleton/pseudocode)
- Use mermaid for state diagram
- Focus on WHAT each state does, not HOW to implement
- Maximum 5 pages

## SUCCESS CRITERIA
- [ ] Clear state transitions defined (STOPPED ↔ ACTIVE)
- [ ] State file schema includes all necessary fields
- [ ] Startup checks verify environment properly
- [ ] Stop sequence includes cleanup and reporting
```

---

## 3. CHECKPOINT REVIEW TEMPLATE

**Use when:** Returning to Desktop Claude after CC completes checkpoint

**Paste to Desktop Claude:**

```
Checkpoint [N] complete.

[Paste key findings, or say "see attached" and attach the MD file]

Key findings:
- [Finding 1]
- [Finding 2]

Issues found:
- [Issue 1 if any]
- [Issue 2 if any]

Questions:
1. [Decision needed]
2. [Clarification needed]

Ready for Checkpoint [N+1]?
```

**Example:**
```
Checkpoint 2 complete.

See attached CHECKPOINT_2_STATE.md

Key findings:
- State management design looks solid
- Startup checks comprehensive
- 30-second timeout for agent cleanup

Issues found:
- None - design approved

Questions:
1. Should VERSION file be external or embedded in code?
2. Confirmed GitHub repo path?

Ready for Checkpoint 3 (Deployment Model)?
```

---

## 4. COURSE CORRECTION TEMPLATE

**Use when:** Checkpoint reveals need to change direction

**Paste to Desktop Claude:**

```
Checkpoint [N] revealed unexpected issue: [description]

Original plan was: [what we thought would happen]

Actual situation: [what we discovered]

Should we:
A. [Option 1 - description]
B. [Option 2 - description]  
C. [Other approach]

If [chosen option], what should Checkpoint [N+1] focus on?
```

**Example:**
```
Checkpoint 1 revealed unexpected issue: We're not actually using direct GLM API

Original plan was: Fix glm_direct.py to use GLM_API_KEY

Actual situation: We're using Z.ai's Anthropic-compatible endpoint with ANTHROPIC_AUTH_TOKEN

Should we:
A. Update all scripts to use the Z.ai endpoint pattern
B. Keep both methods (direct API + Z.ai endpoint)
C. Standardize on Z.ai only and remove direct API code

If A, what should Checkpoint 2 focus on?
```

---

## 5. MULTI-AGENT COORDINATION TEMPLATE

**Use when:** Task requires multiple agents working together

**Paste to Desktop Claude:**

```
I need to coordinate multiple agents for: [objective]

Agents available:
- GLM: [capabilities]
- Codex: [capabilities]
- Gemini: [capabilities]

Task breakdown:
1. [Subtask 1] → Which agent?
2. [Subtask 2] → Which agent?
3. [Subtask 3] → Which agent?

Verification strategy: [how to check results are consistent]

Create coordination checkpoint prompt for Claude Code.
```

**Generated prompt should look like:**

```markdown
# CHECKPOINT N: [Multi-Agent Task Name]

## TASK
Coordinate agents to accomplish: [objective]

## AGENT ASSIGNMENTS
- GLM-4.7: [specific subtask with clear deliverable]
- Codex: [specific subtask with clear deliverable]
- Gemini: [specific subtask with clear deliverable]

## COORDINATION FLOW
1. GLM produces: [deliverable] → .agents/output/glm/[filename]
2. Codex reviews: [what aspect] → .agents/output/codex/[filename]
3. Gemini analyzes: [large context task] → .agents/output/gemini/[filename]
4. Aggregate results → .agents/coordinated/[final_output]
5. Report summary to: CHECKPOINT_N_[NAME].md

## FILE STRUCTURE
```
.agents/
├── output/
│   ├── glm/[task_name].txt
│   ├── codex/[review_results].txt
│   └── gemini/[analysis].txt
└── coordinated/
    └── [final_aggregated_output].md
```

## SUCCESS CRITERIA
- [ ] GLM output meets [specific criteria]
- [ ] Codex verification passes [specific checks]
- [ ] Gemini analysis covers [specific aspects]
- [ ] No conflicts between agent outputs
- [ ] Final aggregation is coherent and actionable
```

---

## 6. STATUS UPDATE TEMPLATE

**Use when:** End of session or major milestone

**Paste to Desktop Claude:**

```
Session ending. Please update status.

Completed checkpoints:
- Checkpoint [N]: [name]
- Checkpoint [N+1]: [name]

Still pending:
- [Task from TODO.md]
- [Task from TODO.md]

Update SYSTEM_STATUS.md and TODO.md
```

**Desktop Claude will:**
1. Read completed checkpoints
2. Update SYSTEM_STATUS.md with progress
3. Update TODO.md with completed/remaining tasks
4. Provide summary for next session

---

## 7. SESSION RESUME TEMPLATE

**Use when:** Starting work after break

**Paste to Desktop Claude:**

```
Resuming work on [project].

Last session ended at: Checkpoint [N]

Please read:
- SYSTEM_STATUS.md
- TODO.md  
- Last checkpoint: CHECKPOINT_[N]_[NAME].md

What's the next priority task?
```

**Desktop Claude will:**
1. Read status files
2. Review last checkpoint
3. Check TODO.md
4. Recommend next checkpoint
5. Generate prompt when you're ready

---

## 8. EMERGENCY STOP TEMPLATE

**Use when:** Something is going wrong, need to halt

**Paste to Desktop Claude:**

```
STOP - issue detected.

Problem: [what went wrong]

Current checkpoint: [N]

Affected files: [list]

Should we:
1. Rollback checkpoint [N]
2. Fix and continue
3. Skip to different task

Please advise recovery strategy.
```

---

## 9. FILE LOCATION ENFORCEMENT

**Add to ANY checkpoint prompt when file writes are involved:**

```markdown
## CRITICAL FILE LOCATION RULES

ALL files must be written to explicitly specified paths.

ALLOWED:
- docs/coordination/CHECKPOINT_*.md
- docs/analysis/*.md
- .agents/output/
- .agents/coordinated/

FORBIDDEN:
- Project root (no *.md files at /)
- README.md, LICENSE, VERSION (protected files)
- Any location not explicitly specified in this prompt

If unsure where a file should go: ASK before creating it.
```

---

## 10. MINIMAL COMPLEXITY CONSTRAINT

**Add when you want simple/fast results:**

```markdown
## ADDITIONAL CONSTRAINT: MINIMAL IMPLEMENTATION

Keep this as simple as possible:
- Use basic print() statements (no fancy libraries)
- Core functionality only
- Skip polish and optimization  
- Get it working first, enhance later
- Maximum [X] lines of code per file
```

---

## TEMPLATE SELECTION GUIDE

| Situation | Use Template |
|-----------|-------------|
| Starting new project | #1 Project Kickoff |
| Desktop generating prompt for CC | #2 Checkpoint Prompt |
| CC finished, back to Desktop | #3 Checkpoint Review |
| Unexpected discovery | #4 Course Correction |
| Multi-agent task needed | #5 Multi-Agent Coordination |
| End of session | #6 Status Update |
| Beginning of session | #7 Session Resume |
| Something breaking | #8 Emergency Stop |

---

## CUSTOMIZATION NOTES

**Adjust these per project:**
- File paths (\\100.106.201.33\cdc\Storage\projects\[YOUR_PROJECT]\)
- Number of checkpoints (start with 3-5 for small projects)
- Constraints (code vs no-code, length limits, diagram requirements)
- Available agents (GLM, Codex, Gemini, or just Claude Code)

**Keep consistent:**
- Checkpoint naming (CHECKPOINT_N_TOPIC.md)
- Output locations (docs/coordination/)
- Review cycle (complete → evaluate → approve → next)
- Single checkpoint per prompt (don't combine)

---

## ANTI-PATTERNS TO AVOID

❌ **Vague objectives**
```
Bad: "Improve the system"
Good: "Add real-time status monitoring for active agents"
```

❌ **Missing file paths**
```
Bad: "Create documentation"
Good: "Create: \\...\docs\coordination\CHECKPOINT_3_DEPLOY.md"
```

❌ **No success criteria**
```
Bad: [No criteria section]
Good: "- [ ] Monitoring shows which agents are active"
```

❌ **Too many deliverables**
```
Bad: 15 different things in one checkpoint
Good: 3-5 related deliverables per checkpoint
```

❌ **Scope creep mid-checkpoint**
```
Bad: "Also add this feature I just thought of"
Good: "Add to TODO.md, address in next checkpoint"
```
