#!/usr/bin/env python3
"""
Automated Pattern Archival Engine

Automatically archives low-value patterns to reduce active memory footprint
while preserving searchability.

Archival Criteria:
- Age > 180 days
- use_count < 3
- confidence < 0.70 (or not set)
- NOT in global scope (keep all global patterns)

Usage:
    python scripts/auto-archive-patterns.py              # Auto-archive qualified patterns
    python scripts/auto-archive-patterns.py --dry-run    # Preview archival
    python scripts/auto-archive-patterns.py --report     # Show archival candidates
"""

from pathlib import Path
import json
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import shutil

class AutoArchivalEngine:
    """Automated pattern archival based on age and usage"""

    # Archival criteria
    AGE_THRESHOLD_DAYS = 180
    MIN_USE_COUNT = 3
    MIN_CONFIDENCE = 0.70

    def __init__(self, dry_run: bool = False):
        self.base_dir = Path(".claude/memory")
        self.dry_run = dry_run
        self.archival_log = Path(".claude/cache/auto-archival.json")

    def get_pattern_age_days(self, pattern_file: Path, metadata: Dict) -> int:
        """Calculate pattern age in days"""
        # Try last_used from metadata first
        if metadata.get("last_used"):
            try:
                last_used = datetime.fromisoformat(metadata["last_used"])
                age = (datetime.now() - last_used).days
                return age
            except:
                pass

        # Fallback to file modification time
        mtime = datetime.fromtimestamp(pattern_file.stat().st_mtime)
        age = (datetime.now() - mtime).days
        return age

    def scan_archival_candidates(self) -> List[Dict]:
        """Scan all patterns for archival candidates

        Returns list of candidates with metadata
        """
        candidates = []

        # Scan agent-specific patterns only (never archive global)
        for agent_type in ["specialists", "roles"]:
            agents_dir = self.base_dir / agent_type

            if not agents_dir.exists():
                continue

            for agent_dir in agents_dir.iterdir():
                if not agent_dir.is_dir():
                    continue

                agent_name = agent_dir.name

                # Check patterns directory
                patterns_dir = agent_dir / "patterns"
                if patterns_dir.exists():
                    candidates.extend(
                        self.scan_directory_for_archival(
                            patterns_dir, agent_type, agent_name, "patterns"
                        )
                    )

                # Check intermediate directory
                intermediate_dir = agent_dir / "intermediate"
                if intermediate_dir.exists():
                    candidates.extend(
                        self.scan_directory_for_archival(
                            intermediate_dir, agent_type, agent_name, "intermediate"
                        )
                    )

                # Check recent directory (rare, but check anyway)
                recent_dir = agent_dir / "recent"
                if recent_dir.exists():
                    candidates.extend(
                        self.scan_directory_for_archival(
                            recent_dir, agent_type, agent_name, "recent"
                        )
                    )

        # Sort by age (oldest first)
        candidates.sort(key=lambda x: x["age_days"], reverse=True)

        return candidates

    def scan_directory_for_archival(
        self, directory: Path, agent_type: str, agent_name: str, tier: str
    ) -> List[Dict]:
        """Scan a specific directory for archival candidates"""
        candidates = []

        for pattern_file in directory.glob("*.md"):
            metadata_file = pattern_file.with_suffix(".metadata.json")

            if not metadata_file.exists():
                # No metadata - create default
                metadata = {
                    "token_count": 0,
                    "use_count": 0,
                    "confidence": None,
                    "last_used": None
                }
            else:
                metadata = json.loads(metadata_file.read_text())

            # Calculate age
            age_days = self.get_pattern_age_days(pattern_file, metadata)

            # Check archival criteria
            use_count = metadata.get("use_count", 0)
            confidence = metadata.get("confidence")

            qualifies = False
            reasons = []

            # Criteria: age > 180 days AND (use_count < 3 OR confidence < 0.70)
            if age_days > self.AGE_THRESHOLD_DAYS:
                if use_count < self.MIN_USE_COUNT:
                    qualifies = True
                    reasons.append(f"use_count={use_count} < {self.MIN_USE_COUNT}")

                if confidence is None or confidence < self.MIN_CONFIDENCE:
                    qualifies = True
                    conf_str = f"{confidence:.2f}" if confidence else "unset"
                    reasons.append(f"confidence={conf_str} < {self.MIN_CONFIDENCE}")

            if qualifies and age_days > self.AGE_THRESHOLD_DAYS:
                candidates.append({
                    "agent_type": agent_type,
                    "agent_name": agent_name,
                    "tier": tier,
                    "pattern_name": pattern_file.name,
                    "pattern_path": str(pattern_file),
                    "age_days": age_days,
                    "use_count": use_count,
                    "confidence": confidence,
                    "reasons": ", ".join(reasons),
                    "archival_score": self.calculate_archival_score(age_days, use_count, confidence)
                })

        return candidates

    def calculate_archival_score(self, age_days: int, use_count: int, confidence: float) -> float:
        """Calculate archival priority score (0-1)

        Higher score = higher priority for archival
        """
        score = 0.0

        # Age component (max 0.5)
        if age_days > self.AGE_THRESHOLD_DAYS:
            age_ratio = min((age_days - self.AGE_THRESHOLD_DAYS) / 180.0, 1.0)
            score += age_ratio * 0.5

        # Low usage component (max 0.3)
        if use_count < self.MIN_USE_COUNT:
            usage_penalty = (self.MIN_USE_COUNT - use_count) / self.MIN_USE_COUNT
            score += usage_penalty * 0.3

        # Low confidence component (max 0.2)
        if confidence is None:
            score += 0.2
        elif confidence < self.MIN_CONFIDENCE:
            conf_penalty = (self.MIN_CONFIDENCE - confidence) / self.MIN_CONFIDENCE
            score += conf_penalty * 0.2

        return min(score, 1.0)

    def archive_candidates(self, candidates: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
        """Archive qualified candidates

        Returns (successful_archivals, failed_archivals)
        """
        successful = []
        failed = []

        for candidate in candidates:
            try:
                if self.dry_run:
                    print(f"[DRY RUN] Would archive: {candidate['pattern_name']} from {candidate['agent_name']}/{candidate['tier']}")
                    successful.append(candidate)
                else:
                    # Archive pattern
                    source_path = Path(candidate["pattern_path"])
                    archive_dir = self.base_dir / candidate["agent_type"] / candidate["agent_name"] / "archive"
                    archive_dir.mkdir(parents=True, exist_ok=True)

                    dest_path = archive_dir / source_path.name

                    # Move pattern to archive
                    shutil.move(str(source_path), str(dest_path))

                    # Move metadata
                    metadata_source = source_path.with_suffix(".metadata.json")
                    if metadata_source.exists():
                        metadata_dest = dest_path.with_suffix(".metadata.json")

                        # Update metadata with archival info
                        metadata = json.loads(metadata_source.read_text())
                        metadata["archived_at"] = datetime.now().isoformat()
                        metadata["archival_reason"] = candidate["reasons"]
                        metadata["original_tier"] = candidate["tier"]

                        metadata_dest.write_text(json.dumps(metadata, indent=2))
                        metadata_source.unlink()

                    successful.append(candidate)
                    print(f"✅ Archived: {candidate['pattern_name']} from {candidate['agent_name']}/{candidate['tier']}")

            except Exception as e:
                print(f"❌ Error archiving {candidate['pattern_name']}: {e}")
                failed.append(candidate)

        return successful, failed

    def log_archivals(self, successful: List[Dict], failed: List[Dict]):
        """Log archival actions for monitoring"""
        # Load existing log
        log = []
        if self.archival_log.exists():
            log = json.loads(self.archival_log.read_text())

        # Add new entry
        log.append({
            "timestamp": datetime.now().isoformat(),
            "successful_count": len(successful),
            "failed_count": len(failed),
            "successful_patterns": [p["pattern_name"] for p in successful],
            "failed_patterns": [p["pattern_name"] for p in failed],
            "dry_run": self.dry_run
        })

        # Keep last 90 days of history
        log = log[-90:]

        # Save
        self.archival_log.parent.mkdir(parents=True, exist_ok=True)
        self.archival_log.write_text(json.dumps(log, indent=2))

    def print_report(self, candidates: List[Dict]):
        """Print archival candidates report"""
        print("\n" + "=" * 70)
        print("AUTOMATIC ARCHIVAL CANDIDATES")
        print("=" * 70)

        if not candidates:
            print("\n✅ No patterns qualify for archival at this time")
            return

        print(f"\nFound {len(candidates)} patterns qualifying for archival:\n")

        for i, candidate in enumerate(candidates, 1):
            print(f"{i:2d}. {candidate['pattern_name'][:50]:50s}")
            print(f"    Agent: {candidate['agent_name']}/{candidate['tier']}")
            print(f"    Score: {candidate['archival_score']:.2f}")
            print(f"    Age: {candidate['age_days']} days (threshold: {self.AGE_THRESHOLD_DAYS})")
            print(f"    Use count: {candidate['use_count']}, Confidence: {candidate['confidence']}")
            print(f"    Reasons: {candidate['reasons']}")
            print()

        print("=" * 70)


def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Automatically archive low-value patterns"
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview archival without executing")
    parser.add_argument("--report", action="store_true",
                        help="Show archival candidates without archiving")

    args = parser.parse_args()

    engine = AutoArchivalEngine(dry_run=args.dry_run)

    # Scan for candidates
    candidates = engine.scan_archival_candidates()

    if args.report:
        # Just show report
        engine.print_report(candidates)
        return 0

    # Show candidates
    engine.print_report(candidates)

    if not candidates:
        return 0

    # Archive candidates
    print("\n" + "=" * 70)
    print("ARCHIVING LOW-VALUE PATTERNS")
    print("=" * 70)
    print()

    successful, failed = engine.archive_candidates(candidates)

    # Log archivals
    engine.log_archivals(successful, failed)

    # Summary
    print("\n" + "=" * 70)
    print("ARCHIVAL SUMMARY")
    print("=" * 70)
    print(f"{'[DRY RUN] ' if args.dry_run else ''}Archived: {len(successful)} patterns")
    print(f"Failed: {len(failed)} patterns")

    if not args.dry_run and successful:
        print(f"\n✅ Archival log updated: {engine.archival_log}")

    print("=" * 70)

    return 0 if len(failed) == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
