# App Launcher Portal Implementation Plan - apps.grc-ops.com

**Created:** October 4, 2025
**Target Deployment:** Next week (progress-dependent)
**Architecture:** Multi-app portal with single sign-on
**Total Cost:** $23/month (Sales Journal + App Launcher)

---

## Executive Summary

**What We're Building:**
- Single portal domain: **apps.grc-ops.com**
- Landing page showing available apps (like AWS access portal)
- Path-based routing: `/sales-journal`, `/app2`, etc.
- Single sign-on via ALB + IAM Identity Center
- Infrastructure shared across all apps (cost-effective)

**User Experience:**
1. User goes to apps.grc-ops.com
2. Authenticates once with Active Directory credentials
3. Sees landing page with app tiles
4. Clicks "Sales Journal" → navigates to apps.grc-ops.com/sales-journal
5. Already authenticated, app loads immediately
6. Can navigate back to launcher, click other apps (no re-login)

**Benefits vs. Original Plan:**
- ✅ Single URL to remember (not 6 different subdomains)
- ✅ One authentication for all apps
- ✅ Easier to add new apps (just add routing rule + app card)
- ✅ Professional app discovery experience
- ✅ Same cost as original approach

---

## Architecture Overview

### Domain Structure:
```
apps.grc-ops.com
├── /                      → App Launcher Portal (landing page)
├── /sales-journal/*       → Sales Journal React app
├── /app2/*               → Future app #2
├── /app3/*               → Future app #3
├── /app4/*               → Future app #4
├── /app5/*               → Future app #5
└── /app6/*               → Future app #6
```

### ALB Routing Flow:
```
User Request → Skynet-ELB (ALB)
                  ↓
            OIDC Authentication Check
                  ↓
        ┌─────────┴─────────┐
        │ Has valid session? │
        └─────────┬─────────┘
                  │
        ┌─────────┴─────────┐
       NO                   YES
        │                    │
        ▼                    ▼
  Redirect to IAM      Path-based routing:
  Identity Center      - / → App Launcher
        │              - /sales-journal/* → Sales Journal
        │              - /app2/* → App 2
        ▼              - etc.
  User logs in
        │
        ▼
  Set session cookie (8 hours)
        │
        ▼
  Redirect back to original URL
```

### Infrastructure Components:
1. **Skynet-ELB (existing ALB)** - HTTPS listener with OIDC auth
2. **Target Groups:**
   - `app-launcher-tg` - Serves landing page
   - `sales-journal-tg` - Serves Sales Journal app
   - Future: `app2-tg`, `app3-tg`, etc.
3. **ECS Fargate Services:**
   - `app-launcher` - Static HTML or React landing page
   - `sales-journal` - Sales Journal React app
   - Future: app2, app3, etc.
4. **IAM Identity Center** - OIDC application for authentication
5. **Route 53** - DNS record: apps.grc-ops.com → Skynet-ELB
6. **ACM Certificate** - Existing grc-ops.com wildcard cert

---

## Phase 1: App Launcher Portal Implementation

### Option A: Static HTML Launcher (RECOMMENDED FOR INITIAL DEPLOYMENT)

**Pros:**
- ✅ Simple, fast to build
- ✅ Zero additional cost (minimal CloudWatch logs)
- ✅ Can be updated easily (just edit HTML)
- ✅ Works perfectly for 6 apps

**Cons:**
- ⚠️ Shows all apps to all users (no personalization)
- ⚠️ Manual updates when adding apps

**Implementation:**

