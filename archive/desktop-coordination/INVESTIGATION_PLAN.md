# Agent-Based Investigation & Deployment Plan
**Date**: 2026-01-01
**Purpose**: Systematic investigation using GLM, Codex, and agent coordination

---

## INVESTIGATION PHILOSOPHY

**Principle**: Claude Desktop coordinates, agents execute, Claude Code implements.

**NOT**: Desktop Claude doing everything manually
**YES**: Desktop Claude deploying investigative tasks to agents

---

## PHASE 1: DISCOVERY (Use GLM - Cheap)

### Task 1.1: File System Audit
**Agent**: GLM
**Prompt**:
```
Search the following directories and create a comprehensive inventory:
- \\100.106.201.33\cdc\Storage\projects\agent-coordinator
- \\100.106.201.33\cdc\Storage\projects\simple-agents

For each project, list:
1. All .md files in root and subdirectories
2. All command definitions (in commands/ directories)
3. All configuration files (.json, .yml, .env.example)
4. All Python scripts
5. All bash/shell scripts
6. All expect scripts (.exp files)

Output format: Structured JSON with full paths, file sizes and creation/modification dates.
Save to: /docs/coordination/analysis/file_inventory.json  -- folder /docs/coordination/ already exists, create /analysis inside of them
```

**Deliverable**: Complete file inventory

---

### Task 1.2: Reference Discovery
**Agent**: GLM
**Prompt**:
```
Search all text files in agent-coordinator and simple-agents for references to:
- "Cline"
- "KiloCode"
- "cline-cli"
- "/dev"
- "/api"

For each match, provide:
- File path
- Line number
- Context (3 lines before and after)

Output to: docs/coordination/analysis/deprecated_references.json
```

**Deliverable**: List of outdated references to clean up

---

### Task 1.3: Command Inventory
**Agent**: GLM
**Prompt**:
```
Extract all slash command definitions from:
- agent-coordinator/commands/*.md
- simple-agents/*/commands/*.md

For each command, document:
- Command name
- Purpose (from file content)
- Dependencies
- Current status (working/broken)

Output to: docs/coordination/analysis/command_inventory.md
```

**Deliverable**: Complete command reference

---

## PHASE 2: EXTERNAL RESEARCH (Use Codex - Web Access)

### Task 2.1: GLM Version Research
**Agent**: Codex
**Prompt**:
```
Research GLM-4 API differences:
1. Search Z.ai documentation for GLM-4.6 vs GLM-4.7
2. Find deployment limits, request limits, token limits
3. Identify which version is better for documentation tasks
4. Check pricing differences

Sources to check:
- https://z.ai/docs
- https://open.bigmodel.cn (GLM official docs)

Output structured findings to: docs/coordination/research/glm_versions.md
```

**Deliverable**: GLM version comparison

---

### Task 2.2: MiniMax M2.1 API Research
**Agent**: Codex
**Prompt**:
```
Research MiniMax M2.1 API integration:
1. Read MiniMax API documentation
2. Verify Anthropic API compatibility claim
3. Identify authentication method
4. Find endpoint URLs
5. Check rate limits and pricing
6. Create example integration code similar to glm_direct.py

Reference: https://platform.minimaxi.com/document/MiniMax%20API%20documentation

Output to: docs/coordination/research/minimax_integration.md
Include: Sample Python code for direct HTTP calls
```

**Deliverable**: MiniMax integration guide + code sample

---

### Task 2.3: Skills Research
**Agent**: Codex
**Prompt**:
```
Research Claude Skills system:
1. Read Anthropic documentation on Skills
2. Find example Skills implementations
3. Identify Skills best practices for:
   - Documentation automation
   - Code review workflows
   - Multi-agent coordination
4. Propose 3-5 specific Skills for our agent system

Output to: docs/coordination/research/skills_recommendations.md
```

**Deliverable**: Skills implementation recommendations

---

## PHASE 3: CODE ANALYSIS (Use Codex)

### Task 3.1: Permission System Analysis
**Agent**: Codex
**Prompt**:
```
Analyze .claude/settings.local.json across all projects.
Identify:
1. All currently allowed bash commands
2. Potentially dangerous permissions (rm, python, sudo)
3. Missing permissions for agent operations
4. Redundant permissions

Recommend:
- Safe default permission set
- Agent-specific permissions needed
- Commands to restrict

Output to: docs/coordination/analysis/permission_recommendations.md
```

