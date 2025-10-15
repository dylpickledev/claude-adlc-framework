#!/usr/bin/env python3
"""
One-Time Migration Script: Move Existing Patterns to Three-Tier Structure

Migrates patterns from flat .claude/memory/patterns/ structure to
hierarchical recent/ → intermediate/ → patterns/ structure based on
age, usage, and confidence.

Migration Logic:
- Age <30 days → recent/ (full detail)
- Confidence ≥0.85 OR use_count ≥3 → patterns/ (permanent)
- Everything else → intermediate/ (summarized)

Usage:
    python scripts/migrate-to-tiers.py                  # Run migration
    python scripts/migrate-to-tiers.py --dry-run        # Preview only
    python scripts/migrate-to-tiers.py --backup         # Backup first
"""

from pathlib import Path
import json
import shutil
from datetime import datetime
from typing import Dict, List
import sys

# Import utilities
import importlib.util
script_dir = Path(__file__).parent

# Load summarizer
spec = importlib.util.spec_from_file_location("summarize_patterns", script_dir / "summarize-patterns.py")
summarize_patterns = importlib.util.module_from_spec(spec)
spec.loader.exec_module(summarize_patterns)
PatternSummarizer = summarize_patterns.PatternSummarizer


def days_since_timestamp(timestamp: float) -> int:
    """Calculate days since a Unix timestamp"""
    date = datetime.fromtimestamp(timestamp)
    return (datetime.now() - date).days


class PatternMigrator:
    """Migrates existing patterns to three-tier structure"""

    def __init__(self, base_dir: Path = None):
        """
        Initialize migrator.

        Args:
            base_dir: Base memory directory (default: .claude/memory)
        """
        self.base_dir = base_dir or Path(".claude/memory")
        self.patterns_dir = self.base_dir / "patterns"
        self.recent_dir = self.base_dir / "recent"
        self.intermediate_dir = self.base_dir / "intermediate"
        self.patterns_new_dir = self.base_dir / "patterns_new"
        self.summarizer = PatternSummarizer()

    def load_metadata(self, pattern_file: Path) -> Dict:
        """Load pattern metadata"""
        metadata_file = pattern_file.with_suffix('.metadata.json')
        if metadata_file.exists():
            return json.loads(metadata_file.read_text())
        return {}

    def classify_pattern(self, pattern_file: Path, metadata: Dict) -> tuple[str, str]:
        """
        Classify pattern into tier.

        Returns:
            (tier_name, reason)
        """
        # Get file age
        file_age_days = days_since_timestamp(pattern_file.stat().st_mtime)

        # Get metadata
        use_count = metadata.get('use_count', 0)
        confidence = metadata.get('confidence', 0)
        if isinstance(confidence, str):
            try:
                confidence = float(confidence)
            except ValueError:
                confidence = 0

        # Recent (< 30 days)
        if file_age_days < 30:
            return "recent", f"Recent file ({file_age_days}d old)"

        # High-value patterns (permanent storage)
        if confidence >= 0.85:
            return "patterns", f"High confidence ({confidence:.2f})"

        if use_count >= 3:
            return "patterns", f"High usage ({use_count} uses)"

        # Everything else goes to intermediate (with summarization)
        return "intermediate", f"Age {file_age_days}d, conf {confidence:.2f}, uses {use_count}"

    def migrate_pattern(
        self,
        pattern_file: Path,
        metadata: Dict,
        tier: str,
        reason: str,
        dry_run: bool = False
    ) -> bool:
        """
        Migrate a single pattern to its tier.

        Args:
            pattern_file: Pattern file to migrate
            metadata: Pattern metadata
            tier: Destination tier (recent, intermediate, patterns)
            reason: Classification reason
            dry_run: If True, don't actually move files

        Returns:
            True if migrated successfully
        """
        # Determine destination directory
        if tier == "recent":
            dest_dir = self.recent_dir
        elif tier == "intermediate":
            dest_dir = self.intermediate_dir
        elif tier == "patterns":
            dest_dir = self.patterns_new_dir
        else:
            return False

        dest_file = dest_dir / pattern_file.name

        print(f"  → {tier:12s} {pattern_file.name}")
        print(f"     Reason: {reason}")

        if dry_run:
            if tier == "intermediate":
                print(f"     [Would summarize]")
            return True

        # Copy pattern
        shutil.copy2(pattern_file, dest_file)

        # Copy metadata
        source_metadata = pattern_file.with_suffix('.metadata.json')
        if source_metadata.exists():
            dest_metadata = dest_file.with_suffix('.metadata.json')
            shutil.copy2(source_metadata, dest_metadata)

            # Update metadata with tier info
            metadata['tier'] = tier
            metadata['migrated_at'] = datetime.now().isoformat()
            metadata['migration_reason'] = reason
            dest_metadata.write_text(json.dumps(metadata, indent=2))

        # Summarize if going to intermediate
        if tier == "intermediate":
            try:
                summary = self.summarizer.summarize_pattern(dest_file)
                dest_file.write_text(summary)
                print(f"     ✓ Summarized")
            except Exception as e:
                print(f"     ⚠️  Summarization failed: {e}")

        return True

    def migrate_directory(
        self,
        source_dir: Path,
        dry_run: bool = False
    ) -> Dict[str, List[str]]:
        """
        Migrate all patterns from source directory.

        Args:
            source_dir: Source directory (patterns/)
            dry_run: If True, preview without moving

        Returns:
            Dictionary mapping tier to list of pattern names
        """
        # Create destination directories
        if not dry_run:
            self.recent_dir.mkdir(exist_ok=True)
            self.intermediate_dir.mkdir(exist_ok=True)
            self.patterns_new_dir.mkdir(exist_ok=True)

        # Track migrations
        migrations = {
            "recent": [],
            "intermediate": [],
            "patterns": []
        }

        # Process each pattern
        for pattern_file in source_dir.glob("*.md"):
            if not pattern_file.is_file():
                continue

            # Load metadata
            metadata = self.load_metadata(pattern_file)

            # Classify
            tier, reason = self.classify_pattern(pattern_file, metadata)

            # Migrate
            if self.migrate_pattern(pattern_file, metadata, tier, reason, dry_run=dry_run):
                migrations[tier].append(pattern_file.name)

        return migrations

    def finalize_migration(self, backup: bool = True, dry_run: bool = False):
        """
        Finalize migration by replacing old patterns/ with new.

        Args:
            backup: Create backup of old patterns/
            dry_run: If True, don't actually move
        """
        if dry_run:
            print("\n⚠️  DRY RUN - Would finalize migration:")
            if backup:
                print(f"   - Backup: {self.patterns_dir} → {self.patterns_dir}_backup")
            print(f"   - Replace: {self.patterns_new_dir} → {self.patterns_dir}")
            return

        # Backup old patterns/
        if backup:
            backup_dir = self.base_dir / "patterns_backup"
            if backup_dir.exists():
                shutil.rmtree(backup_dir)
            shutil.copytree(self.patterns_dir, backup_dir)
            print(f"✅ Backup created: {backup_dir}")

        # Remove old patterns/
        shutil.rmtree(self.patterns_dir)

        # Rename patterns_new to patterns
        shutil.move(self.patterns_new_dir, self.patterns_dir)

        print(f"✅ Migration finalized")


