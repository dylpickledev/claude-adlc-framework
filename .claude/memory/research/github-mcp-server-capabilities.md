# GitHub MCP Server Capabilities Documentation

## Overview

The GitHub MCP Server (`@modelcontextprotocol/server-github`) connects AI tools directly to GitHub's platform, enabling AI agents to interact with repositories, issues, pull requests, and more through the Model Context Protocol.

**Status**: Package deprecated in favor of GitHub's official server at `github/github-mcp-server`
**Current Implementation**: `@modelcontextprotocol/server-github` v2025.4.8 (available in Claude Code)
**Official Migration**: GitHub-hosted server at https://api.githubcopilot.com/mcp/

---

## Complete Tool Inventory

### Repository Management Tools

#### `create_or_update_file`
**Purpose**: Create a new file or completely overwrite an existing file in a GitHub repository

**Parameters**:
- `owner` (required): Repository owner (username or organization)
- `repo` (required): Repository name
- `path` (required): Path where to create/update the file
- `content` (required): Content of the file
- `message` (required): Commit message
- `branch` (required): Branch to create/update the file in
- `sha` (optional): SHA of the file being replaced (required when updating existing files)

**Returns**: Confirmation of file creation/update with commit details

**Use Cases**:
- Creating configuration files in repositories
- Updating documentation
- Committing code changes programmatically
- Automated file management

**Limitations**:
- Requires write access to repository
- SHA required for updates (prevents accidental overwrites)
- Single file per operation (use `push_files` for batch)

---

#### `get_file_contents`
**Purpose**: Get the contents of a file or directory from a GitHub repository

**Parameters**:
- `owner` (required): Repository owner (username or organization)
- `repo` (required): Repository name
- `path` (required): Path to the file or directory
- `branch` (optional): Branch to get contents from

**Returns**:
- For files: Base64 encoded content, size, SHA, download URL
- For directories: Array of files/subdirectories with metadata

**Use Cases**:
- Reading configuration files
- Analyzing code structure
- Retrieving documentation
- Directory exploration

