#!/usr/bin/env python3
"""
Sandbox Manager - Safe self-development for agent-coordinator

Prevents breaking the canonical install when using agents to develop the system itself.

Usage:
    python sandbox_manager.py create     # Create sandbox from canonical
    python sandbox_manager.py sync       # Sync canonical -> sandbox (update sandbox)
    python sandbox_manager.py promote    # Promote sandbox -> canonical (after testing)
    python sandbox_manager.py status     # Show sandbox status
    python sandbox_manager.py clean      # Remove sandbox
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
from datetime import datetime


# Paths
PROJECTS_DIR = Path.home() / "Storage" / "projects"
CANONICAL = PROJECTS_DIR / "agent-coordinator"
SANDBOX = PROJECTS_DIR / "agent-coordinator-dev"
SANDBOX_MARKER = SANDBOX / ".SANDBOX"


def create_sandbox():
    """Create a sandbox copy of the canonical install."""
    if SANDBOX.exists():
        print(f"Sandbox already exists at: {SANDBOX}")
        print("Use 'python sandbox_manager.py clean' first if you want to recreate it.")
        return False

    print(f"Creating sandbox at: {SANDBOX}")
    print(f"Copying from: {CANONICAL}")

    # Copy canonical to sandbox (exclude runtime state)
    shutil.copytree(CANONICAL, SANDBOX,
                    ignore=shutil.ignore_patterns(
                        ".git", "__pycache__", "*.pyc",
                        ".agents", "*.log", "*.bak"
                    ),
                    dirs_exist_ok=True)

    # Create marker file
    SANDBOX_MARKER.write_text(f"Sandbox created: {datetime.now().isoformat()}\n")
    SANDBOX_MARKER.write_text(f"Canonical source: {CANONICAL}\n")

    print(f"\nSandbox created successfully!")
    print(f"Sandbox location: {SANDBOX}")
    print(f"\nTo use sandbox for development:")
    print(f"  1. Edit files in {SANDBOX}")
    print(f"  2. Test changes with agent tasks")
    print(f"  3. When satisfied, run 'python sandbox_manager.py promote'")
    return True


def sync_to_sandbox():
    """Sync canonical -> sandbox (update sandbox with latest from canonical)."""
    if not SANDBOX.exists():
        print(f"Sandbox does not exist. Run 'create' first.")
        return False

    print(f"Syncing canonical -> sandbox...")
    print(f"This will UPDATE the sandbox with changes from canonical.")
    print(f"Any uncommitted sandbox changes will be LOST!")

    # Simple approach: remove and recreate
    # (In production, we'd want smarter merging)
    shutil.rmtree(SANDBOX)
    return create_sandbox()


def promote_to_canonical():
    """
    Promote sandbox -> canonical (merge tested changes back).

    WARNING: This overwrites canonical files!
    """
    if not SANDBOX.exists():
        print(f"Sandbox does not exist.")
        return False

    print(f"\n⚠️  PROMOTING SANDBOX TO CANONICAL ⚠️")
    print(f"\nCanonical: {CANONICAL}")
    print(f"Sandbox:  {SANDBOX}")
    print(f"\nThis will OVERWRITE canonical files with sandbox versions.")
    print(f"\nFiles to be copied:")

    # Show what will change
    canonical_files = set(CANONICAL.rglob("*")) if CANONICAL.exists() else set()
    sandbox_files = set(SANDBOX.rglob("*"))

    # Find files in sandbox that are different/new
    changes = []
    for sb_file in sandbox_files:
        if sb_file.is_file() and ".git" not in str(sb_file):
            rel_path = sb_file.relative_to(SANDBOX)
            canonical_file = CANONICAL / rel_path
            if not canonical_file.exists() or canonical_file.read_text() != sb_file.read_text():
                changes.append(rel_path)

    if not changes:
        print("  (No changes detected - sandbox and canonical are identical)")
        return True

    for change in changes[:20]:  # Show first 20
        print(f"  - {change}")
    if len(changes) > 20:
        print(f"  ... and {len(changes) - 20} more")

    print(f"\nTotal changes: {len(changes)}")
    response = input("\nProceed with promotion? (yes/no): ")

    if response.lower() != "yes":
        print("Promotion cancelled.")
        return False

    # Copy changed files to canonical
    for rel_path in changes:
        sandbox_file = SANDBOX / rel_path
        canonical_file = CANONICAL / rel_path
        canonical_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(sandbox_file, canonical_file)

    print(f"\nPromoted {len(changes)} files to canonical.")
    print(f"Review changes with: cd {CANONICAL} && git diff")
    return True


def show_status():
    """Show sandbox status."""
    print("=" * 60)
    print("  SANDBOX STATUS")
    print("=" * 60)

    if not SANDBOX.exists():
        print("Status: No sandbox exists")
        print(f"\nTo create: python sandbox_manager.py create")
        return

    # Check marker
    if SANDBOX_MARKER.exists():
        created_at = SANDBOX_MARKER.read_text().strip()
        print(f"Status: Sandbox exists")
        print(f"Created: {created_at}")
    else:
        print("Status: Sandbox exists (no marker)")

    # Count files
    sandbox_files = list(SANDBOX.rglob("*"))
    sandbox_files = [f for f in sandbox_files if f.is_file()]
    print(f"Files: {len(sandbox_files)}")

    # Check for differences
    canonical_files = set(CANONICAL.rglob("*")) if CANONICAL.exists() else set()
    sandbox_file_set = set(SANDBOX.rglob("*"))

    new_files = []
    modified_files = []

    for sb_file in sandbox_file_set:
        if sb_file.is_file() and ".git" not in str(sb_file) and "__pycache__" not in str(sb_file):
            rel_path = sb_file.relative_to(SANDBOX)
            canonical_file = CANONICAL / rel_path

            if not canonical_file.exists():
                new_files.append(rel_path)
            elif canonical_file.is_file() and canonical_file.read_text() != sb_file.read_text():
                modified_files.append(rel_path)

    print(f"\nChanges in sandbox:")
    print(f"  New files: {len(new_files)}")
    print(f"  Modified: {len(modified_files)}")

    if modified_files:
        print(f"\nModified files (first 10):")
        for f in modified_files[:10]:
            print(f"  - {f}")

    print(f"\nPaths:")
    print(f"  Canonical: {CANONICAL}")
    print(f"  Sandbox:  {SANDBOX}")


def clean_sandbox():
    """Remove the sandbox."""
    if not SANDBOX.exists():
        print("No sandbox exists.")
        return True

    print(f"Removing sandbox at: {SANDBOX}")
    response = input("Confirm removal? (yes/no): ")

    if response.lower() != "yes":
        print("Cancelled.")
        return False

    shutil.rmtree(SANDBOX)
    print("Sandbox removed.")
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python sandbox_manager.py [create|sync|promote|status|clean]")
        print("\nCommands:")
        print("  create   - Create sandbox from canonical")
        print("  sync     - Sync canonical -> sandbox (update sandbox)")
        print("  promote  - Promote sandbox -> canonical (merge tested changes)")
        print("  status   - Show sandbox status")
        print("  clean    - Remove sandbox")
        sys.exit(1)

    command = sys.argv[1]

    if command == "create":
        create_sandbox()
    elif command == "sync":
        sync_to_sandbox()
    elif command == "promote":
        promote_to_canonical()
    elif command == "status":
        show_status()
    elif command == "clean":
        clean_sandbox()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
