#!/usr/bin/env python3
"""
File Write Validator Hook
Enforces file writing rules defined in config/agent_rules.json
Prevents agents from modifying protected files and directories
"""

import json
import sys
import os
from pathlib import Path

# Handle __file__ potentially being undefined when run as a hook command
if '__file__' in globals():
    HOOKS_DIR = Path(__file__).parent
    PROJECT_ROOT = HOOKS_DIR.parent.parent
else:
    PROJECT_ROOT = Path.cwd()
    if (PROJECT_ROOT / "hooks" / "core").exists():
        HOOKS_DIR = PROJECT_ROOT / "hooks" / "core"
    else:
        # Try to find project root
        current = PROJECT_ROOT
        while current != current.parent:
            if (current / "config" / "agent_rules.json").exists():
                PROJECT_ROOT = current
                HOOKS_DIR = current / "hooks" / "core"
                break
            current = current.parent

CONFIG_FILE = PROJECT_ROOT / "config" / "agent_rules.json"


def load_agent_rules():
    """Load agent writing rules from config file."""
    if not CONFIG_FILE.exists():
        # Return default restrictive rules if config missing
        return {
            "forbidden_paths": {
                "root_markdown": ["README.md", "*.md"],
                "config": ["config/*"],
                "hooks": ["hooks/*"]
            },
            "protected_paths": {
                "require_approval": ["docs/", ".env", ".gitignore"]
            },
            "allowed_paths": {
                "write_freely": [".agents/", "docs/coordination/", "docs/analysis/"]
            },
            "enforcement": {
                "block_root_md_writes": True,
                "require_approval_for_protected": True
            },
            "block_message": "BLOCKED: Cannot modify protected file: {file_path}\n\nReason: {reason}"
        }

    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Warning: Could not load agent rules: {e}", file=sys.stderr)
        return None


def parse_tool_input():
    """Parse tool input from stdin."""
    import select
    if select.select([sys.stdin], [], [], 0.0)[0]:
        try:
            tool_data = json.load(sys.stdin)
            return tool_data
        except json.JSONDecodeError:
            return None
    else:
        return None


def get_file_paths_from_tool(tool_input):
    """Extract file paths from tool input."""
    file_paths = []

    if not tool_input:
        return file_paths

    # Handle different tool formats
    tool_name = tool_input.get('tool_name', '')

    if tool_name == 'Write':
        # Write tool has 'file_path'
        if 'file_path' in tool_input.get('tool_input', {}):
            file_paths.append(tool_input['tool_input']['file_path'])

    elif tool_name == 'Edit':
        # Edit tool has 'file_path'
        if 'file_path' in tool_input.get('tool_input', {}):
            file_paths.append(tool_input['tool_input']['file_path'])

    elif tool_name == 'Glob':
        # Glob tool - we only care about write operations
        pass

    # Also check for direct 'file_path' or 'files' keys
    if 'file_path' in tool_input:
        file_paths.append(tool_input['file_path'])
    if 'files' in tool_input:
        file_paths.extend(tool_input['files'])

    return file_paths


def matches_pattern(path_str, pattern):
    """Check if a path matches a pattern (supports wildcards)."""
    path = Path(path_str).resolve()
    pattern_path = Path(pattern).resolve()

    # Simple wildcard matching
    if '*' in pattern:
        # Convert glob pattern to regex
        import re
        regex = re.escape(pattern)
        regex = regex.replace(r'\*', '.*')
        regex = regex.replace(r'\?', '.')
        regex = f'^{regex}$'
        return re.match(regex, str(path)) is not None

    # Exact match or prefix match for directories
    if pattern.endswith('/'):
        return str(path).startswith(str(pattern_path))
    else:
        return path == pattern_path or path.is_relative_to(pattern_path)


def is_forbidden(file_path, rules):
    """Check if a file path is forbidden."""
    if not rules or 'forbidden_paths' not in rules:
        return False, None

    path = Path(file_path).resolve()
    relative_path = path.relative_to(PROJECT_ROOT) if path.is_relative_to(PROJECT_ROOT) else path

    # Check each forbidden category
    for category, patterns in rules.get('forbidden_paths', {}).items():
        for pattern in patterns:
            if matches_pattern(str(relative_path), pattern):
                return True, f"Category: {category}, Pattern: {pattern}"

    return False, None


