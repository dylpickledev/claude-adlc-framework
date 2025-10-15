# Phase 5 Implementation: Automated Pattern Lifecycle

**Status**: 🚧 IN PROGRESS
**Started**: 2025-10-14
**Target**: Complete automated pattern lifecycle management

## Overview

Automate the pattern lifecycle to reduce manual maintenance by 80% through automated promotion, archival, and cleanup based on usage patterns and cross-agent value.

## Goals

### Primary Goals
1. **Automated Promotion**: Promote high-value agent-specific patterns to global scope
2. **Automated Archival**: Archive low-value patterns automatically
3. **Agent Scope Cleanup**: Remove duplicate and stale patterns from agent scopes
4. **Monitoring & Alerts**: Track pattern lifecycle metrics and alert on issues

### Success Criteria
- ✅ 80% reduction in manual pattern curation time
- ✅ Zero high-value pattern loss during automation
- ✅ Duplicate patterns detected and consolidated
- ✅ Stale patterns (>180 days, <3 uses) archived automatically
- ✅ Pattern lifecycle metrics dashboard operational

## Implementation Tasks

### Task 1: Automated Promotion Engine

**Objective**: Automatically promote agent-specific patterns to global scope when they prove valuable across multiple agents.

**Promotion Criteria** (Phase 4 already defined):
- `use_count >= 3` (used by multiple agents)
- `confidence >= 0.85` (high quality)
- Cross-agent usage detected

**Implementation**:
1. **Usage Tracking Across Agents**
   - Track which agents use which patterns
   - Detect when agent-specific pattern used by other agents
   - Count cross-agent usage frequency

2. **Automated Promotion Workflow**
   - Scan agent-specific patterns daily
   - Identify patterns meeting promotion criteria
   - Auto-promote with metadata tracking
   - Notify user of promotions (optional)

3. **Promotion Monitoring**
   - Log all automatic promotions
   - Track promotion rate over time
   - Alert if promotion rate anomalous

**Script**: `scripts/auto-promote-patterns.py`

**Cron Schedule**: Daily at 3 AM (after consolidation)

---

### Task 2: Automated Archival Engine

**Objective**: Archive low-value patterns to reduce active memory footprint while preserving searchability.

**Archival Criteria** (from spec):
- Age > 180 days
- `use_count < 3`
- `confidence < 0.70` (or not set)
- NOT in global scope (keep all global patterns)

**Implementation**:
1. **Staleness Detection**
   - Scan all patterns (global, agent-specific)
   - Calculate age from `last_used` or file mtime
   - Identify patterns meeting archival criteria

2. **Automated Archival Workflow**
   - Move stale patterns to archive tier
   - Preserve metadata for searchability
   - Update token counts
   - Log archival actions

3. **Archival Monitoring**
   - Track archival rate over time
   - Alert if archival rate too high (potential issue)
   - Report archived pattern recovery if needed

**Script**: `scripts/auto-archive-patterns.py`

**Cron Schedule**: Monthly (first Sunday at 4 AM)

---

### Task 3: Duplicate Detection & Consolidation

**Objective**: Detect and consolidate duplicate patterns across agent scopes.

**Duplicate Detection Strategy**:
1. **Exact Match**: MD5 hash of content
2. **Near Match**: High semantic similarity (>0.95)
3. **Structural Match**: Same problem/solution, different wording

**Implementation**:
1. **Duplicate Scanning**
   - Generate content hashes for all patterns
   - Detect exact duplicates
   - Optional: Use embeddings for near-duplicates (Phase 3)

2. **Consolidation Workflow**
   - Identify duplicate groups
   - Select canonical version (highest use_count or confidence)
   - Update references to canonical
   - Archive duplicates

3. **Deduplication Monitoring**
   - Track duplicate rate over time
   - Report consolidation actions
   - Alert if deduplication rate spikes

**Script**: `scripts/deduplicate-patterns.py`

**Cron Schedule**: Weekly (Saturday at 5 AM)

---

### Task 4: Agent Scope Cleanup Automation

**Objective**: Maintain agent-specific memory health through automated cleanup.

**Cleanup Actions**:
1. **Remove Orphaned Patterns**: Patterns in agent scope not matching agent expertise
2. **Remove Low-Relevance Patterns**: Relevance score < 0.30 after re-analysis
3. **Remove Superseded Patterns**: Newer version exists in same scope
4. **Remove Unused Patterns**: Zero uses after 90 days

