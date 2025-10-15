#!/usr/bin/env python3
"""
Pattern Deduplication Engine

Detects and reports duplicate patterns across agent scopes using MD5 hash matching.

Usage:
    python scripts/deduplicate-patterns.py              # Report duplicates
    python scripts/deduplicate-patterns.py --cleanup    # Remove duplicates (dry-run)
"""

from pathlib import Path
import json
import sys
import hashlib
from typing import Dict, List
from collections import defaultdict

class DeduplicationEngine:
    """Detect duplicate patterns using content hashing"""

    def __init__(self):
        self.base_dir = Path(".claude/memory")

    def calculate_hash(self, file_path: Path) -> str:
        """Calculate MD5 hash of file content"""
        content = file_path.read_text(encoding='utf-8')
        return hashlib.md5(content.encode()).hexdigest()

    def scan_duplicates(self) -> Dict[str, List[Path]]:
        """Scan all patterns and group by hash

        Returns dict of hash -> [list of file paths]
        """
        hash_map = defaultdict(list)

        # Scan all pattern files
        for pattern_file in self.base_dir.glob("**/*.md"):
            if pattern_file.is_file():
                file_hash = self.calculate_hash(pattern_file)
                hash_map[file_hash].append(pattern_file)

        # Filter to only duplicates (hash appears > 1 time)
        duplicates = {h: files for h, files in hash_map.items() if len(files) > 1}

        return duplicates

    def print_report(self, duplicates: Dict[str, List[Path]]):
        """Print duplicate patterns report"""
        print("\n" + "=" * 70)
        print("DUPLICATE PATTERN DETECTION")
        print("=" * 70)

        if not duplicates:
            print("\n✅ No duplicate patterns detected")
            return

        total_duplicates = sum(len(files) - 1 for files in duplicates.values())
        print(f"\nFound {len(duplicates)} sets of duplicates ({total_duplicates} duplicate files):\n")

        for i, (hash_value, files) in enumerate(sorted(duplicates.items()), 1):
            print(f"{i}. Hash: {hash_value[:12]}... ({len(files)} copies)")
            for file_path in sorted(files):
                relative_path = file_path.relative_to(self.base_dir)
                print(f"   - {relative_path}")
            print()

        print("=" * 70)
        print(f"\nTotal duplicate files: {total_duplicates}")
        print(f"Potential space savings: Keep 1 copy of each set")
        print("\n💡 Review duplicates and use promote-to-global.py to consolidate")
        print("=" * 70)


def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Detect duplicate patterns across agent scopes"
    )
    parser.add_argument("--cleanup", action="store_true",
                        help="Report cleanup recommendations (dry-run)")

    args = parser.parse_args()

    engine = DeduplicationEngine()

    # Scan for duplicates
    duplicates = engine.scan_duplicates()

    # Print report
    engine.print_report(duplicates)

    if args.cleanup and duplicates:
        print("\n📝 CLEANUP RECOMMENDATIONS:")
        print("1. Review duplicate sets above")
        print("2. Keep canonical version (highest use_count or in global scope)")
        print("3. Archive or remove duplicates from agent scopes")
        print("4. Consider promoting common patterns to global scope")

    return 0


if __name__ == "__main__":
    sys.exit(main())
