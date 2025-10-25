# /complete Command Protocol (Enhanced with ACE Learning)

## Purpose
Complete and archive projects with automated knowledge extraction, performance metrics tracking, ACE-based continuous learning, and intelligent knowledge dissemination. Implements prompt-first ADLC project completion with skill discovery, pattern evolution, and subagent-enhanced analysis.

## Usage
```bash
claude /complete [project-name]
```

## Protocol Overview

```
🔍 Analysis Phase (Steps 1-1.9):
   - Project knowledge extraction
   - Performance metrics & delegation effectiveness
   - ACE self-reflection on what worked/failed
   - Skill discovery from repetitive workflows
   - Pattern confidence evolution
   - Subagent validation (configuration, patterns, dissemination)

💬 Approval Phase:
   - User reviews and approves proposed changes

✅ Execution Phase (Steps 2-5):
   - Execute approved knowledge updates
   - Archive project with patterns
   - Git workflow guidance
   - GitHub issue closure
```

---

## Analysis Phase: Steps 1-1.9

### Step 1: Project Analysis & Knowledge Extraction

**Claude analyzes completed project for:**
- **Technical Documentation**: Architecture patterns, implementation strategies
- **Agent Knowledge**: Tool-specific learnings and best practices
- **Process Insights**: Workflow improvements and organizational patterns
- **Integration Patterns**: Cross-system coordination strategies
- **Performance Metrics**: Agent effectiveness and routing intelligence

**Actions**:
1. **Read project files**: `spec.md`, `context.md`, `tasks/`, `README.md`
2. **Identify extractable knowledge**:
   - Architecture patterns and technical decisions
   - Tool-specific insights for specialist agents
   - Process improvements and workflow learnings
   - Integration strategies and coordination patterns

---

### Step 1.5: Extract Performance Metrics & Delegation Effectiveness

**Track quantitative AND qualitative data for continuous improvement:**

#### 1.5.1 Agent Invocation Patterns
- Count agent invocations by type (dbt-expert: 3, snowflake-expert: 2, etc.)
- Document success/retry patterns for each agent
- Measure estimated execution times

#### 1.5.2 Performance Indicators
- Success rate (completed without retries vs total attempts)
- Task complexity indicators (simple query vs complex transformation)
- Cross-agent coordination effectiveness

#### 1.5.3 Delegation Effectiveness Analysis (NEW)

For each specialist agent invoked, assess:

```markdown
### [specialist-name] Delegation Assessment

**Invocations**: [X] times
**Tasks Delegated**:
1. [Task 1 description]
2. [Task 2 description]

**Value Delivered**:
- **Specialist Outcome**: [What specialist provided]
- **Compared to Direct Role Work**: [Would role agent have achieved same quality?]
- **Unique Value**: [What specifically required specialist expertise?]
- **Business Impact**: [Cost savings, bug prevention, time saved]

**Delegation Necessity**:
- ✅ **Necessary**: Required specialist expertise, role confidence <0.60
- ⚠️ **Marginal**: Role could have handled, but specialist added quality
- ❌ **Unnecessary**: Role agent could have achieved same outcome directly

**Token Cost vs Value**:
- Specialist tokens: [X]
- Estimated direct role tokens: [Y]
- Cost multiplier: [X/Y]x
- Value delivered: [$Z business impact / time saved / bugs prevented]
- ROI: [Z / token cost] = [High/Medium/Low] value
```

#### 1.5.4 Confidence Threshold Validation (NEW)

```markdown
### Delegation Decision Validation

**Role Agent Confidence Levels This Project**:
| Task | Role Confidence | Delegated? | Outcome | Correct Decision? |
|------|----------------|------------|---------|-------------------|
| [task-1] | 0.75 | ❌ No | ✅ Success | ✅ Yes (confidence adequate) |
| [task-2] | 0.55 | ✅ Yes | ✅ Success | ✅ Yes (needed specialist) |
| [task-3] | 0.75 | ✅ Yes | ✅ Success | ⚠️ Marginal (could have tried directly) |

**Threshold Optimization**:
- Current delegation threshold: 0.60
- Delegation decisions correct: [X]/[Y] ([Z]%)
- Threshold adjustment: [Recommendation based on data]
```

#### 1.5.5 Confidence Score Updates

