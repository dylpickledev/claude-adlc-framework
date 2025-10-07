# Claude GitHub Workflows

## Active Workflows

### Primary Claude Interaction Workflows

**`claude-issue-mentions.yml`**
- **Trigger**: Issue comments containing `@claude` or `claude[bot]`
- **Purpose**: Interactive Claude responses to user requests
- **Commands**:
  - `@claude investigate` - Deep investigation
  - `@claude fix` - Create fix plan
  - `@claude analyze` - Technical analysis
  - `@claude create PR` - PR creation guidance
- **Agent Selection**: Automatic based on request type
- **Documentation**: See `.github/CLAUDE_WORKFLOW_GUIDE.md`

**`claude-label-trigger.yml`**
- **Trigger**: Labels matching `claude:*` pattern or investigation labels
- **Purpose**: Automatic background investigation
- **Supported Labels**:
  - `claude:investigate` - Full investigation
  - `claude:fix` - Fix plan generation
  - `claude:analyze` - System-wide analysis
  - `investigate` - Alternative trigger
  - `needs-investigation` - Alternative trigger
- **Agent Selection**: Based on label type
- **Documentation**: See `.github/CLAUDE_WORKFLOW_GUIDE.md`

## Disabled Workflows

**`claude-collaborative-fixes.yml.disabled`**
- **Status**: Disabled to prevent duplicate responses
- **Reason**: Functionality superseded by split workflows above
- **History**: Original comprehensive workflow, now split into two focused workflows
- **To Re-enable**: Rename to `.yml` extension (not recommended - will cause duplicates)

## Other Claude Workflows

### Repository-Specific Workflows

**`dbt-issue-sleuth.yml`**
- **Trigger**: `repository_dispatch` or manual workflow dispatch
- **Purpose**: dbt-specific issue investigation from other repos
- **Use Case**: Cross-repository dbt error analysis

**`claude-hub.yml`**
- **Trigger**: `repository_dispatch` from other repos
- **Purpose**: Central hub for cross-repository Claude operations
- **Use Case**: Coordinated analysis across dbt_cloud, roy_kent, etc.

**`manual-issue-investigation.yml`**
- **Trigger**: Label `claude-investigate` added to issues
- **Purpose**: Manual trigger for focused investigation
- **Note**: Overlaps with `claude-label-trigger.yml` - consider consolidating

### Project Management Workflows

**`claude-complete.yml`**
- **Trigger**: Manual dispatch with project name
- **Purpose**: Project completion automation via `/complete` command

**`suggest-completion-decision.yml`**
- **Trigger**: PR events
- **Purpose**: Suggest when projects should be completed

**`pr-completion-gate.yml`**
- **Trigger**: PR reviews
- **Purpose**: Quality gate for project completions

### Operations Workflows

**`auto-resolution-monitor.yml`**
- **Trigger**: Scheduled or manual
- **Purpose**: Monitor for issues that can be auto-resolved

**`claude-error-classifier.yml`**
- **Trigger**: Issue creation or updates
- **Purpose**: Classify error types for routing

**`cross-repository-coordination.yml`**
- **Trigger**: Repository dispatch
- **Purpose**: Coordinate fixes across multiple repos

**`claude-hub-test.yml`**
- **Trigger**: Manual testing
- **Purpose**: Test central hub functionality

**`test-claude-auth.yml`**
- **Trigger**: Manual testing
- **Purpose**: Verify Claude authentication and API access

## Workflow Selection Guide

### When to Use Which Workflow?

**For Interactive Issue Help**:
→ Use `@claude` mentions (triggers `claude-issue-mentions.yml`)
- Best for: Questions, specific requests, iterative problem-solving
- Example: `@claude why is this model failing?`

**For Automatic Background Investigation**:
→ Add labels (triggers `claude-label-trigger.yml`)
- Best for: Batch triage, systematic investigation, queuing work
- Example: Add `claude:investigate` label during issue triage

**For dbt-Specific Issues**:
→ Use `dbt-issue-sleuth.yml` via dispatch
- Best for: Cross-repository dbt error analysis
- Triggered automatically by dbt error workflows in other repos

**For Cross-Repo Coordination**:
→ Use `claude-hub.yml` via dispatch
- Best for: Fixes spanning multiple repositories
- Triggered by other repos needing da-agent-hub expertise

## Migration Notes

### Changes from Old Workflow System

**Before** (claude-collaborative-fixes.yml):
- Single workflow handling all triggers
- Model specification issues (`claude-3-5-sonnet-20250114`)
- Complex conditional logic

**After** (Current):
- Two focused workflows (mentions + labels)
- Default model (more reliable)
- Cleaner separation of concerns
- Better debugging and monitoring

### Why Split Into Two Workflows?

1. **Clarity**: Easier to understand trigger conditions
2. **Debugging**: Faster to identify which workflow failed
3. **Customization**: Can tune @mention vs label behavior independently
4. **Monitoring**: Separate success metrics for interactive vs automatic

## Troubleshooting

### Workflow Not Triggering

**Check**:
```bash
# Verify workflow files exist
ls -la .github/workflows/claude-*.yml

# Check recent runs
gh run list --workflow="Claude Issue Mentions" --limit 5
gh run list --workflow="Claude Label Trigger" --limit 5
```

### Duplicate Responses

**Cause**: Multiple workflows triggering on same event

**Fix**:
- Ensure only one workflow per trigger type is enabled
- `.disabled` workflows won't trigger

### No Response Posted

**Check logs**:
```bash
# Find recent run
gh run list --limit 5

# View logs
gh run view RUN_ID --log
```

## Maintenance

### Monthly Review

1. Check workflow success rates
2. Review agent selection effectiveness
3. Update prompts based on learnings
4. Archive or remove unused workflows

### Monitoring Commands

```bash
# Success rate for mentions
gh run list --workflow="Claude Issue Mentions" --limit 50 --json conclusion | \
  jq 'group_by(.conclusion) | map({conclusion: .[0].conclusion, count: length})'

# Success rate for labels
gh run list --workflow="Claude Label Trigger" --limit 50 --json conclusion | \
  jq 'group_by(.conclusion) | map({conclusion: .[0].conclusion, count: length})'

# Recent Claude activity
gh search issues --repo graniterock/da-agent-hub \
  --involves "claude[bot]" \
  --sort updated \
  --limit 10
```

## Documentation

- **Usage Guide**: `.github/CLAUDE_WORKFLOW_GUIDE.md` - How to use workflows
- **Setup Guide**: `.github/SETUP_CLAUDE_WORKFLOWS.md` - Configuration & troubleshooting
- **Status**: `.github/WORKFLOW_STATUS.md` - Current test status
- **This File**: `.github/workflows/README.md` - Workflow reference

---

**Last Updated**: 2025-10-07
**Active Workflows**: 2 (claude-issue-mentions, claude-label-trigger)
**Disabled Workflows**: 1 (claude-collaborative-fixes)
