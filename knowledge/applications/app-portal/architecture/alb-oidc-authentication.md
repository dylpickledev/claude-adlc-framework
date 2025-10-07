# ALB OIDC Authentication Pattern

**Application**: App Portal (https://apps.grc-ops.com)
**Authentication Provider**: Azure AD
**Implementation**: ALB-level OIDC authentication

## Overview

This pattern implements authentication at the AWS Application Load Balancer (ALB) layer using OIDC integration with Azure AD, eliminating the need for application-level authentication libraries like AWS Amplify or Cognito.

## Architecture

```
User Browser
    ↓
ALB (HTTPS:443)
    ↓ (1) Authenticate-OIDC Action
    ↓ (2) Forward Action
    ↓
ECS Fargate (app-portal)
    ↓
nginx (port 80) - Serves React SPA
Python API (port 8080) - Reads ALB OIDC headers
```

## Key Benefits

1. **Infrastructure-Level Authentication**: No client-side auth libraries required
2. **Simplified Application Code**: React app has zero auth logic
3. **Consistent Across Apps**: All apps on ALB use same auth pattern
4. **Centralized Management**: Auth configuration managed at infrastructure layer
5. **Security**: Credentials never reach application code

## Implementation Details

### ALB Rule Configuration

```json
{
  "Priority": 7,
  "Conditions": [
    {
      "Field": "host-header",
      "Values": ["apps.grc-ops.com"]
    }
  ],
  "Actions": [
    {
      "Type": "authenticate-oidc",
      "Order": 1,
      "AuthenticateOidcConfig": {
        "Issuer": "https://login.microsoftonline.com/{tenant_id}/v2.0",
        "AuthorizationEndpoint": "https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize",
        "TokenEndpoint": "https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token",
        "UserInfoEndpoint": "https://graph.microsoft.com/oidc/userinfo",
        "ClientId": "{client_id}",
        "ClientSecret": "{client_secret}",
        "SessionCookieName": "AWSELBAuthSessionCookie",
        "Scope": "openid profile email",
        "OnUnauthenticatedRequest": "authenticate"
      }
    },
    {
      "Type": "forward",
      "Order": 2,
      "TargetGroupArn": "arn:aws:elasticloadbalancing:...:targetgroup/app-portal-tg/..."
    }
  ]
}
```

### Backend API: Reading User Info

**File**: `api/main.py`

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import base64
import json

app = FastAPI()

@app.get("/api/auth/user")
async def get_user(request: Request):
    """
    Extract user information from ALB OIDC headers.

    ALB injects these headers after successful OIDC authentication:
    - x-amzn-oidc-data: JWT containing user claims (base64url encoded)
    - x-amzn-oidc-identity: User's unique identifier
    """
    # Get OIDC data header (JWT)
    oidc_data = request.headers.get("x-amzn-oidc-data")

    if not oidc_data:
        return JSONResponse(
            status_code=401,
            content={"error": "No OIDC data found"}
        )

    try:
        # Decode JWT payload (ALB already verified signature)
        # JWT format: header.payload.signature
        parts = oidc_data.split('.')

        if len(parts) != 3:
            raise ValueError("Invalid JWT format")

        # Decode base64url payload
        payload = parts[1]
        # Add padding if needed
        padding = 4 - (len(payload) % 4)
        if padding != 4:
            payload += '=' * padding

        decoded = base64.urlsafe_b64decode(payload)
        claims = json.loads(decoded)

        # Extract user information from claims
        return {
            "name": claims.get("name", "Unknown User"),
            "email": claims.get("email", ""),
            "sub": claims.get("sub", ""),  # Unique user identifier
            "authenticated": True
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to decode user info: {str(e)}"}
        )
```

### Frontend: Using User Info

**File**: `src/hooks/useAuth.ts`

```typescript
import { useState, useEffect } from 'react';

interface User {
  name: string;
  email: string;
  sub: string;
  authenticated: boolean;
}

export const useAuth = () => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await fetch('/api/auth/user');

        if (!response.ok) {
          throw new Error('Authentication required');
        }

        const userData = await response.json();
        setUser(userData);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, []);

  return { user, loading, error };
};
```

## The HTTP-Only Cookie Problem

### Challenge

ALB sets authentication cookies as **HTTP-only**, which means:
- JavaScript cannot access or modify them
- Standard logout (clearing cookies client-side) doesn't work
- `/oauth2/sign_out` endpoint redirects but doesn't clear ALB session

### Solution: Backend-Assisted Logout

**File**: `api/main.py`

```python
from fastapi import Response
from fastapi.responses import RedirectResponse
import os

