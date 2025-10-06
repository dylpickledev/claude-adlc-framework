# Specialist-MCP Integration Plan
**Research Date**: 2025-10-05
**Foundation**: Based on comprehensive MCP server catalog and Anthropic guidance
**Architecture**: Role → Specialist (with MCP tools) pattern

---

## Executive Summary

This plan maps each specialist agent to relevant MCP servers, following Anthropic's recommended pattern where **specialists use MCP tools with domain expertise** rather than roles using MCP tools directly.

### Key Principles (from Anthropic Research):
1. **MCP provides DATA ACCESS** - retrieve information, query state, access documentation
2. **Specialists provide EXPERTISE** - synthesize decisions, apply patterns, reason about trade-offs
3. **Recommended Pattern**: Role → Specialist (specialist uses MCP) for correctness
4. **Tools WITH Expertise** = Informed decisions | Tools WITHOUT Expertise = Guessing

### Integration Summary:
- **10 Active Specialists** with MCP tool assignments
- **15 Deprecated Specialists** - 6 recommended for revival with MCP enhancement
- **8 New MCP Servers** recommended for immediate integration
- **4 Custom MCP Servers** needed for gaps (Orchestra, Prefect, Great Expectations, Tableau Enhanced)

---

## 1. Active Specialist MCP Mappings

### 1.1 dbt-expert (Transformation Specialist)

**Current Status**: Active specialist
**Location**: `.claude/agents/deprecated/dbt-expert.md`
**Recommendation**: REVIVE and enhance with MCP integration

#### Assigned MCP Servers:
1. **dbt MCP** (CRITICAL - Already Configured)
   - Tools: Project context, model metadata, test execution, documentation generation, lineage
   - Use Cases:
     - Model development assistance
     - Test generation and validation
     - Documentation automation
     - Lineage analysis and impact assessment
     - Debugging transformation logic

2. **Snowflake MCP** (Supporting)
   - Tools: SQL execution, query optimization, warehouse metadata
   - Use Cases:
     - Query performance analysis
     - Cost optimization for transformations
     - Warehouse-specific SQL features

3. **Git MCP** (Supporting)
   - Tools: Repository analysis, code search, commit history
   - Use Cases:
     - Model version analysis
     - Pattern discovery across projects
     - Historical change tracking

#### Integration Pattern:
```
analytics-engineer-role
    ↓ (recognizes dbt complexity)
dbt-expert (specialist)
    ├─ Uses dbt-mcp → Model metadata, test execution, lineage
    ├─ Uses snowflake-mcp → Query optimization, cost analysis
    ├─ Uses git-mcp → Pattern discovery, version analysis
    ├─ Applies transformation expertise
    └─ Returns validated dbt implementation plan
```

#### Quality Standards:
- Model follows dimensional modeling best practices
- Tests cover all critical business logic
- Performance meets SLA requirements (<5 min for incremental)
- Documentation includes business context and lineage
- Cost optimized for warehouse usage

---

### 1.2 snowflake-expert (Warehouse Specialist)

**Current Status**: Active specialist
**Location**: `.claude/agents/deprecated/snowflake-expert.md`
**Recommendation**: REVIVE and enhance with MCP integration

#### Assigned MCP Servers:
1. **Snowflake MCP** (CRITICAL - Already Configured)
   - Tools: Cortex Search, Cortex Analyst, SQL execution, object management, semantic views
   - Use Cases:
     - Query optimization and performance tuning
     - Cost analysis via warehouse metadata
     - Schema design and object management
     - Semantic model querying
     - Data quality validation

2. **dbt MCP** (Supporting)
   - Tools: Model metadata, compilation output
   - Use Cases:
     - Understanding dbt-generated SQL
     - Optimization recommendations for dbt models
     - Warehouse-specific feature suggestions

3. **Sequential Thinking MCP** (Supporting)
   - Tools: Complex problem decomposition
   - Use Cases:
     - Multi-step query optimization
     - Root cause analysis for performance issues
     - Cost anomaly investigation