```markdown
### Confidence Score Updates

**Increases** (Successful patterns):
- [agent-name]: +0.10 ([pattern name])
  - **Evidence**: [Specific success in project]
  - **Validation count**: [X projects using this pattern successfully]
  - **New confidence**: 0.XX → 0.XX

**Decreases** (Knowledge gaps or failures):
- [agent-name]: -0.05 ([area of struggle])
  - **Evidence**: [Specific challenge or failure]
  - **Root cause**: [Why pattern didn't work]
  - **Remediation**: [What was learned, what should change]

**Delegation Threshold Adjustments**:
- [agent-name]: Threshold 0.60 → 0.65 (reduce marginal delegations)
- [agent-name]: Threshold 0.60 → 0.55 (increase delegation for quality)
```

---

### Step 1.75: Project Execution Reflection (NEW - ACE Learning)

**Analyze project execution for continuous improvement learnings:**

#### 1.75.1 Approach Effectiveness Analysis

```markdown
## Project Execution Reflection

### Effective Approaches ✅
1. [Approach name] (Effectiveness: High/Medium)
   - **What worked**: [Specific success]
   - **Evidence**: [Measurable outcome]
   - **Reuse guidance**: When to apply this approach

### Ineffective Approaches ⚠️
1. [Approach name] (Effectiveness: Low)
   - **What didn't work**: [Specific failure]
   - **Root cause**: [Why it failed]
   - **Better alternative**: [What should be used instead]
```

#### 1.75.2 Error Pattern Analysis

```markdown
### Error Patterns Resolved 🔧
1. [Error type]: [Error message or description]
   - **Frequency**: [How many times encountered]
   - **Resolution**: [Solution that worked]
   - **Prevention**: [Pattern to avoid future occurrence]
```

#### 1.75.3 Skill Performance Validation

If skills were used during project:

```markdown
### Skill Performance Validation 🎯
1. [skill-name] (Used: X times)
   - **Outcome**: ✅ Expected / ⚠️ Needs improvement
   - **Feedback**: [What worked, what needs refinement]
   - **Action**: Update skill instructions / No change needed
```

#### 1.75.4 Decision Quality Review

```markdown
### Decision Quality Review 🤔
1. [Decision name]
   - **Evidence used**: [Documentation, benchmarks, patterns]
   - **Outcome**: ✅ Validated / ⚠️ Needs refinement
   - **Pattern**: [Reusable decision framework if applicable]
```

#### 1.75.5 Knowledge Gap Identification

```markdown
### Knowledge Gaps Identified 📚
1. [Gap description]
   - **Impact**: [How it affected project - time lost, uncertainty]
   - **Action**: Add to [agent knowledge base / pattern library / CLAUDE.md]
```

**Questions to Answer**:
- What approaches/patterns worked well? (Rank by effectiveness)
- What approaches didn't work or were inefficient? (Identify failures)
- Were there alternative approaches considered? Which was chosen and why?
- What would you do differently if starting this project again?
- What errors/retries occurred? What was root cause and resolution?
- Which skills were invoked? Did they deliver expected outcomes?
- What major technical decisions were made? Were they validated by outcomes?
- What information was missing that slowed progress?

---

### Step 1.8: Skill Discovery Analysis (NEW - Automation Opportunities)

**Analyze project for repetitive workflows that should be automated:**

#### 1.8.1 Workflow Frequency Analysis

- Review project files (`spec.md`, `context.md`, task findings, `README.md`)
- Identify procedural patterns: "Step A → Step B → Step C" sequences
- Count repetitions: How many times was similar workflow executed?
- Compare to past projects: Have we done this workflow 3+ times total?

#### 1.8.2 Automation Opportunity Scoring

```markdown
## Skill Discovery Analysis 🤖

### Workflow Frequency Detected
| Workflow | This Project | Historical | Time/Exec | Automation Value |
|----------|--------------|------------|-----------|------------------|
| [workflow-1] | X times | Y times total | Z min | HIGH/MED/LOW |
| [workflow-2] | X times | Y times total | Z min | HIGH/MED/LOW |
```

**Scoring Criteria**:
- **HIGH VALUE**: 3+ occurrences, 15+ min each, clear reusable pattern
- **MEDIUM VALUE**: 2-3 occurrences, 10-15 min each, partially reusable
- **LOW VALUE**: 1-2 occurrences, <10 min each, context-specific

