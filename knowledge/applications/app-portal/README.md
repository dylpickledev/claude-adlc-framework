# App Portal - Application Launcher

**Production URL**: https://apps.grc-ops.com
**Status**: ✅ Production (deployed 2025-10-06)
**Stack**: React + TypeScript + Vite + Python FastAPI + nginx + supervisor

---

## Overview

The App Portal is GraniteRock's centralized authentication hub and application launcher. It provides Azure AD single sign-on for all internal web applications and serves as the entry point to the analytics platform.

### Key Features

- **Azure AD SSO**: Infrastructure-level OIDC authentication via ALB
- **Application Launcher**: Card-based interface for accessing internal tools
- **User Management**: Real user credentials from Azure AD (name, email)
- **Secure Logout**: Complete session termination (ALB + Azure AD)
- **Responsive Design**: Mobile-friendly interface

---

## Architecture

### System Design

```
┌─────────────────────────────────────────────────────────────┐
│                     AWS Application Load Balancer            │
│                    (apps.grc-ops.com)                        │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Priority 7: /* (catch-all)                          │   │
│  │   → Authenticate-OIDC (Azure AD)                    │   │
│  │   → ECS Fargate: app-portal service                │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
                ┌────────────────────────┐
                │  ECS Fargate Task      │
                │  (Multi-Service)       │
                │                        │
                │  ┌──────────────────┐ │
                │  │ nginx (port 80)  │ │
                │  │ Serves React SPA │ │
                │  └──────────────────┘ │
                │           ↓            │
                │  ┌──────────────────┐ │
                │  │ Python FastAPI   │ │
                │  │ (port 8080)      │ │
                │  │                  │ │
                │  │ /api/auth/user   │ │
                │  │ /api/logout      │ │
                │  └──────────────────┘ │
                │           ↓            │
                │  ┌──────────────────┐ │
                │  │ supervisor       │ │
                │  │ Process Manager  │ │
                │  └──────────────────┘ │
                └────────────────────────┘
```

### Multi-Service Container Pattern

**Key Innovation**: Single container running multiple services
- nginx serves React SPA (port 80)
- Python API handles backend logic (port 8080)
- supervisor manages both processes
- nginx proxies `/api/*` to Python backend

**Benefits**:
- Simplified deployment (one container)
- Shared filesystem for static assets
- Lower resource overhead than separate containers
- Easier local development parity

---

## Technology Stack

**Frontend**:
- React 18 + TypeScript
- Vite (build tool)
- styled-components (CSS-in-JS)
- Framer Motion (animations)

**Backend API**:
- Python 3.11
- FastAPI (web framework)
- JWT decoding for ALB OIDC headers

**Infrastructure**:
- AWS ECS Fargate (multi-service container)
- AWS ALB (load balancing + OIDC authentication)
- Azure AD (identity provider)
- Docker + supervisor (multi-process container)

---

## Authentication Flow

### Login Process

```
1. User → apps.grc-ops.com
2. ALB → No auth cookie found
3. ALB → Redirect to Azure AD (authenticate-oidc action)
4. User → Authenticates with Azure AD credentials
5. Azure AD → Redirects back to ALB with authorization code
6. ALB → Exchanges code for tokens, sets AWSELBAuthSessionCookie
7. ALB → Injects x-amzn-oidc-data header (JWT)
8. App → Loads React SPA
9. React → Calls /api/auth/user
10. Python API → Decodes JWT from ALB header
11. API → Returns { name, email, sub, authenticated: true }
12. React → Displays user info in UI
```

### Logout Process

**Challenge**: ALB sets HTTP-only cookies that JavaScript cannot clear

**Solution**: Backend-assisted logout
```
1. User → Clicks logout button
2. React → Redirects to /api/logout
3. Python API → Sets expired cookies (AWSELBAuthSessionCookie-0 through -3)
4. Python API → Redirects to Azure AD logout endpoint
5. Azure AD → Clears IdP session
6. Azure AD → Redirects back to apps.grc-ops.com
7. ALB → No valid session → Triggers re-authentication
```

---

## Key Technical Patterns

### ALB OIDC Authentication
See detailed documentation: `./architecture/alb-oidc-authentication.md`

**Highlights**:
- No client-side auth libraries (no Amplify, no Cognito)
- Infrastructure-level authentication
- Zero auth logic in React application
- HTTP-only cookie logout workaround

### Multi-Stage Docker Build

```dockerfile
# Stage 1: Build React app
FROM node:18-alpine AS build
WORKDIR /app
RUN npm ci && npm run build

# Stage 2: Production image
FROM python:3.11-slim
RUN apt-get update && apt-get install -y nginx supervisor

# Python API
COPY api/ /app/
RUN pip install -r /app/requirements.txt

# React build
COPY --from=build /app/dist /usr/share/nginx/html/

# Configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY supervisord.conf /etc/supervisor/conf.d/

EXPOSE 80
CMD ["/usr/bin/supervisord"]
```

---

## Deployed Applications

### Current Apps
- **Sales Journal**: Financial data analysis and reconciliation
- **Future Apps**: Additional analytics tools will be added

### Adding New Applications

1. Add application card to App Portal UI
2. Configure ALB rule with appropriate priority
3. Deploy application to ECS or Lambda
4. Ensure ALB rule has authenticate-oidc action
5. Test navigation and authentication

---

## Related Documentation

- **ALB OIDC Deep Dive**: `./architecture/alb-oidc-authentication.md`
- **Deployment Guide**: `./deployment/production-deploy.md`
- **Multi-Service Docker**: `./architecture/multi-service-containers.md`
- **Troubleshooting**: `./operations/troubleshooting.md`

---

## Repository

**Location**: `/Users/TehFiestyGoat/da-agent-hub/da-agent-hub/repos/front_end/da-app-portal/`
**Branch**: `master`
**Deployment**: Automated via Docker + AWS ECS

---

## Production Configuration

**AWS Account**: 129515616776
**Region**: us-west-2
**Cluster**: skynet-apps-cluster
**Service**: app-portal
**Task Definition**: app-portal:9

**Container**:
- Image: `app-portal@sha256:c36309405e0156...`
- CPU: 256
- Memory: 512 MB
- Port: 80
- Health Check: HTTP / (200 OK)

---

**Last Updated**: 2025-10-07
**Status**: Production (v1.0)
