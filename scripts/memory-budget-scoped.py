#!/usr/bin/env python3
"""
Scope-Aware Memory Budget System

Enhanced memory budget that loads agent-specific patterns first, then global patterns.
This is Phase 4 of the AI Memory System improvements.

Usage:
    from memory_budget_scoped import ScopedMemoryBudget

    budget = ScopedMemoryBudget(
        max_tokens=20000,
        agent_name="dbt-expert",
        agent_type="specialists"
    )

    loaded = budget.load_patterns_with_scope(context={"task": "optimize dbt model"})
"""

from pathlib import Path
from typing import List, Optional, Dict
from dataclasses import dataclass
import json
import sys

# Import existing relevance scorer
import importlib.util
script_dir = Path(__file__).parent
spec = importlib.util.spec_from_file_location("relevance_scoring", script_dir / "relevance-scoring.py")
relevance_scoring = importlib.util.module_from_spec(spec)
spec.loader.exec_module(relevance_scoring)
RelevanceScorer = relevance_scoring.RelevanceScorer
ScoringContext = relevance_scoring.ScoringContext

# Import token counter
spec_token = importlib.util.spec_from_file_location("count_tokens", script_dir / "count-tokens.py")
count_tokens_module = importlib.util.module_from_spec(spec_token)
spec_token.loader.exec_module(count_tokens_module)
TokenCounter = count_tokens_module.TokenCounter

# Import Phase 6 budget components
spec_budget_calc = importlib.util.spec_from_file_location("calculate_agent_budget", script_dir / "calculate-agent-budget.py")
budget_calc_module = importlib.util.module_from_spec(spec_budget_calc)
spec_budget_calc.loader.exec_module(budget_calc_module)
AgentBudgetCalculator = budget_calc_module.AgentBudgetCalculator

spec_complexity = importlib.util.spec_from_file_location("detect_task_complexity", script_dir / "detect-task-complexity.py")
complexity_module = importlib.util.module_from_spec(spec_complexity)
spec_complexity.loader.exec_module(complexity_module)
TaskComplexityDetector = complexity_module.TaskComplexityDetector

spec_monitor = importlib.util.spec_from_file_location("budget_monitor", script_dir / "budget-monitor.py")
monitor_module = importlib.util.module_from_spec(spec_monitor)
spec_monitor.loader.exec_module(monitor_module)
BudgetMonitor = monitor_module.BudgetMonitor


@dataclass
class Pattern:
    """Pattern with metadata"""
    path: Path
    token_count: int
    relevance_score: float
    content: str
    metadata: dict
    scope: str  # "agent-specific" or "global"


