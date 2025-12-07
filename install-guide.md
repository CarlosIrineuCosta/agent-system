# Agent System Standalone - Installation Guide

**Straight-to-the-point installation instructions for the multi-agent development system**

## Quick Start

```bash
# Clone and install
git clone <repository-url>
cd agent-system-standalone
chmod +x validate.py && ./validate.py
```

## Prerequisites

- Python 3.8+
- Git
- Claude Code CLI (recommended)
- Basic understanding of command line operations

---

## Automated Installation Process

### 1. Automated Setup Script

**Usage:**
```bash
# Normal installation
./scripts/setup_hooks.sh

# Force overwrite existing files
./scripts/setup_hooks.sh --force

# Verbose output
./scripts/setup_hooks.sh --verbose
```

**What it does:**
- Creates project directories (`.agents/`, `scripts/`, `docs/`, etc.)
- Copies configuration files
- Sets up symlinks for agent-system components
- Configures VS Code integration
- Sets up Python virtual environment
- Installs dependencies
- Validates installation
- Generates setup instructions

**IMPORTANT MANUAL STEPS** (required for slash commands to work):
```bash
# After running setup_hooks.sh, you MUST also run:
mkdir -p .claude/hooks .claude/commands
cp -r agent-system/hooks/* .claude/hooks/
cp -r agent-system/commands/* .claude/commands/
echo "export CLAUDE_TRUSTED_WORKSPACE=$(pwd)" >> .env
```

### 2. Manual Installation Commands

#### Project Structure Creation
```bash
# Create essential directories
mkdir -p .agents/{reviews,backup,logs}
mkdir -p scripts/agents
mkdir -p docs/agent_system
mkdir -p .claude

# Make scripts executable
chmod +x validate.py
chmod +x scripts/*.py
chmod +x hooks/**/*.py
```

#### Configuration Setup
```bash
# Copy configuration files
cp config/hooks_settings.json ~/.claude/hooks_settings.json
cp config/agent_routing.json ~/.claude/agent_routing.json

# Copy environment template
cp config/.env.example .env.example
```

#### Symlink Creation
```bash
# Create main symlink
ln -sf "$(pwd)" ./agent-system

# Create script symlinks
ln -sf agent-system/scripts/* scripts/ 2>/dev/null || true

# Create hooks symlink
ln -sf agent-system/hooks hooks
```

---

## Configuration Templates

### 1. Hooks Settings (JSON Template)

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python agent-system/hooks/auxiliary/root_protection.py"
          },
          {
            "type": "command",
            "command": "python agent-system/hooks/core/quality_gate.py"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python agent-system/hooks/core/completion_checker.py"
          },
          {
            "type": "command",
            "command": "python agent-system/hooks/session/session_tracker.py"
          }
        ]
      }
    ]
  }
}
```

### 2. Agent Routing (JSON Template)

```json
{
  "routing_rules": {
    "architecture": "claude",
    "implementation": "glm",
    "security": "codex",
    "large_context": "gemini",
    "documentation": "glm",
    "testing": "glm",
    "review": {
      "claude": "glm",
      "glm": "codex",
      "codex": "claude",
      "gemini": "claude"
    }
  },
  "task_keywords": {
    "architecture": ["design", "architecture", "plan", "strategy"],
    "implementation": ["implement", "code", "function", "method"],
    "security": ["security", "auth", "encrypt", "validate"],
    "large_context": ["review", "analyze", "comprehensive"],
    "documentation": ["document", "readme", "comment", "explain"],
    "testing": ["test", "spec", "validate", "check"]
  },
  "agent_capabilities": {
    "claude": ["reasoning", "architecture", "coordination"],
    "glm": ["implementation", "testing", "documentation"],
    "codex": ["security", "optimization", "review"],
    "gemini": ["large_context", "comprehensive_analysis"]
  }
}
```

### 3. Environment Configuration (Template)

```bash
# .env.example
# LLM Configuration
GLM_API_KEY=your_glm_api_key_here
CODEX_API_KEY=your_codex_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# Project Settings
PROJECT_NAME=your-project-name
PROJECT_ROOT=.
PYTHON_ENV=venv

# Agent Configuration
DEFAULT_AGENT=claude
AUTO_ROUTING=true
QUALITY_GATES_ENABLED=true

