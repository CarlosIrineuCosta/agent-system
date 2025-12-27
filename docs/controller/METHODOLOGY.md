# DESKTOP + CLAUDE CODE SUPERVISION METHODOLOGY

## What Worked - The Pattern

**The breakthrough:**
Charles uses Desktop Claude as **Director** and Claude Code as **Chief Engineer** in a checkpoint-based workflow that prevents hallucinations and maintains focus.

---

## THE METHODOLOGY

### Role Separation

**Desktop Claude (Director) - Strategic Layer**
- Creates structured prompts for Claude Code
- Defines checkpoints with clear deliverables
- Evaluates outputs against criteria
- Makes decisions at each checkpoint
- Maintains task list and big picture
- Prevents scope creep and hallucinations

**Claude Code (Chief Engineer) - Execution Layer**
- Executes tasks from Desktop's prompts
- Writes documentation to specified locations
- Reports results to checkpoint files
- Never invents new tasks
- Stays within defined boundaries

---

## THE WORKFLOW - Step by Step

### 1. CONVERSATION PREPARATION (Desktop)

**Opening message template:**

```
I'm working on [project]. 

Current goal: [one sentence]

Context files: [attach relevant MDs from /docs/coordination]

I need you to create structured prompts for Claude Code that:
1. [First objective]
2. [Second objective]
3. [Third objective]

Use checkpoint-based workflow. Each checkpoint should:
- Have ONE clear deliverable
- Output to: \\100.106.201.33\cdc\Storage\projects\[project]\docs\coordination\
- Stop and wait for my review before continuing
```

**Key principles:**
- Attach previous checkpoint files for context
- State what you want in bullet points
- Specify output location explicitly
- Request checkpoints, not one giant task

---

### 2. PROMPT GENERATION (Desktop Creates for CC)

**Desktop Claude will generate:**

```markdown
# CHECKPOINT N: [Task Name]

## CONTEXT
[What we know so far]

## TASK
[Specific, bounded objective]

## OUTPUT FORMAT
Create: \\100.106.201.33\cdc\Storage\projects\[project]\docs\coordination\CHECKPOINT_N_[NAME].md

Include:
1. [Specific section]
2. [Specific section]
3. [Specific section]

## CONSTRAINTS
- NO code dumps
- Use diagrams where possible
- Focus on WHAT not HOW
- Maximum [X] pages

## SUCCESS CRITERIA
- [ ] Criterion 1
- [ ] Criterion 2
```

**What makes this work:**
- ONE checkpoint per prompt
- Explicit file path (prevents root writes)
- Clear sections required
- Success criteria defined upfront
- Constraints prevent over-engineering

---

### 3. EXECUTION (Claude Code)

**Paste the checkpoint prompt to Claude Code.**

Claude Code:
1. Reads the prompt
2. Executes the bounded task
3. Writes output to specified location
4. Reports completion

**Your job:**
- Paste prompt
- Wait for completion
- Don't interrupt
- Don't add requirements mid-execution

---

### 4. EVALUATION (Back to Desktop)

**Return to Desktop Claude:**

```
Checkpoint N complete. 

[Paste key findings or attach the MD file]

Issues found:
- [Issue 1]
- [Issue 2]

Questions:
1. [Decision needed]
2. [Clarification needed]

Ready for next checkpoint?
```

**Desktop Claude will:**
- Evaluate results against criteria
- Identify gaps or problems
- Ask clarifying questions
- Generate next checkpoint prompt (if approved)

**Key decision points:**
- Approve and continue?
- Fix issues first?
- Change direction?

---

### 5. ITERATION

**Repeat steps 2-4 until objective complete.**

**Important patterns:**
- Each checkpoint builds on previous
- Context carried through file attachments
- Desktop maintains task list (TODO.md)
- CC never sees the full scope (prevents overwhelm)
- Human makes all strategic decisions

---

## CRITICAL SUCCESS FACTORS

### Why This Prevents Hallucinations

1. **Bounded tasks** - CC can't invent requirements
2. **Explicit outputs** - CC knows exactly what to produce
3. **Desktop evaluation** - Human + Director AI review every output
4. **Checkpoint gates** - No work proceeds without approval
5. **File-based handoff** - Results are tangible, reviewable

### Why This Maintains Focus

1. **One checkpoint at a time** - No distraction
2. **TODO.md as single source** - Clear priorities
3. **Desktop holds big picture** - CC doesn't need to
4. **Explicit file locations** - No "where should this go?" decisions
5. **Success criteria** - Clear definition of done

---

## WHEN TO USE THIS METHOD

**Good for:**
- ✅ Complex, multi-step projects
- ✅ System design and architecture
- ✅ Documentation generation
- ✅ Coordinated refactoring
- ✅ Research and analysis
- ✅ Building tools that build themselves

**Not needed for:**
- ❌ Simple one-off tasks
- ❌ Quick bug fixes
- ❌ Straightforward implementations
- ❌ Tasks you can explain in one sentence

---

## COMMON PITFALLS & SOLUTIONS

### Pitfall 1: Too Much in One Checkpoint
**Symptom:** Claude Code produces 50-page document
**Solution:** Break into smaller checkpoints (max 3-5 deliverables each)

### Pitfall 2: Lost Context Between Checkpoints  
**Symptom:** CC doesn't remember previous decisions
**Solution:** Always attach previous checkpoint files to Desktop prompts

