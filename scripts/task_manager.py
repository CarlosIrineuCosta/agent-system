#!/usr/bin/env python3
"""
Task Manager - Persistent task tracking for agent system
Ensures tasks are never lost across sessions
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any


class TaskManager:
    """
    Manages persistent task storage and retrieval.

    Task file location: .claude/agent-coordinator/runtime/tasks.json
    """

    STATE_DIR = Path.home() / ".claude" / "agent-coordinator" / "runtime"
    TASKS_FILE = STATE_DIR / "tasks.json"
    BACKUP_DIR = STATE_DIR / "backups"

    # Task statuses
    STATUS_PENDING = "pending"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_COMPLETED = "completed"
    STATUS_BLOCKED = "blocked"
    STATUS_CANCELLED = "cancelled"

    # Valid priorities
    PRIORITIES = ["critical", "high", "medium", "low"]

    def __init__(self):
        """Initialize task manager and ensure directories exist."""
        self.STATE_DIR.mkdir(parents=True, exist_ok=True)
        self.BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        self._tasks: Optional[Dict[str, Any]] = None

    def _load(self) -> Dict[str, Any]:
        """Load tasks from disk."""
        if self._tasks is not None:
            return self._tasks

        if self.TASKS_FILE.exists():
            try:
                self._tasks = json.loads(self.TASKS_FILE.read_text())
            except json.JSONDecodeError:
                # Backup corrupt file and start fresh
                self._backup_corrupt_file()
                self._tasks = self._get_empty_tasks()
        else:
            self._tasks = self._get_empty_tasks()

        return self._tasks

    def _save(self, tasks: Dict[str, Any]) -> bool:
        """Save tasks to disk with backup."""
        try:
            # Create backup of current file if it exists
            if self.TASKS_FILE.exists():
                backup_name = f"tasks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                self.TASKS_FILE.rename(self.BACKUP_DIR / backup_name)

            # Write new tasks file
            self.TASKS_FILE.write_text(json.dumps(tasks, indent=2))
            self._tasks = tasks
            return True
        except Exception as e:
            print(f"Error saving tasks: {e}", file=sys.stderr)
            return False

    def _backup_corrupt_file(self):
        """Backup a corrupt tasks.json file."""
        backup_name = f"tasks_corrupt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self.TASKS_FILE.rename(self.BACKUP_DIR / backup_name)

    def _get_empty_tasks(self) -> Dict[str, Any]:
        """Return empty task structure."""
        return {
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "tasks": []
        }

    def _generate_id(self) -> str:
        """Generate unique task ID with microsecond precision."""
        # Use timestamp with microseconds to avoid collisions
        now = datetime.now()
        return f"task_{now.strftime('%Y%m%d%H%M%S')}{now.microsecond:06d}"

    # ========================================================================
    # TASK CRUD OPERATIONS
    # ========================================================================

    def add(self, content: str, priority: str = "medium",
            category: str = "general", context: Optional[str] = None) -> str:
        """
        Add a new task.

        Args:
            content: Task description (what needs to be done)
            priority: One of: critical, high, medium, low
            category: Task category (e.g., "implementation", "review", "docs")
            context: Additional context or notes

        Returns:
            Task ID of created task
        """
        if priority not in self.PRIORITIES:
            priority = "medium"

        tasks = self._load()
        task_id = self._generate_id()

        new_task = {
            "id": task_id,
            "content": content,
            "status": self.STATUS_PENDING,
            "priority": priority,
            "category": category,
            "context": context or "",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "completed_at": None,
            "blocked_by": [],
            "tags": []
        }

        tasks["tasks"].append(new_task)
        tasks["updated_at"] = datetime.now().isoformat()

        if self._save(tasks):
            return task_id
        return ""

    def update(self, task_id: str, **kwargs) -> bool:
        """
        Update an existing task.

        Args:
            task_id: ID of task to update
            **kwargs: Fields to update (content, status, priority, etc.)

        Returns:
            True if updated, False if not found
        """
        tasks = self._load()

        for task in tasks["tasks"]:
            if task["id"] == task_id:
                for key, value in kwargs.items():
                    if key in task:
                        task[key] = value
                        task["updated_at"] = datetime.now().isoformat()

                        # Auto-set completed_at when status changes to completed
                        if key == "status" and value == self.STATUS_COMPLETED:
                            task["completed_at"] = datetime.now().isoformat()

                tasks["updated_at"] = datetime.now().isoformat()
                return self._save(tasks)

        return False

    def complete(self, task_id: str) -> bool:
        """Mark a task as completed."""
        return self.update(task_id, status=self.STATUS_COMPLETED)

    def start(self, task_id: str) -> bool:
        """Mark a task as in progress."""
        return self.update(task_id, status=self.STATUS_IN_PROGRESS)

    def block(self, task_id: str, blocked_by: List[str]) -> bool:
        """Mark a task as blocked by other task IDs."""
        return self.update(task_id, status=self.STATUS_BLOCKED, blocked_by=blocked_by)

    def cancel(self, task_id: str) -> bool:
        """Cancel a task."""
        return self.update(task_id, status=self.STATUS_CANCELLED)

    def remove(self, task_id: str) -> bool:
        """
        Remove a task entirely (use with caution).

        Returns:
            True if removed, False if not found
        """
        tasks = self._load()
        original_count = len(tasks["tasks"])

        tasks["tasks"] = [t for t in tasks["tasks"] if t["id"] != task_id]

        if len(tasks["tasks"]) < original_count:
            tasks["updated_at"] = datetime.now().isoformat()
            return self._save(tasks)

        return False

    # ========================================================================
    # TASK QUERIES
    # ========================================================================

    def get(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific task by ID."""
        tasks = self._load()

        for task in tasks["tasks"]:
            if task["id"] == task_id:
                return task.copy()

        return None

    def list_all(self) -> List[Dict[str, Any]]:
        """Get all tasks."""
        return self._load()["tasks"].copy()

    def list_by_status(self, status: str) -> List[Dict[str, Any]]:
        """Get tasks filtered by status."""
        return [t for t in self._load()["tasks"] if t["status"] == status]

    def list_by_priority(self, priority: str) -> List[Dict[str, Any]]:
        """Get tasks filtered by priority."""
        return [t for t in self._load()["tasks"] if t["priority"] == priority]

    def list_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get tasks filtered by category."""
        return [t for t in self._load()["tasks"] if t["category"] == category]

    def get_active(self) -> List[Dict[str, Any]]:
        """Get pending and in_progress tasks."""
        return [
            t for t in self._load()["tasks"]
            if t["status"] in (self.STATUS_PENDING, self.STATUS_IN_PROGRESS)
        ]

    def get_next(self) -> Optional[Dict[str, Any]]:
        """
        Get the next task to work on.
        Priority order: critical > high > medium > low
        """
        active_tasks = self.get_active()
        if not active_tasks:
            return None

        # Sort by priority
        priority_order = {p: i for i, p in enumerate(self.PRIORITIES)}
        active_tasks.sort(key=lambda t: (priority_order[t["priority"]], t["created_at"]))

        return active_tasks[0]

    # ========================================================================
    # REPORTING
    # ========================================================================

    def summary(self) -> Dict[str, Any]:
        """Get task summary statistics."""
        tasks = self._load()["tasks"]

        stats = {
            "total": len(tasks),
            "pending": 0,
            "in_progress": 0,
            "completed": 0,
            "blocked": 0,
            "cancelled": 0,
            "by_priority": {p: 0 for p in self.PRIORITIES},
            "by_category": {}
        }

        for task in tasks:
            stats[task["status"]] = stats.get(task["status"], 0) + 1
            stats["by_priority"][task["priority"]] += 1

            cat = task["category"]
            stats["by_category"][cat] = stats["by_category"].get(cat, 0) + 1

        return stats

    def format_for_display(self, tasks: List[Dict[str, Any]]) -> str:
        """Format tasks for terminal display."""
        if not tasks:
            return "No tasks found."

        lines = []
        for task in tasks:
            status_symbol = {
                self.STATUS_PENDING: "[ ]",
                self.STATUS_IN_PROGRESS: "[>]",
                self.STATUS_COMPLETED: "[x]",
                self.STATUS_BLOCKED: "[!]",
                self.STATUS_CANCELLED: "[_]"
            }.get(task["status"], "[?]")

            priority_symbol = {
                "critical": "!",
                "high": "+",
                "medium": "-",
                "low": "o"
            }.get(task["priority"], "?")

            lines.append(
                f"{status_symbol} {priority_symbol} {task['id']}: {task['content']}"
            )

            if task.get("context"):
                lines.append(f"    Context: {task['context']}")

            if task.get("blocked_by"):
                lines.append(f"    Blocked by: {', '.join(task['blocked_by'])}")

        return "\n".join(lines)


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Agent Coordinator Task Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s add "Implement feature X" --priority high
  %(prog)s list --status pending
  %(prog)s start task_20231227120000
  %(prog)s complete task_20231227120000
  %(prog)s summary
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("content", help="Task description")
    add_parser.add_argument("--priority", choices=TaskManager.PRIORITIES,
                            default="medium", help="Task priority")
    add_parser.add_argument("--category", default="general",
                            help="Task category (default: general)")
    add_parser.add_argument("--context", help="Additional context")

    # List command
    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("--status", help="Filter by status")
    list_parser.add_argument("--priority", help="Filter by priority")
    list_parser.add_argument("--category", help="Filter by category")
    list_parser.add_argument("--active", action="store_true",
                             help="Show only active tasks")

    # Show command
    show_parser = subparsers.add_parser("show", help="Show task details")
    show_parser.add_argument("task_id", help="Task ID")

    # Start command
    start_parser = subparsers.add_parser("start", help="Mark task as in progress")
    start_parser.add_argument("task_id", help="Task ID")

    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Mark task as completed")
    complete_parser.add_argument("task_id", help="Task ID")

    # Block command
    block_parser = subparsers.add_parser("block", help="Mark task as blocked")
    block_parser.add_argument("task_id", help="Task ID")
    block_parser.add_argument("by", nargs="+", help="Task IDs blocking this task")

    # Cancel command
    cancel_parser = subparsers.add_parser("cancel", help="Cancel a task")
    cancel_parser.add_argument("task_id", help="Task ID")

    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Remove a task")
    remove_parser.add_argument("task_id", help="Task ID")

    # Summary command
    subparsers.add_parser("summary", help="Show task summary")

    # Next command
    subparsers.add_parser("next", help="Show next task to work on")

    args = parser.parse_args()
    mgr = TaskManager()

    if args.command == "add":
        task_id = mgr.add(args.content, args.priority, args.category, args.context)
        print(f"Created: {task_id}")

    elif args.command == "list":
        if args.active:
            tasks = mgr.get_active()
        elif args.status:
            tasks = mgr.list_by_status(args.status)
        elif args.priority:
            tasks = mgr.list_by_priority(args.priority)
        elif args.category:
            tasks = mgr.list_by_category(args.category)
        else:
            tasks = mgr.list_all()

        print(mgr.format_for_display(tasks))

    elif args.command == "show":
        task = mgr.get(args.task_id)
        if task:
            print(json.dumps(task, indent=2))
        else:
            print(f"Task not found: {args.task_id}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "start":
        if mgr.start(args.task_id):
            print(f"Started: {args.task_id}")
        else:
            print(f"Task not found: {args.task_id}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "complete":
        if mgr.complete(args.task_id):
            print(f"Completed: {args.task_id}")
        else:
            print(f"Task not found: {args.task_id}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "block":
        if mgr.block(args.task_id, args.by):
            print(f"Blocked: {args.task_id}")
        else:
            print(f"Task not found: {args.task_id}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "cancel":
        if mgr.cancel(args.task_id):
            print(f"Cancelled: {args.task_id}")
        else:
            print(f"Task not found: {args.task_id}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "remove":
        if mgr.remove(args.task_id):
            print(f"Removed: {args.task_id}")
        else:
            print(f"Task not found: {args.task_id}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "summary":
        stats = mgr.summary()
        print("Task Summary:")
        print(f"  Total: {stats['total']}")
        print(f"  Pending: {stats['pending']}")
        print(f"  In Progress: {stats['in_progress']}")
        print(f"  Completed: {stats['completed']}")
        print(f"  Blocked: {stats['blocked']}")
        print(f"\nBy Priority:")
        for p, count in stats["by_priority"].items():
            print(f"  {p}: {count}")
        if stats["by_category"]:
            print(f"\nBy Category:")
            for cat, count in stats["by_category"].items():
                print(f"  {cat}: {count}")

    elif args.command == "next":
        task = mgr.get_next()
        if task:
            print(f"Next task: {task['id']}")
            print(f"  Content: {task['content']}")
            print(f"  Priority: {task['priority']}")
            print(f"  Category: {task['category']}")
        else:
            print("No active tasks.")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
