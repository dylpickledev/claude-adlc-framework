# SSO Implementation Summary

**Status:** ✅ Code Complete - Ready for AWS Configuration
**Date:** 2025-10-04
**Authentication Method:** IAM Identity Center + Directory Service (graniterock.corp)

---

## What Was Implemented

### 1. Authentication Components

**Created Files:**
- `src/components/auth/AuthProvider.tsx` - Main authentication wrapper
- `src/components/auth/DevAuthBypass.tsx` - Development bypass for local testing
- `src/pages/AuthCallback.tsx` - OAuth redirect handler
- `src/App.tsx` - App with automatic environment detection

**Features:**
- ✅ SSO-only authentication (no email/password)
- ✅ IAM Identity Center integration
- ✅ Directory Service authentication (graniterock.corp)
- ✅ **Automatic environment detection** (dev bypass locally, real SSO in production)
- ✅ Automatic redirect to GraniteRock SSO
- ✅ User info display in sidebar
- ✅ Secure sign out
- ✅ Loading states and error handling
- ✅ Local development without domain access

### 2. Amplify Configuration

**Modified Files:**
- `amplify/auth/resource.ts` - SAML SSO configuration

**Configuration:**
- Provider Name: `GraniteRockSSO`
- Callback URLs: localhost + production
- User Attributes: email, givenName, familyName
- Admin-provisioned users only (no self-service)

### 3. Dependencies Installed

```json
{
  "aws-amplify": "^6.15.7",
  "@aws-amplify/ui-react": "^6.13.0"
}
```

### 4. Documentation Created

**Setup Guides:**
1. `AWS_IAM_ROLE_SETUP.md` - Complete `react_dev` IAM role configuration
2. `IAM_IDENTITY_CENTER_SETUP.md` - Step-by-step SSO setup (7 phases)
3. `LOCAL_DEVELOPMENT.md` - **NEW:** Local development guide with automatic environment detection
4. `.env.example` - Environment variables template
5. `SSO_IMPLEMENTATION_SUMMARY.md` - This file

---

## 🆕 Automatic Environment Detection

The app now **automatically** detects whether it's running locally or in production and uses the appropriate authentication method:

### Local Development (http://localhost:5173)
- **Automatically uses `DevAuthBypass`** component
- No SSO configuration needed
- Development login screen with email input
- Session stored in `sessionStorage`
- Perfect for testing without domain access

### Production (AWS Amplify)
- **Automatically uses `AuthProvider`** component
- Real IAM Identity Center SSO
- Redirects to GraniteRock login
- Requires domain access

### How It Works

The `App.tsx` component uses `import.meta.env.DEV` to detect the environment:

```typescript
const isDevelopment = import.meta.env.DEV;
const AuthComponent = isDevelopment ? DevAuthBypass : AuthProvider;
```

**Benefits:**
- ✅ No manual file switching needed
- ✅ Same `App.tsx` works everywhere
- ✅ Safe to commit - production automatically uses real SSO
- ✅ Easy local testing - just run `npm run dev`

**See:** `LOCAL_DEVELOPMENT.md` for complete guide

---

## Next Steps (IT Admin Required)

### Step 1: Create `react_dev` IAM Role (30 min)

**Follow:** `AWS_IAM_ROLE_SETUP.md`

**Quick setup:**
```bash
# Assume you have admin access
aws iam create-role --role-name react_dev \
  --assume-role-policy-document file://trust-policy.json

aws iam put-role-policy --role-name react_dev \
  --policy-name ReactDevFullAccess \
  --policy-document file://react-dev-policy.json
```

**Verification:**
```bash
# Assume the role
aws sts assume-role --role-arn arn:aws:iam::129515616776:role/react_dev \
  --role-session-name test --external-id sales-journal-dev

# Test permissions
aws amplify list-apps --region us-west-2
aws cognito-idp list-user-pools --region us-west-2 --max-results 10
aws sso-admin list-instances --region us-west-2
```

### Step 2: Deploy App to AWS Amplify (15 min)

