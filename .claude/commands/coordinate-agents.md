---
description: Coordinate multiple sub-agents for complex D&A tasks
argument-hint: [task-description]
---

The **main Claude instance** is the master coordinator for D&A platform sub-agents. The main Claude's role is to orchestrate multiple specialist agents while ensuring each works autonomously within their expertise.

## Available Sub-Agents

Each agent works **independently** and writes to their own directory in `.claude/tasks/`:

- **business-context**: Business requirements, stakeholder analysis, process documentation
- **dbt-expert**: SQL transformations, data modeling, dbt testing and optimization  
- **tableau-expert**: Dashboard performance, visualization optimization, reporting analysis
- **snowflake-expert**: Query optimization, cost analysis, warehouse configuration
- **orchestra-expert**: Pipeline orchestration, workflow scheduling, integration patterns
- **dlthub-expert**: Data ingestion, source connectivity, connector configuration

## Coordination Strategy

### 1. Task Assignment Pattern
For complex tasks that span multiple domains:

1. **Start with business-context** (if business requirements unclear)
2. **Assign technical specialists** based on the core systems involved
3. **Let agents work autonomously** - they don't coordinate with each other
4. **Review each agent's findings** in their respective directories
5. **Synthesize recommendations** and create implementation plan

### 2. Agent Invocation (Main Claude Only)
The main Claude instance uses the sub-agent system correctly:
- Invoke agents using Claude's built-in sub-agent mechanism 
- **Never** let agents try `claude --agent` commands (they don't have CLI access)
- **Never** tell agents to coordinate with each other directly
- Each agent reads the shared `current-task.md` and works independently

### 3. File-Based Communication
- **Shared Context**: All agents read `.claude/tasks/current-task.md`
- **Individual Findings**: Each agent writes to `.claude/tasks/{agent-name}/`
- **Cross-Reference**: Agents can read others' findings but never modify them
- **Your Role**: Review all agent directories and synthesize results

### 4. Common Multi-Agent Workflows

**Data Quality Investigation:**
```
1. business-context → understand business impact and requirements
2. dbt-expert → analyze model structure and test failures  
3. snowflake-expert → check query performance and data volumes
4. Synthesize → combine findings into root cause and fix plan
```

**Dashboard Performance Issue:**
```
1. tableau-expert → analyze dashboard and visualization performance
2. dbt-expert → review underlying model performance 
3. snowflake-expert → optimize database queries and configuration
4. Synthesize → create coordinated optimization plan
```

**New Data Source Integration:**
```
1. business-context → gather requirements and stakeholder priorities
2. dlthub-expert → design ingestion pipeline and connectors
3. dbt-expert → plan data modeling and transformations
4. orchestra-expert → design workflow orchestration
5. Synthesize → create integrated implementation plan
```

## Main Claude's Coordination Tasks

Based on the task provided, the main Claude instance should:

1. **Analyze the task scope** - determine which agents are needed
2. **Set up shared context** - write clear task description to `current-task.md`  
3. **Invoke appropriate agents** - use Claude's sub-agent system to assign work
4. **Monitor progress** - check each agent's directory for findings
5. **Synthesize results** - combine agent findings into coherent plan
6. **Execute implementations** - carry out the changes agents recommend
7. **Run validation tests** - execute the testing procedures agents specify
8. **Report results** - provide user with implemented solutions and test outcomes

## Task Execution

Execute the coordination strategy for: **$ARGUMENTS**

Create the shared task context, invoke the appropriate sub-agents, and synthesize their autonomous findings into a cohesive solution.