# Plockly v2 - Full Stack App

A modern full-stack application with Django backend and React frontend, containerized with Docker.

## Project Structure

```
plockly_v2/
├── backend/           # Django Python backend
│   ├── backend/      # Django project settings
│   ├── api/          # API Django app
│   ├── users/        # Users Django app
│   ├── Dockerfile    # Backend container
│   └── manage.py     # Django management script
├── frontend/          # React TypeScript frontend
│   ├── src/          # Source code
│   ├── public/       # Public assets
│   ├── Dockerfile    # Frontend container
│   └── package.json  # Node dependencies
├── deploy/            # Production deployment files
├── .github/           # GitHub Actions CI/CD
├── docker-compose.yml # Multi-container setup
└── README.md         # This file
```

## Backend (Django)

- **Framework**: Django 5.2+
- **Language**: Python 3.11+
- **Database**: PostgreSQL 15
- **Authentication**: Django REST Framework JWT
- **API**: RESTful API with Django REST Framework
- **Admin**: Django Admin interface
- **Container**: Docker with Python 3.11-slim

## Frontend (React)

- **Framework**: React 18+
- **Language**: TypeScript
- **Build Tool**: Vite
- **State Management**: Redux Toolkit
- **UI Components**: Material-UI
- **Routing**: React Router
- **HTTP Client**: Axios
- **Container**: Docker with Node.js 20

## Quick Start with Docker

### Prerequisites
- Docker and Docker Compose installed
- Ports 3001, 8000, 5433, and 6380 available

### Start All Services
```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

### Individual Services
```bash
# Start only database
docker-compose up db

# Start backend
docker-compose up backend

# Start frontend
docker-compose up frontend
```

### Stop Services
```bash
docker-compose down
```

## Development Without Docker

### Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Features

- **Containerized**: Full Docker setup with PostgreSQL and Redis
- **RESTful API**: Django REST Framework with JWT authentication
- **Modern Frontend**: React with TypeScript and Material-UI
- **Database**: PostgreSQL for production-ready data storage
- **Caching**: Redis for session management and caching
- **Admin Interface**: Django admin for data management
- **Type Safety**: TypeScript for frontend development
- **Hot Reload**: Fast development with Vite

## Development URLs

- **Frontend**: http://localhost:3001
- **Backend API**: http://localhost:8000/api/
- **Django Admin**: http://localhost:8000/admin/
- **Database**: localhost:5433
- **Redis**: localhost:6380

## Docker Commands

```bash
# View logs
docker-compose logs -f [service_name]

# Execute commands in container
docker-compose exec backend python manage.py shell
docker-compose exec frontend npm run build

# Rebuild specific service
docker-compose build backend

# Clean up
docker-compose down -v  # Remove volumes
docker system prune     # Clean unused images
```

## CI/CD Pipeline 🚀

### GitHub Actions Workflow

Our project includes a comprehensive CI/CD pipeline that runs automatically on every push and pull request.

#### **Pipeline Stages:**

1. **Backend Testing** 🐍
   - Python 3.11 setup
   - Dependency installation with caching
   - Code linting (Black, isort, flake8)
   - Django tests with coverage
   - PostgreSQL & Redis service containers

2. **Frontend Testing** ⚛️
   - Node.js 20 setup
   - NPM dependency caching
   - ESLint code quality checks
   - Jest unit tests with coverage
   - Production build verification

3. **Docker Build Testing** 🐳
   - Multi-stage Docker builds
   - Container health checks
   - Image size optimization
   - Build artifact validation

4. **Security Scanning** 🔒
   - Trivy vulnerability scanning
   - Dependency security analysis
   - GitHub Security tab integration
   - CVE detection and reporting

5. **Deployment** 🚀
   - **Staging**: Automatic deployment on main branch
   - **Production**: Manual deployment with approval
   - Environment-specific configurations
   - Health check monitoring

#### **Pipeline Triggers:**

- **Push to main**: Full pipeline + staging deployment
- **Push to develop**: Full pipeline (no deployment)
- **Pull Request**: Full pipeline (no deployment)
- **Manual**: Production deployment trigger

#### **Quality Gates:**

- ✅ **Code Coverage**: Minimum 70% required
- ✅ **Linting**: Black, isort, flake8 must pass
- ✅ **Tests**: All Django and React tests must pass
- ✅ **Security**: No critical vulnerabilities
- ✅ **Build**: Docker images must build successfully

### Local Development Quality Tools

#### **Backend (Python):**

```bash
# Code formatting
cd backend
black .                    # Auto-format code
isort .                    # Sort imports
flake8 .                   # Lint code

# Testing
pytest                     # Run all tests
pytest --cov=.            # Run with coverage
pytest -m "not slow"      # Skip slow tests
```

#### **Frontend (React):**

```bash
# Code quality
cd frontend
npm run lint               # ESLint checks
npm run lint:fix           # Auto-fix issues

# Testing
npm test                   # Run tests
npm run test:coverage      # Coverage report
npm run build              # Production build
```

### Deployment Environments

#### **Staging Environment:**
- **Auto-deploy**: On every push to main branch
- **Purpose**: Pre-production testing
- **URL**: `staging.plockly.com` (example)
- **Database**: Staging PostgreSQL instance
- **Monitoring**: Basic health checks

#### **Production Environment:**
- **Manual deploy**: Requires approval
- **Purpose**: Live application
- **URL**: `plockly.com` (example)
- **Database**: Production PostgreSQL cluster
- **Monitoring**: Full observability stack

### Environment Variables

Create `.env` files for each environment:

```bash
# .env.staging
DEBUG=False
SECRET_KEY=your-staging-secret-key
DATABASE_URL=postgresql://user:pass@staging-db:5432/plockly
ALLOWED_HOSTS=staging.plockly.com

