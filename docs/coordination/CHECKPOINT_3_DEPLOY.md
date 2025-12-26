# Dev vs Deploy Strategy

## 1. Current State (The Mess)

### What Actually Exists

| Location | Type | Purpose |
|----------|------|---------|
| `~/Storage/projects/agent-coordinator/` | Standalone git repo | Development workspace |
| `zora/agent-system/` | Git submodule | Production (in zora) |
| `lumen-2026/agent-system/` | Git submodule | Production (in lumen) |
| `photo-tagger/agent-system/` | Git submodule | Production (in photo-tagger) |
| `crypto-trader/agent-system/` | Git submodule | Production (in crypto-trader) |

### Key Findings

1. **NO `.claude/agent-coordinator` installations exist** - all projects use root-level `agent-system/` submodules

2. **Two separate agent systems exist:**
   - `agent-system` - the submodule in existing projects (1 commit, initial setup)
   - `agent-coordinator` - the new development project (active development)

3. **Version consistency:** All submodules point to the same remote (`CarlosIrineuCosta/agent-system`)

4. **Development workflow:** Currently developing in `agent-coordinator`, but production projects use `agent-system` submodules

5. **The disconnect:** Changes in `agent-coordinator` are NOT reaching the production projects

---

## 2. Option Comparison

### Option A: Git Submodule

| Criterion | Score | Notes |
|-----------|-------|-------|
| Update friction | Medium | Must update each project separately |
| Version control | Excellent | Each project can pin to specific commit |
| Breaking changes | Safe | Old projects unaffected by updates |
| Development flow | Complex | Must push to remote, then update submodules |
| Security | Good | Standard git controls apply |

**Verdict:** Good for stability, bad for rapid development iteration.

### Option B: Symlink to Canonical Install

| Criterion | Score | Notes |
|-----------|-------|-------|
| Update friction | Excellent | One `git pull` affects all projects |
| Version control | Poor | All projects must use same version |
| Breaking changes | Risky | Broken master breaks everything immediately |
| Development flow | Excellent | Edit once, test everywhere instantly |
| Security | Poor | Easy to accidentally commit project-specific data |

**Verdict:** Great for development, dangerous for production.

### Option C: Install Script with Copy

| Criterion | Score | Notes |
|-----------|-------|-------|
| Update friction | High | Must run script in each project |
| Version control | Excellent | Each project has independent copy |
| Breaking changes | Safe | Old projects unaffected |
| Development flow | Poor | Must redeploy to test changes |
| Security | Good | Each project isolated |

**Verdict:** Safest, but highest friction.

---

## 3. RECOMMENDATION: Option B (Symlink) with Development Sandbox

**Chosen approach:** **Option B - Symlink to Canonical Install**

### Why Option B Makes Sense Here

1. **Active development phase:** The system is evolving rapidly. Being able to edit once and see effects across all projects is critical.

2. **Charles is the only user:** No risk of conflicting requirements between projects.

3. **Single machine:** All projects live on the same dev machine (`/home/cdc/Storage/projects/`)

4. **Rollback is cheap:** If something breaks, just revert the symlink target or revert the commit.

5. **Real-world pattern:** This is how tools like `mise`, `homebrew`, and VS Code extensions work.

### The Hybrid Approach (Best of Both Worlds)

```
~/Storage/projects/agent-coordinator/     # Development (git repo)
├── scripts/
├── hooks/
├── commands/
└── ...

Each project:
~/Storage/projects/zora/.claude/agent-coordinator -> ~/Storage/projects/agent-coordinator
~/Storage/projects/lumen-2026/.claude/agent-coordinator -> ~/Storage/projects/agent-coordinator
```

**Benefits:**
- Development happens in one place
- All projects see changes instantly
- Projects CAN override by using their own `.env` or local hooks
- Easy to test across multiple projects

---

## 4. Migration Plan

### Step 1: Clean Up Existing Submodules

```bash
# In each project (zora, lumen-2026, photo-tagger, crypto-trader)
git submodule deinit -f agent-system
git rm -f agent-system
rm -rf .git/modules/agent-system
git commit -m "Remove old agent-system submodule"
```

### Step 2: Create Symlinks

```bash
# In each project
ln -s ~/Storage/projects/agent-coordinator .claude/agent-coordinator

# Add to .gitignore
echo ".claude/agent-coordinator" >> .gitignore
git add .gitignore
git commit -m "Add agent-coordinator symlink"
```

### Step 3: Update agent-coordinator Remote

```bash
cd ~/Storage/projects/agent-coordinator

# Ensure it points to the canonical repo
git remote set-url origin https://github.com/CarlosIrineuCosta/agent-system.git

# OR if keeping separate:
git remote set-url origin https://github.com/CarlosIrineuCosta/agent-coordinator.git
```

### Step 4: Verify All Projects