#### Integration Pattern:
```
analytics-engineer-role / data-engineer-role
    ↓ (recognizes Snowflake complexity)
snowflake-expert (specialist)
    ├─ Uses snowflake-mcp → Query metadata, warehouse stats, Cortex AI
    ├─ Uses dbt-mcp → Model compilation analysis
    ├─ Uses sequential-thinking-mcp → Complex optimization reasoning
    ├─ Applies warehouse expertise
    └─ Returns optimized configuration and queries
```

#### Quality Standards:
- Queries optimized for Snowflake query engine
- Warehouse sizing appropriate for workload
- Clustering keys applied for large tables
- Cost per query under budget thresholds
- Materialization strategy optimized

---

### 1.3 tableau-expert (BI Specialist)

**Current Status**: Active specialist
**Location**: `.claude/agents/deprecated/tableau-expert.md`
**Recommendation**: REVIVE and enhance with MCP + file parsing

#### Assigned MCP Servers:
1. **Tableau MCP** (When Enhanced - Currently Basic)
   - Tools: Dashboard metadata, data source queries
   - Use Cases:
     - Dashboard performance analysis
     - Data source optimization
     - Usage pattern analysis

2. **Snowflake MCP** (Primary for Data Source Analysis)
   - Tools: Query execution, performance metadata
   - Use Cases:
     - Analyzing Tableau data source queries
     - Optimizing extract vs. live connections
     - Warehouse impact of dashboard loads

3. **dbt MCP** (Supporting)
   - Tools: Semantic layer models
   - Use Cases:
     - Identifying optimal mart models for dashboards
     - Ensuring dashboard uses certified datasets

4. **Filesystem MCP** (Current Primary Method)
   - Tools: File operations for .twb/.twbx parsing
   - Use Cases:
     - Parsing Tableau workbook XML
     - Analyzing calculated fields
     - Extracting data source definitions

#### Integration Pattern:
```
bi-developer-role
    ↓ (recognizes Tableau complexity)
tableau-expert (specialist)
    ├─ Uses filesystem-mcp → Parse .twb/.twbx files
    ├─ Uses snowflake-mcp → Analyze data source queries
    ├─ Uses dbt-mcp → Validate semantic layer usage
    ├─ Uses tableau-mcp → Dashboard metadata (when available)
    ├─ Applies BI visualization expertise
    └─ Returns dashboard optimization recommendations
```

#### Quality Standards:
- Dashboard load time <3 seconds
- Data sources use certified mart models
- Extract refresh schedules optimized
- Calculated fields performant
- User experience follows best practices

---

### 1.4 orchestra-expert (Workflow Orchestration Specialist)

**Current Status**: Active specialist
**Location**: `.claude/agents/deprecated/orchestra-expert.md`
**Recommendation**: REVIVE and create custom Orchestra MCP server

#### Assigned MCP Servers:
1. **Orchestra MCP** (CRITICAL - Custom Development Needed)
   - Proposed Tools:
     - `list_workflows`: Get all workflow definitions
     - `get_workflow_status`: Current execution state
     - `get_workflow_history`: Execution history and logs
     - `trigger_workflow`: Manual workflow execution
     - `get_dependencies`: DAG visualization
     - `analyze_performance`: Workflow timing analysis
   - Use Cases:
     - Workflow orchestration debugging
     - Dependency analysis
     - Performance optimization
     - Failure investigation

2. **Prefect MCP** (Supporting - Custom Development Needed)
   - Proposed Tools: Flow metadata, execution logs, task analysis
   - Use Cases: Prefect flow performance when Orchestra triggers them

3. **Airbyte MCP** (Supporting - Available)
   - Tools: Pipeline metadata, connector configuration
   - Use Cases: Ingestion pipeline orchestrated by Orchestra

4. **dbt MCP** (Supporting)
   - Tools: Job metadata, run history
   - Use Cases: dbt job orchestration via Orchestra

5. **Slack MCP** (Notification)
   - Tools: Message posting, channel management
   - Use Cases: Workflow failure notifications

#### Integration Pattern:
```
data-engineer-role
    ↓ (recognizes orchestration complexity)
orchestra-expert (specialist)
    ├─ Uses orchestra-mcp → Workflow metadata, dependencies, performance
    ├─ Uses prefect-mcp → Prefect flow analysis (when triggered)
    ├─ Uses airbyte-mcp → Ingestion pipeline status
    ├─ Uses dbt-mcp → Transformation job status
    ├─ Uses slack-mcp → Alert team on failures
    ├─ Applies orchestration expertise
    └─ Returns workflow optimization and debugging plan
```

