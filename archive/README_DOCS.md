# Documentation Guide - Agent Coordinator System

**Last Updated:** 2025-12-27  
**Status:** Alpha Development  
**Purpose:** Navigate this documentation when you return months later

---

## 🎯 START HERE

**If you're returning after a break, read in this order:**

1. **SYSTEM_STATUS.md** - Current state of the system (what works, what doesn't)
2. **TODO.md** - Active task list (what needs doing)
3. **DESKTOP_CC_METHODOLOGY.md** - How to work with Desktop + Claude Code
4. **coordination/CHECKPOINT_*.md** - Review latest checkpoints to see progress

---

## 📁 DOCUMENTATION STRUCTURE

```
docs/
├── README_DOCS.md (this file)           # Navigation guide
├── SYSTEM_STATUS.md                     # Current system state
├── TODO.md                              # Master task list
├── DESKTOP_CC_METHODOLOGY.md            # Work methodology
├── OVERSEER_MICROSTRUCTURE.md           # Future automation design
│
├── coordination/                        # Checkpoint outputs
│   ├── CHECKPOINT_1_ENV.md             # Environment analysis
│   ├── CHECKPOINT_2_STATE.md           # State management design
│   ├── CHECKPOINT_3_DEPLOY.md          # Deployment strategy
│   ├── CHECKPOINT_4_TEST.md            # First agent invocation
│   └── VISIBILITY_SYSTEM.md            # Monitoring dashboard (if complete)
│
└── analysis/                            # Research and comparisons
    └── (future comparative analysis docs)
```

---

## 📋 DOCUMENT PURPOSES

### Core Documents

**SYSTEM_STATUS.md**
- **Read when:** Starting any session
- **Contains:** What works, what doesn't, key decisions made
- **Update:** After major milestones or changes
- **Critical for:** Understanding current capabilities

**TODO.md**
- **Read when:** Before starting work
- **Contains:** Prioritized task list, completed tasks, estimates
- **Update:** After completing each task
- **Critical for:** Knowing what to work on next

**DESKTOP_CC_METHODOLOGY.md**
- **Read when:** Setting up a work session, or teaching someone else
- **Contains:** The Director/Engineer workflow pattern that works
- **Update:** Rarely (only when methodology evolves)
- **Critical for:** Maintaining quality and preventing hallucinations

**OVERSEER_MICROSTRUCTURE.md**
- **Read when:** Ready to automate the Desktop/CC coordination
- **Contains:** Design for Python automation of checkpoint workflow
- **Update:** As automation features get built
- **Critical for:** Future self-coordinating system

### Checkpoint Documents (coordination/)

**Purpose:** Historical record of development process

**CHECKPOINT_1_ENV.md**
- Environment configuration analysis
- Where secrets live, how GLM access works
- Key finding: Z.ai Anthropic-compatible endpoint

**CHECKPOINT_2_STATE.md**
- State management system design
- Start/stop lifecycle
- Update checking mechanism

**CHECKPOINT_3_DEPLOY.md**
- Deployment model decision (symlink approach)
- Migration plan from old submodules
- Security measures (.gitignore, pre-commit hooks)

**CHECKPOINT_4_TEST.md**
- First successful agent invocation
- GLM-4.7 working via coordinator
- Proof system actually works

**VISIBILITY_SYSTEM.md** (if created)
- Real-time monitoring dashboard
- Agent status tracking
- Terminal UI design

---

## 🔍 QUICK REFERENCE GUIDE

### I Want To...

**...understand what this system does**
→ Read `SYSTEM_STATUS.md` sections 1-2

**...know what to work on next**
→ Read `TODO.md` → High Priority section

**...remember how to use Desktop + Code workflow**
→ Read `DESKTOP_CC_METHODOLOGY.md` → THE WORKFLOW section

**...see what decisions were made**
→ Read `coordination/CHECKPOINT_3_DEPLOY.md` → Key Decisions

**...understand the environment setup**
→ Read `coordination/CHECKPOINT_1_ENV.md`

**...know deployment process**
→ Read `coordination/CHECKPOINT_3_DEPLOY.md` → Migration Plan

**...check if agents are working**
→ Read `coordination/CHECKPOINT_4_TEST.md` → Result: SUCCESS

**...build the automation**
→ Read `OVERSEER_MICROSTRUCTURE.md`

---

## 🚀 RESUMING WORK AFTER A BREAK

### Quick Start Procedure

1. **Read current state** (5 min)
   ```
   Open: SYSTEM_STATUS.md
   Scan: What Works / What Doesn't
   Note: Any critical issues
   ```

2. **Check task list** (2 min)
   ```
   Open: TODO.md
   Read: High Priority section
   Pick: ONE task to tackle
   ```

3. **Review latest checkpoints** (10 min)
   ```
   Open: coordination/CHECKPOINT_4_TEST.md (or latest)
   Understand: Where we left off
   Context: What was working
   ```

4. **Start Desktop session**
   ```
   Message: "I'm resuming work on agent-coordinator.
            Last checkpoint: [N]
            Current goal: [from TODO.md]
            Attach: SYSTEM_STATUS.md, TODO.md"
   ```

5. **Generate next prompt**
   ```
   Desktop creates checkpoint prompt
   Paste to Claude Code
   Execute and review
   ```

---

## 📊 PROJECT TIMELINE (Key Milestones)

**2025-12-26:**
- ✅ Checkpoint 1: Environment analysis complete
- ✅ Checkpoint 2: State management designed
- ✅ Checkpoint 3: Deployment strategy chosen (symlink)
- ✅ Checkpoint 4: First agent invocation successful (GLM-4.7)
- ✅ Methodology documented
- ✅ TODO system established

**Next milestones:**
- [ ] Visibility system implemented
- [ ] Start/stop commands working
- [ ] Multi-agent parallel execution tested
- [ ] Overseer automation built

---

## ⚠️ IMPORTANT NOTES

### Security Reminders

**NEVER commit:**
- `~/.config/secrets/ai.env`
- Any file containing `ANTHROPIC_AUTH_TOKEN`
- Any file containing `*API_KEY*`
- Real `.env` files (only `.env.example` is safe)

**Always check:**
- `.gitignore` is comprehensive
- Pre-commit hooks are active
- No secrets in staged files

### File Organization Rules

**DO:**
- ✅ Write checkpoints to `docs/coordination/`
- ✅ Update `SYSTEM_STATUS.md` after major changes
- ✅ Update `TODO.md` after completing tasks
- ✅ Use full UNC paths in prompts

**DON'T:**
- ❌ Write markdown files to project root
- ❌ Create files outside `docs/` or `.agents/`
- ❌ Mix documentation and code
- ❌ Start new work without reading TODO.md

### Methodology Principles

**Remember:**
- Desktop Claude = Director (strategic)
- Claude Code = Chief Engineer (tactical)
- One checkpoint at a time
- Human makes all decisions
- File-based handoffs prevent hallucinations

---

## 🔧 TROUBLESHOOTING

### Can't Find Where We Left Off

**Solution:**
1. Read `SYSTEM_STATUS.md` → "What Works" section
2. Read latest `CHECKPOINT_*.md` in `coordination/`
3. Read `TODO.md` → "ACTIVE TASKS" section

### Don't Remember How Workflow Works

**Solution:**
1. Read `DESKTOP_CC_METHODOLOGY.md` → "THE WORKFLOW" section
2. Follow the 5-step process
3. Use the prompt templates

### System Not Working

**Solution:**
1. Check `SYSTEM_STATUS.md` → "What Doesn't Work Yet"
2. Verify environment: `echo $ANTHROPIC_BASE_URL`
3. Read `coordination/CHECKPOINT_1_ENV.md` for setup details
4. Check `TODO.md` for known issues

### Lost Context on a Decision

**Solution:**
1. Search `coordination/CHECKPOINT_3_DEPLOY.md` for deployment decisions
2. Search `coordination/CHECKPOINT_2_STATE.md` for design decisions
3. Search `SYSTEM_STATUS.md` for "Key Decisions Made"

---

## 🎓 FOR NEW CONTRIBUTORS (Future)

**If someone else is reading this:**

This system is currently **single-user alpha**. See:
- Main `README.md` for multi-user warnings
- `coordination/CHECKPOINT_3_DEPLOY.md` for why symlinks won't work for you
- Better alternatives: LangChain, AutoGen, Goose

**If you still want to try:**
1. Read `SYSTEM_STATUS.md` → Architecture Overview
2. Read `coordination/CHECKPOINT_1_ENV.md` → Environment setup
3. Use git submodule, not symlink
4. You're on your own for configuration

---

## 📈 FUTURE AUTOMATION (OVERSEER)

**See:** `OVERSEER_MICROSTRUCTURE.md`

**Vision:**
- Desktop Claude as always-on supervisor
- Automatic checkpoint progression
- File-watching triggers next steps
- Self-coordinating development

**Status:** Design phase only

**Next steps:**
1. Implement basic file watcher
2. Create checkpoint auto-trigger
3. Build Desktop → Code bridge
4. Test autonomous operation

---

## 📞 CONTACT / SUPPORT

**This is a personal project by Charles.**

- GitHub: https://github.com/CarlosIrineuCosta/agent-system
- Issues: Use GitHub issues (but expect limited support)
- Questions: Check TODO.md and SYSTEM_STATUS.md first

---

## 🔄 DOCUMENT MAINTENANCE

**When to update this guide:**
- Major structural changes to docs/
- New document types added
- Workflow methodology changes
- New automation features added

**How to update:**
- Edit this file directly
- Update "Last Updated" date
- Add new sections as needed
- Keep "START HERE" section accurate

---

## ✨ FINAL NOTES

**This documentation system is part of the agent-coordinator.**

It represents:
- The checkpoint-based development process
- The Desktop/Code supervision methodology
- The actual decisions made during development
- A template for future similar projects

**Key insight:**
The methodology that built this system is documented alongside the system itself. This is meta-documentation - the process is the product.

**When you return:**
1. Read this file (you're doing it now)
2. Follow "RESUMING WORK AFTER A BREAK"
3. Trust the checkpoint process
4. Update TODO.md as you go

**Good luck, future Charles.** 🚀

---

**END OF NAVIGATION GUIDE**
