don't look at the full .env file. Only search for the var names up to the equals sign.

# Security & Branch Protection Rules

## Protected Branches - NEVER Commit Directly
**CRITICAL SECURITY RULE**: Claude must NEVER commit code directly to protected branches.

### Protected Branch List
- `main`
- `master`
- `production`
- `prod`
- Any branch matching pattern: `release/*`, `hotfix/*`

### Mandatory Workflow
1. **ALWAYS create feature branch** before making any code changes
2. **ALWAYS create Pull Request** for code review and approval
3. **NEVER push directly** to protected branches
4. **NEVER merge without approval** (except for da-agent-hub documentation updates)

### Pre-Commit Safety Check
Before executing ANY git commit command, Claude MUST:

```bash
# Check current branch
CURRENT_BRANCH=$(git branch --show-current)

# Protected branches list
PROTECTED_BRANCHES=("main" "master" "production" "prod")

# Check if on protected branch
for branch in "${PROTECTED_BRANCHES[@]}"; do
    if [ "$CURRENT_BRANCH" = "$branch" ]; then
        echo "❌ ERROR: Cannot commit directly to protected branch '$CURRENT_BRANCH'"
        echo "Please create a feature branch first:"
        echo "  git checkout -b feature/your-feature-name"
        exit 1
    fi
done
```

### Enforcement Protocol
**If user asks to commit to protected branch:**
1. **Stop immediately** - Do not execute the commit
2. **Explain the security policy** - Protected branches require PR workflow
3. **Offer to create feature branch** - Suggest branch name based on work
4. **Create PR after commit** - Ensure changes go through approval process

**Example Response:**
```
❌ I cannot commit directly to the 'main' branch due to security policies.

All code changes must go through the Pull Request approval workflow.

I can:
1. Create a feature branch: feature/[description]
2. Commit your changes to that branch
3. Create a PR for review and approval

Would you like me to proceed with this workflow?
```

### Exceptions
**ONLY exception**: Documentation-only changes in da-agent-hub repository
- Changes to `*.md` files in da-agent-hub can be committed to main
- All code changes still require feature branch + PR workflow
- Claude should confirm: "These are documentation-only changes, proceeding with direct commit to main"

### Feature Branch Naming
When creating feature branches, use these conventions:
- `feature/[description]` - New features
- `fix/[description]` - Bug fixes
- `docs/[description]` - Documentation updates (code repos only)
- `refactor/[description]` - Code refactoring
- `test/[description]` - Testing improvements

# DA Agent Hub: Analytics Development Lifecycle (ADLC) AI Platform

## Overview

