# Workflow Configuration Guide

Complete guide for setting up and customizing the DA Agent Hub workflows.

## 🏗️ Architecture Overview

The system consists of three main workflows:

1. **dbt Error Monitoring** (in your dbt repositories)
2. **dbt Issue Sleuthing** (in da-agent-hub)
3. **Claude Collaborative Fixes** (in da-agent-hub)

## 📋 Repository Setup

### 1. dbt Project Repository Configuration

#### Required Secrets

Set these secrets in your dbt project repository:

```bash
# dbt Cloud API access
DBT_CLOUD_API_TOKEN=your_dbt_cloud_token
DBT_CLOUD_ACCOUNT_ID=your_account_id

# GitHub cross-repository access
GITHUB_API_TOKEN=your_github_pat_token
```

#### Workflow File Location

```
your-dbt-repo/
└── .github/
    └── workflows/
        └── dbt-error-monitor.yml
```

#### Environment-Specific Configuration

For multiple environments (dev, staging, prod):

```yaml
# dbt-error-monitor.yml
jobs:
  monitor-production:
    # Production monitoring configuration
    env:
      DBT_ENVIRONMENT_ID: 308928  # Production environment

  monitor-staging:
    # Staging monitoring configuration
    env:
      DBT_ENVIRONMENT_ID: 308929  # Staging environment
```

### 2. da-agent-hub Repository Configuration

#### Required Secrets

```bash
# Claude AI authentication
ANTHROPIC_API_KEY=your_claude_oauth_token

# dbt Cloud API access (for investigation)
DBT_CLOUD_API_TOKEN=your_dbt_cloud_token
DBT_CLOUD_ACCOUNT_ID=your_account_id

# GitHub token (usually inherited)
GITHUB_TOKEN=automatically_provided
```

#### Workflow Files

```
da-agent-hub/
└── .github/
    └── workflows/
        ├── dbt-issue-sleuth.yml
        └── claude-collaborative-fixes.yml
```

## ⚙️ Workflow Customization

### dbt Error Monitoring Workflow

#### Schedule Configuration

```yaml
on:
  schedule:
    - cron: '30 6 * * *'    # 6:30 AM UTC daily
    - cron: '0 14 * * 1-5'  # 2:00 PM UTC weekdays only
  workflow_dispatch:         # Manual trigger
```

#### Project-Specific Settings

```yaml
env:
  DBT_PROJECT_NAME: your_project_name
  DBT_ENVIRONMENT_ID: your_environment_id
  GITHUB_REPO: your_org/your_repo

  # Optional: Custom settings
  IGNORE_WARNINGS: true
  ISSUE_LABELS: "dbt-error,high-priority"
  ASSIGNEES: "data-team"
```

#### Error Filtering

```yaml
# Custom environment variables for filtering
env:
  SEVERITY_THRESHOLD: "error"     # Only errors, not warnings
  MODEL_PATTERN: "rpt_*,dm_*"     # Only specific model patterns
  EXCLUDE_TESTS: "audit_*"        # Exclude certain test patterns
```

### Claude Investigation Workflow

#### Agent Selection Configuration

```yaml
# In the workflow prompt
Multi-Agent Analysis based on issue type:
- SQL errors → dbt-expert
- Performance → snowflake-expert
- Dashboards → tableau-expert
- Business logic → business-context
- Architecture → da-architect
- Data ingestion → dlthub-expert
```

#### Custom Investigation Prompts

```yaml
prompt: |
  # Custom Investigation Framework

  ## Context
  - **Organization**: Your Company Name
  - **Data Stack**: dbt + Snowflake + Tableau
  - **Priority Systems**: ERP, CRM, Operations

  ## Investigation Focus
  1. Check impact on business-critical reports
  2. Analyze data freshness requirements
  3. Consider compliance implications
  4. Assess user impact severity

  ## Your specific investigation criteria...
```

### Claude Collaborative Workflow

#### Trigger Customization

