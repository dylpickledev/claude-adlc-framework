# Role-Based Agent + MCP Integration Architecture Diagrams

## 1. Three-Layer Architecture Overview

```mermaid
graph TB
    subgraph "LAYER 1: Role-Based Orchestrator"
        CM[cloud-manager-role<br/>Primary Orchestrator<br/>Confidence ≥0.85: Independent<br/>Confidence <0.85: Consult Specialist]
    end

    subgraph "LAYER 2: MCP Tool Layer"
        API[aws-api MCP<br/>Infrastructure State<br/>Read-Only Operations]
        DOCS[aws-docs MCP<br/>Latest Documentation<br/>API References]
        KNOW[aws-knowledge MCP<br/>Best Practices<br/>Well-Architected]
    end

    subgraph "LAYER 3: Specialist Consultant"
        AWS[aws-expert<br/>Deep AWS Patterns<br/>Complex Optimization<br/>20% Consultation Rate]
    end

    CM -->|Direct Access<br/>80% of Work| API
    CM -->|Direct Access<br/>Syntax Validation| DOCS
    CM -->|Direct Access<br/>Framework Guidance| KNOW
    CM -->|Consult When<br/>Confidence <0.85| AWS
    AWS -.->|Expert Guidance<br/>Returns to Role| CM

    style CM fill:#4A90E2,stroke:#2E5C8A,stroke-width:3px,color:#fff
    style API fill:#7ED321,stroke:#5FA319,stroke-width:2px
    style DOCS fill:#7ED321,stroke:#5FA319,stroke-width:2px
    style KNOW fill:#7ED321,stroke:#5FA319,stroke-width:2px
    style AWS fill:#F5A623,stroke:#C17D11,stroke-width:2px
```

## 2. Decision Flow: When to Use Each Layer

```mermaid
graph TD
    START[Cloud Infrastructure Task] --> Q1{Task Complexity<br/>Assessment}

    Q1 -->|Simple/Standard<br/>Confidence ≥0.85| ROLE[cloud-manager-role<br/>Handles Independently]
    Q1 -->|Complex/Specialized<br/>Confidence <0.85| CONSULT[Consult aws-expert]

    ROLE --> MCP_CHECK{Which MCP<br/>Tool Needed?}

    MCP_CHECK -->|Current State| API[Use aws-api MCP<br/>Infrastructure Discovery]
    MCP_CHECK -->|Latest Syntax| DOCS[Use aws-docs MCP<br/>Documentation Lookup]
    MCP_CHECK -->|Best Practices| KNOW[Use aws-knowledge MCP<br/>Framework Guidance]

    API --> CONF_CHECK{Confidence<br/>After MCP?}
    DOCS --> CONF_CHECK
    KNOW --> CONF_CHECK

    CONF_CHECK -->|Still ≥0.85| IMPLEMENT[Role Implements<br/>Solution]
    CONF_CHECK -->|Dropped <0.85| CONSULT

    CONSULT --> EXPERT[aws-expert Analysis<br/>Deep Patterns]
    EXPERT --> COLLAB[Collaborative<br/>Implementation]
    COLLAB --> IMPLEMENT

    IMPLEMENT --> OUTPUT[Infrastructure Code<br/>Documentation<br/>Recommendations]

    style START fill:#E8E8E8,stroke:#999,stroke-width:2px
    style ROLE fill:#4A90E2,stroke:#2E5C8A,stroke-width:3px,color:#fff
    style API fill:#7ED321,stroke:#5FA319,stroke-width:2px
    style DOCS fill:#7ED321,stroke:#5FA319,stroke-width:2px
    style KNOW fill:#7ED321,stroke:#5FA319,stroke-width:2px
    style CONSULT fill:#F5A623,stroke:#C17D11,stroke-width:2px
    style EXPERT fill:#F5A623,stroke:#C17D11,stroke-width:2px
    style IMPLEMENT fill:#50E3C2,stroke:#2EB398,stroke-width:2px
    style OUTPUT fill:#B8E986,stroke:#8BC34A,stroke-width:2px
```

