# Recommendations (Current)
**Updated**: 2026-01-01
**Scope**: CLI-only, no direct API usage

---

## Overall Assessment
The system drifted into an API-centric design (Z.ai/MiniMax Anthropic-compatible endpoints) while the project constraint is "no APIs ever." That caused model identity confusion (Anthropic labels pointing to non-Anthropic endpoints) and led to wrapper implementations that must be retired. Going forward, the agentic system should be CLI-only: Claude Code as primary, and OpenCode or other CLI tools as secondary, with hooks and routing done via bash. This clarifies model provenance, aligns with plan/CLI usage, and avoids hidden endpoint swaps.

## Current Recommendations
1. **Keep Claude Code on Anthropic**: Do not set `ANTHROPIC_BASE_URL` or `ANTHROPIC_AUTH_TOKEN`. Select `/model opus` or `/model sonnet` interactively rather than pinning IDs.
2. **Archive all direct-API wrappers**: `scripts/glm_direct.py`, `scripts/glm_cli.py`, `scripts/glm_internal.py`, `scripts/test_parallel_agents.py` are legacy and should remain archived.
3. **Make routing CLI-only**: Any cross-model routing must call CLIs via bash (Claude Code, OpenCode, Gemini CLI), not HTTP.
4. **Fix hook/command paths**: Claude Code slash commands must live in `.claude/commands/`, and hooks must be configured in `.claude/settings*.json`.
5. **Document a single source of truth**: Keep one short "current state" doc and link out to legacy investigations as reference.

## References
- **Legacy recommendations (archived)**: `archive/desktop-coordination/RECOMMENDATIONS_2025-12-31_LEGACY.md`
- **Current state overview**: `docs/desktop-coordination/CURRENT_STATE.md`

## How To Use These Docs
1. Read `docs/desktop-coordination/CURRENT_STATE.md` first for the latest ground truth.
2. Use this file for current action items only (CLI-only, no APIs).
3. Consult archived docs only when you need provenance or historical context.
