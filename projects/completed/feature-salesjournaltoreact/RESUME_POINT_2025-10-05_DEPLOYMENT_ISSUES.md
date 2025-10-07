# Sales Journal & App Portal Deployment - Session Resume Point
**Date**: 2025-10-05
**Status**: ⚠️ DEPLOYED BUT NOT SHOWING IN PRODUCTION

---

## Current Situation

### What We Deployed

**1. react-sales-journal (Sales Journal App)**
- **Branch**: `hotfix/alb-oidc-authentication`
- **Commit**: 92df99b
- **Changes**:
  - Added `/api/auth/user` endpoint for ALB OIDC (api/main.py)
  - Created `AuthProvider-ALB.tsx` for ALB-based auth flow
  - Updated `main.tsx` to use ALB auth provider
  - Enhanced error handling in stores (errorStore.ts, syncStore.ts)
  - Updated vite.config.ts
- **ECR Image**: `129515616776.dkr.ecr.us-west-2.amazonaws.com/sales-journal:latest`
  - Digest: `sha256:f02fa812ed933b3858efd49ba6d72681b6fa761e955ed6aafb7a3bfd71d71bb5`
- **ECS Deployment**:
  - Service: `sales-journal` in `skynet-apps-cluster`
  - Status: ACTIVE, 1/1 tasks running
  - Rollout: COMPLETED
  - Target Health: healthy
- **Production URL**: https://apps.grc-ops.com/sales-journal/

**2. da-app-portal (App Launcher)**
- **Branch**: `hotfix/navigation-and-logout-improvements`
- **Commit**: 95c374a
- **Changes**:
  - Fixed Sales Journal link: `/sales-journal` → `/sales-journal/` (trailing slash)
  - Added visible logout tooltip on avatar hover
  - Created `UserAvatarWrapper` and `LogoutTooltip` styled components
- **ECR Image**: `129515616776.dkr.ecr.us-west-2.amazonaws.com/app-launcher:latest`
  - Digest: `sha256:e6465ea61db5def592f19e98fa348a4d34b1ed0a8ade9243e409c43664bac735`
- **ECS Deployment**:
  - Service: `app-launcher` in `skynet-apps-cluster`
  - Status: ACTIVE, 1/1 tasks running
  - Rollout: COMPLETED
  - Target Health: unused (⚠️ "Target group is not configured to receive traffic from the load balancer")
- **Production URL**: https://apps.grc-ops.com/

### What's NOT Working in Production

**User Report**: Changes deployed but not visible at https://apps.grc-ops.com/

**Issues**:
1. **Logout tooltip not appearing** on avatar hover
2. **Sales Journal link not navigating** properly

### Potential Root Causes

**1. Browser Cache**
- Old React bundle cached in browser
- Hard refresh (Cmd+Shift+R / Ctrl+Shift+F5) needed

**2. CloudFront or CDN Caching**
- If there's a CloudFront distribution in front of ALB
- Cache invalidation needed

**3. ALB Target Group Issue**
- app-launcher target shows "unused" - not receiving traffic from ALB
- ALB listener rules may be misconfigured

**4. Wrong Image Deployed**
- ECS might be running old image despite push
- Task definition might need update

**5. Build Hash Mismatch**
- React build generates hashed filenames
- index.html might reference old bundle

---

## Next Steps to Investigate

### 1. Check ALB Listener Rules (CRITICAL)
```bash
# Get ALB ARN
aws elbv2 describe-load-balancers --region us-west-2 --query 'LoadBalancers[?LoadBalancerName==`Skynet-ELB`].LoadBalancerArn' --output text

# List all listener rules
aws elbv2 describe-rules --listener-arn <HTTPS_LISTENER_ARN> --region us-west-2
```

**Expected**:
- Priority 5 or 6: Path `/` or `/*` → `app-launcher-tg`
- Priority 10: Path `/sales-journal/*` → `sales-journal-tg`

**Check**: Are rules routing to correct target groups?

### 2. Verify Actual Running Container
```bash
# Get task ARN
aws ecs list-tasks --cluster skynet-apps-cluster --service-name app-launcher --region us-west-2

# Describe task to see image digest
aws ecs describe-tasks --cluster skynet-apps-cluster --tasks <TASK_ARN> --region us-west-2 --query 'tasks[0].containers[0].image'
```

**Expected**: Should match digest `sha256:e6465ea61db5...`

### 3. Check Running Container Contents
```bash
# If you can exec into container
aws ecs execute-command --cluster skynet-apps-cluster --task <TASK_ARN> --container app-launcher --interactive --command "/bin/sh"

# Then inside container:
ls -la /usr/share/nginx/html/
cat /usr/share/nginx/html/index.html | head -20
```

**Look For**: Verify index.html has new bundle hash from build

