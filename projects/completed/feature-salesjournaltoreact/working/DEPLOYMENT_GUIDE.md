# Sales Journal App Launcher Deployment Guide

**Target Deployment:** Next week (progress-dependent)
**Architecture:** App Launcher Portal with path-based routing
**Domain:** apps.grc-ops.com
**Infrastructure:** Existing Skynet-VPC, Skynet-ELB, NAT Gateway
**Authentication:** AWS IAM Identity Center (OIDC)
**Cost:** ~$32/month (Sales Journal + App Launcher)

---

## Architecture Overview

```
User → apps.grc-ops.com (DNS) → ALB (Skynet-ELB) → OIDC Auth → Path Routing
├── /                      → App Launcher (ECS Fargate, nginx)
└── /sales-journal/*       → Sales Journal (ECS Fargate, nginx + React)
```

### Key Design Decisions
- **Hosting:** ECS Fargate (0.5 vCPU, 1GB memory per app)
- **DNS:** apps.grc-ops.com (single domain for all apps)
- **Routing:** Path-based ALB rules
- **SSO:** Single sign-on across all apps
- **Future apps:** Add via ALB rule + ECS service

---

## Phase 1: Prerequisites (Day 1)

### 1.1 Verify AWS Infrastructure
All resources already exist from infrastructure inventory:

```bash
# Verify VPC
aws ec2 describe-vpcs --vpc-ids vpc-1900307e

# Verify ALB
aws elbv2 describe-load-balancers --names Skynet-ELB

# Verify SSL Certificate
aws acm list-certificates --region us-west-2 | grep grc-ops.com

# Verify Route 53 Hosted Zone
aws route53 list-hosted-zones | grep grc-ops.com
```

**Expected Results:**
- ✅ Skynet-VPC (vpc-1900307e) with public/private subnets
- ✅ Skynet-ELB ALB in us-west-2
- ✅ ACM certificate for *.grc-ops.com or grc-ops.com
- ✅ Route 53 hosted zone for grc-ops.com

### 1.2 Configure IAM Identity Center OIDC Application

**Location:** AWS IAM Identity Center → Applications

1. **Create new OIDC application:**
   - Application name: `GraniteRock Apps Portal`
   - Description: `Multi-app portal with Sales Journal and future applications`
   - Application type: `Custom SAML 2.0/OIDC application`

2. **Configure OIDC settings:**
   - Client ID: `<generated-by-aws>`
   - Client Secret: `<generated-by-aws>`
   - Redirect URLs:
     - `https://apps.grc-ops.com/oauth2/idpresponse`
   - Sign-out URL: `https://apps.grc-ops.com/`
   - Scopes: `openid`, `email`, `profile`

3. **Assign users/groups:**
   - Assign Active Directory groups that need access
   - Typically: Finance, Accounting, IT teams

4. **Save credentials:**
   ```bash
   export OIDC_CLIENT_ID="<client-id-from-aws>"
   export OIDC_CLIENT_SECRET="<client-secret-from-aws>"
   export OIDC_ISSUER="<issuer-url-from-aws>"
   ```

---

## Phase 2: Infrastructure Setup (Day 1-2)

### 2.1 Create ECS Cluster

```bash
# Create ECS cluster
aws ecs create-cluster \
  --cluster-name skynet-apps-cluster \
  --region us-west-2 \
  --tags key=Environment,value=Production key=Project,value=SalesJournal

# Verify creation
aws ecs describe-clusters --clusters skynet-apps-cluster
```

### 2.2 Create ECR Repositories

```bash
# Create repository for App Launcher
aws ecr create-repository \
  --repository-name app-launcher \
  --region us-west-2 \
  --tags Key=Environment,Value=Production Key=Project,Value=SalesJournal

# Create repository for Sales Journal
aws ecr create-repository \
  --repository-name sales-journal \
  --region us-west-2 \
  --tags Key=Environment,Value=Production Key=Project,Value=SalesJournal

# Get repository URIs
aws ecr describe-repositories --region us-west-2 | grep repositoryUri
```

**Save repository URIs:**
```bash
export APP_LAUNCHER_REPO="129515616776.dkr.ecr.us-west-2.amazonaws.com/app-launcher"
export SALES_JOURNAL_REPO="129515616776.dkr.ecr.us-west-2.amazonaws.com/sales-journal"
```

### 2.3 Create Route 53 DNS Record

