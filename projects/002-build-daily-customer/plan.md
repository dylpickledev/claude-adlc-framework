# Data Analytics Implementation Plan: Build daily customer lifecycle metrics dashboard showing acquisition, retention, and churn trends with data from Salesforce CRM, Stripe billing, and support ticket volumes

**Branch**: `dashboard/002-build-daily-customer` | **Date**: 2025-09-09 | **Spec**: spec.md
**Input**: Feature specification from `/projects/dashboard/002-build-daily-customer/spec.md`

## Execution Flow (/plan command scope)
```
1. Load feature spec from Input path
   → If not found: ERROR "No feature spec at {path}"
2. Fill Technical Context (scan for NEEDS CLARIFICATION)
   → Detect Data Project Type (pipeline, dashboard, analysis, model)
   → Set Tool Selection based on requirements
3. Evaluate Data Constitution Check section below
   → If violations exist: Document in Complexity Tracking
   → If no data governance justification: ERROR "Address data quality first"
   → Update Progress Tracking: Initial Constitution Check
4. Execute Phase 0 → research.md (data sources, tool capabilities)
   → If NEEDS CLARIFICATION remain: ERROR "Resolve data unknowns"
5. Execute Phase 1 → data-model.md, contracts/, quickstart.md, CLAUDE.md
6. Re-evaluate Data Constitution Check section
   → If new violations: Refactor design, return to Phase 1
   → Update Progress Tracking: Post-Design Constitution Check
7. Plan Phase 2 → Describe task generation approach (DO NOT create tasks.md)
8. STOP - Ready for /tasks command
```

**IMPORTANT**: The /plan command STOPS at step 7. Phases 2-4 are executed by other commands:
- Phase 2: /tasks command creates tasks.md
- Phase 3-4: Implementation execution (manual or via sub-agents)

## Summary
[Extract from feature spec: primary business question + technical approach from research]

## Technical Context
**Data Stack**: [e.g., dbt + Snowflake + Tableau, Python + Orchestra, or NEEDS CLARIFICATION]  
**Primary Tools**: [e.g., dbt 1.6, Tableau Server, Orchestra Cloud or NEEDS CLARIFICATION]  
**Data Storage**: [e.g., Snowflake, PostgreSQL, S3 or NEEDS CLARIFICATION]  
**Orchestration**: [e.g., Orchestra, Airflow, cron or N/A]  
**Testing Framework**: [e.g., dbt tests, Great Expectations, custom or NEEDS CLARIFICATION]  
**Data Platform**: [e.g., Cloud data warehouse, on-prem, hybrid or NEEDS CLARIFICATION]
**Project Type**: [pipeline/dashboard/analysis/model - determines structure]  
**Performance Goals**: [e.g., <5min refresh, <2s query response, 99.9% uptime or NEEDS CLARIFICATION]  
**Data Volume**: [e.g., 1M rows/day, 10GB total, real-time stream or NEEDS CLARIFICATION]  
**Business SLA**: [e.g., daily by 9AM, hourly updates, weekly reports or NEEDS CLARIFICATION]

## Data Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Data Quality First**:
- Data quality tests planned before transformation logic?
- Source data validation included?
- Business rule validation tests defined?
- Data lineage tracking enabled?
- Error handling and alerting specified?

**Tool-Specific Standards**:
- **dbt**: Models follow staging → intermediate → marts pattern?
- **Snowflake**: Proper schema design (raw → clean → presentation)?
- **Tableau**: Data source optimization and extract strategy?
- **Orchestra**: Pipeline monitoring and failure recovery?

**Testing (NON-NEGOTIABLE)**:
- Data quality tests before transformation implementation?
- Business logic validation with sample data?
- End-to-end pipeline testing with real data?
- Dashboard/report accuracy validation?
- Performance testing under expected load?

**Cross-System Integration**:
- Clear handoff points between tools identified?
- Data contracts defined between systems?
- Shared schema/model documentation?
- Coordinated deployment strategy?

**Business Alignment**:
- Stakeholder review checkpoints planned?
- Business metric validation included?
- User acceptance testing with actual data consumers?
- Training/documentation for end users?

## Project Structure

### Documentation (this feature)
- `spec.md` - Business requirements and data definitions
- `plan.md` - This implementation plan
- `research.md` - Tool research and technical decisions
- `quickstart.md` - Setup and testing instructions
- `CLAUDE.md` - Agent context and coordination instructions

