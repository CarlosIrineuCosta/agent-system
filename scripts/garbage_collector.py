#!/usr/bin/env python3
"""
Garbage Collector - Cleans up old agent outputs and logs

Usage:
    python garbage_collector.py --dry-run    # Preview what would be deleted
    python garbage_collector.py --clean      # Actually clean up
    python garbage_collector.py --stats      # Show disk usage
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import argparse


class GarbageCollector:
    """Cleans up old agent outputs and logs"""

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path.cwd()
        self.agents_dir = self.project_root / ".agents"
        self.runtime_dir = Path.home() / ".claude" / "agent-coordinator" / "runtime"

        # Default retention periods
        self.output_retention_days = 7
        self.log_retention_days = 30

    def get_disk_usage(self) -> Dict[str, int]:
        """
        Get disk usage for agent directories.

        Returns:
            Dict with keys: total_bytes, total_mb, breakdown (dict)
        """
        usage = {}
        total = 0

        for dir_name in ["queue", "output", "coordinated", "logs"]:
            dir_path = self.agents_dir / dir_name
            if dir_path.exists():
                dir_size = sum(f.stat().st_size for f in dir_path.rglob('*') if f.is_file())
                usage[dir_name] = dir_size
                total += dir_size
            else:
                usage[dir_name] = 0

        usage["total_bytes"] = total
        usage["total_mb"] = total / (1024 * 1024)

        return usage

    def print_usage_stats(self):
        """Print disk usage statistics."""
        usage = self.get_disk_usage()

        print("=== Agent System Disk Usage ===")
        print(f"Total: {usage['total_mb']:.2f} MB")
        print()
        print("Breakdown:")
        for dir_name, size in usage.items():
            if dir_name not in ["total_bytes", "total_mb"]:
                mb = size / (1024 * 1024)
                print(f"  .agents/{dir_name}/: {mb:.2f} MB")

    def clean_old_outputs(self, days: int = 7, dry_run: bool = True) -> List[Path]:
        """
        Remove old agent outputs.

        Args:
            days: Retention period in days
            dry_run: If True, don't actually delete

        Returns:
            List of paths that would be/were deleted
        """
        cutoff = datetime.now() - timedelta(days=days)
        deleted = []

        for subdir in ["output", "coordinated"]:
            dir_path = self.agents_dir / subdir
            if not dir_path.exists():
                continue

            for item in dir_path.iterdir():
                if item.is_dir():
                    # Check directory modification time
                    mtime = datetime.fromtimestamp(item.stat().st_mtime)
                    if mtime < cutoff:
                        if dry_run:
                            print(f"Would delete: {item}")
                        else:
                            shutil.rmtree(item)
                            print(f"Deleted: {item}")
                        deleted.append(item)

        return deleted

    def clean_old_logs(self, days: int = 30, dry_run: bool = True) -> List[Path]:
        """
        Remove or archive old logs.

        Args:
            days: Retention period in days
            dry_run: If True, don't actually delete

        Returns:
            List of paths that would be/were deleted
        """
        cutoff = datetime.now() - timedelta(days=days)
        deleted = []

        # Clean .agents/logs/
        logs_dir = self.agents_dir / "logs"
        if logs_dir.exists():
            for log_file in logs_dir.glob("*.log"):
                mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
                if mtime < cutoff:
                    if dry_run:
                        print(f"Would delete: {log_file}")
                    else:
                        log_file.unlink()
                        print(f"Deleted: {log_file}")
                    deleted.append(log_file)

        # Clean runtime/logs/
        runtime_logs = self.runtime_dir / "logs"
        if runtime_logs.exists():
            for log_file in runtime_logs.glob("*.json"):
                mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
                if mtime < cutoff:
                    if dry_run:
                        print(f"Would delete: {log_file}")
                    else:
                        log_file.unlink()
                        print(f"Deleted: {log_file}")
                    deleted.append(log_file)

        return deleted

    def clean_empty_dirs(self, dry_run: bool = True) -> List[Path]:
        """
        Remove empty directories.

        Args:
            dry_run: If True, don't actually delete

        Returns:
            List of paths that would be/were deleted
        """
        deleted = []

        for subdir in ["output", "coordinated", "queue", "logs"]:
            dir_path = self.agents_dir / subdir
            if not dir_path.exists():
                continue

            for item in dir_path.rglob('*'):
                if item.is_dir() and not any(item.iterdir()):
                    if dry_run:
                        print(f"Would remove empty dir: {item}")
                    else:
                        item.rmdir()
                        print(f"Removed empty dir: {item}")
                    deleted.append(item)

        return deleted

    def clean_all(self, dry_run: bool = True) -> Dict[str, List[Path]]:
        """
        Run all cleanup operations.

        Args:
            dry_run: If True, don't actually delete

        Returns:
            Dict with lists of deleted paths by category
        """
        results = {
            "old_outputs": self.clean_old_outputs(self.output_retention_days, dry_run),
            "old_logs": self.clean_old_logs(self.log_retention_days, dry_run),
            "empty_dirs": self.clean_empty_dirs(dry_run)
        }

        total = sum(len(v) for v in results.values())
        print()
        print(f"{'Would delete' if dry_run else 'Deleted'} {total} items")

        return results


def main():
    parser = argparse.ArgumentParser(
        description="Garbage collector for agent-coordinator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python garbage_collector.py --stats          Show disk usage
  python garbage_collector.py --dry-run        Preview cleanup
  python garbage_collector.py --clean          Actually clean up
  python garbage_collector.py --clean --output-days 3
        """
    )

    parser.add_argument("--stats", action="store_true",
                       help="Show disk usage statistics")
    parser.add_argument("--clean", action="store_true",
                       help="Run cleanup (not dry-run)")
    parser.add_argument("--dry-run", action="store_true",
                       help="Preview what would be deleted")
    parser.add_argument("--output-days", type=int, default=7,
                       help="Output retention period (default: 7)")
    parser.add_argument("--log-days", type=int, default=30,
                       help="Log retention period (default: 30)")

    args = parser.parse_args()

    gc = GarbageCollector()

    if args.stats:
        gc.print_usage_stats()
        return 0

    if args.clean or args.dry_run:
        gc.output_retention_days = args.output_days
        gc.log_retention_days = args.log_days

        print("=== Garbage Collection ===")
        print(f"Output retention: {args.output_days} days")
        print(f"Log retention: {args.log_days} days")
        print(f"Mode: {'DRY RUN (no changes)' if args.dry_run else 'LIVE (will delete)'}")
        print()

        gc.clean_all(dry_run=args.dry_run)
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
