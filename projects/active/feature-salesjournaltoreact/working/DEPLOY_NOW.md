# App Launcher Portal - Quick Deployment Guide

**Status:** ✅ Infrastructure configured, ready for deployment
**Date:** October 4, 2025

---

## Prerequisites Completed ✅

All infrastructure has been created and configured:

- ✅ Azure AD application registered with OIDC
- ✅ AWS Route 53 DNS record (apps.grc-ops.com)
- ✅ ALB listener rules with Azure AD authentication
- ✅ ECS cluster created (skynet-apps-cluster)
- ✅ ECR repositories created (app-launcher, sales-journal)
- ✅ Target groups created with health checks
- ✅ CloudWatch log groups created
- ✅ ECS task definitions registered
- ✅ IAM task execution role created

---

## Deployment Steps

### Option 1: Automated Deployment (Recommended)

Run the complete deployment script:

```bash
cd /Users/TehFiestyGoat/da-agent-hub/da-agent-hub/projects/active/feature-salesjournaltoreact/working
./deploy.sh
```

**What this script does:**
1. Authenticates with ECR
2. Builds App Launcher Docker image
3. Builds Sales Journal Docker image (with VITE_BASE_PATH=/sales-journal)
4. Pushes both images to ECR
5. Creates security group for ECS tasks (if needed)
6. Creates ECS services for both applications
7. Waits for services to stabilize
8. Verifies target health

**Duration:** ~5-7 minutes

---

### Option 2: Manual Deployment (Step-by-Step)

If you prefer manual control, follow these steps:

#### 1. Authenticate with ECR
```bash
aws ecr get-login-password --region us-west-2 | \
  docker login --username AWS --password-stdin 129515616776.dkr.ecr.us-west-2.amazonaws.com
```

#### 2. Build and Push App Launcher
```bash
cd /Users/TehFiestyGoat/da-agent-hub/da-agent-hub/projects/active/feature-salesjournaltoreact/working/app-launcher
docker build -t app-launcher:latest .
docker tag app-launcher:latest 129515616776.dkr.ecr.us-west-2.amazonaws.com/app-launcher:latest
docker push 129515616776.dkr.ecr.us-west-2.amazonaws.com/app-launcher:latest
```

#### 3. Build and Push Sales Journal
```bash
cd /Users/TehFiestyGoat/da-agent-hub/react-sales-journal
VITE_BASE_PATH=/sales-journal npm run build
docker build -t sales-journal:latest .
docker tag sales-journal:latest 129515616776.dkr.ecr.us-west-2.amazonaws.com/sales-journal:latest
docker push 129515616776.dkr.ecr.us-west-2.amazonaws.com/sales-journal:latest
```

#### 4. Create Security Group for ECS Tasks
```bash
# Create security group
SG_ID=$(aws ec2 create-security-group \
  --group-name ecs-apps-sg \
  --description "Security group for ECS Fargate tasks" \
  --vpc-id vpc-1900307e \
  --region us-west-2 \
  --query 'GroupId' \
  --output text)

# Get ALB security group
ALB_SG=$(aws elbv2 describe-load-balancers \
  --names Skynet-ELB \
  --region us-west-2 \
  --query 'LoadBalancers[0].SecurityGroups[0]' \
  --output text)

# Allow HTTP from ALB
aws ec2 authorize-security-group-ingress \
  --group-id ${SG_ID} \
  --protocol tcp \
  --port 80 \
  --source-group ${ALB_SG} \
  --region us-west-2
```

#### 5. Get Private Subnets
```bash
SUBNETS=$(aws ec2 describe-subnets \
  --filters "Name=vpc-id,Values=vpc-1900307e" "Name=tag:Name,Values=Skynet-Private-Subnet*" \
  --query 'Subnets[0:2].SubnetId' \
  --output text \
  --region us-west-2 | tr '\t' ',')

echo "Subnets: ${SUBNETS}"
```

#### 6. Create ECS Services
```bash
# Create App Launcher service
aws ecs create-service \
  --cluster skynet-apps-cluster \
  --service-name app-launcher \
  --task-definition app-launcher:1 \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[${SUBNETS}],securityGroups=[${SG_ID}],assignPublicIp=DISABLED}" \
  --load-balancers "targetGroupArn=arn:aws:elasticloadbalancing:us-west-2:129515616776:targetgroup/app-launcher-tg/b6ce8e538c04aefb,containerName=app-launcher,containerPort=80" \
  --health-check-grace-period-seconds 60 \
  --region us-west-2

# Create Sales Journal service
aws ecs create-service \
  --cluster skynet-apps-cluster \
  --service-name sales-journal \
  --task-definition sales-journal:1 \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[${SUBNETS}],securityGroups=[${SG_ID}],assignPublicIp=DISABLED}" \
  --load-balancers "targetGroupArn=arn:aws:elasticloadbalancing:us-west-2:129515616776:targetgroup/sales-journal-tg/fe4f6879199e4000,containerName=sales-journal,containerPort=80" \
  --health-check-grace-period-seconds 60 \
  --region us-west-2
```

#### 7. Monitor Deployment
```bash
# Wait for services to stabilize
aws ecs wait services-stable --cluster skynet-apps-cluster --services app-launcher --region us-west-2
aws ecs wait services-stable --cluster skynet-apps-cluster --services sales-journal --region us-west-2

# Check target health
aws elbv2 describe-target-health \
  --target-group-arn arn:aws:elasticloadbalancing:us-west-2:129515616776:targetgroup/app-launcher-tg/b6ce8e538c04aefb \
  --region us-west-2

aws elbv2 describe-target-health \
  --target-group-arn arn:aws:elasticloadbalancing:us-west-2:129515616776:targetgroup/sales-journal-tg/fe4f6879199e4000 \
  --region us-west-2
```

