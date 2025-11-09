# Deployment Guide - Stride Events Platform

Complete guide for deploying the Stride Events Platform to production.

---

## Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Environment Setup](#environment-setup)
3. [Docker Deployment](#docker-deployment)
4. [Manual Deployment](#manual-deployment)
5. [Database Setup](#database-setup)
6. [Monitoring & Logging](#monitoring--logging)
7. [Backup & Recovery](#backup--recovery)
8. [Troubleshooting](#troubleshooting)

---

## Pre-Deployment Checklist

### Security
- [ ] Generate strong `SECRET_KEY` (32+ characters)
- [ ] Set up SSL certificates (Let's Encrypt recommended)
- [ ] Configure firewall rules
- [ ] Enable database SSL connections
- [ ] Set up VPN/bastion for database access
- [ ] Review and restrict CORS origins
- [ ] Enable rate limiting on API endpoints
- [ ] Set up WAF (Web Application Firewall)

### Infrastructure
- [ ] Provision production servers (min 4GB RAM, 2 vCPUs)
- [ ] Set up PostgreSQL 16 database
- [ ] Configure load balancer (if needed)
- [ ] Set up CDN for static assets
- [ ] Configure DNS records
- [ ] Set up monitoring (DataDog, New Relic, or Prometheus)
- [ ] Configure log aggregation (ELK, Splunk, or CloudWatch)

### API Credentials
- [ ] Obtain Stride ID API credentials
- [ ] Obtain SendGrid API key and verify sender
- [ ] Obtain Assessment Manager API credentials
- [ ] Test all API integrations in staging

### Code
- [ ] Run all tests (`pytest` backend, `pnpm test` frontend)
- [ ] Code review completed
- [ ] Security audit completed
- [ ] Performance testing completed
- [ ] Documentation updated

---

## Environment Setup

### Production Environment Variables

Create `/opt/stride-events/.env.production`:

```env
# Application
ENVIRONMENT=production
API_V1_PREFIX=/api/v1

# Database
DATABASE_URL=postgresql+asyncpg://stride_user:STRONG_PASSWORD@db.internal:5432/stride_events_prod?ssl=require

# JWT (Generate with: openssl rand -hex 32)
SECRET_KEY=your-production-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Stride ID API
STRIDE_ID_API_URL=https://stride-id-api.strideahead.in
STRIDE_ID_API_KEY=prod_key_here

# SendGrid
SENDGRID_API_KEY=SG.production_key_here
FROM_EMAIL=noreply@strideahead.in

# CORS
BACKEND_CORS_ORIGINS=["https://events.strideahead.in","https://www.strideahead.in"]

# Monitoring
SENTRY_DSN=https://your-sentry-dsn
LOG_LEVEL=INFO
```

### Frontend Environment

Create `frontend/.env.production`:

```env
VITE_API_URL=https://api.events.strideahead.in
```

---

## Docker Deployment

### Production Docker Compose

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    restart: always
    env_file:
      - .env.production
    ports:
      - "8000:8000"
    depends_on:
      - postgres
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.prod
      args:
        VITE_API_URL: https://api.events.strideahead.in
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/ssl:/etc/nginx/ssl:ro
      - ./nginx/conf.d:/etc/nginx/conf.d:ro
    depends_on:
      - backend
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  postgres:
    image: postgres:16
    restart: always
    environment:
      POSTGRES_DB: stride_events_prod
      POSTGRES_USER: stride_user
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups
    ports:
      - "127.0.0.1:5432:5432"
    command: 
      - "postgres"
      - "-c"
      - "max_connections=200"
      - "-c"
      - "shared_buffers=256MB"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U stride_user"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
    driver: local
```

### Deployment Steps

```bash
# 1. Clone repository on production server
git clone <repository-url> /opt/stride-events
cd /opt/stride-events

# 2. Create production environment file
cp .env.example .env.production
nano .env.production  # Edit with production values

# 3. Build images
docker-compose -f docker-compose.prod.yml build

# 4. Start services
docker-compose -f docker-compose.prod.yml up -d

# 5. Run database migrations
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head

# 6. Verify deployment
docker-compose -f docker-compose.prod.yml ps
curl https://api.events.strideahead.in/health
```

---

## Manual Deployment

### Backend Deployment (Systemd)

1. **Install Python and dependencies**

```bash
sudo apt update
sudo apt install python3.11 python3.11-venv postgresql-client

cd /opt/stride-events/backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Create systemd service**

Create `/etc/systemd/system/stride-events-api.service`:

```ini
[Unit]
Description=Stride Events API
After=network.target postgresql.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/opt/stride-events/backend
Environment="PATH=/opt/stride-events/backend/venv/bin"
EnvironmentFile=/opt/stride-events/.env.production
ExecStart=/opt/stride-events/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

3. **Start service**

```bash
sudo systemctl daemon-reload
sudo systemctl enable stride-events-api
sudo systemctl start stride-events-api
sudo systemctl status stride-events-api
```

### Frontend Deployment (Nginx)

1. **Build frontend**

```bash
cd /opt/stride-events/frontend
pnpm install
pnpm build
```

2. **Configure Nginx**

Create `/etc/nginx/sites-available/stride-events`:

```nginx
# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name events.strideahead.in;
    return 301 https://$server_name$request_uri;
}

# HTTPS server
server {
    listen 443 ssl http2;
    server_name events.strideahead.in;

    # SSL configuration
    ssl_certificate /etc/letsencrypt/live/events.strideahead.in/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/events.strideahead.in/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Frontend
    root /opt/stride-events/frontend/dist;
    index index.html;

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;

    # Frontend routes
    location / {
        try_files $uri $uri/ /index.html;
    }

    # API proxy
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
```

3. **Enable site**

```bash
sudo ln -s /etc/nginx/sites-available/stride-events /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## Database Setup

### PostgreSQL Configuration

1. **Create database and user**

```sql
-- Connect as postgres user
sudo -u postgres psql

-- Create database
CREATE DATABASE stride_events_prod;

-- Create user
CREATE USER stride_user WITH ENCRYPTED PASSWORD 'STRONG_PASSWORD';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE stride_events_prod TO stride_user;

-- Enable UUID extension
\c stride_events_prod
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

2. **Configure PostgreSQL for production**

Edit `/etc/postgresql/16/main/postgresql.conf`:

```conf
max_connections = 200
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
work_mem = 1310kB
min_wal_size = 1GB
max_wal_size = 4GB
```

3. **Enable SSL**

```bash
# Generate SSL certificates
sudo -u postgres openssl req -new -x509 -days 365 -nodes -text \
  -out /var/lib/postgresql/16/main/server.crt \
  -keyout /var/lib/postgresql/16/main/server.key

# Set permissions
sudo chmod 600 /var/lib/postgresql/16/main/server.key
sudo chown postgres:postgres /var/lib/postgresql/16/main/server.*

# Enable in postgresql.conf
ssl = on
ssl_cert_file = 'server.crt'
ssl_key_file = 'server.key'
```

4. **Run migrations**

```bash
cd /opt/stride-events/backend
source venv/bin/activate
alembic upgrade head
```

---

## Monitoring & Logging

### Application Monitoring

1. **Install Sentry (Error Tracking)**

```bash
pip install sentry-sdk[fastapi]
```

Add to `backend/app/main.py`:

```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    integrations=[FastApiIntegration()],
    environment=settings.ENVIRONMENT,
    traces_sample_rate=0.1,
)
```

2. **Configure Structured Logging**

Create `backend/app/core/logging.py`:

```python
import logging
import sys
from loguru import logger

# Remove default handler
logger.remove()

# Add custom handler
logger.add(
    sys.stdout,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO",
)

# Add file handler
logger.add(
    "/var/log/stride-events/app.log",
    rotation="500 MB",
    retention="10 days",
    level="INFO",
)
```

### Infrastructure Monitoring

1. **Prometheus + Grafana**

```yaml
# docker-compose.monitoring.yml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin

volumes:
  prometheus_data:
  grafana_data:
```

2. **Health Check Endpoints**

Already implemented in `backend/app/main.py`:
- `/health` - Basic health check
- `/api/v1/docs` - API documentation

---

## Backup & Recovery

### Database Backups

1. **Automated backup script**

Create `/opt/stride-events/scripts/backup-db.sh`:

```bash
#!/bin/bash

BACKUP_DIR="/backups/postgres"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/stride_events_$TIMESTAMP.sql.gz"

# Create backup
pg_dump -h localhost -U stride_user stride_events_prod | gzip > $BACKUP_FILE

# Keep only last 7 days
find $BACKUP_DIR -name "stride_events_*.sql.gz" -mtime +7 -delete

# Upload to S3 (optional)
# aws s3 cp $BACKUP_FILE s3://stride-backups/database/
```

2. **Schedule with cron**

```bash
# Add to crontab
0 2 * * * /opt/stride-events/scripts/backup-db.sh
```

### Restore from Backup

```bash
# Restore database
gunzip < /backups/postgres/stride_events_20250109_020000.sql.gz | \
  psql -h localhost -U stride_user stride_events_prod
```

---

## Troubleshooting

### Common Issues

#### 1. Database Connection Errors

```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check connection
psql -h localhost -U stride_user -d stride_events_prod

# View logs
sudo tail -f /var/log/postgresql/postgresql-16-main.log
```

#### 2. API Not Responding

```bash
# Check service status
sudo systemctl status stride-events-api

# View logs
sudo journalctl -u stride-events-api -f

# Check port
sudo netstat -tulpn | grep 8000
```

#### 3. Frontend Not Loading

```bash
# Check Nginx status
sudo systemctl status nginx

# Test configuration
sudo nginx -t

# View error logs
sudo tail -f /var/log/nginx/error.log
```

#### 4. High Memory Usage

```bash
# Check memory
free -h

# Check processes
top

# Restart services
sudo systemctl restart stride-events-api
```

### Performance Optimization

1. **Database Indexing**

```sql
-- Add indexes for frequently queried columns
CREATE INDEX idx_events_slug ON events(slug);
CREATE INDEX idx_events_status ON events(status);
CREATE INDEX idx_student_registrations_event_id ON student_registrations(event_id);
CREATE INDEX idx_student_registrations_email ON student_registrations(email);
```

2. **Enable Query Caching**

Add Redis for caching:

```python
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
```

3. **Enable CDN**

Configure CloudFlare or AWS CloudFront for static assets.

---

## Security Best Practices

1. **Regular Updates**
```bash
# Update system packages
sudo apt update && sudo apt upgrade

# Update Python packages
pip list --outdated
pip install --upgrade <package>

# Update Node packages
pnpm update
```

2. **Security Scanning**
```bash
# Backend security audit
pip install safety
safety check

# Frontend security audit
pnpm audit
```

3. **Rate Limiting**

Add to `backend/app/main.py`:

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/api/v1/events")
@limiter.limit("100/minute")
async def list_events(request: Request):
    ...
```

---

## Support

For deployment issues:
- DevOps Team: devops@strideahead.in
- Backend Team: backend@strideahead.in
- Emergency: +91-XXXX-XXXXXX

---

**Last Updated:** November 9, 2025  
**Version:** 1.0
