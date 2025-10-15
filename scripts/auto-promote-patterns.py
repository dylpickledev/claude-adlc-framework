#!/usr/bin/env python3
"""
Automated Pattern Promotion Engine

Automatically promotes agent-specific patterns to global scope when they
prove valuable across multiple agents.

Promotion Criteria:
- use_count >= 3 (used by multiple agents)
- confidence >= 0.85 (high quality)
- Cross-agent usage detected

Usage:
    python scripts/auto-promote-patterns.py              # Auto-promote qualified patterns
    python scripts/auto-promote-patterns.py --dry-run    # Preview promotions
    python scripts/auto-promote-patterns.py --report     # Show promotion candidates
"""

from pathlib import Path
import json
import sys
from datetime import datetime
from typing import List, Dict, Tuple
import shutil

# Import promote-to-global functionality
import importlib.util
script_dir = Path(__file__).parent
spec = importlib.util.spec_from_file_location("promote_to_global", script_dir / "promote-to-global.py")
promote_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(promote_module)
promote_pattern_to_global = promote_module.promote_pattern_to_global


class AutoPromotionEngine:
    """Automated pattern promotion based on usage and quality"""

    def __init__(self, dry_run: bool = False):
        self.base_dir = Path(".claude/memory")
        self.dry_run = dry_run
        self.promotion_log = Path(".claude/cache/auto-promotions.json")

    def scan_promotion_candidates(self) -> List[Dict]:
        """Scan all agent-specific patterns for promotion candidates

        Returns list of candidates with metadata
        """
        candidates = []

        for agent_type in ["specialists", "roles"]:
            agents_dir = self.base_dir / agent_type

            if not agents_dir.exists():
                continue

            for agent_dir in agents_dir.iterdir():
                if not agent_dir.is_dir():
                    continue

                agent_name = agent_dir.name
                patterns_dir = agent_dir / "patterns"

                if not patterns_dir.exists():
                    continue

                for pattern_file in patterns_dir.glob("*.md"):
                    metadata_file = pattern_file.with_suffix(".metadata.json")

                    if not metadata_file.exists():
                        continue

                    metadata = json.loads(metadata_file.read_text())

                    # Check promotion criteria
                    use_count = metadata.get("use_count", 0)
                    confidence = metadata.get("confidence")

                    # Criteria: use_count >= 3 OR confidence >= 0.85
                    qualifies = False
                    reason = []

                    if use_count >= 3:
                        qualifies = True
                        reason.append(f"use_count={use_count} >= 3")

                    if confidence is not None and confidence >= 0.85:
                        qualifies = True
                        reason.append(f"confidence={confidence:.2f} >= 0.85")

                    # Additional check: cross-agent usage if tracked
                    used_by_agents = metadata.get("used_by_agents", [])
                    if len(used_by_agents) >= 2:
                        qualifies = True
                        reason.append(f"used_by {len(used_by_agents)} agents")

                    if qualifies:
                        # Check if already exists in global
                        global_path = self.base_dir / "patterns" / pattern_file.name
                        if global_path.exists():
                            continue  # Skip if already in global

                        candidates.append({
                            "agent_type": agent_type,
                            "agent_name": agent_name,
                            "pattern_name": pattern_file.name,
                            "pattern_path": str(pattern_file),
                            "use_count": use_count,
                            "confidence": confidence,
                            "used_by_agents": used_by_agents,
                            "reason": ", ".join(reason),
                            "promotion_score": self.calculate_promotion_score(metadata)
                        })

        # Sort by promotion score
        candidates.sort(key=lambda x: x["promotion_score"], reverse=True)

        return candidates

    def calculate_promotion_score(self, metadata: Dict) -> float:
        """Calculate promotion score (0-1) based on metadata

        Higher score = higher priority for promotion
        """
        score = 0.0

        # Use count component (max 0.4)
        use_count = metadata.get("use_count", 0)
        score += min(use_count / 10.0, 0.4)

        # Confidence component (max 0.4)
        confidence = metadata.get("confidence", 0.0)
        if confidence:
            score += confidence * 0.4

        # Cross-agent usage component (max 0.2)
        used_by_agents = metadata.get("used_by_agents", [])
        score += min(len(used_by_agents) / 5.0, 0.2) * 0.2

        return min(score, 1.0)

    def promote_candidates(self, candidates: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
        """Promote qualified candidates to global scope

        Returns (successful_promotions, failed_promotions)
        """
        successful = []
        failed = []

        for candidate in candidates:
            try:
                if self.dry_run:
                    print(f"[DRY RUN] Would promote: {candidate['pattern_name']} from {candidate['agent_name']}")
                    successful.append(candidate)
                else:
                    # Use existing promote-to-global functionality
                    success = promote_pattern_to_global(
                        agent_type=candidate["agent_type"],
                        agent_name=candidate["agent_name"],
                        pattern_name=candidate["pattern_name"],
                        force=True  # Auto-promotion bypasses criteria checks
                    )

                    if success:
                        successful.append(candidate)
                        print(f"✅ Promoted: {candidate['pattern_name']} from {candidate['agent_name']}")
                    else:
                        failed.append(candidate)
                        print(f"❌ Failed to promote: {candidate['pattern_name']}")

            except Exception as e:
                print(f"❌ Error promoting {candidate['pattern_name']}: {e}")
                failed.append(candidate)

        return successful, failed

    def log_promotions(self, successful: List[Dict], failed: List[Dict]):
        """Log promotion actions for monitoring"""
        # Load existing log
        log = []
        if self.promotion_log.exists():
            log = json.loads(self.promotion_log.read_text())

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
        self.promotion_log.parent.mkdir(parents=True, exist_ok=True)
        self.promotion_log.write_text(json.dumps(log, indent=2))

    def print_report(self, candidates: List[Dict]):
        """Print promotion candidates report"""
        print("\n" + "=" * 70)
        print("AUTOMATIC PROMOTION CANDIDATES")
        print("=" * 70)

        if not candidates:
            print("\n✅ No patterns qualify for promotion at this time")
            return

        print(f"\nFound {len(candidates)} patterns qualifying for promotion:\n")

        for i, candidate in enumerate(candidates, 1):
            print(f"{i:2d}. {candidate['pattern_name'][:50]:50s}")
            print(f"    Agent: {candidate['agent_name']}")
            print(f"    Score: {candidate['promotion_score']:.2f}")
            print(f"    Reason: {candidate['reason']}")
            print(f"    Use count: {candidate['use_count']}, Confidence: {candidate['confidence']}")
            if candidate.get('used_by_agents'):
                print(f"    Used by: {', '.join(candidate['used_by_agents'])}")
            print()

        print("=" * 70)


def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Automatically promote agent-specific patterns to global scope"
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview promotions without executing")
    parser.add_argument("--report", action="store_true",
                        help="Show promotion candidates without promoting")

    args = parser.parse_args()

    engine = AutoPromotionEngine(dry_run=args.dry_run)

    # Scan for candidates
    candidates = engine.scan_promotion_candidates()

    if args.report:
        # Just show report
        engine.print_report(candidates)
        return 0

    # Show candidates
    engine.print_report(candidates)

    if not candidates:
        return 0

    # Promote candidates
    print("\n" + "=" * 70)
    print("PROMOTING PATTERNS TO GLOBAL SCOPE")
    print("=" * 70)
    print()

    successful, failed = engine.promote_candidates(candidates)

    # Log promotions
    engine.log_promotions(successful, failed)

    # Summary
    print("\n" + "=" * 70)
    print("PROMOTION SUMMARY")
    print("=" * 70)
    print(f"{'[DRY RUN] ' if args.dry_run else ''}Promoted: {len(successful)} patterns")
    print(f"Failed: {len(failed)} patterns")

    if not args.dry_run and successful:
        print(f"\n✅ Promotion log updated: {engine.promotion_log}")

    print("=" * 70)

    return 0 if len(failed) == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