#### Quality Standards:
- Workflows complete within SLA windows
- Dependencies correctly defined (no circular)
- Failure handling and retries configured
- Resource allocation optimized
- Monitoring and alerting in place

**CRITICAL GAP**: Orchestra MCP server must be developed for full integration

---

### 1.5 prefect-expert (Python Workflow Specialist)

**Current Status**: Active specialist
**Location**: `.claude/agents/deprecated/prefect-expert.md`
**Recommendation**: REVIVE and create custom Prefect MCP server

#### Assigned MCP Servers:
1. **Prefect MCP** (CRITICAL - Custom Development Needed)
   - Proposed Tools:
     - `list_flows`: All flow definitions
     - `get_flow_runs`: Execution history
     - `get_task_runs`: Task-level details
     - `analyze_performance`: Flow performance metrics
     - `get_logs`: Detailed execution logs
   - Use Cases:
     - Flow debugging and optimization
     - Task failure analysis
     - Performance tuning
     - Resource optimization

2. **Orchestra MCP** (Coordination)
   - Tools: Workflow metadata (when Prefect called by Orchestra)
   - Use Cases: Understanding upstream/downstream dependencies

3. **Python-specific MCP** (If Available)
   - Tools: Code analysis, dependency tracking
   - Use Cases: Flow code quality analysis

#### Integration Pattern:
```
data-engineer-role
    ↓ (recognizes Prefect flow complexity)
prefect-expert (specialist)
    ├─ Uses prefect-mcp → Flow metadata, task analysis, performance
    ├─ Uses orchestra-mcp → Orchestration context
    ├─ Applies Python workflow expertise
    └─ Returns optimized flow implementation
```

#### Quality Standards:
- Flows idempotent and retryable
- Task granularity optimized
- Resource allocation appropriate
- Error handling comprehensive
- Logging and monitoring in place

**CRITICAL GAP**: Prefect MCP server must be developed

---

### 1.6 dlthub-expert (Data Ingestion Specialist)

**Current Status**: Active specialist
**Location**: `.claude/agents/deprecated/dlthub-expert.md`
**Recommendation**: REVIVE and enhance with Airbyte MCP integration

#### Assigned MCP Servers:
1. **Airbyte MCP** (Primary - Available)
   - Tools: Connector metadata, pipeline code generation, documentation access
   - Use Cases:
     - Source connector setup
     - Pipeline scaffolding
     - Configuration assistance
     - Error handling patterns

2. **Snowflake MCP** (Destination)
   - Tools: Loading strategies, staging tables, warehouse management
   - Use Cases:
     - Destination configuration
     - Data validation
     - Performance optimization

3. **Orchestra MCP** (Orchestration)
   - Tools: Workflow scheduling, dependency management
   - Use Cases: Pipeline orchestration coordination

#### Integration Pattern:
```
data-engineer-role
    ↓ (recognizes ingestion complexity)
dlthub-expert (specialist)
    ├─ Uses airbyte-mcp → Connector setup, code generation
    ├─ Uses snowflake-mcp → Destination optimization
    ├─ Uses orchestra-mcp → Orchestration coordination
    ├─ Applies ingestion expertise
    └─ Returns complete ingestion pipeline
```

#### Quality Standards:
- Source connectors configured correctly
- Incremental loading optimized
- Error handling and retries robust
- Data quality validation at ingestion
- Performance meets SLA requirements

---

### 1.7 aws-expert (Cloud Infrastructure Specialist)

**Current Status**: Active specialist
**Location**: `.claude/agents/aws-expert.md`
**Recommendation**: ENHANCE with full MCP suite

#### Assigned MCP Servers:
1. **AWS API MCP** (CRITICAL - Already Configured)
   - Tools: All AWS service APIs, infrastructure state queries
   - Use Cases:
     - ECS task definition analysis
     - S3 bucket management
     - IAM policy validation
     - CloudWatch metrics
     - Cost Explorer data

