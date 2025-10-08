# GitHub Sleuth Expert - MCP Tool Enhancement Guide

## Purpose
This document provides detailed GitHub MCP tool knowledge for the `github-sleuth-expert` specialist agent, enabling it to provide precise, validated recommendations for GitHub repository analysis, issue management, and cross-repo coordination.

---

## Agent Integration Pattern

### Recommended MCP Tool Execution Pattern
The specialist agent creates recommendations, main Claude executes them:

```markdown
### RECOMMENDED MCP TOOL EXECUTION
**Tool**: mcp__github__<tool_name>
**Parameters**:
  - owner: "graniterock"
  - repo: "dbt_cloud"
  - <additional parameters>
**Expected Result**: <what this should return>
**Fallback**: <alternative approach if MCP unavailable>
**Confidence**: HIGH (0.85) - Production-validated pattern
```

Main Claude then executes the MCP tool call and returns results.

---

## Core Competencies for GitHub Sleuth Expert

### 1. Repository Context Resolution
**Always resolve owner/repo before recommendations**:

```bash
# Resolve from config/repositories.json
python3 scripts/resolve-repo-context.py dbt_cloud
# Returns: graniterock dbt_cloud
```

**Tool Recommendation Template**:
```markdown
**Prerequisite**: Resolve repository context
`python3 scripts/resolve-repo-context.py <repo_name>`

**Tool**: mcp__github__<tool_name>
**Parameters**:
  - owner: "<resolved_owner>"
  - repo: "<resolved_repo>"
```

---

### 2. Repository Intelligence Tools

#### Deep Code Analysis Pattern
**Scenario**: Understanding codebase structure and patterns

**Tool Sequence**:
```markdown
1. **Directory Structure**
   Tool: mcp__github__get_file_contents
   Parameters: {owner, repo, path: "/", branch: "main"}
   Returns: Directory tree

2. **Recent Changes**
   Tool: mcp__github__list_commits
   Parameters: {owner, repo, sha: "main", per_page: 20}
   Returns: Recent commit history

3. **Code Pattern Search**
   Tool: mcp__github__search_code
   Parameters: {q: "repo:owner/repo <pattern>"}
   Returns: Code matches with context
```

**Use Cases**:
- Understanding project architecture
- Finding implementation patterns
- Locating specific functionality
- Analyzing recent changes

---

#### Cross-Repository Analysis Pattern
**Scenario**: Finding patterns across multiple repositories

**Tool Sequence**:
```markdown
1. **Repository Discovery**
   Tool: mcp__github__search_repositories
   Parameters: {query: "org:graniterock language:SQL"}
   Returns: Matching repositories

2. **For Each Repository**:
   a. Tool: mcp__github__get_file_contents
      Parameters: {owner, repo, path: "dbt_project.yml"}
      Returns: dbt configuration

   b. Tool: mcp__github__search_code
      Parameters: {q: "repo:owner/repo path:models/ SELECT"}
      Returns: SQL model patterns
```

**Use Cases**:
- Stack analysis across team
- Finding code duplication
- Identifying migration candidates
- Technology usage patterns

---

### 3. Issue Management Intelligence

#### Issue Triage Pattern
**Scenario**: Analyzing and categorizing issues

**Tool Sequence**:
```markdown
1. **Get Open Issues**
   Tool: mcp__github__list_issues
   Parameters: {
     owner, repo,
     state: "open",
     sort: "created",
     direction: "desc"
   }
   Returns: Recent open issues

2. **For High-Priority Issues**:
   Tool: mcp__github__get_issue
   Parameters: {owner, repo, issue_number}
   Returns: Full issue details with comments

3. **Add Analysis**
   Tool: mcp__github__add_issue_comment
   Parameters: {
     owner, repo, issue_number,
     body: "<AI analysis and recommendations>"
   }
```

**Use Cases**:
- Bug triage automation
- Feature request analysis
- Priority assessment
- Issue categorization

---

#### Cross-Repo Issue Tracking Pattern
**Scenario**: Finding related issues across repositories

**Tool Sequence**:
```markdown
1. **Global Issue Search**
   Tool: mcp__github__search_issues
   Parameters: {
     q: "org:graniterock is:issue is:open label:bug <keyword>"
   }
   Returns: All matching issues

2. **Aggregate by Repository**
   Process: Group results by repo

3. **For Each Repository**:
   Tool: mcp__github__list_issues
   Parameters: {owner, repo, labels: ["bug"], state: "open"}
   Returns: Repository-specific bugs
```

**Use Cases**:
- Cross-repo bug tracking
- Feature coordination
- Dependency issue discovery
- Migration impact analysis

---

### 4. Pull Request Analysis

#### PR Review Intelligence Pattern
**Scenario**: Comprehensive PR analysis

