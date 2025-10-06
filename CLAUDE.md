don't look at the full .env file. Only search for the var names up to the equals sign.

# DA Agent Hub: Analytics Development Lifecycle (ADLC) AI Platform

## Quick Reference

**Security**: See `.claude/memory/patterns/git-workflow-patterns.md` for protected branch rules
**Testing**: See `.claude/memory/patterns/testing-patterns.md` for ADLC testing framework
**Cross-System Analysis**: See `.claude/memory/patterns/cross-system-analysis-patterns.md` for multi-tool coordination

## Three-Layer Architecture

```
💡 LAYER 1: PLAN → Ideation & strategic planning with AI organization
🔧 LAYER 2: DEVELOP + TEST + DEPLOY → Local development with specialist agents
🤖 LAYER 3: OPERATE + OBSERVE + DISCOVER + ANALYZE → Automated operations
```

## Simplified 4-Command Workflow

### Essential Commands
1. **`./scripts/capture.sh "[idea]"`** → Brainstorm and collect ideas (auto-organizes at 3+ ideas)
2. **`./scripts/roadmap.sh [timeframe]`** → Strategic planning and prioritization
3. **`./scripts/build.sh [idea-name]`** → Execute highest priority ideas (creates full project setup)
4. **`./scripts/finish.sh [project-name]`** → Complete and archive projects

### Support Command
5. **`./scripts/switch.sh [optional-branch]`** → Zero-loss context switching with automated backup

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

**Cloud Manager** (`cloud-manager-role`) - Owns cloud infrastructure (AWS + Azure)
- Cloud resource provisioning, scaling, and cost optimization
- Security configuration, IAM, networking, compliance
- Direct AWS MCP access (aws-api, aws-docs, aws-knowledge), consults aws-expert for edge cases
- Handles 80% of cloud infrastructure independently

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
Available for complex edge cases requiring deep tool expertise:
- `dbt-expert`, `snowflake-expert`, `tableau-expert`
- `dlthub-expert`, `orchestra-expert`, `prefect-expert`
- `streamlit-expert`, `react-expert`, `ui-ux-expert`
- `aws-expert`, `azure-expert` (cloud infrastructure specialists)
- `documentation-expert`, `github-sleuth-expert`

**When to use specialists**: Role agents consult them for 20% of complex scenarios requiring deep tool knowledge
**Note**: cloud-manager-role uses AWS MCP tools directly (aws-api, aws-docs, aws-knowledge) for 80% of AWS work, consults aws-expert for advanced patterns (SageMaker, EKS, Step Functions, multi-account)

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

## Knowledge Repository Structure

### Team Documentation Template
`knowledge/da_team_documentation/` - Template for organizing your team's D&A documentation

### DA Agent Hub Platform Documentation
`knowledge/da-agent-hub/` - Complete platform documentation organized by ADLC phases:
- **Planning Layer** (`planning/`): Idea management and strategic planning
- **Development Layer** (`development/`): Local development and agent coordination
- **Operations Layer** (`operations/`): Automated operations and cross-repo coordination

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

### Improvement PR Decision Framework
Create separate improvement PRs for:
- **HIGH IMPACT**: Agent updates benefiting multiple future projects
- **KNOWLEDGE GAPS**: Missing documentation causing repeated research
- **PROCESS OPTIMIZATION**: Workflow improvements with measurable efficiency gains
- **INTEGRATION ENHANCEMENT**: Cross-tool coordination improvements
- **ADLC METHODOLOGY**: Core system workflow refinements

**Examples**:
- "feat: Enhance dbt-expert with incremental model optimization patterns"
- "docs: Add Snowflake cost optimization playbook to knowledge base"
- "feat: Create tableau-performance-expert agent for dashboard optimization"

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
💡 CAPTURE: ./scripts/capture.sh → auto-organize → roadmap planning
    ↓ Strategic prioritization
🗺️ ROADMAP: ./scripts/roadmap.sh → impact/effort analysis → execution planning
    ↓ Priority selection
🔧 BUILD: ./scripts/build.sh → project setup → specialist agents → development
    ↓ Deploy to production
🎯 FINISH: ./scripts/finish.sh → archive → git workflow → next iteration
    ↓ Operations monitoring
🤖 OPERATIONS: GitHub Actions → Error detection → AI investigation → Cross-repo PRs
```

## Additional Resources

**Git Workflows**: `.claude/memory/patterns/git-workflow-patterns.md`
**Testing Patterns**: `.claude/memory/patterns/testing-patterns.md`
**Cross-System Analysis**: `.claude/memory/patterns/cross-system-analysis-patterns.md`
**Agent Definitions**: `.claude/agents/`
**Platform Documentation**: `knowledge/da-agent-hub/README.md`
**Personal Settings**: `knowledge/da_obsidian/Cody/Claude-Personal-Settings.md` (if available)
