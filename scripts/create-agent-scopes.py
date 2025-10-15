#!/usr/bin/env python3
"""
Create Agent-Specific Memory Scope Directories

Creates the directory structure for agent-specific memory scopes to enable
context reduction by loading only relevant patterns per agent.

Usage:
    python scripts/create-agent-scopes.py
    python scripts/create-agent-scopes.py --dry-run
"""

from pathlib import Path
import sys

def create_agent_scope_structure(dry_run: bool = False):
    """Create directory structure for agent-specific memory scopes"""

    base = Path(".claude/memory")

    # Specialist agents (from .claude/agents/specialists/)
    specialists = [
        "aws-expert",
        "dbt-expert",
        "snowflake-expert",
        "tableau-expert",
        "dlthub-expert",
        "orchestra-expert",
        "prefect-expert",
        "react-expert",
        "streamlit-expert",
        "documentation-expert",
        "github-sleuth-expert",
        "business-context",
        "data-quality-specialist",
        "cost-optimization-specialist",
        "ui-ux-expert",
        "project-delivery-expert",
    ]

    # Role agents (from .claude/agents/roles/)
    roles = [
        "analytics-engineer-role",
        "data-engineer-role",
        "bi-developer-role",
        "ui-ux-developer-role",
        "data-architect-role",
        "business-analyst-role",
        "qa-engineer-role",
        "project-manager-role",
        "dba-role",
        "research-role",
    ]

    created_count = 0

    # Create specialist directories
    print("Creating specialist memory scopes...")
    for specialist in specialists:
        specialist_dir = base / "specialists" / specialist
        for tier in ["recent", "intermediate", "patterns", "archive"]:
            tier_dir = specialist_dir / tier

            if dry_run:
                print(f"[DRY RUN] Would create: {tier_dir}")
            else:
                tier_dir.mkdir(parents=True, exist_ok=True)
                print(f"✅ Created: {tier_dir}")

            created_count += 1

    # Create role directories
    print("\nCreating role memory scopes...")
    for role in roles:
        role_dir = base / "roles" / role
        for tier in ["recent", "intermediate", "patterns", "archive"]:
            tier_dir = role_dir / tier

            if dry_run:
                print(f"[DRY RUN] Would create: {tier_dir}")
            else:
                tier_dir.mkdir(parents=True, exist_ok=True)
                print(f"✅ Created: {tier_dir}")

            created_count += 1

    # Summary
    print(f"\n{'[DRY RUN] ' if dry_run else ''}Summary:")
    print(f"✅ {'Would create' if dry_run else 'Created'} {len(specialists)} specialist scopes ({len(specialists) * 4} directories)")
    print(f"✅ {'Would create' if dry_run else 'Created'} {len(roles)} role scopes ({len(roles) * 4} directories)")
    print(f"✅ Total: {created_count} directories")

    if not dry_run:
        print(f"\n📍 Base directory: {base.absolute()}")
        print(f"📁 specialists/: Agent-specific memory for 16 specialists")
        print(f"📁 roles/: Agent-specific memory for 10 roles")


def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Create agent-specific memory scope directories"
    )
    parser.add_argument("--dry-run", action="store_true", help="Show what would be created without creating")

    args = parser.parse_args()

    create_agent_scope_structure(dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main() if main() is not None else 0)
