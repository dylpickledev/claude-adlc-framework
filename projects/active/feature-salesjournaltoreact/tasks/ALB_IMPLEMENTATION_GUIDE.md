# ALB Implementation Guide - Sales Journal SSO

**Status:** Ready for deployment
**Created:** October 4, 2025
**Implementation Artifacts:** Complete

---

## Implementation Artifacts Created

### 1. ALBAuthProvider.tsx
**Location:** `working/ALBAuthProvider.tsx`

**Purpose:** Production-ready React authentication provider that reads ALB-injected OIDC headers

**Features:**
- ✅ Reads x-amzn-oidc-data JWT from meta tags (injected by nginx)
- ✅ Parses JWT to extract user email, name, sub, groups
- ✅ Comprehensive error handling with detailed debug information
- ✅ Production-grade loading and error states
- ✅ No external authentication calls needed (ALB handles auth)
- ✅ Logout redirects to ALB logout endpoint

**Key Functions:**
- `readALBHeaders()`: Extracts auth data from DOM meta tags
- `parseJWT()`: Decodes JWT payload (signature already validated by ALB)
- `authenticateUser()`: Main authentication flow with error handling
- `signOut()`: Redirects to ALB logout endpoint

### 2. nginx-alb.conf
**Location:** `working/nginx-alb.conf`

**Purpose:** nginx configuration that receives ALB auth headers and injects them into React app

**Features:**
- ✅ Injects x-amzn-oidc-identity and x-amzn-oidc-data as meta tags
- ✅ React Router support (SPA routing)
- ✅ Static asset caching for performance
- ✅ Health check endpoint for ALB target group
- ✅ API proxy to existing API Gateway backend
- ✅ Gzip compression
- ✅ Security headers (X-Frame-Options, X-Content-Type-Options, etc.)

**Critical Section:**
```nginx
location = /index.html {
    sub_filter '</head>' '
        <meta name="x-amzn-oidc-identity" content="$http_x_amzn_oidc_identity">
        <meta name="x-amzn-oidc-data" content="$http_x_amzn_oidc_data">
    </head>';
}
```

### 3. Dockerfile
**Location:** `working/Dockerfile`

**Purpose:** Multi-stage Docker build for ECS Fargate deployment

**Features:**
- ✅ Multi-stage build (reduces image size)
- ✅ Stage 1: Node 18 Alpine for React build
- ✅ Stage 2: nginx Alpine for serving
- ✅ Includes nginx-alb.conf configuration
- ✅ Health check endpoint for container orchestration
- ✅ Production-optimized dependencies only

---

## Deployment Decisions Needed

### Decision 1: Hosting Model
**Options:**

**A) ECS Fargate (RECOMMENDED)**
- Cost: ~$12/month (0.5 vCPU, 1GB memory, 24/7)
- Pros: Scalable, no server management, container-native
- Cons: Slightly more complex initial setup

**B) EC2 t3.small**
- Cost: ~$15/month on-demand, ~$10/month reserved
- Pros: Simpler, traditional approach
- Cons: More maintenance (OS patches, etc.)

**Recommendation:** ECS Fargate - better scalability and less ongoing maintenance

### Decision 2: DNS Configuration
**Options:**

**A) sales-journal.graniterock.com (NEW SUBDOMAIN)**
- Pros: Clean, professional URL
- Cons: Requires new DNS record

**B) Update existing Amplify domain**
- Pros: No DNS change for users
- Cons: Amplify domain name is ugly

**Recommendation:** sales-journal.graniterock.com

### Decision 3: Deployment Window
**Downtime Required:** ~30 minutes (during DNS cutover)

**Best Times:**
- Evening after business hours (5pm-7pm)
- Weekend (Saturday morning)
- Early morning before business hours (6am-8am)

### Decision 4: Budget Approval
**Current Costs:** ~$15/month (Amplify hosting)
**New Costs:** ~$50-80/month
- ALB: ~$28/month
- ECS Fargate: ~$12/month
- CloudWatch logs: ~$5/month
- NAT Gateway (if needed): ~$32/month

**Cost Increase:** ~$35-65/month
**Business Value:** Working SSO with Active Directory integration

---

## Pre-Deployment Checklist

### AWS Resources Required
- [ ] Verify VPC with public/private subnets exists
- [ ] Request/verify SSL certificate in ACM for sales-journal.graniterock.com
- [ ] Confirm IAM permissions for ALB, ECS, IAM Identity Center
- [ ] Review security group configurations

### IAM Identity Center Setup
- [ ] Create new customer-managed application (not custom SAML)
- [ ] Use OIDC protocol (not SAML)
- [ ] Configure callback URL: `https://sales-journal-alb-xxx.elb.amazonaws.com/oauth2/idpresponse`
- [ ] Assign "Snow Flake SSO" group to application
- [ ] Save OIDC client ID, client secret, issuer URL

### Code Deployment Preparation
- [ ] Copy ALBAuthProvider.tsx to `react-sales-journal/src/components/auth/`
- [ ] Update App.tsx to use ALBAuthProvider (production) or DevAuthBypass (dev)
- [ ] Build production bundle: `npm run build`
- [ ] Test build locally: `npm run preview`
- [ ] Verify all application features work