**Deliverable**: Permission system recommendations

---

### Task 3.2: Wrapper Status Analysis
**Agent**: Codex
**Prompt**:
```
Analyze all agent wrapper scripts:
- agent-coordinator/scripts/*_wrapper.py
- simple-agents/*.exp
- simple-agents/*_wrapper.sh

For each:
1. Current implementation approach
2. Dependencies and requirements
3. Known issues (TTY, arg limits, etc)
4. Test status

Compare expect wrappers vs Python wrappers.
Recommend best approach for each agent.

Output to: docs/coordination/analysis/wrapper_comparison.md
```

**Deliverable**: Wrapper implementation strategy

---

### Task 3.3: Hooks System Audit
**Agent**: Codex
**Prompt**:
```
Analyze agent-coordinator/hooks/ structure:
1. List all existing hooks
2. Document what each hook does
3. Identify gaps (e.g., auto-documentation hook missing)
4. Propose hook architecture for:
   - Auto-documentation
   - Task list cleanup
   - Cross-agent coordination

Output to: docs/coordination/analysis/hooks_audit.md
```

**Deliverable**: Hooks system enhancement plan

---

## PHASE 4: PROJECT RECONCILIATION (Use GLM)

### Task 4.1: Agent Projects Comparison
**Agent**: GLM
**Prompt**:
```
Compare three agent system implementations:
1. agent-coordinator/
2. simple-agents/agent-new/
3. simple-agents/agent-system-standalone/

Create comparison matrix:
- Feature completeness
- Hook systems
- Agent wrappers
- Configuration
- Documentation quality
- Last modified dates

Recommend:
- Which should be canonical version
- What to merge from others
- What to archive/delete

Output to: docs/coordination/analysis/project_reconciliation.md
```

**Deliverable**: Project consolidation plan

---

### Task 4.2: Backup Analysis
**Agent**: GLM
**Prompt**:
```
Examine contents of:
- simple-agents/old_backup/ (all tar/gz files)
- simple-agents/agent-system-standalone/agent-system-standalone-backup-20251208-001313.tar.gz

List:
1. What files are in each backup
2. Date of backups
3. Any unique files not in current projects
4. Whether backups can be safely deleted

Output to: docs/coordination/analysis/backup_inventory.md
```

**Deliverable**: Backup cleanup recommendations

---

## PHASE 5: INTEGRATION PLANNING (Use Codex)

### Task 5.1: MiniMax Integration Code
**Agent**: Codex
**Prompt**:
```
Create MiniMax M2.1 integration following glm_direct.py pattern:

Requirements:
1. Direct HTTP calls (no SDK)
2. Environment variable authentication
3. Anthropic-compatible message format
4. Error handling and retries
5. Token counting and logging

Deliverable: scripts/minimax_direct.py
Test with simple prompt: "Hello, world"

Output to: docs/coordination/implementations/minimax_direct.py
Include: README with setup instructions
```

**Deliverable**: Working MiniMax integration code

---

### Task 5.2: Auto-Documentation Hook Design
**Agent**: Codex
**Prompt**:
```
Design PostToolUse hook for automatic documentation:

Requirements:
1. Triggers after EditFile or CreateFile
2. Updates relevant docs based on changed files
3. Maintains task list (move completed items)
4. Generates changelog entries
5. Does NOT write to project root

Design:
- Hook configuration JSON
- Python implementation
- Integration with existing quality gates
- Skill definition (if applicable)

Output to: docs/coordination/implementations/auto_doc_hook/
Files: config.json, hook.py, SKILL.md, README.md
```

**Deliverable**: Complete auto-doc hook implementation

---

### Task 5.3: Skills Package Design
**Agent**: Codex
**Prompt**:
```
Create Skills package for agent coordination:

Required Skills:
1. Multi-LLM routing decision making
2. Documentation generation patterns
3. Code review coordination
4. Task breakdown strategies

For each Skill:
- SKILL.md with instructions
- Example usage
- Integration points with hooks
- Best practices

Output to: docs/coordination/implementations/coordination-skills/
Structure: /mnt/skills/user/coordination-skills/
```

**Deliverable**: Coordination Skills package

---

## PHASE 6: TESTING (Use GLM + Codex)

