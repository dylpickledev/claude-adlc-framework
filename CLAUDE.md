don't look at the full .env file. Only search for the var names up to the equals sign.

# DA Agent Hub: Analytics Development Lifecycle (ADLC) AI Platform

## Quick Reference

**Security**: See `.claude/memory/patterns/git-workflow-patterns.md` for protected branch rules
**Testing**: See `.claude/memory/patterns/testing-patterns.md` for ADLC testing framework
**Cross-System Analysis**: See `.claude/memory/patterns/cross-system-analysis-patterns.md` for multi-tool coordination

### Mandatory Workflow (CRITICAL - Never Violate)
1. **ALWAYS create feature branch** before making any code changes
2. **ALWAYS create Pull Request** for code review and approval
3. **NEVER push directly** to protected branches
4. **NEVER merge without approval** (except for da-agent-hub documentation updates)

## Three-Layer Architecture

```
💡 LAYER 1: PLAN → Ideation & strategic planning with AI organization
🔧 LAYER 2: DEVELOP + TEST + DEPLOY → Local development with specialist agents
🤖 LAYER 3: OPERATE + OBSERVE + DISCOVER + ANALYZE → Automated operations
```

## Simplified Workflow Commands

### Essential Commands (Use Slash Commands)
1. **`/idea "[idea]"`** → Quick idea capture (creates GitHub issues with auto-labeling)
2. **`/research [text|issue#]`** → Deep exploration and analysis (pre-capture or issue analysis)
3. **`/roadmap [timeframe]`** → Strategic planning and prioritization (analyzes GitHub issues)
4. **`/start [issue#|"text"]`** → Begin development (from issue OR creates issue from text + starts)
5. **`/complete [project]`** → Complete and archive projects (closes GitHub issue + cleans up worktree)

### Support Commands
6. **`/switch [optional-branch]`** → Zero-loss context switching with automated backup
7. **`/pause [description]`** → Save conversation context for seamless resumption
8. **`/setup-worktrees`** → One-time VS Code worktree integration setup

### Deprecated (Still Work, But Use New Names)
- **`/capture`** → Use `/idea` instead
- **`/build`** → Use `/start` instead

### Underlying Scripts (Called by Slash Commands)
- `/idea` → `./scripts/idea.sh`
- `/research` → `./scripts/research.sh`
- `/roadmap` → `./scripts/roadmap.sh`
- `/start` → `./scripts/start.sh`
- `/complete` → `./scripts/finish.sh`
- `/switch` → `./scripts/switch.sh`
- `/pause` → (Claude-native, no script)
- `/setup-worktrees` → `./scripts/setup-worktrees.sh`

**Note**: Prefer slash commands for better Claude integration. Scripts can be run directly if needed.

### GitHub Issues Integration
All ideas are managed as GitHub issues with 'idea' label:
- **View all ideas**: `gh issue list --label idea --state open`
- **Filter by category**: `gh issue list --label idea --label bi-analytics`
- **Search ideas**: `gh issue list --label idea --search "dashboard"`
- **Track progress**: Issues automatically labeled 'in-progress' when built

## Project File Structure

```
projects/active/<project-name>/
├── README.md           # Navigation hub with quick links and progress
├── spec.md            # Project specification (stable requirements)
├── context.md         # Working context (dynamic state tracking)
└── tasks/             # Agent coordination directory
    ├── current-task.md     # Current agent assignments
    └── <tool>-findings.md  # Detailed agent findings
```

