# D&A Agent Hub Data Constitution

## Core Principles

### I. Data Quality First
**Every data project starts with quality validation before transformation logic**  
- Source data profiling and validation tests must be implemented before any dbt staging models
- Data quality tests must be written and fail before implementing transformation logic (TDD for data)
- Business rule validation with real data required before production deployment
- Data lineage tracking mandatory for all production data assets
- Error handling and alerting specified for all data pipeline failures

### II. Tool-Specific Standards
**Each tool in the data stack has defined standards and integration patterns**  
- **dbt**: Models must follow staging → intermediate → marts layer pattern
- **Snowflake**: Schema design follows raw → clean → presentation structure  
- **Tableau**: Data sources optimized with extract strategy and performance considerations
- **Orchestra**: Pipelines include comprehensive monitoring and failure recovery mechanisms
- **Cross-tool**: Clear data contracts defined between all system boundaries

### III. Test-First Data Development (NON-NEGOTIABLE)
**TDD methodology adapted for data analytics projects**  
- Data quality tests written and validated to fail before implementing transformation logic
- Business logic validation with sample data before full implementation  
- End-to-end pipeline testing with realistic data volumes before production
- Dashboard/report accuracy validation against known correct results
- Performance testing under expected load conditions mandatory

### IV. Business Alignment & Stakeholder Validation
**All data work must trace back to clear business value**  
- Business questions and success metrics defined before technical implementation
- Stakeholder review checkpoints planned throughout implementation
- User acceptance testing with actual data consumers required
- Business metric validation included in all data quality testing
- Training and documentation planned for all end-user facing deliverables

### V. Cross-System Integration Standards  
**Data projects span multiple tools and require coordination**  
- Clear handoff points identified between all tools in the stack
- Shared schema and model documentation maintained across tools
- Coordinated deployment strategy prevents system conflicts
- Integration testing validates data flow through complete pipeline
- Performance optimization considers cross-tool impact

## Data Governance Requirements

### Data Security & Compliance
- Row-level security implemented where business rules require data access controls
- Personally identifiable information (PII) handling complies with company data policies  
- Data retention and archival policies defined and implemented in all storage layers
- Audit logging enabled for all data access and modification operations
- Data classification and sensitivity labeling applied consistently

### Data Lineage & Documentation
- Complete data lineage tracked from source systems through all transformation layers
- Business glossary maintained with consistent metric and dimension definitions
- Data dictionary updated with every schema or calculation change
- Impact analysis documented for all changes affecting downstream consumers
- Version control applied to all data models, dashboards, and pipeline definitions

### Performance & Scalability Standards
- Query performance SLAs defined and monitored for all user-facing data assets
- Resource usage monitored and optimized across all tools in the stack
- Auto-scaling policies implemented for variable data processing loads
- Data partitioning and clustering strategies implemented for large datasets
- Caching strategies optimized for common access patterns

## Sub-Agent Coordination Principles

### Research-First Approach
- Sub-agents conduct thorough research and create detailed implementation plans
- Parent agent implements based on sub-agent findings and recommendations
- Communication via standardized specification and findings documents
- Clear separation maintained between research/planning and implementation phases

### Expertise-Driven Task Assignment
- **dbt-expert**: All dbt model design, testing strategy, performance optimization
- **snowflake-expert**: Schema design, query optimization, security implementation
- **tableau-expert**: Dashboard design, data source optimization, user experience
- **orchestra-expert**: Pipeline orchestration, monitoring, failure handling, scheduling
- **business-context**: Stakeholder coordination, requirement validation, user training
- **da-architect**: System design decisions, tool selection, cross-platform strategy

### Handoff Protocols
- Predecessor agents document findings and recommendations in standardized format
- Successor agents read predecessor findings before beginning work
- Parent agent coordinates cross-tool integration points and resolves conflicts
- Critical integration points explicitly managed with validation checkpoints

## Quality Gates

### Pre-Implementation Gates
- Business requirements fully specified with measurable success criteria
- Data sources validated and schemas documented before transformation logic
- Performance requirements defined with specific SLA targets
- Security and compliance requirements identified and planned
- Cross-tool architecture validated for feasibility and performance

### Implementation Gates  
- Data quality tests pass before transformation logic deployment
- Business logic validated with known correct test data
- Integration testing completed across all tool boundaries
- Performance testing validates system meets defined SLAs
- Security testing validates access controls and data protection

### Pre-Production Gates
- End-to-end pipeline testing with production-scale data completed
- User acceptance testing completed with actual business stakeholders
- Documentation and training materials completed and validated
- Monitoring and alerting configured and tested
- Rollback procedures tested and documented

## Development Workflow Standards

### Project Structure
- All data projects use numbered feature branches (001-project-name)
- Specification-driven development with /specify → /plan → /tasks workflow
- Cross-repository coordination for projects spanning dbt + Snowflake + Tableau
- Version control applied to all data assets including dashboards and pipeline definitions

### Testing Strategy
- TDD methodology: tests written → validated to fail → implementation → tests pass
- Integration testing for all tool boundaries and data handoff points
- Performance testing with realistic data volumes and user concurrency
- Business logic validation with stakeholder-provided test cases
- Regression testing for all changes affecting existing data consumers

### Deployment Standards
- Staged deployment through development → staging → production environments
- Coordinated deployments across all tools to prevent integration failures
- Blue-green deployment strategy for critical business-facing data assets
- Automated rollback capabilities for all production data pipeline changes
- Post-deployment monitoring for data quality, performance, and user adoption

## Governance & Amendment Process

### Constitutional Authority
- This constitution supersedes all other development practices for data projects
- All project specifications must validate compliance before implementation
- Complexity that violates constitutional principles requires documented business justification
- Amendments require approval from data platform stakeholders and technical leads

### Compliance Monitoring
- All project reviews must verify constitutional compliance
- Regular audits of implemented projects against constitutional principles  
- Violations tracked and addressed through process improvement initiatives
- Success metrics include constitutional compliance rates and data quality outcomes

### Continuous Improvement
- Constitution updated based on lessons learned from implemented projects
- Best practices evolved based on tool capabilities and business requirements
- Regular review cycles to ensure principles remain relevant and effective
- Community feedback incorporated from data consumers and platform users

---

**Version**: 1.0.0 | **Ratified**: 2025-09-09 | **Last Amended**: 2025-09-09

**Amendment Authority**: Data Platform Team + Sub-Agent Maintainers  
**Review Cycle**: Quarterly review, annual formal updates  
**Compliance Owner**: Parent Agent + Data Architecture Review Board