# Phase 1: Token-Aware Memory Loading - Implementation Tasks

## Overview

**Goal**: Implement token counting and budget system to reduce context noise by 40-60%
**Timeline**: Weeks 1-2 (2025-01-14 to 2025-01-28)
**Status**: In Progress

## Success Criteria

✅ Token counting utility functional
✅ Memory budget system enforced
✅ Relevance scoring implemented
✅ 40-60% context reduction measured
✅ No regression in pattern access
✅ Documentation updated

## Detailed Tasks

### Task 1: Create Token Counting Utility
**Status**: Pending
**Est. Time**: 2 hours

**Requirements**:
- Use tiktoken library (cl100k_base encoding for Claude)
- Count tokens for markdown files
- Handle files with code blocks, tables, special characters
- Cache token counts to avoid repeated processing
- CLI interface for ad-hoc counting

**Implementation**:
```python
# scripts/count-tokens.py

import tiktoken
from pathlib import Path
import json
import hashlib

def count_tokens(text: str, model: str = "claude-3-5-sonnet") -> int:
    """Count tokens using tiktoken (cl100k_base for Claude)"""
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))

def count_file_tokens(file_path: Path) -> dict:
    """Count tokens in a file and return metadata"""
    content = file_path.read_text(encoding='utf-8')
    token_count = count_tokens(content)
    content_hash = hashlib.md5(content.encode()).hexdigest()

    return {
        "path": str(file_path),
        "token_count": token_count,
        "content_hash": content_hash,
        "size_bytes": file_path.stat().st_size
    }

def count_directory_tokens(dir_path: Path, pattern: str = "*.md") -> list:
    """Count tokens for all files in directory matching pattern"""
    results = []
    for file_path in dir_path.rglob(pattern):
        if file_path.is_file():
            results.append(count_file_tokens(file_path))
    return results

# CLI interface
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Count tokens in markdown files")
    parser.add_argument("path", help="File or directory path")
    parser.add_argument("--pattern", default="*.md", help="File pattern for directories")
    parser.add_argument("--output", help="Output JSON file")

    args = parser.parse_args()
    # ... implementation
```

**Testing**:
- [ ] Test with single pattern file
- [ ] Test with entire `.claude/memory/patterns/` directory
- [ ] Test with specialist agent files
- [ ] Verify cache works (repeated counts use cache)
- [ ] Validate token counts are accurate

**Deliverable**: `scripts/count-tokens.py` with tests

---

### Task 2: Implement Memory Budget System
**Status**: Pending
**Est. Time**: 3 hours

**Requirements**:
- Track current token usage
- Enforce 20k token budget
- Priority-based loading (relevance score)
- Graceful handling when budget exhausted
- Logging of what was loaded/skipped

**Implementation**:
```python
# scripts/memory-budget.py

from dataclasses import dataclass
from typing import List, Optional
from pathlib import Path
import json

@dataclass
class Pattern:
    path: Path
    token_count: int
    relevance_score: float
    content: str
    metadata: dict

class MemoryBudget:
    def __init__(self, max_tokens: int = 20000):
        self.max_tokens = max_tokens
        self.current_tokens = 0
        self.loaded_patterns: List[Pattern] = []
        self.skipped_patterns: List[Pattern] = []

    def can_load(self, pattern: Pattern) -> bool:
        """Check if pattern can be loaded within budget"""
        return self.current_tokens + pattern.token_count <= self.max_tokens

    def add_pattern(self, pattern: Pattern) -> bool:
        """Attempt to add pattern to budget"""
        if self.can_load(pattern):
            self.loaded_patterns.append(pattern)
            self.current_tokens += pattern.token_count
            return True
        else:
            self.skipped_patterns.append(pattern)
            return False

    def get_stats(self) -> dict:
        """Get budget utilization statistics"""
        return {
            "max_tokens": self.max_tokens,
            "used_tokens": self.current_tokens,
            "utilization_pct": (self.current_tokens / self.max_tokens) * 100,
            "loaded_count": len(self.loaded_patterns),
            "skipped_count": len(self.skipped_patterns),
            "loaded_patterns": [p.path.name for p in self.loaded_patterns],
            "skipped_patterns": [p.path.name for p in self.skipped_patterns]
        }

    def load_patterns_with_budget(self, patterns: List[Pattern]) -> List[Pattern]:
        """Load patterns respecting budget, prioritized by relevance"""
        # Sort by relevance score (highest first)
        sorted_patterns = sorted(patterns, key=lambda p: p.relevance_score, reverse=True)

        for pattern in sorted_patterns:
            self.add_pattern(pattern)

        return self.loaded_patterns
```