**Implementation**:
1. **Scope Health Analysis**
   - Re-run relevance analysis for all agent-specific patterns
   - Detect orphaned patterns (mis-classified during migration)
   - Identify superseded patterns

2. **Automated Cleanup Workflow**
   - Remove orphaned patterns (move back to global or archive)
   - Archive low-relevance patterns
   - Consolidate superseded patterns
   - Log all cleanup actions

3. **Cleanup Monitoring**
   - Track cleanup rate per agent
   - Alert if agent scope growing unexpectedly
   - Report scope health metrics

**Script**: `scripts/cleanup-agent-scopes.py`

**Cron Schedule**: Monthly (second Sunday at 4 AM)

---

### Task 5: Pattern Lifecycle Monitoring Dashboard

**Objective**: Provide visibility into pattern lifecycle health and automation effectiveness.

**Metrics to Track**:
1. **Promotion Metrics**
   - Patterns promoted per day/week/month
   - Average time to promotion
   - Promotion success rate (promoted patterns remain active)

2. **Archival Metrics**
   - Patterns archived per month
   - Archive size growth
   - Pattern recovery rate (archived patterns restored)

3. **Deduplication Metrics**
   - Duplicate patterns detected
   - Consolidation rate
   - Token savings from deduplication

4. **Scope Health Metrics**
   - Agent scope size (tokens, file count)
   - Scope efficiency (relevant vs total patterns)
   - Scope growth rate

5. **Overall Health**
   - Active memory size (total tokens)
   - Memory churn rate (patterns added/removed)
   - Manual intervention rate (automation failures)

**Implementation**:
1. **Metrics Collection**
   - Extend memory health check with lifecycle metrics
   - Store historical metrics in JSON
   - Calculate trends and anomalies

2. **Dashboard Display**
   - Enhance `scripts/check-memory-health.py` with lifecycle section
   - Show promotion/archival/deduplication stats
   - Display scope health per agent
   - Highlight anomalies and alerts

3. **Alerting System**
   - Email/Slack notifications for anomalies
   - Alert on automation failures
   - Alert on scope health degradation

**Script**: Enhanced `scripts/check-memory-health.py`

**Reporting**: Weekly summary report

---

### Task 6: Automated Workflow Orchestration

**Objective**: Coordinate all automation workflows with proper sequencing and error handling.

**Workflow Sequence**:
1. **Daily** (3 AM):
   - Phase 2 consolidation (existing)
   - Automated promotion scan
   - Update lifecycle metrics

2. **Weekly** (Saturday, 3 AM):
   - Phase 2 weekly promotion (existing)
   - Duplicate detection & consolidation
   - Scope health check
   - Weekly summary report

3. **Monthly** (First Sunday, 4 AM):
   - Phase 2 monthly archival (existing)
   - Automated archival scan
   - Agent scope cleanup
   - Monthly health report

**Implementation**:
1. **Orchestration Script**
   - Master script to coordinate workflows
   - Error handling and retry logic
   - Logging and notification

2. **Workflow Configuration**
   - Configurable schedules
   - Enable/disable specific workflows
   - Dry-run mode for testing

3. **Monitoring & Logging**
   - Centralized logging
   - Workflow execution metrics
   - Error tracking and alerting

**Script**: `scripts/orchestrate-lifecycle.sh`

**Cron Configuration**: Updated `scripts/schedule-consolidation.sh`

---

## Integration with Existing Phases

### Phase 2 (Consolidation Pipeline)
Phase 5 extends Phase 2's consolidation with:
- Automated promotion from agent scopes
- Enhanced archival criteria
- Duplicate detection across tiers

### Phase 4 (Agent-Specific Scopes)
Phase 5 maintains Phase 4's scope health through:
- Automated cleanup of agent scopes
- Cross-scope promotion tracking
- Scope efficiency monitoring

## Technical Architecture

### Promotion Tracking
```python
# Extend metadata with promotion tracking
{
    "token_count": 2867,
    "use_count": 5,
    "confidence": 0.90,
    "last_used": "2025-10-14T12:00:00",
    "used_by_agents": ["dbt-expert", "snowflake-expert", "data-quality-specialist"],
    "promotion_candidate": true,
    "promotion_score": 0.85
}
```

