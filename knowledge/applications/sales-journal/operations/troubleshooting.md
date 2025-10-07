# Sales Journal - Troubleshooting Guide

**Application**: Sales Journal
**Production**: https://apps.grc-ops.com/sales-journal/

---

## Quick Diagnostics

### Check Application Health

```bash
# 1. Verify ECS service running
aws ecs describe-services \
  --cluster skynet-apps-cluster \
  --service sales-journal \
  --query 'services[0].[serviceName,status,runningCount,desiredCount,deployments[0].status]'

# Expected: ["sales-journal", "ACTIVE", 1, 1, "PRIMARY"]

# 2. Check target group health
aws elbv2 describe-target-health \
  --target-group-arn arn:aws:elasticloadbalancing:us-west-2:129515616776:targetgroup/sales-journal-tg/...

# Expected: TargetHealth.State = "healthy"

# 3. Test production URL
curl -I https://apps.grc-ops.com/sales-journal/

# Expected: HTTP/2 200 (after redirect to auth)
```

### Check Backend API Health

```bash
# Verify Lambda function
aws lambda get-function-configuration \
  --function-name sales-journal-api \
  --query '[FunctionName,State,LastUpdateStatus,Runtime,MemorySize]'

# Expected: ["sales-journal-api", "Active", "Successful", "python3.12", 1024]

# Check recent errors
aws logs tail /aws/lambda/sales-journal-api --since 30m
```

---

## Common Issues

### Issue 1: Application Returns 404 Not Found

**Symptoms**:
- Browser shows 404 error
- ALB health checks failing
- ECS task running but unhealthy

**Diagnosis**:
```bash
# Check nginx configuration
aws ecs describe-task-definition \
  --task-definition sales-journal:1 \
  --query 'taskDefinition.containerDefinitions[0].environment'

# Verify BASE_PATH=/sales-journal

# Check container logs
aws logs tail /ecs/sales-journal --since 15m
```

**Common Causes**:
1. nginx configuration missing `/sales-journal/` location block
2. BASE_PATH environment variable not set
3. React build has wrong `base` path in vite.config.ts

**Solutions**:
```bash
# Rebuild with correct configuration
cd react-sales-journal
# Fix nginx.conf or vite.config.ts
docker build -t sales-journal:latest .
# Redeploy (see deployment runbook)
```

---

### Issue 2: API Calls Return 401 Unauthorized

**Symptoms**:
- Application loads but dashboard shows "Authentication Required"
- Console errors: `GET /api/auth/user 401`
- API calls fail with 401 status

**Diagnosis**:
```bash
# Check ALB rule has authenticate-oidc action
aws elbv2 describe-rules \
  --listener-arn arn:aws:elasticloadbalancing:us-west-2:129515616776:listener/app/Skynet-ELB/.../... \
  --query 'Rules[?Priority==`5`]'

# Verify Action Order 1 is "authenticate-oidc"

# Check Lambda logs for header issues
aws logs tail /aws/lambda/sales-journal-api --since 5m --filter-pattern "x-amzn-oidc"
```

**Common Causes**:
1. ALB rule priority 5 missing `authenticate-oidc` action
2. ALB rule has `forward` only (no OIDC)
3. Lambda CORS configuration blocks requests

**Solution**:
```bash
# Add authenticate-oidc action to ALB rule
aws elbv2 modify-rule \
  --rule-arn arn:aws:elasticloadbalancing:us-west-2:129515616776:listener-rule/... \
  --actions \
    Type=authenticate-oidc,Order=1,AuthenticateOidcConfig={...} \
    Type=forward,Order=2,TargetGroupArn=<lambda-tg-arn>
```

---

### Issue 3: Logout Doesn't Clear Session

**Symptoms**:
- User clicks logout
- Redirects but stays authenticated
- Browser shows logged-in user after logout

**Diagnosis**:
This should NOT occur - logout is implemented correctly with backend-assisted cookie clearing.