The DA Agent Hub implements the complete [dbt Analytics Development Lifecycle](https://www.getdbt.com/resources/the-analytics-development-lifecycle) with three integrated AI-powered layers that map to ADLC phases:

### 🔄 ADLC Alignment
```
💡 LAYER 1: PLAN → Ideation & strategic planning with AI organization
🔧 LAYER 2: DEVELOP + TEST + DEPLOY → Local development with specialist agents
🤖 LAYER 3: OPERATE + OBSERVE + DISCOVER + ANALYZE → Automated operations
```

### Three-Layer Architecture
1. **💡 Planning Layer** - ADLC Plan: Transform brainstorming into structured roadmaps
2. **🔧 Development Layer** - ADLC Develop/Test/Deploy: Execute with specialist AI coordination
3. **🤖 Operations Layer** - ADLC Operate/Observe/Discover/Analyze: Monitor and optimize

## Layer 1: ADLC Planning Phase - Idea Management System ("Spaghetti Organizer")

### ADLC Plan Alignment
This layer implements the **Plan** phase of the Analytics Development Lifecycle:
- **Business case validation**: `./scripts/capture.sh` captures problems and opportunities
- **Implementation planning**: Auto-organization with intelligent clustering
- **Stakeholder feedback**: `./scripts/roadmap.sh` facilitates strategic planning
- **Impact analysis**: AI clustering identifies downstream effects
- **Long-term maintenance**: Roadmaps consider sustainability

### Simplified Workflow
The complete analytics development lifecycle is now handled by **4 simple commands**:

#### 1. **`./scripts/capture.sh "[idea]"`** or **`/capture "[idea]"`** - Idea Capture
- Rapid idea collection (< 30 seconds)
- Auto-organizes when inbox reaches 3+ ideas
- ADLC Plan: Business case validation and idea collection

#### 2. **`./scripts/roadmap.sh [timeframe]`** or **`/roadmap [timeframe]`** - Strategic Planning
- Creates prioritization frameworks
- Impact vs effort analysis
- Timeframe options: quarterly, sprint, annual
- ADLC Plan: Strategic planning and stakeholder feedback

#### 3. **`./scripts/build.sh [idea-name]`** or **`/build [idea-name]`** - Project Execution
- One command from idea → full project setup
- Auto-promotes ideas through pipeline
- Creates complete project structure
- ADLC Develop/Test/Deploy: Complete project implementation

#### 4. **`./scripts/finish.sh [project-name]`** or **`/finish [project-name]`** - Project Completion
- Archives completed projects
- Updates related ideas
- Handles git workflow guidance
- ADLC Complete: Project archival and operations transition

### Organization Workflow
Ideas flow automatically through these stages:
- **Inbox**: Raw ideas from `capture.sh` (`ideas/inbox/`)
- **Organized**: Auto-clustered themes (`ideas/organized/`)
- **Roadmaps**: Strategic planning outputs (`ideas/roadmaps/`)
- **Pipeline**: Ideas ready for `build.sh` (`ideas/pipeline/`)
- **Archive**: Completed or rejected ideas (`ideas/archive/`)

### Granularity Rules

**Keep Local (da-agent-hub)**:
- Technical spikes and proof-of-concepts
- Detailed implementation work (models, code, testing)
- Agent coordination and technical findings
- Knowledge preservation and learning documentation

**Export to ClickUp**:
- Strategic roadmaps for stakeholder visibility
- Cross-departmental initiatives requiring coordination
- Executive-level milestones and budget requests
- Stakeholder communication and milestone tracking

### Integration with Project System
- **Seamless promotion**: `/build` uses existing `work-init.sh` workflow
- **Context preservation**: Links maintained between ideas and projects
- **Specialist agents**: Technical analysis from dbt-expert, snowflake-expert, etc.
- **Git workflow**: Full version control for idea evolution

## Layer 2: ADLC Development Phase - Local Development & Project Management

### ADLC Develop/Test/Deploy Alignment
This layer implements **Develop**, **Test**, and **Deploy** phases:
- **Human-readable code**: Specialist agents ensure code quality and documentation
- **Flexible workflows**: Project structure adapts to different analytics needs
- **Code quality**: Agent coordination maintains standards and best practices
- **Peer review**: Agent analysis provides technical review before deployment
- **Automated deployment**: Integration with CI/CD via existing workflows
- **Testing strategy**: Data quality validation and system integration testing

### Project Execution Workflow
Use the structured project management system for implementing ideas:

```
ideas/organized/customer-analytics/
    ↓ /build customer-analytics
projects/active/feature-customer-analytics/
    ├── spec.md           # Enhanced from organized idea
    ├── context.md        # Dynamic state tracking
    ├── tasks/           # Agent coordination
    └── README.md        # Navigation hub
```

### Specialist Agent Coordination
Leverage domain experts throughout development:
- **dbt-expert**: SQL transformations, model optimization, test development
- **snowflake-expert**: Query performance, cost analysis, warehouse optimization
- **tableau-expert**: Dashboard development, report model analysis
- **business-context**: Requirements gathering, stakeholder alignment
- **da-architect**: System design, data flow analysis, strategic decisions
- **dlthub-expert**: Data ingestion, source system integration
- **orchestra-expert**: Workflow orchestration (leads all workflow analysis)
- **prefect-expert**: Prefect flow performance when Orchestra triggers them
- **qa-coordinator**: Comprehensive testing and quality assurance (ALWAYS use after tasks requiring testing/validation)

### Project Management Commands
All project management is now handled by the simplified 4-command system:
- **`./scripts/build.sh [idea-name]`** - Initialize project from organized idea
- **`./scripts/finish.sh [project-name]`** - Complete and archive project

**Legacy scripts** (still available but not needed):
- `./scripts/work-init.sh` - Used internally by `build.sh`
- `./scripts/work-complete.sh` - Used internally by `finish.sh`

## Layer 3: ADLC Operations Phase - Automated Operations & Cross-Repo Intelligence

### ADLC Operate/Observe/Discover/Analyze Alignment
This layer implements the operational phases of the Analytics Development Lifecycle:
- **Operate**: 24/7 system monitoring via GitHub Actions, error-tolerant workflows
- **Observe**: Performance monitoring, key metrics tracking, proactive issue detection
- **Discover**: Cross-repo artifact exploration, collaborative investigation analysis
- **Analyze**: Business insight generation, automated documentation, re-iteration support

### GitHub Actions Integration
The system includes automated workflows that provide Claude instances with:
- **Error Detection**: dbt Cloud monitoring and issue creation
- **Cross-Repo Context**: Access to multiple repository states
- **Investigation Tools**: Specialist agents for deep technical analysis
- **Resolution Capabilities**: Automated PR generation across repositories

### Operations Context for Claude
When Claude operates via GitHub Actions, it has access to:
- **Repository Network**: dbt_cloud, snowflake utilities, tableau configs
- **Error Context**: Full stack traces, data lineage, system states
- **Agent Expertise**: Same specialist agents available for operations
- **Resolution Patterns**: Historical fix patterns and knowledge base

### Automated Workflow Capabilities
- **Issue Investigation**: AI-powered analysis of dbt errors and data quality issues
- **Cross-System Fixes**: PRs spanning multiple repositories when needed
- **Context Preservation**: Links back to original ideas and projects when relevant
- **Stakeholder Communication**: Automated updates and resolution summaries

## Knowledge Repository Structure

### Team Documentation Template
The `knowledge/da_team_documentation/` directory provides a template structure for comprehensive Data & Analytics team documentation:

- **Location**: `knowledge/da_team_documentation/readme.md`
- **Purpose**: Template for organizing your team's Data & Analytics documentation
- **Structure**: Organized by data products, architecture, integrations, and templates
- **Navigation**: Use the readme.md as the main entry point for team documentation
- **Note**: Replace template content with your organization's specific documentation

### DA Agent Hub Platform Documentation
The `knowledge/da-agent-hub/` directory contains comprehensive documentation for the DA Agent Hub platform, organized by ADLC workflow phases:

- **Location**: `knowledge/da-agent-hub/README.md`
- **Purpose**: Complete documentation for the Analytics Development Lifecycle AI platform
- **Structure**: Three ADLC-aligned layers with phase-specific documentation
- **Navigation**: Each layer has dedicated subfolder with overview and specific guides

#### ADLC Documentation Structure:
- **Planning Layer** (`knowledge/da-agent-hub/planning/`): Idea management and strategic planning workflows
- **Development Layer** (`knowledge/da-agent-hub/development/`): Local development, agent coordination, and project management
- **Operations Layer** (`knowledge/da-agent-hub/operations/`): Automated operations, cross-repo coordination, and troubleshooting

### Knowledge Folder Management
- **Top-level files**: Included in version control for team collaboration
- **Subfolders**: Generally excluded (other knowledge repos should be separately source controlled)
- **Exceptions**:
  - `knowledge/da_team_documentation/` - GraniteRock D&A team documentation
  - `knowledge/da-agent-hub/` - DA Agent Hub platform documentation organized by ADLC phases

## Repository Branch Structures

### dbt_cloud
- **master**: Production branch
- **dbt_dw**: Staging branch
- **Workflow**: Branch from dbt_dw, sync before creating features

### dbt_errors_to_issues
- **main**: Production branch (no staging branch)
- **Workflow**: Branch directly from main

### roy_kent
- **master**: Production branch (no staging branch)  
- **Workflow**: Branch directly from master

### sherlock
- **main**: Production branch (no staging branch)
- **Workflow**: Branch directly from main

## General Git Workflow

### Branch Naming Convention
- Feature branches: `feature/description`
- Fix branches: `fix/description`

### Standard Workflow Steps
1. **Always branch from up-to-date main**: Ensure main branch is current before creating features
   - Run `git checkout main && git pull origin main` before starting any work
   - Critical for `/build` command and all da-agent-hub changes
2. Sync with production/staging branch before creating features
3. Create descriptive branch names
4. Keep branches focused and atomic
5. Test locally before pushing

## Cross-System Issue Analysis & Coordination

### Common Issue Categories (Multi-Tool)
1. **Schema/Column Reference Errors**: Tests referencing incorrect column names vs actual model schemas
2. **Data Quality Issues**: Uniqueness constraint violations, null constraint failures, massive duplications
3. **Cross-System Validation Failures**: Mismatches between source systems and dbt model expectations
4. **Business Logic Validation**: Failed reconciliation tests, metric validation errors

### Architecture-Aware Analysis Approach
- **Data Flow Context**: Issues often span multiple layers (Orchestra → [Prefect, dbt, Airbyte] → Snowflake → Semantic Layer)
- **Orchestra-Centric**: Orchestra kicks off everything - Prefect flows, dbt jobs, Airbyte syncs, direct Snowflake operations
- **Model Layer Impact**: Problems cascade from staging (stg_) through marts (dm_) to reports (rpt_)
- **Source System Dependencies**: ERP, Customer, Operations, Safety systems create different data patterns
- **Tableau Data Pipeline Analysis**: Parse TFL flows to understand published extracts, parse TWB workbooks to validate connections, trace data flow issues through XML/JSON analysis

## Complete Development Workflow

### Three-Layer Integration - Simplified 4-Command Workflow
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

### Cross-Tool Prioritization Framework
1. **CRITICAL**: Schema compilation errors that block other work (dbt-expert)
2. **HIGH**: Large-scale data quality issues indicating upstream pipeline problems (orchestra-expert + dlthub-expert)
3. **MEDIUM**: Business logic and validation failures (dbt-expert + business-context)
4. **LOW**: Warning-level issues that don't break functionality

### Agent Coordination Strategy
- **orchestra-expert**: LEADS all workflow analysis - Orchestra kicks off everything (Prefect, dbt, Airbyte, Snowflake)
- **documentation-expert**: ENSURES all agents create proper documentation within their tools and follow GraniteRock standards
- **qa-coordinator**: ⚠️ CONFIGURED BUT NOT REGISTERED - Use general-purpose agent with qa-coordinator.md standards for comprehensive testing
- **dbt-expert**: Examine model schemas vs test expectations, focus on blocking compilation issues first, maintain model documentation
- **prefect-expert**: Prefect flow performance analysis when Orchestra triggers them
- **snowflake-expert**: Validate warehouse-level performance and data quality issues, document schema purposes
- **dlthub-expert**: Source system data quality for cross-system reconciliation failures
- **tableau-expert**: Dashboard performance AND data pipeline analysis via file parsing, extract data source configurations and trace data flow issues through XML/JSON analysis, create user guides
- **business-context**: Business logic validation and stakeholder requirement clarification using knowledge base templates
- **da-architect**: System design, data flow analysis, and strategic platform decisions across the entire data stack

#### Known Agent Configuration Issues

**qa-coordinator Agent - Custom Subagent Usage**
- **Status**: `.claude/agents/qa-coordinator.md` exists as custom subagent definition
- **Root Cause**: Claude Code Task tool only supports built-in agent types (hardcoded list)
- **Solution**: Use `general-purpose` agent which can reference custom subagent definitions
- **How It Works**: general-purpose agent reads `.claude/agents/qa-coordinator.md` for behavior
- **Usage Pattern**:
  ```
  Task for general-purpose agent:
  Act as qa-coordinator (read .claude/agents/qa-coordinator.md for your role)

  Test requirements:
  - Application: http://localhost:5175
  - Changes made: [list changes]
  - Test: [specific testing requirements]
  - Capture screenshots and document findings
  ```

### Personal Claude Settings Integration

The DA Agent Hub integrates with personal Claude settings for individualized workflows:

**Personal Settings Location**: `knowledge/da_obsidian/Cody/Claude-Personal-Settings.md`

**Key Personal Workflow Integrations**:
- **QA Integration**: qa-coordinator automatically deployed after tasks requiring testing/validation
- **Agent Coordination**: Sequential execution with Roy Kent personality and 80s/90s pop culture references
- **Testing Standards**: Comprehensive hands-on testing requirements for all UI/UX work
- **Production Quality**: All code treated as production-ready with enterprise-grade standards
- **Communication Style**: Roy Kent mode with quirky humor, detailed technical responses, and multiple recommendations

**Agent-to-Task Mapping** (from personal settings):
- **UI/UX Development**: react-expert + ui-ux-expert + documentation-expert → qa-coordinator
- **Data Architecture**: da-architect + snowflake-expert + documentation-expert → qa-coordinator (validation)
- **Analytics/BI**: tableau-expert + snowflake-expert + documentation-expert → qa-coordinator (testing)

**Personal Preferences Applied**:
- Documentation-expert ALWAYS included for GraniteRock standards
- Screenshot capture required during all testing phases
- Multi-agent coordination with specialized sub-agents prioritized
- Enterprise data warehouse architect perspective maintained throughout

**Dynamic 80s/90s Pop Culture Integration**:
Claude dynamically integrates Ready Player One-style nostalgia references from era-specific contexts:
- **Movies**: Back to the Future trilogy, Goonies, Ferris Bueller, Indiana Jones, Ghostbusters, Die Hard, Top Gun
- **Gaming**: Arcade classics, Nintendo, early PC gaming, Konami Code references
- **Music**: New Wave, hair metal, early hip-hop cultural context
- **Technology**: Dial-up modems, floppy disks, early gaming consoles for technical analogies
- **MTV Generation**: Peak arcade culture, John Hughes films for project management metaphors

*Examples dynamically applied*:
- "This architecture needs more than 1.21 gigawatts to power through the data pipeline"
- "Building this system like it's the final boss fight - no extra lives, production-ready from the start"
- "Time to assemble the A-Team of sub-agents - each specialist gets their own mission"

### Development Best Practices
- **Always start from up-to-date main branch**: Essential for `/build` command and all da-agent-hub changes
- **Personal Settings Reference**: Claude automatically references `knowledge/da_obsidian/Cody/Claude-Personal-Settings.md` for workflow preferences
- **DO NOT MOVE FORWARD until you've fixed a problem**: If you encounter a blocker on step 1, DO NOT jump to step 2. Stop, identify the issue, fix it completely, then proceed. Never skip ahead when blocked.
- Git branches should be prefixed by feature/ or fix/
- Use subagents for tasks to help optimize your context window
- Determine if it'd be best to use defined agent, or if its general then give to a general subagent
- Always preserve context links between ideas → projects → operations

## Context Management & Memory System

### Session Start Protocol
When beginning any work session, Claude should check the file-based memory system:

1. **Recent Patterns** (`.claude/memory/recent/`)
   - Review monthly pattern files from the last 30 days
   - Look for relevant solutions to similar problems
   - Check for error fixes that might apply

2. **Domain Patterns** (`.claude/memory/patterns/`)
   - Load patterns relevant to the current work type
   - Check for established architectural patterns
   - Review proven solutions before investigating

3. **Task Context** (`.claude/tasks/`)
   - Check for any unfinished work or findings
   - Review recent agent outputs
   - Identify work that might need continuation

4. **Project Templates** (`.claude/memory/templates/`)
   - Use appropriate template based on branch type
   - Load investigation vs. building vs. fix templates

### Pattern Documentation Protocol
When documenting findings in `.claude/tasks/*/findings.md`, use these markers for automatic extraction:

```markdown
PATTERN: [Description of reusable pattern]
SOLUTION: [Specific solution that worked]
ERROR-FIX: [Error message] -> [Fix that resolved it]
ARCHITECTURE: [System design pattern]
INTEGRATION: [Cross-system coordination approach]
```

### Memory Extraction at Project Completion
The `/complete` command automatically:
- Extracts marked patterns from task findings
- Updates `.claude/memory/recent/` with new discoveries
- Preserves valuable learnings for future sessions
- Cleans up task findings after extraction

### Context Optimization Tips
- Reference memory patterns before starting investigations
- Document novel solutions with pattern markers
- Check recent memory for similar work before diving deep
- Use templates to start branches with appropriate context

### Automatic QA Testing Protocol

**MANDATORY**: Before reporting work complete, invoke qa-coordinator for comprehensive testing.

#### When to Trigger QA Testing
Claude MUST automatically invoke qa-coordinator when:
1. **Completing a logical set of changes** (feature addition, bug fix, refactoring)
2. **About to report "changes complete"** or "ready for review"
3. **After implementing UI/UX changes** (all interactive elements)
4. **After API/backend changes** (endpoint functionality)
5. **Before marking project milestones as complete**

#### QA Testing Workflow
```
1. Complete code changes in sandbox
2. BEFORE responding to user:
   → Launch qa-coordinator agent with testing requirements
   → Wait for comprehensive test results
   → Document test outcomes in project findings
3. Report to user: Changes + Test Results
4. Fix any issues found during testing
5. Re-test if fixes were required
```

#### What Counts as "Complete"
Work is NOT complete until:
- ✅ Code changes implemented
- ✅ QA testing performed (qa-coordinator)
- ✅ All tests passing or issues documented
- ✅ Screenshots captured (for UI changes)
- ✅ Test findings written to project tasks/

#### QA Coordinator Testing Standards
Per personal settings and qa-coordinator requirements:
- **Comprehensive hands-on testing** - Not just "it loads"
- **Every interactive element tested** - All buttons, forms, filters
- **Screenshot documentation** - Capture during testing phases
- **Real data validation** - No mock data, verify actual functionality
- **Error scenario testing** - Test failure cases, not just happy paths

#### Example QA Invocation

Use general-purpose agent with qa-coordinator role:

```markdown
Task for general-purpose agent:
Act as qa-coordinator (read .claude/agents/qa-coordinator.md for your role)

Test the Sales Journal Dashboard changes in sandbox:
- Application: http://localhost:5175
- Changes made: Fixed DMS status logic, removed mock data fallbacks
- Test Requirements:
  ✓ Verify dashboard loads with real data (no mock fallbacks)
  ✓ Test all Quick Action buttons functionality
  ✓ Validate Pipeline Status card shows correct state
  ✓ Test every interactive element (buttons, filters, tabs)
  ✓ Capture screenshots of each major section
  ✓ Test error scenarios and edge cases
- Standards: Enterprise-grade, production-ready testing per qa-coordinator.md
- Documentation: Write findings to projects/active/[project]/tasks/qa-findings.md
```

#### Reporting Format After Testing
```
✅ Changes Complete + QA Testing Results

Changes:
- [List changes made]

QA Testing (qa-coordinator):
- ✅ All tests passing
- ✅ Screenshots captured
- 🔴 [Any issues found]

[Include test findings summary or link to tasks/qa-findings.md]
```

This ensures production-quality code with enterprise-grade testing before considering work "done".

## ADLC Continuous Improvement Strategy

### Agent Knowledge Evolution
During project completion (via `/complete` command), actively identify and capture:

#### Agent Capability Enhancements
- **New tool patterns** discovered during implementation
- **Integration strategies** that proved effective across specialist domains
- **Troubleshooting insights** for common cross-system issues
- **Performance optimizations** specific to tool combinations
- **Best practices** that emerged from collaborative work

#### Agent File Updates (`/.claude/agents/`)
**Update agent files when projects demonstrate:**
- **dbt-expert.md**: Novel SQL patterns, model architectures, testing strategies
- **snowflake-expert.md**: Query optimization techniques, cost management patterns
- **tableau-expert.md**: Dashboard design patterns, user experience improvements
- **da-architect.md**: System integration patterns, architecture decision frameworks
- **documentation-expert.md**: Enhanced documentation standards and templates
- **business-context.md**: Stakeholder management patterns, requirement gathering improvements
- **orchestra-expert.md**: Workflow orchestration patterns, dependency management strategies
- **dlthub-expert.md**: Data ingestion patterns, source system integration improvements

#### Knowledge Base Enhancement (`/knowledge/`)
**Add documentation when projects reveal:**
- **System architecture patterns**: Novel integration strategies worth preserving
- **Process improvements**: Workflow enhancements that improve team efficiency
- **Technical guides**: Implementation patterns for complex multi-tool scenarios
- **Team collaboration methods**: Cross-functional coordination strategies
- **ADLC methodology refinements**: Improvements to the development lifecycle itself

### Proactive Improvement Identification
**During project work, continuously assess:**

#### Should We Open a Separate PR for System Improvements?
**Consider system improvement PRs when discovering:**
- **Agent capability gaps**: Missing expertise areas that would benefit the team
- **Knowledge documentation needs**: Undocumented patterns that cause repeated questions
- **Process bottlenecks**: Workflow inefficiencies that slow development
- **Tool integration opportunities**: Missing connections between specialist agents
- **ADLC phase improvements**: Enhancements to capture/roadmap/build/complete workflows

#### Improvement PR Decision Framework
**Create separate improvement PRs for:**
- **HIGH IMPACT**: Agent updates that benefit multiple future projects
- **KNOWLEDGE GAPS**: Missing documentation that causes repeated research
- **PROCESS OPTIMIZATION**: Workflow improvements with measurable efficiency gains
- **INTEGRATION ENHANCEMENT**: Cross-tool coordination improvements
- **ADLC METHODOLOGY**: Core system workflow refinements

**Examples of improvement PR topics:**
```
- "feat: Enhance dbt-expert with incremental model optimization patterns"
- "docs: Add Snowflake cost optimization playbook to knowledge base"
- "feat: Create tableau-performance-expert agent for dashboard optimization"
- "docs: Document cross-repo coordination patterns in operations guide"
- "feat: Improve /complete command with automated knowledge extraction"
```

### Implementation During Project Work
**While completing projects, suggest improvements:**

1. **During Implementation**: "This pattern might be valuable for future projects - should we document it?"
2. **During Testing**: "This troubleshooting approach could benefit [relevant-expert] agent"
3. **During Completion**: "The integration strategy here could improve our ADLC workflow"
4. **During Archival**: "This process improvement warrants a separate PR for the team"

### Continuous Improvement Workflow
```
🔧 PROJECT WORK (current focus)
    ↓ Identify improvement opportunities
📝 IMPROVEMENT IDENTIFICATION
    ↓ Assess impact and scope
🎯 IMPROVEMENT PR RECOMMENDATION
    ↓ Separate from current work
🚀 SYSTEM ENHANCEMENT
    ↓ Benefits future projects
💡 ENHANCED ADLC CAPABILITY
```

### Success Metrics for Continuous Improvement
- **Agent effectiveness**: Reduced need for manual research on recurring topics
- **Knowledge accessibility**: Faster onboarding and reduced repeated questions
- **Process efficiency**: Measurable improvements in project completion time
- **Cross-tool coordination**: Smoother integration across specialist domains
- **Team learning velocity**: Faster adoption of new patterns and best practices

## Agent Training & Learning System

### Automated Chat Analysis for Continuous Improvement
The DA Agent Hub includes an intelligent training system that analyzes Claude Code conversation histories to continuously improve agent effectiveness. This system learns from real usage patterns to enhance the ADLC workflow.

#### Chat Analysis Features
- **User-Agnostic Discovery**: Automatically finds Claude conversations regardless of developer setup
- **Privacy-Preserving**: Personal analysis results stay local, only anonymized insights shared
- **Effectiveness Metrics**: Tracks agent usage patterns, success rates, and knowledge gaps
- **Improvement Recommendations**: Generates specific suggestions for agent enhancements

#### Usage Commands
```bash
# Analyze your Claude conversations for training insights
./scripts/analyze-claude-chats.sh

# Results stored locally (not committed to git)
ls knowledge/da-agent-hub/training/analysis-results/

# Use insights to create agent improvement PRs
git checkout -b feature/improve-[agent-name]-based-on-analysis
```

#### Integration with Project Completion
The `/complete` command automatically analyzes project-related conversations:
- **Extracts learnings** from project chat history
- **Identifies patterns** in agent usage and effectiveness
- **Generates recommendations** for agent improvements
- **Creates PR suggestions** for high-impact enhancements

#### Training Data Sources
- **Agent invocation patterns**: Which agents are used for what tasks
- **Success/failure indicators**: User corrections, retry attempts, satisfaction signals
- **Knowledge gaps**: Areas where agents lack sufficient information
- **Collaboration patterns**: Multi-agent coordination effectiveness
- **Query types**: Common question patterns requiring better responses

#### Continuous Learning Loop
```
🔧 PROJECT WORK → 💬 CLAUDE CONVERSATIONS → 📊 AUTOMATED ANALYSIS
    ↑                                                      ↓
🚀 ENHANCED AGENTS ← 📝 IMPROVEMENT PRs ← 💡 RECOMMENDATIONS
```

#### Privacy & Security
- **Local processing**: All analysis happens on developer's machine
- **Git exclusion**: Personal analysis results automatically ignored
- **Anonymized insights**: Only high-level patterns shared with team
- **Opt-in sharing**: Developers choose what improvements to contribute

#### Example Analysis Output
```markdown
## Agent Effectiveness Report
- dbt-expert: 47 invocations (72% first-attempt success)
- snowflake-expert: 31 invocations (85% satisfaction rate)

## Knowledge Gaps Identified
1. Incremental model strategies (8 requests need better guidance)
2. Cross-system debugging patterns (5 requests lack clear workflows)

## Recommended Improvements
- Update dbt-expert.md with incremental model decision framework
- Create cross-system troubleshooting playbook for da-architect.md
```

This training system ensures the DA Agent Hub becomes more effective with every project, creating a self-improving ADLC platform that learns from real team usage patterns.

## Task vs Project Classification

### Use Project Structure (`/start_project` + `projects/` directory) When:
- **Multi-day efforts** that span multiple work sessions
- **Cross-repository coordination** (dbt + snowflake + tableau changes)
- **Research and analysis** that will inform multiple decisions
- **Collaborative work** with team members or reviewers
- **Knowledge preservation** needed for future reference
- **Complex troubleshooting** requiring systematic investigation

### Use Simple Task Execution (TodoWrite + direct action) When:
- **Quick fixes** (typos, small config changes, single-file updates)  
- **Immediate responses** to questions or information requests
- **One-off scripts** or utilities
- **Documentation updates** that don't require research
- **Status checks** or system diagnostics
- **Simple file operations** or code formatting

### Communication Patterns
- **Project Work**: Sub-agents read requirements from `projects/<project-name>/spec.md`, receive tasks from `projects/<project-name>/tasks/current-task.md`, and write findings to `projects/<project-name>/tasks/[tool]-findings.md`
- **Simple Tasks**: Direct TodoWrite tracking, immediate execution, no intermediate files

### Context Clarity & File Reference System

To prevent context confusion during development, Claude uses explicit file source indicators and maintains clear context boundaries:

#### Visual File Reference Indicators
Claude prefixes all file references with location indicators:
- **📁 PROJECT**: Working files in `projects/active/<project-name>/`
- **📦 REPO**: Source repository files (original/production versions)
- **🎯 DEPLOY**: Deployment target locations

**Examples:**
- "Analyzing 📁 PROJECT `streamlit_app.py`" → Using project working file
- "Comparing with 📦 REPO `streamlit_apps_snowflake/apex-sales-journal/`" → Referencing production
- "Ready to deploy to 🎯 DEPLOY `production-repo/`" → Deployment target

#### Workflow Signal Commands
Users can explicitly direct Claude's context focus:

| User Signal | Claude Action | Context Used |
|-------------|--------------|--------------|
| "Use the project version" | Analyze project working files | `projects/active/*/` |
| "Check the repo version" | Reference production/original | Source repository |
| "Deploy to production" | Prepare deployment from project → repo | Both, with explicit mapping |
| "Compare project vs repo" | Side-by-side analysis | Both with clear differentiation |

#### Context Declaration Protocol
Claude proactively declares context assumptions at key decision points:

**Before Analysis:**
```
📍 Context Check:
- Working File: 📁 PROJECT projects/active/feature-x/app.py
- Reference: 📦 REPO ../original-repo/app.py
- Deploy Target: 🎯 DEPLOY production-repo/

If you want different sources, please redirect me.
```

#### File Sources Section in context.md
Every project's `context.md` includes a "File Sources & Working Versions" section that explicitly declares:
- **Primary Working Files**: Files being actively developed in project directory
- **Reference Files**: Read-only sources for comparison
- **Deployment Targets**: Where changes will ultimately be deployed

This prevents accidental analysis of the wrong file version and ensures both user and Claude share the same understanding of which files are authoritative for the current work.

#### Sandbox Principle for Active Projects

**CRITICAL RULE**: `projects/active/<project-name>/` functions as an **isolated sandbox**

**All work stays in the project folder until explicit deployment:**
- Analysis files → `projects/active/<project>/`
- Code changes → `projects/active/<project>/`
- Documentation → `projects/active/<project>/`
- Testing → `projects/active/<project>/`
- Findings → `projects/active/<project>/tasks/`

**Never write to production repositories during active development** unless user explicitly requests:
- "Deploy this to [repo]"
- "Push to production"
- "Create PR in [repo]"
- Project finalized with `/finish` command

**Read-only access to production repos:**
- Reference original code for comparison
- Check current production state
- Verify deployment targets

This sandbox approach prevents accidental production changes and keeps all work isolated until ready for deployment.

## Simplified Analytics Development Commands

### Complete Workflow in 4 Commands

The DA Agent Hub now provides a streamlined approach that reduces complexity while maintaining full functionality:

#### **Essential Commands:**
1. **`./scripts/capture.sh "[idea]"`** → Brainstorm and collect ideas
2. **`./scripts/roadmap.sh [timeframe]`** → Strategic planning and prioritization
3. **`./scripts/build.sh [idea-name]`** → Execute highest priority ideas
4. **`./scripts/finish.sh [project-name]`** → Complete and archive projects

#### **Development Support Commands:**
5. **`./scripts/switch.sh [optional-branch]`** or **`/switch [optional-branch]`** → Context switching with work preservation
   - Zero-loss project switching
   - Automated work preservation and remote backup
   - Clean context preparation for new work
   - ADLC Support: Seamless phase transitions and project context management

#### **Usage Examples:**
```bash
# Weekly team brainstorming
./scripts/capture.sh "Customer churn prediction model"
./scripts/capture.sh "Real-time safety metrics dashboard"

# Monthly strategic planning
./scripts/roadmap.sh quarterly

# Execute top priority
./scripts/build.sh "customer-churn-prediction"

# Context switching during development
./scripts/switch.sh  # Save current work, switch to main
./scripts/switch.sh feature-urgent-fix  # Switch to urgent work

# Complete project
./scripts/finish.sh "feature-customer-churn-prediction"
```

#### **When to Use This Approach:**
- **All analytics projects** - from simple reports to complex multi-tool implementations
- **Cross-repository coordination** - automatic specialist agent involvement
- **Business stakeholder alignment** - built-in prioritization frameworks
- **Complex data pipelines** - full project structure and coordination
- **Team collaboration** - shared ideation and strategic planning processes

#### **Auto-Branch Management:**
The `build.sh` command automatically handles git workflow:
- Creates feature branches following naming conventions
- Sets up complete project structure with specialist agent coordination
- Integrates with existing `work-init.sh` and `work-complete.sh` infrastructure

### Project File Structure
Each project created with `./scripts/build.sh` follows this structure:

```
projects/active/<project-name>/
├── README.md           # Navigation hub with quick links and progress
├── spec.md            # Project specification (stable requirements)
├── context.md         # Working context (dynamic state tracking)
└── tasks/             # Agent coordination directory
    ├── current-task.md     # Current agent assignments
    └── <tool>-findings.md  # Detailed agent findings
```

#### File Purposes:
- **README.md**: Entry point for navigation, progress summary, key decisions
- **spec.md**: Stable project requirements, end goals, implementation plan, success criteria
- **context.md**: Dynamic state tracking - branches, PRs, blockers, current focus
- **tasks/**: Agent coordination - task assignments and detailed findings

## Analytics Development Testing Strategy

### ADLC Testing Alignment
Following the Analytics Development Lifecycle testing approach:

**Unit Tests**: Logic testing within individual models
**Data Tests**: Data quality and conformance validation
**Integration Tests**: Cross-system and end-to-end validation

### Data Quality Testing Framework
- **Schema Tests**: Column existence, data types, constraints
- **Business Logic Tests**: Metric validation, referential integrity
- **Performance Tests**: Query execution time, result set sizes
- **Cross-System Tests**: Source system vs. warehouse validation

### Personal Settings Testing Integration
Personal Claude settings automatically enhance testing workflows:
- **qa-coordinator deployment**: Triggered after any task requiring testing/validation
- **Hands-on testing requirements**: Comprehensive UI interaction, not just connectivity checks
- **Screenshot documentation**: Captured during all testing phases per personal preferences
- **Roy Kent testing philosophy**: "It loads" is NOT testing - every button gets clicked
- **Enterprise standards**: All testing treated as production-ready with zero shortcuts

### Testing Commands for Analytics Work
```bash
# ADLC-aligned testing workflow
dbt test --select <model_name>                   # Run all test types
dbt run --select <model_name>                    # Execute implementation
dbt test --select <model_name> --store-failures  # Validate results
```
- ensure you are always branching from an up to date main branch when starting a project (i.e. @scripts/build.md) and in general when working on changes to the da-agent-hub files