**File Purposes**:
- **README.md**: Entry point for navigation, progress summary, key decisions
- **spec.md**: Stable project requirements, end goals, implementation plan, success criteria
- **context.md**: Dynamic state tracking - branches, PRs, blockers, current focus
- **tasks/**: Agent coordination - task assignments and detailed findings

## Role-Based Agent System

### Agent Creation Guidelines

**ALWAYS use templates when creating new agents**:
- **New role agent**: Copy `.claude/agents/roles/role-template.md`
- **New specialist agent**: Copy `.claude/agents/specialists/specialist-template.md`

Templates encode correct architecture patterns:
- Roles delegate to specialists (80% independent, 20% consultation)
- Specialists use MCP tools + expertise (correctness-first)
- Both include quality standards, validation protocols, /complete integration

### Primary Agents (Use These First)
**Analytics Engineer** (`analytics-engineer-role`) - Owns transformation layer (dbt + Snowflake + BI data)
- SQL transformations, data modeling, performance optimization
- Business logic implementation, metrics, semantic layer
- Handles 80% of transformation work independently

**Data Engineer** (`data-engineer-role`) - Owns ingestion layer (Orchestra + dlthub + Prefect + Airbyte)
- Pipeline setup and orchestration (batch AND streaming)
- Source system integration, data quality at ingestion
- Chooses right tool (dlthub vs Prefect) based on requirements

**BI Developer** (`bi-developer-role`) - Owns BI consumption layer (Tableau + Power BI)
- Enterprise BI dashboards, reports, executive views
- BI tool performance optimization, self-service analytics
- Business user training and documentation

**UI/UX Developer** (`ui-ux-developer-role`) - Owns web application layer (Streamlit + React)
- Data applications, admin tools, custom web interfaces
- User experience design, responsive applications
- Interactive prototypes and proof-of-concepts

**Data Architect** (`data-architect-role`) - Strategic platform decisions and system design
- Architecture patterns, technology selection, cross-system integration
- Platform roadmap, governance, standards

**Business Analyst** (`business-analyst-role`) - Requirements and stakeholder alignment
- Business logic validation, metric definitions
- Stakeholder communication, project scoping

**QA Engineer** (`qa-engineer-role`) - Testing and quality assurance
- Comprehensive testing strategies, validation frameworks
- Data quality validation, system integration testing

**Project Manager** (`project-manager-role`) - Delivery coordination and stakeholder management
- Project planning, UAT frameworks, milestone tracking
- Cross-functional coordination, risk management

### Tool Specialists (Consultation Layer - Use When Needed)
Role agents delegate to specialists who combine deep domain expertise with MCP tool access for informed, validated recommendations.

**Cloud & Infrastructure**:
- `aws-expert`: THE specialist for AWS infrastructure (uses aws-api, aws-docs, aws-knowledge MCP)
- `azure-expert`: Azure infrastructure specialist (future - uses azure-mcp when available)

**Data Platform**:
- `dbt-expert`: SQL transformations, dbt patterns (uses dbt-mcp, snowflake-mcp, git-mcp)
- `snowflake-expert`: Warehouse optimization, cost analysis (uses snowflake-mcp, dbt-mcp)
- `orchestra-expert`: Workflow orchestration (uses orchestra-mcp custom, prefect-mcp, airbyte-mcp)
- `prefect-expert`: Python workflows (uses prefect-mcp custom, orchestra-mcp)
- `dlthub-expert`: Data ingestion (uses airbyte-mcp, snowflake-mcp, orchestra-mcp)

**BI & Visualization**:
- `tableau-expert`: BI optimization (uses tableau-mcp, snowflake-mcp, dbt-mcp)

**Development**:
- `react-expert`: React patterns (uses github-mcp, git-mcp)
- `streamlit-expert`: Streamlit apps (uses github-mcp, filesystem-mcp)
- `ui-ux-expert`: UX design (uses notion-mcp, filesystem-mcp)

**Cross-Functional**:
- `documentation-expert`: Standards and docs (uses confluence-mcp, github-mcp, dbt-mcp)
- `github-sleuth-expert`: Repository analysis (uses github-mcp, git-mcp, filesystem-mcp)
- `business-context`: Requirements (uses atlassian-mcp, slack-mcp, dbt-mcp)
- `qa-coordinator`: Quality assurance (uses dbt-mcp, snowflake-mcp, github-mcp)

**Pattern**: Role agents delegate when confidence <0.60 OR domain expertise needed
**Specialists**: Use MCP tools + expertise to provide validated, correct recommendations
**Correctness > Speed**: 15x token cost justified by significantly better outcomes (per Anthropic research)

### MCP Tool Execution Pattern

**Specialist agents provide MCP tool recommendations, main Claude executes them**:

1. **Specialist creates recommendation**:
   ```markdown
   ### RECOMMENDED MCP TOOL EXECUTION
   **Tool**: snowflake_query_manager
   **Query**: SELECT * FROM TASK_HISTORY WHERE STATE = 'FAILED'
   **Expected Result**: List of failed tasks
   **Fallback**: Direct Python execution if MCP unavailable
   ```

2. **Main Claude executes**:
   - Reads specialist recommendation
   - Executes MCP tool call or fallback approach
   - Returns results to specialist (if needed for analysis)
   - Implements specialist recommendations

3. **Why this pattern**:
   - Specialists focus on expertise (what to do, which tools to use)
   - Main Claude handles execution (MCP calls, Python scripts, Bash commands)
   - Specialists can't execute directly (research-only by design)
   - Clear separation of concerns: planning vs execution

*See `.claude/memory/patterns/cross-system-analysis-patterns.md` for detailed agent coordination*

## Context Management & Memory System

### Session Start Protocol
1. **Recent Patterns** (`.claude/memory/recent/`) → Review last 30 days for similar solutions
2. **Domain Patterns** (`.claude/memory/patterns/`) → Load relevant architectural patterns
3. **Task Context** (`.claude/tasks/`) → Check for unfinished work
4. **Project Templates** (`.claude/memory/templates/`) → Use appropriate template

### Pattern Documentation Protocol
Use these markers in `.claude/tasks/*/findings.md` for automatic extraction:

```markdown
PATTERN: [Description of reusable pattern]
SOLUTION: [Specific solution that worked]
ERROR-FIX: [Error message] -> [Fix that resolved it]
ARCHITECTURE: [System design pattern]
INTEGRATION: [Cross-system coordination approach]
```

## Critical Rules

### Security & Git Workflow
**CRITICAL**: NEVER commit directly to protected branches (main, master, production, prod)
- Always create feature branch first
- All code changes require PR workflow
- Exception: da-agent-hub documentation-only changes

*See `.claude/memory/patterns/git-workflow-patterns.md` for complete git workflow patterns*

### Sandbox Principle
**CRITICAL**: `projects/active/<project-name>/` functions as an **isolated sandbox**

**All work stays in project folder until explicit deployment**:
- Analysis, code, documentation, testing → `projects/active/<project>/`
- Never write to production repos during active development
- Read-only access to production for comparison only

**Deploy only when user explicitly requests**:
- "Deploy this to [repo]"
- "Push to production"
- "Create PR in [repo]"
- Project finalized with `/finish` command

### Development Best Practices
- **Always start from up-to-date main branch**: Run `git checkout main && git pull origin main` before starting any work
- **DO NOT MOVE FORWARD until you've fixed a problem**: If blocked on step 1, stop and fix completely before step 2
- **Git branches**: Prefix with `feature/` or `fix/`
- **Use subagents**: Optimize context window with task delegation
- **Preserve context links**: Maintain connections between ideas → projects → operations

## Task vs Project Classification

### Use Project Structure When:
- Multi-day efforts spanning multiple work sessions
- Cross-repository coordination (dbt + snowflake + tableau)
- Research and analysis informing multiple decisions
- Collaborative work with team members/reviewers
- Knowledge preservation needed for future reference
- Complex troubleshooting requiring systematic investigation

### Use Simple Task Execution When:
- Quick fixes (typos, small config changes, single-file updates)
- Immediate responses to questions or information requests
- One-off scripts or utilities
- Documentation updates without research
- Status checks or system diagnostics
- Simple file operations or code formatting

## Context Clarity & File Reference System

### Visual File Reference Indicators
- **📁 PROJECT**: Working files in `projects/active/<project-name>/`
- **📦 REPO**: Source repository files (original/production versions)
- **🎯 DEPLOY**: Deployment target locations

### Context Declaration Protocol
Before analysis, declare context assumptions:

```
📍 Context Check:
- Working File: 📁 PROJECT projects/active/feature-x/app.py
- Reference: 📦 REPO ../original-repo/app.py
- Deploy Target: 🎯 DEPLOY production-repo/

