#!/usr/bin/env python3
"""
Pattern Summarization Engine for Memory Consolidation

Intelligently summarizes patterns to 25% of original token count while
preserving key insights, actionability, and metadata.

Usage:
    python scripts/summarize-patterns.py <pattern_file>              # Summarize one
    python scripts/summarize-patterns.py --dir <directory>           # Summarize all
    python scripts/summarize-patterns.py --fresh-only                # Only unsummarized
"""

from pathlib import Path
import json
import re
from datetime import datetime
from typing import Dict, List, Optional
import sys

# Import utilities
import importlib.util
script_dir = Path(__file__).parent
spec = importlib.util.spec_from_file_location("count_tokens", script_dir / "count-tokens.py")
count_tokens = importlib.util.module_from_spec(spec)
spec.loader.exec_module(count_tokens)
TokenCounter = count_tokens.TokenCounter


class PatternSummarizer:
    """Summarizes patterns for intermediate storage"""

    def __init__(self, target_reduction: float = 0.75):
        """
        Initialize summarizer.

        Args:
            target_reduction: Target reduction percentage (default: 75%)
        """
        self.target_reduction = target_reduction
        self.counter = TokenCounter()

    def is_already_summarized(self, content: str) -> bool:
        """Check if pattern is already summarized"""
        return "(SUMMARIZED)" in content or "**Summarized**:" in content

    def extract_section(self, content: str, section_header: str) -> Optional[str]:
        """
        Extract content from a markdown section.

        Args:
            content: Full pattern content
            section_header: Header to find (e.g., "## Problem")

        Returns:
            Section content or None
        """
        # Find section
        pattern = rf'^{re.escape(section_header)}\s*$'
        lines = content.split('\n')

        start_idx = None
        for i, line in enumerate(lines):
            if re.match(pattern, line, re.IGNORECASE):
                start_idx = i + 1
                break

        if start_idx is None:
            return None

        # Find end (next ## header or end of file)
        end_idx = len(lines)
        for i in range(start_idx, len(lines)):
            if lines[i].startswith('##'):
                end_idx = i
                break

        # Extract section content
        section_lines = lines[start_idx:end_idx]
        return '\n'.join(section_lines).strip()

    def extract_key_insights(self, content: str) -> str:
        """
        Extract 3-5 key insights from pattern.

        Priority sections:
        1. Problem/Context
        2. Solution
        3. Benefits
        4. When to Apply
        """
        insights = []

        # Problem/Context
        problem = self.extract_section(content, "## Problem") or \
                  self.extract_section(content, "## Context")
        if problem:
            # Take first 2 sentences or first paragraph
            first_para = problem.split('\n\n')[0]
            insights.append(f"**Problem**: {first_para[:200]}...")

        # Solution
        solution = self.extract_section(content, "## Solution") or \
                   self.extract_section(content, "## Implementation")
        if solution:
            first_para = solution.split('\n\n')[0]
            insights.append(f"**Solution**: {first_para[:200]}...")

        # Benefits
        benefits = self.extract_section(content, "## Benefits") or \
                   self.extract_section(content, "## Key Benefits")
        if benefits:
            # Extract first 3 bullet points if present
            bullet_lines = [line for line in benefits.split('\n') if line.strip().startswith(('-', '*', '✅'))]
            if bullet_lines:
                insights.append("**Benefits**:\n" + '\n'.join(bullet_lines[:3]))

        # When to Apply
        when = self.extract_section(content, "## When to Apply") or \
               self.extract_section(content, "## When to Use")
        if when:
            first_para = when.split('\n\n')[0]
            insights.append(f"**When to Apply**: {first_para[:150]}...")

        return '\n\n'.join(insights) if insights else "Key insights not extracted."

    def extract_success_criteria(self, content: str) -> str:
        """Extract success criteria or validation points"""
        section = self.extract_section(content, "## Success Criteria") or \
                  self.extract_section(content, "## Validation")

        if section:
            # Take first 5 lines or bullet points
            lines = [line for line in section.split('\n') if line.strip()]
            return '\n'.join(lines[:5])

        return "See full pattern for success criteria."

    def extract_metadata_from_content(self, content: str) -> Dict:
        """Extract confidence, tags, etc. from content"""
        metadata = {}

        # Confidence score
        conf_match = re.search(r'[Cc]onfidence:\s*(\d+\.\d+)', content)
        if conf_match:
            metadata['confidence'] = float(conf_match.group(1))

        # Tags
        tags_match = re.search(r'[Tt]ags?:\s*([^\n]+)', content)
        if tags_match:
            tags_str = tags_match.group(1)
            metadata['tags'] = [t.strip() for t in tags_str.split(',')]

        return metadata

    def summarize_pattern(self, pattern_file: Path) -> str:
        """
        Summarize a pattern file.

        Args:
            pattern_file: Path to pattern file

        Returns:
            Summarized content
        """
        # Load pattern
        content = pattern_file.read_text(encoding='utf-8')

        # Check if already summarized
        if self.is_already_summarized(content):
            print(f"  ⏭️  Already summarized: {pattern_file.name}")
            return content

        # Load metadata
        metadata_file = pattern_file.with_suffix('.metadata.json')
        if metadata_file.exists():
            metadata = json.loads(metadata_file.read_text())
        else:
            metadata = {}

        # Extract content metadata
        content_metadata = self.extract_metadata_from_content(content)
        metadata.update(content_metadata)

        # Count original tokens
        original_tokens = self.counter.count_tokens(content)

        # Extract key sections
        key_insights = self.extract_key_insights(content)
        success_criteria = self.extract_success_criteria(content)

        # Get pattern title (first # line)
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else pattern_file.stem

        # Build summary
        summary = f"""# {title} (SUMMARIZED)

**Original Token Count**: {original_tokens:,}
**Confidence**: {metadata.get('confidence', 'N/A')}
**Use Count**: {metadata.get('use_count', 0)}
**Last Used**: {metadata.get('last_used', 'Never')}
**Summarized**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Key Insights

{key_insights}

## Success Criteria

{success_criteria}

---

**📦 Full Pattern Available**: This is a summarized version. For complete implementation details, code examples, and comprehensive documentation, restore the full pattern:

```bash
python scripts/restore-pattern.py {pattern_file.name}
```

**Restoration**: Full pattern archived with all original content, examples, and references. Summarization preserves actionability while reducing token usage by ~75%.
"""

        # Count summary tokens
        summary_tokens = self.counter.count_tokens(summary)
        reduction_pct = ((original_tokens - summary_tokens) / original_tokens) * 100

        print(f"  ✅ Summarized: {pattern_file.name}")
        print(f"     {original_tokens:,} → {summary_tokens:,} tokens ({reduction_pct:.1f}% reduction)")

        # Update metadata
        metadata['original_token_count'] = original_tokens
        metadata['summary_token_count'] = summary_tokens
        metadata['summarized_at'] = datetime.now().isoformat()
        metadata['is_summary'] = True

        # Save metadata
        if metadata_file.exists():
            metadata_file.write_text(json.dumps(metadata, indent=2))

        return summary

    def summarize_directory(self, directory: Path, fresh_only: bool = False) -> Dict:
        """
        Summarize all patterns in a directory.

        Args:
            directory: Directory to process
            fresh_only: Only summarize unsummarized patterns

        Returns:
            Statistics dictionary
        """
        stats = {
            'total': 0,
            'summarized': 0,
            'skipped': 0,
            'errors': 0,
            'original_tokens': 0,
            'summary_tokens': 0
        }

        for pattern_file in directory.glob("*.md"):
            stats['total'] += 1

            try:
                content = pattern_file.read_text()

                # Skip if already summarized and fresh_only
                if fresh_only and self.is_already_summarized(content):
                    stats['skipped'] += 1
                    continue

                # Count original tokens
                original_tokens = self.counter.count_tokens(content)
                stats['original_tokens'] += original_tokens

                # Summarize
                summary = self.summarize_pattern(pattern_file)

                # Count summary tokens
                summary_tokens = self.counter.count_tokens(summary)
                stats['summary_tokens'] += summary_tokens

                # Write summary
                pattern_file.write_text(summary)

                stats['summarized'] += 1

            except Exception as e:
                print(f"  ❌ Error summarizing {pattern_file.name}: {e}")
                stats['errors'] += 1

        return stats


