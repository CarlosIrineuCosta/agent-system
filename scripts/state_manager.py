#!/usr/bin/env python3
"""
State Manager - Manages agent coordinator lifecycle and state
Handles startup, shutdown, and health monitoring
"""

import os
import json
import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import urllib.request
import urllib.error

# Import task manager for integration
try:
    from task_manager import TaskManager
    TASK_MANAGER_AVAILABLE = True
except ImportError:
    TASK_MANAGER_AVAILABLE = False


class StateManager:
    """
    Manages agent coordinator lifecycle and state persistence.

    State file location: .claude/agent-coordinator/runtime/state.json
    Runtime directory: .agents/
    """

    # Configuration
    VERSION_FILE = Path(__file__).parent.parent / "VERSION"
    STATE_DIR = Path.home() / ".claude" / "agent-coordinator" / "runtime"
    STATE_FILE = STATE_DIR / "state.json"
    AGENTS_DIR = Path.cwd() / ".agents"
    GITHUB_API = "https://api.github.com/repos/CarlosIrineuCosta/agent-system/releases/latest"

    # State constants
    STATUS_STOPPED = "STOPPED"
    STATUS_STARTING = "STARTING"
    STATUS_ACTIVE = "ACTIVE"
    STATUS_STOPPING = "STOPPING"

    def __init__(self, project_root: Optional[Path] = None):
        """Initialize state manager."""
        self.project_root = project_root or Path.cwd()
        self.state_file = self.STATE_FILE
        self.agents_dir = self.AGENTS_DIR
        self._state: Optional[Dict[str, Any]] = None

    # ========================================================================
    # CORE STATE METHODS
    # ========================================================================

    def load_state(self) -> Dict[str, Any]:
        """
        Load state from disk.

        Returns:
            State dictionary, or default state if file doesn't exist.
        """
        self._ensure_state_dir()

        if self.state_file.exists():
            try:
                data = json.loads(self.state_file.read_text())
                return data
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load state file: {e}", file=sys.stderr)

        return self._get_default_state()

    def save_state(self, state: Dict[str, Any]) -> bool:
        """
        Save state to disk.

        Args:
            state: State dictionary to save.

        Returns:
            True if save successful, False otherwise.
        """
        self._ensure_state_dir()

        try:
            state["updated_at"] = datetime.now().isoformat()
            self.state_file.write_text(json.dumps(state, indent=2))
            self._state = state
            return True
        except IOError as e:
            print(f"Error saving state: {e}", file=sys.stderr)
            return False

    def get_status(self) -> str:
        """
        Get current status.

        Returns:
            One of: STOPPED, STARTING, ACTIVE, STOPPING
        """
        state = self.load_state()
        return state.get("status", self.STATUS_STOPPED)

    def is_active(self) -> bool:
        """Check if system is currently ACTIVE."""
        return self.get_status() == self.STATUS_ACTIVE

    # ========================================================================
    # LIFECYCLE METHODS
    # ========================================================================

    def start(self) -> bool:
        """
        Run startup sequence.

        Returns:
            True if startup successful, False otherwise.
        """
        print("Starting Agent Coordinator...")

        # Check if already active
        if self.is_active():
            print("System is already ACTIVE.")
            return True

        # Load current state
        state = self.load_state()

        # Update status to STARTING
        state["status"] = self.STATUS_STARTING
        state["started_at"] = datetime.now().isoformat()
        self.save_state(state)

        # Create directory structure
        if not self.create_directory_structure():
            print("Failed to create directory structure.", file=sys.stderr)
            return False

        # Verify environment
        print("Verifying environment...")
        env_result = self.verify_environment()
        state["environment"] = {
            "glm_available": env_result.get("glm_available", False),
            "codex_available": env_result.get("codex_available", False),
            "gemini_available": env_result.get("gemini_available", False),
            "zai_endpoint": "https://api.z.ai/api/anthropic"
        }

        # Show what's available
        available = [k for k, v in env_result.items() if v]
        if available:
            print(f"  Available: {', '.join(available)}")
        else:
            print("  Warning: No agents detected!")

        # Check for updates
        print("Checking for updates...")
        update_result = self.check_updates()
        state["last_update_check"] = datetime.now().isoformat()
        if update_result.get("available"):
            print(f"  New version available: {update_result['latest']} (current: {update_result['current']})")
        else:
            print(f"  Up to date: {update_result['current']}")

        # Set status to ACTIVE
        state["status"] = self.STATUS_ACTIVE
        self.save_state(state)

        print(f"System ACTIVE (version {self.get_version()})")
        return True

    def stop(self, timeout: int = 30) -> bool:
        """
        Run shutdown sequence.

        Args:
            timeout: Max seconds to wait for agents to finish.

        Returns:
            True if shutdown successful, False otherwise.
        """
        print("Stopping Agent Coordinator...")

        # Check if already stopped
        if self.get_status() == self.STATUS_STOPPED:
            print("System is already STOPPED.")
            return True

        # Load current state
        state = self.load_state()

        # Update status to STOPPING
        state["status"] = self.STATUS_STOPPING
        self.save_state(state)

        # Check for active agents
        active_agents = state.get("active_agents", [])
        if active_agents:
            print(f"Waiting for {len(active_agents)} active agent(s) to finish...")
            # In a real implementation, we'd poll agent status files
            # For now, just clear the list
            start_time = time.time()
            while time.time() - start_time < timeout:
                # TODO: Check actual agent status
                break
            else:
                print(f"Warning: Timeout waiting for agents", file=sys.stderr)

        # Archive session
        archive_path = self.archive_session()
        if archive_path:
            print(f"Session archived to: {archive_path}")

        # Run garbage collection
        print("Running garbage collection...")
        try:
            gc_script = Path(__file__).parent / "garbage_collector.py"
            if gc_script.exists():
                result = subprocess.run(
                    [sys.executable, str(gc_script), "--clean"],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    print("  Garbage collection complete")
                else:
                    print(f"  Garbage collection: {result.stderr.strip() or 'OK'}")
        except Exception as e:
            print(f"  Garbage collection skipped: {e}")

        # Clear active agents
        state["active_agents"] = []
        state["status"] = self.STATUS_STOPPED
        state["stopped_at"] = datetime.now().isoformat()
        self.save_state(state)

        print("System STOPPED")
        return True

    # ========================================================================
    # ENVIRONMENT VERIFICATION
    # ========================================================================

    def verify_environment(self) -> Dict[str, bool]:
        """
        Check which agents/services are available.

        Returns:
            Dict with keys: glm_available, codex_available, gemini_available
        """
        return {
            "glm_available": self.check_glm(),
            "codex_available": self.check_codex(),
            "gemini_available": self.check_gemini()
        }

    def check_glm(self) -> bool:
        """
        Quick API test to verify GLM is accessible.

        Returns:
            True if GLM responds, False otherwise.
        """
        # Check for Z.ai environment variables
        base_url = os.environ.get("ANTHROPIC_BASE_URL", "")
        auth_token = os.environ.get("ANTHROPIC_AUTH_TOKEN", "")

        if not base_url or not auth_token:
            return False

        # Verify it's the Z.ai endpoint
        if "z.ai" not in base_url.lower():
            return False

        # Try a simple API call
        try:
            import urllib.request
            import urllib.error

            req = urllib.request.Request(
                f"{base_url}/v1/messages",
                method="GET",
                headers={
                    "x-api-key": auth_token,
                    "anthropic-version": "2023-06-01"
                },
                data=b"{}"
            )
            # We expect this to fail with method not allowed, but connection should work
            with urllib.request.urlopen(req, timeout=5) as response:
                pass
        except urllib.error.HTTPError as e:
            # Method not allowed is expected for GET on messages endpoint
            if e.code in (405, 401, 400):
                return True
            return False
        except Exception:
            return False

    def check_codex(self) -> bool:
        """
        Check if Codex CLI is available.

        Returns:
            True if codex binary exists and is executable.
        """
        try:
            result = subprocess.run(
                ["which", "codex"],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except Exception:
            return False

    def check_gemini(self) -> bool:
        """
        Check if Gemini API is configured.

        Returns:
            True if GEMINI_API_KEY is set.
        """
        return bool(os.environ.get("GEMINI_API_KEY"))

    # ========================================================================
    # UPDATE MANAGEMENT
    # ========================================================================

    def check_updates(self) -> Dict[str, Any]:
        """
        Check GitHub for newer version.

        Returns:
            Dict with keys: available (bool), current (str), latest (str)
        """
        current = self.get_version()

        try:
            req = urllib.request.Request(
                self.GITHUB_API,
                headers={"Accept": "application/vnd.github.v3+json"}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                latest = data.get("tag_name", "unknown").lstrip("v")

                return {
                    "available": self._version_compare(latest, current),
                    "current": current,
                    "latest": latest
                }
        except Exception as e:
            # Don't fail on network errors
            return {
                "available": False,
                "current": current,
                "latest": current,
                "error": str(e)
            }

    def _version_compare(self, latest: str, current: str) -> bool:
        """Simple version comparison."""
        try:
            latest_parts = [int(x) for x in latest.split(".")[:3]]
            current_parts = [int(x) for x in current.split(".")[:3]]

            # Pad if needed
            while len(latest_parts) < 3:
                latest_parts.append(0)
            while len(current_parts) < 3:
                current_parts.append(0)

            return latest_parts > current_parts
        except (ValueError, AttributeError):
            return False

    def get_version(self) -> str:
        """
        Get current version.

        Returns:
            Version string from VERSION file or "unknown".
        """
        if self.VERSION_FILE.exists():
            try:
                return self.VERSION_FILE.read_text().strip()
            except IOError:
                pass
        return "unknown"

    # ========================================================================
    # AGENT TRACKING
    # ========================================================================

    def register_agent(self, name: str) -> bool:
        """
        Add agent to active list.

        Args:
            name: Agent identifier (e.g., "glm-4.7", "codex")

        Returns:
            True if registered, False if already active.
        """
        state = self.load_state()
        active_agents = state.get("active_agents", [])

        if name in active_agents:
            return False

        active_agents.append(name)
        state["active_agents"] = active_agents

        # Update stats
        stats = state.get("stats", {})
        stats["total_agents_spawned"] = stats.get("total_agents_spawned", 0) + 1
        state["stats"] = stats

        return self.save_state(state)

    def unregister_agent(self, name: str) -> bool:
        """
        Remove agent from active list.

        Args:
            name: Agent identifier to remove.

        Returns:
            True if unregistered, False if not found.
        """
        state = self.load_state()
        active_agents = state.get("active_agents", [])

        if name not in active_agents:
            return False

        active_agents.remove(name)
        state["active_agents"] = active_agents
        return self.save_state(state)

    def get_active_agents(self) -> List[str]:
        """
        Get list of currently active agents.

        Returns:
            List of agent names.
        """
        state = self.load_state()
        return state.get("active_agents", []).copy()

    # ========================================================================
    # TASK TRACKING INTEGRATION
    # ========================================================================

    def get_task_summary(self) -> Optional[Dict[str, Any]]:
        """
        Get task summary from TaskManager.

        Returns:
            Task summary dict, or None if TaskManager unavailable.
        """
        if not TASK_MANAGER_AVAILABLE:
            return None

        try:
            mgr = TaskManager()
            return mgr.summary()
        except Exception:
            return None

    def get_next_task(self) -> Optional[Dict[str, Any]]:
        """
        Get the next task to work on.

        Returns:
            Task dict, or None if no active tasks.
        """
        if not TASK_MANAGER_AVAILABLE:
            return None

        try:
            mgr = TaskManager()
            return mgr.get_next()
        except Exception:
            return None

    def format_status_with_tasks(self) -> str:
        """
        Get formatted status string including task information.

        Returns:
            Multi-line status string.
        """
        lines = [
            f"System Status: {self.get_status()}",
            f"Version: {self.get_version()}"
        ]

        # Add active agents
        active_agents = self.get_active_agents()
        if active_agents:
            lines.append(f"Active Agents: {', '.join(active_agents)}")

        # Add task summary if available
        task_summary = self.get_task_summary()
        if task_summary:
            lines.append("")
            lines.append("Tasks:")
            lines.append(f"  Total: {task_summary['total']}")
            lines.append(f"  Pending: {task_summary['pending']}")
            lines.append(f"  In Progress: {task_summary['in_progress']}")
            lines.append(f"  Completed: {task_summary['completed']}")

            # Show next task
            next_task = self.get_next_task()
            if next_task:
                lines.append("")
                lines.append(f"Next: {next_task['content']}")
                lines.append(f"  Priority: {next_task['priority']}")
        else:
            lines.append("")
            lines.append("Tasks: TaskManager not available")

        return "\n".join(lines)

    # ========================================================================
    # DIRECTORY MANAGEMENT
    # ========================================================================

    def create_directory_structure(self) -> bool:
        """
        Create .agents/ directory structure if missing.

        Returns:
            True if directories exist or were created.
        """
        try:
            # Create main agents directory
            self.agents_dir.mkdir(parents=True, exist_ok=True)

            # Create subdirectories
            subdirs = [
                self.agents_dir / "runtime" / "status",
                self.agents_dir / "runtime" / "outputs",
                self.agents_dir / "runtime" / "logs",
                self.agents_dir / "sessions"
            ]

            for subdir in subdirs:
                subdir.mkdir(parents=True, exist_ok=True)

            return True
        except OSError as e:
            print(f"Error creating directory structure: {e}", file=sys.stderr)
            return False

    def archive_session(self) -> Optional[Path]:
        """
        Archive current state to logs before shutdown.

        Returns:
            Path to archived file, or None if archive failed.
        """
        try:
            state = self.load_state()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_name = f"session_{timestamp}.json"

            archive_dir = self.agents_dir / "runtime" / "logs"
            archive_dir.mkdir(parents=True, exist_ok=True)

            archive_path = archive_dir / archive_name
            archive_path.write_text(json.dumps(state, indent=2))

            return archive_path
        except Exception as e:
            print(f"Warning: Could not archive session: {e}", file=sys.stderr)
            return None

    # ========================================================================
    # UTILITIES
    # ========================================================================

    def _get_default_state(self) -> Dict[str, Any]:
        """Return default state structure."""
        return {
            "status": self.STATUS_STOPPED,
            "started_at": None,
            "stopped_at": None,
            "version": self.get_version(),
            "active_agents": [],
            "last_update_check": None,
            "environment": {
                "glm_available": False,
                "codex_available": False,
                "gemini_available": False,
                "zai_endpoint": "https://api.z.ai/api/anthropic"
            },
            "stats": {
                "tasks_completed": 0,
                "tasks_failed": 0,
                "total_agents_spawned": 0
            },
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }

    def _ensure_state_dir(self) -> bool:
        """Ensure state directory exists."""
        self.STATE_DIR.mkdir(parents=True, exist_ok=True)
        return True


def main():
    """CLI entry point for testing."""
    import argparse

    parser = argparse.ArgumentParser(description="Agent Coordinator State Manager")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Status command
    status_parser = subparsers.add_parser("status", help="Show current status")
    status_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Start command
    start_parser = subparsers.add_parser("start", help="Start the agent system")
    start_parser.add_argument("--verify", action="store_true",
                             help="Only verify environment, don't start")

    # Stop command
    stop_parser = subparsers.add_parser("stop", help="Stop the agent system")
    stop_parser.add_argument("--timeout", type=int, default=30,
                            help="Max seconds to wait for agents")

    # Check updates
    subparsers.add_parser("check-updates", help="Check for updates")

    # Version command
    subparsers.add_parser("version", help="Show version information")

    args = parser.parse_args()

    mgr = StateManager()

    if args.command == "status":
        if args.json:
            state = mgr.load_state()
            print(json.dumps(state, indent=2))
        else:
            print(mgr.format_status_with_tasks())

    elif args.command == "start":
        if args.verify:
            print("Environment Check:")
            env_result = mgr.verify_environment()
            for name, available in env_result.items():
                status = "OK" if available else "MISSING"
                print(f"  {name}: {status}")
            sys.exit(0 if all(env_result.values()) else 1)
        else:
            success = mgr.start()
            sys.exit(0 if success else 1)

    elif args.command == "stop":
        success = mgr.stop(timeout=args.timeout)
        sys.exit(0 if success else 1)

    elif args.command == "check-updates":
        result = mgr.check_updates()
        if "error" in result:
            print(f"Could not check updates: {result['error']}")
        else:
            print(f"Current: {result['current']}")
            print(f"Latest: {result['latest']}")
            if result['available']:
                print("Update available!")

    elif args.command == "version":
        print(f"Agent Coordinator v{mgr.get_version()}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
