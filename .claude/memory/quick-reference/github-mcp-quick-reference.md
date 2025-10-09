# GitHub MCP Quick Reference Card

**Purpose**: Fast lookup for GitHub repository operations, issues, and pull requests
**Primary Users**: github-sleuth-expert, ALL role agents, qa-engineer-role, data-engineer-role
**Server**: github (npx package: @modelcontextprotocol/server-github)

---

## 🚀 Most Common Operations

### 1. Repository Operations

**Search repositories**:
```bash
mcp__github__search_repositories \
  query="org:graniterock language:Python" \
  perPage=10
```

**Get file contents**:
```bash
mcp__github__get_file_contents \
  owner="graniterock" \
  repo="dbt_cloud" \
  path="README.md"
```

**Create/update single file**:
```bash
mcp__github__create_or_update_file \
  owner="graniterock" \
  repo="dbt_cloud" \
  path="models/marts/sales/fct_orders.sql" \
  content="[SQL content]" \
  message="feat: Add fct_orders model" \
  branch="feature/add-orders-model"
```

**Push multiple files** (batch update):
```bash
mcp__github__push_files \
  owner="graniterock" \
  repo="dbt_cloud" \
  branch="feature/add-models" \
  files=[
    {"path": "models/staging/stg_orders.sql", "content": "[SQL]"},
    {"path": "models/marts/fct_orders.sql", "content": "[SQL]"}
  ] \
  message="feat: Add orders staging and fact models"
```

**Create branch**:
```bash
mcp__github__create_branch \
  owner="graniterock" \
  repo="dbt_cloud" \
  branch="feature/new-models"
```

**List commits**:
```bash
mcp__github__list_commits \
  owner="graniterock" \
  repo="dbt_cloud" \
  sha="main" \
  perPage=10
```

---

### 2. Issue Management

**List issues**:
```bash
mcp__github__list_issues \
  owner="graniterock" \
  repo="dbt_cloud" \
  state="open" \
  per_page=20
```

**Filter issues by label**:
```bash
mcp__github__list_issues \
  owner="graniterock" \
  repo="dbt_cloud" \
  state="open" \
  labels=["bug", "data-quality"]
```

**Get issue details**:
```bash
mcp__github__get_issue \
  owner="graniterock" \
  repo="dbt_cloud" \
  issue_number=123
```

**Create issue**:
```bash
mcp__github__create_issue \
  owner="graniterock" \
  repo="dbt_cloud" \
  title="Data quality issue in fct_orders" \
  body="Test failure: duplicate order_ids found..." \
  labels=["bug", "data-quality"]
```

**Update issue**:
```bash
mcp__github__update_issue \
  owner="graniterock" \
  repo="dbt_cloud" \
  issue_number=123 \
  state="closed"
```

**Add issue comment**:
```bash
mcp__github__add_issue_comment \
  owner="graniterock" \
  repo="dbt_cloud" \
  issue_number=123 \
  body="Fixed in PR #456"
```

**Search issues** (cross-repo):
```bash
mcp__github__search_issues \
  q="org:graniterock type:issue state:open label:bug" \
  per_page=20
```

---

### 3. Pull Request Management

**List pull requests**:
```bash
mcp__github__list_pull_requests \
  owner="graniterock" \
  repo="dbt_cloud" \
  state="open"
```

**Get pull request details**:
```bash
mcp__github__get_pull_request \
  owner="graniterock" \
  repo="dbt_cloud" \
  pull_number=456
```

**Get PR files** (changed files):
```bash
mcp__github__get_pull_request_files \
  owner="graniterock" \
  repo="dbt_cloud" \
  pull_number=456
```

**Get PR status** (checks, CI/CD):
```bash
mcp__github__get_pull_request_status \
  owner="graniterock" \
  repo="dbt_cloud" \
  pull_number=456
```

**Create pull request**:
```bash
mcp__github__create_pull_request \
  owner="graniterock" \
  repo="dbt_cloud" \
  title="feat: Add orders data models" \
  head="feature/add-orders-model" \
  base="main" \
  body="## Summary\n- Added stg_orders staging model\n- Added fct_orders fact model\n\n## Testing\n- dbt test passed\n- Data validation complete"
```

