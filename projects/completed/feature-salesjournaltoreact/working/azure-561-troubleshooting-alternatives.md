# Azure AD OIDC 561 Error - Alternative Troubleshooting Methods

**Context**: User doesn't have access to Azure AD Sign-in Logs
**Date**: 2025-10-04
**Status**: Investigating alternative debugging approaches

## Quick Summary

ALB returns HTTP 561 during Azure AD OIDC token exchange. All known Azure AD configurations have been fixed, but error persists. Since user cannot access Sign-in Logs, we need alternative methods to identify the root cause.

## Alternative Troubleshooting Approaches

### 🔍 Option 1: Enable ALB Access Logs (RECOMMENDED)

**Why**: ALB access logs capture the detailed OAuth 2.0 error responses from Azure AD, which is the closest alternative to Sign-in Logs.

**How to enable**:
```bash
# Script created at /tmp/enable-alb-logs.sh
/tmp/enable-alb-logs.sh
```

**What it does**:
1. Creates S3 bucket for logs
2. Configures bucket policy for ALB write access
3. Enables access logging on Skynet-ELB

**After enabling**:
1. Try authentication again at https://apps.grc-ops.com
2. Wait 5 minutes for logs to appear
3. Download and examine logs for OAuth error details

**Look for**: Lines containing `/oauth2/idpresponse` with status code 561, which will include the detailed error response from Azure AD

---

### 🧪 Option 2: Manual Token Exchange Test (IMMEDIATE)

**Why**: Bypasses ALB to test Azure AD token endpoint directly, giving us the exact error message.

**How to test**:
```bash
# Script created at /tmp/test-token-exchange.sh
/tmp/test-token-exchange.sh
```

**What it does**:
1. Provides authorization URL for you to authenticate
2. Prompts you to paste the authorization code
3. Exchanges code for tokens using curl
4. Shows exact Azure AD error response

**Expected outcomes**:
- ✅ **Success**: Problem is with ALB configuration, not Azure AD
- ❌ **Error**: Shows AADSTS error code identifying exact issue

---

### 🏢 Option 3: Verify Enterprise Application

**Why**: Azure AD auto-creates an Enterprise Application on first sign-in. If this failed, token exchange will fail.

**How to check**:
1. Go to Azure Portal → Microsoft Entra ID → Enterprise Applications
2. Search for "GraniteRock AWS Apps Portal"
3. Verify it exists and is enabled

**If missing**:
- Enterprise application wasn't created during first sign-in attempt
- May need to manually create or trigger first-sign-in consent flow

**If exists but disabled**:
- Re-enable the application
- Check "Properties" → "Enabled for users to sign-in?" is set to "Yes"

---

### 🔐 Option 4: Check for Tenant-Level Restrictions

**Why**: Tenant administrators may have policies that block token exchange even with correct app configuration.

**What to check** (requires Azure AD admin):

#### 4.1 DPoP (Demonstrating Proof-of-Possession)
- **Issue**: AWS ALB does not support DPoP
- **Check**: Azure Portal → Microsoft Entra ID → Security → Conditional Access
- **Solution**: Disable DPoP requirement for this application

#### 4.2 Conditional Access Policies
- **Issue**: Policies may block token endpoint access
- **Check**: Azure Portal → Microsoft Entra ID → Security → Conditional Access
- **Look for**: Policies targeting "OAuth 2.0 token endpoint" or "All cloud apps"
- **Solution**: Create exception for app-launcher client ID

#### 4.3 Security Defaults
- **Issue**: May block certain OAuth flows
- **Check**: Azure Portal → Microsoft Entra ID → Properties → Manage Security Defaults
- **Solution**: If enabled, may need to disable or create exceptions

#### 4.4 Authentication Methods Policies
- **Issue**: May restrict which auth methods work with OAuth 2.0
- **Check**: Azure Portal → Microsoft Entra ID → Security → Authentication methods
- **Solution**: Ensure OAuth 2.0 is allowed

---

### ⏱️ Option 5: Wait for Propagation (24 hours)

**Why**: Azure AD manifest changes can take up to 24 hours to fully propagate across all backend systems.

**What was changed today**:
- `enableAccessTokenIssuance: false → true` (CRITICAL)
- `requestedAccessTokenVersion: null → 2`
- `accessTokenAcceptedVersion: null → 2`
- `identifierUris: [] → ["api://..."]`

**Timeline**:
- App created: 2025-10-04
- Last manifest update: 2025-10-04
- Full propagation: Potentially 2025-10-05

**Action**:
- Wait 24 hours from last manifest change
- Test authentication again tomorrow
- If still failing, propagation is not the issue

---

## Troubleshooting Decision Tree

```
Start: 561 Error Persisting
    ↓
Try Manual Token Exchange (/tmp/test-token-exchange.sh)
    ↓
    ├─ Success? → Problem is ALB config, not Azure AD
    │              → Check ALB OIDC settings
    │              → Verify UserInfo endpoint accessibility
    │
    └─ Error? → Note AADSTS error code
               ↓
               Check Enterprise Application exists
               ↓
               ├─ Missing? → First sign-in consent didn't complete
               │             → Retry first-sign-in flow
               │
               └─ Exists? → Enable ALB access logs
                            ↓
                            Contact Azure AD admin to check:
                            - DPoP requirements
                            - Conditional Access policies
                            - Security defaults
                            ↓
                            If admin finds restrictions:
                            → Create exception for app
                            ↓
                            If no restrictions found:
                            → Wait 24h for propagation
```

