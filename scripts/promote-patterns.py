#!/usr/bin/env python3
"""
Pattern Promotion Engine for Memory Consolidation

Promotes high-value patterns from intermediate storage to permanent patterns directory.

Promotion Criteria:
- Confidence score ≥0.85 (validated by /complete)
- Use count ≥3 (proven useful)
- Use count ≥2 AND confidence ≥0.70 AND used in last 60 days

Usage:
    python scripts/promote-patterns.py                       # Promote all eligible
    python scripts/promote-patterns.py --dry-run             # Preview only
    python scripts/promote-patterns.py --threshold 0.90      # Custom threshold
"""

from pathlib import Path
import json
import shutil
from datetime import datetime, timedelta
from typing import List, Dict
import sys


def days_since(date_str: str) -> int:
    """Calculate days since a date string"""
    try:
        date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return (datetime.now() - date).days
    except (ValueError, TypeError):
        return 999  # Unknown date = very old


class PatternPromoter:
    """Promotes patterns from intermediate to permanent storage"""

    def __init__(self, confidence_threshold: float = 0.85, usage_threshold: int = 3):
        """
        Initialize promoter.

        Args:
            confidence_threshold: Minimum confidence for promotion (default: 0.85)
            usage_threshold: Minimum use count for promotion (default: 3)
        """
        self.confidence_threshold = confidence_threshold
        self.usage_threshold = usage_threshold

    def load_metadata(self, pattern_file: Path) -> Dict:
        """Load pattern metadata"""
        metadata_file = pattern_file.with_suffix('.metadata.json')
        if metadata_file.exists():
            return json.loads(metadata_file.read_text())
        return {}

    def save_metadata(self, pattern_file: Path, metadata: Dict):
        """Save pattern metadata"""
        metadata_file = pattern_file.with_suffix('.metadata.json')
        metadata_file.write_text(json.dumps(metadata, indent=2))

    def is_summarized(self, content: str) -> bool:
        """Check if pattern is summarized"""
        return "(SUMMARIZED)" in content or "**Summarized**:" in content

    def should_promote(self, metadata: Dict) -> tuple[bool, str]:
        """
        Determine if pattern should be promoted.

        Returns:
            (should_promote, reason)
        """
        # High confidence (validated by /complete)
        confidence = metadata.get('confidence', 0)
        if isinstance(confidence, str):
            try:
                confidence = float(confidence)
            except ValueError:
                confidence = 0

        if confidence >= self.confidence_threshold:
            return True, f"High confidence ({confidence:.2f})"

        # High usage (proven useful)
        use_count = metadata.get('use_count', 0)
        if use_count >= self.usage_threshold:
            return True, f"High usage ({use_count} uses)"

        # Recently used with moderate confidence
        if use_count >= 2 and confidence >= 0.70:
            last_used = metadata.get('last_used')
            if last_used:
                days = days_since(last_used)
                if days < 60:
                    return True, f"Recent + moderate confidence ({use_count} uses, conf {confidence:.2f}, {days}d ago)"

        return False, "Does not meet promotion criteria"

    def restore_from_summary(self, pattern_file: Path) -> str:
        """
        Restore full pattern from summary.

        For now, returns the summary with a note. In future, could retrieve
        from archive if we implement full pattern archival.
        """
        content = pattern_file.read_text()

        if not self.is_summarized(content):
            return content

        # For now, promote the summary with a note
        # Future: Retrieve full pattern from archive
        return content + "\n\n**Note**: Full pattern restoration not yet implemented. Summary promoted to permanent storage."

    def promote_pattern(self, source_file: Path, dest_dir: Path, dry_run: bool = False) -> bool:
        """
        Promote a single pattern.

        Args:
            source_file: Pattern file in intermediate/
            dest_dir: Destination directory (patterns/)
            dry_run: If True, don't actually move files

        Returns:
            True if promoted
        """
        # Load metadata
        metadata = self.load_metadata(source_file)

        # Check if should promote
        should_promote, reason = self.should_promote(metadata)

        if not should_promote:
            return False

        print(f"  ✅ Promoting: {source_file.name}")
        print(f"     Reason: {reason}")

        if dry_run:
            print(f"     [DRY RUN - would promote to {dest_dir / source_file.name}]")
            return True

        # Get content (restore if summarized)
        content = self.restore_from_summary(source_file)

        # Write to destination
        dest_file = dest_dir / source_file.name
        dest_file.write_text(content)

        # Update metadata
        metadata['promoted_at'] = datetime.now().isoformat()
        metadata['tier'] = 'patterns'
        metadata['promoted_from'] = 'intermediate'
        self.save_metadata(dest_file, metadata)

        # Move metadata
        source_metadata = source_file.with_suffix('.metadata.json')
        if source_metadata.exists():
            dest_metadata = dest_file.with_suffix('.metadata.json')
            shutil.copy2(source_metadata, dest_metadata)

        # Remove from source
        source_file.unlink()
        if source_metadata.exists():
            source_metadata.unlink()

        return True

    def promote_eligible_patterns(
        self,
        source_dir: Path,
        dest_dir: Path,
        dry_run: bool = False
    ) -> List[str]:
        """
        Promote all eligible patterns from source to destination.

        Args:
            source_dir: Source directory (intermediate/)
            dest_dir: Destination directory (patterns/)
            dry_run: If True, preview without moving

        Returns:
            List of promoted pattern names
        """
        promoted = []

        for pattern_file in source_dir.glob("*.md"):
            if self.promote_pattern(pattern_file, dest_dir, dry_run=dry_run):
                promoted.append(pattern_file.name)

        return promoted


def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Promote high-value patterns to permanent storage"
    )
    parser.add_argument(
        "--source",
        default=".claude/memory/intermediate",
        help="Source directory (default: .claude/memory/intermediate)"
    )
    parser.add_argument(
        "--dest",
        default=".claude/memory/patterns",
        help="Destination directory (default: .claude/memory/patterns)"
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.85,
        help="Confidence threshold (default: 0.85)"
    )
    parser.add_argument(
        "--usage",
        type=int,
        default=3,
        help="Usage threshold (default: 3)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview without promoting"
    )

    args = parser.parse_args()

    source_dir = Path(args.source)
    dest_dir = Path(args.dest)

    if not source_dir.exists():
        print(f"❌ Error: Source directory not found: {source_dir}")
        return 1

    dest_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'=' * 60}")
    print("PATTERN PROMOTION")
    print(f"{'=' * 60}")
    print(f"Source: {source_dir}")
    print(f"Destination: {dest_dir}")
    print(f"Confidence Threshold: {args.threshold}")
    print(f"Usage Threshold: {args.usage}")
    print("")

    promoter = PatternPromoter(
        confidence_threshold=args.threshold,
        usage_threshold=args.usage
    )

    promoted = promoter.promote_eligible_patterns(source_dir, dest_dir, dry_run=args.dry_run)

    print(f"\n{'=' * 60}")
    print("PROMOTION RESULTS")
    print(f"{'=' * 60}")
    print(f"Patterns Promoted: {len(promoted)}")

    if promoted:
        print("\nPromoted:")
        for name in promoted:
            print(f"  - {name}")

    if args.dry_run:
        print("\n⚠️  DRY RUN - No files modified")
    else:
        print("\n✅ Promotion complete")

    print(f"{'=' * 60}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
