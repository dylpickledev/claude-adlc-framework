# Snowflake MCP Server Integration

This document describes the integration of the official Snowflake MCP (Model Context Protocol) server into the DA Agent Hub, providing Claude with direct access to Snowflake databases and Cortex AI capabilities.

## Overview

The Snowflake MCP server enables Claude to:
- Execute SQL queries against Snowflake databases
- Access Cortex Search for unstructured data querying
- Use Cortex Analyst for structured data analysis
- Leverage Cortex Agent for agentic data retrieval
- Manage Snowflake objects (databases, schemas, tables)
- Perform secure, read-only operations with comprehensive safety controls

## Architecture

```
Claude Code ← MCP Protocol → Snowflake MCP Server ← Snowflake SDK → Snowflake Cloud
                                        ↓
                              Cortex AI Services:
                              • Cortex Search
                              • Cortex Analyst
                              • Cortex Agent
```

## Configuration

### MCP Server Configuration
The Snowflake MCP server is configured in `.claude/mcp.json`:

```json
{
  "mcpServers": {
    "snowflake-mcp": {
      "command": "uvx",
      "args": [
        "snowflake-labs-mcp",
        "--service-config-file",
        "config/snowflake_tools_config.yaml",
        "--connection-name",
        "default"
      ]
    }
  }
}
```

### Environment Variables
Required environment variables in `.env`:

```bash
# Snowflake Configuration (for MCP server integration)
SNOWFLAKE_ACCOUNT=your_snowflake_account
SNOWFLAKE_USER=your_snowflake_user
SNOWFLAKE_AUTH_METHOD=password
SNOWFLAKE_PASSWORD=your_snowflake_password
SNOWFLAKE_DATABASE=your_default_database
SNOWFLAKE_SCHEMA=your_default_schema
SNOWFLAKE_WAREHOUSE=your_default_warehouse
SNOWFLAKE_ROLE=your_default_role
```

### Authentication Methods

#### 1. Password Authentication (Default)
```bash
SNOWFLAKE_AUTH_METHOD=password
SNOWFLAKE_PASSWORD=your_password
```

#### 2. Private Key Authentication (Recommended for Production)
```bash
SNOWFLAKE_AUTH_METHOD=private_key
SNOWFLAKE_PRIVATE_KEY_PATH=/path/to/private/key.p8
SNOWFLAKE_PRIVATE_KEY_PASSPHRASE=optional_passphrase
```

#### 3. Browser Authentication (Interactive Sessions)
```bash
SNOWFLAKE_AUTH_METHOD=browser
```

## Installation

### Prerequisites
- Python 3.8+ with `uvx` package manager
- Access to Snowflake account with appropriate permissions
- Claude Code with MCP support

### Install the Snowflake MCP Server
```bash
# Install via uvx (automatic with first use)
uvx snowflake-labs-mcp --help

# Verify installation
uvx snowflake-labs-mcp --version
```

### Configure Environment
1. Copy `.env.template` to `.env`
2. Fill in your Snowflake credentials
3. Update `config/snowflake_tools_config.yaml` as needed
4. Restart Claude Code to load the new MCP server

## Features

### SQL Execution
- **Read-only queries**: SELECT, WITH, SHOW, DESCRIBE statements
- **Auto-limiting**: Automatically adds LIMIT clauses to prevent large result sets
- **Query timeout**: Configurable timeout to prevent long-running queries
- **SQL validation**: Pattern matching to block dangerous operations

### Cortex AI Integration
- **Cortex Search**: Query unstructured data using semantic search
- **Cortex Analyst**: Analyze structured data with AI-powered insights
- **Cortex Agent**: Agentic data retrieval and analysis workflows

### Object Management
- **Metadata access**: Browse databases, schemas, tables, and views
- **Schema inspection**: Examine table structures and column definitions
- **Read-only operations**: Safe exploration without modification risks

### Security Features
- **Enforced read-only mode**: Prevents any data modification
- **SQL pattern filtering**: Blocks potentially dangerous statements
- **Query logging**: Audit trail for all executed queries
- **Connection encryption**: Secure communication with Snowflake

## Usage Examples

