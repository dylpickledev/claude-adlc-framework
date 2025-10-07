# SSO Implementation Status - Sales Journal

**Last Updated:** October 4, 2025
**Status:** BLOCKED - Architectural incompatibility identified
**Recommended Path:** Migrate to ALB with IAM Identity Center authentication

---

## Executive Summary

After extensive troubleshooting, we've identified a fundamental architectural incompatibility between:
- Amazon Cognito User Pools
- AWS IAM Identity Center custom SAML applications
- SP-initiated SSO flows (user starts from app URL)

**Current State:** SSO authentication fails with "Bad input" error due to IAM Identity Center's custom SAML applications being designed exclusively for IdP-initiated flows (user starts from AWS access portal).

**Recommendation:** Migrate to Application Load Balancer (ALB) with native IAM Identity Center integration - the AWS-recommended pattern for web applications requiring SSO.

---

## What We Accomplished

### ✅ Successfully Configured

1. **IAM Identity Center Setup**
   - Instance: `ssoins-790755f0cd17e168` (us-west-2)
   - Directory: `graniterock.corp` (d-9267138180) - AD Connector
   - Users synced from Active Directory (20+ users)
   - Groups synced (2 groups including "Snow Flake SSO")

2. **SAML Application Created**
   - Application: "Sales Journal" (`apl-9d89a42057729784`)
   - SAML metadata URL: `https://portal.sso.us-west-2.amazonaws.com/saml/metadata/MTI5NTE1NjE2Nzc2X2lucy05ZDg5YTQyMDU3NzI5Nzg0`
   - Attribute mappings configured:
     - Subject → `${user:email}`
     - email → `${user:email}`
     - given_name → `${user:name.givenName}`
     - family_name → `${user:name.familyName}`

3. **Cognito User Pool Configuration**
   - User Pool: `us-west-2_tiuhvmLJZ`
   - Domain: `graniterock-sales-journal.auth.us-west-2.amazoncognito.com`
   - SAML Identity Provider: "GraniteRock-SSO" created
   - Attribute mappings configured with correct SAML claim URIs
   - App client configured with callback URLs

4. **User Authorization**
   - User `ckaiser@graniterock.com` assigned to Sales Journal application
   - Group "Snow Flake SSO" assigned to Sales Journal application
   - User membership in group confirmed

### ❌ Persistent Issues

1. **"Bad input" Error**
   - Error occurs when IAM Identity Center tries to process SAML assertion
   - Appears regardless of SP-initiated or IdP-initiated flow attempts
   - Authentication succeeds (CloudTrail confirms `CredentialChallenge: Success`)
   - Authorization check fails at application level

2. **"No access" Error**
   - Intermittent error despite valid user/group assignments
   - Appears to be session caching issue in IAM Identity Center
   - Persists even after clearing cookies and fresh login

3. **403 Forbidden in Debug Mode**
   - IAM Identity Center's Shift+Click debug feature returns 403
   - Indicates application-level access control issue
   - User has correct assignments but access denied

---

## Root Cause Analysis

### Architectural Incompatibility

IAM Identity Center's **custom SAML applications** are designed for:
- **IdP-initiated SSO** (user starts from AWS access portal)
- **AWS console and AWS applications** as SAML service providers
- **Internal AWS service integrations**

They do **NOT** properly support:
- **SP-initiated SSO** (user starts from external app like Cognito)
- **Third-party service providers** making SAML requests
- **External authentication flows** from non-AWS services

### Technical Evidence

1. **Cognito generates SP-initiated SAML requests** that IAM Identity Center custom apps don't recognize
2. **"Bad input" error** is IAM Identity Center rejecting the SAML AuthnRequest format
3. **AWS documentation** recommends ALB for web apps, not Cognito+SAML for IAM Identity Center
4. **Stack Overflow evidence** shows this pattern consistently fails

### Why IdP-Initiated Flow Also Failed

Even when attempting IdP-initiated flow (user starts from AWS access portal):
- Application access control appears broken
- Assignment propagation issues persist
- No clear error messages to debug authorization logic

---

## Attempted Solutions (All Failed)

### 1. Attribute Mapping Corrections ❌
- Fixed swapped given_name/family_name mappings
- Added username/nameidentifier mapping
- Used full SAML claim URIs
- Result: Still "Bad input" error

### 2. Instance-Level Attribute Configuration ❌
- Created and deleted instance access control attributes
- Tested with and without ABAC configuration
- Result: "Invalid user attributes" errors

### 3. Direct User Assignment ❌
- Added user directly to application (in addition to group)
- Verified assignments via AWS CLI
- Result: "No access" errors persisted

### 4. Session Reset & Cache Clearing ❌
- Signed out completely from IAM Identity Center
- Cleared all browser cookies
- Waited for propagation delays
- Result: Authentication works, authorization still fails

### 5. Multiple Flow Attempts ❌
- **SP-initiated via Cognito Hosted UI**: "Bad input"
- **IdP-initiated via AWS Access Portal**: "No access" / "Bad input"
- **Debug mode (Shift+Click)**: 403 Forbidden
- Result: All paths blocked

---

## Current System State