**Testing**:
- [ ] Test budget enforcement (exceed budget)
- [ ] Test priority loading (high relevance first)
- [ ] Test with realistic pattern set (100+ patterns)
- [ ] Verify statistics are accurate
- [ ] Test edge cases (empty, single pattern, exact budget)

**Deliverable**: `scripts/memory-budget.py` with tests

---

### Task 3: Create Relevance Scoring Algorithm
**Status**: Pending
**Est. Time**: 4 hours

**Requirements**:
- Recency score (when pattern was last used/updated)
- Usage score (how often pattern has been applied)
- Context score (relevance to current task/agent)
- Weighted combination (configurable weights)
- Handle missing metadata gracefully

**Implementation**:
```python
# scripts/relevance-scoring.py

from datetime import datetime, timedelta
from pathlib import Path
import json
from typing import Optional

class RelevanceScorer:
    def __init__(self, recency_weight: float = 0.3,
                 usage_weight: float = 0.3,
                 context_weight: float = 0.4):
        self.recency_weight = recency_weight
        self.usage_weight = usage_weight
        self.context_weight = context_weight

    def calculate_recency_score(self, last_used: Optional[datetime]) -> float:
        """Score 0-1 based on recency (exponential decay)"""
        if last_used is None:
            return 0.5  # Default for unknown

        days_ago = (datetime.now() - last_used).days

        # Exponential decay: recent = 1.0, 30 days = 0.5, 90+ days = 0.1
        if days_ago == 0:
            return 1.0
        elif days_ago <= 30:
            return 1.0 - (days_ago / 30) * 0.5
        else:
            return max(0.1, 0.5 - ((days_ago - 30) / 60) * 0.4)

    def calculate_usage_score(self, use_count: Optional[int]) -> float:
        """Score 0-1 based on usage frequency (logarithmic)"""
        if use_count is None or use_count == 0:
            return 0.3  # Default for unused

        # Logarithmic scale: 1 use = 0.5, 10 uses = 0.8, 100+ uses = 1.0
        import math
        return min(1.0, 0.5 + (math.log10(use_count) / 2) * 0.5)

    def calculate_context_score(self, pattern: Pattern, context: dict) -> float:
        """Score 0-1 based on context relevance"""
        score = 0.5  # Default baseline

        # Agent match
        if context.get("agent_name"):
            if context["agent_name"] in str(pattern.path):
                score += 0.3

        # Technology/tool match
        if context.get("technologies"):
            pattern_content_lower = pattern.content.lower()
            matches = sum(1 for tech in context["technologies"]
                         if tech.lower() in pattern_content_lower)
            score += min(0.2, matches * 0.05)

        # Task type match
        if context.get("task_type"):
            if context["task_type"].lower() in pattern.content.lower():
                score += 0.2

        return min(1.0, score)

    def calculate_relevance(self, pattern: Pattern, context: dict) -> float:
        """Calculate overall relevance score (0-1)"""
        recency = self.calculate_recency_score(pattern.metadata.get("last_used"))
        usage = self.calculate_usage_score(pattern.metadata.get("use_count"))
        context_match = self.calculate_context_score(pattern, context)

        relevance = (
            self.recency_weight * recency +
            self.usage_weight * usage +
            self.context_weight * context_match
        )

        return relevance
```