@app.get("/api/logout")
async def logout():
    """
    Clear ALB session cookies and redirect to Azure AD logout.

    This is the ONLY way to properly log out with ALB OIDC authentication.
    """
    tenant_id = os.getenv("AZURE_TENANT_ID")
    post_logout_uri = "https://apps.grc-ops.com"

    # Create redirect to Azure AD logout endpoint
    azure_logout_url = (
        f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/logout"
        f"?post_logout_redirect_uri={post_logout_uri}"
    )

    response = RedirectResponse(
        url=azure_logout_url,
        status_code=302
    )

    # Set expired cookies with same names as ALB cookies
    # This is the KEY to clearing ALB session
    for i in range(4):  # ALB creates up to 4 cookie fragments
        response.set_cookie(
            key=f"AWSELBAuthSessionCookie-{i}",
            value="",
            max_age=0,
            expires="Thu, 01 Jan 1970 00:00:00 GMT",
            path="/",
            secure=True,
            httponly=True,
            samesite="none"
        )

    return response
```

### Frontend Logout Handler

**File**: `src/App.tsx`

```typescript
const handleLogout = () => {
  // Simply redirect to backend logout endpoint
  // Backend will handle cookie clearing + Azure AD logout
  window.location.href = '/api/logout';
};
```

## Multi-Stage Docker Build

Pattern: Single container running nginx + Python API via supervisor

**File**: `Dockerfile`

```dockerfile
# Stage 1: Build React app
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Production image with nginx + Python
FROM python:3.11-slim

# Install nginx and supervisor
RUN apt-get update && apt-get install -y \
    nginx \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Copy Python API
WORKDIR /app
COPY api/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY api/ ./

# Copy React build to nginx
COPY --from=build /app/dist /usr/share/nginx/html/

# Configure nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Configure supervisor to run both services
RUN echo '[supervisord]' > /etc/supervisor/conf.d/supervisord.conf && \
    echo 'nodaemon=true' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo '' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo '[program:nginx]' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'command=nginx -g "daemon off;"' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'autostart=true' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'autorestart=true' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo '' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo '[program:api]' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'command=uvicorn main:app --host 0.0.0.0 --port 8080' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'directory=/app' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'autostart=true' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'autorestart=true' >> /etc/supervisor/conf.d/supervisord.conf

EXPOSE 80

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
```

**File**: `nginx.conf`

```nginx
server {
    listen 80;
    server_name _;

    # Serve React SPA
    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }

    # Proxy API requests to Python backend
    location /api/ {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Common Pitfalls & Solutions

### Pitfall 1: Missing authenticate-oidc Action
**Symptom**: Application receives no OIDC headers, authentication fails
**Cause**: ALB rule only has `forward` action, no `authenticate-oidc` action
**Solution**: Ensure `authenticate-oidc` is action Order 1, `forward` is Order 2

### Pitfall 2: Logout Doesn't Work
**Symptom**: User clicks logout but stays authenticated
**Cause**: HTTP-only cookies can't be cleared client-side
**Solution**: Use backend endpoint to set expired cookies + redirect to IdP logout

### Pitfall 3: API Gets No Auth Headers
**Symptom**: Lambda/ECS receives requests but `x-amzn-oidc-data` header is missing
**Cause**: ALB rule for API path doesn't have `authenticate-oidc` action
**Solution**: Add OIDC authentication to ALL ALB rules that need user identity

### Pitfall 4: Wrong Rule Priority
**Symptom**: Requests go to wrong target group
**Cause**: Catch-all rule executes before specific path rule
**Solution**: Ensure specific paths have LOWER priority numbers than catch-alls

## Testing Checklist

- [ ] User can authenticate with Azure AD
- [ ] Application receives correct user info from ALB headers
- [ ] Backend can decode JWT and extract claims
- [ ] User information displays correctly in UI
- [ ] Logout clears ALB session cookies
- [ ] Logout redirects to Azure AD logout
- [ ] Azure AD redirects back to application
- [ ] Re-authentication required after logout
- [ ] All API endpoints receive OIDC headers
- [ ] HTTP-only cookies set correctly

## Security Considerations

1. **JWT Verification**: ALB verifies JWT signatures automatically - don't verify again in application
2. **HTTPS Only**: All auth cookies require HTTPS (`secure=True`)
3. **Client Secret**: Store in AWS Secrets Manager, never in code
4. **Tenant ID**: Environment-specific, confirm correct Azure AD tenant
5. **Scope**: Request minimal scopes needed (`openid profile email`)

## References

- **AWS Documentation**: ALB Authentication (authenticate-oidc)
- **Azure AD**: OIDC Authentication Flow
- **Project Documentation**: `projects/active/feature-salesjournaltoreact/RESUME_POINT_2025-10-06_APP_PORTAL_COMPLETE.md`

## Lessons Learned

1. **HTTP-only cookies require backend logout** - Can't be cleared from JavaScript
2. **ALB rule actions have order** - authenticate-oidc must be before forward
3. **Every API path needs auth action** - Lambda receives no headers without it
4. **Supervisor simplifies deployment** - Single container > multiple containers for simple cases
5. **Priority numbers are critical** - Lower = higher priority (counterintuitive)

---

**Last Updated**: 2025-10-07
**Deployed**: App Portal (production) + Sales Journal (production)
**Status**: ✅ Validated in production with real users