```bash
# Get ALB DNS name
ALB_DNS=$(aws elbv2 describe-load-balancers \
  --names Skynet-ELB \
  --query 'LoadBalancers[0].DNSName' \
  --output text)

# Get hosted zone ID
HOSTED_ZONE_ID=$(aws route53 list-hosted-zones \
  --query "HostedZones[?Name=='grc-ops.com.'].Id" \
  --output text | cut -d'/' -f3)

# Create A record (alias to ALB)
aws route53 change-resource-record-sets \
  --hosted-zone-id $HOSTED_ZONE_ID \
  --change-batch '{
    "Changes": [{
      "Action": "CREATE",
      "ResourceRecordSet": {
        "Name": "apps.grc-ops.com",
        "Type": "A",
        "AliasTarget": {
          "HostedZoneId": "Z1BKCTXD74EZPE",
          "DNSName": "'$ALB_DNS'",
          "EvaluateTargetHealth": false
        }
      }
    }]
  }'

# Verify DNS propagation (may take 5-10 minutes)
dig apps.grc-ops.com
```

---

## Phase 3: Build and Push Docker Images (Day 2)

### 3.1 Build App Launcher

```bash
cd /Users/TehFiestyGoat/da-agent-hub/da-agent-hub/projects/active/feature-salesjournaltoreact/working/app-launcher

# Build Docker image
docker build -t app-launcher:latest .

# Test locally
docker run -p 8080:80 app-launcher:latest
# Open http://localhost:8080 to verify

# Login to ECR
aws ecr get-login-password --region us-west-2 | \
  docker login --username AWS --password-stdin 129515616776.dkr.ecr.us-west-2.amazonaws.com

# Tag and push
docker tag app-launcher:latest $APP_LAUNCHER_REPO:latest
docker push $APP_LAUNCHER_REPO:latest
```

### 3.2 Build Sales Journal

```bash
cd /Users/TehFiestyGoat/da-agent-hub/react-sales-journal

# Build Docker image
docker build -t sales-journal:latest .

# Test locally (simulates /sales-journal path)
docker run -p 8081:80 sales-journal:latest
# Verify static assets load correctly

# Tag and push
docker tag sales-journal:latest $SALES_JOURNAL_REPO:latest
docker push $SALES_JOURNAL_REPO:latest
```

---

## Phase 4: ECS Services Setup (Day 2-3)

### 4.1 Create Task Execution Role

```bash
# Create IAM role for ECS task execution
aws iam create-role \
  --role-name ecsTaskExecutionRole \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "ecs-tasks.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }'

# Attach AWS managed policy
aws iam attach-role-policy \
  --role-name ecsTaskExecutionRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
```

### 4.2 Create ECS Task Definitions

**App Launcher Task Definition:**

Create file: `app-launcher-task-def.json`
```json
{
  "family": "app-launcher",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::129515616776:role/ecsTaskExecutionRole",
  "containerDefinitions": [{
    "name": "app-launcher",
    "image": "129515616776.dkr.ecr.us-west-2.amazonaws.com/app-launcher:latest",
    "portMappings": [{
      "containerPort": 80,
      "protocol": "tcp"
    }],
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "/ecs/app-launcher",
        "awslogs-region": "us-west-2",
        "awslogs-stream-prefix": "ecs"
      }
    },
    "healthCheck": {
      "command": ["CMD-SHELL", "wget --spider http://localhost/health || exit 1"],
      "interval": 30,
      "timeout": 5,
      "retries": 3,
      "startPeriod": 10
    }
  }]
}
```

**Sales Journal Task Definition:**

Create file: `sales-journal-task-def.json`
```json
{
  "family": "sales-journal",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::129515616776:role/ecsTaskExecutionRole",
  "containerDefinitions": [{
    "name": "sales-journal",
    "image": "129515616776.dkr.ecr.us-west-2.amazonaws.com/sales-journal:latest",
    "portMappings": [{
      "containerPort": 80,
      "protocol": "tcp"
    }],
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "/ecs/sales-journal",
        "awslogs-region": "us-west-2",
        "awslogs-stream-prefix": "ecs"
      }
    },
    "healthCheck": {
      "command": ["CMD-SHELL", "wget --spider http://localhost/health || exit 1"],
      "interval": 30,
      "timeout": 5,
      "retries": 3,
      "startPeriod": 10
    }
  }]
}
```

**Register task definitions:**
```bash
# Create CloudWatch log groups
aws logs create-log-group --log-group-name /ecs/app-launcher
aws logs create-log-group --log-group-name /ecs/sales-journal

# Register task definitions
aws ecs register-task-definition --cli-input-json file://app-launcher-task-def.json
aws ecs register-task-definition --cli-input-json file://sales-journal-task-def.json
```

### 4.3 Create ALB Target Groups