```yaml
# Customize trigger conditions
if: |
  (github.event_name == 'issue_comment' &&
   contains(github.event.comment.body, '@claude')) ||
  (github.event_name == 'issues' &&
   github.event.action == 'assigned' &&
   github.event.assignee.login == 'claude[bot]') ||
  (github.event_name == 'issues' &&
   github.event.action == 'labeled' &&
   contains(github.event.label.name, 'claude:'))
```

#### Custom Action Detection

```yaml
# Add custom action patterns
if [[ "$COMMENT_BODY" == *"create PR"* ]] ||
   [[ "$COMMENT_BODY" == *"implement fix"* ]] ||
   [[ "$COMMENT_BODY" == *"deploy solution"* ]]; then
  echo "action=create_pr" >> $GITHUB_OUTPUT
```

## 🔐 Security Configuration

### API Token Permissions

#### dbt Cloud API Token

Required permissions:
- **Account**: Read access to account information
- **Environment**: Read access to specific environments
- **Project**: Read access to project metadata
- **Job**: Read access to job runs and results

#### GitHub Personal Access Token

Required scopes:
```bash
# Classic token scopes
repo                    # Full repository access
workflow               # Workflow management
admin:repo_hook        # Repository webhooks
```

#### Claude OAuth Token

Obtain from Claude Pro/Max account:
1. Go to Claude settings
2. Generate OAuth token
3. Copy token to repository secrets

### Secrets Management

#### Repository-Level Secrets

```bash
# Set via GitHub CLI
gh secret set DBT_CLOUD_API_TOKEN --body "your_token"
gh secret set ANTHROPIC_API_KEY --body "your_oauth_token"

# Set via GitHub web interface
Repository → Settings → Secrets and variables → Actions
```

#### Organization-Level Secrets

For multiple repositories:

```bash
# Set organization secrets
gh secret set DBT_CLOUD_ACCOUNT_ID --org your_org --body "12345"
```

#### Environment-Specific Secrets

```yaml
# Use different secrets per environment
jobs:
  production:
    environment: production
    env:
      DBT_CLOUD_API_TOKEN: ${{ secrets.PROD_DBT_TOKEN }}

  staging:
    environment: staging
    env:
      DBT_CLOUD_API_TOKEN: ${{ secrets.STAGING_DBT_TOKEN }}
```

## 🎯 Advanced Configuration

### Cross-Repository Coordination

#### Repository Dispatch Configuration

```yaml
# In monitoring workflow
- name: Trigger Claude Investigation
  uses: peter-evans/repository-dispatch@v3
  with:
    token: ${{ secrets.GITHUB_API_TOKEN }}
    repository: graniterock/da-agent-hub
    event-type: dbt-issue-sleuth
    client-payload: |
      {
        "repository": "${{ github.repository }}",
        "project": "${{ env.DBT_PROJECT_NAME }}",
        "environment": "${{ env.DBT_ENVIRONMENT_ID }}",
        "trigger": "scheduled_monitoring",
        "run_id": "${{ github.run_id }}",
        "priority": "high"
      }
```

#### Multiple Project Support

```yaml
# Matrix strategy for multiple projects
strategy:
  matrix:
    project:
      - name: "roy_kent"
        environment_id: "308928"
        repo: "graniterock/roy_kent"
      - name: "dbt_cloud"
        environment_id: "308930"
        repo: "graniterock/dbt_cloud"
```

### Custom Agent Integration

#### Agent Selection Logic

```yaml
# Custom agent routing
- name: Select Expert Agent
  id: agent
  run: |
    if [[ "${{ github.event.issue.title }}" == *"performance"* ]]; then
      echo "agent=snowflake-expert" >> $GITHUB_OUTPUT
    elif [[ "${{ github.event.issue.title }}" == *"dashboard"* ]]; then
      echo "agent=tableau-expert" >> $GITHUB_OUTPUT
    else
      echo "agent=dbt-expert" >> $GITHUB_OUTPUT
    fi
```

#### Custom Agent Prompts