**Merge code and deploy:**
```bash
# 1. Create feature branch
git checkout -b feature/iam-identity-center-sso

# 2. Replace App.tsx
mv src/App.tsx src/App-original.tsx
mv src/App-with-auth.tsx src/App.tsx

# 3. Commit and deploy
git add .
git commit -m "feat: Add IAM Identity Center SSO authentication"
git push origin feature/iam-identity-center-sso

# 4. Create PR and merge
gh pr create --title "feat: IAM Identity Center SSO"
gh pr merge --squash
```

**Monitor build:**
```bash
aws amplify list-jobs --app-id dwau7b1q9q1iw \
  --branch-name master --region us-west-2 --max-items 1
```

### Step 3: Configure IAM Identity Center (2-3 hours)

**Follow:** `IAM_IDENTITY_CENTER_SETUP.md`

**7 Phases:**
1. Enable IAM Identity Center and connect to Directory Service
2. Get Cognito User Pool details from deployed app
3. Create custom SAML application in Identity Center
4. Add SAML identity provider to Cognito
5. Assign users to the application
6. Configure environment variables
7. Test and verify

**Key Information Needed:**
- Cognito User Pool ID (from AWS Console after deployment)
- Cognito App Client ID (from Cognito → App Integration)
- Cognito Domain (create if not exists)
- IAM Identity Center Instance ARN

### Step 4: Test SSO Flow (30 min)

**Production Testing:**
```bash
# Open app
open https://master.dwau7b1q9q1iw.amplifyapp.com

# Expected flow:
# 1. Shows "Sign in with GraniteRock SSO" button
# 2. Redirects to IAM Identity Center
# 3. Shows GraniteRock Directory Service login
# 4. Authenticates user
# 5. Redirects back to Sales Journal
# 6. Shows Dashboard with user info
```