### Data Architecture
- `data-model.md` - Entity definitions and relationships
- `contracts/` - API specs and data contracts between systems
  - `dbt-contracts.yml` - dbt model contracts and tests
  - `tableau-datasources.yml` - Dashboard data source definitions
  - `snowflake-schema.sql` - Database schema and permissions

### Implementation Structure
```
[Project Root]/
├── dbt_project/
│   ├── models/
│   │   ├── staging/     # Raw data transformations
│   │   ├── intermediate/# Business logic models
│   │   └── marts/       # Final presentation models
│   └── tests/           # Data quality tests
├── tableau/
│   ├── datasources/     # Published data sources
│   └── workbooks/       # Dashboard definitions
├── snowflake/
│   ├── schemas/         # Database object definitions
│   └── permissions/     # Access control scripts
└── orchestration/
    ├── pipelines/       # Orchestra job definitions
    └── monitoring/      # Alerting and observability
```

## Data Pipeline Architecture

### Data Flow
1. **Ingestion Layer**: [Source → Raw storage]
2. **Transformation Layer**: [Raw → Clean → Business Logic]
3. **Presentation Layer**: [Marts → Dashboards/APIs]
4. **Orchestration Layer**: [Job scheduling and monitoring]

### Tool Coordination
- **Source Data**: [Systems and refresh patterns]
- **dbt Models**: [Staging, intermediate, mart layer responsibilities]
- **Snowflake**: [Storage optimization and query patterns]  
- **Tableau**: [Dashboard refresh strategy and data sources]
- **Orchestra**: [Pipeline dependencies and failure handling]

## Phase 0: Research & Discovery *(executed in this command)*

### Technical Research Areas
- [ ] Data source availability and schema validation
- [ ] Tool version compatibility and best practices
- [ ] Performance benchmarking for expected data volumes
- [ ] Security and compliance requirements
- [ ] Integration patterns between selected tools

### Business Research Areas  
- [ ] Stakeholder data consumption patterns
- [ ] Existing similar solutions and gaps
- [ ] Data governance and approval processes
- [ ] Training and change management needs

## Phase 1: Design & Contracts *(executed in this command)*

### Data Model Design
- Entity relationship mapping from business requirements
- Grain definition for each mart table
- Slowly changing dimension strategies
- Data quality threshold definitions

### System Integration Contracts
- dbt model interfaces and tests
- Snowflake schema and permission model
- Tableau data source optimization
- Orchestra pipeline dependencies

### Testing Strategy
- Data quality test coverage plan
- Business logic validation approach
- End-to-end integration testing
- Performance and scale testing

## Phase 2: Task Planning *(planned here, executed by /tasks command)*

### Task Generation Strategy
Will break implementation into these task categories:

**Setup Tasks** (sequential):
- Environment and tool configuration
- Database schema and permission setup
- Repository and branch structure

**Data Foundation Tasks** (can be parallel where tools don't conflict):
- [P] Source data validation and profiling
- [P] dbt staging model creation
- [P] Snowflake raw schema setup
- [P] Orchestra pipeline skeleton

**Business Logic Tasks** (sequential within tool, parallel across tools):
- dbt intermediate and mart model development
- Tableau data source and calculated field creation
- Snowflake optimization (indexes, clustering)
- Orchestra job scheduling and monitoring

**Integration & Testing Tasks**:
- End-to-end pipeline testing
- Dashboard accuracy validation
- Performance optimization
- User acceptance testing

**Deployment Tasks**:
- Production environment setup
- User training and documentation
- Go-live coordination

### Sub-Agent Coordination
- **dbt-expert**: Model design, testing strategy, performance optimization
- **snowflake-expert**: Schema design, query optimization, security
- **tableau-expert**: Dashboard design, data source optimization
- **orchestra-expert**: Pipeline orchestration, monitoring, failure handling
- **business-context**: Stakeholder coordination, requirement validation

## Complexity Tracking
*Document any constitutional violations and their justifications*

[Any complexity that violates the constitution should be listed here with business justification]

## Progress Tracking
*Updated during execution*

- [ ] Technical context filled
- [ ] Initial constitution check passed
- [ ] Phase 0 research completed
- [ ] Phase 1 design completed
- [ ] Post-design constitution check passed
- [ ] Phase 2 task planning completed
- [ ] Ready for /tasks command

---