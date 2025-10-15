#!/usr/bin/env python3
"""
Migrate Patterns to Agent-Specific Scopes

Migrates patterns from global directory to agent-specific scopes based on
relevance analysis. Preserves originals in global directory for backward compatibility.

Usage:
    python scripts/migrate-patterns-to-scopes.py
    python scripts/migrate-patterns-to-scopes.py --min-score 3
    python scripts/migrate-patterns-to-scopes.py --dry-run
"""

from pathlib import Path
import json
import shutil
import sys


def migrate_patterns_to_scopes(min_score: int = 3, dry_run: bool = False):
    """Migrate patterns to agent-specific scopes based on analysis"""

    # Load distribution analysis
    analysis_file = Path("projects/active/ai-memory-system-improvements/tasks/pattern-distribution.json")
    if not analysis_file.exists():
        print("❌ Pattern distribution analysis not found!")
        print("   Run: python scripts/analyze-pattern-distribution.py")
        return False

    distribution = json.loads(analysis_file.read_text())

    base = Path(".claude/memory")
    migrated_count = 0
    total_copies = 0

    print("=" * 70)
    print("PATTERN MIGRATION TO AGENT SCOPES")
    print("=" * 70)
    print(f"Minimum relevance score: {min_score}")
    print(f"Dry run: {dry_run}")
    print()

    for agent, patterns in sorted(distribution.items()):
        # Determine agent type (specialist vs role)
        if "role" in agent:
            agent_type = "roles"
        else:
            agent_type = "specialists"

        agent_migrated = 0

        for pattern_info in patterns:
            # Only migrate high-relevance patterns
            if pattern_info["relevance_score"] < min_score:
                continue

            # Construct source path
            source_path = base / pattern_info["path"]

            if not source_path.exists():
                print(f"⚠️  Source not found: {source_path}")
                continue

            # Construct destination path
            dest_dir = base / agent_type / agent / "patterns"
            dest_path = dest_dir / source_path.name

            if dry_run:
                print(f"[DRY RUN] Would migrate: {source_path.name} → {agent} (score: {pattern_info['relevance_score']})")
            else:
                # Create destination directory
                dest_dir.mkdir(parents=True, exist_ok=True)

                # Copy pattern
                shutil.copy2(source_path, dest_path)

                # Copy metadata if exists
                metadata_source = source_path.with_suffix(".metadata.json")
                if metadata_source.exists():
                    metadata_dest = dest_path.with_suffix(".metadata.json")
                    shutil.copy2(metadata_source, metadata_dest)

                print(f"✅ {source_path.name[:45]:45s} → {agent:30s} (score: {pattern_info['relevance_score']})")

            agent_migrated += 1
            total_copies += 1

        if agent_migrated > 0:
            migrated_count += 1

    print()
    print("=" * 70)
    print("MIGRATION SUMMARY")
    print("=" * 70)
    print(f"{'Would migrate' if dry_run else 'Migrated'} to {migrated_count} agents")
    print(f"Total pattern copies: {total_copies}")
    print(f"\n{'[DRY RUN] ' if dry_run else ''}Original patterns preserved in global directory")

    if not dry_run:
        print("\n✅ Migration complete!")
        print("📍 Agent-specific patterns: .claude/memory/{specialists,roles}/*/patterns/")
        print("📦 Global patterns: .claude/memory/patterns/ (unchanged)")

    return True


def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Migrate patterns to agent-specific scopes"
    )
    parser.add_argument("--min-score", type=int, default=3,
                        help="Minimum relevance score for migration (default: 3)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be migrated without migrating")

    args = parser.parse_args()

    success = migrate_patterns_to_scopes(
        min_score=args.min_score,
        dry_run=args.dry_run
    )

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
