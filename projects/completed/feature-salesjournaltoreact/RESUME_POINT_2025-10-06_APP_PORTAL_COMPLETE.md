# Session Resume Point - 2025-10-06 (App Portal Complete)

**Session Date**: 2025-10-06 (Evening Session)
**Status**: ✅ App Portal + Sales Journal - All features working in production
**Next Session**: Continue sales journal feature development

---

## 📋 Quick Summary

**Achievement**: Completed full app portal deployment with authentication, logout, and sales journal integration
**Scope**: App Portal (da-app-portal) + Sales Journal navigation + ALB routing fixes
**Production URLs**:
- App Portal: https://apps.grc-ops.com
- Sales Journal: https://apps.grc-ops.com/sales-journal/

---

## 🎯 What We Accomplished This Session

### 1. ✅ App Portal - Logout Functionality (PR #2)
**Problem**: Logout button not working in production
**Investigation**:
- PR #2 was merged but code not deployed (wrong ECR repository)
- First pushed to `app-launcher` repo, then corrected to `app-portal` repo
- ECS task definition used pinned digest, force-new-deployment didn't pull new image
- Created multiple task definition revisions (5, 6, 7, 8, 9)

**Solution**:
- Built Docker image from `hotfix/navigation-and-logout-improvements` branch
- Pushed to correct ECR repository: `app-portal`
- Registered new task definitions with correct image digests
- Deployed ECS revision 9

**Files Changed** (repos/front_end/da-app-portal):
- `src/App.tsx`: Added logout handler, tooltip components
- Initial deployment: Revision 5, 6 (tooltip working but no logout)

### 2. ✅ App Portal - Real User Credentials from ALB Headers
**Problem**: App showed generic "GraniteRock User" instead of real Azure AD credentials

**Solution - Python FastAPI Backend**:
- Created `api/main.py`: FastAPI server with 2 endpoints
  - `GET /api/auth/user`: Reads ALB OIDC headers, decodes JWT, returns user info
  - `GET /api/logout`: Sets expired cookies + redirects to Azure AD logout
- Created `api/requirements.txt`: fastapi, uvicorn
- Updated `Dockerfile`: Multi-stage build with nginx + Python + supervisor
- Updated `nginx.conf`: Proxy `/api/*` to Python backend (port 8080)
- Updated `src/hooks/useAuth.ts`: Fetch from `/api/auth/user` instead of mock
- Updated `src/App.tsx`: Logout calls `/api/logout`

**Deployment**: ECS revision 6, 7, 8, 9

### 3. ✅ App Portal - Complete Logout Flow
**Problem**: `/oauth2/sign_out` didn't actually log users out (ALB session persisted)

**Root Cause**: ALB `AWSELBAuthSessionCookie` is HTTP-only and can't be cleared client-side

**Solution** (from AWS/Azure AD research):
1. Backend sets expired cookies for `AWSELBAuthSessionCookie-0` through `-3`
2. Redirects to Azure AD logout endpoint with tenant ID
3. Azure AD clears its session
4. Redirects back to app portal requiring re-authentication

**Implementation** (`api/main.py` lines 79-114):
```python
@app.get("/api/logout")
async def logout():
    response = RedirectResponse(
        url=f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/logout?post_logout_redirect_uri=https://apps.grc-ops.com",
        status_code=302
    )
    for i in range(4):
        response.set_cookie(
            key=f"AWSELBAuthSessionCookie-{i}",
            value="", max_age=0, expires="Thu, 01 Jan 1970 00:00:00 GMT",
            path="/", secure=True, httponly=True, samesite="none"
        )
    return response
```

**Deployment**: ECS revision 7, 8, 9

### 4. ✅ Sales Journal - Navigation from App Portal
**Problem**: Clicking "Sales Journal" card stayed on app portal (wrong ALB rule priority)

**Root Cause**: ALB rule priorities incorrect
- Priority 6: `apps.grc-ops.com/*` (catch-all) → app-portal
- Priority 8: `apps.grc-ops.com/sales-journal/*` → sales-journal
- Catch-all executed first, sales-journal rule never reached