# .env.production
DEBUG=False
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://user:pass@prod-db:5432/plockly
ALLOWED_HOSTS=plockly.com
```

### Monitoring & Observability

- **Health Checks**: `/health` endpoints for all services
- **Logging**: Structured logging with correlation IDs
- **Metrics**: Prometheus metrics collection
- **Tracing**: Distributed tracing with OpenTelemetry
- **Alerts**: Slack/email notifications on failures

## Current Status ✅

### Completed Features
- **Backend**: Django REST API with JWT authentication
- **Frontend**: React TypeScript app with Vite
- **Database**: PostgreSQL with proper models and migrations
- **Authentication**: User registration, login, and JWT tokens
- **API Endpoints**: Items CRUD operations with authentication
- **Admin Interface**: Django admin accessible and functional
- **Docker**: Full containerized environment working
- **CI/CD**: Complete GitHub Actions pipeline
- **Security**: Enhanced JWT with token rotation

### Database Setup
- **Migrations**: Applied successfully
- **Superuser**: Created and ready
- **Models**: Item model with proper relationships
- **Authentication**: User model and JWT system working

## Next Development Steps 🚀

### Phase 1: Frontend Authentication (Week 1)
1. **Create Authentication Components**
   - Login form with Material-UI
   - Registration form with validation
   - Password reset functionality
   - JWT token storage and management

2. **Implement State Management**
   - Set up Redux store for authentication
   - Create auth slices and actions
   - Implement token refresh logic
   - Add protected route components

3. **Build Navigation & Layout**
   - Responsive navigation bar
   - Sidebar/drawer for mobile
   - User profile dropdown
   - Route protection middleware

### Phase 2: Core Application Features (Week 2)
1. **Item Management Interface**
   - Create item form
   - Item list with search and filtering
   - Item detail view
   - Edit and delete functionality

2. **User Dashboard**
   - User profile management
   - User's items overview
   - Activity history
   - Settings and preferences

3. **API Integration**
   - Connect frontend to Django API
   - Implement error handling
   - Add loading states
   - Handle API responses

### Phase 3: Advanced Features (Week 3)
1. **Enhanced UI/UX**
   - Responsive design improvements
   - Dark/light theme toggle
   - Animations and transitions
   - Mobile-first design

2. **Additional API Endpoints**
   - File upload functionality
   - Search and filtering
   - Pagination
   - Real-time updates

3. **Testing & Quality**
   - Unit tests for components
   - API endpoint testing
   - E2E testing setup
   - Code quality tools

### Phase 4: Production Ready (Week 4)
1. **Performance Optimization**
   - Code splitting and lazy loading
   - Image optimization
   - Caching strategies
   - Bundle size optimization

2. **Security & Deployment**
   - Environment variables
   - Production Docker setup
   - SSL/HTTPS configuration
   - CI/CD pipeline setup

3. **Documentation & Monitoring**
   - API documentation
   - User guides
   - Error monitoring
   - Performance analytics

## Getting Started with Development

### 1. Set Up Development Environment
```bash
# Clone the repository
git clone https://github.com/bcg0006/plockly_core.git
cd plockly_core

# Start the application
./start.sh
```

### 2. Access Development Tools
- **Frontend**: http://localhost:3001
- **Backend API**: http://localhost:8000/api/
- **Admin**: http://localhost:8000/admin/
- **Database**: localhost:5433

### 3. Start Building Features
- Begin with authentication components
- Implement Redux store setup
- Create basic UI components
- Connect to Django API endpoints

## Contributing

### Development Workflow

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/new-feature
   ```

2. **Make Changes & Test**
   ```bash
   # Backend
   cd backend
   black . && isort . && flake8 .
   pytest

   # Frontend
   cd frontend
   npm run lint
   npm test
   npm run build
   ```

3. **Commit with Standards**
   ```bash
   git add .
   git commit -m "feat: add new authentication component"
   ```

4. **Push & Create PR**
   ```bash
   git push origin feature/new-feature
   # Create Pull Request on GitHub
   ```

### Code Quality Standards

- **Python**: Black formatting, isort imports, flake8 linting
- **TypeScript**: ESLint rules, Prettier formatting
- **Tests**: Minimum 70% coverage required
- **Commits**: Conventional commit format
- **PRs**: Must pass all CI checks

## Support

- **Backend Issues**: Check Django logs with `docker-compose logs backend`
- **Frontend Issues**: Check React logs with `docker-compose logs frontend`
- **Database Issues**: Check PostgreSQL logs with `docker-compose logs db`
- **General Issues**: Check all logs with `docker-compose logs`
- **CI/CD Issues**: Check GitHub Actions tab in repository

## Deployment

### Production Deployment

1. **Prepare Release**
   ```bash
   git checkout main
   git pull origin main
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **Trigger Deployment**
   - Go to GitHub Actions
   - Select "Deploy to Production"
   - Click "Run workflow"
   - Approve deployment

3. **Monitor Deployment**
   - Watch GitHub Actions logs
   - Check health endpoints
   - Verify all services running

---

**Happy coding! 🚀✨**
