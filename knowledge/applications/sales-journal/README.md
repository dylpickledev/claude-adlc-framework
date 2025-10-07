# Sales Journal - React Application

**Production URL**: https://apps.grc-ops.com/sales-journal/
**Status**: ✅ Production (deployed 2025-10-06)
**Stack**: React + TypeScript + Vite + FastAPI (Lambda) + PostgreSQL + Orchestra API

---

## Overview

The Sales Journal is a financial data analysis and reconciliation tool for GraniteRock's accounting operations. It provides real-time visibility into sales transactions, pipeline status, and data quality metrics.

### Key Features

- **Real-Time Dashboard**: Pipeline status, DMS replication, tieout validation, balance checking
- **Multi-Tab Interface**: 10 specialized tabs for different analysis workflows
- **Pipeline Control**: Trigger and monitor Orchestra workflows (Refresh + Finalize)
- **Data Exploration**: Filter, search, and analyze financial transactions
- **Export Capabilities**: CSV, Excel, and PDF export functionality
- **Authentication**: Azure AD SSO via ALB OIDC (infrastructure-level)

---

## Architecture

### System Design

```
┌─────────────────────────────────────────────────────────────┐
│                     AWS Application Load Balancer            │
│                    (apps.grc-ops.com)                        │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Priority 5: /sales-journal/api/*                    │   │
│  │   → Authenticate-OIDC (Azure AD)                    │   │
│  │   → Lambda: sales-journal-api                       │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Priority 6: /sales-journal/*                        │   │
│  │   → Authenticate-OIDC (Azure AD)                    │   │
│  │   → ECS Fargate: sales-journal service             │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                │                           │
                ▼                           ▼
    ┌────────────────────┐      ┌────────────────────┐
    │  ECS Fargate Task  │      │  Lambda Function   │
    │  (nginx + React)   │      │  (Python FastAPI)  │
    │                    │      │                    │
    │  Port 80           │      │  Runtime: 3.12     │
    │  /sales-journal/   │      │  Memory: 1024MB    │
    └────────────────────┘      │  Timeout: 30s      │
                                 └────────────────────┘
                                          │
                                          ▼
                        ┌─────────────────────────────────┐
                        │      External Services          │
                        │                                 │
                        │  • PostgreSQL (RDS)             │
                        │  • Orchestra API                │
                        │  • AWS Secrets Manager          │
                        └─────────────────────────────────┘
```

### Technology Stack

**Frontend**:
- React 18 + TypeScript
- Vite (build tool)
- Zustand (state management)
- styled-components (CSS-in-JS)
- Framer Motion (animations)
- Recharts (data visualization)

**Backend API**:
- Python 3.12
- FastAPI (web framework)
- psycopg2 (PostgreSQL driver)
- httpx (Orchestra API client)
- AWS Lambda (serverless deployment)

**Infrastructure**:
- AWS ECS Fargate (React app hosting)
- AWS Lambda (API backend)
- AWS ALB (load balancing + authentication)
- AWS Secrets Manager (credentials)
- Docker (containerization)

**Data Sources**:
- PostgreSQL RDS (financial data)
- Orchestra API (pipeline orchestration)
- dbt models (data transformations)

---

## Key Features

### Dashboard
Real-time status monitoring with 4 key metrics:
- Pipeline Status (REFRESH + FINAL pipelines)
- DMS Replication Status (all tasks must be ready)
- Tieout Validation (pass/fail counts)
- Out of Balance Total (color-coded by threshold)

### Pipeline Control
- Trigger Refresh pipeline (daily data sync)
- Trigger Finalize pipeline (period close)
- Real-time status monitoring
- Pipeline history (last 15 runs)

### Data Analysis Tabs
1. Sales Journal - Main transaction view
2. Detail by Ticket - Line-item analysis
3. Out of Balance - Balance validation
4. 1140 Research - Account-specific research
5. Pipeline Control - Workflow management
6. Tieout Management - Reconciliation testing
7. Pipeline History - Audit trail
8. Documentation - User guides
9. Debug Tools - Technical diagnostics

### State Management
- Shared filters across all tabs
- Auto-reset logic (batch_id updates when batch_type/is_proof changes)
- Cache invalidation on filter changes
- Real-time pipeline status updates

---

## Related Documentation

- **Architecture**: `./architecture/` - System design and data flow
- **Deployment**: `./deployment/` - Deployment guides and runbooks
- **Operations**: `./operations/` - Monitoring and troubleshooting
- **ALB OIDC Auth**: `../app-portal/architecture/alb-oidc-authentication.md`

---

## Repository

**Location**: `/Users/TehFiestyGoat/da-agent-hub/react-sales-journal/`
**Production Branch**: `hotfix/alb-oidc-authentication`
**Deployment**: Automated via Docker + AWS ECS

---

**Last Updated**: 2025-10-07
**Status**: Production (v1.0)