**Get PR comments**:
```bash
mcp__github__get_pull_request_comments \
  owner="graniterock" \
  repo="dbt_cloud" \
  pull_number=456
```

**Get PR reviews**:
```bash
mcp__github__get_pull_request_reviews \
  owner="graniterock" \
  repo="dbt_cloud" \
  pull_number=456
```

**Create PR review**:
```bash
mcp__github__create_pull_request_review \
  owner="graniterock" \
  repo="dbt_cloud" \
  pull_number=456 \
  body="LGTM - code quality looks good" \
  event="APPROVE"
```

**Merge pull request**:
```bash
mcp__github__merge_pull_request \
  owner="graniterock" \
  repo="dbt_cloud" \
  pull_number=456 \
  merge_method="squash"
```

**Update PR branch** (sync with base):
```bash
mcp__github__update_pull_request_branch \
  owner="graniterock" \
  repo="dbt_cloud" \
  pull_number=456
```

---

### 4. Search Operations

**Search code**:
```bash
mcp__github__search_code \
  q="org:graniterock incremental dbt" \
  per_page=10
```

**Search users**:
```bash
mcp__github__search_users \
  q="type:user location:Sacramento" \
  per_page=10
```

---

## 🎯 Common Workflows

### Workflow 1: Issue Investigation
```bash
# 1. Search for similar issues across org
mcp__github__search_issues \
  q="org:graniterock type:issue state:open dbt test failure" \
  per_page=20

# 2. Get detailed issue information
mcp__github__get_issue \
  owner="graniterock" \
  repo="dbt_cloud" \
  issue_number=123

# 3. Search related code
mcp__github__search_code \
  q="org:graniterock fct_orders incremental" \
  per_page=10

# 4. Get file contents for analysis
mcp__github__get_file_contents \
  owner="graniterock" \
  repo="dbt_cloud" \
  path="models/marts/fct_orders.sql"

# 5. Add investigation findings
mcp__github__add_issue_comment \
  owner="graniterock" \
  repo="dbt_cloud" \
  issue_number=123 \
  body="Root cause identified: missing unique_key configuration"
```

### Workflow 2: Pull Request Review
```bash
# 1. Get PR details
mcp__github__get_pull_request \
  owner="graniterock" \
  repo="dbt_cloud" \
  pull_number=456

# 2. Get changed files
mcp__github__get_pull_request_files \
  owner="graniterock" \
  repo="dbt_cloud" \
  pull_number=456

# 3. Read file contents for review
mcp__github__get_file_contents \
  owner="graniterock" \
  repo="dbt_cloud" \
  path="models/marts/fct_orders.sql" \
  branch="feature/add-orders-model"

# 4. Check PR status (CI/CD checks)
mcp__github__get_pull_request_status \
  owner="graniterock" \
  repo="dbt_cloud" \
  pull_number=456

# 5. Create review
mcp__github__create_pull_request_review \
  owner="graniterock" \
  repo="dbt_cloud" \
  pull_number=456 \
  body="Code looks good, tests passed" \
  event="APPROVE"
```

### Workflow 3: Feature Development
```bash
# 1. Create feature branch
mcp__github__create_branch \
  owner="graniterock" \
  repo="dbt_cloud" \
  branch="feature/add-customer-models"

# 2. Push multiple files
mcp__github__push_files \
  owner="graniterock" \
  repo="dbt_cloud" \
  branch="feature/add-customer-models" \
  files=[
    {"path": "models/staging/stg_customers.sql", "content": "[SQL]"},
    {"path": "models/marts/dim_customers.sql", "content": "[SQL]"}
  ] \
  message="feat: Add customer staging and dimension models"

# 3. Create pull request
mcp__github__create_pull_request \
  owner="graniterock" \
  repo="dbt_cloud" \
  title="feat: Add customer data models" \
  head="feature/add-customer-models" \
  base="main" \
  body="## Summary\nAdded customer models...\n\n## Testing\ndbt test passed"

# 4. Monitor PR status
mcp__github__get_pull_request_status \
  owner="graniterock" \
  repo="dbt_cloud" \
  pull_number=[PR number from step 3]
```

