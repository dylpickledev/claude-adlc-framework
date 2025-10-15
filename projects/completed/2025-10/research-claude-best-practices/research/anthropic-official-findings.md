# Anthropic Official Best Practices - Research Findings

## Source Priority
This document captures findings from **highest-priority official Anthropic sources**:
1. Anthropic engineering blog posts
2. Claude official documentation
3. Claude Cookbook (official GitHub repository)
4. Building Effective Agents article (Schluntz & Zhang)

---

## 1. Prompt Engineering Best Practices

### Core Principles (from Anthropic Documentation)

**Treat Claude Like a New Intern**
- "Claude should be treated like an intern on their first day of the job"
- Provide clear, explicit instructions with all necessary detail
- Vague prompts leave room for misinterpretation
- Clear directives improve output quality significantly

**Optimization Hierarchy** (in order of effectiveness):
1. **Clear and Direct Communication**: System prompts should use simple, direct language at the right altitude
2. **XML Tags for Structure**: Claude is trained to recognize XML-style tags as signposts
3. **Examples (Few-Shot Prompting)**: Show clear input-output examples for nuanced/stylistic tasks
4. **Chain-of-Thought Reasoning**: Tell Claude to "think step by step" for complex queries

### Context Engineering for AI Agents

**Guiding Principle**: "Find the smallest possible set of high-signal tokens that maximize the likelihood of your desired outcome"

**Key Insights**:
- Good context engineering = smallest set of high-signal tokens
- Maximize likelihood of desired outcome
- Reduce noise, increase signal
- Token efficiency directly impacts performance

**XML Structure Benefits**:
- Acts like signposts helping model separate instructions, examples, and inputs
- Claude specifically trained to recognize XML-style tags
- Improves parsing and response accuracy

### Business Impact
- Good prompts improve outputs AND reduce deployment costs
- Combining prompt engineers with subject matter experts improves accuracy by **20%**
- On-brand customer-facing experiences through precise prompting

---

## 2. Multi-Agent Architecture Patterns (Claude Cookbook)

### Source: "Building Effective Agents" by Erik Schluntz & Barry Zhang

**Official Anthropic Definition**:
- **Workflows**: Multiple LLMs orchestrated using pre-defined patterns
- **Agents**: LLMs dynamically direct their own processes and tool usage

### Basic Building Blocks

#### 1. Prompt Chaining
**Pattern**: Decompose tasks into sequential subtasks where each step builds on previous results

**Implementation**:
```python
def chain(input: str, prompts: List[str]) -> str:
    result = input
    for prompt in prompts:
        result = llm_call(f"{prompt}\nInput: {result}")
    return result
```

**Use Cases**:
- Structured data extraction and transformation
- Multi-step data processing pipelines
- Sequential refinement tasks

**Key Learning**: Each step progressively transforms input toward desired output

#### 2. Parallelization
**Pattern**: Distribute independent subtasks across multiple LLMs for concurrent processing

**Implementation**:
```python
def parallel(prompt: str, inputs: List[str]) -> List[str]:
    with ThreadPoolExecutor(max_workers=n_workers) as executor:
        futures = [executor.submit(llm_call, f"{prompt}\nInput: {x}")
                   for x in inputs]
        return [f.result() for f in futures]
```

**Use Cases**:
- Stakeholder impact analysis across multiple groups
- Batch processing independent items
- Concurrent evaluation of multiple options

**Key Learning**: Maximum efficiency when tasks are truly independent

#### 3. Routing
**Pattern**: Dynamically select specialized LLM paths based on input characteristics

**Process**:
1. LLM classifier analyzes input with chain-of-thought
2. Selects appropriate specialized prompt/route
3. Processes input with selected specialization

**Use Cases**:
- Customer support ticket routing
- Content categorization and specialized handling
- Domain-specific response generation

**Key Learning**: Use chain-of-thought in router for better classification

### Advanced Workflows

#### 4. Orchestrator-Workers Pattern
**Pattern**: Central LLM breaks down tasks dynamically, delegates to workers, synthesizes results

**When to Use**:
- Complex tasks where subtasks can't be predicted upfront
- Flexibility needed in task decomposition
- Different from parallelization: subtasks determined by orchestrator, not pre-defined

**Architecture**:
```
Orchestrator (analyzes task)
    ↓
Generates dynamic subtasks
    ↓
Worker LLMs (execute subtasks in parallel)
    ↓
Orchestrator (synthesizes results)
```

**Key Components**:
1. **Orchestrator Prompt**: Task analysis and decomposition
2. **Worker Prompt**: Specialized execution based on task type
3. **XML Format**: Structured task definitions and results

**Example XML Structure**:
```xml
<analysis>
Orchestrator's understanding of the task
</analysis>

<tasks>
    <task>
        <type>formal</type>
        <description>Technical approach</description>
    </task>
    <task>
        <type>conversational</type>
        <description>Engaging approach</description>
    </task>
</tasks>
```

**Key Learning**:
- Orchestrator provides context and task framing
- Workers focus on specialized execution
- XML enables clear communication between components