**Testing**:
- [ ] Test recency scoring (recent vs. old)
- [ ] Test usage scoring (never used vs. heavily used)
- [ ] Test context scoring (agent match, tech match)
- [ ] Test weighted combination
- [ ] Test edge cases (missing metadata)

**Deliverable**: `scripts/relevance-scoring.py` with tests

---

### Task 4: Add Token Metadata to Existing Patterns
**Status**: Pending
**Est. Time**: 2 hours

**Requirements**:
- Scan all existing patterns
- Add token counts to metadata
- Initialize usage tracking (use_count: 0, last_used: null)
- Create metadata JSON files alongside patterns
- Handle patterns without metadata gracefully

**Implementation**:
```python
# scripts/add-token-metadata.py

from pathlib import Path
import json
from count_tokens import count_file_tokens

def add_metadata_to_patterns(base_dir: Path = Path(".claude/memory")):
    """Add token metadata to all existing patterns"""
    for pattern_file in base_dir.rglob("*.md"):
        metadata_file = pattern_file.with_suffix(".metadata.json")

        # Skip if metadata already exists
        if metadata_file.exists():
            continue

        # Count tokens
        token_data = count_file_tokens(pattern_file)

        # Initialize metadata
        metadata = {
            "pattern_file": pattern_file.name,
            "token_count": token_data["token_count"],
            "content_hash": token_data["content_hash"],
            "use_count": 0,
            "last_used": None,
            "created_at": pattern_file.stat().st_mtime,
            "confidence": None,  # To be extracted from content if present
        }

        # Write metadata
        metadata_file.write_text(json.dumps(metadata, indent=2))

if __name__ == "__main__":
    add_metadata_to_patterns()
    print("✅ Token metadata added to all patterns")
```

