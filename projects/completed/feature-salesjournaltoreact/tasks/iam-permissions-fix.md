# AWS IAM Permissions Fix for Amplify Deployment

## Problem
CDK deployment fails with SSM GetParameter permission error:
```
AccessDeniedException: User is not authorized to perform: ssm:GetParameter
on resource: arn:aws:ssm:us-west-2:395333095307:parameter/cdk-bootstrap/hnb659fds/version
```

## Root Cause
Amplify CodeBuild IAM role lacks SSM read permissions required by CDK to check bootstrap stack version.

## Affected IAM Role
**Role Name**: `AemiliaControlPlaneLambda-CodeBuildRole-11HNYF0P8C56M`
**Account**: 395333095307
**Region**: us-west-2

## Solution Steps

### 1. Navigate to IAM Console
- Go to AWS Console → IAM → Roles
- Search for: `AemiliaControlPlaneLambda-CodeBuildRole-11HNYF0P8C56M`

### 2. Add Inline Policy
Click **Add permissions** → **Create inline policy**

**Policy JSON**:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "CDKBootstrapSSMAccess",
      "Effect": "Allow",
      "Action": "ssm:GetParameter",
      "Resource": "arn:aws:ssm:*:*:parameter/cdk-bootstrap/*"
    }
  ]
}
```

**Policy Name**: `CDKBootstrapSSMReadAccess`

### 3. Verify Policy
After adding, verify the role has:
- Existing CodeBuild permissions
- **NEW**: SSM GetParameter for CDK bootstrap parameters

### 4. Trigger New Build
Once IAM policy is applied:
1. Go to Amplify Console
2. Select the app
3. Click **Redeploy this version**
4. Monitor build logs for successful deployment

## Expected Result After Fix
```
✅ Backend synthesized in X.XX seconds
✅ Type checks completed in X.XX seconds
✅ Building and publishing assets...
✅ Deploying stack...
✅ API Gateway endpoint: https://xxxxx.execute-api.us-west-2.amazonaws.com
```

## Alternative: Managed Policy Approach
If inline policy is not preferred, attach AWS managed policy:
- **Policy**: `AmazonSSMReadOnlyAccess` (broader permissions)
- **Pros**: AWS-managed, automatically updated
- **Cons**: Broader than needed (grants read to all SSM parameters)

**Recommended**: Use inline policy (more specific, principle of least privilege)

## Verification Commands
After deployment, verify Lambda and API Gateway:
```bash
# List Lambda functions
aws lambda list-functions --region us-west-2 | grep sales-journal

# Get API Gateway URL
aws apigatewayv2 get-apis --region us-west-2 | grep sales-journal
```

## Related Files
- **Backend Config**: `/Users/TehFiestyGoat/da-agent-hub/react-sales-journal/amplify/backend.ts`
- **Build Config**: `/Users/TehFiestyGoat/da-agent-hub/react-sales-journal/amplify.yml`
- **Project Context**: `projects/active/feature-salesjournaltoreact/context.md`

## Status
- **Created**: 2025-10-03
- **Status**: Awaiting IAM policy update
- **Next Action**: Apply IAM policy and trigger build
