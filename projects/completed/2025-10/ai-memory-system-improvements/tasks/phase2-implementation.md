# Phase 2: Memory Consolidation Pipeline - Implementation Tasks

## Overview

**Goal**: Implement three-tier memory hierarchy with automated consolidation to prevent pattern loss
**Timeline**: Weeks 3-4 (2025-01-15 to 2025-01-28)
**Status**: Starting

**Building on Phase 1**: Phase 1 achieved 91.7% token reduction with budget system. Phase 2 adds lifecycle management to prevent losing valuable patterns as they age.

## Success Criteria

✅ Three-tier directory structure operational
✅ Automated consolidation pipeline running
✅ Zero pattern loss validated (no high-value patterns dropped)
✅ 30-50% reduction in total memory files
✅ Summarization quality reviewed
✅ Documentation complete

## Architecture: Three-Tier Memory Hierarchy

### Tier 1: Recent (Hot Storage)
**Location**: `.claude/memory/recent/`
**Timeframe**: Last 30 days
**Content**: Full, detailed patterns
**Token Impact**: Highest priority for loading

**Characteristics**:
- Recently used or created patterns
- Full detail preserved
- High relevance scores
- Fast access

**Example**: Pattern used yesterday stays in recent/ with full detail

### Tier 2: Intermediate (Warm Storage)
**Location**: `.claude/memory/intermediate/`
**Timeframe**: 30-90 days
**Content**: Summarized patterns (75% reduction)
**Token Impact**: Medium priority for loading

**Characteristics**:
- Patterns transitioning from recent to permanent
- Summarized to key insights only
- Metadata preserved
- Can be promoted back to recent if used

**Example**: Pattern from 45 days ago, summarized to core findings

### Tier 3: Patterns (Cold Storage)
**Location**: `.claude/memory/patterns/`
**Timeframe**: Permanent (90+ days OR validated high-value)
**Content**: Validated, production-ready patterns
**Token Impact**: Loaded only when highly relevant

**Characteristics**:
- Proven patterns with high success rate
- Confidence score ≥0.85
- Used ≥3 times successfully
- Permanent retention

**Example**: Generic export pattern (confidence: 0.85, use_count: 15)

## Consolidation Workflow

### Daily Consolidation (Automated)
**Time**: 3:00 AM local
**Action**: Move 30+ day old files from recent/ to intermediate/

```bash
# Move files older than 30 days
find .claude/memory/recent/ -name "*.md" -mtime +30 -exec mv {} .claude/memory/intermediate/ \;

# Summarize moved files
python scripts/summarize-patterns.py --dir .claude/memory/intermediate/ --fresh-only
```

### Weekly Consolidation (Automated)
**Time**: Sunday 3:00 AM
**Action**: Promote high-value patterns from intermediate/ to patterns/

```bash
# Detect patterns with confidence ≥0.85 OR use_count ≥3
python scripts/promote-patterns.py --source intermediate/ --dest patterns/ --threshold 0.85
```

### Monthly Consolidation (Automated)
**Time**: 1st of month, 3:00 AM
**Action**: Archive inactive intermediate/ patterns (90+ days, low usage)

```bash
# Archive patterns older than 90 days with use_count < 2
python scripts/archive-patterns.py --source intermediate/ --age 90 --min-uses 2
```

## Detailed Tasks

### Task 1: Create Three-Tier Directory Structure
**Status**: Pending
**Est. Time**: 30 minutes

**Implementation**:
```bash
# Create directories
mkdir -p .claude/memory/recent
mkdir -p .claude/memory/intermediate
mkdir -p .claude/memory/patterns

# Migrate existing patterns based on age/usage
python scripts/migrate-to-tiers.py
```

**Migration Logic**:
- Files modified in last 30 days → recent/
- Files 30-90 days old → intermediate/ (with summarization)
- Files with confidence ≥0.85 OR use_count ≥3 → patterns/
- All others → intermediate/

**Deliverable**: Three-tier directory structure with migrated patterns