### Working Components
- ✅ Active Directory integration with IAM Identity Center
- ✅ User authentication (password validation succeeds)
- ✅ User/group assignments in IAM Identity Center
- ✅ Cognito User Pool exists and configured
- ✅ SAML metadata exchange configured
- ✅ Application deployed to Amplify (https://master.dwau7b1q9q1iw.amplifyapp.com)
- ✅ API Gateway + Lambda backend functional
- ✅ DevAuthBypass works for local development

### Non-Working Components
- ❌ SAML SSO flow (all variations)
- ❌ IAM Identity Center custom SAML application access
- ❌ SP-initiated authentication from Cognito
- ❌ IdP-initiated authentication from AWS portal

### Current Workaround
- **Development**: DevAuthBypass allows local testing with any email
- **Production**: SSO non-functional, users cannot authenticate

---

## Configuration Details for Reference

### IAM Identity Center
```
Instance ARN: arn:aws:sso:::instance/ssoins-790755f0cd17e168
Region: us-west-2
Identity Source: Active Directory (graniterock.corp)
Directory ID: d-9267138180

Application: Sales Journal
ARN: arn:aws:sso::129515616776:application/ssoins-790755f0cd17e168/apl-9d89a42057729784
Type: Custom SAML 2.0

SAML Metadata URL:
https://portal.sso.us-west-2.amazonaws.com/saml/metadata/MTI5NTE1NjE2Nzc2X2lucy05ZDg5YTQyMDU3NzI5Nzg0

ACS URL (configured):
https://graniterock-sales-journal.auth.us-west-2.amazoncognito.com/saml2/idpresponse

SAML Audience:
urn:amazon:cognito:sp:us-west-2_tiuhvmLJZ
```

### Cognito User Pool
```
User Pool ID: us-west-2_tiuhvmLJZ
Domain: graniterock-sales-journal.auth.us-west-2.amazoncognito.com
Region: us-west-2

SAML Identity Provider: GraniteRock-SSO
Provider Type: SAML

App Client ID: 7feo9ck7c4icop4flic4be9duk
Callback URLs:
  - https://master.dwau7b1q9q1iw.amplifyapp.com
  - https://localhost:5173

OAuth Flows: Authorization code grant
OAuth Scopes: openid, email, profile, phone

SAML Attribute Mappings:
  username → http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier
  email → http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress
  given_name → http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname
  family_name → http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname
```

### Test User
```
Username: ckaiser@graniterock.com
User ID: 9267138180-3c372556-5d35-489e-8936-1cef3771069c
Name: Cody Kaiser
Email: ckaiser@Graniterock.com (from AD)
Groups: Snow Flake SSO@graniterock.corp

Application Assignments:
  - Direct user assignment ✅
  - Group assignment (Snow Flake SSO) ✅

Authentication Status: ✅ Password validation succeeds
Authorization Status: ❌ Application access denied
```

---

## Recommended Solution: ALB with IAM Identity Center

### Why ALB is Better

1. **Native IAM Identity Center support** - purpose-built integration
2. **SP-initiated flows work correctly** - users can start from app URL
3. **Simpler configuration** - no SAML complexity
4. **AWS-recommended pattern** for web applications
5. **Better security** - authentication before app access
6. **Works with existing AD** - uses same IAM Identity Center instance

### Architecture Comparison

**Current (Not Working):**
```
User → Amplify CloudFront → React App → Cognito Login
                                ↓
                           SAML Request
                                ↓
                    IAM Identity Center (FAILS)
```

**Recommended (ALB):**
```
User → ALB (auth intercept) → IAM Identity Center → AD Authentication
                ↓                                              ↓
         Auth succeeds?                              Password validated
                ↓                                              ↓
        Forward to app with headers ← ← ← ← ← ← ← ← ← ← ← ← ←
                ↓
        React App (S3/EC2/ECS)
                ↓
        API Gateway + Lambda
```

### Benefits of ALB Approach

1. **User experience**: Start directly from app URL (no AWS portal required)
2. **Security**: All requests authenticated at ALB before reaching app
3. **Simplicity**: No Cognito, no SAML complexity
4. **Standard pattern**: Matches AWS recommendations
5. **Maintainability**: Clear separation of concerns
6. **Flexibility**: Easy to add additional auth rules at ALB

---

## Next Steps

See `ALB_MIGRATION_PLAN.md` for detailed implementation guide.

**Immediate actions:**
1. Review and approve ALB architecture approach
2. Decide on hosting model (EC2 vs ECS for React app)
3. Plan deployment window (requires brief downtime)
4. Implement ALB migration following documented plan

**Current workaround:**
- Use DevAuthBypass for development and testing
- Production SSO remains non-functional until ALB migration

---

## Lessons Learned

1. **IAM Identity Center custom SAML apps ≠ general SAML IdP** - They're designed for specific AWS use cases
2. **Cognito + IAM Identity Center SAML = incompatible** - This pattern is not supported/reliable
3. **Always check AWS-recommended patterns first** - Would have saved hours of debugging
4. **ALB authentication is the standard** for web apps with IAM Identity Center
5. **"Bad input" errors are often architectural** - Not just configuration issues

---

## References

- [AWS re:Post - Integrate IAM Identity Center with Cognito](https://repost.aws/knowledge-center/cognito-user-pool-iam-integration)
- [ALB Authentication with OIDC](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/listener-authenticate-users.html)
- [IAM Identity Center Troubleshooting](https://docs.aws.amazon.com/singlesignon/latest/userguide/troubleshooting.html)
- Stack Overflow: Spring Boot SAML using AWS SSO as IdP errors with Bad Input

---

## Contact & Support

For questions about this implementation:
- Review `COGNITO_SAML_SETUP.md` for detailed SAML configuration attempts
- Review `ALB_MIGRATION_PLAN.md` for recommended implementation path
- Check CloudTrail logs for authentication events (filter on username: ckaiser)
- Test user authentication status via AWS CLI:
  ```bash
  aws identitystore describe-user \
    --identity-store-id d-9267138180 \
    --user-id 9267138180-3c372556-5d35-489e-8936-1cef3771069c \
    --region us-west-2
  ```
