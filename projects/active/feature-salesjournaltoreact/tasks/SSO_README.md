# Sales Journal SSO Implementation - Quick Reference

**Last Updated:** October 4, 2025
**Current Status:** SSO non-functional, ALB migration recommended

---

## 📋 Documentation Index

| Document | Purpose | Status |
|----------|---------|--------|
| **[SSO_IMPLEMENTATION_STATUS.md](SSO_IMPLEMENTATION_STATUS.md)** | Comprehensive analysis of Cognito+SAML attempt and why it failed | ✅ Complete |
| **[ALB_MIGRATION_PLAN.md](ALB_MIGRATION_PLAN.md)** | Step-by-step guide for implementing working SSO with ALB | ✅ Ready to implement |
| **[COGNITO_SAML_SETUP.md](COGNITO_SAML_SETUP.md)** | Original SAML configuration (deprecated, kept for reference) | ⚠️ Non-functional |
| **[AWS_SSO_SETUP_INSTRUCTIONS.md](AWS_SSO_SETUP_INSTRUCTIONS.md)** | IAM Identity Center setup (completed successfully) | ✅ Complete |

---

## 🎯 Current Situation

### What Works ✅
- ✅ Application deployed to AWS Amplify: https://master.dwau7b1q9q1iw.amplifyapp.com
- ✅ API Gateway + Lambda backend functional
- ✅ IAM Identity Center configured with Active Directory
- ✅ User authentication to IAM Identity Center works (password validation succeeds)
- ✅ DevAuthBypass works for local development
- ✅ All application features work (when auth is bypassed)

### What Doesn't Work ❌
- ❌ SAML SSO from Cognito to IAM Identity Center
- ❌ SP-initiated authentication flow (user starts from app URL)
- ❌ IdP-initiated authentication flow (user starts from AWS portal)
- ❌ Production user authentication (SSO required)

### Root Cause
**IAM Identity Center's custom SAML applications** are incompatible with **Cognito's SP-initiated SAML flows**. This is a fundamental architectural limitation, not a configuration issue.

After extensive debugging (multiple hours):
- Verified all SAML metadata and attribute mappings are correct
- Confirmed user has proper application assignments
- Tested both SP-initiated and IdP-initiated flows
- Persistent "Bad input" and "No access" errors
- CloudTrail shows authentication succeeds but authorization fails

**Conclusion:** This pattern (Cognito + SAML + IAM Identity Center) is not viable. AWS recommends ALB for web apps with IAM Identity Center SSO.

---

## 🚀 Recommended Path Forward

### Option 1: ALB with IAM Identity Center (RECOMMENDED)
**Implementation Time:** 3-4 hours
**Status:** Documented and ready to implement

**Benefits:**
- ✅ Native AWS support - purpose-built for this use case
- ✅ SP-initiated flows work correctly
- ✅ Users start directly from app URL
- ✅ Simpler configuration (OIDC instead of SAML)
- ✅ Better security and session management

**Next Steps:**
1. Review [ALB_MIGRATION_PLAN.md](ALB_MIGRATION_PLAN.md)
2. Make architecture decisions:
   - Hosting: EC2 vs ECS Fargate
   - DNS: Subdomain selection
   - Budget: Approve ~$50-80/month cost increase
3. Schedule 3-4 hour implementation window
4. Execute migration plan

**Cost:** ~$50-80/month (vs current $15/month)

### Option 2: Keep DevAuthBypass in Production (INTERIM)
**Implementation Time:** 5 minutes
**Status:** Already implemented for development

**Use case:** Temporary solution while planning ALB migration

**How it works:**
- Users enter any email address (no password required)
- No actual authentication - dev/testing only
- **Security risk:** Not suitable for production long-term

**Steps:**
```typescript
// In src/App.tsx, remove environment check:
const AuthComponent = DevAuthBypass; // Was: isDevelopment ? DevAuthBypass : AuthProvider
```

**When to use:**
- Need app working immediately
- Planning ALB migration within 1-2 weeks
- Internal testing only (not customer-facing)

### Option 3: Different IdP (NOT RECOMMENDED)
**Implementation Time:** 1-2 days
**Cost:** Additional service fees

Use third-party IdP (Okta, Auth0) between AD and Cognito.

**Why not recommended:**
- Adds complexity and cost
- Still using Cognito (when ALB is better)
- Requires ongoing IdP subscription
- More moving parts to maintain

---

## 📊 Configuration Reference

### Current AWS Resources

**IAM Identity Center:**
```
Instance: ssoins-790755f0cd17e168
Region: us-west-2
Directory: graniterock.corp (d-9267138180)
Application: Sales Journal (apl-9d89a42057729784)
User: ckaiser@graniterock.com (9267138180-3c372556-5d35-489e-8936-1cef3771069c)
```