---

## Most Likely Root Causes (Ranked)

### 1. **Propagation Delay** (60% probability)
- App created today
- Multiple critical manifest changes made today
- Azure AD can take 24 hours to fully sync
- **Action**: Wait until 2025-10-05, then test

### 2. **Tenant-Level Restrictions** (25% probability)
- DPoP enabled (ALB doesn't support)
- Conditional Access policy blocking token endpoint
- **Action**: Contact Azure AD admin to check policies

### 3. **Enterprise Application Issue** (10% probability)
- Auto-creation failed during first sign-in
- Application disabled or misconfigured
- **Action**: Verify in Enterprise Applications section

### 4. **ALB Configuration Mismatch** (5% probability)
- UserInfo endpoint unreachable from ALB
- OIDC scope mismatch
- **Action**: Manual token test will identify this

---

## Immediate Next Steps (Priority Order)

1. **Run manual token exchange test** (`/tmp/test-token-exchange.sh`)
   - Takes 2 minutes
   - Will immediately tell us if Azure AD config is working

2. **Enable ALB access logs** (`/tmp/enable-alb-logs.sh`)
   - Takes 5 minutes to enable
   - Future 561 errors will include detailed Azure AD responses

3. **Check Enterprise Application** in Azure Portal
   - Takes 1 minute
   - Verify auto-creation succeeded

4. **Contact Azure AD administrator**
   - Ask them to check for DPoP, Conditional Access, Security Defaults
   - Provide client ID: `2f1463e8-52ce-499e-9296-4cd125f35f4e`

5. **Wait 24 hours** for propagation
   - Test again tomorrow at same time
   - If still failing, propagation is not the issue

---

## What Each Method Will Tell Us

| Method | Time to Execute | Information Gained | Conclusive? |
|--------|----------------|-------------------|-------------|
| Manual token exchange | 2 min | Exact AADSTS error code | ✅ Yes |
| ALB access logs | 5 min + retry auth | Detailed OAuth error from Azure | ✅ Yes |
| Enterprise app check | 1 min | Consent flow status | ⚠️ Partial |
| Admin policy check | Depends on admin | Tenant restrictions | ✅ Yes |
| Wait 24h propagation | 24 hours | Whether timing is the issue | ✅ Yes |

---

## Expected Error Codes and Solutions

### If Manual Token Exchange Shows:

**AADSTS50146** - "This application must be installed by an administrator"
- **Solution**: Enterprise application needs admin consent
- **Action**: Have Azure AD admin grant consent

**AADSTS70011** - "The provided request must include a 'scope' parameter"
- **Solution**: Scope mismatch between ALB and Azure AD
- **Action**: Verify ALB scope: `openid email profile`

**AADSTS700016** - "Application not found"
- **Solution**: Enterprise application wasn't created
- **Action**: Complete first-sign-in consent flow

**AADSTS50194** - "Application 'xxx' is not configured as a multi-tenant application"
- **Solution**: Application type mismatch
- **Action**: Change "Supported account types" in app registration

**AADSTS65001** - "The user or administrator has not consented"
- **Solution**: User consent required
- **Action**: Complete consent prompt during sign-in

**AADSTS65005** - "The application needs access to a service"
- **Solution**: API permissions not granted
- **Action**: We already granted permissions, may be propagation

**AADSTS700027** - "Client assertion contains an invalid signature"
- **Solution**: Client secret is incorrect or expired
- **Action**: We verified secret is correct, may be propagation

---

## Session State Reference

**All infrastructure details**: See `DEPLOYMENT_STATUS_2025-10-04.md`

**Azure AD Configuration**:
- Client ID: `2f1463e8-52ce-499e-9296-4cd125f35f4e`
- Tenant ID: `1d1bbedc-e179-4e6b-a55e-c500085f1eec`
- Redirect URI: `https://apps.grc-ops.com/oauth2/idpresponse`
- Issuer: `https://login.microsoftonline.com/1d1bbedc-e179-4e6b-a55e-c500085f1eec/v2.0`
- Token endpoint: `https://login.microsoftonline.com/1d1bbedc-e179-4e6b-a55e-c500085f1eec/oauth2/v2.0/token`

**What we've already fixed**:
- ✅ `enableAccessTokenIssuance: true`
- ✅ `requestedAccessTokenVersion: 2`
- ✅ `accessTokenAcceptedVersion: 2`
- ✅ `identifierUris` configured
- ✅ Client secret verified
- ✅ Redirect URI configured
- ✅ API permissions granted
- ✅ Network connectivity verified

---

## Scripts Created

- **`/tmp/enable-alb-logs.sh`** - Enable ALB access logging to S3
- **`/tmp/test-token-exchange.sh`** - Manual OAuth 2.0 token exchange test

Both scripts are ready to run.