## 3. Confidence Level Enhancement via MCP

```mermaid
graph LR
    subgraph "Before MCP Integration"
        B1[Infrastructure Audits<br/>0.65 Confidence]
        B2[Cost Analysis<br/>0.89 Confidence]
        B3[Security Review<br/>0.70 Confidence]
        B4[Compliance Check<br/>0.60 Confidence]
    end

    subgraph "MCP Tool Layer"
        MCP1[aws-api<br/>Real-time State]
        MCP2[aws-knowledge<br/>Best Practices]
        MCP3[aws-docs<br/>Latest Standards]
    end

    subgraph "After MCP Integration"
        A1[Infrastructure Audits<br/>0.95 Confidence<br/>+0.30 boost]
        A2[Cost Analysis<br/>0.95 Confidence<br/>+0.06 boost]
        A3[Security Review<br/>0.90 Confidence<br/>+0.20 boost]
        A4[Compliance Check<br/>0.88 Confidence<br/>+0.28 boost]
    end

    B1 -->|Uses| MCP1
    MCP1 --> A1

    B2 -->|Uses| MCP1
    B2 -->|Uses| MCP2
    MCP2 --> A2

    B3 -->|Uses| MCP2
    B3 -->|Uses| MCP3
    MCP3 --> A3

    B4 -->|Uses| MCP2
    B4 -->|Uses| MCP3
    MCP2 --> A4

    style B1 fill:#FFE5E5,stroke:#FF6B6B,stroke-width:2px
    style B2 fill:#FFF4E5,stroke:#FFA726,stroke-width:2px
    style B3 fill:#FFE5E5,stroke:#FF6B6B,stroke-width:2px
    style B4 fill:#FFE5E5,stroke:#FF6B6B,stroke-width:2px

    style MCP1 fill:#7ED321,stroke:#5FA319,stroke-width:2px
    style MCP2 fill:#7ED321,stroke:#5FA319,stroke-width:2px
    style MCP3 fill:#7ED321,stroke:#5FA319,stroke-width:2px

    style A1 fill:#E5F7E5,stroke:#4CAF50,stroke-width:2px
    style A2 fill:#E5F7E5,stroke:#4CAF50,stroke-width:2px
    style A3 fill:#E5F7E5,stroke:#4CAF50,stroke-width:2px
    style A4 fill:#E5F7E5,stroke:#4CAF50,stroke-width:2px
```

## 4. Integration Workflow Example: Infrastructure Audit

```mermaid
sequenceDiagram
    participant User
    participant CM as cloud-manager-role
    participant API as aws-api MCP
    participant KNOW as aws-knowledge MCP
    participant AWS as aws-expert
    participant OUT as Output

    User->>CM: Request AWS Infrastructure Audit

    Note over CM: Step 1: State Discovery<br/>(Confidence: 0.92 base)

    CM->>API: List ECS services
    API-->>CM: Service configurations

    CM->>API: Query Lambda functions
    API-->>CM: Function details (runtime, memory, timeout)

    CM->>API: Get ALB/RDS configs
    API-->>CM: Resource metadata

    Note over CM: Confidence now: 0.95<br/>(+0.03 from real-time data)

    Note over CM: Step 2: Best Practices Validation<br/>(Confidence: 0.89 base)

    CM->>KNOW: Query Well-Architected cost patterns
    KNOW-->>CM: Optimization opportunities

    CM->>KNOW: Get security best practices
    KNOW-->>CM: Security recommendations

    Note over CM: Confidence now: 0.95<br/>(+0.06 from best practices)

    Note over CM: Step 3: Complex Pattern Check

    alt Advanced Lambda Optimization Needed
        Note over CM: Confidence <0.85 on cold starts
        CM->>AWS: Consult on Lambda optimization
        AWS->>AWS: Deep pattern analysis
        AWS-->>CM: Expert recommendations
        Note over CM: Collaborate on implementation
    else Standard Patterns Sufficient
        Note over CM: Confidence ≥0.85
        Note over CM: Handle independently
    end

    Note over CM: Step 4: Implementation

    CM->>OUT: Infrastructure as Code
    CM->>OUT: Architecture documentation
    CM->>OUT: Cost analysis report
    CM->>OUT: Optimization roadmap

    OUT-->>User: Complete audit deliverables

    Note over User,OUT: 50-70% faster than<br/>multi-agent coordination
```

