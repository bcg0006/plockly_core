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
- **Container**: Docker with Node.js 18

## Quick Start with Docker

### Prerequisites
- Docker and Docker Compose installed
- Ports 3000, 8000, 5432, and 6379 available

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

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/
- **Django Admin**: http://localhost:8000/admin/
- **Database**: localhost:5432
- **Redis**: localhost:6379

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

## Next Steps

1. Configure Django settings for your needs
2. Create models in the Django apps
3. Set up serializers and views
4. Configure API endpoints
5. Build React components
6. Set up Redux store
7. Implement authentication flow
8. Add environment variables for production