---

### Task 2: Build Pattern Summarization Engine
**Status**: Pending
**Est. Time**: 3 hours

**Requirements**:
- Extract key insights from full patterns
- Preserve metadata (token_count, confidence, use_count)
- Target 75% token reduction
- Maintain actionability

**Implementation**:
```python
# scripts/summarize-patterns.py

class PatternSummarizer:
    """Summarizes patterns for intermediate storage"""

    def summarize(self, full_pattern: str, metadata: dict) -> str:
        """
        Summarize pattern to 25% of original token count.

        Preserves:
        - Pattern name and purpose
        - Key insights (3-5 bullet points)
        - When to apply
        - Success criteria
        - Original confidence score
        """

        sections_to_extract = [
            "## Problem",
            "## Solution",
            "## When to Apply",
            "## Key Benefits"
        ]

        # Extract sections
        summary_parts = self.extract_sections(full_pattern, sections_to_extract)

        # Generate summary
        summary = f"""# {metadata['pattern_file']} (SUMMARIZED)

**Original Token Count**: {metadata['token_count']}
**Confidence**: {metadata.get('confidence', 'N/A')}
**Use Count**: {metadata.get('use_count', 0)}
**Summarized**: {datetime.now().isoformat()}

## Key Insights
{self.extract_key_insights(summary_parts)}

## When to Apply
{self.extract_when_to_apply(summary_parts)}

---
*Full pattern available in archive. Restore with: `scripts/restore-pattern.py {metadata['pattern_file']}`*
"""
        return summary
```

**Testing**:
- [ ] Test with 5 sample patterns
- [ ] Verify 75% token reduction
- [ ] Validate summary preserves key info
- [ ] Test restore functionality

**Deliverable**: `scripts/summarize-patterns.py` with tests

---

### Task 3: Build Pattern Promotion Engine
**Status**: Pending
**Est. Time**: 2 hours

**Requirements**:
- Detect high-value patterns in intermediate/
- Promote to patterns/ (permanent storage)
- Update metadata
- Track promotion history

**Promotion Criteria**:
```python
def should_promote(metadata: dict) -> bool:
    """Determine if pattern should be promoted to permanent storage"""

    # High confidence (validated by /complete)
    if metadata.get('confidence', 0) >= 0.85:
        return True

    # High usage (proven useful)
    if metadata.get('use_count', 0) >= 3:
        return True

    # Recently used and moderate confidence
    if metadata.get('use_count', 0) >= 2 and metadata.get('confidence', 0) >= 0.70:
        last_used = metadata.get('last_used')
        if last_used and days_since(last_used) < 60:
            return True

    return False
```

**Implementation**:
```python
# scripts/promote-patterns.py

class PatternPromoter:
    """Promotes patterns from intermediate to permanent storage"""

    def promote_eligible_patterns(self, source_dir: Path, dest_dir: Path):
        """Scan intermediate/ and promote eligible patterns"""

        promoted = []
        for pattern_file in source_dir.glob("*.md"):
            metadata = self.load_metadata(pattern_file)

            if self.should_promote(metadata):
                # Restore full pattern if summarized
                if self.is_summarized(pattern_file):
                    full_pattern = self.restore_from_archive(pattern_file)
                else:
                    full_pattern = pattern_file.read_text()

                # Promote to patterns/
                dest_file = dest_dir / pattern_file.name
                dest_file.write_text(full_pattern)

                # Update metadata
                metadata['promoted_at'] = datetime.now().isoformat()
                metadata['tier'] = 'patterns'
                self.save_metadata(dest_file, metadata)

                # Remove from intermediate
                pattern_file.unlink()

                promoted.append(pattern_file.name)

        return promoted
```

**Deliverable**: `scripts/promote-patterns.py` with tests

---

### Task 4: Build Pattern Archival Engine
**Status**: Pending
**Est. Time**: 2 hours

**Requirements**:
- Archive low-value patterns from intermediate/
- Preserve in `.claude/memory/archive/`
- Searchable archive with metadata
- Restore capability

