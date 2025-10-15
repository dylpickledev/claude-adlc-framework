#!/usr/bin/env python3
"""
Token Counting Utility for DA Agent Hub Memory System

Uses tiktoken (cl100k_base encoding) to count tokens in markdown files.
Supports caching for performance and provides CLI interface.

Usage:
    python scripts/count-tokens.py <path>                    # Count single file
    python scripts/count-tokens.py <dir> --pattern "*.md"   # Count directory
    python scripts/count-tokens.py <path> --output stats.json  # Save to JSON
"""

import tiktoken
from pathlib import Path
import json
import hashlib
import argparse
import sys
from typing import List, Dict, Optional
from datetime import datetime


class TokenCounter:
    """Token counting utility using tiktoken"""

    def __init__(self, cache_file: Optional[Path] = None):
        """
        Initialize token counter with optional caching.

        Args:
            cache_file: Path to cache file for storing token counts
        """
        self.encoding = tiktoken.get_encoding("cl100k_base")  # Claude tokenizer
        self.cache_file = cache_file or Path(".claude/cache/token-counts.json")
        self.cache = self._load_cache()

    def _load_cache(self) -> Dict:
        """Load token count cache from disk"""
        if self.cache_file.exists():
            try:
                return json.loads(self.cache_file.read_text())
            except json.JSONDecodeError:
                return {}
        return {}

    def _save_cache(self):
        """Save token count cache to disk"""
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        self.cache_file.write_text(json.dumps(self.cache, indent=2))

    def count_tokens(self, text: str) -> int:
        """
        Count tokens in text using tiktoken.

        Args:
            text: Text content to count

        Returns:
            Number of tokens
        """
        return len(self.encoding.encode(text))

    def get_content_hash(self, content: str) -> str:
        """Get MD5 hash of content for cache validation"""
        return hashlib.md5(content.encode('utf-8')).hexdigest()

    def count_file_tokens(self, file_path: Path, use_cache: bool = True) -> Dict:
        """
        Count tokens in a file with optional caching.

        Args:
            file_path: Path to file
            use_cache: Whether to use cached counts

        Returns:
            Dict with path, token_count, content_hash, size_bytes, cached
        """
        # Read file content
        try:
            content = file_path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            # Try latin-1 as fallback
            content = file_path.read_text(encoding='latin-1')
        except Exception as e:
            return {
                "path": str(file_path),
                "error": str(e),
                "token_count": 0
            }

        content_hash = self.get_content_hash(content)
        cache_key = str(file_path)

        # Check cache
        if use_cache and cache_key in self.cache:
            cached_data = self.cache[cache_key]
            if cached_data.get("content_hash") == content_hash:
                return {
                    **cached_data,
                    "cached": True
                }

        # Count tokens
        token_count = self.count_tokens(content)

        # Build result
        result = {
            "path": str(file_path),
            "token_count": token_count,
            "content_hash": content_hash,
            "size_bytes": file_path.stat().st_size,
            "cached": False,
            "counted_at": datetime.now().isoformat()
        }

        # Update cache
        if use_cache:
            self.cache[cache_key] = result
            self._save_cache()

        return result

    def count_directory_tokens(self, dir_path: Path, pattern: str = "*.md", use_cache: bool = True) -> List[Dict]:
        """
        Count tokens for all files in directory matching pattern.

        Args:
            dir_path: Directory to scan
            pattern: File pattern (default: *.md)
            use_cache: Whether to use cached counts

        Returns:
            List of token count results
        """
        results = []
        files = list(dir_path.rglob(pattern))

        print(f"Counting tokens in {len(files)} files...")

        for i, file_path in enumerate(files, 1):
            if file_path.is_file():
                result = self.count_file_tokens(file_path, use_cache=use_cache)
                results.append(result)

                # Progress indicator
                if i % 10 == 0 or i == len(files):
                    cached_count = sum(1 for r in results if r.get("cached", False))
                    print(f"  Processed {i}/{len(files)} files ({cached_count} cached)")

        return results

    def get_summary(self, results: List[Dict]) -> Dict:
        """
        Generate summary statistics from token count results.

        Args:
            results: List of token count results

        Returns:
            Summary statistics
        """
        total_tokens = sum(r["token_count"] for r in results if "error" not in r)
        total_files = len(results)
        successful_files = len([r for r in results if "error" not in r])
        cached_files = sum(1 for r in results if r.get("cached", False))
        errors = [r for r in results if "error" in r]

        return {
            "total_files": total_files,
            "successful_files": successful_files,
            "cached_files": cached_files,
            "errors": len(errors),
            "total_tokens": total_tokens,
            "avg_tokens_per_file": total_tokens / successful_files if successful_files > 0 else 0,
            "min_tokens": min((r["token_count"] for r in results if "error" not in r), default=0),
            "max_tokens": max((r["token_count"] for r in results if "error" not in r), default=0)
        }


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Count tokens in markdown files for DA Agent Hub memory system",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("path", help="File or directory path")
    parser.add_argument("--pattern", default="*.md", help="File pattern for directories (default: *.md)")
    parser.add_argument("--output", help="Output JSON file for results")
    parser.add_argument("--no-cache", action="store_true", help="Disable caching")
    parser.add_argument("--summary-only", action="store_true", help="Show only summary statistics")

    args = parser.parse_args()

    # Initialize counter
    counter = TokenCounter()

    # Resolve path
    path = Path(args.path)
    if not path.exists():
        print(f"❌ Error: Path does not exist: {path}", file=sys.stderr)
        sys.exit(1)

    # Count tokens
    if path.is_file():
        result = counter.count_file_tokens(path, use_cache=not args.no_cache)
        results = [result]
    elif path.is_dir():
        results = counter.count_directory_tokens(path, args.pattern, use_cache=not args.no_cache)
    else:
        print(f"❌ Error: Path is neither file nor directory: {path}", file=sys.stderr)
        sys.exit(1)

    # Generate summary
    summary = counter.get_summary(results)

    # Output results
    output_data = {
        "summary": summary,
        "results": results
    }

    if args.output:
        output_file = Path(args.output)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(json.dumps(output_data, indent=2))
        print(f"\n✅ Results saved to: {output_file}")

    # Display summary
    print("\n" + "=" * 60)
    print("TOKEN COUNT SUMMARY")
    print("=" * 60)
    print(f"Total Files:        {summary['total_files']}")
    print(f"Successful:         {summary['successful_files']}")
    print(f"Cached:             {summary['cached_files']}")
    print(f"Errors:             {summary['errors']}")
    print(f"Total Tokens:       {summary['total_tokens']:,}")
    print(f"Avg Tokens/File:    {summary['avg_tokens_per_file']:.0f}")
    print(f"Min Tokens:         {summary['min_tokens']:,}")
    print(f"Max Tokens:         {summary['max_tokens']:,}")
    print("=" * 60)

    # Display detailed results if not summary-only
    if not args.summary_only and len(results) <= 20:
        print("\nDETAILED RESULTS:")
        print("-" * 60)
        for result in sorted(results, key=lambda r: r.get("token_count", 0), reverse=True):
            if "error" not in result:
                path_display = Path(result["path"]).name
                cached_indicator = " [cached]" if result.get("cached") else ""
                print(f"  {result['token_count']:>6,} tokens - {path_display}{cached_indicator}")
            else:
                print(f"  ERROR: {result['path']} - {result['error']}")

    if not args.summary_only and len(results) > 20:
        print(f"\n(Showing summary only - {len(results)} files is too many for detailed view)")
        print("Use --summary-only flag to suppress this message")

    return 0


if __name__ == "__main__":
    sys.exit(main())