**File: `app-launcher/index.html`**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GraniteRock Applications</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #0f4c38 0%, #2d8a5f 100%);
            min-height: 100vh;
            color: white;
        }

        .header {
            text-align: center;
            padding: 40px 20px;
        }

        .logo {
            font-size: 4rem;
            margin-bottom: 20px;
        }

        h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
        }

        .subtitle {
            font-size: 1.2rem;
            opacity: 0.9;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }

        .app-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-top: 40px;
        }

        .app-card {
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid rgba(255, 255, 255, 0.2);
            border-radius: 12px;
            padding: 30px;
            text-decoration: none;
            color: white;
            transition: all 0.3s ease;
            cursor: pointer;
            backdrop-filter: blur(10px);
        }

        .app-card:hover {
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.15);
            border-color: rgba(255, 255, 255, 0.4);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }

        .app-card.disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        .app-card.disabled:hover {
            transform: none;
            background: rgba(255, 255, 255, 0.1);
        }

        .app-icon {
            font-size: 3.5rem;
            margin-bottom: 15px;
        }

        .app-name {
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 10px;
        }

        .app-description {
            font-size: 0.95rem;
            opacity: 0.9;
            line-height: 1.5;
        }

        .footer {
            text-align: center;
            padding: 40px 20px;
            opacity: 0.7;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">🏔️</div>
        <h1>GraniteRock Applications</h1>
        <p class="subtitle">Select an application to continue</p>
    </div>

    <div class="container">
        <div class="app-grid">
            <!-- Sales Journal App -->
            <a href="/sales-journal/" class="app-card">
                <div class="app-icon">📊</div>
                <h3 class="app-name">Sales Journal</h3>
                <p class="app-description">
                    Financial data analysis and reporting. View sales transactions,
                    batch processing, and out-of-balance detection.
                </p>
            </a>

            <!-- Placeholder apps (coming soon) -->
            <div class="app-card disabled">
                <div class="app-icon">📈</div>
                <h3 class="app-name">Analytics Dashboard</h3>
                <p class="app-description">Coming soon...</p>
            </div>

            <div class="app-card disabled">
                <div class="app-icon">🔧</div>
                <h3 class="app-name">Operations Portal</h3>
                <p class="app-description">Coming soon...</p>
            </div>

            <div class="app-card disabled">
                <div class="app-icon">📱</div>
                <h3 class="app-name">Mobile Access</h3>
                <p class="app-description">Coming soon...</p>
            </div>

            <div class="app-card disabled">
                <div class="app-icon">🎯</div>
                <h3 class="app-name">Project Tracker</h3>
                <p class="app-description">Coming soon...</p>
            </div>

            <div class="app-card disabled">
                <div class="app-icon">💼</div>
                <h3 class="app-name">Resource Manager</h3>
                <p class="app-description">Coming soon...</p>
            </div>
        </div>
    </div>

    <div class="footer">
        <p>&copy; 2025 GraniteRock. All rights reserved.</p>
    </div>
</body>
</html>
```

**Deployment: Static nginx Container**

**File: `app-launcher/Dockerfile`**
```dockerfile
FROM nginx:alpine

# Copy landing page
COPY index.html /usr/share/nginx/html/

# Simple nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
```

**File: `app-launcher/nginx.conf`**
```nginx
server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    # Serve landing page
    location = / {
        try_files /index.html =404;
    }

    # Health check for ALB
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }

    # Caching
    location ~* \.(html|css|js)$ {
        expires 1h;
        add_header Cache-Control "public, must-revalidate";
    }
}
```

**Cost:** $0/month (minimal CloudWatch logs, ~$1-2/month max)

---

### Option B: Dynamic React Launcher (FUTURE ENHANCEMENT)

**When to use:**
- Need personalized app lists based on user groups
- Want usage analytics
- Need dynamic app configuration (no code deploys to add apps)

**Cost:** $18/month (Fargate container)

**Deferred until Phase 2** (after Sales Journal is live)

---

## Phase 2: Sales Journal React App Updates

### Required Changes for Path-Based Routing

The React app needs to handle the `/sales-journal` base path.

**File: `react-sales-journal/vite.config.ts`**
```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  base: process.env.VITE_BASE_PATH || '/', // Allow override for production
  server: {
    port: 5175,
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
  },
});
```

**File: `react-sales-journal/.env.production`** (new file)
```bash
# Production environment variables (apps.grc-ops.com deployment)
VITE_API_BASE_URL=https://4gihwvts8c.execute-api.us-west-2.amazonaws.com
VITE_BASE_PATH=/sales-journal
```

**File: `react-sales-journal/src/main.tsx`**
```typescript
import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';

