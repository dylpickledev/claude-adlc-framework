#!/usr/bin/env python3
"""
Task Complexity Detector

Automatically detects task complexity from description and context to
determine appropriate memory budget allocation.

Complexity Tiers:
- simple: Single query, single tool, specific question (0.5x budget)
- medium: Multiple steps, single system, standard analysis (1.0x budget)
- complex: Multi-step workflow, multiple tools, deep analysis (1.5x budget)
- multi-system: Cross-system coordination, architectural decisions (2.0x budget)

Usage:
    python scripts/detect-task-complexity.py "List all Snowflake tables"
    python scripts/detect-task-complexity.py "Investigate cross-system data freshness"
    python scripts/detect-task-complexity.py --interactive
    echo "Optimize dbt model performance" | python scripts/detect-task-complexity.py --stdin
"""

import sys
import re
from typing import Dict, List, Tuple
from pathlib import Path
import json


class TaskComplexityDetector:
    """Detect task complexity from natural language descriptions"""

    def __init__(self):
        """Initialize detector with signal patterns"""
        # Load complexity definitions from budget profiles
        profiles_path = Path(".claude/memory/budget-profiles.json")
        if profiles_path.exists():
            config = json.loads(profiles_path.read_text())
            self.complexity_definitions = config.get("complexity_multipliers", {})
        else:
            self.complexity_definitions = {}

        # Signal patterns for each complexity tier
        self.complexity_signals = {
            "simple": [
                # Single action verbs
                r"\b(list|show|get|fetch|find|display|view|check)\b",
                # Status queries
                r"\b(status|state|current)\b",
                # Counting
                r"\bhow many\b",
                r"\bcount\b",
                # Simple lookups
                r"\bwhat is\b",
                r"\bwhere is\b",
                r"\bwhich\b",
            ],
            "complex": [
                # Analysis verbs
                r"\b(analyze|investigate|troubleshoot|debug|diagnose)\b",
                r"\b(optimize|improve|enhance|refactor)\b",
                r"\b(compare|evaluate|assess|review)\b",
                # Multi-step indicators
                r"\bmulti[- ]step\b",
                r"\bcomprehensive\b",
                r"\bdeep dive\b",
                r"\bin[- ]depth\b",
                # Problem-solving
                r"\b(fix|resolve|solve|address)\b",
                r"\broot cause\b",
                r"\bperformance (issue|problem)\b",
            ],
            "multi-system": [
                # Cross-system keywords
                r"\bcross[- ]system\b",
                r"\bend[- ]to[- ]end\b",
                r"\b(integration|coordinate|orchestrat)\w*\b",
                r"\bmultiple (tools|systems|services)\b",
                # Architecture keywords
                r"\b(architecture|design|platform)\b",
                r"\b(migrate|migration)\b",
                r"\bdata flow\b",
                r"\bpipeline\b.*\b(analysis|design)\b",
                # Cross-tool combinations
                r"\b(dbt|snowflake|tableau|prefect|orchestra).*\b(dbt|snowflake|tableau|prefect|orchestra)\b",
            ]
        }

        # Negative signals (reduce complexity)
        self.simplicity_boosters = [
            r"\bsimple\b",
            r"\bquick\b",
            r"\bjust\b",
            r"\bonly\b",
        ]

        # Complexity boosters (increase complexity)
        self.complexity_boosters = [
            r"\ball\b",
            r"\bevery\b",
            r"\bcomplex\b",
            r"\bdetailed\b",
        ]

    def detect_complexity(
        self,
        task_description: str,
        context: Dict = None
    ) -> Tuple[str, float, List[str]]:
        """Detect task complexity from description

        Args:
            task_description: Natural language task description
            context: Optional context (agent history, related tasks, etc.)

        Returns:
            (complexity_tier, confidence_score, matched_signals)
        """
        desc_lower = task_description.lower()
        signals_matched = []
        scores = {
            "simple": 0.0,
            "medium": 0.0,
            "complex": 0.0,
            "multi-system": 0.0
        }

        # Score each complexity tier by signal matches
        for tier, patterns in self.complexity_signals.items():
            for pattern in patterns:
                matches = re.findall(pattern, desc_lower)
                if matches:
                    # Each match adds to score
                    # Simple patterns get higher weight (more definitive)
                    if tier == "simple":
                        match_weight = 2.0 / len(patterns)
                    elif tier == "multi-system":
                        match_weight = 1.5 / len(patterns)
                    else:
                        match_weight = 1.0 / len(patterns)

                    scores[tier] += match_weight * len(matches)
                    signals_matched.append(f"{tier}: {pattern}")

        # Apply simplicity boosters (reduce complexity)
        simplicity_boost = 0
        for pattern in self.simplicity_boosters:
            if re.search(pattern, desc_lower):
                simplicity_boost += 1.0
                signals_matched.append(f"simplicity: {pattern}")

        # Apply complexity boosters (increase complexity)
        # Note: "all" is weak signal - don't overweight it
        complexity_boost = 0
        for pattern in self.complexity_boosters:
            if re.search(pattern, desc_lower):
                # "all" is weak, others are stronger
                if pattern == r"\ball\b":
                    complexity_boost += 0.1
                else:
                    complexity_boost += 0.5
                signals_matched.append(f"complexity: {pattern}")

        # Adjust scores
        if simplicity_boost > 0:
            scores["simple"] += simplicity_boost

        if complexity_boost > 0:
            scores["complex"] += complexity_boost
            scores["multi-system"] += complexity_boost

        # Context-based adjustments
        if context:
            # Multiple agents mentioned → multi-system
            agent_count = context.get("agent_count", 0)
            if agent_count > 1:
                scores["multi-system"] += 1.0
                signals_matched.append(f"context: {agent_count} agents")

            # Task history → if previous tasks were complex
            previous_complexity = context.get("previous_complexity")
            if previous_complexity in ["complex", "multi-system"]:
                scores[previous_complexity] += 0.5
                signals_matched.append(f"context: previous task was {previous_complexity}")

        # Determine winning tier
        max_score = max(scores.values())

        if max_score == 0:
            # No clear signals → default to medium
            detected_tier = "medium"
            confidence = 0.5
        else:
            detected_tier = max(scores, key=scores.get)
            # Confidence based on score separation
            sorted_scores = sorted(scores.values(), reverse=True)
            if len(sorted_scores) > 1:
                separation = sorted_scores[0] - sorted_scores[1]
                confidence = min(0.5 + (separation * 0.2), 1.0)
            else:
                confidence = 0.7

        return detected_tier, confidence, signals_matched

    def explain_complexity(
        self,
        task_description: str,
        context: Dict = None
    ) -> Dict:
        """Detect complexity and provide detailed explanation

        Returns:
            {
                "task": str,
                "detected_complexity": str,
                "confidence": float,
                "description": str,
                "multiplier": float,
                "signals_matched": list,
                "recommendations": list
            }
        """
        tier, confidence, signals = self.detect_complexity(task_description, context)

        # Get complexity definition
        tier_config = self.complexity_definitions.get(tier, {})

        # Generate recommendations
        recommendations = []

        if confidence < 0.6:
            recommendations.append(
                "⚠️ Low confidence detection - consider manual override if needed"
            )

        if tier == "simple" and len(task_description.split()) > 20:
            recommendations.append(
                "💡 Task description is long but classified as simple - verify complexity"
            )

        if tier == "multi-system" and confidence > 0.8:
            recommendations.append(
                "✅ High confidence multi-system task - ensure sufficient budget"
            )

        return {
            "task": task_description,
            "detected_complexity": tier,
            "confidence": confidence,
            "description": tier_config.get("description", ""),
            "multiplier": tier_config.get("multiplier", 1.0),
            "signals_matched": signals,
            "recommendations": recommendations
        }