#### 1.8.3 Template Extraction

- Identify reusable document structures (spec.md sections, README patterns)
- Identify reusable code patterns (dbt model boilerplate, SQL patterns)
- Identify reusable configuration (git workflows, deployment steps)

#### 1.8.4 Skill Candidate Proposal

For each HIGH VALUE automation opportunity:

```markdown
### Skill Candidate: [proposed-skill-name]

**Trigger**: You've executed [workflow] [X] times manually
**Workflow Steps**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Templates Needed**:
- [template-1.md]: [Purpose]
- [template-2.sql]: [Purpose]

**Expected Time Savings**: [Y] minutes per execution × [frequency] = [Z] min/month

**Should I create this skill?**
- Type 'yes' to implement skill with templates
- Type 'defer' to track as candidate for future
- Type 'no' if not worth automating
```

---

### Step 1.9: Pattern Confidence Evolution (NEW - ACE Context Evolution)

**Update pattern confidence scores based on project validation:**

#### 1.9.1 DELEGATE to memory-system-expert

**Task**: Analyze extracted patterns and optimize for reusability

**Delegation Context**:
```
Analyze project for pattern validation and evolution:

Raw Patterns Extracted:
- [List PATTERN:, SOLUTION:, ERROR-FIX: markers from project]

Existing Pattern Library:
- .claude/memory/patterns/ ([X] patterns currently)

Questions:
1. Which extracted patterns are genuinely reusable vs project-specific?
2. Do any extracted patterns overlap with existing patterns?
3. What patterns are missing that would be valuable?
4. How should confidence scores be updated based on validation?
5. Are there patterns that should be deprecated in favor of better approaches?

Deliverable: Pattern extraction recommendations with reusability assessment
```

**Expected Output from memory-system-expert**:

```markdown
## Pattern Extraction Optimization

**Reusable Patterns (Create New)**:
1. **[new-pattern-name]** (Confidence: 0.XX)
   - Source: [Where pattern came from]
   - Reusability: HIGH/MEDIUM/LOW
   - Create as: .claude/memory/patterns/[pattern-name].md

**Update Existing Patterns**:
2. **[existing-pattern-name]**
   - Current confidence: 0.XX
   - New validation: [Xth] project success
   - Update confidence: 0.XX → 0.XX
   - Add contextual guidance: "[New scenario-specific guidance]"

**Project-Specific (Don't Extract)**:
3. [Pattern that's too context-specific]
   - Reason: [Why not reusable]

**Implicit Patterns Discovered**:
4. [Pattern not explicitly marked but evident from execution]
   - Confidence: 0.XX
   - Action: Extract as reusable pattern
```

#### 1.9.2 Pattern Outcome Assessment

For each pattern used in project:

```markdown
### Pattern: [pattern-name]

**Usage Context**: [When/how pattern was applied]
**Outcome**: ✅ Success / ⚠️ Partial success / ❌ Failed
**Success Criteria**:
- Expected result: [What pattern promised]
- Actual result: [What actually happened]
- Match quality: [Exact match / Close / Significant deviation]

**Modifications Required**:
- ✅ None (pattern worked as documented)
- ⚠️ Minor (small adjustments needed)
- ❌ Major (significant rework required)

**Contextual Fit**:
- Scenario: [Project-specific context]
- Pattern fit: ✅ Perfect / ⚠️ Adequate / ❌ Poor
- Edge cases discovered: [Any scenarios where pattern struggled]
```

---

### Step 1: Propose Knowledge Changes (Synthesize All Analysis)

**DELEGATE to claude-code-expert** for configuration quality audit:

**Task**: Review proposed agent knowledge updates for Anthropic best practices alignment

**Delegation Context**:
```
Review proposed knowledge updates:

Project Files Analyzed:
- .claude/agents/[agent-files-modified].md
- .claude/skills/[skills-used].md
- Proposed updates: [Show proposed changes]

Questions:
1. Do proposed agent updates follow Anthropic agent best practices?
2. Are confidence score adjustments appropriate (+0.05 to +0.15 range)?
3. Should any new patterns be created vs updating existing agent files?
4. Are skill performance validations comprehensive?
5. Do proposed updates maintain single-purpose focus for agents?

Deliverable: Configuration quality validation report with approval/refinements
```