2. **AWS Knowledge MCP** (CRITICAL - Already Configured)
   - Tools: Documentation search, best practices, regional availability
   - Use Cases:
     - Architectural guidance
     - Service selection recommendations
     - Best practice validation
     - Cost optimization strategies

3. **AWS Documentation MCP** (CRITICAL - Already Configured)
   - Tools: Latest docs, API references, What's New, blogs, Well-Architected
   - Use Cases:
     - Latest feature discovery
     - Migration guidance
     - Architecture pattern research

4. **AWS Cloud Control MCP** (Recommended Addition)
   - Tools: Resource CRUD operations
   - Use Cases: Infrastructure automation, IaC implementation

#### Integration Pattern:
```
ui-ux-developer-role / cloud-manager-role
    ↓ (recognizes AWS infrastructure need)
aws-expert (specialist)
    ├─ Uses aws-api-mcp → Infrastructure state, service queries
    ├─ Uses aws-knowledge-mcp → Best practices, recommendations
    ├─ Uses aws-docs-mcp → Latest documentation, patterns
    ├─ Applies AWS architecture expertise
    └─ Returns validated deployment strategy
```

#### Quality Standards:
- Architecture follows AWS Well-Architected Framework
- Security configurations meet best practices
- Cost optimized for workload
- Performance meets SLA requirements
- Disaster recovery and backup configured

---

### 1.8 github-sleuth-expert (Repository Analysis Specialist)

**Current Status**: Active specialist
**Location**: `.claude/agents/deprecated/github-sleuth-expert.md`
**Recommendation**: REVIVE and enhance with GitHub MCP

#### Assigned MCP Servers:
1. **GitHub MCP** (CRITICAL - Recommended Addition)
   - Tools: Repository management, issue tracking, PR operations, code search
   - Use Cases:
     - PR review and analysis
     - Issue tracking integration
     - Code pattern discovery
     - Workflow automation

2. **Git MCP** (Supporting)
   - Tools: Repository analysis, code search, commit history
   - Use Cases:
     - Local repository analysis
     - Pattern discovery
     - Change history tracking

3. **Filesystem MCP** (Supporting)
   - Tools: File operations
   - Use Cases: Repository file analysis

#### Integration Pattern:
```
project-manager-role
    ↓ (recognizes GitHub investigation need)
github-sleuth-expert (specialist)
    ├─ Uses github-mcp → PR analysis, issue tracking, workflow automation
    ├─ Uses git-mcp → Repository analysis, pattern discovery
    ├─ Uses filesystem-mcp → File-level analysis
    ├─ Applies repository investigation expertise
    └─ Returns comprehensive analysis and recommendations
```

#### Quality Standards:
- PR reviews thorough and actionable
- Issue tracking accurate and up-to-date
- Code patterns align with best practices
- Workflow automation optimized
- Repository health monitored

---

### 1.9 documentation-expert (Documentation Specialist)

**Current Status**: Active specialist
**Location**: `.claude/agents/deprecated/documentation-expert.md`
**Recommendation**: ENHANCE with documentation MCP servers

#### Assigned MCP Servers:
1. **Confluence MCP** (HIGH PRIORITY - Recommended Addition)
   - Tools: Space/page listing, Markdown content, CQL search, page CRUD
   - Use Cases:
     - Technical documentation access
     - Runbook retrieval
     - Process documentation
     - Knowledge base updates

2. **Notion MCP** (Alternative/Supplementary)
   - Tools: Markdown API, page/database operations
   - Use Cases: Alternative documentation platform

3. **dbt MCP** (Domain-Specific)
   - Tools: Model documentation, lineage documentation
   - Use Cases: Data model documentation

4. **GitHub MCP** (Supporting)
   - Tools: README updates, wiki management
   - Use Cases: Code repository documentation

#### Integration Pattern:
```
analytics-engineer-role / project-manager-role
    ↓ (recognizes documentation need)
documentation-expert (specialist)
    ├─ Uses confluence-mcp → Knowledge base access, updates
    ├─ Uses dbt-mcp → Data model documentation
    ├─ Uses github-mcp → Repository documentation
    ├─ Applies documentation expertise
    └─ Returns comprehensive, accessible documentation
```

#### Quality Standards:
- Documentation accurate and up-to-date
- Follows GraniteRock standards
- Accessible to target audience
- Searchable and well-organized
- Includes examples and context