# Session Settings
SESSION_TRACKING=true
BACKUP_ENABLED=true
LOG_LEVEL=INFO
```

---

## Step-by-Step Installation Process

### Step 1: System Requirements Check

```bash
# Check Python version
python3 --version  # Should be 3.8+

# Check Git
git --version

# Check if Claude Code is installed
claude --version  # Optional
```

### Step 2: Clone Repository

```bash
git clone <repository-url>
cd agent-system-standalone
```

### Step 3: Validate System

```bash
# Run validation script
python3 validate.py

# Expected output should show:
# ✓ All checks passed! System is ready for use.
```

### Step 4: Install Dependencies

```bash
# Install Python requirements
pip install -r requirements.txt

# Essential packages (if requirements.txt missing)
pip install python-dotenv jsonschema requests pyyaml click
```

### Step 5: Configure Environment

```bash
# Copy environment template
cp config/.env.example .env

# Edit .env file with your API keys
nano .env  # or your preferred editor
```

### Step 6: Setup Claude Code Integration (Required for Slash Commands)

```bash
# Copy Claude configuration
mkdir -p ~/.claude
cp config/hooks_settings.json ~/.claude/hooks_settings.json
cp config/agent_routing.json ~/.claude/agent_routing.json

# IMPORTANT: Copy hooks and commands to project .claude directory
mkdir -p .claude/hooks .claude/commands
cp -r hooks/* .claude/hooks/
cp -r commands/* .claude/commands/
```

### Step 7: Create Project Structure

```bash
# Create directories for new projects
mkdir -p my-project
cd my-project

# Link agent-system
ln -sf ../agent-system agent-system

# Initialize coordination files
touch COORDINATION.md AGENT_SUMMARY.md TASKS_TRACKING.md
```

### Step 8: Set Up Virtual Environment

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies in venv
pip install -r ../agent-system/requirements.txt
```

---

## Post-Installation Validation

### 1. System Health Check

```bash
# Run comprehensive validation
./agent-system/validate.py
```

**Expected health statuses:**
- 🟢 **EXCELLENT** (90-100%) - All systems operational
- 🟡 **GOOD** (70-89%) - Minor issues only
- 🟠 **FAIR** (50-69%) - Some attention needed
- 🔴 **POOR** (<50%) - Requires immediate attention

### 2. Component Verification

```bash
# Check essential files
ls -la agent-system/
ls -la hooks/
ls -la scripts/
ls -la config/

# Verify executables
which python3 agent-system/validate.py
which python3 scripts/agent_coordinator.py
```

### 3. Hook Testing

```bash
# Test individual hooks
python3 hooks/core/quality_gate.py
python3 hooks/core/completion_checker.py
python3 hooks/session/session_tracker.py
```

### 4. Agent Coordinator Test

```bash
# Test agent coordinator
python3 scripts/agent_coordinator.py --help
python3 scripts/agent_coordinator.py --test
```

---

## Quick Validation Commands

### 1. System Validation
```bash
./agent-system/validate.py
```

### 2. Agent System Health
```bash
# Check agent system integrity
python3 scripts/agent_coordinator.py --test
python3 scripts/multi_llm_coordinator.py --test
```

### 3. Configuration Validation
```bash
# Test configuration files
python3 -m json.tool config/hooks_settings.json
python3 -m json.tool config/agent_routing.json
```

### 4. Symlink Validation
```bash
# Check broken symlinks
find . -type l -exec test ! -e {} \; -print
```

---

## Troubleshooting

### Common Issues and Solutions

#### 1. Permission Errors
```bash
# Fix executable permissions
chmod +x agent-system/*.py
chmod +x scripts/*.py
chmod +x hooks/**/*.py
chmod +x validate.py
```

#### 2. Python Import Errors
```bash
# Install missing dependencies
pip install python-dotenv jsonschema
pip install -r requirements.txt

# Check Python path
echo $PYTHONPATH
```

#### 3. Hook Configuration Issues
```bash
# Validate JSON syntax
python3 -m json.tool ~/.claude/hooks_settings.json

# Check file permissions
ls -la ~/.claude/
```

#### 4. Broken Symlinks
```bash
# Recreate symlinks
rm -f agent-system
ln -sf "$(pwd)" agent-system

