#!/usr/bin/env python3
"""
Agent Budget Calculator

Calculates memory budget for agents based on their profile and task complexity.

Profiles:
- specialist-narrow: 20-50K tokens (single-tool specialists)
- specialist-broad: 35-75K tokens (cross-tool specialists)
- role-coordinator: 50-100K tokens (role agents)
- role-architect: 75-150K tokens (strategic architects)

Complexity Tiers:
- simple: 0.5x base budget (single query, specific question)
- medium: 1.0x base budget (standard analysis, default)
- complex: 1.5x base budget (multi-step workflow)
- multi-system: 2.0x base budget (cross-system coordination)

Usage:
    python scripts/calculate-agent-budget.py <agent_name> [complexity]
    python scripts/calculate-agent-budget.py specialists/dbt-expert medium
    python scripts/calculate-agent-budget.py roles/data-architect-role complex
    python scripts/calculate-agent-budget.py --list-profiles
    python scripts/calculate-agent-budget.py --show-assignments
"""

import json
import sys
from pathlib import Path
from typing import Dict, Tuple, Optional


class AgentBudgetCalculator:
    """Calculate memory budgets for agents based on profiles and complexity"""

    def __init__(self, profiles_path: Optional[Path] = None):
        """Initialize calculator with budget profiles"""
        if profiles_path is None:
            profiles_path = Path(".claude/memory/budget-profiles.json")

        self.profiles_path = profiles_path
        self.config = self._load_profiles()

    def _load_profiles(self) -> Dict:
        """Load budget profiles configuration"""
        if not self.profiles_path.exists():
            raise FileNotFoundError(
                f"Budget profiles not found: {self.profiles_path}\n"
                f"Run Phase 6 setup to create budget-profiles.json"
            )

        return json.loads(self.profiles_path.read_text())

    def get_agent_profile(self, agent_name: str) -> Tuple[str, Dict]:
        """Get profile configuration for an agent

        Args:
            agent_name: Agent identifier (e.g., "specialists/dbt-expert")

        Returns:
            (profile_name, profile_config) tuple

        Raises:
            ValueError: If agent not found in assignments
        """
        assignments = self.config.get("agent_assignments", {})

        if agent_name not in assignments:
            # Try fuzzy matching
            if "/" not in agent_name:
                # Try both specialists/ and roles/ prefixes
                for prefix in ["specialists", "roles"]:
                    full_name = f"{prefix}/{agent_name}"
                    if full_name in assignments:
                        agent_name = full_name
                        break

            if agent_name not in assignments:
                raise ValueError(
                    f"Agent '{agent_name}' not found in budget profile assignments.\n"
                    f"Use --show-assignments to see all assigned agents."
                )

        profile_name = assignments[agent_name]
        profiles = self.config.get("profiles", {})

        if profile_name not in profiles:
            raise ValueError(f"Profile '{profile_name}' not found in configuration")

        return profile_name, profiles[profile_name]

    def calculate_budget(
        self,
        agent_name: str,
        complexity: str = "medium"
    ) -> Dict:
        """Calculate memory budget for agent

        Args:
            agent_name: Agent identifier (e.g., "specialists/dbt-expert")
            complexity: Task complexity tier (simple, medium, complex, multi-system)

        Returns:
            Budget calculation details:
            {
                "agent": str,
                "profile_name": str,
                "profile_description": str,
                "complexity": str,
                "base_budget": int,
                "max_budget": int,
                "multiplier": float,
                "calculated_budget": int,
                "scope_weights": dict
            }
        """
        # Get agent's profile
        profile_name, profile_config = self.get_agent_profile(agent_name)

        # Get complexity multiplier
        complexity_multipliers = self.config.get("complexity_multipliers", {})

        if complexity not in complexity_multipliers:
            raise ValueError(
                f"Invalid complexity '{complexity}'. "
                f"Valid options: {', '.join(complexity_multipliers.keys())}"
            )

        complexity_config = complexity_multipliers[complexity]
        multiplier = complexity_config["multiplier"]

        # Calculate budget
        base_budget = profile_config["base_budget"]
        max_budget = profile_config["max_budget"]
        calculated_budget = int(base_budget * multiplier)

        # Cap at max budget
        calculated_budget = min(calculated_budget, max_budget)

        return {
            "agent": agent_name,
            "profile_name": profile_name,
            "profile_description": profile_config["description"],
            "complexity": complexity,
            "complexity_description": complexity_config["description"],
            "base_budget": base_budget,
            "max_budget": max_budget,
            "multiplier": multiplier,
            "calculated_budget": calculated_budget,
            "capped": calculated_budget >= max_budget,
            "scope_weights": profile_config["scope_weights"]
        }

    def list_profiles(self):
        """List all available budget profiles"""
        print("\n" + "=" * 70)
        print("AVAILABLE BUDGET PROFILES")
        print("=" * 70)

        profiles = self.config.get("profiles", {})

        for profile_name, profile_config in profiles.items():
            print(f"\n{profile_name.upper()}")
            print(f"  Description: {profile_config['description']}")
            print(f"  Base Budget: {profile_config['base_budget']:,} tokens")
            print(f"  Max Budget:  {profile_config['max_budget']:,} tokens")
            print(f"  Scope Weights:")
            for scope, weight in profile_config['scope_weights'].items():
                print(f"    - {scope:20s}: {weight:.1%}")

            if "examples" in profile_config:
                print(f"  Examples: {', '.join(profile_config['examples'])}")

        print("\n" + "=" * 70)

    def show_assignments(self):
        """Show all agent profile assignments"""
        print("\n" + "=" * 70)
        print("AGENT PROFILE ASSIGNMENTS")
        print("=" * 70)

        assignments = self.config.get("agent_assignments", {})
        profiles = self.config.get("profiles", {})

        # Group by profile
        by_profile = {}
        for agent_name, profile_name in assignments.items():
            if profile_name not in by_profile:
                by_profile[profile_name] = []
            by_profile[profile_name].append(agent_name)

        for profile_name in sorted(by_profile.keys()):
            profile_config = profiles.get(profile_name, {})
            agents = sorted(by_profile[profile_name])

            print(f"\n{profile_name.upper()} ({len(agents)} agents)")
            print(f"  Budget: {profile_config.get('base_budget', 0):,} - "
                  f"{profile_config.get('max_budget', 0):,} tokens")

            for agent in agents:
                agent_type = agent.split("/")[0]
                agent_short = agent.split("/")[1]
                print(f"  - {agent_short:40s} ({agent_type})")

        print("\n" + "=" * 70)
        print(f"\nTotal agents: {len(assignments)}")

    def show_complexity_tiers(self):
        """Show all complexity tiers and examples"""
        print("\n" + "=" * 70)
        print("TASK COMPLEXITY TIERS")
        print("=" * 70)

        complexity_multipliers = self.config.get("complexity_multipliers", {})

        tier_order = ["simple", "medium", "complex", "multi-system"]

        for tier in tier_order:
            if tier not in complexity_multipliers:
                continue

            config = complexity_multipliers[tier]
            print(f"\n{tier.upper()} (×{config['multiplier']:.1f})")
            print(f"  {config['description']}")

            if "examples" in config:
                print(f"  Examples:")
                for example in config["examples"]:
                    print(f"    - {example}")

        print("\n" + "=" * 70)


