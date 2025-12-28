#!/bin/bash

###############################################################################
# Agent-Coordinator Installation Script
###############################################################################
# This script will:
#   1. Create necessary directories
#   2. Prompt you for API keys (stored locally only)
#   3. Set up Claude hooks and commands
#   4. Validate the installation
#
# SECURITY TRANSPARENCY:
#   - All secrets are stored in .env file at project root
#   - .env is set to permissions 600 (owner read/write only)
#   - .env is in .gitignore (never uploaded to git)
#   - You can inspect this script to verify everything it does
###############################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project root detection
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}============================================================================${NC}"
echo -e "${BLUE}  Agent-Coordinator Installation${NC}"
echo -e "${BLUE}============================================================================${NC}"
echo ""

# Step 1: Load configuration
echo -e "${YELLOW}[1/6] Loading configuration...${NC}"
CONFIG_FILE="$PROJECT_ROOT/INSTALL_CONFIG.json"

if [ ! -f "$CONFIG_FILE" ]; then
    echo -e "${RED}ERROR: INSTALL_CONFIG.json not found!${NC}"
    echo "Please ensure INSTALL_CONFIG.json exists in the project root."
    exit 1
fi

echo -e "${GREEN}Configuration loaded from: $CONFIG_FILE${NC}"
cat "$CONFIG_FILE" | grep -v "_comment"
echo ""

# Step 2: Explain security and storage
echo -e "${YELLOW}[2/6] Security & Storage Information${NC}"
echo ""
echo -e "${BLUE}WHERE secrets will be stored:${NC}"
echo "  File: $PROJECT_ROOT/.env"
echo ""
echo -e "${BLUE}HOW secrets will be stored:${NC}"
echo "  - File permissions: 600 (owner read/write only)"
echo "  - Location: Local project directory only"
echo "  - Git: .env is in .gitignore (never committed)"
echo ""
echo -e "${BLUE}WHAT secrets are needed:${NC}"
echo "  1. Claude API Key (anthropic.ai)"
echo "  2. GLM API Key (zhipuai.cn for Z.Ai)"
echo "  3. Codex CLI Key (optional, for security agent)"
echo "  4. SambaNova API Key (optional)"
echo "  5. OpenRouter API Key (optional)"
echo ""
echo -e "${YELLOW}You can skip optional keys by pressing Enter.${NC}"
echo ""

read -p "Press Enter to continue, or Ctrl+C to cancel..."
echo ""

# Step 3: Prompt for API keys
echo -e "${YELLOW}[3/6] Collecting API Keys${NC}"
echo ""

# Claude API
echo -e "${BLUE}Claude API Key${NC}"
echo "  Provider: anthropic.ai"
echo "  Used for: Primary LLM orchestration"
echo "  Get your key at: https://console.anthropic.io/"
read -p "  Enter your Claude API key (sk-ant-...): " CLAUDE_API_KEY
echo ""

# GLM API
echo -e "${BLUE}GLM API Key${NC}"
echo "  Provider: zhipuai.cn (Z.Ai integration)"
echo "  Used for: Chinese language tasks, documentation"
echo "  Get your key at: https://open.bigmodel.cn/"
read -p "  Enter your GLM API key: " GLM_API_KEY
echo ""

# Codex CLI (optional)
echo -e "${BLUE}Codex CLI Key (optional)${NC}"
echo "  Provider: Codex CLI"
echo "  Used for: Security analysis tasks"
read -p "  Enter your Codex CLI key (or press Enter to skip): " CODEX_API_KEY
echo ""

# SambaNova (optional)
echo -e "${BLUE}SambaNova API Key (optional)${NC}"
echo "  Provider: sambanova.ai"
echo "  Used for: Alternative LLM provider"
read -p "  Enter your SambaNova API key (or press Enter to skip): " SAMBANOVA_API_KEY
echo ""

# OpenRouter (optional)
echo -e "${BLUE}OpenRouter API Key (optional)${NC}"
echo "  Provider: openrouter.ai"
echo "  Used for: Multi-model routing"
read -p "  Enter your OpenRouter API key (or press Enter to skip): " OPENROUTER_API_KEY
echo ""

# Step 4: Create .env file with secure permissions
echo -e "${YELLOW}[4/6] Creating secure .env file...${NC}"

ENV_FILE="$PROJECT_ROOT/.env"

# Create .env file
cat > "$ENV_FILE" << EOF
# Agent-Coordinator Environment Configuration
# Generated: $(date)
# Permissions: 600 (owner read/write only)
# Location: Local only (in .gitignore)

# Claude API (Primary)
ANTHROPIC_API_KEY=$CLAUDE_API_KEY

# GLM API (Z.Ai)
GLM_API_KEY=$GLM_API_KEY