**Tool Sequence**:
```markdown
1. **Get PR List**
   Tool: mcp__github__list_pull_requests
   Parameters: {owner, repo, state: "open"}
   Returns: Open PRs

2. **For Each PR**:
   a. Tool: mcp__github__get_pull_request
      Parameters: {owner, repo, pull_number}
      Returns: PR metadata and status

   b. Tool: mcp__github__get_pull_request_files
      Parameters: {owner, repo, pull_number}
      Returns: Changed files with diffs

   c. Tool: mcp__github__get_pull_request_status
      Parameters: {owner, repo, pull_number}
      Returns: CI/CD check status

   d. Tool: mcp__github__get_pull_request_reviews
      Parameters: {owner, repo, pull_number}
      Returns: Existing reviews
```

**Use Cases**:
- PR queue management
- Review prioritization
- Merge readiness assessment
- Code quality analysis

---

#### PR Comment Analysis Pattern
**Scenario**: Understanding PR discussions and feedback

**Tool Sequence**:
```markdown
1. **Get Review Comments**
   Tool: mcp__github__get_pull_request_comments
   Parameters: {owner, repo, pull_number}
   Returns: Line-specific review comments

2. **Analyze Discussion**
   Process: Extract themes, concerns, questions

3. **Provide Summary**
   Aggregate: Common issues, approval blockers
```

**Use Cases**:
- Review feedback aggregation
- Common issue identification
- Documentation of discussions
- Knowledge extraction

---

### 5. CI/CD & Actions Intelligence

#### Workflow Failure Analysis Pattern
**Scenario**: Understanding why builds fail (when Actions toolset enabled)

**Tool Sequence** (GitHub Official Server):
```markdown
1. **List Workflow Runs**
   Tool: list_workflow_runs (actions toolset)
   Parameters: {owner, repo, status: "failed"}
   Returns: Failed workflow runs

2. **Get Workflow Logs**
   Tool: get_workflow_run_logs (actions toolset)
   Parameters: {owner, repo, run_id}
   Returns: Detailed failure logs

3. **Cross-Reference PRs**
   Tool: mcp__github__search_issues
   Parameters: {q: "repo:owner/repo is:pr is:open"}
   Correlation: Match failures to PRs
```

**Use Cases**:
- Build failure debugging
- CI/CD optimization
- Test reliability analysis
- Deployment issue tracking

---

### 6. Security & Code Quality

#### Security Alert Pattern (GitHub Official Server)
**Scenario**: Analyzing security findings

**Tool Sequence**:
```markdown
1. **List Code Scanning Alerts**
   Tool: list_code_scanning_alerts (code_security toolset)
   Parameters: {owner, repo, state: "open"}
   Returns: Security findings

2. **Get Alert Details**
   Tool: get_code_scanning_alert (code_security toolset)
   Parameters: {owner, repo, alert_number}
   Returns: Detailed security analysis

3. **Dependabot Alerts**
   Tool: <dependabot toolset>
   Returns: Dependency vulnerabilities
```

**Use Cases**:
- Security auditing
- Vulnerability tracking
- Dependency management
- Compliance verification

---

## Known Issues & Workarounds

### Issue: get_file_contents Missing SHA

**Problem**: `get_file_contents` does not return SHA hash needed for `create_or_update_file`

**Workaround**:
```markdown
**Recommended Approach**:
1. Tool: mcp__github__list_commits
   Parameters: {owner, repo, path: "<file_path>", per_page: 1}
   Returns: Most recent commit with SHA

2. Tool: mcp__github__get_file_contents
   Parameters: {owner, repo, path: "<file_path>"}
   Returns: File content

3. Extract SHA from commit or use GitHub API directly
   Alternative: Use push_files for batch operations (no SHA required)

**Confidence**: MEDIUM (0.60) - Workaround required
```

**GitHub Issue Reference**: https://github.com/github/github-mcp-server/issues/595

---

## Search Syntax Patterns

### Repository Search
```
Examples:
- "org:graniterock language:Python stars:>5"
- "user:username topic:dbt fork:false"
- "dbt in:name,description,readme"
- "size:<1000 created:>2025-01-01"
```

### Code Search
```
Examples:
- "repo:owner/repo addClass in:file language:js"
- "spark size:>1000 extension:scala"
- "SELECT path:models/ extension:sql repo:owner/repo"
- "import pandas path:src/ language:python"
```

### Issue/PR Search
```
Examples:
- "is:issue is:open label:bug repo:owner/repo"
- "is:pr is:open review:required author:username"
- "type:issue created:>2025-01-01 sort:comments-desc"
- "is:pr is:merged merged:>2025-09-01"
```

### User Search
```
Examples:
- "location:Seattle language:Python followers:>100"
- "data engineer in:fullname"
- "repos:>10 followers:>500 location:USA"
```

---

## Rate Limiting Strategy

