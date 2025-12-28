# Agent Coordinator

A multi-agent orchestration system for Claude Code that enables parallel task execution, intelligent routing, and coordinated workflows across specialized AI agents.

## Features

- **Multi-Agent Coordination**: Route tasks to specialized agents (Claude, GLM, Codex, Gemini) based on task type and keywords
- **Parallel Execution**: Run multiple agents concurrently on different aspects of a project
- **Quality Gates**: Built-in validation hooks ensure code quality before completion
- **Session Tracking**: Maintain context and state across development sessions
- **Slash Commands**: Pre-built commands for common workflows (`/start`, `/end`, `/api`, `/dev`, etc.)

## Architecture

The system uses a hierarchical coordination model:

```
Claude Opus (Orchestrator)
    |
    +-- Claude Sonnet (Implementation)
    +-- GLM-4 (Documentation & Testing)
    +-- Code Interpreter (Security & Analysis)
    +-- Gemini Pro (Large Context Tasks)
```

## Quick Start

### Prerequisites

- Python 3.8+
- Claude Code CLI
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/CarlosIrineuCosta/agent-system.git
cd agent-system

# Install (copies hooks and commands to ~/.claude/)
pip install -e .

# Configure your API keys
./scripts/install.sh

# Restart Claude Code
```

The install script prompts for:
- Claude API key (required) - https://console.anthropic.io/
- GLM API key (required) - https://open.bigmodel.cn/
- Optional: Codex, SambaNova, OpenRouter keys

All secrets are stored locally in `.env` with permissions 600, never committed to git.

## Usage

Once installed, the system integrates with Claude Code:

```bash
# Start a development session
cd your-project
claude

# Use slash commands
/start     # Initialize session tracking
/end       # Finalize session and generate summary
/api       # Switch to API development mode
/dev       # Switch to development mode
```

## Configuration

### Agent Routing

Edit `config/agent_routing.json` to customize task-to-agent mappings:

```json
{
  "routing": {
    "architecture": ["claude-opus"],
    "implementation": ["claude-sonnet"],
    "documentation": ["glm-4"],
    "security": ["codex"]
  }
}
```

### Hooks

Hooks in `config/hooks_settings.json` control quality gates and validation:

```json
{
  "post_tool_use": {
    "enabled": true,
    "validator": "quality_gate"
  }
}
```

## Directory Structure

```
agent-coordinator/
├── commands/           # Slash command definitions
├── config/            # Configuration files
│   ├── agent_routing.json
│   └── hooks_settings.json
├── docs/              # Documentation
├── hooks/             # Quality control hooks
│   ├── core/          # Quality gates, completion checkers
│   ├── auxiliary/     # Root protection
│   └── session/       # Session tracking
├── scripts/           # Python utilities
│   ├── install.sh     # Interactive installer
│   ├── multi_llm_coordinator.py
│   └── parallel_coordinator.py
├── prompts/           # Agent-specific prompts
├── setup.py           # Package installer
└── .env.example       # Environment template
```

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/install.sh` | Interactive API key setup |
| `scripts/multi_llm_coordinator.py` | Multi-agent coordination |
| `scripts/parallel_coordinator.py` | Parallel task execution |

## Documentation

- `docs/coordination/TASK_SYSTEM.md` - Task tracking and state management
- `docs/coordination/FILE_WRITING_RULES.md` - File operation guidelines
- `docs/coordination/PARALLEL_EXECUTION.md` - Parallel execution architecture
- `docs/coordination/VISIBILITY_SYSTEM.md` - Context and visibility rules

## Requirements

- Python 3.8+
- No external dependencies (uses standard library only)

## License

MIT License - see LICENSE file for details

## Contributing

Contributions welcome. Please:
1. Follow existing code patterns
2. Add tests for new features
3. Update documentation
4. Run `python validate.py` before submitting

## Support

For issues, questions, or contributions, please use the GitHub issue tracker.
