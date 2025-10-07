# Sales Journal AWS Deployment - Current Status
**Date**: 2025-10-04 22:55 PST
**Session**: Deployment to AWS ECS with Azure AD Authentication
**Status**: 🟡 Infrastructure Complete, Authentication Troubleshooting in Progress

---

## ✅ Completed Infrastructure

### Docker Images Built & Deployed
- **app-launcher**: `129515616776.dkr.ecr.us-west-2.amazonaws.com/app-launcher:latest`
  - SHA: `06e87006bc1ffbc7b3e18863be2c8c3ecfb71b9048466719804ee416f8de2db2`
  - Status: Running successfully

- **sales-journal**: `129515616776.dkr.ecr.us-west-2.amazonaws.com/sales-journal:latest`
  - SHA: `797b8c1f8084e4e7e834a3c2ef65b1d2c11780472f1490bf669ac0adf896887b`
  - Status: Running successfully (nginx DNS issue resolved)

### ECS Services Deployed
- **Cluster**: skynet-apps-cluster
- **Services**:
  - `app-launcher`: ACTIVE, 1/1 tasks running
  - `sales-journal`: ACTIVE, 1/1 tasks running, HEALTHY target

### AWS Infrastructure
- **Region**: us-west-2
- **VPC**: vpc-1900307e
- **Private Subnets**:
  - subnet-0164065d787727e01
  - subnet-c280cca5
- **Security Group**: sg-04e0e784d3140d98a (ecs-apps-sg)
  - Allows traffic from ALB security group
- **ALB**: Skynet-ELB
  - Security Group: sg-8069e5fb (allows all outbound)
  - Listener: Port 443 (HTTPS)

### Target Groups (Healthy)
- **app-launcher-tg**: `arn:aws:elasticloadbalancing:us-west-2:129515616776:targetgroup/app-launcher-tg/b6ce8e538c04aefb`
  - Health: Running

- **sales-journal-tg**: `arn:aws:elasticloadbalancing:us-west-2:129515616776:targetgroup/sales-journal-tg/fe4f6879199e4000`
  - Health: Healthy (192.168.6.40:80)

### ALB Listener Rules Configured
**Rule Priority 5** (Sales Journal):
```
Conditions:
  - Host: apps.grc-ops.com
  - Path: /sales-journal, /sales-journal/*
Actions:
  1. authenticate-oidc (Azure AD)
  2. forward to sales-journal-tg
```

**Rule Priority 6** (App Launcher):
```
Conditions:
  - Host: apps.grc-ops.com
Actions:
  1. authenticate-oidc (Azure AD)
  2. forward to app-launcher-tg
```

---

## 🟡 Current Blocker: Azure AD OIDC Authentication (561 Error)

### Problem
- Users successfully authenticate with Azure AD
- Authorization code is returned to ALB
- **ALB returns HTTP 561 error** when exchanging code for tokens
- URL: `https://apps.grc-ops.com/oauth2/idpresponse?code=...&state=...`

### Azure AD Configuration (CURRENT STATE)

**App Registration**: GraniteRock AWS Apps Portal
**Client ID**: `2f1463e8-52ce-499e-9296-4cd125f35f4e`
**Tenant ID**: `1d1bbedc-e179-4e6b-a55e-c500085f1eec`

#### ✅ Completed Azure AD Fixes
1. **Client Secret**: `***REMOVED***`
   - Stored in AWS Secrets Manager: `app-launcher/azure-ad-client-secret`
   - Expires: 10/4/2027
   - ✅ Updated in both ALB listener rules

2. **Redirect URI**: ✅ `https://apps.grc-ops.com/oauth2/idpresponse`
   - Configured in Authentication → Web platform

3. **API Permissions**: ✅ All granted
   - openid (37f7f235-527c-4136-accd-4a02d197296e)
   - email (64a6cdd6-aab1-4aaf-94b8-3cc8405e90d0)
   - profile (14dad69e-099b-42c9-810b-d002981feec1)
   - User.Read (e1fe6dd8-ba31-4d61-89e7-88639da4683d)

