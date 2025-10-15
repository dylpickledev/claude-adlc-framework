#!/usr/bin/env python3
"""
Promote Agent-Specific Pattern to Global Scope

Promotes high-value agent-specific patterns to global scope when they prove
useful across multiple agents.

Promotion Criteria:
- Use count ≥ 3 (used by multiple agents)
- Confidence score ≥ 0.85 (high quality)
- Manual promotion flag (user/agent discretion)

Usage:
    python scripts/promote-to-global.py specialists dbt-expert dbt-optimization-pattern.md
    python scripts/promote-to-global.py roles analytics-engineer-role data-modeling-pattern.md
    python scripts/promote-to-global.py specialists aws-expert alb-pattern.md --force
"""

from pathlib import Path
import json
import shutil
import sys
from datetime import datetime


def promote_pattern_to_global(agent_type: str, agent_name: str, pattern_name: str, force: bool = False) -> bool:
    """Promote agent-specific pattern to global scope

    Args:
        agent_type: "specialists" or "roles"
        agent_name: Name of the agent (e.g., "dbt-expert")
        pattern_name: Name of the pattern file (e.g., "dbt-optimization.md")
        force: Skip promotion criteria checks

    Returns:
        True if promoted successfully, False otherwise
    """

    base = Path(".claude/memory")
    source_dir = base / agent_type / agent_name / "patterns"
    source_pattern = source_dir / pattern_name

    # Validate source exists
    if not source_pattern.exists():
        print(f"❌ Pattern not found: {source_pattern}")
        print(f"   Available patterns in {agent_name}:")
        if source_dir.exists():
            for p in source_dir.glob("*.md"):
                print(f"     - {p.name}")
        return False

    # Check promotion criteria (unless forced)
    if not force:
        metadata_file = source_pattern.with_suffix(".metadata.json")
        if metadata_file.exists():
            metadata = json.loads(metadata_file.read_text())

            # Criteria checks
            use_count = metadata.get("use_count", 0)
            confidence = metadata.get("confidence")

            print(f"Promotion Criteria Check:")
            print(f"  Pattern: {pattern_name}")
            print(f"  Use count: {use_count} (required: ≥3)")
            if confidence is not None:
                print(f"  Confidence: {confidence} (required: ≥0.85)")
            else:
                print(f"  Confidence: Not set")

            # Validate criteria
            criteria_met = True

            if use_count < 3:
                print(f"\n⚠️  Pattern needs more usage")
                print(f"   Current: {use_count}, Required: 3")
                criteria_met = False

            if confidence is not None and confidence < 0.85:
                print(f"\n⚠️  Pattern needs higher confidence")
                print(f"   Current: {confidence}, Required: 0.85")
                criteria_met = False

            if not criteria_met:
                print(f"\n❌ Promotion criteria not met")
                print(f"   Use --force to promote anyway")
                return False

            print(f"\n✅ Promotion criteria met!")
        else:
            print(f"⚠️  No metadata file found, checking manually...")
            print(f"   Use --force to promote without criteria check")
            if not force:
                return False

    # Promote to global
    dest_dir = base / "patterns"
    dest_pattern = dest_dir / pattern_name

    # Check if already exists in global
    if dest_pattern.exists():
        print(f"\n⚠️  Pattern already exists in global scope")
        response = input(f"   Overwrite? (y/n): ")
        if response.lower() != 'y':
            print(f"❌ Promotion cancelled")
            return False

    # Copy pattern to global
    shutil.copy2(source_pattern, dest_pattern)
    print(f"\n✅ Pattern promoted to global scope")
    print(f"📍 Source: {source_pattern}")
    print(f"📍 Destination: {dest_pattern}")

    # Copy metadata
    metadata_source = source_pattern.with_suffix(".metadata.json")
    if metadata_source.exists():
        metadata_dest = dest_pattern.with_suffix(".metadata.json")

        # Update metadata with promotion info
        metadata = json.loads(metadata_source.read_text())
        metadata["promoted_from"] = f"{agent_type}/{agent_name}"
        metadata["promoted_at"] = datetime.now().isoformat()

        metadata_dest.write_text(json.dumps(metadata, indent=2))
        print(f"✅ Metadata copied and updated")

    print(f"\n📦 Pattern now available globally to all agents")
    print(f"🔗 Original remains in {agent_name} scope")

    return True


def list_promotable_patterns(agent_type: str, agent_name: str):
    """List patterns that meet promotion criteria"""

    base = Path(".claude/memory")
    source_dir = base / agent_type / agent_name / "patterns"

    if not source_dir.exists():
        print(f"❌ No patterns directory for {agent_name}")
        return

    promotable = []
    all_patterns = []

    for pattern_file in source_dir.glob("*.md"):
        metadata_file = pattern_file.with_suffix(".metadata.json")

        if metadata_file.exists():
            metadata = json.loads(metadata_file.read_text())
            use_count = metadata.get("use_count", 0)
            confidence = metadata.get("confidence")

            # Check criteria
            meets_criteria = use_count >= 3 or (confidence is not None and confidence >= 0.85)

            pattern_info = {
                "name": pattern_file.name,
                "use_count": use_count,
                "confidence": confidence,
                "meets_criteria": meets_criteria
            }

            all_patterns.append(pattern_info)
            if meets_criteria:
                promotable.append(pattern_info)

    print(f"\nPatterns in {agent_name}:")
    print("=" * 70)

    if promotable:
        print(f"\n✅ PROMOTABLE ({len(promotable)} patterns):")
        for p in sorted(promotable, key=lambda x: (x['use_count'], x['confidence'] or 0), reverse=True):
            print(f"  - {p['name'][:50]:50s} (uses: {p['use_count']}, conf: {p['confidence']})")

    non_promotable = [p for p in all_patterns if not p['meets_criteria']]
    if non_promotable:
        print(f"\n⏳ NOT YET PROMOTABLE ({len(non_promotable)} patterns):")
        for p in sorted(non_promotable, key=lambda x: (x['use_count'], x['confidence'] or 0), reverse=True):
            print(f"  - {p['name'][:50]:50s} (uses: {p['use_count']}, conf: {p['confidence']})")


def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Promote agent pattern to global scope"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Promote command
    promote_parser = subparsers.add_parser("promote", help="Promote a pattern")
    promote_parser.add_argument("agent_type", choices=["specialists", "roles"])
    promote_parser.add_argument("agent_name")
    promote_parser.add_argument("pattern_name")
    promote_parser.add_argument("--force", action="store_true", help="Skip promotion criteria checks")

    # List command
    list_parser = subparsers.add_parser("list", help="List promotable patterns")
    list_parser.add_argument("agent_type", choices=["specialists", "roles"])
    list_parser.add_argument("agent_name")

    # Default to promote if no subcommand (backward compatibility)
    if len(sys.argv) > 1 and sys.argv[1] not in ["promote", "list"]:
        sys.argv.insert(1, "promote")

    args = parser.parse_args()

    if args.command == "list":
        list_promotable_patterns(args.agent_type, args.agent_name)
        return 0
    elif args.command == "promote":
        success = promote_pattern_to_global(
            args.agent_type,
            args.agent_name,
            args.pattern_name,
            force=args.force
        )
        return 0 if success else 1
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
