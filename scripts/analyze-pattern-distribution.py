#!/usr/bin/env python3
"""
Analyze Pattern Distribution Across Agents

Analyzes which patterns should belong to which agents based on content keywords.
This informs the migration strategy for Phase 4 agent-specific memory scopes.

Usage:
    python scripts/analyze-pattern-distribution.py
    python scripts/analyze-pattern-distribution.py --min-relevance 3
"""

from pathlib import Path
import json
from collections import defaultdict
import sys

# Technology/tool keywords for each agent
AGENT_KEYWORDS = {
    # Specialists
    "dbt-expert": ["dbt", "sql", "model", "test", "macro", "jinja", "manifest", "run", "seed", "snapshot"],
    "snowflake-expert": ["snowflake", "warehouse", "database", "query", "performance", "compute", "storage", "clustering"],
    "aws-expert": ["aws", "ec2", "s3", "lambda", "ecs", "cloudformation", "alb", "vpc", "iam", "cloudwatch"],
    "tableau-expert": ["tableau", "dashboard", "visualization", "workbook", "viz", "calculated field", "parameter"],
    "github-sleuth-expert": ["github", "repository", "pr", "pull request", "issue", "commit", "branch", "merge"],
    "react-expert": ["react", "jsx", "component", "state", "hook", "usestate", "useeffect", "props"],
    "streamlit-expert": ["streamlit", "st.", "app.py", "st.write", "st.button", "st.dataframe"],
    "orchestra-expert": ["orchestra", "pipeline", "workflow", "dag", "task", "dependency", "schedule"],
    "prefect-expert": ["prefect", "flow", "task", "@flow", "@task", "deployment", "work pool"],
    "dlthub-expert": ["dlt", "dlthub", "source", "destination", "pipeline", "extract", "load"],
    "documentation-expert": ["documentation", "readme", "guide", "tutorial", "markdown", "confluence"],
    "business-context": ["business", "stakeholder", "requirement", "metric", "kpi", "report"],
    "data-quality-specialist": ["quality", "validation", "test", "check", "data quality", "accuracy"],
    "cost-optimization-specialist": ["cost", "optimization", "budget", "pricing", "savings", "efficiency"],
    "ui-ux-expert": ["ui", "ux", "design", "user experience", "interface", "usability"],
    "project-delivery-expert": ["project", "delivery", "milestone", "uat", "deployment", "stakeholder"],

    # Roles
    "analytics-engineer-role": ["analytics", "dbt", "sql", "data model", "transformation", "metrics"],
    "data-engineer-role": ["pipeline", "etl", "ingestion", "orchestration", "data flow"],
    "bi-developer-role": ["bi", "business intelligence", "tableau", "dashboard", "report"],
    "ui-ux-developer-role": ["react", "streamlit", "app", "interface", "frontend"],
    "data-architect-role": ["architecture", "design", "platform", "infrastructure", "integration"],
    "business-analyst-role": ["business", "requirement", "analysis", "stakeholder", "scope"],
    "qa-engineer-role": ["testing", "qa", "quality", "validation", "test case"],
    "project-manager-role": ["project", "plan", "schedule", "risk", "delivery", "coordination"],
    "dba-role": ["database", "admin", "backup", "recovery", "performance tuning"],
    "research-role": ["research", "analysis", "investigation", "findings", "recommendation"],
}


def analyze_pattern_distribution(min_relevance: int = 1):
    """Analyze which patterns should belong to which agents"""

    patterns_dir = Path(".claude/memory/patterns")
    results = defaultdict(list)

    # Scan all pattern files
    pattern_files = list(patterns_dir.glob("**/*.md"))

    print(f"Analyzing {len(pattern_files)} patterns...")
    print()

    for pattern_file in pattern_files:
        if not pattern_file.is_file():
            continue

        try:
            content = pattern_file.read_text(encoding='utf-8').lower()
        except Exception as e:
            print(f"⚠️  Error reading {pattern_file.name}: {e}")
            continue

        # Check which agents this pattern is relevant to
        for agent, keywords in AGENT_KEYWORDS.items():
            relevance_score = sum(1 for kw in keywords if kw in content)

            if relevance_score >= min_relevance:
                results[agent].append({
                    "pattern": pattern_file.name,
                    "relevance_score": relevance_score,
                    "matched_keywords": [kw for kw in keywords if kw in content],
                    "path": str(pattern_file.relative_to(Path(".claude/memory")))
                })

    # Sort results by relevance score (highest first)
    for agent in results:
        results[agent] = sorted(results[agent], key=lambda x: x["relevance_score"], reverse=True)

    # Save analysis results
    output = Path("projects/active/ai-memory-system-improvements/tasks/pattern-distribution.json")
    output.write_text(json.dumps(results, indent=2))

    # Print summary
    print("=" * 70)
    print("PATTERN DISTRIBUTION ANALYSIS")
    print("=" * 70)
    print(f"Minimum relevance threshold: {min_relevance}")
    print(f"Total patterns analyzed: {len(pattern_files)}")
    print()

    # Summary by agent
    specialist_total = 0
    role_total = 0

    print("SPECIALISTS:")
    for agent in sorted(AGENT_KEYWORDS.keys()):
        if "role" not in agent and agent in results:
            count = len(results[agent])
            specialist_total += count
            top_score = results[agent][0]["relevance_score"] if results[agent] else 0
            print(f"  {agent:30s}: {count:2d} patterns (top score: {top_score})")

    print()
    print("ROLES:")
    for agent in sorted(AGENT_KEYWORDS.keys()):
        if "role" in agent and agent in results:
            count = len(results[agent])
            role_total += count
            top_score = results[agent][0]["relevance_score"] if results[agent] else 0
            print(f"  {agent:30s}: {count:2d} patterns (top score: {top_score})")

    print()
    print("=" * 70)
    print(f"Total specialist patterns: {specialist_total}")
    print(f"Total role patterns: {role_total}")
    print(f"\n✅ Analysis saved to: {output}")

    # Top patterns per agent (detailed view)
    print()
    print("=" * 70)
    print("TOP PATTERNS PER AGENT (Top 3)")
    print("=" * 70)

    for agent in sorted(results.keys()):
        if results[agent]:
            print(f"\n{agent}:")
            for i, pattern_info in enumerate(results[agent][:3], 1):
                score = pattern_info["relevance_score"]
                pattern = pattern_info["pattern"]
                keywords = ", ".join(pattern_info["matched_keywords"][:5])
                print(f"  {i}. {pattern} (score: {score})")
                print(f"     Keywords: {keywords}...")

    return results


def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Analyze pattern distribution across agents"
    )
    parser.add_argument("--min-relevance", type=int, default=1,
                        help="Minimum relevance score (default: 1)")

    args = parser.parse_args()

    analyze_pattern_distribution(min_relevance=args.min_relevance)


if __name__ == "__main__":
    sys.exit(main() if main() is not None else 0)