4. **Token Configuration**: ✅ All set correctly
   - `enableAccessTokenIssuance: true` ⚠️ **CRITICAL FIX**
   - `enableIdTokenIssuance: true`
   - `requestedAccessTokenVersion: 2`
   - `accessTokenAcceptedVersion: 2`

5. **Application ID URI**: ✅ `api://2f1463e8-52ce-499e-9296-4cd125f35f4e`
   - Set via "Expose an API" page

### ALB OIDC Configuration (CURRENT)
```
Issuer: https://login.microsoftonline.com/1d1bbedc-e179-4e6b-a55e-c500085f1eec/v2.0
Authorization Endpoint: https://login.microsoftonline.com/1d1bbedc-e179-4e6b-a55e-c500085f1eec/oauth2/v2.0/authorize
Token Endpoint: https://login.microsoftonline.com/1d1bbedc-e179-4e6b-a55e-c500085f1eec/oauth2/v2.0/token
UserInfo Endpoint: https://graph.microsoft.com/oidc/userinfo
Scope: openid email profile
Client ID: 2f1463e8-52ce-499e-9296-4cd125f35f4e
Client Secret: ***REMOVED***
```

### Investigation Summary

**Ruled Out Issues**:
- ❌ Network connectivity (ALB SG allows all outbound traffic)
- ❌ Wrong client secret (verified exact match from Azure Portal)
- ❌ Missing redirect URI (verified configured)
- ❌ Missing API permissions (all granted)
- ❌ ID tokens disabled (enabled)
- ❌ Wrong token version (v2.0 configured correctly)
- ❌ Access token issuance disabled (NOW ENABLED - critical fix)
- ❌ Missing Application ID URI (NOW SET)

**Next Troubleshooting Step**:
Check **Azure AD Sign-in Logs** for specific AADSTS error code:
1. Azure Portal → Azure Active Directory → Sign-in logs
2. Filter by Application ID: `2f1463e8-52ce-499e-9296-4cd125f35f4e`
3. Find failed authentication attempts
4. Get specific AADSTS error code

**Possible Remaining Issues**:
1. **DPoP (Demonstrating Proof-of-Possession)** enabled on tenant
   - AWS ALB doesn't support DPoP
   - Would need to disable DPoP or use custom Lambda authorizer
2. **Tenant-level Conditional Access policies** blocking token exchange
3. **Azure AD propagation delays** (app was just created today)
4. **Enterprise application not created** (auto-created on first sign-in, might have issues)

---

## 🔧 Technical Issues Resolved This Session

### Issue #1: Nginx DNS Resolution Failure
**Problem**: nginx tried to resolve API Gateway hostname at startup, failed in private subnets
**Error**: `nginx: [emerg] host not found in upstream "4gihwvts8c.execute-api.us-west-2.amazonaws.com"`

**Fix Applied** (nginx.conf:66-88):
```nginx
# Use AWS VPC DNS resolver for runtime resolution
resolver 169.254.169.253 valid=10s;

# Use variable to force runtime DNS resolution instead of startup
set $backend "4gihwvts8c.execute-api.us-west-2.amazonaws.com";

# Production API Gateway endpoint
proxy_pass https://$backend/api/;

proxy_set_header Host $backend;
```

**Result**: ✅ Nginx now starts successfully, ECS tasks healthy

### Issue #2: Docker Build Performance
**Problem**: Multi-stage Docker build with `npm install` took >10 minutes, timing out

**Fix Applied**:
1. Build React app locally: `VITE_BASE_PATH=/sales-journal npm run build` (8.56s)
2. Created `Dockerfile.simple` - nginx-only, copies pre-built dist
3. Created `.dockerignore.simple` - allows dist folder
4. Swap dockerignore files during build:
```bash
mv .dockerignore.simple .dockerignore && \
docker build -f Dockerfile.simple -t sales-journal:latest . && \
mv .dockerignore .dockerignore.simple && \
mv .dockerignore.full .dockerignore
```

**Result**: ✅ Docker builds complete in seconds instead of minutes

### Issue #3: Docker PATH Issues
**Problem**: `docker` and `docker-credential-desktop` not found in PATH