If you want different sources, please redirect me.
```

## Smart Repository Context Resolution

### Automatic Owner/Repo Detection
When working with GitHub repositories, use smart context resolution to avoid specifying owner repeatedly:

```bash
# Resolve repository context from config/repositories.json
python3 scripts/resolve-repo-context.py dbt_cloud
# Output: graniterock dbt_cloud

# Use resolved context in GitHub MCP operations
mcp__github__list_issues owner="graniterock" repo="dbt_cloud"
```

### Available Commands
- `python3 scripts/resolve-repo-context.py <repo_name>` - Get owner and repo
- `python3 scripts/resolve-repo-context.py --json <repo_name>` - Get full context as JSON
- `python3 scripts/resolve-repo-context.py --list` - List all resolvable repositories
- `./scripts/get-repo-owner.sh <repo_name>` - Get just the owner (bash helper)

### Agent Integration
All specialist agents working with GitHub should:
1. Resolve repository context before GitHub MCP calls
2. Use explicit owner/repo parameters in all GitHub MCP operations
3. Reference pattern documentation: `.claude/memory/patterns/github-repo-context-resolution.md`

**Benefit**: Eliminates cognitive overhead of remembering "graniterock" for every GitHub operation while maintaining explicit, correct MCP calls.

## Knowledge Repository Structure

### Team Documentation
`knowledge/da_team_documentation/` - Data & Analytics team structured documentation (data architecture, integrations, products, templates)

### Team Knowledge Vault
`knowledge/da_obsidian/` - Data & Analytics team Obsidian vault for raw notes and unrefined ideas before ADLC planning

### DA Agent Hub Platform Documentation
`knowledge/da-agent-hub/` - Complete platform documentation organized by ADLC phases:
- **Planning Layer** (`planning/`): Idea management and strategic planning
- **Development Layer** (`development/`): Local development and agent coordination
- **Operations Layer** (`operations/`): Automated operations and cross-repo coordination

### Production Applications Documentation
`knowledge/applications/` - Comprehensive documentation for deployed applications

**Three-Tier Documentation Architecture**:

**Tier 1: Repository README** (Lightweight, Developer-Focused)
- **Location**: `<repo>/README.md` (e.g., `react-sales-journal/README.md`)
- **Purpose**: Get developers productive fast
- **Contains**: App purpose, local dev setup, npm commands, link to knowledge base
- **Audience**: Human developers, AI doing code-level work
- **Size**: < 200 lines

**Tier 2: Knowledge Base** (Comprehensive, Cross-System)
- **Location**: `knowledge/applications/<app-name>/`
- **Purpose**: Complete reference for deployment, operations, architecture
- **Structure**:
  - `architecture/` - System design, data flows, infrastructure
  - `deployment/` - Deployment runbooks, Docker builds, AWS config
  - `operations/` - Monitoring, troubleshooting, incident response
- **Audience**: AI agents coordinating deployments/operations
- **Size**: Unlimited - source of truth

**Tier 3: Agent Pattern Index** (Pointers + Confidence)
- **Location**: `.claude/agents/specialists/<agent>.md` (e.g., `aws-expert.md`)
- **Purpose**: Help agents find proven patterns quickly
- **Contains**: Pattern name, confidence score, link to Tier 2, when to use
- **Audience**: AI agents deciding what pattern to apply
- **Size**: Index only, not full content

**Key Principles**:
- **Single Source of Truth**: Each piece of info lives in ONE canonical location
- **Cross-Reference, Don't Duplicate**: Use links instead of copying content
- **Task-Aware Discovery**: Agents read what they need, when they need it
- **Layer-Appropriate Detail**: Match detail level to audience needs

**Example Flow**:
```
Agent Task: "Deploy Sales Journal update"
1. Check ui-ux-developer-role.md → Known Applications → Find knowledge/applications/sales-journal/
2. Read knowledge/applications/sales-journal/deployment/production-deploy.md → Complete runbook
3. Delegate AWS work → aws-expert reads same knowledge base docs + applies patterns
```

## Repository Branch Structures

**dbt_cloud**: master (prod), dbt_dw (staging) - Branch from dbt_dw
**dbt_errors_to_issues**: main (prod) - Branch directly from main
**roy_kent**: master (prod) - Branch directly from master
**sherlock**: main (prod) - Branch directly from main

*See `.claude/memory/patterns/git-workflow-patterns.md` for detailed workflows*

## ADLC Continuous Improvement Strategy

### During Project Completion
Actively identify and capture:
- **Agent Capability Enhancements**: New tool patterns, integration strategies, troubleshooting insights
- **Agent File Updates**: Novel patterns for specialist agents (`.claude/agents/`)
- **Knowledge Base Enhancement**: System architecture patterns, process improvements (`knowledge/`)

### Knowledge Extraction Locations

When completing projects, extract learnings to appropriate locations based on content type:

**Production Application Knowledge** → `knowledge/applications/<app-name>/`
- **When**: Deploying new apps or major app updates
- **Structure**: Three-tier pattern (Tier 2 - comprehensive docs)
  - `architecture/` - System design, data flows, infrastructure details
  - `deployment/` - Complete deployment runbooks, Docker builds, AWS configuration
  - `operations/` - Monitoring, troubleshooting guides, incident response
- **Examples**: ALB OIDC authentication, ECS deployment patterns, multi-service Docker
- **Updates Required**:
  1. Create/update knowledge base docs for the application
  2. Update agent pattern index (e.g., aws-expert.md with confidence scores)
  3. Add to "Known Applications" in relevant role agents (e.g., ui-ux-developer-role.md)
  4. Create lightweight README in actual repo (Tier 1) linking to knowledge base

**Platform/Tool Patterns** → `knowledge/da-agent-hub/`
- **When**: Discovering reusable patterns for ADLC workflow
- **Structure**: Organized by ADLC phase (planning/, development/, operations/)
- **Examples**: Testing frameworks, git workflows, cross-system analysis patterns

**Agent Expertise** → `.claude/agents/specialists/<agent>.md`
- **When**: Validating patterns in production, improving confidence scores
- **Updates**: Add production-validated patterns section, update confidence levels
- **Reference**: Link to knowledge base (Tier 2) for full implementation

**Role Agent Applications** → `.claude/agents/roles/<role>.md`
- **When**: New applications deployed that role will work on
- **Updates**: Add to "Known Applications" section with stack, patterns, key learnings
- **Purpose**: Help agents quickly find context when tasked with app work

### Improvement PR Decision Framework
Create separate improvement PRs for:
- **HIGH IMPACT**: Agent updates benefiting multiple future projects
- **KNOWLEDGE GAPS**: Missing documentation causing repeated research
- **PROCESS OPTIMIZATION**: Workflow improvements with measurable efficiency gains
- **INTEGRATION ENHANCEMENT**: Cross-tool coordination improvements
- **ADLC METHODOLOGY**: Core system workflow refinements

**Examples**:
- "feat: Enhance aws-expert with ALB OIDC production patterns from sales-journal deployment"
- "docs: Add React + FastAPI application architecture to knowledge/applications/"
- "feat: Document three-tier documentation pattern for future app deployments"

## Agent Training & Learning System

### Chat Analysis Features
- User-agnostic discovery of Claude conversations
- Privacy-preserving local analysis
- Effectiveness metrics and improvement recommendations
- Integration with `/complete` command for automatic learning extraction

**Usage**: `./scripts/analyze-claude-chats.sh`

**Results**: `knowledge/da-agent-hub/training/analysis-results/` (local only)

### Continuous Learning Loop
```
🔧 PROJECT WORK → 💬 CONVERSATIONS → 📊 ANALYSIS
    ↑                                      ↓
