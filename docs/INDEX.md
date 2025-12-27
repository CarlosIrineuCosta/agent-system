# Agent Coordinator Documentation Index

## Quick Links

- **[Summary of Checkpoints](coordination/SUMMARY.md)** - Key takeaways from all development work
- **[System Status](SYSTEM_STATUS.md)** - **SSOT** - Current task list and progress

## Architecture

- **[Architecture](architecture.md)** - System overview with mermaid diagrams

## Working Documentation

### Coordination Guides
- **[Summary](coordination/SUMMARY.md)** - Checkpoint summaries and quick reference
- **[File Writing Rules](coordination/FILE_WRITING_RULES.md)** - What agents can/cannot write
- **[Garbage Collection](coordination/GARBAGE_COLLECTION.md)** - Cleanup policies and usage
- **[Safe Self-Development](coordination/SAFE_SELF_DEVELOPMENT.md)** - Sandbox pattern for self-modification
- **[Visibility System](coordination/VISIBILITY_SYSTEM.md)** - Real-time monitoring guide
- **[Parallel Execution](coordination/PARALLEL_EXECUTION.md)** - Multi-agent coordination patterns

## File Roles

| File | Role | Update Frequency |
|------|------|-----------------|
| `SYSTEM_STATUS.md` | **SSOT** - Current tasks & checkpoints | After every task |
| `coordination/SUMMARY.md` | Checkpoint reference | When checkpoints complete |
| `archive/tasks_*.md` | Historical snapshots (read-only) | Never |

## Archived Documentation

*(Located in `archive/` directory - historical reference only)*

- `archive/tasks_20251226.md` - System state as of 2025-12-26 (all core features completed)
- `integration.md` - Old git submodule docs (superseded by symlink approach)
- `FOR_CLAUDE_INSTALLATION.md` - Installation guide
- `install-guide.md` - Duplicate installation guide
- `IMPLEMENTATION_SUMMARY.md` - Original implementation summary

## Script Reference

| Script | Purpose |
|--------|---------|
| `multi_llm_coordinator.py` | Route tasks to appropriate LLMs |
| `glm_direct.py` | GLM-4.7 API via Z.ai endpoint |
| `monitor.py` | Terminal-based agent monitoring |
| `garbage_collector.py` | Cleanup old outputs/logs |
| `sandbox_manager.py` | Safe self-development |
| `state_manager.py` | Lifecycle management (skeleton) |
| `codex_wrapper.py` | Codex CLI integration |
| `gemini_wrapper.py` | Gemini API integration |

## Configuration Files

| File | Purpose |
|------|---------|
| `config/agent_routing.json` | Task → agent mappings |
| `config/agent_rules.json` | File writing restrictions |
| `config/hooks_settings.json` | Hook configuration |

## Quick Start

### Run an Agent Task
```bash
python scripts/multi_llm_coordinator.py --task "Implement tests"
```

### Monitor Activity
```bash
python scripts/monitor.py
```

### Safe Self-Development
```bash
python scripts/sandbox_manager.py create    # Create sandbox
python scripts/sandbox_manager.py promote   # Merge to canonical
```

---

**Version:** 1.0.0-alpha | **Last Updated:** 2025-12-27
