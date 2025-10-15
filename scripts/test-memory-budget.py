#!/usr/bin/env python3
"""
Integration Test and Demo for Memory Budget System

Demonstrates the complete token-aware memory loading system:
1. Loads all patterns with metadata
2. Calculates relevance scores
3. Applies token budget
4. Shows before/after comparison

Usage:
    python scripts/test-memory-budget.py                    # Default test
    python scripts/test-memory-budget.py --agent dbt-expert # Specific agent
    python scripts/test-memory-budget.py --budget 15000     # Custom budget
"""

from pathlib import Path
import json
import sys

# Import our utilities with fallback for hyphenated filenames
import importlib.util
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

# Load memory_budget module
spec = importlib.util.spec_from_file_location("memory_budget", script_dir / "memory-budget.py")
memory_budget = importlib.util.module_from_spec(spec)
spec.loader.exec_module(memory_budget)
MemoryBudget = memory_budget.MemoryBudget
Pattern = memory_budget.Pattern

# Load relevance_scoring module
spec = importlib.util.spec_from_file_location("relevance_scoring", script_dir / "relevance-scoring.py")
relevance_scoring = importlib.util.module_from_spec(spec)
spec.loader.exec_module(relevance_scoring)
RelevanceScorer = relevance_scoring.RelevanceScorer
ScoringContext = relevance_scoring.ScoringContext

# Load count_tokens module
spec = importlib.util.spec_from_file_location("count_tokens", script_dir / "count-tokens.py")
count_tokens = importlib.util.module_from_spec(spec)
spec.loader.exec_module(count_tokens)
TokenCounter = count_tokens.TokenCounter


def load_patterns_from_directory(directory: Path) -> list:
    """
    Load all patterns from a directory with metadata.

    Args:
        directory: Directory containing patterns

    Returns:
        List of Pattern objects
    """
    patterns = []

    for pattern_file in directory.rglob("*.md"):
        if not pattern_file.is_file():
            continue

        # Load metadata
        metadata_file = pattern_file.with_suffix('.metadata.json')
        if not metadata_file.exists():
            continue

        try:
            metadata = json.loads(metadata_file.read_text())
            content = pattern_file.read_text(encoding='utf-8')

            pattern = Pattern(
                path=pattern_file,
                token_count=metadata["token_count"],
                relevance_score=0.5,  # Will be calculated
                content=content,
                metadata=metadata
            )
            patterns.append(pattern)
        except Exception as e:
            print(f"⚠️  Error loading {pattern_file.name}: {e}")

    return patterns