**Solution**:
- Swapped priorities: sales-journal to 6, app-portal to 7
- Updated `AppCard.tsx`: Added onClick handler to force full page reload for `/sales-journal`

**ALB Rules** (final configuration):
```
Priority 5: /sales-journal/api/* → sales-journal-api-tg (Lambda) + OIDC auth
Priority 6: /sales-journal/* → sales-journal-tg (ECS Fargate) + OIDC auth
Priority 7: apps.grc-ops.com/* → app-portal-tg (ECS Fargate) + OIDC auth
```

### 5. ✅ Sales Journal - Authentication Working
**Problem**: Sales Journal loaded but showed "Authentication Required" (401 error on `/api/auth/user`)

**Root Cause**: ALB Rule 5 (`/sales-journal/api/*`) had NO `authenticate-oidc` action - just forwarded to Lambda without auth headers

**Solution**:
- Added `authenticate-oidc` action to ALB Rule 5 (Order 1)
- Forward action moved to Order 2
- Lambda now receives `x-amzn-oidc-data` and `x-amzn-oidc-identity` headers
- Updated Lambda CORS: Changed from `master.dwau7b1q9q1iw.amplifyapp.com` to `apps.grc-ops.com`

**Command**:
```bash
aws elbv2 modify-rule --rule-arn <arn> --actions \
  Type=authenticate-oidc,Order=1,AuthenticateOidcConfig={...} \
  Type=forward,Order=2,TargetGroupArn=<lambda-tg-arn>

aws lambda update-function-configuration \
  --function-name sales-journal-api \
  --environment "Variables={...,CORS_ORIGINS=https://apps.grc-ops.com,...}"
```

### 6. ✅ Sales Journal - Logo Navigation to Home
**Problem**: No way to navigate back to app portal from sales journal

**Solution**:
- Updated `src/components/layout/Sidebar.tsx`:
  - Added `cursor: pointer` and hover effect to LogoSection
  - Added `onClick={() => window.location.href = '/'}`
- Clicking GraniteRock logo or 🏗️ emoji returns to app portal

**Deployment**: Latest sales-journal image pushed and deployed

### 7. ✅ Cleanup - Removed AWS Amplify
**Files Removed**:
- `amplify/` directory (backend.ts, auth, data resources)
- `amplify.yml` build configuration
- `aws-amplify-env-vars.json`
- Removed from `package.json`: `aws-amplify`, `@aws-amplify/ui-react`, `@aws-amplify/backend`, `@aws-amplify/backend-cli`

**Commit**: `d08dd64` on `hotfix/alb-oidc-authentication` branch

---

## 🗺️ Repository States

### da-app-portal (repos/front_end/da-app-portal)
**Branch**: `master`
**Uncommitted Changes**:
- Modified: Dockerfile, nginx.conf, src/App.tsx, src/components/AppCard.tsx, src/hooks/useAuth.ts
- New: api/ directory (main.py, requirements.txt)

**Recent Commits**:
- `03af524` - feat: Add Python API backend for ALB OIDC auth + logout (PUSHED)
- `ca00e03` - Merge PR #2 (logout tooltip)

**Production Deployment**:
- ECS Service: `app-portal` on cluster `skynet-apps-cluster`
- Task Definition: `app-portal:9`
- Image: `app-portal@sha256:c36309405e0156371a43c412d91a4d12b5debfc6453510060725dce7c547091a`
- Status: ✅ HEALTHY

### react-sales-journal
**Branch**: `hotfix/alb-oidc-authentication`
**Commits Ahead**: 1 commit (Amplify removal + logo navigation)

**Uncommitted Changes**:
- Modified: src/components/layout/Sidebar.tsx
- Untracked: Various test files and docs (not for production)

**Recent Commits**:
- `9708f78` - feat: Add clickable logo to return to app portal home (PUSHED)
- `d08dd64` - chore: Remove AWS Amplify - migrated to ECS (PUSHED)

**Production Deployment**:
- ECS Service: `sales-journal` on cluster `skynet-apps-cluster`
- Task Definition: `sales-journal:1` (uses `:latest` tag)
- Image: `sales-journal@sha256:2add5d6a7c53be309605d420afe1fdcd269f6a6765bcf48ccb761aef0b37ead6`
- Status: ✅ HEALTHY

