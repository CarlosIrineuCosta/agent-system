# Agent Permission Prompt Patterns - Test Results
**Generated**: 2025-12-31
**Test**: Permission prompt capture across multiple AI agents

---

## EXECUTIVE SUMMARY

Tested 4 AI agent tools to identify exact permission prompt patterns. Key finding: **permission prompts originate from different sources depending on the agent**.

| Agent | Method | Permission Source | Bypass Available |
|-------|--------|-------------------|------------------|
| GLM | Direct API | None (uses env var) | Yes |
| Codex | CLI tool | TTY requirement | Partial |
| Gemini | CLI tool | IDE extension check | Yes |
| OpenAI | Python CLI | Module not installed | N/A |

---

## TEST RESULTS DETAIL

### Test 1: GLM (via glm_direct.py)

**Command**:
```bash
python3 scripts/glm_direct.py "say hello"
```

**Result**: SUCCESS
```
Hello! How can I help you today?
```

**Permission Pattern**: None
- Uses `ANTHROPIC_AUTH_TOKEN` or `ZAI_API_KEY` environment variable
- Direct HTTP POST to `https://api.z.ai/api/anthropic/v1/messages`
- No interactive prompts
- No TTY requirement

**Code Reference** (`scripts/glm_direct.py:18-104`):
```python
def __init__(self, api_key: str = None, model: str = DEFAULT_MODEL):
    self.api_key = api_key or API_KEY
    self.endpoint = f"{BASE_URL}/v1/messages"
    self.headers = {
        'Content-Type': 'application/json',
        'x-api-key': self.api_key,
        'anthropic-version': '2023-06-01'
    }
```

**Verdict**: GLM is already non-interactive compatible. Use this pattern for other agents.

---

### Test 2: Codex CLI

**Command**:
```bash
codex --version
codex "say hello"
python3 scripts/codex_wrapper.py --task "say hello"
```

**Result**: FAIL (stdin requirement)
```
codex-cli 0.77.0
Error: stdin is not a terminal
```

**Permission Pattern**: Interactive TTY required
- Codex CLI requires terminal input
- Fails when called via subprocess without TTY
- Likely prompts for confirmation in interactive mode

**Code Reference** (`scripts/codex_wrapper.py:74-81`):
```python
result = subprocess.run(
    cmd,
    capture_output=True,
    text=True,
    timeout=300,
    cwd=Path.cwd()
)
```

**Issue**: Wrapper passes prompt as command-line argument, but Codex expects stdin.

**Verdict**: Need to either:
1. Use `expect` automation script (existing in `/simple-agents/agent-new/wrappers/codex.exp`)
2. Find Codex direct API endpoint
3. Use stdin redirection with pty module

---

### Test 3: Gemini CLI

**Command**:
```bash
gemini "say hello"
python3 scripts/gemini_wrapper.py --task "say hello"
```

**Result**: PARTIAL
```
Loaded cached credentials.
[ERROR] [IDEClient] Failed to connect to IDE companion extension in VS Code.
Hello! I'm ready to assist you today.
```

**Permission Pattern**: IDE dependency check
- Shows IDE companion extension error
- Proceeds anyway after showing warning
- No actual blocking permission prompt

**Code Reference** (`scripts/gemini_wrapper.py:68-72`):
```python
cmd = [GEMINI_CLI, '--model', model, '--max-tokens', '800000']
cmd.extend(['--prompt', prompt])
```

**Issue**: When called with many files, hits OS argument limit:
```
OSError: [Errno 7] Argument list too long: 'gemini'
```

**Verdict**: Gemini is mostly compatible but:
1. IDE error is cosmetic (can suppress stderr)
2. Large context via CLI args fails - need stdin or file-based input

---

### Test 4: OpenAI CLI

**Command**:
```bash
openai api chat.completions.create -m gpt-4 --messages '[{"role":"user","content":"say hello"}]'
```

**Result**: FAIL (module not installed)
```
ModuleNotFoundError: No module named 'openai'
```

**Verdict**: OpenAI CLI not properly installed. Recommend using direct Python requests instead.

---

## ARCHITECTURAL RECOMMENDATIONS

### For Non-Interactive Agent Orchestration

1. **Use GLM Pattern**: Direct HTTP API calls with environment variable auth
   - No subprocess calls
   - No TTY dependencies
   - Fully automated

2. **Avoid Subprocess for Interactive CLIs**:
   - Codex requires TTY
   - Gemini has argument length limits
   - Both fail in non-interactive contexts

3. **Implement Agent Abstraction Layer**:

```python
class AgentClient(ABC):
    @abstractmethod
    def send_message(self, prompt: str, context: list = None) -> dict:
        pass

class GLMAgent(AgentClient):
    def send_message(self, prompt, context=None):
        # Direct HTTP POST
        response = requests.post(self.endpoint, json=payload)
        return response.json()

class CodexAgent(AgentClient):
    def send_message(self, prompt, context=None):
        # Use expect script or direct API
        pass
```

---

## EXISTING INTEGRATION POINTS

### Available Wrappers in agent-coordinator

| Script | Purpose | Status |
|--------|---------|--------|
| `glm_direct.py` | Direct GLM API | Working |
| `codex_wrapper.py` | Codex CLI wrapper | Fails (stdin) |
| `gemini_wrapper.py` | Gemini CLI wrapper | Fails (arg limit) |

### External Wrappers (need integration)

From `/simple-agents/agent-new/wrappers/`:
- `cline_glm.exp` - Expect script for Cline/GLM
- `gemini.exp` - Expect script for Gemini
- `codex.exp` - Expect script for Codex

**These expect scripts may solve the TTY issues.**

---

## NEXT STEPS (Request Claude Desktop)

### Option A: Integrate Expect Scripts
Copy and integrate expect wrappers from `/simple-agents/agent-new/wrappers/` into agent-coordinator

### Option B: Direct API for All Agents
Research and implement direct HTTP API calls for Codex and Gemini (matching GLM pattern)

### Option C: Stdin/PTY Wrapper
Create Python wrapper using `pty` module to fake TTY for interactive CLIs

---

## TEST LOG

Full test output saved to: `/tmp/agent-test-log.txt`

```
=== Testing Cline/GLM ===
/bin/bash: line 1: cline-cli: command not found

=== Testing Gemini ===
Loaded cached credentials.
[ERROR] [IDEClient] Failed to connect to IDE companion extension in VS Code.
Hello! I'm ready to assist you today?

=== Testing Codex ===
Traceback (most recent call last):
  File "/home/cdc/.local/bin/openai", line 3, in <module>
    from openai.cli import main
ModuleNotFoundError: No module named 'openai'

=== Testing Codex ===
codex-cli 0.77.0
Error: stdin is not a terminal

=== Testing GLM Script ===
Hello! How can I help you today?
```

---

**End of Report**

Pending: Instructions from Claude Desktop on preferred integration approach.
