# /complete Command Protocol

## Purpose
Complete and archive projects with automated knowledge extraction, performance metrics tracking, and intelligent knowledge dissemination. Implements prompt-first ADLC project completion with intelligent knowledge preservation.

## Usage
```bash
claude /complete [project-name]
```

## Protocol

### 1. Project Analysis & Knowledge Extraction
**Claude analyzes completed project for:**
- **Technical Documentation**: Architecture patterns, implementation strategies
- **Agent Knowledge**: Tool-specific learnings and best practices
- **Process Insights**: Workflow improvements and organizational patterns
- **Integration Patterns**: Cross-system coordination strategies
- **Performance Metrics**: Agent effectiveness and routing intelligence

### 2. Automated Knowledge Dissemination
**Before archiving, Claude automatically:**
- **Extracts key patterns** from project specifications and findings
- **Updates agent knowledge bases** with tool-specific insights
- **Tracks performance metrics** for continuous improvement
- **Updates confidence scores** based on project outcomes
- **Preserves technical documentation** in knowledge directory
- **Creates cross-references** for future project reference

### 3. Complete Project Archival
- **Archives project**: Moves to `projects/completed/YYYY-MM/[project-name]/`
- **Extracts patterns**: Auto-populates memory system via finish.sh
- **Git workflow guidance**: Provides PR creation and merge options
- **Updates related ideas**: Links completion back to original archived ideas
- **Enables operations**: Project ready for ADLC Operate phase monitoring

## Claude Instructions

When user runs `/complete [project-name]`:

### Step 1: Analyze Project and Propose Knowledge Changes
1. **Read project files**: spec.md, context.md, tasks/, README.md
2. **Identify extractable knowledge**:
   - Architecture patterns and technical decisions
   - Tool-specific insights for specialist agents
   - Process improvements and workflow learnings
   - Integration strategies and coordination patterns

3. **Present proposed changes BEFORE making them**:
   - List specific agent files to update with exact content additions
   - Identify new knowledge documents to create
   - Show proposed updates to README.md or CLAUDE.md if relevant
   - Request explicit approval: "Should I proceed with these knowledge updates?"

4. **WAIT for user approval** before making any changes

### Step 1.5: Extract Performance Metrics
**Track quantitative data for continuous improvement:**

1. **Agent invocation patterns**:
   - Count agent invocations by type (dbt-expert: 3, snowflake-expert: 2, etc.)
   - Document success/retry patterns for each agent
   - Measure estimated execution times

2. **Performance indicators**:
   - Success rate (completed without retries vs total attempts)
   - Task complexity indicators (simple query vs complex transformation)
   - Cross-agent coordination effectiveness

3. **Failure pattern documentation**:
   - Common error types encountered
   - Retry scenarios and resolution methods
   - Knowledge gaps identified during execution

4. **Confidence score updates**:
   - Identify successful patterns that should increase agent confidence
   - Document areas where agents struggled (decrease confidence)
   - Calculate confidence adjustments based on task outcomes

### Step 2: Execute Approved Knowledge Updates (Only After Approval)
**Check for updates to:**

#### Agent Knowledge (`/.claude/agents/`)
- **dbt-expert.md**: SQL patterns, model architectures, testing strategies + confidence updates
- **snowflake-expert.md**: Query optimization, cost management patterns + confidence updates
- **tableau-expert.md**: Dashboard design patterns, visualization strategies + confidence updates
- **da-architect.md**: System design patterns, data flow architectures + confidence updates
- **documentation-expert.md**: Documentation standards and templates + confidence updates
- **business-context.md**: Stakeholder management and requirement patterns + confidence updates
- **[other-agents].md**: Tool-specific insights and best practices + confidence updates

**Confidence Score Management:**
- Update agent confidence levels based on project outcomes
- Document successful patterns that warrant confidence increases (+0.05 to +0.15)
- Identify knowledge gaps that suggest confidence decreases (-0.05 to -0.10)
- Create routing recommendations for future similar tasks

#### Technical Documentation (`/knowledge/`)

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

**Three-Tier Documentation Principle**:
- **Tier 1**: Repository README (lightweight, < 200 lines, developer-focused)
- **Tier 2**: Knowledge base (comprehensive source of truth, unlimited size)
- **Tier 3**: Agent pattern index (pointers with confidence scores)