---

### 1.10 business-context (Business Requirements Specialist)

**Current Status**: Active specialist
**Location**: `.claude/agents/deprecated/business-context.md`
**Recommendation**: ENHANCE with project management MCP servers

#### Assigned MCP Servers:
1. **Atlassian MCP** (Jira + Confluence) (HIGH PRIORITY)
   - Tools: Issue tracking, project management, wiki access
   - Use Cases:
     - Stakeholder requirements gathering
     - Sprint planning integration
     - User story analysis
     - Business process documentation

2. **Slack MCP** (Communication)
   - Tools: Message history, channel context
   - Use Cases:
     - Stakeholder communication analysis
     - Requirements clarification
     - Feedback collection

3. **dbt MCP** (Semantic Layer)
   - Tools: Metric definitions, semantic models
   - Use Cases: Business metric validation

#### Integration Pattern:
```
analytics-engineer-role
    ↓ (recognizes business requirement complexity)
business-context (specialist)
    ├─ Uses atlassian-mcp → User stories, requirements, documentation
    ├─ Uses slack-mcp → Stakeholder communication context
    ├─ Uses dbt-mcp → Metric definition validation
    ├─ Applies business analysis expertise
    └─ Returns validated business requirements
```

#### Quality Standards:
- Requirements clear and measurable
- Stakeholder alignment documented
- Business logic validated
- Metrics defined accurately
- Success criteria established

---

## 2. Deprecated Specialists - Revival Recommendations

### 2.1 REVIVE with MCP Enhancement (High Priority)

#### 2.1.1 da-architect (Data Architecture Specialist)
**Current Status**: Deprecated
**Recommendation**: REVIVE - Critical for system design decisions

**Assigned MCP Servers**:
- AWS MCP Suite (infrastructure architecture)
- Snowflake MCP (warehouse architecture)
- dbt MCP (transformation architecture)
- Sequential Thinking MCP (complex design reasoning)
- BigQuery/Azure MCP (multi-cloud architecture)

**Revival Rationale**: System-level design decisions require architectural expertise that benefits from comprehensive MCP tool access

#### 2.1.2 qa-coordinator (Quality Assurance Specialist)
**Current Status**: Deprecated (custom subagent definition exists)
**Recommendation**: REVIVE as proper specialist with MCP integration

**Assigned MCP Servers**:
- dbt MCP (test validation)
- Snowflake MCP (data quality checks)
- Great Expectations MCP (when developed)
- GitHub MCP (test automation workflows)

**Revival Rationale**: Comprehensive testing requires specialist coordination with quality-focused MCP tools

### 2.2 REVIVE with Limited MCP (Medium Priority)

#### 2.2.1 react-expert (Frontend Development Specialist)
**Current Status**: Deprecated
**Recommendation**: REVIVE for UI development projects

**Assigned MCP Servers**:
- GitHub MCP (code repository management)
- Git MCP (version control)
- Filesystem MCP (component file management)
- AWS MCP (deployment to S3/CloudFront)

#### 2.2.2 streamlit-expert (Data App Specialist)
**Current Status**: Deprecated
**Recommendation**: REVIVE for internal data applications

**Assigned MCP Servers**:
- Snowflake MCP (data source queries)
- dbt MCP (semantic layer access)
- GitHub MCP (app repository)

#### 2.2.3 ui-ux-expert (Design Specialist)
**Current Status**: Deprecated
**Recommendation**: REVIVE for design-focused projects

**Assigned MCP Servers**:
- Filesystem MCP (design asset management)
- GitHub MCP (design system repository)
- Notion/Confluence MCP (design documentation)

### 2.3 KEEP DEPRECATED (Low Priority)

#### 2.3.1 project-delivery-expert
**Status**: Deprecated
**Recommendation**: Keep deprecated - functionality covered by project-manager-role with Atlassian MCP

#### 2.3.2 issue-lifecycle-expert
**Status**: Deprecated
**Recommendation**: Keep deprecated - functionality covered by github-sleuth-expert with GitHub MCP

---

## 3. New Specialist Opportunities with MCP

