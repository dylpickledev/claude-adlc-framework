#!/usr/bin/env python3
"""
Add Token Metadata to Existing Patterns

Scans memory patterns and agent files, adds metadata with token counts,
and initializes usage tracking.

Usage:
    python scripts/add-token-metadata.py                    # Add to all patterns
    python scripts/add-token-metadata.py --dry-run          # Preview only
    python scripts/add-token-metadata.py --dir .claude/memory/patterns  # Specific directory
"""

from pathlib import Path
import json
import sys
from datetime import datetime

# Import token counter
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

try:
    from count_tokens import TokenCounter
except ImportError:
    # If running as module, try direct import
    import importlib.util
    spec = importlib.util.spec_from_file_location("count_tokens", script_dir / "count-tokens.py")
    count_tokens = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(count_tokens)
    TokenCounter = count_tokens.TokenCounter


class MetadataManager:
    """Manages metadata for memory patterns"""

    def __init__(self, token_counter: TokenCounter):
        """
        Initialize metadata manager.

        Args:
            token_counter: TokenCounter instance
        """
        self.counter = token_counter

    def create_metadata(self, pattern_file: Path) -> dict:
        """
        Create metadata dictionary for a pattern file.

        Args:
            pattern_file: Path to pattern file

        Returns:
            Metadata dictionary
        """
        # Count tokens
        token_data = self.counter.count_file_tokens(pattern_file)

        # Get file stats
        stat = pattern_file.stat()

        # Initialize metadata
        metadata = {
            "pattern_file": pattern_file.name,
            "token_count": token_data["token_count"],
            "content_hash": token_data["content_hash"],
            "use_count": 0,
            "last_used": None,
            "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "confidence": None,  # To be extracted from content if present
            "tags": []  # To be populated later
        }

        # Try to extract confidence from content
        try:
            content = pattern_file.read_text(encoding='utf-8')
            confidence = self._extract_confidence(content)
            if confidence:
                metadata["confidence"] = confidence
        except Exception:
            pass

        return metadata

    def _extract_confidence(self, content: str) -> float:
        """
        Extract confidence score from pattern content.

        Looks for patterns like:
        - Confidence: 0.85
        - (confidence: 0.90)
        - confidence=0.92

        Args:
            content: Pattern content

        Returns:
            Confidence score or None
        """
        import re

        patterns = [
            r'[Cc]onfidence:\s*(\d+\.\d+)',
            r'\([Cc]onfidence:\s*(\d+\.\d+)\)',
            r'[Cc]onfidence=(\d+\.\d+)'
        ]

        for pattern in patterns:
            match = re.search(pattern, content)
            if match:
                try:
                    confidence = float(match.group(1))
                    if 0.0 <= confidence <= 1.0:
                        return confidence
                except ValueError:
                    pass

        return None

    def get_metadata_path(self, pattern_file: Path) -> Path:
        """
        Get path to metadata file for a pattern.

        Args:
            pattern_file: Path to pattern file

        Returns:
            Path to metadata file
        """
        return pattern_file.with_suffix('.metadata.json')

    def metadata_exists(self, pattern_file: Path) -> bool:
        """
        Check if metadata file already exists.

        Args:
            pattern_file: Path to pattern file

        Returns:
            True if metadata exists
        """
        return self.get_metadata_path(pattern_file).exists()

    def load_metadata(self, pattern_file: Path) -> dict:
        """
        Load existing metadata for a pattern.

        Args:
            pattern_file: Path to pattern file

        Returns:
            Metadata dictionary or None
        """
        metadata_file = self.get_metadata_path(pattern_file)
        if metadata_file.exists():
            try:
                return json.loads(metadata_file.read_text())
            except json.JSONDecodeError:
                return None
        return None

    def save_metadata(self, pattern_file: Path, metadata: dict):
        """
        Save metadata to file.

        Args:
            pattern_file: Path to pattern file
            metadata: Metadata dictionary
        """
        metadata_file = self.get_metadata_path(pattern_file)
        metadata_file.write_text(json.dumps(metadata, indent=2))

    def update_metadata(self, pattern_file: Path, force: bool = False) -> bool:
        """
        Update metadata for a pattern file.

        Args:
            pattern_file: Path to pattern file
            force: Force update even if metadata exists

        Returns:
            True if metadata was created/updated
        """
        metadata_file = self.get_metadata_path(pattern_file)

        # Check if metadata exists and should be skipped
        if metadata_file.exists() and not force:
            # Verify content hash
            existing_metadata = self.load_metadata(pattern_file)
            token_data = self.counter.count_file_tokens(pattern_file)

            if existing_metadata.get("content_hash") == token_data["content_hash"]:
                # Content unchanged, skip
                return False

        # Create/update metadata
        metadata = self.create_metadata(pattern_file)
        self.save_metadata(pattern_file, metadata)
        return True