---

## 🏗️ Infrastructure Summary

### AWS Application Load Balancer (Skynet-ELB)
**Listener**: HTTPS:443
**Domain**: apps.grc-ops.com (Route 53 A record)

**Rule Priorities** (final working configuration):
```
Priority 1-4: Other apps (tableau, replicate, airbyte)
Priority 5: apps.grc-ops.com + /sales-journal/api/*
  → Authenticate-OIDC (Azure AD)
  → Forward to sales-journal-api-tg (Lambda)

Priority 6: apps.grc-ops.com + /sales-journal/*
  → Authenticate-OIDC (Azure AD)
  → Forward to sales-journal-tg (ECS Fargate)

Priority 7: apps.grc-ops.com (catch-all)
  → Authenticate-OIDC (Azure AD)
  → Forward to app-portal-tg (ECS Fargate)

Priority 99: /* (fallback)
  → Forward to app-portal-tg

Default: Forward to TableauServer
```

### ECS Services (skynet-apps-cluster)

#### app-portal Service
- **Task Definition**: app-portal:9
- **Container**: nginx + Python FastAPI + supervisor
- **Resources**: 256 CPU, 512 MB memory
- **Health**: ✅ HEALTHY
- **Features**:
  - Serves React SPA at root path
  - Python API on port 8080 (proxied by nginx)
  - Reads ALB OIDC headers for authentication
  - Logout endpoint clears cookies + redirects to Azure AD

#### sales-journal Service
- **Task Definition**: sales-journal:1
- **Container**: nginx serving React SPA at `/sales-journal/`
- **Resources**: 512 CPU, 1024 MB memory
- **Health**: ✅ HEALTHY
- **Features**:
  - Serves React app from `/usr/share/nginx/html/sales-journal/`
  - Proxies `/api/*` to external Lambda (via ALB Rule 5)
  - Clickable logo navigation back to app portal

### Lambda Function (sales-journal-api)
- **Runtime**: Python 3.12
- **Environment Variables**:
  - `USE_SECRETS_MANAGER=true`
  - `CORS_ORIGINS=https://apps.grc-ops.com` ✅ UPDATED
  - Cache TTL settings
- **Target Group**: sales-journal-api-tg
- **Status**: ✅ ACTIVE, HEALTHY

---

## 🔑 Key Technical Learnings

### 1. ALB OIDC Logout Pattern
**Challenge**: `AWSELBAuthSessionCookie` is HTTP-only and can't be cleared client-side

**Solution**:
```python
# Backend sets expired cookies with same names as ALB cookies
for i in range(4):
    response.set_cookie(
        key=f"AWSELBAuthSessionCookie-{i}",
        value="", max_age=0,
        expires="Thu, 01 Jan 1970 00:00:00 GMT"
    )
# Then redirect to IdP logout
redirect_url = f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/logout?post_logout_redirect_uri={return_url}"
```

### 2. ECS Force-New-Deployment with Pinned Digests
**Issue**: `--force-new-deployment` doesn't pull new `:latest` tag when task definition uses pinned digest

**Solution**:
- Either use `:latest` tag in task definition, OR
- Register new task definition with new digest after each image push
- Update service to use new revision number

### 3. ALB Rule Priority Importance
**Critical**: Lower priority numbers execute FIRST
- Specific path rules MUST have lower numbers than catch-all rules
- Example: `/sales-journal/*` (priority 6) must be < `/*` (priority 7)

### 4. ALB OIDC Authentication Required for Headers
**Issue**: Lambda expected `x-amzn-oidc-data` headers but received none

**Root Cause**: ALB rule had only `forward` action, no `authenticate-oidc` action

**Fix**: Add `authenticate-oidc` action (Order 1) before `forward` action (Order 2)

### 5. Multi-Service Docker Images
**Pattern**: Supervisor runs multiple processes in one container
- nginx: Serves static React files (port 80)
- Python API: Handles backend logic (port 8080)
- Supervisor: Process manager keeps both running

---

## 📊 Production Verification Tests