def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Detect task complexity from natural language description"
    )
    parser.add_argument("task", nargs="?",
                        help="Task description to analyze")
    parser.add_argument("--stdin", action="store_true",
                        help="Read task from stdin")
    parser.add_argument("--interactive", "-i", action="store_true",
                        help="Interactive mode for multiple tasks")
    parser.add_argument("--json", action="store_true",
                        help="Output results as JSON")
    parser.add_argument("--show-signals", action="store_true",
                        help="Show all complexity signal patterns")

    args = parser.parse_args()

    detector = TaskComplexityDetector()

    # Show signal patterns
    if args.show_signals:
        print("\n" + "=" * 70)
        print("COMPLEXITY DETECTION SIGNALS")
        print("=" * 70)

        for tier, patterns in detector.complexity_signals.items():
            print(f"\n{tier.upper()}:")
            for pattern in patterns:
                print(f"  - {pattern}")

        print("\nSIMPLICITY BOOSTERS:")
        for pattern in detector.simplicity_boosters:
            print(f"  - {pattern}")

        print("\nCOMPLEXITY BOOSTERS:")
        for pattern in detector.complexity_boosters:
            print(f"  - {pattern}")

        print("=" * 70)
        return 0

    # Interactive mode
    if args.interactive:
        print("\n" + "=" * 70)
        print("INTERACTIVE COMPLEXITY DETECTION")
        print("=" * 70)
        print("\nEnter task descriptions (one per line)")
        print("Press Ctrl+D (Unix) or Ctrl+Z (Windows) when done\n")

        try:
            while True:
                task = input("Task: ").strip()
                if not task:
                    continue

                result = detector.explain_complexity(task)

                print(f"\n  Complexity: {result['detected_complexity'].upper()} "
                      f"(confidence: {result['confidence']:.1%})")
                print(f"  Multiplier: ×{result['multiplier']:.1f}")

                if result['signals_matched']:
                    print(f"  Signals: {len(result['signals_matched'])} matched")

                print()

        except (EOFError, KeyboardInterrupt):
            print("\n\nDone!")
            return 0

    # Read from stdin
    if args.stdin:
        task = sys.stdin.read().strip()
    elif args.task:
        task = args.task
    else:
        parser.print_help()
        return 1

    if not task:
        print("Error: No task provided", file=sys.stderr)
        return 1

    # Detect complexity
    result = detector.explain_complexity(task)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        # Pretty print
        print("\n" + "=" * 70)
        print("TASK COMPLEXITY DETECTION")
        print("=" * 70)
        print(f"\nTask: {result['task']}")
        print(f"\nDetected Complexity: {result['detected_complexity'].upper()}")
        print(f"Confidence: {result['confidence']:.1%}")
        print(f"Multiplier: ×{result['multiplier']:.1f}")
        print(f"Description: {result['description']}")

        if result['signals_matched']:
            print(f"\nSignals Matched ({len(result['signals_matched'])}):")
            for signal in result['signals_matched'][:10]:  # Show first 10
                print(f"  - {signal}")
            if len(result['signals_matched']) > 10:
                print(f"  ... and {len(result['signals_matched']) - 10} more")

        if result['recommendations']:
            print("\nRecommendations:")
            for rec in result['recommendations']:
                print(f"  {rec}")

        print("=" * 70)

    return 0


if __name__ == "__main__":
    sys.exit(main())
