#!/usr/bin/env python3
"""
Memory Budget System for DA Agent Hub

Enforces token budgets for loading memory patterns and agent files.
Prioritizes patterns by relevance score and respects token limits.

Usage:
    from memory_budget import MemoryBudget, Pattern

    budget = MemoryBudget(max_tokens=20000)
    patterns = load_patterns_from_disk()
    loaded = budget.load_patterns_with_budget(patterns)
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from pathlib import Path
import json
from datetime import datetime


@dataclass
class Pattern:
    """Represents a memory pattern or agent file"""
    path: Path
    token_count: int
    relevance_score: float
    content: str
    metadata: Dict = field(default_factory=dict)

    @property
    def name(self) -> str:
        """Get pattern name"""
        return self.path.name

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        return {
            "path": str(self.path),
            "name": self.name,
            "token_count": self.token_count,
            "relevance_score": self.relevance_score,
            "metadata": self.metadata
        }


class MemoryBudget:
    """Manages token budget for loading memory patterns"""

    def __init__(self, max_tokens: int = 20000):
        """
        Initialize memory budget system.

        Args:
            max_tokens: Maximum tokens allowed (default: 20k)
        """
        self.max_tokens = max_tokens
        self.current_tokens = 0
        self.loaded_patterns: List[Pattern] = []
        self.skipped_patterns: List[Pattern] = []

    def reset(self):
        """Reset budget to empty state"""
        self.current_tokens = 0
        self.loaded_patterns = []
        self.skipped_patterns = []

    def available_tokens(self) -> int:
        """Get remaining token budget"""
        return self.max_tokens - self.current_tokens

    def utilization_pct(self) -> float:
        """Get budget utilization percentage"""
        return (self.current_tokens / self.max_tokens) * 100

    def can_load(self, pattern: Pattern) -> bool:
        """
        Check if pattern can be loaded within budget.

        Args:
            pattern: Pattern to check

        Returns:
            True if pattern fits in remaining budget
        """
        return self.current_tokens + pattern.token_count <= self.max_tokens

    def add_pattern(self, pattern: Pattern) -> bool:
        """
        Attempt to add pattern to budget.

        Args:
            pattern: Pattern to add

        Returns:
            True if pattern was added, False if budget exhausted
        """
        if self.can_load(pattern):
            self.loaded_patterns.append(pattern)
            self.current_tokens += pattern.token_count
            return True
        else:
            self.skipped_patterns.append(pattern)
            return False

    def load_patterns_with_budget(self, patterns: List[Pattern]) -> List[Pattern]:
        """
        Load patterns respecting budget, prioritized by relevance.

        Args:
            patterns: List of patterns to load

        Returns:
            List of loaded patterns (within budget)
        """
        # Sort by relevance score (highest first)
        sorted_patterns = sorted(
            patterns,
            key=lambda p: p.relevance_score,
            reverse=True
        )

        # Load patterns until budget exhausted
        for pattern in sorted_patterns:
            if not self.add_pattern(pattern):
                # Budget exhausted, remaining patterns skipped
                pass

        return self.loaded_patterns

    def get_stats(self) -> Dict:
        """
        Get budget utilization statistics.

        Returns:
            Dictionary with detailed statistics
        """
        return {
            "budget": {
                "max_tokens": self.max_tokens,
                "used_tokens": self.current_tokens,
                "available_tokens": self.available_tokens(),
                "utilization_pct": round(self.utilization_pct(), 2)
            },
            "patterns": {
                "loaded_count": len(self.loaded_patterns),
                "skipped_count": len(self.skipped_patterns),
                "total_count": len(self.loaded_patterns) + len(self.skipped_patterns)
            },
            "loaded_patterns": [p.to_dict() for p in self.loaded_patterns],
            "skipped_patterns": [p.to_dict() for p in self.skipped_patterns]
        }

    def get_summary(self) -> str:
        """
        Get human-readable summary of budget utilization.

        Returns:
            Formatted summary string
        """
        stats = self.get_stats()

        lines = [
            "=" * 60,
            "MEMORY BUDGET SUMMARY",
            "=" * 60,
            f"Budget Limit:       {stats['budget']['max_tokens']:,} tokens",
            f"Tokens Used:        {stats['budget']['used_tokens']:,} tokens",
            f"Tokens Available:   {stats['budget']['available_tokens']:,} tokens",
            f"Utilization:        {stats['budget']['utilization_pct']:.1f}%",
            "",
            f"Patterns Loaded:    {stats['patterns']['loaded_count']}",
            f"Patterns Skipped:   {stats['patterns']['skipped_count']}",
            f"Total Patterns:     {stats['patterns']['total_count']}",
            "=" * 60
        ]

        return "\n".join(lines)

    def save_stats(self, output_file: Path):
        """
        Save budget statistics to JSON file.

        Args:
            output_file: Path to output JSON file
        """
        output_file.parent.mkdir(parents=True, exist_ok=True)
        stats = self.get_stats()

        # Add timestamp
        stats["timestamp"] = datetime.now().isoformat()

        output_file.write_text(json.dumps(stats, indent=2))


class MemoryBudgetManager:
    """High-level manager for memory budgets across different scopes"""

    def __init__(self, config_file: Optional[Path] = None):
        """
        Initialize budget manager with configuration.

        Args:
            config_file: Path to budget configuration JSON
        """
        self.config_file = config_file or Path(".claude/config/memory-budget.json")
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """Load budget configuration from file"""
        if self.config_file.exists():
            return json.loads(self.config_file.read_text())
        else:
            # Default configuration
            return {
                "global_budget": 20000,
                "scope_budgets": {
                    "patterns": 10000,
                    "agents": 8000,
                    "recent": 2000
                },
                "agent_specific_budgets": {
                    "analytics-engineer": 20000,
                    "dbt-expert": 15000,
                    "snowflake-expert": 15000,
                    "aws-expert": 15000
                }
            }

    def save_config(self):
        """Save configuration to file"""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        self.config_file.write_text(json.dumps(self.config, indent=2))

    def get_budget_for_scope(self, scope: str) -> int:
        """
        Get token budget for a specific scope.

        Args:
            scope: Scope name (patterns, agents, recent, or agent name)

        Returns:
            Token budget for scope
        """
        # Check scope-specific budgets
        if scope in self.config.get("scope_budgets", {}):
            return self.config["scope_budgets"][scope]

        # Check agent-specific budgets
        if scope in self.config.get("agent_specific_budgets", {}):
            return self.config["agent_specific_budgets"][scope]

        # Default to global budget
        return self.config.get("global_budget", 20000)

    def create_budget(self, scope: str) -> MemoryBudget:
        """
        Create a MemoryBudget instance for a scope.

        Args:
            scope: Scope name

        Returns:
            Configured MemoryBudget instance
        """
        max_tokens = self.get_budget_for_scope(scope)
        return MemoryBudget(max_tokens=max_tokens)


def main():
    """CLI entry point for testing"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Memory budget system for DA Agent Hub"
    )
    parser.add_argument("--scope", default="global", help="Budget scope")
    parser.add_argument("--max-tokens", type=int, help="Override max tokens")
    parser.add_argument("--config", help="Path to config file")

    args = parser.parse_args()

    # Initialize manager
    config_file = Path(args.config) if args.config else None
    manager = MemoryBudgetManager(config_file=config_file)

    # Create budget for scope
    if args.max_tokens:
        budget = MemoryBudget(max_tokens=args.max_tokens)
    else:
        budget = manager.create_budget(args.scope)

    print(f"\nMemory Budget for scope '{args.scope}':")
    print(f"Max Tokens: {budget.max_tokens:,}")
    print(f"\nConfiguration loaded from: {manager.config_file}")

    # Save default config if it doesn't exist
    if not manager.config_file.exists():
        manager.save_config()
        print(f"✅ Default configuration saved to: {manager.config_file}")


if __name__ == "__main__":
    main()