```bash
# Get VPC ID
VPC_ID=$(aws ec2 describe-vpcs \
  --filters "Name=tag:Name,Values=Skynet-VPC" \
  --query 'Vpcs[0].VpcId' \
  --output text)

# Create target group for App Launcher
aws elbv2 create-target-group \
  --name app-launcher-tg \
  --protocol HTTP \
  --port 80 \
  --vpc-id $VPC_ID \
  --target-type ip \
  --health-check-path /health \
  --health-check-interval-seconds 30 \
  --health-check-timeout-seconds 5 \
  --healthy-threshold-count 2 \
  --unhealthy-threshold-count 3

# Create target group for Sales Journal
aws elbv2 create-target-group \
  --name sales-journal-tg \
  --protocol HTTP \
  --port 80 \
  --vpc-id $VPC_ID \
  --target-type ip \
  --health-check-path /health \
  --health-check-interval-seconds 30 \
  --health-check-timeout-seconds 5 \
  --healthy-threshold-count 2 \
  --unhealthy-threshold-count 3

# Save target group ARNs
export APP_LAUNCHER_TG_ARN=$(aws elbv2 describe-target-groups \
  --names app-launcher-tg \
  --query 'TargetGroups[0].TargetGroupArn' \
  --output text)

export SALES_JOURNAL_TG_ARN=$(aws elbv2 describe-target-groups \
  --names sales-journal-tg \
  --query 'TargetGroups[0].TargetGroupArn' \
  --output text)
```

### 4.4 Configure ALB Listener Rules

```bash
# Get ALB ARN
ALB_ARN=$(aws elbv2 describe-load-balancers \
  --names Skynet-ELB \
  --query 'LoadBalancers[0].LoadBalancerArn' \
  --output text)

# Get HTTPS listener ARN
LISTENER_ARN=$(aws elbv2 describe-listeners \
  --load-balancer-arn $ALB_ARN \
  --query 'Listeners[?Protocol==`HTTPS`].ListenerArn' \
  --output text)

# Add OIDC authentication to listener (default action)
aws elbv2 modify-listener \
  --listener-arn $LISTENER_ARN \
  --default-actions Type=authenticate-oidc,Order=1,AuthenticateOidcConfig={Issuer=$OIDC_ISSUER,ClientId=$OIDC_CLIENT_ID,ClientSecret=$OIDC_CLIENT_SECRET,AuthorizationEndpoint=https://<identity-center-domain>/oauth2/authorize,TokenEndpoint=https://<identity-center-domain>/oauth2/token,UserInfoEndpoint=https://<identity-center-domain>/oauth2/userInfo,SessionCookieName=AWSELBAuthSessionCookie,Scope=openid email profile} \
  Type=forward,Order=2,TargetGroupArn=$APP_LAUNCHER_TG_ARN

# Create rule for /sales-journal/*
aws elbv2 create-rule \
  --listener-arn $LISTENER_ARN \
  --priority 10 \
  --conditions Field=path-pattern,Values='/sales-journal*' \
  --actions Type=authenticate-oidc,Order=1,AuthenticateOidcConfig={Issuer=$OIDC_ISSUER,ClientId=$OIDC_CLIENT_ID,ClientSecret=$OIDC_CLIENT_SECRET,AuthorizationEndpoint=https://<identity-center-domain>/oauth2/authorize,TokenEndpoint=https://<identity-center-domain>/oauth2/token,UserInfoEndpoint=https://<identity-center-domain>/oauth2/userInfo,SessionCookieName=AWSELBAuthSessionCookie,Scope=openid email profile} \
  Type=forward,Order=2,TargetGroupArn=$SALES_JOURNAL_TG_ARN
```

### 4.5 Create ECS Services

```bash
# Get private subnet IDs from Skynet-VPC
PRIVATE_SUBNETS=$(aws ec2 describe-subnets \
  --filters "Name=vpc-id,Values=$VPC_ID" "Name=tag:Name,Values=*Private*" \
  --query 'Subnets[*].SubnetId' \
  --output text | tr '\t' ',')

# Get security group ID (or create new one)
SG_ID=$(aws ec2 describe-security-groups \
  --filters "Name=vpc-id,Values=$VPC_ID" "Name=group-name,Values=default" \
  --query 'SecurityGroups[0].GroupId' \
  --output text)

# Create App Launcher service
aws ecs create-service \
  --cluster skynet-apps-cluster \
  --service-name app-launcher \
  --task-definition app-launcher \
  --desired-count 1 \
  --launch-type FARGATE \
  --platform-version LATEST \
  --network-configuration "awsvpcConfiguration={subnets=[$PRIVATE_SUBNETS],securityGroups=[$SG_ID],assignPublicIp=DISABLED}" \
  --load-balancers targetGroupArn=$APP_LAUNCHER_TG_ARN,containerName=app-launcher,containerPort=80

# Create Sales Journal service
aws ecs create-service \
  --cluster skynet-apps-cluster \
  --service-name sales-journal \
  --task-definition sales-journal \
  --desired-count 1 \
  --launch-type FARGATE \
  --platform-version LATEST \
  --network-configuration "awsvpcConfiguration={subnets=[$PRIVATE_SUBNETS],securityGroups=[$SG_ID],assignPublicIp=DISABLED}" \
  --load-balancers targetGroupArn=$SALES_JOURNAL_TG_ARN,containerName=sales-journal,containerPort=80
```

