# GitHub MCP Server - Quick Reference Card

**Last Updated**: 2025-10-08
**Package**: @modelcontextprotocol/server-github v2025.4.8
**Total Tools**: 28

---

## Essential Pattern

### 1. Always Resolve Context First
```bash
python3 scripts/resolve-repo-context.py <repo_name>
```

### 2. MCP Tool Recommendation Format
```markdown
**Tool**: mcp__github__<tool_name>
**Parameters**: {owner, repo, ...}
**Expected**: <result>
**Confidence**: HIGH/MEDIUM/LOW (0.XX)
```

---

## Tool Categories & Most Used

### Repository (9 tools) ⭐ Most Used
- `get_file_contents` - Read files/directories (⚠️ no SHA)
- `push_files` - Batch commit (BEST for multi-file)
- `create_or_update_file` - Single file (requires SHA)
- `search_code` - Find code patterns
- `list_commits` - Git history

### Issues (6 tools) ⭐ Most Used
- `list_issues` - Filtered list (state, labels, sort)
- `get_issue` - Full details
- `create_issue` - New issue
- `search_issues` - Cross-repo search

### Pull Requests (10 tools) ⭐ Most Used
- `list_pull_requests` - Filtered PRs
- `get_pull_request` - PR details
- `get_pull_request_status` - CI/CD checks
- `get_pull_request_files` - Changed files
- `create_pull_request` - New PR

### Search (3 tools)
- `search_repositories` - Find repos
- `search_code` - Find code
- `search_issues` - Find issues/PRs

---

## Quick Tool Selection

**I need to...**
- Read a file → `get_file_contents`
- Update multiple files → `push_files`
- List repo issues → `list_issues`
- Find code pattern → `search_code`
- Check PR status → `get_pull_request_status`
- See what changed in PR → `get_pull_request_files`
- Find all bugs → `search_issues` (q: "is:issue label:bug")

---

## Common Search Patterns

### Repository
```
org:graniterock language:Python
user:username topic:dbt
```

### Code
```
repo:owner/repo SELECT extension:sql
import pandas language:python
```

### Issues/PRs
```
is:issue is:open label:bug
is:pr review:required
```

---

## Known Issues ⚠️

**get_file_contents missing SHA** (Issue #595)
- Problem: Can't update files without SHA
- Workaround: Use `push_files` OR get SHA from `list_commits`
- Confidence: MEDIUM (0.60)

---

## Rate Limits

- **Standard**: 5,000/hour (PAT)
- **Search**: 30/minute
- **Strategy**: Batch, cache, paginate

---

## Confidence Levels

- **HIGH (0.80-0.95)**: Production-validated, straightforward
- **MEDIUM (0.60-0.79)**: Multi-step or workarounds
- **LOW (0.40-0.59)**: Experimental/edge cases

---

## Common Workflows

### Repo Analysis
```
1. get_file_contents (path: "/") → structure
2. list_commits → recent changes
3. search_code → patterns
```

### Issue Triage
```
1. list_issues → open issues
2. get_issue → details
3. add_issue_comment → analysis
```

### PR Review
```
1. get_pull_request_status → CI checks
2. get_pull_request_files → changes
3. get_pull_request_reviews → approvals
```

---

## Full Documentation

- **Complete Capabilities**: `.claude/memory/research/github-mcp-server-capabilities.md`
- **Enhancement Guide**: `.claude/memory/research/github-sleuth-expert-enhancement.md`
- **Summary**: `.claude/memory/research/GITHUB_MCP_RESEARCH_SUMMARY.md`

---

*Keep this card handy for quick MCP tool lookups!*
