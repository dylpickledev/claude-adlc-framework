# dlthub Integration Specification

## Objective
Integrate dlthub data ingestion tool into DA Agent Hub platform with full specialist agent, MCP server connectivity, and comprehensive documentation. Create reusable template for future tool integrations.

## Background
- **Tool**: dlthub (dlt+) - Python-based data ingestion platform
- **License**: Paid dlt+ license (user has access)
- **Use Case**: Replace Prefect-based data ingestion code with dlt-first approach
- **Scope**: Data ingestion layer of analytics stack

## Requirements

### 1. Specialist Agent (dlthub-expert.md)
- Follow specialist template pattern (chain-of-thought reasoning, MCP tools, quality standards)
- Core responsibilities: Pipeline development, connector configuration, schema management, incremental loading, performance optimization
- Consultation patterns: Who delegates (data-engineer, analytics-engineer, dba), common scenarios
- MCP tool integration: dlthub-mcp, snowflake-mcp, dbt-mcp, orchestra-mcp coordination
- Confidence levels: Primary expertise (≥0.85), secondary (0.60-0.84), developing (<0.60)
- Quality standards: Idempotency, incremental loading, state management, error handling, schema validation
- Documentation-first research protocol

### 2. MCP Server Configuration (.mcp.json)
- Entry: `dlthub-mcp` following dbt-mcp/orchestra-mcp pattern
- Launch: Wrapper script `scripts/launch-dlthub-mcp.sh`
- Authentication: dlt+ license key from 1Password
- Package: `dlt-plus[mcp]==0.9.0` via uv tool runner
- Environment: Inherit 1Password env vars for license

### 3. MCP Launch Script (scripts/launch-dlthub-mcp.sh)
- Pattern: Follow dbt-mcp pattern (load secrets, launch with uv)
- Command: `uv tool run --with "dlt-plus[mcp]==0.9.0" dlt mcp run`
- Secrets: Load from 1Password via ~/dotfiles/load-secrets-from-1password.sh
- Logging: Debug log to /tmp/dlthub-mcp-debug.log
- Error handling: Clean stderr filtering, proper exit codes

### 4. 1Password Configuration (~/dotfiles/load-secrets-from-1password.sh)
- Add dlt+ license key retrieval from "DA Agent Hub - dlthub" item
- Export as `DLTHUB_LICENSE_KEY` environment variable
- Cache in ~/.da-agent-hub-secrets-cache (24-hour TTL)
- Secure permissions (chmod 600)

### 5. Comprehensive Documentation (knowledge/da-agent-hub/mcp-servers/dlthub-mcp.md)
- Overview: What is dlthub MCP, what problems it solves
- Setup: Step-by-step installation and configuration
- Available Tools: Complete MCP tool inventory with examples
- Use Cases: Common scenarios with code samples
- Authentication: 1Password integration pattern
- Troubleshooting: Common issues and solutions
- Best Practices: Performance, testing, production patterns

### 6. Reusable Tool Integration Template (knowledge/da-agent-hub/templates/tool-integration-template.md)
- Overview: When to use this template
- Checklist: Step-by-step tool integration process
- Specialist Agent: How to create using specialist-template.md
- MCP Server: Configuration patterns and launch scripts
- Secrets Management: 1Password integration approach
- Documentation: Knowledge base structure and content
- Testing: Validation and health check procedures
- Example: Point to dlthub integration as reference

## Implementation Plan

### Phase 1: Specialist Agent Creation
1. Create .claude/agents/specialists/dlthub-expert.md
2. Define role, responsibilities, consultation patterns
3. Document MCP tool integration approach
4. Add confidence levels and quality standards
5. Include chain-of-thought reasoning protocol

### Phase 2: MCP Server Setup
1. Add dlthub-mcp entry to .mcp.json
2. Create scripts/launch-dlthub-mcp.sh wrapper
3. Configure 1Password secret retrieval
4. Test MCP server connection
5. Verify tools are accessible

### Phase 3: Documentation
1. Create knowledge/da-agent-hub/mcp-servers/dlthub-mcp.md
2. Document MCP tools with examples
3. Add troubleshooting guide
4. Include best practices

### Phase 4: Template Documentation
1. Create knowledge/da-agent-hub/templates/tool-integration-template.md
2. Document reusable integration process
3. Reference dlthub as working example
4. Add decision frameworks and checklists

### Phase 5: Testing & Validation
1. Test dlthub MCP server launches successfully
2. Verify specialist agent can be invoked
3. Test MCP tools are accessible and functional
4. Validate documentation accuracy
5. Run health check: ./scripts/check-mcp-health.sh

## Success Criteria
- ✅ dlthub-expert.md follows specialist template pattern completely
- ✅ dlthub-mcp appears in MCP health check as "Connected"
- ✅ MCP tools are documented and testable
- ✅ 1Password integration working (license key loaded)
- ✅ Comprehensive documentation in knowledge base
- ✅ Reusable template created for future tools
- ✅ Zero health check failures (11/11 servers connected)

## Risks & Mitigations
- **Risk**: dlt+ license key issues → Mitigation: Test 1Password retrieval early
- **Risk**: MCP server compatibility → Mitigation: Follow exact dlthub docs for version
- **Risk**: Documentation incomplete → Mitigation: Use dbt-mcp docs as quality bar

## Future Enhancements
- Add dlthub specialist to data-engineer-role delegation list
- Create example dlthub pipeline in repos/ingestion_operational
- Document dlthub vs Prefect decision framework
- Add dlthub patterns to cross-system-analysis-patterns.md