---

## Phase 5: Testing & Validation (Day 3-4)

### 5.1 Verify Services are Running

```bash
# Check service status
aws ecs describe-services \
  --cluster skynet-apps-cluster \
  --services app-launcher sales-journal

# Check task health
aws ecs list-tasks --cluster skynet-apps-cluster

# Check target group health
aws elbv2 describe-target-health --target-group-arn $APP_LAUNCHER_TG_ARN
aws elbv2 describe-target-health --target-group-arn $SALES_JOURNAL_TG_ARN
```

**Expected Results:**
- Services: `ACTIVE` with `runningCount: 1`
- Tasks: `RUNNING` status
- Target Health: `healthy` state

### 5.2 Test Authentication Flow

1. **Open browser:** https://apps.grc-ops.com
2. **Expect:** Redirect to IAM Identity Center login
3. **Login:** Use Active Directory credentials
4. **Expect:** Redirect back to App Launcher landing page
5. **Verify:** User name displayed from OIDC token

### 5.3 Test App Launcher

1. **Landing page:** https://apps.grc-ops.com/
2. **Verify:**
   - GraniteRock branding (green gradient)
   - Welcome message with user's name
   - 6 app cards (1 active: Sales Journal, 5 coming soon)
   - Sales Journal card is clickable

### 5.4 Test Sales Journal

1. **Click:** Sales Journal card
2. **Navigate to:** https://apps.grc-ops.com/sales-journal/
3. **Verify:**
   - No re-authentication required (SSO session active)
   - Sales Journal loads correctly
   - All routes work (Dashboard, Journal, Details, etc.)
   - API calls succeed (check Network tab)
   - Static assets load from `/sales-journal/assets/`

### 5.5 Test API Integration

```bash
# Test API endpoint directly (with auth)
curl -H "x-amzn-oidc-data: <token-from-browser>" \
  https://apps.grc-ops.com/api/health

# Expected: {"status": "healthy", ...}
```

### 5.6 Test Routing Scenarios

| URL | Expected Result |
|-----|----------------|
| `https://apps.grc-ops.com/` | App Launcher landing page |
| `https://apps.grc-ops.com/sales-journal` | Redirect to /sales-journal/ |
| `https://apps.grc-ops.com/sales-journal/` | Sales Journal dashboard |
| `https://apps.grc-ops.com/sales-journal/journal` | Sales Journal page |
| `https://apps.grc-ops.com/api/health` | API health check |
| `https://apps.grc-ops.com/invalid` | App Launcher (default route) |

---

## Phase 6: Monitoring & Observability (Day 4-5)

### 6.1 CloudWatch Dashboards

Create dashboard: `Sales-Journal-App-Portal`

**Metrics to monitor:**
- ALB request count
- ALB target response time
- ALB 2xx/4xx/5xx counts
- ECS CPU/Memory utilization
- Target group health
- OIDC authentication failures

### 6.2 CloudWatch Alarms

```bash
# Alarm: App Launcher unhealthy targets
aws cloudwatch put-metric-alarm \
  --alarm-name app-launcher-unhealthy-targets \
  --metric-name UnHealthyHostCount \
  --namespace AWS/ApplicationELB \
  --statistic Maximum \
  --period 60 \
  --evaluation-periods 2 \
  --threshold 1 \
  --comparison-operator GreaterThanOrEqualToThreshold \
  --dimensions Name=TargetGroup,Value=$APP_LAUNCHER_TG_ARN

# Alarm: Sales Journal unhealthy targets
aws cloudwatch put-metric-alarm \
  --alarm-name sales-journal-unhealthy-targets \
  --metric-name UnHealthyHostCount \
  --namespace AWS/ApplicationELB \
  --statistic Maximum \
  --period 60 \
  --evaluation-periods 2 \
  --threshold 1 \
  --comparison-operator GreaterThanOrEqualToThreshold \
  --dimensions Name=TargetGroup,Value=$SALES_JOURNAL_TG_ARN
```