### Infrastructure Deployment
- [ ] Create ECR repository: `sales-journal-web`
- [ ] Build Docker image using Dockerfile
- [ ] Push image to ECR
- [ ] Create ECS cluster and Fargate service
- [ ] Create ALB with OIDC authentication listener
- [ ] Create target group pointing to ECS service
- [ ] Configure health checks

### DNS and Final Steps
- [ ] Create Route 53 record: sales-journal.graniterock.com → ALB
- [ ] Update IAM Identity Center app with final DNS
- [ ] Test authentication flow end-to-end
- [ ] Monitor ALB CloudWatch metrics
- [ ] Update documentation

---

## Testing Protocol

### Pre-Deployment Testing (Local)
1. **Build verification:**
   ```bash
   cd /Users/TehFiestyGoat/da-agent-hub/react-sales-journal
   npm run build
   npm run preview
   ```

2. **Route testing:** Verify all React Router routes work
3. **API testing:** Confirm API calls to existing backend succeed
4. **DevAuthBypass:** Verify local development still works

### Post-Deployment Testing (Production)
1. **Authentication flow:**
   - Visit https://sales-journal.graniterock.com
   - Should redirect to IAM Identity Center login
   - Login with ckaiser@graniterock.com
   - Verify redirect back to app with user info displayed

2. **Authorization:**
   - Verify users in "Snow Flake SSO" group have access
   - Verify users not in group are denied (if configured)

3. **Application functionality:**
   - Dashboard loads with data
   - Sales Journal page works
   - Detail by Ticket page works
   - Out of Balance page works
   - Tieout Management page works
   - Research 1140 page works
   - Pipeline Control functions work
   - All filters, sorting, search work correctly

4. **Session management:**
   - Session persists across page refreshes
   - Session expires after configured timeout
   - Sign out clears session and redirects

5. **Performance:**
   - Page load time < 2 seconds
   - API response times acceptable
   - No console errors

---

## Rollback Plan

### Quick Rollback (5 minutes)
If critical issues arise:

1. **Point DNS back to Amplify:**
   ```bash
   # Update Route 53 record
   sales-journal.graniterock.com → master.dwau7b1q9q1iw.amplifyapp.com
   ```

2. **Enable DevAuthBypass in production** (temporary workaround)

### Full Rollback (15 minutes)
If ALB approach fundamentally doesn't work:

1. Revert DNS to Amplify
2. Delete ALB and target group
3. Stop ECS service and delete cluster
4. Delete IAM Identity Center ALB application
5. Delete ECR repository
6. Document lessons learned
7. Re-evaluate alternatives

---

## Architecture Comparison

### Current (Non-Functional)
```
User → Amplify CloudFront → React App → Cognito Login
                                   ↓
                            SAML Request
                                   ↓
                       IAM Identity Center (FAILS)
```

### New (ALB)
```
User → Route 53 DNS → ALB (OIDC auth intercept) → IAM Identity Center
                          ↓                               ↓
                    Auth succeeds?                 AD authentication
                          ↓                               ↓
                   Forward with headers ← ← ← ← ← ← ← ← ←
                          ↓
                    ECS Fargate (nginx + React)
                          ↓
                    API Gateway + Lambda (unchanged)
```

---

## Key Benefits of ALB Approach

1. **User Experience:** Users start directly from app URL (no AWS portal required)
2. **Native Integration:** ALB has first-class IAM Identity Center OIDC support
3. **Simpler Protocol:** OIDC instead of SAML complexity
4. **AWS Recommended:** Official pattern for web apps with IAM Identity Center
5. **Security:** Authentication happens before request reaches application
6. **Existing Infrastructure:** Uses same IAM Identity Center + AD integration
7. **Scalability:** ALB handles load balancing and auto-scaling

---

## Cost-Benefit Analysis

### Costs
- **Infrastructure:** +$35-65/month
- **Implementation Time:** 3-4 hours one-time
- **Ongoing Maintenance:** Minimal (container updates)

### Benefits
- **Working SSO:** Users can actually authenticate (current blocker)
- **AD Integration:** Leverages existing GraniteRock Active Directory
- **Better Security:** Centralized authentication, proper session management
- **Scalability:** Can handle increased traffic without code changes
- **Maintainability:** Standard AWS pattern, well-documented

### ROI
**Acceptable for enterprise application requiring SSO authentication**

---

## Next Steps

1. **Stakeholder Review:** Present this implementation plan
2. **Make Decisions:** Hosting (ECS), DNS (subdomain), budget approval
3. **Schedule Implementation:** Choose deployment window
4. **Execute Deployment:** Follow ALB_MIGRATION_PLAN.md step-by-step
5. **Test Thoroughly:** Complete testing protocol above
6. **Monitor:** Watch CloudWatch metrics, user feedback
7. **Update Documentation:** Mark SSO blocker resolved

---

## Related Documentation

- `SSO_IMPLEMENTATION_STATUS.md` - Why we needed ALB migration
- `ALB_MIGRATION_PLAN.md` - Detailed implementation steps
- `SSO_README.md` - Quick reference for all SSO docs
- `COGNITO_SAML_SETUP.md` - Failed SAML attempt (reference only)

---

**Implementation Status:** Ready for deployment after decisions made
**Estimated Implementation Time:** 3-4 hours
**Estimated Downtime:** 30 minutes (DNS cutover only)
**Success Probability:** High (AWS-recommended pattern)
