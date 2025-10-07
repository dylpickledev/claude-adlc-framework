# App Launcher Portal

**Purpose:** Landing page for apps.grc-ops.com showing all available GraniteRock applications

## Files

- `index.html` - Static landing page with app tiles
- `nginx.conf` - nginx configuration with ALB auth header injection
- `Dockerfile` - Container image definition
- `README.md` - This file

## Local Testing

```bash
# Build Docker image
docker build -t app-launcher:latest .

# Run locally
docker run -p 8080:80 app-launcher:latest

# Test in browser
open http://localhost:8080
```

## Deployment

```bash
# Tag for ECR
docker tag app-launcher:latest 129515616776.dkr.ecr.us-west-2.amazonaws.com/app-launcher:latest

# Login to ECR
aws ecr get-login-password --region us-west-2 | \
  docker login --username AWS --password-stdin 129515616776.dkr.ecr.us-west-2.amazonaws.com

# Push to ECR
docker push 129515616776.dkr.ecr.us-west-2.amazonaws.com/app-launcher:latest
```

## Features

- ✅ Responsive design (mobile-friendly)
- ✅ ALB auth header injection for personalization
- ✅ Displays user's name from OIDC token
- ✅ 6 app cards (1 active: Sales Journal, 5 coming soon)
- ✅ Fade-in animations on load
- ✅ GraniteRock branding (green gradient)
- ✅ Health check endpoint for ALB
- ✅ Gzip compression
- ✅ Security headers

## Adding New Apps

When deploying a new app:

1. **Edit `index.html`:**
   - Find the "coming soon" card for the app
   - Change `<div class="app-card disabled">` to `<a href="/app-name/" class="app-card">`
   - Remove `disabled` class
   - Remove `<span class="coming-soon-badge">Coming Soon</span>`
   - Update href to match ALB routing path

2. **Rebuild and redeploy:**
   ```bash
   docker build -t app-launcher:latest .
   docker push 129515616776.dkr.ecr.us-west-2.amazonaws.com/app-launcher:latest

   # Force ECS service to use new image
   aws ecs update-service \
     --cluster skynet-apps-cluster \
     --service app-launcher \
     --force-new-deployment \
     --region us-west-2
   ```

## Customization

### Changing Colors
Edit `index.html` styles:
- Background gradient: `background: linear-gradient(135deg, #0f4c38 0%, #2d8a5f 100%);`
- Card colors: `background: rgba(255, 255, 255, 0.1);`

### Changing Icons
Replace emoji icons in app cards:
- 📊 Sales Journal
- 📈 Analytics
- 🔧 Operations
- 📱 Mobile
- 🎯 Projects
- 💼 Resources

### Adding User Groups
To show different apps to different users, upgrade to dynamic React launcher (see APP_LAUNCHER_IMPLEMENTATION_PLAN.md Option B)

## Cost

- Fargate (0.25 vCPU, 0.5GB): **~$9/month**
- CloudWatch logs: **~$1/month**
- **Total: ~$10/month**

## Monitoring

- **Health checks:** `/health` endpoint
- **CloudWatch Logs:** `/ecs/app-launcher` log group
- **Metrics:** ALB target group health, request count

## Troubleshooting

### Landing page shows but no user name
- Check ALB OIDC authentication is configured
- Verify nginx is injecting x-amzn-oidc-data header as meta tag
- Check browser console for JavaScript errors

### Health checks failing
- Verify container is running: `docker logs <container-id>`
- Test health endpoint: `curl http://localhost/health`
- Check nginx error logs

### Stale content after update
- Force browser refresh: Cmd+Shift+R (Mac) or Ctrl+F5 (Windows)
- Verify new Docker image pushed to ECR
- Force ECS service deployment with `--force-new-deployment`