const basename = import.meta.env.VITE_BASE_PATH || '/';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter basename={basename}>
      <App />
    </BrowserRouter>
  </React.StrictMode>
);
```

**Updated nginx config for Sales Journal:**

**File: `working/nginx-alb-sales-journal.conf`** (updated from nginx-alb.conf)
```nginx
server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # React Router support - all sales-journal routes serve index.html
    # ALB forwards requests to /sales-journal/* to this container
    # nginx sees the path without /sales-journal prefix (ALB strips it via target group path pattern)
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Inject ALB auth headers as meta tags
    location = /index.html {
        add_header Cache-Control "no-cache, no-store, must-revalidate";
        add_header Pragma "no-cache";
        add_header Expires "0";

        sub_filter_types text/html;
        sub_filter_once on;

        sub_filter '</head>' '
    <meta name="x-amzn-oidc-identity" content="$http_x_amzn_oidc_identity">
    <meta name="x-amzn-oidc-data" content="$http_x_amzn_oidc_data">
  </head>';
    }

    # Static assets caching
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Health check
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript
               application/javascript application/x-javascript
               application/xml+rss application/json;
}
```

---

## Phase 3: ALB Configuration

### DNS Configuration

**Create Route 53 A Record:**
```bash
aws route53 change-resource-record-sets \
  --hosted-zone-id Z07973311LKA61CBKPCVA \
  --change-batch '{
    "Changes": [{
      "Action": "CREATE",
      "ResourceRecordSet": {
        "Name": "apps.grc-ops.com",
        "Type": "A",
        "AliasTarget": {
          "HostedZoneId": "Z1H1FL5HABSF5",
          "DNSName": "Skynet-ELB-1907289844.us-west-2.elb.amazonaws.com",
          "EvaluateTargetHealth": false
        }
      }
    }]
  }'
```

### Target Groups

**1. App Launcher Target Group**
```bash
aws elbv2 create-target-group \
  --name app-launcher-tg \
  --protocol HTTP \
  --port 80 \
  --vpc-id vpc-1900307e \
  --health-check-path /health \
  --health-check-interval-seconds 30 \
  --health-check-timeout-seconds 5 \
  --healthy-threshold-count 2 \
  --unhealthy-threshold-count 3 \
  --target-type ip \
  --region us-west-2
```

**2. Sales Journal Target Group**
```bash
aws elbv2 create-target-group \
  --name sales-journal-tg \
  --protocol HTTP \
  --port 80 \
  --vpc-id vpc-1900307e \
  --health-check-path /health \
  --health-check-interval-seconds 30 \
  --health-check-timeout-seconds 5 \
  --healthy-threshold-count 2 \
  --unhealthy-threshold-count 3 \
  --target-type ip \
  --region us-west-2
```

### ALB Listener Rules (Path-Based Routing)

Get the HTTPS listener ARN:
```bash
LISTENER_ARN=$(aws elbv2 describe-listeners \
  --load-balancer-arn arn:aws:elasticloadbalancing:us-west-2:129515616776:loadbalancer/app/Skynet-ELB/cc92401e4b4665d2 \
  --region us-west-2 \
  --query 'Listeners[?Port==`443`].ListenerArn' \
  --output text)
```

**Add listener rules (BEFORE default rule):**

**Rule 1: Sales Journal** (higher priority = evaluated first)
```bash
aws elbv2 create-rule \
  --listener-arn $LISTENER_ARN \
  --priority 10 \
  --conditions Field=path-pattern,Values='/sales-journal*' \
  --actions Type=forward,TargetGroupArn=<sales-journal-tg-arn> \
  --region us-west-2
```

**Rule 2: App Launcher** (default for apps.grc-ops.com)
```bash
aws elbv2 create-rule \
  --listener-arn $LISTENER_ARN \
  --priority 20 \
  --conditions Field=host-header,Values='apps.grc-ops.com' \
  --actions Type=forward,TargetGroupArn=<app-launcher-tg-arn> \
  --region us-west-2
