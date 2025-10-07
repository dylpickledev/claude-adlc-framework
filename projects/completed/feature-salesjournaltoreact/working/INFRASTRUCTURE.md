# App Launcher Portal - Infrastructure Documentation

**Last Updated:** 2025-10-04
**Environment:** Production
**Domain:** apps.grc-ops.com

---

## Architecture Overview

```
User Request Flow:
User → apps.grc-ops.com (Route 53)
  → Skynet-ELB ALB (HTTPS:443)
  → Azure AD OIDC Authentication
  → Path-based routing:
     - / → App Launcher (ECS Fargate)
     - /sales-journal/* → Sales Journal (ECS Fargate)
```

---

## Azure Active Directory (Microsoft Entra ID)

### Authentication Provider
**Purpose:** SSO authentication for all apps via OIDC

| Resource | Value | Notes |
|----------|-------|-------|
| **Tenant Name** | GraniteRock | Organization directory |
| **Tenant ID** | `1d1bbedc-e179-4e6b-a55e-c500085f1eec` | Directory identifier |
| **Identity Source** | Active Directory | AD Connector |
| **Directory ID** | `d-9267138180` | AD Sync configuration |

### Application Registration
**Name:** GraniteRock AWS Apps Portal
**Created:** October 4, 2025

| Setting | Value |
|---------|-------|
| **Application (client) ID** | `2f1463e8-52ce-499e-9296-4cd125f35f4e` |
| **Object ID** | `01f36d24-4410-4439-92f6-678ece732efe` |
| **Supported account types** | Single tenant (GraniteRock only) |
| **Redirect URI** | `https://apps.grc-ops.com/oauth2/idpresponse` |
| **Platform** | Web application |

### Client Credentials
| Credential | Value | Expires |
|------------|-------|---------|
| **Client Secret** | `75138342-5c5a-46a6-92a8-7649cc65a9dc` (Secret ID) | October 4, 2027 (24 months) |
| **Description** | AWS-APP-PORTAL | Production secret for ALB |

### OIDC Endpoints
| Endpoint | URL |
|----------|-----|
| **Issuer** | `https://login.microsoftonline.com/1d1bbedc-e179-4e6b-a55e-c500085f1eec/v2.0` |
| **Authorization** | `https://login.microsoftonline.com/1d1bbedc-e179-4e6b-a55e-c500085f1eec/oauth2/v2.0/authorize` |
| **Token** | `https://login.microsoftonline.com/1d1bbedc-e179-4e6b-a55e-c500085f1eec/oauth2/v2.0/token` |
| **UserInfo** | `https://graph.microsoft.com/oidc/userinfo` |
| **JWKS** | `https://login.microsoftonline.com/1d1bbedc-e179-4e6b-a55e-c500085f1eec/discovery/v2.0/keys` |

### Scopes Requested
- `openid` - Required for OIDC authentication
- `email` - User email address
- `profile` - User profile information (name, etc.)

---

## AWS Infrastructure

### Account Information
| Setting | Value |
|---------|-------|
| **Account ID** | 129515616776 |
| **Region** | us-west-2 (Oregon) |
| **Environment** | Production |

---

## Route 53 (DNS)

### Hosted Zone
| Setting | Value |
|---------|-------|
| **Hosted Zone ID** | `Z07973311LKA61CBKPCVA` |
| **Domain** | grc-ops.com |
| **Type** | Public hosted zone |
| **Record Count** | 20+ |

### DNS Records
| Name | Type | Target | Purpose |
|------|------|--------|---------|
| **apps.grc-ops.com** | A (Alias) | Skynet-ELB-1907289844.us-west-2.elb.amazonaws.com | App Launcher Portal |
| **ALB Hosted Zone** | - | Z1H1FL5HABSF5 | AWS ALB zone for us-west-2 |
| **Created** | - | October 4, 2025 | DNS propagation: ~5-10 minutes |

---

## VPC & Networking

### VPC: Skynet-VPC
**Purpose:** Shared production VPC for multiple applications

| Setting | Value |
|---------|-------|
| **VPC ID** | `vpc-1900307e` |
| **Name** | Skynet-VPC |
| **CIDR Block** | (Query needed) |
| **Status** | Available |
| **Tenancy** | Default |

### Subnets
| Type | Purpose | Availability |
|------|---------|--------------|
| **Public Subnets** | ALB, NAT Gateway | Multiple AZs |
| **Private Subnets** | ECS Fargate tasks | Multiple AZs |

