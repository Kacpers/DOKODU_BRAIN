# Stage 1: Build frontend
FROM node:20-alpine AS frontend-build
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# Stage 2: Runtime
FROM python:3.11-slim
WORKDIR /app

# Install nginx
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend
COPY backend/ ./backend/

# Copy frontend static build
COPY --from=frontend-build /app/frontend/out ./frontend-static/

# Copy nginx config
COPY nginx.conf /etc/nginx/sites-enabled/default

# Cleanup script
RUN echo '#!/bin/sh\nfind /tmp/tender -mindepth 1 -maxdepth 1 -mmin +60 -exec rm -rf {} +' > /usr/local/bin/cleanup.sh && chmod +x /usr/local/bin/cleanup.sh

EXPOSE 80

CMD sh -c "mkdir -p /tmp/tender && \
    (while true; do /usr/local/bin/cleanup.sh; sleep 300; done &) && \
    uvicorn backend.main:app --host 0.0.0.0 --port 8000 & \
    nginx -g 'daemon off;'"