#### 5. Evaluator-Optimizer Pattern
**Pattern**: Iterative quality assessment and improvement

**Use Cases**:
- Content refinement through feedback loops
- Quality assurance workflows
- Iterative optimization tasks

---

## 3. Tool Use and MCP Server Patterns

### Official Claude Code Best Practices

**Three Ways MCP Servers Connect**:
1. **Tools**: Functions Claude can call
2. **Resources**: Data Claude can access
3. **Prompts**: Templates Claude can use

### Slash Commands Pattern
**Official Recommendation**: Store prompt templates in `.claude/commands/` folder
- Markdown files become slash commands
- Can be checked into git for team sharing
- Enables repeatable workflows

**Example Structure**:
```
.claude/commands/
├── review-pr.md
├── analyze-code.md
└── generate-tests.md
```

### CLAUDE.md Configuration
**Highest-Impact Practice**: Master the CLAUDE.md file
- Acts as "permanent brain" for your project
- Ensures AI consistently follows guidelines
- Defines architectural patterns
- Commands and workflow instructions

---

## 4. Agent Delegation and Specialization

### Subagent Pattern (from Cookbook)
**Official Pattern**: Create specialized subagents for complex queries

**Delegation Strategy**:
1. Create specialized subagents (e.g., Asana, Slack, Google Drive, Web Search)
2. Each subagent exclusively uses specific tools
3. Delegate integration-specific research to subagents
4. Main agent conducts final analysis and synthesis

**Key Insight**: "Delegate integration-specific research to subagents and conduct final analysis yourself"

### Parallel Tool Execution
**Official Recommendation**: Invoke all relevant tools simultaneously rather than sequentially

**Benefit**: Maximum efficiency for independent operations

**Implementation Note**: Use parallel execution when operations have no dependencies

---

## 5. Quality and Correctness Standards

### Production-Ready Mindset
**From Claude Code Best Practices**:
- Treat every line of code as production-bound
- No "we'll fix it later" mentality
- Enterprise-grade error handling from the start
- Performance considerations built in

### Error Handling
**Best Practice**: Comprehensive error handling patterns
- Anticipate failure modes
- Provide graceful degradation
- Clear error messages and recovery paths

### Testing Integration
**Recommendation**: Build testing into agent workflows
- Evaluator-Optimizer pattern for quality assurance
- Automated validation where possible
- Clear success criteria

---

## 6. Context and Memory Management

### Token Optimization
**Principle**: Smallest set of high-signal tokens

**Strategies**:
1. Remove unnecessary verbosity
2. Use structured formats (XML) for parsing efficiency
3. Chain prompts to reduce context size per call
4. Parallelize to avoid sequential context bloat

### Long-Context Scenarios
**Best Practices**:
- Break large tasks into chains
- Use routing to avoid processing irrelevant context
- Orchestrator pattern to manage complex multi-step tasks
- XML tags to help model focus on relevant sections

---

## 7. Iterative Improvement Patterns

### Evaluator-Optimizer Workflow
**Pattern**:
1. Generate initial output
2. Evaluate against criteria
3. Provide specific feedback
4. Optimize based on feedback
5. Repeat until quality threshold met

**Use Cases**:
- Content refinement
- Code optimization
- Design iteration
- Quality assurance

### Continuous Learning
**Recommendation**:
- Extract patterns from successful interactions
- Document effective prompts and workflows
- Build library of proven approaches
- Share knowledge across team through git-committed patterns

---

## 8. Team Collaboration Patterns

### Git-Committed Configuration
**Official Pattern**:
- Commit `.claude/commands/` to version control
- Share successful prompts across team
- Enable consistent AI behavior across developers
- Version control for AI configurations

### Knowledge Sharing
**Best Practice**:
- Document effective agent patterns
- Share CLAUDE.md configurations
- Build team library of MCP servers
- Collaborative improvement of prompts

---

## Summary of Official Recommendations

### Top 5 Highest-Impact Practices:
1. **CLAUDE.md Mastery**: Permanent brain for consistent AI behavior
2. **XML Structure**: Use throughout for better parsing and control
3. **Orchestrator-Workers**: For complex, dynamic task decomposition
4. **Parallel Execution**: Maximize efficiency with concurrent operations
5. **Chain-of-Thought**: Enable better reasoning for complex tasks

### Agent Architecture Principles:
- Start simple: Basic patterns before complex frameworks
- Use composable patterns: Chain, Parallel, Route, Orchestrator-Workers
- Delegate strategically: Specialized subagents for domain-specific work
- Synthesize centrally: Main agent coordinates and synthesizes

### Production Readiness:
- Clear, explicit instructions (treat Claude like new intern)
- Comprehensive error handling from the start
- Quality assurance through Evaluator-Optimizer patterns
- Token efficiency through smart context engineering

---

## References
- [Building Effective Agents](https://www.anthropic.com/news/building-effective-agents) - Schluntz & Zhang
- [Claude Cookbook - Agent Patterns](https://github.com/anthropics/anthropic-cookbook/tree/main/patterns/agents)
- [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Prompt Engineering Overview](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview)
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