**DELEGATE to documentation-expert** for dissemination strategy:

**Task**: Design optimal knowledge dissemination strategy for project learnings

**Delegation Context**:
```
Design knowledge dissemination strategy:

Extractable Knowledge:
- [Architecture pattern 1]: [Description]
- [Tool insight 1]: [Description]
- [Process improvement 1]: [Description]

Questions:
1. Which knowledge belongs in agent files vs patterns vs application docs?
2. Should new application documentation follow three-tier pattern?
3. What cross-references should be created between documentation layers?
4. Are there existing docs to update vs create new?
5. What detail level appropriate for each documentation location?

Deliverable: Knowledge dissemination strategy with specific file updates
```

#### 1.10 Synthesize Specialist Recommendations

**Main Claude synthesizes**:
- memory-system-expert pattern recommendations
- claude-code-expert configuration validation
- documentation-expert dissemination strategy

**Present unified proposal to user** with all recommended changes:

```markdown
🔍 Analyzing project: [project-name]
📊 Extracting performance metrics...

📈 Project Performance Summary:
   • Agents invoked: [X] (agent-1: Y, agent-2: Z)
   • Success rate: [X]% ([Y] retries needed)
   • Estimated execution time: [X] minutes
   • Task complexity: [Simple/Medium/Complex]
   • New patterns discovered: [X]

🎯 Delegation Effectiveness:

   **[agent-name] ([X] invocations)**:
   - Value: HIGH/MEDIUM/LOW ([business impact])
   - Necessity: ✅ Necessary ([X]/[Y]), ⚠️ Marginal ([Z]/[Y])
   - Token ROI: [X]x ([tokens] → [value])
   - Unique contribution: [What specialist provided]

🎯 Confidence Updates:
   ↗️ [agent-name]: +0.10 ([pattern name])
      - Evidence: [Xth] successful project using this pattern
      - New confidence: 0.XX → 0.XX

## Project Execution Reflection

### Effective Approaches ✅
[List approaches that worked well]

### Ineffective Approaches ⚠️
[List approaches that didn't work]

### Error Patterns Resolved 🔧
[List errors and their resolutions]

### Skill Performance Validation 🎯
[List skills used and their effectiveness]

## Skill Discovery Analysis 🤖

### Workflow Frequency Detected
[Table showing workflows and automation value]

### Skill Candidates (HIGH VALUE)
[List proposed skills with time savings calculations]

## Pattern Confidence Evolution 📊

### Patterns Validated This Project
[List patterns with updated confidence scores]

### Pattern Supersession Detected
[List deprecated patterns replaced by better approaches]

💡 Proposed Knowledge Updates:

### Agent Files to Update:
📝 .claude/agents/[agent-name].md
   + [Pattern name] section
   + Confidence: +0.XX ([reason])
   + [show exact content additions]

### New Knowledge Documents:
📄 knowledge/applications/[app-name]/ (if deploying new app)
   + architecture/system-design.md - [Purpose]
   + deployment/production-deploy.md - [Purpose]
   + operations/troubleshooting.md - [Purpose]

📄 .claude/memory/patterns/[new-pattern].md
   + [Pattern purpose and key content]

### Memory Extraction (Automatic):
🤖 finish.sh will automatically extract:
   - [X] PATTERN markers from task findings
   - [Y] SOLUTION markers
   - [Z] ERROR-FIX markers
   → Saved to memory/recent/YYYY-MM.md

### Configuration Quality Validation (claude-code-expert):
✅ [Agent updates follow Anthropic best practices]
⚠️ [Recommendations for refinement]

### Knowledge Dissemination Strategy (documentation-expert):
✅ [Optimal knowledge placement following three-tier pattern]

🤔 **Should I proceed with these knowledge updates?**
   - Type 'yes' to execute all proposed changes
   - Type 'modify' to adjust specific updates
   - Type 'skip' to complete project without knowledge updates
```

---

## Approval Phase

### WAIT for User Approval

User options:
- **yes**: Execute all proposed changes
- **modify**: Adjust specific updates (Claude asks which to modify)
- **skip**: Complete project without knowledge updates

---

## Execution Phase: Steps 2-5

### Step 2: Execute Approved Knowledge Updates

