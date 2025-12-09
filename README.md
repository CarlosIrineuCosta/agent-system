# Agent System Standalone

A comprehensive multi-agent development system that provides structured coordination between specialized AI agents for efficient software engineering workflows.

## Overview

The Agent System Standalone implements a hierarchical coordination model where Claude serves as the primary orchestrator and multiple specialized agents handle domain-specific tasks. This system enables parallel processing, quality control, and structured communication across different technical domains.

## Architecture Overview

The system employs a multi-agent architecture with distinct roles and responsibilities:

### Primary Agents

- **Claude Opus**: Acts as the primary architect and orchestrator
  - High-level strategic planning and design
  - Cross-domain coordination and integration
  - Quality oversight and final validation
  - See `/config/agent_routing.json` for routing rules

- **Claude Sonnet**: Handles implementation and coding tasks
  - Backend and frontend development
  - Code generation and optimization
  - Implementation of architectural designs
  - Follows standardized interfaces and patterns

- **GLM-4**: Specialized in technical documentation and testing
  - Code documentation and README generation
  - Test case development and validation
  - Technical writing and explanation
  - See `/config/hooks_settings.json` for integration

- **Code Interpreter**: Focuses on security and code analysis
  - Security validation and vulnerability assessment
  - Code optimization and performance analysis
  - Review and audit of implementations
  - Integration with quality gates

- **Gemini Pro**: Handles large-context tasks
  - Comprehensive codebase analysis
  - Architecture review and validation
  - Large-scale documentation generation
  - Multi-file coordination tasks

### System Characteristics

- **Hierarchical Coordination**: Clear separation between architectural and implementation layers
- **Parallel Processing**: Multiple agents work concurrently on different domains
- **Quality Gates**: Built-in validation at critical workflow points
- **Session Integration**: Comprehensive state tracking across sessions
- **Cross-Agent Review**: Automatic reviewer rotation system

## Installation Instructions

### Prerequisites

- Python 3.8 or higher
- Claude Code CLI integration
- Git for version control

### Quick Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/CarlosIrineuCosta/agent-system.git
   cd agent-system
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up configuration**
   ```bash
   cp config/hooks_settings.json ~/.claude/settings.json
   cp config/agent_routing.json ~/.claude/agent_routing.json
   ```

4. **Install hooks**
   ```bash
   python scripts/setup_hooks.sh
   ```

5. **CRITICAL: Enable Slash Commands** (Required for /start, /end, /api, etc.)
   ```bash
   # Copy hooks and commands to project directory
   mkdir -p .claude/hooks .claude/commands
   cp -r hooks/* .claude/hooks/
   cp -r commands/* .claude/commands/

   # Set required environment variable
   echo "export CLAUDE_TRUSTED_WORKSPACE=$(pwd)" >> .env
   ```

### Configuration Files

- **`/config/hooks_settings.json`**: Hook configuration for quality control
- **`/config/agent_routing.json`**: Agent routing rules and task mappings
- **`/config/VERSION`**: System version information

## Quick Start Guide

### Basic Usage

1. **Initialize a new project**
   ```bash
   python scripts/agent_coordinator.py --init-project my-project
   ```

2. **Run validation checks**
   ```bash
   python validate.py
   ```

3. **Start development session**
   ```bash
   cd my-project
   claude
   ```

### Common Commands

- **Process proposals**: `python scripts/process_proposals.py`
- **Multi-agent coordination**: `python scripts/multi_llm_coordinator.py`
- **Parallel task execution**: `python scripts/parallel_coordinator.py`

## Directory Structure

```
agent-system/
├── commands/                 # Executable command scripts
├── config/                  # System configuration files
│   ├── agent_routing.json   # Agent routing and task mapping
│   └── hooks_settings.json  # Hook configuration
├── docs/                    # Documentation and guides
│   └── VALIDATION_SCRIPT.md # Validation documentation
├── hooks/                   # Quality control hooks
│   ├── core/                # Core validation hooks
│   │   ├── quality_gate.py  # Quality validation
│   │   └── completion_checker.py # Task completion verification
│   ├── auxiliary/           # Helper hooks
│   │   └── root_protection.py # File system protection
│   └── session/            # Session management
│       └── session_tracker.py # State tracking
├── prompts/                # Agent-specific prompts
├── scripts/                 # Python utilities
│   ├── agent_coordinator.py # Main coordination script
│   ├── multi_llm_coordinator.py # Multi-agent coordination
│   ├── parallel_coordinator.py # Parallel task execution
│   ├── process_proposals.py # Proposal processing
│   └── gemini_wrapper.py   # Gemini integration
├── templates/              # Project initialization templates
├── validate.py              # System validation script
├── setup.py                # Package setup
└── requirements.txt        # Dependencies
```