**Testing**:
- [ ] Test on `.claude/memory/patterns/`
- [ ] Test on `.claude/memory/recent/`
- [ ] Verify metadata files created
- [ ] Verify token counts are accurate
- [ ] Test idempotency (re-running doesn't duplicate)

**Deliverable**: Metadata files for all existing patterns

---

### Task 5: Measure Baseline Metrics
**Status**: Pending
**Est. Time**: 1 hour

**Requirements**:
- Count total tokens in current memory system
- Count patterns loaded per agent invocation (simulated)
- Measure current context usage
- Document baseline for comparison

**Metrics to Capture**:
```json
{
  "baseline_metrics": {
    "total_patterns": 50,
    "total_tokens": 150000,
    "avg_tokens_per_pattern": 3000,
    "patterns_loaded_per_invocation": {
      "analytics-engineer": 35,
      "dbt-expert": 28,
      "snowflake-expert": 22
    },
    "tokens_loaded_per_invocation": {
      "analytics-engineer": 105000,
      "dbt-expert": 84000,
      "snowflake-expert": 66000
    },
    "context_utilization_pct": {
      "analytics-engineer": 52.5,
      "dbt-expert": 42.0,
      "snowflake-expert": 33.0
    }
  }
}
```

**Script**:
```python
# scripts/measure-baseline.py

def measure_baseline():
    """Measure current memory system baseline"""
    patterns_dir = Path(".claude/memory/patterns")
    recent_dir = Path(".claude/memory/recent")

    # Count all patterns
    all_patterns = list(patterns_dir.glob("*.md")) + list(recent_dir.glob("*.md"))

    # ... measure and save
```

**Deliverable**: `projects/active/ai-memory-system-improvements/tasks/baseline-metrics.json`

---

### Task 6: Integration and Testing
**Status**: Pending
**Est. Time**: 3 hours

**Requirements**:
- Integrate all components
- Test end-to-end workflow
- Simulate agent invocations with budget
- Validate 40-60% reduction target
- Handle edge cases

**Test Scenarios**:
1. **Analytics Engineer task**: Load dbt + snowflake patterns with budget
2. **Specialist consultation**: Load scoped patterns within budget
3. **Budget exhaustion**: Gracefully handle when budget reached
4. **Empty context**: Default scoring when no context provided
5. **All patterns relevant**: Budget prioritization works

**Deliverable**: Integration tests passing

---

### Task 7: Measure After Metrics
**Status**: Pending
**Est. Time**: 1 hour

**Requirements**:
- Re-measure with budget system active
- Compare to baseline
- Validate 40-60% reduction achieved
- Document findings

**Metrics to Capture**:
```json
{
  "after_metrics": {
    "total_patterns": 50,
    "total_tokens": 150000,
    "budget_max_tokens": 20000,
    "patterns_loaded_per_invocation": {
      "analytics-engineer": 12,
      "dbt-expert": 10,
      "snowflake-expert": 9
    },
    "tokens_loaded_per_invocation": {
      "analytics-engineer": 19500,
      "dbt-expert": 18200,
      "snowflake-expert": 17800
    },
    "context_reduction_pct": {
      "analytics-engineer": 81.4,
      "dbt-expert": 78.3,
      "snowflake-expert": 73.0
    }
  }
}
```

**Validation**:
- [ ] Context reduction >40% (target: 40-60%)
- [ ] No pattern access regression
- [ ] Budget respected in all cases
- [ ] High-relevance patterns always loaded

**Deliverable**: `projects/active/ai-memory-system-improvements/tasks/after-metrics.json`

---

### Task 8: Documentation
**Status**: Pending
**Est. Time**: 2 hours

**Requirements**:
- Document token budget configuration
- Document relevance scoring algorithm
- Update CLAUDE.md with memory budget usage
- Create example usage guide
- Document metadata format

**Files to Update**:
- `CLAUDE.md` - Add memory budget section
- `knowledge/da-agent-hub/development/memory-system.md` - Comprehensive docs
- `.claude/config/memory-budget.json` - Configuration file
- `scripts/README.md` - Script usage

**Deliverable**: Complete documentation

---

## Timeline

**Week 1** (2025-01-14 to 2025-01-20):
- [ ] Task 1: Token counting utility (Mon)
- [ ] Task 2: Memory budget system (Tue)
- [ ] Task 3: Relevance scoring (Wed-Thu)
- [ ] Task 4: Add metadata to patterns (Fri)

**Week 2** (2025-01-21 to 2025-01-28):
- [ ] Task 5: Measure baseline (Mon)
- [ ] Task 6: Integration and testing (Tue-Thu)
- [ ] Task 7: Measure after metrics (Thu)
- [ ] Task 8: Documentation (Fri)

## Dependencies

- Python 3.10+
- tiktoken library (`pip install tiktoken`)
- pytest for testing (`pip install pytest`)
- Access to `.claude/memory/` directory

## Risk Mitigation

**Risk**: Token counts inaccurate
**Mitigation**: Validate against known sample, use official tiktoken

**Risk**: Budget too restrictive
**Mitigation**: Start at 20k, tune based on metrics

**Risk**: Relevance scoring too simplistic
**Mitigation**: Iterate based on real usage, add more signals

**Risk**: Performance overhead
**Mitigation**: Cache token counts, lazy loading

## Success Validation

✅ **Functional Requirements**:
- Token counting works for all patterns
- Budget system enforces 20k limit
- Relevance scoring prioritizes correctly
- Metadata added to all patterns

✅ **Performance Requirements**:
- 40-60% context reduction measured
- No regression in pattern access
- Budget respected in 100% of loads
- Relevance scoring accuracy >80%

✅ **Quality Requirements**:
- All tests passing
- Documentation complete
- Code reviewed
- Metrics validated

---

*This implementation plan breaks down Phase 1 into concrete, measurable tasks with clear deliverables and success criteria. Each task builds on the previous, culminating in a validated token-aware memory system.*
