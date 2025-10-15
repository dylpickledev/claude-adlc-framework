#!/usr/bin/env python3
"""
Budget Monitor - Real-time memory budget tracking

Monitors agent memory budget usage during task execution with real-time
alerts when thresholds are exceeded.

Alert Thresholds:
- INFO (75%): Normal usage, not concerning
- WARNING (90%): Consider bumping complexity tier
- CRITICAL (100%): Budget exceeded, automatic tier bump

Usage:
    from budget_monitor import BudgetMonitor

    # Initialize monitor
    monitor = BudgetMonitor(
        agent_name="specialists/dbt-expert",
        budget=20000,
        task_description="Analyze model performance"
    )

    # Track memory loading
    monitor.track_load("global", 4000)
    monitor.track_load("agent_patterns", 10000)

    # Get status
    status = monitor.get_status()

    # Log usage
    monitor.log_usage()
"""

import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import sys


class BudgetMonitor:
    """Monitor agent memory budget usage in real-time"""

    def __init__(
        self,
        agent_name: str,
        budget: int,
        task_description: str = "",
        complexity: str = "medium",
        log_file: Optional[Path] = None
    ):
        """Initialize budget monitor

        Args:
            agent_name: Agent identifier (e.g., "specialists/dbt-expert")
            budget: Allocated token budget
            task_description: Optional task description
            complexity: Task complexity tier
            log_file: Optional custom log file path
        """
        self.agent_name = agent_name
        self.budget = budget
        self.task_description = task_description
        self.complexity = complexity
        self.loaded_tokens = 0
        self.scope_loads = {}  # Track tokens by scope
        self.warnings = []
        self.start_time = time.time()

        # Load alert thresholds from config
        profiles_path = Path(".claude/memory/budget-profiles.json")
        if profiles_path.exists():
            config = json.loads(profiles_path.read_text())
            self.thresholds = config.get("alert_thresholds", {
                "info": 0.75,
                "warning": 0.90,
                "critical": 1.0
            })
        else:
            self.thresholds = {
                "info": 0.75,
                "warning": 0.90,
                "critical": 1.0
            }

        # Log file
        if log_file is None:
            log_dir = Path(".claude/cache")
            log_dir.mkdir(parents=True, exist_ok=True)
            log_file = log_dir / "budget-usage.jsonl"

        self.log_file = log_file

        # Tracking state
        self.info_threshold_triggered = False
        self.warning_threshold_triggered = False
        self.critical_threshold_triggered = False

    def track_load(self, scope: str, tokens: int):
        """Track tokens loaded from a scope

        Args:
            scope: Scope name (global, agent_recent, agent_patterns, etc.)
            tokens: Number of tokens loaded from this scope
        """
        self.loaded_tokens += tokens

        # Track by scope
        if scope not in self.scope_loads:
            self.scope_loads[scope] = 0
        self.scope_loads[scope] += tokens

        # Check thresholds
        usage_pct = self.loaded_tokens / self.budget

        # INFO threshold (75%)
        if usage_pct >= self.thresholds["info"] and not self.info_threshold_triggered:
            self.info_threshold_triggered = True
            self.warnings.append({
                "timestamp": datetime.now().isoformat(),
                "threshold": "info",
                "usage_pct": usage_pct,
                "message": f"ℹ️  Budget 75% consumed ({self.loaded_tokens:,}/{self.budget:,} tokens)"
            })
            print(f"ℹ️  Budget 75% consumed ({self.loaded_tokens:,}/{self.budget:,} tokens)")

        # WARNING threshold (90%)
        if usage_pct >= self.thresholds["warning"] and not self.warning_threshold_triggered:
            self.warning_threshold_triggered = True
            self.warnings.append({
                "timestamp": datetime.now().isoformat(),
                "threshold": "warning",
                "usage_pct": usage_pct,
                "message": f"⚠️  Budget 90% consumed ({self.loaded_tokens:,}/{self.budget:,} tokens)"
            })
            print(f"⚠️  Budget 90% consumed ({self.loaded_tokens:,}/{self.budget:,} tokens)")

        # CRITICAL threshold (100%)
        if usage_pct >= self.thresholds["critical"] and not self.critical_threshold_triggered:
            self.critical_threshold_triggered = True
            self.warnings.append({
                "timestamp": datetime.now().isoformat(),
                "threshold": "critical",
                "usage_pct": usage_pct,
                "message": f"❌ Budget EXCEEDED ({self.loaded_tokens:,}/{self.budget:,} tokens)"
            })
            print(f"❌ Budget EXCEEDED ({self.loaded_tokens:,}/{self.budget:,} tokens)")

    def get_status(self) -> Dict:
        """Get current budget status

        Returns:
            {
                "agent": str,
                "budget": int,
                "loaded": int,
                "usage_pct": float,
                "remaining": int,
                "warnings": list,
                "scope_breakdown": dict,
                "exceeded": bool
            }
        """
        usage_pct = (self.loaded_tokens / self.budget) * 100 if self.budget > 0 else 0

        return {
            "agent": self.agent_name,
            "task": self.task_description,
            "complexity": self.complexity,
            "budget": self.budget,
            "loaded": self.loaded_tokens,
            "usage_pct": usage_pct,
            "remaining": max(0, self.budget - self.loaded_tokens),
            "warnings": self.warnings,
            "scope_breakdown": self.scope_loads,
            "exceeded": self.loaded_tokens > self.budget,
            "duration_seconds": time.time() - self.start_time
        }

    def log_usage(self, success: bool = True, error_message: str = ""):
        """Log budget usage to JSONL file

        Args:
            success: Whether task completed successfully
            error_message: Optional error message if task failed
        """
        status = self.get_status()

        # Add completion metadata
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent": self.agent_name,
            "task": self.task_description,
            "complexity": self.complexity,
            "budget_allocated": self.budget,
            "tokens_loaded": self.loaded_tokens,
            "usage_pct": status["usage_pct"],
            "exceeded_budget": status["exceeded"],
            "scope_breakdown": self.scope_loads,
            "warnings_count": len(self.warnings),
            "warnings": self.warnings,
            "duration_seconds": status["duration_seconds"],
            "success": success,
            "error": error_message if error_message else None
        }

        # Append to JSONL file
        try:
            with open(self.log_file, "a") as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            print(f"Warning: Failed to log budget usage: {e}", file=sys.stderr)

    def print_summary(self):
        """Print budget usage summary"""
        status = self.get_status()

        print("\n" + "=" * 70)
        print("BUDGET USAGE SUMMARY")
        print("=" * 70)
        print(f"\nAgent: {status['agent']}")
        if status['task']:
            print(f"Task: {status['task']}")
        print(f"Complexity: {status['complexity']}")
        print(f"\nBudget: {status['budget']:,} tokens")
        print(f"Loaded: {status['loaded']:,} tokens ({status['usage_pct']:.1f}%)")
        print(f"Remaining: {status['remaining']:,} tokens")

        if status['exceeded']:
            overage = status['loaded'] - status['budget']
            print(f"\n❌ EXCEEDED by {overage:,} tokens ({(overage/status['budget'])*100:.1f}%)")

        if status['scope_breakdown']:
            print(f"\nScope Breakdown:")
            for scope, tokens in sorted(status['scope_breakdown'].items(), key=lambda x: x[1], reverse=True):
                pct = (tokens / status['loaded']) * 100 if status['loaded'] > 0 else 0
                print(f"  {scope:20s}: {tokens:7,} tokens ({pct:5.1f}%)")

        if status['warnings']:
            print(f"\nWarnings ({len(status['warnings'])}):")
            for warning in status['warnings']:
                print(f"  {warning['message']}")

        print(f"\nDuration: {status['duration_seconds']:.2f}s")
        print("=" * 70)


