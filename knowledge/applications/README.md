# GraniteRock Production Applications

This directory contains comprehensive documentation for production web applications deployed on AWS infrastructure.

## Applications

### [App Portal](./app-portal/)
**Production URL**: https://apps.grc-ops.com
**Purpose**: Central authentication hub and application launcher for GraniteRock internal tools
**Stack**: React + TypeScript + Python FastAPI + nginx + ALB OIDC (Azure AD)

**Key Features**:
- Azure AD single sign-on via ALB OIDC
- Application launcher interface
- User authentication management
- Logout flow with HTTP-only cookie handling

### [Sales Journal](./sales-journal/)
**Production URL**: https://apps.grc-ops.com/sales-journal/
**Purpose**: Financial data analysis and reconciliation tool for accounting operations
**Stack**: React + TypeScript + Python FastAPI + Lambda + PostgreSQL + Orchestra API

**Key Features**:
- Real-time financial data dashboard
- Pipeline status monitoring and control
- Multi-tab data exploration interface
- Export functionality (CSV/Excel/PDF)
- Integration with Orchestra workflow orchestration

## Documentation Structure

Each application directory follows this structure:

```
<application>/
├── README.md                 # Application overview and quick start
├── architecture/
│   ├── system-design.md     # High-level architecture
│   ├── infrastructure.md    # AWS resources and configuration
│   └── data-flow.md         # Data architecture and APIs
├── deployment/
│   ├── local-development.md # Local setup instructions
│   ├── docker-build.md      # Container build process
│   └── production-deploy.md # Production deployment runbook
└── operations/
    ├── monitoring.md        # Logging and alerting
    ├── troubleshooting.md   # Common issues and solutions
    └── runbooks.md          # Operational procedures
```

## Infrastructure Overview

### Shared Infrastructure
- **Load Balancer**: Skynet-ELB (Application Load Balancer)
- **Domain**: apps.grc-ops.com (Route 53)
- **Authentication**: Azure AD via ALB OIDC
- **Container Orchestration**: AWS ECS Fargate (skynet-apps-cluster)

### ALB Routing Configuration
```
Priority 1-4: Other apps (tableau, replicate, airbyte)
Priority 5: /sales-journal/api/* → Lambda (sales-journal-api)
Priority 6: /sales-journal/* → ECS (sales-journal service)
Priority 7: apps.grc-ops.com/* → ECS (app-portal service)
Priority 99: /* (catch-all fallback)
```

## Key Technical Patterns

### ALB OIDC Authentication
Both applications use ALB-level OIDC authentication with Azure AD, eliminating need for application-level auth libraries like AWS Amplify or Cognito.

**Benefits**:
- Centralized authentication at infrastructure layer
- No client-side auth libraries required
- Simplified application code
- Consistent auth across all apps on ALB

### Multi-Service Docker Containers
Pattern: Single container running multiple services via supervisor
- nginx (port 80) - Serves React SPA
- Python API (port 8080) - Backend logic
- supervisor - Process manager

**Benefits**:
- Simplified deployment (single container)
- Shared filesystem for static assets
- Lower resource overhead than separate containers

### Path-Based Routing
ALB routes requests based on URL path patterns with priority rules ensuring specific paths match before catch-all rules.

**Critical**: Lower priority numbers execute FIRST
- Specific paths (e.g., `/sales-journal/*`) must have lower priority than catch-all (`/*`)

## Related Documentation

- **AWS Infrastructure Patterns**: `../da-agent-hub/development/aws-ecs-deployment-patterns.md`
- **Agent Training**: `../../.claude/agents/specialists/aws-expert.md`
- **Team Documentation**: `../da_team_documentation/`

## Version History

- **2025-10-07**: Initial documentation structure created
- **2025-10-06**: App Portal + Sales Journal deployed to production
- **2025-10-04**: ALB OIDC authentication implementation complete