class ScopedMemoryBudget:
    """Memory budget with agent-specific scope awareness and Phase 6 budget profiles"""

    def __init__(
        self,
        max_tokens: int = None,
        agent_name: Optional[str] = None,
        agent_type: Optional[str] = None,
        task_description: str = "",
        complexity: str = None,
        use_budget_profiles: bool = True
    ):
        """Initialize scoped memory budget

        Args:
            max_tokens: Maximum tokens (if None, use budget profiles)
            agent_name: Agent name (e.g., "dbt-expert")
            agent_type: Agent type ("specialists" or "roles")
            task_description: Task description for complexity detection
            complexity: Override complexity (simple, medium, complex, multi-system)
            use_budget_profiles: Enable Phase 6 budget profile system
        """
        self.agent_name = agent_name
        self.agent_type = agent_type  # "specialists" or "roles"
        self.task_description = task_description
        self.use_budget_profiles = use_budget_profiles

        # Phase 6: Calculate budget from profiles if enabled
        if use_budget_profiles and agent_name and agent_type:
            try:
                # Build full agent path
                agent_full_name = f"{agent_type}/{agent_name}"

                # Detect complexity if not provided
                if complexity is None and task_description:
                    detector = TaskComplexityDetector()
                    complexity, _, _ = detector.detect_complexity(task_description)
                elif complexity is None:
                    complexity = "medium"  # Default

                self.detected_complexity = complexity

                # Calculate budget
                calculator = AgentBudgetCalculator()
                budget_info = calculator.calculate_budget(agent_full_name, complexity)

                self.max_tokens = budget_info["calculated_budget"]
                self.budget_info = budget_info

                # Initialize budget monitor
                self.monitor = BudgetMonitor(
                    agent_name=agent_full_name,
                    budget=self.max_tokens,
                    task_description=task_description,
                    complexity=complexity
                )

                print(f"📊 Budget Profile: {budget_info['profile_name']} "
                      f"| Complexity: {complexity} | Budget: {self.max_tokens:,} tokens")

            except Exception as e:
                # Fallback to manual budget if profiles fail
                print(f"⚠️  Budget profile failed ({e}), using manual budget")
                self.max_tokens = max_tokens or 20000
                self.budget_info = None
                self.monitor = None
                self.detected_complexity = None
        else:
            # Use manual budget (Phase 4 behavior)
            self.max_tokens = max_tokens or 20000
            self.budget_info = None
            self.monitor = None
            self.detected_complexity = None

        self.current_tokens = 0
        self.loaded_patterns: List[Pattern] = []
        self.skipped_patterns: List[Pattern] = []
        self.relevance_scorer = RelevanceScorer()
        self.token_counter = TokenCounter()

    def get_scope_directories(self) -> List[tuple]:
        """Get directories to load patterns from, in priority order

        Returns list of (directory, scope_type) tuples
        """
        base = Path(".claude/memory")
        directories = []

        # Priority 1: Agent-specific patterns (if agent specified)
        if self.agent_name and self.agent_type:
            agent_dir = base / self.agent_type / self.agent_name

            if agent_dir.exists():
                # Load in tier order: patterns > recent > intermediate
                if (agent_dir / "patterns").exists():
                    directories.append((agent_dir / "patterns", "agent-specific"))
                if (agent_dir / "recent").exists():
                    directories.append((agent_dir / "recent", "agent-specific"))
                if (agent_dir / "intermediate").exists():
                    directories.append((agent_dir / "intermediate", "agent-specific"))

        # Priority 2: Global patterns (always loaded)
        if (base / "patterns").exists():
            directories.append((base / "patterns", "global"))
        if (base / "recent").exists():
            directories.append((base / "recent", "global"))

        return directories

    def load_pattern(self, pattern_file: Path, scope: str, context: dict) -> Pattern:
        """Load a single pattern with metadata and relevance scoring"""

        content = pattern_file.read_text(encoding='utf-8')

        # Get token count from metadata or calculate
        metadata_file = pattern_file.with_suffix('.metadata.json')
        if metadata_file.exists():
            metadata = json.loads(metadata_file.read_text())
            token_count = metadata.get('token_count', 0)
            if token_count == 0:
                # Fallback: calculate if missing
                result = self.token_counter.count_file_tokens(pattern_file)
                token_count = result['token_count']
        else:
            # No metadata: calculate tokens
            result = self.token_counter.count_file_tokens(pattern_file)
            token_count = result['token_count']
            metadata = {
                'token_count': token_count,
                'use_count': 0,
                'confidence': None,
                'last_used': None
            }

        # Calculate relevance with context
        # Convert dict context to ScoringContext
        scoring_context = ScoringContext(
            technologies=context.get('technologies', []),
            task_type=context.get('task_type', 'general'),
            agent_name=context.get('agent_name'),
            keywords=context.get('keywords', [])
        )

        relevance = self.relevance_scorer.calculate_relevance(
            pattern_file,
            content,
            metadata,
            scoring_context
        )

        # Apply scope bonus
        if scope == "agent-specific":
            relevance += 0.3  # 30% bonus for agent-specific patterns

        # Create pattern object
        pattern_obj = Pattern(
            path=pattern_file,
            token_count=token_count,
            relevance_score=min(1.0, relevance),
            content=content,
            metadata=metadata,
            scope=scope
        )

        return pattern_obj

    def can_load(self, pattern: Pattern) -> bool:
        """Check if pattern can be loaded within budget"""
        return self.current_tokens + pattern.token_count <= self.max_tokens

    def add_pattern(self, pattern: Pattern) -> bool:
        """Attempt to add pattern to budget"""
        if self.can_load(pattern):
            self.loaded_patterns.append(pattern)
            self.current_tokens += pattern.token_count

            # Phase 6: Track loading in budget monitor
            if self.monitor:
                self.monitor.track_load(pattern.scope, pattern.token_count)

            return True
        else:
            self.skipped_patterns.append(pattern)
            return False

    def load_patterns_with_scope(self, context: dict) -> List[Pattern]:
        """Load patterns with scope awareness

        Args:
            context: Dict with task context (agent_name, technologies, task_type, etc.)

        Returns:
            List of loaded Pattern objects
        """
        all_patterns = []

        # Get scope directories in priority order
        scope_dirs = self.get_scope_directories()

        # Load patterns from each scope
        for scope_dir, scope_type in scope_dirs:
            for pattern_file in scope_dir.glob("*.md"):
                if pattern_file.is_file():
                    pattern = self.load_pattern(pattern_file, scope_type, context)
                    all_patterns.append(pattern)

        # Sort by relevance (scope-aware patterns already have bonus)
        sorted_patterns = sorted(
            all_patterns,
            key=lambda p: p.relevance_score,
            reverse=True
        )

        # Load patterns until budget exhausted
        for pattern in sorted_patterns:
            if not self.add_pattern(pattern):
                # Budget exhausted
                break

        return self.loaded_patterns

    def get_stats(self) -> dict:
        """Get budget utilization statistics"""
        return {
            "max_tokens": self.max_tokens,
            "used_tokens": self.current_tokens,
            "utilization_pct": (self.current_tokens / self.max_tokens) * 100,
            "loaded_count": len(self.loaded_patterns),
            "skipped_count": len(self.skipped_patterns),
            "loaded_patterns": [p.path.name for p in self.loaded_patterns],
            "skipped_patterns": [p.path.name for p in self.skipped_patterns]
        }

    def get_scope_stats(self) -> dict:
        """Get statistics about scope usage"""
        agent_patterns = []
        global_patterns = []

        for pattern in self.loaded_patterns:
            if pattern.scope == "agent-specific":
                agent_patterns.append(pattern)
            else:
                global_patterns.append(pattern)

        return {
            "agent_specific_count": len(agent_patterns),
            "global_count": len(global_patterns),
            "agent_specific_tokens": sum(p.token_count for p in agent_patterns),
            "global_tokens": sum(p.token_count for p in global_patterns),
            "agent_specific_pct": (len(agent_patterns) / len(self.loaded_patterns) * 100) if self.loaded_patterns else 0,
            "scope_efficiency": (sum(p.token_count for p in agent_patterns) / self.current_tokens * 100) if self.current_tokens > 0 else 0
        }

    def finish_loading(self, success: bool = True, error_message: str = ""):
        """Finalize pattern loading and log budget usage

        Args:
            success: Whether loading completed successfully
            error_message: Optional error message if loading failed
        """
        if self.monitor:
            self.monitor.log_usage(success=success, error_message=error_message)

    def print_stats(self, detailed: bool = False):
        """Print formatted statistics"""
        stats = self.get_stats()
        scope_stats = self.get_scope_stats()

        print("\n" + "=" * 70)
        print("SCOPED MEMORY BUDGET STATISTICS")
        print("=" * 70)

        if self.agent_name:
            print(f"Agent: {self.agent_name} ({self.agent_type})")
        else:
            print("Agent: None (global patterns only)")

        # Phase 6: Show budget profile info
        if self.budget_info:
            print(f"Profile: {self.budget_info['profile_name']} ({self.budget_info['complexity']})")

        print(f"\nBudget Utilization:")
        print(f"  Max Tokens:     {stats['max_tokens']:,}")
        print(f"  Used Tokens:    {stats['used_tokens']:,} ({stats['utilization_pct']:.1f}%)")
        print(f"  Loaded Patterns: {stats['loaded_count']}")
        print(f"  Skipped Patterns: {stats['skipped_count']}")

        print(f"\nScope Breakdown:")
        print(f"  Agent-Specific: {scope_stats['agent_specific_count']} patterns ({scope_stats['agent_specific_tokens']:,} tokens)")
        print(f"  Global:         {scope_stats['global_count']} patterns ({scope_stats['global_tokens']:,} tokens)")
        print(f"  Scope Efficiency: {scope_stats['scope_efficiency']:.1f}% of tokens from agent-specific patterns")

        # Phase 6: Show budget monitor warnings
        if self.monitor and self.monitor.warnings:
            print(f"\nBudget Alerts:")
            for warning in self.monitor.warnings:
                print(f"  {warning['message']}")

        if detailed:
            print("\n" + "=" * 70)
            print("LOADED PATTERNS (Top 10 by Relevance)")
            print("=" * 70)

            sorted_patterns = sorted(self.loaded_patterns, key=lambda p: p.relevance_score, reverse=True)
            for i, pattern in enumerate(sorted_patterns[:10], 1):
                scope_icon = "🎯" if pattern.scope == "agent-specific" else "🌍"
                print(f"{i:2d}. {scope_icon} {pattern.path.name[:50]:50s} (score: {pattern.relevance_score:.2f}, tokens: {pattern.token_count:,})")

        print("=" * 70)