### Component Explanations

- **Commands**: High-level operations for system management
- **Config**: Centralized configuration for routing and hooks
- **Hooks**: Quality control points that execute at workflow stages
- **Scripts**: Coordination and utility scripts for agent management
- **Templates**: Project initialization boilerplates and patterns
- **Prompts**: Agent-specific interaction templates

## Configuration Options

### Agent Routing Configuration

The routing system (`/config/agent_routing.json`) defines:

- **Task-to-agent mappings**: Which agent handles specific task types
- **Review rotation**: Automatic reviewer assignment (Claude→GLM→Codex→Claude)
- **Keyword detection**: Automatic agent selection based on task keywords

### Hook Configuration

Hooks (`/config/hooks_settings.json`) provide:

- **Post-tool use validation**: Quality checks after file modifications
- **Stop hooks**: Completion verification and session tracking
- **Custom validation**: Extensible quality control mechanisms

### Session Management

- **State tracking**: Maintains session context across interactions
- **Review prevention**: Avoids duplicate reviews in same session
- **Progress tracking**: Monitors task completion and milestones

## Usage Examples

### Example 1: Multi-Agent Development Workflow

```bash
# Initialize multi-agent project
python scripts/agent_coordinator.py --init-project web-app

# Start development session
cd web-app
claude

# System automatically routes tasks:
# - Claude Opus handles architecture and design
# - Claude Sonnet implements backend/frontend
# - GLM generates documentation
# - Code Interpreter performs security review
```

### Example 2: Parallel Task Execution

```bash
# Execute multiple agents in parallel
python scripts/parallel_coordinator.py --tasks "backend,frontend,docs"
```

### Example 3: Proposal Processing

```bash
# Process development proposals
python scripts/process_proposals.py --input proposals.json
```

## Contributing Guidelines

### Development Process

1. **Follow established patterns**: Use existing templates and interfaces
2. **Implement quality hooks**: Add appropriate validation for new features
3. **Update documentation**: Keep README and configuration current
4. **Test integration**: Ensure compatibility with existing components
5. **Use validation script**: Run `python validate.py` before commits

### Code Standards

- **Python 3.8+**: Use modern Python features and practices
- **Type hints**: Include type annotations for better code clarity
- **Error handling**: Implement robust error handling and logging
- **Documentation**: Include docstrings and comments
- **Testing**: Follow existing test patterns and conventions

### Extension Guidelines

- **New agents**: Must implement standardized interfaces
- **New hooks**: Should integrate with existing quality gates
- **New scripts**: Should follow established naming conventions
- **New configs**: Should maintain backward compatibility

## System Validation

The validation script (`validate.py`) provides comprehensive system health checks:

```bash
python validate.py
```

### Validation Coverage

- **Directory structure**: Verifies all required components exist
- **Configuration validation**: Checks syntax and completeness
- **Hook functionality**: Tests all hook components
- **Script validation**: Ensures Python scripts are syntactically correct
- **Agent routing**: Validates routing configuration
- **Session integration**: Tests state tracking mechanisms

### Health Assessment

- **System health score**: 0-100% overall rating
- **Component status**: Individual pass/fail indicators
- **Recommendations**: Actionable suggestions for improvements
- **Error details**: Specific error messages for failed checks

## Troubleshooting

### Common Issues

- **Hook failures**: Check hook configuration file syntax
- **Agent routing errors**: Verify agent routing configuration
- **Session tracking issues**: Ensure proper session initialization
- **Quality gate problems**: Check file permissions and paths

### Debug Commands

```bash
# Check system health
python validate.py

# Test individual components
python scripts/agent_coordinator.py --test
python scripts/multi_llm_coordinator.py --test
python scripts/parallel_coordinator.py --test
```

## Best Practices

1. **Task Definition**: Ensure tasks are well-defined before delegation
2. **Quality Gates**: Always pass through defined validation points
3. **Interface Compliance**: Maintain consistent interfaces between agents
4. **Progress Reporting**: Provide regular updates on task completion
5. **Documentation**: Keep documentation current with system changes

## Version Information

- **Current Version**: 1.0.0
- **Python Requirements**: 3.8+
- **Dependencies**: Standard library only
- **License**: [Specify license if applicable]

## Support

For issues and questions:
- **Documentation**: See `/docs/VALIDATION_SCRIPT.md` for detailed validation
- **Configuration**: Reference `/config/` directory for settings
- **Examples**: Check `/templates/` for usage patterns
- **Validation**: Run `python validate.py` for system health checks

---

*For detailed implementation guidance and advanced usage, refer to the specific configuration files and documentation referenced throughout this document.*