def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Migrate existing patterns to three-tier structure"
    )
    parser.add_argument(
        "--source",
        default=".claude/memory/patterns",
        help="Source directory (default: .claude/memory/patterns)"
    )
    parser.add_argument(
        "--backup",
        action="store_true",
        help="Create backup before migration"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview migration without moving files"
    )

    args = parser.parse_args()

    source_dir = Path(args.source)
    if not source_dir.exists():
        print(f"❌ Error: Source directory not found: {source_dir}")
        return 1

    print(f"\n{'=' * 70}")
    print("PATTERN MIGRATION TO THREE-TIER STRUCTURE")
    print(f"{'=' * 70}")
    print(f"Source: {source_dir}")
    print("")

    migrator = PatternMigrator()

    # Run migration
    migrations = migrator.migrate_directory(source_dir, dry_run=args.dry_run)

    # Print results
    print(f"\n{'=' * 70}")
    print("MIGRATION RESULTS")
    print(f"{'=' * 70}")
    print(f"Recent (full detail):        {len(migrations['recent'])} patterns")
    print(f"Intermediate (summarized):   {len(migrations['intermediate'])} patterns")
    print(f"Patterns (permanent):        {len(migrations['patterns'])} patterns")
    print(f"Total:                       {sum(len(v) for v in migrations.values())} patterns")

    if migrations['recent']:
        print(f"\nRecent:")
        for name in migrations['recent'][:5]:
            print(f"  - {name}")
        if len(migrations['recent']) > 5:
            print(f"  ... and {len(migrations['recent']) - 5} more")

    if migrations['intermediate']:
        print(f"\nIntermediate (will be summarized):")
        for name in migrations['intermediate'][:5]:
            print(f"  - {name}")
        if len(migrations['intermediate']) > 5:
            print(f"  ... and {len(migrations['intermediate']) - 5} more")

    if migrations['patterns']:
        print(f"\nPatterns (permanent):")
        for name in migrations['patterns'][:5]:
            print(f"  - {name}")
        if len(migrations['patterns']) > 5:
            print(f"  ... and {len(migrations['patterns']) - 5} more")

    if args.dry_run:
        print(f"\n{'=' * 70}")
        print("⚠️  DRY RUN - No files were modified")
        print("Run without --dry-run to apply migration")
        print(f"{'=' * 70}")
    else:
        # Finalize migration
        print(f"\n{'=' * 70}")
        print("FINALIZING MIGRATION")
        print(f"{'=' * 70}")
        migrator.finalize_migration(backup=args.backup, dry_run=False)
        print(f"\n✅ Migration complete!")
        print(f"\nNew structure:")
        print(f"  .claude/memory/recent/       - {len(migrations['recent'])} patterns")
        print(f"  .claude/memory/intermediate/ - {len(migrations['intermediate'])} patterns")
        print(f"  .claude/memory/patterns/     - {len(migrations['patterns'])} patterns")
        if args.backup:
            print(f"  .claude/memory/patterns_backup/ - Original backup")
        print(f"{'=' * 70}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