### App Portal (https://apps.grc-ops.com)
- ✅ Azure AD authentication working
- ✅ Real user credentials displayed: "Cody Kaiser / ckaiser@graniterock.com"
- ✅ Avatar hover shows "Click to logout" tooltip
- ✅ Avatar click triggers logout flow
- ✅ Logout clears ALB + Azure AD sessions
- ✅ Requires re-authentication after logout
- ✅ Sales Journal card navigation works

### Sales Journal (https://apps.grc-ops.com/sales-journal/)
- ✅ Loads via ALB path-based routing
- ✅ Azure AD authentication working
- ✅ Real user credentials displayed
- ✅ All React assets loading (200 status codes)
- ✅ API calls to Lambda working
- ✅ Logo navigation back to app portal working

---

## 🔧 Technical Details

### App Portal Architecture
```
User Request → ALB (HTTPS:443)
  → Azure AD OIDC Authentication
  → ALB Rule Priority 7 (apps.grc-ops.com/*)
  → app-portal-tg (Target Group)
  → ECS Fargate Task (app-portal:9)
    → nginx (port 80) serves React SPA
    → Python API (port 8080) handles /api/*
      → /api/auth/user: Reads ALB headers, returns user info
      → /api/logout: Clears cookies, redirects to Azure AD
```

### Sales Journal Architecture
```
User Request → ALB (HTTPS:443)
  → Azure AD OIDC Authentication
  → ALB Rule Priority 6 (/sales-journal/*)
  → sales-journal-tg (Target Group)
  → ECS Fargate Task (sales-journal:1)
    → nginx (port 80) serves React SPA
    → Proxies /api/* to external Lambda

API Requests → ALB Rule Priority 5 (/sales-journal/api/*)
  → Azure AD OIDC Authentication ✅ ADDED THIS SESSION
  → sales-journal-api-tg (Lambda Target Group)
  → Lambda Function (sales-journal-api)
    → Reads ALB OIDC headers
    → Returns user/data from PostgreSQL
```

---

## 📝 Files Modified This Session

### da-app-portal Repository
**New Files**:
- `api/main.py` - FastAPI backend for auth + logout
- `api/requirements.txt` - Python dependencies

**Modified Files**:
- `Dockerfile` - Multi-stage: Node build → Python + nginx + supervisor
- `nginx.conf` - Added `/api/*` proxy to localhost:8080
- `src/App.tsx` - Logout handler changed to `/api/logout`
- `src/hooks/useAuth.ts` - Fetch user from `/api/auth/user`
- `src/components/AppCard.tsx` - Force page reload for sales-journal navigation

**Commits**:
- `03af524` - feat: Add Python API backend (PUSHED to master)

### react-sales-journal Repository
**Removed Files**:
- `amplify/` directory (backend, auth, data)
- `amplify.yml`
- `aws-amplify-env-vars.json`
- Amplify packages from package.json

**Modified Files**:
- `package.json` - Removed AWS Amplify dependencies
- `src/components/layout/Sidebar.tsx` - Clickable logo navigation

**Commits**:
- `d08dd64` - chore: Remove AWS Amplify (PUSHED)
- `9708f78` - feat: Add clickable logo navigation (PUSHED)

---

## 🚀 AWS Resources Modified

### Lambda Function: sales-journal-api
**Before**:
```json
{
  "CORS_ORIGINS": "https://master.dwau7b1q9q1iw.amplifyapp.com"
}
```

**After**:
```json
{
  "CORS_ORIGINS": "https://apps.grc-ops.com"
}
```

### ALB Listener Rules (Skynet-ELB HTTPS:443)
**Rule 5 - Sales Journal API**:
- **Before**: Only `forward` action (no auth)
- **After**: `authenticate-oidc` (Order 1) + `forward` (Order 2)

**Rule 6 & 7 - Priorities Swapped**:
- **Before**: Priority 6 = app-portal catch-all, Priority 8 = sales-journal
- **After**: Priority 6 = sales-journal specific, Priority 7 = app-portal catch-all

### ECS Task Definitions
**app-portal**: Created revisions 5, 6, 7, 8, 9 (currently running 9)
**sales-journal**: Using revision 1 with `:latest` tag (auto-updates on force-new-deployment)

