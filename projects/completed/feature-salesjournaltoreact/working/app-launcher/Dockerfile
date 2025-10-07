# App Launcher Portal - Dockerfile
# Lightweight static HTML server with nginx

FROM nginx:alpine

# Copy landing page HTML
COPY index.html /usr/share/nginx/html/

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Remove default nginx configs
RUN rm -f /etc/nginx/conf.d/default.conf.bak 2>/dev/null || true

# Expose port 80
EXPOSE 80

# Health check for ECS/ALB
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost/health || exit 1

# Start nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