If occurring:
```bash
# Check Lambda /api/logout implementation
aws lambda get-function --function-name sales-journal-api

# Verify redirect URL in code
# Should redirect to: https://login.microsoftonline.com/{tenant}/oauth2/v2.0/logout
```

**Root Cause**:
HTTP-only cookies can only be cleared by backend setting expired cookies

**Solution**: Already implemented in production (no action needed)

---

### Issue 4: Pipeline Trigger Fails

**Symptoms**:
- User clicks Refresh/Finalize button
- Error message appears
- Pipeline doesn't start

**Diagnosis**:
```bash
# Check Lambda logs for Orchestra API errors
aws logs tail /aws/lambda/sales-journal-api --since 5m --filter-pattern "ERROR"

# Common errors:
# - "Orchestra API authentication failed" → Token expired
# - "Pipeline ID not found" → Wrong pipeline ID
# - "Rate limit exceeded" → Too many triggers
```

**Solutions**:

**Orchestra API Token Expired**:
```bash
# Update token in Secrets Manager
aws secretsmanager update-secret \
  --secret-id sales-journal-db-credentials \
  --secret-string '{"orchestra_api_token":"new-token-here",...}'

# Force Lambda to reload
aws lambda update-function-configuration \
  --function-name sales-journal-api \
  --environment Variables={USE_SECRETS_MANAGER=true,...}
```

**Wrong Pipeline ID**:
- Verify IDs in Lambda code match Orchestra dashboard
- Refresh: `c468dd21-7af0-4892-9f48-d8cdf24d9b7d`
- Final: `daa39221-b30f-4b27-a8ee-a1b98ca28d0f`

---

### Issue 5: Dashboard Shows Stale Data

**Symptoms**:
- User reports old data
- Pipeline ran but dashboard not updated
- Refresh button doesn't help

**Diagnosis**:
```bash
# Check cache TTL settings
aws lambda get-function-configuration \
  --function-name sales-journal-api \
  --query 'Environment.Variables'

# Verify CACHE_TTL_* variables set correctly
```

**Solution**:
- Cache TTLs are set to 5-10 minutes (intentional)
- If data is truly stale (> 10 min old), check PostgreSQL replication
- Verify DMS replication task is running

**Check DMS Status**:
```bash
# User can check DMS status in dashboard
# Should show "CHANGE PROCESSING" when all tasks ready
# If shows "WAITING" or "ERROR", investigate DMS tasks
```

---

### Issue 6: Slow API Responses

**Symptoms**:
- Dashboard takes > 5 seconds to load
- API calls timeout
- User reports sluggish performance

**Diagnosis**:
```bash
# Check Lambda execution time
aws logs tail /aws/lambda/sales-journal-api --since 15m --filter-pattern "Duration:"

# Check for database connection issues
aws logs tail /aws/lambda/sales-journal-api --since 15m --filter-pattern "OperationalError"
```

**Common Causes**:
1. Database query slow (missing index)
2. Lambda cold start (first invocation)
3. PostgreSQL connection timeout
4. Large result sets (pagination needed)

**Solutions**:

**Slow Queries**:
- Investigate specific query performance in PostgreSQL
- Check for missing indexes on filter columns
- Consider query optimization or result set limits

**Cold Starts**:
- Acceptable for internal tool (1-2 seconds)
- For critical paths: Consider provisioned concurrency

**Connection Timeouts**:
```bash
# Check Lambda VPC configuration
aws lambda get-function-configuration \
  --function-name sales-journal-api \
  --query 'VpcConfig'

# Verify security groups allow PostgreSQL (5432)
```

---

### Issue 7: ALB Rule Priority Conflict

**Symptoms**:
- Requests go to wrong application
- `/sales-journal/` loads app-portal instead
- API calls route incorrectly

