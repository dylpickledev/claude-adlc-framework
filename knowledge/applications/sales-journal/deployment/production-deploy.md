# Sales Journal - Production Deployment Runbook

**Last Updated**: 2025-10-07
**Production URL**: https://apps.grc-ops.com/sales-journal/
**AWS Account**: 129515616776
**Region**: us-west-2

---

## Prerequisites

- AWS CLI configured with appropriate credentials
- Docker installed and running
- Access to ECR repository: `sales-journal`
- Permissions: ECS service updates, ECR push

---

## Deployment Process

### Step 1: Build Docker Image

```bash
# Navigate to repository
cd /Users/TehFiestyGoat/da-agent-hub/react-sales-journal

# Build Docker image
docker build -t sales-journal:latest .

# Expected output: Successfully built <image-id>
# Build time: ~2-3 minutes
```

**What this does**:
- Builds React app from source (npm run build)
- Creates nginx container with React static assets
- Configures nginx to serve from `/sales-journal/` path
- Sets up health check endpoint

### Step 2: Tag for ECR

```bash
# Tag with ECR repository URL
docker tag sales-journal:latest \
  129515616776.dkr.ecr.us-west-2.amazonaws.com/sales-journal:latest
```

### Step 3: Authenticate to ECR

```bash
# Get ECR login token and authenticate Docker
aws ecr get-login-password --region us-west-2 | \
  docker login --username AWS --password-stdin \
  129515616776.dkr.ecr.us-west-2.amazonaws.com

# Expected output: Login Succeeded
```

### Step 4: Push to ECR

```bash
# Push image to ECR
docker push 129515616776.dkr.ecr.us-west-2.amazonaws.com/sales-journal:latest

# Expected output:
# Pushed layers...
# latest: digest: sha256:... size: ...
# Push time: ~1-2 minutes
```

### Step 5: Deploy to ECS

```bash
# Force new deployment (pulls latest image)
aws ecs update-service \
  --cluster skynet-apps-cluster \
  --service sales-journal \
  --force-new-deployment

# Expected output: Service update initiated
# Deployment time: ~3-5 minutes
```

**What happens**:
1. ECS starts new task with latest image
2. Health checks run (HTTP GET /sales-journal/)
3. ALB routes traffic to new task
4. Old task drains connections (~30 seconds)
5. Old task terminates

### Step 6: Verify Deployment

```bash
# Check service status
aws ecs describe-services \
  --cluster skynet-apps-cluster \
  --service sales-journal \
  --query 'services[0].[serviceName,status,runningCount,desiredCount]'

# Expected output:
# [
#   "sales-journal",
#   "ACTIVE",
#   1,  # runningCount
#   1   # desiredCount
# ]

# Check target health
aws elbv2 describe-target-health \
  --target-group-arn arn:aws:elasticloadbalancing:us-west-2:129515616776:targetgroup/sales-journal-tg/...

# Expected: "State": "healthy"
```

### Step 7: Test Production

```bash
# Test application loads
curl -I https://apps.grc-ops.com/sales-journal/

# Expected: HTTP/2 200 (after auth redirect)

# Test API endpoint (requires authentication)
# Manual test in browser: https://apps.grc-ops.com/sales-journal/
# Should redirect to Azure AD login, then load app
```

---

## Task Definition Configuration

**Current**: `sales-journal:1`

**Image Strategy**: Uses `:latest` tag (auto-updates with force-new-deployment)

```json
{
  "family": "sales-journal",
  "taskRoleArn": "arn:aws:iam::129515616776:role/ecsTaskExecutionRole",
  "executionRoleArn": "arn:aws:iam::129515616776:role/ecsTaskExecutionRole",
  "networkMode": "awsvpc",
  "containerDefinitions": [
    {
      "name": "sales-journal",
      "image": "129515616776.dkr.ecr.us-west-2.amazonaws.com/sales-journal:latest",
      "cpu": 512,
      "memory": 1024,
      "portMappings": [
        {
          "containerPort": 80,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "BASE_PATH",
          "value": "/sales-journal"
        }
      ],
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost/sales-journal/ || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3
      }
    }
  ],
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024"
}
```

---

## ALB Configuration

### Listener Rule: Priority 6 (Sales Journal App)

**Conditions**:
- Host: `apps.grc-ops.com`
- Path: `/sales-journal/*`

**Actions**:
1. `authenticate-oidc` (Order 1) - Azure AD authentication
2. `forward` (Order 2) - Forward to sales-journal-tg

**Target Group**: `sales-journal-tg`
- Protocol: HTTP
- Port: 80
- Health check: `/sales-journal/` (200 OK)

### Listener Rule: Priority 5 (Sales Journal API)

**Conditions**:
- Host: `apps.grc-ops.com`
- Path: `/sales-journal/api/*`

**Actions**:
1. `authenticate-oidc` (Order 1) - Azure AD authentication
2. `forward` (Order 2) - Forward to sales-journal-api-tg (Lambda)

**Target Group**: `sales-journal-api-tg`
- Type: Lambda
- Function: `sales-journal-api`

---

## Rollback Procedure

### Quick Rollback (Previous Image)

