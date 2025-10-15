#!/usr/bin/env python3
"""
Relevance Scoring Algorithm for DA Agent Hub Memory System

Calculates relevance scores (0-1) based on:
- Recency: When pattern was last used/updated
- Usage: How often pattern has been applied
- Context: Relevance to current task/agent

Usage:
    from relevance_scoring import RelevanceScorer

    scorer = RelevanceScorer()
    score = scorer.calculate_relevance(pattern, context)
"""

from datetime import datetime, timedelta
from pathlib import Path
import json
import math
from typing import Optional, Dict, List
from dataclasses import dataclass


@dataclass
class ScoringContext:
    """Context for relevance scoring"""
    agent_name: Optional[str] = None
    task_type: Optional[str] = None
    technologies: Optional[List[str]] = None
    keywords: Optional[List[str]] = None

    @classmethod
    def from_dict(cls, data: Dict) -> 'ScoringContext':
        """Create context from dictionary"""
        return cls(
            agent_name=data.get("agent_name"),
            task_type=data.get("task_type"),
            technologies=data.get("technologies", []),
            keywords=data.get("keywords", [])
        )


class RelevanceScorer:
    """Calculates relevance scores for memory patterns"""

    def __init__(
        self,
        recency_weight: float = 0.3,
        usage_weight: float = 0.3,
        context_weight: float = 0.4
    ):
        """
        Initialize relevance scorer with weights.

        Args:
            recency_weight: Weight for recency component (default: 0.3)
            usage_weight: Weight for usage frequency component (default: 0.3)
            context_weight: Weight for context match component (default: 0.4)
        """
        # Validate weights sum to 1.0
        total_weight = recency_weight + usage_weight + context_weight
        if not math.isclose(total_weight, 1.0):
            raise ValueError(f"Weights must sum to 1.0 (got {total_weight})")

        self.recency_weight = recency_weight
        self.usage_weight = usage_weight
        self.context_weight = context_weight

    def calculate_recency_score(self, last_used: Optional[datetime]) -> float:
        """
        Score 0-1 based on recency (exponential decay).

        Scoring logic:
        - Today: 1.0
        - 1-30 days: Linear decay 1.0 → 0.5
        - 31-90 days: Slower decay 0.5 → 0.1
        - 90+ days: Floor at 0.1

        Args:
            last_used: When pattern was last used

        Returns:
            Recency score (0-1)
        """
        if last_used is None:
            return 0.5  # Default for unknown

        # Handle both datetime and string inputs
        if isinstance(last_used, str):
            try:
                last_used = datetime.fromisoformat(last_used.replace('Z', '+00:00'))
            except ValueError:
                return 0.5  # Default for parse errors

        days_ago = (datetime.now() - last_used).days

        # Fresh (today)
        if days_ago == 0:
            return 1.0

        # Recent (1-30 days): Linear decay
        elif days_ago <= 30:
            return 1.0 - (days_ago / 30) * 0.5

        # Older (31-90 days): Slower decay
        elif days_ago <= 90:
            return 0.5 - ((days_ago - 30) / 60) * 0.4

        # Very old (90+ days): Floor
        else:
            return 0.1

    def calculate_usage_score(self, use_count: Optional[int]) -> float:
        """
        Score 0-1 based on usage frequency (logarithmic).

        Scoring logic:
        - Never used: 0.3 (give it a chance)
        - 1 use: 0.5
        - 10 uses: 0.8
        - 100+ uses: 1.0

        Args:
            use_count: Number of times pattern has been used

        Returns:
            Usage score (0-1)
        """
        if use_count is None or use_count == 0:
            return 0.3  # Default for unused (give it a chance)

        # Logarithmic scale
        # log10(1) = 0 → 0.5
        # log10(10) = 1 → 0.8
        # log10(100) = 2 → 1.0
        log_score = math.log10(use_count)
        return min(1.0, 0.5 + (log_score / 2) * 0.5)

    def calculate_context_score(self, pattern_path: Path, pattern_content: str, context: ScoringContext) -> float:
        """
        Score 0-1 based on context relevance.

        Checks for matches in:
        - Agent name in path
        - Technologies in content
        - Task type in content
        - Keywords in content

        Args:
            pattern_path: Path to pattern file
            pattern_content: Pattern file content
            context: Scoring context

        Returns:
            Context score (0-1)
        """
        score = 0.5  # Baseline

        path_str = str(pattern_path).lower()
        content_lower = pattern_content.lower()

        # Agent name match (+0.3)
        if context.agent_name:
            if context.agent_name.lower() in path_str:
                score += 0.3

        # Technology matches (+0.05 each, max +0.2)
        if context.technologies:
            matches = sum(
                1 for tech in context.technologies
                if tech.lower() in content_lower
            )
            score += min(0.2, matches * 0.05)

        # Task type match (+0.2)
        if context.task_type:
            if context.task_type.lower() in content_lower:
                score += 0.2

        # Keyword matches (+0.05 each, max +0.15)
        if context.keywords:
            matches = sum(
                1 for keyword in context.keywords
                if keyword.lower() in content_lower
            )
            score += min(0.15, matches * 0.05)

        return min(1.0, score)

    def calculate_relevance(
        self,
        pattern_path: Path,
        pattern_content: str,
        metadata: Dict,
        context: ScoringContext
    ) -> float:
        """
        Calculate overall relevance score (0-1).

        Args:
            pattern_path: Path to pattern file
            pattern_content: Pattern content
            metadata: Pattern metadata (last_used, use_count)
            context: Scoring context

        Returns:
            Overall relevance score (0-1)
        """
        # Calculate component scores
        recency = self.calculate_recency_score(metadata.get("last_used"))
        usage = self.calculate_usage_score(metadata.get("use_count"))
        context_match = self.calculate_context_score(pattern_path, pattern_content, context)

        # Weighted combination
        relevance = (
            self.recency_weight * recency +
            self.usage_weight * usage +
            self.context_weight * context_match
        )

        return relevance

    def explain_score(
        self,
        pattern_path: Path,
        pattern_content: str,
        metadata: Dict,
        context: ScoringContext
    ) -> Dict:
        """
        Calculate relevance and provide detailed explanation.

        Args:
            pattern_path: Path to pattern file
            pattern_content: Pattern content
            metadata: Pattern metadata
            context: Scoring context

        Returns:
            Dictionary with overall score and component breakdown
        """
        recency = self.calculate_recency_score(metadata.get("last_used"))
        usage = self.calculate_usage_score(metadata.get("use_count"))
        context_match = self.calculate_context_score(pattern_path, pattern_content, context)

        overall = (
            self.recency_weight * recency +
            self.usage_weight * usage +
            self.context_weight * context_match
        )

        return {
            "overall_score": round(overall, 3),
            "components": {
                "recency": {
                    "score": round(recency, 3),
                    "weight": self.recency_weight,
                    "contribution": round(self.recency_weight * recency, 3),
                    "last_used": metadata.get("last_used")
                },
                "usage": {
                    "score": round(usage, 3),
                    "weight": self.usage_weight,
                    "contribution": round(self.usage_weight * usage, 3),
                    "use_count": metadata.get("use_count", 0)
                },
                "context": {
                    "score": round(context_match, 3),
                    "weight": self.context_weight,
                    "contribution": round(self.context_weight * context_match, 3),
                    "matches": {
                        "agent_name": context.agent_name if context.agent_name else None,
                        "task_type": context.task_type if context.task_type else None,
                        "technologies": context.technologies if context.technologies else [],
                        "keywords": context.keywords if context.keywords else []
                    }
                }
            },
            "pattern": {
                "path": str(pattern_path),
                "name": pattern_path.name
            }
        }