**Only after user approval, Claude executes:**

#### 2.1 Agent Knowledge Updates

Update agent files with:
- Tool-specific insights and best practices
- Confidence score adjustments based on outcomes
- Integration patterns and coordination strategies
- Performance metrics updates

**For each agent file updated**:
- Add new pattern sections with evidence
- Update confidence scores with validation counts
- Add contextual guidance (when to use, when to avoid)
- Update routing recommendations

#### 2.2 Technical Documentation

**Production Application Knowledge** → `knowledge/applications/<app-name>/`:
- **When**: Deploying new apps or major app updates
- **Structure**: Three-tier pattern (Tier 2 - comprehensive docs)
  - `architecture/` - System design, data flows, infrastructure details
  - `deployment/` - Complete deployment runbooks, Docker builds, AWS configuration
  - `operations/` - Monitoring, troubleshooting guides, incident response
- **Updates Required**:
  1. Create/update knowledge base docs for the application
  2. Update agent pattern index (e.g., aws-expert.md with confidence scores)
  3. Add to "Known Applications" in relevant role agents
  4. Create lightweight README in actual repo (Tier 1) linking to knowledge base

**Platform/Tool Patterns** → `knowledge/da-agent-hub/`:
- **When**: Discovering reusable patterns for ADLC workflow
- **Structure**: Organized by ADLC phase (planning/, development/, operations/)
- **Examples**: Testing frameworks, git workflows, cross-system analysis patterns

#### 2.3 Pattern Library Updates

- Create new patterns based on memory-system-expert recommendations
- Update existing patterns with new validations and confidence scores
- Add contextual guidance to patterns (when to use, when to avoid)
- Deprecate superseded patterns with links to better approaches

#### 2.4 Skill Creation (If Proposed)

If HIGH VALUE skill candidates identified:
- Create `.claude/skills/[skill-name]/skill.md` with workflow
- Add templates to `.claude/skills/[skill-name]/templates/`
- Update `.claude/skills/README.md` catalog
- Document trigger phrases and expected outcomes

#### 2.5 Memory System Updates

**Note**: Pattern extraction happens automatically via `finish.sh`:
- Extracts patterns marked with PATTERN:, SOLUTION:, ERROR-FIX:, etc.
- Saves to `.claude/memory/recent/YYYY-MM.md`
- No manual action needed - automatic during archival

---

### Step 3: Archive Project

1. **Create archive directory**: `projects/completed/YYYY-MM/[project-name]/`
2. **Move project files**: Complete project structure with full history
3. **Remove from active**: Clean up `projects/active/[project-name]/`
4. **Execute finish.sh**: Automatic pattern extraction, GitHub issue closure, worktree cleanup

---

### Step 4: Git Workflow Guidance

**Provide branch-aware options:**
- **Feature branch**: Recommend PR creation for review
- **Main branch**: Confirm direct merge readiness
- **Stay on branch**: Option to continue working

**Git workflow commands**:
```bash
# Create PR (recommended for feature branches)
gh pr create --title "Complete [project-name]" --body "[description]"

# Or merge to main
git checkout main && git merge [branch]
```

---

### Step 5: Handle Related Ideas

- **Search for source ideas**: Look for original idea that led to this project
- **Handle based on what's found**:
  - **If source idea exists**: Move to archive and update with completion status
  - **If no source idea**: Note as ad-hoc project (no idea cleanup needed)
  - **If orphaned ideas found**: Clean up any related unarchived ideas
- **Cross-reference completion**: Maintain idea → project → completion traceability
- **Clean up workflow**: Ensure no orphaned ideas remain

---

## Response Format

### Phase 1: Analysis and Proposal
```markdown
🔍 Analyzing project: [project-name]
📊 Extracting performance metrics...
[Complete analysis output as shown in Step 1.10]

🤔 **Should I proceed with these knowledge updates?**
```