### Rate Limit Awareness
```markdown
**Before Expensive Operations**:
Check: X-RateLimit-Remaining header
Alert: If remaining < 100 requests

**Search Operations**:
Limit: 30 requests/minute (authenticated)
Strategy: Batch searches, cache results

**Standard Operations**:
Limit: 5,000 requests/hour (PAT)
Strategy: Pagination, efficient queries
```

---

## Tool Selection Decision Tree

### When to Use Which Tool?

**Need file contents?**
- Single file → `get_file_contents`
- Multiple files in one commit → `push_files`
- Directory listing → `get_file_contents` (path: directory)

**Need issue information?**
- Specific issue → `get_issue`
- List with filters → `list_issues`
- Cross-repo search → `search_issues`

**Need PR information?**
- Specific PR → `get_pull_request`
- Changed files → `get_pull_request_files`
- CI/CD status → `get_pull_request_status`
- Review status → `get_pull_request_reviews`
- Review comments → `get_pull_request_comments`

**Need to find something?**
- Repositories → `search_repositories`
- Code patterns → `search_code`
- Issues/PRs → `search_issues`
- Users → `search_users`

**Need to create/modify?**
- Single file → `create_or_update_file` (with SHA)
- Multiple files → `push_files` (batch)
- New repo → `create_repository`
- New branch → `create_branch`
- Fork → `fork_repository`

---

## Confidence Scoring Guidelines

### HIGH Confidence (0.80-0.95)
- Standard CRUD operations (create_issue, get_file_contents)
- Well-documented search patterns
- Production-validated workflows
- Straightforward parameter usage

### MEDIUM Confidence (0.60-0.79)
- Complex multi-step workflows
- Requires workarounds (e.g., SHA issue)
- Rate limiting considerations
- Edge case handling needed

### LOW Confidence (0.40-0.59)
- Experimental features
- Undocumented behavior
- Complex permission scenarios
- GitHub API quirks

### RESEARCH NEEDED (<0.40)
- Novel use cases
- Conflicting documentation
- API version differences
- Enterprise-specific behavior

---

## Integration with Other Specialist Agents

### Coordination Patterns

**With dbt-expert**:
- Analyze dbt_project.yml files across repos
- Find model dependencies via code search
- Track dbt issues and PRs

**With snowflake-expert**:
- Coordinate deployment branches
- Track migration issues
- Find SQL patterns in repos

**With documentation-expert**:
- Extract README content
- Find documentation gaps
- Coordinate doc updates

**With qa-coordinator**:
- Track test failures via Actions
- Correlate bugs with PRs
- Monitor CI/CD health

---

## Example Recommendations

### Example 1: Repository Structure Analysis
```markdown
### TASK: Analyze dbt_cloud repository structure

### RECOMMENDED MCP TOOL SEQUENCE

**Step 1: Resolve Repository Context**
Command: `python3 scripts/resolve-repo-context.py dbt_cloud`
Expected: "graniterock dbt_cloud"

**Step 2: Get Directory Structure**
Tool: mcp__github__get_file_contents
Parameters:
  - owner: "graniterock"
  - repo: "dbt_cloud"
  - path: "/"
  - branch: "master"
Expected Result: Directory tree showing models/, macros/, etc.
Confidence: HIGH (0.90)

**Step 3: Get dbt Configuration**
Tool: mcp__github__get_file_contents
Parameters:
  - owner: "graniterock"
  - repo: "dbt_cloud"
  - path: "dbt_project.yml"
Expected Result: dbt project configuration
Confidence: HIGH (0.90)

**Step 4: Analyze Recent Changes**
Tool: mcp__github__list_commits
Parameters:
  - owner: "graniterock"
  - repo: "dbt_cloud"
  - sha: "master"
  - per_page: 20
Expected Result: Recent commits with messages and authors
Confidence: HIGH (0.90)

**Fallback**: Manual repository browsing via GitHub web interface
```

---

### Example 2: Cross-Repo Bug Analysis
```markdown
### TASK: Find all open bugs across DA team repositories

### RECOMMENDED MCP TOOL SEQUENCE

**Step 1: Global Bug Search**
Tool: mcp__github__search_issues
Parameters:
  - q: "org:graniterock is:issue is:open label:bug"
  - sort: "created"
  - order: "desc"
  - per_page: 100
Expected Result: All open bugs across organization
Confidence: HIGH (0.85)

**Step 2: Repository-Specific Analysis**
For each critical repository:

Tool: mcp__github__list_issues
Parameters:
  - owner: "graniterock"
  - repo: "<repo_name>"
  - state: "open"
  - labels: ["bug"]
  - sort: "updated"
Expected Result: Repository-specific bug list
Confidence: HIGH (0.90)

**Step 3: Get High-Priority Bug Details**
For issues with priority labels:

Tool: mcp__github__get_issue
Parameters:
  - owner: "graniterock"
  - repo: "<repo_name>"
  - issue_number: <number>
Expected Result: Full issue details with comments
Confidence: HIGH (0.90)

**Analysis Output**:
- Bug count by repository
- Common patterns
- Priority distribution
- Recommended triage actions

**Fallback**: GitHub web interface project boards
```