### Pitfall 3: Files Written to Wrong Location
**Symptom:** MDs everywhere except /docs/coordination
**Solution:** Explicitly specify FULL file path in every prompt

### Pitfall 4: Scope Creep
**Symptom:** CC starts adding features you didn't ask for
**Solution:** Tighter constraints, clearer success criteria

### Pitfall 5: Hallucinated Requirements
**Symptom:** CC invents tasks not in prompt
**Solution:** Desktop reviews every output, rejects unauthorized work

---

## ADVANCED: AGENT COORDINATION MODE

**When to activate:**
When Desktop Claude needs to coordinate multiple Claude Code sessions or agents.

### The Pattern

```
Desktop Claude (Director)
    ↓ Creates prompts for
    ↓
Claude Code (Chief Engineer)
    ↓ Uses multi-LLM coordinator
    ↓
GLM/Codex/Gemini Agents
```

**Desktop's job:**
- Strategic planning
- Prompt generation
- Result evaluation
- Decision making

**Claude Code's job:**
- Execute prompts
- Coordinate agents (via multi_llm_coordinator.py)
- Aggregate results
- Report to checkpoints

**Agents' job:**
- Execute specific subtasks
- Write to .agents/ directories
- Return structured results

### Agent Coordination Checkpoint Template

```markdown
# CHECKPOINT N: [Multi-Agent Task]

## TASK
Coordinate agents to accomplish: [objective]

## AGENT ASSIGNMENTS
- GLM: [specific subtask]
- Codex: [specific subtask]
- Desktop verification: [what Desktop will check]

## COORDINATION FLOW
1. GLM produces: [deliverable] → .agents/output/glm/
2. Codex reviews: [what] → .agents/output/codex/
3. Aggregate results → .agents/coordinated/
4. Report to: CHECKPOINT_N_[NAME].md

## SUCCESS CRITERIA
- [ ] GLM output meets [criteria]
- [ ] Codex verification passes
- [ ] Final aggregation coherent
- [ ] No conflicts between agents
```

---

## TROUBLESHOOTING

### "Desktop Claude is being vague"
**Fix:** Be more specific in your opening message. Include exact deliverables wanted.

### "Claude Code is hallucinating"
**Fix:** Tighter constraints in prompt. Add explicit "DO NOT" list.

### "Lost track of what we're doing"
**Fix:** Read TODO.md. Attach SYSTEM_STATUS.md to Desktop conversation.

### "Can't find checkpoint files"
**Fix:** Always use full UNC path: `\\100.106.201.33\cdc\Storage\projects\...`

### "Too many open threads"
**Fix:** One checkpoint at a time. Don't start new work until previous is reviewed.

---

## METRICS FOR SUCCESS

You're doing it right when:
- ✅ Each checkpoint produces exactly what was asked
- ✅ No surprise files in project root
- ✅ Clear progression visible in docs/coordination/
- ✅ TODO.md accurately reflects remaining work
- ✅ You can walk away and resume easily
- ✅ No hallucinated features
- ✅ Minimal back-and-forth per checkpoint

---

## QUICK START CHECKLIST

Before starting new project with this method:

- [ ] Create `docs/coordination/` directory
- [ ] Create `TODO.md` with initial tasks
- [ ] Create `SYSTEM_STATUS.md` template
- [ ] Prepare opening message for Desktop Claude
- [ ] Have previous relevant docs ready to attach
- [ ] Know your specific file path (`\\100.106.201.33\...`)
- [ ] Clear 2-3 hours for focused session
- [ ] Open Desktop Claude and Claude Code side-by-side

---

## SESSION END PROCEDURE

**When stopping for the day:**

1. **In Claude Code:** Tell it to update TODO.md with current state
2. **In Desktop Claude:** Ask it to update SYSTEM_STATUS.md
3. **Save both files**
4. **Next session:** Start by reading both files, attach to Desktop

This ensures you can resume exactly where you left off.

---

## FILE ORGANIZATION

**Required structure:**
```
project/
├── docs/
│   ├── coordination/          # Checkpoint outputs
│   │   ├── CHECKPOINT_1_*.md
│   │   ├── CHECKPOINT_2_*.md
│   │   └── ...
│   ├── controller/            # This methodology framework
│   │   ├── METHODOLOGY.md
│   │   ├── TEMPLATES.md
│   │   └── EXAMPLES.md
│   ├── SYSTEM_STATUS.md       # Current state
│   └── TODO.md                # Task list
├── .claude/
│   └── agent-coordinator/     # Agent system (if used)
└── [project files]
```

**File naming:**
- `CHECKPOINT_N_TOPIC.md` - Sequential checkpoint outputs
- `SYSTEM_STATUS.md` - Living document, update after major milestones
- `TODO.md` - Master task list, update constantly

---

## THE META-LOOP

This methodology is self-referential:
- Used Desktop+CC coordination to build agent coordination system
- Used agent coordination system to document Desktop+CC coordination  
- Result: A framework for using AI to build AI systems

**The beautiful recursion:**
You're using the pattern to document the pattern while building systems that use the pattern.

---

## FINAL NOTES

**This methodology works because:**
1. Clear role separation (Director vs Engineer)
2. Bounded tasks prevent overwhelm
3. Checkpoints create review points
4. Human stays in control
5. File-based handoffs are auditable

**Remember:**
- Desktop thinks strategically
- Code executes tactically  
- You decide everything important
- Checkpoints prevent runaway work
- TODO.md is the single source of truth