**Fix Applied** (deploy.sh):
```bash
DOCKER="/Applications/Docker.app/Contents/Resources/bin/docker"
export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"
```

**Result**: ✅ Docker commands work correctly, ECR push successful

---

## 📁 Files Modified This Session

### /Users/TehFiestyGoat/da-agent-hub/react-sales-journal/
- **nginx.conf** (lines 66-88): Added runtime DNS resolution
- **Dockerfile.simple** (new): Lightweight nginx-only Dockerfile
- **.dockerignore.simple** (new): Custom dockerignore allowing dist folder
- **DEPLOYMENT_SESSION_STATE.md** (new): Complete session state documentation

### /Users/TehFiestyGoat/da-agent-hub/da-agent-hub/.claude/agents/
- **azure-expert.md** (new, 18KB): Comprehensive Azure expertise agent
- **aws-expert.md** (pulled from main, 18KB): AWS expertise agent

### /Users/TehFiestyGoat/da-agent-hub/da-agent-hub/.claude/memory/patterns/
- **azure-patterns.md** (new, 32KB): Azure implementation patterns and troubleshooting

### /Users/TehFiestyGoat/da-agent-hub/da-agent-hub/knowledge/da-agent-hub/
- **azure-expert-documentation.md** (new, 13KB): Azure expert knowledge base
- **azure-quick-reference.md** (new, 13KB): Fast lookup reference for Azure

---

## 🔑 Access URLs

- **App Launcher**: https://apps.grc-ops.com
- **Sales Journal**: https://apps.grc-ops.com/sales-journal

**Current Status**: Both return HTTP 561 authentication error after Azure AD login

---

## 🚀 Quick Recovery Commands

### Build and Deploy Sales Journal
```bash
# Navigate to react-sales-journal
cd /Users/TehFiestyGoat/da-agent-hub/react-sales-journal

# Build React app locally
VITE_BASE_PATH=/sales-journal npm run build

# Build Docker image (with dockerignore swap)
bash -c 'export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH" && \
  mv .dockerignore.simple .dockerignore && \
  docker build -f Dockerfile.simple -t sales-journal:latest . && \
  mv .dockerignore .dockerignore.simple && \
  mv .dockerignore.full .dockerignore'

# Tag for ECR
bash -c 'export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH" && \
  docker tag sales-journal:latest 129515616776.dkr.ecr.us-west-2.amazonaws.com/sales-journal:latest'

# Login to ECR and push
bash -c 'export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH" && \
  aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 129515616776.dkr.ecr.us-west-2.amazonaws.com && \
  docker push 129515616776.dkr.ecr.us-west-2.amazonaws.com/sales-journal:latest'

# Force new ECS deployment
aws ecs update-service --cluster skynet-apps-cluster --service sales-journal --force-new-deployment --region us-west-2
```

### Monitor ECS Services
```bash
# Check service status
aws ecs describe-services --cluster skynet-apps-cluster --services app-launcher sales-journal --region us-west-2 --query 'services[*].{Name:serviceName,RunningCount:runningCount,DesiredCount:desiredCount,Status:status}' --output table

# Check target health
aws elbv2 describe-target-health --target-group-arn arn:aws:elasticloadbalancing:us-west-2:129515616776:targetgroup/sales-journal-tg/fe4f6879199e4000 --region us-west-2

# View CloudWatch logs
aws logs tail /ecs/sales-journal --follow --region us-west-2
aws logs tail /ecs/app-launcher --follow --region us-west-2
```

