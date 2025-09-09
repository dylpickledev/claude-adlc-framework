# Data Analytics Feature Specification: Build daily customer lifecycle metrics dashboard showing acquisition, retention, and churn trends with data from Salesforce CRM, Stripe billing, and support ticket volumes

**Feature Branch**: `[###-feature-name]`  
**Created**: [DATE]  
**Status**: Draft  
**Input**: User description: "$ARGUMENTS"

## Execution Flow (main)
```
1. Parse user description from Input
   → If empty: ERROR "No feature description provided"
2. Extract key concepts from description
   → Identify: data sources, stakeholders, business metrics, constraints
3. For each unclear aspect:
   → Mark with [NEEDS CLARIFICATION: specific question]
4. Fill Data Requirements & Business Logic section
   → If no clear data flow: ERROR "Cannot determine data pipeline"
5. Generate Functional Requirements
   → Each requirement must be testable with data
   → Mark ambiguous business rules
6. Identify Key Data Entities and Metrics
7. Run Review Checklist
   → If any [NEEDS CLARIFICATION]: WARN "Spec has uncertainties"
   → If implementation details found: ERROR "Remove tech details"
8. Return: SUCCESS (spec ready for planning)
```

---

## ⚡ Quick Guidelines for Data Projects
- ✅ Focus on WHAT business questions to answer and WHY
- ❌ Avoid HOW to implement (no SQL, dbt models, dashboard specifics)
- 📊 Written for business stakeholders and data consumers
- 🔄 Consider data freshness, quality, and governance requirements

### Section Requirements
- **Mandatory sections**: Must be completed for every data feature
- **Optional sections**: Include only when relevant to the feature
- When a section doesn't apply, remove it entirely (don't leave as "N/A")

### For AI Generation
When creating this spec from a user prompt:
1. **Mark all ambiguities**: Use [NEEDS CLARIFICATION: specific question] for any assumption you'd need to make
2. **Don't guess business logic**: If the prompt doesn't specify calculations, mark it
3. **Think like a data tester**: Every vague requirement should fail the "testable and measurable" checklist item
4. **Common underspecified areas**:
   - Data source definitions and SLAs
   - Business rule calculations and edge cases
   - Data quality thresholds and validation rules
   - Refresh frequency and historical requirements
   - User access patterns and permissions
   - Performance and scale expectations

---

## Business Context & Stakeholders *(mandatory)*

### Primary Business Question
[Describe the main business question this data solution answers]

### Key Stakeholders
- **Primary Users**: [Who will directly consume this data/analysis?]
- **Data Owners**: [Who owns/controls the source data?]
- **Decision Makers**: [Who will act on insights from this data?]

### Success Criteria
- **Business Impact**: [How will success be measured from business perspective?]
- **Usage Metrics**: [How will adoption/utilization be tracked?]

## Data Requirements & Business Logic *(mandatory)*

### Data Sources
- **Source 1**: [System/table name, update frequency, data owner]
- **Source 2**: [System/table name, update frequency, data owner]

### Key Business Rules
1. **BR-001**: [Specific business calculation or logic rule]
2. **BR-002**: [Data validation or quality rule]
3. **BR-003**: [Historical data handling rule]

### Data Flow Requirements
1. **Given** [source data state], **When** [business event occurs], **Then** [expected data outcome]
2. **Given** [data quality condition], **When** [validation runs], **Then** [system behavior]

## Functional Requirements *(mandatory)*

### Data Pipeline Requirements
- **FR-001**: System MUST [specific data ingestion capability]
- **FR-002**: System MUST [specific transformation requirement]  
- **FR-003**: System MUST [specific data quality validation]
- **FR-004**: System MUST [specific refresh/update behavior]

### Analytics Requirements
- **FR-005**: Users MUST be able to [specific analytical capability]
- **FR-006**: System MUST provide [specific metric or calculation]
- **FR-007**: Reports MUST show [specific data visualization requirement]

### Data Governance Requirements
- **FR-008**: System MUST [data retention/archival requirement]
- **FR-009**: System MUST [data access control requirement]
- **FR-010**: System MUST [data lineage/audit requirement]

*Example of marking unclear requirements:*
- **FR-011**: System MUST calculate customer lifetime value using [NEEDS CLARIFICATION: specific formula not provided]
- **FR-012**: Data MUST be refreshed [NEEDS CLARIFICATION: frequency not specified - daily, hourly, real-time?]

### Key Data Entities & Metrics *(include if feature involves new data models)*
- **[Entity 1]**: [What business concept it represents, key attributes]
  - Primary Key: [business identifier description]
  - Key Metrics: [calculated fields or aggregations]
- **[Metric 1]**: [Business definition, calculation logic, granularity]

## Data Quality & Performance Requirements *(mandatory)*

### Quality Thresholds
- **Completeness**: [acceptable null/missing data percentages]
- **Accuracy**: [validation rules and acceptable error rates]
- **Timeliness**: [data freshness requirements and SLAs]

### Performance Requirements
- **Query Performance**: [acceptable response times for different use cases]
- **Data Volume**: [expected data growth and retention periods]
- **Concurrency**: [expected number of simultaneous users/queries]

---

## Cross-System Integration *(include if applicable)*

### dbt Integration
- **Models Required**: [staging, intermediate, mart model concepts]
- **Testing Strategy**: [data quality tests needed]

### Tableau Integration  
- **Dashboard Requirements**: [visualization needs and user groups]
- **Refresh Strategy**: [how often dashboards need updated data]

### Snowflake Integration
- **Storage Requirements**: [database, schema, table structure needs]
- **Access Patterns**: [how data will be queried and by whom]

### Orchestra Integration
- **Pipeline Dependencies**: [upstream and downstream job requirements]
- **Monitoring Needs**: [alerting and failure handling]

---

## Review & Acceptance Checklist
*GATE: Automated checks run during main() execution*

### Content Quality
- [ ] No implementation details (SQL, dbt syntax, dashboard configs)
- [ ] Focused on business value and data requirements
- [ ] Written for business stakeholders and data consumers
- [ ] All mandatory sections completed

### Requirement Completeness  
- [ ] No [NEEDS CLARIFICATION] markers remain
- [ ] Business rules are testable with data
- [ ] Data quality thresholds are measurable
- [ ] Success criteria are quantifiable
- [ ] Data sources and refresh requirements identified
- [ ] Cross-system dependencies mapped

### Data Governance
- [ ] Data ownership and stewardship identified
- [ ] Access control requirements specified  
- [ ] Data retention and archival policies defined
- [ ] Compliance and audit requirements addressed

---

## Execution Status
*Updated by main() during processing*

- [ ] User description parsed
- [ ] Key data concepts extracted  
- [ ] Business rule ambiguities marked
- [ ] Data flow requirements defined
- [ ] Functional requirements generated
- [ ] Data entities and metrics identified
- [ ] Cross-system integration planned
- [ ] Review checklist passed

---