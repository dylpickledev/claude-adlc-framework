# Claude GitHub Workflow Guide

## Overview

Claude can automatically investigate and respond to GitHub issues in the da-agent-hub repository using two complementary workflows:

1. **@mention workflow** - Tag Claude in issue comments
2. **Label workflow** - Add specific labels to trigger actions

## Method 1: @Mention Claude in Comments

### Basic Usage

Comment on any issue with `@claude` followed by your request:

```
@claude investigate this error
```

```
@claude analyze the data quality issue
```

```
@claude fix this model compilation error
```

### Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `@claude investigate` | Deep investigation of the issue | `@claude investigate why this model is failing` |
| `@claude fix` | Create a fix plan and potentially a PR | `@claude fix this schema error` |
| `@claude create PR` | Same as fix - suggests PR approach | `@claude create PR for this issue` |
| `@claude analyze` | Technical deep-dive analysis | `@claude analyze the performance impact` |
| `@claude` (general) | Respond with context and suggestions | `@claude what's causing this?` |

### What Claude Does

When you @mention Claude:
1. Triggers the `claude-issue-mentions.yml` workflow
2. Reads the issue context and your comment
3. Selects appropriate specialist agent (dbt-expert, github-sleuth-expert, etc.)
4. Investigates using GitHub MCP tools
5. Posts findings as a comment on the issue

## Method 2: Label-Based Triggers

### Available Labels

Add these labels to issues to trigger automatic Claude investigation:

| Label | Action | Use Case |
|-------|--------|----------|
| `claude:investigate` | Full investigation | New errors or unknown issues |
| `investigate` | Same as above | Alternative label name |
| `needs-investigation` | Same as above | Alternative label name |
| `claude:fix` | Create fix plan | When you want solution suggestions |
| `claude:analyze` | Deep technical analysis | Complex system-wide issues |

### What Happens

When you add a label:
1. Triggers the `claude-label-trigger.yml` workflow
2. Selects appropriate agent based on label
3. Analyzes issue automatically (no manual request needed)
4. Posts findings as a comment
5. May suggest additional labels or next steps

## Workflows in Detail

### Issue Comment Workflow (`claude-issue-mentions.yml`)

**Trigger**: Comment containing `@claude` or `claude[bot]`

**Capabilities**:
- Parse natural language requests
- Delegate to specialist agents
- Access GitHub MCP for cross-issue analysis
- Post detailed responses

**Example Interaction**:
```
User: @claude investigate why dm_sales_summary is failing tests

Claude: 🤖 Investigation Results

I've analyzed issue #123 using the dbt-expert agent.

**Root Cause**:
The test `unique_dm_sales_summary_transaction_id` is failing because...

**Related Issues**:
- #115 (similar uniqueness constraint failure)
- #98 (upstream data quality issue in stg_sales)

**Recommended Fix**:
1. Update the unique test to account for...
2. Add data quality check in staging layer...

**Files to Change**:
- `models/marts/dm_sales_summary.sql:45`
- `models/staging/stg_sales.sql:23`

Would you like me to create a PR with these fixes?
```

### Label Trigger Workflow (`claude-label-trigger.yml`)

**Trigger**: Label added to issue (matching pattern `claude:*` or specific investigation labels)

**Capabilities**:
- Automatic classification
- Proactive investigation
- Label-based routing to experts
- Suggest additional labels

**Example Interaction**:
```
[User adds "claude:investigate" label to issue]

Claude: 🏷️ Automated Investigation Triggered

I've been automatically triggered by the `claude:investigate` label.

**Issue Classification**: Data Quality Issue

**Analysis**:
This appears to be a cascade failure from upstream source...

**Downstream Impact**:
- 3 mart models affected
- 2 reports will show stale data

**Priority**: HIGH - affects production dashboards

**Recommended Labels**:
- `priority:high`
- `type:data-quality`
- `area:sales`

**Next Steps**:
1. Investigate source system data refresh
2. Check orchestration logs in Orchestra
3. Consider adding data freshness tests

Assigning to data engineering team for source investigation.
```

## Best Practices

### When to Use @Mentions vs Labels

**Use @mentions when**:
- You want to ask specific questions
- You need clarification or context
- You want Claude to explain something
- You're collaborating on a solution

