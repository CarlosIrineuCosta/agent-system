# Agent System Setup Guide

This guide explains how to set up the external agent-system dependency for Lumen projects.

## Overview

Lumen uses an external agent-system repository to provide development workflow management, quality assurance, and multi-agent coordination. This approach keeps the development tools separate from the application code while providing powerful automation capabilities.

## Prerequisites

- Git installed
- Python 3.11+ installed
- Access to the agent-system repository
- Appropriate permissions for your development environment

## Installation Steps

### 1. Clone the Agent System Repository

Choose a permanent location for the agent-system on your development machine:

```bash
# Recommended location in your home directory
git clone https://github.com/CarlosIrineuCosta/agent-system.git ~/agent-system

# Alternative location
git clone https://github.com/CarlosIrineuCosta/agent-system.git ~/.agent-system

# Or in a development tools directory
mkdir -p ~/dev-tools
git clone https://github.com/CarlosIrineuCosta/agent-system.git ~/dev-tools/agent-system
```

### 2. Update the Agent System

Keep the agent-system up to date:

```bash
cd ~/agent-system  # or your chosen location
git pull origin main
```

### 3. Install Hooks for Your Lumen Project

Run the setup script to configure the agent-system hooks for your specific Lumen project:

```bash
cd ~/agent-system
./scripts/setup_hooks.sh /path/to/your/lumen/project
```

For example:
```bash
./scripts/setup_hooks.sh /home/cdc/Storage/projects/lumen
```

### 4. Validate the Installation

Verify that the agent-system is properly installed and configured:

```bash
cd ~/agent-system
python3 validate.py --project /path/to/your/lumen/project
```

### 5. Verify Hook Configuration

Check that the hooks are properly configured:

```bash
# Check Claude settings
ls -la /path/to/lumen/.claude/settings.json

# Check hook symlinks
ls -la /path/to/lumen/.claude/hooks/

# Check configuration
cat /path/to/lumen/.claude/hooks_settings.json
```

## Agent System Features

Once installed, the agent-system provides the following capabilities:

### Available Commands

When using Claude Code with the agent-system hooks installed, you have access to:

- `/start` - Begin a structured development session
- `/end` - Complete a session with comprehensive review
- `/check` - Run quality validation and health checks
- `/audit` - Perform comprehensive project analysis
- `/deploy` - Execute deployment pipeline with safety checks
- `/dev` - Start development environment with auto-restart
- `/api` - Backend API development and integration
- `/ui` - Frontend UI development and design
- `/security-review` - Security vulnerability scanning
- `/edis` - EDIS Swiss VPS health monitoring
- `/edis-enhanced` - Enhanced EDIS monitoring with safety analysis

### Quality Assurance

The agent-system provides automated:

- Code quality gates and linting
- Security vulnerability scanning
- Performance profiling
- Documentation validation
- Test coverage analysis
- Dependency vulnerability checking

### Session Management

- Development session tracking
- State persistence across sessions
- Progress monitoring and reporting
- Automated session summaries

## Troubleshooting

### Common Issues

1. **Hooks not found**:
   - Ensure the setup script completed successfully
   - Check that symlinks were created in `.claude/hooks/`
   - Verify the agent-system path is correct

2. **Permission errors**:
   - Ensure the agent-system directory is writable
   - Check file permissions on hook scripts
   - Run setup script with appropriate permissions

3. **Python path issues**:
   - Ensure Python 3.11+ is being used
   - Check that required packages are installed
   - Verify virtual environment if using one

### Validation Issues

If validation fails, check:

1. Agent-system directory exists and is accessible
2. Python dependencies are installed
3. Hook scripts have execute permissions
4. Configuration files are properly formatted
5. Symlinks are correctly created

### Getting Help

- Check the agent-system documentation in your installation
- Review validation output for specific issues
- Ensure all prerequisites are met
- Verify the agent-system version is up to date

## Maintenance

### Regular Updates

Keep your agent-system installation updated:

```bash
cd ~/agent-system
git pull origin main
```

### Re-running Setup

If you encounter issues or need to reconfigure:

```bash
# Remove existing configuration (if needed)
rm -f /path/to/lumen/.claude/settings.json
rm -rf /path/to/lumen/.claude/hooks/

# Re-run setup
cd ~/agent-system
./scripts/setup_hooks.sh /path/to/lumen/project
```

### Project-Specific Configuration

Each Lumen project can have its own agent-system configuration. The setup script creates project-specific hook configurations while sharing the core agent-system code.

## Best Practices

1. **Use a consistent agent-system location** across projects
2. **Keep agent-system updated** regularly
3. **Run validation** after major changes
4. **Commit hook configuration** with your project (excluding sensitive data)
5. **Document any project-specific** agent-system customizations

## Integration with Development Workflow

The agent-system integrates seamlessly with your development workflow:

1. **Start sessions** with `/start` for structured development
2. **Use quality gates** automatically during development
3. **Track progress** with session management
4. **Validate changes** before commits with `/check`
5. **Deploy safely** with `/deploy` commands

This external dependency approach provides powerful development tools while keeping your project repository clean and focused.