# Fix script symlinks
find scripts -name "*.py" -exec ln -sf "../agent-system/$(basename {})" {} \;
```

#### 5. Slash Commands Not Working (/start, /end, etc.)
```bash
# Check if commands directory exists
ls -la .claude/commands/

# If missing, copy commands
mkdir -p .claude/commands
cp -r agent-system/commands/* .claude/commands/

# Check if hooks directory exists
ls -la .claude/hooks/

# If missing, copy hooks
mkdir -p .claude/hooks
cp -r agent-system/hooks/* .claude/hooks/

# Set required environment variable
echo "export CLAUDE_TRUSTED_WORKSPACE=$(pwd)" >> .env
source .env

# IMPORTANT: Update Claude settings to use absolute paths
# Option 1: Manual edit
# Edit ~/.claude/settings.json or .claude/settings.json and replace:
# "python agent-system/hooks/" with "python /full/path/to/project/.claude/hooks/"

# Option 2: Automated fix (RECOMMENDED)
# Run the included fix script:
python agent-system/scripts/fix_hook_paths.py

# Or use: "python $(pwd)/.claude/hooks/" for dynamic path resolution
```

#### 6. Virtual Environment Issues
```bash
# Rebuild virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Debug Commands

```bash
# Check system architecture
python3 -c "import sys; print(sys.version)"

# Test imports
python3 -c "import json; print('JSON OK')"

# Check file structure
find . -name "*.py" | head -10

# Test hooks individually
python3 hooks/core/quality_gate.py --test
python3 hooks/core/completion_checker.py --test
```

### Validation Log Analysis

```bash
# Check validation output
./agent-system/validate.py 2>&1 | tee validation.log

# Look for specific errors
grep -i error validation.log
grep -i fail validation.log
```

---

## Development Setup

### 1. VS Code Integration

```bash
# Copy VS Code settings
mkdir -p .vscode
cp agent-system/templates/.vscode/* .vscode/

# Install VS Code extensions
code --install-extension ms-python.python
code --install-extension ms-vscode.vscode-json
```

### 2. Git Integration

```bash
# Create .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
venv/
.env
*.env

# Agent system
.agents/
*.log

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
EOF
```

### 3. Automation Scripts

```bash
# Create quick start script
cat > start.sh << 'EOF'
#!/bin/bash
echo "Starting Agent System..."
python3 validate.py
source venv/bin/activate  # if using virtual environment
echo "Ready for development!"
EOF

chmod +x start.sh
```

---

## Advanced Configuration

### 1. Custom Agent Routing

Edit `config/agent_routing.json` to modify agent assignments:

```json
{
  "routing_rules": {
    "architecture": "claude",
    "implementation": "sonnet",
    "security": "codex",
    "documentation": "glm"
  }
}
```

### 2. Hook Customization

Modify `config/hooks_settings.json` to add custom hooks:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python custom_hooks/validation.py"
          }
        ]
      }
    ]
  }
}
```

### 3. Environment Variables

Set additional environment variables:

```bash
export AGENT_SYSTEM_DEBUG=true
export LOG_LEVEL=DEBUG
export SESSION_TRACKING=true
```

---

## Support and Resources

### Documentation
- Main documentation: `README.md`
- Validation guide: `docs/VALIDATION_SCRIPT.md`
- Agent coordination: `docs/COORDINATION.md`

### Support Commands
```bash
# Check system status
./agent-system/validate.py

# Get help
./scripts/setup_hooks.sh --help
./scripts/agent_coordinator.py --help

# Test system
./scripts/agent_coordinator.py --test
```

### Common Commands
```bash
# Initialize new project
python3 scripts/agent_coordinator.py --init-project my-project

# Process proposals
python3 scripts/process_proposals.py --input proposals.json

# Multi-agent coordination
python3 scripts/multi_llm_coordinator.py --tasks "backend,frontend,docs"
```

---

## Next Steps

1. **Validate Installation**: Run `./agent-system/validate.py`
2. **Configure Environment**: Edit `.env` file with API keys
3. **Start Development**: Use `claude` CLI or run agents directly
4. **Monitor Progress**: Check `COORDINATION.md` and `AGENT_SUMMARY.md`

**Quick Reference**: The system is now ready for multi-agent development workflows with automatic quality gates and agent coordination.