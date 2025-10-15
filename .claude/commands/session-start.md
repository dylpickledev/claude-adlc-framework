# Session Start - Initialize Claude Session with Memory Health Check

**Purpose**: Run memory health check and load session context at the start of every Claude session.

**Description**: Verifies the AI memory system is within healthy token thresholds, displays current status, and ensures the session starts with optimal context loading.

## Instructions

Execute the following steps:

1. **Run Memory Health Check**:
   ```bash
   source projects/active/ai-memory-system-improvements/.venv/bin/activate && \
   python3 scripts/check-memory-health.py
   ```

2. **Display Session Context**:
   - Current memory status and token usage
   - Alert levels (150K warning, 180K critical, 200K limit)
   - Consolidation system status (cron jobs running)

3. **Output Summary**:
   - Memory system health: ✅ HEALTHY / ⚠️ WARNING / 🚨 CRITICAL
   - Active memory token count and percentage of limit
   - Next recommended actions based on status

## Expected Results

**Healthy Status (Current)**:
```
Memory System Health: ✅ HEALTHY
Total Active Memory: 46,012 tokens (23% of 200K limit)
Status: Prompt caching approach optimal
Next Actions: Continue monthly health checks
```

**Warning Status** (if >150K tokens):
```
Memory System Health: ⚠️ WARNING
Total Active Memory: 155,000 tokens (77.5% of 200K limit)
Status: Begin planning Phase 3 (BM25 semantic search)
Next Actions: Review implementation guide, schedule development
```

## Background

The AI memory system manages Claude's pattern knowledge base to prevent context overflow:
- **Phase 1 & 2**: Token-aware loading + automated consolidation (DEPLOYED)
- **Current capacity**: 46,012 / 200,000 tokens (23%)
- **Consolidation**: Daily/weekly/monthly cron jobs running
- **Phase 3 trigger**: 150K tokens (semantic search with BM25)

## Files Modified/Created

- None (read-only health check)

## Related Commands

- `/pause` - Save session context for later resumption
- `/complete` - Finish project and extract learnings

## Technical Details

**Virtual Environment**: `projects/active/ai-memory-system-improvements/.venv`
**Health Check Script**: `scripts/check-memory-health.py`
**Consolidation Logs**: `.claude/logs/consolidation/`
**Token History**: `.claude/cache/memory-health-history.json`

---

*Session initialization ensures optimal memory system performance and alerts you to capacity issues before they impact Claude's effectiveness.*