```bash
# List recent images
aws ecr describe-images \
  --repository-name sales-journal \
  --query 'sort_by(imageDetails,&imagePushedAt)[-5:].[imageTags[0],imageDigest,imagePushedAt]'

# Identify previous working image digest

# Update task definition with specific digest
aws ecs register-task-definition \
  --family sales-journal \
  --cli-input-json file://task-definition-with-digest.json

# Update service to use new revision
aws ecs update-service \
  --cluster skynet-apps-cluster \
  --service sales-journal \
  --task-definition sales-journal:X
```

### Full Rollback (Previous Task Definition)

```bash
# List task definitions
aws ecs list-task-definitions \
  --family-prefix sales-journal \
  --sort DESC

# Rollback to previous revision
aws ecs update-service \
  --cluster skynet-apps-cluster \
  --service sales-journal \
  --task-definition sales-journal:1  # Previous working revision
```

---

## Monitoring Deployment

### Watch Service Events

```bash
# Stream service events
aws ecs describe-services \
  --cluster skynet-apps-cluster \
  --service sales-journal \
  --query 'services[0].events[:10]' \
  --output table

# Watch for:
# - "has started 1 tasks"
# - "has reached a steady state"
```

### Monitor Logs

```bash
# Tail ECS logs
aws logs tail /ecs/sales-journal --follow

# Watch for:
# - nginx startup
# - Health check requests (200 OK)
# - Application errors (none expected)
```

### Check Target Health

```bash
# Wait for healthy status
aws elbv2 describe-target-health \
  --target-group-arn arn:aws:elasticloadbalancing:us-west-2:129515616776:targetgroup/sales-journal-tg/... \
  --query 'TargetHealthDescriptions[*].[Target.Id,TargetHealth.State,TargetHealth.Reason]'

# Expected: ["<task-id>", "healthy", null]
```

---

## Common Deployment Issues

### Issue: New Image Not Deployed

**Symptom**: `force-new-deployment` runs but old code still active

**Possible Causes**:
1. Task definition uses pinned digest (not `:latest` tag)
2. Docker image not pushed to ECR
3. ECR cache issue

**Solutions**:
```bash
# Verify image pushed
aws ecr describe-images \
  --repository-name sales-journal \
  --image-ids imageTag=latest

# Check task definition image reference
aws ecs describe-task-definition \
  --task-definition sales-journal:1 \
  --query 'taskDefinition.containerDefinitions[0].image'

# Should show: ...sales-journal:latest (not pinned digest)
```

### Issue: Health Checks Failing

**Symptom**: Tasks start but immediately marked unhealthy

**Diagnosis**:
```bash
# Check task logs
aws logs tail /ecs/sales-journal --since 5m

# Look for:
# - nginx startup errors
# - Port binding issues
# - Missing environment variables
```

**Common Fixes**:
- Verify BASE_PATH environment variable set to `/sales-journal`
- Check nginx.conf has correct `location /sales-journal/` block
- Ensure container exposes port 80

### Issue: 404 Errors in Production

**Symptom**: App loads but assets return 404

**Cause**: nginx base path misconfiguration

**Fix**:
- Verify `index.html` has `<base href="/sales-journal/">`
- Check nginx.conf `root` directive
- Confirm vite.config.ts has `base: '/sales-journal/'`

---

## Emergency Procedures

### Complete Service Failure

```bash
# Stop service (removes from ALB)
aws ecs update-service \
  --cluster skynet-apps-cluster \
  --service sales-journal \
  --desired-count 0

# Investigate logs
aws logs tail /ecs/sales-journal --since 1h > sales-journal-failure.log

# Rollback to previous task definition
aws ecs update-service \
  --cluster skynet-apps-cluster \
  --service sales-journal \
  --task-definition sales-journal:1 \
  --desired-count 1
```

### Database Connection Issues

Check Lambda API logs (backend handles database):
```bash
aws logs tail /aws/lambda/sales-journal-api --since 30m --follow
```

### ALB Authentication Issues

```bash
# Verify ALB listener rules
aws elbv2 describe-rules \
  --listener-arn arn:aws:elasticloadbalancing:us-west-2:129515616776:listener/app/Skynet-ELB/.../...

# Check for authenticate-oidc action on both rules:
# - Priority 5: /sales-journal/api/*
# - Priority 6: /sales-journal/*
```

---

## Deployment Checklist

Pre-Deployment:
- [ ] Code changes tested locally
- [ ] Tests passing
- [ ] PR approved and merged
- [ ] Backup of current image digest documented

Build:
- [ ] Docker build successful
- [ ] Image tagged correctly
- [ ] ECR authentication successful
- [ ] Image pushed to ECR

Deploy:
- [ ] Service update initiated
- [ ] New task started
- [ ] Health checks passing
- [ ] Target group shows healthy
- [ ] Old task drained and stopped

Verification:
- [ ] Production URL loads (https://apps.grc-ops.com/sales-journal/)
- [ ] Azure AD authentication working
- [ ] User info displays correctly
- [ ] API calls successful
- [ ] No console errors
- [ ] Logo navigation to app portal works

Post-Deployment:
- [ ] Monitor logs for 15 minutes
- [ ] Check error rates in CloudWatch
- [ ] Verify no user reports of issues
- [ ] Document deployment in changelog

---

## Related Documentation

- **Architecture**: `../architecture/system-design.md`
- **Operations**: `../operations/troubleshooting.md`
- **ALB OIDC**: `../../app-portal/architecture/alb-oidc-authentication.md`

---

**Deployment Time**: ~10-15 minutes total
**Rollback Time**: ~5 minutes
**Zero-Downtime**: ✅ Yes (rolling deployment)