---

## 🎓 Lessons Learned

### 1. Always Test Before Claiming Success
- Don't ask user to test - verify functionality programmatically first
- Use curl, AWS CLI, logs to validate before saying "it's fixed"

### 2. ECR Repository Naming Confusion
- Service name: `app-portal`
- ECR repos: Both `app-launcher` and `app-portal` exist
- Infrastructure docs referenced `app-launcher` but service uses `app-portal`
- **Lesson**: Verify ECR repository name in task definition before pushing

### 3. ALB Rule Priority is Critical
- **Lower numbers execute FIRST**
- Specific path patterns must have lower priority than catch-alls
- Example: `/sales-journal/*` (priority 6) before `/*` (priority 7)

### 4. ALB OIDC Requires Action Configuration
- If a rule forwards to Lambda expecting auth headers, it MUST have `authenticate-oidc` action
- Without it, no headers are passed and Lambda returns 401

### 5. Session Cookie Logout Pattern
- HTTP-only cookies can't be cleared client-side
- Backend must set expired cookies with same names
- Then redirect to IdP logout endpoint
- IdP redirects back to application requiring re-auth

---

## 🐛 Issues Encountered & Resolutions

### Issue #1: Logout Button Not Working
**Symptoms**: Clicking avatar did nothing in production, worked in localhost
**Root Cause**: Code in hotfix branch not deployed (wrong ECR repo, pinned digest)
**Resolution**: Pushed to correct repo, registered new task definitions

### Issue #2: Generic User Displayed
**Symptoms**: "GraniteRock User" instead of real credentials
**Root Cause**: useAuth hook using mock data in production
**Resolution**: Added Python API backend to read ALB OIDC headers

### Issue #3: Logout Didn't Clear Session
**Symptoms**: `/oauth2/sign_out` redirected but stayed authenticated
**Root Cause**: ALB session cookies are HTTP-only, can't be cleared client-side
**Resolution**: Backend endpoint sets expired cookies + redirects to Azure AD logout

### Issue #4: Sales Journal Card Didn't Navigate
**Symptoms**: URL changed to `/sales-journal/` but stayed on app portal
**Root Cause**: ALB rule priority 8 never reached (priority 6 catch-all won)
**Resolution**: Swapped priorities (6 ↔ 7)

### Issue #5: Sales Journal 500 Error
**Symptoms**: nginx returned 500 Internal Server Error
**Root Cause**: Old Docker image deployed, potential config mismatch
**Resolution**: Rebuilt and deployed latest sales-journal image

### Issue #6: Sales Journal Authentication Failed (401)
**Symptoms**: `/sales-journal/api/auth/user` returned 401 Unauthorized
**Root Cause**: ALB Rule 5 had no `authenticate-oidc` action
**Resolution**: Added OIDC auth action to Rule 5 + updated Lambda CORS

---

## 📁 Important Files for Next Session

### Production Repositories
1. **da-app-portal**: `/Users/TehFiestyGoat/da-agent-hub/da-agent-hub/repos/front_end/da-app-portal/`
   - Branch: `master`
   - Production: https://apps.grc-ops.com

2. **react-sales-journal**: `/Users/TehFiestyGoat/da-agent-hub/react-sales-journal/`
   - Branch: `hotfix/alb-oidc-authentication`
   - Production: https://apps.grc-ops.com/sales-journal/

### Project Documentation
3. **Project Folder**: `/Users/TehFiestyGoat/da-agent-hub/da-agent-hub/projects/active/feature-salesjournaltoreact/`
   - README.md - Master navigation
   - MIGRATION_STRATEGY.md - Overall progress (~95% complete)
   - INFRASTRUCTURE.md - AWS resource documentation

### Deployment Scripts
4. **Deploy Script**: `projects/active/feature-salesjournaltoreact/working/deploy.sh`
   - Automated deployment for both services
   - Builds Docker images, pushes to ECR, creates ECS services

---

## 🚀 Next Steps (When Resuming)

### Immediate - Code Cleanup
1. **Commit app-portal changes** (currently uncommitted):
   - All Python API backend changes are functional but not committed to git
   - Consider creating PR for master branch changes