```bash
for proj in zora lumen-2026 photo-tagger crypto-trader; do
  echo "=== $proj ==="
  ls -ld ~/Storage/projects/$proj/.claude/agent-coordinator
done
```

---

## 5. Security Implementation

### .gitignore Updates

**For agent-coordinator repo:**
```gitignore
# Secrets (CRITICAL)
.env
*.env
!.env.example
config/secrets/
ai.env

# Runtime state (don't commit transient data)
.agents/
.claude/agent-coordinator/runtime/
*.state
*.lock

# Keys (block patterns)
*API_KEY*
*AUTH_TOKEN*
*SECRET*
*.key
*.pem
```

**For each project:**
```gitignore
# Agent coordinator symlink
.claude/agent-coordinator

# Project-specific secrets
.env
*.key
```

### Pre-commit Hook

**File:** `.git/hooks/pre-commit` (in agent-coordinator)

```bash
#!/bin/bash
# Prevent accidental secret commits

# Patterns that should NEVER be committed
forbidden_patterns=(
    "ANTHROPIC_AUTH_TOKEN"
    "ZAI_API_KEY"
    "GLM_API_KEY"
    "sk-[a-zA-Z0-9]{32,}"  # OpenAI-style keys
    "90d7df3e421f48b99f78e9914f1b682b"  # Specific known keys
)

# Check staged files
for file in $(git diff --cached --name-only); do
    for pattern in "${forbidden_patterns[@]}"; do
        if git diff --cached "$file" | grep -q "$pattern"; then
            echo "ERROR: Potential secret found in $file"
            echo "Pattern: $pattern"
            echo "Commit blocked. Remove secrets before committing."
            exit 1
        fi
    done
done
```

### Installation Script Safety

The install script must:
1. Never copy `.env` files (only `.env.example`)
2. Run the pre-commit check before any git operations
3. Warn if secrets detected in working directory

```bash
# In install.sh
check_for_secrets() {
    if grep -r "ANTHROPIC_AUTH_TOKEN\|API_KEY" . --exclude-dir=.git 2>/dev/null | grep -v "example" | grep -v ".pyc"; then
        echo "WARNING: Potential secrets detected in files!"
        echo "Please remove before committing."
        return 1
    fi
}
```

---

## 6. Update Workflow

### Future Update Process

```bash
# 1. Pull latest changes
cd ~/Storage/projects/agent-coordinator
git pull origin main

# 2. All projects immediately see updates (via symlink)

# 3. Test in each project
cd ~/Storage/projects/zora
# Test functionality

cd ~/Storage/projects/lumen-2026
# Test functionality

# 4. If something breaks, rollback:
cd ~/Storage/projects/agent-coordinator
git revert HEAD
# Or: git checkout <previous-commit>
```

### Development Workflow

```
1. Make changes in agent-coordinator
2. Test locally in agent-coordinator
3. Test in one project (e.g., zora)
4. If good, commit
5. All projects now have the change
```

---

## 7. Rollback Procedure

### Quick Rollback (Broken Change)

```bash
cd ~/Storage/projects/agent-coordinator
git log --oneline -5  # Find the good commit
git checkout <good-commit>
# All projects instantly reverted
```

### Per-Project Override (If One Project Needs Old Version)

```bash
# In specific project
rm .claude/agent-coordinator
git clone https://github.com/CarlosIrineuCosta/agent-system.git .claude/agent-coordinator
cd .claude/agent-coordinator
git checkout <specific-version>
```

### Emergency Disconnect

If everything is broken and you need to isolate:

```bash
# In each project
rm .claude/agent-coordinator
# Project now has no agent system (safe but non-functional)
```

---

## 8. Testing Strategy

### Where to Test Changes

1. **Unit testing:** In `agent-coordinator/` itself
2. **Integration testing:** Use `zora` as primary test project
3. **Smoke testing:** Before committing, test in at least 2 projects

### Pre-commit Checklist

- [ ] Run `validate.py` in agent-coordinator
- [ ] Test in `zora` project
- [ ] Test in one more project
- [ ] No secrets in staged files
- [ ] `.gitignore` is correct

---

## 9. Decision Matrix

| Scenario | Recommended Action |
|----------|-------------------|
| Active development, single machine | **Symlink (Option B)** |
| Multiple developers, different machines | Submodule (Option A) |
| Production stability required | Submodule with pinned commit |
| Rapid prototyping | Symlink (Option B) |
| Need per-project customization | Symlink + local overrides |

---

## 10. Implementation Tasks

- [ ] Remove old `agent-system` submodules from projects
- [ ] Create symlinks in each project to `agent-coordinator`
- [ ] Update `.gitignore` in all projects
- [ ] Create pre-commit hook in `agent-coordinator`
- [ ] Document the symlink structure in project READMEs
- [ ] Create rollback script for emergencies
- [ ] Test update workflow end-to-end
