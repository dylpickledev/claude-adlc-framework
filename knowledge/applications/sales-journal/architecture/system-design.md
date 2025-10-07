# Sales Journal - System Architecture

**Application**: Sales Journal
**Production**: https://apps.grc-ops.com/sales-journal/
**Status**: ✅ Production (v1.0)

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        User Browser                                  │
│                    (Azure AD Authenticated)                          │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   AWS Application Load Balancer                      │
│                      (apps.grc-ops.com)                              │
│                                                                       │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │ Priority 5: /sales-journal/api/*                           │    │
│  │   Action 1: authenticate-oidc (Azure AD)                   │    │
│  │   Action 2: forward → sales-journal-api-tg (Lambda)        │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                       │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │ Priority 6: /sales-journal/*                               │    │
│  │   Action 1: authenticate-oidc (Azure AD)                   │    │
│  │   Action 2: forward → sales-journal-tg (ECS)               │    │
│  └────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
                │                                  │
                │                                  │
       ┌────────▼────────┐              ┌─────────▼──────────┐
       │  ECS Fargate    │              │  Lambda Function    │
       │  Task           │              │  sales-journal-api  │
       │                 │              │                     │
       │  nginx (port 80)│              │  Python 3.12        │
       │  Serves React   │              │  FastAPI            │
       │  from /sales-   │              │  1024 MB            │
       │  journal/       │              │  30s timeout        │
       │                 │              │                     │
       │  CPU: 512       │              └─────────┬──────────┘
       │  Memory: 1024MB │                        │
       └─────────────────┘                        │
                                                  │
                                    ┌─────────────▼────────────────┐
                                    │    External Services         │
                                    │                              │
                                    │  • PostgreSQL RDS            │
                                    │    (financial data)          │
                                    │                              │
                                    │  • Orchestra API             │
                                    │    (pipeline orchestration)  │
                                    │                              │
                                    │  • AWS Secrets Manager       │
                                    │    (database credentials)    │
                                    └──────────────────────────────┘
```

---

## Component Details

### Frontend (ECS Fargate)

**Container**: nginx serving React SPA
**Image**: `129515616776.dkr.ecr.us-west-2.amazonaws.com/sales-journal:latest`
**Resources**: 512 CPU units, 1024 MB memory
**Port**: 80 (HTTP)
**Base Path**: `/sales-journal/`

**Technology**:
- React 18 + TypeScript
- Vite (build tool)
- Zustand (state management)
- styled-components (CSS-in-JS)
- Framer Motion (animations)
- Recharts (charts)

**Key Features**:
- 10-tab interface for financial analysis
- Real-time dashboard with status cards
- Filter persistence across tabs
- Export functionality (CSV, Excel, PDF)
- Pipeline trigger controls

### Backend API (Lambda)

**Function**: `sales-journal-api`
**Runtime**: Python 3.12
**Memory**: 1024 MB
**Timeout**: 30 seconds
**Handler**: `main.handler`

**Technology**:
- FastAPI (web framework)
- psycopg2 (PostgreSQL driver)
- httpx (Orchestra API client)
- Mangum (ASGI adapter for Lambda)

**Environment Variables** (from Secrets Manager):
```
USE_SECRETS_MANAGER=true
CORS_ORIGINS=https://apps.grc-ops.com
CACHE_TTL_BALANCE=300
CACHE_TTL_DMS=300
CACHE_TTL_TIEOUT=300
CACHE_TTL_DROPDOWN=600
```

**API Endpoints**:
- `/api/auth/user` - User info from ALB headers
- `/api/status/*` - Dashboard status queries
- `/api/journal/*` - Journal data queries
- `/api/pipeline/*` - Orchestra integration

---

## Authentication Architecture

### ALB OIDC Flow

See comprehensive documentation: `../../app-portal/architecture/alb-oidc-authentication.md`

**Quick Summary**:
1. User requests `/sales-journal/`
2. ALB checks for `AWSELBAuthSessionCookie`
3. No cookie → Redirect to Azure AD
4. User authenticates → Azure AD redirects back with auth code
5. ALB exchanges code for tokens → Sets HTTP-only session cookie
6. ALB injects `x-amzn-oidc-data` header (JWT with user claims)
7. Request forwarded to ECS/Lambda with user identity

**Key Benefit**: React app has ZERO authentication code - all handled by ALB

---

## Data Flow

### Dashboard Load Sequence

```
1. User → /sales-journal/
2. React App Loads
3. financialStore.loadDashboardStatus()
   ├─→ GET /api/status/balance
   ├─→ GET /api/status/dms
   ├─→ GET /api/status/tieout
   └─→ GET /api/status/out-of-balance
4. Lambda queries PostgreSQL
5. Results cached (5 min TTL)
6. Response → React updates UI
```

### Pipeline Trigger Flow

```
1. User clicks "🔄 Refresh Sales Journal" button
2. Confirmation dialog appears
3. User confirms
4. POST /api/pipeline/trigger { pipeline_type: "refresh" }
5. Lambda → Orchestra API trigger endpoint
6. Orchestra starts pipeline run
7. Response: { run_id, status, pipeline_name }
8. React stores run_id in state
9. Status polling begins (optional - not yet implemented)
```

### Filter Update Flow

```
1. User changes batch_type from CASH → CREDIT
2. financialStore.updateSharedFilter('batch_type', 'CREDIT')
3. Filter auto-reset logic triggers:
   ├─→ Detect batch_type changed
   ├─→ GET /api/dropdown/batch-ids?batch_type=CREDIT&is_proof=Y
   ├─→ Lambda queries PostgreSQL for valid batch_ids
   ├─→ Response: ['All', '12345', '12344', ...]
   └─→ Auto-set batch_id to first non-'All' option
4. Cache invalidation for affected queries
5. All tabs re-render with new filters
```

---

## State Management Architecture

### Zustand Store: financialStore

**Purpose**: Single source of truth for all application state

**State Categories**:

1. **Shared Filters** (persist across tabs):
   - `batch_type`: 'CASH' | 'CREDIT' | 'INTRA'
   - `is_proof`: 'Y' | 'N'
   - `batch_id`: string | 'All'
   - `invalid_account`: string | 'All'
   - `accountcode`: string

2. **Dashboard Status**:
   - `balanceStatus`: Latest balance validation results
   - `dmsStatus`: DMS replication task status
   - `tieoutStatus`: Reconciliation test results
   - `outOfBalanceTotal`: Total out of balance amount
   - `outOfBalanceColor`: 'red' | 'green' | 'gray'

3. **Pipeline State**:
   - `pipelineStatus`: Current pipeline status
   - `pipelineHistory`: Last 15 pipeline runs
   - `pending_refresh`: Trigger in progress flag

4. **Data State**:
   - `journalData`: Sales journal entries
   - `detailData`: Detail by ticket records
   - `outOfBalanceData`: Out of balance records
   - `tieoutData`: Tieout test results

**Key Features**:
- Filter auto-reset when batch_type/is_proof changes
- Cache invalidation on filter updates
- Optimized data fetching (shared queries)
- Loading and error states per query

---

## Integration Points

### PostgreSQL Database

**Connection**: Via Lambda (not direct from React)
**Tables Used**:
- `dash_r245a_apex_sales_journal_review` - Main journal
- `dash_r245a_apex_sales_journal_review_detail` - Detail records
- `dash_r245a_apex_sales_journal_review_out_of_balance` - Balance validation
- `rpt_r245t_apex_sales_journal_tieout_app_only` - Tieout tests

**Access Pattern**: Lambda queries via psycopg2, results cached with TTL

### Orchestra API

**Base URL**: `https://app.getorchestra.io/api`
**Authentication**: API token in Secrets Manager

**Endpoints Used**:
- `POST /pipeline-runs/trigger` - Trigger pipeline execution
- `GET /pipeline-runs` - Pipeline history
- `GET /pipeline-runs/{id}` - Pipeline status details

**Pipeline IDs**:
- Refresh: `c468dd21-7af0-4892-9f48-d8cdf24d9b7d`
- Final: `daa39221-b30f-4b27-a8ee-a1b98ca28d0f`

---

## Security Architecture

### Authentication
- **Method**: ALB OIDC with Azure AD
- **User Identity**: Extracted from `x-amzn-oidc-data` JWT
- **Session**: HTTP-only cookies (AWSELBAuthSessionCookie)
- **Logout**: Backend-assisted (sets expired cookies + IdP redirect)

### Network Security
- **TLS**: All traffic HTTPS via ALB (certificate managed by AWS)
- **CORS**: Lambda configured for `https://apps.grc-ops.com` only
- **VPC**: Lambda in VPC for PostgreSQL access (private subnet)

### Secrets Management
- **Database Credentials**: AWS Secrets Manager
- **Orchestra API Token**: AWS Secrets Manager
- **Azure AD Client Secret**: Stored in ALB OIDC configuration

---

## Performance Characteristics

### Response Times
- **Static Assets**: < 100ms (served from ECS nginx)
- **API Calls (cached)**: < 200ms (in-memory cache hits)
- **API Calls (fresh)**: 500ms - 2s (database queries)
- **Pipeline Trigger**: 1-3s (Orchestra API latency)

### Caching Strategy
- **Dropdown Options**: 10 min TTL (batch_id, invalid_account)
- **Status Queries**: 5 min TTL (balance, DMS, tieout)
- **Journal Data**: No cache (user-driven queries)

### Resource Utilization
- **ECS Task**: ~200 MB memory (nginx + React assets)
- **Lambda**: ~150-300 MB memory per invocation
- **Cold Start**: ~1-2 seconds (Lambda first invocation)

---

## Scalability Considerations

### Current Capacity
- **ECS**: 1 task (sufficient for internal tool)
- **Lambda**: 1000 concurrent executions (AWS default)
- **ALB**: Handles 10K requests/second easily

### Auto-Scaling (Future)
- ECS can scale based on CPU/memory metrics
- Lambda scales automatically (no configuration needed)
- Database connection pooling required if scaling Lambda

---

## Related Documentation

- **Deployment Runbook**: `../deployment/production-deploy.md`
- **Operations Guide**: `../operations/monitoring.md`
- **Troubleshooting**: `../operations/troubleshooting.md`
- **ALB OIDC Pattern**: `../../app-portal/architecture/alb-oidc-authentication.md`

---

**Last Updated**: 2025-10-07
**Architecture Version**: 1.0
**Production Status**: ✅ Stable