### 4. Test Direct to ECS Task (Bypass ALB)
```bash
# Get task private IP
aws ecs describe-tasks --cluster skynet-apps-cluster --tasks <TASK_ARN> --region us-west-2 --query 'tasks[0].containers[0].networkInterfaces[0].privateIpv4Address'

# If you're in VPC, curl directly to task
curl http://<TASK_IP>/
```

### 5. Check for CloudFront Distribution
```bash
# List CloudFront distributions
aws cloudfront list-distributions --query 'DistributionList.Items[?Origins.Items[?DomainName==`apps.grc-ops.com`]]' --region us-west-2

# If exists, invalidate cache
aws cloudfront create-invalidation --distribution-id <DIST_ID> --paths "/*"
```

### 6. Force Complete Rebuild & Redeploy

If all else fails, nuke from orbit:

```bash
# Stop all tasks to force fresh pull
aws ecs update-service --cluster skynet-apps-cluster --service app-launcher --force-new-deployment --region us-west-2

# Or update task definition to force new revision
# Then deploy that revision
```

---

## File Locations

### da-app-portal Repository
```
/Users/TehFiestyGoat/da-agent-hub/da-app-portal/
├── Branch: hotfix/navigation-and-logout-improvements
├── src/App.tsx (modified - logout tooltip + navigation fix)
└── dist/ (built assets)
```

### react-sales-journal Repository
```
/Users/TehFiestyGoat/da-agent-hub/react-sales-journal/
├── Branch: hotfix/alb-oidc-authentication
├── api/main.py (modified - /api/auth/user endpoint)
├── src/components/auth/AuthProvider-ALB.tsx (modified)
├── src/main.tsx (modified)
└── dist/ (built assets)
```

### da-agent-hub Documentation
```
/Users/TehFiestyGoat/da-agent-hub/da-agent-hub/
├── Branch: docs/salesjournal-migration-status-update
└── projects/active/feature-salesjournaltoreact/
    ├── DEPLOYMENT_SUCCESS_2025-10-05.md (previous success doc)
    ├── SESSION_2025-10-04_DEPLOYMENT.md (previous session)
    └── RESUME_POINT_2025-10-05_DEPLOYMENT_ISSUES.md (THIS FILE)
```

---

## Quick Commands Reference

### Check Deployment Status
```bash
# App launcher
aws ecs describe-services --cluster skynet-apps-cluster --services app-launcher --region us-west-2 --query 'services[0].{Status:status,Deployments:deployments[*].rolloutState}'

# Sales journal
aws ecs describe-services --cluster skynet-apps-cluster --services sales-journal --region us-west-2 --query 'services[0].{Status:status,Deployments:deployments[*].rolloutState}'

# Target health
aws elbv2 describe-target-health --target-group-arn arn:aws:elasticloadbalancing:us-west-2:129515616776:targetgroup/app-launcher-tg/b6ce8e538c04aefb --region us-west-2
```

### View Logs
```bash
# App launcher logs
aws logs tail /ecs/app-launcher --follow --region us-west-2

# Sales journal logs
aws logs tail /ecs/sales-journal --follow --region us-west-2
```

### Force Redeploy
```bash
# App launcher
aws ecs update-service --cluster skynet-apps-cluster --service app-launcher --force-new-deployment --region us-west-2

# Sales journal
aws ecs update-service --cluster skynet-apps-cluster --service sales-journal --force-new-deployment --region us-west-2
```

---

## What User Tested

User refreshed https://apps.grc-ops.com/ and reported:
1. ❌ Logout tooltip NOT appearing on avatar hover
2. ❌ Sales Journal link NOT navigating to `/sales-journal/`

**User saw same old behavior** - changes not visible despite successful deployment.

---

## Critical Questions to Answer

1. **Is there a CloudFront distribution?** (Cache invalidation needed)
2. **Are ALB listener rules correct?** (app-launcher-tg getting traffic?)
3. **Is the new image actually running?** (Check task image digest)
4. **Is there a browser cache issue?** (Hard refresh tried?)
5. **Are we looking at the right environment?** (Correct AWS account/region?)

---

## Lessons Learned (The Fuck-Ups)

1. **Tested localhost instead of production** - Deployed without verifying actual site
2. **Assumed ECS deployment = live changes** - Didn't account for caching layers
3. **Didn't check ALB routing** - Target group shows "unused" which is suspicious
4. **Didn't verify container contents** - Should have exec'd in to confirm files

---

## Resume Checklist

When you come back:
- [ ] Check ALB listener rules configuration
- [ ] Verify running container image digest matches ECR push
- [ ] Test direct to ECS task IP (bypass ALB)
- [ ] Look for CloudFront distribution
- [ ] Exec into container to verify files
- [ ] Check nginx access/error logs in CloudWatch
- [ ] Consider force-stopping tasks to pull fresh image

**Most Likely Issue**: ALB routing problem. app-launcher target group showing "unused" is a huge red flag.