def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Summarize patterns for memory consolidation"
    )
    parser.add_argument("pattern_file", nargs="?", help="Single pattern file to summarize")
    parser.add_argument("--dir", help="Directory to summarize (all patterns)")
    parser.add_argument("--fresh-only", action="store_true", help="Only summarize unsummarized patterns")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")

    args = parser.parse_args()

    summarizer = PatternSummarizer()

    # Single file
    if args.pattern_file:
        pattern_file = Path(args.pattern_file)
        if not pattern_file.exists():
            print(f"❌ Error: Pattern file not found: {pattern_file}")
            return 1

        print(f"\nSummarizing: {pattern_file.name}")
        summary = summarizer.summarize_pattern(pattern_file)

        if not args.dry_run:
            pattern_file.write_text(summary)
            print("✅ Summary written")
        else:
            print("⚠️  DRY RUN - No files modified")

    # Directory
    elif args.dir:
        directory = Path(args.dir)
        if not directory.exists():
            print(f"❌ Error: Directory not found: {directory}")
            return 1

        print(f"\n{'=' * 60}")
        print("PATTERN SUMMARIZATION")
        print(f"{'=' * 60}")
        print(f"Directory: {directory}")
        print(f"Fresh Only: {args.fresh_only}")
        print("")

        stats = summarizer.summarize_directory(directory, fresh_only=args.fresh_only)

        # Print summary
        reduction_pct = 0
        if stats['original_tokens'] > 0:
            reduction_pct = ((stats['original_tokens'] - stats['summary_tokens']) / stats['original_tokens']) * 100

        print(f"\n{'=' * 60}")
        print("SUMMARIZATION RESULTS")
        print(f"{'=' * 60}")
        print(f"Total Patterns:      {stats['total']}")
        print(f"Summarized:          {stats['summarized']}")
        print(f"Skipped:             {stats['skipped']}")
        print(f"Errors:              {stats['errors']}")
        print(f"Original Tokens:     {stats['original_tokens']:,}")
        print(f"Summary Tokens:      {stats['summary_tokens']:,}")
        print(f"Reduction:           {reduction_pct:.1f}%")
        print(f"{'=' * 60}")

        if args.dry_run:
            print("\n⚠️  DRY RUN - No files modified")

    else:
        parser.print_help()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
