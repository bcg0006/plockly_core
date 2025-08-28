# Environment Setup Guide for Plockly v2

This guide will walk you through setting up staging and production environments for your Django + React application.

## 🚀 Quick Start

### 1. Run the Setup Script
```bash
# From the project root directory
./deploy/setup-env.sh
```

This script will:
- Create `.env.staging` and `.env.production` files
- Generate secure SECRET_KEYs for each environment
- Provide guidance on GitHub secrets setup
- Validate your environment configuration

## 📋 Environment Configuration

### Staging Environment (`.env.staging`)

**Purpose**: Pre-production testing environment
**URL**: `staging.plockly.com` (example)
**Database**: Staging PostgreSQL instance
**Security**: Development-level security settings

**Key Variables**:
```bash
# Django Settings
DEBUG=False
SECRET_KEY=auto-generated-secure-key
ALLOWED_HOSTS=staging.plockly.com,localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://staging_user:staging_password@staging-db:5432/plockly_staging
POSTGRES_DB=plockly_staging
POSTGRES_USER=staging_user
POSTGRES_PASSWORD=staging_password

# Security (Staging)
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

### Production Environment (`.env.production`)

**Purpose**: Live application environment
**URL**: `plockly.com` (example)
**Database**: Production PostgreSQL cluster
**Security**: Production-level security settings

**Key Variables**:
```bash
# Django Settings
DEBUG=False
SECRET_KEY=auto-generated-secure-key
ALLOWED_HOSTS=plockly.com,www.plockly.com,api.plockly.com

# Database
DATABASE_URL=postgresql://prod_user:prod_password@prod-db:5432/plockly_production
POSTGRES_DB=plockly_production
POSTGRES_USER=prod_user
POSTGRES_PASSWORD=prod_password

# Security (Production)
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
```

## 🔐 GitHub Repository Secrets

### Required Secrets

Navigate to: `https://github.com/bcg0006/plockly_core/settings/secrets/actions`

#### Staging Secrets:
```
STAGING_SECRET_KEY: [auto-generated]
STAGING_DATABASE_URL: postgresql://staging_user:staging_password@staging-db:5432/plockly_staging
STAGING_ALLOWED_HOSTS: staging.plockly.com,localhost,127.0.0.1
```

#### Production Secrets:
```
PRODUCTION_SECRET_KEY: [auto-generated]
PRODUCTION_DATABASE_URL: postgresql://prod_user:prod_password@prod-db:5432/plockly_production
PRODUCTION_ALLOWED_HOSTS: plockly.com,www.plockly.com,api.plockly.com
```

#### Optional Secrets:
```
SENTRY_DSN: [your-sentry-dsn]
GOOGLE_ANALYTICS_ID: [your-ga-id]
EMAIL_HOST_USER: [your-email]
EMAIL_HOST_PASSWORD: [your-app-password]
```

## 🐳 Docker Environment Setup

### Staging Docker Compose
```bash
# Copy staging environment file
cp deploy/.env.staging .env

# Start staging services
docker-compose -f deploy/docker-compose.prod.yml up -d
```

### Production Docker Compose
```bash
# Copy production environment file
cp deploy/.env.production .env

# Start production services
docker-compose -f deploy/docker-compose.prod.yml up -d
```

## 🗄️ Database Setup

### Staging Database
```sql
-- Connect to staging PostgreSQL
CREATE DATABASE plockly_staging;
CREATE USER staging_user WITH PASSWORD 'staging_password';
GRANT ALL PRIVILEGES ON DATABASE plockly_staging TO staging_user;
```

### Production Database
```sql
-- Connect to production PostgreSQL
CREATE DATABASE plockly_production;
CREATE USER prod_user WITH PASSWORD 'prod_password';
GRANT ALL PRIVILEGES ON DATABASE plockly_production TO prod_user;
```

### Apply Migrations
```bash
# Staging
docker-compose -f deploy/docker-compose.prod.yml exec backend python manage.py migrate

# Production
docker-compose -f deploy/docker-compose.prod.yml exec backend python manage.py migrate
```