def main():
    """CLI test entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Test scope-aware memory budget with Phase 6 budget profiles"
    )
    parser.add_argument("--agent-name", help="Agent name (e.g., dbt-expert)")
    parser.add_argument("--agent-type", choices=["specialists", "roles"], help="Agent type")
    parser.add_argument("--max-tokens", type=int, help="Maximum tokens (manual override)")
    parser.add_argument("--task", default="", help="Task description for complexity detection")
    parser.add_argument("--complexity", choices=["simple", "medium", "complex", "multi-system"],
                        help="Override complexity tier")
    parser.add_argument("--no-profiles", action="store_true", help="Disable budget profiles (Phase 4 mode)")
    parser.add_argument("--detailed", action="store_true", help="Show detailed stats")

    args = parser.parse_args()

    # Create budget
    budget = ScopedMemoryBudget(
        max_tokens=args.max_tokens,
        agent_name=args.agent_name,
        agent_type=args.agent_type,
        task_description=args.task,
        complexity=args.complexity,
        use_budget_profiles=not args.no_profiles
    )

    # Load patterns
    context = {
        "agent_name": args.agent_name,
        "technologies": ["dbt", "snowflake", "sql"] if args.agent_name == "dbt-expert" else []
    }

    print(f"\nLoading patterns for {args.agent_name or 'global'}...")
    loaded = budget.load_patterns_with_scope(context)

    # Finalize loading
    budget.finish_loading(success=True)

    # Print stats
    budget.print_stats(detailed=args.detailed)


if __name__ == "__main__":
    sys.exit(main() if main() is not None else 0)
