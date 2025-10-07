# Sales Journal Deployment Session State

**Date**: 2025-10-04
**Branch**: fix/configure-saml-via-console
**Status**: In Progress - Azure AD OIDC Authentication Troubleshooting

## Completed Steps

### ✅ Infrastructure Deployment
1. **Docker Images Built and Pushed to ECR**:
   - app-launcher:latest - `129515616776.dkr.ecr.us-west-2.amazonaws.com/app-launcher:latest`
   - sales-journal:latest - `129515616776.dkr.ecr.us-west-2.amazonaws.com/sales-journal:latest`

2. **ECS Services Deployed**:
   - Cluster: skynet-apps-cluster
   - app-launcher service: ACTIVE (1/1 tasks running)
   - sales-journal service: ACTIVE (1/1 tasks running, healthy)

3. **ALB Configuration**:
   - Load Balancer: Skynet-ELB
   - Listener: Port 443 (HTTPS)
   - Rules configured:
     - Priority 5: apps.grc-ops.com/sales-journal* → sales-journal-tg
     - Priority 6: apps.grc-ops.com → app-launcher-tg

4. **Security Groups**:
   - ECS tasks: sg-04e0e784d3140d98a (ecs-apps-sg)
   - ALB: sg-8069e5fb (Skynet-ELB) - allows all outbound traffic

5. **Target Groups**:
   - sales-journal-tg: Healthy (192.168.6.40:80)
   - app-launcher-tg: Running

### ✅ Fixed Issues
1. **Nginx DNS Resolution**: Modified nginx.conf to use runtime DNS resolution with AWS VPC DNS resolver (169.254.169.253)
2. **Docker Build Performance**: Switched to pre-built dist approach (Dockerfile.simple) to avoid slow npm install in Alpine
3. **Docker Credential Issues**: Resolved PATH issues for docker-credential-desktop

## Current Blocker: Azure AD OIDC 561 Authentication Error

### Problem
- Users successfully authenticate with Azure AD
- Authorization code is returned to ALB
- **ALB returns 561 error** during token exchange
- URL: https://apps.grc-ops.com/oauth2/idpresponse?code=...

### Azure AD Configuration (Current State)
- **App Name**: GraniteRock AWS Apps Portal
- **Client ID**: 2f1463e8-52ce-499e-9296-4cd125f35f4e
- **Tenant ID**: 1d1bbedc-e179-4e6b-a55e-c500085f1eec
- **Client Secret**: ***REMOVED*** (expires 10/4/2027)
- **Redirect URI**: https://apps.grc-ops.com/oauth2/idpresponse ✅ Configured
- **API Permissions**: openid, email, profile, User.Read ✅ Granted
- **ID Tokens**: ✅ Enabled in implicit grant settings

### ALB OIDC Configuration (Current State)
```
Issuer: https://login.microsoftonline.com/1d1bbedc-e179-4e6b-a55e-c500085f1eec/v2.0
Authorization Endpoint: https://login.microsoftonline.com/1d1bbedc-e179-4e6b-a55e-c500085f1eec/oauth2/v2.0/authorize
Token Endpoint: https://login.microsoftonline.com/1d1bbedc-e179-4e6b-a55e-c500085f1eec/oauth2/v2.0/token
UserInfo Endpoint: https://graph.microsoft.com/oidc/userinfo
Scope: openid email profile
Client ID: 2f1463e8-52ce-499e-9296-4cd125f35f4e
Client Secret: ***REMOVED***
```

### Ruled Out Issues
❌ Network connectivity (ALB SG allows all outbound)
❌ Incorrect client secret (verified correct value from Azure Portal)
❌ Missing redirect URI (verified configured)
❌ Missing API permissions (verified granted)
❌ ID tokens disabled (verified enabled)

### Next Steps to Investigate
1. **Check Azure AD App Manifest Settings** (HIGH PRIORITY):
   - `accessTokenAcceptedVersion`: Should be `2` (not `null` or `1`)
   - `oauth2AllowIdTokenImplicitFlow`: Should be `true`

2. **Check for DPoP (Demonstrating Proof-of-Possession)**:
   - AWS ALB does not support DPoP
   - If enabled in Azure AD tenant, it will cause 561 errors
   - Solution: Disable DPoP, enable PKCE instead

3. **Verify Token Endpoint Response**:
   - Enable ALB access logs for detailed error messages
   - Check if Azure AD is returning specific error codes

## Files Modified This Session

### nginx.conf
- Added AWS VPC DNS resolver (169.254.169.253)
- Changed proxy_pass to use variable for runtime DNS resolution
- Lines 66-88

### Dockerfile.simple (Created)
- Lightweight nginx-only Dockerfile
- Uses pre-built dist folder from local npm build
- Avoids slow multi-stage build

### .dockerignore.simple (Created)
- Custom dockerignore that allows dist folder
- Used during simple Docker builds

## AWS Resources Created

### ECR Repositories
- 129515616776.dkr.ecr.us-west-2.amazonaws.com/app-launcher
- 129515616776.dkr.ecr.us-west-2.amazonaws.com/sales-journal

