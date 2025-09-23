---
name: gh-workflow
description: GitHub CLI integration workflows for enhanced repository management
---

I'll help you leverage GitHub CLI for enhanced development workflows, following Claude Code best practices.

## 🚀 **GitHub CLI Enhanced Workflows**

### Pull Request Management
```bash
# Create PR with context
gh pr create --title "feature/data-quality-improvements" \
  --body "$(cat .claude/tasks/current-task.md)" \
  --label "data-engineering,enhancement"

# Review PRs with Claude analysis
gh pr view 123 --json files | jq '.files[].filename' | \
  xargs -I {} echo "Analyze: {}"
```

### Issue Integration
```bash
# Create issues from agent findings
gh issue create --title "dbt model performance optimization" \
  --body "$(cat .claude/tasks/agent-findings/dbt-expert-analysis.md)" \
  --label "performance,dbt"
```

### Repository Insights
```bash
# Get repository health metrics
gh api repos/:owner/:repo/stats/contributors | \
  jq '.[] | {author: .author.login, commits: .total}'
```

This leverages Claude Code's **GitHub CLI integration** recommendation for enhanced development workflows.