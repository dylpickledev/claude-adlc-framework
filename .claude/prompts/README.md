# Reusable Prompt Library

## Purpose
Collection of proven prompt templates for consistent, high-quality agent outputs across the team.

**Pattern**: These are reusable components that agents can reference and customize for specific tasks. Like LEGO blocks - combine them to build complex prompts.

---

## Directory Structure

```
.claude/prompts/
├── README.md (this file)
├── analysis/          # Analytical reasoning templates
│   ├── chain-of-thought.md
│   ├── root-cause-analysis.md
│   ├── impact-assessment.md
│   └── stakeholder-analysis.md
├── generation/        # Content creation templates
│   ├── documentation.md
│   ├── test-cases.md
│   ├── error-messages.md
│   └── commit-messages.md
├── evaluation/        # Quality assessment templates
│   ├── code-quality.md
│   ├── performance.md
│   ├── security.md
│   └── user-experience.md
└── orchestration/     # Multi-agent coordination templates
    ├── task-decomposition.md
    ├── parallel-coordination.md
    └── result-synthesis.md
```

---

## How to Use

### For Agents

**Reference in agent files**:
```markdown
When performing root cause analysis, use the prompt template:
`.claude/prompts/analysis/root-cause-analysis.md`
```

**Inline in task**:
```markdown
I'm using the chain-of-thought template from .claude/prompts/analysis/chain-of-thought.md:

<reasoning>
[Apply template here]
</reasoning>
```

### For Users

**Direct reference**:
```
Use the root cause analysis template to investigate the dashboard issue
```

**Combination**:
```
Combine task decomposition + parallel coordination templates to plan this migration
```

---

## Template Variables

Templates use `{{VARIABLE}}` syntax for customization:

**Example**:
```markdown
Task: {{TASK_DESCRIPTION}}
Expected Output: {{EXPECTED_OUTPUT}}
```

**Usage**:
```markdown
Task: Optimize Snowflake query performance
Expected Output: Query execution time < 5 seconds
```

---

## Template Quality Standards

Every template must include:
- **Purpose**: What problem this template solves
- **When to Use**: Specific scenarios where template applies
- **Variables**: What needs to be customized
- **Example**: Concrete usage example
- **Expected Output**: What result looks like

---

## Contributing New Templates

**Process**:
1. Use pattern successfully 3+ times
2. Extract reusable structure
3. Document in appropriate category
4. Add example usage
5. Reference in relevant agent files

**Quality Bar**:
- ✅ Proven in real projects
- ✅ Reusable across contexts
- ✅ Clear variable placeholders
- ✅ Concrete example provided
- ✅ Consistent format

---

## Template Categories Explained

### Analysis Templates
**Purpose**: Structured thinking and problem investigation

**When to Use**:
- Troubleshooting issues
- Understanding complex systems
- Making decisions
- Assessing impact

**Examples**:
- Root cause analysis (5 Whys)
- Chain-of-thought reasoning
- Stakeholder analysis

---

### Generation Templates
**Purpose**: Creating consistent, high-quality content

**When to Use**:
- Writing documentation
- Creating test cases
- Generating error messages
- Crafting commit messages

**Examples**:
- Technical documentation structure
- Test case format
- User-friendly error messages

---

### Evaluation Templates
**Purpose**: Assessing quality and identifying improvements

**When to Use**:
- Code reviews
- Performance analysis
- Security audits
- UX assessments

**Examples**:
- Code quality checklist
- Performance criteria
- Security vulnerability assessment

---

### Orchestration Templates
**Purpose**: Multi-agent coordination and synthesis

**When to Use**:
- Complex multi-specialist tasks
- Cross-domain problems
- Large-scale initiatives

**Examples**:
- Task decomposition strategy
- Parallel worker coordination
- Result synthesis approach

---

## Best Practices

### DO
- ✅ Reference templates by path for traceability
- ✅ Customize variables for specific context
- ✅ Combine templates when appropriate
- ✅ Update templates based on learnings
- ✅ Share successful patterns

### DON'T
- ❌ Copy-paste without customization
- ❌ Create template for one-time use
- ❌ Ignore template when better approach exists
- ❌ Use template blindly without understanding
- ❌ Create redundant templates

---

## Metrics & Improvement

Track template effectiveness:
- Usage frequency
- Success rate
- Time savings
- Quality improvement
- Team adoption

Update templates based on:
- Project learnings
- Agent feedback
- Pattern evolution
- New best practices

---

*This prompt library enables consistent, high-quality outputs across all agents and projects. Templates are living documents - improve them as we learn.*