---

## Post-Deployment Testing

### 1. Test Authentication Flow
```bash
# Open in browser (requires GraniteRock Azure AD credentials)
open https://apps.grc-ops.com
```

**Expected:**
- Redirect to Azure AD login (login.microsoftonline.com)
- After login, redirect back to App Launcher landing page
- User name displayed from Azure AD token
- Sales Journal card clickable

### 2. Test Sales Journal
```bash
open https://apps.grc-ops.com/sales-journal
```

**Expected:**
- No re-authentication required (SSO)
- Dashboard loads successfully
- All routes functional (Journal, Details, Out of Balance, etc.)
- API calls succeed (check Network tab)
- Static assets load from `/sales-journal/assets/`

### 3. Monitor Logs
```bash
# App Launcher logs
aws logs tail /ecs/app-launcher --follow --region us-west-2

# Sales Journal logs
aws logs tail /ecs/sales-journal --follow --region us-west-2
```

### 4. Check Service Status
```bash
# ECS service status
aws ecs describe-services \
  --cluster skynet-apps-cluster \
  --services app-launcher sales-journal \
  --region us-west-2 \
  --query 'services[*].[serviceName,status,desiredCount,runningCount]' \
  --output table

# Target group health
aws elbv2 describe-target-health \
  --target-group-arn arn:aws:elasticloadbalancing:us-west-2:129515616776:targetgroup/app-launcher-tg/b6ce8e538c04aefb \
  --region us-west-2 \
  --query 'TargetHealthDescriptions[*].[Target.Id,TargetHealth.State,TargetHealth.Reason]' \
  --output table
```

---

## Troubleshooting

### Service Not Starting
```bash
# Check task failures
aws ecs list-tasks --cluster skynet-apps-cluster --region us-west-2
aws ecs describe-tasks --cluster skynet-apps-cluster --tasks <task-arn> --region us-west-2

# Check logs for errors
aws logs tail /ecs/app-launcher --since 5m --region us-west-2
aws logs tail /ecs/sales-journal --since 5m --region us-west-2
```

### Unhealthy Targets
```bash
# Check target health details
aws elbv2 describe-target-health \
  --target-group-arn <target-group-arn> \
  --region us-west-2

# Common issues:
# - Health check path /health not responding (check nginx config)
# - Security group blocking ALB → ECS traffic
# - Container not listening on port 80
```

### Authentication Issues
```bash
# Check ALB listener rules
aws elbv2 describe-rules \
  --listener-arn arn:aws:elasticloadbalancing:us-west-2:129515616776:listener/app/Skynet-ELB/cc92401e4b4665d2/e20981587c6fe263 \
  --region us-west-2

# Verify Azure AD configuration in Azure Portal:
# - Redirect URI matches: https://apps.grc-ops.com/oauth2/idpresponse
# - Client secret is valid (expires October 4, 2027)
# - Users/groups assigned to application
```

### DNS Issues
```bash
# Check DNS propagation
dig apps.grc-ops.com

# Should return ALB DNS name:
# apps.grc-ops.com. 300 IN A <ALB IP addresses>
```

---

## Rollback Plan

If deployment fails or issues arise:

### Stop ECS Services (keeps infrastructure)
```bash
aws ecs update-service --cluster skynet-apps-cluster --service app-launcher --desired-count 0 --region us-west-2
aws ecs update-service --cluster skynet-apps-cluster --service sales-journal --desired-count 0 --region us-west-2
```

### Delete ECS Services (complete rollback)
```bash
aws ecs delete-service --cluster skynet-apps-cluster --service app-launcher --force --region us-west-2
aws ecs delete-service --cluster skynet-apps-cluster --service sales-journal --force --region us-west-2
```

### Keep Amplify Running
The existing Amplify deployment at `https://master.dwau7b1q9q1iw.amplifyapp.com` is still operational and can serve as fallback if needed.

---

## Success Criteria

✅ **Authentication:**
- Users can log in via Azure AD
- No authentication errors in CloudWatch logs

✅ **App Launcher:**
- Landing page loads at apps.grc-ops.com
- User name displayed correctly
- Sales Journal card navigates to /sales-journal

✅ **Sales Journal:**
- All routes functional
- API calls succeed
- No JavaScript errors in browser console
- Static assets load correctly

✅ **Performance:**
- Page load time < 3 seconds
- Health checks passing
- Target groups showing "healthy" status

✅ **Monitoring:**
- CloudWatch logs capturing container output
- No 5xx errors in ALB metrics

---

## Next Steps After Successful Deployment

1. **User Acceptance Testing (1 week)**
   - Finance team tests Sales Journal functionality
   - Collect feedback on performance and UX
   - Monitor CloudWatch logs for errors

2. **Azure AD User Assignment**
   - Assign GraniteRock users/groups to Azure AD app
   - Test with multiple users to verify SSO

3. **Decommission Amplify (after 1 week stable operation)**
   - Delete Amplify app
   - Remove Amplify DNS records
   - Save ~$15/month

4. **Add Future Apps**
   - Follow same pattern for Apps 2-6
   - Each new app: Dockerfile → ECR → Task Definition → Service → ALB Rule
   - Marginal cost: $9-18/app (Fargate only)

---

**Documentation:**
- Infrastructure: `INFRASTRUCTURE.md`
- Complete Deployment Guide: `DEPLOYMENT_GUIDE.md`
- Architecture: `APP_LAUNCHER_IMPLEMENTATION_PLAN.md`
- Deployment Readiness: `DEPLOYMENT_READINESS.md`

**Support:**
- Check deployment logs: `deploy.sh` output
- Monitor CloudWatch: `/ecs/app-launcher`, `/ecs/sales-journal`
- AWS Console: ECS → skynet-apps-cluster → services