### Basic SQL Queries
```sql
-- Query customer data
SELECT customer_id, customer_name, region
FROM dim_customers
LIMIT 100;

-- Analyze sales trends
WITH monthly_sales AS (
  SELECT
    DATE_TRUNC('month', order_date) as month,
    SUM(total_amount) as revenue
  FROM fact_orders
  GROUP BY 1
)
SELECT * FROM monthly_sales
ORDER BY month DESC;
```

### Cortex Search
```sql
-- Search documents for safety-related content
SELECT cortex_search(
  'safety_documents_search_service',
  'incident report workplace safety'
) as search_results;
```

### Schema Exploration
```sql
-- Explore available tables
SHOW TABLES IN SCHEMA analytics.marts;

-- Describe table structure
DESCRIBE TABLE dim_customers;
```

## Integration with DA Agent Hub Workflows

### Specialist Agent Coordination
The Snowflake MCP integration works seamlessly with DA Agent Hub specialist agents:

- **snowflake-expert**: Enhanced with direct database access for performance analysis
- **dbt-expert**: Can validate model outputs against actual Snowflake data
- **da-architect**: Analyzes data architecture using live schema information
- **business-context**: Validates business logic against actual data patterns

### ADLC Workflow Integration
- **Plan Phase**: Data discovery and requirement validation
- **Develop Phase**: Real-time model testing and validation
- **Test Phase**: Data quality verification and performance analysis
- **Deploy Phase**: Pre-deployment validation and impact analysis
- **Operate Phase**: Monitoring and performance optimization

## Troubleshooting

### Common Issues

#### Connection Failures
```bash
# Check network connectivity
ping your_snowflake_account.snowflakecomputing.com

# Verify credentials
uvx snowflake-labs-mcp --test-connection
```

#### Permission Errors
- Ensure the Snowflake user has appropriate role assignments
- Verify warehouse and database access permissions
- Check that the role has USAGE privileges on required schemas

#### Configuration Issues
- Validate YAML syntax in `snowflake_tools_config.yaml`
- Check environment variable names and values
- Verify file paths for private key authentication

### Debug Mode
Enable detailed logging by updating the configuration:

```yaml
logging:
  level: "DEBUG"
  log_sql: true
  log_results: false
```

## Best Practices

### Security
1. **Use service accounts**: Create dedicated users for MCP access
2. **Minimal permissions**: Grant only necessary privileges
3. **Private key auth**: Use key-pair authentication in production
4. **Regular rotation**: Rotate credentials periodically
5. **Audit logging**: Monitor query execution and access patterns

### Performance
1. **Appropriate warehouses**: Use right-sized compute resources
2. **Query optimization**: Write efficient SQL queries
3. **Result limiting**: Keep result sets reasonable
4. **Connection pooling**: Reuse connections when possible

### Development
1. **Environment separation**: Use different accounts for dev/prod
2. **Schema conventions**: Follow consistent naming patterns
3. **Documentation**: Document custom configurations
4. **Testing**: Validate queries before production use

## Advanced Configuration

### Custom Cortex Services
Configure specific Cortex services in the YAML file:

```yaml
tools:
  cortex_search:
    enabled: true
    max_results: 50
    search_services:
      - "safety_documents_search"
      - "technical_manuals_search"

  cortex_analyst:
    enabled: true
    semantic_models:
      - "customer_analytics"
      - "financial_reporting"
```

### Multi-Environment Setup
Configure multiple Snowflake connections:

```yaml
connections:
  dev:
    account: "dev-account"
    database: "DEV_DB"
    # ... other dev settings

  prod:
    account: "prod-account"
    database: "PROD_DB"
    # ... other prod settings
```

## Related Documentation

- [Snowflake MCP Server GitHub Repository](https://github.com/Snowflake-Labs/mcp)
- [DA Agent Hub MCP Integration Guide](../knowledge/da-agent-hub/development/mcp-integration.md)
- [Snowflake Expert Agent Documentation](../.claude/agents/snowflake-expert.md)
- [ADLC Development Workflow](../knowledge/da-agent-hub/development/adlc-workflow.md)

## Changelog

### 2025-09-29
- Initial Snowflake MCP integration
- Added comprehensive configuration and documentation
- Integrated with existing DA Agent Hub specialist agents
- Configured security and performance best practices