**Cognito (configured but non-functional):**
```
User Pool: us-west-2_tiuhvmLJZ
Domain: graniterock-sales-journal.auth.us-west-2.amazoncognito.com
SAML Provider: GraniteRock-SSO
App Client: 7feo9ck7c4icop4flic4be9duk
```

**Application:**
```
Frontend: https://master.dwau7b1q9q1iw.amplifyapp.com
Backend API: https://4gihwvts8c.execute-api.us-west-2.amazonaws.com
Local Dev: http://localhost:5173
Local API: http://localhost:8000
```

### Quick Commands

**Check IAM Identity Center user:**
```bash
aws identitystore describe-user \
  --identity-store-id d-9267138180 \
  --user-id 9267138180-3c372556-5d35-489e-8936-1cef3771069c \
  --region us-west-2
```

**Check application assignments:**
```bash
aws sso-admin list-application-assignments \
  --application-arn arn:aws:sso::129515616776:application/ssoins-790755f0cd17e168/apl-9d89a42057729784 \
  --region us-west-2
```

**Check Cognito SAML provider:**
```bash
aws cognito-idp describe-identity-provider \
  --user-pool-id us-west-2_tiuhvmLJZ \
  --provider-name GraniteRock-SSO \
  --region us-west-2
```

**View CloudTrail authentication events:**
```bash
aws cloudtrail lookup-events \
  --region us-west-2 \
  --max-results 5 \
  --query 'Events[?contains(CloudTrailEvent, `ckaiser`)]'
```

---

## 🔧 Development Workflow

### Local Development (Works)
```bash
# Terminal 1: Start backend API
cd /Users/TehFiestyGoat/da-agent-hub/react-sales-journal
source venv/bin/activate
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Start frontend
npm run dev
# Access at http://localhost:5173
# DevAuthBypass allows entering any email
```

### Production Build
```bash
# Build optimized production bundle
npm run build

# Test production build locally
npm run preview
# Access at http://localhost:4173
```

### Deploy to Amplify
```bash
# Amplify deploys automatically on git push to main branch
git add .
git commit -m "Update: <description>"
git push origin main

# Or trigger manual deployment:
git push origin main
```

---

## ⏱️ Timeline to Working SSO

| Approach | Implementation Time | When Available |
|----------|-------------------|----------------|
| **ALB Migration** | 3-4 hours | 1-2 weeks (with planning) |
| **DevAuthBypass (interim)** | 5 minutes | Immediate |
| **Different IdP** | 1-2 days | 1 week |

---

## 📞 Next Steps

### Immediate (Today)
- [x] Document current state and lessons learned
- [x] Create ALB migration plan
- [x] Update deprecated SAML documentation
- [ ] Review documentation with stakeholders
- [ ] Decide on interim vs. permanent solution

### Short-term (This Week)
- [ ] Make architecture decisions for ALB (EC2 vs ECS, DNS, budget)
- [ ] Get approval for cost increase (~$35-65/month)
- [ ] Schedule implementation window (3-4 hours)
- [ ] Assign resources for ALB implementation

### Long-term (Next 2 Weeks)
- [ ] Execute ALB migration plan
- [ ] User acceptance testing
- [ ] Production cutover
- [ ] Monitor and optimize
- [ ] Document final architecture

---

## 📚 Additional Resources

### AWS Documentation
- [ALB Authentication with OIDC](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/listener-authenticate-users.html)
- [IAM Identity Center Applications](https://docs.aws.amazon.com/singlesignon/latest/userguide/manage-your-applications.html)
- [Troubleshooting IAM Identity Center](https://docs.aws.amazon.com/singlesignon/latest/userguide/troubleshooting.html)

### Project Files
- `amplify/auth/resource.ts` - Auth configuration (needs replacement for ALB)
- `src/components/auth/AuthProvider.tsx` - Current auth component
- `src/components/auth/DevAuthBypass.tsx` - Dev bypass (working)
- `src/components/auth/ALBAuthProvider.tsx` - Future ALB auth (to be created)

---

## 🤝 Support

**For questions about:**
- **Current state:** See [SSO_IMPLEMENTATION_STATUS.md](SSO_IMPLEMENTATION_STATUS.md)
- **ALB implementation:** See [ALB_MIGRATION_PLAN.md](ALB_MIGRATION_PLAN.md)
- **SAML configuration (deprecated):** See [COGNITO_SAML_SETUP.md](COGNITO_SAML_SETUP.md)
- **IAM Identity Center setup:** See [AWS_SSO_SETUP_INSTRUCTIONS.md](AWS_SSO_SETUP_INSTRUCTIONS.md)

**Technical issues:**
- Check CloudTrail logs for authentication events
- Verify IAM Identity Center user assignments
- Review `SSO_IMPLEMENTATION_STATUS.md` for known issues
- Test with DevAuthBypass to isolate auth vs. app issues

---

**Document Version:** 1.0
**Last Updated:** October 4, 2025
**Maintained By:** Data & Analytics Team
**Contact:** See project documentation