### Archival Tracking
```python
# Archive metadata
{
    "archived_at": "2025-10-14T12:00:00",
    "archival_reason": "age > 180 days, use_count < 3",
    "original_path": ".claude/memory/specialists/dbt-expert/patterns/old-pattern.md",
    "recoverable": true
}
```

### Lifecycle Metrics
```python
# Lifecycle metrics structure
{
    "timestamp": "2025-10-14T12:00:00",
    "promotions": {
        "count": 3,
        "patterns": ["pattern1.md", "pattern2.md", "pattern3.md"]
    },
    "archivals": {
        "count": 5,
        "reasons": {"stale": 3, "low_usage": 2}
    },
    "duplicates": {
        "detected": 2,
        "consolidated": 2
    },
    "scope_cleanup": {
        "orphaned_removed": 1,
        "low_relevance_archived": 2
    }
}
```

## Testing Strategy

### Unit Tests
- Promotion criteria evaluation
- Archival criteria evaluation
- Duplicate detection algorithm
- Scope cleanup logic

### Integration Tests
- End-to-end promotion workflow
- End-to-end archival workflow
- Deduplication workflow
- Orchestration workflow

### Validation Tests
- Zero high-value pattern loss
- Promoted patterns remain active
- Archived patterns recoverable
- Scope health maintained

## Rollout Plan

1. **Week 1**: Implement automated promotion engine (Task 1)
2. **Week 1**: Implement automated archival engine (Task 2)
3. **Week 2**: Implement duplicate detection (Task 3)
4. **Week 2**: Implement scope cleanup (Task 4)
5. **Week 2**: Implement monitoring dashboard (Task 5)
6. **Week 2**: Implement orchestration (Task 6)
7. **Week 2**: Testing & validation
8. **Week 2**: Documentation & deployment

## Success Metrics

### Automation Effectiveness
- **Manual curation time**: Reduce by 80%
- **Automation accuracy**: >95% correct promotion/archival decisions
- **Zero pattern loss**: No high-value patterns lost

### Pattern Lifecycle Health
- **Promotion rate**: 3-5 patterns/week promoted to global
- **Archival rate**: 5-10 patterns/month archived
- **Duplicate rate**: <5% duplicate patterns in system
- **Scope efficiency**: >90% relevant patterns per agent

### System Health
- **Active memory growth**: <5% per month
- **Archive growth**: Expected from archival workflow
- **Scope balance**: Agent scopes within 20-30K tokens

## Deliverables

1. **Scripts** (6 new):
   - `scripts/auto-promote-patterns.py`
   - `scripts/auto-archive-patterns.py`
   - `scripts/deduplicate-patterns.py`
   - `scripts/cleanup-agent-scopes.py`
   - `scripts/orchestrate-lifecycle.sh`
   - Enhanced `scripts/check-memory-health.py`

2. **Configuration**:
   - Updated `scripts/schedule-consolidation.sh` with Phase 5 workflows
   - Lifecycle automation config file

3. **Documentation**:
   - Phase 5 completion report
   - Automation workflow documentation
   - Monitoring dashboard guide
   - Troubleshooting guide

4. **Testing**:
   - Unit test suite
   - Integration test suite
   - Validation test suite

## Risk Mitigation

### Risk: Incorrect Archival
**Mitigation**:
- Conservative archival criteria (>180 days, <3 uses)
- Never archive global patterns automatically
- Archive recovery mechanism
- Manual review option before archival

### Risk: Over-Promotion
**Mitigation**:
- Strict promotion criteria (use_count >= 3, confidence >= 0.85)
- Promotion cooldown period
- Manual approval for bulk promotions

### Risk: Scope Cleanup Errors
**Mitigation**:
- Dry-run mode for cleanup
- Backup before cleanup
- Orphan recovery mechanism
- Manual review of cleanup actions

### Risk: Automation Failures
**Mitigation**:
- Comprehensive error handling
- Retry logic for transient failures
- Alerting on persistent failures
- Graceful degradation (manual fallback)

## Next Steps After Phase 5

**Phase 6: Memory Budget Profiles**
- Agent-specific memory budgets
- Dynamic budget adjustment
- Budget monitoring and optimization

**Future Enhancements**:
- Machine learning for promotion/archival decisions
- Semantic similarity for duplicate detection (requires Phase 3)
- Automated pattern merging and refactoring
- Pattern version control and rollback
