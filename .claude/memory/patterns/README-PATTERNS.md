# Pattern Files - Important Note

**Status**: Many pattern files in this directory contain examples from an internal company environment and reference components not available in the public claude-adlc-framework repository.

## What to Know

**Pattern files are examples/templates** meant to show proven approaches. They may reference:
- MCP servers not configured in this public repo (aws-mcp, snowflake-mcp, github-mcp, etc.)
- Specialist agents not included in public repo (aws-expert, business-context, etc.)
- Internal company infrastructure and workflows

## How to Use Patterns

1. **Treat as inspiration**, not exact instructions
2. **Adapt to your environment** - replace internal components with your own
3. **Focus on the pattern/approach**, not specific tools mentioned

## Which Patterns Are Accurate for Public Repo?

**Fully accurate** (reference only public repo components):
- `git-workflow-patterns.md` - Protected branch workflows
- `testing-patterns.md` - ADLC testing framework
- `knowledge-organization-strategy.md` - Agents vs Skills vs Patterns

**Contain internal examples** (adapt for your use):
- `agent-mcp-integration-guide.md` - Shows MCP integration patterns (your MCP servers will differ)
- `cross-system-analysis-patterns.md` - Cross-tool coordination (adapt tools to yours)
- `mcp-delegation-enforcement.md` - Delegation patterns (adapt specialists to yours)
- Most files in `cross-tool-integration/` - Integration examples (your tools will differ)

## For Best Results

Use the **agent and skill templates** in `.claude/agents/` to create components for YOUR specific environment and tools. The pattern files show the approach - you implement for your stack.
