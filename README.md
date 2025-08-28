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

## Current Status ✅

### Completed Features
- **Backend**: Django REST API with JWT authentication
- **Frontend**: React TypeScript app with Vite
- **Database**: PostgreSQL with proper models and migrations
- **Authentication**: User registration, login, and JWT tokens
- **API Endpoints**: Items CRUD operations with authentication
- **Admin Interface**: Django admin accessible and functional
- **Docker**: Full containerized environment working

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

1. Create a feature branch: `git checkout -b feature/new-feature`
2. Make your changes and test thoroughly
3. Commit with descriptive messages: `git commit -m "Add new feature"`
4. Push to your branch: `git push origin feature/new-feature`
5. Create a pull request with detailed description

## Support

- **Backend Issues**: Check Django logs with `docker-compose logs backend`
- **Frontend Issues**: Check React logs with `docker-compose logs frontend`
- **Database Issues**: Check PostgreSQL logs with `docker-compose logs db`
- **General Issues**: Check all logs with `docker-compose logs`

---

**Happy coding! 🚀✨**