### Phase 2: Execution (After Approval)
```markdown
✅ Executing approved knowledge updates...

💡 Knowledge Updates Applied:
   ✅ Updated: agents/[agent-name].md (pattern + confidence: +0.XX)
   ✅ Updated: agents/[agent-name].md (confidence: +0.XX)
   ✅ Created: .claude/memory/patterns/[new-pattern].md
   ✅ Created: knowledge/applications/[app-name]/ (three-tier docs)
   ✅ Created: .claude/skills/[skill-name]/ (automation opportunity)

📦 Archiving project...
   ✅ Moved to: projects/completed/YYYY-MM/[project-name]/
   🧹 Pattern extraction: [X] patterns saved to memory/recent/

🔀 Git workflow options:
   1. Create PR: gh pr create --title "Complete [project-name]"
   2. Merge to main: git checkout main && git merge [branch]
   3. Stay on branch: Continue working

🤖 Routing Recommendations for Future Projects:
   • For [task type]: Prefer [agent] (confidence: 0.XX)
   • For [coordination pattern]: [agent-1] + [agent-2] (proven sequence)

✅ Project '[project-name]' completed with ACE learning and skill discovery!

🎉 Next steps:
   - Review performance metrics and confidence updates
   - Review extracted knowledge and new skills
   - Create PR if on feature branch
   - Plan next project
```

---

## Knowledge Extraction Criteria

### Agent Knowledge Updates
**Update agent files when project contains:**
- New tool patterns specific to each tool
- Best practices for tool configuration/usage
- Integration patterns with other systems
- Troubleshooting insights and resolution patterns
- Performance optimizations and cost management
- Confidence adjustments based on success/failure patterns

### Technical Documentation
**Add to knowledge/ when project demonstrates:**
- **Production applications** (`knowledge/applications/<app-name>/`): New deployments or major updates
- System architecture: Novel integration or design patterns
- Process improvements: Workflow enhancements worth preserving
- Standards evolution: Updated team practices
- Cross-system coordination: Multi-tool orchestration patterns

### Pattern Confidence Evolution
**Track and update when project reveals:**
- Pattern validation (successful usage increases confidence)
- Pattern edge cases (scenarios where pattern struggles)
- Pattern supersession (better approaches discovered)
- Contextual guidance (when to use, when to avoid)

### Skill Discovery
**Create skills when analysis shows:**
- Workflow repeated 3+ times (frequency threshold)
- 15+ minutes per execution (time savings threshold)
- Clear procedural steps (automation feasibility)
- Reusable templates identified (template extraction)

### Delegation Effectiveness
**Update delegation strategy when revealing:**
- Agent effectiveness patterns (which agents excel at specific tasks)
- Coordination strategies (successful multi-agent workflows)
- Threshold optimization (adjust 0.60 threshold based on decisions)
- Token ROI measurements (cost vs business value delivered)

---

## Integration with ADLC & ACE Learning

- **ADLC Deploy Completion**: Final deployment with knowledge preservation
- **ADLC Operate Transition**: Project ready for operations with documented patterns
- **ACE Context Evolution**: Patterns, confidence scores, and skills evolve based on outcomes
- **ACE Self-Reflection**: Systematic analysis of what worked, what failed, why
- **ACE Skill Acquisition**: Automated discovery of workflows to automate
- **Cross-layer Context**: Full traceability from idea to operations with preserved learnings
- **Memory System**: Automatic pattern extraction populates `.claude/memory/recent/`
- **Confidence Routing**: Performance metrics inform future agent selection

---

## Success Criteria

- [ ] Project knowledge automatically extracted and preserved
- [ ] Performance metrics tracked and analyzed
- [ ] Agent confidence scores updated based on outcomes
- [ ] Delegation effectiveness measured (qualitative + quantitative)
- [ ] ACE self-reflection completed (approaches, errors, decisions)
- [ ] Skill discovery analysis performed (automation opportunities identified)
- [ ] Pattern confidence evolution executed (validation counts updated)
- [ ] Subagent validation completed (claude-code-expert, memory-system-expert, documentation-expert)
- [ ] Relevant agent files updated with new insights + confidence adjustments
- [ ] Technical documentation created when warranted (three-tier pattern)
- [ ] Memory system populated with patterns (automatic via finish.sh)
- [ ] Routing recommendations generated for future projects
- [ ] Project successfully archived to completed directory
- [ ] Git workflow guidance provided based on current branch
- [ ] Related ideas updated with completion status
- [ ] Clear next steps for continued development cycle

---

*ADLC project completion with ACE-enhanced continuous learning, automated skill discovery, pattern evolution, and subagent-validated knowledge extraction - from active development to operational wisdom with compound intelligence.*