**Known Issues**:
- Does NOT return SHA hash in response (Issue #595 in github-mcp-server)
- Makes updating files with `create_or_update_file` difficult (SHA is required)

---

#### `push_files`
**Purpose**: Push multiple files to a GitHub repository in a single commit

**Parameters**:
- `owner` (required): Repository owner (username or organization)
- `repo` (required): Repository name
- `branch` (required): Branch to push to (e.g., 'main' or 'master')
- `files` (required): Array of files to push
  - Each file object contains:
    - `path` (required): File path in repository
    - `content` (required): File content
- `message` (required): Commit message

**Returns**: Confirmation with commit SHA and details

**Use Cases**:
- Batch file operations
- Project scaffolding
- Multi-file updates in single commit
- Automated deployments

**Advantages**:
- Single commit for multiple files
- More efficient than individual `create_or_update_file` calls
- Preserves Git history better

---

#### `search_repositories`
**Purpose**: Search for GitHub repositories using GitHub's search syntax

**Parameters**:
- `query` (required): Search query (supports GitHub search syntax)
- `page` (optional): Page number for pagination (default: 1)
- `perPage` (optional): Number of results per page (default: 30, max: 100)

**Returns**: Array of repositories with metadata (name, description, stars, forks, language, etc.)

**Use Cases**:
- Finding repositories by topic or technology
- Discovering similar projects
- Market research on open source
- Finding code examples

**Search Syntax Examples**:
- `"user:graniterock language:SQL"` - User's SQL repos
- `"topic:dbt stars:>100"` - dbt projects with 100+ stars
- `"org:modelcontextprotocol"` - Org repositories
- `"react in:readme"` - Repos mentioning React in README

---

#### `create_repository`
**Purpose**: Create a new GitHub repository in your account

**Parameters**:
- `name` (required): Repository name
- `description` (optional): Repository description
- `private` (optional): Whether the repository should be private (default: false)
- `autoInit` (optional): Initialize with README.md (default: false)

**Returns**: Repository details including clone URLs, API URLs, permissions

**Use Cases**:
- Automated project setup
- Repository scaffolding
- Creating test repositories
- Batch repository creation

---

#### `fork_repository`
**Purpose**: Fork a GitHub repository to your account or specified organization

**Parameters**:
- `owner` (required): Repository owner (username or organization)
- `repo` (required): Repository name
- `organization` (optional): Organization to fork to (defaults to your personal account)

**Returns**: Forked repository details

**Use Cases**:
- Contributing to open source
- Creating repository copies for experimentation
- Organization-wide forks
- Automated fork management

---

#### `create_branch`
**Purpose**: Create a new branch in a GitHub repository

**Parameters**:
- `owner` (required): Repository owner (username or organization)
- `repo` (required): Repository name
- `branch` (required): Name for the new branch
- `from_branch` (optional): Source branch to create from (defaults to repository's default branch)

**Returns**: Branch creation confirmation with reference details

**Use Cases**:
- Feature branch creation
- Release branch setup
- Automated branching workflows
- Branch-based development automation

---

#### `list_commits`
**Purpose**: Get list of commits of a branch in a GitHub repository

**Parameters**:
- `owner` (required): Repository owner
- `repo` (required): Repository name
- `sha` (optional): Branch name or commit SHA to start from
- `page` (optional): Page number for pagination
- `perPage` (optional): Results per page

**Returns**: Array of commits with SHA, message, author, date, etc.

**Use Cases**:
- Git history analysis
- Change tracking
- Commit auditing
- Finding specific changes

---

### Issue Management Tools

#### `create_issue`
**Purpose**: Create a new issue in a GitHub repository

**Parameters**:
- `owner` (required): Repository owner
- `repo` (required): Repository name
- `title` (required): Issue title
- `body` (optional): Issue body/description
- `assignees` (optional): Array of usernames to assign
- `labels` (optional): Array of label names
- `milestone` (optional): Milestone number

**Returns**: Created issue details including issue number, URL, state

**Use Cases**:
- Bug reporting automation
- Feature request creation
- Task management
- Automated issue creation from errors/alerts

---

#### `list_issues`
**Purpose**: List issues in a GitHub repository with filtering options

**Parameters**:
- `owner` (required): Repository owner
- `repo` (required): Repository name
- `state` (optional): Issue state - "open", "closed", or "all" (default: "open")
- `labels` (optional): Array of label names to filter by
- `sort` (optional): Sort by "created", "updated", or "comments" (default: "created")
- `direction` (optional): Sort direction - "asc" or "desc" (default: "desc")
- `since` (optional): Only issues updated after this date (ISO 8601 format)
- `page` (optional): Page number
- `per_page` (optional): Results per page

**Returns**: Array of issues with full metadata

**Use Cases**:
- Issue triage
- Sprint planning
- Bug tracking
- Project management queries

---

#### `get_issue`
**Purpose**: Get details of a specific issue in a GitHub repository

**Parameters**:
- `owner` (required): Repository owner
- `repo` (required): Repository name
- `issue_number` (required): Issue number

**Returns**: Complete issue details including comments count, labels, assignees, state

**Use Cases**:
- Issue status checking
- Detailed issue analysis
- Context retrieval for AI responses
- Issue tracking

---

#### `update_issue`
**Purpose**: Update an existing issue in a GitHub repository

**Parameters**:
- `owner` (required): Repository owner
- `repo` (required): Repository name
- `issue_number` (required): Issue number to update
- `title` (optional): New issue title
- `body` (optional): New issue body
- `state` (optional): New state - "open" or "closed"
- `assignees` (optional): Array of usernames to assign
- `labels` (optional): Array of label names
- `milestone` (optional): Milestone number

**Returns**: Updated issue details

**Use Cases**:
- Issue state management
- Automated issue updates
- Label management
- Assignment changes

---

#### `add_issue_comment`
**Purpose**: Add a comment to an existing issue

**Parameters**:
- `owner` (required): Repository owner
- `repo` (required): Repository name
- `issue_number` (required): Issue number
- `body` (required): Comment text

**Returns**: Created comment details

**Use Cases**:
- Automated status updates
- Bot responses
- Investigation findings
- Collaboration automation

---

### Pull Request Tools

#### `create_pull_request`
**Purpose**: Create a new pull request in a GitHub repository

**Parameters**:
- `owner` (required): Repository owner (username or organization)
- `repo` (required): Repository name
- `title` (required): Pull request title
- `head` (required): The name of the branch where your changes are implemented
- `base` (required): The name of the branch you want the changes pulled into
- `body` (optional): Pull request body/description
- `draft` (optional): Whether to create the pull request as a draft
- `maintainer_can_modify` (optional): Whether maintainers can modify the pull request

**Returns**: Created pull request details including PR number, URL, state

**Use Cases**:
- Automated PR creation
- Feature branch workflows
- CI/CD integration
- Code review automation

---

#### `get_pull_request`
**Purpose**: Get details of a specific pull request

**Parameters**:
- `owner` (required): Repository owner
- `repo` (required): Repository name
- `pull_number` (required): Pull request number

**Returns**: Complete PR details including merge status, reviewers, checks

**Use Cases**:
- PR status checking
- Review coordination
- Merge readiness assessment
- CI/CD status monitoring

---

#### `list_pull_requests`
**Purpose**: List and filter repository pull requests

**Parameters**:
- `owner` (required): Repository owner
- `repo` (required): Repository name
- `state` (optional): PR state - "open", "closed", or "all" (default: "open")
- `head` (optional): Filter by head user or head organization and branch name
- `base` (optional): Filter by base branch name
- `sort` (optional): Sort by "created", "updated", "popularity", or "long-running" (default: "created")
- `direction` (optional): Sort direction - "asc" or "desc" (default: "desc")
- `page` (optional): Page number
- `per_page` (optional): Results per page (max 100)

**Returns**: Array of pull requests with metadata

**Use Cases**:
- PR queue management
- Review assignment
- Branch cleanup identification
- Release coordination

---

#### `get_pull_request_files`
**Purpose**: Get the list of files changed in a pull request

**Parameters**:
- `owner` (required): Repository owner
- `repo` (required): Repository name
- `pull_number` (required): Pull request number

**Returns**: Array of changed files with additions, deletions, patch content

**Use Cases**:
- Code review preparation
- Impact analysis
- Test planning
- Documentation verification

---

#### `get_pull_request_status`
**Purpose**: Get the combined status of all status checks for a pull request

**Parameters**:
- `owner` (required): Repository owner
- `repo` (required): Repository name
- `pull_number` (required): Pull request number

**Returns**: Combined status (success, pending, failure) and individual check statuses

**Use Cases**:
- CI/CD monitoring
- Merge readiness checking
- Automated merge decisions
- Status reporting

---

#### `get_pull_request_comments`
**Purpose**: Get the review comments on a pull request

**Parameters**:
- `owner` (required): Repository owner
- `repo` (required): Repository name
- `pull_number` (required): Pull request number

**Returns**: Array of review comments with file, line, and comment content

**Use Cases**:
- Review analysis
- Feedback aggregation
- Code quality insights
- Discussion tracking

---

#### `get_pull_request_reviews`
**Purpose**: Get the reviews on a pull request

**Parameters**:
- `owner` (required): Repository owner
- `repo` (required): Repository name
- `pull_number` (required): Pull request number

**Returns**: Array of reviews with state (APPROVED, CHANGES_REQUESTED, COMMENTED)

**Use Cases**:
- Approval tracking
- Review workflow automation
- Merge readiness assessment
- Compliance verification

---

#### `create_pull_request_review`
**Purpose**: Create a review on a pull request

**Parameters**:
- `owner` (required): Repository owner
- `repo` (required): Repository name
- `pull_number` (required): Pull request number
- `body` (required): The body text of the review
- `event` (required): The review action - "APPROVE", "REQUEST_CHANGES", or "COMMENT"
- `commit_id` (optional): The SHA of the commit that needs a review
- `comments` (optional): Array of review comments
  - Each comment contains:
    - `path` (required): The relative path to the file
    - `body` (required): Text of the review comment
    - Either:
      - `position` (number): Position in the diff
      - OR `line` (number): Line number in the file

**Returns**: Created review details

**Use Cases**:
- Automated code review
- Policy enforcement
- Security scanning feedback
- Quality gate implementation

---

#### `merge_pull_request`
**Purpose**: Merge a pull request

**Parameters**:
- `owner` (required): Repository owner
- `repo` (required): Repository name
- `pull_number` (required): Pull request number
- `merge_method` (optional): Merge method - "merge", "squash", or "rebase" (default: "merge")
- `commit_title` (optional): Title for the automatic commit message
- `commit_message` (optional): Extra detail to append to automatic commit message

**Returns**: Merge confirmation with SHA and merge status

**Use Cases**:
- Automated merging
- CI/CD workflows
- Release automation
- Branch management

---

#### `update_pull_request_branch`
**Purpose**: Update a pull request branch with the latest changes from the base branch

**Parameters**:
- `owner` (required): Repository owner
- `repo` (required): Repository name
- `pull_number` (required): Pull request number
- `expected_head_sha` (optional): The expected SHA of the pull request's HEAD ref

**Returns**: Update status and new HEAD SHA

**Use Cases**:
- Keeping PRs up-to-date
- Merge conflict prevention
- CI re-triggering
- Automated branch maintenance

---

### Search Tools

#### `search_code`
**Purpose**: Search for code across GitHub repositories

**Parameters**:
- `q` (required): Search query (supports GitHub code search syntax)
- `sort` (optional): Sort field (not commonly used for code search)
- `order` (optional): Sort order - "asc" or "desc"
- `page` (optional): Page number (minimum: 1)
- `per_page` (optional): Results per page (minimum: 1, maximum: 100)

**Returns**: Array of code matches with repository, file path, and code snippets

**Use Cases**:
- Finding code patterns
- Security vulnerability scanning
- API usage examples
- Code reference lookup

**Search Syntax Examples**:
- `"q=addClass in:file language:js repo:jquery/jquery"`
- `"q=spark size:>1000 extension:scala"`
- `"q=SQLAlchemy language:python"`

**Limitations**:
- GitHub API rate limits apply
- Search results limited to 100 per page
- May not include very recent changes

---

#### `search_issues`
**Purpose**: Search for issues and pull requests across GitHub repositories

**Parameters**:
- `q` (required): Search query (supports GitHub issues search syntax)
- `sort` (optional): Sort by "comments", "reactions", "reactions-+1", "reactions--1", "reactions-smile", "reactions-thinking_face", "reactions-heart", "reactions-tada", "interactions", "created", "updated"
- `order` (optional): Sort order - "asc" or "desc"
- `page` (optional): Page number (minimum: 1)
- `per_page` (optional): Results per page (minimum: 1, maximum: 100)

**Returns**: Array of issues/PRs with full metadata

**Use Cases**:
- Cross-repository issue tracking
- Bug pattern analysis
- Feature request aggregation
- Community engagement metrics

**Search Syntax Examples**:
- `"q=type:issue state:open label:bug repo:owner/repo"`
- `"q=is:pr is:open review:required"`
- `"q=type:issue author:username created:>2025-01-01"`

---

#### `search_users`
**Purpose**: Search for users on GitHub

**Parameters**:
- `q` (required): Search query (supports GitHub users search syntax)
- `sort` (optional): Sort by "followers", "repositories", or "joined"
- `order` (optional): Sort order - "asc" or "desc"
- `page` (optional): Page number (minimum: 1)
- `per_page` (optional): Results per page (minimum: 1, maximum: 100)

**Returns**: Array of user profiles with metadata

**Use Cases**:
- Finding contributors
- Recruiting developers
- Community discovery
- Collaboration identification

**Search Syntax Examples**:
- `"q=location:Seattle language:Python"`
- `"q=followers:>1000 repos:>10"`
- `"q=data engineer in:fullname"`

---

## Authentication & Configuration

### GitHub Personal Access Token (PAT)

**Required Scopes**:
- `repo` - Full control of private repositories (includes read/write)
- OR `public_repo` - For public repositories only (read/write)
- `read:org` - Read organization membership and teams (optional, for org access)
- `read:project` - Read project boards (optional)

**Token Creation**:
1. Go to GitHub Settings > Developer settings > Personal access tokens
2. Generate new token (classic or fine-grained)
3. Select required scopes
4. Store securely in 1Password or environment variables

### Configuration in Claude Code

**.mcp.json**:
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"
      }
    }
  }
}
```

### GitHub's Official MCP Server (New)

**Remote Server**: https://api.githubcopilot.com/mcp/
**Authentication**: OAuth or PAT
**Supported Clients**: VS Code, Claude Desktop, Cursor

**Advantages**:
- Hosted by GitHub (no local Docker needed)
- Automatic updates
- OAuth authentication (one-click setup)
- Dynamic toolset discovery

---

## Toolsets (GitHub Official Server)

The GitHub official MCP server organizes tools into toolsets that can be enabled/disabled:

1. **context** - User and GitHub context tools
2. **repos** - Repository management and code browsing
3. **issues** - Issue management and automation
4. **pull_requests** - Pull request workflows
5. **actions** - GitHub Actions CI/CD tools
6. **code_security** - Code scanning and security alerts
7. **dependabot** - Dependabot automation
8. **discussions** - GitHub Discussions tools
9. **experiments** - Experimental/beta features
10. **gists** - GitHub Gist management
11. **notifications** - Notification management
12. **orgs** - Organization management
13. **projects** - GitHub Projects tools
14. **secret_protection** - Secret scanning tools
15. **security_advisories** - Security advisory tools
16. **stargazers** - Stargazer analytics
17. **users** - User management tools

**Configuration**:
```json
{
  "env": {
    "GITHUB_TOOLSETS": "repos,issues,pull_requests,actions,code_security"
  }
}
```

Use `"all"` to enable all toolsets.

---

## Rate Limits & Limitations

### GitHub API Rate Limits

**Authenticated Requests**:
- 5,000 requests per hour (standard PAT)
- 15,000 requests per hour (OAuth app)

**Search API**:
- 30 requests per minute (authenticated)
- 10 requests per minute (unauthenticated)

**Rate Limit Headers**:
- `X-RateLimit-Limit` - Maximum requests per hour
- `X-RateLimit-Remaining` - Requests remaining
- `X-RateLimit-Reset` - Time when limit resets (Unix timestamp)

### Tool-Specific Limitations

**`get_file_contents`**:
- Known issue: Does not return SHA hash (required for updates)
- Workaround: Use `list_commits` or GitHub API directly to get SHA

**Search Tools**:
- Maximum 100 results per page
- Search may not include very recent changes
- Rate limited to 30 requests/minute

**`push_files`**:
- Limited by repository size and GitHub's file size limits
- Single commit for batch (good for Git history)

**Branch Operations**:
- Cannot force push (Git history preserved)
- Automatic branch creation on file operations

---

## Common Use Cases & Examples

### Automated Issue Management

**Use Case**: Create issues from error logs
```
1. Detect error in logs
2. Call search_issues to check if issue already exists
3. If not exists, call create_issue with error details
4. Call add_issue_comment with additional context
5. Call update_issue to add labels (e.g., "bug", "auto-generated")
```

---

### Code Review Workflow

**Use Case**: Automated PR review and merge
```
1. Call list_pull_requests to get open PRs
2. For each PR:
   a. Call get_pull_request_files to analyze changes
   b. Call get_pull_request_status to check CI/CD
   c. Call create_pull_request_review with automated feedback
   d. If approved and tests pass, call merge_pull_request
