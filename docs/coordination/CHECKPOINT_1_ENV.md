# Environment Configuration Map

## Current State

| Item | Location/Value |
|------|----------------|
| **Global config** | `~/.config/secrets/ai.env` |
| **Sourced by** | `~/.bashrc` line 42: `[ -f ~/.config/secrets/ai.env ] && . ~/.config/secrets/ai.env` |
| **GLM version** | `glm-4.7` (set in `ai.env`, updated 2025-12-26) |
| **Active key** | `ANTHROPIC_AUTH_TOKEN` (Z.ai API key) |
| **Endpoint** | `https://api.z.ai/api/anthropic` |

### Projects with `.env` files
- `/agent-coordinator/.env` - **placeholders only** (not configured)
- `/zora/.env` - contains `CLAUDE_TRUSTED_WORKSPACE` only
- `/lumen-2026/.env` - contains `CLAUDE_TRUSTED_WORKSPACE` only
- `/photo-tagger/.env` - contains `CLAUDE_TRUSTED_WORKSPACE` only
- `/crypto-trader/.env` - unknown content
- `/lumen-broken-20251212/.env` - unknown content

### GLM Version References in agent-coordinator
| File | Current Version |
|------|-----------------|
| `scripts/glm_direct.py` | `glm-4.5` (hardcoded) |
| `scripts/glm_internal.py` | `glm-4.5-flash` |
| `scripts/glm_cli.py` | `glm-4.5` |
| `.env` | `glm-4.5-flash` (placeholder) |

## How It Works

```
1. User opens shell
   ↓
2. ~/.bashrc loads
   ↓
3. Sources ~/.config/secrets/ai.env (if exists)
   ↓
4. Sets ANTHROPIC_* variables pointing to Z.ai
   ↓
5. Claude Code uses these to call GLM models
```

**Key variables in `ai.env`:**
- `ANTHROPIC_BASE_URL="https://api.z.ai/api/anthropic"`
- `ANTHROPIC_AUTH_TOKEN="<Z.ai API key>"`
- `ANTHROPIC_MODEL="glm-4.7"`
- `ANTHROPIC_SMALL_FAST_MODEL="glm-4.5-air"`

## What Needs to Change

1. **Mismatched variable names**: `glm_direct.py` looks for `GLM_API_KEY` but the actual setup uses `ANTHROPIC_AUTH_TOKEN` via Z.ai

2. **Hardcoded old versions**: Agent coordinator scripts have `glm-4.5` hardcoded while global config uses `glm-4.7`

3. **Unused .env**: The agent-coordinator `.env` file contains placeholder values that are never loaded

4. **No runtime directory**: `.agents/` has never been created - system has never executed

5. **Wrong endpoint**: `glm_direct.py` uses `https://api.z.ai/api/coding/paas/v4` but the working setup uses `https://api.z.ai/api/anthropic`

## The ACTUAL Working GLM Access Pattern

The "alternate access" is the **Anthropic-compatible Z.ai endpoint** that's already working:

```
ANTHROPIC_BASE_URL="https://api.z.ai/api/anthropic"
ANTHROPIC_AUTH_TOKEN="$ZAI_API_KEY"
ANTHROPIC_MODEL="glm-4.7"
```

This makes Z.ai GLM appear as a drop-in replacement for Claude's API. No special `GLM_API_KEY` needed.

### Why lumen-2026 glm_cli.py doesn't actually work

It tries to `from zai import ZaiClient` but the `zai` library is NOT installed. The real working path is the Anthropic-compatible endpoint already configured in `ai.env`.

## Recommendation

**Use the existing Anthropic-compatible Z.ai endpoint (`ANTHROPIC_*` variables) instead of `GLM_API_KEY`.**

The `glm_direct.py` in agent-coordinator was copied from another project and uses the wrong pattern. Fix it to use:
- `ZAI_API_KEY` (from `ai.env`)
- `https://api.z.ai/api/anthropic` endpoint
- Standard Anthropic API client (or requests with Anthropic headers)