def run_test(agent_name: str = "dbt-expert", budget_limit: int = 20000, task_type: str = "optimization"):
    """
    Run complete memory budget test.

    Args:
        agent_name: Agent name for context
        budget_limit: Token budget limit
        task_type: Task type for context scoring
    """
    print("\n" + "=" * 70)
    print("MEMORY BUDGET SYSTEM - INTEGRATION TEST")
    print("=" * 70)

    # Load patterns
    print(f"\n📂 Loading patterns from .claude/memory...")
    memory_dir = Path(".claude/memory")
    patterns = load_patterns_from_directory(memory_dir)
    print(f"   Loaded {len(patterns)} patterns")

    # Load agent files
    print(f"\n📂 Loading agent files from .claude/agents...")
    agents_dir = Path(".claude/agents")
    agent_patterns = load_patterns_from_directory(agents_dir)
    print(f"   Loaded {len(agent_patterns)} agent files")

    # Combine
    all_patterns = patterns + agent_patterns
    total_tokens_available = sum(p.token_count for p in all_patterns)

    print(f"\n📊 Baseline (before budget):")
    print(f"   Total patterns:     {len(all_patterns)}")
    print(f"   Total tokens:       {total_tokens_available:,}")
    print(f"   Context window:     200,000 tokens")
    print(f"   Overflow:           {total_tokens_available - 200000:,} tokens ({((total_tokens_available - 200000) / 200000 * 100):.1f}%)")

    # Calculate relevance scores
    print(f"\n🎯 Calculating relevance scores for agent='{agent_name}', task='{task_type}'...")
    scorer = RelevanceScorer()
    context = ScoringContext(
        agent_name=agent_name,
        task_type=task_type,
        technologies=["dbt", "snowflake", "sql"],
        keywords=["optimization", "performance", "query"]
    )

    for pattern in all_patterns:
        pattern.relevance_score = scorer.calculate_relevance(
            pattern.path,
            pattern.content,
            pattern.metadata,
            context
        )

    # Apply budget
    print(f"\n💰 Applying {budget_limit:,} token budget...")
    budget = MemoryBudget(max_tokens=budget_limit)
    loaded_patterns = budget.load_patterns_with_budget(all_patterns)

    # Results
    print(f"\n✅ Budget Results:")
    print(f"   Loaded patterns:    {len(loaded_patterns)}")
    print(f"   Skipped patterns:   {len(budget.skipped_patterns)}")
    print(f"   Tokens used:        {budget.current_tokens:,}")
    print(f"   Tokens available:   {budget.available_tokens():,}")
    print(f"   Utilization:        {budget.utilization_pct():.1f}%")

    # Calculate reduction
    loaded_tokens = budget.current_tokens
    reduction_pct = ((total_tokens_available - loaded_tokens) / total_tokens_available) * 100

    print(f"\n📉 Token Reduction:")
    print(f"   Before:             {total_tokens_available:,} tokens")
    print(f"   After:              {loaded_tokens:,} tokens")
    print(f"   Reduction:          {reduction_pct:.1f}%")
    print(f"   Context freed:      {total_tokens_available - loaded_tokens:,} tokens for actual work")

    # Show top loaded patterns
    print(f"\n🏆 Top 10 Loaded Patterns (by relevance):")
    for i, pattern in enumerate(loaded_patterns[:10], 1):
        print(f"   {i:2d}. {pattern.relevance_score:.3f} - {pattern.name[:50]}")

    # Show top skipped patterns
    if budget.skipped_patterns:
        print(f"\n⏭️  Top 10 Skipped Patterns (lowest relevance):")
        sorted_skipped = sorted(budget.skipped_patterns, key=lambda p: p.relevance_score, reverse=True)
        for i, pattern in enumerate(sorted_skipped[:10], 1):
            print(f"   {i:2d}. {pattern.relevance_score:.3f} - {pattern.name[:50]}")

    # Success validation
    print(f"\n✓ SUCCESS CRITERIA:")
    print(f"   ✅ Token budget enforced:     {loaded_tokens <= budget_limit}")
    print(f"   ✅ Reduction >40%:            {reduction_pct > 40}")
    print(f"   ✅ Patterns loaded:           {len(loaded_patterns) > 0}")
    print(f"   ✅ Relevance-based priority:  {loaded_patterns[0].relevance_score >= loaded_patterns[-1].relevance_score}")

    print("\n" + "=" * 70)

    # Save results
    output_file = Path("projects/active/ai-memory-system-improvements/tasks/test-results.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    results = {
        "test_config": {
            "agent_name": agent_name,
            "budget_limit": budget_limit,
            "task_type": task_type
        },
        "baseline": {
            "total_patterns": len(all_patterns),
            "total_tokens": total_tokens_available,
            "overflow_tokens": total_tokens_available - 200000
        },
        "results": {
            "loaded_patterns": len(loaded_patterns),
            "skipped_patterns": len(budget.skipped_patterns),
            "tokens_used": loaded_tokens,
            "tokens_available": budget.available_tokens(),
            "utilization_pct": budget.utilization_pct()
        },
        "metrics": {
            "reduction_pct": reduction_pct,
            "context_freed": total_tokens_available - loaded_tokens
        },
        "validation": {
            "budget_enforced": loaded_tokens <= budget_limit,
            "reduction_target_met": reduction_pct > 40,
            "patterns_loaded": len(loaded_patterns) > 0,
            "relevance_priority": loaded_patterns[0].relevance_score >= loaded_patterns[-1].relevance_score
        }
    }

    output_file.write_text(json.dumps(results, indent=2))
    print(f"\n📄 Results saved to: {output_file}")


def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Test memory budget system with realistic loads"
    )
    parser.add_argument(
        "--agent",
        default="dbt-expert",
        help="Agent name for context (default: dbt-expert)"
    )
    parser.add_argument(
        "--budget",
        type=int,
        default=20000,
        help="Token budget limit (default: 20000)"
    )
    parser.add_argument(
        "--task-type",
        default="optimization",
        help="Task type for context (default: optimization)"
    )

    args = parser.parse_args()

    try:
        run_test(
            agent_name=args.agent,
            budget_limit=args.budget,
            task_type=args.task_type
        )
        return 0
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