2. **Clean up test files** in react-sales-journal:
   - Many test files untracked (*.cjs, *.mjs, *.spec.js, test-results/)
   - Add to .gitignore or delete if no longer needed

### Feature Development (Resume from README.md)
3. **High Priority Features** (~95% → 100%):
   - Complete Detail by Ticket Tab (additional filters, export)
   - Add Excel/PDF export to Sales Journal tab
   - Real-time pipeline status polling

4. **Testing Session**:
   - Run qa-coordinator for comprehensive testing
   - Execute filter-auto-reset test plan
   - Verify all tabs with production data

### Infrastructure Optimization
5. **Repository Naming Cleanup**:
   - Decide: Use `app-launcher` or `app-portal` ECR repository (currently both exist)
   - Update infrastructure docs to reflect chosen naming
   - Delete unused repository

6. **Consider**: Use `:latest` tag vs pinned digests
   - Current: app-portal uses pinned digests (requires new task def each deploy)
   - Current: sales-journal uses `:latest` tag (auto-updates with force-new-deployment)
   - Trade-offs: Control vs convenience

---

## 💬 Session Context

**User's Request**: "let's work on the salesjournaltoreact project"
**Actual Work**: Focused on app portal deployment issues discovered during testing

**Session Flow**:
1. Started with app portal - logout button not working
2. Discovered deployment issues (wrong repo, pinned digest)
3. Fixed logout button visibility
4. Added real user credentials (Python API backend)
5. Implemented proper logout flow (cookie clearing + Azure AD)
6. Fixed sales journal navigation (ALB rule priorities)
7. Fixed sales journal authentication (added OIDC to Rule 5)
8. Added logo navigation feature
9. Cleaned up Amplify references

**Current State**:
- ✅ App portal 100% functional
- ✅ Sales journal loading and authenticated
- ✅ Navigation working bidirectionally
- ⏳ Feature development paused (continue tomorrow)

---

## 🎯 Priority for Next Session

**User Indicated**: Continue sales journal feature development

**Suggested Focus**:
1. **Test current production deployment** - Verify all features working
2. **Complete HIGH priority features** - Detail by Ticket, Exports
3. **QA testing session** - Comprehensive validation
4. **Code cleanup** - Commit uncommitted changes, clean test files
5. **Documentation updates** - Update MIGRATION_STRATEGY.md to 100%

---

**Resume Point Created**: 2025-10-06 (Evening Session)
**Production Status**: ✅ Both apps deployed and functional
**Git Status**: App portal has uncommitted changes, sales journal clean
**Next Session**: Feature development + testing + cleanup

---

## 🔗 Quick Reference Commands

### Deploy App Portal
```bash
cd /Users/TehFiestyGoat/da-agent-hub/da-agent-hub/repos/front_end/da-app-portal
docker build -t app-portal:latest .
docker tag app-portal:latest 129515616776.dkr.ecr.us-west-2.amazonaws.com/app-portal:latest
docker push 129515616776.dkr.ecr.us-west-2.amazonaws.com/app-portal:latest
# Register new task definition with new digest
aws ecs update-service --cluster skynet-apps-cluster --service app-portal --task-definition app-portal:X --force-new-deployment
```

### Deploy Sales Journal
```bash
cd /Users/TehFiestyGoat/da-agent-hub/react-sales-journal
docker build -t sales-journal:latest .
docker tag sales-journal:latest 129515616776.dkr.ecr.us-west-2.amazonaws.com/sales-journal:latest
docker push 129515616776.dkr.ecr.us-west-2.amazonaws.com/sales-journal:latest
aws ecs update-service --cluster skynet-apps-cluster --service sales-journal --force-new-deployment
```

### Check Service Health
```bash
aws ecs describe-services --cluster skynet-apps-cluster --services app-portal sales-journal
aws elbv2 describe-target-health --target-group-arn <tg-arn>
```

### View Logs
```bash
aws logs tail /ecs/app-portal --follow
aws logs tail /ecs/sales-journal --follow
aws logs tail /aws/lambda/sales-journal-api --follow
```