### 3.1 cost-optimization-specialist (NEW)
**Rationale**: Cost analysis spans multiple platforms (AWS, Snowflake, dbt Cloud)

**Assigned MCP Servers**:
- AWS API MCP → Cost Explorer data, resource utilization
- AWS Knowledge MCP → Cost optimization best practices
- Snowflake MCP → Warehouse cost analysis, query performance
- dbt MCP → Model execution costs
- Sequential Thinking MCP → Complex cost trade-off analysis

**Use Cases**:
- Multi-platform cost analysis
- Resource optimization recommendations
- Budget forecasting
- Cost anomaly investigation

### 3.2 data-quality-specialist (NEW)
**Rationale**: Data quality testing requires specialized focus

**Assigned MCP Servers**:
- Great Expectations MCP (when developed)
- dbt MCP → Test execution and results
- Snowflake MCP → Data profiling queries
- Airbyte MCP → Ingestion quality checks

**Use Cases**:
- Comprehensive data quality framework
- Test generation and validation
- Data profiling and anomaly detection
- Quality SLA monitoring

### 3.3 multi-cloud-specialist (NEW - If Needed)
**Rationale**: Multi-cloud strategy requires cross-platform expertise

**Assigned MCP Servers**:
- AWS MCP Suite → AWS infrastructure
- Azure MCP → Azure resources (if using)
- BigQuery MCP → GCP analytics (if using)
- Sequential Thinking MCP → Cross-cloud architecture reasoning

**Use Cases**:
- Multi-cloud architecture design
- Cloud migration planning
- Cross-platform optimization
- Vendor comparison analysis

---

## 4. MCP Server Development Priorities

### 4.1 CRITICAL - Build Immediately
1. **Orchestra MCP Server**
   - Reason: Core orchestration platform, no alternative exists
   - Impact: Enables orchestra-expert full functionality
   - Effort: Medium (REST API integration)

2. **Prefect MCP Server**
   - Reason: Python workflow automation critical
   - Impact: Enables prefect-expert full functionality
   - Effort: Medium (Prefect API integration)

### 4.2 HIGH - Build Next Quarter
3. **Great Expectations MCP Server**
   - Reason: Data quality testing framework
   - Impact: Enables comprehensive quality validation
   - Effort: Medium-High (Python library integration)

4. **Tableau Enhanced MCP Server**
   - Reason: Current Tableau MCP has limited functionality
   - Impact: Full BI optimization capabilities
   - Effort: High (Complex Tableau API/XML parsing)

### 4.3 MEDIUM - Future Consideration
5. **Airflow MCP Server** (if needed)
6. **Dagster MCP Server** (if needed)
7. **dbt-expectations MCP Server** (testing framework)

---

## 5. Integration Implementation Roadmap

### Phase 1: Foundation (Weeks 1-2)
**Goal**: Revive core specialists with existing MCP servers

**Actions**:
1. Revive dbt-expert with dbt MCP integration
2. Revive snowflake-expert with Snowflake MCP integration
3. Enhance aws-expert with full AWS MCP suite
4. Add GitHub MCP server
5. Add Slack MCP server
6. Test integration patterns

**Success Metrics**:
- 3 specialists operational with MCP tools
- GitHub MCP integrated
- Slack MCP integrated
- Role → Specialist delegation working

### Phase 2: Orchestration & Pipelines (Weeks 3-4)
**Goal**: Enable workflow orchestration specialists

**Actions**:
1. Develop Orchestra MCP server (CRITICAL)
2. Develop Prefect MCP server (CRITICAL)
3. Revive orchestra-expert with new MCP
4. Revive prefect-expert with new MCP
5. Enhance dlthub-expert with Airbyte MCP
6. Add Airbyte MCP server

**Success Metrics**:
- Orchestra MCP operational
- Prefect MCP operational
- 3 additional specialists operational
- Pipeline debugging workflows functional

### Phase 3: BI & Documentation (Weeks 5-6)
**Goal**: Enable BI and documentation specialists

**Actions**:
1. Revive tableau-expert with Tableau MCP + file parsing
2. Revive documentation-expert with Confluence MCP
3. Enhance business-context with Atlassian MCP
4. Add Atlassian MCP server
5. Add Filesystem MCP server
6. Add Git MCP server