### Task 6.1: Wrapper Testing Suite
**Agent**: Codex
**Prompt**:
```
Create comprehensive test suite for all agent wrappers:

Test coverage:
1. GLM direct HTTP (should pass)
2. Codex wrapper (currently fails - TTY)
3. Gemini wrapper (currently fails - arg limit)
4. MiniMax wrapper (new - test all edge cases)

For each:
- Unit tests
- Integration tests
- Error handling tests
- Timeout tests

Output to: docs/coordination/tests/wrapper_tests.py
Include: pytest configuration
```

**Deliverable**: Complete test suite

---

### Task 6.2: Permission Testing
**Agent**: GLM
**Prompt**:
```
Create test script that validates permission system:

Tests:
1. Allowed commands work without prompts
2. Restricted commands properly blocked
3. Settings persist across sessions
4. Permission inheritance in subdirectories

Output to: docs/coordination/tests/permission_tests.sh
Include: Expected vs actual results log
```

**Deliverable**: Permission validation suite

---

## AGENT DEPLOYMENT SEQUENCE

### Step 1: Deploy Discovery Tasks (Parallel)
```bash
# GLM handles cheap tasks
Task 1.1: File inventory
Task 1.2: Reference discovery
Task 1.3: Command inventory
Task 4.1: Project comparison
Task 4.2: Backup analysis

# Estimated time: 5-10 minutes (parallel)
```

### Step 2: Deploy Research Tasks (Sequential)
```bash
# Codex handles web research
Task 2.1: GLM versions → blocks 5.1
Task 2.2: MiniMax API → blocks 5.1
Task 2.3: Skills research → blocks 5.3

# Estimated time: 15-20 minutes
```

### Step 3: Deploy Analysis Tasks (Parallel)
```bash
# Codex analyzes code
Task 3.1: Permissions
Task 3.2: Wrappers
Task 3.3: Hooks

# Estimated time: 10-15 minutes
```

### Step 4: Deploy Implementation Tasks (Sequential)
```bash
# Dependencies from research phase
Task 5.1: MiniMax integration (needs 2.2)
Task 5.2: Auto-doc hook (needs 3.3)
Task 5.3: Skills package (needs 2.3)

# Estimated time: 20-30 minutes
```

### Step 5: Deploy Testing Tasks (Final)
```bash
# Validation
Task 6.1: Wrapper tests
Task 6.2: Permission tests

# Estimated time: 10 minutes
```

**Total estimated time**: 60-85 minutes for complete investigation

---

## COORDINATION APPROACH

### Desktop Claude (Me) Responsibilities
1. ✅ Create investigation prompts (this document)
2. ✅ Deploy tasks to appropriate agents
3. ✅ Monitor progress
4. ✅ Aggregate results
5. ✅ Synthesize recommendations
6. ✅ Coordinate with Charles

### Claude Code Responsibilities
1. Execute implementation tasks
2. Run tests
3. Modify files based on findings
4. Deploy new wrappers/hooks
5. Update configurations

### GLM Responsibilities (Cheap Tasks)
- File inventories
- Documentation searches
- Simple analysis
- Backup inspection

### Codex Responsibilities (Research + Code Analysis)
- Web research
- API documentation review
- Code review
- Integration design
- Test creation

---

## OUTPUT STRUCTURE

All agent outputs go to:
```
docs/coordination/
├── analysis/           # Discovery findings (Phase 1, 3, 4)
├── research/           # External research (Phase 2)
├── implementations/    # New code (Phase 5)
└── tests/              # Test suites (Phase 6)
```

Final deliverables compiled to:
```
docs/desktop-coordination/
├── INVESTIGATION_FINDINGS.md
├── RECOMMENDATIONS.md
└── IMPLEMENTATION_ROADMAP.md
```

---

## BLOCKERS

**Cannot proceed until**:
1. Charles answers questions in QUESTIONS_FOR_CHARLES.md
2. Clarification on /dev and /api commands
3. Decision on which agent project is canonical

**Can proceed with**:
- File inventory (Task 1.1)
- Reference discovery (Task 1.2)
- Backup analysis (Task 4.2)

---

## DEPLOYMENT TRIGGER

**When ready**, Charles says:
```
"Execute investigation plan"
```

Then I will:
1. Deploy Phase 1 tasks immediately
2. Wait for results
3. Deploy Phase 2-6 based on dependencies
4. Compile findings
5. Present recommendations

---

**Status**: PLAN READY - AWAITING CHARLES APPROVAL