**Archival Criteria**:
```python
def should_archive(metadata: dict) -> bool:
    """Determine if pattern should be archived"""

    # Old and unused
    modified_days = days_since(metadata.get('modified_at'))
    use_count = metadata.get('use_count', 0)

    if modified_days > 90 and use_count < 2:
        return True

    # Very old and low usage
    if modified_days > 180 and use_count < 5:
        return True

    return False
```

**Implementation**:
```python
# scripts/archive-patterns.py

class PatternArchiver:
    """Archives low-value patterns to reduce active memory"""

    def archive_eligible_patterns(self, source_dir: Path):
        """Archive patterns from intermediate/ that meet criteria"""

        archive_dir = Path(".claude/memory/archive")
        archive_dir.mkdir(exist_ok=True)

        archived = []
        for pattern_file in source_dir.glob("*.md"):
            metadata = self.load_metadata(pattern_file)

            if self.should_archive(metadata):
                # Move to archive with timestamp
                archive_name = f"{pattern_file.stem}_{datetime.now().strftime('%Y%m%d')}.md"
                archive_file = archive_dir / archive_name

                # Move pattern and metadata
                pattern_file.rename(archive_file)
                metadata_file = pattern_file.with_suffix('.metadata.json')
                if metadata_file.exists():
                    metadata_file.rename(archive_file.with_suffix('.metadata.json'))

                archived.append(pattern_file.name)

        return archived
```

**Deliverable**: `scripts/archive-patterns.py` with tests

---

### Task 5: Create Migration Script
**Status**: Pending
**Est. Time**: 2 hours

**Requirements**:
- Migrate existing patterns to three-tier structure
- Preserve all metadata
- Handle edge cases
- Idempotent (safe to re-run)

**Implementation**:
```python
# scripts/migrate-to-tiers.py

def migrate_existing_patterns():
    """One-time migration to three-tier structure"""

    # Current location
    current_dir = Path(".claude/memory/patterns")

    # New locations
    recent_dir = Path(".claude/memory/recent")
    intermediate_dir = Path(".claude/memory/intermediate")
    patterns_dir = Path(".claude/memory/patterns_new")

    recent_dir.mkdir(exist_ok=True)
    intermediate_dir.mkdir(exist_ok=True)
    patterns_dir.mkdir(exist_ok=True)

    for pattern_file in current_dir.glob("*.md"):
        metadata = load_metadata(pattern_file)
        modified_days = days_since(pattern_file.stat().st_mtime)

        # Recent (< 30 days)
        if modified_days < 30:
            dest = recent_dir / pattern_file.name

        # High-value → Patterns (permanent)
        elif metadata.get('confidence', 0) >= 0.85 or metadata.get('use_count', 0) >= 3:
            dest = patterns_dir / pattern_file.name

        # Everything else → Intermediate (with summarization)
        else:
            # Summarize first
            summary = summarize_pattern(pattern_file, metadata)
            dest = intermediate_dir / pattern_file.name
            dest.write_text(summary)
            copy_metadata(pattern_file, dest)
            continue

        # Move pattern and metadata
        shutil.copy2(pattern_file, dest)
        copy_metadata(pattern_file, dest)

    # Rename patterns_new to patterns (after backup)
    if patterns_dir.exists():
        shutil.move(current_dir, current_dir.parent / "patterns_backup")
        shutil.move(patterns_dir, current_dir)
```

**Deliverable**: `scripts/migrate-to-tiers.py` (one-time migration)

---

### Task 6: Create Consolidation Scheduler
**Status**: Pending
**Est. Time**: 2 hours

**Requirements**:
- Automated daily/weekly/monthly consolidation
- Configurable schedules
- Logging and error handling
- Dry-run mode for testing