---

### Example 3: PR Review Automation
```markdown
### TASK: Analyze open PRs for merge readiness

### RECOMMENDED MCP TOOL SEQUENCE

**Step 1: Get Open PRs**
Tool: mcp__github__list_pull_requests
Parameters:
  - owner: "graniterock"
  - repo: "dbt_cloud"
  - state: "open"
  - sort: "created"
Expected Result: List of open PRs
Confidence: HIGH (0.90)

**Step 2: For Each PR - Get Status**
Tool: mcp__github__get_pull_request_status
Parameters:
  - owner: "graniterock"
  - repo: "dbt_cloud"
  - pull_number: <number>
Expected Result: CI/CD check status (success/failure/pending)
Confidence: HIGH (0.90)

**Step 3: Get Review Status**
Tool: mcp__github__get_pull_request_reviews
Parameters:
  - owner: "graniterock"
  - repo: "dbt_cloud"
  - pull_number: <number>
Expected Result: Approvals/change requests
Confidence: HIGH (0.90)

**Step 4: Get Changed Files**
Tool: mcp__github__get_pull_request_files
Parameters:
  - owner: "graniterock"
  - repo: "dbt_cloud"
  - pull_number: <number>
Expected Result: List of changed files with additions/deletions
Confidence: HIGH (0.90)

**Merge Readiness Criteria**:
- ✅ All CI checks passing
- ✅ At least one approval
- ✅ No change requests outstanding
- ✅ Branch up to date with base

**Recommendation**: Provide merge readiness report for each PR

**Fallback**: Manual PR review via GitHub web interface
```

---

## Best Practices Summary

### 1. Always Resolve Context First
```bash
python3 scripts/resolve-repo-context.py <repo_name>
```

### 2. Use Appropriate Pagination
- Start with `per_page: 30` for explorations
- Use `per_page: 100` for comprehensive analysis
- Implement pagination for large datasets

### 3. Leverage Search Operators
- Use specific filters to reduce API calls
- Combine operators for precise queries
- Cache search results when appropriate

### 4. Handle Rate Limits Gracefully
- Monitor remaining quota
- Batch operations when possible
- Implement exponential backoff

### 5. Provide Fallback Options
- Always include manual alternative
- Document workarounds for known issues
- Suggest GitHub web interface when appropriate

### 6. Clear Confidence Scoring
- HIGH: Production-validated, straightforward
- MEDIUM: Requires workarounds or multi-step
- LOW: Experimental or edge cases
- Document reasoning for score

---

## Migration to GitHub Official Server

### When to Recommend GitHub Official MCP Server

**Advantages**:
- No Docker management required
- Automatic updates
- OAuth authentication (easier setup)
- 16+ toolsets vs ~20 tools
- Dynamic toolset discovery
- GitHub Actions integration
- Security scanning tools

**Current Setup** (da-agent-hub):
```json
{
  "github": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-github"],
    "env": {
      "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"
    }
  }
}
```

**Recommended Migration** (Future):
```json
{
  "github": {
    "command": "npx",
    "args": ["-y", "@github/github-mcp-server"],
    "env": {
      "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}",
      "GITHUB_TOOLSETS": "repos,issues,pull_requests,actions,code_security"
    }
  }
}
```

**OR use hosted version**:
- URL: https://api.githubcopilot.com/mcp/
- Auth: OAuth or PAT
- No local installation required

---

## References

- **Pattern Documentation**: `.claude/memory/patterns/github-repo-context-resolution.md`
- **Repository Config**: `config/repositories.json`
- **Tool Definitions**: See function definitions in system prompt
- **GitHub Official Server**: https://github.com/github/github-mcp-server
- **Comprehensive Capabilities Doc**: `.claude/memory/research/github-mcp-server-capabilities.md`

---

## Agent Enhancement Checklist

When updating `github-sleuth-expert.md`:

- [ ] Add repository context resolution pattern
- [ ] Document all 28 available tools
- [ ] Include tool selection decision tree
- [ ] Add confidence scoring guidelines
- [ ] Document known issues and workarounds
- [ ] Provide example recommendations with MCP tool patterns
- [ ] Add search syntax patterns
- [ ] Include rate limiting strategy
- [ ] Document coordination with other specialists
- [ ] Add migration notes for GitHub official server
- [ ] Update confidence scores for production-validated patterns

---

*Last Updated: 2025-10-08*
*Package: @modelcontextprotocol/server-github v2025.4.8*
*Total Tools Documented: 28*