### Update ALB OIDC Configuration
```bash
# Update sales-journal listener rule (Priority 5)
aws elbv2 modify-rule \
  --rule-arn arn:aws:elasticloadbalancing:us-west-2:129515616776:listener-rule/app/Skynet-ELB/cc92401e4b4665d2/e20981587c6fe263/80d6abbff7f13191 \
  --region us-west-2 \
  --actions Type=authenticate-oidc,Order=1,AuthenticateOidcConfig='{
    Issuer=https://login.microsoftonline.com/1d1bbedc-e179-4e6b-a55e-c500085f1eec/v2.0,
    AuthorizationEndpoint=https://login.microsoftonline.com/1d1bbedc-e179-4e6b-a55e-c500085f1eec/oauth2/v2.0/authorize,
    TokenEndpoint=https://login.microsoftonline.com/1d1bbedc-e179-4e6b-a55e-c500085f1eec/oauth2/v2.0/token,
    UserInfoEndpoint=https://graph.microsoft.com/oidc/userinfo,
    ClientId=2f1463e8-52ce-499e-9296-4cd125f35f4e,
    ClientSecret=***REMOVED***,
    SessionCookieName=AWSELBAuthSessionCookie,
    Scope="openid email profile",
    SessionTimeout=43200,
    OnUnauthenticatedRequest=authenticate
  }' \
  Type=forward,Order=2,TargetGroupArn=arn:aws:elasticloadbalancing:us-west-2:129515616776:targetgroup/sales-journal-tg/fe4f6879199e4000
```

---

## 📋 Next Session Checklist

1. **Check Azure AD Sign-in Logs**
   - Get specific AADSTS error code
   - Identify exact reason for token exchange failure

2. **Verify Enterprise Application Created**
   - Azure AD → Enterprise Applications
   - Search for "GraniteRock AWS Apps Portal"
   - Check if auto-created during first sign-in

3. **Check for Conditional Access Policies**
   - Azure AD → Security → Conditional Access
   - Look for policies affecting the application
   - Check if DPoP is required

4. **Test Manual Token Exchange** (if needed)
   ```bash
   curl -X POST "https://login.microsoftonline.com/1d1bbedc-e179-4e6b-a55e-c500085f1eec/oauth2/v2.0/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "grant_type=authorization_code" \
     -d "client_id=2f1463e8-52ce-499e-9296-4cd125f35f4e" \
     -d "client_secret=***REMOVED***" \
     -d "code=AUTHORIZATION_CODE_FROM_URL" \
     -d "redirect_uri=https://apps.grc-ops.com/oauth2/idpresponse" \
     -d "scope=openid email profile"
   ```

5. **Enable ALB Access Logs** (if not already enabled)
   - Get detailed error messages beyond 561
   - Identify specific OAuth 2.0 error responses

6. **Contact Azure AD Administrator**
   - If all configs correct, may need tenant-level permissions
   - Check for org-wide policies blocking external OAuth apps

---

## 🎯 Success Criteria

Authentication will be considered working when:
1. ✅ User can access https://apps.grc-ops.com
2. ✅ Azure AD login completes successfully
3. ✅ No 561 error during token exchange
4. ✅ User sees App Launcher portal with Sales Journal tile
5. ✅ Clicking Sales Journal tile loads the application
6. ✅ All Sales Journal features work (data loading, filtering, export)

---

## 📚 Reference Documentation

### Created This Session
- Azure Expert Agent: `.claude/agents/azure-expert.md`
- Azure Patterns: `.claude/memory/patterns/azure-patterns.md`
- AWS Expert Agent: `.claude/agents/aws-expert.md` (pulled from main)
- Session State: `react-sales-journal/DEPLOYMENT_SESSION_STATE.md`

### AWS Resources
- ALB ARN: `arn:aws:elasticloadbalancing:us-west-2:129515616776:loadbalancer/app/Skynet-ELB/cc92401e4b4665d2`
- Listener ARN: `arn:aws:elasticloadbalancing:us-west-2:129515616776:listener/app/Skynet-ELB/cc92401e4b4665d2/e20981587c6fe263`
- ECS Cluster: `skynet-apps-cluster`
- ECR Registry: `129515616776.dkr.ecr.us-west-2.amazonaws.com`

### Azure Resources
- Tenant ID: `1d1bbedc-e179-4e6b-a55e-c500085f1eec`
- App Registration ID: `01f36d24-4410-4439-92f6-678ece732efe`
- Application (Client) ID: `2f1463e8-52ce-499e-9296-4cd125f35f4e`
- Application ID URI: `api://2f1463e8-52ce-499e-9296-4cd125f35f4e`

---

**Last Updated**: 2025-10-04 22:55 PST
**Next Action**: Check Azure AD Sign-in Logs for AADSTS error code