def main():
    """CLI entry point for testing"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Relevance scoring for memory patterns"
    )
    parser.add_argument("pattern_file", help="Path to pattern file")
    parser.add_argument("--agent", help="Agent name for context")
    parser.add_argument("--task-type", help="Task type for context")
    parser.add_argument("--technologies", nargs="+", help="Technologies for context")
    parser.add_argument("--keywords", nargs="+", help="Keywords for context")
    parser.add_argument("--last-used", help="Last used date (ISO format)")
    parser.add_argument("--use-count", type=int, default=0, help="Use count")

    args = parser.parse_args()

    # Load pattern
    pattern_path = Path(args.pattern_file)
    if not pattern_path.exists():
        print(f"❌ Error: Pattern file not found: {pattern_path}")
        return 1

    pattern_content = pattern_path.read_text(encoding='utf-8')

    # Build context
    context = ScoringContext(
        agent_name=args.agent,
        task_type=args.task_type,
        technologies=args.technologies or [],
        keywords=args.keywords or []
    )

    # Build metadata
    metadata = {
        "use_count": args.use_count
    }
    if args.last_used:
        metadata["last_used"] = args.last_used

    # Calculate score
    scorer = RelevanceScorer()
    explanation = scorer.explain_score(pattern_path, pattern_content, metadata, context)

    # Print results
    print("\n" + "=" * 60)
    print("RELEVANCE SCORE EXPLANATION")
    print("=" * 60)
    print(f"\nPattern: {explanation['pattern']['name']}")
    print(f"Overall Score: {explanation['overall_score']:.3f}")
    print("\nComponent Breakdown:")
    print(f"  Recency:  {explanation['components']['recency']['score']:.3f} " +
          f"(weight: {explanation['components']['recency']['weight']:.1f}) " +
          f"→ {explanation['components']['recency']['contribution']:.3f}")
    print(f"  Usage:    {explanation['components']['usage']['score']:.3f} " +
          f"(weight: {explanation['components']['usage']['weight']:.1f}) " +
          f"→ {explanation['components']['usage']['contribution']:.3f}")
    print(f"  Context:  {explanation['components']['context']['score']:.3f} " +
          f"(weight: {explanation['components']['context']['weight']:.1f}) " +
          f"→ {explanation['components']['context']['contribution']:.3f}")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