**Diagnosis**:
```bash
# List ALB rules by priority
aws elbv2 describe-rules \
  --listener-arn arn:aws:elasticloadbalancing:us-west-2:129515616776:listener/app/Skynet-ELB/.../... \
  --query 'Rules | sort_by(@, &Priority)[*].[Priority,Conditions[0].Values[0]]'

# Expected order:
# 5: /sales-journal/api/*
# 6: /sales-journal/*
# 7: /* (catch-all app-portal)
```

**Common Cause**: Priority numbers wrong (lower = higher priority!)

**Solution**:
```bash
# Swap priorities if needed
aws elbv2 set-rule-priorities \
  --rule-priorities \
    RuleArn=<sales-journal-api-rule>,Priority=5 \
    RuleArn=<sales-journal-app-rule>,Priority=6 \
    RuleArn=<app-portal-rule>,Priority=7
```

---

### Issue 8: New Docker Image Not Deploying

**Symptoms**:
- Docker push successful
- ECS service updated
- Old code still running

**Diagnosis**:
```bash
# Check task definition image reference
aws ecs describe-task-definition \
  --task-definition sales-journal:1 \
  --query 'taskDefinition.containerDefinitions[0].image'

# Should show: ...sales-journal:latest (not pinned digest)

# Verify latest image pushed
aws ecr describe-images \
  --repository-name sales-journal \
  --query 'sort_by(imageDetails,&imagePushedAt)[-1].[imageTags[0],imagePushedAt]'
```

**Common Cause**: Task definition uses pinned digest instead of `:latest` tag

**Solution**:
- Current configuration uses `:latest` tag (correct)
- force-new-deployment pulls latest automatically
- If issue persists: Register new task definition manually

---

## Monitoring Queries

### Check Recent Deployments

```bash
# List recent task definition revisions
aws ecs list-task-definitions \
  --family-prefix sales-journal \
  --sort DESC \
  --max-items 5

# Check deployment history
aws ecs describe-services \
  --cluster skynet-apps-cluster \
  --service sales-journal \
  --query 'services[0].deployments'
```

### Monitor Error Rates

```bash
# ECS application errors
aws logs tail /ecs/sales-journal --since 1h --filter-pattern "ERROR"

# Lambda errors
aws logs tail /aws/lambda/sales-journal-api --since 1h --filter-pattern "ERROR"

# Count errors in last hour
aws logs filter-log-events \
  --log-group-name /aws/lambda/sales-journal-api \
  --start-time $(date -u -v-1H +%s)000 \
  --filter-pattern "ERROR" \
  | grep -c "message"
```

### Database Connection Health

```bash
# Check Lambda logs for connection issues
aws logs tail /aws/lambda/sales-journal-api --since 30m --filter-pattern "psycopg2"

# Look for:
# - "connection timeout"
# - "could not connect"
# - "authentication failed"
```

---

## Emergency Contacts

**Team**: Data & Analytics
**Slack**: #da-team channel
**On-Call**: DevOps team (for infrastructure issues)
**Escalation**: Data Architect (for data/integration issues)

---

## Incident Response Checklist

**Initial Response** (< 5 minutes):
- [ ] Verify issue (check production URL)
- [ ] Check ECS service status
- [ ] Check Lambda function status
- [ ] Review CloudWatch logs (last 15 min)
- [ ] Notify team in Slack

**Investigation** (< 15 minutes):
- [ ] Identify affected component (ECS, Lambda, ALB, Database)
- [ ] Check recent deployments (was this introduced?)
- [ ] Review error logs in detail
- [ ] Test specific functionality

**Resolution** (< 30 minutes):
- [ ] Apply fix OR rollback to previous version
- [ ] Verify fix resolves issue
- [ ] Monitor for 15 minutes post-fix
- [ ] Document root cause and resolution

**Post-Incident** (< 24 hours):
- [ ] Create incident report
- [ ] Update troubleshooting guide (this doc)
- [ ] Identify preventive measures
- [ ] Update monitoring/alerting if needed

---

**Last Updated**: 2025-10-07
**Validated**: Production incidents and resolutions from 2025-10-04 through 2025-10-06 deployment