## 🔒 Security Configuration

### SSL/HTTPS Setup

#### Staging (Optional):
```bash
# Self-signed certificate for testing
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout staging.key -out staging.crt \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=staging.plockly.com"
```

#### Production (Required):
```bash
# Let's Encrypt certificate
certbot certonly --standalone -d plockly.com -d www.plockly.com
```

### Firewall Configuration
```bash
# Allow only necessary ports
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw allow 5432/tcp  # PostgreSQL (if external)
ufw enable
```

## 📊 Monitoring & Logging

### Health Check Endpoints
- **Backend**: `http://your-domain:8000/health/`
- **Frontend**: `http://your-domain/health`
- **Database**: PostgreSQL connection test
- **Redis**: Redis connection test

### Log Files
```bash
# Application logs
tail -f /app/logs/staging.log
tail -f /app/logs/production.log

# Docker logs
docker-compose -f deploy/docker-compose.prod.yml logs -f backend
docker-compose -f deploy/docker-compose.prod.yml logs -f frontend
```

### Monitoring Tools
- **Sentry**: Error tracking and performance monitoring
- **Prometheus**: Metrics collection
- **Grafana**: Visualization and alerting
- **Uptime Robot**: External monitoring

## 🚀 Deployment Process

### Staging Deployment (Automatic)
1. Push to `main` branch
2. GitHub Actions runs full pipeline
3. Automatic deployment to staging
4. Health checks verify deployment

### Production Deployment (Manual)
1. Go to GitHub Actions
2. Select "Deploy to Production"
3. Click "Run workflow"
4. Approve deployment
5. Monitor deployment logs

### Rollback Process
```bash
# Rollback to previous version
git checkout HEAD~1
git push origin main --force

# Or manually rollback Docker images
docker-compose -f deploy/docker-compose.prod.yml down
docker-compose -f deploy/docker-compose.prod.yml up -d
```

## 🔧 Environment-Specific Settings

### Django Settings Override
The `settings_env.py` file automatically configures:
- Database connections
- Security settings
- Logging levels
- CORS origins
- Cache configurations

### Frontend Environment Variables
```bash
# Create .env files in frontend directory
REACT_APP_API_URL=https://api.plockly.com
REACT_APP_ENVIRONMENT=production
REACT_APP_SENTRY_DSN=your-sentry-dsn
```

## 📝 Environment Checklist

### Staging Environment:
- [ ] Environment file created (`.env.staging`)
- [ ] Database created and configured
- [ ] GitHub secrets added
- [ ] SSL certificate (optional)
- [ ] Health checks working
- [ ] Monitoring configured

### Production Environment:
- [ ] Environment file created (`.env.production`)
- [ ] Database created and configured
- [ ] GitHub secrets added
- [ ] SSL certificate installed
- [ ] Firewall configured
- [ ] Health checks working
- [ ] Monitoring configured
- [ ] Backup strategy implemented

## 🆘 Troubleshooting

### Common Issues:

#### 1. Database Connection Failed
```bash
# Check database status
docker-compose -f deploy/docker-compose.prod.yml logs db

# Test connection
docker-compose -f deploy/docker-compose.prod.yml exec backend python manage.py dbshell
```

#### 2. Environment Variables Not Loading
```bash
# Verify .env file exists
ls -la deploy/.env.*

# Check variable loading
docker-compose -f deploy/docker-compose.prod.yml exec backend env | grep DATABASE
```

#### 3. SSL Certificate Issues
```bash
# Check certificate validity
openssl x509 -in /etc/letsencrypt/live/plockly.com/fullchain.pem -text -noout

# Renew certificate
certbot renew
```

## 📚 Additional Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)
- [Docker Production Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [PostgreSQL Security](https://www.postgresql.org/docs/current/security.html)
- [Nginx Configuration](https://nginx.org/en/docs/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)

---

**Need Help?** Check the main README.md or create an issue in the GitHub repository.
