# 🤖 DA Agent Hub: AI-Powered Data Infrastructure Management

**Automated dbt error monitoring and Claude AI-powered investigation system with interactive collaboration capabilities.**

[![dbt](https://img.shields.io/badge/dbt-Cloud-orange?logo=dbt)](https://cloud.getdbt.com/)
[![Claude](https://img.shields.io/badge/Claude-AI-blue?logo=anthropic)](https://claude.ai/)
[![GitHub](https://img.shields.io/badge/GitHub-Actions-black?logo=github)](https://github.com/features/actions)
[![Snowflake](https://img.shields.io/badge/Snowflake-Data-lightblue?logo=snowflake)](https://snowflake.com/)

---

## 🌟 Overview

The DA Agent Hub provides a **complete end-to-end solution** for proactive data infrastructure management. It automatically monitors your dbt Cloud projects for errors, creates GitHub issues with detailed context, and uses Claude AI to investigate and propose fixes—all while enabling interactive collaboration for complex problem-solving.

### 🏗️ System Architecture

```mermaid
graph TB
    subgraph "Data Infrastructure"
        DBT[dbt Cloud]
        SF[Snowflake]
        TB[Tableau]
    end

    subgraph "Monitoring & Alerting"
        GHA[GitHub Actions<br/>Daily Monitor]
        GI[GitHub Issues<br/>Auto-Created]
    end

    subgraph "AI Investigation System"
        CA[Claude AI<br/>Investigation]
        MA[Multi-Agent<br/>Analysis]
        IC[Interactive<br/>Collaboration]
    end

    subgraph "Human Collaboration"
        DEV[Data Engineers]
        PR[Pull Requests<br/>Auto-Generated]
        FIX[Implemented Fixes]
    end

    DBT -->|Errors| GHA
    GHA -->|Creates/Updates| GI
    GI -->|Triggers| CA
    CA -->|Uses| MA
    MA -->|Analysis| IC
    IC -->|Responds to| DEV
    DEV -->|@claude mentions| IC
    IC -->|Creates| PR
    PR -->|Implements| FIX
    FIX -->|Resolves| DBT
```

---

## 🎯 Key Features

### 🔍 **Automated Error Detection**
- **Daily Monitoring**: Checks dbt Cloud at 6:30 AM UTC for test failures and model errors
- **Smart Issue Management**: Creates/updates GitHub issues with comprehensive error details
- **Priority Classification**: Automatically categorizes issues by error type and severity
- **Cross-Repository Support**: Works across multiple dbt projects (roy_kent, dbt_cloud)

### 🤖 **AI-Powered Investigation**
- **Automatic Analysis**: Claude investigates every new issue with specialized domain expertise
- **Multi-Agent System**: Uses expert agents for different aspects:
  - **dbt-expert**: Model compilation, test failures, SQL optimization
  - **snowflake-expert**: Warehouse performance, query optimization
  - **tableau-expert**: Dashboard and report model issues
  - **business-context**: Requirements validation and stakeholder alignment
  - **da-architect**: Cross-system analysis and strategic decisions

### 💬 **Interactive Collaboration**
- **@claude Mentions**: Comment on any issue to get AI assistance
- **Automatic PR Creation**: Request fixes with `@claude create PR`
- **Assignment-Based Fixing**: Assign issues to `claude[bot]` for auto-fix attempts
- **Label-Based Triggers**: Use labels like `claude:fix` and `claude:investigate`
- **Multi-Turn Conversations**: Collaborative problem-solving with context retention

---

## 🚀 Quick Start

### Prerequisites

- **GitHub Repository**: Access to your dbt projects on GitHub
- **dbt Cloud**: Active dbt Cloud account with API access
- **Claude Pro/Max**: Subscription for OAuth token authentication
- **GitHub Actions**: Enabled in your repositories

### 1. Setup Repositories

The system works across **three repositories**:

1. **Your dbt Project** (e.g., `roy_kent`, `dbt_cloud`)
   - Contains dbt models, tests, and configurations
   - Gets the monitoring workflow

2. **graniterock/dbt_errors_to_issues**
   - Shared Python scripts for error processing
   - Handles dbt Cloud API integration

3. **graniterock/da-agent-hub** (this repo)
   - Claude AI investigation system
   - Interactive collaboration workflows

### 2. Configure Secrets

Set up these GitHub repository secrets:

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

### 3. Deploy Monitoring Workflow

Copy the monitoring workflow to your dbt project:

```yaml
# .github/workflows/dbt-error-monitor.yml
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

---

## 🎮 Usage Guide

### 💬 Interactive Commands

#### **@claude Mentions**
Comment on any GitHub issue to get Claude's help:

```bash
# Request a fix
@claude create PR to resolve this unique constraint issue

# Deep investigation
@claude investigate the upstream data quality for this model

# General discussion
@claude what do you think is causing these test failures?

# Collaborative debugging
@claude I think this might be related to the ERP data load timing, can you check?
```

#### **Assignment-Based Auto-Fix**
Assign any issue to `claude[bot]` and Claude will:
1. Analyze the problem thoroughly
2. Determine if it's suitable for auto-fixing
3. Create a PR with the solution (for simple fixes)
4. Or explain why manual intervention is needed (for complex issues)

#### **Label-Based Triggers**
Add labels to issues for specific actions:

- 🏷️ **`claude:fix`**: Create a pull request with a fix
- 🏷️ **`claude:investigate`**: Perform deeper analysis
- 🏷️ **`claude:collaborate`**: Start interactive discussion mode

### 📊 Daily Workflow

```mermaid
graph LR
    A[6:30 AM UTC<br/>Monitor Runs] --> B[Issues Created/<br/>Updated]
    B --> C[Claude Auto-<br/>Investigates]
    C --> D[Team Reviews<br/>AI Findings]
    D --> E[Request PR or<br/>Collaborate]
    E --> F[Claude Creates<br/>Fix PR]
    F --> G[Team Reviews<br/>& Merges]
```

### 🔧 Example Interactions

#### **Scenario 1: Simple Fix Request**
```
You: @claude create PR to fix the unique constraint violation

Claude: I'll analyze the bt4_rpt_stock_receipt_reconciliation model
and create a PR. Let me check the duplicate records and implement
a deduplication solution.

→ Creates PR: "fix: deduplicate primary keys in stock receipt model"
  - Adds DISTINCT clause to staging model
  - Updates test configuration
  - Includes documentation updates
```

#### **Scenario 2: Collaborative Investigation**
```
You: @claude I think this might be related to the upstream ERP data
timing. Can you investigate that angle?

Claude: Great insight! Let me investigate the upstream data patterns
using the dlthub-expert agent to check source ingestion timing...

→ Updates issue with:
  - ERP data load schedule analysis
  - Timing conflict identification
  - Recommended schedule adjustments
  - Pipeline health assessment
```

#### **Scenario 3: Auto-Fix Assignment**
```
Action: You assign issue to claude[bot]

Claude: I've been assigned to fix this issue. Analyzing...
- Found duplicate primary keys in stock receipt data
- Root cause: Missing deduplication in staging model
- This is a simple fix appropriate for auto-implementation
- Creating PR with solution...

→ Automatically creates and links PR with fix
```

---

## 🏛️ System Architecture

### 🔄 Data Flow

1. **Detection Phase**: dbt Cloud runs daily tests and transformations
2. **Monitoring Phase**: GitHub Actions monitors dbt Cloud API for failures
3. **Issue Management**: Creates/updates GitHub issues with detailed error context
4. **AI Trigger**: Automatically dispatches investigation request to Claude
5. **Investigation Phase**: Claude analyzes using specialized expert agents
6. **Collaboration Phase**: Users interact via comments, assignments, or labels
7. **Resolution Phase**: Claude creates PRs with fixes or provides guidance

### 🧠 Multi-Agent Intelligence

The system leverages **specialized AI agents** for domain expertise:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   dbt-expert    │    │ snowflake-expert │    │ tableau-expert  │
│                 │    │                  │    │                 │
│ • SQL Logic     │    │ • Query Perf     │    │ • Dashboard     │
│ • Model Tests   │    │ • Cost Analysis  │    │   Performance   │
│ • Dependencies  │    │ • Schema Issues  │    │ • Report Models │
└─────────────────┘    └──────────────────┘    └─────────────────┘

┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│business-context │    │   da-architect   │    │ dlthub-expert   │
│                 │    │                  │    │                 │
│ • Requirements  │    │ • System Design  │    │ • Data Ingestion│
│ • Stakeholder   │    │ • Cross-Platform │    │ • Source Quality│
│   Alignment     │    │   Decisions      │    │ • Connectors    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### 🔐 Security & Authentication

- **dbt Cloud API**: Account-specific tokens with environment-level permissions
- **GitHub Actions**: Classic Personal Access Tokens for cross-repository access
- **Claude AI**: OAuth token authentication (requires Claude Pro/Max subscription)
- **Secrets Management**: All credentials stored as encrypted GitHub repository secrets
- **Least Privilege**: Each component has minimal required permissions

---

## 💰 Cost Analysis

### **Annual Operating Costs: $0-100**

| Component | Cost | Notes |
|-----------|------|-------|
| **GitHub Actions** | $0 | Free tier covers typical usage (2,000 minutes/month) |
| **Claude API** | $0 | OAuth token uses existing Claude Pro/Max subscription |
| **dbt Cloud API** | $0 | Read-only access, no additional charges |
| **Repository Storage** | $0 | Normal GitHub repository limits |
| **Total Annual** | **$0-100** | May incur small costs for heavy usage |

### **ROI Benefits**
- **Reduced MTTR**: Issues resolved 50-80% faster with AI guidance
- **Proactive Detection**: Catch problems hours vs. days after occurrence
- **Team Efficiency**: Data engineers focus on implementation vs. diagnosis
- **Knowledge Preservation**: Investigation findings become searchable institutional knowledge

---

## 🛠️ Advanced Configuration

### Cross-Repository Setup

For organizations with multiple dbt projects:

1. **Central Hub**: One da-agent-hub repository for all AI investigation
2. **Project-Specific Monitoring**: Each dbt repository gets its own monitoring workflow
3. **Shared Scripts**: Single dbt_errors_to_issues repository handles all projects
4. **Unified Intelligence**: Claude provides consistent analysis across projects

### Custom Agent Development

Extend the system with custom agents:

```markdown
# .claude/agents/custom-expert.md

You are a specialized expert for [your domain].

## Capabilities
- Domain-specific analysis
- Custom tool integration
- Specialized knowledge base

## When to Use
- Issue involves [specific conditions]
- Complex [domain] problems
- Cross-system [domain] analysis

## Analysis Framework
1. [Domain-specific step 1]
2. [Domain-specific step 2]
3. [Domain-specific step 3]
```

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

---

## 🧪 Testing & Validation

### Test the System

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

### Health Checks

Monitor system health:

```bash
# Check workflow status
gh run list --workflow="dbt Error Monitoring" --limit 3

# Verify Claude authentication
gh run list --workflow="Claude Collaborative Fixes" --limit 3

# Review recent issues
gh issue list --label="dbt-error" --limit 5
```

---

## 🚨 Troubleshooting

### Common Issues

| Problem | Symptoms | Solution |
|---------|----------|----------|
| **Workflow not triggering** | No new runs after @claude mention | Check workflow is on main branch |
| **Authentication failed** | "Invalid API key" error | Verify OAuth token in secrets |
| **No issues created** | dbt errors but no GitHub issues | Check dbt Cloud API permissions |
| **Claude not responding** | Workflow runs but no comments | Verify ANTHROPIC_API_KEY secret |

### Debug Steps

1. **Check workflow files**:
   ```bash
   ls -la .github/workflows/
   ```

2. **Verify secrets**:
   ```bash
   gh secret list
   ```

3. **Review workflow logs**:
   ```bash
   gh run view --log-failed
   ```

4. **Test API connectivity**:
   ```bash
   curl -H "Authorization: Bearer $DBT_TOKEN" \
     "https://cloud.getdbt.com/api/v2/accounts/$ACCOUNT_ID/"
   ```

---

## 🎯 Best Practices

### For Data Teams

1. **Proactive Monitoring**: Review daily AI investigations to catch patterns
2. **Collaborative Debugging**: Use @claude mentions for complex issues
3. **Knowledge Building**: Let Claude document solutions for future reference
4. **Gradual Automation**: Start with investigation, progress to auto-fixing

### For Claude Interactions

1. **Be Specific**: "Investigate unique constraint violations in dim_customer"
2. **Provide Context**: "This started after yesterday's ERP data load"
3. **Ask Follow-ups**: "What about impact on downstream dashboards?"
4. **Request Actions**: "Create a PR to fix this" vs. "What should we do?"

### for System Administration

1. **Regular Health Checks**: Monitor workflow success rates
2. **Token Rotation**: Update API tokens before expiration
3. **Capacity Planning**: Monitor GitHub Actions usage
4. **Security Auditing**: Review access logs periodically

---

## 🔮 Future Enhancements

### Planned Features
- **Slack Integration**: Real-time notifications and interactions
- **Tableau Dashboard**: System health and metrics visualization
- **Advanced Analytics**: Pattern recognition across historical issues
- **Auto-Deployment**: Safe automatic deployment of simple fixes
- **Multi-Cloud Support**: AWS, GCP, Azure data platforms

### Contributing

We welcome contributions! Areas for enhancement:

- Custom agent development
- Additional data platform integrations
- Enhanced error pattern recognition
- Improved auto-fix capabilities
- Documentation and examples

---

## 📚 Documentation

### Quick References
- **[Claude Interaction Guide](docs/claude-interactions.md)**: Complete command reference
- **[Agent Development](docs/agent-development.md)**: Creating custom experts
- **[Workflow Configuration](docs/workflow-config.md)**: Setup and customization
- **[Troubleshooting Guide](docs/troubleshooting.md)**: Common issues and solutions

### External Resources
- [dbt Cloud API Documentation](https://docs.getdbt.com/dbt-cloud/api-v2)
- [Claude Code Documentation](https://docs.anthropic.com/claude/docs)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

## 📞 Support & Community

- **Issues**: [GitHub Issues](https://github.com/graniterock/da-agent-hub/issues)
- **Documentation**: [Wiki](https://github.com/graniterock/da-agent-hub/wiki)
- **Discussions**: [GitHub Discussions](https://github.com/graniterock/da-agent-hub/discussions)

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

**Built with ❤️ for data teams who want AI-powered infrastructure management**

*Transform your reactive error handling into proactive, intelligent data operations.*