```

**Note:** Existing rules for tableau.grc-ops.com will continue to work (different host header)

---

## Phase 4: IAM Identity Center Configuration

### Create Customer-Managed OIDC Application

**Via AWS Console** (easier than CLI for OIDC setup):

1. Go to: https://us-west-2.console.aws.amazon.com/singlesignon/home
2. **Applications** → **Add application**
3. **Application type:** "I have an application I want to set up"
4. **Application provider:** "Custom SAML 2.0" → Change to **"Add a custom OIDC application"**
5. **Display name:** "GraniteRock Apps Portal"
6. **Description:** "Multi-app portal with SSO for Sales Journal and future apps"
7. **Application start URL:** `https://apps.grc-ops.com`
8. **Redirect URIs:**
   - `https://apps.grc-ops.com/oauth2/idpresponse`
   - (ALB OIDC callback endpoint)
9. **Scopes:** openid, email, profile
10. **Assign users/groups:**
    - Group: "Snow Flake SSO"
    - Or specific users

11. **Save** and note the OIDC details:
    - **Client ID**: [copy this]
    - **Client Secret**: [copy this - shown once]
    - **Issuer URL**: `https://oidc.us-west-2.amazonaws.com/[instance-id]`
    - **Authorization endpoint**
    - **Token endpoint**
    - **User info endpoint**

### Update ALB HTTPS Listener for OIDC Authentication

**Add authentication action** (before forwarding rules):

```bash
# This needs to be done via AWS Console (easier for OIDC configuration)
# Or use CloudFormation/CDK for infrastructure-as-code
```

**Manual steps in Console:**
1. Go to EC2 → Load Balancers → Skynet-ELB
2. Listeners tab → HTTPS:443 listener
3. Click listener → View/edit rules
4. Edit default SSL policy
5. **Add action: Authenticate** (BEFORE forward action)
   - **Type:** Authenticate with OIDC
   - **Issuer:** `https://oidc.us-west-2.amazonaws.com/[instance-id]`
   - **Authorization endpoint:** [from IAM Identity Center]
   - **Token endpoint:** [from IAM Identity Center]
   - **User info endpoint:** [from IAM Identity Center]
   - **Client ID:** [from IAM Identity Center]
   - **Client secret:** [from IAM Identity Center]
   - **Session cookie name:** AWSELBAuthSessionCookie
   - **Session timeout:** 28800 (8 hours)
   - **Scope:** openid email profile
   - **On unauthenticated request:** Authenticate (deny)

**Result:** All requests to apps.grc-ops.com require authentication before reaching app

---

## Phase 5: ECS Deployment

### Create ECS Cluster

```bash
aws ecs create-cluster \
  --cluster-name skynet-apps-cluster \
  --region us-west-2 \
  --tags key=Environment,value=Production key=ManagedBy,value=DataAnalytics
```

### Create ECR Repositories

```bash
# App Launcher
aws ecr create-repository \
  --repository-name app-launcher \
  --region us-west-2 \
  --image-scanning-configuration scanOnPush=true

# Sales Journal
aws ecr create-repository \
  --repository-name sales-journal-web \
  --region us-west-2 \
  --image-scanning-configuration scanOnPush=true
```

### Build and Push Docker Images

**App Launcher:**
```bash
cd app-launcher
docker build -t app-launcher:latest .
docker tag app-launcher:latest 129515616776.dkr.ecr.us-west-2.amazonaws.com/app-launcher:latest

aws ecr get-login-password --region us-west-2 | \
  docker login --username AWS --password-stdin 129515616776.dkr.ecr.us-west-2.amazonaws.com

docker push 129515616776.dkr.ecr.us-west-2.amazonaws.com/app-launcher:latest
```

**Sales Journal:**
```bash
cd /Users/TehFiestyGoat/da-agent-hub/react-sales-journal

# Build with production env vars
VITE_BASE_PATH=/sales-journal \
VITE_API_BASE_URL=https://4gihwvts8c.execute-api.us-west-2.amazonaws.com \
npm run build

# Build Docker image
docker build -t sales-journal-web:latest .
docker tag sales-journal-web:latest 129515616776.dkr.ecr.us-west-2.amazonaws.com/sales-journal-web:latest

docker push 129515616776.dkr.ecr.us-west-2.amazonaws.com/sales-journal-web:latest
```

### Create ECS Task Definitions