### Workflow 4: Bug Tracking
```bash
# 1. Create bug report
mcp__github__create_issue \
  owner="graniterock" \
  repo="dbt_cloud" \
  title="Data quality issue: duplicate records in fct_orders" \
  body="## Issue\nDuplicates found...\n\n## Reproduction\n..." \
  labels=["bug", "data-quality"]

# 2. List all open bugs
mcp__github__list_issues \
  owner="graniterock" \
  repo="dbt_cloud" \
  state="open" \
  labels=["bug"]

# 3. After fix, update issue
mcp__github__add_issue_comment \
  owner="graniterock" \
  repo="dbt_cloud" \
  issue_number=[issue number] \
  body="Fixed in PR #456"

# 4. Close issue
mcp__github__update_issue \
  owner="graniterock" \
  repo="dbt_cloud" \
  issue_number=[issue number] \
  state="closed"
```

### Workflow 5: Repository Context Resolution
```bash
# ALWAYS resolve owner/repo before GitHub operations
# (Smart context resolution pattern)

# 1. Resolve repository context
python3 scripts/resolve-repo-context.py dbt_cloud
# Output: graniterock dbt_cloud

# 2. Use resolved context in GitHub MCP operations
mcp__github__list_issues owner="graniterock" repo="dbt_cloud" state="open"

# Alternative: Get just owner
owner=$(./scripts/get-repo-owner.sh dbt_cloud)
mcp__github__list_issues owner="$owner" repo="dbt_cloud" state="open"
```

---

## ⚠️ Important Notes

### Authentication & Permissions

**Personal Access Token (PAT)**:
- Stored in 1Password as `GITHUB_PERSONAL_ACCESS_TOKEN`
- **Scopes**: `repo`, `read:org`, `read:project`
- Required for all GitHub MCP operations

**Rate Limits**:
- **Standard API**: 5000 requests/hour (authenticated)
- **Search API**: 30 requests/minute
- **HTTP 429**: Exponential backoff recommended

### Known Issues

**Issue #1: get_file_contents Missing SHA** (CRITICAL)
- **Problem**: `get_file_contents` doesn't return file SHA
- **Impact**: Cannot reliably use `create_or_update_file` for updates
- **Workaround**: Use `push_files` for batch updates OR `list_commits` to get SHA
- **Confidence**: MEDIUM (0.60-0.65) - Functional workaround exists
- **Tracking**: https://github.com/github/github-mcp-server/issues/595

### Best Practices

**Repository Context Resolution**:
- ALWAYS resolve owner/repo from `config/repositories.json` first
- Eliminates cognitive overhead of remembering "graniterock"
- Ensures correct owner for each repository
- See pattern: `.claude/memory/patterns/github-repo-context-resolution.md`

**Search Optimization**:
- Use specific search qualifiers (`org:`, `type:`, `state:`, `label:`)
- Limit results to avoid rate limiting (`per_page` parameter)
- Search code uses different API with stricter rate limits (30/min)

**File Operations**:
- Prefer `push_files` for batch updates (single commit, multiple files)
- Use `create_or_update_file` for single file changes only
- Always provide descriptive commit messages

**Pull Request Reviews**:
- Check PR status before merging (CI/CD checks must pass)
- Use appropriate review events: `APPROVE`, `REQUEST_CHANGES`, `COMMENT`
- Update PR branch before merge if base branch has new commits

---

## 🔧 Troubleshooting

### Common Issues

**Issue**: "Resource not accessible by Personal Access Token"
- **Cause**: Insufficient PAT scopes OR token expired
- **Fix**: Regenerate PAT with correct scopes (repo, read:org, read:project)

**Issue**: "Not Found" error for get_file_contents
- **Cause**: Incorrect path OR file doesn't exist OR wrong branch
- **Fix**: Verify file path with repository browse, check branch name

