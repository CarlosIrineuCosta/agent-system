# Lumen Project

A comprehensive image processing and storage management system with modern architecture and agent-based development workflow.

## Quick Start

This project uses an external **agent-system** dependency for development workflow management. The agent-system provides structured coordination between development tasks and quality assurance processes.

### Agent System Integration

**Important**: The agent-system is now managed as an external dependency, not as a Git submodule.

#### Setup Agent System

1. **Clone the agent-system repository**:
   ```bash
   # Clone to your preferred external location
   git clone https://github.com/CarlosIrineuCosta/agent-system.git ~/agent-system
   ```

2. **Install and configure hooks**:
   ```bash
   cd ~/agent-system
   ./scripts/setup_hooks.sh /path/to/your/lumen/project
   ```

3. **Validate installation**:
   ```bash
   cd ~/agent-system
   python3 validate.py --project /path/to/your/lumen/project
   ```

#### Agent System Features

The external agent-system provides:
- **Multi-agent coordination**: Structured task delegation and management
- **Quality gates**: Automated validation and code review processes
- **Session tracking**: Development session state management
- **Hook system**: Pre/post-operation validation and quality checks
- **Agent routing**: Intelligent task assignment to specialized agents

## Lumen Architecture

### Core Components

1. **Backend API**: FastAPI-based REST service
2. **Frontend Interface**: Modern web UI
3. **Image Processing**: Advanced image manipulation and storage
4. **Database Layer**: PostgreSQL with SQLAlchemy ORM
5. **Agent Integration**: External agent-system for development workflow

### Development Workflow

1. **Set up external agent-system** (see above)
2. **Initialize project environment**:
   ```bash
   cd lumen
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```
4. **Run development server**:
   ```bash
   python3 main.py
   ```

## Project Structure

```
lumen/
├── backend/           # FastAPI backend service
├── frontend/          # Web interface
├── docs/             # Project documentation
├── scripts/          # Utility scripts
├── config/           # Configuration files
└── storage/          # Image processing and storage
```

## Getting Help

- **Agent System Documentation**: See your external agent-system installation
- **Lumen Documentation**: See `docs/` directory
- **Issues**: Report in the project repository

## Development with Agent System

When the agent-system hooks are properly installed, you'll have access to:
- `/start` - Begin development sessions
- `/end` - Complete sessions with review
- `/check` - Run quality validation
- `/audit` - Comprehensive project analysis
- `/deploy` - Deployment pipeline management

## Agent Workflow

### Typical Workflow Process

1. **Project Analysis**: Orchestrator conducts initial project assessment
2. **Task Decomposition**: High-level tasks broken into domain-specific components
3. **Agent Assignment**: Tasks delegated to appropriate specialized agents
4. **Parallel Execution**: Agents work concurrently in their domains
5. **Quality Validation**: Results pass through quality gates
6. **Integration**: Components are integrated and tested
7. **Completion Verification**: Final validation against project requirements

### Communication Flow

- **Upward Communication**: Agents report progress and issues to orchestrator
- **Downward Communication**: Orchestrator provides guidance and constraints
- **Peer Communication**: Agents coordinate interfaces and dependencies
- **Artifact Exchange**: Structured exchange of deliverables between agents

## Directory Structure

```
agent-system/
├── commands/          # Executable command scripts
├── config/           # Configuration files and settings
├── docs/             # Documentation and guides
├── hooks/            # Quality control and validation hooks
│   ├── core/         # Core validation hooks
│   └── auxiliary/    # Helper and utility hooks
├── prompts/          # Agent-specific prompts and templates
├── scripts/          # Python utilities and coordination scripts
├── templates/        # Project initialization templates
└── validate.py       # System validation script
```

### Component Roles

- **Commands**: High-level operations and system commands
- **Hooks**: Quality control points and validation logic
- **Scripts**: Coordination and utility scripts
- **Templates**: Project initialization boilerplates
- **Prompts**: Agent-specific interaction patterns

## System Operation

### Claude as Orchestrator

Claude operates as the central orchestrator with these responsibilities:

- **Strategic Planning**: Defines high-level project architecture and approach
- **Resource Allocation**: Assigns tasks to appropriate specialized agents
- **Quality Oversight**: Ensures deliverables meet quality standards
- **Integration Management**: Coordinates between different agent outputs
- **Progress Tracking**: Monitors overall project progress and milestones

### Specialized Agents

Specialized agents operate with clear boundaries:

- **Domain Expertise**: Each agent focuses on specific technical domains
- **Interface Compliance**: Agents follow standardized interfaces and protocols
- **Autonomous Operation**: Agents execute tasks independently within constraints
- **Quality Accountability**: Agents ensure their deliverables meet quality standards

### Coordination Mechanisms

The system uses several coordination mechanisms:

- **Structured Prompts**: Well-defined interaction templates for consistent communication
- **Quality Gates**: Validation points that must be passed before proceeding
- **Artifact Standards**: Defined formats and structures for exchanged deliverables
- **Progress Reporting**: Regular status updates and milestone tracking

## Troubleshooting

For troubleshooting guidance, see `/docs/troubleshooting.md`. Key topics covered:
- Common issues and their solutions
- Debug hook failures and quality gate problems
- Agent communication troubleshooting
- Configuration and setup issues

## Best Practices

1. **Clear Task Definition**: Ensure tasks are well-defined before delegation
2. **Quality Gates**: Always pass through defined validation points
3. **Interface Compliance**: Maintain consistent interfaces between agents
4. **Progress Reporting**: Provide regular updates on task completion
5. **Documentation**: Keep documentation current with system changes

## Contributing

When extending the system:

1. **Define Clear Interfaces**: New agents must follow established patterns
2. **Implement Quality Hooks**: Add appropriate validation for new components
3. **Update Documentation**: Keep README and docs current
4. **Test Integration**: Ensure new components work with existing system
5. **Follow Templates**: Use established patterns for consistency

---

*For detailed implementation guidance, refer to the specific documentation files and templates referenced throughout this document.*