**App Launcher Task Definition:**
```json
{
  "family": "app-launcher",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [
    {
      "name": "app-launcher",
      "image": "129515616776.dkr.ecr.us-west-2.amazonaws.com/app-launcher:latest",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 80,
          "protocol": "tcp"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/app-launcher",
          "awslogs-region": "us-west-2",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

**Sales Journal Task Definition:**
```json
{
  "family": "sales-journal",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "sales-journal",
      "image": "129515616776.dkr.ecr.us-west-2.amazonaws.com/sales-journal-web:latest",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 80,
          "protocol": "tcp"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/sales-journal",
          "awslogs-region": "us-west-2",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

### Create ECS Services

**App Launcher Service:**
```bash
aws ecs create-service \
  --cluster skynet-apps-cluster \
  --service-name app-launcher \
  --task-definition app-launcher:1 \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={
    subnets=[subnet-94e582dd,subnet-c280cca5],
    securityGroups=[sg-xxxxx],
    assignPublicIp=DISABLED
  }" \
  --load-balancers "targetGroupArn=<app-launcher-tg-arn>,containerName=app-launcher,containerPort=80" \
  --region us-west-2
```

**Sales Journal Service:**
```bash
aws ecs create-service \
  --cluster skynet-apps-cluster \
  --service-name sales-journal \
  --task-definition sales-journal:1 \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={
    subnets=[subnet-94e582dd,subnet-c280cca5],
    securityGroups=[sg-xxxxx],
    assignPublicIp=DISABLED
  }" \
  --load-balancers "targetGroupArn=<sales-journal-tg-arn>,containerName=sales-journal,containerPort=80" \
  --region us-west-2
```

---

## Phase 6: Testing & Validation

### Pre-Deployment Tests

1. **Build Docker images locally** and test:
   ```bash
   # App Launcher
   docker run -p 8080:80 app-launcher:latest
   # Visit http://localhost:8080 - should see landing page

   # Sales Journal
   docker run -p 8081:80 sales-journal-web:latest
   # Visit http://localhost:8081 - should see app (may need mock auth)
   ```

2. **Test React app base path** locally:
   ```bash
   cd react-sales-journal
   VITE_BASE_PATH=/sales-journal npm run dev
   # Visit http://localhost:5175/sales-journal
   ```

### Post-Deployment Tests

**End-to-End Flow:**
1. Navigate to **https://apps.grc-ops.com**
2. Should redirect to IAM Identity Center login
3. Login with ckaiser@graniterock.com (AD credentials)
4. Should redirect back to apps.grc-ops.com showing landing page
5. Click "Sales Journal" card
6. Should navigate to **https://apps.grc-ops.com/sales-journal**
7. App loads (already authenticated, no second login)
8. Test app functionality (dashboard, filters, etc.)
9. Navigate back to **https://apps.grc-ops.com** (browser back or direct URL)
10. Should show landing page again (still authenticated)
11. Click Sales Journal again → should load immediately (session valid)

**Authentication Tests:**
1. **Session persistence:** Refresh page, should stay logged in
2. **Session timeout:** Wait 8 hours, should re-authenticate
3. **Logout:** Navigate to /logout endpoint, session cleared
4. **Cross-app auth:** When app #2 added, verify single login works for both

**Performance Tests:**
1. ALB health checks passing for both target groups
2. App Launcher loads in < 500ms
3. Sales Journal loads in < 2s (first load)
4. Subsequent navigations < 500ms
5. No console errors

**Security Tests:**
1. Unauthenticated request → redirects to login
2. Invalid session cookie → re-authenticates
3. HTTPS only (no HTTP access)
4. Security headers present (X-Frame-Options, etc.)

---

## Phase 7: Future App Additions (Template)

**For each new app (Apps #2-6):**

1. **Build app Docker image** with base path support
2. **Create ECR repo:** `aws ecr create-repository --repository-name app-name`
3. **Push image:** `docker push 129515616776.dkr.ecr.us-west-2.amazonaws.com/app-name:latest`
4. **Create target group:** Same as sales-journal but with new name
5. **Add ALB listener rule:**
   ```bash
   aws elbv2 create-rule \
     --listener-arn $LISTENER_ARN \
     --priority [next-available] \
     --conditions Field=path-pattern,Values='/app-name*' \
     --actions Type=forward,TargetGroupArn=<app-tg-arn>
   ```
6. **Create ECS task definition** (copy template, update image)
7. **Create ECS service** pointing to new target group
8. **Update app launcher HTML:** Add new app card
9. **Rebuild app-launcher Docker image**
10. **Update ECS service:** Force new deployment with updated image
11. **Test:** Navigate to apps.grc-ops.com/app-name

**Time per app:** ~1 hour (30 min deployment + 30 min testing)

---

## Cost Summary (Updated for App Launcher)

### Phase 1: App Launcher + Sales Journal

**Monthly Costs:**
- App Launcher Fargate (0.25 vCPU, 0.5GB): **~$9/month**
- Sales Journal Fargate (0.5 vCPU, 1GB): **$18/month**
- CloudWatch Logs: **$5/month**
- ALB (reusing existing): **$0**
- NAT Gateway (reusing existing): **$0**
- **Total: ~$32/month**

**Cost increase from current Amplify:** $17/month (from $15 to $32)

### Phase 7: Six Apps Total

**Monthly Costs:**
- App Launcher Fargate: **$9/month**
- 6 apps × $18/month: **$108/month**
- CloudWatch Logs: **$10/month**
- **Total: ~$127/month** (~$21/app average)

vs. $498/month if each had separate ALB/infrastructure
**Savings: $371/month**

---

## Rollback Plan

### Quick Rollback (5 minutes)

If critical issues during deployment:

1. **Update DNS back to Amplify:**
   ```bash
   # Point apps.grc-ops.com to Amplify instead of ALB
   # Or just delete the DNS record entirely
   ```

2. **Users can still access via:** https://master.dwau7b1q9q1iw.amplifyapp.com

### Partial Rollback

If App Launcher works but Sales Journal has issues:
1. Keep apps.grc-ops.com live with launcher
2. Mark Sales Journal card as "Under Maintenance"
3. Debug Sales Journal separately
4. Re-enable when fixed

---

## Timeline & Milestones

### Day 1-2: Infrastructure Preparation
- ✅ Infrastructure inventory complete
- ⏳ Create app launcher HTML/Docker
- ⏳ Update Sales Journal for base path routing
- ⏳ Build and test Docker images locally

### Day 3-4: AWS Resource Creation
- ⏳ Create ECS cluster
- ⏳ Create ECR repos
- ⏳ Create target groups
- ⏳ Create IAM Identity Center OIDC app
- ⏳ Configure ALB listener rules
- ⏳ Create DNS record

### Day 5: Deployment
- ⏳ Push Docker images to ECR
- ⏳ Create ECS task definitions
- ⏳ Deploy ECS services
- ⏳ Verify health checks passing

### Day 6: Testing
- ⏳ End-to-end authentication testing
- ⏳ App functionality testing
- ⏳ Performance testing
- ⏳ Security validation

### Day 7: Go-Live
- ⏳ Update documentation
- ⏳ Notify users
- ⏳ Monitor for 24 hours
- ⏳ Address any issues

**Total: 7 days** (can be compressed to 3-4 days if needed)

---

## Success Criteria

- [ ] apps.grc-ops.com resolves and loads landing page
- [ ] HTTPS works with valid certificate
- [ ] ALB OIDC authentication works with IAM Identity Center
- [ ] Users can log in with AD credentials
- [ ] Landing page shows all 6 app cards (1 active, 5 coming soon)
- [ ] Clicking Sales Journal navigates to /sales-journal and loads app
- [ ] Sales Journal app fully functional (all features work)
- [ ] Session persists across app navigation
- [ ] No console errors or warnings
- [ ] Performance targets met (< 2s load time)
- [ ] Cost within budget (~$32/month)
- [ ] Rollback plan tested and validated

---

## Next Actions

1. **Create app launcher artifacts** (HTML, Docker, nginx config)
2. **Update Sales Journal** for base path routing
3. **Test locally** before AWS deployment
4. **Execute AWS resource creation** (ECS, ECR, ALB config)
5. **Deploy and test** end-to-end flow
6. **Document** any changes or learnings
7. **Plan for apps #2-6** based on this template

---

**Document Version:** 1.0
**Last Updated:** October 4, 2025
**Status:** Ready for implementation
**Target: Next week (progress-dependent)**