**Implementation**:
```python
# scripts/consolidation-scheduler.py

class ConsolidationScheduler:
    """Manages automated memory consolidation"""

    def run_daily_consolidation(self):
        """Move 30+ day patterns to intermediate/"""
        print("🔄 Running daily consolidation...")

        recent_dir = Path(".claude/memory/recent")
        intermediate_dir = Path(".claude/memory/intermediate")

        moved = 0
        for pattern_file in recent_dir.glob("*.md"):
            if days_since(pattern_file.stat().st_mtime) > 30:
                # Move to intermediate
                dest = intermediate_dir / pattern_file.name
                shutil.move(pattern_file, dest)

                # Summarize
                summarize_pattern(dest)

                moved += 1

        print(f"✅ Daily consolidation: Moved {moved} patterns to intermediate/")

    def run_weekly_consolidation(self):
        """Promote high-value patterns to permanent storage"""
        print("🔄 Running weekly consolidation...")

        promoter = PatternPromoter()
        promoted = promoter.promote_eligible_patterns(
            Path(".claude/memory/intermediate"),
            Path(".claude/memory/patterns")
        )

        print(f"✅ Weekly consolidation: Promoted {len(promoted)} patterns to permanent storage")

    def run_monthly_consolidation(self):
        """Archive low-value patterns"""
        print("🔄 Running monthly consolidation...")

        archiver = PatternArchiver()
        archived = archiver.archive_eligible_patterns(
            Path(".claude/memory/intermediate")
        )

        print(f"✅ Monthly consolidation: Archived {len(archived)} patterns")
```

**Deliverable**: `scripts/consolidation-scheduler.py` with cron integration

---

### Task 7: Integration Testing
**Status**: Pending
**Est. Time**: 2 hours

**Test Scenarios**:
1. **Full Lifecycle Test**: Create pattern → Use 30 days → Auto-move to intermediate → Summarize
2. **Promotion Test**: Pattern with confidence 0.85 → Promote to patterns/
3. **Archival Test**: Pattern unused 90+ days → Archive
4. **Restore Test**: Restore archived pattern → Verify full content
5. **Zero Loss Test**: Run consolidation → Verify no high-value patterns lost

**Validation**:
```python
def test_zero_pattern_loss():
    """Critical test: Ensure no high-value patterns are lost"""

    # Before consolidation
    before = collect_all_patterns()
    high_value_before = [p for p in before if p.confidence >= 0.70 or p.use_count >= 2]

    # Run consolidation
    run_full_consolidation()

    # After consolidation
    after = collect_all_patterns(include_archive=True)
    high_value_after = [p for p in after if p.confidence >= 0.70 or p.use_count >= 2]

    # Validate
    assert len(high_value_before) == len(high_value_after), "High-value patterns lost!"
    print("✅ Zero pattern loss validated")
```

**Deliverable**: Integration test suite passing

---

## Timeline

**Week 3** (2025-01-15 to 2025-01-21):
- [ ] Task 1: Three-tier structure (Mon)
- [ ] Task 2: Summarization engine (Tue-Wed)
- [ ] Task 3: Promotion engine (Thu)
- [ ] Task 4: Archival engine (Fri)

**Week 4** (2025-01-22 to 2025-01-28):
- [ ] Task 5: Migration script (Mon)
- [ ] Task 6: Consolidation scheduler (Tue)
- [ ] Task 7: Integration testing (Wed-Thu)
- [ ] Documentation and validation (Fri)

## Success Validation

✅ **Functional Requirements**:
- Three tiers operational (recent, intermediate, patterns)
- Automated consolidation running
- Summarization reduces tokens by 75%
- Promotion logic working
- Archival preserves searchability

✅ **Quality Requirements**:
- Zero high-value pattern loss
- 30-50% reduction in active memory files
- Summarization preserves key insights
- All tests passing

✅ **Performance Requirements**:
- Daily consolidation < 1 minute
- Weekly consolidation < 2 minutes
- Monthly consolidation < 5 minutes
- No impact on pattern access speed

---

*Phase 2 builds on Phase 1's token budget system, adding lifecycle management to ensure patterns are preserved at appropriate detail levels based on age and value.*
