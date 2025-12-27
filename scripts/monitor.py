#!/usr/bin/env python3
"""
Real-time monitoring of agent coordinator activity
Usage: python scripts/monitor.py
"""

import json
import sys
import time
from pathlib import Path
from datetime import datetime


class AgentMonitor:
    def __init__(self):
        self.status_dir = Path.cwd() / ".agents" / "runtime" / "status"
        self.state_file = Path.home() / ".claude" / "agent-coordinator" / "runtime" / "state.json"
        self.queue_dir = Path.cwd() / ".agents" / "queue"

    def read_agent_statuses(self):
        """Read all .status files"""
        statuses = {}
        if self.status_dir.exists():
            for status_file in self.status_dir.glob("*.status"):
                agent_name = status_file.stem
                try:
                    with open(status_file) as f:
                        statuses[agent_name] = json.load(f)
                except:
                    pass
        return statuses

    def read_system_state(self):
        """Read state.json"""
        if self.state_file.exists():
            try:
                with open(self.state_file) as f:
                    return json.load(f)
            except:
                pass
        return None

    def get_status_icon(self, status):
        """Get icon for status"""
        icons = {
            'active': '[GREEN]',
            'idle': '[WHITE]',
            'error': '[RED]'
        }
        return icons.get(status, '[GRAY]')

    def format_time_ago(self, iso_timestamp):
        """Format timestamp as time ago"""
        if not iso_timestamp:
            return "-"

        try:
            dt = datetime.fromisoformat(iso_timestamp)
            delta = datetime.now() - dt
            minutes = int(delta.total_seconds() / 60)

            if minutes < 1:
                return "just now"
            elif minutes < 60:
                return f"{minutes}m ago"
            else:
                hours = minutes // 60
                return f"{hours}h ago"
        except:
            return "-"

    def display(self):
        """Render current status to terminal"""
        # Clear screen
        print("\033[2J\033[H", end="")

        # Header
        print("=" * 60)
        print("  AGENT COORDINATOR - LIVE STATUS")
        print("=" * 60)

        # System state
        state = self.read_system_state()
        if state:
            status = state.get('status', 'UNKNOWN')
            version = state.get('version', 'unknown')
            started = state.get('started_at', '')
            uptime = ""
            if started:
                uptime = self.format_time_ago(started)
            print(f"  System: {status} | Version: {version} | Uptime: {uptime}")
        else:
            print("  System: UNKNOWN (state.json not found)")

        print("-" * 60)

        # Active agents
        print("  ACTIVE AGENTS")
        statuses = self.read_agent_statuses()

        if not statuses:
            print("  No agent status files found")
        else:
            for agent_name, status_data in statuses.items():
                status = status_data.get('status', 'unknown')
                task = status_data.get('task', '')[:30]
                progress = status_data.get('progress')
                started = status_data.get('started_at', '')

                icon = self.get_status_icon(status)
                time_ago = self.format_time_ago(started)

                progress_str = ""
                if progress is not None:
                    progress_str = f" | {int(progress * 100)}%"

                print(f"  {icon} {agent_name.upper():12} | {task:30} | {time_ago:>8}{progress_str}")

        print("-" * 60)

        # Queue
        print("  QUEUE")
        queue_files = []
        if self.queue_dir.exists():
            queue_files = list(self.queue_dir.glob("*"))
            queue_files = [f for f in queue_files if f.is_file()]

        if not queue_files:
            print("  No pending tasks")
        else:
            for i, qf in enumerate(queue_files[:5], 1):
                print(f"  {i}. {qf.name}")
            if len(queue_files) > 5:
                print(f"  ... and {len(queue_files) - 5} more")

        print("-" * 60)

        # Footer
        print(f"  Last update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Press Ctrl+C to exit")
        print("=" * 60)

    def run(self):
        """Main loop - update every 2 seconds"""
        try:
            while True:
                self.display()
                time.sleep(2)
        except KeyboardInterrupt:
            print("\n\nMonitor stopped.")
            sys.exit(0)


def main():
    monitor = AgentMonitor()

    if len(sys.argv) > 1 and sys.argv[1] == '--once':
        monitor.display()
    else:
        monitor.run()


if __name__ == "__main__":
    main()
