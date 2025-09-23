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

### Step 2: Execute Approved Knowledge Updates (Only After Approval)
**Check for updates to:**

#### Agent Knowledge (`/.claude/agents/`)
- **dbt-expert.md**: SQL patterns, model architectures, testing strategies
- **snowflake-expert.md**: Query optimization, cost management patterns
- **tableau-expert.md**: Dashboard design patterns, visualization strategies
- **da-architect.md**: System design patterns, data flow architectures
- **documentation-expert.md**: Documentation standards and templates
- **business-context.md**: Stakeholder management and requirement patterns
- **[other-agents].md**: Tool-specific insights and best practices

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
📚 Identifying knowledge for preservation...

💡 Proposed Knowledge Updates:

### Agent Files to Update:
📝 .claude/agents/da-architect.md
   + GitHub Actions automation patterns section
   + AI-powered workflow design best practices
   + [show exact content additions]

📝 .claude/agents/[other-agent].md
   + [specific additions with exact content]

### New Knowledge Documents:
📄 knowledge/technical/[new-document].md
   + [document purpose and key content outline]

### Project Documentation Updates:
📋 README.md or CLAUDE.md updates (if needed)
   + [specific sections to update]

🤔 **Should I proceed with these knowledge updates?**
   - Type 'yes' to execute all proposed changes
   - Type 'modify' to adjust specific updates
   - Type 'skip' to complete project without knowledge updates
```

### Phase 2: Execution (After Approval)
```
✅ Executing approved knowledge updates...

💡 Knowledge Updates Applied:
   ✅ Updated: agents/da-architect.md (integration patterns)
   ✅ Updated: agents/documentation-expert.md (process standards)
   ✅ Added: knowledge/technical/idea-organization-systems.md

📦 Archiving project...
   ✅ Moved to: projects/completed/YYYY-MM/[project-name]/

🔀 Git workflow options:
   1. Create PR: gh pr create --title "Complete [project-name]" --body "Project completion with knowledge extraction"
   2. Merge to main: git checkout main && git merge [branch]
   3. Stay on branch: Continue working

💡 Recommended: Create PR for review

🔗 Related ideas handled:
   ✅ Source idea found and archived: ideas/[location]/[idea-file] → ideas/archive/
   OR
   💡 No source idea found - ad-hoc project (no cleanup needed)

✅ Project '[project-name]' completed with knowledge preserved!

🎉 Next steps:
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