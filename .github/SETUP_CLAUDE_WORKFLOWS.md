# Setting Up Claude GitHub Workflows

## Quick Start

Your Claude GitHub workflows are now configured and ready to use! Here's what's available:

### ✅ Installed Workflows

1. **`claude-issue-mentions.yml`** - Responds to @claude mentions in issue comments
2. **`claude-label-trigger.yml`** - Automatically investigates when specific labels are added

### 🎯 How to Use

#### Method 1: @Mention Claude (Recommended for Interactive Work)

Comment on any issue with:
```
@claude investigate this error
```

Other commands:
- `@claude fix` - Get a fix plan
- `@claude analyze` - Deep technical analysis
- `@claude create PR` - Get PR creation guidance

#### Method 2: Add Labels (Recommended for Batch Triage)

Add these labels to issues:
- `claude:investigate` - Automatic investigation
- `claude:fix` - Get solution suggestions
- `claude:analyze` - System-wide impact analysis

## Verification Steps

### 1. Check Secrets Are Configured

```bash
gh secret list
```

**Required secrets**:
- ✅ `ANTHROPIC_API_KEY` - For Claude API access
- ✅ `GITHUB_TOKEN` - Auto-provided by GitHub Actions
- ✅ `DA_AGENT_HUB_PAT` - For cross-repo operations (optional but recommended)

### 2. Test the Workflows

**Test Issue Created**: #102
- Has `claude:investigate` label applied
- Should trigger automatic investigation

Check workflow status:
```bash
gh run list --limit 5
```

Check for Claude's response:
```bash
gh issue view 102 --comments
```

### 3. View Workflow Logs

If Claude doesn't respond as expected:

```bash
# List recent runs
gh run list --workflow="Claude Label Trigger" --limit 3

# View specific run logs (replace RUN_ID)
gh run view RUN_ID --log
```

## Troubleshooting

### Workflow Not Triggering

**Check**:
1. Workflow files are in `.github/workflows/`
2. Workflows are enabled in repository settings
3. Branch protection rules aren't blocking Actions

```bash
# Verify workflow files exist
ls -la .github/workflows/claude-*.yml

# Check git status
git status
```

### Claude Not Responding

**Common Issues**:

1. **API Key Missing**:
   ```bash
   # Check if ANTHROPIC_API_KEY is set
   gh secret list | grep ANTHROPIC
   ```

2. **Workflow Failed**:
   ```bash
   # Check latest run status
   gh run list --workflow="Claude Label Trigger" --limit 1

   # View failure details
   gh run view <RUN_ID> --log
   ```

3. **Permissions Issue**:
   - Check that workflow has `issues: write` permission
   - Verify GitHub token has necessary scopes

### Workflow Syntax Errors

Test workflow syntax locally:
```bash
# Install actionlint
brew install actionlint

# Validate workflows
actionlint .github/workflows/claude-*.yml
```

## Advanced Configuration

### Customize Agent Selection

Edit `.github/workflows/claude-issue-mentions.yml` to change which agents handle which commands:

```yaml
- name: Execute Claude Investigation
  uses: anthropics/claude-code-action@v1
  with:
    prompt: |
      # Use specific agent based on issue labels
      # Modify agent selection logic here
```

### Add New Label Triggers

Edit `.github/workflows/claude-label-trigger.yml`:

```yaml
jobs:
  claude-action:
    if: |
      contains(github.event.label.name, 'claude:') ||
      github.event.label.name == 'investigate' ||
      github.event.label.name == 'your-custom-label'  # Add here
```

### Cross-Repository Setup

To enable Claude workflows in other repositories (like dbt_cloud, roy_kent):

1. Copy workflow files to target repo:
   ```bash
   cd ../dbt_cloud
   cp ../da-agent-hub/.github/workflows/claude-*.yml .github/workflows/
   ```

2. Add required secrets to target repo:
   ```bash
   gh secret set ANTHROPIC_API_KEY --repo graniterock/dbt_cloud
   ```

3. Adjust workflows for repo-specific agents (e.g., dbt-expert for dbt_cloud)