### ECS Task Definitions
- app-launcher:1
- sales-journal:1

### ECS Services
- skynet-apps-cluster/app-launcher
- skynet-apps-cluster/sales-journal

### Target Groups
- arn:aws:elasticloadbalancing:us-west-2:129515616776:targetgroup/app-launcher-tg/b6ce8e538c04aefb
- arn:aws:elasticloadbalancing:us-west-2:129515616776:targetgroup/sales-journal-tg/fe4f6879199e4000

### ALB Listener Rules
- arn:aws:elasticloadbalancing:us-west-2:129515616776:listener-rule/app/Skynet-ELB/cc92401e4b4665d2/e20981587c6fe263/80d6abbff7f13191 (Priority 5)
- arn:aws:elasticloadbalancing:us-west-2:129515616776:listener-rule/app/Skynet-ELB/cc92401e4b4665d2/e20981587c6fe263/11b41135fc8fded6 (Priority 6)

### Secrets Manager
- app-launcher/azure-ad-client-secret (Updated with correct value)

## Access URLs

- **App Launcher**: https://apps.grc-ops.com
- **Sales Journal**: https://apps.grc-ops.com/sales-journal

Both URLs currently return 561 authentication error after Azure AD login.

## Key Decisions Made

1. **Deployment Strategy**: ECS Fargate (not Lambda/Amplify) for better control and simpler architecture
2. **Build Approach**: Pre-build React app locally, use simple nginx Dockerfile to avoid slow Docker builds
3. **DNS Resolution**: Runtime resolution in nginx to work in private subnets without NAT Gateway
4. **Authentication**: ALB-level OIDC (not application-level) for centralized auth and session management

## Commands for Quick Reference

### Build and Deploy
```bash
# Build React app locally
VITE_BASE_PATH=/sales-journal npm run build

# Build Docker image
mv .dockerignore.simple .dockerignore && \
docker build -f Dockerfile.simple -t sales-journal:latest . && \
mv .dockerignore .dockerignore.simple && \
mv .dockerignore.full .dockerignore

# Push to ECR
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 129515616776.dkr.ecr.us-west-2.amazonaws.com
docker push 129515616776.dkr.ecr.us-west-2.amazonaws.com/sales-journal:latest

# Force new deployment
aws ecs update-service --cluster skynet-apps-cluster --service sales-journal --force-new-deployment --region us-west-2
```

### Monitoring
```bash
# Check service status
aws ecs describe-services --cluster skynet-apps-cluster --services app-launcher sales-journal --region us-west-2

# Check target health
aws elbv2 describe-target-health --target-group-arn arn:aws:elasticloadbalancing:us-west-2:129515616776:targetgroup/sales-journal-tg/fe4f6879199e4000 --region us-west-2

# View logs
aws logs tail /ecs/sales-journal --follow --region us-west-2
aws logs tail /ecs/app-launcher --follow --region us-west-2
```

## Resume Point

**Current Task**: Resolve Azure AD OIDC 561 authentication error

**Status**: All known Azure AD manifest settings have been fixed, but 561 error persists. User does NOT have access to Azure AD Sign-in Logs.

**Alternative Troubleshooting Approaches Created**:

See full details in: `projects/active/feature-salesjournaltoreact/working/azure-561-troubleshooting-alternatives.md`

### Immediate Actions Available:

1. **Manual Token Exchange Test** (2 minutes - RECOMMENDED FIRST)
   ```bash
   /tmp/test-token-exchange.sh
   ```
   - Tests Azure AD token endpoint directly
   - Will show exact AADSTS error code
   - Bypasses ALB to isolate issue

2. **Enable ALB Access Logs** (5 minutes)
   ```bash
   /tmp/enable-alb-logs.sh
   ```
   - Captures detailed OAuth 2.0 error responses
   - Future auth attempts will log Azure AD errors
   - Closest alternative to Sign-in Logs

3. **Check Enterprise Application** (1 minute)
   - Azure Portal → Microsoft Entra ID → Enterprise Applications
   - Search for "GraniteRock AWS Apps Portal"
   - Verify it exists and is enabled

4. **Contact Azure AD Administrator**
   - Check for tenant-level restrictions:
     - DPoP enabled (ALB doesn't support)
     - Conditional Access policies
     - Security defaults
   - Provide client ID: `2f1463e8-52ce-499e-9296-4cd125f35f4e`

5. **Wait 24 Hours for Propagation**
   - App created today (2025-10-04)
   - Critical manifest changes made today
   - Azure AD can take 24h to fully propagate
   - Test again: 2025-10-05

**Most Likely Causes** (ranked):
1. Propagation delay (60%) - wait 24h
2. Tenant-level restrictions (25%) - need admin
3. Enterprise app issue (10%) - verify in portal
4. ALB config mismatch (5%) - manual test will show

**Research Complete**:
- ✅ azure-expert agent created with 20+ years expertise
- ✅ aws-expert agent pulled from main branch
- ✅ Alternative troubleshooting methods documented
- ✅ Session state saved to DEPLOYMENT_STATUS_2025-10-04.md
