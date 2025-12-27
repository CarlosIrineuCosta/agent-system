# FOR CLAUDE INSTALLATION GUIDE
# Claude-to-Claude Agent System Installation Instructions

## INTRODUCTION

This document provides Claude-readable and actionable instructions for installing the multi-agent development system. Follow these steps precisely to set up a working agent-system environment.

## PRE-INSTALLATION QUESTIONS TO ASK USER

Before beginning installation, ask the user these questions:

1. **Project Type**: "What type of project are you planning to develop?" (web app, API, data analysis tool, etc.)
2. **Preferred Tech Stack**: "What technology stack do you prefer?" (Python/React, Node.js/Express, etc.)
3. **Development Environment**: "Are you using local development, cloud IDE, or remote server?"
4. **Existing Project**: "Is this for an existing project or new development?"
5. **Quality Control**: "Do you want automated quality gates and code reviews?"
6. **Multi-LLM Preference**: "Do you want to use multiple LLMs (Claude + GLM + others) or just Claude?"

## INSTALLATION CHECKLIST

### Phase 1: System Prerequisites

```bash
# Check Python version (requires 3.8+)
python3 --version

# Check pip installation
pip3 --version

# Install essential Python packages if missing
pip3 install python-dotenv jsonschema
```

### Phase 2: Agent System Deployment

```bash
# Navigate to project directory
cd /path/to/your/project

# Copy agent-system to project (from source location)
cp -r /path/to/source/agent-system/ .

# Set proper permissions
chmod +x agent-system/validate.py
chmod -R +x agent-system/scripts/*.py
chmod -R +x agent-system/hooks/*.py
```

### Phase 3: Configuration Setup

```bash
# Copy environment template
cp agent-system/config/.env.example agent-system/.env

# Create unified configuration
cat > agent-system/config/unified_config.json << 'EOF'
{
  "agents": {
    "claude": {
      "enabled": true,
      "capabilities": ["reasoning", "architecture", "coordination"],
      "priority": "high"
    },
    "glm": {
      "enabled": true,
      "capabilities": ["implementation", "testing", "documentation"],
      "priority": "medium"
    },
    "codex": {
      "enabled": false,
      "capabilities": ["security", "optimization", "review"],
      "priority": "low"
    },
    "gemini": {
      "enabled": false,
      "capabilities": ["large_context", "comprehensive_analysis"],
      "priority": "low"
    }
  },
  "hooks": {
    "quality_control": true,
    "completion_tracking": true,
    "root_protection": true
  },
  "routing": {
    "architecture": "claude",
    "implementation": "glm",
    "security": "codex",
    "large_context": "gemini",
    "documentation": "glm",
    "testing": "glm"
  }
}
EOF

# CRITICAL: Enable Slash Commands (/start, /end, /api, etc.)
mkdir -p .claude/hooks .claude/commands
cp -r agent-system/hooks/* .claude/hooks/
cp -r agent-system/commands/* .claude/commands/

# Set required environment variable
echo "export CLAUDE_TRUSTED_WORKSPACE=$(pwd)" >> .env

# Update Claude Code hooks configuration
# User must manually update Claude Code settings to point to:
# agent-system/hooks/ for PostToolUse and Stop hooks
```

### Phase 4: Environment Configuration

Edit `agent-system/.env` with user-specific settings:

```bash
# Edit .env file
nano agent-system/.env
```

Key settings to configure:
- `CODEX_CLI_PATH=/usr/local/bin/codex` (if using Codex)
- `GEMINI_CLI_PATH=/usr/local/bin/gemini` (if using Gemini)
- `MAX_PARALLEL_TASKS=3` (adjust based on system)
- `DEFAULT_TIMEOUT=300` (seconds)

### Phase 5: Project Integration

```bash
# Create project-specific hooks symlink
ln -sf agent-system/hooks hooks

# Create scripts access
mkdir -p scripts
ln -sf ../agent-system/scripts/*.py scripts/ 2>/dev/null || true

# Add .claude directory if missing
mkdir -p .claude/state

# Initialize project templates
cp -r agent-system/templates/* . 2>/dev/null || true
```

## JSON CONFIGURATION EXAMPLES

### Example 1: Basic Project Setup
```json
{
  "project_name": "MyWebApp",
  "tech_stack": "Python/React",
  "architecture": "monolith",
  "quality_gates": true,
  "multi_llm": false,
  "primary_agent": "claude"
}
```

