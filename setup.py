"""
Agent-Coordinator Setup Script

This is a standalone setup.py that works with a GitHub clone.
No symlinks required - everything is copied to the right places.

Usage:
    pip install -e .

Or for development:
    python setup.py develop
"""

import os
import shutil
import sys
from pathlib import Path
from setuptools import setup, find_packages

# ANSI colors for terminal output
class Colors:
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    NC = '\033[0m'  # No Color

def print_header(msg):
    print(f"{Colors.BLUE}{'='*70}{Colors.NC}")
    print(f"{Colors.BLUE}  {msg}{Colors.NC}")
    print(f"{Colors.BLUE}{'='*70}{Colors.NC}")
    print()

def print_step(num, total, msg):
    print(f"{Colors.YELLOW}[{num}/{total}] {msg}{Colors.NC}")

def print_success(msg):
    print(f"{Colors.GREEN}[OK] {msg}{Colors.NC}")

def print_error(msg):
    print(f"{Colors.RED}[ERROR] {msg}{Colors.NC}")

def get_project_root():
    """Get the project root directory."""
    return Path(__file__).parent.absolute()

def install_hooks(project_root, claude_dir):
    """Install hooks to Claude directory."""
    hooks_src = project_root / "hooks"
    hooks_dst = claude_dir / "hooks"

    if not hooks_src.exists():
        print_error(f"Hooks source directory not found: {hooks_src}")
        return False

    hooks_dst.mkdir(parents=True, exist_ok=True)

    # Copy all hook files
    for hook_file in hooks_src.rglob("*.sh"):
        rel_path = hook_file.relative_to(hooks_src)
        dst_file = hooks_dst / rel_path
        dst_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(hook_file, dst_file)

    hook_count = len(list(hooks_dst.rglob("*.sh")))
    print_success(f"Installed {hook_count} hooks to {hooks_dst}")
    return True

def install_commands(project_root, claude_dir):
    """Install commands to Claude directory."""
    cmds_src = project_root / "commands"
    cmds_dst = claude_dir / "commands"

    if not cmds_src.exists():
        print_error(f"Commands source directory not found: {cmds_src}")
        return False

    cmds_dst.mkdir(parents=True, exist_ok=True)

    # Copy all command files
    for cmd_file in cmds_src.rglob("*"):
        if cmd_file.is_file():
            rel_path = cmd_file.relative_to(cmds_src)
            dst_file = cmds_dst / rel_path
            dst_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(cmd_file, dst_file)

    cmd_count = len([f for f in cmds_dst.rglob("*") if f.is_file()])
    print_success(f"Installed {cmd_count} commands to {cmds_dst}")
    return True

def install_configs(project_root, claude_dir):
    """Install configuration files to Claude directory."""
    config_src = project_root / "config"

    if not config_src.exists():
        print_error(f"Config source directory not found: {config_src}")
        return False

    # Copy agent_routing.json if it exists
    agent_routing = config_src / "agent_routing.json"
    if agent_routing.exists():
        shutil.copy2(agent_routing, claude_dir / "agent_routing.json")
        print_success(f"Installed agent_routing.json to {claude_dir}")

    # Copy hooks_settings.json if it exists
    hooks_settings = config_src / "hooks_settings.json"
    if hooks_settings.exists():
        dst = claude_dir / "settings.json"
        shutil.copy2(hooks_settings, dst)
        print_success(f"Installed hooks_settings.json to {dst}")

    return True

def create_env_template(project_root):
    """Create .env template if it doesn't exist."""
    env_example = project_root / ".env.example"
    env_file = project_root / ".env"

    if env_example.exists() and not env_file.exists():
        shutil.copy2(env_example, env_file)
        print_success(f"Created .env template (add your API keys)")
    elif env_file.exists():
        print_success(f".env file already exists")
    else:
        print_success(f"No .env template found (optional)")

def validate_installation(claude_dir):
    """Validate that installation was successful."""
    hooks_dir = claude_dir / "hooks"
    commands_dir = claude_dir / "commands"

    issues = []

    if not hooks_dir.exists():
        issues.append("Hooks directory not found")
    else:
        hook_count = len(list(hooks_dir.rglob("*.sh")))
        if hook_count == 0:
            issues.append("No hooks installed")

    if not commands_dir.exists():
        issues.append("Commands directory not found")
    else:
        cmd_count = len([f for f in commands_dir.rglob("*") if f.is_file()])
        if cmd_count == 0:
            issues.append("No commands installed")

    return issues

def run_post_install():
    """Run post-installation setup."""
    print_header("Agent-Coordinator Installation")

    project_root = get_project_root()
    claude_dir = Path.home() / ".claude"

    print_step(1, 5, f"Installing from: {project_root}")
    print_step(2, 5, f"Target directory: {claude_dir}")
    print()

    # Step 3: Install hooks
    print_step(3, 5, "Installing hooks...")
    if not install_hooks(project_root, claude_dir):
        sys.exit(1)
    print()

    # Step 4: Install commands
    print_step(4, 5, "Installing commands...")
    if not install_commands(project_root, claude_dir):
        sys.exit(1)
    print()

    # Step 5: Install configs
    print_step(5, 5, "Installing configuration files...")
    if not install_configs(project_root, claude_dir):
        sys.exit(1)
    print()

    # Create .env template
    create_env_template(project_root)
    print()

    # Validate
    issues = validate_installation(claude_dir)
    if issues:
        print_error("Installation validation failed:")
        for issue in issues:
            print(f"  - {issue}")
        sys.exit(1)

    print_header("Installation Complete!")
    print(f"{Colors.GREEN}All hooks, commands, and configs installed.{Colors.NC}")
    print()
    print(f"{Colors.BLUE}Next steps:{Colors.NC}")
    print(f"  1. Add your API keys to: {project_root / '.env'}")
    print(f"  2. Run: ./scripts/install.sh  (for interactive API key setup)")
    print(f"  3. Restart Claude Code to load changes")
    print()

# Get project root and read version
project_root = get_project_root()
try:
    with open(project_root / "VERSION") as f:
        version = f.read().strip()
except:
    version = "1.0.0"

# Standard setuptools setup
setup(
    name="agent-coordinator",
    version=version,
    description="Multi-agent AI workflow coordination system",
    long_description=open("README.md").read() if (Path(__file__).parent / "README.md").exists() else "",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "agent-coordinator=agent_coordinator.cli:main",
        ],
    },
)

# Run post-installation setup
if __name__ == "__main__":
    # Only run post-install if we're actually installing (not just gathering info)
    if len(sys.argv) > 1 and sys.argv[1] in ("install", "develop"):
        run_post_install()
