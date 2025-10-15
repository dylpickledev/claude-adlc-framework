#!/usr/bin/env python3
"""
Pattern Archival Engine for Memory Consolidation

Archives low-value patterns from intermediate storage to reduce active memory.

Archival Criteria:
- Age >90 days AND use count <2 (old and unused)
- Age >180 days AND use count <5 (very old and low usage)

Usage:
    python scripts/archive-patterns.py                       # Archive all eligible
    python scripts/archive-patterns.py --dry-run             # Preview only
    python scripts/archive-patterns.py --age 120             # Custom age threshold
"""

from pathlib import Path
import json
import shutil
from datetime import datetime
from typing import List, Dict
import sys


def days_since_timestamp(timestamp: float) -> int:
    """Calculate days since a Unix timestamp"""
    date = datetime.fromtimestamp(timestamp)
    return (datetime.now() - date).days


def days_since_iso(date_str: str) -> int:
    """Calculate days since an ISO date string"""
    try:
        date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return (datetime.now() - date).days
    except (ValueError, TypeError):
        return 999


class PatternArchiver:
    """Archives low-value patterns to reduce active memory"""

    def __init__(self, age_threshold: int = 90, min_uses: int = 2):
        """
        Initialize archiver.

        Args:
            age_threshold: Minimum age in days for archival (default: 90)
            min_uses: Minimum use count to avoid archival (default: 2)
        """
        self.age_threshold = age_threshold
        self.min_uses = min_uses

    def load_metadata(self, pattern_file: Path) -> Dict:
        """Load pattern metadata"""
        metadata_file = pattern_file.with_suffix('.metadata.json')
        if metadata_file.exists():
            return json.loads(metadata_file.read_text())
        return {}

    def should_archive(self, pattern_file: Path, metadata: Dict) -> tuple[bool, str]:
        """
        Determine if pattern should be archived.

        Returns:
            (should_archive, reason)
        """
        # Get file age
        file_modified_days = days_since_timestamp(pattern_file.stat().st_mtime)

        # Get metadata
        use_count = metadata.get('use_count', 0)
        confidence = metadata.get('confidence', 0)

        # Never archive high-confidence patterns
        if isinstance(confidence, (int, float)) and confidence >= 0.70:
            return False, "High confidence - keep active"

        # Old and unused
        if file_modified_days > self.age_threshold and use_count < self.min_uses:
            return True, f"Old and unused ({file_modified_days}d, {use_count} uses)"

        # Very old and low usage
        if file_modified_days > 180 and use_count < 5:
            return True, f"Very old with low usage ({file_modified_days}d, {use_count} uses)"

        return False, "Does not meet archival criteria"

    def archive_pattern(self, pattern_file: Path, archive_dir: Path, dry_run: bool = False) -> bool:
        """
        Archive a single pattern.

        Args:
            pattern_file: Pattern file to archive
            archive_dir: Archive directory
            dry_run: If True, don't actually move files

        Returns:
            True if archived
        """
        # Load metadata
        metadata = self.load_metadata(pattern_file)

        # Check if should archive
        should_archive, reason = self.should_archive(pattern_file, metadata)

        if not should_archive:
            return False

        print(f"  📦 Archiving: {pattern_file.name}")
        print(f"     Reason: {reason}")

        if dry_run:
            archive_name = f"{pattern_file.stem}_{datetime.now().strftime('%Y%m%d')}.md"
            print(f"     [DRY RUN - would archive to {archive_dir / archive_name}]")
            return True

        # Create archive filename with timestamp
        archive_name = f"{pattern_file.stem}_{datetime.now().strftime('%Y%m%d')}.md"
        archive_file = archive_dir / archive_name

        # Move pattern
        shutil.move(pattern_file, archive_file)

        # Move metadata
        source_metadata = pattern_file.with_suffix('.metadata.json')
        if source_metadata.exists():
            archive_metadata = archive_file.with_suffix('.metadata.json')
            shutil.move(source_metadata, archive_metadata)

            # Update metadata with archive info
            metadata['archived_at'] = datetime.now().isoformat()
            metadata['archive_reason'] = reason
            archive_metadata.write_text(json.dumps(metadata, indent=2))

        return True

    def archive_eligible_patterns(
        self,
        source_dir: Path,
        archive_dir: Path,
        dry_run: bool = False
    ) -> List[str]:
        """
        Archive all eligible patterns from source directory.

        Args:
            source_dir: Source directory (intermediate/)
            archive_dir: Archive directory
            dry_run: If True, preview without moving

        Returns:
            List of archived pattern names
        """
        archived = []

        # Ensure archive directory exists
        if not dry_run:
            archive_dir.mkdir(parents=True, exist_ok=True)

        for pattern_file in source_dir.glob("*.md"):
            if self.archive_pattern(pattern_file, archive_dir, dry_run=dry_run):
                archived.append(pattern_file.name)

        return archived


def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Archive low-value patterns to reduce active memory"
    )
    parser.add_argument(
        "--source",
        default=".claude/memory/intermediate",
        help="Source directory (default: .claude/memory/intermediate)"
    )
    parser.add_argument(
        "--archive",
        default=".claude/memory/archive",
        help="Archive directory (default: .claude/memory/archive)"
    )
    parser.add_argument(
        "--age",
        type=int,
        default=90,
        help="Age threshold in days (default: 90)"
    )
    parser.add_argument(
        "--min-uses",
        type=int,
        default=2,
        help="Minimum use count to avoid archival (default: 2)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview without archiving"
    )

    args = parser.parse_args()

    source_dir = Path(args.source)
    archive_dir = Path(args.archive)

    if not source_dir.exists():
        print(f"❌ Error: Source directory not found: {source_dir}")
        return 1

    print(f"\n{'=' * 60}")
    print("PATTERN ARCHIVAL")
    print(f"{'=' * 60}")
    print(f"Source: {source_dir}")
    print(f"Archive: {archive_dir}")
    print(f"Age Threshold: {args.age} days")
    print(f"Min Uses: {args.min_uses}")
    print("")

    archiver = PatternArchiver(age_threshold=args.age, min_uses=args.min_uses)
    archived = archiver.archive_eligible_patterns(source_dir, archive_dir, dry_run=args.dry_run)

    print(f"\n{'=' * 60}")
    print("ARCHIVAL RESULTS")
    print(f"{'=' * 60}")
    print(f"Patterns Archived: {len(archived)}")

    if archived:
        print("\nArchived:")
        for name in archived:
            print(f"  - {name}")

    if args.dry_run:
        print("\n⚠️  DRY RUN - No files modified")
    else:
        print("\n✅ Archival complete")

    print(f"{'=' * 60}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