#### Memory System Updates (`/.claude/memory/`)
**Note**: Pattern extraction happens automatically via `finish.sh`:
- Extracts patterns marked with PATTERN:, SOLUTION:, ERROR-FIX:, etc.
- Saves to `.claude/memory/recent/YYYY-MM.md`
- No manual action needed - automatic during archival

### Step 3: Archive Project
1. **Create archive directory**: `projects/completed/YYYY-MM/[project-name]/`
2. **Move project files**: Complete project structure with full history
3. **Remove from active**: Clean up `projects/active/[project-name]/`

### Step 4: Git Workflow Guidance
**Provide branch-aware options:**
- **Feature branch**: Recommend PR creation for review
- **Main branch**: Confirm direct merge readiness
- **Stay on branch**: Option to continue working

### Step 5: Handle Related Ideas (If Any)
- **Search for source ideas**: Look for original idea that led to this project
- **Handle based on what's found**:
  - **If source idea exists**: Move to archive and update with completion status
  - **If no source idea**: Note as ad-hoc project (no idea cleanup needed)
  - **If orphaned ideas found**: Clean up any related unarchived ideas
- **Cross-reference completion**: Maintain idea → project → completion traceability when applicable
- **Clean up workflow**: Ensure no orphaned ideas remain in inbox/organized

## Response Format

### Phase 1: Analysis and Proposal
```
🔍 Analyzing project: [project-name]
📊 Extracting performance metrics...

📈 Project Performance Summary:
   • Agents invoked: 5 (dbt-expert: 3, snowflake-expert: 2)
   • Success rate: 100% (0 retries needed)
   • Estimated execution time: 18 minutes
   • Task complexity: Medium (cross-system integration)
   • New patterns discovered: 3

🎯 Confidence Updates:
   ↗️ dbt-expert: +0.10 (incremental model optimization)
   ↗️ snowflake-expert: +0.05 (query performance tuning)
   ➡️ tableau-expert: No change (limited involvement)

📚 Identifying knowledge for preservation...

💡 Proposed Knowledge Updates:

### Agent Files to Update:
📝 .claude/agents/da-architect.md
   + GitHub Actions automation patterns section
   + AI-powered workflow design best practices
   + Confidence: +0.08
   + [show exact content additions]

📝 .claude/agents/dbt-expert.md
   + Incremental model optimization patterns
   + Confidence: +0.10
   + [specific additions with exact content]

### New Knowledge Documents:
📄 knowledge/applications/[app-name]/ (if deploying new app)
   + architecture/system-design.md - System architecture and data flows
   + deployment/production-deploy.md - Complete deployment runbook
   + operations/troubleshooting.md - Monitoring and incident response
   + Three-tier pattern integration:
     - Update aws-expert.md pattern index (Tier 3) with confidence scores
     - Add to ui-ux-developer-role.md Known Applications section
     - Create lightweight README in app repo (Tier 1) linking to knowledge base

📄 knowledge/da-agent-hub/[new-pattern].md (if platform improvement)
   + [document purpose and key content outline]

### Memory Extraction (Automatic):
🤖 finish.sh will automatically extract:
   - 3 PATTERN markers from task findings
   - 2 SOLUTION markers
   - 1 ERROR-FIX marker
   → Saved to memory/recent/YYYY-MM.md

🤔 **Should I proceed with these knowledge updates?**
   - Type 'yes' to execute all proposed changes
   - Type 'modify' to adjust specific updates
   - Type 'skip' to complete project without knowledge updates
```