## Workflow Architecture

### How It Works

```
Issue Comment (@claude) → Webhook → GitHub Actions → Claude Code Action
                                                              ↓
                                    ← Posts Comment ← Claude Investigation
                                                              ↑
                                                      Specialist Agents
                                                      (dbt-expert, etc.)
```

### Data Flow

1. **Trigger**: Comment or label on issue
2. **Context Extraction**: Workflow parses issue body, comments, labels
3. **Agent Selection**: Maps request to appropriate specialist
4. **Claude Execution**: Runs with full repo context and MCP tools
5. **Response**: Posts findings as issue comment

### Permissions Model

Workflows run with these permissions:
- ✅ Read repository contents
- ✅ Write comments on issues/PRs
- ✅ Update labels
- ❌ No direct push to protected branches (creates PRs instead)

## Monitoring and Maintenance

### Health Check Commands

```bash
# Check recent Claude workflow runs
gh run list --workflow="Claude Label Trigger" --limit 10
gh run list --workflow="Claude Issue Mentions" --limit 10

# View success rate
gh run list --workflow="Claude Label Trigger" --json conclusion --limit 20 | \
  jq '[.[] | .conclusion] | group_by(.) | map({key: .[0], count: length})'

# Recent issues Claude has commented on
gh search issues --repo graniterock/da-agent-hub \
  --involves "claude[bot]" \
  --sort updated \
  --limit 10
```

### Monthly Maintenance

1. **Review agent effectiveness**:
   - Check which agents are being triggered most
   - Review comment quality and user feedback
   - Update agent prompts based on learnings

2. **Check for stale investigations**:
   ```bash
   # Find old issues with claude labels still applied
   gh issue list --label "claude:investigate" --state open --json number,title,updatedAt
   ```

3. **Update dependencies**:
   - Check for new versions of `anthropics/claude-code-action`
   - Review GitHub Actions security advisories

## Cost Monitoring

Each Claude investigation uses the Anthropic API. Monitor usage:

```bash
# Count workflow runs this month
gh run list --workflow="Claude Label Trigger" \
  --created="$(date -v-30d +%Y-%m-%d)" \
  --json conclusion | jq 'length'
```

**Estimated costs**:
- Investigation: ~0.05-0.15 per issue (depending on complexity)
- Analysis: ~0.10-0.30 per deep-dive
- Most repos: $5-20/month for typical usage

## Integration with Existing Workflows

### dbt Error Monitor Integration

The existing `dbt-issue-sleuth.yml` workflow can trigger Claude:

```yaml
- name: Label for Claude Investigation
  if: steps.error-check.outputs.critical == 'true'
  run: |
    gh issue edit ${{ steps.create-issue.outputs.number }} \
      --add-label "claude:investigate"
```

### PR Review Integration

Add to existing PR workflows:

```yaml
- name: Request Claude Review
  if: contains(github.event.pull_request.labels.*.name, 'needs-review')
  run: |
    gh pr comment ${{ github.event.pull_request.number }} \
      --body "@claude analyze this PR for dbt best practices"
```

## Next Steps

1. ✅ **Test workflows** with issue #102
2. ✅ **Try @mention** in a real issue
3. 📝 **Document patterns** you discover
4. 🚀 **Expand to other repos** as needed
5. 📊 **Monitor effectiveness** and iterate

## Resources

- **Usage Guide**: `.github/CLAUDE_WORKFLOW_GUIDE.md`
- **Workflow Files**:
  - `.github/workflows/claude-issue-mentions.yml`
  - `.github/workflows/claude-label-trigger.yml`
- **Agent Definitions**: `.claude/agents/specialists/github-sleuth-expert.md`
- **Test Issue**: https://github.com/graniterock/da-agent-hub/issues/102

## Support

Questions or issues?
- Check workflow run logs for debugging
- Review the usage guide for best practices
- Tag @dylanmorrish for workflow configuration issues
- Create an issue with label `workflow:claude` for bugs

---

**Setup Date**: 2025-10-07
**Status**: ✅ Active and Ready
**Test Issue**: #102
