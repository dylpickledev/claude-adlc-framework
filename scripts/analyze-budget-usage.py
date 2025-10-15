#!/usr/bin/env python3
"""
Budget Usage Analytics

Analyzes budget usage logs to identify patterns, exceedances, and optimization
opportunities. Generates recommendations for profile adjustments.

Usage:
    python scripts/analyze-budget-usage.py                    # Full analysis
    python scripts/analyze-budget-usage.py --agent dbt-expert  # Specific agent
    python scripts/analyze-budget-usage.py --days 7            # Last 7 days
    python scripts/analyze-budget-usage.py --recommendations   # Show recommendations only
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from collections import defaultdict
import statistics


class BudgetUsageAnalyzer:
    """Analyze budget usage patterns and generate recommendations"""

    def __init__(self, log_file: Path = None, profiles_file: Path = None):
        """Initialize analyzer

        Args:
            log_file: Path to budget usage JSONL log
            profiles_file: Path to budget profiles configuration
        """
        if log_file is None:
            log_file = Path(".claude/cache/budget-usage.jsonl")

        if profiles_file is None:
            profiles_file = Path(".claude/memory/budget-profiles.json")

        self.log_file = log_file
        self.profiles_file = profiles_file

        # Load profiles config
        if self.profiles_file.exists():
            self.config = json.loads(self.profiles_file.read_text())
            self.tuning_params = self.config.get("tuning_parameters", {})
        else:
            self.config = {}
            self.tuning_params = {}

    def load_usage_data(
        self,
        days: int = None,
        agent_filter: str = None
    ) -> List[Dict]:
        """Load budget usage data from JSONL log

        Args:
            days: Only load data from last N days (None = all data)
            agent_filter: Filter to specific agent (None = all agents)

        Returns:
            List of usage log entries
        """
        if not self.log_file.exists():
            return []

        data = []
        cutoff_date = None

        if days:
            cutoff_date = datetime.now() - timedelta(days=days)

        with open(self.log_file, "r") as f:
            for line in f:
                try:
                    entry = json.loads(line)

                    # Date filter
                    if cutoff_date:
                        entry_date = datetime.fromisoformat(entry["timestamp"])
                        if entry_date < cutoff_date:
                            continue

                    # Agent filter
                    if agent_filter:
                        agent_name = entry["agent"]
                        if agent_filter not in agent_name:
                            continue

                    data.append(entry)

                except json.JSONDecodeError:
                    continue

        return data

    def analyze_agent_usage(self, agent_name: str, data: List[Dict]) -> Dict:
        """Analyze usage patterns for a specific agent

        Returns:
            {
                "agent": str,
                "total_executions": int,
                "avg_usage_pct": float,
                "max_usage_pct": float,
                "exceedance_count": int,
                "exceedance_rate": float,
                "complexity_breakdown": dict,
                "scope_distribution": dict
            }
        """
        agent_data = [e for e in data if e["agent"] == agent_name]

        if not agent_data:
            return None

        usage_pcts = [e["usage_pct"] for e in agent_data]
        exceedances = [e for e in agent_data if e["exceeded_budget"]]

        # Complexity breakdown
        complexity_counts = defaultdict(int)
        complexity_usage = defaultdict(list)

        for entry in agent_data:
            complexity = entry.get("complexity", "unknown")
            complexity_counts[complexity] += 1
            complexity_usage[complexity].append(entry["usage_pct"])

        # Scope distribution (average across all executions)
        scope_totals = defaultdict(float)
        scope_counts = defaultdict(int)

        for entry in agent_data:
            scope_breakdown = entry.get("scope_breakdown", {})
            total_tokens = entry.get("tokens_loaded", 0)

            if total_tokens > 0:
                for scope, tokens in scope_breakdown.items():
                    scope_pct = (tokens / total_tokens) * 100
                    scope_totals[scope] += scope_pct
                    scope_counts[scope] += 1

        scope_distribution = {
            scope: scope_totals[scope] / scope_counts[scope]
            for scope in scope_totals
            if scope_counts[scope] > 0
        }

        return {
            "agent": agent_name,
            "total_executions": len(agent_data),
            "avg_usage_pct": statistics.mean(usage_pcts) if usage_pcts else 0,
            "median_usage_pct": statistics.median(usage_pcts) if usage_pcts else 0,
            "max_usage_pct": max(usage_pcts) if usage_pcts else 0,
            "min_usage_pct": min(usage_pcts) if usage_pcts else 0,
            "exceedance_count": len(exceedances),
            "exceedance_rate": len(exceedances) / len(agent_data) if agent_data else 0,
            "complexity_breakdown": dict(complexity_counts),
            "complexity_avg_usage": {
                c: statistics.mean(usage) for c, usage in complexity_usage.items()
            },
            "scope_distribution": scope_distribution
        }

    def generate_recommendations(self, data: List[Dict]) -> List[Dict]:
        """Generate profile adjustment recommendations

        Returns list of recommendations:
        [
            {
                "agent": str,
                "current_profile": str,
                "recommended_action": str (upgrade|downgrade|adjust_weights|maintain),
                "reason": str,
                "confidence": float,
                "details": dict
            }
        ]
        """
        recommendations = []

        # Get thresholds from config
        exceedance_threshold = self.tuning_params.get("exceedance_threshold_for_upgrade", 0.2)
        underutilization_threshold = self.tuning_params.get("underutilization_threshold_for_downgrade", 0.5)
        min_samples = self.tuning_params.get("minimum_samples_for_recommendation", 10)
        min_confidence = self.tuning_params.get("recommendation_confidence_threshold", 0.7)

        # Group data by agent
        agents = set(e["agent"] for e in data)

        for agent_name in sorted(agents):
            analysis = self.analyze_agent_usage(agent_name, data)

            if not analysis or analysis["total_executions"] < min_samples:
                continue  # Not enough data

            # Get current profile
            assignments = self.config.get("agent_assignments", {})
            current_profile = assignments.get(agent_name, "unknown")

            # Check for exceedance (upgrade needed)
            if analysis["exceedance_rate"] > exceedance_threshold:
                confidence = min(0.7 + (analysis["exceedance_rate"] - exceedance_threshold), 1.0)

                if confidence >= min_confidence:
                    recommendations.append({
                        "agent": agent_name,
                        "current_profile": current_profile,
                        "recommended_action": "upgrade",
                        "reason": f"Budget exceeded in {analysis['exceedance_count']}/{analysis['total_executions']} "
                                  f"executions ({analysis['exceedance_rate']:.1%} exceedance rate)",
                        "confidence": confidence,
                        "details": {
                            "avg_usage_pct": analysis["avg_usage_pct"],
                            "max_usage_pct": analysis["max_usage_pct"],
                            "exceedance_rate": analysis["exceedance_rate"]
                        }
                    })

            # Check for underutilization (downgrade possible)
            elif analysis["avg_usage_pct"] < (underutilization_threshold * 100):
                confidence = min(0.6 + (underutilization_threshold - analysis["avg_usage_pct"]/100), 0.9)

                if confidence >= min_confidence:
                    recommendations.append({
                        "agent": agent_name,
                        "current_profile": current_profile,
                        "recommended_action": "downgrade",
                        "reason": f"Low average usage ({analysis['avg_usage_pct']:.1f}% of budget)",
                        "confidence": confidence,
                        "details": {
                            "avg_usage_pct": analysis["avg_usage_pct"],
                            "max_usage_pct": analysis["max_usage_pct"],
                            "potential_savings": f"{100 - analysis['avg_usage_pct']:.1f}%"
                        }
                    })

            # Check scope distribution vs profile weights
            else:
                scope_dist = analysis.get("scope_distribution", {})
                profiles = self.config.get("profiles", {})
                profile_config = profiles.get(current_profile, {})
                profile_weights = profile_config.get("scope_weights", {})

                # Compare actual vs expected
                weight_diffs = {}
                for scope, expected_pct in profile_weights.items():
                    actual_pct = scope_dist.get(scope, 0) / 100
                    diff = abs(actual_pct - expected_pct)
                    if diff > 0.1:  # >10% difference
                        weight_diffs[scope] = {
                            "expected": expected_pct,
                            "actual": actual_pct,
                            "diff": diff
                        }

                if weight_diffs:
                    confidence = min(0.6 + (len(weight_diffs) * 0.1), 0.85)

                    if confidence >= min_confidence:
                        recommendations.append({
                            "agent": agent_name,
                            "current_profile": current_profile,
                            "recommended_action": "adjust_weights",
                            "reason": f"Scope usage differs from profile ({len(weight_diffs)} scopes)",
                            "confidence": confidence,
                            "details": {
                                "scope_differences": weight_diffs,
                                "current_weights": profile_weights,
                                "actual_distribution": {k: v/100 for k, v in scope_dist.items()}
                            }
                        })

        # Sort by confidence
        recommendations.sort(key=lambda x: x["confidence"], reverse=True)

        return recommendations

    def print_analysis(self, data: List[Dict], agent_filter: str = None):
        """Print comprehensive analysis report"""
        print("\n" + "=" * 70)
        print("BUDGET USAGE ANALYSIS")
        print("=" * 70)

        if not data:
            print("\n❌ No usage data found")
            return

        print(f"\nTotal Executions: {len(data)}")
        print(f"Date Range: {data[0]['timestamp']} to {data[-1]['timestamp']}")

        # Overall stats
        all_usage_pcts = [e["usage_pct"] for e in data]
        exceedances = [e for e in data if e["exceeded_budget"]]

        print(f"\nOverall Usage:")
        print(f"  Average: {statistics.mean(all_usage_pcts):.1f}%")
        print(f"  Median:  {statistics.median(all_usage_pcts):.1f}%")
        print(f"  Max:     {max(all_usage_pcts):.1f}%")
        print(f"  Min:     {min(all_usage_pcts):.1f}%")
        print(f"\nExceedances: {len(exceedances)} ({len(exceedances)/len(data):.1%})")

        # Per-agent breakdown
        agents = set(e["agent"] for e in data)

        print(f"\n{'Agent':<40s} {'Execs':>7s} {'Avg %':>8s} {'Max %':>8s} {'Exceed':>7s}")
        print("-" * 70)

        for agent_name in sorted(agents):
            if agent_filter and agent_filter not in agent_name:
                continue

            analysis = self.analyze_agent_usage(agent_name, data)

            if analysis:
                agent_short = agent_name.split("/")[-1][:38]
                print(f"{agent_short:<40s} "
                      f"{analysis['total_executions']:>7d} "
                      f"{analysis['avg_usage_pct']:>7.1f}% "
                      f"{analysis['max_usage_pct']:>7.1f}% "
                      f"{analysis['exceedance_count']:>7d}")

        print("=" * 70)

    def print_recommendations(self, recommendations: List[Dict]):
        """Print profile adjustment recommendations"""
        print("\n" + "=" * 70)
        print("BUDGET PROFILE RECOMMENDATIONS")
        print("=" * 70)

        if not recommendations:
            print("\n✅ No profile adjustments recommended at this time")
            return

        print(f"\nFound {len(recommendations)} recommendations:\n")

        for i, rec in enumerate(recommendations, 1):
            agent_short = rec["agent"].split("/")[-1]

            print(f"{i:2d}. {agent_short}")
            print(f"    Current Profile: {rec['current_profile']}")
            print(f"    Recommendation: {rec['recommended_action'].upper()}")
            print(f"    Confidence: {rec['confidence']:.0%}")
            print(f"    Reason: {rec['reason']}")

            if rec["recommended_action"] == "adjust_weights":
                scope_diffs = rec["details"].get("scope_differences", {})
                if scope_diffs:
                    print(f"    Scope Weight Differences:")
                    for scope, diff_info in scope_diffs.items():
                        print(f"      {scope:20s}: Expected {diff_info['expected']:.1%}, "
                              f"Actual {diff_info['actual']:.1%}")

            print()

        print("=" * 70)


def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Analyze budget usage patterns and generate recommendations"
    )
    parser.add_argument("--agent", help="Filter to specific agent")
    parser.add_argument("--days", type=int, help="Only analyze last N days")
    parser.add_argument("--recommendations", action="store_true",
                        help="Show recommendations only")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON")

    args = parser.parse_args()

    analyzer = BudgetUsageAnalyzer()

    # Load data
    data = analyzer.load_usage_data(days=args.days, agent_filter=args.agent)

    if not data:
        print("\n❌ No usage data found", file=sys.stderr)
        print("\nTip: Usage data is logged by BudgetMonitor during agent execution")
        print("Log file: .claude/cache/budget-usage.jsonl")
        return 1

    # Generate recommendations
    recommendations = analyzer.generate_recommendations(data)

    if args.json:
        # JSON output
        output = {
            "total_executions": len(data),
            "date_range": {
                "start": data[0]["timestamp"],
                "end": data[-1]["timestamp"]
            },
            "recommendations": recommendations
        }
        print(json.dumps(output, indent=2))

    elif args.recommendations:
        # Recommendations only
        analyzer.print_recommendations(recommendations)

    else:
        # Full analysis
        analyzer.print_analysis(data, agent_filter=args.agent)
        analyzer.print_recommendations(recommendations)

    return 0


if __name__ == "__main__":
    sys.exit(main())
