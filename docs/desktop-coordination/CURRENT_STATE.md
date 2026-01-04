# Current State (Single Source of Truth)
**Updated**: 2026-01-01

## What is true right now
- Claude Code is back on Anthropic models (no base URL override).
- The system must be CLI-only; direct HTTP API calls are disallowed.
- Legacy direct-API wrappers are archived under `archive/legacy_api/`.

## What went wrong
- Model identity drift: Anthropic labels were routed to Z.ai endpoints via `ANTHROPIC_BASE_URL`, producing non-Anthropic outputs.
- Investigation docs recommended direct API usage, which violates the no-API rule.
- Multiple plans and duplicated docs created confusion about the actual execution path.

## What we will keep
- Claude Code as primary orchestrator (slash commands, hooks, skills).
- OpenCode as a CLI-based secondary model runner if needed.
- Bash-based routing and plan execution (no SDKs, no HTTP clients).

## Known constraints
- Do not set `ANTHROPIC_BASE_URL` or `ANTHROPIC_AUTH_TOKEN` in production shells.
- Do not pin model IDs in env vars; prefer `/model opus` or `/model sonnet`.
- Any model access for GLM/MiniMax must be via CLI wrappers only.

## Files to treat as legacy (reference only)
- `archive/desktop-coordination/RECOMMENDATIONS_2025-12-31_LEGACY.md`
- `archive/desktop-coordination/INVESTIGATION_FINDINGS.md`
- `archive/desktop-coordination/IMPLEMENTATION_ROADMAP.md`
- `archive/desktop-coordination/CONVERSATION_HANDOFF_2026-01-01.md`

## Files to keep as authoritative
- `docs/desktop-coordination/RECOMMENDATIONS.md`
- `docs/desktop-coordination/CURRENT_STATE.md`

## Open questions (to resolve in the next pass)
- Which CLI tool(s) should front GLM/MiniMax without touching HTTP endpoints?
- Should `scripts/multi_llm_coordinator.py` be retained, or replaced with a pure bash router?
- Which existing hooks should be kept, removed, or relocated to `.claude/`?