def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Calculate memory budget for agents based on profiles and complexity"
    )
    parser.add_argument("agent", nargs="?",
                        help="Agent name (e.g., specialists/dbt-expert)")
    parser.add_argument("complexity", nargs="?", default="medium",
                        help="Task complexity (simple, medium, complex, multi-system)")
    parser.add_argument("--list-profiles", action="store_true",
                        help="List all available budget profiles")
    parser.add_argument("--show-assignments", action="store_true",
                        help="Show all agent profile assignments")
    parser.add_argument("--show-complexity", action="store_true",
                        help="Show all complexity tiers")
    parser.add_argument("--json", action="store_true",
                        help="Output results as JSON")

    args = parser.parse_args()

    try:
        calculator = AgentBudgetCalculator()

        # List profiles
        if args.list_profiles:
            calculator.list_profiles()
            return 0

        # Show assignments
        if args.show_assignments:
            calculator.show_assignments()
            return 0

        # Show complexity
        if args.show_complexity:
            calculator.show_complexity_tiers()
            return 0

        # Calculate budget for agent
        if not args.agent:
            parser.print_help()
            return 1

        result = calculator.calculate_budget(args.agent, args.complexity)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            # Pretty print
            print("\n" + "=" * 70)
            print("AGENT BUDGET CALCULATION")
            print("=" * 70)
            print(f"\nAgent:      {result['agent']}")
            print(f"Profile:    {result['profile_name']}")
            print(f"            {result['profile_description']}")
            print(f"\nComplexity: {result['complexity']} (×{result['multiplier']:.1f})")
            print(f"            {result['complexity_description']}")
            print(f"\nBase Budget:       {result['base_budget']:,} tokens")
            print(f"Multiplier:        ×{result['multiplier']:.1f}")
            print(f"Calculated Budget: {result['calculated_budget']:,} tokens")
            print(f"Max Budget:        {result['max_budget']:,} tokens")

            if result['capped']:
                print(f"\n⚠️  Budget capped at maximum ({result['max_budget']:,} tokens)")

            print(f"\nScope Weights:")
            for scope, weight in result['scope_weights'].items():
                tokens = int(result['calculated_budget'] * weight)
                print(f"  {scope:20s}: {weight:5.1%} ({tokens:,} tokens)")

            print("=" * 70)

        return 0

    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