### NAT Gateway
**Purpose:** Outbound internet for ECS tasks in private subnets (e.g., pulling ECR images, calling external APIs)

| Setting | Value |
|---------|-------|
| **Location** | Skynet-VPC |
| **Status** | Active |
| **Monthly Cost** | ~$32 (existing, reused) |

### Security Groups
**TODO:** Document security group IDs and rules after ECS deployment

---

## SSL/TLS Certificates

### ACM Certificate
**Purpose:** HTTPS termination at ALB

| Setting | Value |
|---------|-------|
| **Domain** | grc-ops.com (wildcard or specific) |
| **Certificate ARN** | `arn:aws:acm:us-west-2:129515616776:certificate/724bf7b4-9985-403b-8c16-32c70d2a4434` |
| **Status** | ISSUED |
| **Validation** | DNS validation |
| **Used By** | Skynet-ELB (HTTPS:443 listener) |

---

## Application Load Balancer (ALB)

### Skynet-ELB
**Purpose:** Shared ALB for multiple applications with OIDC authentication and path-based routing

| Setting | Value |
|---------|-------|
| **Load Balancer Name** | Skynet-ELB |
| **ARN** | `arn:aws:elasticloadbalancing:us-west-2:129515616776:loadbalancer/app/Skynet-ELB/cc92401e4b4665d2` |
| **DNS Name** | `Skynet-ELB-1907289844.us-west-2.elb.amazonaws.com` |
| **Hosted Zone ID** | `Z1H1FL5HABSF5` |
| **Scheme** | Internet-facing |
| **IP Address Type** | IPv4 |
| **VPC** | vpc-1900307e (Skynet-VPC) |
| **Status** | Active |
| **Monthly Cost** | ~$28 (existing, reused) |

### HTTPS Listener (Port 443)
| Setting | Value |
|---------|-------|
| **Listener ARN** | `arn:aws:elasticloadbalancing:us-west-2:129515616776:listener/app/Skynet-ELB/cc92401e4b4665d2/e20981587c6fe263` |
| **Protocol** | HTTPS |
| **Port** | 443 |
| **SSL Certificate** | grc-ops.com (ACM) |
| **Default Action** | Authenticate-OIDC → Forward to app-launcher-tg |

### Listener Rules
**Rules are prioritized - lower numbers execute first**