def process_directory(
    directory: Path,
    pattern: str = "*.md",
    dry_run: bool = False,
    force: bool = False
) -> dict:
    """
    Process all patterns in a directory.

    Args:
        directory: Directory to process
        pattern: File pattern (default: *.md)
        dry_run: If True, don't write metadata
        force: Force update even if metadata exists

    Returns:
        Statistics dictionary
    """
    counter = TokenCounter()
    manager = MetadataManager(counter)

    stats = {
        "total_files": 0,
        "created": 0,
        "updated": 0,
        "skipped": 0,
        "errors": []
    }

    files = list(directory.rglob(pattern))
    stats["total_files"] = len(files)

    print(f"Processing {len(files)} files in {directory}...")

    for i, pattern_file in enumerate(files, 1):
        if not pattern_file.is_file():
            continue

        try:
            # Check if metadata exists
            metadata_exists = manager.metadata_exists(pattern_file)

            if dry_run:
                if metadata_exists and not force:
                    print(f"  [{i}/{len(files)}] SKIP: {pattern_file.name}")
                    stats["skipped"] += 1
                else:
                    print(f"  [{i}/{len(files)}] WOULD CREATE: {pattern_file.name}")
                    stats["created"] += 1
            else:
                updated = manager.update_metadata(pattern_file, force=force)
                if updated:
                    action = "UPDATED" if metadata_exists else "CREATED"
                    print(f"  [{i}/{len(files)}] {action}: {pattern_file.name}")
                    if metadata_exists:
                        stats["updated"] += 1
                    else:
                        stats["created"] += 1
                else:
                    print(f"  [{i}/{len(files)}] SKIP: {pattern_file.name}")
                    stats["skipped"] += 1

        except Exception as e:
            print(f"  [{i}/{len(files)}] ERROR: {pattern_file.name} - {e}")
            stats["errors"].append({
                "file": str(pattern_file),
                "error": str(e)
            })

    return stats


def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Add token metadata to memory patterns"
    )
    parser.add_argument(
        "--dir",
        default=".claude/memory",
        help="Directory to process (default: .claude/memory)"
    )
    parser.add_argument(
        "--pattern",
        default="*.md",
        help="File pattern (default: *.md)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without writing"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force update even if metadata exists"
    )
    parser.add_argument(
        "--agents",
        action="store_true",
        help="Also process agent files"
    )

    args = parser.parse_args()

    # Process memory directory
    memory_dir = Path(args.dir)
    if not memory_dir.exists():
        print(f"❌ Error: Directory not found: {memory_dir}")
        return 1

    print("\n" + "=" * 60)
    print("ADD TOKEN METADATA TO PATTERNS")
    print("=" * 60)

    stats = process_directory(
        memory_dir,
        pattern=args.pattern,
        dry_run=args.dry_run,
        force=args.force
    )

    # Process agents if requested
    agents_stats = None
    if args.agents:
        agents_dir = Path(".claude/agents")
        if agents_dir.exists():
            print(f"\nProcessing agent files...")
            agents_stats = process_directory(
                agents_dir,
                pattern=args.pattern,
                dry_run=args.dry_run,
                force=args.force
            )

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Memory Patterns:")
    print(f"  Total Files:   {stats['total_files']}")
    print(f"  Created:       {stats['created']}")
    print(f"  Updated:       {stats['updated']}")
    print(f"  Skipped:       {stats['skipped']}")
    print(f"  Errors:        {len(stats['errors'])}")

    if agents_stats:
        print(f"\nAgent Files:")
        print(f"  Total Files:   {agents_stats['total_files']}")
        print(f"  Created:       {agents_stats['created']}")
        print(f"  Updated:       {agents_stats['updated']}")
        print(f"  Skipped:       {agents_stats['skipped']}")
        print(f"  Errors:        {len(agents_stats['errors'])}")

    if args.dry_run:
        print("\n⚠️  DRY RUN - No files were modified")
        print("Run without --dry-run to apply changes")
    else:
        print("\n✅ Metadata updated successfully")

    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
