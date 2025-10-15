#!/usr/bin/env python3
"""
Memory Health Check - Token Monitoring and Alerts

Monitors memory system token usage and alerts when approaching thresholds
that would require implementing Phase 3 (semantic search/retrieval).

Thresholds (per Anthropic guidance):
- <200K tokens: Use prompt caching (current approach)
- 150K tokens: WARNING - Begin planning Phase 3
- 180K tokens: CRITICAL - Implement Phase 3 immediately
- 200K tokens: LIMIT - Must have retrieval in place

Usage:
    python scripts/check-memory-health.py                    # Check current status
    python scripts/check-memory-health.py --history          # Show growth trend
    python scripts/check-memory-health.py --detailed         # Detailed breakdown
"""

from pathlib import Path
import json
from datetime import datetime
from typing import Dict, List
import sys

# Import token counter
import importlib.util
script_dir = Path(__file__).parent
spec = importlib.util.spec_from_file_location("count_tokens", script_dir / "count-tokens.py")
count_tokens = importlib.util.module_from_spec(spec)
spec.loader.exec_module(count_tokens)
TokenCounter = count_tokens.TokenCounter


class MemoryHealthChecker:
    """Monitors memory system health and token usage"""

    # Thresholds per Anthropic guidance
    WARNING_THRESHOLD = 150000  # 75% of 200K
    CRITICAL_THRESHOLD = 180000  # 90% of 200K
    LIMIT_THRESHOLD = 200000     # 100% - must have retrieval

    def __init__(self):
        self.counter = TokenCounter()
        self.base_dir = Path(".claude/memory")
        self.history_file = Path(".claude/cache/memory-health-history.json")

    def count_directory_tokens(self, directory: Path) -> Dict:
        """Count tokens in a directory"""
        total_tokens = 0
        file_count = 0
        files = []

        if not directory.exists():
            return {"total_tokens": 0, "file_count": 0, "files": [], "avg_tokens": 0}

        for pattern_file in directory.glob("**/*.md"):
            if pattern_file.is_file():
                result = self.counter.count_file_tokens(pattern_file)
                total_tokens += result["token_count"]
                file_count += 1
                files.append({
                    "file": pattern_file.name,
                    "tokens": result["token_count"],
                    "path": str(pattern_file.relative_to(self.base_dir))
                })

        avg_tokens = total_tokens / file_count if file_count > 0 else 0

        return {
            "total_tokens": total_tokens,
            "file_count": file_count,
            "files": sorted(files, key=lambda x: x["tokens"], reverse=True),
            "avg_tokens": int(avg_tokens)
        }

    def get_scope_breakdown(self) -> Dict:
        """Get breakdown by agent scopes (Phase 4)"""
        scope_stats = {
            "global": {
                "patterns": self.count_directory_tokens(self.base_dir / "patterns"),
                "recent": self.count_directory_tokens(self.base_dir / "recent")
            },
            "specialists": {},
            "roles": {}
        }

        # Count specialist scopes
        specialists_dir = self.base_dir / "specialists"
        if specialists_dir.exists():
            for agent_dir in specialists_dir.iterdir():
                if agent_dir.is_dir():
                    scope_stats["specialists"][agent_dir.name] = self.count_directory_tokens(agent_dir / "patterns")

        # Count role scopes
        roles_dir = self.base_dir / "roles"
        if roles_dir.exists():
            for role_dir in roles_dir.iterdir():
                if role_dir.is_dir():
                    scope_stats["roles"][role_dir.name] = self.count_directory_tokens(role_dir / "patterns")

        return scope_stats

    def get_memory_status(self) -> Dict:
        """Get current memory system status"""
        # Count tokens in each directory
        recent = self.count_directory_tokens(self.base_dir / "recent")
        intermediate = self.count_directory_tokens(self.base_dir / "intermediate")
        patterns = self.count_directory_tokens(self.base_dir / "patterns")
        archive = self.count_directory_tokens(self.base_dir / "archive")

        # Get scope breakdown (Phase 4)
        scopes = self.get_scope_breakdown()

        # Total
        total_tokens = (recent["total_tokens"] + intermediate["total_tokens"] +
                       patterns["total_tokens"])  # Don't count archive in active memory
        total_files = recent["file_count"] + intermediate["file_count"] + patterns["file_count"]

        # Calculate percentages
        warning_pct = (total_tokens / self.WARNING_THRESHOLD) * 100
        critical_pct = (total_tokens / self.CRITICAL_THRESHOLD) * 100
        limit_pct = (total_tokens / self.LIMIT_THRESHOLD) * 100

        # Determine status
        if total_tokens >= self.LIMIT_THRESHOLD:
            status = "🛑 LIMIT EXCEEDED"
            message = "MUST implement retrieval immediately"
        elif total_tokens >= self.CRITICAL_THRESHOLD:
            status = "🚨 CRITICAL"
            message = "Implement Phase 3 (BM25 retrieval) NOW"
        elif total_tokens >= self.WARNING_THRESHOLD:
            status = "⚠️  WARNING"
            message = "Begin planning Phase 3 implementation"
        else:
            status = "✅ HEALTHY"
            message = "Prompt caching approach optimal"

        return {
            "timestamp": datetime.now().isoformat(),
            "status": status,
            "message": message,
            "total_tokens": total_tokens,
            "total_files": total_files,
            "thresholds": {
                "warning": {"tokens": self.WARNING_THRESHOLD, "pct": warning_pct},
                "critical": {"tokens": self.CRITICAL_THRESHOLD, "pct": critical_pct},
                "limit": {"tokens": self.LIMIT_THRESHOLD, "pct": limit_pct}
            },
            "breakdown": {
                "recent": recent,
                "intermediate": intermediate,
                "patterns": patterns,
                "archive": archive
            }
        }

    def save_history(self, status: Dict):
        """Save status to history file"""
        # Load existing history
        history = []
        if self.history_file.exists():
            history = json.loads(self.history_file.read_text())

        # Add current status (simplified for history)
        history.append({
            "timestamp": status["timestamp"],
            "total_tokens": status["total_tokens"],
            "total_files": status["total_files"],
            "status": status["status"]
        })

        # Keep last 90 days of history (assuming monthly checks)
        history = history[-90:]

        # Save
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        self.history_file.write_text(json.dumps(history, indent=2))

    def show_history(self):
        """Show token growth trend"""
        if not self.history_file.exists():
            print("No history available yet. Run health check first.")
            return

        history = json.loads(self.history_file.read_text())

        if len(history) < 2:
            print("Not enough history for trend analysis. Need at least 2 data points.")
            return

        print("\n" + "=" * 70)
        print("MEMORY GROWTH TREND")
        print("=" * 70)

        # Show historical data
        for entry in history:
            date = entry["timestamp"][:10]  # Just date
            tokens = entry["total_tokens"]
            files = entry["total_files"]
            status = entry["status"]
            print(f"{date}: {tokens:>8,} tokens ({files:>3} files) {status}")

        # Calculate growth
        if len(history) >= 2:
            first = history[0]
            last = history[-1]
            token_growth = last["total_tokens"] - first["total_tokens"]
            file_growth = last["total_files"] - first["total_files"]
            pct_growth = (token_growth / first["total_tokens"]) * 100 if first["total_tokens"] > 0 else 0

            print("\n" + "=" * 70)
            print("GROWTH ANALYSIS")
            print("=" * 70)
            print(f"Token Growth:     {token_growth:+,} tokens ({pct_growth:+.1f}%)")
            print(f"File Growth:      {file_growth:+,} files")

            # Project when thresholds will be reached
            if token_growth > 0 and len(history) >= 3:
                # Calculate days between measurements
                first_date = datetime.fromisoformat(first["timestamp"])
                last_date = datetime.fromisoformat(last["timestamp"])
                days_elapsed = (last_date - first_date).days

                if days_elapsed > 0:
                    tokens_per_day = token_growth / days_elapsed
                    current_tokens = last["total_tokens"]

                    warning_days = (self.WARNING_THRESHOLD - current_tokens) / tokens_per_day if current_tokens < self.WARNING_THRESHOLD else 0
                    critical_days = (self.CRITICAL_THRESHOLD - current_tokens) / tokens_per_day if current_tokens < self.CRITICAL_THRESHOLD else 0
                    limit_days = (self.LIMIT_THRESHOLD - current_tokens) / tokens_per_day if current_tokens < self.LIMIT_THRESHOLD else 0

                    print("\nProjected Timeline:")
                    if warning_days > 0:
                        print(f"  ⚠️  WARNING (150K):  ~{int(warning_days)} days ({int(warning_days/30)} months)")
                    if critical_days > 0:
                        print(f"  🚨 CRITICAL (180K): ~{int(critical_days)} days ({int(critical_days/30)} months)")
                    if limit_days > 0:
                        print(f"  🛑 LIMIT (200K):    ~{int(limit_days)} days ({int(limit_days/30)} months)")

    def print_status(self, status: Dict, detailed: bool = False):
        """Print formatted status"""
        print("\n" + "=" * 70)
        print("MEMORY SYSTEM HEALTH CHECK")
        print("=" * 70)
        print(f"Date: {status['timestamp'][:19]}")
        print(f"Status: {status['status']}")
        print(f"Message: {status['message']}")
        print("")

        # Current usage
        total = status["total_tokens"]
        files = status["total_files"]
        print(f"Total Active Memory: {total:,} tokens ({files} files)")
        print("")

        # Thresholds
        print("Thresholds:")
        for name, data in status["thresholds"].items():
            tokens = data["tokens"]
            pct = data["pct"]
            bar_length = int(pct / 2)  # Scale to 50 chars max
            bar = "█" * min(bar_length, 50)
            symbol = "✅" if pct < 75 else "⚠️ " if pct < 90 else "🚨"
            print(f"  {symbol} {name.upper():10s}: {tokens:>8,} tokens ({pct:>5.1f}%) {bar}")

        # Breakdown
        print("\nMemory Breakdown:")
        breakdown = status["breakdown"]
        for tier, data in breakdown.items():
            if tier == "archive":
                continue  # Don't count archive in active memory
            tokens = data["total_tokens"]
            files = data["file_count"]
            avg = data["avg_tokens"]
            print(f"  {tier:15s}: {tokens:>8,} tokens ({files:>3} files, avg {avg:>5,}/file)")

        # Archive (informational)
        archive = breakdown["archive"]
        if archive["file_count"] > 0:
            print(f"\n  {'archive':15s}: {archive['total_tokens']:>8,} tokens ({archive['file_count']:>3} files) [not counted in active]")

        # Phase 4: Scope breakdown
        print("\n" + "=" * 70)
        print("PHASE 4: AGENT-SPECIFIC SCOPE BREAKDOWN")
        print("=" * 70)

        scope_stats = self.get_scope_breakdown()

        # Global scope
        global_patterns = scope_stats["global"]["patterns"]["total_tokens"]
        global_recent = scope_stats["global"]["recent"]["total_tokens"]
        global_total = global_patterns + global_recent
        global_files = scope_stats["global"]["patterns"]["file_count"] + scope_stats["global"]["recent"]["file_count"]

        print(f"\n🌍 Global Scope:")
        print(f"  Total:    {global_total:>8,} tokens ({global_files:>3} files)")
        print(f"  Patterns: {global_patterns:>8,} tokens ({scope_stats['global']['patterns']['file_count']:>3} files)")
        print(f"  Recent:   {global_recent:>8,} tokens ({scope_stats['global']['recent']['file_count']:>3} files)")

        # Specialists scope
        specialist_total_tokens = sum(data["total_tokens"] for data in scope_stats["specialists"].values())
        specialist_total_files = sum(data["file_count"] for data in scope_stats["specialists"].values())
        specialist_count = len(scope_stats["specialists"])

        print(f"\n🎯 Specialists Scope ({specialist_count} agents):")
        print(f"  Total:    {specialist_total_tokens:>8,} tokens ({specialist_total_files:>3} files)")

        if scope_stats["specialists"]:
            # Show top 5 specialists by token count
            top_specialists = sorted(
                scope_stats["specialists"].items(),
                key=lambda x: x[1]["total_tokens"],
                reverse=True
            )[:5]

            print(f"\n  Top 5 Specialists by Token Count:")
            for i, (agent, data) in enumerate(top_specialists, 1):
                print(f"    {i}. {agent:30s} {data['total_tokens']:>8,} tokens ({data['file_count']:>3} files)")

        # Roles scope
        role_total_tokens = sum(data["total_tokens"] for data in scope_stats["roles"].values())
        role_total_files = sum(data["file_count"] for data in scope_stats["roles"].values())
        role_count = len(scope_stats["roles"])

        print(f"\n👥 Roles Scope ({role_count} agents):")
        print(f"  Total:    {role_total_tokens:>8,} tokens ({role_total_files:>3} files)")

        if scope_stats["roles"]:
            # Show top 5 roles by token count
            top_roles = sorted(
                scope_stats["roles"].items(),
                key=lambda x: x[1]["total_tokens"],
                reverse=True
            )[:5]

            print(f"\n  Top 5 Roles by Token Count:")
            for i, (role, data) in enumerate(top_roles, 1):
                print(f"    {i}. {role:30s} {data['total_tokens']:>8,} tokens ({data['file_count']:>3} files)")

        # Total scope stats
        total_scope_tokens = specialist_total_tokens + role_total_tokens
        total_scope_files = specialist_total_files + role_total_files

        print(f"\n📊 Scope Summary:")
        print(f"  Global:      {global_total:>8,} tokens ({global_files:>3} files)")
        print(f"  Agent-Specific: {total_scope_tokens:>8,} tokens ({total_scope_files:>3} files)")
        print(f"  TOTAL:       {global_total + total_scope_tokens:>8,} tokens ({global_files + total_scope_files:>3} files)")

        if detailed:
            print("\n" + "=" * 70)
            print("DETAILED FILE BREAKDOWN (Top 10 Largest)")
            print("=" * 70)

            # Collect all files
            all_files = []
            for tier, data in breakdown.items():
                for file_info in data["files"]:
                    file_info["tier"] = tier
                    all_files.append(file_info)

            # Sort by size
            all_files.sort(key=lambda x: x["tokens"], reverse=True)

            # Show top 10
            for i, file_info in enumerate(all_files[:10], 1):
                print(f"{i:2d}. {file_info['file']:40s} {file_info['tokens']:>6,} tokens [{file_info['tier']}]")

        print("\n" + "=" * 70)
        print("NEXT ACTIONS")
        print("=" * 70)

        if total >= self.LIMIT_THRESHOLD:
            print("🛑 IMMEDIATE ACTION REQUIRED:")
            print("  1. Implement Phase 3 (BM25 retrieval) NOW")
            print("  2. Review: .claude/tasks/semantic-search-research/bm25-future-implementation.md")
            print("  3. Install bm25s library and build retrieval system")
        elif total >= self.CRITICAL_THRESHOLD:
            print("🚨 CRITICAL - ACTION NEEDED THIS WEEK:")
            print("  1. Schedule Phase 3 implementation immediately")
            print("  2. Begin BM25 retrieval development")
            print("  3. Test with current memory corpus")
        elif total >= self.WARNING_THRESHOLD:
            print("⚠️  WARNING - PLAN AHEAD:")
            print("  1. Review Phase 3 implementation guide")
            print("  2. Schedule development time in next sprint")
            print("  3. Test BM25 approach with sample data")
        else:
            print("✅ ALL GOOD:")
            print("  1. Current approach (prompt caching) is optimal")
            print("  2. Continue monthly health checks")
            print("  3. Phase 3 not needed yet")

        print("=" * 70)


def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Check memory system health and token usage"
    )
    parser.add_argument("--history", action="store_true", help="Show growth trend")
    parser.add_argument("--detailed", action="store_true", help="Show detailed file breakdown")

    args = parser.parse_args()

    checker = MemoryHealthChecker()

    if args.history:
        checker.show_history()
    else:
        # Get and save status
        status = checker.get_memory_status()
        checker.save_history(status)

        # Print status
        checker.print_status(status, detailed=args.detailed)


if __name__ == "__main__":
    sys.exit(main() if main() is not None else 0)