## 5. Comparison: Old vs New Architecture

### Old Architecture (Tool-Specific Agents)

```mermaid
graph TD
    USER[User Request] --> T1[tableau-expert]
    T1 --> T2[dbt-expert]
    T2 --> T3[snowflake-expert]
    T3 --> T4[dbt-expert]
    T4 --> T5[tableau-expert]
    T5 --> T6[documentation-expert]
    T6 --> OUT[Deliverable]

    style USER fill:#E8E8E8,stroke:#999
    style T1 fill:#FFE5E5,stroke:#FF6B6B
    style T2 fill:#FFE5E5,stroke:#FF6B6B
    style T3 fill:#FFE5E5,stroke:#FF6B6B
    style T4 fill:#FFE5E5,stroke:#FF6B6B
    style T5 fill:#FFE5E5,stroke:#FF6B6B
    style T6 fill:#FFE5E5,stroke:#FF6B6B
    style OUT fill:#B8E986,stroke:#8BC34A

    Note[6 agents<br/>5 handoffs<br/>3 hours<br/>High coordination overhead]
```

### New Architecture (Role + MCP + Specialist)

```mermaid
graph TD
    USER2[User Request] --> ROLE[Role Agent<br/>+<br/>MCP Tools]
    ROLE -->|Only if needed| SPEC[Specialist<br/>Consultant]
    SPEC -.->|Guidance| ROLE
    ROLE --> OUT2[Deliverable]

    style USER2 fill:#E8E8E8,stroke:#999
    style ROLE fill:#4A90E2,stroke:#2E5C8A,stroke-width:3px,color:#fff
    style SPEC fill:#F5A623,stroke:#C17D11,stroke-width:2px
    style OUT2 fill:#B8E986,stroke:#8BC34A

    Note2[2 agents<br/>1 optional handoff<br/>1 hour<br/>50-70% faster]
```

## 6. MCP Tool Selection Matrix

```mermaid
graph TB
    TASK[Infrastructure Task] --> Q1{What do I need?}

    Q1 -->|Current State<br/>Resource Inventory| USE_API[Use aws-api MCP]
    Q1 -->|Latest Syntax<br/>Code Examples| USE_DOCS[Use aws-docs MCP]
    Q1 -->|Best Practices<br/>Governance| USE_KNOW[Use aws-knowledge MCP]

    USE_API --> API_EX[Examples:<br/>• List ECS services<br/>• Get Lambda configs<br/>• Query RDS instances<br/>• ALB listener rules]

    USE_DOCS --> DOCS_EX[Examples:<br/>• CloudWatch syntax<br/>• EventBridge patterns<br/>• IAM policy structure<br/>• Service quotas]

    USE_KNOW --> KNOW_EX[Examples:<br/>• Well-Architected pillars<br/>• Security patterns<br/>• Cost optimization<br/>• Compliance frameworks]

    API_EX --> RESULT[Enhanced Confidence<br/>Real-time Data<br/>Accurate State]
    DOCS_EX --> RESULT
    KNOW_EX --> RESULT

    style TASK fill:#E8E8E8,stroke:#999,stroke-width:2px
    style USE_API fill:#7ED321,stroke:#5FA319,stroke-width:3px
    style USE_DOCS fill:#7ED321,stroke:#5FA319,stroke-width:3px
    style USE_KNOW fill:#7ED321,stroke:#5FA319,stroke-width:3px
    style API_EX fill:#E5F7E5,stroke:#4CAF50,stroke-width:2px
    style DOCS_EX fill:#E5F7E5,stroke:#4CAF50,stroke-width:2px
    style KNOW_EX fill:#E5F7E5,stroke:#4CAF50,stroke-width:2px
    style RESULT fill:#B8E986,stroke:#8BC34A,stroke-width:2px
```

