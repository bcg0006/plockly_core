# 🚀 Quick Reference Guide - Plockly v2

## **⚡ Essential Commands**

### **🔄 Pre-commit Hooks**
```bash
# Install pre-commit hooks
pre-commit install

# Run all hooks manually
pre-commit run --all-files

# Run specific hook
pre-commit run black --all-files
pre-commit run isort --all-files
pre-commit run flake8 --all-files
```

### **🐍 Backend Development**
```bash
cd backend

# Virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Database
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# Development server
python manage.py runserver

# Quality checks
./format.sh
python manage.py test
```

### **⚛️ Frontend Development**
```bash
cd frontend

# Install dependencies
npm install

# Development server
npm run dev

# Quality checks
npm run lint
npm run test
npm run test:coverage
npm run build
```

### **🐳 Docker Development**
```bash
# Start all services
./start.sh

# Start specific services
docker-compose up backend
docker-compose up frontend

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop services
docker-compose down
```

---

## **🔍 Quality Check Commands**

### **Backend Quality**
```bash
cd backend

# Format code
black .
isort .

# Lint code
flake8 .

# Run all quality checks
./format.sh

# Test with coverage
python manage.py test --coverage
```

### **Frontend Quality**
```bash
cd frontend

# Lint code
npm run lint

# Run tests
npm run test
npm run test:watch
npm run test:coverage

# Type check
npx tsc --noEmit
```

---

## **🧪 Testing Commands**

### **Backend Tests**
```bash
cd backend

# Run all tests
python manage.py test

# Run specific app tests
python manage.py test users
python manage.py test api

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### **Frontend Tests**
```bash
cd frontend

# Run all tests
npm run test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage

# Run tests in CI mode
npm run test:ci
```

---

## **🚀 Deployment Commands**

### **Environment Setup**
```bash
# Generate environment files
cd deploy
./setup-env.sh

# View environment variables
cat .env.staging
cat .env.production
```

### **Production Build**
```bash
# Backend production
cd backend
docker build -t plockly-backend:latest .

# Frontend production
cd frontend
npm run build
docker build -f Dockerfile.prod -t plockly-frontend:latest .
```

---

## **📊 Monitoring Commands**

### **Health Checks**
```bash
# Backend health
curl http://localhost:8000/health/

# Frontend health
curl http://localhost:5173/health

# Database health
docker-compose exec db pg_isready -U postgres

# Redis health
docker-compose exec redis redis-cli ping
```

### **Logs**
```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
docker-compose logs -f redis
```

---

## **🔧 Troubleshooting Commands**

### **Common Issues**
```bash
# Reset database
cd backend
python manage.py flush
python manage.py migrate

# Clear cache
docker-compose exec redis redis-cli flushall

# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up

# Check port conflicts
lsof -i :8000
lsof -i :5173
lsof -i :5432
lsof -i :6379
```

### **Dependency Issues**
```bash
# Backend dependencies
cd backend
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall

# Frontend dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

## **📚 Git Workflow**

### **Branch Management**
```bash
# Create feature branch
git checkout -b feature/new-feature

# Create bugfix branch
git checkout -b bugfix/fix-description

# Create hotfix branch
git checkout -b hotfix/urgent-fix

# Switch branches
git checkout main
git checkout develop
```

### **Commit & Push**
```bash
# Stage changes
git add .

# Commit with conventional format
git commit -m "feat: add new user authentication system"
git commit -m "fix: resolve login validation issue"
git commit -m "docs: update API documentation"
git commit -m "test: add unit tests for user model"

# Push to remote
git push origin feature/new-feature
```

### **Pull Request Process**
```bash
# Update branch with latest changes
git checkout develop
git pull origin develop
git checkout feature/new-feature
git merge develop

# Push updated branch
git push origin feature/new-feature
```

---

## **🎯 IDE Configuration**

### **VS Code Settings**
```json
{
  "python.defaultInterpreterPath": "./backend/venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  }
}
```

### **VS Code Extensions**
- Python (Microsoft)
- Black Formatter
- isort
- Flake8
- TypeScript and JavaScript Language Features
- Prettier
- Tailwind CSS IntelliSense
- GitLens

---

## **📱 Mobile Development**

### **React Native Commands**
```bash
cd mobile

# Install dependencies
npm install

# iOS development
npx react-native run-ios

# Android development
npx react-native run-android

# Metro bundler
npx react-native start
```

---

## **🔐 Security Commands**

### **Secret Management**
```bash
# Generate new secret key
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Check for secrets in code
detect-secrets scan --baseline .secrets.baseline

# Update secrets baseline
detect-secrets scan --baseline .secrets.baseline --update .secrets.baseline
```

### **Security Scanning**
```bash
# Backend security scan
cd backend
bandit -r . -f json -o bandit-report.json

# Frontend security scan
cd frontend
npm audit
npm audit fix
```

---

## **📈 Performance Commands**

### **Backend Performance**
```bash
cd backend

# Database query analysis
python manage.py shell
from django.db import connection
# Run your queries here
print(connection.queries)

# Memory profiling
pip install memory-profiler
python -m memory_profiler manage.py shell
```

### **Frontend Performance**
```bash
cd frontend

# Bundle analysis
npm run build
npx webpack-bundle-analyzer dist/stats.json

# Lighthouse audit
npx lighthouse http://localhost:5173 --output html --output-path ./lighthouse-report.html
```

---

## **🚨 Emergency Commands**

### **Rollback Deployment**
```bash
# Rollback to previous version
git checkout HEAD~1
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d

# Restore database backup
docker-compose exec db pg_restore -U postgres -d plockly_db backup.sql
```

### **Service Recovery**
```bash
# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart backend
docker-compose restart frontend

# Check service status
docker-compose ps
```

---

**💡 Pro Tip**: Bookmark this page for quick access during development! 🚀