```yaml
prompt: |
  Use the ${{ steps.agent.outputs.agent }} agent for this analysis.

  ## Custom Analysis Framework for ${{ steps.agent.outputs.agent }}

  ### dbt-expert specific instructions:
  - Focus on SQL optimization
  - Check model dependencies
  - Analyze test coverage

  ### snowflake-expert specific instructions:
  - Analyze query performance
  - Check warehouse utilization
  - Review cost implications
```

### Notification Integration

#### Slack Integration

```yaml
- name: Notify Slack
  if: contains(github.event.issue.labels.*.name, 'high-priority')
  uses: rtCamp/action-slack-notify@v2
  env:
    SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}
    SLACK_MESSAGE: |
      🚨 High-priority dbt issue detected
      Issue: ${{ github.event.issue.title }}
      Claude investigation: Starting...
```

#### Email Notifications

```yaml
- name: Email Alert
  uses: dawidd6/action-send-mail@v3
  with:
    server_address: smtp.gmail.com
    server_port: 465
    username: ${{ secrets.EMAIL_USERNAME }}
    password: ${{ secrets.EMAIL_PASSWORD }}
    subject: "dbt Error Alert: ${{ github.event.issue.title }}"
    body: |
      A critical dbt error has been detected and is being investigated by Claude.

      View issue: ${{ github.event.issue.html_url }}
```

## 📊 Monitoring & Observability

### Workflow Health Monitoring

```yaml
- name: Health Check
  run: |
    # Check recent workflow success rates
    gh run list --workflow="dbt Error Monitoring" --limit 10 --json status

    # Alert if success rate drops below threshold
    SUCCESS_RATE=$(gh run list --workflow="dbt Error Monitoring" --limit 10 --json status | jq '[.[] | select(.status=="completed")] | length')
    if [[ $SUCCESS_RATE -lt 8 ]]; then
      echo "::warning::Workflow success rate below 80%"
    fi
```

### Performance Metrics

```yaml
- name: Collect Metrics
  run: |
    echo "workflow_duration=${{ job.duration }}" >> $GITHUB_OUTPUT
    echo "issues_processed=$(gh issue list --label dbt-error --limit 100 | wc -l)" >> $GITHUB_OUTPUT
    echo "claude_responses=$(gh issue list --json comments | jq '[.[] | .comments[] | select(.author.login=="claude[bot]")] | length')" >> $GITHUB_OUTPUT
```

## 🔧 Troubleshooting Configuration

### Debug Mode

```yaml
# Enable detailed logging
env:
  ACTIONS_STEP_DEBUG: true
  ACTIONS_RUNNER_DEBUG: true

- name: Debug Information
  run: |
    echo "Repository: ${{ github.repository }}"
    echo "Event: ${{ github.event_name }}"
    echo "Actor: ${{ github.actor }}"
    env | grep -E "(DBT_|GITHUB_|ANTHROPIC_)" | sort
```

### Validation Steps

```yaml
- name: Validate Configuration
  run: |
    # Check required secrets
    if [[ -z "${{ secrets.DBT_CLOUD_API_TOKEN }}" ]]; then
      echo "::error::DBT_CLOUD_API_TOKEN not set"
      exit 1
    fi

    # Test API connectivity
    curl -f -H "Authorization: Bearer ${{ secrets.DBT_CLOUD_API_TOKEN }}" \
      "https://cloud.getdbt.com/api/v2/accounts/${{ secrets.DBT_CLOUD_ACCOUNT_ID }}/"
```

### Error Recovery

```yaml
- name: Error Recovery
  if: failure()
  run: |
    # Create fallback issue
    gh issue create --title "Workflow Failure: dbt Monitoring" \
      --body "The dbt error monitoring workflow failed. Manual investigation required." \
      --label "infrastructure,urgent"
```

---

## 📚 Configuration Examples

### Basic Setup
See the main README for the minimal configuration.

### Enterprise Setup
For large organizations with multiple projects and environments.

### Custom Integration
For organizations with specific tool chains or requirements.

### Development Environment
For testing and developing workflow modifications.

---

**Next Steps**: After configuring your workflows, see the [Claude Interaction Guide](claude-interactions.md) for usage instructions.