**Issue**: "Reference does not exist" when creating branch
- **Cause**: Base branch (from_branch) doesn't exist
- **Fix**: Verify base branch exists, default is repository's default branch

**Issue**: "Pull request already exists"
- **Cause**: PR already open for head→base branch combination
- **Fix**: List existing PRs, update existing PR instead of creating new one

**Issue**: "API rate limit exceeded"
- **Cause**: Too many requests in short timeframe
- **Fix**: Implement exponential backoff, reduce request frequency, use pagination

**Issue**: "Validation failed: sha is required"
- **Cause**: Attempting create_or_update_file on existing file without SHA
- **Fix**: Use push_files for updates OR get SHA from list_commits first

---

## 📊 Confidence Levels

| Operation | Confidence | Notes |
|-----------|------------|-------|
| List/search operations | HIGH (0.95) | Core discovery operations |
| Get issue/PR details | HIGH (0.95) | Standard operations |
| Create issues/comments | HIGH (0.92) | Production-validated |
| Create PRs | HIGH (0.90) | Well-tested workflow |
| File operations (push_files) | HIGH (0.88) | Batch updates recommended |
| File operations (create_or_update) | MEDIUM (0.65) | Missing SHA workaround needed |
| Merge PRs | HIGH (0.85) | Status checks validation recommended |

---

## 🎓 When to Delegate to github-sleuth-expert

**Direct use OK** (ALL role agents):
- ✅ List issues/PRs in known repository
- ✅ Get issue/PR details
- ✅ Create issues for bugs/tasks
- ✅ Add comments to issues/PRs
- ✅ Get file contents (specific file path known)

**Delegate to specialist** (confidence <0.60):
- ❌ Cross-repository pattern analysis (org-wide issue search)
- ❌ Issue investigation (root cause analysis across multiple repos)
- ❌ Code change impact analysis (blast radius determination)
- ❌ Historical defect pattern analysis (recurring issues)
- ❌ Test coverage gap identification from repo history

---

## 📚 Related Resources

- **Full GitHub-MCP Documentation**: `knowledge/mcp-servers/github-mcp/`
- **github-sleuth-expert Agent**: `.claude/agents/specialists/github-sleuth-expert.md`
- **Repository Context Resolution**: `.claude/memory/patterns/github-repo-context-resolution.md`
- **MCP Integration Guide**: `.claude/memory/patterns/agent-mcp-integration-guide.md`
- **GitHub API Docs**: https://docs.github.com/en/rest

---

## 🔗 Integration Patterns

### With filesystem-mcp (Local + Remote Sync)
```
1. filesystem-mcp → Read local changes
2. github-mcp → Push changes to remote
3. github-mcp → Create PR for review
```

### With dbt-mcp (dbt Development Workflow)
```
1. dbt-mcp → Get model details
2. github-mcp → Create feature branch
3. github-mcp → Push dbt model changes
4. dbt-mcp → Run dbt tests
5. github-mcp → Create PR with test results
```

### With qa-engineer-role (Testing Workflow)
```
1. github-mcp → Get PR files (test scope)
2. qa-engineer-role → Execute testing
3. github-mcp → Create issue for bugs found
4. github-mcp → Add PR review (APPROVE or REQUEST_CHANGES)
```

---

## 🌟 Resolvable Repositories

Repositories configured in `config/repositories.json`:
- `da-agent-hub` → graniterock/da-agent-hub
- `dbt_cloud` → graniterock/dbt_cloud
- `react-sales-journal` → graniterock/react-sales-journal
- `dbt_errors_to_issues` → graniterock/dbt_errors_to_issues
- `roy_kent` → graniterock/roy_kent
- `sherlock` → graniterock/sherlock
- And more... (13+ repositories)

**Always resolve first**: `python3 scripts/resolve-repo-context.py <repo_name>`

---

*Created: 2025-10-08*
*Last Updated: 2025-10-08*
*Quick Reference for rapid MCP tool lookup*
