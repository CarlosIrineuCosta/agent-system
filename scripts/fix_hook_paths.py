#!/usr/bin/env python3
"""
Fix hook paths in all Claude configuration files

This script updates all Claude configuration files to use absolute paths
for hooks, preventing issues when working in subdirectories.
"""

import os
import json
import glob
from pathlib import Path

def fix_hook_paths(project_root=None):
    """Fix hooks in all Claude configuration files"""

    if project_root is None:
        project_root = os.getcwd()

    hooks_path = os.path.join(project_root, ".claude", "hooks")

    def fix_file(filepath):
        """Fix hooks in a single configuration file"""
        try:
            with open(filepath, 'r') as f:
                content = f.read()

            # Replace various hook path patterns with absolute paths
            content = content.replace(
                '"command": "python agent-system/hooks/',
                f'"command": "python {hooks_path}/'
            )
            content = content.replace(
                '"command": "python ./.claude/hooks/',
                f'"command": "python {hooks_path}/'
            )

            # Handle relative paths with ./
            if not content.startswith('/'):
                content = content.replace(
                    '"command": "python ./',
                    f'"command": "python {os.path.join(project_root, "")}/'
                )

            with open(filepath, 'w') as f:
                f.write(content)

            print(f"✓ Fixed: {filepath}")
        except Exception as e:
            print(f"✗ Error fixing {filepath}: {e}")

    # Find all configuration files
    config_patterns = [
        os.path.join(project_root, ".claude", "*.json"),
        os.path.join(project_root, "**", ".claude", "*.json")
    ]

    print(f"Fixing hook paths in: {project_root}")
    print(f"Target hooks path: {hooks_path}")
    print("-" * 50)

    for pattern in config_patterns:
        for filepath in glob.glob(pattern, recursive=True):
            if os.path.isfile(filepath) and filepath.endswith('.json'):
                fix_file(filepath)

    print("\n✅ All hook paths fixed!")
    print("\nTo verify the fix:")
    print(f"grep -n '{hooks_path}' {project_root}/.claude/settings.json")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Fix Claude hook paths")
    parser.add_argument("--project-root", help="Project root directory", default=None)
    args = parser.parse_args()

    fix_hook_paths(args.project_root)