def is_protected(file_path, rules):
    """Check if a file path is protected (requires approval)."""
    if not rules or 'protected_paths' not in rules:
        return False, None

    path = Path(file_path).resolve()
    relative_path = path.relative_to(PROJECT_ROOT) if path.is_relative_to(PROJECT_ROOT) else path

    for category, patterns in rules.get('protected_paths', {}).items():
        for pattern in patterns:
            if matches_pattern(str(relative_path), pattern):
                return True, f"Category: {category}"

    return False, None


def is_allowed(file_path, rules):
    """Check if a file path is explicitly allowed for writing."""
    if not rules or 'allowed_paths' not in rules:
        return False

    path = Path(file_path).resolve()
    relative_path = path.relative_to(PROJECT_ROOT) if path.is_relative_to(PROJECT_ROOT) else path

    # Only check write_freely patterns, not read_only
    write_patterns = rules.get('allowed_paths', {}).get('write_freely', [])
    for pattern in write_patterns:
        if matches_pattern(str(relative_path), pattern):
            return True

    return False


def check_root_markdown_violation(file_path, rules):
    """Check if this is a root markdown file violation."""
    enforcement = rules.get('enforcement', {})

    if not enforcement.get('block_root_md_writes', True):
        return False

    path = Path(file_path).resolve()
    relative_path = path.relative_to(PROJECT_ROOT) if path.is_relative_to(PROJECT_ROOT) else path

    # Check if it's a markdown file in root
    if path.suffix.lower() == '.md':
        # Check if parent is project root
        try:
            if path.parent == PROJECT_ROOT:
                return True, "Markdown files cannot be created in project root"
        except:
            # If we can't resolve relative to project root, check path depth
            parts = relative_path.parts
            if len(parts) == 1 and path.suffix.lower() == '.md':
                return True, "Markdown files cannot be created in project root"

    return False, None


def validate_file_writes(file_paths, rules):
    """Validate a list of file paths against the rules."""
    if not rules:
        return [], [], []  # No rules to enforce

    blocked = []
    warnings = []
    allowed = []

    for file_path in file_paths:
        # Check if explicitly allowed first
        if is_allowed(file_path, rules):
            allowed.append(file_path)
            continue

        # Check for root markdown violations
        is_root_md, reason = check_root_markdown_violation(file_path, rules)
        if is_root_md:
            blocked.append((file_path, reason))
            continue

        # Check forbidden paths
        is_bad, reason = is_forbidden(file_path, rules)
        if is_bad:
            blocked.append((file_path, f"Protected path: {reason}"))
            continue

        # Check protected paths
        is_prot, reason = is_protected(file_path, rules)
        if is_prot:
            warnings.append((file_path, f"Protected path: {reason}"))
            continue

        # Default to allowed if no rules matched
        allowed.append(file_path)

    return blocked, warnings, allowed


def format_block_message(rules, blocked_items):
    """Format the block message with details."""
    if not blocked_items:
        return ""

    template = rules.get('block_message',
        "BLOCKED: Cannot modify protected file: {file_path}\n\nReason: {reason}")

    lines = ["=" * 60]
    lines.append("FILE WRITE VALIDATION FAILED")
    lines.append("=" * 60)
    lines.append("")

    for file_path, reason in blocked_items:
        lines.append(template.format(file_path=file_path, reason=reason))
        lines.append("")

    lines.append("Allowed write locations:")
    for pattern in rules.get('allowed_paths', {}).get('write_freely', []):
        lines.append(f"  - {pattern}")
    lines.append("")

    lines.append("If you need to modify this file, ask the user to do it manually.")
    lines.append("=" * 60)

    return "\n".join(lines)


def main():
    """Main hook execution."""
    tool_input = parse_tool_input()

    if not tool_input:
        sys.exit(0)

    # Only validate write operations
    tool_name = tool_input.get('tool_name', '')
    if tool_name not in ['Write', 'Edit']:
        sys.exit(0)

    # Load rules
    rules = load_agent_rules()
    if not rules:
        sys.exit(0)  # Allow if no rules

    # Get file paths
    file_paths = get_file_paths_from_tool(tool_input)

    if not file_paths:
        sys.exit(0)

    # Validate
    blocked, warnings, allowed = validate_file_writes(file_paths, rules)

    # Print warnings for protected files
    for file_path, reason in warnings:
        print(f"Warning: Writing to protected file: {file_path} ({reason})", file=sys.stderr)

    # Block forbidden files
    if blocked:
        print(format_block_message(rules, blocked), file=sys.stderr)
        sys.exit(1)  # Exit with error to block the operation

    # Allow the operation
    sys.exit(0)


if __name__ == '__main__':
    main()
