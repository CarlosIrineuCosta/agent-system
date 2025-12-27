# Agent System Integration Guide

This guide explains how to integrate the Agent System with external projects like Lumen, following the Single Source of Truth (SSOT) approach.

## What is SSOT?

**Single Source of Truth (SSOT)** means this repository is the authoritative source for the agent system implementation. Instead of copying or forking the agent system code into your project, you integrate it as an external dependency. This approach ensures:

- All projects use the same tested version
- Bug fixes and improvements benefit all projects automatically
- No code duplication or drift
- Centralized maintenance and updates

## Integration Methods

### Method 1: Git Submodule (Recommended)

Git submodules allow you to include the agent system as a nested repository while maintaining its connection to the original source.

#### Step 1: Add the Submodule

```bash
# Navigate to your project root
cd /path/to/your/project

# Add agent-system as a submodule
git submodule add https://github.com/CarlosIrineuCosta/agent-system.git agent-system

# Initialize and update the submodule
git submodule update --init --recursive
```

This creates:
- `.gitmodules` file tracking the submodule
- `agent-system/` directory containing the agent system code
- Git tracking for the specific commit used

#### Step 2: Set Up Project Structure

```bash
# Create necessary directories in your project
mkdir -p .claude/hooks .claude/commands

# Create symlinks for seamless integration
ln -s ../../agent-system/hooks/* .claude/hooks/
ln -s ../../agent-system/commands/* .claude/commands/
```

#### Step 3: Configure the Agent System

```bash
# Copy configuration templates
cp agent-system/config/hooks_settings.json .claude/settings.json
cp agent-system/config/agent_routing.json .claude/agent_routing.json

# Set required environment variable
echo "export CLAUDE_TRUSTED_WORKSPACE=$(pwd)" >> .env
```

#### Step 4: Commit Integration

```bash
git add .gitmodules .claude/ .env
git commit -m "Integrate agent-system as SSOT submodule"
```

### Method 2: Package Installation (Future)

Future versions will support pip installation:

```bash
pip install agent-system
agent-system init --project-type your-type
```

## Project-Specific Configuration

While the agent system code is shared, each project needs its own configuration:

### 1. Project Type Detection

Create `.claude/project_type.json`:
```json
{
  "type": "web-application",
  "framework": "fastapi",
  "database": "postgresql",
  "deployment": "docker"
}
```

### 2. Custom Hooks

Project-specific hooks can be added to `.claude/hooks/custom/`:
```python
# .claude/hooks/custom/project_validation.py
def validate_project_specific():
    # Your custom validation logic
    pass
```

### 3. Agent Routing Overrides

Extend the default routing in `.claude/agent_routing.json`:
```json
{
  "extends": "../agent-system/config/agent_routing.json",
  "overrides": {
    "routes": {
      "database": "specialized-db-agent"
    }
  }
}
```

## Working with Submodules

### Updating the Agent System

```bash
# Navigate to submodule directory
cd agent-system

# Pull latest changes
git pull origin main

# Return to project and commit update
cd ..
git add agent-system
git commit -m "Update agent-system to latest version"
```

### Checking for Updates

```bash
# Check submodule status
git submodule status

# Check for remote updates
cd agent-system
git fetch
git log HEAD..origin/main
```

### Pinning to a Specific Version

```bash
# Use a specific tag or commit
cd agent-system
git checkout v1.2.0
cd ..
git add agent-system
git commit -m "Pin agent-system to v1.2.0"
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: CI with Agent System
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          submodules: recursive

      - name: Validate Agent System
        run: |
          cd agent-system
          python validate.py

      - name: Run Project Tests
        run: |
          # Your test commands
```

### Docker Integration

```dockerfile
# Dockerfile
FROM python:3.9

# Clone with submodules
RUN git clone --recurse-submodules https://github.com/youruser/yourproject.git .
RUN cd agent-system && pip install -r requirements.txt

# Continue with your Docker setup
```

## Troubleshooting

### Common Issues

1. **Submodule not initialized**
   ```bash
   git submodule update --init --recursive
   ```

2. **Detached HEAD in submodule**
   ```bash
   cd agent-system
   git checkout main
   ```

3. **Stale symlinks after pull**
   ```bash
   # Recreate symlinks
   rm .claude/hooks/* .claude/commands/*
   ln -s ../../agent-system/hooks/* .claude/hooks/
   ln -s ../../agent-system/commands/* .claude/commands/
   ```

### Validation Commands

```bash
# Check agent system health
cd agent-system
python validate.py

# Verify integration
cd ..
python -c "
import os
assert os.path.exists('.claude/hooks/core/quality_gate.py')
assert os.path.exists('.claude/commands/start.md')
print('Integration successful!')
"
```

## Best Practices

### 1. Version Management
- Always pin to a specific tag or commit for production
- Use semantic versioning (v1.0.0, v1.1.0, etc.)
- Document version compatibility in your project

### 2. Configuration Management
- Never modify files inside the agent-system directory
- Keep all custom configurations in your project's .claude/
- Use environment variables for project-specific settings

### 3. Team Collaboration
- Add `.gitmodules` to your project's `.gitignore` documentation
- Include submodule update instructions in your project's README
- Train team members on submodule workflow

### 4. Backup and Recovery
- The submodule reference is tracked in `.gitmodules`
- Regular commits ensure you can recover the exact version used
- Tag releases with the agent-system version for reference

## Migration from Copied Code

If you currently have a copied version of the agent system:

1. **Identify Customizations**
   ```bash
   diff -r agent-system-copy/ agent-system-standalone/ > customizations.patch
   ```

2. **Replace with Submodule**
   ```bash
   rm -rf agent-system-copy/
   git submodule add https://github.com/CarlosIrineuCosta/agent-system.git agent-system
   ```

3. **Apply Customizations Properly**
   - Move custom hooks to `.claude/hooks/custom/`
   - Add configuration overrides to `.claude/`
   - Document customizations for future reference

## Support and Contributing

- **Issues**: Report bugs at https://github.com/CarlosIrineuCosta/agent-system/issues
- **Discussions**: Use GitHub Discussions for questions and ideas
- **Contributions**: Follow the contributing guidelines in the agent-system repository

---

Remember: This integration approach ensures all projects benefit from improvements while allowing project-specific customizations where needed.