**Success Metrics**:
- Tableau analysis functional
- Documentation access automated
- Business context integration working
- 3 additional specialists operational

### Phase 4: Advanced Capabilities (Weeks 7-8)
**Goal**: Add advanced reasoning and quality specialists

**Actions**:
1. Revive github-sleuth-expert with GitHub MCP
2. Revive qa-coordinator with testing MCP suite
3. Develop Great Expectations MCP (start)
4. Add Sequential Thinking MCP
5. Add Time MCP
6. Add Memory MCP

**Success Metrics**:
- Repository analysis enhanced
- QA coordination operational
- Advanced reasoning available
- All core specialists operational with MCP

### Phase 5: Specialized & New (Weeks 9-12)
**Goal**: Add specialized and new capabilities

**Actions**:
1. Revive react-expert, streamlit-expert, ui-ux-expert
2. Create cost-optimization-specialist
3. Create data-quality-specialist (with Great Expectations MCP)
4. Evaluate multi-cloud-specialist need
5. Complete Tableau Enhanced MCP development
6. Add any remaining Phase 3 MCP servers

**Success Metrics**:
- All revival specialists operational
- 2 new specialists created
- Enhanced MCP servers functional
- Complete MCP suite integrated

---

## 6. Quality Standards & Validation Patterns

### 6.1 Specialist MCP Usage Validation

For each specialist + MCP integration, validate:

**Correctness Framework**:
1. **Tool Selection** - Specialist uses appropriate MCP tools
2. **Data Interpretation** - Specialist correctly interprets MCP responses
3. **Pattern Application** - Specialist applies domain expertise to MCP data
4. **Decision Quality** - Specialist makes informed recommendations
5. **Error Prevention** - Specialist identifies and prevents issues

**Example (dbt-expert with dbt MCP)**:
- ✅ Uses dbt MCP to get model metadata
- ✅ Interprets schema information correctly
- ✅ Applies dimensional modeling patterns
- ✅ Recommends optimal incremental strategy
- ✅ Identifies potential performance issues before deployment

### 6.2 Integration Testing Protocol

**Test Cases for Each Specialist**:
1. **Tool Access** - Specialist can successfully call MCP tools
2. **Error Handling** - Specialist handles MCP errors gracefully
3. **Multi-Tool Coordination** - Specialist uses multiple MCP tools in parallel
4. **Context Preservation** - Specialist maintains context across tool calls
5. **Quality Output** - Specialist produces correct, actionable recommendations

**Example Test (snowflake-expert)**:
```
Given: Slow-running dbt model
When: analytics-engineer-role delegates to snowflake-expert
Then:
  - Specialist uses dbt-mcp to get compiled SQL
  - Specialist uses snowflake-mcp to analyze query plan
  - Specialist uses sequential-thinking-mcp for optimization reasoning
  - Specialist returns specific optimization recommendations
  - Recommendations are correct and implementable
```

### 6.3 Performance Metrics

**Track for Each Specialist**:
- **MCP Tool Usage**: Which tools used, frequency, success rate
- **Delegation Frequency**: How often role delegates to specialist
- **Success Rate**: % of specialist recommendations that are correct
- **Time to Resolution**: Average time from delegation to resolution
- **User Satisfaction**: Quality ratings from role agents

---

## 7. Configuration Examples

### 7.1 Complete MCP Configuration for DA Hub