# Codex CLI (Security agent - optional)
$(if [ -n "$CODEX_API_KEY" ]; then echo "CODEX_API_KEY=$CODEX_API_KEY"; else echo "# CODEX_API_KEY=sk-..."; fi)

# SambaNova (optional)
$(if [ -n "$SAMBANOVA_API_KEY" ]; then echo "SAMBANOVA_API_KEY=$SAMBANOVA_API_KEY"; else echo "# SAMBANOVA_API_KEY=..."; fi)

# OpenRouter (optional)
$(if [ -n "$OPENROUTER_API_KEY" ]; then echo "OPENROUTER_API_KEY=$OPENROUTER_API_KEY"; else echo "# OPENROUTER_API_KEY=..."; fi)
EOF

# Set secure permissions
chmod 600 "$ENV_FILE"

echo -e "${GREEN}.env file created: $ENV_FILE${NC}"
echo -e "${GREEN}File permissions set to 600 (owner only)${NC}"
echo ""

# Step 5: Set up hooks and commands
echo -e "${YELLOW}[5/6] Setting up Claude hooks and commands...${NC}"

# Expand paths
CLAUDE_DIR="${HOME}/.claude"
HOOKS_DIR="$CLAUDE_DIR/hooks"
COMMANDS_DIR="$CLAUDE_DIR/commands"
PROJECT_HOOKS="$PROJECT_ROOT/hooks"
PROJECT_COMMANDS="$PROJECT_ROOT/commands"

# Create directories
mkdir -p "$HOOKS_DIR"
mkdir -p "$COMMANDS_DIR"

# Set up hooks
if [ -d "$PROJECT_HOOKS" ]; then
    echo "  Linking hooks from $PROJECT_HOOKS..."
    for hook in "$PROJECT_HOOKS"/*/*.sh; do
        if [ -f "$hook" ]; then
            hook_name=$(basename "$hook" .sh)
            hook_dir=$(basename "$(dirname "$hook")")
            target_dir="$HOOKS_DIR/$hook_dir"
            mkdir -p "$target_dir"
            ln -sf "$hook" "$target_dir/$hook_name.sh"
            echo "    - $hook_dir/$hook_name"
        fi
    done
fi

# Set up commands
if [ -d "$PROJECT_COMMANDS" ]; then
    echo "  Linking commands from $PROJECT_COMMANDS..."
    for cmd in "$PROJECT_COMMANDS"/*; do
        if [ -f "$cmd" ]; then
            cmd_name=$(basename "$cmd")
            ln -sf "$cmd" "$COMMANDS_DIR/$cmd_name"
            echo "    - $cmd_name"
        fi
    done
fi

echo -e "${GREEN}Hooks and commands installed${NC}"
echo ""

# Step 6: Validate installation
echo -e "${YELLOW}[6/6] Validating installation...${NC}"

# Check .env exists and has correct permissions
if [ -f "$ENV_FILE" ]; then
    perms=$(stat -c "%a" "$ENV_FILE" 2>/dev/null || stat -f "%A" "$ENV_FILE" 2>/dev/null)
    echo -e "${GREEN}[OK] .env file exists (permissions: $perms)${NC}"
else
    echo -e "${RED}[FAIL] .env file not found${NC}"
    exit 1
fi

# Check hooks directory
if [ -d "$HOOKS_DIR" ]; then
    hook_count=$(find "$HOOKS_DIR" -name "*.sh" | wc -l)
    echo -e "${GREEN}[OK] Hooks directory exists ($hook_count hooks installed)${NC}"
else
    echo -e "${RED}[FAIL] Hooks directory not found${NC}"
    exit 1
fi

# Check commands directory
if [ -d "$COMMANDS_DIR" ]; then
    cmd_count=$(find "$COMMANDS_DIR" -type f | wc -l)
    echo -e "${GREEN}[OK] Commands directory exists ($cmd_count commands installed)${NC}"
else
    echo -e "${RED}[FAIL] Commands directory not found${NC}"
    exit 1
fi

# Validate API keys (basic format check)
if [[ "$CLAUDE_API_KEY" == sk-ant-* ]]; then
    echo -e "${GREEN}[OK] Claude API key format valid${NC}"
else
    echo -e "${YELLOW}[WARN] Claude API key format may be invalid${NC}"
fi

echo ""
echo -e "${GREEN}============================================================================${NC}"
echo -e "${GREEN}  Installation Complete!${NC}"
echo -e "${GREEN}============================================================================${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "  1. Restart Claude Code to load the new configuration"
echo "  2. Test with: /start (if available)"
echo "  3. Check .env file: cat $ENV_FILE"
echo ""
echo -e "${BLUE}Security reminder:${NC}"
echo "  - Never commit .env to git"
echo "  - Keep your API keys secret"
echo "  - You can rotate keys anytime by editing .env"
echo ""