```

---

### Repository Analysis

**Use Case**: Analyze repository structure and recent changes
```
1. Call get_file_contents on root directory to see structure
2. Call list_commits to see recent changes
3. Call search_code to find specific patterns
4. Call get_file_contents on specific files for detailed analysis
```

---

### Multi-File Project Setup

**Use Case**: Scaffold new project in repository
```
1. Call create_branch to create feature branch
2. Call push_files with multiple project files:
   - README.md
   - .gitignore
   - config files
   - initial source files
3. Call create_pull_request to propose changes
```

---

### Cross-Repository Search

**Use Case**: Find all repos using a specific technology
```
1. Call search_repositories with technology query
2. For each repo:
   a. Call get_file_contents to read package.json or requirements.txt
   b. Call search_code to find specific usage patterns
   c. Aggregate findings for analysis
```

---

## Best Practices

### 1. Repository Context Resolution
Always resolve repository owner/name before making calls:
```bash
python3 scripts/resolve-repo-context.py dbt_cloud
# Output: graniterock dbt_cloud
```

### 2. Error Handling
- Always check rate limit headers
- Implement retry logic with exponential backoff
- Handle 404 (not found) and 403 (forbidden) gracefully
- Validate SHA before file updates

### 3. Batch Operations
- Use `push_files` for multi-file commits (better Git history)
- Use `list_*` tools with pagination for large datasets
- Cache results when appropriate to reduce API calls

### 4. Security
- Store PAT in 1Password or secure environment variables
- Use minimum required scopes
- Rotate tokens regularly
- Never commit tokens to repositories

### 5. Performance
- Filter searches to reduce result sets
- Use pagination to avoid large payloads
- Leverage caching for static data
- Monitor rate limits proactively

---

## Migration Notes

### From @modelcontextprotocol/server-github to GitHub Official

The `@modelcontextprotocol/server-github` package is deprecated. GitHub's official server offers:

**Advantages**:
- Hosted service (no Docker required)
- OAuth authentication (easier setup)
- Automatic updates
- Dynamic toolset discovery
- More comprehensive toolsets (16+ vs ~20 tools)

**Migration Path**:
1. Update .mcp.json to use GitHub's hosted server
2. Switch to OAuth authentication (or continue with PAT)
3. Enable desired toolsets via GITHUB_TOOLSETS env var
4. Test all existing integrations

**Backward Compatibility**:
Current tools should continue working, but check for:
- Tool name changes
- Parameter schema updates
- New required fields

---

## References

- **GitHub MCP Server Repository**: https://github.com/github/github-mcp-server
- **MCP Servers Collection**: https://github.com/modelcontextprotocol/servers
- **GitHub API Documentation**: https://docs.github.com/en/rest
- **MCP Protocol Spec**: https://modelcontextprotocol.io/
- **GitHub Blog - Practical Guide**: https://github.blog/ai-and-ml/generative-ai/a-practical-guide-on-how-to-use-the-github-mcp-server/
- **npm Package**: https://www.npmjs.com/package/@modelcontextprotocol/server-github

---

## Changelog

- **2025-10-08**: Initial comprehensive documentation based on research
- Package version: `@modelcontextprotocol/server-github` v2025.4.8
- Documented 28 tools across repository, issue, PR, and search categories
- Identified known issues (get_file_contents SHA missing)
- Documented GitHub official server migration path