## 7. Specialist Consultation Triggers

```mermaid
graph TD
    START[Task Analysis] --> CONF{Confidence Level?}

    CONF -->|≥0.85| INDEPENDENT[Role Handles<br/>Independently<br/>80% of Tasks]
    CONF -->|<0.85| CHECK{Service Type?}

    CHECK -->|SageMaker| CONSULT1[aws-expert<br/>Confidence: 0.45]
    CHECK -->|EKS| CONSULT2[aws-expert<br/>Confidence: 0.50]
    CHECK -->|Step Functions| CONSULT3[aws-expert<br/>Confidence: 0.55]
    CHECK -->|Organizations| CONSULT4[aws-expert<br/>Confidence: 0.48]

    INDEPENDENT --> MCP[Use MCP Tools<br/>Direct Access]
    MCP --> IMPL1[Implement Solution]

    CONSULT1 --> EXPERT[Specialist Analysis<br/>Deep Patterns]
    CONSULT2 --> EXPERT
    CONSULT3 --> EXPERT
    CONSULT4 --> EXPERT

    EXPERT --> COLLAB[Collaborative<br/>Implementation<br/>20% of Tasks]
    COLLAB --> IMPL2[Implement Solution]

    IMPL1 --> OUT[Deliverable]
    IMPL2 --> OUT

    style START fill:#E8E8E8,stroke:#999
    style INDEPENDENT fill:#4A90E2,stroke:#2E5C8A,stroke-width:3px,color:#fff
    style MCP fill:#7ED321,stroke:#5FA319,stroke-width:2px
    style CONSULT1 fill:#FFE5E5,stroke:#FF6B6B,stroke-width:2px
    style CONSULT2 fill:#FFE5E5,stroke:#FF6B6B,stroke-width:2px
    style CONSULT3 fill:#FFE5E5,stroke:#FF6B6B,stroke-width:2px
    style CONSULT4 fill:#FFE5E5,stroke:#FF6B6B,stroke-width:2px
    style EXPERT fill:#F5A623,stroke:#C17D11,stroke-width:2px
    style COLLAB fill:#F5A623,stroke:#C17D11,stroke-width:2px
    style OUT fill:#B8E986,stroke:#8BC34A
```

## Legend

**Colors:**
- 🔵 Blue: Role-based agents (primary orchestrators)
- 🟢 Green: MCP tool layer (direct access)
- 🟠 Orange: Specialist agents (consultation)
- 🔴 Red: Low confidence areas (need specialist)
- ⚪ Gray: User input / neutral states
- 🟩 Light Green: Success / completion states

**Metrics:**
- **Confidence ≥0.85**: Independent handling by role agent
- **Confidence <0.85**: Specialist consultation needed
- **80/20 rule**: 80% independent, 20% consultation
- **50-70% faster**: Proven coordination reduction

---

## Key Takeaways from Diagrams

1. **Three-Layer Architecture**: Role (orchestrator) → MCP (tools) → Specialist (consultant)
2. **Direct MCP Access**: Roles use tools directly for enhanced capability (+0.05 to +0.30 confidence)
3. **Confidence-Driven Delegation**: ≥0.85 independent, <0.85 consult specialist
4. **Efficiency Gains**: 50-70% coordination reduction vs old tool-specific agents
5. **Tool Selection**: aws-api (state), aws-docs (syntax), aws-knowledge (best practices)

These diagrams illustrate the recommended architecture for integrating role-based agents with MCP servers and specialist consultants, based on Anthropic guidance and industry best practices.