### Phase 2: Execution (After Approval)
```
✅ Executing approved knowledge updates...

💡 Knowledge Updates Applied:
   ✅ Updated: agents/da-architect.md (integration patterns + confidence: +0.08)
   ✅ Updated: agents/dbt-expert.md (incremental model patterns + confidence: +0.10)
   ✅ Updated: agents/documentation-expert.md (process standards + confidence: +0.03)
   ✅ Added: knowledge/applications/[app-name]/ (three-tier docs for production app)
      - architecture/system-design.md, deployment/production-deploy.md, operations/troubleshooting.md
      - Updated aws-expert.md pattern index + ui-ux-developer-role.md Known Applications
   ✅ Added: knowledge/da-agent-hub/[new-pattern].md (platform improvement)

📦 Archiving project...
   ✅ Moved to: projects/completed/YYYY-MM/[project-name]/
   🧹 Pattern extraction: 6 patterns saved to memory/recent/

🔀 Git workflow options:
   1. Create PR: gh pr create --title "Complete [project-name]" --body "Project completion with knowledge extraction"
   2. Merge to main: git checkout main && git merge [branch]
   3. Stay on branch: Continue working

💡 Recommended: Create PR for review

🤖 Routing Recommendations for Future Projects:
   • For incremental model work: Prefer dbt-expert (confidence: 0.92)
   • For query optimization: dbt-expert + snowflake-expert (high coordination success)
   • For cross-system integration: da-architect → dbt-expert → snowflake-expert (proven sequence)

🔗 Related ideas handled:
   ✅ Source idea found and archived: ideas/[location]/[idea-file] → ideas/archive/
   OR
   💡 No source idea found - ad-hoc project (no cleanup needed)

✅ Project '[project-name]' completed with knowledge preserved and metrics tracked!

🎉 Next steps:
   - Review performance metrics and confidence updates
   - Review completed work and extracted knowledge
   - Create PR if on feature branch
   - Plan next project: ./scripts/build.sh [idea-name]
```

## Knowledge Extraction Criteria

### Agent Knowledge Updates
**Update agent files when project contains:**
- **New tool patterns**: Implementation strategies specific to each tool
- **Best practices**: Proven approaches for tool configuration/usage
- **Integration patterns**: How tools coordinate with other systems
- **Troubleshooting insights**: Common issues and resolution patterns
- **Performance optimizations**: Efficiency improvements and cost management
- **Confidence adjustments**: Success/failure patterns affecting agent reliability

### Technical Documentation
**Add to knowledge/ when project demonstrates:**
- **Production applications** (`knowledge/applications/<app-name>/`): New deployments or major app updates
  - Follow three-tier pattern: Tier 2 comprehensive docs (architecture/, deployment/, operations/)
  - Update agent pattern indexes (Tier 3) and Known Applications in role agents
  - Create lightweight repo README (Tier 1) linking to knowledge base
- **System architecture**: Novel integration or design patterns
- **Process improvements**: Workflow enhancements worth preserving
- **Standards evolution**: Updated team practices and conventions
- **Cross-system coordination**: Multi-tool orchestration patterns

### Performance Metrics Documentation
**Track and update when project reveals:**
- **Agent effectiveness patterns**: Which agents excel at specific tasks
- **Coordination strategies**: Successful multi-agent workflows
- **Failure modes**: Common pitfalls and prevention strategies
- **Routing intelligence**: Optimal agent selection for task types

### Dissemination Decision Framework
- **High impact + high confidence**: Core system changes → Update multiple agent files + increase confidence
- **Tool-specific + proven**: Single tool insights → Update relevant agent only + confidence boost
- **Process innovation**: Workflow improvements → Update knowledge/ + document success patterns
- **Team learning**: Collaborative insights → Update da_team_documentation/ + share metrics
- **Failed experiments**: Document what didn't work → Decrease confidence + capture lessons

## Integration with ADLC & Memory System
- **ADLC Deploy Completion**: Final deployment with knowledge preservation and metrics
- **ADLC Operate Transition**: Project ready for operations with documented patterns and performance data
- **ADLC Observe Setup**: Knowledge base + metrics enable better monitoring and issue resolution
- **Cross-layer context**: Full traceability from idea to operations with preserved learnings
- **Memory System**: Automatic pattern extraction via finish.sh populates `.claude/memory/recent/`
- **Confidence Routing**: Performance metrics inform future agent selection and coordination

## Success Criteria
- [ ] Project knowledge automatically extracted and preserved
- [ ] Performance metrics tracked and analyzed
- [ ] Agent confidence scores updated based on outcomes
- [ ] Relevant agent files updated with new insights + confidence adjustments
- [ ] Technical documentation created when warranted
- [ ] Memory system populated with patterns (automatic via finish.sh)
- [ ] Routing recommendations generated for future projects
- [ ] Project successfully archived to completed directory
- [ ] Git workflow guidance provided based on current branch
- [ ] Related archived ideas updated with completion status
- [ ] Clear next steps for continued development cycle

---

*ADLC project completion with intelligent knowledge preservation, performance tracking, and confidence-based routing - from active development to operational wisdom with compound learning.*