### 6.3 Log Analysis

```bash
# View App Launcher logs
aws logs tail /ecs/app-launcher --follow

# View Sales Journal logs
aws logs tail /ecs/sales-journal --follow

# Search for errors
aws logs filter-log-events \
  --log-group-name /ecs/sales-journal \
  --filter-pattern "ERROR"
```

---

## Phase 7: Production Deployment Checklist

### Pre-Deployment
- [ ] IAM Identity Center OIDC app configured
- [ ] DNS record created and propagated
- [ ] Docker images built and pushed to ECR
- [ ] ECS cluster and services created
- [ ] ALB listener rules configured
- [ ] Target groups healthy
- [ ] CloudWatch logs/metrics enabled

### Deployment
- [ ] Services deployed and running
- [ ] Health checks passing
- [ ] Authentication flow tested
- [ ] All routes tested
- [ ] API integration verified
- [ ] User acceptance testing completed

### Post-Deployment
- [ ] Monitor CloudWatch metrics for 24 hours
- [ ] Verify no 5xx errors
- [ ] Check user feedback
- [ ] Document any issues
- [ ] Plan for future app additions

---

## Adding Future Apps

When ready to deploy App #2, #3, etc.:

1. **Update App Launcher `index.html`:**
   ```html
   <!-- Change from: -->
   <div class="app-card disabled">
     <span class="coming-soon-badge">Coming Soon</span>
   </div>

   <!-- Change to: -->
   <a href="/app-name/" class="app-card">
     <!-- No "coming soon" badge -->
   </a>
   ```

2. **Rebuild and deploy App Launcher:**
   ```bash
   docker build -t app-launcher:latest .
   docker push $APP_LAUNCHER_REPO:latest

   # Force ECS service to use new image
   aws ecs update-service \
     --cluster skynet-apps-cluster \
     --service app-launcher \
     --force-new-deployment
   ```

3. **Create new app infrastructure:**
   - Build Docker image for new app
   - Create ECR repository
   - Create ECS task definition
   - Create target group
   - Create ALB listener rule for `/app-name/*`
   - Create ECS service

4. **Test new app:**
   - Navigate to `https://apps.grc-ops.com/app-name/`
   - Verify SSO session shares across apps
   - Test all app functionality

---

## Cost Breakdown

| Service | Configuration | Monthly Cost |
|---------|--------------|--------------|
| **App Launcher** | Fargate 0.25 vCPU, 0.5GB | $9 |
| **Sales Journal** | Fargate 0.5 vCPU, 1GB | $18 |
| **CloudWatch Logs** | 2 log groups, 1GB/month | $1 |
| **Data Transfer** | Minimal (internal VPC) | $1 |
| **DNS Queries** | Route 53 hosted zone | $1 |
| **Existing (no charge)** | ALB, NAT Gateway, VPC | $0 (already paid) |
| **TOTAL** | | **~$30/month** |

**Future app additions:** ~$9-18/month per app (depending on size)

---

## Troubleshooting

### Issue: Authentication redirect loop
**Cause:** OIDC configuration mismatch
**Fix:** Verify OIDC client ID, secret, and redirect URLs match IAM Identity Center exactly

### Issue: 502 Bad Gateway
**Cause:** Target group health checks failing
**Fix:** Check ECS task logs (`aws logs tail /ecs/<service-name>`), verify `/health` endpoint works

### Issue: Static assets 404 on Sales Journal
**Cause:** Base path mismatch
**Fix:** Verify Vite build used `VITE_BASE_PATH=/sales-journal`, check nginx config strips path correctly

### Issue: API calls fail
**Cause:** CORS or proxy configuration
**Fix:** Verify nginx proxy_pass to API Gateway, check API Gateway CORS settings

### Issue: Can't see user name on App Launcher
**Cause:** ALB not injecting OIDC headers
**Fix:** Verify nginx sub_filter is injecting meta tags, check browser console for JavaScript errors

---

## Support & Contacts

- **AWS Account:** 129515616776
- **Region:** us-west-2 (Oregon)
- **VPC:** Skynet-VPC (vpc-1900307e)
- **ALB:** Skynet-ELB
- **Domain:** apps.grc-ops.com
- **Deployment Timeline:** Next week (progress-dependent)

---

**Last Updated:** 2025-10-04
**Deployment Status:** Ready for Phase 1 (Prerequisites)
