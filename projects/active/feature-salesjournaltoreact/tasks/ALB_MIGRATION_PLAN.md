# ALB Migration Plan - Sales Journal SSO Implementation

**Purpose:** Migrate from Amplify + Cognito to ALB + IAM Identity Center for working SSO authentication
**Estimated Time:** 3-4 hours
**Downtime Required:** ~30 minutes (during DNS cutover)

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Prerequisites](#prerequisites)
3. [Implementation Steps](#implementation-steps)
4. [Testing Plan](#testing-plan)
5. [Rollback Plan](#rollback-plan)
6. [Cost Implications](#cost-implications)

---

## Architecture Overview

### New Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Browser                             │
└────────────┬────────────────────────────────────────────────────┘
             │
             │ HTTPS Request
             ▼
┌─────────────────────────────────────────────────────────────────┐
│              Application Load Balancer (ALB)                     │
│                                                                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  Listener Rule: Authenticate with IAM Identity Center  │    │
│  └────────────────────────────────────────────────────────┘    │
│                           │                                      │
│                           │ No session cookie?                   │
│                           ▼                                      │
│              ┌─────────────────────────────┐                    │
│              │  Redirect to IAM IdC login   │                    │
│              └─────────────────────────────┘                    │
└────────────┬────────────────────────────────────────────────────┘
             │
             │ Authenticated request with headers:
             │ - x-amzn-oidc-identity
             │ - x-amzn-oidc-data (JWT with user claims)
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Target Group                                  │
│                                                                   │
│  ┌──────────────────┐          ┌──────────────────┐            │
│  │  EC2 Instance    │    OR    │  ECS Fargate     │            │
│  │  (nginx + React) │          │  (nginx + React) │            │
│  └──────────────────┘          └──────────────────┘            │
│         │                              │                         │
│         └──────────────┬───────────────┘                        │
│                        │                                         │
│                        │ API calls                               │
│                        ▼                                         │
│         ┌────────────────────────────────┐                      │
│         │  API Gateway + Lambda (keeps)  │                      │
│         │  (existing backend unchanged)  │                      │
│         └────────────────────────────────┘                      │
└─────────────────────────────────────────────────────────────────┘
             │
             │ Data queries
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Data Sources                                  │
│  - Snowflake                                                     │
│  - Other data connections (unchanged)                            │
└─────────────────────────────────────────────────────────────────┘

Authentication Flow:
┌───────────┐      ┌───────┐      ┌──────────────┐      ┌──────┐
│    ALB    │─────▶│ IdC   │─────▶│ AD (LDAP)    │─────▶│ User │
│           │◀─────│       │◀─────│ graniterock  │◀─────│      │
└───────────┘      └───────┘      └──────────────┘      └──────┘
    │                   │
    │ Sets OIDC        │ Returns
    │ session cookie   │ user claims
    │                   │
    ▼                   ▼
React App receives headers with authenticated user info
```

### Key Components

1. **Application Load Balancer (ALB)**
   - Handles all incoming HTTPS traffic
   - Authenticates users via IAM Identity Center (OIDC)
   - Injects user information in request headers
   - Manages session cookies

2. **IAM Identity Center Application (new)**
   - Application type: **Customer managed** (not custom SAML)
   - Protocol: **OIDC** (not SAML)
   - Connected to Active Directory (existing)

3. **React App Hosting** (choose one):
   - **Option A: EC2** - Simple t3.small instance with nginx
   - **Option B: ECS Fargate** - Containerized deployment (recommended for prod)

4. **Backend (unchanged)**
   - Keep existing API Gateway + Lambda
   - Update to validate ALB headers (optional security enhancement)

---

## Prerequisites

### Required AWS Resources
- ✅ IAM Identity Center instance (already created)
- ✅ Active Directory connection (already configured)
- ✅ User groups in AD (already synced)
- ⏳ VPC with public/private subnets (verify exists)
- ⏳ SSL certificate in ACM for your domain
- ⏳ Target hosting decision (EC2 vs ECS)

### Required Access
- IAM permissions to create:
  - Application Load Balancers
  - Target Groups
  - EC2 instances or ECS services
  - IAM roles for ALB and compute
  - IAM Identity Center applications

### Preparation Tasks
1. **Build production React bundle:**
   ```bash
   cd /Users/TehFiestyGoat/da-agent-hub/react-sales-journal
   npm run build
   # Creates optimized production build in dist/
   ```

2. **Test build locally:**
   ```bash
   npm run preview
   # Verify app works at http://localhost:4173
   ```

3. **Update app to read ALB headers:**
   - Modify AuthProvider to check for `x-amzn-oidc-data` header
   - Parse JWT to extract user email, name, groups
   - No login redirect needed - ALB handles it

---

## Implementation Steps

### Phase 1: Create IAM Identity Center Application (30 min)

1. **Create new application in IAM Identity Center:**
   ```bash
   aws sso-admin create-application \
     --instance-arn arn:aws:sso:::instance/ssoins-790755f0cd17e168 \
     --name "Sales Journal ALB" \
     --description "Sales Journal with ALB authentication" \
     --application-provider-arn arn:aws:sso::aws:applicationProvider/custom \
     --region us-west-2
   ```

2. **Configure application in AWS Console:**
   - Go to: https://us-west-2.console.aws.amazon.com/singlesignon/home
   - Find "Sales Journal ALB" application
   - Click "Actions" → "Edit configuration"
   - **Application type:** Customer managed
   - **Sign-in URL:** `https://your-alb-domain.com` (will update after ALB creation)
   - **Sign-out URL:** Leave blank initially

3. **Assign users/groups:**
   - Use existing "Snow Flake SSO" group
   - Or assign individual users

4. **Get OIDC details (save these):**
   - Client ID
   - Client secret
   - Issuer URL: `https://oidc.us-west-2.amazonaws.com/[instance-id]`
   - Authorization endpoint
   - Token endpoint
   - User info endpoint

### Phase 2: Setup React App Hosting (45-60 min)

#### Option A: EC2 Instance (Simpler)

1. **Launch EC2 instance:**
   ```bash
   # Amazon Linux 2023, t3.small, in public subnet
   # Security group: Allow 80 from ALB security group
   aws ec2 run-instances \
     --image-id ami-0c55b159cbfafe1f0 \
     --instance-type t3.small \
     --key-name your-key \
     --security-group-ids sg-xxxxx \
     --subnet-id subnet-xxxxx \
     --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=SalesJournal-Web}]'
   ```

2. **Install nginx and copy build files:**
   ```bash
   # SSH to instance
   ssh ec2-user@instance-ip

   # Install nginx
   sudo yum install -y nginx

   # Upload build files
   # On local machine:
   cd /Users/TehFiestyGoat/da-agent-hub/react-sales-journal
   tar czf dist.tar.gz dist/
   scp dist.tar.gz ec2-user@instance-ip:~/

   # On instance:
   cd /usr/share/nginx/html
   sudo tar xzf ~/dist.tar.gz
   sudo mv dist/* .
   sudo rmdir dist
   ```

3. **Configure nginx:**
   ```bash
   # Create /etc/nginx/conf.d/sales-journal.conf
   sudo tee /etc/nginx/conf.d/sales-journal.conf <<'EOF'
   server {
       listen 80;
       server_name _;
       root /usr/share/nginx/html;
       index index.html;

       # React Router support
       location / {
           try_files $uri $uri/ /index.html;
       }

       # Pass ALB headers to React app (accessible via window.location)
       # React will read these from meta tags we inject
       location = /index.html {
           add_header Cache-Control "no-cache";
           sub_filter '</head>' '
               <meta name="x-amzn-oidc-identity" content="$http_x_amzn_oidc_identity">
               <meta name="x-amzn-oidc-data" content="$http_x_amzn_oidc_data">
               </head>';
           sub_filter_once on;
       }

       # API proxy (optional, or keep direct API Gateway calls)
       location /api/ {
           proxy_pass https://4gihwvts8c.execute-api.us-west-2.amazonaws.com/;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   EOF

   sudo systemctl restart nginx
   sudo systemctl enable nginx
   ```

#### Option B: ECS Fargate (Production-ready)

1. **Create Dockerfile:**
   ```dockerfile
   FROM nginx:alpine
   COPY dist/ /usr/share/nginx/html/
   COPY nginx.conf /etc/nginx/conf.d/default.conf
   EXPOSE 80
   CMD ["nginx", "-g", "daemon off;"]
   ```

2. **Build and push to ECR:**
   ```bash
   # Create ECR repository
   aws ecr create-repository --repository-name sales-journal-web --region us-west-2

   # Build and push
   aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 129515616776.dkr.ecr.us-west-2.amazonaws.com
   docker build -t sales-journal-web .
   docker tag sales-journal-web:latest 129515616776.dkr.ecr.us-west-2.amazonaws.com/sales-journal-web:latest
   docker push 129515616776.dkr.ecr.us-west-2.amazonaws.com/sales-journal-web:latest
   ```

3. **Create ECS cluster and service:**
   - Use AWS Console or CDK
   - Fargate task: 0.5 vCPU, 1GB memory
   - Task role with permissions for Secrets Manager (if needed)

### Phase 3: Create Application Load Balancer (45 min)

1. **Create ALB:**
   ```bash
   aws elbv2 create-load-balancer \
     --name sales-journal-alb \
     --subnets subnet-xxxxx subnet-yyyyy \
     --security-groups sg-alb \
     --scheme internet-facing \
     --type application \
     --region us-west-2
   ```

2. **Create target group:**
   ```bash
   # For EC2:
   aws elbv2 create-target-group \
     --name sales-journal-tg \
     --protocol HTTP \
     --port 80 \
     --vpc-id vpc-xxxxx \
     --health-check-path / \
     --health-check-interval-seconds 30 \
     --region us-west-2

   # Register EC2 instance:
   aws elbv2 register-targets \
     --target-group-arn arn:aws:elasticloadbalancing:... \
     --targets Id=i-xxxxx \
     --region us-west-2
   ```

3. **Create HTTPS listener with IAM Identity Center auth:**

   **Via AWS Console (easier):**
   - Go to EC2 → Load Balancers → sales-journal-alb
   - Listeners tab → Add listener
   - Protocol: HTTPS, Port: 443
   - Default SSL certificate: Select from ACM
   - **Add rule: Authenticate**
     - Action type: Authenticate with IAM Identity Center
     - Client ID: [from Phase 1]
     - Client secret: [from Phase 1]
     - Issuer: https://oidc.us-west-2.amazonaws.com/[instance-id]
     - Authorization endpoint: [from Phase 1]
     - Token endpoint: [from Phase 1]
     - User info endpoint: [from Phase 1]
     - Session cookie name: AWSELBAuthSessionCookie
     - Session timeout: 8 hours (28800 seconds)
     - Scope: openid, email, profile
     - On unauthenticated request: Authenticate
   - **Then add action: Forward to target group**
     - Target group: sales-journal-tg

4. **Update IAM Identity Center application callback:**
   - Get ALB DNS name: `sales-journal-alb-xxxxx.us-west-2.elb.amazonaws.com`
   - Update IAM Identity Center application:
     - Callback URL: `https://[ALB-DNS]/oauth2/idpresponse`
     - Sign-in URL: `https://[ALB-DNS]`

### Phase 4: Update React App for ALB Auth (30 min)

Create new `src/components/auth/ALBAuthProvider.tsx`:

```typescript
import React, { useEffect, useState } from 'react';

interface ALBUser {
  email: string;
  name: string;
  sub: string;
}

interface ALBAuthProviderProps {
  children: (user: ALBUser | null, signOut: () => void) => React.ReactNode;
}

export const ALBAuthProvider: React.FC<ALBAuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<ALBUser | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Read ALB-injected user data from meta tags
    const identityMeta = document.querySelector('meta[name="x-amzn-oidc-identity"]');
    const dataMeta = document.querySelector('meta[name="x-amzn-oidc-data"]');

    if (dataMeta) {
      try {
        // x-amzn-oidc-data is a JWT with user claims
        const jwt = dataMeta.getAttribute('content');
        if (jwt) {
          // Decode JWT (it's already validated by ALB)
          const payload = JSON.parse(atob(jwt.split('.')[1]));

          setUser({
            email: payload.email,
            name: payload.name || payload.email,
            sub: payload.sub,
          });
        }
      } catch (error) {
        console.error('Failed to parse ALB user data:', error);
      }
    }

    setLoading(false);
  }, []);

  const signOut = () => {
    // Redirect to ALB logout endpoint
    window.location.href = '/logout';
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  // If no user data, ALB should have redirected to login
  // But if somehow we're here without auth, show error
  if (!user) {
    return <div>Authentication required. Please refresh the page.</div>;
  }

  return <>{children(user, signOut)}</>;
};
```

Update `src/App.tsx`:

```typescript
import { ALBAuthProvider } from './components/auth/ALBAuthProvider';

const App: React.FC = () => {
  const isDevelopment = import.meta.env.DEV;
  const AuthComponent = isDevelopment ? DevAuthBypass : ALBAuthProvider;

  return (
    <ThemeProvider theme={graniteRockTheme}>
      <GlobalStyles />
      <Router>
        <Routes>
          <Route
            path="/*"
            element={
              <AuthComponent>
                {(user, signOut) => <AuthenticatedApp user={user} signOut={signOut} />}
              </AuthComponent>
            }
          />
        </Routes>
      </Router>
    </ThemeProvider>
  );
};
```

### Phase 5: DNS and Final Configuration (15 min)

1. **Create Route 53 alias record** (or update existing):
   ```
   sales-journal.graniterock.com → ALIAS → sales-journal-alb-xxxxx.elb.amazonaws.com
   ```

2. **Test authentication flow:**
   - Visit https://sales-journal.graniterock.com
   - Should redirect to IAM Identity Center login
   - Login with AD credentials
   - Should redirect back to app with session cookie
   - App should display user's name from ALB headers

3. **Update Amplify environment variables** (if keeping API Gateway):
   ```bash
   aws amplify update-app \
     --app-id [app-id] \
     --environment-variables VITE_AUTH_MODE=alb \
     --region us-west-2
   ```

---

## Testing Plan

### Pre-Deployment Tests
- [ ] Build production bundle locally: `npm run build`
- [ ] Test preview locally: `npm run preview`
- [ ] Verify all routes work (React Router)
- [ ] Test API calls work (update base URL if needed)

### Post-Deployment Tests
- [ ] **Authentication flow:**
  - [ ] Visit app URL → redirects to IAM Identity Center
  - [ ] Login with AD credentials → success
  - [ ] Redirected back to app → user info displayed
  - [ ] Session cookie persists (8 hours)

- [ ] **Authorization:**
  - [ ] User in "Snow Flake SSO" group → access granted
  - [ ] User not in group → access denied (if configured)

- [ ] **Application functionality:**
  - [ ] Dashboard loads with data
  - [ ] Sales Journal page works
  - [ ] Detail by Ticket page works
  - [ ] All API calls succeed
  - [ ] Pipeline Control functions

- [ ] **Session management:**
  - [ ] Session persists across page refreshes
  - [ ] Sign out works → clears session
  - [ ] Session expires after 8 hours → re-authenticate

### Load Testing (Optional)
- [ ] Test with 10+ concurrent users
- [ ] Verify ALB distributes load (if using multiple targets)
- [ ] Check ALB CloudWatch metrics

---

## Rollback Plan

### Quick Rollback (5 min)
If issues arise during deployment:

1. **DNS rollback:**
   ```bash
   # Point DNS back to Amplify
   # Update Route 53 record:
   sales-journal.graniterock.com → master.dwau7b1q9q1iw.amplifyapp.com
   ```

2. **Keep DevAuthBypass active** in production temporarily

### Full Rollback (15 min)
If ALB approach doesn't work:

1. Revert DNS to Amplify
2. Delete ALB and target group
3. Terminate EC2 instance or delete ECS service
4. Delete IAM Identity Center "Sales Journal ALB" application
5. Document lessons learned

---

## Cost Implications

### Current Monthly Costs (Amplify + Cognito)
- Amplify Hosting: ~$15/month (build + hosting)
- Cognito User Pool: Free tier (< 50,000 MAU)
- **Total: ~$15/month**

### New Monthly Costs (ALB)
- **ALB:** ~$22/month (base) + $0.008/LCU-hour (~$6/month for low traffic) = **~$28/month**
- **EC2 t3.small:** ~$15/month (on-demand) OR ~$10/month (1-year reserved)
  - Alternative: ECS Fargate = ~$12/month (0.5 vCPU, 1GB, 24/7)
- **NAT Gateway:** ~$32/month (if needed for private subnet)
- **CloudWatch logs:** ~$5/month
- **Total: ~$50-80/month** (depending on NAT Gateway need)

### Cost Optimization Options
1. Use EC2 reserved instances (-33% cost)
2. Use ECS Fargate Spot (if acceptable availability)
3. Share NAT Gateway with other services
4. Reduce CloudWatch log retention

### Cost vs. Benefit
- **Benefit:** Working SSO with AD integration
- **Benefit:** Better security and user management
- **Benefit:** Scalable architecture
- **Cost increase:** ~$35-65/month
- **ROI:** Acceptable for enterprise SSO requirement

---

## Security Considerations

### ALB Security
- [ ] Use HTTPS only (redirect HTTP → HTTPS)
- [ ] Use latest TLS version (1.2+)
- [ ] Configure security group: Allow 443 from 0.0.0.0/0, deny all else
- [ ] Enable access logs to S3
- [ ] Enable WAF (optional, adds cost)

### IAM Identity Center
- [ ] Assign only required users/groups
- [ ] Use group-based assignment (not individual users)
- [ ] Set appropriate session timeout (8 hours recommended)
- [ ] Review CloudTrail logs for authentication events

### Instance/Container Security
- [ ] Security group: Allow 80 only from ALB security group
- [ ] No public IP address (use private subnet + NAT)
- [ ] Use IAM role for AWS API access (not access keys)
- [ ] Keep nginx and OS updated
- [ ] Enable Systems Manager Session Manager (no SSH key needed)

### API Security (Optional Enhancement)
Update Lambda to validate ALB headers:
```python
def validate_alb_headers(event):
    # Verify request came through ALB with valid auth
    if 'x-amzn-oidc-data' not in event['headers']:
        raise Exception('Unauthorized: No ALB authentication')

    # Decode and validate JWT
    jwt_token = event['headers']['x-amzn-oidc-data']
    # Validate signature using ALB public key
    # ...
    return user_claims
```

---

## Maintenance Tasks

### Ongoing Maintenance
- Monitor ALB CloudWatch metrics (request count, latency, errors)
- Review IAM Identity Center audit logs monthly
- Update React app: `npm run build` → upload to EC2/ECS
- Patch nginx and OS monthly (EC2 option)
- Rebuild container monthly (ECS option)

### Scaling Considerations
- Add more EC2 instances or ECS tasks as traffic grows
- Configure ALB auto-scaling based on metrics
- Consider CloudFront in front of ALB for global performance

---

## Timeline

### Recommended Implementation Schedule

**Week 1: Planning and Preparation**
- Day 1: Review architecture, get approvals
- Day 2-3: Create IAM Identity Center application, test authentication
- Day 4-5: Update React app code for ALB auth, test locally

**Week 2: Infrastructure Deployment**
- Day 1: Create EC2/ECS infrastructure, deploy React app
- Day 2: Create ALB, configure authentication
- Day 3: Integration testing, fix any issues
- Day 4: User acceptance testing
- Day 5: DNS cutover, production deployment

**Total: 2 weeks** (conservative timeline with testing)

**Fast-track: 1 day** (if urgent, but higher risk)

---

## Success Criteria

- [ ] Users can access app via bookmark/URL (no AWS portal required)
- [ ] Authentication via AD credentials works
- [ ] User information displayed correctly in app
- [ ] All application features functional
- [ ] Session persists appropriately
- [ ] Sign out clears session
- [ ] No security vulnerabilities
- [ ] Acceptable performance (< 2s page load)
- [ ] Cost within approved budget

---

## Additional Resources

### AWS Documentation
- [ALB Authentication with OIDC](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/listener-authenticate-users.html)
- [IAM Identity Center Applications](https://docs.aws.amazon.com/singlesignon/latest/userguide/manage-your-applications.html)
- [ECS Fargate Getting Started](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/getting-started-fargate.html)

### Related Documentation
- `SSO_IMPLEMENTATION_STATUS.md` - Current state and why ALB is needed
- `COGNITO_SAML_SETUP.md` - Previous SAML attempt (for reference only)
- `amplify/backend.ts` - Keep existing API Gateway + Lambda

---

## Questions and Decisions Needed

Before proceeding with implementation:

1. **Hosting model:** EC2 or ECS Fargate?
   - Recommendation: **ECS Fargate** (more scalable, less maintenance)

2. **DNS domain:** What domain to use?
   - Option A: `sales-journal.graniterock.com` (new subdomain)
   - Option B: Update existing Amplify domain

3. **Deployment window:** When can we schedule 30-minute downtime?
   - Best: Outside business hours
   - Alternative: Gradual rollout with DNS TTL

4. **Budget approval:** Confirm ~$50-80/month is acceptable
   - Additional cost vs. no working SSO

5. **User groups:** Finalize which AD groups should have access
   - Current: "Snow Flake SSO" group
   - Consider: Additional groups for different access levels

---

**Next Steps:** Review this plan, make decisions on open questions, then schedule implementation session.