🚀 ENHANCED AGENTS ← 📝 IMPROVEMENT PRs ← 💡 RECOMMENDATIONS
```

## Complete Development Workflow

```
💡 IDEA: /idea → GitHub issue creation → auto-labeling → roadmap planning
    ↓ Strategic prioritization (optional deep analysis)
🔬 RESEARCH: /research [text|issue#] → Deep exploration → Feasibility → Technical approach
    ↓ Informed decision-making
🗺️ ROADMAP: /roadmap → impact/effort analysis → GitHub issue analysis → execution planning
    ↓ Priority selection
🚀 START: /start [issue#|"text"] → project setup → worktree creation → specialist agents → development
    ↓ Deploy to production
✅ COMPLETE: /complete → archive → worktree cleanup → close GitHub issue → next iteration
    ↓ Operations monitoring
🤖 OPERATIONS: GitHub Actions → Error detection → AI investigation → Cross-repo PRs
```

## Additional Resources

**Git Workflows**: `.claude/memory/patterns/git-workflow-patterns.md`
**Testing Patterns**: `.claude/memory/patterns/testing-patterns.md`
**Cross-System Analysis**: `.claude/memory/patterns/cross-system-analysis-patterns.md`
**VS Code Worktrees**: `knowledge/da-agent-hub/development/vscode-worktree-integration.md`
**Agent Definitions**: `.claude/agents/`
**Platform Documentation**: `knowledge/da-agent-hub/README.md`