**Use labels when**:
- You want automatic background investigation
- You're triaging multiple issues
- You want systematic classification
- You want to queue issues for Claude review

### Effective @Mention Requests

✅ **Good**:
```
@claude investigate why the sales mart is missing Q4 data
```
```
@claude analyze the performance impact of this change
```

❌ **Less Effective**:
```
@claude help
```
```
@claude look at this
```

### Label Workflow Tips

1. **Start with `needs-investigation`** for new issues
2. **Use `claude:analyze`** for complex system-wide impacts
3. **Apply `claude:fix`** only when you want solution proposals
4. **Remove labels** after Claude responds if you want to prevent re-triggering

## Workflow Permissions

Both workflows have these permissions:
- ✅ Read repository contents
- ✅ Write comments on issues and PRs
- ✅ Create and update labels
- ❌ Cannot push directly to protected branches (must create PRs)

## Troubleshooting

### Claude Didn't Respond

**Check**:
1. Did the workflow run? (Check Actions tab)
2. Was the @mention spelled correctly?
3. Is the label exactly matching the trigger pattern?

### Workflow Failed

**Common Issues**:
1. API key not set (needs `ANTHROPIC_API_KEY` secret)
2. GitHub token expired
3. Rate limiting (wait a few minutes)

### Claude Response Too Generic

**Improve by**:
1. Provide more context in your @mention
2. Include error messages or logs in issue body
3. Reference specific files or line numbers
4. Use more specific command (`@claude investigate` vs just `@claude`)

## Examples from da-agent-hub

### Example 1: dbt Test Failure
```
Issue: Test failure in dm_safety_incidents

@claude investigate why unique_dm_safety_incidents_incident_id is failing

Claude Response:
🔍 Investigation using dbt-expert + snowflake-expert

Root Cause: Duplicate incident IDs from MSHA data source (incidents being
reported multiple times due to amendment updates).

Fix: Add deduplication logic in stg_msha_incidents to keep latest amendment.

Files:
- models/staging/stg_msha_incidents.sql:34
- models/marts/dm_safety_incidents.sql:12

Ready to create PR with fix?
```

### Example 2: Cross-System Analysis
```
Issue: Dashboard showing stale data

[Apply label: claude:analyze]

Claude Response:
🏷️ Automated Analysis via Label Trigger

Cross-system analysis (Orchestra → dbt → Tableau):

1. **Orchestra**: Job "daily_refresh_sales" succeeded at 6:05 AM ✅
2. **dbt**: dm_sales_summary last updated 6:45 AM ✅
3. **Tableau**: Extract last refresh 4:30 AM ❌

Problem: Tableau extract refresh scheduled before data refresh completes.

Recommendation: Update Tableau extract schedule to 8:00 AM or use live connection.

Labels suggested: `type:infrastructure`, `area:bi`, `priority:medium`
```

## Advanced Features

### Multi-Agent Coordination

Claude automatically delegates to appropriate experts:
- **dbt-expert**: SQL, transformations, testing
- **data-engineer-role**: Pipelines, orchestration
- **tableau-expert**: Dashboard performance
- **github-sleuth-expert**: Cross-issue pattern analysis
- **da-architect**: System-wide design questions

### GitHub MCP Integration

Claude uses GitHub MCP to:
- Find related issues across repositories
- Search code for error patterns
- Check PR history for similar fixes
- Analyze issue trends and patterns

### Context Preservation

Claude can reference:
- Previous comments on the same issue
- Related issues you've linked
- Code from the repository
- Documentation from knowledge base

## Future Enhancements

Planned improvements:
- **Auto-assignment**: Claude assigns issues to appropriate team members
- **PR creation**: Direct PR creation (not just suggestions)
- **Proactive monitoring**: Scheduled scans for common issue patterns
- **Cross-repo coordination**: Coordinate fixes across dbt_cloud, roy_kent, etc.

## Support

For issues with Claude workflows:
1. Check workflow run logs in Actions tab
2. Review this guide for correct usage patterns
3. Create issue with label `workflow:claude` for workflow problems
4. Tag @dylanmorrish for critical workflow failures

---

**Last Updated**: 2025-10-07
**Workflows**: `claude-issue-mentions.yml`, `claude-label-trigger.yml`
**Repository**: graniterock/da-agent-hub
