# Detailed Setup Guide

## Automated Operations Setup

### Repository Architecture

The automated system works across **three repositories**:

1. **Your dbt Project** (e.g., `roy_kent`, `dbt_cloud`)
   - Contains dbt models, tests, and configurations
   - Gets the monitoring workflow

2. **graniterock/dbt_errors_to_issues**
   - Shared Python scripts for error processing
   - Handles dbt Cloud API integration

3. **graniterock/da-agent-hub** (this repo)
   - Claude AI investigation system
   - Interactive collaboration workflows

### Secret Configuration

#### In Your dbt Project Repository:
```bash
DBT_CLOUD_API_TOKEN=your_dbt_cloud_api_token
DBT_CLOUD_ACCOUNT_ID=your_account_id
GITHUB_API_TOKEN=your_github_pat_token
```

#### In da-agent-hub Repository:
```bash
ANTHROPIC_API_KEY=your_claude_oauth_token
DBT_CLOUD_API_TOKEN=your_dbt_cloud_api_token
DBT_CLOUD_ACCOUNT_ID=your_account_id
```

### Complete Monitoring Workflow

Copy this to your dbt project as `.github/workflows/dbt-error-monitor.yml`:

```yaml
name: dbt Error Monitoring

on:
  schedule:
    - cron: '30 6 * * *'  # 6:30 AM UTC daily
  workflow_dispatch:

jobs:
  monitor-dbt-errors:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout dbt_errors_to_issues repository
      uses: actions/checkout@v4
      with:
        repository: graniterock/dbt_errors_to_issues
        ref: main
        path: dbt-error-monitor

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        cd dbt-error-monitor
        pip install -r requirements.txt

    - name: Run dbt error monitoring for your_project
      run: |
        cd dbt-error-monitor
        python run_for_project.py
      env:
        DBT_PROJECT_NAME: your_project_name
        DBT_CLOUD_API_TOKEN: ${{ secrets.DBT_CLOUD_API_TOKEN }}
        DBT_CLOUD_ACCOUNT_ID: ${{ secrets.DBT_CLOUD_ACCOUNT_ID }}
        GITHUB_API_TOKEN: ${{ secrets.GITHUB_API_TOKEN }}
        GITHUB_REPO: your_org/your_dbt_repo

    - name: Trigger Claude sleuthing for new issues
      uses: peter-evans/repository-dispatch@v3
      with:
        token: ${{ secrets.GITHUB_API_TOKEN }}
        repository: graniterock/da-agent-hub
        event-type: dbt-issue-sleuth
        client-payload: |
          {
            "repository": "your_org/your_dbt_repo",
            "project": "your_project_name",
            "trigger": "scheduled_monitoring",
            "run_id": "${{ github.run_id }}"
          }
```

### Cross-Repository Setup

For organizations with multiple dbt projects:

1. **Central Hub**: One da-agent-hub repository for all AI investigation
2. **Project-Specific Monitoring**: Each dbt repository gets its own monitoring workflow
3. **Shared Scripts**: Single dbt_errors_to_issues repository handles all projects
4. **Unified Intelligence**: Claude provides consistent analysis across projects

### Security & Authentication

- **dbt Cloud API**: Account-specific tokens with environment-level permissions
- **GitHub Actions**: Classic Personal Access Tokens for cross-repository access
- **Claude AI**: OAuth token authentication (requires Claude Pro/Max subscription)
- **Secrets Management**: All credentials stored as encrypted GitHub repository secrets
- **Least Privilege**: Each component has minimal required permissions

### Integration with CI/CD

Enhance your deployment pipeline:

```yaml
# Add to your CI/CD workflow
- name: Trigger Pre-Deployment Analysis
  if: contains(github.head_ref, 'claude/')
  uses: peter-evans/repository-dispatch@v3
  with:
    repository: graniterock/da-agent-hub
    event-type: pre-deployment-analysis
    client-payload: |
      {
        "pr_number": "${{ github.event.number }}",
        "branch": "${{ github.head_ref }}",
        "analysis_type": "pre_deployment"
      }
```

### Testing & Validation

#### Test the System

1. **Create a test dbt issue**:
   ```bash
   gh issue create --title "Test Claude Collaboration" \
     --body "Testing the AI investigation system"
   ```

2. **Trigger Claude investigation**:
   ```bash
   # Comment on the issue
   @claude investigate this test issue and demonstrate system capabilities
   ```

3. **Verify workflow execution**:
   ```bash
   gh run list --limit 5
   ```

#### Health Checks

Monitor system health:

```bash
# Check workflow status
gh run list --workflow="dbt Error Monitoring" --limit 3

# Verify Claude authentication
gh run list --workflow="Claude Collaborative Fixes" --limit 3

# Review recent issues
gh issue list --label="dbt-error" --limit 5
```