**Local Development Testing:**
```bash
# 1. Create .env.local (after AWS setup complete)
cp .env.example .env.local
# Fill in values from Cognito

# 2. Start dev server
npm run dev

# 3. Test SSO flow on localhost:5173
```

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ User opens Sales Journal                                     │
│ https://master.dwau7b1q9q1iw.amplifyapp.com                 │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ AuthProvider checks authentication                           │
│ - No session → Show "Sign in with GraniteRock SSO" button  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ Redirect to AWS IAM Identity Center                         │
│ https://portal.sso.us-west-2.amazonaws.com                  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ IAM Identity Center authenticates via Directory Service     │
│ - User enters GraniteRock credentials                       │
│ - AD Connector forwards to graniterock.corp                 │
│ - Validates username/password                               │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ IAM Identity Center sends SAML response to Cognito          │
│ - Includes email, givenName, familyName                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ Cognito creates user session                                │
│ - Validates SAML response                                   │
│ - Creates Cognito user (if first login)                     │
│ - Issues JWT access token                                   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ Redirect back to Sales Journal with auth code               │
│ https://master.dwau7b1q9q1iw.amplifyapp.com/auth/callback  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ AuthCallback exchanges code for tokens                      │
│ - Amplify handles OAuth code flow automatically             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ AuthProvider validates session and shows app                │
│ - User sees Dashboard                                       │
│ - User info shown in sidebar                                │
│ - JWT token sent with all API requests                      │
└─────────────────────────────────────────────────────────────┘
```

---

## Files Modified

### New Files Created
- ✅ `src/components/auth/AuthProvider.tsx` - Real SSO authentication
- ✅ `src/components/auth/DevAuthBypass.tsx` - **NEW:** Local development bypass
- ✅ `src/pages/AuthCallback.tsx` - OAuth callback handler
- ✅ `src/App-dev.tsx` - **NEW:** Legacy dev bypass reference
- ✅ `.env.example` - Environment variables template
- ✅ `AWS_IAM_ROLE_SETUP.md` - IAM role setup guide
- ✅ `IAM_IDENTITY_CENTER_SETUP.md` - SSO setup guide (7 phases)
- ✅ `LOCAL_DEVELOPMENT.md` - **NEW:** Local development guide
- ✅ `SSO_IMPLEMENTATION_SUMMARY.md` - This file

### Modified Files
- ✅ `src/App.tsx` - **UPDATED:** Now has automatic environment detection
- ✅ `amplify/auth/resource.ts` - SAML SSO configuration
- ✅ `package.json` - Added aws-amplify dependencies

### Not Modified (Keep Original)
- ⏳ `src/components/layout/Sidebar.tsx` - Will need user props added (optional)

---

## Security Features

### ✅ Implemented
- SSO-only authentication (no password storage)
- Admin-provisioned users (IT controls access)
- SAML-based authentication (industry standard)
- Secure token exchange (OAuth 2.0 authorization code flow)
- JWT tokens for API authentication
- Environment variables for sensitive config (not committed)
- Automatic sign-out on session expiration

### 🔜 Recommended (Optional)
- MFA requirement via IAM Identity Center
- Session timeout configuration
- IP allowlisting for production
- CloudWatch alerting for failed auth attempts
- Audit logging of user sign-ins

---

## User Experience

### Sign In Flow
1. User navigates to app
2. Sees "Sign in with GraniteRock SSO" button with company branding
3. Clicks button → redirects to familiar GraniteRock login
4. Enters existing company credentials
5. Automatically redirected back to Sales Journal
6. Sees Dashboard with their name in sidebar

### Sign Out Flow
1. User clicks "Sign Out" button in sidebar
2. Session terminated in Cognito
3. Redirected to app homepage
4. Shows sign-in screen again

### Session Management
- Default session: 1 hour
- Auto-refresh tokens when active
- Graceful expiration handling (redirects to sign-in)

---

## Cost Estimate

**AWS IAM Identity Center:** Free
**AWS Cognito:**
- First 50,000 MAUs: Free
- After that: $0.0055/MAU
- **Estimated monthly cost:** $0 (< 50k users)

**Total estimated monthly cost:** **$0**

---

## Support & Troubleshooting

### Common Issues and Solutions

**Issue 1: "Access Denied" when setting up IAM role**
- **Solution:** Use root account or account admin to create `react_dev` role

**Issue 2: "Invalid SAML response"**
- **Solution:** Check attribute mapping in both IAM Identity Center and Cognito

**Issue 3: "User not assigned to application"**
- **Solution:** Assign user in IAM Identity Center → Applications → Sales Journal

**Issue 4: Environment variables not loading**
- **Solution:** Verify Amplify environment variables are set, then trigger new build

### Getting Help

1. **AWS Documentation:** https://docs.aws.amazon.com/singlesignon/
2. **Amplify Gen 2 Auth Docs:** https://docs.amplify.aws/gen2/build-a-backend/auth/
3. **Internal:** Contact ckaiser@graniterock.com for implementation questions

---

## Rollback Plan (If Needed)

If SSO implementation needs to be rolled back:

```bash
# 1. Revert to original App.tsx
git checkout main
mv src/App-original.tsx src/App.tsx

# 2. Revert auth/resource.ts
git checkout HEAD~1 amplify/auth/resource.ts

# 3. Deploy
git commit -am "revert: Remove SSO authentication"
git push origin main
```

---

## Success Criteria

- [ ] `react_dev` IAM role created and functional
- [ ] App deployed to AWS Amplify successfully
- [ ] IAM Identity Center connected to Directory Service
- [ ] Custom SAML application created
- [ ] SAML identity provider configured in Cognito
- [ ] Test user can sign in with GraniteRock credentials
- [ ] User info displays correctly in sidebar
- [ ] Sign out works correctly
- [ ] Local development environment configured
- [ ] All production tests passing

---

**Implementation Complete!** 🎉

The code is ready for deployment. Follow the setup guides in order:
1. `AWS_IAM_ROLE_SETUP.md`
2. Deploy the app
3. `IAM_IDENTITY_CENTER_SETUP.md`

**Questions?** Reach out to the project team for assistance.