```json
{
  "mcpServers": {
    "dbt-mcp": {
      "command": "uvx",
      "args": ["--env-file", ".env", "dbt-mcp"],
      "disabled": false,
      "autoApprove": ["read", "compile", "test"]
    },
    "snowflake-mcp": {
      "command": "uvx",
      "args": [
        "snowflake-labs-mcp",
        "--service-config-file",
        "config/snowflake_tools_config.yaml",
        "--connection-name",
        "default"
      ],
      "disabled": false,
      "autoApprove": ["read", "query"]
    },
    "aws-api": {
      "command": "uvx",
      "args": ["awslabs.aws-api-mcp-server@latest"],
      "env": {
        "AWS_REGION": "us-west-2",
        "AWS_PROFILE": "default",
        "READ_OPERATIONS_ONLY": "true"
      },
      "disabled": false,
      "autoApprove": ["list", "describe", "get"]
    },
    "aws-knowledge": {
      "command": "uvx",
      "args": ["awslabs.aws-knowledge-mcp-server@latest"],
      "disabled": false,
      "autoApprove": ["search", "read", "recommend"]
    },
    "aws-docs": {
      "command": "uvx",
      "args": ["awslabs.aws-documentation-mcp-server@latest"],
      "disabled": false,
      "autoApprove": ["read"]
    },
    "github": {
      "command": "claude",
      "args": ["mcp", "add", "--transport", "sse", "github", "https://mcp.github.com/sse"],
      "disabled": false,
      "autoApprove": ["read", "list"]
    },
    "airbyte": {
      "command": "remote",
      "url": "https://airbyte-mcp.herokuapp.com",
      "disabled": false,
      "autoApprove": ["read", "generate"]
    },
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}",
        "SLACK_TEAM_ID": "${SLACK_TEAM_ID}"
      },
      "disabled": false,
      "autoApprove": ["read", "post_message"]
    },
    "atlassian": {
      "command": "claude",
      "args": ["mcp", "add", "--transport", "sse", "atlassian", "https://mcp.atlassian.com/v1/sse"],
      "disabled": false,
      "autoApprove": ["read", "search"]
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/TehFiestyGoat/da-agent-hub"],
      "disabled": false,
      "autoApprove": ["read"]
    },
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git"],
      "disabled": false,
      "autoApprove": ["read", "search", "log"]
    },
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"],
      "disabled": false,
      "autoApprove": ["think"]
    },
    "time": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-time"],
      "disabled": false,
      "autoApprove": ["convert", "now"]
    }
  }
}
```

### 7.2 Specialist Tool Assignments (in specialist.md files)

**Example: dbt-expert.md enhancement**
```markdown
## MCP Tool Access

### Primary MCP Tools
- **dbt-mcp**: Model metadata, test execution, documentation, lineage
- **snowflake-mcp**: Query optimization, warehouse metadata
- **git-mcp**: Repository analysis, pattern discovery

### Tool Usage Patterns
1. **Model Development**:
   - Use dbt-mcp to get current model metadata
   - Use git-mcp to find similar model patterns
   - Apply transformation expertise
   - Use snowflake-mcp to validate query performance

2. **Test Generation**:
   - Use dbt-mcp to analyze model schema
   - Use dbt-mcp to check existing tests
   - Generate comprehensive test suite
   - Use dbt-mcp to execute and validate

3. **Debugging**:
   - Use dbt-mcp to get compilation errors
   - Use snowflake-mcp to analyze query execution
   - Use sequential-thinking-mcp for complex issues
   - Apply debugging expertise
```

---

## 8. Success Criteria

### 8.1 Integration Success Metrics

**Technical Success**:
- ✅ All critical MCP servers integrated (8 servers in Phase 1)
- ✅ All core specialists revived with MCP tools (6 specialists)
- ✅ Custom MCP servers developed (Orchestra, Prefect)
- ✅ Role → Specialist delegation pattern working
- ✅ MCP tool usage tracked and optimized

**Quality Success**:
- ✅ Specialist recommendations 90%+ correct (validated by users)
- ✅ Time to resolution reduced 50% (vs. manual analysis)
- ✅ User satisfaction 85%+ (role agents rating specialists)
- ✅ Error prevention improved (issues caught before deployment)

**Business Success**:
- ✅ Faster project delivery (specialists with MCP accelerate work)
- ✅ Higher quality outputs (specialists + MCP = better decisions)
- ✅ Reduced operational incidents (proactive issue detection)
- ✅ Team learning accelerated (specialists share expertise via MCP)

### 8.2 Validation Checkpoints

**Week 2**: Core specialists operational
**Week 4**: Orchestration specialists operational
**Week 6**: BI and documentation specialists operational
**Week 8**: All core specialists operational with MCP
**Week 12**: Specialized and new specialists operational

---

**Document Status**: Integration Plan Complete
**Next Steps**: Create role-specialist delegation framework
**Dependencies**: MCP server catalog, Anthropic research findings
**Custom Development**: 4 MCP servers (Orchestra, Prefect, Great Expectations, Tableau Enhanced)
