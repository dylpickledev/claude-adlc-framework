# /complete Command Protocol

## Purpose
Complete and archive projects with automated knowledge extraction and dissemination. Implements prompt-first ADLC project completion with intelligent knowledge preservation.

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

### 2. Automated Knowledge Dissemination
**Before archiving, Claude automatically:**
- **Extracts key patterns** from project specifications and findings
- **Updates agent knowledge bases** with tool-specific insights
- **Preserves technical documentation** in knowledge directory
- **Creates cross-references** for future project reference

### 3. Complete Project Archival
- **Archives project**: Moves to `projects/completed/YYYY-MM/[project-name]/`
- **Git workflow guidance**: Provides PR creation and merge options
- **Updates related ideas**: Links completion back to original archived ideas
- **Enables operations**: Project ready for ADLC Operate phase monitoring

## Claude Instructions

When user runs `/complete [project-name]`:

### Step 1: Analyze Project for Knowledge
1. **Read project files**: spec.md, context.md, tasks/, README.md
2. **Identify extractable knowledge**:
   - Architecture patterns and technical decisions
   - Tool-specific insights for specialist agents
   - Process improvements and workflow learnings
   - Integration strategies and coordination patterns

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

### Step 2: Extract and Preserve Knowledge
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
- **Architecture patterns**: System design and integration strategies
- **Process documentation**: Workflow improvements and organizational methods
- **Technical guides**: Implementation patterns and troubleshooting
- **Team documentation**: Standards and collaborative practices

### Step 3: Archive Project
1. **Create archive directory**: `projects/completed/YYYY-MM/[project-name]/`
2. **Move project files**: Complete project structure with full history
3. **Remove from active**: Clean up `projects/active/[project-name]/`

### Step 4: Git Workflow Guidance
**Provide branch-aware options:**
- **Feature branch**: Recommend PR creation for review
- **Main branch**: Confirm direct merge readiness
- **Stay on branch**: Option to continue working

### Step 5: Update Related Ideas
- **Search related ideas**: Find and update any linked archived ideas
- **Cross-reference completion**: Maintain idea → project → completion traceability

## Response Format
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

📚 Extracting knowledge for preservation...

💡 Knowledge Updates:
   ✅ Updated: agents/da-architect.md (integration patterns + confidence: +0.08)
   ✅ Updated: agents/documentation-expert.md (process standards + confidence: +0.03)
   ✅ Updated: agents/dbt-expert.md (incremental model patterns + confidence: +0.10)
   ✅ Added: knowledge/technical/idea-organization-systems.md

📦 Archiving project...
   ✅ Moved to: projects/completed/YYYY-MM/[project-name]/

🔀 Git workflow options:
   1. Create PR: gh pr create --title "Complete [project-name]" --body "Project completion with knowledge extraction"
   2. Merge to main: git checkout main && git merge [branch]
   3. Stay on branch: Continue working

💡 Recommended: Create PR for review

🤖 Routing Recommendations for Future Projects:
   • For incremental model work: Prefer dbt-expert (confidence: 0.92)
   • For query optimization: dbt-expert + snowflake-expert (high coordination success)
   • For cross-system integration: da-architect → dbt-expert → snowflake-expert (proven sequence)

🔗 Related ideas updated: [list any updated archived ideas]

✅ Project '[project-name]' completed with knowledge preserved and metrics tracked!

🎉 Next steps:
   - Review performance metrics and confidence updates
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

### Technical Documentation
**Add to knowledge/ when project demonstrates:**
- **System architecture**: Novel integration or design patterns
- **Process improvements**: Workflow enhancements worth preserving
- **Standards evolution**: Updated team practices and conventions
- **Cross-system coordination**: Multi-tool orchestration patterns

### Dissemination Decision Framework
- **High impact**: Core system changes → Update multiple agent files
- **Tool-specific**: Single tool insights → Update relevant agent only
- **Process innovation**: Workflow improvements → Update knowledge/
- **Team learning**: Collaborative insights → Update da_team_documentation/

## Integration with ADLC
- **ADLC Deploy Completion**: Final deployment with knowledge preservation
- **ADLC Operate Transition**: Project ready for operations with documented patterns
- **ADLC Observe Setup**: Knowledge base enables better monitoring and issue resolution
- **Cross-layer context**: Full traceability from idea to operations with preserved learnings

## Success Criteria
- [ ] Project knowledge automatically extracted and preserved
- [ ] Relevant agent files updated with new insights
- [ ] Technical documentation created when warranted
- [ ] Project successfully archived to completed directory
- [ ] Git workflow guidance provided based on current branch
- [ ] Related archived ideas updated with completion status
- [ ] Clear next steps for continued development cycle

---

*ADLC project completion with intelligent knowledge preservation - from active development to operational wisdom.*