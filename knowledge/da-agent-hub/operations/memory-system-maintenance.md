# Memory System Maintenance Guide

**System**: AI Memory & Context Management
**Status**: Production (deployed 2025-10-14)
**Automation**: Fully automated via cron jobs
**Owner**: Platform team

## Overview

The DA Agent Hub memory system implements token-aware loading with multi-tier consolidation to maintain optimal context window utilization while preserving high-value patterns.

**Current Health** (2025-10-14):
- Total memory: 46,012 tokens (23% of 200K capacity)
- Budget executions: 3 (avg 76.4% utilization)
- Alert thresholds: 150K (warning), 180K (critical for semantic search)

## Architecture

### Three-Tier Memory Structure
- **recent/**: Patterns <30 days (full detail, ~3,000 tokens avg)
- **intermediate/**: Patterns 30-90 days (summarized, ~200 tokens avg)
- **patterns/**: High-value permanent patterns (confidence ≥0.85 OR use_count ≥3)
- **archive/**: Low-value patterns (searchable, rarely loaded)

### Agent-Specific Scopes
- **26 agents**: 16 specialists + 10 roles
- **104 directories**: specialists/roles → agent-name → 4 tiers
- **Priority loading**: Agent-specific patterns get 30% relevance bonus

### Budget Profiles (Phase 6)
- **4 profile types**: specialist-narrow (20K), specialist-broad (35K), role-coordinator (50K), role-architect (75K)
- **Complexity tiers**: simple (0.5x), medium (1.0x), complex (1.5x), multi-system (2.0x)
- **Auto-detection**: Task description → complexity → budget calculation

## Automated Maintenance

### Daily (2 AM): Pattern Aging
```bash
/Users/TehFiestyGoat/GRC/da-agent-hub/scripts/run-phase5-automation.sh daily
```
- Moves patterns 30+ days from recent/ → intermediate/ with summarization
- Runs in ~2-5 minutes
- Logs: `.claude/cache/phase5-logs/daily.log`

### Weekly (Sunday 6 AM): Pattern Promotion
```bash
/Users/TehFiestyGoat/GRC/da-agent-hub/scripts/run-phase5-automation.sh weekly
```
- Promotes high-value patterns (confidence ≥0.85 OR use_count ≥3) to patterns/
- Analyzes budget usage (last 7 days)
- Runs in ~5-10 minutes
- Logs: `.claude/cache/phase5-logs/weekly.log`

### Monthly (1st day 7 AM): Pattern Archival
```bash
/Users/TehFiestyGoat/GRC/da-agent-hub/scripts/run-phase5-automation.sh monthly
```
- Archives low-value patterns >90 days with <2 uses
- Generates budget profile recommendations (last 30 days)
- Duplicate detection across scopes
- Runs in ~10-15 minutes
- Logs: `.claude/cache/phase5-logs/monthly.log`

## Monitoring

### Health Check
```bash
source projects/active/ai-memory-system-improvements/.venv/bin/activate
python3 scripts/check-memory-health.py
```

**Displays**:
- Total memory usage and percentage of capacity
- Phase 6 budget execution summary
- Complexity distribution
- Top agents by memory usage
- Alert if approaching 150K tokens

### Budget Usage Analytics
```bash
python3 scripts/analyze-budget-usage.py --days 7
python3 scripts/analyze-budget-usage.py --days 30 --recommendations
```

## Troubleshooting

### Issue: Memory Growth Above 150K Tokens
**Trigger**: Health check shows >150K tokens
**Action**: Implement Phase 3 semantic search (BM25)
**Reference**: `tasks/semantic-search-research/bm25-future-implementation.md`

### Issue: Budget Exceedances
**Symptom**: Budget usage logs show >100% utilization
**Diagnosis**: Check `.claude/cache/budget-usage.jsonl` for exceeding agents
**Fix**: Adjust budget profiles in `.claude/memory/budget-profiles.json`
**Tool**: `python3 scripts/analyze-budget-usage.py --recommendations`

### Issue: Low Pattern Relevance for Agents
**Symptom**: Agents loading many irrelevant patterns
**Diagnosis**: Check scope efficiency in health check (should be >70%)
**Fix**: Migrate more patterns to agent-specific scopes
**Tool**: `python3 scripts/migrate-patterns-to-scopes.py`

## Key Files

**Scripts**:
- `scripts/memory-budget-scoped.py` - Main loading system with Phase 6 integration
- `scripts/check-memory-health.py` - Health monitoring
- `scripts/run-phase5-automation.sh` - Consolidation automation
- `scripts/analyze-budget-usage.py` - Budget analytics

**Configuration**:
- `.claude/memory/budget-profiles.json` - Budget profiles and agent assignments
- Cron jobs: `crontab -l | grep phase5`

**Logs**:
- `.claude/cache/phase5-logs/` - Consolidation logs
- `.claude/cache/budget-usage.jsonl` - Budget execution history

## References

- **Project Documentation**: projects/completed/2025-10/ai-memory-system-improvements/
- **Phase 5 Report**: PHASE5_COMPLETE_2025-10-14.md
- **Phase 6 Report**: PHASE6_COMPLETE_2025-10-14.md
- **Deployment Guide**: PHASE6_DEPLOYMENT_GUIDE.md
- **Specialist Agent**: `.claude/agents/specialists/memory-system-expert.md`