def main():
    """CLI entry point for testing"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Test budget monitoring functionality"
    )
    parser.add_argument("agent", help="Agent name")
    parser.add_argument("budget", type=int, help="Budget in tokens")
    parser.add_argument("--task", default="", help="Task description")
    parser.add_argument("--complexity", default="medium", help="Task complexity")

    args = parser.parse_args()

    # Create monitor
    monitor = BudgetMonitor(
        agent_name=args.agent,
        budget=args.budget,
        task_description=args.task,
        complexity=args.complexity
    )

    print(f"\nMonitoring budget for {args.agent}")
    print(f"Budget: {args.budget:,} tokens")
    print(f"Thresholds: INFO={monitor.thresholds['info']:.0%}, "
          f"WARNING={monitor.thresholds['warning']:.0%}, "
          f"CRITICAL={monitor.thresholds['critical']:.0%}\n")

    # Simulate loading
    print("Simulating memory loads...\n")

    # Load global scope (20% of budget)
    global_tokens = int(args.budget * 0.2)
    print(f"Loading global scope: {global_tokens:,} tokens")
    monitor.track_load("global", global_tokens)
    time.sleep(0.5)

    # Load recent scope (30% of budget)
    recent_tokens = int(args.budget * 0.3)
    print(f"Loading recent scope: {recent_tokens:,} tokens")
    monitor.track_load("agent_recent", recent_tokens)
    time.sleep(0.5)

    # Load patterns scope (40% of budget - will trigger warnings)
    patterns_tokens = int(args.budget * 0.4)
    print(f"Loading patterns scope: {patterns_tokens:,} tokens")
    monitor.track_load("agent_patterns", patterns_tokens)
    time.sleep(0.5)

    # Print summary
    monitor.print_summary()

    # Log usage
    monitor.log_usage(success=True)
    print(f"\n✅ Usage logged to: {monitor.log_file}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
