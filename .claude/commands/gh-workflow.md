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

# Link commits to issues
git commit -m "fix: resolve schema validation issue

Closes #123 - implements dbt test improvements
from dbt-expert analysis"
```

### Repository Insights
```bash
# Get repository health metrics
gh api repos/:owner/:repo/stats/contributors | \
  jq '.[] | {author: .author.login, commits: .total}'

# Check workflow status
gh run list --limit 5 --json status,conclusion,name
```

## 🔧 **Integration with DA Agent Hub**

### Multi-Repository Workflows
```bash
# Update all workspace repositories
cd repos/
for repo in */; do
  cd "$repo"
  gh repo sync
  cd ..
done
```

### Agent-Driven Development
```bash
# Create branch based on agent analysis
TASK=$(head -1 .claude/tasks/current-task.md)
BRANCH="feature/$(echo $TASK | tr ' ' '-' | tr '[:upper:]' '[:lower:]')"
git checkout -b "$BRANCH"

# Push with PR template
gh pr create --template .github/pull_request_template.md
```

### Release Management
```bash
# Create release from agent findings
gh release create v1.2.0 \
  --title "Data Pipeline Improvements" \
  --notes "$(cat .claude/tasks/agent-findings/*-analysis.md)" \
  --generate-notes
```

## 📊 **Analytics and Reporting**

### Repository Health Checks
```bash
# Check all workspace repos
./scripts/manage-workspace.sh list | while read repo; do
  echo "Checking $repo..."
  cd "repos/$repo"
  gh repo view --json name,isArchived,pushedAt
  cd ../..
done
```

### Team Collaboration Metrics
```bash
# Get PR review patterns
gh pr list --state all --json author,reviews | \
  jq 'group_by(.author.login) | map({author: .[0].author.login, prs: length})'
```

## 🎯 **Best Practices Integration**

### With Sub-Agent Workflow
1. **Agent Analysis Phase**: Generate findings in `.claude/tasks/agent-findings/`
2. **GitHub Issue Creation**: `gh issue create` from agent findings
3. **Feature Branch**: Create branch linked to issue
4. **Implementation**: Follow agent recommendations
5. **PR Creation**: Include agent analysis in PR description

### Repository Template Usage
```bash
# Create new DA project from template
gh repo create my-new-da-project \
  --template graniterock/da-agent-hub \
  --private \
  --description "Data analytics project with agent hub"
```

This leverages Claude Code's **GitHub CLI integration** recommendation for enhanced development workflows.