### Example 2: Advanced Multi-Agent Setup
```json
{
  "project_name": "APIPlatform",
  "tech_stack": "Node.js/PostgreSQL",
  "architecture": "microservices",
  "quality_gates": true,
  "multi_llm": true,
  "agents": {
    "claude": "architecture_coordination",
    "glm": "implementation_testing",
    "codex": "security_review",
    "gemini": "documentation_analysis"
  },
  "routing": {
    "api_design": "claude",
    "backend_implementation": "glm",
    "security_audit": "codex",
    "api_documentation": "gemini"
  }
}
```

## VALIDATION STEPS

After installation, run these validation commands:

```bash
# Navigate to agent-system directory
cd agent-system

# Run comprehensive validation
python3 validate.py

# Expected output should show:
# • All validation checks passing
# • System health 90%+
# • All dependencies installed
# • All scripts executable
# • Configuration files valid

# Test individual components
python3 hooks/core/quality_gate.py
python3 hooks/core/completion_checker.py
python3 scripts/agent_coordinator.py --help
```

## COMMON DECISIONS CLAUDE NEEDS TO MAKE

### 1. Agent Configuration Decisions
- **Single Agent Mode**: Use only Claude for simplicity
- **Multi-Agent Mode**: Enable GLM + Claude for enhanced capabilities
- **Advanced Mode**: Enable all agents (Claude, GLM, Codex, Gemini) for maximum flexibility

### 2. Quality Gate Decisions
- **Basic QC**: Enable quality_gate.py only
- **Enhanced QC**: Add root_protection.py and completion_checker.py
- **Full QC**: Enable all hooks including session tracking

### 3. Routing Configuration Decisions
- **Simple Routing**: Use architecture->Claude, implementation->GLM
- **Complex Routing**: Enable multi-agent routing based on task keywords
- **Custom Routing**: Create custom routing rules for specific domains

### 4. Environment Setup Decisions
- **Local Development**: Install all CLI tools locally
- **Cloud IDE**: Use web-based interfaces or API endpoints
- **Remote Server**: Set up SSH access and remote CLI tools

## TROUBLESHOOTING GUIDE

### Issue 1: Validation Fails
```bash
# Check permissions
chmod +x agent-system/validate.py
chmod -R +x agent-system/scripts/
chmod -R +x agent-system/hooks/

# Check dependencies
pip3 install python-dotenv jsonschema

# Check file structure
ls -la agent-system/
```

### Issue 2: Hook Configuration Problems
```bash
# Verify hooks_settings.json format
cat agent-system/config/hooks_settings.json

# Check symlink for hooks
ls -la hooks/
```

### Issue 3: Agent Communication Issues
```bash
# Test agent coordinator
python3 scripts/agent_coordinator.py --test

# Check unified configuration
cat agent-system/config/unified_config.json
```

### Issue 4: Environment Variables
```bash
# Verify .env file
cat agent-system/.env

# Test environment loading
python3 -c "import os; print('CODEX:', os.getenv('CODEX_CLI_PATH'))"
```

## POST-INSTALLATION VERIFICATION

Complete these steps to ensure successful installation:

1. **Run Validation**: Execute `python3 validate.py` and ensure 100% pass rate
2. **Test Hooks**: Manually trigger hooks to verify functionality
3. **Check Permissions**: Ensure all scripts are executable
4. **Validate Configuration**: Test JSON configuration files
5. **Test Communication**: Verify agent coordination scripts
6. **Check Integration**: Confirm Claude Code hooks are properly configured

## NEXT STEPS AFTER INSTALLATION

1. **Project Initialization**: Use `/start` command to initialize new project
2. **Agent Coordination**: Use `/delegate` command for multi-agent tasks
3. **Quality Control**: Monitor hook execution during development
4. **System Updates**: Run validation regularly to ensure system health
5. **Customization**: Modify routing and configuration as needed

## NOTES FOR CLAUDE

- Always run validation after making configuration changes
- Keep backup of configuration files before major modifications
- Test agent coordination in development environment first
- Use GLM as primary implementation agent when available
- Reserve Claude for architectural and coordination tasks
- Use Codex for security-sensitive operations when enabled
- Use Gemini for large context analysis when enabled

This installation guide ensures consistent and reliable deployment of the multi-agent development system across different environments and project types.