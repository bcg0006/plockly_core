#!/bin/bash

echo "🚀 Starting Plockly v2 Development Environment..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if ports are available
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "❌ Port $1 is already in use. Please free up port $1 and try again."
        exit 1
    fi
}

echo "🔍 Checking port availability..."
check_port 3000
check_port 8000
check_port 5432
check_port 6379

echo "✅ Ports are available"

# Build and start services
echo "🐳 Building and starting Docker services..."
docker-compose up --build -d

echo "⏳ Waiting for services to start..."
sleep 10

# Check service status
echo "📊 Service Status:"
docker-compose ps

echo ""
echo "🎉 Development environment is ready!"
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000/api/"
echo "⚙️  Django Admin: http://localhost:8000/admin/"
echo ""
echo "📝 Useful commands:"
echo "  View logs: docker-compose logs -f [service_name]"
echo "  Stop services: docker-compose down"
echo "  Rebuild: docker-compose up --build"
echo ""
echo "Happy coding! 🚀"