#### Existing Application Rules (Priorities 1-4)
| Priority | Host Condition | Path Condition | Target |
|----------|----------------|----------------|--------|
| **1** | tableau.grc-ops.com | - | TableauServer |
| **2** | replicate.grc-ops.com | - | Qlik-Replicate-AWS |
| **3** | airbyte.grc-ops.com | /v1/* | aribyte-api |
| **4** | airbyte.grc-ops.com | - | Airbyte-On-Prem |

#### Rule 5: Sales Journal App ✅
**Status:** Configured October 4, 2025

| Setting | Value |
|---------|-------|
| **Priority** | 5 |
| **Rule ARN** | `arn:aws:elasticloadbalancing:us-west-2:129515616776:listener-rule/app/Skynet-ELB/cc92401e4b4665d2/e20981587c6fe263/80d6abbff7f13191` |
| **Host Condition** | apps.grc-ops.com |
| **Path Condition** | `/sales-journal`, `/sales-journal/*` |
| **Action 1** | Authenticate-OIDC (Azure AD) |
| **Action 2** | Forward to sales-journal-tg |
| **Session Timeout** | 43200 seconds (12 hours) |

#### Rule 6: App Launcher Landing Page ✅
**Status:** Configured October 4, 2025

| Setting | Value |
|---------|-------|
| **Priority** | 6 |
| **Rule ARN** | `arn:aws:elasticloadbalancing:us-west-2:129515616776:listener-rule/app/Skynet-ELB/cc92401e4b4665d2/e20981587c6fe263/11b41135fc8fded6` |
| **Host Condition** | apps.grc-ops.com |
| **Path Condition** | All paths (/) |
| **Action 1** | Authenticate-OIDC (Azure AD) |
| **Action 2** | Forward to app-launcher-tg |
| **Session Timeout** | 43200 seconds (12 hours) |

#### Default Rule: Tableau Server Fallback
| Setting | Value |
|---------|-------|
| **Condition** | Default (no host/path match) |
| **Action** | Forward to TableauServer |

### OIDC Authentication Configuration
**Provider:** Azure Active Directory (Microsoft Entra ID)

| Setting | Value |
|---------|-------|
| **Issuer** | `https://login.microsoftonline.com/1d1bbedc-e179-4e6b-a55e-c500085f1eec/v2.0` |
| **Authorization Endpoint** | `https://login.microsoftonline.com/1d1bbedc-e179-4e6b-a55e-c500085f1eec/oauth2/v2.0/authorize` |
| **Token Endpoint** | `https://login.microsoftonline.com/1d1bbedc-e179-4e6b-a55e-c500085f1eec/oauth2/v2.0/token` |
| **UserInfo Endpoint** | `https://graph.microsoft.com/oidc/userinfo` |
| **Client ID** | `2f1463e8-52ce-499e-9296-4cd125f35f4e` |
| **Client Secret** | Stored in ALB configuration (not displayed) |
| **Scope** | `openid email profile` |
| **Session Cookie Name** | `AWSELBAuthSessionCookie` |
| **Session Timeout** | 604800 seconds (7 days) |

---

## Target Groups

### app-launcher-tg
**Purpose:** Route traffic to App Launcher ECS tasks

| Setting | Value |
|---------|-------|
| **Target Group Name** | app-launcher-tg |
| **ARN** | `arn:aws:elasticloadbalancing:us-west-2:129515616776:targetgroup/app-launcher-tg/b6ce8e538c04aefb` |
| **Protocol** | HTTP |
| **Port** | 80 |
| **VPC** | vpc-1900307e |
| **Target Type** | IP (for Fargate) |
| **Health Check Path** | `/health` |
| **Health Check Interval** | 30 seconds |
| **Health Check Timeout** | 5 seconds |
| **Healthy Threshold** | 2 |
| **Unhealthy Threshold** | 3 |
| **Matcher** | HTTP 200 |

### sales-journal-tg
**Purpose:** Route traffic to Sales Journal ECS tasks

| Setting | Value |
|---------|-------|
| **Target Group Name** | sales-journal-tg |
| **ARN** | `arn:aws:elasticloadbalancing:us-west-2:129515616776:targetgroup/sales-journal-tg/fe4f6879199e4000` |
| **Protocol** | HTTP |
| **Port** | 80 |
| **VPC** | vpc-1900307e |
| **Target Type** | IP (for Fargate) |
| **Health Check Path** | `/health` |
| **Health Check Interval** | 30 seconds |
| **Health Check Timeout** | 5 seconds |
| **Healthy Threshold** | 2 |
| **Unhealthy Threshold** | 3 |
| **Matcher** | HTTP 200 |

---

## ECS (Elastic Container Service)

### Cluster: skynet-apps-cluster
**Purpose:** Fargate cluster for App Launcher Portal applications

| Setting | Value |
|---------|-------|
| **Cluster Name** | skynet-apps-cluster |
| **ARN** | `arn:aws:ecs:us-west-2:129515616776:cluster/skynet-apps-cluster` |
| **Status** | ACTIVE |
| **Capacity Providers** | Fargate, Fargate Spot |
| **Container Insights** | Disabled |
| **Created** | October 4, 2025 |
| **Tags** | Environment=Production, Project=SalesJournal, Purpose=AppLauncherPortal |

### Task Definitions

#### app-launcher:1 ✅
**Status:** Registered October 4, 2025

| Setting | Value |
|---------|-------|
| **Task Definition ARN** | `arn:aws:ecs:us-west-2:129515616776:task-definition/app-launcher:1` |
| **Family** | app-launcher |
| **Revision** | 1 |
| **Task CPU** | 256 (0.25 vCPU) |
| **Task Memory** | 512 MB |
| **Network Mode** | awsvpc |
| **Requires Compatibilities** | Fargate |
| **Execution Role** | ecsTaskExecutionRole |
| **Container Name** | app-launcher |
| **Container Port** | 80 |
| **Image** | 129515616776.dkr.ecr.us-west-2.amazonaws.com/app-launcher:latest |
| **Log Driver** | awslogs |
| **Log Group** | /ecs/app-launcher |

#### sales-journal:1 ✅
**Status:** Registered October 4, 2025

| Setting | Value |
|---------|-------|
| **Task Definition ARN** | `arn:aws:ecs:us-west-2:129515616776:task-definition/sales-journal:1` |
| **Family** | sales-journal |
| **Revision** | 1 |
| **Task CPU** | 512 (0.5 vCPU) |
| **Task Memory** | 1024 MB (1 GB) |
| **Network Mode** | awsvpc |
| **Requires Compatibilities** | Fargate |
| **Execution Role** | ecsTaskExecutionRole |
| **Container Name** | sales-journal |
| **Container Port** | 80 |
| **Image** | 129515616776.dkr.ecr.us-west-2.amazonaws.com/sales-journal:latest |
| **Log Driver** | awslogs |
| **Log Group** | /ecs/sales-journal |
| **Environment Variables** | VITE_API_BASE_URL, VITE_BASE_PATH |

**Sales Journal Environment:**
- `VITE_API_BASE_URL`: https://4gihwvts8c.execute-api.us-west-2.amazonaws.com
- `VITE_BASE_PATH`: /sales-journal

### Services
**Status:** Ready to deploy (use `deploy.sh` script)

---

## ECR (Elastic Container Registry)

### Repositories
**Purpose:** Store Docker images for ECS deployment

#### app-launcher
| Setting | Value |
|---------|-------|
| **Repository Name** | app-launcher |
| **Repository ARN** | `arn:aws:ecr:us-west-2:129515616776:repository/app-launcher` |
| **Repository URI** | `129515616776.dkr.ecr.us-west-2.amazonaws.com/app-launcher` |
| **Image Scanning** | Scan on push (enabled) |
| **Encryption** | AES256 |
| **Created** | October 4, 2025 |
| **Images** | None (TODO: Push Docker image) |

#### sales-journal
| Setting | Value |
|---------|-------|
| **Repository Name** | sales-journal |
| **Repository ARN** | `arn:aws:ecr:us-west-2:129515616776:repository/sales-journal` |
| **Repository URI** | `129515616776.dkr.ecr.us-west-2.amazonaws.com/sales-journal` |
| **Image Scanning** | Scan on push (enabled) |
| **Encryption** | AES256 |
| **Created** | October 4, 2025 |
| **Images** | None (TODO: Push Docker image) |

---

## CloudWatch Logs

### Log Groups
**Purpose:** Container logs from ECS Fargate tasks

#### /ecs/app-launcher
| Setting | Value |
|---------|-------|
| **Log Group Name** | `/ecs/app-launcher` |
| **Retention** | Never expire (default) |
| **Created** | October 4, 2025 |
| **Stored Bytes** | 0 (no logs yet) |
| **Monthly Cost** | ~$0.50 (estimated after deployment) |

#### /ecs/sales-journal
| Setting | Value |
|---------|-------|
| **Log Group Name** | `/ecs/sales-journal` |
| **Retention** | Never expire (default) |
| **Created** | October 4, 2025 |
| **Stored Bytes** | 0 (no logs yet) |
| **Monthly Cost** | ~$0.50 (estimated after deployment) |

---

## IAM Roles

### ECS Task Execution Role ✅
**Status:** Created October 4, 2025

| Setting | Value |
|---------|-------|
| **Role Name** | `ecsTaskExecutionRole` |
| **Role ARN** | `arn:aws:iam::129515616776:role/ecsTaskExecutionRole` |
| **Role ID** | `AROAR4J53PIEGXEGSVD4M` |
| **Created** | October 5, 2025 |

**Purpose:** Allows ECS tasks to:
- Pull images from ECR
- Write logs to CloudWatch
- Access Secrets Manager (if needed)

**Attached Policies:**
- `AmazonECSTaskExecutionRolePolicy` (AWS managed)

**Trust Policy:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

---

## Secrets Manager

### Azure AD Client Secret
**Purpose:** Securely store Azure AD client secret for ALB OIDC authentication

| Setting | Value |
|---------|-------|
| **Secret Name** | `app-launcher/azure-ad-client-secret` |
| **Secret ARN** | `arn:aws:secretsmanager:us-west-2:129515616776:secret:app-launcher/azure-ad-client-secret-M9yCKF` |
| **Description** | Azure AD client secret for GraniteRock AWS Apps Portal OIDC authentication |
| **Created** | October 4, 2025 |
| **Rotation** | Manual (client secret expires October 4, 2027) |

**Note:** The client secret value is stored both in AWS Secrets Manager and configured directly in the ALB listener rules.

---

## Cost Summary

### Existing Infrastructure (Reused)
| Resource | Monthly Cost | Notes |
|----------|--------------|-------|
| **Skynet-ELB (ALB)** | $0 | Existing, shared with other apps |
| **NAT Gateway** | $0 | Existing in Skynet-VPC |
| **Route 53 Hosted Zone** | $0 | Existing grc-ops.com zone |
| **SSL Certificate** | $0 | AWS ACM certificates are free |
| **Total Reused** | **$0** | Saves ~$60/month |

### New Infrastructure (App Launcher Portal)
| Resource | Configuration | Monthly Cost |
|----------|---------------|--------------|
| **App Launcher (ECS Fargate)** | 0.25 vCPU, 0.5 GB | $9 |
| **Sales Journal (ECS Fargate)** | 0.5 vCPU, 1 GB | $18 |
| **CloudWatch Logs** | 2 log groups, ~1 GB/month | $1 |
| **Secrets Manager** | 1 secret | $0.40 |
| **Data Transfer** | Minimal (internal VPC) | $1 |
| **Route 53 Queries** | Incremental | $0.60 |
| **Total New** | | **$30/month** |

### Total Monthly Cost
| Category | Amount |
|----------|--------|
| **New Infrastructure** | $30 |
| **Existing (Reused)** | $0 |
| **Total** | **$30/month** |

**vs. Original Estimate:** $80/month (saves $50/month)
**vs. Current Amplify:** $15/month (increase $15/month)

---

## Monitoring & Observability

### CloudWatch Metrics
**TODO:** Configure dashboards after deployment

**Key Metrics to Monitor:**
- ALB request count
- ALB target response time
- ALB 2xx/4xx/5xx counts
- ECS CPU/Memory utilization
- Target group health
- OIDC authentication failures

### CloudWatch Alarms
**TODO:** Create alarms after deployment

**Recommended Alarms:**
- Unhealthy targets in app-launcher-tg
- Unhealthy targets in sales-journal-tg
- High 5xx error rate on ALB
- High CPU/memory on ECS tasks

---

## Security Configuration

### Azure AD Security
- **Multi-factor Authentication:** Configured at tenant level
- **Conditional Access:** (TODO: Document if configured)
- **Session Management:** 7-day ALB session cookies
- **Token Rotation:** Client secret expires October 4, 2027

### AWS Security
- **ALB Security Groups:** (TODO: Document after configuration)
- **ECS Task Security Groups:** (TODO: Document after deployment)
- **ECR Image Scanning:** Enabled (scan on push)
- **SSL/TLS:** TLS 1.2+ enforced at ALB

---

## Deployment

### Deployment Script ✅
**Location:** `working/deploy.sh`
**Status:** Ready to execute

The automated deployment script handles:
1. ECR authentication
2. Docker image builds (app-launcher and sales-journal)
3. Image tagging and pushing to ECR
4. Security group creation for ECS tasks
5. ECS service creation (both applications)
6. Health monitoring and verification

**Usage:**
```bash
cd /Users/TehFiestyGoat/da-agent-hub/da-agent-hub/projects/active/feature-salesjournaltoreact/working
./deploy.sh
```

**Duration:** ~5-7 minutes

### Deployment Documentation ✅
**Location:** `working/DEPLOY_NOW.md`

Complete deployment guide with:
- Automated deployment option (deploy.sh)
- Manual step-by-step instructions
- Post-deployment testing procedures
- Troubleshooting reference
- Rollback procedures

### Docker Images
**Source Locations:**
- App Launcher: `working/app-launcher/`
- Sales Journal: `react-sales-journal/`

**ECR Destinations:**
- `129515616776.dkr.ecr.us-west-2.amazonaws.com/app-launcher:latest`
- `129515616776.dkr.ecr.us-west-2.amazonaws.com/sales-journal:latest`

---

## Troubleshooting Reference

### DNS Issues
```bash
# Verify DNS propagation
dig apps.grc-ops.com

# Check Route 53 record
aws route53 list-resource-record-sets --hosted-zone-id Z07973311LKA61CBKPCVA | grep apps
```

### ALB Issues
```bash
# Check target health
aws elbv2 describe-target-health --target-group-arn <tg-arn>

# Check listener rules
aws elbv2 describe-rules --listener-arn <listener-arn>
```

### ECS Issues
```bash
# Check service status
aws ecs describe-services --cluster skynet-apps-cluster --services app-launcher sales-journal

# View task logs
aws logs tail /ecs/app-launcher --follow
aws logs tail /ecs/sales-journal --follow
```

### Azure AD Issues
- **Login failures:** Check Azure AD Sign-in logs
- **Token errors:** Verify client secret hasn't expired
- **Redirect errors:** Confirm redirect URI matches exactly

---

**Maintained By:** DA Agent Hub
**Documentation Location:** `projects/active/feature-salesjournaltoreact/working/INFRASTRUCTURE.md`
